"""
外部扰动仿真模块（External Disturbance Simulation）
核心原理：模拟真实世界中的各种扰动，包括负载变化、外部冲击力、随机干扰
支持：周期性外力、随机冲击力、负载变化、地面振动、传感器噪声叠加
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


class DisturbanceSimulator:
    """外部扰动模拟器"""
    
    def __init__(self, config=None):
        config = config or {}
        
        self.enabled = config.get("enabled", True)
        
        # 周期性外力
        self.periodic_force_enabled = config.get("periodic_force_enabled", True)
        self.periodic_force_magnitude = config.get("periodic_force_magnitude", 5.0)
        self.periodic_force_period = config.get("periodic_force_period", 2.0)
        
        # 随机冲击力
        self.impulse_enabled = config.get("impulse_enabled", True)
        self.impulse_probability = config.get("impulse_probability", 0.02)
        self.impulse_magnitude_range = config.get("impulse_magnitude_range", [1, 10])
        
        # 负载变化
        self.load_change_enabled = config.get("load_change_enabled", True)
        self.load_change_probability = config.get("load_change_probability", 0.01)
        self.load_mass_range = config.get("load_mass_range", [0.1, 2.0])
        
        # 地面振动
        self.vibration_enabled = config.get("vibration_enabled", True)
        self.vibration_magnitude = config.get("vibration_magnitude", 0.01)
        self.vibration_frequency = config.get("vibration_frequency", 50.0)
        
        # 当前负载
        self.current_load_mass = 0.0
        
        self.stats = {
            "total_disturbances": 0,
            "periodic_forces_applied": 0,
            "impulses_applied": 0,
            "load_changes": 0,
            "total_impulse_magnitude": 0,
            "max_load_mass": 0
        }
        
        self._last_disturbance_time = 0
    
    def apply_periodic_force(self, robot_id, ee_index, current_time):
        """应用周期性外力"""
        if not self.enabled or not self.periodic_force_enabled:
            return None
        
        force = [
            self.periodic_force_magnitude * np.sin(2 * np.pi * current_time / self.periodic_force_period),
            self.periodic_force_magnitude * np.cos(2 * np.pi * current_time / self.periodic_force_period),
            self.periodic_force_magnitude * 0.5 * np.sin(4 * np.pi * current_time / self.periodic_force_period)
        ]
        
        p.applyExternalForce(
            objectUniqueId=robot_id,
            linkIndex=ee_index,
            forceObj=force,
            posObj=[0, 0, 0],
            flags=p.WORLD_FRAME
        )
        
        self.stats["periodic_forces_applied"] += 1
        self.stats["total_disturbances"] += 1
        
        return {"type": "periodic", "force": force}
    
    def apply_random_impulse(self, robot_id, ee_index):
        """应用随机冲击力"""
        if not self.enabled or not self.impulse_enabled:
            return None
        
        if random.random() < self.impulse_probability:
            magnitude = random.uniform(*self.impulse_magnitude_range)
            
            direction = np.random.randn(3)
            direction = direction / np.linalg.norm(direction)
            
            impulse = direction * magnitude
            
            p.applyExternalImpulse(
                objectUniqueId=robot_id,
                linkIndex=ee_index,
                impulseObj=impulse,
                posObj=[0, 0, 0],
                flags=p.WORLD_FRAME
            )
            
            self.stats["impulses_applied"] += 1
            self.stats["total_disturbances"] += 1
            self.stats["total_impulse_magnitude"] += magnitude
            
            return {"type": "impulse", "impulse": impulse.tolist()}
        
        return None
    
    def apply_load_change(self, robot_id, ee_index):
        """应用负载变化"""
        if not self.enabled or not self.load_change_enabled:
            return None
        
        if random.random() < self.load_change_probability:
            new_load = random.uniform(*self.load_mass_range)
            
            # 移除旧负载
            if self.current_load_mass > 0:
                p.changeDynamics(robot_id, ee_index, mass=1.0)
            
            # 添加新负载
            self.current_load_mass = new_load
            p.changeDynamics(robot_id, ee_index, mass=1.0 + new_load)
            
            self.stats["load_changes"] += 1
            self.stats["total_disturbances"] += 1
            self.stats["max_load_mass"] = max(self.stats["max_load_mass"], new_load)
            
            return {"type": "load_change", "mass": new_load}
        
        return None
    
    def apply_vibration(self, robot_id):
        """应用地面振动"""
        if not self.enabled or not self.vibration_enabled:
            return None
        
        num_joints = p.getNumJoints(robot_id)
        current_time = time.time()
        
        for i in range(num_joints):
            # 在关节处添加微小振动
            vibration = [
                self.vibration_magnitude * np.sin(2 * np.pi * self.vibration_frequency * current_time + i),
                self.vibration_magnitude * np.cos(2 * np.pi * self.vibration_frequency * current_time + i),
                0
            ]
            
            p.applyExternalForce(
                objectUniqueId=robot_id,
                linkIndex=i,
                forceObj=vibration,
                posObj=[0, 0, 0],
                flags=p.WORLD_FRAME
            )
        
        return {"type": "vibration", "magnitude": self.vibration_magnitude}
    
    def apply_all_disturbances(self, robot_id, ee_index, current_time=None):
        """应用所有扰动"""
        if not self.enabled:
            return []
        
        if current_time is None:
            current_time = time.time()
        
        disturbances = []
        
        # 周期性外力
        result = self.apply_periodic_force(robot_id, ee_index, current_time)
        if result:
            disturbances.append(result)
        
        # 随机冲击力
        result = self.apply_random_impulse(robot_id, ee_index)
        if result:
            disturbances.append(result)
        
        # 负载变化
        result = self.apply_load_change(robot_id, ee_index)
        if result:
            disturbances.append(result)
        
        # 地面振动
        result = self.apply_vibration(robot_id)
        if result:
            disturbances.append(result)
        
        return disturbances
    
    def reset_load(self):
        """重置负载"""
        self.current_load_mass = 0.0
    
    def get_stats(self):
        """获取扰动统计"""
        return self.stats.copy()
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def is_enabled(self):
        return self.enabled


class ImpactSimulator:
    """冲击力模拟器 - 模拟碰撞和冲击"""
    
    def __init__(self, config=None):
        config = config or {}
        
        self.enabled = config.get("enabled", True)
        self.impact_probability = config.get("impact_probability", 0.01)
        self.min_impact_force = config.get("min_impact_force", 5.0)
        self.max_impact_force = config.get("max_impact_force", 50.0)
        self.impact_duration = config.get("impact_duration", 0.1)
        
        self.stats = {
            "impacts_applied": 0,
            "total_impact_force": 0,
            "max_impact_force": 0
        }
    
    def apply_impact(self, robot_id, ee_index):
        """应用冲击力"""
        if not self.enabled:
            return None
        
        if random.random() < self.impact_probability:
            force_magnitude = random.uniform(self.min_impact_force, self.max_impact_force)
            
            direction = np.random.randn(3)
            direction[2] = abs(direction[2])
            direction = direction / np.linalg.norm(direction)
            
            force = direction * force_magnitude
            
            # 在短时间内持续施加力
            for _ in range(int(self.impact_duration / 0.001)):
                p.applyExternalForce(
                    objectUniqueId=robot_id,
                    linkIndex=ee_index,
                    forceObj=force,
                    posObj=[0, 0, 0],
                    flags=p.WORLD_FRAME
                )
                p.stepSimulation()
            
            self.stats["impacts_applied"] += 1
            self.stats["total_impact_force"] += force_magnitude
            self.stats["max_impact_force"] = max(self.stats["max_impact_force"], force_magnitude)
            
            return {"type": "impact", "force": force.tolist(), "duration": self.impact_duration}
        
        return None
    
    def get_stats(self):
        """获取冲击力统计"""
        return self.stats.copy()
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def is_enabled(self):
        return self.enabled


class LoadSimulator:
    """负载模拟器 - 模拟末端执行器负载变化"""
    
    def __init__(self, config=None):
        config = config or {}
        
        self.enabled = config.get("enabled", True)
        self.min_load = config.get("min_load", 0)
        self.max_load = config.get("max_load", 3.0)
        self.load_change_probability = config.get("load_change_probability", 0.005)
        self.load_smoothness = config.get("load_smoothness", 0.1)
        
        self.current_load = 0.0
        self.target_load = 0.0
        
        self.stats = {
            "load_changes": 0,
            "max_load_applied": 0,
            "avg_load": 0,
            "load_history": []
        }
    
    def update_load(self, robot_id, ee_index):
        """更新负载"""
        if not self.enabled:
            return None
        
        # 随机改变目标负载
        if random.random() < self.load_change_probability:
            self.target_load = random.uniform(self.min_load, self.max_load)
            self.stats["load_changes"] += 1
            self.stats["max_load_applied"] = max(self.stats["max_load_applied"], self.target_load)
        
        # 平滑过渡
        self.current_load += (self.target_load - self.current_load) * self.load_smoothness
        
        # 更新末端执行器质量
        base_mass = 1.0
        p.changeDynamics(robot_id, ee_index, mass=base_mass + self.current_load)
        
        # 记录统计
        self.stats["load_history"].append(self.current_load)
        if len(self.stats["load_history"]) > 100:
            self.stats["load_history"].pop(0)
        
        if self.stats["load_history"]:
            self.stats["avg_load"] = sum(self.stats["load_history"]) / len(self.stats["load_history"])
        
        return {"type": "load", "mass": self.current_load}
    
    def reset(self):
        """重置负载"""
        self.current_load = 0.0
        self.target_load = 0.0
    
    def get_stats(self):
        """获取负载统计"""
        return self.stats.copy()
    
    def enable(self):
        self.enabled = True
    
    def disable(self):
        self.enabled = False
    
    def is_enabled(self):
        return self.enabled


class DisturbanceSystem:
    """扰动系统 - 整合所有扰动模块"""
    
    def __init__(self, config=None):
        config = config or {}
        
        self.disturbance_simulator = DisturbanceSimulator(config.get("disturbance_simulator", {}))
        self.impact_simulator = ImpactSimulator(config.get("impact_simulator", {}))
        self.load_simulator = LoadSimulator(config.get("load_simulator", {}))
        
        self.enabled = config.get("enabled", True)
    
    def apply_disturbances(self, robot_id, ee_index, current_time=None):
        """应用所有扰动"""
        if not self.enabled:
            return []
        
        disturbances = []
        
        # 基础扰动
        result = self.disturbance_simulator.apply_all_disturbances(robot_id, ee_index, current_time)
        if result:
            disturbances.extend(result)
        
        # 冲击力
        result = self.impact_simulator.apply_impact(robot_id, ee_index)
        if result:
            disturbances.append(result)
        
        # 负载变化
        result = self.load_simulator.update_load(robot_id, ee_index)
        if result:
            disturbances.append(result)
        
        return disturbances
    
    def get_stats(self):
        """获取扰动统计"""
        return {
            "disturbance_simulator": self.disturbance_simulator.get_stats(),
            "impact_simulator": self.impact_simulator.get_stats(),
            "load_simulator": self.load_simulator.get_stats()
        }
    
    def reset(self):
        """重置扰动状态"""
        self.disturbance_simulator.reset_load()
        self.load_simulator.reset()
    
    def enable(self):
        self.enabled = True
        self.disturbance_simulator.enable()
        self.impact_simulator.enable()
        self.load_simulator.enable()
    
    def disable(self):
        self.enabled = False
        self.disturbance_simulator.disable()
        self.impact_simulator.disable()
        self.load_simulator.disable()
    
    def is_enabled(self):
        return self.enabled