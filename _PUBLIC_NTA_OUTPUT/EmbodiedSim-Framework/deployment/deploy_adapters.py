"""
通信适配器抽象层（框架版）
================================================
定义「仿真/真机」统一通信接口，支持：
  - TCP / UDP 网络协议
  - CAN / EtherCAT 工业总线
  - ROS1 / ROS2 机器人中间件
  - Modbus PLC设备接入

说明：本文件展示「多协议通信适配」的抽象设计模式，
      不包含任何真实IP、端口、企业私有协议参数。
"""

from __future__ import annotations

import abc
import time
import socket
import threading
import struct
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


# ============================================================
# 协议枚举 & 消息包
# ============================================================
class CommProtocol:
    TCP = "tcp"
    UDP = "udp"
    CAN = "can"
    ETHERCAT = "ethercat"
    ROS1 = "ros1"
    ROS2 = "ros2"
    MODBUS = "modbus"
    MOCK = "mock"

    ALL_NETWORK = (TCP, UDP)
    ALL_BUS = (CAN, ETHERCAT, MODBUS)
    ALL_MIDDLEWARE = (ROS1, ROS2)


@dataclass
class CommConfig:
    """通信配置模板（示例值，无真实敏感地址）"""
    protocol: str = CommProtocol.MOCK
    host: str = "127.0.0.1"
    port: int = 5000
    timeout_s: float = 2.0
    auto_reconnect: bool = True
    reconnect_interval_s: float = 3.0
    # CAN/总线类
    channel: str = "can0"
    bitrate: int = 1000000
    # ROS类
    node_name: str = "embodied_comm_node"
    master_uri: str = "http://127.0.0.1:11311"
    # 调试
    verbose: bool = False


@dataclass
class CommPacket:
    """统一通信包格式（跨协议通用）"""
    packet_id: int = 0
    source: str = ""
    target: str = ""
    data_type: str = "raw"    # raw / json / joint_cmd / robot_state
    payload: bytes = b""
    timestamp_s: float = field(default_factory=time.time)

    def payload_json(self) -> Dict[str, Any]:
        import json
        if self.data_type == "json":
            return json.loads(self.payload.decode("utf-8"))
        return {"raw_hex": self.payload.hex()}


# ============================================================
# 适配器抽象基类
# ============================================================
class CommunicationAdapter(abc.ABC):
    """通信适配器统一抽象接口（所有协议都实现这个接口）"""

    protocol_name: str = "abstract"

    def __init__(self, config: Optional[CommConfig] = None):
        self.cfg = config or CommConfig()
        self._connected: bool = False
        self._rx_callbacks: List[Callable[[CommPacket], None]] = []
        self._stats = {"tx": 0, "rx": 0, "tx_bytes": 0, "rx_bytes": 0,
                       "errors": 0, "reconnects": 0,
                       "connected_at": 0.0, "last_rx_at": 0.0}

    # ---- 基础生命周期 ----
    @abc.abstractmethod
    def connect(self) -> bool:
        """建立连接 / 打开通道"""
        raise NotImplementedError

    @abc.abstractmethod
    def disconnect(self) -> None:
        """断开连接 / 关闭通道"""
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, packet: CommPacket) -> bool:
        """发送数据包（同步阻塞，返回是否成功）"""
        raise NotImplementedError

    @abc.abstractmethod
    def recv(self, timeout_s: Optional[float] = None) -> Optional[CommPacket]:
        """尝试接收一个数据包（None=超时/无数据）"""
        raise NotImplementedError

    # ---- 通用辅助方法 ----
    @property
    def connected(self) -> bool:
        return self._connected

    def on_receive(self, callback: Callable[[CommPacket], None]) -> None:
        """注册接收回调（推荐用于异步/守护线程模式）"""
        self._rx_callbacks.append(callback)

    def _dispatch_rx(self, pkt: CommPacket) -> None:
        self._stats["rx"] += 1
        self._stats["rx_bytes"] += len(pkt.payload)
        self._stats["last_rx_at"] = time.time()
        for cb in list(self._rx_callbacks):
            try:
                cb(pkt)
            except Exception as e:
                self._stats["errors"] += 1
                print(f"[Comm/{self.protocol_name}] RX回调异常: {e}")

    def get_stats(self) -> Dict[str, Any]:
        return {
            "protocol": self.protocol_name,
            "connected": self._connected,
            **self._stats,
            "uptime_s": (time.time() - self._stats["connected_at"])
            if self._connected and self._stats["connected_at"] else 0.0,
        }

    def start_daemon(self) -> threading.Thread:
        """启动守护线程循环接收，自动调用 on_receive 回调"""
        def _loop():
            while self._connected:
                try:
                    pkt = self.recv(timeout_s=0.2)
                    if pkt is not None:
                        self._dispatch_rx(pkt)
                except Exception as e:
                    self._stats["errors"] += 1
                    if self.cfg.verbose:
                        print(f"[Comm/{self.protocol_name}] RX循环异常: {e}")
                    time.sleep(0.2)
        t = threading.Thread(target=_loop, name=f"comm_{self.protocol_name}_daemon",
                             daemon=True)
        t.start()
        return t

    # ---- 上下文管理器 ----
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__} protocol={self.protocol_name} "
                f"connected={self._connected} stats={self.get_stats()}>")


# ============================================================
# Mock适配器（公共示例默认，用于无硬件时的系统联调）
# ============================================================
class MockCommunicationAdapter(CommunicationAdapter):
    """
    Mock通信适配器
    ------------------------------------------------
    行为：
      send() -> 直接写入内部队列，模拟已成功发出
      recv() -> 从队列取数据包 + 可注入模拟上行数据
    """
    protocol_name = CommProtocol.MOCK

    def __init__(self, config: Optional[CommConfig] = None):
        super().__init__(config or CommConfig(protocol=CommProtocol.MOCK))
        import queue
        self._q: "queue.Queue[CommPacket]" = queue.Queue()
        self._loopback_enabled = True   # 默认开启回环：发送的自己也能收到（便于联调）

    def connect(self) -> bool:
        if self._connected:
            return True
        self._connected = True
        self._stats["connected_at"] = time.time()
        if self.cfg.verbose:
            print(f"[Comm/MOCK] 已连接（Mock模式，不访问真实网络）")
        return True

    def disconnect(self) -> None:
        self._connected = False
        if self.cfg.verbose:
            print(f"[Comm/MOCK] 已断开")

    def send(self, packet: CommPacket) -> bool:
        if not self._connected:
            return False
        self._stats["tx"] += 1
        self._stats["tx_bytes"] += len(packet.payload)
        if self._loopback_enabled:
            self._q.put(packet)
        return True

    def recv(self, timeout_s: Optional[float] = None) -> Optional[CommPacket]:
        import queue as _q
        try:
            return self._q.get(timeout=(timeout_s or self.cfg.timeout_s))
        except _q.Empty:
            return None

    def inject_incoming(self, pkt: CommPacket) -> None:
        """测试用：手动注入一个「接收到」的数据包"""
        self._q.put(pkt)


# ============================================================
# TCP / UDP 适配器（展示通用网络编程模式，无真实私有IP）
# ============================================================
class TCPCommunicationAdapter(CommunicationAdapter):
    """TCP适配器（Client模式，展示标准socket编程模板）"""
    protocol_name = CommProtocol.TCP

    def __init__(self, config: Optional[CommConfig] = None):
        cfg = config or CommConfig(protocol=CommProtocol.TCP)
        super().__init__(cfg)
        self._sock: Optional[socket.socket] = None

    def connect(self) -> bool:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.cfg.timeout_s)
            s.connect((self.cfg.host, self.cfg.port))
            self._sock = s
            self._connected = True
            self._stats["connected_at"] = time.time()
            return True
        except socket.error as e:
            print(f"[Comm/TCP] 连接失败: {e}（如只是演示框架请使用Mock适配器）")
            self._sock = None
            return False

    def disconnect(self) -> None:
        self._connected = False
        if self._sock:
            try:
                self._sock.close()
            finally:
                self._sock = None

    def send(self, packet: CommPacket) -> bool:
        if not self._sock:
            return False
        try:
            header = struct.pack("!II", packet.packet_id & 0xFFFFFFFF,
                                 len(packet.payload))
            self._sock.sendall(header + packet.payload)
            self._stats["tx"] += 1
            self._stats["tx_bytes"] += len(packet.payload)
            return True
        except socket.error:
            self._stats["errors"] += 1
            self._connected = False
            return False

    def recv(self, timeout_s: Optional[float] = None) -> Optional[CommPacket]:
        if not self._sock:
            return None
        try:
            self._sock.settimeout(timeout_s or self.cfg.timeout_s)
            header = b""
            while len(header) < 8:
                chunk = self._sock.recv(8 - len(header))
                if not chunk:
                    self._connected = False
                    return None
                header += chunk
            pkt_id, plen = struct.unpack("!II", header)
            body = b""
            while len(body) < plen:
                chunk = self._sock.recv(plen - len(body))
                if not chunk:
                    self._connected = False
                    return None
                body += chunk
            return CommPacket(packet_id=pkt_id, payload=body)
        except socket.timeout:
            return None
        except socket.error:
            self._stats["errors"] += 1
            self._connected = False
            return None


# ============================================================
# 适配器工厂（展示工厂模式 + 协议注册表）
# ============================================================
class AdapterFactory:
    """
    通信适配器工厂
    ------------------------------------------------
    使用：
        >>> cfg = CommConfig(protocol="mock")
        >>> adapter = AdapterFactory.create(cfg)
        >>> adapter.connect()
    """
    _REGISTRY: Dict[str, Any] = {
        CommProtocol.MOCK: MockCommunicationAdapter,
        CommProtocol.TCP: TCPCommunicationAdapter,
        # 其他协议：预留扩展点（接入真机时注册实现）
        # CommProtocol.UDP: UDPCommunicationAdapter,
        # CommProtocol.CAN: SocketCANAdapter,
        # CommProtocol.ETHERCAT: EtherlabIgHAdapter,
        # CommProtocol.MODBUS: ModbusTcpAdapter,
        # CommProtocol.ROS1: Ros1BridgeAdapter,
        # CommProtocol.ROS2: Ros2BridgeAdapter,
    }

    @classmethod
    def register(cls, protocol: str, impl_cls: Any) -> None:
        cls._REGISTRY[protocol] = impl_cls

    @classmethod
    def supported(cls) -> List[str]:
        return sorted(cls._REGISTRY.keys())

    @classmethod
    def create(cls, config: CommConfig) -> CommunicationAdapter:
        impl = cls._REGISTRY.get(config.protocol)
        if impl is None:
            raise NotImplementedError(
                f"协议 [{config.protocol}] 暂未实现（已支持: {cls.supported()}）。"
                f"公共示例版推荐使用 mock 模式进行框架联调。"
            )
        return impl(config)


# ============================================================
# 快捷入口
# ============================================================
def build_adapter(
    protocol: str = "mock",
    host: str = "127.0.0.1",
    port: int = 5000,
    verbose: bool = False,
) -> CommunicationAdapter:
    cfg = CommConfig(protocol=protocol, host=host, port=port, verbose=verbose)
    return AdapterFactory.create(cfg)
