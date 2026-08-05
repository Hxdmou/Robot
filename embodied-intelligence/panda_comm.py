"""
Franka Panda 机械臂通信模块
支持 Franka Control Interface (FCI) 协议
安全原则：速度限制、力限制、异常恢复
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



import socket
import json
import time
import threading

from robot_comm import BaseRobotComm, RobotCommError, RobotTimeoutError


class PandaComm(BaseRobotComm):
    def __init__(self, host="127.0.0.1", port=8080, timeout=5.0):
        super().__init__(timeout=timeout)
        self.host = host
        self.port = port
        self.socket = None
        self._recv_buffer = ""
        self._last_state = None
        self._state_thread = None
        self._state_running = False

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"[PANDA] 已连接到 {self.host}:{self.port}")

            self._start_state_listener()
            return True
        except socket.timeout:
            raise RobotTimeoutError(f"连接超时 ({self.host}:{self.port})")
        except Exception as e:
            raise RobotCommError(f"连接失败: {e}")

    def disconnect(self):
        self._state_running = False
        if self._state_thread:
            self._state_thread.join(timeout=2)

        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        self.connected = False
        print("[PANDA] 连接已断开")

    def _start_state_listener(self):
        self._state_running = True
        self._state_thread = threading.Thread(target=self._state_listener_loop, daemon=True)
        self._state_thread.start()

    def _state_listener_loop(self):
        while self._state_running and self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if data:
                    self._recv_buffer += data
                    while '\n' in self._recv_buffer:
                        line, self._recv_buffer = self._recv_buffer.split('\n', 1)
                        try:
                            self._last_state = json.loads(line)
                        except:
                            pass
            except socket.timeout:
                continue
            except Exception as e:
                if self._state_running:
                    print(f"[PANDA] 状态监听异常: {e}")
                break

    def send_command(self, cmd, *args, **kwargs):
        if not self.connected:
            raise RobotCommError("未连接")

        try:
            command = {"command": cmd, "args": args, "kwargs": kwargs}
            self.socket.sendall((json.dumps(command) + "\n").encode('utf-8'))
            return True
        except Exception as e:
            raise RobotCommError(f"发送命令失败: {e}")

    def read_response(self):
        timeout = time.time() + self.timeout
        while time.time() < timeout:
            if self._last_state:
                return self._last_state
            time.sleep(0.01)
        raise RobotTimeoutError("读取响应超时")

    def get_joint_states(self):
        if self._last_state and "joint_states" in self._last_state:
            return self._last_state["joint_states"]

        self.send_command("get_joint_states")
        response = self.read_response()
        return response.get("joint_states", [])

    def move_joints(self, joint_angles, speed=1.0):
        self.send_command("move_joints", joint_angles, speed)
        response = self.read_response()
        return response.get("success", False)

    def move_cartesian(self, x, y, z, rx=0, ry=0, rz=0, speed=1.0):
        self.send_command("move_cartesian", x, y, z, rx, ry, rz, speed)
        response = self.read_response()
        return response.get("success", False)

    def get_ee_pose(self):
        if self._last_state and "ee_pose" in self._last_state:
            return self._last_state["ee_pose"]

        self.send_command("get_ee_pose")
        response = self.read_response()
        return response.get("ee_pose", {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]})

    def stop(self):
        self.send_command("stop")

    def set_speed(self, speed):
        self.send_command("set_speed", speed)

    def set_force_limit(self, force):
        self.send_command("set_force_limit", force)

    def get_robot_status(self):
        self.send_command("get_status")
        response = self.read_response()
        return response.get("status", {})
