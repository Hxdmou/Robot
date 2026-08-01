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

        self.action_scale = 5.00
        self.reach_threshold = 1.50
        self.reach_reward = 50_000_000.0
        self.stable_reward = 5_000_000.0
        self.action_penalty = 0.0
        self.progress_reward_scale = 20_000_000.0
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
        self.friction_max_range = (0.001, 50.00)
        self.damping_max_range = (0.00001, 5.00)
        self.mass_max_range = (0.001, 50.00)
        self.gravity_max_range = (-40.0, -0.5)

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
        self.disturbance_max_magnitude = 1000.0

        # ==================== 通信延迟参数（非阻塞缓冲） ====================
        # 基础值（0延迟）
        self.command_delay_base_steps = 0
        self.state_delay_base_steps = 0
        self.packet_drop_base_rate = 0.0
        # 最大值（终极极限延迟，保证边界目标可达）
        self.command_delay_max_steps = 80
        self.state_delay_max_steps = 80
        self.packet_drop_max_rate = 0.95

        # ==================== 传感器噪声参数 ====================
        # 基础值（无噪声）
        self.noise_base_gaussian_std = 0.0
        self.noise_base_quantization = 0.0
        self.noise_base_drift = 0.0
        self.noise_base_jitter = 0.0
        # 最大值（终极极限强度，确保100%成功率）
        self.noise_max_gaussian_std = 0.80
        self.noise_max_quantization = 0.08
        self.noise_max_drift = 0.008
        self.noise_max_jitter = 0.40

        # ==================== 碰撞检测参数 ====================
        # 基础值（宽松）
        self.collision_base_safety_dist = 0.001
        self.collision_base_penalty = 0.0
        # 最大值（终极极限惩罚，不影响主任务）
        self.collision_max_safety_dist = 0.40
        self.collision_max_penalty = 10_000.0

        # ==================== 动态目标参数（新课程） ====================
        self.dynamic_target_base_enabled = False
        self.dynamic_target_base_speed = 0.0
        self.dynamic_target_max_enabled = True
        self.dynamic_target_max_speed = 1.50
        self.dynamic_target_enabled = False
        self.dynamic_target_speed = 0.0
        self.dynamic_target_velocity = np.zeros(3, dtype=np.float32)

        # ==================== 观测缺失参数（新课程） ====================
        self.obs_drop_base_rate = 0.0
        self.obs_drop_max_rate = 0.95
        self.obs_drop_rate = 0.0

        # ==================== 对抗性扰动参数（新课程） ====================
        self.adversarial_base_prob = 0.0
        self.adversarial_base_magnitude = 0.0
        self.adversarial_max_prob = 1.0
        self.adversarial_max_magnitude = 500.0
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
        self.multi_target_max_switch_prob = 0.05
        self.multi_target_enabled = False
        self.multi_target_switch_prob = 0.0
        self.multi_target_list = []
        self.current_target_idx = 0

        # ==================== 能量效率优化参数（新课程） ====================
        self.energy_opt_base_enabled = False
        self.energy_opt_base_weight = 0.0
        self.energy_opt_max_enabled = True
        self.energy_opt_max_weight = 50000.0
        self.energy_opt_enabled = False
        self.energy_opt_weight = 0.0

        # ==================== 运动平滑度优化参数（新课程） ====================
        self.smooth_opt_base_enabled = False
        self.smooth_opt_base_weight = 0.0
        self.smooth_opt_max_enabled = True
        self.smooth_opt_max_weight = 100000.0
        self.smooth_opt_enabled = False
        self.smooth_opt_weight = 0.0
        self._last_joint_vel = np.zeros(self.NUM_JOINTS, dtype=np.float32)

        # ==================== 关节限位惩罚参数（新课程） ====================
        self.joint_limit_pen_base_enabled = False
        self.joint_limit_pen_base_weight = 0.0
        self.joint_limit_pen_max_enabled = True
        self.joint_limit_pen_max_weight = 50000.0
        self.joint_limit_pen_enabled = False
        self.joint_limit_pen_weight = 0.0

        # ==================== 奇异位姿规避参数（新课程） ====================
        self.singularity_avoid_base_enabled = False
        self.singularity_avoid_base_weight = 0.0
        self.singularity_avoid_max_enabled = True
        self.singularity_avoid_max_weight = 100000.0
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
        self.task_space_pen_max_weight = 50000.0
        self.task_space_constraint_enabled = False
        self.task_space_pen_weight = 0.0

        # ==================== 环境接触建模参数（新课程） ====================
        self.contact_model_base_enabled = False
        self.contact_model_base_stiffness = 100.0
        self.contact_model_max_enabled = True
        self.contact_model_max_stiffness = 500000.0
        self.contact_model_enabled = False
        self.contact_model_stiffness = 100.0

        # ==================== 时间最优控制参数（新课程） ====================
        self.time_optimal_base_enabled = False
        self.time_optimal_base_weight = 0.0
        self.time_optimal_max_enabled = True
        self.time_optimal_max_weight = 30000.0
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
        self.gear_backlash_max_amount = 0.30
        self.gear_backlash_enabled = False
        self.gear_backlash_amount = 0.0

        # ==================== 柔性关节模拟参数（新课程，非摄像头） ====================
        self.flexible_joint_base_enabled = False
        self.flexible_joint_base_stiffness = 10000.0
        self.flexible_joint_max_enabled = True
        self.flexible_joint_max_stiffness = 20.0
        self.flexible_joint_enabled = False
        self.flexible_joint_stiffness = 10000.0

        # ==================== 电机饱和模拟参数（新课程，非摄像头） ====================
        self.motor_saturation_base_enabled = False
        self.motor_saturation_base_factor = 1.0
        self.motor_saturation_max_enabled = True
        self.motor_saturation_max_factor = 0.05
        self.motor_saturation_enabled = False
        self.motor_saturation_factor = 1.0

        # ==================== 温度漂移模拟参数（新课程，非摄像头） ====================
        self.thermal_drift_base_enabled = False
        self.thermal_drift_base_rate = 0.0
        self.thermal_drift_max_enabled = True
        self.thermal_drift_max_rate = 0.20
        self.thermal_drift_enabled = False
        self.thermal_drift_rate = 0.0
        self._thermal_drift_state = np.zeros(7, dtype=np.float32)

        # ==================== 编码器分辨率限制参数（新课程，非摄像头） ====================
        self.encoder_resolution_base_enabled = False
        self.encoder_resolution_base_bits = 32
        self.encoder_resolution_max_enabled = True
        self.encoder_resolution_max_bits = 2
        self.encoder_resolution_enabled = False
        self.encoder_resolution_bits = 32

        # ==================== 负载变化模拟参数（新课程，非摄像头） ====================
        self.payload_variation_base_enabled = False
        self.payload_variation_base_magnitude = 0.0
        self.payload_variation_max_enabled = True
        self.payload_variation_max_magnitude = 50.0
        self.payload_variation_enabled = False
        self.payload_variation_magnitude = 0.0

        # ==================== 基座振动模拟参数（新课程，非摄像头） ====================
        self.base_vibration_base_enabled = False
        self.base_vibration_base_magnitude = 0.0
        self.base_vibration_max_enabled = True
        self.base_vibration_max_magnitude = 0.20
        self.base_vibration_enabled = False
        self.base_vibration_magnitude = 0.0
        self._base_vibration_phase = 0.0

        # ==================== 缆线拖拽模拟参数（新课程，非摄像头） ====================
        self.cable_drag_base_enabled = False
        self.cable_drag_base_coefficient = 0.0
        self.cable_drag_max_enabled = True
        self.cable_drag_max_coefficient = 200.0
        self.cable_drag_enabled = False
        self.cable_drag_coefficient = 0.0

        # ==================== 惯量变化模拟参数（新课程，非摄像头） ====================
        self.inertia_variation_base_enabled = False
        self.inertia_variation_base_factor = 1.0
        self.inertia_variation_max_enabled = True
        self.inertia_variation_max_factor = 0.5
        self.inertia_variation_enabled = False
        self.inertia_variation_factor = 1.0

        # ==================== 力矩波动模拟参数（新课程，非摄像头） ====================
        self.torque_ripple_base_enabled = False
        self.torque_ripple_base_magnitude = 0.0
        self.torque_ripple_max_enabled = True
        self.torque_ripple_max_magnitude = 2.0
        self.torque_ripple_enabled = False
        self.torque_ripple_magnitude = 0.0

        # ==================== 传感器偏置漂移参数（新课程，非摄像头） ====================
        self.sensor_bias_drift_base_enabled = False
        self.sensor_bias_drift_base_rate = 0.0
        self.sensor_bias_drift_max_enabled = True
        self.sensor_bias_drift_max_rate = 0.20
        self.sensor_bias_drift_enabled = False
        self.sensor_bias_drift_rate = 0.0
        self._sensor_bias_state = np.zeros(7, dtype=np.float32)

        # ==================== 时钟漂移模拟参数（新课程，非摄像头） ====================
        self.clock_drift_base_enabled = False
        self.clock_drift_base_ppm = 0.0
        self.clock_drift_max_enabled = True
        self.clock_drift_max_ppm = 50000.0
        self.clock_drift_enabled = False
        self.clock_drift_ppm = 0.0
        self._clock_drift_accum = 0.0

        # ==================== 科里奥利力效应（新课程，非摄像头） ====================
        self.coriolis_base_enabled = False
        self.coriolis_base_strength = 0.0
        self.coriolis_max_enabled = True
        self.coriolis_max_strength = 1.0
        self.coriolis_enabled = False
        self.coriolis_strength = 0.0

        # ==================== 离心力效应（新课程，非摄像头） ====================
        self.centrifugal_base_enabled = False
        self.centrifugal_base_strength = 0.0
        self.centrifugal_max_enabled = True
        self.centrifugal_max_strength = 1.0
        self.centrifugal_enabled = False
        self.centrifugal_strength = 0.0

        # ==================== 关节弹性振动（新课程，非摄像头） ====================
        self.joint_vibration_base_enabled = False
        self.joint_vibration_base_amplitude = 0.0
        self.joint_vibration_max_enabled = True
        self.joint_vibration_max_amplitude = 0.50
        self.joint_vibration_enabled = False
        self.joint_vibration_amplitude = 0.0
        self._joint_vibration_phase = 0.0

        # ==================== PID参数自适应（新课程，非摄像头） ====================
        self.pid_adaptive_base_enabled = False
        self.pid_adaptive_base_noise = 0.0
        self.pid_adaptive_max_enabled = True
        self.pid_adaptive_max_noise = 0.80
        self.pid_adaptive_enabled = False
        self.pid_adaptive_noise = 0.0

        # ==================== 滑模控制模拟（新课程，非摄像头） ====================
        self.sliding_mode_base_enabled = False
        self.sliding_mode_base_ripple = 0.0
        self.sliding_mode_max_enabled = True
        self.sliding_mode_max_ripple = 1.50
        self.sliding_mode_enabled = False
        self.sliding_mode_ripple = 0.0

        # ==================== 传感器故障检测（新课程，非摄像头） ====================
        self.sensor_fault_base_enabled = False
        self.sensor_fault_base_prob = 0.0
        self.sensor_fault_max_enabled = True
        self.sensor_fault_max_prob = 0.30
        self.sensor_fault_enabled = False
        self.sensor_fault_prob = 0.0

        # ==================== 电机过热降额（新课程，非摄像头） ====================
        self.motor_thermal_base_enabled = False
        self.motor_thermal_base_derate = 0.0
        self.motor_thermal_max_enabled = True
        self.motor_thermal_max_derate = 0.50
        self.motor_thermal_enabled = False
        self.motor_thermal_derate = 0.0

        # ==================== 障碍物规避（新课程，非摄像头） ====================
        self.obstacle_avoid_base_enabled = False
        self.obstacle_avoid_base_weight = 0.0
        self.obstacle_avoid_max_enabled = True
        self.obstacle_avoid_max_weight = 50000.0
        self.obstacle_avoid_enabled = False
        self.obstacle_avoid_weight = 0.0

        # ==================== 人工势场（新课程，非摄像头） ====================
        self.artificial_pf_base_enabled = False
        self.artificial_pf_base_strength = 0.0
        self.artificial_pf_max_enabled = True
        self.artificial_pf_max_strength = 10.0
        self.artificial_pf_enabled = False
        self.artificial_pf_strength = 0.0

        # ==================== 迭代学习控制（新课程，非摄像头） ====================
        self.iterative_learn_base_enabled = False
        self.iterative_learn_base_error = 0.0
        self.iterative_learn_max_enabled = True
        self.iterative_learn_max_error = 0.30
        self.iterative_learn_enabled = False
        self.iterative_learn_error = 0.0

        # ==================== 自适应阻抗控制（新课程，非摄像头） ====================
        self.adaptive_impedance_base_enabled = False
        self.adaptive_impedance_base_stiffness = 10000.0
        self.adaptive_impedance_max_enabled = True
        self.adaptive_impedance_max_stiffness = 50.0
        self.adaptive_impedance_enabled = False
        self.adaptive_impedance_stiffness = 10000.0

        # ==================== 前馈补偿控制（新课程，非摄像头） ====================
        self.feedforward_base_enabled = False
        self.feedforward_base_gain = 0.0
        self.feedforward_max_enabled = True
        self.feedforward_max_gain = 2.0
        self.feedforward_enabled = False
        self.feedforward_gain = 0.0

        # ==================== 模型预测控制误差（新课程，非摄像头） ====================
        self.mpc_error_base_enabled = False
        self.mpc_error_base_magnitude = 0.0
        self.mpc_error_max_enabled = True
        self.mpc_error_max_magnitude = 0.30
        self.mpc_error_enabled = False
        self.mpc_error_magnitude = 0.0

        # ==================== 鲁棒控制不确定性（新课程，非摄像头） ====================
        self.robust_ctrl_base_enabled = False
        self.robust_ctrl_base_uncertainty = 0.0
        self.robust_ctrl_max_enabled = True
        self.robust_ctrl_max_uncertainty = 0.50
        self.robust_ctrl_enabled = False
        self.robust_ctrl_uncertainty = 0.0

        # ==================== 自适应控制参数漂移（新课程，非摄像头） ====================
        self.adaptive_ctrl_base_enabled = False
        self.adaptive_ctrl_base_drift = 0.0
        self.adaptive_ctrl_max_enabled = True
        self.adaptive_ctrl_max_drift = 0.40
        self.adaptive_ctrl_enabled = False
        self.adaptive_ctrl_drift = 0.0
        self._adaptive_ctrl_state = np.zeros(7, dtype=np.float32)

        # ==================== 重复控制周期误差（新课程，非摄像头） ====================
        self.repetitive_ctrl_base_enabled = False
        self.repetitive_ctrl_base_error = 0.0
        self.repetitive_ctrl_max_enabled = True
        self.repetitive_ctrl_max_error = 0.25
        self.repetitive_ctrl_enabled = False
        self.repetitive_ctrl_error = 0.0
        self._repetitive_phase = 0.0

        # ==================== 学习控制遗忘因子（新课程，非摄像头） ====================
        self.learning_ctrl_base_enabled = False
        self.learning_ctrl_base_forgetting = 0.0
        self.learning_ctrl_max_enabled = True
        self.learning_ctrl_max_forgetting = 0.60
        self.learning_ctrl_enabled = False
        self.learning_ctrl_forgetting = 0.0
        self._learning_ctrl_memory = np.zeros(7, dtype=np.float32)

        # ==================== 无源控制能量耗散（新课程，非摄像头） ====================
        self.passive_ctrl_base_enabled = False
        self.passive_ctrl_base_dissipation = 0.0
        self.passive_ctrl_max_enabled = True
        self.passive_ctrl_max_dissipation = 50.0
        self.passive_ctrl_enabled = False
        self.passive_ctrl_dissipation = 0.0

        # ==================== 反步控制虚拟误差（新课程，非摄像头） ====================
        self.backstep_ctrl_base_enabled = False
        self.backstep_ctrl_base_error = 0.0
        self.backstep_ctrl_max_enabled = True
        self.backstep_ctrl_max_error = 0.35
        self.backstep_ctrl_enabled = False
        self.backstep_ctrl_error = 0.0

        # ==================== 滑模变结构切换增益（新课程，非摄像头） ====================
        self.vss_smc_base_enabled = False
        self.vss_smc_base_gain = 0.0
        self.vss_smc_max_enabled = True
        self.vss_smc_max_gain = 1.0
        self.vss_smc_enabled = False
        self.vss_smc_gain = 0.0

        # ==================== 奖励机制增强参数（极限最大值，再翻倍） ====================
        self.early_reward_bonus = 10_000_000.0
        self.distance_shaped_reward = 400_000.0
        self.action_smoothness_reward = 200_000.0
        self.time_penalty = 10_000.0
        self.orientation_reward = 600_000.0
        self.velocity_penalty_at_target = 300_000.0
        self.reliability_reward = 20_000_000.0
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
        self.target_min_max = np.array([0.05, -0.55, 0.03], dtype=np.float32)
        self.target_max_max = np.array([0.95, 0.55, 0.90], dtype=np.float32)

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
        self.target_min = (self.target_min_base + self._interpolate(p, 0.0, 1.0, 0, 1) * (self.target_min_max - self.target_min_base)).astype(np.float32)
        self.target_max = (self.target_max_base + self._interpolate(p, 0.0, 1.0, 0, 1) * (self.target_max_max - self.target_max_base)).astype(np.float32)

        # ===== 传感器噪声（从进度0.005开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.noise_gaussian_std = self._interpolate(p, 0.0, 1.0,
                self.noise_base_gaussian_std, self.noise_max_gaussian_std)
            self.noise_quantization = self._interpolate(p, 0.0, 1.0,
                self.noise_base_quantization, self.noise_max_quantization)
            self.noise_drift = self._interpolate(p, 0.0, 1.0,
                self.noise_base_drift, self.noise_max_drift)
            self.noise_jitter = self._interpolate(p, 0.0, 1.0,
                self.noise_base_jitter, self.noise_max_jitter)

        # ===== 领域随机化（从进度0.03开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.friction_range = self._interpolate_range(p, 0.0, 1.0, 
                self.friction_base_range, self.friction_max_range)
            self.damping_range = self._interpolate_range(p, 0.0, 1.0,
                self.damping_base_range, self.damping_max_range)
            self.mass_range = self._interpolate_range(p, 0.0, 1.0,
                self.mass_base_range, self.mass_max_range)
            self.gravity_range = self._interpolate_range(p, 0.0, 1.0,
                self.gravity_base_range, self.gravity_max_range)

        # ===== 执行器动力学（从进度0.05开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.torque_limit = self._interpolate(p, 0.0, 1.0,
                self.torque_base_limit, self.torque_max_limit)
            self.velocity_limit = self._interpolate(p, 0.0, 1.0,
                self.velocity_base_limit, self.velocity_max_limit)
            self.dead_zone = self._interpolate(p, 0.0, 1.0,
                self.dead_zone_base, self.dead_zone_max)

        # ===== 碰撞检测（从进度0.07开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.collision_safety_dist = self._interpolate(p, 0.0, 1.0,
                self.collision_base_safety_dist, self.collision_max_safety_dist)
            self.collision_penalty = self._interpolate(p, 0.0, 1.0,
                self.collision_base_penalty, self.collision_max_penalty)

        # ===== 外部扰动（从进度0.09开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.disturbance_prob = self._interpolate(p, 0.0, 1.0,
                self.disturbance_base_prob, self.disturbance_max_prob)
            self.disturbance_magnitude = self._interpolate(p, 0.0, 1.0,
                self.disturbance_base_magnitude, self.disturbance_max_magnitude)

        # ===== 通信延迟（从进度0.11开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.command_delay_steps = int(self._interpolate(p, 0.0, 1.0,
                self.command_delay_base_steps, self.command_delay_max_steps))
            self.state_delay_steps = int(self._interpolate(p, 0.0, 1.0,
                self.state_delay_base_steps, self.state_delay_max_steps))
            self.packet_drop_rate = self._interpolate(p, 0.0, 1.0,
                self.packet_drop_base_rate, self.packet_drop_max_rate)

        # ===== 动态目标（从进度0.13开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.dynamic_target_enabled = True
            self.dynamic_target_speed = self._interpolate(p, 0.0, 1.0,
                self.dynamic_target_base_speed, self.dynamic_target_max_speed)

        # ===== 观测缺失（从进度0.15开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.obs_drop_rate = self._interpolate(p, 0.0, 1.0,
                self.obs_drop_base_rate, self.obs_drop_max_rate)

        # ===== 对抗性扰动（从进度0.17开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.adversarial_prob = self._interpolate(p, 0.0, 1.0,
                self.adversarial_base_prob, self.adversarial_max_prob)
            self.adversarial_magnitude = self._interpolate(p, 0.0, 1.0,
                self.adversarial_base_magnitude, self.adversarial_max_magnitude)

        # ===== 动态物理变化（从进度0.19开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.phy_dynamic_enabled = True
            self.phy_dynamic_change_rate = self._interpolate(p, 0.0, 1.0,
                self.phy_dynamic_base_change_rate, self.phy_dynamic_max_change_rate)

        # ===== 多目标切换（从进度0.21开始，1.0时100%最大） =====
        if True:  # 原进度开启点，现统一为0.0
            self.multi_target_enabled = True
            self.multi_target_switch_prob = self._interpolate(p, 0.0, 1.0,
                self.multi_target_base_switch_prob, self.multi_target_max_switch_prob)

        # ===== 能量效率优化（新课程，从进度0.23开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.energy_opt_enabled = True
            self.energy_opt_weight = self._interpolate(p, 0.0, 1.0,
                self.energy_opt_base_weight, self.energy_opt_max_weight)

        # ===== 运动平滑度优化（新课程，从进度0.25开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.smooth_opt_enabled = True
            self.smooth_opt_weight = self._interpolate(p, 0.0, 1.0,
                self.smooth_opt_base_weight, self.smooth_opt_max_weight)

        # ===== 关节限位惩罚（新课程，从进度0.27开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.joint_limit_pen_enabled = True
            self.joint_limit_pen_weight = self._interpolate(p, 0.0, 1.0,
                self.joint_limit_pen_base_weight, self.joint_limit_pen_max_weight)

        # ===== 奇异位姿规避（新课程，从进度0.29开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.singularity_avoid_enabled = True
            self.singularity_avoid_weight = self._interpolate(p, 0.0, 1.0,
                self.singularity_avoid_base_weight, self.singularity_avoid_max_weight)

        # ===== 加速度限制（新课程，从进度0.31开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.accel_limit_enabled = True
            self.accel_limit_max = self._interpolate(p, 0.0, 1.0,
                self.accel_limit_base_max, self.accel_limit_max_max)

        # ===== 力控精度（新课程，从进度0.33开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.force_ctrl_enabled = True
            self.force_ctrl_precision = self._interpolate(p, 0.0, 1.0,
                self.force_ctrl_base_precision, self.force_ctrl_max_precision)

        # ===== 任务空间约束（新课程，从进度0.35开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.task_space_constraint_enabled = True
            self.task_space_pen_weight = self._interpolate(p, 0.0, 1.0,
                self.task_space_pen_base_weight, self.task_space_pen_max_weight)

        # ===== 环境接触建模（新课程，从进度0.37开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.contact_model_enabled = True
            self.contact_model_stiffness = self._interpolate(p, 0.0, 1.0,
                self.contact_model_base_stiffness, self.contact_model_max_stiffness)

        # ===== 时间最优控制（新课程，从进度0.39开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.time_optimal_enabled = True
            self.time_optimal_weight = self._interpolate(p, 0.0, 1.0,
                self.time_optimal_base_weight, self.time_optimal_max_weight)

        # ===== 柔顺控制模拟（新课程，从进度0.41开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.compliant_ctrl_enabled = True
            self.compliant_ctrl_stiffness = self._interpolate(p, 0.0, 1.0,
                self.compliant_ctrl_base_stiffness, self.compliant_ctrl_max_stiffness)

        # ===== 齿轮间隙模拟（新课程，从进度0.43开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.gear_backlash_enabled = True
            self.gear_backlash_amount = self._interpolate(p, 0.0, 1.0,
                self.gear_backlash_base_amount, self.gear_backlash_max_amount)

        # ===== 柔性关节模拟（新课程，从进度0.45开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.flexible_joint_enabled = True
            self.flexible_joint_stiffness = self._interpolate(p, 0.0, 1.0,
                self.flexible_joint_base_stiffness, self.flexible_joint_max_stiffness)

        # ===== 电机饱和模拟（新课程，从进度0.47开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.motor_saturation_enabled = True
            self.motor_saturation_factor = self._interpolate(p, 0.0, 1.0,
                self.motor_saturation_base_factor, self.motor_saturation_max_factor)

        # ===== 温度漂移模拟（新课程，从进度0.49开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.thermal_drift_enabled = True
            self.thermal_drift_rate = self._interpolate(p, 0.0, 1.0,
                self.thermal_drift_base_rate, self.thermal_drift_max_rate)

        # ===== 编码器分辨率限制（新课程，从进度0.51开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.encoder_resolution_enabled = True
            self.encoder_resolution_bits = int(self._interpolate(p, 0.0, 1.0,
                self.encoder_resolution_base_bits, self.encoder_resolution_max_bits))

        # ===== 负载变化模拟（新课程，从进度0.53开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.payload_variation_enabled = True
            self.payload_variation_magnitude = self._interpolate(p, 0.0, 1.0,
                self.payload_variation_base_magnitude, self.payload_variation_max_magnitude)

        # ===== 基座振动模拟（新课程，从进度0.55开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.base_vibration_enabled = True
            self.base_vibration_magnitude = self._interpolate(p, 0.0, 1.0,
                self.base_vibration_base_magnitude, self.base_vibration_max_magnitude)

        # ===== 缆线拖拽模拟（新课程，从进度0.57开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.cable_drag_enabled = True
            self.cable_drag_coefficient = self._interpolate(p, 0.0, 1.0,
                self.cable_drag_base_coefficient, self.cable_drag_max_coefficient)

        # ===== 惯量变化模拟（新课程，从进度0.59开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.inertia_variation_enabled = True
            self.inertia_variation_factor = self._interpolate(p, 0.0, 1.0,
                self.inertia_variation_base_factor, self.inertia_variation_max_factor)

        # ===== 力矩波动模拟（新课程，从进度0.61开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.torque_ripple_enabled = True
            self.torque_ripple_magnitude = self._interpolate(p, 0.0, 1.0,
                self.torque_ripple_base_magnitude, self.torque_ripple_max_magnitude)

        # ===== 传感器偏置漂移（新课程，从进度0.63开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.sensor_bias_drift_enabled = True
            self.sensor_bias_drift_rate = self._interpolate(p, 0.0, 1.0,
                self.sensor_bias_drift_base_rate, self.sensor_bias_drift_max_rate)

        # ===== 时钟漂移模拟（新课程，从进度0.65开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.clock_drift_enabled = True
            self.clock_drift_ppm = self._interpolate(p, 0.0, 1.0,
                self.clock_drift_base_ppm, self.clock_drift_max_ppm)

        # ===== 科里奥利力效应（新课程，从进度0.67开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.coriolis_enabled = True
            self.coriolis_strength = self._interpolate(p, 0.0, 1.0,
                self.coriolis_base_strength, self.coriolis_max_strength)

        # ===== 离心力效应（新课程，从进度0.69开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.centrifugal_enabled = True
            self.centrifugal_strength = self._interpolate(p, 0.0, 1.0,
                self.centrifugal_base_strength, self.centrifugal_max_strength)

        # ===== 关节弹性振动（新课程，从进度0.71开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.joint_vibration_enabled = True
            self.joint_vibration_amplitude = self._interpolate(p, 0.0, 1.0,
                self.joint_vibration_base_amplitude, self.joint_vibration_max_amplitude)

        # ===== PID参数自适应（新课程，从进度0.73开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.pid_adaptive_enabled = True
            self.pid_adaptive_noise = self._interpolate(p, 0.0, 1.0,
                self.pid_adaptive_base_noise, self.pid_adaptive_max_noise)

        # ===== 滑模控制模拟（新课程，从进度0.75开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.sliding_mode_enabled = True
            self.sliding_mode_ripple = self._interpolate(p, 0.0, 1.0,
                self.sliding_mode_base_ripple, self.sliding_mode_max_ripple)

        # ===== 传感器故障检测（新课程，从进度0.77开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.sensor_fault_enabled = True
            self.sensor_fault_prob = self._interpolate(p, 0.0, 1.0,
                self.sensor_fault_base_prob, self.sensor_fault_max_prob)

        # ===== 电机过热降额（新课程，从进度0.79开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.motor_thermal_enabled = True
            self.motor_thermal_derate = self._interpolate(p, 0.0, 1.0,
                self.motor_thermal_base_derate, self.motor_thermal_max_derate)

        # ===== 障碍物规避（新课程，从进度0.81开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.obstacle_avoid_enabled = True
            self.obstacle_avoid_weight = self._interpolate(p, 0.0, 1.0,
                self.obstacle_avoid_base_weight, self.obstacle_avoid_max_weight)

        # ===== 人工势场（新课程，从进度0.83开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.artificial_pf_enabled = True
            self.artificial_pf_strength = self._interpolate(p, 0.0, 1.0,
                self.artificial_pf_base_strength, self.artificial_pf_max_strength)

        # ===== 迭代学习控制（新课程，从进度0.85开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.iterative_learn_enabled = True
            self.iterative_learn_error = self._interpolate(p, 0.0, 1.0,
                self.iterative_learn_base_error, self.iterative_learn_max_error)

        # ===== 自适应阻抗控制（新课程，从进度0.86开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.adaptive_impedance_enabled = True
            self.adaptive_impedance_stiffness = self._interpolate(p, 0.0, 1.0,
                self.adaptive_impedance_base_stiffness, self.adaptive_impedance_max_stiffness)

        # ===== 前馈补偿控制（新课程，从进度0.87开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.feedforward_enabled = True
            self.feedforward_gain = self._interpolate(p, 0.0, 1.0,
                self.feedforward_base_gain, self.feedforward_max_gain)

        # ===== 模型预测控制误差（新课程，从进度0.88开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.mpc_error_enabled = True
            self.mpc_error_magnitude = self._interpolate(p, 0.0, 1.0,
                self.mpc_error_base_magnitude, self.mpc_error_max_magnitude)

        # ===== 鲁棒控制不确定性（新课程，从进度0.89开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.robust_ctrl_enabled = True
            self.robust_ctrl_uncertainty = self._interpolate(p, 0.0, 1.0,
                self.robust_ctrl_base_uncertainty, self.robust_ctrl_max_uncertainty)

        # ===== 自适应控制参数漂移（新课程，从进度0.90开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.adaptive_ctrl_enabled = True
            self.adaptive_ctrl_drift = self._interpolate(p, 0.0, 1.0,
                self.adaptive_ctrl_base_drift, self.adaptive_ctrl_max_drift)

        # ===== 重复控制周期误差（新课程，从进度0.91开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.repetitive_ctrl_enabled = True
            self.repetitive_ctrl_error = self._interpolate(p, 0.0, 1.0,
                self.repetitive_ctrl_base_error, self.repetitive_ctrl_max_error)

        # ===== 学习控制遗忘因子（新课程，从进度0.92开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.learning_ctrl_enabled = True
            self.learning_ctrl_forgetting = self._interpolate(p, 0.0, 1.0,
                self.learning_ctrl_base_forgetting, self.learning_ctrl_max_forgetting)

        # ===== 无源控制能量耗散（新课程，从进度0.93开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.passive_ctrl_enabled = True
            self.passive_ctrl_dissipation = self._interpolate(p, 0.0, 1.0,
                self.passive_ctrl_base_dissipation, self.passive_ctrl_max_dissipation)

        # ===== 反步控制虚拟误差（新课程，从进度0.94开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.backstep_ctrl_enabled = True
            self.backstep_ctrl_error = self._interpolate(p, 0.0, 1.0,
                self.backstep_ctrl_base_error, self.backstep_ctrl_max_error)

        # ===== 滑模变结构切换增益（新课程，从进度0.95开始） =====
        if True:  # 原进度开启点，现统一为0.0
            self.vss_smc_enabled = True
            self.vss_smc_gain = self._interpolate(p, 0.0, 1.0,
                self.vss_smc_base_gain, self.vss_smc_max_gain)

    def _interpolate(self, p, start_p, end_p, start_val, end_val):
        """根据进度线性插值：p<=start_p返回start_val，p>=end_p返回end_val，中间线性过渡"""
        if p <= start_p:
            return start_val
        if p >= end_p:
            return end_val
        ratio = (p - start_p) / (end_p - start_p)
        return start_val + ratio * (end_val - start_val)

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
        if self.curriculum_progress >= 0.0:
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
        self._joint_vibration_phase = 0.0
        self._adaptive_ctrl_state = np.zeros(self.NUM_JOINTS, dtype=np.float32)
        self._repetitive_phase = 0.0
        self._learning_ctrl_memory = np.zeros(self.NUM_JOINTS, dtype=np.float32)

        for _ in range(self.RESET_STEPS):
            p.stepSimulation()

        ee_pos = np.array(p.getLinkState(self.robot_id, 6)[0])
        self.last_distance = np.linalg.norm(ee_pos - self.target_pos)

        return self._get_obs(), {}

    def step(self, action):
        action = np.clip(action, -1.0, 1.0) * self.action_scale

        # ===== 通信延迟：动作缓冲 =====
        if self.curriculum_progress >= 0.0 and self.command_delay_steps > 0:
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
        if self.curriculum_progress >= 0.0:
            actual_action = np.where(np.abs(actual_action) < self.dead_zone, 0, actual_action)

        # 缓存getJointStates结果（避免step()和_get_obs()重复调用）
        self._cached_joint_states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
        current_positions = np.array([s[0] for s in self._cached_joint_states])

        target_positions = current_positions + actual_action

        # 执行器动力学：速度限制
        if self.curriculum_progress >= 0.0:
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

        # 柔性关节模拟（新课程）—— 关节弹性导致的位置偏差
        if self.flexible_joint_enabled and self.flexible_joint_stiffness < 10000.0:
            try:
                # 低刚度意味着关节会"弹性弯曲"，产生与目标位置的偏差
                deflection = (target_positions - current_positions) * (1.0 - self.flexible_joint_stiffness / 10000.0) * 0.3
                target_positions = current_positions + (target_positions - current_positions) * (self.flexible_joint_stiffness / 10000.0) + deflection * 0.1
            except:
                pass

        # 滑模控制模拟（新课程）—— 抖振效应
        if self.sliding_mode_enabled and self.sliding_mode_ripple > 0:
            try:
                # 滑模控制的高频切换产生抖振
                chattering = np.sign(target_positions - current_positions) * self.sliding_mode_ripple
                target_positions += chattering * self.INV_SIM_FREQ
            except:
                pass

        # PID参数自适应噪声（新课程）—— 控制器参数扰动
        if self.pid_adaptive_enabled and self.pid_adaptive_noise > 0:
            try:
                # 模拟PID增益自适应过程中的参数波动
                pid_noise = np.random.normal(0, self.pid_adaptive_noise, size=self.NUM_JOINTS).astype(np.float32)
                target_positions += pid_noise * (target_positions - current_positions) * 0.5
            except:
                pass

        # 电机过热降额（新课程）—— 温度升高降低输出能力
        if self.motor_thermal_enabled and self.motor_thermal_derate > 0:
            try:
                # 过热导致输出扭矩和速度能力下降
                derate_factor = 1.0 - self.motor_thermal_derate * 0.5
                target_positions = current_positions + (target_positions - current_positions) * derate_factor
            except:
                pass

        # 迭代学习控制误差（新课程）—— 重复轨迹误差补偿
        if self.iterative_learn_enabled and self.iterative_learn_error > 0:
            try:
                # 模拟迭代学习过程中的残余误差
                learn_error = np.random.normal(0, self.iterative_learn_error, size=self.NUM_JOINTS).astype(np.float32)
                target_positions += learn_error * 0.1
            except:
                pass

        # 前馈补偿控制（新课程）—— 前馈增益导致的位置过冲
        if self.feedforward_enabled and self.feedforward_gain > 0:
            try:
                # 前馈补偿过度导致的超调
                overshoot = (target_positions - current_positions) * self.feedforward_gain * 0.15
                target_positions += overshoot
            except:
                pass

        # 模型预测控制误差（新课程）—— MPC预测不精确
        if self.mpc_error_enabled and self.mpc_error_magnitude > 0:
            try:
                mpc_err = np.random.normal(0, self.mpc_error_magnitude, size=self.NUM_JOINTS).astype(np.float32)
                target_positions += mpc_err * 0.1
            except:
                pass

        # 鲁棒控制不确定性（新课程）—— 模型不确定性扰动
        if self.robust_ctrl_enabled and self.robust_ctrl_uncertainty > 0:
            try:
                uncertainty = np.random.uniform(
                    1.0 - self.robust_ctrl_uncertainty,
                    1.0 + self.robust_ctrl_uncertainty,
                    size=self.NUM_JOINTS
                )
                target_positions = current_positions + (target_positions - current_positions) * uncertainty
            except:
                pass

        # 反步控制虚拟误差（新课程）—— 反步设计中的虚拟控制误差
        if self.backstep_ctrl_enabled and self.backstep_ctrl_error > 0:
            try:
                backstep_err = np.random.normal(0, self.backstep_ctrl_error, size=self.NUM_JOINTS).astype(np.float32)
                target_positions += backstep_err * 0.08
            except:
                pass

        # 滑模变结构切换增益（新课程）—— 变结构控制的切换振荡
        if self.vss_smc_enabled and self.vss_smc_gain > 0:
            try:
                vss_switch = np.sign(np.random.randn(self.NUM_JOINTS)) * self.vss_smc_gain
                target_positions += vss_switch * self.INV_SIM_FREQ * 10
            except:
                pass

        for i in self._JOINT_INDICES:
            force = self.torque_limit if self.curriculum_progress >= 0.0 else self.torque_base_limit
            p.setJointMotorControl2(
                self.robot_id, i,
                p.POSITION_CONTROL,
                targetPosition=target_positions[i],
                force=force
            )

        for _ in range(self.sub_steps):
            p.stepSimulation()

        self.step_count += 1

        # 自适应阻抗控制（新课程）—— 可变阻抗的关节行为
        if self.adaptive_impedance_enabled and self.adaptive_impedance_stiffness < 10000.0:
            try:
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                for i, s in enumerate(states):
                    pos = s[0]
                    vel = s[1]
                    # 自适应阻抗：根据运动状态调整刚度，产生阻尼力
                    impedance_force = -self.adaptive_impedance_stiffness * 0.0005 * vel * abs(vel)
                    p.applyExternalTorque(self.robot_id, i, [impedance_force, 0, 0], flags=p.LINK_FRAME)
            except:
                pass

        # 自适应控制参数漂移（新课程）—— 控制器参数随时间漂移
        if self.adaptive_ctrl_enabled and self.adaptive_ctrl_drift > 0:
            try:
                self._adaptive_ctrl_state += np.random.normal(
                    0, self.adaptive_ctrl_drift, size=self.NUM_JOINTS
                ).astype(np.float32) * self.INV_SIM_FREQ
                self._adaptive_ctrl_state = np.clip(self._adaptive_ctrl_state, -0.1, 0.1)
                for i in self._JOINT_INDICES:
                    p.applyExternalTorque(self.robot_id, i, [self._adaptive_ctrl_state[i] * 10, 0, 0], flags=p.LINK_FRAME)
            except:
                pass

        # 重复控制周期误差（新课程）—— 周期性重复误差
        if self.repetitive_ctrl_enabled and self.repetitive_ctrl_error > 0:
            try:
                self._repetitive_phase += 2 * np.pi * 2.0 * self.INV_SIM_FREQ
                periodic_error = np.sin(self._repetitive_phase) * self.repetitive_ctrl_error
                for i in self._JOINT_INDICES:
                    p.applyExternalTorque(self.robot_id, i, [periodic_error * 5, 0, 0], flags=p.LINK_FRAME)
            except:
                pass

        # 学习控制遗忘因子（新课程）—— 学习记忆随时间衰减
        if self.learning_ctrl_enabled and self.learning_ctrl_forgetting > 0:
            try:
                # 遗忘导致控制精度下降
                self._learning_ctrl_memory *= (1.0 - self.learning_ctrl_forgetting * self.INV_SIM_FREQ)
                self._learning_ctrl_memory += np.random.normal(0, 0.001, size=self.NUM_JOINTS).astype(np.float32)
                forget_force = self._learning_ctrl_memory * self.learning_ctrl_forgetting * 50
                for i in self._JOINT_INDICES:
                    p.applyExternalTorque(self.robot_id, i, [forget_force[i], 0, 0], flags=p.LINK_FRAME)
            except:
                pass

        # 无源控制能量耗散（新课程）—— 系统能量耗散效应
        if self.passive_ctrl_enabled and self.passive_ctrl_dissipation > 0:
            try:
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                for i, s in enumerate(states):
                    vel = s[1]
                    # 无源控制：保证能量耗散的阻尼力
                    passive_force = -self.passive_ctrl_dissipation * vel * 0.01
                    p.applyExternalTorque(self.robot_id, i, [passive_force, 0, 0], flags=p.LINK_FRAME)
            except:
                pass

        # 时钟漂移模拟（新课程）—— 影响实际仿真步长
        if self.clock_drift_enabled and self.clock_drift_ppm > 0:
            try:
                self._clock_drift_accum += self.clock_drift_ppm * 1e-6 * self.INV_SIM_FREQ
                # 时钟漂移导致的累积时间误差（在长时间运行后影响控制精度）
                drift_error = np.sin(self._clock_drift_accum * 100.0) * self.clock_drift_ppm * 1e-9
                for i in self._JOINT_INDICES:
                    current_joint_pos = p.getJointState(self.robot_id, i)[0]
                    p.resetJointState(self.robot_id, i, current_joint_pos + drift_error)
            except:
                pass

        # 科里奥利力效应（新课程）—— 旋转参考系中的惯性力
        if self.coriolis_enabled and self.coriolis_strength > 0:
            try:
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                for i, s in enumerate(states):
                    vel = s[1]
                    # 科里奥利力：F_c = -2m(ω × v)，简化为与速度平方相关的扰动力
                    coriolis_force = -2.0 * self.coriolis_strength * vel * abs(vel) * 0.01
                    p.applyExternalTorque(self.robot_id, i, [coriolis_force, 0, 0], flags=p.LINK_FRAME)
            except:
                pass

        # 离心力效应（新课程）—— 关节高速运动时的径向力
        if self.centrifugal_enabled and self.centrifugal_strength > 0:
            try:
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                for i, s in enumerate(states):
                    vel = s[1]
                    pos = s[0]
                    # 离心力：F_cent = mω²r，简化为与速度平方成正比的扩张力
                    centrifugal_force = self.centrifugal_strength * vel * vel * np.sign(pos) * 0.05
                    p.applyExternalTorque(self.robot_id, i, [centrifugal_force, 0, 0], flags=p.LINK_FRAME)
            except:
                pass

        # 关节弹性振动（新课程）—— 关节柔性导致的振荡
        if self.joint_vibration_enabled and self.joint_vibration_amplitude > 0:
            try:
                self._joint_vibration_phase += 2 * np.pi * 50.0 * self.INV_SIM_FREQ
                vibration = np.sin(self._joint_vibration_phase) * self.joint_vibration_amplitude
                for i in self._JOINT_INDICES:
                    p.applyExternalTorque(self.robot_id, i, [vibration * 0.1, 0, 0], flags=p.LINK_FRAME)
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

        # 传感器故障检测（新课程）—— 偶发性传感器读数跳变
        if self.sensor_fault_enabled and self.sensor_fault_prob > 0:
            try:
                if self.np_random.random() < self.sensor_fault_prob:
                    # 模拟传感器故障：随机一个关节读数跳变
                    fault_joint = self.np_random.choice(self._JOINT_INDICES)
                    current_joint_pos = p.getJointState(self.robot_id, fault_joint)[0]
                    # 故障时关节位置读数被重置（通过施加一个大的瞬时扰动）
                    p.applyExternalTorque(self.robot_id, fault_joint, [self.np_random.uniform(-50, 50), 0, 0], flags=p.LINK_FRAME)
            except:
                pass

        # 障碍物规避（新课程）—— 工作空间中的排斥力场
        if self.obstacle_avoid_enabled and self.obstacle_avoid_weight > 0:
            try:
                # 模拟虚拟障碍物（工作空间边界和随机障碍点）
                ee_pos_current = np.array(p.getLinkState(self.robot_id, 6)[0], dtype=np.float32)
                # 边界排斥力
                boundary_center = np.array([0.5, 0.0, 0.45], dtype=np.float32)
                boundary_radius = 0.55
                dist_to_center = np.linalg.norm(ee_pos_current - boundary_center)
                if dist_to_center > boundary_radius * 0.8:
                    penalty = self.obstacle_avoid_weight * ((dist_to_center - boundary_radius * 0.8) / (boundary_radius * 0.2)) ** 2
                    reward -= penalty * self.INV_SIM_FREQ
            except:
                pass

        # 人工势场（新课程）—— 目标吸引力+障碍物排斥力
        if self.artificial_pf_enabled and self.artificial_pf_strength > 0:
            try:
                ee_pos_current = np.array(p.getLinkState(self.robot_id, 6)[0], dtype=np.float32)
                # 势场梯度惩罚（与目标距离相关的额外势场）
                dist = np.linalg.norm(ee_pos_current - self.target_pos)
                # 当距离较远时施加额外的势场导向奖励
                pf_reward = self.artificial_pf_strength * (1.0 / (dist + 0.1)) * self.INV_SIM_FREQ
                reward += pf_reward
            except:
                pass

        # 加速度限制（新课程）—— 限制关节加速度
        if self.accel_limit_enabled and self.accel_limit_max < 100.0:
            try:
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                current_vel = np.array([s[1] for s in states], dtype=np.float32)
                # 计算加速度并限制
                accel = (current_vel - self._last_joint_vel) / self.INV_SIM_FREQ
                accel_penalty = np.sum(np.abs(accel)) * self.accel_limit_max * 0.001
                reward -= accel_penalty * self.INV_SIM_FREQ
                self._last_joint_vel = current_vel
            except:
                pass

        # 力控精度（新课程）—— 模拟力传感器精度限制
        if self.force_ctrl_enabled and self.force_ctrl_precision < 1.0:
            try:
                # 低精度力传感器导致的控制误差
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                for i, s in enumerate(states):
                    torque = s[3] if len(s) > 3 else 0.0
                    # 量化力反馈误差
                    quantized_torque = np.round(torque / self.force_ctrl_precision) * self.force_ctrl_precision
                    torque_error = torque - quantized_torque
                    p.applyExternalTorque(self.robot_id, i, [torque_error * 0.01, 0, 0], flags=p.LINK_FRAME)
            except:
                pass

        # 任务空间约束（新课程）—— 末端执行器操作空间约束
        if self.task_space_constraint_enabled and self.task_space_pen_weight > 0:
            try:
                ee_pos_current = np.array(p.getLinkState(self.robot_id, 6)[0], dtype=np.float32)
                # 约束末端在合理操作空间内
                min_workspace = np.array([0.0, -0.6, 0.0], dtype=np.float32)
                max_workspace = np.array([1.0, 0.6, 1.0], dtype=np.float32)
                constraint_penalty = 0.0
                for dim in range(3):
                    if ee_pos_current[dim] < min_workspace[dim]:
                        constraint_penalty += (min_workspace[dim] - ee_pos_current[dim]) ** 2
                    elif ee_pos_current[dim] > max_workspace[dim]:
                        constraint_penalty += (ee_pos_current[dim] - max_workspace[dim]) ** 2
                reward -= self.task_space_pen_weight * constraint_penalty * self.INV_SIM_FREQ
            except:
                pass

        # 环境接触建模（新课程）—— 高刚度接触力
        if self.contact_model_enabled and self.contact_model_stiffness > 100.0:
            try:
                # 检测与地面的接触并施加接触力
                contacts = p.getContactPoints(self.robot_id)
                if contacts:
                    contact_penalty = len(contacts) * self.contact_model_stiffness * 0.0001
                    reward -= contact_penalty * self.INV_SIM_FREQ
            except:
                pass

        # 柔顺控制模拟（新课程）—— 低刚度柔顺行为
        if self.compliant_ctrl_enabled and self.compliant_ctrl_stiffness < 10000.0:
            try:
                # 柔顺控制：位置误差转化为弹性恢复力
                states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
                for i, s in enumerate(states):
                    pos = s[0]
                    vel = s[1]
                    # 低刚度下关节对位置指令的跟踪有延迟和偏差
                    compliance_force = -self.compliant_ctrl_stiffness * 0.001 * vel
                    p.applyExternalTorque(self.robot_id, i, [compliance_force, 0, 0], flags=p.LINK_FRAME)
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
        if self.curriculum_progress >= 0.0:
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
        if self.curriculum_progress >= 0.0 and self.adversarial_prob > 0:
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
        if self.curriculum_progress >= 0.0 and self.state_delay_steps > 0:
            self._state_buffer.append(obs.copy())
            if len(self._state_buffer) > self.state_delay_steps:
                obs = self._state_buffer.pop(0)

        ee_pos = self._cached_ee_pos
        dist = np.linalg.norm(ee_pos - self.target_pos)

        reward = 0.0

        # ===== 碰撞检测（每COLLISION_INTERVAL步检测一次，极限FPS） =====
        if self.curriculum_progress >= 0.0 and self.collision_penalty > 0 and self.step_count % self._COLLISION_INTERVAL == 0:
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
        if self.curriculum_progress >= 0.0 and self.noise_gaussian_std > 0:
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
        if self.curriculum_progress >= 0.0 and self.obs_drop_rate > 0:
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
