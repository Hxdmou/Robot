"""
真实机械臂适配器（多品牌兼容版 v15.0）
提供统一的机器人控制接口，支持仿真和真实模式切换
兼容品牌：Franka Emika、KUKA、Universal Robots、ABB、Dobot、
          步科、宇树、云深处、Agility Robotics、Apptronik 等全球主流品牌
兼容仿真：PyBullet、MuJoCo、Isaac Sim、ROS2/Gazebo（通过仿真器抽象层）
安全原则：模式隔离、异常保护、状态同步、紧急停止
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
from typing import Dict, Any, Optional, List

from robot_comm import SimRobotComm
from panda_comm import PandaComm
from robot_safety import SafetyController, EmergencyStopMonitor
from robot_arm_db import RobotArmDB, ARM_DATABASE


# ============================================================================
# 全球主流品牌通信映射表（可扩展）
# ============================================================================
BRAND_COMM_MAP = {
    # Franka Emika
    "franka_panda": "panda_libfranka",
    "franka_research_3": "panda_libfranka",
    # KUKA
    "kuka_iiwa": "kuka_fri",
    "kuka_lbr_iiwa_14_r820": "kuka_fri",
    "kuka_kr_agilus": "kuka_eki",
    # Universal Robots
    "ur5e": "ur_rtde",
    "ur3e": "ur_rtde",
    "ur10e": "ur_rtde",
    "ur16e": "ur_rtde",
    "ur20": "ur_rtde",
    # ABB
    "abb_yumi": "abb_egm",
    "abb_irb_14000": "abb_egm",
    "abb_irb_1200": "abb_rapid",
    # Dobot
    "dobot_magician": "dobot_serial",
    "dobot_cr5": "dobot_tcp",
    "dobot_cr10": "dobot_tcp",
    # 国产
    "airbot_p7": "airbot_tcp",
    "ufactory_cra": "ufactory_tcp",
    "jaka_zu35": "jaka_tcp",
    "jaka_zu12": "jaka_tcp",
    "buke_collaborative": "buke_modbus",
    # 人形/四足
    "unitree_h1": "unitree_udp",
    "unitree_g1": "unitree_udp",
    "deeprobotics_dr02": "deeprobotics_tcp",
}

# 协议实现映射（协议名 → 适配器类，延迟导入避免依赖缺失）
PROTOCOL_ADAPTERS = {
    "panda_libfranka": "panda_comm.PandaComm",
    "kuka_fri": "protocol_adapters.KukaFRIAdapter",
    "kuka_eki": "protocol_adapters.KukaEKIAdapter",
    "ur_rtde": "protocol_adapters.URRTDEAdapter",
    "abb_egm": "protocol_adapters.ABBEGMAdapter",
    "abb_rapid": "protocol_adapters.ABBRapidAdapter",
    "dobot_serial": "protocol_adapters.DobotSerialAdapter",
    "dobot_tcp": "protocol_adapters.DobotTCPAdapter",
    "airbot_tcp": "protocol_adapters.AirbotTCPAdapter",
    "ufactory_tcp": "protocol_adapters.UFactoryTCPAdapter",
    "jaka_tcp": "protocol_adapters.JakaTCPAdapter",
    "buke_modbus": "protocol_adapters.BukeModbusAdapter",
    "unitree_udp": "protocol_adapters.UnitreeUDPAdapter",
    "deeprobotics_tcp": "protocol_adapters.DeepRoboticsTCPAdapter",
}


class RobotAdapter:
    """多品牌兼容机器人适配器
    
    设计原则：
      1. 不绑定任何特定品牌或协议 - 通过 robot_arm_db 动态加载配置
      2. 不绑定任何特定仿真器 - 通过 SimulatorBackend 抽象层支持 PyBullet/MuJoCo/Isaac Sim
      3. 安全优先 - 所有运动指令经过安全控制器校验
      4. 可扩展 - 新增品牌只需在 BRAND_COMM_MAP 和 protocol_adapters 中注册
    
    用法：
        # 仿真模式（PyBullet）
        adapter = RobotAdapter(mode="sim", arm_key="franka_panda")
        adapter.initialize()
        
        # 真机模式
        adapter = RobotAdapter(mode="real", arm_key="ur5e", 
                                config={"host": "192.168.1.100"})
        adapter.initialize()
        
        # 统一控制接口（仿真/真机完全一致）
        adapter.move_joints([0, -0.785, 0, -2.356, 0, 1.571, 0.785])
        adapter.move_cartesian(0.5, 0.0, 0.3)
    """

    def __init__(self, mode="sim", arm_key: Optional[str] = None, 
                 config: Optional[Dict[str, Any]] = None,
                 simulator_backend: Optional[str] = "pybullet"):
        """
        Args:
            mode: "sim" 或 "real"
            arm_key: 机器人型号key（如 "franka_panda", "ur5e", "kuka_iiwa"），
                     None 时从 config 中读取或使用默认
            config: 额外配置（host, port, joint_limits 等）
            simulator_backend: 仿真后端（pybullet/mujoco/isaac_sim/ros2），仅 sim 模式有效
        """
        self.mode = mode
        self.arm_key = arm_key or config.get("arm_key") if config else None
        self.config = config or {}
        self.simulator_backend = simulator_backend
        self.comm = None
        self.safety = SafetyController()
        self.emergency_stop = None
        self._initialized = False
        self._db = RobotArmDB()

        # 加载机器人配置
        if self.arm_key and self.arm_key in ARM_DATABASE:
            self.arm_config = ARM_DATABASE[self.arm_key]
            self.brand = self.arm_config.get("brand", "Unknown")
            self.model = self.arm_config.get("model", "Unknown")
            self.dofs = self.arm_config.get("degrees_of_freedom", 7)
            self.joint_indices = self.arm_config.get("joint_indices", list(range(self.dofs)))
            self.ee_link = self.arm_config.get("ee_link", "ee_link")
        else:
            self.arm_config = {}
            self.brand = self.config.get("brand", "Custom")
            self.model = self.config.get("model", "Custom")
            self.dofs = self.config.get("dofs", 7)
            self.joint_indices = self.config.get("joint_indices", list(range(self.dofs)))
            self.ee_link = self.config.get("ee_link", "ee_link")

    def _detect_protocol(self) -> str:
        """根据 arm_key 自动检测通信协议"""
        if self.arm_key and self.arm_key in BRAND_COMM_MAP:
            return BRAND_COMM_MAP[self.arm_key]
        return self.arm_config.get("communication", {}).get("protocol", "unknown")

    def _create_comm_real(self):
        """创建真机通信适配器（支持多品牌多协议）"""
        protocol = self._detect_protocol()
        comm_cfg = self.arm_config.get("communication", {})
        host = self.config.get("host") or comm_cfg.get("default_host", "192.168.1.1")
        port = self.config.get("port") or comm_cfg.get("default_port", 8080)

        print(f"[ADAPTER] 目标机器人: {self.brand} {self.model} ({self.arm_key})")
        print(f"[ADAPTER] 通信协议: {protocol} | 地址: {host}:{port}")

        # 优先使用已知适配器
        if protocol == "panda_libfranka":
            return PandaComm(host=host, port=port)
        elif protocol in PROTOCOL_ADAPTERS:
            # 延迟导入，避免缺少依赖时崩溃
            try:
                module_path, class_name = PROTOCOL_ADAPTERS[protocol].rsplit(".", 1)
                module = __import__(module_path, fromlist=[class_name])
                adapter_cls = getattr(module, class_name)
                return adapter_cls(host=host, port=port, config=self.arm_config)
            except (ImportError, AttributeError) as e:
                print(f"[ADAPTER] ⚠️  协议适配器 {protocol} 不可用: {e}")
                print(f"[ADAPTER] 降级为通用TCP适配器，请确保机器人支持标准控制接口")
                from deploy_adapters import MultiProtocolAdapter
                return MultiProtocolAdapter(self.arm_key or "custom")
        else:
            # 未知协议，使用通用适配器
            print(f"[ADAPTER] ⚠️  未知协议: {protocol}，使用通用适配器")
            from deploy_adapters import MultiProtocolAdapter
            return MultiProtocolAdapter(self.arm_key or "custom")

    def _create_comm_sim(self):
        """创建仿真通信适配器（通过仿真器抽象层，不绑定PyBullet）"""
        backend = self.simulator_backend.lower()
        print(f"[ADAPTER] 仿真后端: {backend} | 机器人: {self.brand} {self.model}")

        if backend == "pybullet":
            return SimRobotComm()
        elif backend == "mujoco":
            try:
                from sim_backends import MuJoCoBackend
                return MuJoCoBackend(self.arm_config, self.config)
            except ImportError:
                print("[ADAPTER] ⚠️  MuJoCo 不可用，降级为 PyBullet")
                return SimRobotComm()
        elif backend == "isaac_sim":
            try:
                from sim_backends import IsaacSimBackend
                return IsaacSimBackend(self.arm_config, self.config)
            except ImportError:
                print("[ADAPTER] ⚠️  Isaac Sim 不可用，降级为 PyBullet")
                return SimRobotComm()
        elif backend in ("ros2", "gazebo"):
            try:
                from sim_backends import ROS2Backend
                return ROS2Backend(self.arm_config, self.config)
            except ImportError:
                print("[ADAPTER] ⚠️  ROS2 不可用，降级为 PyBullet")
                return SimRobotComm()
        else:
            print(f"[ADAPTER] ⚠️  未知仿真后端: {backend}，使用 PyBullet")
            return SimRobotComm()

    def initialize(self):
        if self.mode == "real":
            self.comm = self._create_comm_real()
        else:
            self.comm = self._create_comm_sim()

        try:
            self.comm.connect()
            self._initialized = True
            print(f"[ADAPTER] 机器人适配器初始化完成 (模式: {self.mode})")

            # 从 arm_config 加载关节限制
            joint_limits = self.config.get("joint_limits") or self.arm_config.get("joint_limits")
            if joint_limits:
                self.safety.set_joint_limits(
                    self.joint_indices,
                    joint_limits.get("lower", []),
                    joint_limits.get("upper", [])
                )

            # 加载工作空间限制
            workspace = self.arm_config.get("workspace")
            if workspace:
                self.safety.set_workspace_limits(workspace)

            if self.mode == "real":
                self.emergency_stop = EmergencyStopMonitor(self.comm)
                self.emergency_stop.start()

            return True
        except Exception as e:
            print(f"[ADAPTER] 初始化失败: {e}")
            if self.comm:
                try:
                    self.comm.disconnect()
                except Exception:
                    pass
            return False

    def shutdown(self):
        if self.emergency_stop:
            self.emergency_stop.stop()

        if self.comm:
            try:
                self.comm.disconnect()
            except Exception:
                pass

        self._initialized = False
        print("[ADAPTER] 机器人适配器已关闭")

    def update_sim_params(self, robot_id, joint_indices, ee_index):
        if self.mode == "sim" and isinstance(self.comm, SimRobotComm):
            self.comm.robot_id = robot_id
            self.comm.joint_indices = joint_indices
            self.comm.ee_index = ee_index

    def list_supported_arms(self) -> List[str]:
        """列出所有支持的机器人型号"""
        return list(ARM_DATABASE.keys())

    def get_arm_info(self) -> Dict[str, Any]:
        """获取当前机器人信息"""
        return {
            "arm_key": self.arm_key,
            "brand": self.brand,
            "model": self.model,
            "dofs": self.dofs,
            "mode": self.mode,
            "simulator_backend": self.simulator_backend if self.mode == "sim" else None,
            "protocol": self._detect_protocol() if self.mode == "real" else None,
            "initialized": self._initialized,
            "connected": self.is_connected(),
        }

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
            self.safety.check_joint_limits(joint_angles, self.joint_indices)
            self.comm.move_joints(joint_angles, speed)
            return True
        except Exception as e:
            print(f"[ADAPTER] 移动关节失败: {e}")
            try:
                self.comm.stop()
            except Exception:
                pass
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
            try:
                self.comm.stop()
            except Exception:
                pass
            return False

    def get_ee_pose(self):
        if not self._initialized:
            return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}
        return self.comm.get_ee_pose()

    def stop(self):
        if self.comm:
            try:
                self.comm.stop()
            except Exception:
                pass

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
        return self.comm and getattr(self.comm, "connected", False)

    def set_safety_enabled(self, enabled):
        if enabled:
            self.safety.enable()
        else:
            self.safety.disable()
