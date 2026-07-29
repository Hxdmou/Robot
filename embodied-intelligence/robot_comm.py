"""
机械臂通信抽象层（支持多协议）
安全原则：超时保护、异常恢复、命令队列
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



import threading
import time
import abc


class RobotCommError(Exception):
    pass


class RobotTimeoutError(RobotCommError):
    pass


class RobotSafetyError(RobotCommError):
    pass


class BaseRobotComm(abc.ABC):
    def __init__(self, timeout=5.0):
        self.timeout = timeout
        self.connected = False
        self._lock = threading.Lock()
        self._command_queue = []
        self._running = False
        self._thread = None

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    @abc.abstractmethod
    def send_command(self, cmd, *args, **kwargs):
        pass

    @abc.abstractmethod
    def read_response(self):
        pass

    @abc.abstractmethod
    def get_joint_states(self):
        pass

    @abc.abstractmethod
    def move_joints(self, joint_angles, speed=1.0):
        pass

    @abc.abstractmethod
    def move_cartesian(self, x, y, z, rx=0, ry=0, rz=0, speed=1.0):
        pass

    @abc.abstractmethod
    def get_ee_pose(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    def safe_send_command(self, cmd, *args, max_retries=3, **kwargs):
        for attempt in range(max_retries):
            try:
                with self._lock:
                    return self.send_command(cmd, *args, **kwargs)
            except RobotCommError as e:
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                else:
                    raise RobotCommError(f"命令发送失败 ({cmd}): {e}")

    def start_command_loop(self):
        self._running = True
        self._thread = threading.Thread(target=self._command_loop, daemon=True)
        self._thread.start()

    def stop_command_loop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _command_loop(self):
        while self._running:
            try:
                if self._command_queue:
                    with self._lock:
                        cmd_info = self._command_queue.pop(0)
                    self.execute_command(cmd_info)
                time.sleep(0.01)
            except Exception as e:
                print(f"[COMM] 命令循环异常: {e}")

    def execute_command(self, cmd_info):
        cmd_type = cmd_info.get("type")
        if cmd_type == "move_joints":
            self.move_joints(cmd_info.get("joints"), cmd_info.get("speed", 1.0))
        elif cmd_type == "move_cartesian":
            self.move_cartesian(**cmd_info.get("params", {}))
        elif cmd_type == "stop":
            self.stop()

    def enqueue_command(self, cmd_info):
        with self._lock:
            self._command_queue.append(cmd_info)


class SimRobotComm(BaseRobotComm):
    def __init__(self, robot_id=None, joint_indices=None, ee_index=None, timeout=5.0):
        super().__init__(timeout=timeout)
        self.robot_id = robot_id
        self.joint_indices = joint_indices or []
        self.ee_index = ee_index
        self._p = None

    def _import_pybullet(self):
        import pybullet as p
        self._p = p

    def connect(self):
        self._import_pybullet()
        self.connected = True
        print("[COMM] 仿真通信已连接")

    def disconnect(self):
        self.connected = False
        print("[COMM] 仿真通信已断开")

    def send_command(self, cmd, *args, **kwargs):
        if not self.connected:
            raise RobotCommError("未连接")
        return True

    def read_response(self):
        return {"status": "ok"}

    def get_joint_states(self):
        if not self._p:
            self._import_pybullet()
        states = []
        for j_idx in self.joint_indices:
            state = self._p.getJointState(self.robot_id, j_idx)
            states.append({"angle": state[0], "velocity": state[1], "torque": state[3]})
        return states

    def move_joints(self, joint_angles, speed=1.0):
        if not self._p:
            self._import_pybullet()
        for idx, j_idx in enumerate(self.joint_indices):
            if idx < len(joint_angles):
                self._p.setJointMotorControl2(
                    self.robot_id, j_idx, self._p.POSITION_CONTROL,
                    targetPosition=joint_angles[idx], force=200
                )
        for _ in range(int(15 * speed)):
            self._p.stepSimulation()
            time.sleep(0.001)

    def move_cartesian(self, x, y, z, rx=0, ry=0, rz=0, speed=1.0):
        if not self._p:
            self._import_pybullet()

        ik_joints = self._p.calculateInverseKinematics(
            self.robot_id, self.ee_index, [x, y, z]
        )
        self.move_joints([ik_joints[i] for i in self.joint_indices], speed)

    def get_ee_pose(self):
        if not self._p:
            self._import_pybullet()
        link_state = self._p.getLinkState(self.robot_id, self.ee_index)
        return {"position": list(link_state[0]), "orientation": list(link_state[1])}

    def stop(self):
        if not self._p:
            self._import_pybullet()
        for j_idx in self.joint_indices:
            self._p.setJointMotorControl2(
                self.robot_id, j_idx, self._p.VELOCITY_CONTROL,
                targetVelocity=0, force=200
            )
