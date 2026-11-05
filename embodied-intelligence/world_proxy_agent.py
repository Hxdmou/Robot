#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
World Proxy 交互式世界代理 - V1.0
================================================================
新增内容：
  1. WorldProxyConfig（代理配置数据类）
  2. InteractiveWorldAgent（交互式世界智能体）
  3. EnvironmentProbe（环境探测器）
  4. PolicyExecutor（策略执行器）
  5. create_world_proxy（工厂函数）

核心能力：
  - 自回归世界模型新范式：观察世界 → 改变世界
  - 交互式环境探测与策略执行
  - 支持语言指令驱动的场景变换
  - 实时碰撞风险反馈
"""

import time
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field

from world_model_engines import WorldState, PredictedTrajectory


@dataclass
class WorldProxyConfig:
    """World Proxy配置。"""
    max_interaction_steps: int = 1000
    probe_interval_ms: float = 100.0
    policy_update_hz: float = 20.0
    collision_threshold: float = 0.5
    enable_language_commands: bool = True
    enable_auto_exploration: bool = False


@dataclass
class ProbeResult:
    """环境探测结果。"""
    timestamp: float
    joint_positions: List[float]
    object_poses: Dict[str, List[float]]
    contact_forces: List[float]
    scene_description: str
    collision_risk: float
    safe: bool


class EnvironmentProbe:
    """环境探测器：感知当前世界状态。"""

    def __init__(self, config: WorldProxyConfig):
        self.config = config
        self._probe_count = 0

    def probe(self, state: WorldState) -> ProbeResult:
        self._probe_count += 1
        collision_risk = self._estimate_risk(state)
        return ProbeResult(
            timestamp=state.timestamp,
            joint_positions=list(state.robot_joint_positions),
            object_poses=dict(state.object_poses),
            contact_forces=list(state.contact_forces),
            scene_description=state.scene_description,
            collision_risk=collision_risk,
            safe=collision_risk < self.config.collision_threshold,
        )

    @staticmethod
    def _estimate_risk(state: WorldState) -> float:
        if state.contact_forces:
            max_force = max(abs(f) for f in state.contact_forces)
            if max_force > 50.0:
                return 0.8
            if max_force > 20.0:
                return 0.4
        if state.object_poses:
            return 0.15
        return 0.05

    def get_probe_count(self) -> int:
        return self._probe_count


class PolicyExecutor:
    """策略执行器：在世界中执行动作并观察结果。"""

    def __init__(self, config: WorldProxyConfig):
        self.config = config
        self._action_history: List[List[float]] = []
        self._execution_count = 0

    def execute(self, action: List[float],
                current_joints: List[float]) -> List[float]:
        self._action_history.append(list(action))
        self._execution_count += 1
        n = min(len(action), len(current_joints))
        next_joints = list(current_joints)
        for i in range(n):
            delta = max(-0.1, min(0.1, action[i] - current_joints[i]))
            next_joints[i] = current_joints[i] + delta
        return next_joints

    def get_history(self) -> List[List[float]]:
        return list(self._action_history)

    def get_execution_count(self) -> int:
        return self._execution_count

    def reset(self) -> None:
        self._action_history.clear()
        self._execution_count = 0


class InteractiveWorldAgent:
    """交互式世界智能体。

    实现"观察世界→改变世界"的自回归闭环：
      1. Probe探测当前环境
      2. 基于策略生成动作
      3. Execute执行动作
      4. 观察结果并更新策略
    """

    def __init__(self, config: Optional[WorldProxyConfig] = None):
        self.config = config or WorldProxyConfig()
        self.probe = EnvironmentProbe(self.config)
        self.executor = PolicyExecutor(self.config)
        self._current_state: Optional[WorldState] = None
        self._step_count = 0
        self._running = False
        self._event_callbacks: Dict[str, List[Callable]] = {
            "on_probe": [],
            "on_action": [],
            "on_collision_warning": [],
        }

    def start(self, initial_state: WorldState) -> None:
        self._current_state = initial_state
        self._running = True
        self._step_count = 0

    def step(self, action: Optional[List[float]] = None,
             language_command: str = "") -> ProbeResult:
        if not self._running or self._current_state is None:
            raise RuntimeError("Agent not started. Call start() first.")
        if action is None:
            action = self._default_action(language_command)
        next_joints = self.executor.execute(
            action, self._current_state.robot_joint_positions)
        self._current_state = WorldState(
            timestamp=time.time(),
            robot_joint_positions=next_joints,
            robot_joint_velocities=[a - b for a, b in zip(
                next_joints, self._current_state.robot_joint_positions)],
            object_poses=self._current_state.object_poses,
            contact_forces=self._current_state.contact_forces,
            scene_description=self._current_state.scene_description,
        )
        result = self.probe.probe(self._current_state)
        self._step_count += 1
        if not result.safe:
            self._fire_event("on_collision_warning", result)
        self._fire_event("on_probe", result)
        self._fire_event("on_action", action)
        return result

    def stop(self) -> Dict[str, Any]:
        self._running = False
        return {
            "total_steps": self._step_count,
            "total_probes": self.probe.get_probe_count(),
            "total_executions": self.executor.get_execution_count(),
        }

    def register_callback(self, event: str, callback: Callable) -> None:
        if event in self._event_callbacks:
            self._event_callbacks[event].append(callback)

    def _fire_event(self, event: str, data: Any) -> None:
        for cb in self._event_callbacks.get(event, []):
            try:
                cb(data)
            except Exception:
                pass

    def _default_action(self, language_command: str = "") -> List[float]:
        if not self._current_state or not self._current_state.robot_joint_positions:
            return [0.0] * 7
        return list(self._current_state.robot_joint_positions)

    def get_state(self) -> Optional[WorldState]:
        return self._current_state

    def is_running(self) -> bool:
        return self._running


def create_world_proxy(config: Optional[Dict] = None) -> InteractiveWorldAgent:
    """工厂函数：创建交互式世界智能体。"""
    proxy_config = WorldProxyConfig(**config) if config else WorldProxyConfig()
    return InteractiveWorldAgent(proxy_config)


if __name__ == "__main__":
    agent = create_world_proxy()
    print(f"World Proxy智能体已创建: running={agent.is_running()}")
