"""
数字孪生系统（框架版）
================================================
展示「实体机器人 ↔ 虚拟孪生体」双向同步的工程架构：
  - 实体状态 → 孪生体：关节/末端/IO/告警 同步写入
  - 孪生体 → 仿真/可视化：PyBullet 渲染镜像
  - 历史回放：DataRecorder 读取已归档 CSV/JSONL
  - 事件总线：基于标准 Message 的发布订阅

说明：公共示例版无真实真机对接，使用 Mock 数据流完整演示框架。
"""

from __future__ import annotations

import abc
import csv
import json
import os
import time
import threading
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional


# ============================================================
# 孪生体状态模型
# ============================================================
@dataclass
class TwinState:
    """数字孪生体的标准状态（与实体一一对应）"""
    timestamp_s: float = field(default_factory=time.time)
    # 本体
    robot_type: str = "panda"
    joint_positions: List[float] = field(default_factory=lambda: [0.0]*7)
    joint_velocities: List[float] = field(default_factory=lambda: [0.0]*7)
    joint_torques: List[float] = field(default_factory=list)
    end_effector_pos_m: List[float] = field(default_factory=lambda: [0.3, 0.0, 0.6])
    end_effector_orn_xyzw: List[float] = field(default_factory=lambda: [0,0,0,1])
    gripper_state: str = "open"                # open / close / unknown
    # 工作空间中的物体（镜像）
    objects_in_scene: List[Dict[str, Any]] = field(default_factory=list)
    # 子系统状态
    safety_ok: bool = True
    safety_event: str = ""                      # 若有事件
    operating_mode: str = "IDLE"                # IDLE / AUTO / MANUAL / ESTOP
    # 能源 & 温度
    supply_voltage_ratio: float = 1.0
    joint_temperatures_c: List[float] = field(default_factory=list)
    # 业务
    current_skill: str = ""
    task_id: str = ""
    progress_percent: int = 0

    def to_flat_row(self) -> Dict[str, Any]:
        return {
            "timestamp_s": f"{self.timestamp_s:.6f}",
            "robot_type": self.robot_type,
            "joint_positions": json.dumps(self.joint_positions),
            "ee_xyz_m": json.dumps(self.end_effector_pos_m),
            "ee_xyzw": json.dumps(self.end_effector_orn_xyzw),
            "gripper": self.gripper_state,
            "safety_ok": self.safety_ok,
            "mode": self.operating_mode,
            "voltage_ratio": self.voltage_ratio,
            "skill": self.current_skill,
            "task_id": self.task_id,
            "progress_pct": self.progress_percent,
            "num_objects": len(self.objects_in_scene),
        }


# ============================================================
# 状态来源抽象：实体机器人 / 回放 / Mock
# ============================================================
class TwinStateSource(abc.ABC):
    """孪生体状态数据源抽象"""

    @abc.abstractmethod
    def read(self) -> Optional[TwinState]:
        """返回下一个状态或 None（结束/无数据）"""
        raise NotImplementedError


class MockTwinStateSource(TwinStateSource):
    """
    Mock数据源：按一个「移动→抓取→搬运→放下」的循环生成状态序列
    ------------------------------------------------
    用于演示数字孪生系统在无真机情况下的完整画面更新。
    """
    def __init__(self, total_steps: int = 200, sleep_s_per_step: float = 0.05):
        self.total = total_steps
        self.sleep_s = sleep_s_per_step
        self.step = 0
        self._state = TwinState()

    def _advance(self) -> None:
        t = self.step / max(1, self.total - 1)
        s = self._state
        s.timestamp_s = time.time()
        # 演示轨迹：从(0.30,0,0.60) 到 (0.55,0.10,0.25) 再返回
        if t < 0.5:
            u = t / 0.5
            s.end_effector_pos_m = [
                0.30 + 0.25 * u,
                0.00 + 0.10 * u,
                0.60 - 0.35 * u,
            ]
            s.current_skill = "move_reach"
            s.progress_percent = int(u * 50)
        elif t < 0.7:
            u = (t - 0.5) / 0.2
            s.current_skill = "grip_close"
            s.gripper_state = "close" if u >= 1.0 else "opening"
            s.progress_percent = 50 + int(u * 20)
        elif t < 0.9:
            u = (t - 0.7) / 0.2
            s.end_effector_pos_m = [
                0.55 - 0.45 * u,
                0.10 - 0.50 * u,
                0.25 + 0.35 * u,
            ]
            s.current_skill = "move_carry"
            s.progress_percent = 70 + int(u * 20)
        else:
            u = (t - 0.9) / 0.1
            s.gripper_state = "open" if u >= 1 else "closing"
            s.current_skill = "release"
            s.progress_percent = 100
        # 随机温度
        import random
        s.joint_temperatures_c = [30.0 + random.random()*8 for _ in range(7)]
        s.voltage_ratio = 0.96 + random.random()*0.08
        # 关节状态简单镜像（7关节：首末摆动）
        s.joint_positions = [
            0.2 * u - 0.1,
            -0.4 + 0.2 * u,
            0.1,
            -1.8 + 0.3 * u,
            0.0,
            1.2 - 0.3 * u,
            0.78,
        ]
        self.step += 1
        if self.sleep_s > 0:
            time.sleep(self.sleep_s)

    def read(self) -> Optional[TwinState]:
        if self.step >= self.total:
            return None
        self._advance()
        return self._state


class ReplayFromJSONLSource(TwinStateSource):
    """
    回放数据源：从 DataRecorder 生成的 JSONL 文件读取
    ------------------------------------------------
    仅演示接口，实际使用请传入真实文件路径。
    """

    def __init__(self, jsonl_path: str):
        if not os.path.isfile(jsonl_path):
            raise FileNotFoundError(jsonl_path)
        self._path = jsonl_path
        self._lines: List[str] = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for ln in f:
                if ln.strip():
                    self._lines.append(ln)
        self._idx = 0

    def read(self) -> Optional[TwinState]:
        while self._idx < len(self._lines):
            try:
                row = json.loads(self._lines[self._idx])
                self._idx += 1
                p = json.loads(row.get("payload_json", "{}"))
                if row.get("record_type") == "joint_state":
                    return TwinState(
                        timestamp_s=float(row.get("timestamp_s", time.time())),
                        joint_positions=p.get("positions", [0.0]*7),
                        joint_velocities=p.get("velocities", []),
                        joint_torques=p.get("torques", []),
                    )
            except Exception:
                continue
        return None


# ============================================================
# 可视化器抽象 & 实现
# ============================================================
class TwinRenderer(abc.ABC):
    """孪生体可视化器"""

    @abc.abstractmethod
    def render(self, state: TwinState) -> None:
        raise NotImplementedError

    def close(self) -> None:
        pass


class ConsoleRenderer(TwinRenderer):
    """
    控制台渲染器：把 TwinState 打印成简洁仪表盘（无需GUI也能演示）
    """
    WIDTH = 78

    def render(self, state: TwinState) -> None:
        mode_color = {
            "IDLE": "\033[36m", "AUTO": "\033[32m", "MANUAL": "\033[33m", "ESTOP": "\033[31m"
        }.get(state.operating_mode, "\033[37m")
        reset = "\033[0m"
        bar_len = 40
        filled = int(bar_len * state.progress_percent / 100)
        bar = "█" * filled + "░" * (bar_len - filled)
        lines = []
        lines.append("╔" + "═" * (self.WIDTH - 2) + "╗")
        lines.append(f"║  🤖 数字孪生控制台  {mode_color}{state.operating_mode:>6s}{reset}"
                     f"   🔩 {state.robot_type:<16s}"
                     f"   ⚡ {state.voltage_ratio:+.2%}V ║")
        lines.append("╠" + "─" * (self.WIDTH - 2) + "╣")
        lines.append(f"║  末端 XYZ: ({state.end_effector_pos_m[0]:+.3f}, "
                     f"{state.end_effector_pos_m[1]:+.3f}, "
                     f"{state.end_effector_pos_m[2]:+.3f}) m   "
                     f"夹爪: {'▣ 闭合' if state.gripper_state=='close' else '▢ 张开'}       ║")
        lines.append(f"║  当前技能: {state.current_skill or '(无)':<20s}"
                     f"  任务ID: {state.task_id or '—':<14s}            ║")
        lines.append(f"║  进度: [{bar}] {state.progress_percent:>3d}%                           ║")
        temps = " / ".join(f"{t:>4.1f}°C" for t in state.joint_temperatures_c[:4])
        if state.joint_temperatures_c:
            lines.append(f"║  关节温度(前4): {temps:<44s}║")
        safety_icon = "✅" if state.safety_ok else "🚨"
        safety_msg = state.safety_event or "系统安全"
        lines.append(f"║  安全状态: {safety_icon} {safety_msg:<60s}║")
        lines.append("╚" + "═" * (self.WIDTH - 2) + "╝")
        # 回到顶行重绘（类top效果）
        print("\033[" + str(len(lines)) + "A", end="") if state.progress_percent > 0 else None
        print("\n".join(lines))


class PyBulletMirrorRenderer(TwinRenderer):
    """
    PyBullet 镜像渲染器（可选：把孪生体同步到 PyBullet 仿真窗口）
    ------------------------------------------------
    公共示例版只提供轻量封装，避免未安装 pybullet 时导入异常。
    """
    def __init__(self, robot_type: str = "panda", mode: str = "gui"):
        try:
            from core.simulation_env import PyBulletSimulationEnv, SimConfig
        except Exception as e:
            raise RuntimeError(f"依赖缺失: {e}")
        self.env = PyBulletSimulationEnv(SimConfig(mode=mode, verbose=False))
        self.env.load_robot(robot_type)

    def render(self, state: TwinState) -> None:
        if state.joint_positions:
            self.env.set_joint_positions(state.joint_positions)
        else:
            self.env.set_end_effector_pose(tuple(state.end_effector_pos_m))
        self.env.step(2)

    def close(self) -> None:
        self.env.close()


# ============================================================
# 数字孪生主系统
# ============================================================
class DigitalTwinSystem:
    """
    数字孪生系统（核心编排类）
    ------------------------------------------------
    用法：
        >>> sys = DigitalTwinSystem()
        >>> sys.set_source(MockTwinStateSource(total_steps=100))
        >>> sys.attach_renderer(ConsoleRenderer())
        >>> sys.run()
    """

    def __init__(self):
        self._source: Optional[TwinStateSource] = None
        self._renderers: List[TwinRenderer] = []
        self._listeners: List[Callable[[TwinState], None]] = []
        self._history: List[TwinState] = []
        self._running = False
        self._lock = threading.Lock()
        self._csv_log_path: Optional[str] = None
        self._csv_fd = None
        self._csv_writer = None

    # ---- 装配 ----
    def set_source(self, source: TwinStateSource) -> None:
        self._source = source

    def attach_renderer(self, renderer: TwinRenderer) -> None:
        self._renderers.append(renderer)

    def on_state(self, listener: Callable[[TwinState], None]) -> None:
        self._listeners.append(listener)

    def enable_csv_log(self, path: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self._csv_log_path = path
        self._csv_fd = open(path, "w", encoding="utf-8", newline="")
        cols = list(TwinState().to_flat_row().keys())
        self._csv_writer = csv.DictWriter(self._csv_fd, fieldnames=cols)
        self._csv_writer.writeheader()

    # ---- 运行 ----
    def run_once(self) -> Optional[TwinState]:
        if self._source is None:
            raise RuntimeError("先调用 set_source() 设置数据源")
        state = self._source.read()
        if state is None:
            return None
        with self._lock:
            self._history.append(state)
            if len(self._history) > 10000:
                self._history = self._history[-10000:]
            if self._csv_writer:
                try:
                    self._csv_writer.writerow(state.to_flat_row())
                except Exception:
                    pass
        for r in list(self._renderers):
            try:
                r.render(state)
            except Exception:
                pass  # 渲染器异常不阻断主循环
        for l in list(self._listeners):
            try:
                l(state)
            except Exception:
                pass
        return state

    def run(self, max_states: int = 0) -> int:
        """
        持续读取并渲染状态，直到数据源结束或达到 max_states
        :param max_states: 0=直到数据源EOF
        :return: 实际处理的状态条数
        """
        self._running = True
        count = 0
        try:
            while self._running:
                state = self.run_once()
                if state is None:
                    break
                count += 1
                if max_states > 0 and count >= max_states:
                    break
        except KeyboardInterrupt:
            print("\n[DigitalTwinSystem] 用户中断")
        finally:
            self._running = False
            self.close()
        return count

    def stop(self) -> None:
        self._running = False

    def close(self) -> None:
        for r in self._renderers:
            try:
                r.close()
            except Exception:
                pass
        if self._csv_fd:
            try:
                self._csv_fd.close()
            except Exception:
                pass
            self._csv_fd = None

    # ---- 查询 ----
    @property
    def latest_state(self) -> Optional[TwinState]:
        return self._history[-1] if self._history else None

    def report(self) -> Dict[str, Any]:
        h = self._history
        if not h:
            return {"states": 0}
        dur = h[-1].timestamp_s - h[0].timestamp_s
        return {
            "states": len(h),
            "duration_s": round(dur, 3),
            "avg_hz": round((len(h)-1) / dur, 2) if dur > 0 else 0.0,
            "safety_events": sum(1 for s in h if not s.safety_ok),
            "mode_histogram": {m: sum(1 for s in h if s.operating_mode == m)
                               for m in sorted({s.operating_mode for s in h})},
            "latest": asdict(h[-1]),
            "csv_log": self._csv_log_path,
        }
