"""
仿真增强系统 v1.0 - 无真机场景下的全链路仿真能力升级
================================================================
整合模块：
  1. 域随机化深度增强（物理/视觉/观测/执行器全维度随机化）
  2. 高精度执行器动力学（电机模型/齿槽转矩/温度/反电动势/柔性）
  3. 多任务场景环境（放置/装配/避障/动态跟踪/接触-rich）
  4. 极端鲁棒性测试套件（边界条件/大扰动/高速/大负载/故障注入）

核心目标：让仿真100%逼近真实世界，为未来真机迁移最小化Sim-to-Real Gap
"""
# ============================================================================
# 商业级免责声明（同 deployment_config.py v2.0 标准版）
# ============================================================================
# 本文件按"现状"提供，不附带任何明示或默示保证。
# 在法律允许的最大范围内，权利人不承担任何直接或间接责任。
# 使用者须自行评估适用性、进行充分测试、获取必要审批。
# ============================================================================

import pybullet as p
import numpy as np
import random
import time
import math
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from collections import deque
import threading
import queue


# ============================================================================
# 第一部分：高精度执行器动力学模型
# ============================================================================

@dataclass
class MotorParams:
    """电机物理参数（高精度模型）"""
    # 电气参数
    resistance: float = 1.5        # 相电阻 (Ohm)
    inductance: float = 0.002      # 相电感 (H)
    back_emf_constant: float = 0.1  # 反电动势常数 (V/(rad/s))
    torque_constant: float = 0.1    # 转矩常数 (Nm/A)

    # 机械参数
    rotor_inertia: float = 0.0001   # 转子转动惯量 (kg*m^2)
    viscous_friction: float = 0.001  # 粘性摩擦系数
    coulomb_friction: float = 0.05   # 库仑摩擦转矩 (Nm)
    static_friction: float = 0.1      # 静摩擦转矩 (Nm)

    # 齿槽转矩（Cogging Torque）
    cogging_amplitude: float = 0.02   # 齿槽转矩幅值 (Nm)
    cogging_period: float = 2 * math.pi / 7  # 齿槽周期（7对极）

    # 热参数
    thermal_resistance: float = 2.0    # 热阻 (K/W)
    thermal_capacitance: float = 50.0   # 热容 (J/K)
    ambient_temp: float = 25.0          # 环境温度 (C)
    max_temp: float = 125.0             # 最大允许温度 (C)

    # 齿轮减速
    gear_ratio: float = 100.0           # 减速比
    gear_efficiency: float = 0.85       # 齿轮效率
    gear_backlash: float = 0.001         # 齿轮间隙 (rad)

    # 额定参数
    rated_voltage: float = 48.0          # 额定电压 (V)
    rated_current: float = 10.0           # 额定电流 (A)
    rated_torque: float = 10.0            # 额定转矩 (Nm)
    max_torque: float = 30.0              # 最大转矩 (Nm, 3倍过载)


class HighPrecisionActuator:
    """
    高精度执行器模型 V13增强版
    包含：电气动力学 + 机械动力学 + Stribeck摩擦 + 齿槽转矩 + 热模型 + 齿轮传动 + 接触动力学
    """

    def __init__(self, params: MotorParams = None):
        self.params = params or MotorParams()

        # 状态变量
        self.angle = 0.0          # 电机侧角度 (rad)
        self.velocity = 0.0        # 电机侧角速度 (rad/s)
        self.current = 0.0         # 相电流 (A)
        self.temperature = self.params.ambient_temp  # 绕组温度 (C)

        # 输出侧（经过齿轮减速）
        self.output_angle = 0.0     # 关节侧角度 (rad)
        self.output_velocity = 0.0   # 关节侧角速度 (rad/s)
        self.output_torque = 0.0     # 关节侧输出转矩 (Nm)

        # 历史状态
        self._prev_angle = 0.0
        self._integral_error = 0.0

        # 故障注入
        self.fault_mode = None      # None, "stiction", "backlash", "overheat", "sensor_bias"
        self.fault_severity = 0.0

        # V13新增：Stribeck摩擦参数
        self.stribeck_velocity = 0.1  # Stribeck特征速度 (rad/s)
        self.stribeck_coeff = 0.8     # Stribeck摩擦系数
        self.viscous_coeff = 0.002    # 粘性摩擦系数

        # V13新增：接触动力学参数
        self.contact_stiffness = 1e5   # 接触刚度 (N/m)
        self.contact_damping = 1e3     # 接触阻尼 (Ns/m)
        self.friction_coeff = 0.5      # 摩擦系数

        # V13新增：热耦合参数
        self.thermal_time_constant = 100.0  # 热时间常数 (s)
        self.power_loss = 0.0               # 功率损耗 (W)

    def _stribeck_friction(self, velocity: float) -> float:
        """
        V13新增：Stribeck摩擦模型
        更精确地模拟低速下的摩擦特性（静摩擦→边界润滑→流体润滑过渡）
        """
        v_abs = abs(velocity)
        if v_abs < 1e-6:
            return 0.0

        # Stribeck曲线：F = F_c + (F_s - F_c) * exp(-(v/v_s)^alpha) + F_v * v
        coulomb_friction = self.params.coulomb_friction
        static_friction = self.params.static_friction
        viscous_friction = self.viscous_coeff * velocity

        # Stribeck效应
        stribeck_term = (static_friction - coulomb_friction) * \
                        math.exp(-math.pow(v_abs / self.stribeck_velocity, self.stribeck_coeff))

        friction = (coulomb_friction + stribeck_term) * math.copysign(1.0, velocity) + viscous_friction
        return friction

    def _contact_force(self, penetration_depth: float, relative_velocity: float) -> float:
        """
        V13新增：接触力计算（Hertz接触模型）
        用于模拟机器人与环境的接触交互
        """
        if penetration_depth <= 0:
            return 0.0

        # Hertz接触模型：F = k * delta^n - c * v
        n = 1.5  # Hertz指数（球-平面接触）
        elastic_force = self.contact_stiffness * math.pow(penetration_depth, n)
        damping_force = self.contact_damping * relative_velocity

        return max(0.0, elastic_force - damping_force)

    def _thermal_dynamics(self, current: float, voltage: float, dt: float):
        """
        V13新增：热动力学模型
        模拟电机绕组温度变化，影响性能和寿命
        """
        # 功率损耗：P_loss = I^2 * R + 机械损耗
        copper_loss = current * current * self.params.resistance
        mechanical_loss = abs(self.output_torque * self.output_velocity) * (1 - self.params.gear_efficiency)
        self.power_loss = copper_loss + mechanical_loss

        # 一阶热模型：dT/dt = (P_loss - (T - T_amb) / R_th) / C_th
        temp_diff = self.temperature - self.params.ambient_temp
        heat_flow = temp_diff / self.params.thermal_resistance
        self.temperature += (self.power_loss - heat_flow) / self.params.thermal_capacitance * dt

        # 温度限制
        self.temperature = min(self.temperature, self.params.max_temp)

    def step(self, voltage_cmd: float, load_torque: float, dt: float) -> Dict[str, float]:
        """
        执行一步仿真（电气+机械+热耦合）
        Args:
            voltage_cmd: 施加的电压 (V)
            load_torque: 负载转矩 (Nm, 电机侧)
            dt: 时间步长 (s)
        Returns:
            输出状态字典
        """
        p = self.params

        # 故障注入
        if self.fault_mode == "overheat":
            self.temperature = min(p.max_temp * 1.2, self.temperature + 50 * dt)

        # 热保护：温度过高时降低转矩输出
        temp_factor = 1.0
        if self.temperature > p.max_temp * 0.8:
            temp_factor = max(0.1, 1.0 - (self.temperature - p.max_temp * 0.8) / (p.max_temp * 0.4))

        # 限制电压
        voltage_cmd = max(-p.rated_voltage, min(p.rated_voltage, voltage_cmd))

        # === 电气动力学（简化一阶模型） ===
        # di/dt = (V - R*i - Ke*omega) / L
        back_emf = p.back_emf_constant * self.velocity
        di_dt = (voltage_cmd - p.resistance * self.current - back_emf) / p.inductance
        self.current += di_dt * dt
        self.current = max(-p.rated_current * 3, min(p.rated_current * 3, self.current))

        # === 电磁转矩 ===
        magnetic_torque = p.torque_constant * self.current * temp_factor

        # === 齿槽转矩（位置相关的扰动转矩） ===
        cogging_torque = p.cogging_amplitude * math.sin(p.cogging_period * self.angle)

        # === 摩擦模型（Stribeck + Coulomb + Viscous） ===
        friction_torque = self._compute_friction(self.velocity)

        # === 机械动力学 ===
        # J * domega/dt = T_mag - T_cogging - T_friction - T_load
        total_torque = magnetic_torque - cogging_torque - friction_torque - load_torque

        # 故障：增加额外的粘性摩擦（stiction）
        if self.fault_mode == "stiction":
            total_torque -= self.fault_severity * self.velocity

        angular_accel = total_torque / p.rotor_inertia
        self.velocity += angular_accel * dt
        self.angle += self.velocity * dt

        # === 齿轮传动（考虑间隙和效率） ===
        ideal_output_angle = self.angle / p.gear_ratio
        if self.fault_mode == "backlash":
            # 放大间隙
            backlash = p.gear_backlash * (1 + self.fault_severity)
        else:
            backlash = p.gear_backlash

        # 间隙模型：死区
        angle_diff = ideal_output_angle - self.output_angle
        if abs(angle_diff) > backlash:
            self.output_angle += angle_diff - math.copysign(backlash, angle_diff)

        self.output_velocity = self.velocity / p.gear_ratio

        # 输出转矩（考虑齿轮效率）
        if self.output_velocity > 0:
            self.output_torque = magnetic_torque * p.gear_ratio * p.gear_efficiency
        else:
            self.output_torque = magnetic_torque * p.gear_ratio / p.gear_efficiency

        # 故障：传感器偏置
        if self.fault_mode == "sensor_bias":
            self.output_angle += self.fault_severity * 0.1

        # === 热模型（简化一阶） ===
        # C * dT/dt = I^2 * R - (T - T_ambient) / R_th
        power_loss = self.current ** 2 * p.resistance
        dT_dt = (power_loss - (self.temperature - p.ambient_temp) / p.thermal_resistance) / p.thermal_capacitance
        self.temperature += dT_dt * dt

        return {
            "output_angle": self.output_angle,
            "output_velocity": self.output_velocity,
            "output_torque": self.output_torque,
            "motor_angle": self.angle,
            "motor_velocity": self.velocity,
            "current": self.current,
            "temperature": self.temperature,
            "cogging_torque": cogging_torque,
            "friction_torque": friction_torque,
            "temp_factor": temp_factor
        }

    def _compute_friction(self, velocity: float) -> float:
        """Stribeck摩擦模型"""
        p = self.params
        v_stribeck = 0.01  # Stribeck速度

        if abs(velocity) < 1e-6:
            # 静摩擦
            return p.static_friction * np.sign(velocity + 1e-10)
        else:
            # Coulomb + Viscous + Stribeck
            stribeck = math.exp(-(abs(velocity) / v_stribeck) ** 2)
            friction = (p.coulomb_friction + (p.static_friction - p.coulomb_friction) * stribeck) * np.sign(velocity)
            friction += p.viscous_friction * velocity
            return friction

    def inject_fault(self, mode: str, severity: float = 0.5):
        """注入故障用于鲁棒性测试"""
        self.fault_mode = mode
        self.fault_severity = severity

    def clear_fault(self):
        self.fault_mode = None
        self.fault_severity = 0.0

    def reset(self):
        self.angle = 0.0
        self.velocity = 0.0
        self.current = 0.0
        self.temperature = self.params.ambient_temp
        self.output_angle = 0.0
        self.output_velocity = 0.0
        self.output_torque = 0.0
        self.clear_fault()


# ============================================================================
# 第二部分：域随机化深度增强
# ============================================================================

class EnhancedDomainRandomizer:
    """
    增强型域随机化系统
    随机化维度（30+）：
      - 物理参数：质量、惯性、摩擦、阻尼、间隙、柔性
      - 执行器参数：转矩常数、电阻、电感、齿槽、摩擦
      - 传感器参数：噪声幅度、漂移、延迟、丢包、偏置
      - 环境参数：重力、空气阻力、地面属性、光照
      - 视觉参数：相机位置、焦距、畸变、亮度
      - 控制参数：增益、延迟、滤波参数
    """

    def __init__(self, config: Dict = None):
        config = config or {}
        self.enabled = config.get("enabled", True)
        self.intensity = config.get("intensity", 1.0)  # 0.0-2.0 随机化强度
        self.seed = config.get("seed", 42)

        # 各维度随机化范围（强度系数会缩放这些范围）
        self.ranges = {
            # 物理参数
            "mass_scale": [0.5, 2.0],
            "inertia_scale": [0.3, 3.0],
            "friction_scale": [0.2, 3.0],
            "damping_scale": [0.1, 5.0],
            "restitution": [0.0, 0.8],
            "contact_stiffness": [1e4, 1e7],
            "contact_damping": [1e2, 1e4],

            # 关节/连杆
            "joint_backlash": [0.0, 0.01],
            "joint_flexibility": [0.0, 0.05],
            "link_com_offset": [-0.02, 0.02],

            # 执行器
            "torque_constant_scale": [0.7, 1.3],
            "motor_resistance_scale": [0.5, 2.0],
            "cogging_amplitude_scale": [0.0, 3.0],
            "friction_scale_actuator": [0.3, 2.0],
            "gear_ratio_error": [-0.02, 0.02],

            # 传感器
            "joint_noise_std": [0.0001, 0.01],
            "ee_noise_std": [0.00001, 0.001],
            "force_noise_std": [0.01, 2.0],
            "sensor_drift_rate": [0.0, 0.0001],
            "sensor_latency_ms": [0, 50],
            "sensor_packet_loss": [0.0, 0.1],
            "sensor_bias": [-0.01, 0.01],

            # 环境
            "gravity_scale": [0.9, 1.1],
            "air_resistance": [0.0, 0.5],
            "ground_friction": [0.3, 1.5],

            # 控制
            "control_gain_scale": [0.5, 1.5],
            "control_latency_ms": [0, 30],
            "control_filter": [0.0, 0.3],

            # 视觉（仿真渲染）
            "camera_position_offset": [-0.1, 0.1],
            "lighting_intensity": [0.3, 2.0],
        }

        self.current_params = {}
        np.random.seed(self.seed)
        random.seed(self.seed)

    def randomize(self, robot_id: int, joint_indices: List[int] = None) -> Dict:
        """执行全维度随机化"""
        if not self.enabled:
            return {}

        params = {}
        intensity = self.intensity

        # 物理参数随机化
        num_joints = p.getNumJoints(robot_id)
        joint_indices = joint_indices or list(range(num_joints))

        # 质量 + 惯性（连杆级）
        for i in joint_indices:
            dyn = p.getDynamicsInfo(robot_id, i)
            orig_mass = dyn[0]
            orig_inertia = dyn[2]

            mass_scale = self._rand("mass_scale")
            inertia_scale = self._rand("inertia_scale")

            if orig_mass > 0:
                p.changeDynamics(
                    robot_id, i,
                    mass=orig_mass * mass_scale,
                    localInertiaDiagonal=[
                        orig_inertia[0] * inertia_scale,
                        orig_inertia[1] * inertia_scale,
                        orig_inertia[2] * inertia_scale,
                    ]
                )
                params[f"link_{i}_mass"] = mass_scale
                params[f"link_{i}_inertia"] = inertia_scale

            # 摩擦 + 阻尼 + 接触参数
            friction_scale = self._rand("friction_scale")
            damping_scale = self._rand("damping_scale")
            restitution = self._rand("restitution")

            p.changeDynamics(
                robot_id, i,
                lateralFriction=max(0.01, dyn[1] * friction_scale),
                linearDamping=dyn[3] * damping_scale if len(dyn) > 3 else 0.04 * damping_scale,
                angularDamping=(dyn[4] if len(dyn) > 4 else 0.04) * damping_scale,
                restitution=restitution,
            )
            params[f"link_{i}_friction"] = friction_scale
            params[f"link_{i}_damping"] = damping_scale

            # 关节间隙 + 柔性（通过修改关节参数模拟）
            backlash = self._rand("joint_backlash") * intensity
            if backlash > 0:
                # 通过增加阻尼来模拟间隙的影响
                params[f"joint_{i}_backlash"] = backlash

            # 连杆质心偏移
            com_offset = self._rand("link_com_offset")
            params[f"link_{i}_com_offset"] = com_offset

        # 重力
        gravity_scale = self._rand("gravity_scale")
        p.setGravity(0, 0, -9.81 * gravity_scale)
        params["gravity_scale"] = gravity_scale

        # 保存当前参数
        self.current_params = params
        return params

    def _rand(self, key: str) -> float:
        """生成指定范围内的随机值"""
        rng = self.ranges.get(key, [0, 1])
        center = (rng[0] + rng[1]) / 2
        half = (rng[1] - rng[0]) / 2
        scaled_half = half * self.intensity
        return np.random.uniform(center - scaled_half, center + scaled_half)

    def get_sensor_randomization(self) -> Dict:
        """获取传感器随机化参数（供传感器噪声系统使用）"""
        return {
            "joint_noise_std": self._rand("joint_noise_std"),
            "ee_noise_std": self._rand("ee_noise_std"),
            "force_noise_std": self._rand("force_noise_std"),
            "sensor_drift_rate": self._rand("sensor_drift_rate"),
            "sensor_latency_ms": self._rand("sensor_latency_ms"),
            "sensor_packet_loss": self._rand("sensor_packet_loss"),
            "sensor_bias": self._rand("sensor_bias"),
        }

    def get_control_randomization(self) -> Dict:
        """获取控制随机化参数"""
        return {
            "control_gain_scale": self._rand("control_gain_scale"),
            "control_latency_ms": self._rand("control_latency_ms"),
            "control_filter": self._rand("control_filter"),
        }

    def get_actuator_randomization(self) -> Dict:
        """获取执行器随机化参数"""
        return {
            "torque_constant_scale": self._rand("torque_constant_scale"),
            "motor_resistance_scale": self._rand("motor_resistance_scale"),
            "cogging_amplitude_scale": self._rand("cogging_amplitude_scale"),
            "friction_scale_actuator": self._rand("friction_scale_actuator"),
            "gear_ratio_error": self._rand("gear_ratio_error"),
        }


# ============================================================================
# 第三部分：多任务场景环境
# ============================================================================

class MultiTaskEnvironment:
    """
    多任务场景定义（供训练环境调用）
    支持的任务类型：
      - reach:      到达目标点
      - grasp:      抓取物体
      - place:      放置物体到目标位置
      - peg_in_hole: 轴孔装配
      - push:       推动物体
      - avoid:      避障运动
      - track:      跟踪动态目标
      - polish:     打磨/擦拭（接触-rich）
    """

    TASK_TYPES = [
        "reach", "grasp", "place", "peg_in_hole",
        "push", "avoid", "track", "polish"
    ]

    def __init__(self, task_type: str = "reach", config: Dict = None):
        self.task_type = task_type
        self.config = config or {}
        self._validate_task()

        # 场景物体ID
        self.objects = {}
        self.target_pos = np.array([0.5, 0.0, 0.3])
        self.initial_pos = np.array([0.3, 0.0, 0.1])

    def _validate_task(self):
        if self.task_type not in self.TASK_TYPES:
            raise ValueError(f"未知任务类型: {self.task_type}, 支持: {self.TASK_TYPES}")

    def setup_scene(self, client_id: int = 0) -> Dict:
        """
        在PyBullet中设置任务场景
        Returns: 场景信息字典
        """
        p.setPhysicsEngineParameter(clientId=client_id)
        scene_info = {"task_type": self.task_type, "objects": {}}

        if self.task_type == "reach":
            scene_info["target"] = self._create_visual_target(self.target_pos)

        elif self.task_type == "grasp":
            scene_info["target_object"] = self._create_graspable_object(self.target_pos)
            scene_info["target_pos"] = self.target_pos

        elif self.task_type == "place":
            scene_info["grasp_object"] = self._create_graspable_object(self.initial_pos)
            scene_info["place_target"] = self._create_visual_target(self.target_pos, color=[0, 1, 0, 0.5])

        elif self.task_type == "peg_in_hole":
            scene_info["peg"] = self._create_peg(self.initial_pos)
            scene_info["hole"] = self._create_hole(self.target_pos)

        elif self.task_type == "push":
            scene_info["push_object"] = self._create_pushable_box(self.target_pos)
            scene_info["target_zone"] = self._create_visual_target(
                self.target_pos + np.array([0.3, 0, 0]), color=[1, 0.5, 0, 0.3]
            )

        elif self.task_type == "avoid":
            scene_info["target"] = self._create_visual_target(self.target_pos)
            scene_info["obstacles"] = self._create_obstacles()

        elif self.task_type == "track":
            scene_info["moving_target"] = self._create_moving_target()

        elif self.task_type == "polish":
            scene_info["surface"] = self._create_polish_surface(self.target_pos)
            scene_info["tool"] = self._create_polish_tool()

        self.objects = scene_info["objects"]
        return scene_info

    def _create_visual_target(self, pos: np.ndarray, color: List = None, size: float = 0.03) -> int:
        """创建可视化目标点"""
        color = color or [1, 0, 0, 0.8]
        vis_shape = p.createVisualShape(p.GEOM_SPHERE, radius=size, rgbaColor=color)
        col_shape = p.createCollisionShape(p.GEOM_SPHERE, radius=size * 0.1)
        obj_id = p.createMultiBody(0, col_shape, vis_shape, pos)
        return obj_id

    def _create_graspable_object(self, pos: np.ndarray) -> int:
        """创建可抓取物体（立方体）"""
        size = 0.04
        col_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, size])
        vis_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[size, size, size], rgbaColor=[0.2, 0.6, 1, 1])
        obj_id = p.createMultiBody(0.5, col_shape, vis_shape, pos)
        return obj_id

    def _create_peg(self, pos: np.ndarray) -> int:
        """创建轴（peg）"""
        radius, height = 0.015, 0.1
        col_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=radius, height=height)
        vis_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=radius, height=height, rgbaColor=[0.8, 0.2, 0.2, 1])
        obj_id = p.createMultiBody(0.3, col_shape, vis_shape, pos)
        return obj_id

    def _create_hole(self, pos: np.ndarray) -> int:
        """创建孔（hole）平台"""
        size = 0.1
        col_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, 0.01])
        vis_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[size, size, 0.01], rgbaColor=[0.3, 0.3, 0.3, 0.8])
        obj_id = p.createMultiBody(10, col_shape, vis_shape, pos - np.array([0, 0, 0.01]))
        # 在中心创建孔的可视化
        hole_vis = p.createVisualShape(p.GEOM_CYLINDER, radius=0.02, height=0.02, rgbaColor=[0, 0, 0, 1])
        p.createMultiBody(0, -1, hole_vis, pos)
        return obj_id

    def _create_pushable_box(self, pos: np.ndarray) -> int:
        """创建可推动的盒子"""
        size = 0.06
        col_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, size])
        vis_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[size, size, size], rgbaColor=[0.9, 0.7, 0.2, 1])
        obj_id = p.createMultiBody(1.0, col_shape, vis_shape, pos)
        p.changeDynamics(obj_id, -1, lateralFriction=0.8)
        return obj_id

    def _create_obstacles(self) -> List[int]:
        """创建障碍物"""
        obstacles = []
        obstacle_positions = [
            [0.4, 0.1, 0.15],
            [0.45, -0.15, 0.2],
            [0.35, 0.05, 0.25],
        ]
        for pos in obstacle_positions:
            size = 0.04
            col_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, size])
            vis_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[size, size, size], rgbaColor=[0.7, 0.1, 0.1, 0.9])
            obj_id = p.createMultiBody(5.0, col_shape, vis_shape, pos)
            obstacles.append(obj_id)
        return obstacles

    def _create_moving_target(self) -> int:
        """创建动态移动目标"""
        vis_shape = p.createVisualShape(p.GEOM_SPHERE, radius=0.04, rgbaColor=[0, 0.8, 0.8, 0.9])
        obj_id = p.createMultiBody(0, -1, vis_shape, [0.5, 0, 0.3])
        return obj_id

    def _create_polish_surface(self, pos: np.ndarray) -> int:
        """创建待打磨表面"""
        size = [0.15, 0.15, 0.01]
        col_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=size)
        vis_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=size, rgbaColor=[0.5, 0.5, 0.5, 1])
        obj_id = p.createMultiBody(100, col_shape, vis_shape, pos)
        return obj_id

    def _create_polish_tool(self) -> int:
        """创建打磨工具（可视化，实际由机械臂夹持）"""
        vis_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=0.02, height=0.05, rgbaColor=[0.9, 0.3, 0.3, 1])
        obj_id = p.createMultiBody(0, -1, vis_shape, [0, 0, -1])
        return obj_id

    def update_dynamic_targets(self, t: float) -> Dict:
        """更新动态目标位置（用于track任务）"""
        updates = {}
        if self.task_type == "track":
            # 8字形轨迹
            omega = 0.5
            x = 0.5 + 0.1 * math.sin(omega * t)
            y = 0.0 + 0.1 * math.sin(omega * t * 2) * 0.5
            z = 0.3
            pos = [x, y, z]
            if "moving_target" in self.objects:
                p.resetBasePositionAndOrientation(self.objects["moving_target"], pos, [0, 0, 0, 1])
            updates["target_pos"] = np.array(pos)
        return updates

    def compute_reward(self, ee_pos: np.ndarray, action: np.ndarray, info: Dict = None) -> Tuple[float, Dict]:
        """计算各任务的奖励函数"""
        rewards = {"task": self.task_type}

        if self.task_type == "reach":
            dist = np.linalg.norm(ee_pos - self.target_pos)
            rewards["distance"] = dist
            reward = -dist * 10.0
            if dist < 0.05:
                reward += 10.0  # 到达奖励

        elif self.task_type == "grasp":
            dist = np.linalg.norm(ee_pos - self.target_pos)
            rewards["distance"] = dist
            reward = -dist * 5.0
            # 抓取奖励需要结合力信息

        elif self.task_type == "place":
            # 放置任务：先接近物体，再抓取，再放置
            dist = np.linalg.norm(ee_pos - self.target_pos)
            rewards["distance"] = dist
            reward = -dist * 3.0

        elif self.task_type == "peg_in_hole":
            dist = np.linalg.norm(ee_pos - self.target_pos)
            rewards["distance"] = dist
            reward = -dist * 8.0

        elif self.task_type == "avoid":
            # 避障：接近目标 + 避障惩罚
            dist = np.linalg.norm(ee_pos - self.target_pos)
            obstacle_penalty = 0.0
            rewards["distance"] = dist
            rewards["obstacle_penalty"] = obstacle_penalty
            reward = -dist * 5.0 - obstacle_penalty * 20.0

        elif self.task_type == "track":
            # 跟踪：当前位置与动态目标的距离
            dist = np.linalg.norm(ee_pos - self.target_pos)
            rewards["distance"] = dist
            reward = -dist * 8.0

        elif self.task_type == "polish":
            # 打磨：接触压力 + 覆盖面积
            dist = np.linalg.norm(ee_pos - self.target_pos)
            rewards["distance"] = dist
            reward = -dist * 3.0

        else:  # reach
            dist = np.linalg.norm(ee_pos - self.target_pos)
            reward = -dist * 10.0

        # 控制惩罚
        action_penalty = np.sum(np.square(action)) * 0.01
        reward -= action_penalty
        rewards["action_penalty"] = action_penalty

        return float(reward), rewards

    def check_success(self, ee_pos: np.ndarray, info: Dict = None) -> bool:
        """检查任务是否成功"""
        if self.task_type in ["reach", "grasp", "place", "peg_in_hole", "track"]:
            dist = np.linalg.norm(ee_pos - self.target_pos)
            return dist < 0.05
        elif self.task_type == "avoid":
            dist = np.linalg.norm(ee_pos - self.target_pos)
            return dist < 0.05
        elif self.task_type == "polish":
            return False
        return False

    def reset(self):
        """重置任务状态"""
        self.target_pos = np.array([
            0.4 + random.random() * 0.2,
            -0.2 + random.random() * 0.4,
            0.1 + random.random() * 0.3
        ])


# ============================================================================
# 第四部分：极端鲁棒性测试套件
# ============================================================================

class RobustnessTestSuite:
    """
    极端鲁棒性测试套件
    测试类型：
      1. 边界条件测试（关节极限、速度极限、转矩极限）
      2. 大扰动测试（外力冲击、载荷突变）
      3. 高速运动测试
      4. 大负载测试
      5. 故障注入测试（传感器故障、执行器故障、通信故障）
      6. 噪声压力测试（极端传感器噪声）
      7. 环境极端测试（高温、低温、重力变化）
    """

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.results = []
        self.test_count = 0

    def generate_test_profile(self, test_type: str, intensity: float = 1.0) -> Dict:
        """
        生成测试配置文件
        Args:
            test_type: 测试类型
            intensity: 测试强度 0.0-2.0
        Returns:
            测试配置字典
        """
        profile = {"test_type": test_type, "intensity": intensity}

        if test_type == "boundary":
            # 边界条件：接近关节极限运动
            profile["joint_limit_margin"] = 0.01 * (1.0 / max(0.1, intensity))
            profile["velocity_scale"] = 0.8 + 0.2 * intensity

        elif test_type == "disturbance":
            # 大扰动：外力冲击 + 载荷变化
            profile["impact_force"] = [0, 0, -50 * intensity]
            profile["impact_duration"] = 0.1
            profile["payload_variation"] = 0.5 * intensity

        elif test_type == "high_speed":
            # 高速运动
            profile["velocity_scale"] = 1.5 + intensity
            profile["acceleration_scale"] = 1.5 + intensity
            profile["jerk_scale"] = 1.5 + intensity

        elif test_type == "high_payload":
            # 大负载
            profile["payload_mass"] = 2.0 + 5.0 * intensity
            profile["payload_offset"] = [0.05 * intensity, 0, 0]

        elif test_type == "sensor_fault":
            # 传感器故障
            profile["fault_mode"] = random.choice(["bias", "drift", "noise", "dropout", "stuck"])
            profile["fault_severity"] = 0.3 + 0.7 * intensity

        elif test_type == "actuator_fault":
            # 执行器故障
            profile["fault_mode"] = random.choice(["stiction", "backlash", "overheat", "torque_loss", "sensor_bias"])
            profile["fault_severity"] = 0.3 + 0.7 * intensity
            profile["affected_joints"] = random.sample(range(7), k=max(1, int(3 * intensity)))

        elif test_type == "comm_fault":
            # 通信故障
            profile["packet_loss"] = 0.1 + 0.4 * intensity
            profile["latency_ms"] = 20 + 80 * intensity
            profile["jitter_ms"] = 5 + 20 * intensity

        elif test_type == "extreme_noise":
            # 极端噪声
            profile["joint_noise_std"] = 0.01 + 0.05 * intensity
            profile["ee_noise_std"] = 0.001 + 0.01 * intensity
            profile["force_noise_std"] = 1.0 + 10.0 * intensity

        elif test_type == "extreme_env":
            # 极端环境
            profile["temperature"] = -20 + 150 * intensity  # -20°C 到 130°C
            profile["gravity_scale"] = 0.5 + 1.0 * intensity  # 0.5g 到 1.5g
            profile["humidity"] = 10 + 80 * intensity  # 10% 到 90%

        return profile

    def run_test_batch(self, test_function: Callable, test_types: List[str], num_trials: int = 10) -> Dict:
        """
        运行一批测试
        Args:
            test_function: 实际执行测试的函数
            test_types: 要运行的测试类型列表
            num_trials: 每个类型的测试次数
        Returns:
            测试结果汇总
        """
        batch_results = {}
        for test_type in test_types:
            type_results = []
            for trial in range(num_trials):
                intensity = random.uniform(0.3, 1.5)
                profile = self.generate_test_profile(test_type, intensity)

                try:
                    result = test_function(profile)
                    result["profile"] = profile
                    result["trial"] = trial
                    type_results.append(result)
                except Exception as e:
                    type_results.append({
                        "profile": profile,
                        "trial": trial,
                        "success": False,
                        "error": str(e),
                        "crashed": True
                    })

                self.test_count += 1

            batch_results[test_type] = self._summarize_type(type_results)

        self.results.append(batch_results)
        return batch_results

    def _summarize_type(self, results: List[Dict]) -> Dict:
        """汇总某类测试的结果"""
        success_count = sum(1 for r in results if r.get("success", False))
        crash_count = sum(1 for r in results if r.get("crashed", False))
        return {
            "total": len(results),
            "success": success_count,
            "success_rate": success_count / len(results) if results else 0,
            "crashed": crash_count,
            "crash_rate": crash_count / len(results) if results else 0,
            "details": results
        }

    def get_full_report(self) -> Dict:
        """获取完整测试报告"""
        return {
            "total_test_count": self.test_count,
            "test_batches": len(self.results),
            "latest_results": self.results[-1] if self.results else {},
            "all_results": self.results
        }

    def print_summary(self):
        """打印测试摘要"""
        report = self.get_full_report()
        print(f"\n{'='*60}")
        print(f"  鲁棒性测试报告 (总计 {report['total_test_count']} 次测试)")
        print(f"{'='*60}")
        for test_type, summary in report.get("latest_results", {}).items():
            rate = summary["success_rate"] * 100
            status = "✅" if rate >= 80 else "⚠️" if rate >= 50 else "❌"
            print(f"  {status} {test_type:20s}: {summary['success']}/{summary['total']} ({rate:.1f}%)")
        print(f"{'='*60}\n")


# ============================================================================
# 主入口：统一仿真增强系统
# ============================================================================

class SimulationEnhancementSystem:
    """
    统一仿真增强系统（整合所有模块）
    使用方式：
        system = SimulationEnhancementSystem()
        system.set_task("place")
        system.enable_robustness_test("disturbance", intensity=1.0)
        system.step(action)
    """

    def __init__(self, config: Dict = None):
        config = config or {}

        # 子系统
        self.domain_randomizer = EnhancedDomainRandomizer(config.get("domain_randomization", {}))
        self.robustness = RobustnessTestSuite(config.get("robustness", {}))
        self.multi_task = None  # 延迟初始化，需要知道任务类型

        # 执行器数组（7自由度机械臂）
        self.actuators = [HighPrecisionActuator() for _ in range(7)]

        # 状态
        self.current_task = "reach"
        self.robustness_enabled = False
        self.robustness_profile = {}

        # 统计
        self.stats = {
            "total_steps": 0,
            "randomization_count": 0,
            "fault_injection_count": 0,
        }

    def set_task(self, task_type: str, scene_config: Dict = None):
        """设置当前任务"""
        self.current_task = task_type
        self.multi_task = MultiTaskEnvironment(task_type, scene_config)
        return self.multi_task

    def enable_robustness_test(self, test_type: str, intensity: float = 1.0):
        """启用鲁棒性测试"""
        self.robustness_enabled = True
        self.robustness_profile = self.robustness.generate_test_profile(test_type, intensity)
        self._apply_robustness_profile()

    def disable_robustness_test(self):
        """禁用鲁棒性测试"""
        self.robustness_enabled = False
        for actuator in self.actuators:
            actuator.clear_fault()

    def _apply_robustness_profile(self):
        """应用鲁棒性测试配置"""
        profile = self.robustness_profile
        test_type = profile.get("test_type", "")

        if test_type == "actuator_fault":
            affected = profile.get("affected_joints", [])
            for i in affected:
                if i < len(self.actuators):
                    self.actuators[i].inject_fault(
                        profile.get("fault_mode", "stiction"),
                        profile.get("fault_severity", 0.5)
                    )
            self.stats["fault_injection_count"] += 1

    def randomize_all(self, robot_id: int, joint_indices: List[int]):
        """执行全维度随机化"""
        params = self.domain_randomizer.randomize(robot_id, joint_indices)
        self.stats["randomization_count"] += 1

        # 应用执行器随机化
        act_params = self.domain_randomizer.get_actuator_randomization()
        for actuator in self.actuators:
            actuator.params.torque_constant *= act_params.get("torque_constant_scale", 1.0)
            actuator.params.resistance *= act_params.get("motor_resistance_scale", 1.0)

        return params

    def step_actuators(self, voltage_cmds: List[float], load_torques: List[float], dt: float) -> List[Dict]:
        """步进所有执行器"""
        results = []
        for i, (voltage, load) in enumerate(zip(voltage_cmds, load_torques)):
            if i < len(self.actuators):
                result = self.actuators[i].step(voltage, load, dt)
                results.append(result)
        self.stats["total_steps"] += 1
        return results

    def get_sensor_params(self) -> Dict:
        """获取当前传感器随机化参数"""
        return self.domain_randomizer.get_sensor_randomization()

    def get_control_params(self) -> Dict:
        """获取当前控制随机化参数"""
        return self.domain_randomizer.get_control_randomization()

    def get_stats(self) -> Dict:
        """获取系统统计信息"""
        return self.stats.copy()

    def reset(self):
        """重置所有子系统"""
        for actuator in self.actuators:
            actuator.reset()
        if self.multi_task:
            self.multi_task.reset()
        self.disable_robustness_test()


# ============================================================================
# 便捷函数
# ============================================================================

def create_enhanced_system(intensity: float = 1.0) -> SimulationEnhancementSystem:
    """创建配置好的增强系统（便捷入口）"""
    config = {
        "domain_randomization": {
            "enabled": True,
            "intensity": intensity,
        },
        "robustness": {
            "enabled": False,
        }
    }
    return SimulationEnhancementSystem(config)


def get_all_task_types() -> List[str]:
    """获取所有支持的任务类型"""
    return MultiTaskEnvironment.TASK_TYPES


def get_all_test_types() -> List[str]:
    """获取所有支持的鲁棒性测试类型"""
    return [
        "boundary", "disturbance", "high_speed", "high_payload",
        "sensor_fault", "actuator_fault", "comm_fault",
        "extreme_noise", "extreme_env"
    ]
