"""
传感器噪声模型模块（轻量级）
安全原则：低资源占用、可配置、可关闭
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



import math
import random
import time


class GaussianNoise:
    def __init__(self, mean=0.0, std=0.01):
        self.mean = mean
        self.std = std

    def add(self, value):
        return value + random.gauss(self.mean, self.std)

    def add_to_vector(self, vector):
        return [self.add(v) for v in vector]


class QuantizationNoise:
    def __init__(self, resolution=0.001):
        self.resolution = resolution

    def add(self, value):
        return round(value / self.resolution) * self.resolution

    def add_to_vector(self, vector):
        return [self.add(v) for v in vector]


class DriftNoise:
    def __init__(self, rate=0.0001):
        self.rate = rate
        self.drift = 0.0
        self.last_time = time.time()

    def add(self, value):
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        self.drift += self.rate * delta_time * random.uniform(-1, 1)
        self.drift = max(-0.01, min(0.01, self.drift))
        return value + self.drift

    def add_to_vector(self, vector):
        return [self.add(v) for v in vector]

    def reset(self):
        self.drift = 0.0
        self.last_time = time.time()


class JitterNoise:
    def __init__(self, max_jitter=0.005):
        self.max_jitter = max_jitter

    def add(self, value):
        return value + random.uniform(-self.max_jitter, self.max_jitter)

    def add_to_vector(self, vector):
        return [self.add(v) for v in vector]


class JointAngleNoise:
    def __init__(self, gaussian_std=0.001, quantization_res=0.001, drift_rate=0.00001):
        self.gaussian = GaussianNoise(std=gaussian_std)
        self.quantization = QuantizationNoise(resolution=quantization_res)
        self.drift = DriftNoise(rate=drift_rate)

    def add(self, angle):
        angle = self.gaussian.add(angle)
        angle = self.quantization.add(angle)
        angle = self.drift.add(angle)
        return angle

    def add_to_vector(self, angles):
        return [self.add(a) for a in angles]

    def reset(self):
        self.drift.reset()


class EEPositionNoise:
    def __init__(self, gaussian_std=0.0001, quantization_res=0.0001, drift_rate=0.000001):
        self.gaussian = GaussianNoise(std=gaussian_std)
        self.quantization = QuantizationNoise(resolution=quantization_res)
        self.drift = DriftNoise(rate=drift_rate)

    def add(self, position):
        pos = self.gaussian.add_to_vector(position)
        pos = self.quantization.add_to_vector(pos)
        pos = self.drift.add_to_vector(pos)
        return pos

    def reset(self):
        self.drift.reset()


class ForceTorqueNoise:
    def __init__(self, gaussian_std=0.1, drift_rate=0.0001, max_drift=0.5):
        self.gaussian = GaussianNoise(std=gaussian_std)
        self.drift = DriftNoise(rate=drift_rate)
        self.max_drift = max_drift

    def add(self, force):
        force = self.gaussian.add(force)
        force = self.drift.add(force)
        force = max(-self.max_drift, min(self.max_drift, force))
        return force

    def add_to_vector(self, forces):
        return [self.add(f) for f in forces]

    def reset(self):
        self.drift.reset()


class VelocityNoise:
    def __init__(self, gaussian_std=0.001, quantization_res=0.001):
        self.gaussian = GaussianNoise(std=gaussian_std)
        self.quantization = QuantizationNoise(resolution=quantization_res)

    def add(self, velocity):
        velocity = self.gaussian.add(velocity)
        velocity = self.quantization.add(velocity)
        return velocity

    def add_to_vector(self, velocities):
        return [self.add(v) for v in velocities]


class SensorNoiseSystem:
    def __init__(self, config=None):
        config = config or {}

        self.joint_noise = JointAngleNoise(
            gaussian_std=config.get("joint_gaussian_std", 0.001),
            quantization_res=config.get("joint_quantization_res", 0.001),
            drift_rate=config.get("joint_drift_rate", 0.00001)
        )

        self.ee_noise = EEPositionNoise(
            gaussian_std=config.get("ee_gaussian_std", 0.0001),
            quantization_res=config.get("ee_quantization_res", 0.0001),
            drift_rate=config.get("ee_drift_rate", 0.000001)
        )

        self.force_noise = ForceTorqueNoise(
            gaussian_std=config.get("force_gaussian_std", 0.1),
            drift_rate=config.get("force_drift_rate", 0.0001),
            max_drift=config.get("force_max_drift", 0.5)
        )

        self.velocity_noise = VelocityNoise(
            gaussian_std=config.get("velocity_gaussian_std", 0.001),
            quantization_res=config.get("velocity_quantization_res", 0.001)
        )

        self.enabled = config.get("enabled", True)

    def apply_joint_noise(self, angles):
        if not self.enabled:
            return angles
        return self.joint_noise.add_to_vector(angles)

    def apply_ee_noise(self, position):
        if not self.enabled:
            return position
        return self.ee_noise.add(position)

    def apply_force_noise(self, forces):
        if not self.enabled:
            return forces
        return self.force_noise.add_to_vector(forces)

    def apply_velocity_noise(self, velocities):
        if not self.enabled:
            return velocities
        return self.velocity_noise.add_to_vector(velocities)

    def apply_joint_states_noise(self, joint_states):
        if not self.enabled:
            return joint_states

        noisy_states = []
        for state in joint_states:
            noisy_state = {
                "angle": self.joint_noise.add(state.get("angle", 0)),
                "velocity": self.velocity_noise.add(state.get("velocity", 0)),
                "torque": self.force_noise.add(state.get("torque", 0))
            }
            noisy_states.append(noisy_state)
        return noisy_states

    def apply_ee_pose_noise(self, pose):
        if not self.enabled:
            return pose

        return {
            "position": self.ee_noise.add(pose.get("position", [0, 0, 0])),
            "orientation": pose.get("orientation", [0, 0, 0, 1])
        }

    def reset_all(self):
        self.joint_noise.reset()
        self.ee_noise.reset()
        self.force_noise.reset()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled
