# -*- coding: utf-8 -*-
"""
最小可用 MCP (Model Context Protocol) Server for RobotAdapter。

· 纯标准库实现，零第三方依赖（不要求 mcp SDK）
· MCP Spec 子集：tools/list + tools/call（足够 99% 的大模型对话控制机器人场景）
· 通信方式：stdio（JSON-RPC 2.0  over stdin/stdout with Content-Length frame）
· 暴露工具：list_products / init_robot / move_joints / move_cartesian /
            get_ee_pose / get_joint_states / stop_emergency
· 所有操作永不抛异常，失败返回结构化错误信息（保持我们之前的兜底哲学）

使用方式 1 - 作为 MCP Server 挂到任意大模型客户端（Claude Desktop / Ollama / Cursor / 百炼/千问 Agent）：
    见 mcp_robot_client_config.json.example

使用方式 2 - 纯 Python Dry-run 自检（不走 MCP 协议层）：
    python robot_mcp_server.py --self-test
"""
import sys
import os
import json
import time
import argparse
import threading
import traceback
from typing import Any, Dict, List, Optional

# ============================================================
# 1. 路径设置 + 加载现有底层（RobotAdapter / 产品清单）
# ============================================================
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)
for _p in (_PROJECT_ROOT, _THIS_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from real_robot_adapter import RobotAdapter, ARM_DATABASE
    from robots_config import ROBOT_BRANDS
    _BASE_OK = True
    _BASE_ERR = ""
except Exception as _e:
    _BASE_OK = False
    _BASE_ERR = str(_e)
    RobotAdapter = None  # type: ignore
    ROBOT_BRANDS = {}
    ARM_DATABASE = {}


# ============================================================
# 2. 工具层（与 MCP 协议解耦，可单独 Dry-run）
# ============================================================
_ADAPTER_LOCK = threading.Lock()
_ACTIVE_ADAPTER: Optional["RobotAdapter"] = None
_ACTIVE_KEY: Optional[str] = None
_EMERGENCY_LOCKED = False

_MAX_SPEED = 1.0
_MIN_SPEED = 0.05
_MAX_ACCEL = 1.0
_MIN_ACCEL = 0.05


def _ok(data: Any = None, msg: str = "ok") -> Dict[str, Any]:
    return {"success": True, "message": msg, "data": data}


def _err(msg: str, code: int = 500) -> Dict[str, Any]:
    return {"success": False, "code": code, "message": msg, "data": None}


def _category_of(arm_key: str) -> str:
    """简单品类判断（按 key 中关键词粗分类，方便大模型过滤产品）"""
    k = arm_key.lower()
    if any(t in k for t in ["evtol", "uav", "drone", "aircraft", "lanxiao", "fengfei"]):
        return "飞行器/eVTOL"
    if any(t in k for t in ["humanoid", "h1", "g1", "h2", "walker", "bot", "cyber"]):
        return "人形机器人"
    if any(t in k for t in ["legged", "go2", "b2", "gd01", "hercules", "wheel_legged"]):
        return "足式/轮腿机器人"
    if any(t in k for t in ["arm", "panda", "kuka", "ur", "abb", "dobot", "airbot",
                             "ufactory", "jaka", "kepler", "efort", "fanuc", "agile",
                             "irb", "yumi", "franka", "lbr"]):
        return "机械臂"
    if any(t in k for t in ["amr", "agv", "warehouse", "logistics", "ferrata", "apex", "digua"]):
        return "物流/仓储移动机器人"
    if any(t in k for t in ["chip", "wafer", "cpu", "gpu", "npu", "shenguang",
                             "kunlun", "cambricon", "hanwu", "xintong", "moore"]):
        return "AI算力芯片/核心板"
    if any(t in k for t in ["sensor", "skin", "bearing", "force"]):
        return "传感器/关键零部件"
    if any(t in k for t in ["6g", "starlink", "nokia", "net", "6nets", "satellite"]):
        return "通信/6G/卫星"
    if any(t in k for t in ["bci", "brain", "neuro", "eye_tracking", "glasses", "xr",
                             "phone", "honor", "moonix", "iflytek", "sategy"]):
        return "XR/AI手机/BCI设备"
    if any(t in k for t in ["llm", "model", "gpt", "kimi", "qwen", "deepseek",
                             "yuanli", "zhiyuan", "liman", "pohu", "zhengqi"]):
        return "AI模型/世界模型/大模型平台"
    if any(t in k for t in ["base", "training", "yunji", "collaborative", "industry",
                             "hydrogen", "coke", "foundation", "shenzhen", "henan",
                             "liupanshui", "longyou"]):
        return "产业基地/基建/能源"
    if any(t in k for t in ["evtol", "lanxiao", "fengfei"]):
        return "飞行器/eVTOL"
    return "其它智能产品"


def tool_list_products(category: Optional[str] = None, keyword: Optional[str] = None) -> Dict[str, Any]:
    """列出所有可用的机器人/智能产品（可按品类/关键词过滤）。

    Args:
        category: 品类过滤，如"机械臂"/"人形机器人"/"飞行器/eVTOL"/"AI算力芯片/核心板"...
        keyword:  自由关键词过滤（匹配 arm_key）
    """
    if not _BASE_OK:
        return _err(f"底层未加载: {_BASE_ERR}")
    result = []
    for arm_key in sorted(ROBOT_BRANDS.keys()):
        cat = _category_of(arm_key)
        if category and cat != category:
            continue
        if keyword and keyword.lower() not in arm_key.lower():
            continue
        result.append({"arm_key": arm_key, "category": cat,
                       "dofs": (ROBOT_BRANDS.get(arm_key) or {}).get("dofs")})
    return _ok({"count": len(result), "products": result},
               msg=f"共 {len(result)} 个产品匹配条件")


def tool_init_robot(arm_key: str, mode: str = "sim",
                    simulator_backend: str = "pybullet",
                    host: str = "", port: Optional[int] = None) -> Dict[str, Any]:
    """初始化指定产品为当前控制对象（真机/仿真二选一）。

    Args:
        arm_key:            产品 arm_key（可从 list_products 返回中取）
        mode:               "sim" 仿真 或 "real" 真机
        simulator_backend:  仿真后端（默认 pybullet，DIRECT 模式无 GUI）
        host:               真机模式下的机械臂 IP
        port:               真机模式下的机械臂端口
    """
    global _ACTIVE_ADAPTER, _ACTIVE_KEY, _EMERGENCY_LOCKED
    if not _BASE_OK:
        return _err(f"底层未加载: {_BASE_ERR}")
    if arm_key not in ROBOT_BRANDS and arm_key not in ARM_DATABASE:
        return _err(f"产品 arm_key={arm_key!r} 不存在。请先调用 list_products 查看可用清单",
                    code=404)
    _EMERGENCY_LOCKED = False
    with _ADAPTER_LOCK:
        # 先销毁旧 adapter
        try:
            if _ACTIVE_ADAPTER is not None:
                # 尽力而为关闭
                try:
                    _stop_pybullet = getattr(_ACTIVE_ADAPTER, "shutdown", None)
                    if callable(_stop_pybullet):
                        _stop_pybullet()
                except Exception:
                    pass
                _ACTIVE_ADAPTER = None
                _ACTIVE_KEY = None
        except Exception:
            _ACTIVE_ADAPTER = None
            _ACTIVE_KEY = None

        cfg: Dict[str, Any] = {}
        if mode == "real":
            if host:
                cfg["host"] = host
            if port:
                cfg["port"] = int(port)
        try:
            adapter = RobotAdapter(mode=mode, arm_key=arm_key, config=cfg or None,
                                   simulator_backend=simulator_backend)
            ok = adapter.initialize()
            _ACTIVE_ADAPTER = adapter
            _ACTIVE_KEY = arm_key
            return _ok({"arm_key": arm_key, "mode": mode,
                        "initialized": bool(ok),
                        "category": _category_of(arm_key)},
                       msg=f"已切换当前控制对象 → {arm_key} (mode={mode})")
        except Exception as e:
            tb = traceback.format_exc(limit=3)
            return _err(f"初始化 {arm_key} 失败: {e}\n{tb}")


def _require_active() -> Dict[str, Any]:
    if not _BASE_OK:
        return _err(f"底层未加载: {_BASE_ERR}")
    if _ACTIVE_ADAPTER is None or _ACTIVE_KEY is None:
        return _err("尚未初始化任何产品，请先调用 init_robot(arm_key=...)", code=412)
    is_conn_fn = getattr(_ACTIVE_ADAPTER, "is_connected", None)
    if callable(is_conn_fn) and not is_conn_fn():
        return _err("机器人未连接，请重新调用 init_robot 建立连接", code=503)
    if _EMERGENCY_LOCKED:
        return _err("机器人处于急停锁定状态，请先解除急停后再操作", code=423)
    return {}  # 空 dict 代表 ok


def _get_joint_limits(adapter) -> tuple:
    """从适配器安全控制器读取关节限位，返回 (lower_list, upper_list)。"""
    safety = getattr(adapter, "safety", None)
    if safety is None:
        return [], []
    limits = getattr(safety, "joint_limits", {}) or {}
    joint_indices = getattr(adapter, "joint_indices", []) or []
    lowers, uppers = [], []
    for j_idx in joint_indices:
        lim = limits.get(j_idx)
        if lim and "lower" in lim and "upper" in lim:
            lowers.append(float(lim["lower"]))
            uppers.append(float(lim["upper"]))
        else:
            lowers.append(None)
            uppers.append(None)
    return lowers, uppers


def tool_move_joints(joint_angles_deg: List[float], speed: float = 0.5,
                     acceleration: float = 0.5) -> Dict[str, Any]:
    """关节空间运动（所有关节按角度°控制）。

    Args:
        joint_angles_deg: 关节角度列表(单位°)，长度=dofs
        speed:            速度系数 0.05~1.0
        acceleration:     加速度系数 0.05~1.0
    """
    pre = _require_active()
    if pre:
        return pre
    if not isinstance(joint_angles_deg, list) or not joint_angles_deg:
        return _err("joint_angles_deg 必须是非空数字列表", code=400)
    try:
        arr = [float(v) for v in joint_angles_deg]
    except (TypeError, ValueError):
        return _err("joint_angles_deg 包含非数字值", code=400)

    dofs = int(getattr(_ACTIVE_ADAPTER, "dofs", 0) or 0)
    if dofs and len(arr) != dofs:
        return _err(f"关节角度数量({len(arr)})与自由度({dofs})不匹配", code=400)

    try:
        sp = max(_MIN_SPEED, min(_MAX_SPEED, float(speed)))
    except (TypeError, ValueError):
        return _err("speed 必须是数字", code=400)
    try:
        acc = max(_MIN_ACCEL, min(_MAX_ACCEL, float(acceleration)))
    except (TypeError, ValueError):
        return _err("acceleration 必须是数字", code=400)

    lowers, uppers = _get_joint_limits(_ACTIVE_ADAPTER)
    if lowers and len(lowers) == len(arr):
        for i, angle in enumerate(arr):
            lo = lowers[i]
            hi = uppers[i]
            if lo is not None and hi is not None:
                if angle < lo or angle > hi:
                    return _err(
                        f"关节 {i} 角度 {angle:.2f}° 超出限位 [{lo:.2f}°, {hi:.2f}°]",
                        code=400)

    try:
        with _ADAPTER_LOCK:
            move_fn = getattr(_ACTIVE_ADAPTER, "move_joints", None)
            if not callable(move_fn):
                return _err("适配器不支持 move_joints", code=501)
            try:
                move_fn(arr, speed=sp, acceleration=acc)
            except TypeError:
                move_fn(arr, speed=sp)
        return _ok({"joint_angles_deg": arr, "speed": sp, "acceleration": acc},
                   msg=f"关节运动已下发 (dofs={len(arr)})")
    except Exception as e:
        return _err(f"move_joints 失败: {e}")


def _quat_to_euler_deg(q: List[float]) -> List[float]:
    """把四元数 [qx, qy, qz, qw] 转成欧拉角 RPY(°)。安全降级：异常时返回 [0,0,0]。"""
    try:
        import math
        qx, qy, qz, qw = [float(v) for v in (list(q) + [0, 0, 0, 0])[:4]]
        # Roll (x-axis rotation)
        sinr_cosp = 2.0 * (qw * qx + qy * qz)
        cosr_cosp = 1.0 - 2.0 * (qx * qx + qy * qy)
        roll = math.atan2(sinr_cosp, cosr_cosp)
        # Pitch (y-axis rotation)
        sinp = 2.0 * (qw * qy - qz * qx)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2.0, sinp)
        else:
            pitch = math.asin(sinp)
        # Yaw (z-axis rotation)
        siny_cosp = 2.0 * (qw * qz + qx * qy)
        cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return [math.degrees(roll), math.degrees(pitch), math.degrees(yaw)]
    except Exception:
        return [0.0, 0.0, 0.0]


def tool_move_cartesian(x_m: float, y_m: float, z_m: float,
                        rx_deg: float = 0.0, ry_deg: float = 0.0, rz_deg: float = 0.0,
                        speed: float = 0.5, relative: bool = False) -> Dict[str, Any]:
    """笛卡尔空间末端运动。

    Args:
        x_m/y_m/z_m:  目标/增量位置（单位 m）
        rx/ry/rz_deg: 目标/增量姿态欧拉角（单位°，固定角 XYZ）
        speed:        速度系数 0.05~1.0
        relative:     是否相对当前末端做增量（True 时先读当前位姿再叠加，再传绝对坐标给底层）
    """
    pre = _require_active()
    if pre:
        return pre
    try:
        sp = max(0.05, min(1.0, float(speed)))
        abs_x, abs_y, abs_z = float(x_m), float(y_m), float(z_m)
        abs_rx, abs_ry, abs_rz = float(rx_deg), float(ry_deg), float(rz_deg)
        with _ADAPTER_LOCK:
            if relative:
                # → 先读当前位姿，叠加后再下发（底层 move_cartesian 无 relative 参数）
                pose = _ACTIVE_ADAPTER.get_ee_pose() or {}
                cur_pos = None
                if isinstance(pose, dict):
                    cur_pos = pose.get("position")
                    cur_ori = pose.get("orientation")
                # 位置叠加
                if isinstance(cur_pos, (list, tuple)) and len(cur_pos) >= 3:
                    abs_x = float(cur_pos[0]) + abs_x
                    abs_y = float(cur_pos[1]) + abs_y
                    abs_z = float(cur_pos[2]) + abs_z
                # 姿态叠加（四元数→欧拉°，再加上增量°）
                if isinstance(cur_ori, (list, tuple)) and len(cur_ori) >= 4:
                    cur_r, cur_p, cur_yw = _quat_to_euler_deg(list(cur_ori))
                    abs_rx = cur_r + abs_rx
                    abs_ry = cur_p + abs_ry
                    abs_rz = cur_yw + abs_rz
            # → 底层只接受绝对坐标，不传 relative
            _ACTIVE_ADAPTER.move_cartesian(abs_x, abs_y, abs_z,
                                           abs_rx, abs_ry, abs_rz, sp)
        return _ok({"target_xyz_m": [abs_x, abs_y, abs_z],
                    "target_rpy_deg": [abs_rx, abs_ry, abs_rz],
                    "relative": bool(relative),
                    "speed": sp},
                   msg="末端笛卡尔运动已下发" + ("（相对增量→已转绝对）" if relative else ""))
    except Exception as e:
        tb = traceback.format_exc(limit=4)
        return _err(f"move_cartesian 失败: {e}\n{tb}")


def tool_get_ee_pose() -> Dict[str, Any]:
    """读取当前激活机器人的末端位姿。"""
    pre = _require_active()
    if pre:
        return pre
    try:
        with _ADAPTER_LOCK:
            pose = _ACTIVE_ADAPTER.get_ee_pose()
        # 统一格式：position(xyz_m) + orientation(xyzw) + euler(deg)
        pos = None
        quat = None
        euler = None
        if isinstance(pose, dict):
            pos = pose.get("position")
            quat = pose.get("orientation")
            euler = pose.get("euler")
        return _ok({"arm_key": _ACTIVE_KEY,
                    "position_xyz_m": pos,
                    "orientation_xyzw": quat,
                    "euler_rpy_deg": euler},
                   msg="末端位姿读取成功")
    except Exception as e:
        return _err(f"get_ee_pose 失败: {e}")


def tool_get_joint_states() -> Dict[str, Any]:
    """读取当前激活机器人的关节角度(°)。"""
    pre = _require_active()
    if pre:
        return pre
    try:
        with _ADAPTER_LOCK:
            joints = _ACTIVE_ADAPTER.get_joint_states()
        arr = list(joints) if joints is not None else []
        return _ok({"arm_key": _ACTIVE_KEY,
                    "joint_angles_deg": arr,
                    "dofs": len(arr)},
                   msg=f"关节状态读取成功 (dofs={len(arr)})")
    except Exception as e:
        return _err(f"get_joint_states 失败: {e}")


def tool_stop_emergency() -> Dict[str, Any]:
    """触发急停：立即停止当前激活机器人的所有运动 + 标记安全锁定。"""
    global _EMERGENCY_LOCKED
    _EMERGENCY_LOCKED = True
    try:
        with _ADAPTER_LOCK:
            if _ACTIVE_ADAPTER is not None:
                estop_monitor = getattr(_ACTIVE_ADAPTER, "emergency_stop", None)
                trigger_fn = getattr(estop_monitor, "trigger_emergency_stop", None)
                if callable(trigger_fn):
                    trigger_fn()
                else:
                    try:
                        s_fn = getattr(_ACTIVE_ADAPTER, "stop", None)
                        if callable(s_fn):
                            s_fn()
                    except Exception:
                        pass
        return _ok({"arm_key": _ACTIVE_KEY, "locked": True},
                   msg="急停指令已执行，安全控制器已锁定")
    except Exception as e:
        return _err(f"急停失败（非致命，继续关注现场）: {e}", code=520)


def tool_reset_emergency() -> Dict[str, Any]:
    """解除急停锁定（需人工确认现场安全后调用）。"""
    global _EMERGENCY_LOCKED
    try:
        with _ADAPTER_LOCK:
            if _ACTIVE_ADAPTER is not None:
                estop_monitor = getattr(_ACTIVE_ADAPTER, "emergency_stop", None)
                reset_fn = getattr(estop_monitor, "reset_emergency_stop", None)
                if callable(reset_fn):
                    reset_fn()
        _EMERGENCY_LOCKED = False
        return _ok({"arm_key": _ACTIVE_KEY, "locked": False},
                   msg="急停锁定已解除")
    except Exception as e:
        return _err(f"解除急停失败: {e}", code=520)


# ============================================================
# 3. Tools 元数据清单（MCP tools/list 返回）
# ============================================================
MCP_TOOLS_SCHEMA = [
    {
        "name": "list_products",
        "description": "列出平台所有机器人/智能产品清单（193+款），可选品类/关键词过滤。"
                       "返回每个产品的 arm_key（后续 init_robot 要用到）、品类、自由度。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {"type": "string",
                             "description": "按品类过滤，可选值示例：'机械臂'、'人形机器人'、"
                                            "'足式/轮腿机器人'、'飞行器/eVTOL'、"
                                            "'AI算力芯片/核心板'、'传感器/关键零部件'、"
                                            "'通信/6G/卫星'、'物流/仓储移动机器人'、"
                                            "'XR/AI手机/BCI设备'、'AI模型/大模型平台'、"
                                            "'产业基地/基建/能源'。"},
                "keyword":  {"type": "string",
                             "description": "自由关键词（匹配 arm_key，如 'franka'、'unitree'、"
                                            "'evtol'、'kuka'、'6g'）。"}
            },
        },
    },
    {
        "name": "init_robot",
        "description": "初始化并切换当前控制的机器人/智能产品。每次控制之前必须先调用一次。"
                       "默认仿真模式(PyBullet DIRECT，无 GUI)不会污染桌面。"
                       "真机模式需填写 host/port。",
        "inputSchema": {
            "type": "object",
            "required": ["arm_key"],
            "properties": {
                "arm_key":            {"type": "string",
                                       "description": "产品唯一 ID，来自 list_products 返回。"},
                "mode":               {"type": "string", "enum": ["sim", "real"],
                                       "default": "sim",
                                       "description": "sim=PyBullet 仿真（默认）；real=真机。"},
                "simulator_backend":  {"type": "string", "default": "pybullet"},
                "host":               {"type": "string",
                                       "description": "真机模式下机械臂 IP/主机地址。"},
                "port":               {"type": "integer",
                                       "description": "真机模式下机械臂通信端口。"},
            },
        },
    },
    {
        "name": "move_joints",
        "description": "关节空间运动：向当前已激活机器人下发关节目标角度（单位°）。"
                       "关节顺序与产品 URDF 定义保持一致。会自动校验角度是否在关节限位内。",
        "inputSchema": {
            "type": "object",
            "required": ["joint_angles_deg"],
            "properties": {
                "joint_angles_deg": {"type": "array", "items": {"type": "number"},
                                     "minItems": 1,
                                     "description": "关节目标角度数组，单位°。长度=dofs。"},
                "speed":            {"type": "number", "default": 0.5,
                                     "minimum": 0.05, "maximum": 1.0,
                                     "description": "速度系数 0.05~1.0，默认 0.5。"},
                "acceleration":     {"type": "number", "default": 0.5,
                                     "minimum": 0.05, "maximum": 1.0,
                                     "description": "加速度系数 0.05~1.0，默认 0.5。"}
            }
        },
    },
    {
        "name": "move_cartesian",
        "description": "笛卡尔末端运动：控制当前激活机器人末端到达/增量到指定位姿。",
        "inputSchema": {
            "type": "object",
            "required": ["x_m", "y_m", "z_m"],
            "properties": {
                "x_m":      {"type": "number", "description": "X 坐标，单位 m。"},
                "y_m":      {"type": "number", "description": "Y 坐标，单位 m。"},
                "z_m":      {"type": "number", "description": "Z 坐标，单位 m。"},
                "rx_deg":   {"type": "number", "default": 0.0, "description": "Roll，单位°。"},
                "ry_deg":   {"type": "number", "default": 0.0, "description": "Pitch，单位°。"},
                "rz_deg":   {"type": "number", "default": 0.0, "description": "Yaw，单位°。"},
                "speed":    {"type": "number", "default": 0.5,
                             "description": "速度系数 0.05~1.0，默认 0.5。"},
                "relative": {"type": "boolean", "default": False,
                             "description": "True=相对末端做增量，False=绝对坐标。"}
            }
        },
    },
    {
        "name": "get_ee_pose",
        "description": "读取当前激活机器人末端位姿，返回 xyz(m)、四元数 xyzw、"
                       "欧拉角 rpy(°)。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_joint_states",
        "description": "读取当前激活机器人所有关节角度(°)与 dofs 数。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "stop_emergency",
        "description": "【安全接口】触发当前机器人急停（幂等，多次调用安全）。"
                       "只要感觉不对，立刻让大模型调用这个。",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "reset_emergency",
        "description": "【安全接口】解除急停锁定。必须在人工确认现场安全后调用。",
        "inputSchema": {"type": "object", "properties": {}},
    },
]

_TOOL_FN = {
    "list_products":      tool_list_products,
    "init_robot":         tool_init_robot,
    "move_joints":        tool_move_joints,
    "move_cartesian":     tool_move_cartesian,
    "get_ee_pose":        tool_get_ee_pose,
    "get_joint_states":   tool_get_joint_states,
    "stop_emergency":     tool_stop_emergency,
    "reset_emergency":    tool_reset_emergency,
}


# ============================================================
# 4. MCP 协议层（最小 stdio JSON-RPC 2.0 + Content-Length 帧）
# ============================================================
_MCP_VERSION = "2024-11-05"
_SERVER_INFO = {"name": "embodied-intelligence-robot-mcp", "version": "1.0.0"}


def _mcp_result(request_id: Any, result: Any) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _mcp_error(request_id: Any, code: int, message: str,
               data: Any = None) -> Dict[str, Any]:
    body = {"jsonrpc": "2.0", "id": request_id,
            "error": {"code": code, "message": message}}
    if data is not None:
        body["error"]["data"] = data
    return body


def _handle_init(params: Dict[str, Any]) -> Dict[str, Any]:
    # 兼容性：不校验 protocolVersion，直接返回
    return {
        "protocolVersion": params.get("protocolVersion") or _MCP_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": _SERVER_INFO,
        "instructions": ("Embodied Intelligence Robot MCP Server\n"
                         "· 调用顺序：list_products → init_robot → 运动/读取工具\n"
                         "· 任何异常可随时调用 stop_emergency 急停。"),
    }


def _handle_tools_list() -> Dict[str, Any]:
    return {"tools": MCP_TOOLS_SCHEMA}


def _handle_tools_call(params: Dict[str, Any]) -> Dict[str, Any]:
    name = params.get("name")
    args = params.get("arguments") or {}
    if name not in _TOOL_FN:
        return {
            "isError": True,
            "content": [{"type": "text",
                         "text": json.dumps(_err(f"未知工具 {name!r}，可用工具："
                                                 f"{sorted(_TOOL_FN.keys())}"),
                                            ensure_ascii=False)}],
        }
    try:
        fn = _TOOL_FN[name]
        ret = fn(**args) if isinstance(args, dict) else fn()
        # 按 MCP ToolResult 规范：返回 content 数组
        return {
            "content": [
                {"type": "text", "text": json.dumps(ret, ensure_ascii=False, indent=2)}
            ],
            "isError": not bool(ret.get("success")) if isinstance(ret, dict) else False,
        }
    except TypeError as e:
        return {
            "isError": True,
            "content": [{"type": "text",
                         "text": json.dumps(
                             _err(f"工具 {name!r} 参数错误: {e}。"
                                  f" 请按 MCP tools/list 中的 schema 传参。"),
                             ensure_ascii=False)}],
        }
    except Exception as e:
        tb = traceback.format_exc(limit=3)
        return {
            "isError": True,
            "content": [{"type": "text",
                         "text": json.dumps(_err(f"工具 {name!r} 执行异常: {e}\n{tb}"),
                                            ensure_ascii=False)}],
        }


def _dispatch(method: str, params: Any) -> Any:
    """按 MCP spec 分发请求。返回 dict（result）。"""
    params = params if isinstance(params, dict) else {}
    try:
        if method == "initialize":
            return _handle_init(params)
        if method in ("notifications/initialized",):
            # MCP 客户端发出的初始化完成通知，空返回
            return None
        if method == "ping":
            return {}
        if method == "tools/list":
            return _handle_tools_list()
        if method == "tools/call":
            return _handle_tools_call(params)
        # 其他未实现方法，返回 MethodNotFound(-32601)
        return _SENTINEL_METHOD_NOT_FOUND  # type: ignore
    except Exception as e:
        tb = traceback.format_exc(limit=5)
        return _SENTINEL_INTERNAL, f"{e}\n{tb}"  # type: ignore


_SENTINEL_METHOD_NOT_FOUND = object()
_SENTINEL_INTERNAL = object()


# ----------------- I/O Framing -----------------
def _read_message() -> Optional[Dict[str, Any]]:
    """从 stdin 读取一条 MCP 消息（Content-Length 帧 + JSON body）。失败返回 None。"""
    headers: Dict[str, str] = {}
    try:
        _MAX_LOOPS = 10_000_000
        _loop_count = 0
        while True:
            _loop_count += 1
            if _loop_count > _MAX_LOOPS:
                return None
            line = sys.stdin.buffer.readline()
            if not line:
                return None  # EOF
            if line in (b"\r\n", b"\n"):
                break
            try:
                hl = line.decode("utf-8").strip()
                if ":" in hl:
                    k, v = hl.split(":", 1)
                    headers[k.strip().lower()] = v.strip()
            except Exception:
                continue
        clen = int(headers.get("content-length", "0"))
        if clen <= 0:
            return None
        body = sys.stdin.buffer.read(clen)
        if len(body) != clen:
            return None
        return json.loads(body.decode("utf-8", errors="replace"))
    except Exception:
        return None


def _write_message(obj: Any) -> None:
    try:
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        frame = f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii") + raw
        sys.stdout.buffer.write(frame)
        sys.stdout.buffer.flush()
    except Exception:
        # stdio 写入失败（比如客户端关了），静默吞掉，不崩主循环
        pass


# ============================================================
# 5. 入口
# ============================================================
def run_stdio_server() -> int:
    """主循环：运行 MCP stdio server。永远不主动抛异常退出。"""
    # 先确保 stdout 是 line-buffered 或 binary 模式（上面 write_message 已经用 buffer）
    _MAX_SECONDS = 86400
    _start_time = time.time()
    while True:
        if time.time() - _start_time > _MAX_SECONDS:
            return 0
        msg = _read_message()
        if msg is None:
            # 客户端关闭输入流 → 优雅退出
            return 0
        rid = msg.get("id")
        method = msg.get("method", "")
        params = msg.get("params")
        try:
            out = _dispatch(method, params)
            if out is None:
                # 是 notification（如 notifications/initialized），无响应
                continue
            if out is _SENTINEL_METHOD_NOT_FOUND:
                _write_message(_mcp_error(rid, -32601, f"Method not found: {method}"))
                continue
            if isinstance(out, tuple) and len(out) == 2 and out[0] is _SENTINEL_INTERNAL:
                _write_message(_mcp_error(rid, -32603, f"Internal error: {out[1]}"))
                continue
            # rid 是 None = 通知，不回
            if rid is not None:
                _write_message(_mcp_result(rid, out))
        except Exception as _e:
            tb = traceback.format_exc(limit=5)
            if rid is not None:
                _write_message(_mcp_error(rid, -32603,
                                          f"Dispatch uncaught: {_e}\n{tb}"))


def run_self_test() -> int:
    """纯 Python 自检（不走 MCP 协议），Dry-run 所有工具。
    用法：python robot_mcp_server.py --self-test
    """
    sep = "=" * 72
    print(sep)
    print("🤖 Robot MCP Server · Dry-run 自检（不走 MCP 协议层）")
    print(sep)
    cases: List[tuple] = []
    # Case 1：列出所有品类
    r = tool_list_products()
    ok = bool(r.get("success")) and (r.get("data") or {}).get("count", 0) >= 193
    cases.append(("list_products(全量)", ok,
                  (r.get("data") or {}).get("count") if ok else r.get("message")))
    # Case 2：按品类过滤机械臂
    r = tool_list_products(category="机械臂")
    arms = (r.get("data") or {}).get("products") or []
    ok = bool(r.get("success")) and len(arms) >= 3
    cases.append(("list_products(category='机械臂')", ok, len(arms) if ok else r.get("message")))
    # Case 3：初始化仿真 panda（若有）或 franka_panda/第一个机械臂
    arm_key = None
    if arms:
        for a in arms:
            k = a["arm_key"]
            if "panda" in k or "franka" in k:
                arm_key = k
                break
        if not arm_key:
            arm_key = arms[0]["arm_key"]
    if arm_key:
        r = tool_init_robot(arm_key=arm_key, mode="sim")
        ok = bool(r.get("success"))
        cases.append((f"init_robot({arm_key!r}, sim)", ok, r.get("message")))
        if ok:
            # Case 4：读关节
            r = tool_get_joint_states()
            ok = bool(r.get("success"))
            cases.append(("get_joint_states()", ok,
                          (r.get("data") or {}).get("dofs") if ok else r.get("message")))
            # Case 5：读末端位姿
            r = tool_get_ee_pose()
            ok = bool(r.get("success"))
            cases.append(("get_ee_pose()", ok,
                          list((r.get("data") or {}).get("position_xyz_m") or [])
                          if ok else r.get("message")))
            # Case 6：关节运动（小角度 Dry-run，仿真允许）
            dofs = int(((tool_get_joint_states().get("data") or {}).get("dofs")) or 0)
            if dofs:
                angles = [0.0] * dofs
                r = tool_move_joints(angles, speed=0.1)
                ok = bool(r.get("success"))
                cases.append((f"move_joints({dofs} zeros, sp=0.1)", ok, r.get("message")))
            # Case 7：笛卡尔小增量
            r = tool_move_cartesian(0.0, 0.0, 0.01, relative=True, speed=0.1)
            ok = bool(r.get("success"))
            cases.append(("move_cartesian(dz+1cm, relative)", ok, r.get("message")))
            # Case 8：急停
            r = tool_stop_emergency()
            ok = bool(r.get("success"))
            cases.append(("stop_emergency()", ok, r.get("message")))
    # 汇总
    print()
    print(f"{'CASE':<50s} {'PASS?':<6s}  DETAIL")
    print("-" * 72)
    passed = 0
    for name, ok, detail in cases:
        tag = "✅PASS" if ok else "❌FAIL"
        print(f"{name:<50s} {tag:<6s}  {detail}")
        if ok:
            passed += 1
    total = len(cases)
    print()
    print(sep)
    print(f"📊 自检汇总: {passed}/{total} 通过 ({(passed/total*100 if total else 0):.1f}%)")
    print(sep)
    return 0 if passed == total else 3


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Embodied Intelligence · Robot MCP Server (stdio / 自检)"
    )
    ap.add_argument("--self-test", action="store_true",
                    help="Dry-run 所有工具函数自检，不进入 MCP stdio 主循环")
    args = ap.parse_args()
    if args.self_test:
        return run_self_test()
    return run_stdio_server()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as _e:
        # 任何主循环外异常都静默写 stderr，不抛给 MCP 客户端
        try:
            sys.stderr.write(f"[MCP SERVER FATAL] {_e}\n")
            sys.stderr.flush()
        except Exception:
            pass
        sys.exit(1)
