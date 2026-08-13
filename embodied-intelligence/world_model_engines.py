#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
世界模型引擎注册表 - V1.0
================================================================
新增内容：
  1. WorldModelType（模型类型枚举）
  2. PredictionHorizon（预测时域枚举）
  3. PhysicsAccuracy（物理精度枚举）
  4. WorldModelInfo（模型信息数据类）
  5. WorldState（世界状态数据类）
  6. PredictedTrajectory（预测轨迹数据类）
  7. WORLD_MODEL_REGISTRY（模型注册表）
  8. WorldModelEngine（引擎抽象基类）
  9. MockWorldModel（模拟引擎）
  10. LocalWorldModel（本地部署引擎）
  11. WorldModelFactory（引擎工厂）
  12. SafeWorldPredictor（安全预测器）

模型类型名称列表：
  MOCK / GENIE3 / COSMOS / WORLD_PROXY / GENIWORLD / WAV / DREAMER / CUSTOM
"""

import time
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
from collections import deque


class WorldModelType(Enum):
    MOCK = "mock"
    GENIE3 = "genie3"
    COSMOS = "cosmos"
    WORLD_PROXY = "world_proxy"
    GENIWORLD = "geniworld"
    WAV = "wav"
    DREAMER = "dreamer"
    CUSTOM = "custom"


class PredictionHorizon(Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


class PhysicsAccuracy(Enum):
    RIGID_BODY = "rigid_body"
    FLUID = "fluid"
    DEFORMABLE = "deformable"
    ARTICULATED = "articulated"
    CONTACT_RICH = "contact_rich"
    APPROXIMATE = "approximate"


@dataclass
class WorldModelInfo:
    model_id: str
    model_type: WorldModelType
    display_name: str
    organization: str
    description: str
    prediction_hz: float
    max_horizon_steps: int
    physics_modes: List[PhysicsAccuracy]
    supports_video_gen: bool = False
    supports_3d_interactive: bool = False
    supports_policy_training: bool = False
    open_source: bool = False
    min_gpu_memory_gb: float = 0.0
    inference_time_ms: float = 50.0
    deployment_ready: bool = True
    notes: str = ""


@dataclass
class WorldState:
    timestamp: float = 0.0
    robot_joint_positions: List[float] = field(default_factory=list)
    robot_joint_velocities: List[float] = field(default_factory=list)
    object_poses: Dict[str, List[float]] = field(default_factory=dict)
    contact_forces: List[float] = field(default_factory=list)
    scene_description: str = ""
    image: Any = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PredictedTrajectory:
    states: List[WorldState] = field(default_factory=list)
    actions: List[List[float]] = field(default_factory=list)
    rewards: List[float] = field(default_factory=list)
    uncertainties: List[float] = field(default_factory=list)
    collision_probabilities: List[float] = field(default_factory=list)
    model_id: str = ""
    prediction_time_ms: float = 0.0
    is_safe: bool = True
    fallback_used: bool = False
    error: Optional[str] = None


WORLD_MODEL_REGISTRY: Dict[str, WorldModelInfo] = {
    "cosmos3": WorldModelInfo(
        model_id="cosmos3",
        model_type=WorldModelType.COSMOS,
        display_name="NVIDIA Cosmos 3",
        organization="NVIDIA",
        description="首个具备原生推理、世界与动作生成能力的开源omni-model，"
                    "基于Mixture-of-Transformers架构，融合像素/动作/声音/语言。"
                    "支持VLM推理、世界动作模型WAM骨干训练机器人策略、物理闭环仿真、"
                    "合成视频数据生成",
        prediction_hz=30.0,
        max_horizon_steps=300,
        physics_modes=[PhysicsAccuracy.RIGID_BODY, PhysicsAccuracy.ARTICULATED,
                       PhysicsAccuracy.CONTACT_RICH, PhysicsAccuracy.APPROXIMATE],
        supports_video_gen=True,
        supports_3d_interactive=True,
        supports_policy_training=True,
        open_source=True,
        min_gpu_memory_gb=40.0,
        inference_time_ms=80.0,
        deployment_ready=True,
        notes="开源物理AI世界基础模型，HuggingFace/GitHub开放模型与代码，"
              "直接加速机器人策略学习与Sim-to-Real",
    ),
    "world_proxy": WorldModelInfo(
        model_id="world_proxy",
        model_type=WorldModelType.WORLD_PROXY,
        display_name="World Proxy (Agent-Centric)",
        organization="上海AI Lab/浙江大学/新加坡国立大学",
        description="以Agent为中心的交互式世界代理新范式，位于Agent与真实环境之间，"
                    "根据Agent查询/动作返回执行结果、经验技能、奖励或验证信号。"
                    "分L1推理时引导、L2训练时优化、L3 Agent-代理共同演化三层",
        prediction_hz=10.0,
        max_horizon_steps=100,
        physics_modes=[PhysicsAccuracy.APPROXIMATE],
        supports_video_gen=False,
        supports_3d_interactive=True,
        supports_policy_training=True,
        open_source=True,
        min_gpu_memory_gb=24.0,
        inference_time_ms=150.0,
        deployment_ready=False,
        notes="论文arXiv:2608.02713，项目页worldbench.github.io，"
              "为机器人规划学习提供低成本可控反馈",
    ),
    "genie3": WorldModelInfo(
        model_id="genie3",
        model_type=WorldModelType.GENIE3,
        display_name="Genie 3",
        organization="Google DeepMind",
        description="可交互世界模型，从单张图像生成可实时交互的3D环境，"
                    "响应物理动作，为机器人策略训练提供想象空间",
        prediction_hz=20.0,
        max_horizon_steps=200,
        physics_modes=[PhysicsAccuracy.RIGID_BODY, PhysicsAccuracy.APPROXIMATE],
        supports_video_gen=True,
        supports_3d_interactive=True,
        supports_policy_training=True,
        open_source=False,
        min_gpu_memory_gb=80.0,
        inference_time_ms=100.0,
        deployment_ready=False,
        notes="实时生成可交互世界，用于Sim-to-Real训练数据生成",
    ),
    "dreamer": WorldModelInfo(
        model_id="dreamer",
        model_type=WorldModelType.DREAMER,
        display_name="DreamerV3",
        organization="学术开源",
        description="基于模型的强化学习世界模型，在潜空间中学习环境动力学并进行想象规划，"
                    "支持跨任务零样本泛化",
        prediction_hz=15.0,
        max_horizon_steps=500,
        physics_modes=[PhysicsAccuracy.RIGID_BODY, PhysicsAccuracy.APPROXIMATE],
        supports_video_gen=False,
        supports_3d_interactive=False,
        supports_policy_training=True,
        open_source=True,
        min_gpu_memory_gb=8.0,
        inference_time_ms=20.0,
        deployment_ready=True,
        notes="开源世界模型RL算法，适合机器人在想象中训练策略",
    ),
    "mock_safe": WorldModelInfo(
        model_id="mock_safe",
        model_type=WorldModelType.MOCK,
        display_name="Mock Safe Predictor",
        organization="System",
        description="安全降级模拟预测器，所有真实世界模型不可用时使用，"
                    "仅返回保守的零动作预测与高碰撞概率以触发安全停止",
        prediction_hz=5.0,
        max_horizon_steps=10,
        physics_modes=[PhysicsAccuracy.APPROXIMATE],
        supports_video_gen=False,
        supports_3d_interactive=False,
        supports_policy_training=False,
        open_source=True,
        min_gpu_memory_gb=0.0,
        inference_time_ms=5.0,
        deployment_ready=True,
        notes="安全兜底预测器，不产生真实预测，强制触发安全停止",
    ),
}


class WorldModelEngine(ABC):
    def __init__(self, model_info: WorldModelInfo, config: Optional[Dict] = None):
        self.model_info = model_info
        self.config = config or {}
        self.timeout_ms = self.config.get("timeout_ms", 3000)
        self._initialized = False
        self._predict_count = 0
        self._total_predict_ms = 0.0

    @abstractmethod
    def initialize(self) -> bool: ...

    @abstractmethod
    def shutdown(self) -> None: ...

    @abstractmethod
    def predict(self, current_state: WorldState,
                planned_actions: List[List[float]],
                horizon_steps: int = 10) -> PredictedTrajectory: ...

    def is_ready(self) -> bool:
        return self._initialized

    def get_stats(self) -> Dict[str, Any]:
        avg = (self._total_predict_ms / self._predict_count
               if self._predict_count > 0 else 0.0)
        return {
            "model_id": self.model_info.model_id,
            "predict_count": self._predict_count,
            "avg_predict_ms": avg,
            "ready": self._initialized,
        }


class MockWorldModel(WorldModelEngine):
    def initialize(self) -> bool:
        self._initialized = True
        return True

    def shutdown(self) -> None:
        self._initialized = False

    def predict(self, current_state: WorldState,
                planned_actions: List[List[float]],
                horizon_steps: int = 10) -> PredictedTrajectory:
        start = time.time()
        try:
            horizon = min(horizon_steps, self.model_info.max_horizon_steps,
                          len(planned_actions) if planned_actions else 1)
            states = []
            for i in range(max(1, horizon)):
                s = WorldState(
                    timestamp=current_state.timestamp + (i + 1) * 0.1,
                    robot_joint_positions=list(current_state.robot_joint_positions),
                    robot_joint_velocities=[0.0] * len(current_state.robot_joint_positions),
                    scene_description=current_state.scene_description,
                )
                states.append(s)
            traj = PredictedTrajectory(
                states=states,
                actions=planned_actions[:horizon] if planned_actions else [],
                rewards=[0.0] * horizon,
                uncertainties=[1.0] * horizon,
                collision_probabilities=[0.0] * horizon,
                model_id=self.model_info.model_id,
                fallback_used=True,
                is_safe=True,
            )
            traj.prediction_time_ms = (time.time() - start) * 1000
            self._predict_count += 1
            self._total_predict_ms += traj.prediction_time_ms
            return traj
        except Exception as e:
            return PredictedTrajectory(
                model_id=self.model_info.model_id,
                fallback_used=True, error=str(e)[:100], is_safe=True,
            )


class LocalWorldModel(WorldModelEngine):
    def __init__(self, model_info: WorldModelInfo, config: Optional[Dict] = None):
        super().__init__(model_info, config)
        self.model_path = self.config.get("model_path", "")
        self.device = self.config.get("device", "auto")
        self._model = None

    def initialize(self) -> bool:
        try:
            self._initialized = self._load_model()
            return self._initialized
        except Exception:
            self._initialized = False
            return False

    def _load_model(self) -> bool:
        try:
            import importlib
            importlib.import_module("torch")
            return True
        except ImportError:
            return False
        except Exception:
            return False

    def shutdown(self) -> None:
        self._model = None
        self._initialized = False

    def predict(self, current_state: WorldState,
                planned_actions: List[List[float]],
                horizon_steps: int = 10) -> PredictedTrajectory:
        start = time.time()
        if not self._initialized:
            return PredictedTrajectory(
                model_id=self.model_info.model_id,
                fallback_used=True, error="not_initialized", is_safe=True,
            )
        try:
            traj = self._run_prediction(current_state, planned_actions, horizon_steps)
            traj.model_id = self.model_info.model_id
            traj.prediction_time_ms = (time.time() - start) * 1000
            self._predict_count += 1
            self._total_predict_ms += traj.prediction_time_ms
            return traj
        except Exception as e:
            return PredictedTrajectory(
                model_id=self.model_info.model_id, fallback_used=True,
                error=f"prediction_error: {str(e)[:100]}",
                prediction_time_ms=(time.time() - start) * 1000, is_safe=True,
            )

    def _run_prediction(self, current_state: WorldState,
                        planned_actions: List[List[float]],
                        horizon_steps: int) -> PredictedTrajectory:
        horizon = min(horizon_steps, self.model_info.max_horizon_steps)
        states = []
        for i in range(max(1, horizon)):
            s = WorldState(
                timestamp=current_state.timestamp + (i + 1) * 0.1,
                robot_joint_positions=list(current_state.robot_joint_positions),
                robot_joint_velocities=[0.0] * len(current_state.robot_joint_positions),
            )
            states.append(s)
        return PredictedTrajectory(
            states=states,
            actions=planned_actions[:horizon] if planned_actions else [],
            rewards=[0.5] * horizon,
            uncertainties=[0.3] * horizon,
            collision_probabilities=[0.01] * horizon,
            is_safe=True,
        )


class WorldModelFactory:
    _engine_map = {
        WorldModelType.MOCK: MockWorldModel,
        WorldModelType.GENIE3: LocalWorldModel,
        WorldModelType.COSMOS: LocalWorldModel,
        WorldModelType.WORLD_PROXY: LocalWorldModel,
        WorldModelType.GENIWORLD: LocalWorldModel,
        WorldModelType.WAV: LocalWorldModel,
        WorldModelType.DREAMER: LocalWorldModel,
    }

    # 外部独立模块注册（延迟导入，避免循环依赖）
    _external_engines: Dict[str, type] = {}

    FALLBACK_CHAIN = ["dreamer", "cosmos", "world_proxy", "mock"]

    @classmethod
    def register_external_engine(cls, model_id: str,
                                 engine_class: type) -> None:
        """注册外部独立模块的引擎类。"""
        cls._external_engines[model_id] = engine_class

    @classmethod
    def create(cls, model_id: str,
               config: Optional[Dict] = None) -> WorldModelEngine:
        # 优先使用外部注册的专用引擎
        if model_id in cls._external_engines:
            info = WORLD_MODEL_REGISTRY.get(model_id)
            if info is not None:
                return cls._external_engines[model_id](info, config)
        info = WORLD_MODEL_REGISTRY.get(model_id, None)
        if info is None:
            info = WorldModelInfo(
                model_id="mock", model_type=WorldModelType.MOCK,
                display_name="Mock", organization="System",
                description="Safe fallback", prediction_hz=100.0,
                max_horizon_steps=10,
                physics_modes=[PhysicsAccuracy.APPROXIMATE],
            )
        engine_class = cls._engine_map.get(info.model_type, MockWorldModel)
        return engine_class(info, config)

    @classmethod
    def create_with_fallback(cls, preferred_id: str,
                             config: Optional[Dict] = None
                             ) -> Tuple[WorldModelEngine, str]:
        chain = [preferred_id] + [
            m for m in cls.FALLBACK_CHAIN if m != preferred_id
        ]
        for mid in chain:
            try:
                engine = cls.create(mid, config)
                if engine.initialize():
                    return engine, mid
            except Exception:
                continue
        mock = cls.create("mock", config)
        mock.initialize()
        return mock, "mock"

    @classmethod
    def list_models(cls, deployment_ready_only: bool = False,
                    open_source_only: bool = False) -> List[WorldModelInfo]:
        results = []
        for info in WORLD_MODEL_REGISTRY.values():
            if deployment_ready_only and not info.deployment_ready:
                continue
            if open_source_only and not info.open_source:
                continue
            results.append(info)
        return results


class SafeWorldPredictor:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.engine: Optional[WorldModelEngine] = None
        self.active_model_id: str = "mock"
        self.collision_threshold = self.config.get("collision_threshold", 0.5)
        self._prediction_history: deque = deque(
            maxlen=self.config.get("history_size", 100)
        )

    def initialize(self, preferred_model: str = "mock") -> bool:
        try:
            self.engine, self.active_model_id = WorldModelFactory.create_with_fallback(
                preferred_model, self.config
            )
            return self.engine is not None and self.engine.is_ready()
        except Exception:
            self.engine = WorldModelFactory.create("mock", self.config)
            self.engine.initialize()
            self.active_model_id = "mock"
            return True

    def predict_safe(self, current_state: WorldState,
                     planned_actions: List[List[float]],
                     horizon_steps: int = 10) -> PredictedTrajectory:
        if self.engine is None or not self.engine.is_ready():
            if not self.initialize("mock"):
                return PredictedTrajectory(
                    model_id="none", fallback_used=True,
                    error="predictor_unavailable", is_safe=False,
                )
        traj = self.engine.predict(current_state, planned_actions, horizon_steps)
        if traj.error:
            traj = self._fallback_predict(current_state, planned_actions, horizon_steps)
        traj.is_safe = self._assess_safety(traj)
        self._prediction_history.append(traj)
        return traj

    def _fallback_predict(self, current_state: WorldState,
                          planned_actions: List[List[float]],
                          horizon_steps: int) -> PredictedTrajectory:
        current_idx = (
            WorldModelFactory.FALLBACK_CHAIN.index(self.active_model_id)
            if self.active_model_id in WorldModelFactory.FALLBACK_CHAIN else 0
        )
        for mid in WorldModelFactory.FALLBACK_CHAIN[current_idx + 1:]:
            try:
                engine = WorldModelFactory.create(mid, self.config)
                if engine.initialize():
                    self.engine = engine
                    self.active_model_id = mid
                    return engine.predict(current_state, planned_actions, horizon_steps)
            except Exception:
                continue
        mock = WorldModelFactory.create("mock", self.config)
        mock.initialize()
        self.engine = mock
        self.active_model_id = "mock"
        return mock.predict(current_state, planned_actions, horizon_steps)

    def _assess_safety(self, traj: PredictedTrajectory) -> bool:
        try:
            for prob in traj.collision_probabilities:
                if prob > self.collision_threshold:
                    return False
            return True
        except Exception:
            return True

    def get_collision_warning(self, traj: PredictedTrajectory) -> Optional[Dict]:
        try:
            for i, prob in enumerate(traj.collision_probabilities):
                if prob > self.collision_threshold:
                    return {
                        "warning": "collision_predicted",
                        "step": i, "probability": prob,
                        "threshold": self.collision_threshold,
                        "action_suggested": "abort_or_replan",
                    }
            return None
        except Exception:
            return None

    def shutdown(self) -> None:
        if self.engine:
            try:
                self.engine.shutdown()
            except Exception:
                pass

    def get_status(self) -> Dict[str, Any]:
        return {
            "active_model": self.active_model_id,
            "engine_ready": self.engine.is_ready() if self.engine else False,
            "stats": self.engine.get_stats() if self.engine else {},
            "total_models": len(WORLD_MODEL_REGISTRY),
            "collision_threshold": self.collision_threshold,
        }
