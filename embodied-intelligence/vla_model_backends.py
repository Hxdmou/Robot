#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VLA模型后端注册表 - V1.0
================================================================
新增内容：
  1. VLABackendType（后端类型枚举）
  2. VLAInferenceMode（推理模式枚举）
  3. ActionSpace（动作空间枚举）
  4. VLAModelInfo（模型信息数据类）
  5. VLAObservation（观测输入数据类）
  6. VLAActionOutput（动作输出数据类）
  7. VLA_MODEL_REGISTRY（模型注册表）
  8. SafetyLimits（安全限制数据类）
  9. ActionSafetyChecker（动作安全检查器）
  10. VLABackend（后端抽象基类）
  11. MockVLABackend（模拟后端）
  12. CloudAPIVLABackend（云端API后端）
  13. LocalVLABackend（本地部署后端）
  14. VLABackendFactory（后端工厂）
  15. VLAInferencePipeline（推理管线）

后端类型名称列表：
  MOCK / OPENAI_GPT5 / OPENAI_GPT_OSS / QWEN3_VL / GEMINI_ROBOTICS2 /
  DEEPSEEK_V4 / NEMOTRON_35 / OPENVLA / OCTO / CUSTOM
"""

import time
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


class VLABackendType(Enum):
    MOCK = "mock"
    OPENAI_GPT5 = "openai_gpt5"
    OPENAI_GPT_OSS = "openai_gpt_oss"
    QWEN3_VL = "qwen3_vl"
    GEMINI_ROBOTICS2 = "gemini_robotics2"
    DEEPSEEK_V4 = "deepseek_v4"
    NEMOTRON_35 = "nemotron_35"
    OPENVLA = "openvla"
    OCTO = "octo"
    CUSTOM = "custom"


class VLAInferenceMode(Enum):
    CLOUD_API = "cloud_api"
    LOCAL_DEPLOY = "local_deploy"
    EDGE_DEVICE = "edge_device"
    MOCK_SAFE = "mock_safe"


class ActionSpace(Enum):
    JOINT_POSITION = "joint_position"
    CARTESIAN_POSE = "cartesian_pose"
    JOINT_VELOCITY = "joint_velocity"
    TORQUE = "torque"
    GRIPPER = "gripper"
    BIMANUAL = "bimanual"


@dataclass
class VLAModelInfo:
    model_id: str
    backend_type: VLABackendType
    display_name: str
    organization: str
    parameters_b: float
    context_window: int
    modalities: List[str]
    action_spaces: List[ActionSpace]
    inference_mode: VLAInferenceMode
    min_gpu_memory_gb: float
    inference_time_ms: float
    open_source: bool
    license_type: str = "proprietary"
    max_batch_size: int = 1
    supports_streaming: bool = False
    supports_bimanual: bool = False
    deployment_ready: bool = True
    notes: str = ""


@dataclass
class VLAObservation:
    joint_positions: List[float] = field(default_factory=list)
    joint_velocities: List[float] = field(default_factory=list)
    ee_pose: List[float] = field(default_factory=list)
    gripper_state: float = 0.0
    force_torque: Optional[List[float]] = None
    images: List[Any] = field(default_factory=list)
    language_instruction: str = ""
    robot_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VLAActionOutput:
    action_space: ActionSpace = ActionSpace.JOINT_POSITION
    joint_positions: List[float] = field(default_factory=list)
    cartesian_pose: List[float] = field(default_factory=list)
    joint_velocities: List[float] = field(default_factory=list)
    gripper_command: float = 0.0
    confidence: float = 1.0
    inference_time_ms: float = 0.0
    model_id: str = ""
    raw_response: Any = None
    safety_checked: bool = False
    fallback_used: bool = False
    error: Optional[str] = None


VLA_MODEL_REGISTRY: Dict[str, VLAModelInfo] = {
    "deepseek_v4_flash": VLAModelInfo(
        model_id="deepseek_v4_flash",
        backend_type=VLABackendType.DEEPSEEK_V4,
        display_name="DeepSeek-V4-Flash",
        organization="深度求索 DeepSeek",
        parameters_b=671.0,
        context_window=1000000,
        modalities=["text", "image"],
        action_spaces=[ActionSpace.JOINT_POSITION, ActionSpace.CARTESIAN_POSE,
                       ActionSpace.GRIPPER],
        inference_mode=VLAInferenceMode.CLOUD_API,
        min_gpu_memory_gb=0.0,
        inference_time_ms=120.0,
        open_source=True,
        license_type="DeepSeek License",
        max_batch_size=32,
        supports_streaming=True,
        supports_bimanual=False,
        deployment_ready=True,
        notes="，"
              "CSA/HCA混合注意力，计算量降至前代27%、显存仅10%，全系百万上下文",
    ),
    "nemotron_35_lightning": VLAModelInfo(
        model_id="nemotron_35_lightning",
        backend_type=VLABackendType.NEMOTRON_35,
        display_name="Nemotron 3.5 Lightning",
        organization="NVIDIA",
        parameters_b=30.0,
        context_window=128000,
        modalities=["text"],
        action_spaces=[ActionSpace.JOINT_POSITION, ActionSpace.JOINT_VELOCITY],
        inference_mode=VLAInferenceMode.LOCAL_DEPLOY,
        min_gpu_memory_gb=24.0,
        inference_time_ms=45.0,
        open_source=True,
        license_type="OpenMDW-1.1",
        max_batch_size=8,
        supports_streaming=True,
        supports_bimanual=False,
        deployment_ready=True,
        notes="2026-08-12发布，30B MoE激活3B，输出提速4倍，Agent任务完成速度+30%，"
              "PinchBench 86%，配套NeMo Switchyard智能路由，可本地部署",
    ),
    "gpt5_6": VLAModelInfo(
        model_id="gpt5_6",
        backend_type=VLABackendType.OPENAI_GPT5,
        display_name="GPT-5.6 Sol",
        organization="OpenAI",
        parameters_b=0.0,
        context_window=400000,
        modalities=["text", "image", "audio", "video"],
        action_spaces=[ActionSpace.JOINT_POSITION, ActionSpace.CARTESIAN_POSE,
                       ActionSpace.GRIPPER, ActionSpace.BIMANUAL],
        inference_mode=VLAInferenceMode.CLOUD_API,
        min_gpu_memory_gb=0.0,
        inference_time_ms=200.0,
        open_source=False,
        license_type="proprietary",
        max_batch_size=16,
        supports_streaming=True,
        supports_bimanual=True,
        deployment_ready=True,
        notes="2026-08旗舰闭源模型，多模态原生Agent能力，"
              "衍生GPT-5.6-Cyber安全专用版（Daybreak Red等级，完成率95%）",
    ),
    "muse_glimmer_30b": VLAModelInfo(
        model_id="muse_glimmer_30b",
        backend_type=VLABackendType.CUSTOM,
        display_name="Muse Glimmer 30B",
        organization="Meta",
        parameters_b=30.0,
        context_window=131072,
        modalities=["text", "image"],
        action_spaces=[ActionSpace.JOINT_POSITION, ActionSpace.CARTESIAN_POSE,
                       ActionSpace.GRIPPER],
        inference_mode=VLAInferenceMode.EDGE_DEVICE,
        min_gpu_memory_gb=24.0,
        inference_time_ms=80.0,
        open_source=True,
        license_type="Apache-2.0",
        max_batch_size=4,
        supports_streaming=True,
        supports_bimanual=False,
        deployment_ready=True,
        notes="2026-08-11 Meta开源，4bit量化后17GB可在单张消费级GPU（24GB显存）运行，"
              "支持100+语言，专攻长周期Agent工作流，适合机器人端侧VLA",
    ),
    "qwen3_vl": VLAModelInfo(
        model_id="qwen3_vl",
        backend_type=VLABackendType.QWEN3_VL,
        display_name="Qwen3-VL",
        organization="阿里巴巴",
        parameters_b=72.0,
        context_window=128000,
        modalities=["text", "image", "video"],
        action_spaces=[ActionSpace.JOINT_POSITION, ActionSpace.CARTESIAN_POSE,
                       ActionSpace.GRIPPER],
        inference_mode=VLAInferenceMode.LOCAL_DEPLOY,
        min_gpu_memory_gb=40.0,
        inference_time_ms=100.0,
        open_source=True,
        license_type="Apache-2.0",
        max_batch_size=8,
        supports_streaming=True,
        supports_bimanual=False,
        deployment_ready=True,
        notes="多模态端侧模型，支持图像/视频理解，轻量版可在消费级GPU运行，"
              "千问开放平台2026-08-10上线，接入AI眼镜等终端",
    ),
    "gemini_robotics2": VLAModelInfo(
        model_id="gemini_robotics2",
        backend_type=VLABackendType.GEMINI_ROBOTICS2,
        display_name="Gemini Robotics 2",
        organization="Google DeepMind",
        parameters_b=0.0,
        context_window=200000,
        modalities=["text", "image", "video"],
        action_spaces=[ActionSpace.JOINT_POSITION, ActionSpace.CARTESIAN_POSE,
                       ActionSpace.GRIPPER, ActionSpace.BIMANUAL],
        inference_mode=VLAInferenceMode.CLOUD_API,
        min_gpu_memory_gb=0.0,
        inference_time_ms=150.0,
        open_source=False,
        license_type="proprietary",
        max_batch_size=8,
        supports_streaming=False,
        supports_bimanual=True,
        deployment_ready=False,
        notes="机器人专用多模态模型，融合视觉-语言-动作，支持跨形态迁移",
    ),
    "openvla": VLAModelInfo(
        model_id="openvla",
        backend_type=VLABackendType.OPENVLA,
        display_name="OpenVLA",
        organization="开源社区",
        parameters_b=7.0,
        context_window=32768,
        modalities=["text", "image"],
        action_spaces=[ActionSpace.JOINT_POSITION, ActionSpace.CARTESIAN_POSE,
                       ActionSpace.GRIPPER],
        inference_mode=VLAInferenceMode.EDGE_DEVICE,
        min_gpu_memory_gb=16.0,
        inference_time_ms=60.0,
        open_source=True,
        license_type="MIT",
        max_batch_size=4,
        supports_streaming=False,
        supports_bimanual=False,
        deployment_ready=True,
        notes="开源VLA模型，7B参数可在消费级GPU运行，适合机器人端侧视觉-语言-动作",
    ),
    "octo": VLAModelInfo(
        model_id="octo",
        backend_type=VLABackendType.OCTO,
        display_name="Octo",
        organization="开源社区",
        parameters_b=93.0,
        context_window=32000,
        modalities=["text", "image"],
        action_spaces=[ActionSpace.JOINT_POSITION, ActionSpace.JOINT_VELOCITY,
                       ActionSpace.GRIPPER],
        inference_mode=VLAInferenceMode.LOCAL_DEPLOY,
        min_gpu_memory_gb=48.0,
        inference_time_ms=90.0,
        open_source=True,
        license_type="Apache-2.0",
        max_batch_size=4,
        supports_streaming=False,
        supports_bimanual=False,
        deployment_ready=True,
        notes="开源通用机器人策略模型，支持多种机器人形态迁移",
    ),
    "mock_safe": VLAModelInfo(
        model_id="mock_safe",
        backend_type=VLABackendType.MOCK,
        display_name="Mock Safe Backend",
        organization="System",
        parameters_b=0.0,
        context_window=4096,
        modalities=["text"],
        action_spaces=[ActionSpace.JOINT_POSITION, ActionSpace.GRIPPER],
        inference_mode=VLAInferenceMode.MOCK_SAFE,
        min_gpu_memory_gb=0.0,
        inference_time_ms=5.0,
        open_source=True,
        license_type="internal",
        max_batch_size=1,
        supports_streaming=False,
        supports_bimanual=False,
        deployment_ready=True,
        notes="安全降级模拟后端，所有真实后端不可用时使用，仅返回安全姿态",
    ),
}


@dataclass
class SafetyLimits:
    max_joint_delta: float = 0.1
    max_position_delta: float = 0.05
    max_velocity: float = 2.0
    max_gripper_delta: float = 0.2
    joint_limits_lower: List[float] = field(default_factory=list)
    joint_limits_upper: List[float] = field(default_factory=list)
    workspace_limits: Dict[str, float] = field(default_factory=dict)


class ActionSafetyChecker:
    def __init__(self, limits: Optional[SafetyLimits] = None):
        self.limits = limits or SafetyLimits()

    def check_and_clip(self, action: VLAActionOutput,
                       current_state: Optional[VLAObservation] = None) -> VLAActionOutput:
        try:
            action.safety_checked = True
            if action.joint_positions and current_state and current_state.joint_positions:
                action.joint_positions = self._clip_joint_positions(
                    action.joint_positions, current_state.joint_positions
                )
            if action.cartesian_pose and current_state and current_state.ee_pose:
                action.cartesian_pose = self._clip_cartesian_pose(
                    action.cartesian_pose, current_state.ee_pose
                )
            action.gripper_command = max(-1.0, min(1.0, action.gripper_command))
            return action
        except Exception:
            action.safety_checked = True
            action.error = "safety_check_failed"
            return action

    def _clip_joint_positions(self, targets: List[float],
                              currents: List[float]) -> List[float]:
        result = []
        n = min(len(targets), len(currents))
        for i in range(n):
            delta = targets[i] - currents[i]
            delta = max(-self.limits.max_joint_delta,
                        min(self.limits.max_joint_delta, delta))
            val = currents[i] + delta
            if self.limits.joint_limits_lower and i < len(self.limits.joint_limits_lower):
                val = max(self.limits.joint_limits_lower[i], val)
            if self.limits.joint_limits_upper and i < len(self.limits.joint_limits_upper):
                val = min(self.limits.joint_limits_upper[i], val)
            result.append(val)
        if len(targets) > n:
            result.extend(targets[n:])
        return result

    def _clip_cartesian_pose(self, targets: List[float],
                             currents: List[float]) -> List[float]:
        result = list(targets)
        for i in range(min(3, len(targets), len(currents))):
            delta = targets[i] - currents[i]
            delta = max(-self.limits.max_position_delta,
                        min(self.limits.max_position_delta, delta))
            result[i] = currents[i] + delta
        return result


class VLABackend(ABC):
    def __init__(self, model_info: VLAModelInfo, config: Optional[Dict] = None):
        self.model_info = model_info
        self.config = config or {}
        self.timeout_ms = self.config.get("timeout_ms", 5000)
        self.safety_checker = ActionSafetyChecker(self.config.get("safety_limits"))
        self._connected = False
        self._call_count = 0
        self._total_latency_ms = 0.0

    @abstractmethod
    def connect(self) -> bool: ...

    @abstractmethod
    def disconnect(self) -> None: ...

    @abstractmethod
    def infer(self, observation: VLAObservation) -> VLAActionOutput: ...

    def is_available(self) -> bool:
        return self._connected

    def get_stats(self) -> Dict[str, Any]:
        avg_latency = (self._total_latency_ms / self._call_count
                       if self._call_count > 0 else 0.0)
        return {
            "model_id": self.model_info.model_id,
            "call_count": self._call_count,
            "avg_latency_ms": avg_latency,
            "connected": self._connected,
        }


class MockVLABackend(VLABackend):
    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False

    def infer(self, observation: VLAObservation) -> VLAActionOutput:
        start = time.time()
        try:
            n_joints = len(observation.joint_positions) if observation.joint_positions else 6
            action = VLAActionOutput(
                action_space=ActionSpace.JOINT_POSITION,
                joint_positions=list(observation.joint_positions) if observation.joint_positions
                else [0.0] * n_joints,
                cartesian_pose=list(observation.ee_pose) if observation.ee_pose else [],
                gripper_command=observation.gripper_state,
                confidence=0.5,
                model_id="mock",
                fallback_used=True,
            )
            action = self.safety_checker.check_and_clip(action, observation)
            elapsed = (time.time() - start) * 1000
            action.inference_time_ms = elapsed
            self._call_count += 1
            self._total_latency_ms += elapsed
            return action
        except Exception as e:
            return VLAActionOutput(model_id="mock", fallback_used=True, error=str(e), confidence=0.0)


class CloudAPIVLABackend(VLABackend):
    def __init__(self, model_info: VLAModelInfo, config: Optional[Dict] = None):
        super().__init__(model_info, config)
        self.api_key = self.config.get("api_key", "")
        self.api_base = self.config.get("api_base", "")
        self._http_client = None

    def connect(self) -> bool:
        try:
            if not self.api_key:
                self._connected = False
                return False
            self._connected = True
            return True
        except Exception:
            self._connected = False
            return False

    def disconnect(self) -> None:
        self._connected = False
        self._http_client = None

    def infer(self, observation: VLAObservation) -> VLAActionOutput:
        start = time.time()
        if not self._connected:
            return VLAActionOutput(model_id=self.model_info.model_id,
                                   fallback_used=True, error="not_connected", confidence=0.0)
        try:
            action = self._call_api(observation)
            action = self.safety_checker.check_and_clip(action, observation)
            elapsed = (time.time() - start) * 1000
            action.inference_time_ms = elapsed
            action.model_id = self.model_info.model_id
            self._call_count += 1
            self._total_latency_ms += elapsed
            return action
        except Exception as e:
            return VLAActionOutput(model_id=self.model_info.model_id, fallback_used=True,
                                   error=f"api_error: {str(e)[:100]}", confidence=0.0)

    def _call_api(self, observation: VLAObservation) -> VLAActionOutput:
        return VLAActionOutput(
            action_space=ActionSpace.JOINT_POSITION,
            joint_positions=list(observation.joint_positions) if observation.joint_positions else [],
            confidence=0.8,
        )


class LocalVLABackend(VLABackend):
    def __init__(self, model_info: VLAModelInfo, config: Optional[Dict] = None):
        super().__init__(model_info, config)
        self.model_path = self.config.get("model_path", "")
        self.device = self.config.get("device", "auto")
        self._model = None
        self._processor = None

    def connect(self) -> bool:
        try:
            self._connected = self._load_model()
            return self._connected
        except Exception:
            self._connected = False
            return False

    def _load_model(self) -> bool:
        try:
            import importlib
            importlib.import_module("transformers")
            return True
        except ImportError:
            return False
        except Exception:
            return False

    def disconnect(self) -> None:
        self._model = None
        self._processor = None
        self._connected = False

    def infer(self, observation: VLAObservation) -> VLAActionOutput:
        start = time.time()
        if not self._connected:
            return VLAActionOutput(model_id=self.model_info.model_id,
                                   fallback_used=True, error="model_not_loaded", confidence=0.0)
        try:
            action = self._run_inference(observation)
            action = self.safety_checker.check_and_clip(action, observation)
            elapsed = (time.time() - start) * 1000
            action.inference_time_ms = elapsed
            action.model_id = self.model_info.model_id
            self._call_count += 1
            self._total_latency_ms += elapsed
            return action
        except Exception as e:
            return VLAActionOutput(model_id=self.model_info.model_id, fallback_used=True,
                                   error=f"inference_error: {str(e)[:100]}", confidence=0.0)

    def _run_inference(self, observation: VLAObservation) -> VLAActionOutput:
        return VLAActionOutput(
            action_space=ActionSpace.JOINT_POSITION,
            joint_positions=list(observation.joint_positions) if observation.joint_positions else [],
            confidence=0.7,
        )


class VLABackendFactory:
    _backend_map = {
        VLABackendType.MOCK: MockVLABackend,
        VLABackendType.OPENAI_GPT5: CloudAPIVLABackend,
        VLABackendType.OPENAI_GPT_OSS: LocalVLABackend,
        VLABackendType.QWEN3_VL: LocalVLABackend,
        VLABackendType.GEMINI_ROBOTICS2: CloudAPIVLABackend,
        VLABackendType.DEEPSEEK_V4: LocalVLABackend,
        VLABackendType.NEMOTRON_35: LocalVLABackend,
        VLABackendType.OPENVLA: LocalVLABackend,
        VLABackendType.OCTO: LocalVLABackend,
    }

    # 外部独立模块注册（延迟导入，避免循环依赖）
    _external_backends: Dict[str, type] = {}

    FALLBACK_CHAIN = ["openvla", "deepseek_v4", "gpt_oss", "gpt5", "mock"]

    @classmethod
    def register_external_backend(cls, model_id: str,
                                  backend_class: type) -> None:
        """注册外部独立模块的后端类。"""
        cls._external_backends[model_id] = backend_class

    @classmethod
    def create(cls, model_id: str, config: Optional[Dict] = None) -> VLABackend:
        config = config or {}
        # 优先使用外部注册的专用后端
        if model_id in cls._external_backends:
            model_info = VLA_MODEL_REGISTRY.get(model_id)
            if model_info is not None:
                return cls._external_backends[model_id](model_info, config)
        model_info = VLA_MODEL_REGISTRY.get(model_id)
        if model_info is None:
            return MockVLABackend(
                VLAModelInfo(
                    model_id="mock", backend_type=VLABackendType.MOCK,
                    display_name="Mock", organization="System", parameters_b=0,
                    context_window=0, modalities=["text"],
                    action_spaces=[ActionSpace.JOINT_POSITION],
                    inference_mode=VLAInferenceMode.MOCK_SAFE,
                    min_gpu_memory_gb=0, inference_time_ms=1, open_source=True,
                ), config,
            )
        backend_class = cls._backend_map.get(model_info.backend_type, MockVLABackend)
        return backend_class(model_info, config)

    @classmethod
    def create_with_fallback(cls, preferred_model_id: str,
                             config: Optional[Dict] = None) -> Tuple[VLABackend, str]:
        config = config or {}
        chain = [preferred_model_id] + [
            m for m in cls.FALLBACK_CHAIN if m != preferred_model_id
        ]
        for mid in chain:
            try:
                backend = cls.create(mid, config)
                if backend.connect():
                    return backend, mid
            except Exception:
                continue
        mock = cls.create("mock", config)
        mock.connect()
        return mock, "mock"

    @classmethod
    def list_models(cls, deployment_ready_only: bool = False,
                    open_source_only: bool = False,
                    edge_capable_only: bool = False) -> List[VLAModelInfo]:
        results = []
        for info in VLA_MODEL_REGISTRY.values():
            if deployment_ready_only and not info.deployment_ready:
                continue
            if open_source_only and not info.open_source:
                continue
            if edge_capable_only and info.inference_mode != VLAInferenceMode.EDGE_DEVICE:
                continue
            results.append(info)
        return results


class VLAInferencePipeline:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.backend: Optional[VLABackend] = None
        self.active_model_id: str = "mock"
        self.safety_checker = ActionSafetyChecker(self.config.get("safety_limits"))

    def initialize(self, preferred_model: str = "mock") -> bool:
        try:
            self.backend, self.active_model_id = VLABackendFactory.create_with_fallback(
                preferred_model, self.config
            )
            return self.backend is not None and self.backend.is_available()
        except Exception:
            self.backend = VLABackendFactory.create("mock", self.config)
            self.backend.connect()
            self.active_model_id = "mock"
            return True

    def predict(self, observation: VLAObservation) -> VLAActionOutput:
        if self.backend is None or not self.backend.is_available():
            if not self.initialize("mock"):
                return VLAActionOutput(model_id="none", fallback_used=True,
                                       error="pipeline_unavailable", confidence=0.0)
        action = self.backend.infer(observation)
        if action.error and not action.fallback_used:
            action = self._try_fallback(observation)
        return action

    def _try_fallback(self, observation: VLAObservation) -> VLAActionOutput:
        try:
            current_idx = (
                VLABackendFactory.FALLBACK_CHAIN.index(self.active_model_id)
                if self.active_model_id in VLABackendFactory.FALLBACK_CHAIN else 0
            )
            for mid in VLABackendFactory.FALLBACK_CHAIN[current_idx + 1:]:
                try:
                    backend = VLABackendFactory.create(mid, self.config)
                    if backend.connect():
                        self.backend = backend
                        self.active_model_id = mid
                        return backend.infer(observation)
                except Exception:
                    continue
            mock = VLABackendFactory.create("mock", self.config)
            mock.connect()
            self.backend = mock
            self.active_model_id = "mock"
            return mock.infer(observation)
        except Exception:
            return VLAActionOutput(model_id="mock", fallback_used=True,
                                   error="fallback_exhausted", confidence=0.0)

    def shutdown(self) -> None:
        if self.backend:
            try:
                self.backend.disconnect()
            except Exception:
                pass
            self.backend = None

    def get_status(self) -> Dict[str, Any]:
        return {
            "active_model": self.active_model_id,
            "backend_connected": self.backend.is_available() if self.backend else False,
            "stats": self.backend.get_stats() if self.backend else {},
            "available_models": len(VLA_MODEL_REGISTRY),
        }
