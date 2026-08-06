"""
领域随机化模块（Domain Randomization）
核心原理：在训练中随机化物理参数，让策略对真实世界的参数不确定性具备鲁棒性
支持：摩擦系数、关节阻尼、连杆质量、控制增益、重力、地面属性等
"""
# ============================================================================
# 免责声明与AI使用规范
# ============================================================================
# 本文件仅供技术研究与学习交流使用，不得用于任何非法用途。
#
# AI使用规范：
#   1. 使用本文件相关内容时须遵守所在地法律法规及伦理准则
#   2. 不得用于侵犯他人合法权益、危害网络安全、破坏公共秩序的活动
#   3. 涉及自动化决策的场景须确保人工复核机制与可解释性
#   4. 处理个人信息时须符合数据保护相关法规要求
#
# 风险提示：
#   本文件内容按"现状"提供，不保证绝对准确无误。
#   使用者须自行评估风险，因使用本文件导致的任何损失由使用者承担。
# ============================================================================



import pybullet as p
import numpy as np
import random
import time


class DomainRandomizer:
    def __init__(self, config=None):
        config = config or {}
        self.enabled = config.get("enabled", True)
        self.seed = config.get("seed", 42)
        self.randomize_on_reset = config.get("randomize_on_reset", True)
        
        self.friction_range = config.get("friction_range", [0.3, 0.8])
        self.damping_range = config.get("damping_range", [0.05, 0.2])
        self.mass_range = config.get("mass_range", [0.85, 1.15])
        self.control_gain_range = config.get("control_gain_range", [0.8, 1.2])
        self.gravity_range = config.get("gravity_range", [-9.9, -9.7])
        
        self.last_randomize_time = 0
        self.randomize_interval = config.get("randomize_interval", 30.0)
        
        self.current_params = {}
        
        np.random.seed(self.seed)
        random.seed(self.seed)
    
    def randomize(self, robot_id, joint_indices=None):
        """执行一次领域随机化"""
        if not self.enabled:
            return
        
        params = {}
        
        if self.friction_range:
            friction = np.random.uniform(*self.friction_range)
            params["friction"] = friction
            self._set_friction(robot_id, friction)
        
        if self.damping_range:
            damping = np.random.uniform(*self.damping_range)
            params["damping"] = damping
            self._set_joint_damping(robot_id, joint_indices, damping)
        
        if self.mass_range:
            mass_scale = np.random.uniform(*self.mass_range)
            params["mass_scale"] = mass_scale
            self._scale_link_mass(robot_id, mass_scale)
        
        if self.control_gain_range:
            gain_scale = np.random.uniform(*self.control_gain_range)
            params["control_gain_scale"] = gain_scale
        
        if self.gravity_range:
            gravity_z = np.random.uniform(*self.gravity_range)
            params["gravity_z"] = gravity_z
            p.setGravity(0, 0, gravity_z)
        
        self.current_params = params
        self.last_randomize_time = time.time()
        
        return params
    
    def _set_friction(self, robot_id, friction):
        """设置机器人所有连杆的摩擦系数"""
        num_joints = p.getNumJoints(robot_id)
        for i in range(num_joints):
            p.changeDynamics(robot_id, i, lateralFriction=friction, 
                            spinningFriction=friction * 0.5,
                            rollingFriction=friction * 0.3)
    
    def _set_joint_damping(self, robot_id, joint_indices, damping):
        """设置关节阻尼"""
        if joint_indices:
            for j_idx in joint_indices:
                p.changeDynamics(robot_id, j_idx, linearDamping=damping,
                                angularDamping=damping * 2)
        else:
            num_joints = p.getNumJoints(robot_id)
            for i in range(num_joints):
                p.changeDynamics(robot_id, i, linearDamping=damping,
                                angularDamping=damping * 2)
    
    def _scale_link_mass(self, robot_id, scale):
        """按比例缩放所有连杆质量"""
        num_joints = p.getNumJoints(robot_id)
        for i in range(num_joints):
            dynamics_info = p.getDynamicsInfo(robot_id, i)
            original_mass = dynamics_info[0]
            if original_mass > 0:
                p.changeDynamics(robot_id, i, mass=original_mass * scale)
    
    def should_randomize(self):
        """检查是否需要执行随机化"""
        if not self.enabled:
            return False
        if self.randomize_interval <= 0:
            return False
        return time.time() - self.last_randomize_time >= self.randomize_interval
    
    def get_current_params(self):
        """获取当前随机化参数"""
        return self.current_params.copy()
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def is_enabled(self):
        return self.enabled


class MassRandomizer:
    """质量随机化器 - 独立控制连杆质量变化"""
    
    def __init__(self, config=None):
        config = config or {}
        self.enabled = config.get("enabled", True)
        self.min_mass_ratio = config.get("min_mass_ratio", 0.7)
        self.max_mass_ratio = config.get("max_mass_ratio", 1.5)
        self.target_link_indices = config.get("target_link_indices", [])
    
    def randomize_mass(self, robot_id):
        if not self.enabled:
            return {}
        
        changes = {}
        if self.target_link_indices:
            indices = self.target_link_indices
        else:
            indices = range(p.getNumJoints(robot_id))
        
        for i in indices:
            dynamics_info = p.getDynamicsInfo(robot_id, i)
            original_mass = dynamics_info[0]
            if original_mass > 0:
                new_mass = original_mass * np.random.uniform(
                    self.min_mass_ratio, self.max_mass_ratio
                )
                p.changeDynamics(robot_id, i, mass=new_mass)
                changes[f"link_{i}"] = {"original": original_mass, "new": new_mass}
        
        return changes


class FrictionRandomizer:
    """摩擦随机化器 - 独立控制不同接触面的摩擦系数"""
    
    def __init__(self, config=None):
        config = config or {}
        self.enabled = config.get("enabled", True)
        self.min_friction = config.get("min_friction", 0.2)
        self.max_friction = config.get("max_friction", 1.0)
        self.min_spinning_friction = config.get("min_spinning_friction", 0.05)
        self.max_spinning_friction = config.get("max_spinning_friction", 0.5)
    
    def randomize_friction(self, robot_id):
        if not self.enabled:
            return {}
        
        num_joints = p.getNumJoints(robot_id)
        changes = {}
        
        for i in range(num_joints):
            lateral_friction = np.random.uniform(self.min_friction, self.max_friction)
            spinning_friction = np.random.uniform(self.min_spinning_friction, self.max_spinning_friction)
            rolling_friction = spinning_friction * 0.5
            
            p.changeDynamics(robot_id, i, 
                            lateralFriction=lateral_friction,
                            spinningFriction=spinning_friction,
                            rollingFriction=rolling_friction)
            
            changes[f"link_{i}"] = {
                "lateral_friction": lateral_friction,
                "spinning_friction": spinning_friction
            }
        
        return changes


class PhysicsDistortion:
    """物理失真模拟 - 模拟真实世界的物理参数偏差"""
    
    def __init__(self, config=None):
        config = config or {}
        self.enabled = config.get("enabled", True)
        self.distortion_prob = config.get("distortion_prob", 0.3)
        self.max_distortion = config.get("max_distortion", 0.2)
    
    def apply_distortion(self, robot_id, joint_indices):
        """随机对某些关节施加物理参数失真"""
        if not self.enabled:
            return {}
        
        changes = {}
        for j_idx in joint_indices:
            if np.random.random() < self.distortion_prob:
                dynamics_info = p.getDynamicsInfo(robot_id, j_idx)
                original_mass = dynamics_info[0]
                original_friction = dynamics_info[1]
                
                mass_distortion = 1 + np.random.uniform(-self.max_distortion, self.max_distortion)
                friction_distortion = 1 + np.random.uniform(-self.max_distortion, self.max_distortion)
                
                p.changeDynamics(robot_id, j_idx, 
                                mass=original_mass * mass_distortion,
                                lateralFriction=original_friction * friction_distortion)
                
                changes[f"joint_{j_idx}"] = {
                    "mass_distortion": mass_distortion,
                    "friction_distortion": friction_distortion
                }
        
        return changes


class DomainRandomizationSystem:
    """领域随机化系统 - 整合所有随机化器"""
    
    def __init__(self, config=None):
        config = config or {}
        
        self.domain_randomizer = DomainRandomizer(config.get("domain_randomizer", {}))
        self.mass_randomizer = MassRandomizer(config.get("mass_randomizer", {}))
        self.friction_randomizer = FrictionRandomizer(config.get("friction_randomizer", {}))
        self.physics_distortion = PhysicsDistortion(config.get("physics_distortion", {}))
        
        self.enabled = config.get("enabled", True)
        self.randomize_on_reset = config.get("randomize_on_reset", True)
        self.stats = {
            "randomize_count": 0,
            "mass_changes": 0,
            "friction_changes": 0,
            "distortion_changes": 0
        }
    
    def randomize_all(self, robot_id, joint_indices):
        """执行所有随机化"""
        if not self.enabled:
            return {}
        
        results = {}
        
        if self.domain_randomizer.is_enabled():
            domain_params = self.domain_randomizer.randomize(robot_id, joint_indices)
            if domain_params:
                results["domain_randomizer"] = domain_params
                self.stats["randomize_count"] += 1
        
        if self.mass_randomizer.is_enabled():
            mass_changes = self.mass_randomizer.randomize_mass(robot_id)
            if mass_changes:
                results["mass_randomizer"] = mass_changes
                self.stats["mass_changes"] += len(mass_changes)
        
        if self.friction_randomizer.is_enabled():
            friction_changes = self.friction_randomizer.randomize_friction(robot_id)
            if friction_changes:
                results["friction_randomizer"] = friction_changes
                self.stats["friction_changes"] += len(friction_changes)
        
        if self.physics_distortion.is_enabled():
            distortion_changes = self.physics_distortion.apply_distortion(robot_id, joint_indices)
            if distortion_changes:
                results["physics_distortion"] = distortion_changes
                self.stats["distortion_changes"] += len(distortion_changes)
        
        return results
    
    def check_and_randomize(self, robot_id, joint_indices):
        """检查并执行周期性随机化"""
        if self.domain_randomizer.should_randomize():
            return self.randomize_all(robot_id, joint_indices)
        return {}
    
    def reset(self):
        """重置随机化状态"""
        self.domain_randomizer.last_randomize_time = 0
    
    def get_stats(self):
        """获取随机化统计"""
        return self.stats.copy()
    
    def enable(self):
        self.enabled = True
        self.domain_randomizer.enable()
        self.mass_randomizer.enable()
        self.friction_randomizer.enable()
        self.physics_distortion.enable()
    
    def disable(self):
        self.enabled = False
        self.domain_randomizer.disable()
        self.mass_randomizer.disable()
        self.friction_randomizer.disable()
        self.physics_distortion.disable()
    
    def is_enabled(self):
        return self.enabled