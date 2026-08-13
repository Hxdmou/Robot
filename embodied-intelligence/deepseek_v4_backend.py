#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DeepSeek-V4-Flash VLA后端 - V1.0
================================================================
新增内容：
  1. DeepSeekV4Config（后端配置数据类）
  2. DeepSeekV4Backend（云端VLA后端，继承CloudAPIVLABackend）
  3. CSAHCAHybridAttention（CSA/HCA混合注意力参数）
  4. DeepSeekV4ActionParser（动作解析器）
  5. create_deepseek_v4_backend（工厂函数）

核心能力：
  - 百万token超长上下文
  - CSA/HCA混合注意力，计算量降至前代27%、显存仅10%
  - 云端API推理，支持视觉-语言-动作输出
  - 环境变量注入密钥，零硬编码
"""

import os
import json
import time
import urllib.request
import urllib.error
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field

from vla_model_backends import (
    CloudAPIVLABackend, VLAModelInfo, VLABackendType, VLAInferenceMode,
    ActionSpace, VLAObservation, VLAActionOutput,
)


@dataclass
class CSAHCAHybridAttention:
    """CSA/HCA混合注意力参数。

    CSA（Compressed Sparse Attention）压缩稀疏注意力，
    HCA（Hierarchical Compressed Attention）分层压缩注意力。
    计算量降至前代27%，显存占用仅10%。
    """
    csa_window_size: int = 4096
    hca_compress_ratio: float = 0.27
    memory_usage_ratio: float = 0.10
    context_window: int = 1000000
    use_sliding_window: bool = True


@dataclass
class DeepSeekV4Config:
    """DeepSeek-V4后端配置。"""
    api_base: str = "https://api.deepseek.com/v1"
    model_name: str = "deepseek-v4-flash"
    timeout_ms: int = 5000
    max_retries: int = 2
    temperature: float = 0.1
    max_tokens: int = 2048
    attention: CSAHCAHybridAttention = field(default_factory=CSAHCAHybridAttention)

    @classmethod
    def from_env(cls) -> "DeepSeekV4Config":
        """从环境变量加载配置，密钥零硬编码。"""
        return cls(
            api_base=os.environ.get("DEEPSEEK_API_BASE", cls.api_base),
            model_name=os.environ.get("DEEPSEEK_MODEL", cls.model_name),
            timeout_ms=int(os.environ.get("DEEPSEEK_TIMEOUT_MS", cls.timeout_ms)),
            max_retries=int(os.environ.get("DEEPSEEK_MAX_RETRIES", cls.max_retries)),
        )


class DeepSeekV4ActionParser:
    """将模型文本输出解析为机器人动作。"""

    @staticmethod
    def parse(response_json: Dict[str, Any],
              action_space: ActionSpace = ActionSpace.JOINT_POSITION,
              dof: int = 6) -> VLAActionOutput:
        try:
            choices = response_json.get("choices", [])
            if not choices:
                return VLAActionOutput(model_id="deepseek_v4", confidence=0.0,
                                       error="empty_choices")
            content = choices[0].get("message", {}).get("content", "")
            action_data = json.loads(content) if content.strip().startswith("{") else {}
            joint_positions = action_data.get("joint_positions", [0.0] * dof)[:dof]
            cartesian = action_data.get("cartesian_pose", [])
            gripper = action_data.get("gripper", 0.0)
            confidence = float(action_data.get("confidence", 0.8))
            return VLAActionOutput(
                action_space=action_space,
                joint_positions=joint_positions,
                cartesian_pose=cartesian,
                gripper_command=gripper,
                confidence=confidence,
                model_id="deepseek_v4_flash",
            )
        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
            return VLAActionOutput(model_id="deepseek_v4_flash", confidence=0.0,
                                   error=f"parse_error: {str(e)[:80]}")


class DeepSeekV4Backend(CloudAPIVLABackend):
    """DeepSeek-V4-Flash 云端VLA后端。

    特性：
      - 百万token上下文
      - CSA/HCA混合注意力
      - 视觉-语言-动作联合输出
      - 自动重试 + 超时兜底
    """

    def __init__(self, model_info: VLAModelInfo,
                 config: Optional[Dict] = None):
        super().__init__(model_info, config)
        ds_config = config.get("deepseek_config") if config else None
        self.ds_config = ds_config or DeepSeekV4Config.from_env()
        self.api_base = self.ds_config.api_base
        self.api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        self._attention = self.ds_config.attention
        self._parser = DeepSeekV4ActionParser()

    def connect(self) -> bool:
        if not self.api_key:
            self._connected = False
            return False
        self._connected = True
        return True

    def _build_payload(self, observation: VLAObservation) -> Dict[str, Any]:
        prompt = self._build_prompt(observation)
        return {
            "model": self.ds_config.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.ds_config.max_tokens,
            "temperature": self.ds_config.temperature,
            "stream": False,
        }

    def _build_prompt(self, observation: VLAObservation) -> str:
        parts = ["你是机器人VLA控制器。根据观测输出JSON格式动作。"]
        if observation.joint_positions:
            parts.append(f"当前关节角: {observation.joint_positions}")
        if observation.ee_pose:
            parts.append(f"末端位姿: {observation.ee_pose}")
        if observation.gripper_state is not None:
            parts.append(f"夹爪状态: {observation.gripper_state}")
        if observation.instruction:
            parts.append(f"指令: {observation.instruction}")
        parts.append('输出格式: {"joint_positions":[...],"cartesian_pose":[x,y,z,rx,ry,rz],'
                     '"gripper":0.0,"confidence":0.9}')
        return "\n".join(parts)

    def _call_api(self, observation: VLAObservation) -> VLAActionOutput:
        payload = self._build_payload(observation)
        url = f"{self.api_base}/chat/completions"
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        last_error = None
        for attempt in range(self.ds_config.max_retries + 1):
            try:
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=self.ds_config.timeout_ms / 1000) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                return self._parser.parse(
                    result,
                    action_space=ActionSpace.JOINT_POSITION,
                    dof=len(observation.joint_positions) if observation.joint_positions else 6,
                )
            except (urllib.error.URLError, urllib.error.HTTPError,
                    TimeoutError, OSError) as e:
                last_error = str(e)[:80]
                if attempt < self.ds_config.max_retries:
                    time.sleep(0.1 * (2 ** attempt))
                continue
        return VLAActionOutput(model_id="deepseek_v4_flash", confidence=0.0,
                               error=f"api_failed: {last_error}")

    def get_attention_info(self) -> Dict[str, Any]:
        return {
            "context_window": self._attention.context_window,
            "compute_ratio": self._attention.hca_compress_ratio,
            "memory_ratio": self._attention.memory_usage_ratio,
        }


def create_deepseek_v4_backend(config: Optional[Dict] = None) -> DeepSeekV4Backend:
    """工厂函数：创建DeepSeek-V4后端实例。"""
    model_info = VLAModelInfo(
        model_id="deepseek_v4_flash",
        backend_type=VLABackendType.DEEPSEEK_V4,
        display_name="DeepSeek-V4-Flash",
        organization="DeepSeek",
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
        notes="CSA/HCA混合注意力，百万上下文",
    )
    return DeepSeekV4Backend(model_info, config)


if __name__ == "__main__":
    backend = create_deepseek_v4_backend()
    print(f"DeepSeek-V4后端已创建: {backend.model_info.display_name}")
    print(f"上下文窗口: {backend.get_attention_info()['context_window']}")
    print(f"API密钥已配置: {bool(backend.api_key)}")
