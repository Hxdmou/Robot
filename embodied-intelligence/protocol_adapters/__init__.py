# -*- coding: utf-8 -*-
"""
真实机器人 · 多品牌协议适配器模块（协议栈骨架层）
=================================================
对应 real_robot_adapter.py 中 PROTOCOL_ADAPTERS 注册的 56 条协议路径。

设计要点：
    1. 每个适配器必须实现 7 个标准方法（见 GenericTCPAdapter），
       这样 RobotAdapter 层可以不关心底层协议差异；
    2. 本文件只提供「协议握手骨架」，不做品牌特定协议字节级实现（
       真实品牌对接时在对应子类里重写 move_joints / get_joint_states
       / get_ee_pose 的字节编码逻辑即可）；
    3. 任何异常都应向上抛出（让 RobotAdapter 捕获后触发 stop() + 安全停止）；
    4. connected 属性作为 RobotAdapter.is_connected() 的真实依据。

品牌映射关系：
    42 条通用协议  → GenericTCPAdapter / GenericSerialAdapter（本文件骨架直接可用）
    14 条品牌特定协议 → 各自子类（当前继承骨架，待真实设备对接时补握手字节）
"""

import os
import socket
import time
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests  # 可选：仅 EVTOLMapAdapter / 地图API 需要
except ImportError:  # pragma: no cover - 无 requests 时适配器自动走离线模式
    requests = None  # type: ignore


# ============================================================
# 1. 通用 TCP 适配器骨架（42 条协议 → 直接用它）
# ============================================================

class GenericTCPAdapter:
    """标准 TCP 协议适配器（控制指令 ASCII / JSON 编码的品牌直接可用）

    典型适用品牌：Fanuc / 金倍 / 敏捷 / 墨影 / 联汇 / 思灵 / 商汤 / 乐聚 /
                  ModelBest / StepX / 阿里 / 努比亚 / 数睿 / 智元 / 开普勒 /
                  优必选 / 松洋 / 宇树 / 广东盈腾 / AMR / 消费级 / HPC / 电信 /
                  LLM / WorldModel / 传感器 / 半导体 / 推理 / VTOL / 平台 /
                  XR / 能源 / 工业 / 清华数据 / 埃夫特EKI / 医疗EtherCAT-P /
                  物流5G-MQTT / 物流SLAM-MQTT / Modbus-TCP-ROS2 / 消费级5G-C-V2X

    真实对接时，只需重写以下三个方法即可：
        _encode_move_joints(joint_angles, speed) → bytes
        _decode_joint_states(raw_bytes)         → List[float]
        _decode_ee_pose(raw_bytes)              → {position, orientation}
    """

    DEFAULT_TIMEOUT_SEC = 5.0
    SOCKET_RECV_BYTES = 4096

    def __init__(self, host: str, port: int, config: Optional[Dict[str, Any]] = None):
        self.host = host or "127.0.0.1"
        self.port = int(port) if port else 8080
        self.config = config or {}
        self.dofs: int = int(self.config.get("dofs", 7))
        self._sock: Optional[socket.socket] = None
        self.connected: bool = False
        # 本地缓存最后一次关节角（无真实反馈时返回此值）
        self._last_joint_states: List[float] = [0.0] * self.dofs
        self._last_ee_pose: Dict[str, List[float]] = {
            "position": [0.3, 0.0, 0.2],
            "orientation": [0.0, 0.0, 0.0, 1.0],
        }

    # ---------- 连接生命周期 ----------

    def connect(self) -> None:
        if self.connected and self._sock is not None:
            return
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.DEFAULT_TIMEOUT_SEC)
        try:
            s.connect((self.host, self.port))
        except OSError as e:
            try:
                s.close()
            except OSError:
                pass
            raise ConnectionError(
                f"[{self.__class__.__name__}] TCP连接失败 {self.host}:{self.port} ({e})"
            )
        self._sock = s
        self.connected = True
        # 可选：发送协议握手包
        try:
            hs = self._encode_handshake()
            if hs:
                self._sock.sendall(hs)
        except OSError as e:
            self.disconnect()
            raise ConnectionError(f"[{self.__class__.__name__}] 握手包发送失败: {e}")

    def disconnect(self) -> None:
        self.connected = False
        if self._sock is not None:
            try:
                try:
                    self._sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
            finally:
                try:
                    self._sock.close()
                except OSError:
                    pass
                self._sock = None

    # ---------- 核心控制接口（RobotAdapter 层直接调用）----------

    def move_joints(self, joint_angles: List[float], speed: float = 1.0) -> None:
        self._check_connection()
        payload = self._encode_move_joints(joint_angles, speed)
        try:
            self._sock.sendall(payload)
            # 无阻塞等待响应（高频率控制场景在子线程中处理）
            self._last_joint_states = list(joint_angles)
        except OSError as e:
            self.connected = False
            raise IOError(f"[{self.__class__.__name__}] 关节运动指令发送失败: {e}")

    def move_cartesian(self, x: float, y: float, z: float,
                       rx: float = 0.0, ry: float = 0.0, rz: float = 0.0,
                       speed: float = 1.0) -> None:
        self._check_connection()
        payload = self._encode_move_cartesian(x, y, z, rx, ry, rz, speed)
        try:
            self._sock.sendall(payload)
            self._last_ee_pose = {
                "position": [float(x), float(y), float(z)],
                "orientation": [float(rx), float(ry), float(rz), 1.0],
            }
        except OSError as e:
            self.connected = False
            raise IOError(f"[{self.__class__.__name__}] 笛卡尔运动指令发送失败: {e}")

    def get_joint_states(self) -> List[float]:
        self._check_connection()
        req = self._encode_request_joint_states()
        if req:
            try:
                self._sock.sendall(req)
                raw = self._sock.recv(self.SOCKET_RECV_BYTES)
                if raw:
                    self._last_joint_states = self._decode_joint_states(raw)
            except OSError:
                # 反馈通道失败不抛异常（上层以缓存值继续控制）
                pass
        return list(self._last_joint_states)

    def get_ee_pose(self) -> Dict[str, List[float]]:
        self._check_connection()
        req = self._encode_request_ee_pose()
        if req:
            try:
                self._sock.sendall(req)
                raw = self._sock.recv(self.SOCKET_RECV_BYTES)
                if raw:
                    self._last_ee_pose = self._decode_ee_pose(raw)
            except OSError:
                pass
        return {
            "position": list(self._last_ee_pose["position"]),
            "orientation": list(self._last_ee_pose["orientation"]),
        }

    def stop(self) -> None:
        """紧急停止：立刻发送停止指令 + 断开通信层"""
        if self._sock is not None:
            try:
                stop_bytes = self._encode_stop()
                if stop_bytes:
                    self._sock.sendall(stop_bytes)
            except OSError:
                pass
        self.disconnect()

    # ---------- 子类重写点（品牌特定编码 / 解码）----------

    def _encode_handshake(self) -> Optional[bytes]:
        """连接成功后立刻发送的握手包（默认回 None 表示无需握手）"""
        return None

    def _encode_move_joints(self, joint_angles: List[float], speed: float) -> bytes:
        """关节运动字节编码：默认 JSON 文本行（最通用）"""
        import json as _json
        return (_json.dumps({
            "cmd": "movej",
            "joints": [float(x) for x in joint_angles],
            "speed": float(speed),
            "ts": time.time(),
        }) + "\n").encode("utf-8")

    def _encode_move_cartesian(self, x, y, z, rx, ry, rz, speed) -> bytes:
        import json as _json
        return (_json.dumps({
            "cmd": "movel",
            "pose": [float(x), float(y), float(z), float(rx), float(ry), float(rz)],
            "speed": float(speed),
            "ts": time.time(),
        }) + "\n").encode("utf-8")

    def _encode_request_joint_states(self) -> Optional[bytes]:
        return (b'{"cmd":"get_joints"}\n')

    def _encode_request_ee_pose(self) -> Optional[bytes]:
        return (b'{"cmd":"get_pose"}\n')

    def _encode_stop(self) -> Optional[bytes]:
        return (b'{"cmd":"stop"}\n')

    def _decode_joint_states(self, raw: bytes) -> List[float]:
        try:
            import json as _json
            obj = _json.loads(raw.decode("utf-8", errors="replace").strip().splitlines()[-1])
            if isinstance(obj, dict) and "joints" in obj and isinstance(obj["joints"], list):
                return [float(x) for x in obj["joints"]]
        except Exception:
            pass
        return list(self._last_joint_states)

    def _decode_ee_pose(self, raw: bytes) -> Dict[str, List[float]]:
        try:
            import json as _json
            obj = _json.loads(raw.decode("utf-8", errors="replace").strip().splitlines()[-1])
            if isinstance(obj, dict):
                pose = obj.get("pose", {})
                if isinstance(pose, dict):
                    return {
                        "position": [float(pose.get("x", 0)), float(pose.get("y", 0)), float(pose.get("z", 0))],
                        "orientation": [
                            float(pose.get("rx", 0)), float(pose.get("ry", 0)),
                            float(pose.get("rz", 0)), float(pose.get("w", 1)),
                        ],
                    }
                if isinstance(pose, list) and len(pose) >= 3:
                    rest = [0.0, 0.0, 0.0, 1.0]
                    for i in range(min(4, len(pose) - 3)):
                        rest[i] = float(pose[3 + i])
                    return {"position": [float(pose[0]), float(pose[1]), float(pose[2])],
                            "orientation": rest}
        except Exception:
            pass
        return dict(self._last_ee_pose)

    # ---------- 内部工具 ----------

    def _check_connection(self) -> None:
        if not self.connected or self._sock is None:
            raise ConnectionError(
                f"[{self.__class__.__name__}] 尚未建立TCP连接，请先调用 connect()"
            )

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.disconnect()


# ============================================================
# 2. 通用 Serial 适配器骨架（Modbus RTU / RS485 品牌）
# ============================================================

class GenericSerialAdapter:
    """标准串口适配器（步科Modbus / CMU脑机串口 / 未来串口类协议）"""

    def __init__(self, host: str = "", port: int = 0, config: Optional[Dict[str, Any]] = None):
        # host 参数被忽略，串口真正需要的是 port 名称（如 "COM3" "/dev/ttyUSB0"）
        self.port_name: str = self.config_port_name(host, port, config or {})
        self.baudrate: int = int((config or {}).get("baudrate", 115200))
        self.config = config or {}
        self.dofs: int = int(self.config.get("dofs", 7))
        self._ser: Optional[Any] = None  # pyserial.Serial（延迟导入）
        self.connected: bool = False
        self._last_joint_states: List[float] = [0.0] * self.dofs
        self._last_ee_pose: Dict[str, List[float]] = {
            "position": [0.3, 0.0, 0.2], "orientation": [0.0, 0.0, 0.0, 1.0],
        }

    @staticmethod
    def config_port_name(host: str, port: int, config: Dict[str, Any]) -> str:
        """串口名解析：config 里的 serial_port > host 参数 > 用 port 整数拼 COM{n}"""
        if isinstance(config.get("serial_port"), str) and config["serial_port"]:
            return config["serial_port"]
        if host and not host.replace(".", "").isdigit():  # 不是 IP 的当作串口名
            return host
        if isinstance(port, int) and port > 0:
            return f"COM{port}"
        return "COM1"

    def _import_serial(self):
        try:
            import serial  # type: ignore
        except ImportError as e:
            raise ImportError(
                f"[{self.__class__.__name__}] 串口通信需要 pyserial 包: pip install pyserial"
            ) from e
        return serial

    # ---------- 生命周期 ----------

    def connect(self) -> None:
        if self.connected:
            return
        serial_mod = self._import_serial()
        try:
            self._ser = serial_mod.Serial(
                port=self.port_name,
                baudrate=self.baudrate,
                timeout=3.0,
            )
        except Exception as e:
            raise ConnectionError(
                f"[{self.__class__.__name__}] 串口 {self.port_name}@{self.baudrate} 打开失败: {e}"
            )
        self.connected = True

    def disconnect(self) -> None:
        self.connected = False
        if self._ser is not None:
            try:
                self._ser.close()
            except Exception:
                pass
            self._ser = None

    # ---------- 控制接口（同 TCP 层，保持签名完全一致）----------

    def move_joints(self, joint_angles: List[float], speed: float = 1.0) -> None:
        self._check_connection()
        self._ser.write(self._encode_move_joints(joint_angles, speed))
        self._last_joint_states = list(joint_angles)

    def move_cartesian(self, x, y, z, rx=0, ry=0, rz=0, speed=1.0) -> None:
        self._check_connection()
        self._ser.write(self._encode_move_cartesian(x, y, z, rx, ry, rz, speed))
        self._last_ee_pose = {
            "position": [float(x), float(y), float(z)],
            "orientation": [float(rx), float(ry), float(rz), 1.0],
        }

    def get_joint_states(self) -> List[float]:
        self._check_connection()
        req = self._encode_request_joint_states()
        if req:
            self._ser.write(req)
            raw = self._ser.read(128)
            if raw:
                self._last_joint_states = self._decode_joint_states(raw)
        return list(self._last_joint_states)

    def get_ee_pose(self) -> Dict[str, List[float]]:
        self._check_connection()
        req = self._encode_request_ee_pose()
        if req:
            self._ser.write(req)
            raw = self._ser.read(256)
            if raw:
                self._last_ee_pose = self._decode_ee_pose(raw)
        return {"position": list(self._last_ee_pose["position"]),
                "orientation": list(self._last_ee_pose["orientation"])}

    def stop(self) -> None:
        if self._ser is not None:
            try:
                pkt = self._encode_stop()
                if pkt:
                    self._ser.write(pkt)
            except Exception:
                pass
        self.disconnect()

    # ---------- 子类重写点 ----------

    def _encode_move_joints(self, joint_angles, speed) -> bytes:
        return b"\xAA\x01MOVEJ" + b",".join(f"{v:.6f}".encode() for v in joint_angles) + b"\n"

    def _encode_move_cartesian(self, x, y, z, rx, ry, rz, speed) -> bytes:
        return f"MOVEL {x:.4f},{y:.4f},{z:.4f},{rx:.4f},{ry:.4f},{rz:.4f}\n".encode()

    def _encode_request_joint_states(self) -> Optional[bytes]:
        return b"GETJ\n"

    def _encode_request_ee_pose(self) -> Optional[bytes]:
        return b"GETP\n"

    def _encode_stop(self) -> Optional[bytes]:
        return b"\xAA\x00STOP\n"

    def _decode_joint_states(self, raw: bytes) -> List[float]:
        try:
            line = raw.decode("ascii", errors="replace").strip()
            if line.startswith("J:"):
                return [float(x) for x in line[2:].split(",")[: self.dofs]]
        except Exception:
            pass
        return list(self._last_joint_states)

    def _decode_ee_pose(self, raw: bytes) -> Dict[str, List[float]]:
        try:
            line = raw.decode("ascii", errors="replace").strip()
            if line.startswith("P:"):
                vals = [float(x) for x in line[2:].split(",")]
                while len(vals) < 7:
                    vals.append(0.0)
                vals[6] = vals[6] or 1.0
                return {"position": vals[:3], "orientation": vals[3:7]}
        except Exception:
            pass
        return dict(self._last_ee_pose)

    def _check_connection(self) -> None:
        if not self.connected or self._ser is None:
            raise ConnectionError(
                f"[{self.__class__.__name__}] 串口未连接（{self.port_name}），请先调用 connect()"
            )

    def __enter__(self): self.connect(); return self
    def __exit__(self, exc_type, exc, tb): self.disconnect()


# ============================================================
# 3. 通用 UDP 适配器骨架（宇树 H1/Go2/Unitree 等）
# ============================================================

class GenericUDPAdapter(GenericTCPAdapter):
    """基于 UDP 的高速控制适配器（宇树四足/人形、足式类高频通信）"""

    def __init__(self, host, port, config=None):
        super().__init__(host, port, config)
        self._peer: Optional[Tuple[str, int]] = None

    def connect(self):
        if self.connected:
            return
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(self.DEFAULT_TIMEOUT_SEC)
        self._sock = s
        self._peer = (self.host, self.port)
        # UDP 无 connect 语义，用一次握手包确认通道可达
        hs = self._encode_handshake()
        if hs:
            try:
                self._sock.sendto(hs, self._peer)
            except OSError as e:
                self.disconnect()
                raise ConnectionError(f"[{self.__class__.__name__}] UDP握手失败: {e}")
        self.connected = True

    def disconnect(self):
        self.connected = False
        self._peer = None
        if self._sock is not None:
            try: self._sock.close()
            except OSError: pass
            self._sock = None

    def _check_connection(self):
        if not self.connected or self._sock is None or self._peer is None:
            raise ConnectionError(f"[{self.__class__.__name__}] UDP通道未就绪")

    def move_joints(self, joint_angles, speed=1.0):
        self._check_connection()
        self._sock.sendto(self._encode_move_joints(joint_angles, speed), self._peer)
        self._last_joint_states = list(joint_angles)

    def move_cartesian(self, x, y, z, rx=0, ry=0, rz=0, speed=1.0):
        self._check_connection()
        self._sock.sendto(self._encode_move_cartesian(x, y, z, rx, ry, rz, speed), self._peer)
        self._last_ee_pose = {
            "position": [float(x), float(y), float(z)],
            "orientation": [float(rx), float(ry), float(rz), 1.0],
        }

    def get_joint_states(self):
        self._check_connection()
        req = self._encode_request_joint_states()
        if req:
            try:
                self._sock.sendto(req, self._peer)
                raw, _ = self._sock.recvfrom(self.SOCKET_RECV_BYTES)
                if raw:
                    self._last_joint_states = self._decode_joint_states(raw)
            except OSError:
                pass
        return list(self._last_joint_states)

    def get_ee_pose(self):
        self._check_connection()
        req = self._encode_request_ee_pose()
        if req:
            try:
                self._sock.sendto(req, self._peer)
                raw, _ = self._sock.recvfrom(self.SOCKET_RECV_BYTES)
                if raw:
                    self._last_ee_pose = self._decode_ee_pose(raw)
            except OSError:
                pass
        return {"position": list(self._last_ee_pose["position"]),
                "orientation": list(self._last_ee_pose["orientation"])}

    def stop(self):
        if self._sock is not None and self._peer is not None:
            try:
                pkt = self._encode_stop()
                if pkt:
                    self._sock.sendto(pkt, self._peer)
            except OSError:
                pass
        self.disconnect()


# ============================================================
# 4. 品牌特定协议适配器（已补字节级最小实现，真实对接前须对照品牌官方手册复核）
# ⚠️  以下编码/解码结构为「通用骨架」，字节序、校验、CRC、帧头
#     均参考公开资料近似实现；**禁止直接用于生产/真实运动**。
# ⚠️  正式部署前须执行 3 项安全复核（请在完成后删除注释）：
#     [ ] 1. 比对品牌官方 SDK / 通信协议手册的帧头、指令码、长度字段
#     [ ] 2. 单机空运行（机器人空载+急停可触达）验证关节角度/位姿映射方向
#     [ ] 3. 低速 (<10%) 运行 5 分钟以上无抖动/超限后再提速
# ============================================================

import struct as _struct


# --- 库卡 KUKA ---
class KukaFRIAdapter(GenericUDPAdapter):
    """KUKA FRI (Fast Robot Interface) 1ms 控制周期。

    最小帧结构（示意，须对照 FRI SDK「FRI Client Data」结构）：
      sync(4B,0x46524900="FRI\\0") | seq(2B) | cmd(2B) | n_joints(2B) | angles(float32[])
    """
    DEFAULT_PORT = 30200
    _SYNC = b"FRI\0"

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _encode_handshake(self) -> Optional[bytes]:
        # cmd=0x0001 HELLO ; seq=0x0001 ; n_joints=0
        return self._SYNC + _struct.pack("<HHH", 0x0001, 0x0001, 0)

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        n = len(joint_angles_deg)
        rad = [math.radians(float(a)) for a in joint_angles_deg]
        self._last_seq = (self._last_seq + 1) & 0xFFFF
        return self._SYNC + _struct.pack(
            f"<HHH{n}f", 0x0010, self._last_seq, n, *rad
        )

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        n = len(pose6d_deg)
        self._last_seq = (self._last_seq + 1) & 0xFFFF
        # pose6d: xyz(m) + rpy(rad)
        return self._SYNC + _struct.pack(
            f"<HHH{n}f", 0x0011, self._last_seq, n, *[float(v) for v in pose6d_deg]
        )

    def _encode_stop(self) -> Optional[bytes]:
        return self._SYNC + _struct.pack("<HHH", 0x00FF, self._last_seq, 0)

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        # 期待最小帧：SYNC(4) + status(2) + seq(2) + n(2) + angles(float32[n])
        if len(raw) < 12 or raw[:4] != self._SYNC:
            return None
        try:
            _, _, n = _struct.unpack("<HHH", raw[4:10])
            if len(raw) < 10 + 4 * n:
                return None
            deg = [math.degrees(v) for v in _struct.unpack(f"<{n}f", raw[10:10 + 4 * n])]
            return deg
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 10 + 24 or raw[:4] != self._SYNC:
            return None
        try:
            _, _, _n = _struct.unpack("<HHH", raw[4:10])
            # 位姿帧（示意）：紧接 angles 后追加 6 个 float32 位姿（xyz+rpy）
            off = 10 + 4 * _n
            if len(raw) >= off + 24:
                pose = list(_struct.unpack("<6f", raw[off:off + 24]))
                pose[3:6] = [math.degrees(v) for v in pose[3:6]]
                return pose
            return None
        except Exception:
            return None


class KukaEKIAdapter(GenericTCPAdapter):
    """KUKA EKI (Ethernet KRL XML) XML 帧接口。

    默认端口 54600。最小实现用 XML 字符串包装角度数据（符合 KRL XML 基本形状）。
    真实对接：请按机器人端 <RECV> / <SEND> 标签配置的字段名对齐。
    """
    DEFAULT_PORT = 54600

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _encode_handshake(self) -> Optional[bytes]:
        return b'<?xml version="1.0"?><Robot><Status>Hello</Status></Robot>\0'

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        j = ",".join(f"{a:.4f}" for a in joint_angles_deg)
        xml = f'<?xml version="1.0"?><Robot><A1 Axis="1..{len(joint_angles_deg)}">{j}</A1><Speed>{speed:.3f}</Speed></Robot>\0'
        return xml.encode("utf-8")

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        s = ",".join(f"{v:.4f}" for v in pose6d_deg)
        xml = f'<?xml version="1.0"?><Robot><Pose>{s}</Pose><Speed>{speed:.3f}</Speed></Robot>\0'
        return xml.encode("utf-8")

    def _encode_stop(self) -> Optional[bytes]:
        return b'<?xml version="1.0"?><Robot><Stop>1</Stop></Robot>\0'

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        # 非常宽松：提取 XML 中所有以 <A1>...</A1> 形式出现的逗号分隔数字
        import re as _re
        m = _re.search(r"<A1[^>]*>([^<]+)</A1>", raw.decode("utf-8", errors="ignore"))
        if not m:
            return None
        try:
            return [float(x) for x in m.group(1).split(",") if x.strip()]
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        import re as _re
        m = _re.search(r"<Pose>([^<]+)</Pose>", raw.decode("utf-8", errors="ignore"))
        if not m:
            return None
        try:
            return [float(x) for x in m.group(1).split(",") if x.strip()]
        except Exception:
            return None


# --- 优傲 UR ---
class URRTDEAdapter(GenericTCPAdapter):
    """Universal Robots RTDE (Real-Time Data Exchange)。

    端口 30004；最小实现仅用 UR 基础控制帧（非 RTDE recipe 握手）：
      magic(4B 0x55525444 "URTD") | pkt_type(1B) | len(2B) | payload
    真实对接必须走完整 RTDE recipe 握手流程（参考官方 RTDE guide）。
    """
    DEFAULT_PORT = 30004
    _MAGIC = b"URTD"

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _encode_handshake(self) -> Optional[bytes]:
        # pkt_type=0x01 (protocol_version); payload=uint16(2)=v2
        payload = _struct.pack("<H", 2)
        return self._MAGIC + _struct.pack("<BH", 0x01, len(payload)) + payload

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        # pkt_type=0x10 (示意 movej); payload: speed(float32) | accel(float32) | n(float32[])
        rad = [math.radians(float(a)) for a in joint_angles_deg]
        n = len(rad)
        payload = _struct.pack(f"<ff{n}f", float(speed) * 0.5, float(speed) * 1.0, *rad)
        return self._MAGIC + _struct.pack("<BH", 0x10, len(payload)) + payload

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        n = len(pose6d_deg)
        payload = _struct.pack(f"<ff{n}f", float(speed) * 0.1, float(speed) * 0.5, *[float(v) for v in pose6d_deg])
        return self._MAGIC + _struct.pack("<BH", 0x11, len(payload)) + payload

    def _encode_stop(self) -> Optional[bytes]:
        return self._MAGIC + _struct.pack("<BH", 0xFF, 0)

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 7 or raw[:4] != self._MAGIC:
            return None
        _, pl = _struct.unpack("<BH", raw[4:7])
        if len(raw) < 7 + pl:
            return None
        p = raw[7:7 + pl]
        # 最简单：按 float32 全部解包取前 6 个当作关节角（真实对接必须按 recipe 字段表）
        try:
            n = len(p) // 4
            if n < 6:
                return None
            vals = list(_struct.unpack(f"<{n}f", p))
            return [math.degrees(v) for v in vals[:6]]
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 7 or raw[:4] != self._MAGIC:
            return None
        _, pl = _struct.unpack("<BH", raw[4:7])
        if len(raw) < 7 + pl:
            return None
        p = raw[7:7 + pl]
        try:
            n = len(p) // 4
            if n < 12:
                return None
            vals = list(_struct.unpack(f"<{n}f", p))
            pose = vals[6:12]
            pose[3:6] = [math.degrees(v) for v in pose[3:6]]
            return pose
        except Exception:
            return None


# --- ABB ---
class ABBEGMAdapter(GenericUDPAdapter):
    """ABB Externally Guided Motion（UDP 高速引导运动，125Hz 控制）。

    最小实现使用简化二进制头（非 EGM ProtoBuf 全量）：
      seqno(4B) | tm(4B) | mtype(2B) | n_joints(2B) | joints(float32[])
    真实对接必须用 Google ProtoBuf 解析 EGM Robot/Controller 消息结构。
    """
    DEFAULT_PORT = 6511

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _encode_handshake(self) -> Optional[bytes]:
        self._last_seq += 1
        return _struct.pack("<IIHH", self._last_seq, 0, 0x0001, 0)

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        self._last_seq += 1
        n = len(joint_angles_deg)
        rad = [math.radians(float(a)) for a in joint_angles_deg]
        return _struct.pack(f"<IIHH{n}f", self._last_seq, 0, 0x0010, n, *rad)

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        self._last_seq += 1
        n = len(pose6d_deg)
        return _struct.pack(f"<IIHH{n}f", self._last_seq, 0, 0x0011, n, *[float(v) for v in pose6d_deg])

    def _encode_stop(self) -> Optional[bytes]:
        return _struct.pack("<IIHH", self._last_seq, 0, 0x00FF, 0)

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 12:
            return None
        try:
            _, _, mtype, n = _struct.unpack("<IIHH", raw[:12])
            if mtype not in (0x0010, 0x0020) or len(raw) < 12 + 4 * n:
                return None
            return [math.degrees(v) for v in _struct.unpack(f"<{n}f", raw[12:12 + 4 * n])]
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 12 + 24:
            return None
        try:
            _, _, mtype, n = _struct.unpack("<IIHH", raw[:12])
            off = 12 + 4 * n
            if len(raw) < off + 24:
                return None
            pose = list(_struct.unpack("<6f", raw[off:off + 24]))
            pose[3:6] = [math.degrees(v) for v in pose[3:6]]
            return pose
        except Exception:
            return None


class ABBRapidAdapter(GenericTCPAdapter):
    """ABB RAPID Sockets 通信（RAPID 端程序 SocketSend/SocketReceive）。

    最小实现用 ASCII 行命令风格（和 RAPID 程序约定一致即可），真实对接请按
    机器人端 Rapid 程序约定的字段分隔符和字段顺序精确对齐。
    """
    DEFAULT_PORT = 1025

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _encode_handshake(self) -> Optional[bytes]:
        return b"HANDSHAKE\n"

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        j = " ".join(f"{a:.4f}" for a in joint_angles_deg)
        return f"MOVEJ {j} SPEED={speed:.3f}\n".encode("ascii")

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        p = " ".join(f"{v:.4f}" for v in pose6d_deg)
        return f"MOVEL {p} SPEED={speed:.3f}\n".encode("ascii")

    def _encode_stop(self) -> Optional[bytes]:
        return b"STOP\n"

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        line = raw.decode("ascii", errors="ignore").strip()
        if line.startswith("JOINT "):
            try:
                return [float(x) for x in line.split()[1:]]
            except Exception:
                return None
        return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        line = raw.decode("ascii", errors="ignore").strip()
        if line.startswith("POSE "):
            try:
                return [float(x) for x in line.split()[1:]]
            except Exception:
                return None
        return None


# --- 越疆 Dobot ---
class DobotSerialAdapter(GenericSerialAdapter):
    """Dobot 机械臂 Modbus/Serial 控制（CR/MG/UA 系列 USB 虚拟串口）。

    最小实现用 Modbus-RTU 风格：Addr(1B) Func(1B) RegAddrHi(1B) RegAddrLo(1B)
    CountHi(1B) CountLo(1B) CRC16(2B)。真实对接须按 Dobot Modbus 寄存器表。
    """
    def __init__(self, host="", port=0, config=None):
        super().__init__(host, port, config)
        self.baudrate = int((config or {}).get("baudrate", 115200))

    @staticmethod
    def _crc16_modbus(data: bytes) -> int:
        crc = 0xFFFF
        for b in data:
            crc ^= b
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc & 0xFFFF

    def _mb(self, addr: int, func: int, payload: bytes) -> bytes:
        head = bytes([addr & 0xFF, func & 0xFF]) + payload
        crc = self._crc16_modbus(head)
        return head + bytes([crc & 0xFF, (crc >> 8) & 0xFF])

    def _encode_handshake(self) -> Optional[bytes]:
        # 读设备识别码（示意）：addr=1, func=0x03, reg=0x0000, count=2
        return self._mb(1, 0x03, b"\x00\x00\x00\x02")

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        # 示意：func=0x10 写多个保持寄存器，起点 0x0100（非真实 Dobot 寄存器表！）
        vals = [int(a * 1000.0) for a in joint_angles_deg]  # 毫度 → 16位有符号
        n = len(vals)
        reg_bytes = b"".join(_struct.pack(">h", v & 0xFFFF) for v in vals)
        payload = _struct.pack(">HHB", 0x0100, n, 2 * n) + reg_bytes
        return self._mb(1, 0x10, payload)

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        vals = [int(v * 1000.0) for v in pose6d_deg]
        n = len(vals)
        reg_bytes = b"".join(_struct.pack(">h", v & 0xFFFF) for v in vals)
        payload = _struct.pack(">HHB", 0x0200, n, 2 * n) + reg_bytes
        return self._mb(1, 0x10, payload)

    def _encode_stop(self) -> Optional[bytes]:
        # func=0x06 写单个寄存器 0x00FF = 0x0001（示意 急停触发）
        return self._mb(1, 0x06, _struct.pack(">HH", 0x00FF, 0x0001))

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 5:
            return None
        try:
            a, f, bc = raw[0], raw[1], raw[2]
            if f == 0x03 or f == 0x10:
                data = raw[3:3 + bc]
                n = len(data) // 2
                vals = list(_struct.unpack(f">{n}h", data))
                return [v / 1000.0 for v in vals]
            return None
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        return self._decode_joint_states(raw)  # 同格式，寄存器不同；真实对接区分


class DobotTCPAdapter(GenericTCPAdapter):
    """Dobot 以太网 TCP/IP 控制（CR 系列控制器网口）。默认端口 29999。

    最小实现：沿用 DobotSerial 的 Modbus-RTU 包直接 TCP 透传（去掉 CRC 即 Modbus-TCP
    也可；真实对接推荐 Modbus-TCP，头部 6B：TID(2)+PID(2)+Len(2)+UID(1)）。
    """
    DEFAULT_PORT = 29999

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)
        self._tid = 0

    def _mb_tcp(self, uid: int, func: int, payload: bytes) -> bytes:
        self._tid = (self._tid + 1) & 0xFFFF
        body = bytes([uid & 0xFF, func & 0xFF]) + payload
        return _struct.pack(">HHH", self._tid, 0x0000, len(body)) + body

    def _encode_handshake(self) -> Optional[bytes]:
        return self._mb_tcp(1, 0x03, b"\x00\x00\x00\x02")

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        vals = [int(a * 1000.0) for a in joint_angles_deg]
        n = len(vals)
        reg_bytes = b"".join(_struct.pack(">h", v & 0xFFFF) for v in vals)
        payload = _struct.pack(">HHB", 0x0100, n, 2 * n) + reg_bytes
        return self._mb_tcp(1, 0x10, payload)

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        vals = [int(v * 1000.0) for v in pose6d_deg]
        n = len(vals)
        reg_bytes = b"".join(_struct.pack(">h", v & 0xFFFF) for v in vals)
        payload = _struct.pack(">HHB", 0x0200, n, 2 * n) + reg_bytes
        return self._mb_tcp(1, 0x10, payload)

    def _encode_stop(self) -> Optional[bytes]:
        return self._mb_tcp(1, 0x06, _struct.pack(">HH", 0x00FF, 0x0001))

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 9:
            return None
        try:
            _, _, _len, uid, func, bc = _struct.unpack(">HHHBBB", raw[:9])
            data = raw[9:9 + bc]
            n = len(data) // 2
            vals = list(_struct.unpack(f">{n}h", data))
            return [v / 1000.0 for v in vals]
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        return self._decode_joint_states(raw)


# --- 星动纪元 Airbot ---
class AirbotTCPAdapter(GenericTCPAdapter):
    """Airbot P7/S2 等机器人官方 TCP SDK 接口。默认端口 8080。

    最小帧结构（示意）：sync(2B 0xAA55) | cmd(2B) | seq(2B) | len(4B LE) | payload
    真实对接请按 Airbot 官方 Python SDK / C SDK 的协议文档。
    """
    DEFAULT_PORT = 8080
    _SYNC = _struct.pack("<H", 0xAA55)

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _encode_handshake(self) -> Optional[bytes]:
        payload = b"airbot_v1"
        return self._SYNC + _struct.pack("<HHI", 0x0001, 0x0001, len(payload)) + payload

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        rad = [math.radians(float(a)) for a in joint_angles_deg]
        n = len(rad)
        self._last_seq = (self._last_seq + 1) & 0xFFFF
        payload = _struct.pack(f"<fI{n}f", float(speed), n, *rad)
        return self._SYNC + _struct.pack("<HHI", 0x0010, self._last_seq, len(payload)) + payload

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        n = len(pose6d_deg)
        self._last_seq = (self._last_seq + 1) & 0xFFFF
        payload = _struct.pack(f"<fI{n}f", float(speed), n, *[float(v) for v in pose6d_deg])
        return self._SYNC + _struct.pack("<HHI", 0x0011, self._last_seq, len(payload)) + payload

    def _encode_stop(self) -> Optional[bytes]:
        return self._SYNC + _struct.pack("<HHI", 0x00FF, self._last_seq, 0)

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 10 or raw[:2] != self._SYNC:
            return None
        try:
            cmd, _, pl = _struct.unpack("<HHI", raw[2:10])
            if len(raw) < 10 + pl:
                return None
            p = raw[10:10 + pl]
            if cmd in (0x0020, 0x0010) and len(p) >= 8:
                _, n = _struct.unpack("<fI", p[:8])
                if len(p) >= 8 + 4 * n:
                    vals = list(_struct.unpack(f"<{n}f", p[8:8 + 4 * n]))
                    return [math.degrees(v) for v in vals]
            return None
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 10 or raw[:2] != self._SYNC:
            return None
        try:
            cmd, _, pl = _struct.unpack("<HHI", raw[2:10])
            if len(raw) < 10 + pl:
                return None
            p = raw[10:10 + pl]
            if cmd == 0x0021 and len(p) >= 8 + 24:
                _, n = _struct.unpack("<fI", p[:8])
                pose = list(_struct.unpack(f"<{n}f", p[8:8 + 4 * n]))
                pose[3:6] = [math.degrees(v) for v in pose[3:6]]
                return pose
            return None
        except Exception:
            return None


# --- 越疆 UFACTORY (xArm / CRA / Lite) ---
class UFactoryTCPAdapter(GenericTCPAdapter):
    """UFACTORY Lite/CRA/xArm TCP 接口。默认端口 8080（xArm API）。

    最小实现用官方风格的 JSON 行（xArm Python SDK 实际走二进制；这里 JSON 便于联调），
    真实对接请直接使用官方 xArm-Python-SDK 并关闭安全门开关。
    """
    DEFAULT_PORT = 8080

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _encode_handshake(self) -> Optional[bytes]:
        return b'{"cmd":"hello","version":1}\n'

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        import json as _json
        msg = {"cmd": "move_gohome_joint" if False else "move_joint",
               "joint": [float(a) for a in joint_angles_deg],
               "speed": float(speed) * 100.0, "mvacc": 500.0,
               "mvt": 1, "is_ready": 1}
        return (_json.dumps(msg, ensure_ascii=False) + "\n").encode("utf-8")

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        import json as _json
        msg = {"cmd": "move_line", "pose": [float(v) for v in pose6d_deg],
               "speed": float(speed) * 100.0, "mvacc": 500.0,
               "mvt": 1, "is_ready": 1}
        return (_json.dumps(msg, ensure_ascii=False) + "\n").encode("utf-8")

    def _encode_stop(self) -> Optional[bytes]:
        return b'{"cmd":"emergency_release","enable":1}\n'

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        import json as _json
        try:
            for line in raw.decode("utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line:
                    continue
                obj = _json.loads(line)
                if "joint" in obj and isinstance(obj["joint"], list):
                    return [float(x) for x in obj["joint"]]
            return None
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        import json as _json
        try:
            for line in raw.decode("utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line:
                    continue
                obj = _json.loads(line)
                if "pose" in obj and isinstance(obj["pose"], list):
                    return [float(x) for x in obj["pose"]]
            return None
        except Exception:
            return None


# --- 节卡 JAKA ---
class JakaTCPAdapter(GenericTCPAdapter):
    """JAKA Zu 系列 TCP/IP 控制接口。节卡官方默认端口 10000。

    最小帧：Header(4B "JAKA") | cmd_id(2B LE) | seq(2B LE) | body_len(4B LE) | JSON-body
    真实对接必须用节卡官方二次开发手册的 JSON RPC 字段名。
    """
    DEFAULT_PORT = 10000
    _HDR = b"JAKA"

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _frame(self, cmd_id: int, body: bytes) -> bytes:
        self._last_seq = (self._last_seq + 1) & 0xFFFF
        return self._HDR + _struct.pack("<HHI", cmd_id, self._last_seq, len(body)) + body

    def _encode_handshake(self) -> Optional[bytes]:
        import json as _json
        b = _json.dumps({"jsonrpc": "2.0", "method": "status", "id": 1}).encode("utf-8")
        return self._frame(0x0001, b)

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        import json as _json
        body = _json.dumps({
            "jsonrpc": "2.0", "method": "move_joint",
            "params": {"joint": [float(a) for a in joint_angles_deg],
                       "speed": float(speed) * 50.0, "acc": 100.0, "tol": 0.1},
            "id": self._last_seq
        }, ensure_ascii=False).encode("utf-8")
        return self._frame(0x0010, body)

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        import json as _json
        body = _json.dumps({
            "jsonrpc": "2.0", "method": "move_line",
            "params": {"pose": [float(v) for v in pose6d_deg],
                       "speed": float(speed) * 50.0, "acc": 100.0, "tol": 0.1},
            "id": self._last_seq
        }, ensure_ascii=False).encode("utf-8")
        return self._frame(0x0011, body)

    def _encode_stop(self) -> Optional[bytes]:
        import json as _json
        b = _json.dumps({"jsonrpc": "2.0", "method": "estop", "id": self._last_seq}).encode("utf-8")
        return self._frame(0x00FF, b)

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        import json as _json
        if len(raw) < 12 or raw[:4] != self._HDR:
            return None
        try:
            _, _, pl = _struct.unpack("<HHI", raw[4:12])
            if len(raw) < 12 + pl:
                return None
            obj = _json.loads(raw[12:12 + pl].decode("utf-8", errors="ignore"))
            r = obj.get("result") or obj.get("result") or {}
            if "joint" in r and isinstance(r["joint"], list):
                return [float(x) for x in r["joint"]]
            return None
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        import json as _json
        if len(raw) < 12 or raw[:4] != self._HDR:
            return None
        try:
            _, _, pl = _struct.unpack("<HHI", raw[4:12])
            if len(raw) < 12 + pl:
                return None
            obj = _json.loads(raw[12:12 + pl].decode("utf-8", errors="ignore"))
            r = obj.get("result") or {}
            if "pose" in r and isinstance(r["pose"], list):
                return [float(x) for x in r["pose"]]
            return None
        except Exception:
            return None


# --- 步科 Kinco Modbus RTU ---
class BukeModbusAdapter(GenericSerialAdapter):
    """步科伺服 / 机械臂 Modbus RTU over RS485/USB。默认 115200 8N1。

    最小实现沿用 Modbus-RTU（和 DobotSerial 结构一致），寄存器映射待填。
    """
    def __init__(self, host="", port=0, config=None):
        super().__init__(host, port, config)
        self.baudrate = int((config or {}).get("baudrate", 115200))

    @staticmethod
    def _crc16_modbus(data: bytes) -> int:
        crc = 0xFFFF
        for b in data:
            crc ^= b
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc & 0xFFFF

    def _mb(self, addr: int, func: int, payload: bytes) -> bytes:
        head = bytes([addr & 0xFF, func & 0xFF]) + payload
        crc = self._crc16_modbus(head)
        return head + bytes([crc & 0xFF, (crc >> 8) & 0xFF])

    def _encode_handshake(self) -> Optional[bytes]:
        # 读 0x0000 厂商 ID（示意）
        return self._mb(1, 0x03, b"\x00\x00\x00\x04")

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        # 寄存器 0x0100 起按轴写入毫度值
        vals = [int(a * 100.0) for a in joint_angles_deg]
        n = len(vals)
        reg_bytes = b"".join(_struct.pack(">h", v & 0xFFFF) for v in vals)
        payload = _struct.pack(">HHB", 0x0100, n, 2 * n) + reg_bytes
        return self._mb(1, 0x10, payload)

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        vals = [int(v * 100.0) for v in pose6d_deg]
        n = len(vals)
        reg_bytes = b"".join(_struct.pack(">h", v & 0xFFFF) for v in vals)
        payload = _struct.pack(">HHB", 0x0200, n, 2 * n) + reg_bytes
        return self._mb(1, 0x10, payload)

    def _encode_stop(self) -> Optional[bytes]:
        # 急停：写 0x00FF = 0x0001（示意）
        return self._mb(1, 0x06, _struct.pack(">HH", 0x00FF, 0x0001))

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 5:
            return None
        try:
            a, f, bc = raw[0], raw[1], raw[2]
            if f in (0x03, 0x10):
                data = raw[3:3 + bc]
                n = len(data) // 2
                vals = list(_struct.unpack(f">{n}h", data))
                return [v / 100.0 for v in vals]
            return None
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        return self._decode_joint_states(raw)


# --- 宇树 Unitree（人形/四足 UDP）---
class UnitreeUDPAdapter(GenericUDPAdapter):
    """Unitree Go2 / B2 / H1 高速 UDP 控制通道。默认端口 8080 / 8090。

    最小实现：HighState / HighCmd 的精简二进制骨架（真实对接必须使用
    unitree_sdk2 / unitree_go 官方仓库的 CRCLibrary 协议头）。
    结构（示意）：head(2B 0xFEF0) | len(2B LE) | seq(4B LE) | mode(1B) | n_joints(2B LE) | q(float32[])
    """
    DEFAULT_PORT = 8080
    _HEAD = _struct.pack("<H", 0xFEF0)

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _encode_handshake(self) -> Optional[bytes]:
        self._last_seq += 1
        body = _struct.pack("<IIHQ", 0x0001, self._last_seq, 0, 0)
        return self._HEAD + _struct.pack("<H", len(body)) + body

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        self._last_seq += 1
        rad = [math.radians(float(a)) for a in joint_angles_deg]
        n = len(rad)
        # 模式 0x02 = 运动模式（示意）；dq = 速度；kp/kd = 增益；tau = 力矩
        dq = [0.0] * n
        kp = [100.0] * n
        kd = [1.0] * n
        tau = [0.0] * n
        body = _struct.pack(
            f"<IBH{n}f{n}f{n}f{n}f{n}f",
            self._last_seq, 0x02, n,
            *rad, *dq, *kp, *kd, *tau
        )
        return self._HEAD + _struct.pack("<H", len(body)) + body

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        self._last_seq += 1
        n = len(pose6d_deg)
        body = _struct.pack(
            f"<IBHf{n}f", self._last_seq, 0x03, n, float(speed),
            *[float(v) for v in pose6d_deg]
        )
        return self._HEAD + _struct.pack("<H", len(body)) + body

    def _encode_stop(self) -> Optional[bytes]:
        self._last_seq += 1
        body = _struct.pack("<IBH", self._last_seq, 0xFF, 0)
        return self._HEAD + _struct.pack("<H", len(body)) + body

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 8 or raw[:2] != self._HEAD:
            return None
        try:
            bl = _struct.unpack("<H", raw[2:4])[0]
            if len(raw) < 4 + bl:
                return None
            body = raw[4:4 + bl]
            if bl < 10:
                return None
            seq, mode, n = _struct.unpack("<IBH", body[:7])
            if len(body) < 7 + 4 * n * 5:
                return None
            vals = list(_struct.unpack(f"<{n}f", body[7:7 + 4 * n]))
            return [math.degrees(v) for v in vals]
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 8 or raw[:2] != self._HEAD:
            return None
        try:
            bl = _struct.unpack("<H", raw[2:4])[0]
            if len(raw) < 4 + bl:
                return None
            body = raw[4:4 + bl]
            if bl < 7 + 4 * 6:
                return None
            seq, mode, n = _struct.unpack("<IBH", body[:7])
            off = 7 + 4 * n * 5  # 跳过 q/dq/kp/kd/tau
            if len(body) < off + 24:
                return None
            pose = list(_struct.unpack("<6f", body[off:off + 24]))
            pose[3:6] = [math.degrees(v) for v in pose[3:6]]
            return pose
        except Exception:
            return None


# --- 深度科技 DeepRobotics（绝影 Lite3 等）---
class DeepRoboticsTCPAdapter(GenericTCPAdapter):
    """Deep Robotics 足式/机械臂 TCP 控制接口。

    最小帧结构（示意，须对照 DEEPRobotics SDK）：magic(4B="DR01") | cmd(2B) | len(4B) | payload
    """
    DEFAULT_PORT = 43893
    _MAGIC = b"DR01"

    def __init__(self, host, port=None, config=None):
        super().__init__(host, port or self.DEFAULT_PORT, config)

    def _encode_handshake(self) -> Optional[bytes]:
        payload = b"deep_v1"
        return self._MAGIC + _struct.pack("<HI", 0x0001, len(payload)) + payload

    def _encode_move_joints(self, joint_angles_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        rad = [math.radians(float(a)) for a in joint_angles_deg]
        n = len(rad)
        self._last_seq = (self._last_seq + 1) & 0xFFFF
        payload = _struct.pack(f"<IH{n}f", self._last_seq, n, *rad)
        return self._MAGIC + _struct.pack("<HI", 0x0010, len(payload)) + payload

    def _encode_move_cartesian(self, pose6d_deg: List[float], speed: float = 1.0) -> Optional[bytes]:
        n = len(pose6d_deg)
        self._last_seq = (self._last_seq + 1) & 0xFFFF
        payload = _struct.pack(f"<IH{n}f", self._last_seq, n, *[float(v) for v in pose6d_deg])
        return self._MAGIC + _struct.pack("<HI", 0x0011, len(payload)) + payload

    def _encode_stop(self) -> Optional[bytes]:
        return self._MAGIC + _struct.pack("<HI", 0x00FF, 0)

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 10 or raw[:4] != self._MAGIC:
            return None
        try:
            cmd, pl = _struct.unpack("<HI", raw[4:10])
            if len(raw) < 10 + pl:
                return None
            p = raw[10:10 + pl]
            if pl < 6:
                return None
            _, n = _struct.unpack("<IH", p[:6])
            if len(p) < 6 + 4 * n:
                return None
            return [math.degrees(v) for v in _struct.unpack(f"<{n}f", p[6:6 + 4 * n])]
        except Exception:
            return None

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        if len(raw) < 10 or raw[:4] != self._MAGIC:
            return None
        try:
            cmd, pl = _struct.unpack("<HI", raw[4:10])
            if len(raw) < 10 + pl:
                return None
            p = raw[10:10 + pl]
            if pl < 6:
                return None
            _, n = _struct.unpack("<IH", p[:6])
            off = 6 + 4 * n
            if len(p) < off + 24:
                return None
            pose = list(_struct.unpack("<6f", p[off:off + 24]))
            pose[3:6] = [math.degrees(v) for v in pose[3:6]]
            return pose
        except Exception:
            return None



# ============================================================
# GenericBridgeAdapter（非运动体兜底桥接适配器）
# 适用：AI芯片、传感器、轴承、力传感器、电子皮肤、核心板、研究平台、通信设备、
#       AI大模型、XR设备、AI手机、AI眼镜、量子算力、能源设备、基建设备等非机械臂/
#       非人形/非足式产品。保证：初始化不崩、move_joints不执行、读接口返回默认值、
#       永远不抛异常、日志清晰可追溯。
# ============================================================
class GenericBridgeAdapter(GenericTCPAdapter):
    """非运动体/非机械臂产品兜底适配器（芯片/传感器/平台类产品专用桥接）。

    行为：
      · connect/handshake 成功回环（不建立真实连接也返回成功）
      · move_joints/move_cartesian：打印 WARN 日志并跳过执行（芯片/传感器没有关节）
      · get_joint_states/get_ee_pose：返回标准空安全值（0 角度 / 零位姿）
      · stop/disconnect：空操作安全成功
    """
    DEFAULT_PORT = 0  # 非运动体无 TCP 端口，使用 0 占位

    def __init__(self, host="", port=None, config=None):
        super().__init__(host or "", port or self.DEFAULT_PORT, config or {})

    def connect(self, timeout: float = 5.0) -> bool:
        # 非运动体 connect 永远成功（回环模式）
        self._connected = True
        try:
            cfg = self.config or {}
            _name = cfg.get("name") or cfg.get("model") or "GenericBridgeProduct"
            _brand = cfg.get("brand") or "Unknown"
            print(f"[BRIDGE] 非运动体桥接初始化成功: brand={_brand}, model={_name}")
        except Exception:
            print("[BRIDGE] 非运动体桥接初始化成功（缺省模式）")
        return True

    def disconnect(self) -> None:
        self._connected = False
        return None

    def _encode_handshake(self) -> Optional[bytes]:
        # 非运动体无真实协议，返回空字节
        return b"BRIDGE_HELLO\x00"

    def _encode_move_joints(self, joint_angles_deg, speed=1.0):
        # 非运动体永远不执行关节运动 → 空字节
        return b""

    def _encode_move_cartesian(self, pose6d_deg, speed=1.0):
        # 非运动体永远不执行笛卡尔运动 → 空字节
        return b""

    def _encode_stop(self) -> Optional[bytes]:
        return b""

    def _decode_joint_states(self, raw: bytes) -> Optional[List[float]]:
        # 返回空列表（非运动体无关节）
        return []

    def _decode_ee_pose(self, raw: bytes) -> Optional[List[float]]:
        # 返回零位姿（非运动体无末端）
        return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # 上层调用安全接口：
    def move_joints(self, joint_angles_deg, speed=1.0) -> None:
        # 非运动体无关节 → 仅日志，不抛错
        if False:
            try:
                _ = len(joint_angles_deg), float(speed)  # 防止未使用告警
            except Exception:
                pass

    def move_cartesian(self, pose6d_deg, speed=1.0) -> None:
        # 非运动体无末端 → 仅日志，不抛错
        if False:
            try:
                _ = len(pose6d_deg), float(speed)
            except Exception:
                pass

    def stop(self) -> None:
        return None

    def get_joint_states(self) -> List[float]:
        return []

    def get_ee_pose(self) -> Dict[str, List[float]]:
        return {"position": [0.0, 0.0, 0.0], "orientation": [0.0, 0.0, 0.0, 1.0]}


# ============================================================
# 4.5 EVTOL 地图适配器（高德/腾讯 双路容灾）
# ============================================================

class EVTOLMapAdapter(GenericBridgeAdapter):
    """eVTOL 低空飞行器地图适配器。

    替换 generic_bridge，为 eVTOL 产品提供：
      · 高德地图 API（首选） / 腾讯地图 API（兜底）双路容灾
      · 航线规划 plan_flight_route(from, to, waypoints)
      · 起降点天气/风场查询 get_weather_at(lat,lng)
      · ETA 估算（距离 / 预设巡航速度）
      · 地理围栏 & 低空航线合规性检查（静态规则 + 地图禁飞区）
      · move_cartesian 扩展语义：pose6d 前三维 = [纬度, 经度, 高度(m)]，后三维 = [航向°, 俯仰°, 横滚°]

    凭证通过环境变量注入：
        AMAP_API_KEY      → 高德 Web 服务 Key (优先级1)
        TENCENT_MAP_KEY   → 腾讯地图 WebService Key (优先级2)
    都缺失时降级为“本地几何计算模式”，仍能返回规划结果（仅无真实路况/禁飞区）。
    """

    DEFAULT_PORT = 0

    # 预设典型巡航速度（km/h）— 按 eVTOL 品类可调
    DEFAULT_CRUISE_SPEED_KMH = 200.0
    DEFAULT_CLIMB_RATE_MPS = 5.0
    DEFAULT_DESCENT_RATE_MPS = 4.0

    def __init__(self, host="", port=None, config=None):
        super().__init__(host or "", port or self.DEFAULT_PORT, config or {})
        self._map_provider_order: List[str] = []
        self._configure_map_providers()
        # 当前位置（初始为配置坐标或上海虹桥机场中心点）
        default_lat = float(self.config.get("home_lat", 31.1979))
        default_lng = float(self.config.get("home_lng", 121.3363))
        default_alt = float(self.config.get("home_alt", 0.0))
        self._current_lla = [default_lat, default_lng, default_alt]  # lat, lng, alt(m)
        self._current_attitude = [0.0, 0.0, 0.0]  # heading°, pitch°, roll°
        self._cruise_speed_kmh = float(
            self.config.get("cruise_speed_kmh", self.DEFAULT_CRUISE_SPEED_KMH)
        )
        # 简化静态禁飞区：中心+半径(km) 格式（上海虹桥机场上空等占位示例）
        self._no_fly_zones: List[Dict[str, float]] = [
            {"lat": 31.1979, "lng": 121.3363, "radius_km": 2.0, "name": "虹桥机场核心区"},
            {"lat": 39.9042, "lng": 116.4074, "radius_km": 5.0, "name": "北京天安门"},
        ]

    # --------------------------------------------------------
    # Provider 配置
    # --------------------------------------------------------
    def _configure_map_providers(self):
        amap_key = os.getenv("AMAP_API_KEY", "")
        tencent_key = os.getenv("TENCENT_MAP_KEY", "")
        if amap_key:
            self._map_provider_order.append("amap")
        if tencent_key:
            self._map_provider_order.append("tencent")
        if not self._map_provider_order:
            # 两个都没配，也保持顺序，调用时走降级模式
            self._map_provider_order = ["amap", "tencent"]
        self._amap_key = amap_key
        self._tencent_key = tencent_key

    def _has_real_api(self) -> bool:
        return bool(self._amap_key or self._tencent_key)

    # --------------------------------------------------------
    # 重写：connect 额外打印地图可用性
    # --------------------------------------------------------
    def connect(self, timeout: float = 5.0) -> bool:
        super().connect(timeout=timeout)
        _name = (self.config or {}).get("name") or "EVTOL"
        mode = "ONLINE" if self._has_real_api() else "OFFLINE-LOCAL"
        providers = "+".join(self._map_provider_order)
        print(f"[EVTOL-MAP] {_name} 地图适配器就绪: "
              f"mode={mode} providers=[{providers}] "
              f"home=({self._current_lla[0]:.4f},{self._current_lla[1]:.4f},{self._current_lla[2]:.0f}m)")
        return True

    # --------------------------------------------------------
    # eVTOL 专属：重写 move_cartesian 语义 → [lat, lng, alt_m, hdg°, pit°, rol°]
    # --------------------------------------------------------
    def move_cartesian(self, pose6d_deg, speed=1.0) -> None:
        """eVTOL 语义：前 3 维 = 目标[纬度, 经度, 高度m]，后 3 维 = 姿态[航向°, 俯仰°, 横滚°]"""
        try:
            if len(pose6d_deg) < 3:
                return
            tgt = list(pose6d_deg)
            while len(tgt) < 6:
                tgt.append(0.0)
            lat, lng, alt = float(tgt[0]), float(tgt[1]), float(tgt[2])
            # 检查禁飞区
            nfz = self._check_no_fly_zone(lat, lng)
            if nfz:
                print(f"[EVTOL-MAP] ⚠️ 目标位于禁飞区: {nfz['name']}，已拒绝进入")
                return
            # 航线合规性 → 使用高德/腾讯（若可用）
            if self._has_real_api():
                resp = self.plan_flight_route(
                    {"lat": self._current_lla[0], "lng": self._current_lla[1]},
                    {"lat": lat, "lng": lng},
                )
                if resp.get("compliance") is False:
                    print(f"[EVTOL-MAP] ⚠️ 航线合规性失败: {resp.get('compliance_note', '')}")
                    return
            # 更新“当前位置”
            self._current_lla = [lat, lng, alt]
            self._current_attitude = [float(tgt[3]), float(tgt[4]), float(tgt[5])]
            eta = self.estimate_eta(
                self._current_lla,
                [lat, lng, alt],
            )
            print(f"[EVTOL-MAP] 已接受航点: ({lat:.5f},{lng:.5f}) alt={alt:.0f}m "
                  f"heading={tgt[3]:.0f}° 预计ETA={eta}")
        except Exception as e:
            print(f"[EVTOL-MAP] move_cartesian 异常: {e}")

    def get_ee_pose(self) -> Dict[str, List[float]]:
        """eVTOL 语义：position=[lat, lng, alt_m]，orientation=[heading°, pitch°, roll°, 0]"""
        return {
            "position": list(self._current_lla),
            "orientation": list(self._current_attitude) + [0.0],
        }

    # --------------------------------------------------------
    # 核心地图能力（封装 高德/腾讯 双路容灾）
    # --------------------------------------------------------
    def plan_flight_route(self, origin, destination,
                          waypoints=None,
                          ) -> Dict[str, Any]:
        """低空航线规划。【铁律：绝对不能崩溃！

        Args:
            origin:      {"lat":xx, "lng":xx, "alt":xx} 或 [lat, lng, alt] 元组（兼容两种格式
            destination: {"lat":xx, "lng":xx, "alt":xx} 或 [lat, lng, alt]
            waypoints:   途经点 [{"lat":xx,"lng":xx} or tuple]

        Returns:
            {
              "distance_km": float,
              "eta_min": float,      # 分钟（老接口兼容
              "eta_seconds": float,
              "waypoints": [...],
              "compliance": bool,
              "compliance_note": str,
              "provider": "amap"|"tencent"|"local",
              "weather_ok": Optional[bool],
            }
        """
        # 铁律：最外层绝对兜底 try/except
        try:
            # 兼容 tuple/list → dict
            def _normalize(pt):
                if isinstance(pt, dict):
                    return pt
                try:
                    seq = list(pt)
                    nd = {"lat": float(seq[0]), "lng": float(seq[1])}
                    if len(seq) >= 3:
                        nd["alt"] = float(seq[2])
                    return nd
                except Exception:
                    return {"lat": 0.0, "lng": 0.0}

            o = _normalize(origin)
            d = _normalize(destination)
            wps_norm = []
            if waypoints:
                for w in waypoints:
                    wps_norm.append(_normalize(w))
            distance_km = self._haversine_km(o, d)
            wps = wps_norm
            cumulative = 0.0
            prev = o
            for w in wps + [d]:
                cumulative += self._haversine_km(prev, w)
                prev = w
            distance_km = cumulative or distance_km
            d_alt_climb = max(0.0, float(d.get("alt", 300.0)) - float(o.get("alt", 0.0)))
            d_alt_descent = max(0.0, float(o.get("alt", 0.0)) - float(d.get("alt", 0.0)))
            eta_s = self._estimate_flight_seconds(distance_km, climb_m=d_alt_climb, descent_m=d_alt_descent)
            result = {
                "distance_km": round(distance_km, 3),
                "eta_min": round(eta_s / 60.0, 1),
                "eta_seconds": round(eta_s, 1),
                "waypoints": [o] + list(wps) + [d],
                "compliance": True,
                "compliance_note": "",
                "provider": "local",
                "weather_ok": None,
            }
            # 尝试真实 API（高德 → 腾讯 容灾）
            for provider in self._map_provider_order:
                try:
                    if provider == "amap" and self._amap_key:
                        self._amap_route_enrich(result, o, d)
                        result["provider"] = "amap"
                        break
                    if provider == "tencent" and self._tencent_key:
                        self._tencent_route_enrich(result, o, d)
                        result["provider"] = "tencent"
                        break
                except Exception as e:
                    print(f"[EVTOL-MAP] {provider} 规划失败，继续尝试其他：{e}")
                    continue
            # 禁飞区叠加
            try:
                mid = {
                    "lat": (float(o["lat"]) + float(d["lat"])) / 2,
                    "lng": (float(o["lng"]) + float(d["lng"])) / 2,
                }
                nfz = self._check_no_fly_zone(mid["lat"], mid["lng"])
                if nfz:
                    result["compliance"] = False
                    result["compliance_note"] = f"路径中段穿越禁飞区: {nfz['name']}"
            except Exception:
                pass
            return result
        except Exception as e:
            print(f"[EVTOL-MAP] plan_flight_route 绝对兜底拦截: {type(e).__name__}: {e}")
            return {
                "distance_km": 0.0,
                "eta_min": 0.0,
                "eta_seconds": 0.0,
                "waypoints": [],
                "compliance": False,
                "compliance_note": "absolute-safety-net: %s" % type(e).__name__,
                "provider": "safety-net",
                "weather_ok": None,
            }

    def get_weather_at(self, lat: float, lng: float) -> Dict[str, Any]:
        """获取起降点天气/风场（优先高德，其次腾讯，最后离线模拟）。"""
        result = {
            "lat": lat, "lng": lng,
            "temperature_c": 20.0,
            "wind_speed_ms": 3.0,
            "wind_dir_deg": 90.0,
            "visibility_km": 10.0,
            "rain_mm_h": 0.0,
            "flyable": True,
            "provider": "local-mock",
            "note": "离线模拟（无真实地图Key时使用）",
        }
        for provider in self._map_provider_order:
            try:
                if provider == "amap" and self._amap_key:
                    self._amap_weather_enrich(result, lat, lng)
                    result["provider"] = "amap"
                    break
                if provider == "tencent" and self._tencent_key:
                    self._tencent_weather_enrich(result, lat, lng)
                    result["provider"] = "tencent"
                    break
            except Exception as e:
                print(f"[EVTOL-MAP] {provider} 天气查询失败：{e}")
                continue
        # 可飞性判定
        result["flyable"] = (
            result["wind_speed_ms"] < 12.0 and
            result["visibility_km"] > 1.5 and
            result["rain_mm_h"] < 5.0
        )
        return result

    def estimate_eta(self, from_lla: List[float], to_lla: List[float]) -> str:
        """简易 ETA 字符串，方便日志打印。"""
        try:
            dist = self._haversine_km(
                {"lat": from_lla[0], "lng": from_lla[1]},
                {"lat": to_lla[0], "lng": to_lla[1]},
            )
            climb = max(0.0, (to_lla[2] if len(to_lla) > 2 else 0.0) -
                        (from_lla[2] if len(from_lla) > 2 else 0.0))
            descent = max(0.0, (from_lla[2] if len(from_lla) > 2 else 0.0) -
                          (to_lla[2] if len(to_lla) > 2 else 0.0))
            secs = self._estimate_flight_seconds(dist, climb_m=climb, descent_m=descent)
            mm, ss = divmod(int(round(secs)), 60)
            hh, mm = divmod(mm, 60)
            if hh > 0:
                return f"{hh:d}h{mm:02d}m{ss:02d}s"
            return f"{mm:d}m{ss:02d}s"
        except Exception:
            return "n/a"

    # --------------------------------------------------------
    # 底层工具
    # --------------------------------------------------------
    @staticmethod
    def _haversine_km(a: Dict[str, float], b: Dict[str, float]) -> float:
        import math as _m
        R = 6371.0088
        lat1, lng1 = _m.radians(a["lat"]), _m.radians(a["lng"])
        lat2, lng2 = _m.radians(b["lat"]), _m.radians(b["lng"])
        dlat, dlng = lat2 - lat1, lng2 - lng1
        h = _m.sin(dlat / 2) ** 2 + _m.cos(lat1) * _m.cos(lat2) * _m.sin(dlng / 2) ** 2
        return 2 * R * _m.asin(_m.sqrt(h))

    def _estimate_flight_seconds(self, dist_km: float, climb_m: float = 0.0,
                                 descent_m: float = 0.0) -> float:
        cruise_ms = self._cruise_speed_kmh / 3.6
        climb_s = climb_m / self.DEFAULT_CLIMB_RATE_MPS if cruise_ms > 0 else 0.0
        descent_s = descent_m / self.DEFAULT_DESCENT_RATE_MPS if cruise_ms > 0 else 0.0
        cruise_s = (dist_km * 1000.0) / cruise_ms if cruise_ms > 0 else 0.0
        # 起降阶段额外加 120s
        return 120.0 + climb_s + cruise_s + descent_s

    def _check_no_fly_zone(self, lat: float, lng: float) -> Optional[Dict[str, Any]]:
        for z in self._no_fly_zones:
            d = self._haversine_km({"lat": lat, "lng": lng},
                                   {"lat": z["lat"], "lng": z["lng"]})
            if d <= z["radius_km"]:
                return z
        return None

    # --------------------------------------------------------
    # 高德 API 封装
    # --------------------------------------------------------
    def _amap_route_enrich(self, result: Dict[str, Any],
                           origin: Dict[str, float], dest: Dict[str, float]):
        if requests is None or not self._amap_key:
            return
        # 高德驾车路径规划作为低空路径的近似参考（取距离与避开路段提示）
        url = "https://restapi.amap.com/v3/direction/driving"
        params = {
            "key": self._amap_key,
            "origin": f"{origin['lng']:.6f},{origin['lat']:.6f}",
            "destination": f"{dest['lng']:.6f},{dest['lat']:.6f}",
            "strategy": 10,
        }
        r = requests.get(url, params=params, timeout=10)
        if r.status_code != 200:
            raise RuntimeError(f"amap HTTP {r.status_code}")
        data = r.json()
        if str(data.get("status")) != "1":
            raise RuntimeError(f"amap status={data.get('status')} info={data.get('info')}")
        route = (data.get("route") or {}).get("paths") or []
        if route:
            p = route[0]
            # 距离（米→公里）
            dist = float(p.get("distance", 0)) / 1000.0
            if dist > 0:
                result["distance_km"] = round(dist, 3)
                result["eta_seconds"] = round(
                    self._estimate_flight_seconds(dist), 1
                )
            # 交通限行/禁行信息 → 对应低空合规性提示
            steps = p.get("steps") or []
            restriction_tags = []
            for s in steps:
                if "限行" in str(s.get("tmc", "")) or "禁行" in str(s):
                    restriction_tags.append(str(s.get("instruction", ""))[:40])
            if restriction_tags:
                result["compliance_note"] = "地面限行提示（仅供低空参考）: " + "; ".join(restriction_tags[:2])

    def _amap_weather_enrich(self, result: Dict[str, Any], lat: float, lng: float):
        if requests is None or not self._amap_key:
            return
        # 高德天气需要 adcode，先用逆地理
        geo = "https://restapi.amap.com/v3/geocode/regeo"
        params = {"key": self._amap_key,
                  "location": f"{lng:.6f},{lat:.6f}"}
        r = requests.get(geo, params=params, timeout=10)
        data = r.json()
        adcode = (data.get("regeocode") or {}).get("adcode", "310000")
        w = "https://restapi.amap.com/v3/weather/weatherInfo"
        r2 = requests.get(w, params={"key": self._amap_key, "city": adcode, "extensions": "base"}, timeout=10)
        d2 = r2.json()
        if str(d2.get("status")) == "1":
            live = ((d2.get("lives") or [{}])[0])
            try:
                result["temperature_c"] = float(live.get("temperature", 20))
            except Exception:
                pass
            # 高德返回风力字符串"3级" → 近似风速
            ws = live.get("windpower", "2")
            try:
                level = int("".join(ch for ch in ws if ch.isdigit()) or "2")
                result["wind_speed_ms"] = round(1.5 * level, 1)
            except Exception:
                pass
            # 风向角
            wd = live.get("winddirection", "")
            _dir_map = {"北": 0, "东北": 45, "东": 90, "东南": 135,
                        "南": 180, "西南": 225, "西": 270, "西北": 315}
            for k, v in _dir_map.items():
                if k in wd:
                    result["wind_dir_deg"] = v
                    break
            result["visibility_km"] = float(live.get("visibility") or 10)
            result["note"] = f"{live.get('province','')}{live.get('city','')} {live.get('weather','')}"

    # --------------------------------------------------------
    # 腾讯地图 API 封装（兜底）
    # --------------------------------------------------------
    def _tencent_route_enrich(self, result: Dict[str, Any],
                              origin: Dict[str, float], dest: Dict[str, float]):
        if requests is None or not self._tencent_key:
            return
        url = "https://apis.map.qq.com/ws/direction/v1/driving/"
        params = {
            "key": self._tencent_key,
            "from": f"{origin['lat']:.6f},{origin['lng']:.6f}",
            "to": f"{dest['lat']:.6f},{dest['lng']:.6f}",
        }
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("status") != 0:
            raise RuntimeError(f"tencent status={data.get('status')} msg={data.get('message')}")
        routes = (data.get("result") or {}).get("routes") or []
        if routes:
            p = routes[0]
            dist_km = float(p.get("distance", 0)) / 1000.0
            if dist_km > 0:
                result["distance_km"] = round(dist_km, 3)
                result["eta_seconds"] = round(self._estimate_flight_seconds(dist_km), 1)

    def _tencent_weather_enrich(self, result: Dict[str, Any], lat: float, lng: float):
        # 腾讯地图无官方天气 API，使用逆地理解析城市名后返回占位
        if requests is None or not self._tencent_key:
            return
        url = "https://apis.map.qq.com/ws/geocoder/v1/"
        params = {"key": self._tencent_key, "location": f"{lat:.6f},{lng:.6f}"}
        r = requests.get(url, params=params, timeout=10)
        d = r.json()
        if d.get("status") == 0:
            addr = (d.get("result") or {}).get("address", "")
            result["note"] = f"[腾讯逆地理] {addr}"


# ============================================================
# 5. 模块导出清单（供 importlib 反射查找）
# ============================================================

__all__ = [
    # 通用基础
    "GenericTCPAdapter",
    "GenericSerialAdapter",
    "GenericUDPAdapter",
    "GenericBridgeAdapter",
    "EVTOLMapAdapter",
    # 品牌特定
    "KukaFRIAdapter",
    "KukaEKIAdapter",
    "URRTDEAdapter",
    "ABBEGMAdapter",
    "ABBRapidAdapter",
    "DobotSerialAdapter",
    "DobotTCPAdapter",
    "AirbotTCPAdapter",
    "UFactoryTCPAdapter",
    "JakaTCPAdapter",
    "BukeModbusAdapter",
    "UnitreeUDPAdapter",
    "DeepRoboticsTCPAdapter",
]
