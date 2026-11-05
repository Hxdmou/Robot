"""
安全控制器 & 碰撞检测（框架版）
================================================
展示工程级安全防护 5 层设计：
  1. 输入合法性校验（范围/类型/频率限流）
  2. 工作空间限制（关节限位 / 笛卡尔空间软围栏）
  3. 碰撞检测接口（与仿真或外部传感器对接）
  4. 速度/加速度软限制
  5. 紧急停止 + 异常熔断 + 日志审计

说明：本文件为安全框架层实现，不含任何品牌相关参数，
      不涉及算法公式推导。
"""

from __future__ import annotations

import math
import time
import threading
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple, Any


# ============================================================
# 安全事件类型
# ============================================================
class SafetyEventType:
    INPUT_INVALID = "input_invalid"
    JOINT_LIMIT = "joint_limit"
    WORKSPACE_LIMIT = "workspace_limit"
    VELOCITY_LIMIT = "velocity_limit"
    ACCELERATION_LIMIT = "acceleration_limit"
    TORQUE_LIMIT = "torque_limit"
    COLLISION_DETECTED = "collision_detected"
    EMERGENCY_STOP = "emergency_stop"
    FUSE_TRIGGERED = "fuse_triggered"
    HEARTBEAT_LOST = "heartbeat_lost"


@dataclass
class SafetyEvent:
    event_type: str
    severity: str                 # INFO / WARN / CRITICAL
    source: str
    message: str
    timestamp_s: float = field(default_factory=time.time)
    extra: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return (f"[Safety {self.severity}] {self.source} :: {self.event_type} "
                f"- {self.message}")


# ============================================================
# 碰撞检测抽象层
# ============================================================
class CollisionDetector:
    """
    碰撞检测抽象接口
    ------------------------------------------------
    可对接多种实现：
      - 基于PyBullet/MuJoCo的几何距离检测
      - 基于关节力矩残差的外部碰撞判断
      - 基于触觉/皮肤传感器的物理接触
      - 基于深度相机的人体入侵检测
    本文件提供「最近距离阈值」通用参考实现 + Mock版本。
    """

    def __init__(self, threshold_m: float = 0.05):
        self.threshold_m = threshold_m
        self._last_check_ts: float = 0.0
        self._last_min_distance: float = 999.0
        self._enabled: bool = True
        self._events: List[SafetyEvent] = []

    # ---- 开关 ----
    @property
    def enabled(self) -> bool:
        return self._enabled

    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    # ---- 核心方法（子类实现具体检测） ----
    def _compute_min_distance(self, *args, **kwargs) -> float:
        """子类重写：返回当前环境的最近障碍物距离（米）"""
        return 999.0  # 默认：无碰撞风险

    def check_collision(self, *args, **kwargs) -> Tuple[bool, float]:
        """
        检查是否发生碰撞或接近碰撞
        :return: (是否触发, 最近距离米)
        """
        if not self._enabled:
            return False, 999.0
        dist = self._compute_min_distance(*args, **kwargs)
        self._last_check_ts = time.time()
        self._last_min_distance = dist
        triggered = dist <= self.threshold_m
        if triggered:
            self._events.append(SafetyEvent(
                event_type=SafetyEventType.COLLISION_DETECTED,
                severity="CRITICAL",
                source=self.__class__.__name__,
                message=f"最近障碍物距离={dist*1000:.2f}mm，阈值={self.threshold_m*1000:.2f}mm",
                extra={"distance_m": dist, "threshold_m": self.threshold_m},
            ))
        return triggered, dist

    @property
    def status(self) -> Dict[str, Any]:
        return {
            "enabled": self._enabled,
            "threshold_m": self.threshold_m,
            "last_check_ts": self._last_check_ts,
            "last_min_distance_m": self._last_min_distance,
            "events_total": len(self._events),
        }


class MockCollisionDetector(CollisionDetector):
    """
    Mock版碰撞检测器：通过注入触发距离来模拟场景
    ------------------------------------------------
    作用：在无仿真/无硬件条件下，让安全控制器能完整联调。
    """

    def __init__(self, threshold_m: float = 0.05,
                 initial_distance_m: float = 0.50):
        super().__init__(threshold_m=threshold_m)
        self._sim_distance = initial_distance_m

    def set_simulated_distance(self, distance_m: float) -> None:
        """模拟当前环境最小障碍物距离"""
        self._sim_distance = max(0.0, distance_m)

    def _compute_min_distance(self, *args, **kwargs) -> float:
        return self._sim_distance


# ============================================================
# 安全控制器（5层防护总装）
# ============================================================
class SafetyController:
    """
    安全控制器（核心防护总装类）
    ------------------------------------------------
    对外能力：
      - validate_command(command): 校验一次动作指令是否合法
      - on_safety_event(fn):       订阅安全事件回调
      - trigger_emergency_stop():  主动触发紧急停止
      - reset_fuses():             故障排除后复位熔断器
    """

    def __init__(
        self,
        robot_type: str = "panda",
        num_joints: int = 7,
        joint_lower: Optional[List[float]] = None,
        joint_upper: Optional[List[float]] = None,
        velocity_limit_rad_s: float = 2.0,
        acceleration_limit_rad_s2: float = 5.0,
        torque_limit_nm: Optional[List[float]] = None,
        cartesian_workspace: Optional[Dict[str, Tuple[float, float]]] = None,
        collision_detector: Optional[CollisionDetector] = None,
    ):
        self.robot_type = robot_type
        self.num_joints = num_joints
        self.joint_lower = joint_lower or [-math.pi] * num_joints
        self.joint_upper = joint_upper or [ math.pi] * num_joints
        self.velocity_limit = velocity_limit_rad_s
        self.acceleration_limit = acceleration_limit_rad_s2
        self.torque_limit = torque_limit or [50.0] * num_joints
        self.workspace = cartesian_workspace or {
            "x": (-0.5,  1.2),
            "y": (-0.8,  0.8),
            "z": (-0.1,  1.5),
        }
        self.collision = collision_detector or MockCollisionDetector()
        self._last_joint_pos: List[float] = [0.0] * num_joints
        self._last_joint_vel: List[float] = [0.0] * num_joints
        self._last_ts: float = time.time()
        self._estop_engaged: bool = False
        self._fuse_blown: bool = False
        self._events: List[SafetyEvent] = []
        self._callbacks: List[Callable[[SafetyEvent], None]] = []
        self._max_command_rate_hz: int = 2000
        self._cmd_timestamps: List[float] = []
        self._lock = threading.RLock()

        if len(self.joint_lower) != num_joints or len(self.joint_upper) != num_joints:
            raise ValueError(
                f"关节限位数组长度不匹配: num_joints={num_joints}, "
                f"lower={len(self.joint_lower)}, upper={len(self.joint_upper)}"
            )
        if len(self.torque_limit) != num_joints:
            raise ValueError(
                f"力矩限制数组长度不匹配: num_joints={num_joints}, "
                f"torque_limit={len(self.torque_limit)}"
            )

        self._emit(SafetyEvent(event_type="SYSTEM_READY", severity="INFO",
                               source="SafetyController",
                               message=f"安全控制器就绪 | robot={robot_type} joints={num_joints}"))

    # ---- 事件系统 ----
    def on_safety_event(self, callback: Callable[[SafetyEvent], None]) -> None:
        self._callbacks.append(callback)

    def _emit(self, event: SafetyEvent) -> None:
        self._events.append(event)
        for cb in list(self._callbacks):
            try:
                cb(event)
            except Exception:
                pass  # 回调异常不影响安全主流程

    # ---- 各层校验实现 ----
    def _chk_input_type(self, joints: Any) -> Optional[SafetyEvent]:
        if not isinstance(joints, (list, tuple)):
            return SafetyEvent(SafetyEventType.INPUT_INVALID, "CRITICAL",
                               "InputValidator", "关节指令必须是list/tuple，收到: " + str(type(joints)))
        if len(joints) != self.num_joints:
            return SafetyEvent(SafetyEventType.INPUT_INVALID, "CRITICAL",
                               "InputValidator",
                               f"关节数量不匹配：期望{self.num_joints}，实际{len(joints)}")
        for i, v in enumerate(joints):
            if not isinstance(v, (int, float)) or math.isnan(v) or math.isinf(v):
                return SafetyEvent(SafetyEventType.INPUT_INVALID, "CRITICAL",
                                   "InputValidator",
                                   f"第{i}个关节值非法: {v!r}")
        return None

    def _chk_joint_limit(self, joints: List[float]) -> Optional[SafetyEvent]:
        n = min(len(joints), len(self.joint_lower), len(self.joint_upper))
        for i in range(n):
            v = joints[i]
            lo = self.joint_lower[i]
            hi = self.joint_upper[i]
            margin = math.radians(2.0)
            if v < lo - margin or v > hi + margin:
                return SafetyEvent(SafetyEventType.JOINT_LIMIT, "CRITICAL",
                                   "JointLimitGuard",
                                   f"关节#{i} 超出硬限位: {v:.3f}rad，允许[{lo:.3f}, {hi:.3f}]")
            if v < lo or v > hi:
                return SafetyEvent(SafetyEventType.JOINT_LIMIT, "WARN",
                                   "JointLimitGuard",
                                   f"关节#{i} 进入软限位裕度: {v:.3f}rad")
        return None

    def _chk_velocity(self, joints: List[float], dt: float) -> Optional[SafetyEvent]:
        for i in range(min(len(self._last_joint_pos), len(joints))):
            prev = self._last_joint_pos[i]
            cur = joints[i]
            vel = abs((cur - prev) / dt)
            if vel > self.velocity_limit:
                return SafetyEvent(SafetyEventType.VELOCITY_LIMIT, "CRITICAL",
                                   "VelocityGuard",
                                   f"关节#{i} 速度超限: {vel:.2f}rad/s (限制 {self.velocity_limit})")
        return None

    def _chk_acceleration(self, joints: List[float], dt: float) -> Optional[SafetyEvent]:
        for i in range(min(len(self._last_joint_pos), len(joints), len(self._last_joint_vel))):
            prev = self._last_joint_pos[i]
            cur = joints[i]
            cur_vel = (cur - prev) / dt
            accel = abs((cur_vel - self._last_joint_vel[i]) / dt)
            if accel > self.acceleration_limit:
                return SafetyEvent(SafetyEventType.ACCELERATION_LIMIT, "CRITICAL",
                                   "AccelerationGuard",
                                   f"关节#{i} 加速度超限: {accel:.2f}rad/s² (限制 {self.acceleration_limit})")
        return None

    def _chk_torque(self, torques: Optional[List[float]]) -> Optional[SafetyEvent]:
        if torques is None:
            return None
        n = min(len(torques), len(self.torque_limit))
        for i in range(n):
            if abs(torques[i]) > self.torque_limit[i]:
                return SafetyEvent(SafetyEventType.TORQUE_LIMIT, "CRITICAL",
                                   "TorqueGuard",
                                   f"关节#{i} 力矩超限: {torques[i]:.2f}Nm (限制 {self.torque_limit[i]})")
        return None

    def _chk_workspace(self, ee_pos: Optional[Tuple[float, float, float]]) -> Optional[SafetyEvent]:
        if ee_pos is None:
            return None
        for axis, (lo, hi) in self.workspace.items():
            idx = {"x": 0, "y": 1, "z": 2}[axis]
            v = ee_pos[idx]
            if not (lo - 0.01 <= v <= hi + 0.01):
                return SafetyEvent(SafetyEventType.WORKSPACE_LIMIT, "CRITICAL",
                                   "WorkspaceGuard",
                                   f"末端{axis}={v:.3f}m 超出工作空间[{lo:.3f}, {hi:.3f}]m")
        return None

    def _chk_collision(self) -> Optional[SafetyEvent]:
        triggered, _dist = self.collision.check_collision()
        if triggered and self.collision._events:
            return self.collision._events[-1]
        return None

    def _chk_rate_limit(self) -> Optional[SafetyEvent]:
        now = time.time()
        self._cmd_timestamps = [t for t in self._cmd_timestamps if now - t <= 1.0]
        if len(self._cmd_timestamps) >= self._max_command_rate_hz:
            return SafetyEvent(SafetyEventType.FUSE_TRIGGERED, "CRITICAL",
                               "RateLimitFuse",
                               f"命令速率超出限流 {self._max_command_rate_hz}/s")
        self._cmd_timestamps.append(now)
        return None

    # ---- 对外：综合校验入口 ----
    @dataclass
    class ValidationResult:
        allowed: bool
        sanitized_joints: List[float]
        events: List[SafetyEvent]

        def short(self) -> str:
            st = "✅ ALLOW" if self.allowed else "⛔ BLOCK"
            return f"{st} (events={len(self.events)})"

    def validate_command(
        self,
        target_joints: Any,
        ee_pos_hint: Optional[Tuple[float, float, float]] = None,
        torque_cmd: Optional[List[float]] = None,
    ) -> ValidationResult:
        """
        统一校验入口：一次动作指令进来，跑完整5层防护
        :param target_joints: 目标关节角列表
        :param ee_pos_hint:   可选：末端笛卡尔位置提示（用于工作空间校验）
        :param torque_cmd:    可选：关节力矩指令（用于力矩限制校验）
        :return: ValidationResult
        """
        with self._lock:
            events_out: List[SafetyEvent] = []

            if self._estop_engaged:
                events_out.append(SafetyEvent(SafetyEventType.EMERGENCY_STOP, "CRITICAL",
                                              "EmergencyStop",
                                              "紧急停止已触发，任何命令被拒绝，调用 reset_fuses() 复位"))
                return SafetyController.ValidationResult(False, list(self._last_joint_pos), events_out)
            if self._fuse_blown:
                events_out.append(SafetyEvent(SafetyEventType.FUSE_TRIGGERED, "CRITICAL",
                                              "SafetyFuse",
                                              "安全熔断器触发，需调用 reset_fuses() 复位后再操作"))
                return SafetyController.ValidationResult(False, list(self._last_joint_pos), events_out)

            ev = self._chk_input_type(target_joints)
            if ev is not None:
                self._emit(ev); events_out.append(ev)
                self._blow_fuse("输入校验异常 → 熔断器触发")
                return SafetyController.ValidationResult(False, list(self._last_joint_pos), events_out)
            joints = [float(v) for v in target_joints]

            now = time.time()
            dt = max(1e-6, now - self._last_ts)

            ev = self._chk_joint_limit(joints)
            if ev is not None:
                self._emit(ev); events_out.append(ev)
                if ev.severity == "CRITICAL":
                    n = min(len(joints), len(self.joint_lower), len(self.joint_upper))
                    clamped = list(joints)
                    for i in range(n):
                        clamped[i] = max(self.joint_lower[i], min(self.joint_upper[i], joints[i]))
                    joints = clamped
                    events_out.append(SafetyEvent("JOINT_CLAMPED", "INFO", "JointLimitGuard",
                                                  "关节指令已自动裁剪到合法限位区间"))

            ev = self._chk_velocity(joints, dt)
            if ev is not None:
                self._emit(ev); events_out.append(ev)
                self._blow_fuse("速度超限 → 熔断器触发")
                return SafetyController.ValidationResult(False, list(self._last_joint_pos), events_out)

            ev = self._chk_acceleration(joints, dt)
            if ev is not None:
                self._emit(ev); events_out.append(ev)
                self._blow_fuse("加速度超限 → 熔断器触发")
                return SafetyController.ValidationResult(False, list(self._last_joint_pos), events_out)

            ev = self._chk_torque(torque_cmd)
            if ev is not None:
                self._emit(ev); events_out.append(ev)
                self._blow_fuse("力矩超限 → 熔断器触发")
                return SafetyController.ValidationResult(False, list(self._last_joint_pos), events_out)

            ev = self._chk_workspace(ee_pos_hint)
            if ev is not None:
                self._emit(ev); events_out.append(ev)
                self._blow_fuse("工作空间越界 → 熔断器触发")
                return SafetyController.ValidationResult(False, list(self._last_joint_pos), events_out)

            ev = self._chk_collision()
            if ev is not None:
                self._emit(ev); events_out.append(ev)
                self.trigger_emergency_stop(reason="碰撞风险 → 紧急停止")
                return SafetyController.ValidationResult(False, list(self._last_joint_pos), events_out)

            ev = self._chk_rate_limit()
            if ev is not None:
                self._emit(ev); events_out.append(ev)
                self._blow_fuse("命令风暴限流 → 熔断器触发")
                return SafetyController.ValidationResult(False, list(self._last_joint_pos), events_out)

            n = min(len(self._last_joint_pos), len(joints))
            for i in range(n):
                self._last_joint_vel[i] = (joints[i] - self._last_joint_pos[i]) / dt
            self._last_joint_pos = joints
            self._last_ts = now
            return SafetyController.ValidationResult(True, joints, events_out)

    # ---- 急停 / 熔断器 ----
    def trigger_emergency_stop(self, reason: str = "手动触发") -> None:
        with self._lock:
            self._estop_engaged = True
            self._emit(SafetyEvent(SafetyEventType.EMERGENCY_STOP, "CRITICAL",
                                   "EmergencyStop", f"紧急停止已触发: {reason}"))

    def _blow_fuse(self, reason: str) -> None:
        with self._lock:
            self._fuse_blown = True
            self._emit(SafetyEvent(SafetyEventType.FUSE_TRIGGERED, "CRITICAL",
                                   "SafetyFuse", f"熔断器触发: {reason}"))

    def reset_fuses(self) -> bool:
        """故障排除后复位熔断器 & 紧急停止（推荐：确认安全后再调用）"""
        with self._lock:
            self._estop_engaged = False
            self._fuse_blown = False
            self._emit(SafetyEvent("FUSES_RESET", "INFO", "SafetyController",
                                   "安全熔断器/紧急停止 已复位"))
            return True

    @property
    def estop_engaged(self) -> bool:
        with self._lock:
            return self._estop_engaged

    @property
    def fuse_blown(self) -> bool:
        with self._lock:
            return self._fuse_blown

    # ---- 状态查询 ----
    @property
    def system_ok(self) -> bool:
        with self._lock:
            return not self._estop_engaged and not self._fuse_blown

    def summary(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "robot": self.robot_type,
                "num_joints": self.num_joints,
                "system_ok": not self._estop_engaged and not self._fuse_blown,
                "emergency_stop": self._estop_engaged,
                "fuse_blown": self._fuse_blown,
                "velocity_limit": self.velocity_limit,
                "acceleration_limit": self.acceleration_limit,
                "torque_limit": self.torque_limit,
                "events_total": len(self._events),
                "collision": self.collision.status,
            }
