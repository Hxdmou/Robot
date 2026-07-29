"""
实时监控模块（轻量级）
安全原则：低CPU占用，定时清理，无阻塞
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



import time
import threading
import psutil

from sensor_noise import SensorNoiseSystem
from noise_config import SENSOR_NOISE_CONFIG

class ResourceMonitor:
    def __init__(self, interval=1.0):
        self.interval = interval
        self.running = False
        self.thread = None
        self.cpu_history = []
        self.mem_history = []
        self.max_history = 100

    def _monitor_loop(self):
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=0.1)
                mem = psutil.virtual_memory().percent

                self.cpu_history.append((time.time(), cpu))
                self.mem_history.append((time.time(), mem))

                if len(self.cpu_history) > self.max_history:
                    self.cpu_history.pop(0)
                if len(self.mem_history) > self.max_history:
                    self.mem_history.pop(0)

                if cpu > 90 or mem > 90:
                    print(f"[WARNING] 资源占用过高 - CPU: {cpu}%, MEM: {mem}%")

                time.sleep(self.interval)
            except Exception as e:
                print(f"[MONITOR] 监控异常: {e}")
                time.sleep(self.interval)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            print("[MONITOR] 资源监控已启动")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[MONITOR] 资源监控已停止")

    def get_stats(self):
        if self.cpu_history and self.mem_history:
            cpu_avg = sum(v[1] for v in self.cpu_history) / len(self.cpu_history)
            mem_avg = sum(v[1] for v in self.mem_history) / len(self.mem_history)
            return {
                "cpu_current": self.cpu_history[-1][1] if self.cpu_history else 0,
                "cpu_avg": cpu_avg,
                "mem_current": self.mem_history[-1][1] if self.mem_history else 0,
                "mem_avg": mem_avg,
            }
        return {"cpu_current": 0, "cpu_avg": 0, "mem_current": 0, "mem_avg": 0}

class RobotMonitor:
    def __init__(self, robot_id, ee_index, joint_indices):
        self.robot_id = robot_id
        self.ee_index = ee_index
        self.joint_indices = joint_indices
        self.error_history = []
        self.max_history = 100
        self.noise_system = SensorNoiseSystem(SENSOR_NOISE_CONFIG)

    def get_joint_states(self):
        states = []
        for j_idx in self.joint_indices:
            state = p.getJointState(self.robot_id, j_idx)
            states.append({"angle": state[0], "velocity": state[1], "torque": state[3]})
        return self.noise_system.apply_joint_states_noise(states)

    def get_ee_position(self):
        link_state = p.getLinkState(self.robot_id, self.ee_index)
        pose = {
            "position": link_state[0],
            "orientation": link_state[1]
        }
        noisy_pose = self.noise_system.apply_ee_pose_noise(pose)
        return noisy_pose["position"]

    def log_error(self, error):
        self.error_history.append((time.time(), error))
        if len(self.error_history) > self.max_history:
            self.error_history.pop(0)

    def get_error_stats(self):
        if self.error_history:
            avg_error = sum(v[1] for v in self.error_history) / len(self.error_history)
            max_error = max(v[1] for v in self.error_history)
            return {"avg_error_mm": avg_error * 1000, "max_error_mm": max_error * 1000}
        return {"avg_error_mm": 0, "max_error_mm": 0}
