"""
增强版机械臂到达环境 - 继承自优化版环境
集成仿真增强模块：
1. 领域随机化 - 训练中随机化物理参数
2. 通信延迟仿真 - 模拟控制延迟和状态读取延迟
3. 执行器动力学 - 模拟真实电机限制
4. 外部扰动仿真 - 模拟真实世界干扰
5. 传感器噪声 - 模拟传感器误差
"""

import numpy as np
import pybullet as p
import gc

from robot_reach_env_optimized import RobotReachEnvOptimized
from domain_randomization import DomainRandomizationSystem
from latency_simulator import LatencySystem
from actuator_dynamics import ActuatorSystem
from disturbance_simulator import DisturbanceSystem
from sensor_noise import SensorNoiseSystem


class RobotReachEnvEnhanced(RobotReachEnvOptimized):
    """增强版机械臂到达环境（集成仿真增强模块）"""

    def __init__(self, render_mode=None, max_steps=500, use_weighted_sampling=True, 
                 dynamic_target=False, enable_enhancement=True):
        super().__init__(render_mode=render_mode, max_steps=max_steps, 
                         use_weighted_sampling=use_weighted_sampling, 
                         dynamic_target=dynamic_target)
        
        self.enable_enhancement = enable_enhancement
        
        # 加速优化：减少物理模拟sub_steps（从4减少到2）
        self.sub_steps = 2
        
        # 初始化仿真增强模块
        if self.enable_enhancement:
            self._init_enhancement_modules()

    def _init_enhancement_modules(self):
        """初始化仿真增强模块（优化版：只开启关键模块）"""
        
        # 领域随机化 - 关闭（最耗性能）
        self.domain_randomizer = DomainRandomizationSystem({
            "enabled": False,
            "domain_randomizer": {"enabled": False},
            "mass_randomizer": {"enabled": False},
            "friction_randomizer": {"enabled": False},
            "physics_distortion": {"enabled": False}
        })
        
        # 通信延迟 - 关闭（性能开销太大，后续优化后开启）
        self.latency_system = LatencySystem({
            "enabled": False,
            "latency_simulator": {"enabled": False},
            "control_delay": {"enabled": False},
            "state_delay": {"enabled": False},
            "network_latency": {"enabled": False}
        })
        
        # 执行器动力学 - 开启（对泛化最关键）
        self.actuator_system = ActuatorSystem({
            "enabled": True,
            "actuator_dynamics": {
                "enabled": True,
                "max_torque": 50.0,
                "max_velocity": 3.0,
                "max_acceleration": 15.0,
                "dead_zone": 0.0005
            },
            "motor_model": {"enabled": False},
            "joint_constraint": {"enabled": True, "max_force": 240.0}
        })
        
        # 外部扰动 - 关闭（最耗性能）
        self.disturbance_system = DisturbanceSystem({
            "enabled": False,
            "disturbance_simulator": {"enabled": False},
            "impact_simulator": {"enabled": False},
            "load_simulator": {"enabled": False}
        })
        
        # 传感器噪声 - 开启（对泛化最关键）
        self.noise_system = SensorNoiseSystem({
            "enabled": True,
            "joint_gaussian_std": 0.0005,
            "joint_quantization_res": 0.001,
            "joint_drift_rate": 0.0001,
            "ee_gaussian_std": 0.0001,
            "ee_quantization_res": 0.0001,
            "ee_drift_rate": 0.000001
        })
        
        print("[ENHANCEMENT] 仿真增强模块已初始化（传感器噪声+执行器动力学）")

    def reset(self, seed=None, options=None):
        obs, info = super().reset(seed=seed, options=options)
        
        # 重置增强模块状态
        if self.enable_enhancement:
            self.domain_randomizer.reset()
            self.disturbance_system.reset()
            self.actuator_system.reset()
        
        return obs, info

    def step(self, action):
        # 应用通信延迟
        if self.enable_enhancement and self.latency_system.is_enabled():
            self.latency_system.apply_control_latency()

        # 获取当前状态
        states = p.getJointStates(self.robot_id, range(7))
        current_positions = np.array([s[0] for s in states])
        current_velocities = np.array([s[1] for s in states])

        # 应用执行器动力学限制
        if self.enable_enhancement and self.actuator_system.is_enabled():
            limited_commands = []
            for i in range(7):
                limited_cmd, _ = self.actuator_system.actuator_dynamics.apply_all_limits(
                    i, action[i], current_velocities[i], 1/240.0
                )
                limited_commands.append(limited_cmd)
            action = np.array(limited_commands)

        # 调用父类step
        obs, reward, terminated, truncated, info = super().step(action)

        # 应用外部扰动（在step之后，确保物理模拟已经执行）
        if self.enable_enhancement and self.disturbance_system.is_enabled():
            self.disturbance_system.apply_disturbances(self.robot_id, 6)

        # 应用领域随机化（周期性）
        if self.enable_enhancement and self.domain_randomizer.is_enabled():
            self.domain_randomizer.check_and_randomize(self.robot_id, list(range(7)))

        return obs, reward, terminated, truncated, info

    def _get_obs(self):
        states = p.getJointStates(self.robot_id, range(7))
        joint_pos = np.array([s[0] for s in states], dtype=np.float32)
        joint_vel = np.array([s[1] for s in states], dtype=np.float32)
        ee_pos = np.array(p.getLinkState(self.robot_id, 6)[0], dtype=np.float32)
        
        # 应用传感器噪声
        if self.enable_enhancement and self.noise_system.is_enabled():
            joint_pos = np.array(self.noise_system.apply_joint_noise(joint_pos.tolist()), dtype=np.float32)
            ee_pos = np.array(self.noise_system.apply_ee_noise(ee_pos.tolist()), dtype=np.float32)

        return np.concatenate([
            joint_pos, joint_vel, ee_pos, self.target_pos
        ], dtype=np.float32)

    def close(self):
        super().close()
        gc.collect()

    def __del__(self):
        self.close()