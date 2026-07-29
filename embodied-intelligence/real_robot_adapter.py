"""
真实机械臂适配器
提供统一的机器人控制接口，支持仿真和真实模式切换
安全原则：模式隔离、异常保护、状态同步
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
import math

from robot_comm import SimRobotComm
from panda_comm import PandaComm
from robot_safety import SafetyController, EmergencyStopMonitor


class RobotAdapter:
    def __init__(self, mode="sim", config=None):
        self.mode = mode
        self.config = config or {}
        self.comm = None
        self.safety = SafetyController()
        self.emergency_stop = None
        self._initialized = False

    def initialize(self):
        if self.mode == "real":
            host = self.config.get("host", "192.168.1.1")
            port = self.config.get("port", 8080)
            self.comm = PandaComm(host=host, port=port)
        else:
            self.comm = SimRobotComm()

        try:
            self.comm.connect()
            self._initialized = True
            print(f"[ADAPTER] 机器人适配器初始化完成 (模式: {self.mode})")

            if "joint_limits" in self.config:
                self.safety.set_joint_limits(
                    self.config.get("joint_indices", []),
                    self.config.get("joint_limits", {}).get("lower", []),
                    self.config.get("joint_limits", {}).get("upper", [])
                )

            if self.mode == "real":
                self.emergency_stop = EmergencyStopMonitor(self.comm)
                self.emergency_stop.start()

            return True
        except Exception as e:
            print(f"[ADAPTER] 初始化失败: {e}")
            if self.comm:
                self.comm.disconnect()
            return False

    def shutdown(self):
        if self.emergency_stop:
            self.emergency_stop.stop()

        if self.comm:
            self.comm.disconnect()

        self._initialized = False
        print("[ADAPTER] 机器人适配器已关闭")

    def update_sim_params(self, robot_id, joint_indices, ee_index):
        if self.mode == "sim" and isinstance(self.comm, SimRobotComm):
            self.comm.robot_id = robot_id
            self.comm.joint_indices = joint_indices
            self.comm.ee_index = ee_index

    def get_joint_states(self):
        if not self._initialized:
            return []
        return self.comm.get_joint_states()

    def move_joints(self, joint_angles, speed=1.0):
        if not self._initialized:
            raise RuntimeError("适配器未初始化")

        if self.emergency_stop and self.emergency_stop.is_emergency_stop():
            raise RuntimeError("紧急停止中")

        try:
            self.safety.check_joint_limits(joint_angles, self.config.get("joint_indices", []))
            self.comm.move_joints(joint_angles, speed)
            return True
        except Exception as e:
            print(f"[ADAPTER] 移动关节失败: {e}")
            self.comm.stop()
            return False

    def move_cartesian(self, x, y, z, rx=0, ry=0, rz=0, speed=1.0):
        if not self._initialized:
            raise RuntimeError("适配器未初始化")

        if self.emergency_stop and self.emergency_stop.is_emergency_stop():
            raise RuntimeError("紧急停止中")

        try:
            self.safety.check_cartesian_limits(x, y, z)
            self.comm.move_cartesian(x, y, z, rx, ry, rz, speed)
            return True
        except Exception as e:
            print(f"[ADAPTER] 笛卡尔移动失败: {e}")
            self.comm.stop()
            return False

    def get_ee_pose(self):
        if not self._initialized:
            return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}
        return self.comm.get_ee_pose()

    def stop(self):
        if self.comm:
            self.comm.stop()

    def converge_to_target(self, target_pos, max_iter=10, threshold=0.001):
        if not self._initialized:
            raise RuntimeError("适配器未初始化")

        for _ in range(max_iter):
            current_pose = self.get_ee_pose()
            current_pos = current_pose["position"]
            error = math.sqrt(
                (current_pos[0] - target_pos[0])**2 +
                (current_pos[1] - target_pos[1])**2 +
                (current_pos[2] - target_pos[2])**2
            )

            if error < threshold:
                return error

            self.move_cartesian(*target_pos, speed=0.5)
            time.sleep(0.1)

        return error

    def is_connected(self):
        return self.comm and self.comm.connected

    def set_safety_enabled(self, enabled):
        if enabled:
            self.safety.enable()
        else:
            self.safety.disable()
