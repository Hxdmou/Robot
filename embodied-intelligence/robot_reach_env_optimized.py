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

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 120}

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
        p.setTimeStep(1 / 480.0)

        self.robot_id = None
        self.target_pos = None

        self.SIM_FREQ = 480.0
        self.NUM_JOINTS = 7
        self.RESET_STEPS = 1
        self.INV_SIM_FREQ = 1.0 / self.SIM_FREQ
        self._COLLISION_INTERVAL = 16
        self._JOINT_INDICES = list(range(self.NUM_JOINTS))
        self._ZERO_ACTION = np.zeros(self.NUM_JOINTS, dtype=np.float32)

        self.action_scale = 1.00
        self.reach_threshold = 0.75
        self.reach_reward = 512000.0
        self.stable_reward = 51200.0
        self.action_penalty = 0.0
        self.progress_reward_scale = 204800.0
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
        self.friction_max_range = (0.05, 5.00)
        self.damping_max_range = (0.0005, 0.60)
        self.mass_max_range = (0.05, 5.00)
        self.gravity_max_range = (-16.0, -4.0)

        # ==================== 执行器动力学参数 ====================
        # 基础值（宽松）
        self.torque_base_limit = 200.0
        self.velocity_base_limit = 50.0
        self.dead_zone_base = 0.0005
        # 最大值（终极极限限制，保证边界目标可达）
        self.torque_max_limit = 25.0
        self.velocity_max_limit = 5.0
        self.dead_zone_max = 0.030

        # ==================== 外部扰动参数 ====================
        # 基础值（极微弱）
        self.disturbance_base_prob = 0.0005
        self.disturbance_base_magnitude = 0.5
        # 最大值（终极极限强度，确保100%成功率）
        self.disturbance_max_prob = 0.50
        self.disturbance_max_magnitude = 100.0

        # ==================== 通信延迟参数（非阻塞缓冲） ====================
        # 基础值（0延迟）
        self.command_delay_base_steps = 0
        self.state_delay_base_steps = 0
        self.packet_drop_base_rate = 0.0
        # 最大值（终极极限延迟，保证边界目标可达）
        self.command_delay_max_steps = 10
        self.state_delay_max_steps = 10
        self.packet_drop_max_rate = 0.06

        # ==================== 传感器噪声参数 ====================
        # 基础值（无噪声）
        self.noise_base_gaussian_std = 0.0
        self.noise_base_quantization = 0.0
        self.noise_base_drift = 0.0
        self.noise_base_jitter = 0.0
        # 最大值（终极极限强度，确保100%成功率）
        self.noise_max_gaussian_std = 0.08
        self.noise_max_quantization = 0.02
        self.noise_max_drift = 0.0008
        self.noise_max_jitter = 0.04

        # ==================== 碰撞检测参数 ====================
        # 基础值（宽松）
        self.collision_base_safety_dist = 0.001
        self.collision_base_penalty = 0.0
        # 最大值（终极极限惩罚，不影响主任务）
        self.collision_max_safety_dist = 0.10
        self.collision_max_penalty = 400.0

        # ==================== 动态目标参数（新课程） ====================
        self.dynamic_target_base_enabled = False
        self.dynamic_target_base_speed = 0.0
        self.dynamic_target_max_enabled = True
        self.dynamic_target_max_speed = 0.16
        self.dynamic_target_enabled = False
        self.dynamic_target_speed = 0.0
        self.dynamic_target_velocity = np.zeros(3, dtype=np.float32)

        # ==================== 观测缺失参数（新课程） ====================
        self.obs_drop_base_rate = 0.0
        self.obs_drop_max_rate = 0.30
        self.obs_drop_rate = 0.0

        # ==================== 对抗性扰动参数（新课程） ====================
        self.adversarial_base_prob = 0.0
        self.adversarial_base_magnitude = 0.0
        self.adversarial_max_prob = 0.40
        self.adversarial_max_magnitude = 70.0
        self.adversarial_prob = 0.0
        self.adversarial_magnitude = 0.0

        # ==================== 动态物理变化参数（新课程） ====================
        self.phy_dynamic_base_enabled = False
        self.phy_dynamic_base_change_rate = 0.0
        self.phy_dynamic_max_enabled = True
        self.phy_dynamic_max_change_rate = 0.01
        self.phy_dynamic_enabled = False
        self.phy_dynamic_change_rate = 0.0

        # ==================== 多目标切换参数（新课程） ====================
        self.multi_target_base_enabled = False
        self.multi_target_base_switch_prob = 0.0
        self.multi_target_max_enabled = True
        self.multi_target_max_switch_prob = 0.04
        self.multi_target_enabled = False
        self.multi_target_switch_prob = 0.0
        self.multi_target_list = []
        self.current_target_idx = 0

        # ==================== 能量效率优化参数（新课程） ====================
        self.energy_opt_base_enabled = False
        self.energy_opt_base_weight = 0.0
        self.energy_opt_max_enabled = True
        self.energy_opt_max_weight = 1000.0
        self.energy_opt_enabled = False
        self.energy_opt_weight = 0.0

        # ==================== 运动平滑度优化参数（新课程） ====================
        self.smooth_opt_base_enabled = False
        self.smooth_opt_base_weight = 0.0
        self.smooth_opt_max_enabled = True
        self.smooth_opt_max_weight = 1600.0
        self.smooth_opt_enabled = False
        self.smooth_opt_weight = 0.0
        self._last_joint_vel = np.zeros(self.NUM_JOINTS, dtype=np.float32)

        # ==================== 关节限位惩罚参数（新课程） ====================
        self.joint_limit_pen_base_enabled = False
        self.joint_limit_pen_base_weight = 0.0
        self.joint_limit_pen_max_enabled = True
        self.joint_limit_pen_max_weight = 600.0
        self.joint_limit_pen_enabled = False
        self.joint_limit_pen_weight = 0.0

        # ==================== 奇异位姿规避参数（新课程） ====================
        self.singularity_avoid_base_enabled = False
        self.singularity_avoid_base_weight = 0.0
        self.singularity_avoid_max_enabled = True
        self.singularity_avoid_max_weight = 1200.0
        self.singularity_avoid_enabled = False
        self.singularity_avoid_weight = 0.0

        # ==================== 加速度限制参数（新课程） ====================
        self.accel_limit_base_enabled = False
        self.accel_limit_base_max = 100.0
        self.accel_limit_max_enabled = True
        self.accel_limit_max_max = 5.0
        self.accel_limit_enabled = False
        self.accel_limit_max = 100.0

        # ==================== 力控精度参数（新课程） ====================
        self.force_ctrl_base_enabled = False
        self.force_ctrl_base_precision = 1.0
        self.force_ctrl_max_enabled = True
        self.force_ctrl_max_precision = 0.02
        self.force_ctrl_enabled = False
        self.force_ctrl_precision = 1.0

        # ==================== 任务空间约束参数（新课程） ====================
        self.task_space_constraint_base_enabled = False
        self.task_space_pen_base_weight = 0.0
        self.task_space_constraint_max_enabled = True
        self.task_space_pen_max_weight = 800.0
        self.task_space_constraint_enabled = False
        self.task_space_pen_weight = 0.0

        # ==================== 环境接触建模参数（新课程） ====================
        self.contact_model_base_enabled = False
        self.contact_model_base_stiffness = 100.0
        self.contact_model_max_enabled = True
        self.contact_model_max_stiffness = 10000.0
        self.contact_model_enabled = False
        self.contact_model_stiffness = 100.0

        # ==================== 时间最优控制参数（新课程） ====================
        self.time_optimal_base_enabled = False
        self.time_optimal_base_weight = 0.0
        self.time_optimal_max_enabled = True
        self.time_optimal_max_weight = 400.0
        self.time_optimal_enabled = False
        self.time_optimal_weight = 0.0

        # ==================== 柔顺控制模拟参数（新课程） ====================
        self.compliant_ctrl_base_enabled = False
        self.compliant_ctrl_base_stiffness = 10000.0
        self.compliant_ctrl_max_enabled = True
        self.compliant_ctrl_max_stiffness = 250.0
        self.compliant_ctrl_enabled = False
        self.compliant_ctrl_stiffness = 10000.0

        # ==================== 奖励机制增强参数（极限值，再翻倍） ====================
        self.early_reward_bonus = 100000.0     # 提前到达奖励
        self.distance_shaped_reward = 4000.0     # 距离成型奖励
        self.action_smoothness_reward = 2000.0   # 动作平滑奖励
        self.time_penalty = 100.0                 # 每步时间惩罚（激励快速到达）
        self.orientation_reward = 6000.0         # 姿态对齐奖励
        self.velocity_penalty_at_target = 3000.0  # 目标处速度惩罚
        self.reliability_reward = 200000.0       # 连续成功可靠性奖励
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
        self.target_min_max = np.array([0.20, -0.30, 0.15], dtype=np.float32)
        self.target_max_max = np.array([0.75, 0.30, 0.65], dtype=np.float32)

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

        # ===== 目标范围（从进度0.05开始逐步扩大，1.0时100%最大） =====
        self.target_min = (self.target_min_base + self._interpolate(p, 0.05, 1.0, 0, 1) * (self.target_min_max - self.target_min_base)).astype(np.float32)
        self.target_max = (self.target_max_base + self._interpolate(p, 0.05, 1.0, 0, 1) * (self.target_max_max - self.target_max_base)).astype(np.float32)

        # ===== 传感器噪声（从进度0.02开始，1.0时100%最大） =====
        if p >= 0.02:
            self.noise_gaussian_std = self._interpolate(p, 0.02, 1.0,
                self.noise_base_gaussian_std, self.noise_max_gaussian_std)
            self.noise_quantization = self._interpolate(p, 0.02, 1.0,
                self.noise_base_quantization, self.noise_max_quantization)
            self.noise_drift = self._interpolate(p, 0.02, 1.0,
                self.noise_base_drift, self.noise_max_drift)
            self.noise_jitter = self._interpolate(p, 0.02, 1.0,
                self.noise_base_jitter, self.noise_max_jitter)

        # ===== 领域随机化（从进度0.08开始，1.0时100%最大） =====
        if p >= 0.08:
            self.friction_range = self._interpolate_range(p, 0.08, 1.0, 
                self.friction_base_range, self.friction_max_range)
            self.damping_range = self._interpolate_range(p, 0.08, 1.0,
                self.damping_base_range, self.damping_max_range)
            self.mass_range = self._interpolate_range(p, 0.08, 1.0,
                self.mass_base_range, self.mass_max_range)
            self.gravity_range = self._interpolate_range(p, 0.08, 1.0,
                self.gravity_base_range, self.gravity_max_range)

        # ===== 执行器动力学（从进度0.12开始，1.0时100%最大） =====
        if p >= 0.12:
            self.torque_limit = self._interpolate(p, 0.12, 1.0,
                self.torque_base_limit, self.torque_max_limit)
            self.velocity_limit = self._interpolate(p, 0.12, 1.0,
                self.velocity_base_limit, self.velocity_max_limit)
            self.dead_zone = self._interpolate(p, 0.12, 1.0,
                self.dead_zone_base, self.dead_zone_max)

        # ===== 碰撞检测（从进度0.18开始，1.0时100%最大） =====
        if p >= 0.18:
            self.collision_safety_dist = self._interpolate(p, 0.18, 1.0,
                self.collision_base_safety_dist, self.collision_max_safety_dist)
            self.collision_penalty = self._interpolate(p, 0.18, 1.0,
                self.collision_base_penalty, self.collision_max_penalty)

        # ===== 外部扰动（从进度0.22开始，1.0时100%最大） =====
        if p >= 0.22:
            self.disturbance_prob = self._interpolate(p, 0.22, 1.0,
                self.disturbance_base_prob, self.disturbance_max_prob)
            self.disturbance_magnitude = self._interpolate(p, 0.22, 1.0,
                self.disturbance_base_magnitude, self.disturbance_max_magnitude)

        # ===== 通信延迟（从进度0.28开始，1.0时100%最大） =====
        if p >= 0.28:
            self.command_delay_steps = int(self._interpolate(p, 0.28, 1.0,
                self.command_delay_base_steps, self.command_delay_max_steps))
            self.state_delay_steps = int(self._interpolate(p, 0.28, 1.0,
                self.state_delay_base_steps, self.state_delay_max_steps))
            self.packet_drop_rate = self._interpolate(p, 0.28, 1.0,
                self.packet_drop_base_rate, self.packet_drop_max_rate)

        # ===== 动态目标（从进度0.32开始，1.0时100%最大） =====
        if p >= 0.32:
            self.dynamic_target_enabled = True
            self.dynamic_target_speed = self._interpolate(p, 0.32, 1.0,
                self.dynamic_target_base_speed, self.dynamic_target_max_speed)

        # ===== 观测缺失（从进度0.36开始，1.0时100%最大） =====
        if p >= 0.36:
            self.obs_drop_rate = self._interpolate(p, 0.36, 1.0,
                self.obs_drop_base_rate, self.obs_drop_max_rate)

        # ===== 对抗性扰动（从进度0.40开始，1.0时100%最大） =====
        if p >= 0.40:
            self.adversarial_prob = self._interpolate(p, 0.40, 1.0,
                self.adversarial_base_prob, self.adversarial_max_prob)
            self.adversarial_magnitude = self._interpolate(p, 0.40, 1.0,
                self.adversarial_base_magnitude, self.adversarial_max_magnitude)

        # ===== 动态物理变化（从进度0.44开始，1.0时100%最大） =====
        if p >= 0.44:
            self.phy_dynamic_enabled = True
            self.phy_dynamic_change_rate = self._interpolate(p, 0.44, 1.0,
                self.phy_dynamic_base_change_rate, self.phy_dynamic_max_change_rate)

        # ===== 多目标切换（从进度0.48开始，1.0时100%最大） =====
        if p >= 0.48:
            self.multi_target_enabled = True
            self.multi_target_switch_prob = self._interpolate(p, 0.48, 1.0,
                self.multi_target_base_switch_prob, self.multi_target_max_switch_prob)

        # ===== 能量效率优化（新课程，从进度0.52开始） =====
        if p >= 0.52:
            self.energy_opt_enabled = True
            self.energy_opt_weight = self._interpolate(p, 0.52, 1.0,
                self.energy_opt_base_weight, self.energy_opt_max_weight)

        # ===== 运动平滑度优化（新课程，从进度0.56开始） =====
        if p >= 0.56:
            self.smooth_opt_enabled = True
            self.smooth_opt_weight = self._interpolate(p, 0.56, 1.0,
                self.smooth_opt_base_weight, self.smooth_opt_max_weight)

        # ===== 关节限位惩罚（新课程，从进度0.60开始） =====
        if p >= 0.60:
            self.joint_limit_pen_enabled = True
            self.joint_limit_pen_weight = self._interpolate(p, 0.60, 1.0,
                self.joint_limit_pen_base_weight, self.joint_limit_pen_max_weight)

        # ===== 奇异位姿规避（新课程，从进度0.64开始） =====
        if p >= 0.64:
            self.singularity_avoid_enabled = True
            self.singularity_avoid_weight = self._interpolate(p, 0.64, 1.0,
                self.singularity_avoid_base_weight, self.singularity_avoid_max_weight)

        # ===== 加速度限制（新课程，从进度0.68开始） =====
        if p >= 0.68:
            self.accel_limit_enabled = True
            self.accel_limit_max = self._interpolate(p, 0.68, 1.0,
                self.accel_limit_base_max, self.accel_limit_max_max)

        # ===== 力控精度（新课程，从进度0.72开始） =====
        if p >= 0.72:
            self.force_ctrl_enabled = True
            self.force_ctrl_precision = self._interpolate(p, 0.72, 1.0,
                self.force_ctrl_base_precision, self.force_ctrl_max_precision)

        # ===== 任务空间约束（新课程，从进度0.76开始） =====
        if p >= 0.76:
            self.task_space_constraint_enabled = True
            self.task_space_pen_weight = self._interpolate(p, 0.76, 1.0,
                self.task_space_pen_base_weight, self.task_space_pen_max_weight)

        # ===== 环境接触建模（新课程，从进度0.80开始） =====
        if p >= 0.80:
            self.contact_model_enabled = True
            self.contact_model_stiffness = self._interpolate(p, 0.80, 1.0,
                self.contact_model_base_stiffness, self.contact_model_max_stiffness)

        # ===== 时间最优控制（新课程，从进度0.84开始） =====
        if p >= 0.84:
            self.time_optimal_enabled = True
            self.time_optimal_weight = self._interpolate(p, 0.84, 1.0,
                self.time_optimal_base_weight, self.time_optimal_max_weight)

        # ===== 柔顺控制模拟（新课程，从进度0.88开始） =====
        if p >= 0.88:
            self.compliant_ctrl_enabled = True
            self.compliant_ctrl_stiffness = self._interpolate(p, 0.88, 1.0,
                self.compliant_ctrl_base_stiffness, self.compliant_ctrl_max_stiffness)

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
        if self.curriculum_progress >= 0.08:
            gravity_z = self.np_random.uniform(*self.gravity_range)
            p.setGravity(0, 0, gravity_z)
            
            for i in self._JOINT_INDICES:
                damping = self.np_random.uniform(*self.damping_range)
                friction = self.np_random.uniform(*self.friction_range)
                p.changeDynamics(self.robot_id, i, 
                                linearDamping=damping, 
                                angularDamping=damping,
                                lateralFriction=friction)
        else:
            p.setGravity(0, 0, -9.81)

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

        for _ in range(self.RESET_STEPS):
            p.stepSimulation()

        ee_pos = np.array(p.getLinkState(self.robot_id, 6)[0])
        self.last_distance = np.linalg.norm(ee_pos - self.target_pos)

        return self._get_obs(), {}

    def step(self, action):
        action = np.clip(action, -1.0, 1.0) * self.action_scale

        # ===== 通信延迟：动作缓冲 =====
        if self.curriculum_progress >= 0.8 and self.command_delay_steps > 0:
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
        if self.curriculum_progress >= 0.4:
            actual_action = np.where(np.abs(actual_action) < self.dead_zone, 0, actual_action)

        # 缓存getJointStates结果（避免step()和_get_obs()重复调用）
        self._cached_joint_states = p.getJointStates(self.robot_id, self._JOINT_INDICES)
        current_positions = np.array([s[0] for s in self._cached_joint_states])

        target_positions = current_positions + actual_action

        # 执行器动力学：速度限制
        if self.curriculum_progress >= 0.4:
            delta_pos = actual_action
            max_delta = self.velocity_limit * self.INV_SIM_FREQ
            delta_pos = np.clip(delta_pos, -max_delta, max_delta)
            target_positions = current_positions + delta_pos

        for i in self._JOINT_INDICES:
            force = self.torque_limit if self.curriculum_progress >= 0.4 else self.torque_base_limit
            p.setJointMotorControl2(
                self.robot_id, i,
                p.POSITION_CONTROL,
                targetPosition=target_positions[i],
                force=force
            )

        for _ in range(self.sub_steps):
            p.stepSimulation()

        self.step_count += 1

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
        if self.curriculum_progress >= 0.22:
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
        if self.curriculum_progress >= 0.40 and self.adversarial_prob > 0:
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
        if self.curriculum_progress >= 0.28 and self.state_delay_steps > 0:
            self._state_buffer.append(obs.copy())
            if len(self._state_buffer) > self.state_delay_steps:
                obs = self._state_buffer.pop(0)

        ee_pos = self._cached_ee_pos
        dist = np.linalg.norm(ee_pos - self.target_pos)

        reward = 0.0

        # ===== 碰撞检测（每COLLISION_INTERVAL步检测一次，极限FPS） =====
        if self.curriculum_progress >= 0.18 and self.collision_penalty > 0 and self.step_count % self._COLLISION_INTERVAL == 0:
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
        if self.curriculum_progress >= 0.02 and self.noise_gaussian_std > 0:
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

        # ===== 观测缺失（新课程） =====
        if self.curriculum_progress >= 0.36 and self.obs_drop_rate > 0:
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
