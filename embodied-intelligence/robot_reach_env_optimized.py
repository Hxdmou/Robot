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

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

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
        p.setTimeStep(1 / 240.0)

        self.robot_id = None
        self.target_pos = None

        self.SIM_FREQ = 240.0
        self.NUM_JOINTS = 7
        self.RESET_STEPS = 2

        self.action_scale = 0.20
        self.reach_threshold = 0.30
        self.reach_reward = 2000.0
        self.stable_reward = 150.0
        self.action_penalty = 0.0
        self.progress_reward_scale = 500.0
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
        # 最大范围（中等）
        self.friction_max_range = (0.90, 1.10)
        self.damping_max_range = (0.03, 0.07)
        self.mass_max_range = (0.90, 1.10)
        self.gravity_max_range = (-9.90, -9.72)

        # ==================== 执行器动力学参数 ====================
        # 基础值（宽松）
        self.torque_base_limit = 200.0
        self.velocity_base_limit = 50.0
        self.dead_zone_base = 0.0005
        # 最大值（中等限制，保证边界目标可达）
        self.torque_max_limit = 150.0
        self.velocity_max_limit = 35.0
        self.dead_zone_max = 0.002

        # ==================== 外部扰动参数 ====================
        # 基础值（极微弱）
        self.disturbance_base_prob = 0.0005
        self.disturbance_base_magnitude = 0.5
        # 最大值（中等）
        self.disturbance_max_prob = 0.02
        self.disturbance_max_magnitude = 5.0

        # ==================== 通信延迟参数（非阻塞缓冲） ====================
        # 基础值（0延迟）
        self.command_delay_base_steps = 0
        self.state_delay_base_steps = 0
        self.packet_drop_base_rate = 0.0
        # 最大值（极轻微延迟，保证边界目标可达）
        self.command_delay_max_steps = 1
        self.state_delay_max_steps = 1
        self.packet_drop_max_rate = 0.002

        # ==================== 传感器噪声参数 ====================
        # 基础值（无噪声）
        self.noise_base_gaussian_std = 0.0
        self.noise_base_quantization = 0.0
        self.noise_base_drift = 0.0
        self.noise_base_jitter = 0.0
        # 最大值（轻微噪声）
        self.noise_max_gaussian_std = 0.002
        self.noise_max_quantization = 0.0005
        self.noise_max_drift = 0.00002
        self.noise_max_jitter = 0.001

        # ==================== 碰撞检测参数 ====================
        # 基础值（宽松）
        self.collision_base_safety_dist = 0.001
        self.collision_base_penalty = 0.0
        # 最大值（轻微惩罚，不影响主任务）
        self.collision_max_safety_dist = 0.005
        self.collision_max_penalty = 20.0

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
        # 目标范围（最大：中等难度，已验证100%可达）
        self.target_min_max = np.array([0.37, -0.12, 0.30], dtype=np.float32)
        self.target_max_max = np.array([0.53, 0.12, 0.42], dtype=np.float32)

        self.target_min = self.target_min_base.copy()
        self.target_max = self.target_max_base.copy()

        self.stable_count = 0
        self.stable_threshold = 2

        self.last_distance = None

    def set_curriculum_progress(self, progress):
        """设置课程学习进度 (0.0 - 1.0)"""
        self.curriculum_progress = np.clip(progress, 0.0, 1.0)

        # 根据进度更新增强模块参数
        p = self.curriculum_progress

        # ===== 目标范围（从进度0.3开始逐步扩大） =====
        self.target_min = (self.target_min_base + self._interpolate(p, 0.3, 1.0, 0, 1) * (self.target_min_max - self.target_min_base)).astype(np.float32)
        self.target_max = (self.target_max_base + self._interpolate(p, 0.3, 1.0, 0, 1) * (self.target_max_max - self.target_max_base)).astype(np.float32)

        # ===== 传感器噪声（从进度0.1开始） =====
        if p >= 0.1:
            self.noise_gaussian_std = self._interpolate(p, 0.1, 1.0,
                self.noise_base_gaussian_std, self.noise_max_gaussian_std)
            self.noise_quantization = self._interpolate(p, 0.1, 1.0,
                self.noise_base_quantization, self.noise_max_quantization)
            self.noise_drift = self._interpolate(p, 0.1, 1.0,
                self.noise_base_drift, self.noise_max_drift)
            self.noise_jitter = self._interpolate(p, 0.1, 1.0,
                self.noise_base_jitter, self.noise_max_jitter)

        # ===== 领域随机化（从进度0.2开始） =====
        if p >= 0.2:
            self.friction_range = self._interpolate_range(p, 0.2, 1.0, 
                self.friction_base_range, self.friction_max_range)
            self.damping_range = self._interpolate_range(p, 0.2, 1.0,
                self.damping_base_range, self.damping_max_range)
            self.mass_range = self._interpolate_range(p, 0.2, 1.0,
                self.mass_base_range, self.mass_max_range)
            self.gravity_range = self._interpolate_range(p, 0.2, 1.0,
                self.gravity_base_range, self.gravity_max_range)

        # ===== 执行器动力学 =====
        if p >= 0.4:
            self.torque_limit = self._interpolate(p, 0.4, 1.0,
                self.torque_base_limit, self.torque_max_limit)
            self.velocity_limit = self._interpolate(p, 0.4, 1.0,
                self.velocity_base_limit, self.velocity_max_limit)
            self.dead_zone = self._interpolate(p, 0.4, 1.0,
                self.dead_zone_base, self.dead_zone_max)

        # ===== 碰撞检测（从进度0.5开始） =====
        if p >= 0.5:
            self.collision_safety_dist = self._interpolate(p, 0.5, 1.0,
                self.collision_base_safety_dist, self.collision_max_safety_dist)
            self.collision_penalty = self._interpolate(p, 0.5, 1.0,
                self.collision_base_penalty, self.collision_max_penalty)

        # ===== 外部扰动（从进度0.6开始） =====
        if p >= 0.6:
            self.disturbance_prob = self._interpolate(p, 0.6, 1.0,
                self.disturbance_base_prob, self.disturbance_max_prob)
            self.disturbance_magnitude = self._interpolate(p, 0.6, 1.0,
                self.disturbance_base_magnitude, self.disturbance_max_magnitude)

        # ===== 通信延迟（从进度0.8开始） =====
        if p >= 0.8:
            self.command_delay_steps = int(self._interpolate(p, 0.8, 1.0,
                self.command_delay_base_steps, self.command_delay_max_steps))
            self.state_delay_steps = int(self._interpolate(p, 0.8, 1.0,
                self.state_delay_base_steps, self.state_delay_max_steps))
            self.packet_drop_rate = self._interpolate(p, 0.8, 1.0,
                self.packet_drop_base_rate, self.packet_drop_max_rate)

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
        if self.curriculum_progress >= 0.2:
            gravity_z = self.np_random.uniform(*self.gravity_range)
            p.setGravity(0, 0, gravity_z)
            
            for i in range(self.NUM_JOINTS):
                damping = self.np_random.uniform(*self.damping_range)
                friction = self.np_random.uniform(*self.friction_range)
                p.changeDynamics(self.robot_id, i, 
                                linearDamping=damping, 
                                angularDamping=damping,
                                lateralFriction=friction)
        else:
            p.setGravity(0, 0, -9.81)

        self.target_pos = self.np_random.uniform(self.target_min, self.target_max).astype(np.float32)

        for i in range(self.NUM_JOINTS):
            p.resetJointState(
                self.robot_id, i,
                self.np_random.uniform(-0.05, 0.05)
            )

        self.step_count = 0
        self.stable_count = 0
        self._cached_ee_pos = np.array(p.getLinkState(self.robot_id, 6)[0], dtype=np.float32)

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

        states = p.getJointStates(self.robot_id, range(self.NUM_JOINTS))
        current_positions = np.array([s[0] for s in states])
        current_velocities = np.array([s[1] for s in states])

        target_positions = current_positions + actual_action

        # 执行器动力学：速度限制
        if self.curriculum_progress >= 0.4:
            delta_pos = actual_action
            max_delta = self.velocity_limit * (1 / self.SIM_FREQ)
            delta_pos = np.clip(delta_pos, -max_delta, max_delta)
            target_positions = current_positions + delta_pos

        for i in range(self.NUM_JOINTS):
            force = self.torque_limit if self.curriculum_progress >= 0.4 else self.torque_base_limit
            p.setJointMotorControl2(
                self.robot_id, i,
                p.POSITION_CONTROL,
                targetPosition=target_positions[i],
                force=force
            )

        for _ in range(self.sub_steps):
            p.stepSimulation()

        # 外部扰动
        if self.curriculum_progress >= 0.6:
            if self.np_random.random() < self.disturbance_prob:
                disturbance = self.np_random.uniform(-self.disturbance_magnitude, 
                                                    self.disturbance_magnitude, 
                                                    size=3)
                p.applyExternalForce(
                    self.robot_id, 6,
                    forceObj=disturbance,
                    posObj=np.array(p.getLinkState(self.robot_id, 6)[0]),
                    flags=p.WORLD_FRAME
                )

        self.step_count += 1

        # 缓存getLinkState结果（避免step()和_get_obs()重复调用）
        self._cached_ee_pos = np.array(p.getLinkState(self.robot_id, 6)[0], dtype=np.float32)

        obs = self._get_obs()

        # ===== 通信延迟：状态缓冲 =====
        if self.curriculum_progress >= 0.8 and self.state_delay_steps > 0:
            self._state_buffer.append(obs.copy())
            if len(self._state_buffer) > self.state_delay_steps:
                obs = self._state_buffer.pop(0)

        ee_pos = self._cached_ee_pos
        dist = np.linalg.norm(ee_pos - self.target_pos)

        reward = 0.0

        # ===== 碰撞检测（每2步检测一次，提升FPS） =====
        if self.curriculum_progress >= 0.5 and self.collision_penalty > 0 and self.step_count % 2 == 0:
            try:
                contacts = p.getContactPoints(self.robot_id)
                if contacts:
                    reward -= self.collision_penalty
            except:
                pass

        if self.last_distance is not None:
            distance_change = self.last_distance - dist
            reward += distance_change * self.progress_reward_scale
        
        self.last_distance = dist

        if dist < self.reach_threshold:
            self.stable_count += 1
            reward += self.stable_reward
            if self.stable_count >= self.stable_threshold:
                reward += self.reach_reward
                terminated = True
            else:
                terminated = False
        else:
            self.stable_count = 0
            terminated = False

        truncated = self.step_count >= self.max_steps

        info = {
            "distance": dist,
            "success": terminated,
            "step": self.step_count,
            "target_pos": self.target_pos.copy(),
            "curriculum_progress": self.curriculum_progress
        }

        return obs, reward, terminated, truncated, info

    def _get_obs(self):
        states = p.getJointStates(self.robot_id, range(self.NUM_JOINTS))
        joint_pos = np.array([s[0] for s in states], dtype=np.float32)
        # 使用step()中缓存的ee_pos，避免重复调用getLinkState
        ee_pos = self._cached_ee_pos

        # ===== 传感器噪声 =====
        if self.curriculum_progress >= 0.1 and self.noise_gaussian_std > 0:
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
