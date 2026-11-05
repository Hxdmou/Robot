"""
Sim2Real 域随机化框架（工程参数版）
================================================
提供在仿真环境中对「物理参数 / 环境参数」做统计分布随机化的能力，
用于缩小 sim→real 迁移时的 reality gap。

包含参数（框架展示：每个参数定义范围+采样函数，不含任何品牌私有参数值）：
  - 表面摩擦系数（库伦摩擦 + 粘性摩擦）
  - 关节阻尼系数
  - 连杆质量扰动（±百分比）
  - 齿轮间隙 / 关节跳动（工业精度维度）
  - 温度系数（影响驱动器热漂移）
  - 电压波动（电池/供电扰动）
  - 传感器噪声（编码器/力矩/视觉）
  - 光照强度 & 颜色偏移（视觉Sim2Real）
  - 延迟抖动（通信与控制环）
  - 光缆损耗（算力互联场景通用参数）

说明：本文件不涉及算法训练（例如 Domain Randomization 与 PPO/SAC 的
      curriculum 联合训练），仅展示「参数分布管理 + 场景采样」的工程框架层。
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# ============================================================
# 参数分布类型
# ============================================================
class DistributionType:
    UNIFORM = "uniform"          # 均匀分布 uniform(low, high)
    NORMAL = "normal"            # 正态分布 normal(mean, std)，支持截断
    CHOICE = "choice"            # 离散选项 choice([options])
    CONSTANT = "constant"        # 固定常数（默认无扰动）


@dataclass
class ParameterSpec:
    """单个随机化参数的规格定义"""
    name: str
    category: str                         # 如 "friction" "damping" "sensor_noise"
    dist_type: str = DistributionType.UNIFORM
    # 根据分布类型填写以下参数（框架使用其中合适的）
    low: float = 0.0
    high: float = 0.0
    mean: float = 0.0
    std: float = 0.0
    choices: List[Any] = field(default_factory=list)
    constant_value: Any = None
    # 可选：截断（仅对NORMAL生效）
    clip_low: Optional[float] = None
    clip_high: Optional[float] = None
    # 元信息
    unit: str = ""
    description: str = ""
    enabled: bool = True


# ============================================================
# 参数规格集合（展示Sim2Real工程上常见的 ≥10 维）
# ============================================================
def build_default_parameter_specs() -> List[ParameterSpec]:
    """
    默认参数集（公共示例版）
    返回一组具代表性的Sim2Real参数，用于展示「多维度联合随机化」设计思路。
    """
    return [
        # --- 1. 表面摩擦 ---
        ParameterSpec(
            "surface_lateral_friction", "friction",
            dist_type=DistributionType.UNIFORM, low=0.30, high=0.80,
            unit="-", description="物体接触面侧向摩擦系数（μ）",
        ),
        ParameterSpec(
            "surface_spinning_friction", "friction",
            dist_type=DistributionType.UNIFORM, low=0.001, high=0.02,
            unit="-", description="绕法线自旋摩擦",
        ),
        # --- 2. 关节阻尼 ---
        ParameterSpec(
            "joint_damping", "dynamics",
            dist_type=DistributionType.NORMAL,
            mean=0.15, std=0.04, clip_low=0.05, clip_high=0.40,
            unit="N·m·s/rad", description="关节粘性阻尼系数（7关节共用分布）",
        ),
        # --- 3. 连杆质量扰动（相对标称 ±百分比）---
        ParameterSpec(
            "link_mass_percent_error", "dynamics",
            dist_type=DistributionType.NORMAL,
            mean=0.0, std=0.05, clip_low=-0.12, clip_high=0.12,
            unit="ratio", description="连杆质量相对误差 ±百分比",
        ),
        # --- 4. 工业精度：齿轮间隙 ---
        ParameterSpec(
            "gear_backlash_rad", "mechanical",
            dist_type=DistributionType.UNIFORM, low=0.0, high=math.radians(0.15),
            unit="rad", description="关节齿轮回差（发丝级）",
        ),
        # --- 5. 工业精度：关节跳动 ---
        ParameterSpec(
            "joint_runout_ratio", "mechanical",
            dist_type=DistributionType.UNIFORM, low=0.0, high=0.005,
            unit="ratio", description="关节径向跳动量比例",
        ),
        # --- 6. 温度 ---
        ParameterSpec(
            "ambient_temperature_c", "thermal",
            dist_type=DistributionType.UNIFORM, low=18.0, high=35.0,
            unit="°C", description="环境温度（影响驱动器热漂移）",
        ),
        # --- 7. 电压波动 ---
        ParameterSpec(
            "supply_voltage_percent", "electrical",
            dist_type=DistributionType.NORMAL,
            mean=1.0, std=0.02, clip_low=0.94, clip_high=1.06,
            unit="ratio", description="供电电压相对标称比例（1.0 = 48V）",
        ),
        # --- 8. 传感器噪声：编码器分辨率 ---
        ParameterSpec(
            "encoder_resolution_bits", "sensor",
            dist_type=DistributionType.CHOICE,
            choices=[15, 17, 19, 20, 22],
            unit="bit/rev", description="关节编码器位数",
        ),
        # --- 9. 传感器噪声：关节力矩噪声 ---
        ParameterSpec(
            "joint_torque_noise_std", "sensor",
            dist_type=DistributionType.UNIFORM, low=0.005, high=0.05,
            unit="N·m", description="关节力矩传感读取高斯噪声σ",
        ),
        # --- 10. 视觉：光照强度 ---
        ParameterSpec(
            "lighting_intensity_ratio", "vision",
            dist_type=DistributionType.UNIFORM, low=0.6, high=1.4,
            unit="ratio", description="场景光照相对标称强度",
        ),
        # --- 11. 延迟抖动：控制环 ---
        ParameterSpec(
            "control_loop_jitter_ms", "communication",
            dist_type=DistributionType.UNIFORM, low=0.0, high=2.0,
            unit="ms", description="控制环调度抖动",
        ),
        # --- 12. 光缆损耗：算力互联（可用于光互联场景通用示例）---
        ParameterSpec(
            "optical_fiber_loss_db_per_km", "datacenter",
            dist_type=DistributionType.UNIFORM, low=0.2, high=0.4,
            unit="dB/km", description="光纤链路每公里损耗（通用参数）",
        ),
    ]


# ============================================================
# 采样器
# ============================================================
class ParameterSampler:
    """按 ParameterSpec 中声明的分布类型执行采样"""

    @staticmethod
    def sample(spec: ParameterSpec, rng: Optional[random.Random] = None) -> Any:
        r = rng or random
        if not spec.enabled:
            return spec.constant_value
        if spec.dist_type == DistributionType.CONSTANT:
            return spec.constant_value
        if spec.dist_type == DistributionType.CHOICE:
            return r.choice(spec.choices) if spec.choices else None
        if spec.dist_type == DistributionType.UNIFORM:
            return r.uniform(spec.low, spec.high)
        if spec.dist_type == DistributionType.NORMAL:
            v = r.gauss(spec.mean, spec.std)
            if spec.clip_low  is not None: v = max(spec.clip_low,  v)
            if spec.clip_high is not None: v = min(spec.clip_high, v)
            return v
        raise ValueError(f"未知分布类型: {spec.dist_type}")


# ============================================================
# 域随机化管理器
# ============================================================
@dataclass
class RandomizationSample:
    """一次完整采样结果（episode级）"""
    episode_id: int
    sample_ts: float
    values: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)

    def get(self, name: str, default: Any = None) -> Any:
        return self.values.get(name, default)

    def summary(self) -> str:
        items = []
        for k, v in self.values.items():
            if isinstance(v, float):
                items.append(f"{k}={v:.5f}")
            else:
                items.append(f"{k}={v!r}")
        return "Sim2RealSample | " + " | ".join(items[:8]) + (
            f" ... (+{len(items)-8} 项)" if len(items) > 8 else "")


class DomainRandomizationManager:
    """
    域随机化管理器
    ------------------------------------------------
    用法：
        >>> dr = DomainRandomizationManager()
        >>> sample = dr.randomize_episode(episode_id=42)
        >>> print(sample.summary())
        >>> friction = sample.get("surface_lateral_friction")
    """

    def __init__(
        self,
        specs: Optional[List[ParameterSpec]] = None,
        seed: Optional[int] = None,
    ):
        self.specs: List[ParameterSpec] = specs or build_default_parameter_specs()
        self._rng = random.Random(seed) if seed is not None else random.Random()
        self._history: List[RandomizationSample] = []
        self._current: Optional[RandomizationSample] = None

    # ---- 规格管理 ----
    def add_spec(self, spec: ParameterSpec) -> None:
        # 若同名覆盖，否则追加
        for i, s in enumerate(self.specs):
            if s.name == spec.name:
                self.specs[i] = spec
                return
        self.specs.append(spec)

    def disable(self, param_name: str) -> bool:
        for s in self.specs:
            if s.name == param_name:
                s.enabled = False
                return True
        return False

    def enable(self, param_name: str) -> bool:
        for s in self.specs:
            if s.name == param_name:
                s.enabled = True
                return True
        return False

    # ---- 采样 ----
    def randomize_episode(self, episode_id: int = 0,
                          **meta) -> RandomizationSample:
        """执行一次episode级的全量参数随机化"""
        values: Dict[str, Any] = {}
        for spec in self.specs:
            values[spec.name] = ParameterSampler.sample(spec, self._rng)
        sample = RandomizationSample(
            episode_id=episode_id,
            sample_ts=float(__import__("time").time()),
            values=values,
            meta=meta,
        )
        self._current = sample
        self._history.append(sample)
        # 控制历史大小，避免OOM
        if len(self._history) > 5000:
            self._history = self._history[-5000:]
        return sample

    # ---- 对 PyBullet 的参考应用方法（框架示例，纯参数不碰具体模型）----
    def apply_to_pybullet_body_hints(self, body_id: int,
                                     client_id: int = 0) -> List[str]:
        """
        框架示例函数：展示如何把 sample 中参数「示意性」地应用到仿真中。

        说明：公共示例版仅列出「拟应用项」，不直接对 body_id 做真实修改，
              避免因未安装 pybullet 或无此 body 而抛异常。
              真实集成时可按注释实现。
        """
        if self._current is None:
            return []
        s = self._current
        applied_log: List[str] = []
        # 1) 摩擦：可调用 p.changeDynamics(body_id, link_idx,
        #                      lateralFriction=s.get("surface_lateral_friction"), ...)
        applied_log.append(
            f"拟应用: body={body_id} lateral_friction="
            f"{s.get('surface_lateral_friction'):.4f}"
        )
        # 2) 关节阻尼：可调用 p.changeDynamics(..., jointDamping=...)
        applied_log.append(
            f"拟应用: body={body_id} joint_damping="
            f"{s.get('joint_damping'):.5f}"
        )
        # 3) 质量扰动：可按 link_mass_percent_error * original_mass 更新
        applied_log.append(
            f"拟应用: body={body_id} link_mass_percent_error="
            f"{s.get('link_mass_percent_error'):+.3%}"
        )
        # 4) 其余参数（噪声/延迟/温度等）记录到 meta 供上层使用
        applied_log.append(
            f"元数据: 温度={s.get('ambient_temperature_c'):.1f}°C "
            f"电压比例={s.get('supply_voltage_percent'):.3f} "
            f"编码器={s.get('encoder_resolution_bits')}bit"
        )
        return applied_log

    # ---- 统计 & 报表 ----
    def total_parameters(self, enabled_only: bool = True) -> int:
        if enabled_only:
            return sum(1 for s in self.specs if s.enabled)
        return len(self.specs)

    def summary(self) -> Dict[str, Any]:
        return {
            "total_specs": len(self.specs),
            "enabled_specs": self.total_parameters(enabled_only=True),
            "categories": sorted({s.category for s in self.specs if s.enabled}),
            "history_length": len(self._history),
            "current": self._current.values if self._current else None,
        }

    def specs_table(self) -> str:
        lines = ["Sim2Real参数规格 (启用/总计={}/{})".format(
            self.total_parameters(True), self.total_parameters(False))]
        lines.append(
            f"{'NAME':<36} {'CATEGORY':<15} {'DISTR':<9} "
            f"{'RANGE/MEAN±STD':<24} {'UNIT':<12} {'ENABLED':<7}"
        )
        for s in self.specs:
            if s.dist_type == DistributionType.UNIFORM:
                rng = f"[{s.low:.4f}, {s.high:.4f}]"
            elif s.dist_type == DistributionType.NORMAL:
                rng = f"μ={s.mean:.4f} σ={s.std:.4f}"
            elif s.dist_type == DistributionType.CHOICE:
                rng = "{" + ",".join(repr(c) for c in s.choices[:4]) + (
                    ",..." if len(s.choices) > 4 else "") + "}"
            else:
                rng = str(s.constant_value)
            lines.append(
                f"{s.name:<36} {s.category:<15} {s.dist_type:<9} "
                f"{rng:<24} {s.unit:<12} {'YES' if s.enabled else 'NO':<7}"
            )
        return "\n".join(lines)
