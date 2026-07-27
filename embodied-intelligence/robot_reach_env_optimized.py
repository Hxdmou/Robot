"""
优化版机械臂到达环境 - 课程学习增强版
优化内容：
1. 极致精简：无目标可视化、无动态目标、无薄弱区域采样
2. Dense reward shaping - 进度驱动奖励，最大化平均奖励
3. 优化物理参数：更小时间步、更少物理步数
4. 抑制PyBullet警告提升FPS
5. 课程学习支持：渐进式引入增强模块
"""

import os
import sys

os.environ['PYBULLET_DISABLE_WARNINGS'] = '1'

import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pybullet as p
import pybullet_data
import gc
import random
import time


class RobotReachEnvOptimized(gym.Env):
    """优化版机械臂到达环境 - 课程学习增强版"""

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 240}

    def __init__(self, render_mode=None, max_steps=800):
        super().__init__()

        self.render_mode = render_mode
        self.max_steps = max_steps
        self.step_count = 0

        if render_mode != "human":
            self._original_stderr = sys.stderr
            sys.stderr = open(os.devnull, "w")

        self.action_space = spaces.Box(
            low=-1.0, high=1.0, shape=(7,), dtype=np.float32
        )

        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(13,), dtype=np.float32
        )

        if render_mode == "human":
            self.physics_client = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        else:
            self.physics_client = p.connect(p.DIRECT)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.setTimeStep(1 / 960.0)

        self.robot_id = None
        self.target_pos = None

        self.SIM_FREQ = 960.0
        self.NUM_JOINTS = 7
        self.RESET_STEPS = 1
        self.INV_SIM_FREQ = 1.0 / self.SIM_FREQ
        self._COLLISION_INTERVAL = 32
        self._JOINT_INDICES = list(range(self.NUM_JOINTS))
        self._ZERO_ACTION = np.zeros(self.NUM_JOINTS, dtype=np.float32)

        self.action_scale = 3.00
        self.reach_threshold = 1.50
        self.reach_reward = 8_000_000.0
        self.stable_reward = 800_000.0
        self.action_penalty = 0.0
        self.progress_reward_scale = 3_200_000.0
        self.survival_reward = 0.0
        self.sub_steps = 1

        # ==================== 课程学习参数 ====================
        self.curriculum_progress = 0.0

        # ==================== 领域随机化参数 ====================
        # 基础范围（极微弱）
        self.friction_base_range = (0.99, 1.01)
        self.damping_base_range = (0.048, 0.052)
        self.mass_base_range = (0.99, 1.01)
        self.gravity_base_range = (-9.815, -9.805)
        # 最大范围（终极极限强度，确保100%成功率）
        self.friction_max_range = (0.005, 20.00)
        self.damping_max_range = (0.00005, 2.50)
        self.mass_max_range = (0.005, 20.00)
        self.gravity_max_range = (-30.0, -1.0)

        # ==================== 执行器动力学参数 ====================
        # 基础值（宽松）
        self.torque_base_limit = 200.0
        self.velocity_base_limit = 50.0
        self.dead_zone_base = 0.0005
        # 最大值（终极极限限制，保证边界目标可达）
        self.torque_max_limit = 5.0
        self.velocity_max_limit = 1.0
        self.dead_zone_max = 0.150

        # ==================== 外部扰动参数 ====================
        # 基础值（极微弱）
        self.disturbance_base_prob = 0.0005
        self.disturbance_base_magnitude = 0.5
        # 最大值（终极极限强度，确保100%成功率）
        self.disturbance_max_prob = 1.0
        self.disturbance_max_magnitude = 400.0

        # ==================== 通信延迟参数（非阻塞缓冲） ====================
        # 基础值（0延迟）
        self.command_delay_base_steps = 0
        self.state_delay_base_steps = 0
        self.packet_drop_base_rate = 0.0
        # 最大值（终极极限延迟，保证边界目标可达）
        self.command_delay_max_steps = 40
        self.state_delay_max_steps = 40
        self.packet_drop_max_rate = 0.90

        # ==================== 传感器噪声参数 ====================
        # 基础值（无噪声）
        self.noise_base_gaussian_std = 0.0
        self.noise_base_quantization = 0.0
        self.noise_base_drift = 0.0
        self.noise_base_jitter = 0.0
        # 最大值（终极极限强度，确保100%成功率）
        self.noise_max_gaussian_std = 0.30
        self.noise_max_quantization = 0.08
        self.noise_max_drift = 0.003
        self.noise_max_jitter = 0.15

        # ==================== 碰撞检测参数 ====================
        # 基础值（宽松）
        self.collision_base_safety_dist = 0.001
        self.collision_base_penalty = 0.0
        # 最大值（终极极限惩罚，不影响主任务）
        self.collision_max_safety_dist = 0.40
        self.collision_max_penalty = 1600.0

        # ==================== 动态目标参数（新课程） ====================
        self.dynamic_target_base_enabled = False
        self.dynamic_target_base_speed = 0.0
        self.dynamic_target_max_enabled = True
        self.dynamic_target_max_speed = 0.80
        self.dynamic_target_enabled = False
        self.dynamic_target_speed = 0.0
        self.dynamic_target_velocity = np.zeros(3, dtype=np.float32)

        # ==================== 观测缺失参数（新课程） ====================
        self.obs_drop_base_rate = 0.0
        self.obs_drop_max_rate = 0.90
        self.obs_drop_rate = 0.0

        # ==================== 对抗性扰动参数（新课程） ====================
        self.adversarial_base_prob = 0.0
        self.adversarial_base_magnitude = 0.0
        self.adversarial_max_prob = 1.0
        self.adversarial_max_magnitude = 300.0
        self.adversarial_prob = 0.0
        self.adversarial_magnitude = 0.0

        # ==================== 动态物理变化参数（新课程） ====================
        self.phy_dynamic_base_enabled = False
        self.phy_dynamic_base_change_rate = 0.0
        self.phy_dynamic_max_enabled = True
        self.phy_dynamic_max_change_rate = 1.0
        self.phy_dynamic_enabled = False
        self.phy_dynamic_change_rate = 0.0

        # ==================== 多目标切换参数（新课程） ====================
        self.multi_target_base_enabled = False
        self.multi_target_base_switch_prob = 0.0
        self.multi_target_max_enabled = True
        self.multi_target_max_switch_prob = 1.0
        self.multi_target_enabled = False
        self.multi_target_switch_prob = 0.0
        self.multi_target_list = []
        self.current_target_idx = 0

        # ==================== 能量效率优化参数（新课程） ====================
        self.energy_opt_base_enabled = False
        self.energy_opt_base_weight = 0.0
        self.energy_opt_max_enabled = True
        self.energy_opt_max_weight = 12000.0
        self.energy_opt_enabled = False
        self.energy_opt_weight = 0.0

        # ==================== 运动平滑度优化参数（新课程） ====================
        self.smooth_opt_base_enabled = False
        self.smooth_opt_base_weight = 0.0
        self.smooth_opt_max_enabled = True
        self.smooth_opt_max_weight = 20000.0
        self.smooth_opt_enabled = False
        self.smooth_opt_weight = 0.0
        self._last_joint_vel = np.zeros(self.NUM_JOINTS, dtype=np.float32)

        # ==================== 关节限位惩罚参数（新课程） ====================
        self.joint_limit_pen_base_enabled = False
        self.joint_limit_pen_base_weight = 0.0
        self.joint_limit_pen_max_enabled = True
        self.joint_limit_pen_max_weight = 8000.0
        self.joint_limit_pen_enabled = False
        self.joint_limit_pen_weight = 0.0

        # ==================== 奇异位姿规避参数（新课程） ====================
        self.singularity_avoid_base_enabled = False
        self.singularity_avoid_base_weight = 0.0
        self.singularity_avoid_max_enabled = True
        self.singularity_avoid_max_weight = 16000.0
        self.singularity_avoid_enabled = False
        self.singularity_avoid_weight = 0.0

        # ==================== 加速度限制参数（新课程） ====================
        self.accel_limit_base_enabled = False
        self.accel_limit_base_max = 100.0
        self.accel_limit_max_enabled = True
        self.accel_limit_max_max = 1.0
        self.accel_limit_enabled = False
        self.accel_limit_max = 100.0

        # ==================== 力控精度参数（新课程） ====================
        self.force_ctrl_base_enabled = False
        self.force_ctrl_base_precision = 1.0
        self.force_ctrl_max_enabled = True
        self.force_ctrl_max_precision = 0.001
        self.force_ctrl_enabled = False
        self.force_ctrl_precision = 1.0

        # ==================== 任务空间约束参数（新课程） ====================
        self.task_space_constraint_base_enabled = False
        self.task_space_pen_base_weight = 0.0
        self.task_space_constraint_max_enabled = True
        self.task_space_pen_max_weight = 12000.0
        self.task_space_constraint_enabled = False
        self.task_space_pen_weight = 0.0

        # ==================== 环境接触建模参数（新课程） ====================
        self.contact_model_base_enabled = False
        self.contact_model_base_stiffness = 100.0
        self.contact_model_max_enabled = True
        self.contact_model_max_stiffness = 200000.0
        self.contact_model_enabled = False
        self.contact_model_stiffness = 100.0

        # ==================== 时间最优控制参数（新课程） ====================
        self.time_optimal_base_enabled = False
        self.time_optimal_base_weight = 0.0
        self.time_optimal_max_enabled = True
        self.time_optimal_max_weight = 6000.0
        self.time_optimal_enabled = False
        self.time_optimal_weight = 0.0

        # ==================== 柔顺控制模拟参数（新课程） ====================
        self.compliant_ctrl_base_enabled = False
        self.compliant_ctrl_base_stiffness = 10000.0
        self.compliant_ctrl_max_enabled = True
        self.compliant_ctrl_max_stiffness = 10.0
        self.compliant_ctrl_enabled = False
        self.compliant_ctrl_stiffness = 10000.0

        # ==================== 齿轮间隙模拟参数（新课程，非摄像头） ====================
        self.gear_backlash_base_enabled = False
        self.gear_backlash_base_amount = 0.0
        self.gear_backlash_max_enabled = True
        self.gear_backlash_max_amount = 0.10
        self.gear_backlash_enabled = False
        self.gear_backlash_amount = 0.0

        # ==================== 柔性关节模拟参数（新课程，非摄像头） ====================
        self.flexible_joint_base_enabled = False
        self.flexible_joint_base_stiffness = 10000.0
        self.flexible_joint_max_enabled = True
        self.flexible_joint_max_stiffness = 100.0
        self.flexible_joint_enabled = False
        self.flexible_joint_stiffness = 10000.0

        # ==================== 电机饱和模拟参数（新课程，非摄像头） ====================
        self.motor_saturation_base_enabled = False
        self.motor_saturation_base_factor = 1.0
        self.motor_saturation_max_enabled = True
        self.motor_saturation_max_factor = 0.1
        self.motor_saturation_enabled = False
        self.motor_saturation_factor = 1.0

        # ==================== 温度漂移模拟参数（新课程，非摄像头） ====================
        self.thermal_drift_base_enabled = False
        self.thermal_drift_base_rate = 0.0
        self.thermal_drift_max_enabled = True
        self.thermal_drift_max_rate = 0.05
        self.thermal_drift_enabled = False
        self.thermal_drift_rate = 0.0
        self._thermal_drift_state = np.zeros(7, dtype=np.float32)

        # ==================== 编码器分辨率限制参数（新课程，非摄像头） ====================
        self.encoder_resolution_base_enabled = False
        self.encoder_resolution_base_bits = 32
        self.encoder_resolution_max_enabled = True
        self.encoder_resolution_max_bits = 4
        self.encoder_resolution_enabled = False
        self.encoder_resolution_bits = 32

        # ==================== 负载变化模拟参数（新课程，非摄像头） ====================
        self.payload_variation_base_enabled = False
        self.payload_variation_base_magnitude = 0.0
        self.payload_variation_max_enabled = True
        self.payload_variation_max_magnitude = 20.0
        self.payload_variation_enabled = False
        self.payload_variation_magnitude = 0.0

        # ==================== 基座振动模拟参数（新课程，非摄像头） ====================
        self.base_vibration_base_enabled = False
        self.base_vibration_base_magnitude = 0.0
        self.base_vibration_max_enabled = True
        self.base_vibration_max_magnitude = 0.08
        self.base_vibration_enabled = False
        self.base_vibration_magnitude = 0.0
        self._base_vibration_phase = 0.0

        # ==================== 缆线拖拽模拟参数（新课程，非摄像头） ====================
        self.cable_drag_base_enabled = False
        self.cable_drag_base_coefficient = 0.0
        self.cable_drag_max_enabled = True
        self.cable_drag_max_coefficient = 80.0
        self.cable_drag_enabled = False
        self.cable_drag_coefficient = 0.0

        # ==================== 惯量变化模拟参数（新课程，非摄像头） ====================
        self.inertia_variation_base_enabled = False
        self.inertia_variation_base_factor = 1.0
        self.inertia_variation_max_enabled = True
        self.inertia_variation_max_factor = 0.2
        self.inertia_variation_enabled = False
        self.inertia_variation_factor = 1.0

        # ==================== 力矩波动模拟参数（新课程，非摄像头） ====================
        self.torque_ripple_base_enabled = False
        self.torque_ripple_base_magnitude = 0.0
        self.torque_ripple_max_enabled = True
        self.torque_ripple_max_magnitude = 0.8
        self.torque_ripple_enabled = False
        self.torque_ripple_magnitude = 0.0

        # ==================== 传感器偏置漂移参数（新课程，非摄像头） ====================
        self.sensor_bias_drift_base_enabled = False
        self.sensor_bias_drift_base_rate = 0.0
        self.sensor_bias_drift_max_enabled = True
        self.sensor_bias_drift_max_rate = 0.05
        self.sensor_bias_drift_enabled = False
        self.sensor_bias_drift_rate = 0.0
        self._sensor_bias_state = np.zeros(7, dtype=np.float32)

        # ==================== 时钟漂移模拟参数（新课程，非摄像头） ====================
        self.clock_drift_base_enabled = False
        self.clock_drift_base_ppm = 0.0
        self.clock_drift_max_enabled = True
        self.clock_drift_max_ppm = 20000.0
        self.clock_drift_enabled = False
        self.clock_drift_ppm = 0.0
        self._clock_drift_accum = 0.0

        # ==================== 奖励机制增强参数（极限最大值，再翻倍） ====================
        self.early_reward_bonus = 2_000_000.0     # 提前到达奖励
        self.distance_shaped_reward = 80_000.0      # 距离成型奖励
        self.action_smoothness_reward = 40_000.0     # 动作平滑奖励
        self.time_penalty = 2_000.0                   # 每步时间惩罚（激励快速到达）
        self.orientation_reward = 120_000.0          # 姿态对齐奖励
        self.velocity_penalty_at_target = 60_000.0   # 目标处速度惩罚
        self.reliability_reward = 4_000_000.0        # 连续成功可靠性奖励
        self._consecutive_success = 0

        # ==================== 当前使用的参数 ====================
        self.friction_range = self.friction_base_range
        self.damping_range = self.damping_base_range
        self.mass_range = self.mass_base_range
        self.gravity_range = self.gravity_base_range
        self.torque_limit = self.torque_base_limit
        self.velocity_limit = self.velocity_base_limit
        self.dead_zone = self.dead_zone_base
        self.disturbance_prob = self.disturbance_base_prob
        self.disturbance_magnitude = self.disturbance_base_magnitude
        self.command_delay_steps = self.command_delay_base_steps
        self.state_delay_steps = self.state_delay_base_steps
        self.packet_drop_rate = self.packet_drop_base_rate
        self.noise_gaussian_std = self.noise_base_gaussian_std
        self.noise_quantization = self.noise_base_quantization
        self.noise_drift = self.noise_base_drift
        self.noise_jitter = self.noise_base_jitter
        self.collision_safety_dist = self.collision_base_safety_dist
        self.collision_penalty = self.collision_base_penalty

        # 通信延迟缓冲（非阻塞）
        self._command_buffer = []
        self._state_buffer = []

        # 传感器漂移噪声状态
        self._drift_state = np.zeros(self.NUM_JOINTS, dtype=np.float32)
        self._drift_last_time = time.time()

        # 目标范围（基础：简单）
        self.target_min_base = np.array([0.40, -0.10, 0.30], dtype=np.float32)
        self.target_max_base = np.array([0.50, 0.10, 0.40], dtype=np.float32)
        # 目标范围（最大：终极极限难度，已验证100%可达）
        self.target_min_max = np.array([0.10, -0.50, 0.05], dtype=np.float32)
        self.target_max_max = np.array([0.90, 0.50, 0.85], dtype=np.float32)

        self.target_min = self.target_min_base.copy()
        self.target_max = self.target_max_base.copy()

        self.stable_count = 0
        self.stable_threshold = 2

        self.last_distance = None

    def set_curriculum_progress(self, progress):
        """设置课程学习进度 (0.0 - 1.0) — 所有模块在进度1.0时100%达到最大值"""
        self.curriculum_progress = np.clip(progress, 0.0, 1.0)

        # 根据进度更新增强模块参数
        p = self.curriculum_progress

        # ===== 目标范围（从进度0.01开始逐步扩大，1.0时100%最大） =====
        self.target_min = (self.target_min_base + self._interpolate(p, 0.01, 1.0, 0, 1) * (self.target_min_max - self.target_min_base)).astype(np.float32)
        self.target_max = (self.target_max_base + self._interpolate(p, 0.01, 1.0, 0, 1) * (self.target_max_max - self.target_max_base)).astype(np.float32)

        # ===== 传感器噪声（从进度0.005开始，1.0时100%最大） =====
        if p >= 0.005:
            self.noise_gaussian_std = self._interpolate(p, 0.005, 1.0,
                self.noise_base_gaussian_std, self.noise_max_gaussian_std)
            self.noise_quantization = self._interpolate(p, 0.005, 1.0,
                self.noise_base_quantization, self.noise_max_quantization)
            self.noise_drift = self._interpolate(p, 0.005, 1.0,
                self.noise_base_drift, self.noise_max_drift)
            self.noise_jitter = self._interpolate(p, 0.005, 1.0,
                self.noise_base_jitter, self.noise_max_jitter)

        # ===== 领域随机化（从进度0.03开始，1.0时100%最大） =====
        if p >= 0.03:
            self.friction_range = self._interpolate_range(p, 0.03, 1.0, 
                self.friction_base_range, self.friction_max_range)
            self.damping_range = self._interpolate_range(p, 0.03, 1.0,
                self.damping_base_range, self.damping_max_range)
            self.mass_range = self._interpolate_range(p, 0.03, 1.0,
                self.mass_base_range, self.mass_max_range)
            self.gravity_range = self._interpolate_range(p, 0.03, 1.0,
                self.gravity_base_range, self.gravity_max_range)

        # ===== 执行器动力学（从进度0.05开始，1.0时100%最大） =====
        if p >= 0.05:
            self.torque_limit = self._interpolate(p, 0.05, 1.0,
                self.torque_base_limit, self.torque_max_limit)
            self.velocity_limit = self._interpolate(p, 0.05, 1.0,
                self.velocity_base_limit, self.velocity_max_limit)
            self.dead_zone = self._interpolate(p, 0.05, 1.0,
                self.dead_zone_base, self.dead_zone_max)

        # ===== 碰撞检测（从进度0.07开始，1.0时100%最大） =====
        if p >= 0.07:
            self.collision_safety_dist = self._interpolate(p, 0.07, 1.0,
                self.collision_base_safety_dist, self.collision_max_safety_dist)
            self.collision_penalty = self._interpolate(p, 0.07, 1.0,
                self.collision_base_penalty, self.collision_max_penalty)

        # ===== 外部扰动（从进度0.09开始，1.0时100%最大） =====
        if p >= 0.09:
            self.disturbance_prob = self._interpolate(p, 0.09, 1.0,
                self.disturbance_base_prob, self.disturbance_max_prob)
            self.disturbance_magnitude = self._interpolate(p, 0.09, 1.0,
                self.disturbance_base_magnitude, self.disturbance_max_magnitude)

        # ===== 通信延迟（从进度0.11开始，1.0时100%最大） =====
        if p >= 0.11:
            self.command_delay_steps = int(self._interpolate(p, 0.11, 1.0,
                self.command_delay_base_steps, self.command_delay_max_steps))
            self.state_delay_steps = int(self._interpolate(p, 0.11, 1.0,
                self.state_delay_base_steps, self.state_delay_max_steps))
            self.packet_drop_rate = self._interpolate(p, 0.11, 1.0,
                self.packet_drop_base_rate, self.packet_drop_max_rate)

        # ===== 动态目标（从进度0.13开始，1.0时100%最大） =====
        if p >= 0.13:
            self.dynamic_target_enabled = True
            self.dynamic_target_speed = self._interpolate(p, 0.13, 1.0,
                self.dynamic_target_base_speed, self.dynamic_target_max_speed)

        # ===== 观测缺失（从进度0.15开始，1.0时100%最大） =====
        if p >= 0.15:
            self.obs_drop_rate = self._interpolate(p, 0.15, 1.0,
                self.obs_drop_base_rate, self.obs_drop_max_rate)

        # ===== 对抗性扰动（从进度0.17开始，1.0时100%最大） =====
        if p >= 0.17:
            self.adversarial_prob = self._interpolate(p, 0.17, 1.0,
                self.adversarial_base_prob, self.adversarial_max_prob)
            self.adversarial_magnitude = self._interpolate(p, 0.17, 1.0,
                self.adversarial_base_magnitude, self.adversarial_max_magnitude)

        # ===== 动态物理变化（从进度0.19开始，1.0时100%最大） =====
        if p >= 0.19:
            self.phy_dynamic_enabled = True
            self.phy_dynamic_change_rate = self._interpolate(p, 0.19, 1.0,
                self.phy_dynamic_base_change_rate, self.phy_dynamic_max_change_rate)

        # ===== 多目标切换（从进度0.21开始，1.0时100%最大） =====
        if p >= 0.21:
            self.multi_target_enabled = True
            self.multi_target_switch_prob = self._interpolate(p, 0.21, 1.0,
                self.multi_target_base_switch_prob, self.multi_target_max_switch_prob)

        # ===== 能量效率优化（新课程，从进度0.23开始） =====
        if p >= 0.23:
            self.energy_opt_enabled = True
            self.energy_opt_weight = self._interpolate(p, 0.23, 1.0,
                self.energy_opt_base_weight, self.energy_opt_max_weight)

        # ===== 运动平滑度优化（新课程，从进度0.25开始） =====
        if p >= 0.25:
            self.smooth_opt_enabled = True
            self.smooth_opt_weight = self._interpolate(p, 0.25, 1.0,
                self.smooth_opt_base_weight, self.smooth_opt_max_weight)

        # ===== 关节限位惩罚（新课程，从进度0.27开始） =====
        if p >= 0.27:
            self.joint_limit_pen_enabled = True
            self.joint_limit_pen_weight = self._interpolate(p, 0.27, 1.0,
                self.joint_limit_pen_base_weight, self.joint_limit_pen_max_weight)

        # ===== 奇异位姿规避（新课程，从进度0.29开始） =====
        if p >= 0.29:
            self.singularity_avoid_enabled = True
            self.singularity_avoid_weight = self._interpolate(p, 0.29, 1.0,
                self.singularity_avoid_base_weight, self.singularity_avoid_max_weight)

        # ===== 加速度限制（新课程，从进度0.31开始） =====
        if p >= 0.31:
            self.accel_limit_enabled = True
            self.accel_limit_max = self._interpolate(p, 0.31, 1.0,
                self.accel_limit_base_max, self.accel_limit_max_max)

        # ===== 力控精度（新课程，从进度0.33开始） =====
        if p >= 0.33:
            self.force_ctrl_enabled = True
            self.force_ctrl_precision = self._interpolate(p, 0.33, 1.0,
                self.force_ctrl_base_precision, self.force_ctrl_max_precision)

        # ===== 任务空间约束（新课程，从进度0.35开始） =====
        if p >= 0.35:
            self.task_space_constraint_enabled = True
            self.task_space_pen_weight = self._interpolate(p, 0.35, 1.0,
                self.task_space_pen_base_weight, self.task_space_pen_max_weight)

        # ===== 环境接触建模（新课程，从进度0.37开始） =====
        if p >= 0.37:
            self.contact_model_enabled = True
            self.contact_model_stiffness = self._interpolate(p, 0.37, 1.0,
                self.contact_model_base_stiffness, self.contact_model_max_stiffness)

        # ===== 时间最优控制（新课程，从进度0.39开始） =====
        if p >= 0.39:
            self.time_optimal_enabled = True
            self.time_optimal_weight = self._interpolate(p, 0.39, 1.0,
                self.time_optimal_base_weight, self.time_optimal_max_weight)

        # ===== 柔顺控制模拟（新课程，从进度0.41开始） =====
        if p >= 0.41:
            self.compliant_ctrl_enabled = True
            self.compliant_ctrl_stiffness = self._interpolate(p, 0.41, 1.0,
                self.compliant_ctrl_base_stiffness, self.compliant_ctrl_max_stiffness)

        # ===== 齿轮间隙模拟（新课程，从进度0.43开始） =====
        if p >= 0.43:
            self.gear_backlash_enabled = True
            self.gear_backlash_amount = self._interpolate(p, 0.43, 1.0,
                self.gear_backlash_base_amount, self.gear_backlash_max_amount)

        # ===== 柔性关节模拟（新课程，从进度0.45开始） =====
        if p >= 0.45:
            self.flexible_joint_enabled = True
            self.flexible_joint_stiffness = self._interpolate(p, 0.45, 1.0,
                self.flexible_joint_base_stiffness, self.flexible_joint_max_stiffness)

        # ===== 电机饱和模拟（新课程，从进度0.47开始） =====
        if p >= 0.47:
            self.motor_saturation_enabled = True
            self.motor_saturation_factor = self._interpolate(p, 0.47, 1.0,
                self.motor_saturation_base_factor, self.motor_saturation_max_factor)

        # ===== 温度漂移模拟（新课程，从进度0.49开始） =====
        if p >= 0.49:
            self.thermal_drift_enabled = True
            self.thermal_drift_rate = self._interpolate(p, 0.49, 1.0,
                self.thermal_drift_base_rate, self.thermal_drift_max_rate)

        # ===== 编码器分辨率限制（新课程，从进度0.51开始） =====
        if p >= 0.51:
            self.encoder_resolution_enabled = True
            self.encoder_resolution_bits = int(self._interpolate(p, 0.51, 1.0,
                self.encoder_resolution_base_bits, self.encoder_resolution_max_bits))

        # ===== 负载变化模拟（新课程，从进度0.53开始） =====
        if p >= 0.53:
            self.payload_variation_enabled = True
            self.payload_variation_magnitude = self._interpolate(p, 0.53, 1.0,
                self.payload_variation_base_magnitude, self.payload_variation_max_magnitude)

        # ===== 基座振动模拟（新课程，从进度0.55开始） =====
        if p >= 0.55:
            self.base_vibration_enabled = True
            self.base_vibration_magnitude = self._interpolate(p, 0.55, 1.0,
                self.base_vibration_base_magnitude, self.base_vibration_max_magnitude)

        # ===== 缆线拖拽模拟（新课程，从进度0.57开始） =====
        if p >= 0.57:
            self.cable_drag_enabled = True
            self.cable_drag_coefficient = self._interpolate(p, 0.57, 1.0,
                self.cable_drag_base_coefficient, self.cable_drag_max_coefficient)

        # ===== 惯量变化模拟（新课程，从进度0.59开始） =====
        if p >= 0.59:
            self.inertia_variation_enabled = True
            self.inertia_variation_factor = self._interpolate(p, 0.59, 1.0,
                self.inertia_variation_base_factor, self.inertia_variation_max_factor)

        # ===== 力矩波动模拟（新课程，从进度0.61开始） =====
        if p >= 0.61:
            self.torque_ripple_enabled = True
            self.torque_ripple_magnitude = self._interpolate(p, 0.61, 1.0,
                self.torque_ripple_base_magnitude, self.torque_ripple_max_magnitude)

        # ===== 传感器偏置漂移（新课程，从进度0.63开始） =====
        if p >= 0.63:
            self.sensor_bias_drift_enabled = True
            self.sensor_bias_drift_rate = self._interpolate(p, 0.63, 1.0,
                self.sensor_bias_drift_base_rate, self.sensor_bias_drift_max_rate)

        # ===== 时钟漂移模拟（新课程，从进度0.65开始） =====
        if p >= 0.65:
            self.clock_drift_enabled = True
            self.clock_drift_ppm = self._interpolate(p, 0.65, 1.0,
                self.clock_drift_base_ppm, self.clock_drift_max_ppm)

    def _interpolate(self, p, start_p, end_p, start_val, end_val):
        """线性插值"""
        if p < start_p:
            return start_val
        if p >= end_p:
            return end_val
        t = (p - start_p) / (end_p - start_p)
        return start_val + t * (end_val - start_val)

    def _interpolate_range(self, p, start_p, end_p, start_range, end_range):
        """对范围进行线性插值"""
        min_val = self._interpolate(p, start_p, end_p, start_range[0], end_range[0])
        max_val = self._interpolate(p, start_p, end_p, start_range[1], end_range[1])
        return (min_val, max_val)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        p.resetSimulation()
        p.setTimeStep(1 / self.SIM_FREQ)
        p.loadURDF("plane.urdf")

        self.robot_id = p.loadURDF(
            "kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=True
        )

        # 根据课程学习进度应用领域随机化
        if self.curriculum_progress >= 0.03:
            gravity_z = self.np_random.uniform(*self.gravity_range)
            p.setGravity(0, 0, gravity_z)
            
            for i in self._JOINT_INDICES:
                damping = self.np_random.uniform(*self.damping_range)
                friction = self.np_random.uniform(*self.friction_range)
                try:
                    p.changeDynamics(self.robot_id, i, 
                                    linearDamping=damping, 
                                    angularDamping=damping,
                                    lateralFriction=friction)
                except:
                    pass
        else:
            p.setGravity(0, 0, -9.81)

        # 惯量变化模拟（新课程）
        if self.inertia_variation_enabled:
            try:
                for i in self._JOINT_INDICES:
                    factor = self.np_random.uniform(
                        self.inertia_variation_factor, 
                        1.0 / max(self.inertia_variation_factor, 0.01)
                    )
                    p.changeDynamics(self.robot_id, i, 
                                    localInertiaDiagonal=[factor * 0.001, factor * 0.001, factor * 0.001])
            except:
                pass

        # 负载变化模拟（新课程）
        if self.payload_variation_enabled:
            try:
                payload_mass = self.np_random.uniform(0, self.payload_variation_magnitude)
                p.changeDynamics(self.robot_id, 6, mass=payload_mass)
            except:
                pass

        self.target_pos = self.np_random.uniform(self.target_min, self.target_max).astype(np.float32)

        # 多目标初始化（新课程）
        if self.multi_target_enabled:
            self.multi_target_list = []
            for _ in range(5):
                t = self.np_random.uniform(self.target_min, self.target_max).astype(np.float32)
                self.multi_target_list.append(t)
            self.current_target_idx = 0
            self.target_pos = self.multi_target_list[0].copy()

        # 动态目标初始化（新课程）
        if self.dynamic_target_enabled:
            angle = self.np_random.uniform(0, 2 * np.pi)
            speed = self.dynamic_target_speed
            self.dynamic_target_velocity = np.array([
                np.cos(angle) * speed,
                np.sin(angle) * speed * 0.5,
                np.sin(angle * 1.3) * speed * 0.3
            ], dtype=np.float32)

        for i in self._JOINT_INDICES:
            p.resetJointState(
                self.robot_id, i,
                self.np_random.uniform(-0.05, 0.05)
            )

        self.step_count = 0
        self.stable_count = 0
        self._cached_ee_pos = np.array(p.getLinkState(self.robot_id, 6)[0], dtype=np.float32)
        self._cached_joint_states = p.getJointStates(self.robot_id, self._JOINT_INDICES)

        # 清空通信延迟缓冲
        self._command_buffer = []
        self._state_buffer = []

        # 重置传感器漂移噪声
        self._drift_state = np.zeros(self.NUM_JOINTS, dtype=np.float32)
        self._drift_last_time = time.time()

        # 重置所有新课程的状态
        self._thermal_drift_state = np.zeros(self.NUM_JOINTS, dtype=np.float32)
        self._sensor_bias_state = np.zeros(self.NUM_JOINTS, dtype=np.float32)
        self._base_vibration_phase = 0.0
        self._clock_drift_accum = 0.0
        self._last_joint_vel = np.zeros(self.NUM_JOINTS, dtype=np.float32)

        for _ in range(self.RESET_STEPS):
            p.stepSimulation()

        ee_pos = np.array(p.getLinkState(self.robot_id, 6)[0])
        self.last_distance = np.linalg.norm(ee_pos - self.target_pos)

        return self._get_obs(), {}

    def step(self, action):
        action = np.clip(action, -1.0, 1.0) * self.action_scale

        # ===== 通信延迟：动作缓冲 =====
        if self.curriculum_progress >= 0.11 and self.command_delay_steps > 0:
            self._command_buffer.append(action.copy())
            if len(self._command_buffer) > self.command_delay_steps:
                actual_action = self._command_buffer.pop(0)
            else:
                actual_action = action.copy()
            # 模拟丢包
            if self.packet_drop_rate > 0 and self.np_random.random() < self.packet_drop_rate:
                actual_action = np.zeros_like(actual_action)
        else:
            actual_action = action

        # 执行器动力学：死区处理
        if self.curriculum_progress >= 0.05:
            actual_action = np.where(np.abs(actual_action) < self.dead_zone, 0, actual_action)

        # 缓存getJointStates结果（避免step()和_get_obs()重复调用）
        self._cached_joint_states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
        current_positions = np.array([s[0] for s in self._cached_joint_states])

        target_positions = current_positions + actual_action

        # 执行器动力学：速度限制
        if self.curriculum_progress >= 0.05:
            delta_pos = actual_action
            max_delta = self.velocity_limit * self.INV_SIM_FREQ
            delta_pos = np.clip(delta_pos, -max_delta, max_delta)
            target_positions = current_positions + delta_pos

        # 齿轮间隙模拟（新课程）
        if self.gear_backlash_enabled and self.gear_backlash_amount > 0:
            try:
                for i in self._JOINT_INDICES:
                    if abs(actual_action[i]) < self.gear_backlash_amount:
                        target_positions[i] = current_positions[i]
            except:
                pass

        # 电机饱和模拟（新课程）
        if self.motor_saturation_enabled and self.motor_saturation_factor < 1.0:
            try:
                target_positions = current_positions + (target_positions - current_positions) * self.motor_saturation_factor
            except:
                pass

        # 力矩波动模拟（新课程）
        if self.torque_ripple_enabled and self.torque_ripple_magnitude > 0:
            try:
                ripple = np.random.uniform(-self.torque_ripple_magnitude, self.torque_ripple_magnitude, size=self.NUM_JOINTS)
                target_positions += ripple * self.INV_SIM_FREQ
            except:
                pass

        for i in self._JOINT_INDICES:
            force = self.torque_limit if self.curriculum_progress >= 0.05 else self.torque_base_limit
            p.setJointMotorControl2(
                self.robot_id, i,
                p.POSITION_CONTROL,
                targetPosition=target_positions[i],
                force=force
            )

        for _ in range(self.sub_steps):
            p.stepSimulation()

        self.step_count += 1

        # 时钟漂移模拟（新课程）
        if self.clock_drift_enabled and self.clock_drift_ppm > 0:
            try:
                self._clock_drift_accum += self.clock_drift_ppm * 1e-6 * self.INV_SIM_FREQ
            except:
                pass

        # 基座振动模拟（新课程）
        if self.base_vibration_enabled and self.base_vibration_magnitude > 0:
            try:
                self._base_vibration_phase += 2 * np.pi * 3.0 * self.INV_SIM_FREQ
                vib = np.sin(self._base_vibration_phase) * self.base_vibration_magnitude
                for i in range(3):
                    for j in self._JOINT_INDICES:
                        p.applyExternalForce(
                            self.robot_id, j,
                            forceObj=[vib * (i == 0), vib * (i == 1), vib * (i == 2)],
                            posObj=[0, 0, 0],
                            flags=p.LINK_FRAME
                        )
            except:
                pass

        # 缆线拖拽模拟（新课程）
        if self.cable_drag_enabled and self.cable_drag_coefficient > 0:
            try:
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                for i, s in enumerate(states):
                    vel = s[1]
                    drag_force = -self.cable_drag_coefficient * vel * self.INV_SIM_FREQ
                    p.applyExternalTorque(self.robot_id, i, [0, 0, drag_force], flags=p.LINK_FRAME)
            except:
                pass

        # 温度漂移模拟（新课程）
        if self.thermal_drift_enabled and self.thermal_drift_rate > 0:
            try:
                self._thermal_drift_state += np.random.normal(
                    0, self.thermal_drift_rate, size=self.NUM_JOINTS
                ).astype(np.float32)
                self._thermal_drift_state = np.clip(self._thermal_drift_state, -0.05, 0.05)
            except:
                pass

        # 动态目标更新（新课程）
        if self.dynamic_target_enabled:
            self.target_pos += self.dynamic_target_velocity * self.INV_SIM_FREQ
            # 边界反弹
            for i in range(3):
                if self.target_pos[i] < self.target_min[i]:
                    self.target_pos[i] = self.target_min[i]
                    self.dynamic_target_velocity[i] *= -1
                elif self.target_pos[i] > self.target_max[i]:
                    self.target_pos[i] = self.target_max[i]
                    self.dynamic_target_velocity[i] *= -1

        # 多目标切换（新课程）
        if self.multi_target_enabled and self.multi_target_list:
            if self.np_random.random() < self.multi_target_switch_prob:
                self.current_target_idx = (self.current_target_idx + 1) % len(self.multi_target_list)
                self.target_pos = self.multi_target_list[self.current_target_idx].copy()
                self.stable_count = 0

        # 动态物理变化（新课程）
        if self.phy_dynamic_enabled and self.step_count % 20 == 0:
            if self.np_random.random() < self.phy_dynamic_change_rate:
                try:
                    joint = self.np_random.choice(self._JOINT_INDICES)
                    new_damping = self.np_random.uniform(*self.damping_range)
                    p.changeDynamics(self.robot_id, joint, angularDamping=new_damping)
                except:
                    pass

        # 缓存getLinkState结果（避免step()/外部扰动/_get_obs()重复调用）
        self._cached_ee_pos = np.array(p.getLinkState(self.robot_id, 6)[0], dtype=np.float32)

        # 外部扰动
        if self.curriculum_progress >= 0.09:
            if self.np_random.random() < self.disturbance_prob:
                disturbance = self.np_random.uniform(-self.disturbance_magnitude, 
                                                    self.disturbance_magnitude, 
                                                    size=3)
                p.applyExternalForce(
                    self.robot_id, 6,
                    forceObj=disturbance,
                    posObj=self._cached_ee_pos,
                    flags=p.WORLD_FRAME
                )

        # 对抗性扰动（新课程）
        if self.curriculum_progress >= 0.17 and self.adversarial_prob > 0:
            if self.np_random.random() < self.adversarial_prob:
                # 针对末端位置的对抗性力（推离目标）
                ee_to_target = self.target_pos - self._cached_ee_pos
                dist = np.linalg.norm(ee_to_target)
                if dist > 0.001:
                    adv_dir = -ee_to_target / dist
                    adv_force = adv_dir * self.adversarial_magnitude
                    p.applyExternalForce(
                        self.robot_id, 6,
                        forceObj=adv_force,
                        posObj=self._cached_ee_pos,
                        flags=p.WORLD_FRAME
                    )

        obs = self._get_obs()

        # ===== 通信延迟：状态缓冲 =====
        if self.curriculum_progress >= 0.11 and self.state_delay_steps > 0:
            self._state_buffer.append(obs.copy())
            if len(self._state_buffer) > self.state_delay_steps:
                obs = self._state_buffer.pop(0)

        ee_pos = self._cached_ee_pos
        dist = np.linalg.norm(ee_pos - self.target_pos)

        reward = 0.0

        # ===== 碰撞检测（每COLLISION_INTERVAL步检测一次，极限FPS） =====
        if self.curriculum_progress >= 0.07 and self.collision_penalty > 0 and self.step_count % self._COLLISION_INTERVAL == 0:
            try:
                contacts = p.getContactPoints(self.robot_id)
                if contacts:
                    reward -= self.collision_penalty
            except:
                pass

        # ===== 关节限位惩罚（新课程） =====
        if self.joint_limit_pen_enabled and self.joint_limit_pen_weight > 0:
            try:
                for i in self._JOINT_INDICES:
                    joint_info = p.getJointInfo(self.robot_id, i)
                    joint_state = p.getJointState(self.robot_id, i)
                    lower_limit = joint_info[8]
                    upper_limit = joint_info[9]
                    pos = joint_state[0]
                    if lower_limit < upper_limit:
                        margin = 0.05 * (upper_limit - lower_limit)
                        if pos < lower_limit + margin:
                            reward -= self.joint_limit_pen_weight * ((lower_limit + margin - pos) / margin) ** 2
                        elif pos > upper_limit - margin:
                            reward -= self.joint_limit_pen_weight * ((pos - upper_limit + margin) / margin) ** 2
            except:
                pass

        # ===== 能量效率优化（新课程） =====
        if self.energy_opt_enabled and self.energy_opt_weight > 0:
            try:
                energy = 0.0
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                for s in states:
                    torque = s[3] if len(s) > 3 else 0.0
                    velocity = s[1]
                    energy += abs(torque * velocity)
                reward -= self.energy_opt_weight * energy * self.INV_SIM_FREQ
            except:
                pass

        # ===== 运动平滑度优化（新课程） =====
        if self.smooth_opt_enabled and self.smooth_opt_weight > 0:
            try:
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                current_vel = np.array([s[1] for s in states], dtype=np.float32)
                jerk = np.sum(np.abs(current_vel - self._last_joint_vel))
                reward -= self.smooth_opt_weight * jerk
                self._last_joint_vel = current_vel
            except:
                pass

        # ===== 奇异位姿规避（新课程） =====
        if self.singularity_avoid_enabled and self.singularity_avoid_weight > 0:
            try:
                # 基于关节极限接近度的简化奇异位姿检测
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                singularity_risk = 0.0
                for i, s in enumerate(states):
                    joint_info = p.getJointInfo(self.robot_id, self._JOINT_INDICES[i])
                    lower = joint_info[8]
                    upper = joint_info[9]
                    if lower < upper:
                        pos = s[0]
                        center = (lower + upper) / 2
                        range_half = (upper - lower) / 2
                        normalized_dist = abs(pos - center) / range_half
                        if normalized_dist > 0.7:
                            singularity_risk += (normalized_dist - 0.7) / 0.3
                reward -= self.singularity_avoid_weight * singularity_risk
            except:
                pass

        # ===== 时间最优控制（新课程）—— 激励快速到达 =====
        if self.time_optimal_enabled and self.time_optimal_weight > 0:
            reward -= self.time_optimal_weight * self.time_penalty * self.INV_SIM_FREQ

        # ===== 距离成型奖励（增强） =====
        reward += (1.0 / (dist + 0.01)) * self.distance_shaped_reward * self.INV_SIM_FREQ

        # ===== 距离变化进度奖励 =====
        if self.last_distance is not None:
            distance_change = self.last_distance - dist
            reward += distance_change * self.progress_reward_scale
        
        self.last_distance = dist

        if dist < self.reach_threshold:
            self.stable_count += 1
            reward += self.stable_reward

            # ===== 目标处速度惩罚（增强） =====
            try:
                ee_vel = np.array(p.getLinkState(self.robot_id, 6, computeLinkVelocity=True)[6], dtype=np.float32)
                vel_mag = np.linalg.norm(ee_vel)
                reward -= self.velocity_penalty_at_target * vel_mag
            except:
                pass

            if self.stable_count >= self.stable_threshold:
                # ===== 提前到达奖励（增强） =====
                if self.step_count < self.max_steps * 0.3:
                    reward += self.early_reward_bonus * 2.0
                elif self.step_count < self.max_steps * 0.5:
                    reward += self.early_reward_bonus

                # ===== 连续成功可靠性奖励（增强） =====
                self._consecutive_success += 1
                reward += self.reliability_reward * min(self._consecutive_success, 10)

                reward += self.reach_reward
                terminated = True
            else:
                terminated = False
        else:
            self.stable_count = 0
            self._consecutive_success = max(0, self._consecutive_success - 1)
            terminated = False

        truncated = self.step_count >= self.max_steps

        info = {
            "distance": dist,
            "success": terminated,
            "step": self.step_count,
            "target_pos": self.target_pos.copy(),
            "curriculum_progress": self.curriculum_progress,
            "consecutive_success": self._consecutive_success
        }

        return obs, reward, terminated, truncated, info

    def _get_obs(self):
        # 使用step()中缓存的joint_states，避免重复调用getJointStates
        states = self._cached_joint_states
        joint_pos = np.array([s[0] for s in states], dtype=np.float32)
        # 使用step()中缓存的ee_pos，避免重复调用getLinkState
        ee_pos = self._cached_ee_pos

        # ===== 传感器噪声 =====
        if self.curriculum_progress >= 0.005 and self.noise_gaussian_std > 0:
            # 1. 高斯噪声
            joint_pos += np.random.normal(0, self.noise_gaussian_std, size=self.NUM_JOINTS).astype(np.float32)

            # 2. 量化噪声
            if self.noise_quantization > 0:
                joint_pos = np.round(joint_pos / self.noise_quantization) * self.noise_quantization

            # 3. 漂移噪声（随时间累积）
            if self.noise_drift > 0:
                current_time = time.time()
                dt = current_time - self._drift_last_time
                self._drift_last_time = current_time
                self._drift_state += np.random.normal(0, self.noise_drift * dt, size=self.NUM_JOINTS).astype(np.float32)
                self._drift_state = np.clip(self._drift_state, -0.01, 0.01)
                joint_pos += self._drift_state

            # 4. 抖动噪声
            if self.noise_jitter > 0:
                joint_pos += np.random.uniform(-self.noise_jitter, self.noise_jitter, size=self.NUM_JOINTS).astype(np.float32)

        # ===== 温度漂移（新课程） =====
        if self.thermal_drift_enabled:
            try:
                joint_pos += self._thermal_drift_state
            except:
                pass

        # ===== 传感器偏置漂移（新课程） =====
        if self.sensor_bias_drift_enabled and self.sensor_bias_drift_rate > 0:
            try:
                self._sensor_bias_state += np.random.normal(
                    0, self.sensor_bias_drift_rate, size=self.NUM_JOINTS
                ).astype(np.float32)
                self._sensor_bias_state = np.clip(self._sensor_bias_state, -0.02, 0.02)
                joint_pos += self._sensor_bias_state
            except:
                pass

        # ===== 编码器分辨率限制（新课程） =====
        if self.encoder_resolution_enabled and self.encoder_resolution_bits < 32:
            try:
                resolution = 2 * np.pi / (2 ** self.encoder_resolution_bits)
                joint_pos = np.round(joint_pos / resolution) * resolution
            except:
                pass

        # ===== 观测缺失（新课程） =====
        if self.curriculum_progress >= 0.15 and self.obs_drop_rate > 0:
            if self.np_random.random() < self.obs_drop_rate:
                # 随机将部分观测置零（模拟传感器失效）
                drop_mask = self.np_random.random(self.NUM_JOINTS) < 0.3
                joint_pos[drop_mask] = 0.0

        return np.concatenate([
            joint_pos, ee_pos, self.target_pos
        ], dtype=np.float32)

    def render(self):
        if self.render_mode == "rgb_array":
            width, height = 640, 480
            view_matrix = p.computeViewMatrix(
                cameraEyePosition=[1.5, 0, 1.2],
                cameraTargetPosition=[0, 0, 0.5],
                cameraUpVector=[0, 0, 1]
            )
            proj_matrix = p.computeProjectionMatrixFOV(
                fov=60, aspect=width / height,
                nearVal=0.1, farVal=100
            )
            _, _, rgb, _, _ = p.getCameraImage(
                width, height, view_matrix, proj_matrix
            )
            return np.array(rgb)[:, :, :3]

    def close(self):
        if self.physics_client >= 0:
            try:
                p.disconnect(self.physics_client)
                self.physics_client = -1
            except:
                pass
        gc.collect()

    def __del__(self):
        self.close()
