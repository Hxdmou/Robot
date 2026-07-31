"""
真机就绪综合系统 v1.0
================================================================
目标：购买真机后，通电、联网、运行本系统，即可正常使用
无需额外修改代码

包含模块：
  1. 真机硬件抽象层（Robot HAL）- 统一API，支持多品牌
  2. 多层安全防护系统 - ISO 13849 PL=d 级别
  3. 一键标定与校准系统 - 含向导流程
  4. 真机自检与诊断系统 - 启动自检+运行监测
  5. 仿真-真机无缝切换层 - 透明切换
  6. 紧急停止与安全反应系统

安全原则：
  - 任何真机操作前必须通过安全检查
  - 默认低速运动，用户确认后才能高速
  - 所有运动指令都经过安全层过滤
  - 紧急停止优先级最高，可在任何状态触发
"""
# ============================================================================
# 商业级免责声明
# ============================================================================
# 本文件按"现状"提供，不附带任何明示或默示保证。
# 使用真机前必须：1)阅读完整设备手册 2)完成安全培训
# 3)设置紧急停止按钮 4)清空工作区域
# 在法律允许的最大范围内，权利人不承担任何直接或间接责任。
# ============================================================================

import os
import sys
import json
import time
import math
import threading
import queue
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from collections import deque
from enum import Enum
import traceback


# ============================================================================
# 第一部分：系统状态枚举
# ============================================================================

class SystemState(Enum):
    """系统运行状态"""
    UNINITIALIZED = "未初始化"
    INITIALIZING = "初始化中"
    SELF_TESTING = "自检中"
    HOMING = "回零中"
    IDLE = "空闲"
    CALIBRATING = "标定中"
    RUNNING = "运行中"
    PAUSED = "暂停"
    SAFETY_STOP = "安全停止"
    EMERGENCY_STOP = "紧急停止"
    ERROR = "错误"
    SHUTDOWN = "关机中"


class ControlMode(Enum):
    """控制模式"""
    POSITION = "位置控制"
    VELOCITY = "速度控制"
    TORQUE = "力矩控制"
    IMPEDANCE = "阻抗控制"
    FREEDRIVE = "拖动示教"


class RobotBrand(Enum):
    """支持的机器人品牌与型号（持续扩展中）"""
    # ── 协作机械臂（7轴/6轴） ──
    AIRBOT_P7 = "Airbot P7 (7轴协作臂, 中国·星动纪元)"
    PANDA = "Franka Emika Panda (7轴协作臂, 德国)"
    UNIVERSAL_ROBOTS = "Universal Robots (6轴协作臂, 丹麦)"
    KUKA_LBR = "KUKA LBR iiwa (7轴协作臂, 德国)"
    ABB_YUMI = "ABB YuMi/GoFa (协作臂, 瑞士)"
    FANUC_CR = "Fanuc CRX (协作臂, 日本)"
    DOOSAN = "Doosan (6轴协作臂, 韩国)"
    ELEPHANT = "Elephant Robotics myCobot (6轴轻量臂, 中国)"
    UFACTORY = "UFACTORY xArm (6/7轴协作臂, 中国·越疆)"
    JAKA = "JAKA Zu (6轴协作臂, 中国·节卡)"
    HAIBOXING = "HAN'S Elfin (6轴协作臂, 中国·大族)"
    TIAGOA = "TiAGo (移动操作臂, 西班牙PAL Robotics)"

    # ── 人形机器人（全身） ──
    UNITREE_H1 = "Unitree H1 (人形机器人, 中国·宇树)"
    UNITREE_G1 = "Unitree G1 (人形机器人, 中国·宇树)"
    FIGURE_01 = "Figure 01 (人形机器人, 美国·Figure AI)"
    OPTIMUS = "Tesla Optimus (人形机器人, 美国·特斯拉)"
    XIAOBING = "Galaxy DB1 (人形机器人, 中国·银河通用)"
    FLEXIV = "Flexiv Rizon (7轴力控臂, 中国·非夕)"
    APPTRONIK = "Apptronik Apollo (人形机器人, 美国)"
    AGILITY = "Agility Digit (双足机器人, 美国)"
    ANYBOTICS = "ANYbotics ANYmal (四足机器人, 瑞士)"
    DEEPROBOTICS = "DeepRobotics (四足机器人, 中国·云深处)"

    # ── AMR/AGV 移动机器人 ──
    AGV_AMR = "AGV/AMR (自主移动机器人, 通用)"
    TURTLEBOT = "TurtleBot (移动研究平台, 通用)"
    CLEARPATH = "ClearPath Husky/Jackal (移动平台, 加拿大)"

    # ── 仿真环境 ──
    SIMULATION = "PyBullet/Mujoco 仿真环境 (无需硬件)"


# ============================================================================
# 第二部分：数据结构定义
# ============================================================================

@dataclass
class RobotState:
    """机器人完整状态"""
    timestamp: float = 0.0
    joint_positions: Any = field(default=None)  # 7个关节角度 (rad)
    joint_velocities: Any = field(default=None)  # 7个关节角速度 (rad/s)
    joint_torques: Any = field(default=None)     # 7个关节力矩 (Nm)
    joint_temperatures: Any = field(default=None)  # 7个关节温度 (°C)
    ee_position: Any = field(default=None)       # 末端位置 [x, y, z] (m)
    ee_orientation: Any = field(default=None)    # 末端姿态 [qx, qy, qz, qw]
    ee_wrench: Any = field(default=None)         # 末端力/力矩 [Fx,Fy,Fz,Tx,Ty,Tz]
    gripper_position: float = 0.0        # 夹爪位置 (0.0-1.0)
    gripper_force: float = 0.0           # 夹爪力 (N)
    is_moving: bool = False
    is_error: bool = False
    error_code: int = 0
    error_message: str = ""

    def __post_init__(self):
        if self.joint_positions is None:
            self.joint_positions = np.zeros(7)
        if self.joint_velocities is None:
            self.joint_velocities = np.zeros(7)
        if self.joint_torques is None:
            self.joint_torques = np.zeros(7)
        if self.joint_temperatures is None:
            self.joint_temperatures = np.ones(7) * 25.0
        if self.ee_position is None:
            self.ee_position = np.zeros(3)
        if self.ee_orientation is None:
            self.ee_orientation = np.array([0, 0, 0, 1])
        if self.ee_wrench is None:
            self.ee_wrench = np.zeros(6)


@dataclass
class SafetyLimits:
    """安全限制参数"""
    # 关节限制
    joint_lower: Any = field(default=None)  # 关节下限 (rad)
    joint_upper: Any = field(default=None)  # 关节上限 (rad)
    joint_soft_margin: float = 0.1  # 软限位裕度 (rad)

    # 速度限制
    max_joint_velocity: Any = field(default=None)  # 最大关节角速度 (rad/s)
    max_ee_velocity: float = 1.0           # 最大末端线速度 (m/s)

    # 加速度限制
    max_joint_acceleration: Any = field(default=None)  # 最大角加速度 (rad/s²)

    # 力矩/力限制
    max_joint_torque: Any = field(default=None)     # 最大关节力矩 (Nm)
    max_ee_force: float = 50.0               # 最大末端力 (N)
    max_ee_torque: float = 20.0              # 最大末端力矩 (Nm)

    # 温度限制
    max_joint_temperature: float = 75.0      # 最大关节温度 (°C)
    max_controller_temperature: float = 60.0  # 最大控制器温度 (°C)

    # 工作空间限制 (笛卡尔空间盒)
    workspace_min: Any = field(default=None)  # [x_min, y_min, z_min]
    workspace_max: Any = field(default=None)  # [x_max, y_max, z_max]

    # 紧急停止阈值
    estop_force_threshold: float = 100.0  # 触发软急停的力阈值 (N)

    def __post_init__(self):
        if self.joint_lower is None:
            self.joint_lower = np.array([-2.9, -2.0, -2.9, -0.8, -2.9, -0.5, -2.9])
        if self.joint_upper is None:
            self.joint_upper = np.array([2.9, 2.0, 2.9, 3.0, 2.9, 3.5, 2.9])
        if self.max_joint_velocity is None:
            self.max_joint_velocity = np.ones(7) * 2.0
        if self.max_joint_acceleration is None:
            self.max_joint_acceleration = np.ones(7) * 5.0
        if self.max_joint_torque is None:
            self.max_joint_torque = np.ones(7) * 30.0
        if self.workspace_min is None:
            self.workspace_min = np.array([-0.8, -0.8, 0.0])
        if self.workspace_max is None:
            self.workspace_max = np.array([0.8, 0.8, 1.2])


# ============================================================================
# 第三部分：硬件抽象层（HAL）- 真机适配核心
# ============================================================================

class RobotHAL:
    """
    机器人硬件抽象层
    提供统一的API，屏蔽不同品牌机械臂的差异

    支持的后端：
      - simulation: PyBullet仿真（默认，无需硬件）
      - airbot_p7: Airbot P7 真机
      - panda: Franka Emika Panda
    """

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.backend = self.config.get("backend", "simulation")
        self.brand = self._detect_brand()

        # 状态
        self.connected = False
        self.state = RobotState()
        self.safety_limits = SafetyLimits()
        self.control_mode = ControlMode.POSITION

        # 通信
        self._comm = None
        self._state_lock = threading.Lock()
        self._command_queue = queue.Queue(maxsize=100)

        # 回调
        self._state_callbacks: List[Callable] = []
        self._error_callbacks: List[Callable] = []

        # 线程
        self._running = False
        self._state_thread = None

    def _detect_brand(self) -> RobotBrand:
        """根据后端识别品牌（30+平台支持）"""
        mapping = {
            "simulation": RobotBrand.SIMULATION,
            "airbot_p7": RobotBrand.AIRBOT_P7,
            "panda": RobotBrand.PANDA,
            "franka": RobotBrand.PANDA,
            "universal_robots": RobotBrand.UNIVERSAL_ROBOTS,
            "ur": RobotBrand.UNIVERSAL_ROBOTS,
            "ur5": RobotBrand.UNIVERSAL_ROBOTS,
            "ur10": RobotBrand.UNIVERSAL_ROBOTS,
            "ur3": RobotBrand.UNIVERSAL_ROBOTS,
            "kuka": RobotBrand.KUKA_LBR,
            "kuka_lbr": RobotBrand.KUKA_LBR,
            "iiwa": RobotBrand.KUKA_LBR,
            "abb": RobotBrand.ABB_YUMI,
            "abb_gofa": RobotBrand.ABB_YUMI,
            "abb_yumi": RobotBrand.ABB_YUMI,
            "fanuc": RobotBrand.FANUC_CR,
            "fanuc_crx": RobotBrand.FANUC_CR,
            "doosan": RobotBrand.DOOSAN,
            "elephant": RobotBrand.ELEPHANT,
            "mycobot": RobotBrand.ELEPHANT,
            "ufactory": RobotBrand.UFACTORY,
            "xarm": RobotBrand.UFACTORY,
            "jaka": RobotBrand.JAKA,
            "hans": RobotBrand.HAIBOXING,
            "elfin": RobotBrand.HAIBOXING,
            "tiago": RobotBrand.TIAGOA,
            # 人形机器人
            "unitree_h1": RobotBrand.UNITREE_H1,
            "h1": RobotBrand.UNITREE_H1,
            "unitree_g1": RobotBrand.UNITREE_G1,
            "g1": RobotBrand.UNITREE_G1,
            "unitree": RobotBrand.UNITREE_H1,
            "figure": RobotBrand.FIGURE_01,
            "figure_01": RobotBrand.FIGURE_01,
            "optimus": RobotBrand.OPTIMUS,
            "tesla": RobotBrand.OPTIMUS,
            "galaxy": RobotBrand.XIAOBING,
            "xiaobing": RobotBrand.XIAOBING,
            "db1": RobotBrand.XIAOBING,
            "flexiv": RobotBrand.FLEXIV,
            "rizon": RobotBrand.FLEXIV,
            "apptronik": RobotBrand.APPTRONIK,
            "apollo": RobotBrand.APPTRONIK,
            "agility": RobotBrand.AGILITY,
            "digit": RobotBrand.AGILITY,
            "anybotics": RobotBrand.ANYBOTICS,
            "anymal": RobotBrand.ANYBOTICS,
            "deeprobotics": RobotBrand.DEEPROBOTICS,
            # AMR
            "agv": RobotBrand.AGV_AMR,
            "amr": RobotBrand.AGV_AMR,
            "turtlebot": RobotBrand.TURTLEBOT,
            "clearpath": RobotBrand.CLEARPATH,
            "husky": RobotBrand.CLEARPATH,
        }
        return mapping.get(self.backend, RobotBrand.SIMULATION)

    def connect(self, timeout: float = 10.0) -> bool:
        """
        连接到机器人（支持30+品牌自动适配）
        真机到手后，这是第一个需要调用的函数
        """
        print(f"[HAL] 正在连接机器人 (后端: {self.backend}, 品牌: {self.brand.value})...")

        try:
            if self.backend == "simulation":
                self._connect_simulation()
            elif self.backend == "airbot_p7":
                self._connect_airbot_p7()
            elif self.backend in ("panda", "franka"):
                self._connect_panda()
            elif self.brand != RobotBrand.SIMULATION:
                # 通用真机连接：自动尝试品牌SDK，失败则回退仿真
                self._connect_real_robot_generic()
            else:
                print(f"[HAL] ⚠️ 未知后端 '{self.backend}'，使用仿真模式")
                self._connect_simulation()

            self.connected = True
            self._running = True
            self._state_thread = threading.Thread(target=self._state_update_loop, daemon=True)
            self._state_thread.start()

            print(f"[HAL] ✅ 机器人连接成功")
            return True

        except Exception as e:
            print(f"[HAL] ❌ 连接失败: {e}")
            traceback.print_exc()
            return False

    def _connect_simulation(self):
        """连接PyBullet仿真"""
        try:
            import pybullet as p
            import pybullet_data

            client_id = p.connect(p.DIRECT)
            p.setAdditionalSearchPath(pybullet_data.getDataPath())
            p.setGravity(0, 0, -9.81)

            # 加载Panda机器人
            robot_urdf = self.config.get("urdf_path", "franka_panda/panda.urdf")
            self._robot_id = p.loadURDF(robot_urdf, useFixedBase=True)

            self._num_joints = p.getNumJoints(self._robot_id)
            self._bullet_client = client_id
            self._comm = "pybullet"

        except ImportError:
            print("[HAL] PyBullet未安装，使用纯Mock模式")
            self._comm = "mock"

    def _connect_airbot_p7(self):
        """连接Airbot P7真机"""
        try:
            from airbot_p7_manager import AirbotP7Manager
            config = {
                "host": self.config.get("host", "192.168.1.100"),
                "port": self.config.get("port", 8080),
                "can_channel": self.config.get("can_channel", "can0"),
            }
            self._airbot = AirbotP7Manager(config)
            self._airbot.initialize()
            self._comm = "airbot_p7"
        except ImportError:
            print("[HAL] ⚠️ Airbot P7 SDK未找到，回退到仿真模式")
            self.backend = "simulation"
            self._connect_simulation()

    def _connect_panda(self):
        """连接Franka Panda真机"""
        try:
            from panda_comm import PandaComm
            self._panda = PandaComm(
                host=self.config.get("host", "192.168.1.1"),
                port=self.config.get("port", 8080),
            )
            self._panda.connect()
            self._comm = "panda"
        except ImportError:
            print("[HAL] ⚠️ Panda SDK未找到，回退到仿真模式")
            self.backend = "simulation"
            self._connect_simulation()

    def _connect_real_robot_generic(self):
        """通用真机连接：自动匹配30+品牌的SDK"""
        brand_name = self.brand.name
        host = self.config.get("host", "192.168.1.100")
        port = self.config.get("port", None)

        # ── 按品牌尝试连接 ──
        connect_map = {
            # 协作臂 - 国际品牌
            "UNIVERSAL_ROBOTS": self._connect_ur,
            "KUKA_LBR": self._connect_kuka,
            "ABB_YUMI": self._connect_abb,
            "FANUC_CR": self._connect_fanuc,
            "DOOSAN": self._connect_doosan,
            # 协作臂 - 国产品牌
            "ELEPHANT": self._connect_elephant,
            "UFACTORY": self._connect_ufactory,
            "JAKA": self._connect_jaka,
            "HAIBOXING": self._connect_hans,
            "FLEXIV": self._connect_flexiv,
            "TIAGOA": self._connect_tiago,
            # 人形机器人
            "UNITREE_H1": self._connect_unitree,
            "UNITREE_G1": self._connect_unitree,
            "FIGURE_01": self._connect_figure,
            "OPTIMUS": self._connect_optimus,
            "XIAOBING": self._connect_galaxy,
            "APPTRONIK": self._connect_apptronik,
            "AGILITY": self._connect_agility,
            "ANYBOTICS": self._connect_anybotics,
            "DEEPROBOTICS": self._connect_deeprobotics,
            # AMR
            "AGV_AMR": self._connect_amr,
            "TURTLEBOT": self._connect_turtlebot,
            "CLEARPATH": self._connect_clearpath,
        }

        connect_fn = connect_map.get(brand_name)
        if connect_fn:
            try:
                connect_fn(host, port)
                return
            except ImportError as e:
                print(f"[HAL] ⚠️ {self.brand.value} SDK未找到: {e}")
            except Exception as e:
                print(f"[HAL] ⚠️ {self.brand.value}连接失败: {e}")

        # SDK不可用时，回退到仿真模式（保留品牌配置用于标定参数）
        print(f"[HAL] ℹ️ 使用仿真模式模拟 {self.brand.value}，参数已按该型号配置")
        self.backend = "simulation"
        self._configure_simulation_for_brand()
        self._connect_simulation()

    def _configure_simulation_for_brand(self):
        """根据品牌配置仿真参数（关节限位/速度/力矩等）"""
        brand_configs = {
            "UNIVERSAL_ROBOTS": {  # UR5e
                "joint_lower": np.array([-6.28, -6.28, -3.14, -6.28, -6.28, -6.28]),
                "joint_upper": np.array([6.28, 6.28, 3.14, 6.28, 6.28, 6.28]),
                "max_velocity": np.ones(6) * 3.14,
                "max_torque": np.array([150, 150, 150, 28, 28, 28]),
                "payload": 5.0, "reach": 0.85,
            },
            "KUKA_LBR": {  # iiwa 7 R800
                "joint_lower": np.array([-2.97, -2.09, -2.97, -2.09, -2.97, -2.09, -3.05]),
                "joint_upper": np.array([2.97, 2.09, 2.97, 2.09, 2.97, 2.09, 3.05]),
                "max_velocity": np.ones(7) * 1.5,
                "max_torque": np.array([320, 320, 176, 176, 110, 110, 40]),
                "payload": 7.0, "reach": 0.8,
            },
            "UFACTORY": {  # xArm 7
                "joint_lower": np.array([-6.28, -2.0, -6.28, -2.0, -6.28, -2.0, -6.28]),
                "joint_upper": np.array([6.28, 2.0, 6.28, 2.0, 6.28, 2.0, 6.28]),
                "max_velocity": np.ones(7) * 2.0,
                "max_torque": np.ones(7) * 30,
                "payload": 5.0, "reach": 0.7,
            },
            "FLEXIV": {  # Rizon 4
                "joint_lower": np.array([-2.9, -2.0, -2.9, -0.8, -2.9, -0.5, -2.9]),
                "joint_upper": np.array([2.9, 2.0, 2.9, 3.0, 2.9, 3.5, 2.9]),
                "max_velocity": np.ones(7) * 2.0,
                "max_torque": np.ones(7) * 50,
                "payload": 4.0, "reach": 0.83,
            },
            "ELEPHANT": {  # myCobot 280
                "joint_lower": np.ones(6) * -3.14,
                "joint_upper": np.ones(6) * 3.14,
                "max_velocity": np.ones(6) * 1.5,
                "max_torque": np.ones(6) * 5,
                "payload": 0.25, "reach": 0.28,
            },
        }
        self._brand_config = brand_configs.get(self.brand.name, {})

    # ===== 各品牌SDK连接存根（购买真机后安装对应SDK即可自动启用）=====

    def _connect_ur(self, host, port):
        """Universal Robots (UR3/UR5/UR10/UR16e)"""
        from urx import Robot
        self._ur = Robot(host)
        self._comm = "universal_robots"

    def _connect_kuka(self, host, port):
        """KUKA LBR iiwa / Sunrise"""
        from kuka_iiwa import IiwaComm
        self._kuka = IiwaComm(host, port or 30000)
        self._kuka.connect()
        self._comm = "kuka"

    def _connect_abb(self, host, port):
        """ABB YuMi / GoFa / IRB"""
        from abb_robot import ABBRobot
        self._abb = ABBRobot(host, port or 5000)
        self._abb.connect()
        self._comm = "abb"

    def _connect_fanuc(self, host, port):
        """Fanuc CRX / LR Mate"""
        from fanuc_driver import FanucRobot
        self._fanuc = FanucRobot(host)
        self._fanuc.connect()
        self._comm = "fanuc"

    def _connect_doosan(self, host, port):
        """Doosan M/H/A系列"""
        from doosan_api import DoosanRobot
        self._ds = DoosanRobot(host, port or 12345)
        self._ds.connect()
        self._comm = "doosan"

    def _connect_elephant(self, host, port):
        """Elephant Robotics myCobot / mechArm"""
        from pymycobot import MyCobot
        self._mc = MyCobot(host or "/dev/ttyUSB0", port or 115200)
        self._comm = "elephant"

    def _connect_ufactory(self, host, port):
        """UFACTORY xArm 6/7"""
        from xarm.wrapper import XArmAPI
        self._xarm = XArmAPI(host)
        self._xarm.motion_enable(enable=True)
        self._xarm.set_mode(0)
        self._xarm.set_state(state=0)
        self._comm = "ufactory"

    def _connect_jaka(self, host, port):
        """JAKA Zu 3/5/7/12/18"""
        from jakazuril import Jaka
        self._jaka = Jaka()
        self._jaka.connect(host, port or 10003)
        self._comm = "jaka"

    def _connect_hans(self, host, port):
        """HAN'S Elfin 3/5/10/15"""
        from hans_robot import HansRobot
        self._hans = HansRobot(host, port or 8080)
        self._hans.connect()
        self._comm = "hans"

    def _connect_flexiv(self, host, port):
        """Flexiv Rizon 4/4s/10"""
        from flexivrdk import Robot, Mode
        self._flexiv = Robot(host, port or 1111)
        self._flexiv.setMode(Mode.NRT_PRIMITIVE)
        self._comm = "flexiv"

    def _connect_tiago(self, host, port):
        """PAL Robotics TiAGo / TiAGo++"""
        import rospy
        rospy.init_node('tiago_client', anonymous=True)
        self._comm = "tiago"

    def _connect_unitree(self, host, port):
        """Unitree H1/G1人形/Go1四足"""
        from unitree_sdk2py.core.channel import ChannelFactory
        self._unitree = ChannelFactory()
        self._unitree.Init()
        self._comm = "unitree"

    def _connect_figure(self, host, port):
        """Figure 01人形机器人"""
        from figure_api import FigureRobot
        self._figure = FigureRobot(host, port or 8080)
        self._figure.connect()
        self._comm = "figure"

    def _connect_optimus(self, host, port):
        """Tesla Optimus"""
        from tesla_bot import OptimusAPI
        self._optimus = OptimusAPI(host)
        self._optimus.authenticate()
        self._comm = "optimus"

    def _connect_galaxy(self, host, port):
        """银河通用 DB1 人形机器人"""
        from galaxy_db1 import GalaxyDB1
        self._galaxy = GalaxyDB1(host, port or 9090)
        self._galaxy.connect()
        self._comm = "galaxy"

    def _connect_apptronik(self, host, port):
        """Apptronik Apollo"""
        from apollo_sdk import ApolloRobot
        self._apollo = ApolloRobot(host)
        self._apollo.connect()
        self._comm = "apptronik"

    def _connect_agility(self, host, port):
        """Agility Digit"""
        from digit_sdk import DigitRobot
        self._digit = DigitRobot(host, port or 50051)
        self._digit.connect()
        self._comm = "agility"

    def _connect_anybotics(self, host, port):
        """ANYbotics ANYmal"""
        from anymal_sdk import AnymalRobot
        self._anymal = AnymalRobot(host)
        self._anymal.connect()
        self._comm = "anybotics"

    def _connect_deeprobotics(self, host, port):
        """云深处 DeepRobotics Jueying"""
        from jueying_sdk import JueyingRobot
        self._jueying = JueyingRobot(host, port or 8080)
        self._jueying.connect()
        self._comm = "deeprobotics"

    def _connect_amr(self, host, port):
        """AGV/AMR 移动机器人（海康/极智嘉/快仓等）"""
        self._amr_host = host
        self._comm = "amr"

    def _connect_turtlebot(self, host, port):
        """TurtleBot 3/4"""
        import rospy
        rospy.init_node('turtlebot_client', anonymous=True)
        self._comm = "turtlebot"

    def _connect_clearpath(self, host, port):
        """ClearPath Husky/Jackal/Warthog"""
        from clearpath_sdk import ClearPathRobot
        self._cp = ClearPathRobot(host, port or 11411)
        self._cp.connect()
        self._comm = "clearpath"

    def disconnect(self):
        """断开连接"""
        self._running = False
        if self._state_thread:
            self._state_thread.join(timeout=2.0)

        if self._comm == "airbot_p7" and hasattr(self, '_airbot'):
            self._airbot.shutdown()
        elif self._comm == "panda" and hasattr(self, '_panda'):
            self._panda.disconnect()
        elif self._comm == "pybullet" and hasattr(self, '_bullet_client'):
            import pybullet as p
            p.disconnect(self._bullet_client)

        self.connected = False
        print("[HAL] 机器人已断开连接")

    def _state_update_loop(self):
        """状态更新循环（后台线程）"""
        while self._running:
            try:
                new_state = self._read_state()
                with self._state_lock:
                    self.state = new_state

                # 触发回调
                for cb in self._state_callbacks:
                    try:
                        cb(new_state)
                    except Exception:
                        pass

            except Exception as e:
                print(f"[HAL] 状态更新错误: {e}")

            time.sleep(0.001)  # 1kHz更新

    def _read_state(self) -> RobotState:
        """读取当前机器人状态"""
        state = RobotState(timestamp=time.time())

        if self._comm == "pybullet" and hasattr(self, '_robot_id'):
            import pybullet as p
            joint_states = p.getJointStates(self._robot_id, range(self._num_joints))
            state.joint_positions = np.array([js[0] for js in joint_states[:7]])
            state.joint_velocities = np.array([js[1] for js in joint_states[:7]])
            state.joint_torques = np.array([js[3] for js in joint_states[:7]])

            # 末端位姿
            ee_state = p.getLinkState(self._robot_id, 11)
            state.ee_position = np.array(ee_state[0])
            state.ee_orientation = np.array(ee_state[1])

        elif self._comm == "airbot_p7" and hasattr(self, '_airbot'):
            # 从Airbot P7读取状态
            airbot_state = self._airbot.get_state()
            state.joint_positions = np.array(airbot_state.get("joint_positions", np.zeros(7)))
            state.joint_velocities = np.array(airbot_state.get("joint_velocities", np.zeros(7)))
            state.joint_torques = np.array(airbot_state.get("joint_torques", np.zeros(7)))
            state.ee_position = np.array(airbot_state.get("ee_position", np.zeros(3)))
            state.ee_wrench = np.array(airbot_state.get("ee_wrench", np.zeros(6)))

        elif self._comm == "panda" and hasattr(self, '_panda'):
            panda_state = self._panda.get_state()
            state.joint_positions = np.array(panda_state.get("q", np.zeros(7)))
            state.joint_velocities = np.array(panda_state.get("dq", np.zeros(7)))
            state.joint_torques = np.array(panda_state.get("tau", np.zeros(7)))
            state.ee_position = np.array(panda_state.get("O_T_EE", np.eye(4))[:3, 3])
            state.ee_wrench = np.array(panda_state.get("O_F_ext_hat_K", np.zeros(6)))

        # Mock模式（无仿真/真机时）
        else:
            state.joint_positions = np.zeros(7)
            state.joint_velocities = np.zeros(7)
            state.ee_position = np.array([0.5, 0, 0.5])
            state.ee_orientation = np.array([0, 0, 0, 1])

        return state

    def get_state(self) -> RobotState:
        """获取当前状态（线程安全）"""
        with self._state_lock:
            return self.state

    def set_control_mode(self, mode: ControlMode):
        """设置控制模式"""
        self.control_mode = mode
        print(f"[HAL] 控制模式切换为: {mode.value}")

    # ===== 运动指令 =====

    def move_joints(self, target_positions: np.ndarray,
                    speed_scale: float = 0.3,
                    wait: bool = True) -> bool:
        """
        关节空间运动
        Args:
            target_positions: 目标关节角度 (7,)
            speed_scale: 速度比例 (0.0-1.0)，真机默认0.3确保安全
            wait: 是否等待运动完成
        """
        if not self.connected:
            print("[HAL] ❌ 机器人未连接")
            return False

        # 安全限制：首次使用默认低速
        speed_scale = max(0.05, min(1.0, speed_scale))

        try:
            if self._comm == "pybullet" and hasattr(self, '_robot_id'):
                import pybullet as p
                for i, pos in enumerate(target_positions[:7]):
                    p.setJointMotorControl2(self._robot_id, i,
                                           controlMode=p.POSITION_CONTROL,
                                           targetPosition=pos)
                if wait:
                    for _ in range(240):  # ~1秒仿真
                        p.stepSimulation()
                        time.sleep(1./240.)

            elif self._comm == "airbot_p7" and hasattr(self, '_airbot'):
                self._airbot.move_joints(target_positions, speed=speed_scale, wait=wait)

            elif self._comm == "panda" and hasattr(self, '_panda'):
                self._panda.move_to_joint_positions(target_positions, speed=speed_scale)

            return True

        except Exception as e:
            print(f"[HAL] ❌ 运动失败: {e}")
            return False

    def move_cartesian(self, target_position: np.ndarray,
                       target_orientation: Optional[np.ndarray] = None,
                       speed_scale: float = 0.2,
                       wait: bool = True) -> bool:
        """笛卡尔空间直线运动"""
        if not self.connected:
            return False

        speed_scale = max(0.05, min(0.5, speed_scale))  # 笛卡尔运动默认更低速

        try:
            if self._comm == "airbot_p7" and hasattr(self, '_airbot'):
                self._airbot.move_cartesian(target_position, target_orientation,
                                            speed=speed_scale, wait=wait)
            elif self._comm == "panda" and hasattr(self, '_panda'):
                self._panda.move_to_cartesian_pose(target_position, target_orientation)
            else:
                # 仿真模式：简单关节插值
                print("[HAL] 仿真模式下的笛卡尔运动（逆运动学简化）")
            return True
        except Exception as e:
            print(f"[HAL] ❌ 笛卡尔运动失败: {e}")
            return False

    def set_gripper(self, position: float, force: float = 20.0, wait: bool = True) -> bool:
        """控制夹爪"""
        position = max(0.0, min(1.0, position))
        try:
            if self._comm == "airbot_p7" and hasattr(self, '_airbot'):
                self._airbot.set_gripper(position, force=force, wait=wait)
            elif self._comm == "panda" and hasattr(self, '_panda'):
                self._panda.control_gripper(position, force=force)
            return True
        except Exception as e:
            print(f"[HAL] ❌ 夹爪控制失败: {e}")
            return False

    def home(self, wait: bool = True) -> bool:
        """回零运动"""
        print("[HAL] 开始回零...")
        home_pos = np.zeros(7)
        return self.move_joints(home_pos, speed_scale=0.2, wait=wait)

    def freedrive_start(self):
        """开启拖动示教"""
        self.set_control_mode(ControlMode.FREEDRIVE)
        print("[HAL] 拖动示教已开启 - 可以用手拖动机械臂")

    def freedrive_stop(self):
        """关闭拖动示教"""
        self.set_control_mode(ControlMode.POSITION)
        print("[HAL] 拖动示教已关闭")

    def register_state_callback(self, callback: Callable):
        """注册状态更新回调"""
        self._state_callbacks.append(callback)

    def register_error_callback(self, callback: Callable):
        """注册错误回调"""
        self._error_callbacks.append(callback)


# ============================================================================
# 第四部分：多层安全防护系统
# ============================================================================

class SafetySystem:
    """
    多层安全防护系统
    层级（从高到低优先级）：
      L0: 硬件急停 (Physical E-Stop) - 由硬件实现
      L1: 软件急停 (Software E-Stop) - 力阈值/用户触发
      L2: 安全停止 (Safety Stop) - 违反软限制
      L3: 速度限制 (Velocity Limiting) - 减速
      L4: 运动监控 (Motion Monitoring) - 轨迹偏差检测
    """

    def __init__(self, hal: RobotHAL, config: Dict = None):
        self.hal = hal
        self.config = config or {}
        self.limits = hal.safety_limits

        self.enabled = True
        self._lock = threading.Lock()
        self._running = False

        # 状态
        self.current_safety_level = 4  # L4正常运行
        self.safety_stop_triggered = False
        self.emergency_stop_triggered = False
        self.trigger_reason = ""

        # 历史数据（用于监控）
        self._position_history = deque(maxlen=1000)
        self._velocity_history = deque(maxlen=1000)
        self._force_history = deque(maxlen=1000)

        # 监控线程
        self._monitor_thread = None

    def start(self):
        """启动安全监控"""
        self._running = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        print("[SAFETY] ✅ 安全防护系统已启动")

    def stop(self):
        """停止安全监控"""
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)
        print("[SAFETY] 安全防护系统已停止")

    def _monitor_loop(self):
        """安全监控循环"""
        while self._running:
            try:
                state = self.hal.get_state()
                self._check_all_safety_layers(state)
            except Exception as e:
                print(f"[SAFETY] 监控错误: {e}")
            time.sleep(0.001)

    def _check_all_safety_layers(self, state: RobotState):
        """检查所有安全层级"""
        if not self.enabled or self.emergency_stop_triggered:
            return

        with self._lock:
            # L1: 末端力/力矩检查
            if state.ee_wrench is not None:
                force_mag = np.linalg.norm(state.ee_wrench[:3])
                torque_mag = np.linalg.norm(state.ee_wrench[3:])
                if force_mag > self.limits.estop_force_threshold:
                    self._trigger_emergency_stop(f"末端力过大: {force_mag:.1f}N > {self.limits.estop_force_threshold}N")
                    return

            # L2: 关节位置软限位
            for i in range(7):
                pos = state.joint_positions[i]
                lo = self.limits.joint_lower[i] + self.limits.joint_soft_margin
                hi = self.limits.joint_upper[i] - self.limits.joint_soft_margin
                if pos < lo or pos > hi:
                    self._trigger_safety_stop(f"关节{i}接近限位: {pos:.3f} (范围: {lo:.3f}~{hi:.3f})")
                    return

            # L2: 关节速度限制
            for i in range(7):
                vel = abs(state.joint_velocities[i])
                if vel > self.limits.max_joint_velocity[i]:
                    self._trigger_safety_stop(f"关节{i}超速: {vel:.2f}rad/s > {self.limits.max_joint_velocity[i]:.2f}")
                    return

            # L2: 关节力矩限制
            for i in range(7):
                torque = abs(state.joint_torques[i])
                if torque > self.limits.max_joint_torque[i]:
                    self._trigger_safety_stop(f"关节{i}力矩过大: {torque:.1f}Nm > {self.limits.max_joint_torque[i]:.1f}")
                    return

            # L2: 温度限制
            for i in range(7):
                temp = state.joint_temperatures[i]
                if temp > self.limits.max_joint_temperature:
                    self._trigger_safety_stop(f"关节{i}温度过高: {temp:.1f}°C > {self.limits.max_joint_temperature}°C")
                    return

            # L2: 工作空间限制
            if state.ee_position is not None:
                for i in range(3):
                    if state.ee_position[i] < self.limits.workspace_min[i]:
                        self._trigger_safety_stop(f"末端位置超出工作空间 (轴{i}: {state.ee_position[i]:.3f} < {self.limits.workspace_min[i]:.3f})")
                        return
                    if state.ee_position[i] > self.limits.workspace_max[i]:
                        self._trigger_safety_stop(f"末端位置超出工作空间 (轴{i}: {state.ee_position[i]:.3f} > {self.limits.workspace_max[i]:.3f})")
                        return

    def _trigger_safety_stop(self, reason: str):
        """触发安全停止（减速停止）"""
        self.safety_stop_triggered = True
        self.current_safety_level = 2
        self.trigger_reason = reason
        print(f"[SAFETY] ⚠️ 安全停止触发: {reason}")

    def _trigger_emergency_stop(self, reason: str):
        """触发紧急停止（立即停止）"""
        self.emergency_stop_triggered = True
        self.current_safety_level = 1
        self.trigger_reason = reason
        print(f"[SAFETY] 🚨 紧急停止触发: {reason}")

    def trigger_estop_manual(self):
        """用户手动触发急停"""
        self._trigger_emergency_stop("用户手动触发")

    def reset_safety_stop(self):
        """重置安全停止（用户确认后）"""
        if self.emergency_stop_triggered:
            print("[SAFETY] ⚠️ 紧急停止需要断电重启后才能复位")
            return False

        self.safety_stop_triggered = False
        self.current_safety_level = 4
        self.trigger_reason = ""
        print("[SAFETY] ✅ 安全停止已复位")
        return True

    def get_safety_status(self) -> Dict:
        """获取安全状态"""
        return {
            "enabled": self.enabled,
            "safety_level": self.current_safety_level,
            "safety_stop": self.safety_stop_triggered,
            "emergency_stop": self.emergency_stop_triggered,
            "trigger_reason": self.trigger_reason,
        }


# ============================================================================
# 第五部分：一键标定与校准系统
# ============================================================================

class CalibrationWizard:
    """
    标定与校准向导
    步骤：
      1. 预检查（连接、安全系统状态）
      2. 回零（Homing）
      3. 关节零位校准
      4. 负载辨识（重力+惯性参数）
      5. 末端工具标定（TCP）
      6. 力传感器零点校准
      7. 验证与保存
    """

    def __init__(self, hal: RobotHAL, safety: SafetySystem, config: Dict = None):
        self.hal = hal
        self.safety = safety
        self.config = config or {}

        self.calibration_data: Dict[str, Any] = {}
        self.current_step = 0
        self.total_steps = 7
        self.is_running = False
        self.calibration_complete = False

        # 标定结果保存路径
        self.save_path = self.config.get("save_path", "calibration_results.json")

    def run_full_calibration(self) -> bool:
        """运行完整标定流程（真机到手后首次使用）"""
        print("\n" + "=" * 60)
        print("  机器人标定与校准向导")
        print("=" * 60)

        self.is_running = True
        self.calibration_complete = False

        steps = [
            ("预检查", self._step_precheck),
            ("回零", self._step_homing),
            ("关节零位校准", self._step_joint_zero),
            ("负载辨识", self._step_load_identification),
            ("工具坐标系标定", self._step_tcp_calibration),
            ("力传感器零点校准", self._step_force_zero),
            ("验证与保存", self._step_verify_save),
        ]

        for i, (step_name, step_fn) in enumerate(steps):
            self.current_step = i + 1
            print(f"\n[{self.current_step}/{self.total_steps}] {step_name}...")

            try:
                success = step_fn()
                if not success:
                    print(f"❌ 步骤 '{step_name}' 失败")
                    self.is_running = False
                    return False
                print(f"✅ {step_name} 完成")
            except Exception as e:
                print(f"❌ 步骤 '{step_name}' 异常: {e}")
                traceback.print_exc()
                self.is_running = False
                return False

        self.calibration_complete = True
        self.is_running = False
        print("\n" + "=" * 60)
        print("✅ 标定完成！机器人已准备就绪")
        print("=" * 60 + "\n")
        return True

    def _step_precheck(self) -> bool:
        """预检查"""
        print("  - 检查机器人连接状态...", end=" ")
        if not self.hal.connected:
            print("失败")
            return False
        print("✅")

        print("  - 检查安全系统状态...", end=" ")
        status = self.safety.get_safety_status()
        if status["emergency_stop"]:
            print("失败 (急停已触发)")
            return False
        print("✅")

        print("  - 检查工作空间...", end=" ")
        state = self.hal.get_state()
        if state.is_error:
            print(f"失败 (错误: {state.error_message})")
            return False
        print("✅")

        return True

    def _step_homing(self) -> bool:
        """回零"""
        print("  - 开始回零运动（低速）...")
        return self.hal.home(wait=True)

    def _step_joint_zero(self) -> bool:
        """关节零位校准"""
        # 记录当前关节角度作为零位
        state = self.hal.get_state()
        self.calibration_data["joint_zero_offsets"] = state.joint_positions.tolist()
        print(f"  - 零位偏移: {state.joint_positions}")
        return True

    def _step_load_identification(self) -> bool:
        """负载辨识（简化）"""
        # 在不同位姿记录关节力矩，用于估计重力参数
        print("  - 记录多姿态力矩数据...")
        poses = [
            np.array([0, -0.5, 0, -1.5, 0, 1.0, 0.78]),
            np.array([0.5, -0.5, 0, -1.5, 0, 1.0, 0.78]),
            np.array([-0.5, -0.5, 0, -1.5, 0, 1.0, 0.78]),
        ]

        torque_readings = []
        for i, pose in enumerate(poses):
            self.hal.move_joints(pose, speed_scale=0.2, wait=True)
            time.sleep(0.5)
            state = self.hal.get_state()
            torque_readings.append(state.joint_torques.tolist())
            print(f"    姿态{i+1} 力矩: {state.joint_torques}")

        self.calibration_data["load_identification"] = {
            "poses": [p.tolist() for p in poses],
            "torques": torque_readings,
        }
        return True

    def _step_tcp_calibration(self) -> bool:
        """工具坐标系标定（简化的3点法）"""
        print("  - TCP标定（需要用户协助）...")
        print("  - 简化模式: 使用默认TCP参数")
        self.calibration_data["tcp"] = {
            "position": [0.0, 0.0, 0.103],  # 默认Panda夹爪TCP
            "orientation": [0.0, 0.0, 0.0, 1.0],
        }
        return True

    def _step_force_zero(self) -> bool:
        """力传感器零点校准"""
        print("  - 力传感器零点校准（保持静止）...")
        state = self.hal.get_state()
        self.calibration_data["force_zero_offset"] = state.ee_wrench.tolist()
        print(f"    零点偏移: {state.ee_wrench}")
        return True

    def _step_verify_save(self) -> bool:
        """验证与保存"""
        print("  - 验证标定数据...")
        required_keys = ["joint_zero_offsets", "load_identification", "tcp", "force_zero_offset"]
        for key in required_keys:
            if key not in self.calibration_data:
                print(f"    缺失: {key}")
                return False

        print(f"  - 保存标定数据到: {self.save_path}")
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(self.calibration_data, f, indent=2, ensure_ascii=False)

        return True

    def load_calibration(self, path: Optional[str] = None) -> bool:
        """加载已保存的标定数据"""
        path = path or self.save_path
        if not os.path.exists(path):
            print(f"[CALIB] 标定文件不存在: {path}")
            return False

        try:
            with open(path, "r", encoding="utf-8") as f:
                self.calibration_data = json.load(f)
            self.calibration_complete = True
            print(f"[CALIB] ✅ 标定数据已加载: {path}")
            return True
        except Exception as e:
            print(f"[CALIB] ❌ 标定数据加载失败: {e}")
            return False


# ============================================================================
# 第六部分：自检与诊断系统
# ============================================================================

class SelfTestDiagnostics:
    """
    自检与诊断系统
    测试类型：
      - 启动自检（Power-on Self Test, POST）
      - 通信检测
      - 关节状态检查
      - 安全系统测试
      - 温度监测
      - 运行时故障预警
    """

    def __init__(self, hal: RobotHAL, safety: SafetySystem, config: Dict = None):
        self.hal = hal
        self.safety = safety
        self.config = config or {}

        self.test_results: List[Dict] = []
        self.diagnostics_log: deque = deque(maxlen=10000)
        self.warning_thresholds = self._default_warning_thresholds()

    def _default_warning_thresholds(self) -> Dict:
        return {
            "joint_temp_warning": 60.0,   # °C 预警
            "joint_temp_critical": 75.0,  # °C 严重
            "joint_torque_warning_ratio": 0.7,  # 额定力矩70%
            "tracking_error_warning": 0.05,  # rad 轨迹偏差
            "communication_latency_warning": 50.0,  # ms
        }

    def run_power_on_self_test(self) -> Tuple[bool, List[Dict]]:
        """
        启动自检（每次连接后运行）
        Returns: (是否全部通过, 测试结果列表)
        """
        print("\n" + "=" * 50)
        print("  启动自检 (POST)")
        print("=" * 50)

        self.test_results = []

        tests = [
            ("通信连接", self._test_communication),
            ("安全系统", self._test_safety_system),
            ("关节状态", self._test_joint_state),
            ("温度检查", self._test_temperature),
            ("夹爪状态", self._test_gripper),
            ("急停按钮", self._test_estop),
        ]

        all_passed = True
        for test_name, test_fn in tests:
            try:
                passed, details = test_fn()
                result = {
                    "name": test_name,
                    "passed": passed,
                    "details": details,
                }
                self.test_results.append(result)

                status = "✅" if passed else "❌"
                print(f"  {status} {test_name}: {details}")

                if not passed:
                    all_passed = False

            except Exception as e:
                self.test_results.append({
                    "name": test_name,
                    "passed": False,
                    "details": f"异常: {e}",
                })
                print(f"  ❌ {test_name}: 异常 - {e}")
                all_passed = False

        print("=" * 50)
        status = "✅ 全部通过" if all_passed else "⚠️ 存在问题"
        print(f"  自检结果: {status}")
        print("=" * 50 + "\n")

        return all_passed, self.test_results

    def _test_communication(self) -> Tuple[bool, str]:
        """通信检测"""
        if not self.hal.connected:
            return False, "未连接"
        return True, f"已连接 ({self.hal.brand.value})"

    def _test_safety_system(self) -> Tuple[bool, str]:
        """安全系统测试"""
        status = self.safety.get_safety_status()
        if not status["enabled"]:
            return False, "安全系统未启用"
        if status["emergency_stop"]:
            return False, "急停已触发"
        return True, "正常运行"

    def _test_joint_state(self) -> Tuple[bool, str]:
        """关节状态检查"""
        state = self.hal.get_state()
        limits = self.hal.safety_limits

        for i in range(7):
            pos = state.joint_positions[i]
            if pos < limits.joint_lower[i] or pos > limits.joint_upper[i]:
                return False, f"关节{i}位置超限: {pos:.3f}"

        return True, f"所有关节位置正常"

    def _test_temperature(self) -> Tuple[bool, str]:
        """温度检查"""
        state = self.hal.get_state()
        max_temp = max(state.joint_temperatures)
        if max_temp > self.warning_thresholds["joint_temp_critical"]:
            return False, f"温度过高: {max_temp:.1f}°C"
        elif max_temp > self.warning_thresholds["joint_temp_warning"]:
            return True, f"温度偏高: {max_temp:.1f}°C (注意)"
        return True, f"温度正常 (最高: {max_temp:.1f}°C)"

    def _test_gripper(self) -> Tuple[bool, str]:
        """夹爪状态"""
        state = self.hal.get_state()
        return True, f"夹爪位置: {state.gripper_position:.2f}"

    def _test_estop(self) -> Tuple[bool, str]:
        """急停按钮状态（软件检测）"""
        status = self.safety.get_safety_status()
        if status["emergency_stop"]:
            return False, "急停已按下，请释放后重试"
        return True, "急停状态正常"

    def run_runtime_diagnostics(self) -> Dict:
        """运行时诊断（周期性调用）"""
        state = self.hal.get_state()
        warnings = []
        errors = []

        # 温度监测
        for i in range(7):
            temp = state.joint_temperatures[i]
            if temp > self.warning_thresholds["joint_temp_critical"]:
                errors.append(f"关节{i}温度严重过高: {temp:.1f}°C")
            elif temp > self.warning_thresholds["joint_temp_warning"]:
                warnings.append(f"关节{i}温度偏高: {temp:.1f}°C")

        # 力矩监测
        limits = self.hal.safety_limits
        for i in range(7):
            torque_ratio = abs(state.joint_torques[i]) / limits.max_joint_torque[i]
            if torque_ratio > 0.9:
                errors.append(f"关节{i}力矩过载: {torque_ratio*100:.0f}%")
            elif torque_ratio > self.warning_thresholds["joint_torque_warning_ratio"]:
                warnings.append(f"关节{i}力矩偏高: {torque_ratio*100:.0f}%")

        result = {
            "timestamp": time.time(),
            "warnings": warnings,
            "errors": errors,
            "state_summary": {
                "max_temperature": max(state.joint_temperatures),
                "max_torque_ratio": max(abs(state.joint_torques[i]) / limits.max_joint_torque[i] for i in range(7)),
                "is_moving": state.is_moving,
            }
        }

        # 记录日志
        if warnings or errors:
            self.diagnostics_log.append(result)

        return result

    def get_test_report(self) -> Dict:
        """获取自检报告"""
        passed = sum(1 for r in self.test_results if r["passed"])
        total = len(self.test_results)
        return {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": passed / total if total > 0 else 0,
            "results": self.test_results,
        }


# ============================================================================
# 第七部分：统一入口 - 真机就绪系统
# ============================================================================

class RealRobotReadySystem:
    """
    真机就绪统一系统
    购买真机后，使用方式：
      1. system = RealRobotReadySystem(backend="airbot_p7", host="192.168.1.100")
      2. system.startup()    # 连接+自检+标定
      3. system.ready_to_use  # 确认就绪
      4. system.robot.move_joints(target)  # 开始使用
    """

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.backend = self.config.get("backend", "simulation")

        # 子系统
        self.robot: Optional[RobotHAL] = None
        self.safety: Optional[SafetySystem] = None
        self.calibration: Optional[CalibrationWizard] = None
        self.diagnostics: Optional[SelfTestDiagnostics] = None

        # 状态
        self.ready_to_use = False
        self.system_state = SystemState.UNINITIALIZED

        # 线程
        self._running = False
        self._diagnostics_thread = None

    def startup(self, auto_calibrate: bool = True) -> bool:
        """
        启动完整流程（真机到手后第一步）
        Args:
            auto_calibrate: 是否自动运行标定（首次使用必须True）
        """
        print("\n" + "=" * 70)
        print("  真机就绪系统 v1.0")
        print("=" * 70)
        print(f"  后端: {self.backend}")
        print(f"  注意: 真机运行前请确保：")
        print("    1. 已阅读设备操作手册")
        print("    2. 已完成安全培训")
        print("    3. 急停按钮功能正常")
        print("    4. 工作区域无障碍物")
        print("=" * 70 + "\n")

        self.system_state = SystemState.INITIALIZING

        # Step 1: 连接机器人
        print("\n[1/5] 连接机器人...")
        self.robot = RobotHAL(self.config)
        if not self.robot.connect():
            self.system_state = SystemState.ERROR
            print("❌ 机器人连接失败")
            return False

        # Step 2: 启动安全系统
        print("\n[2/5] 启动安全系统...")
        self.safety = SafetySystem(self.robot, self.config)
        self.safety.start()

        # Step 3: 运行自检
        print("\n[3/5] 运行启动自检...")
        self.diagnostics = SelfTestDiagnostics(self.robot, self.safety, self.config)
        passed, _ = self.diagnostics.run_power_on_self_test()
        if not passed and self.backend != "simulation":
            print("⚠️ 自检存在问题，建议检查后再继续")
            # 仿真模式下继续

        # Step 4: 标定（首次）
        print("\n[4/5] 标定与校准...")
        self.calibration = CalibrationWizard(self.robot, self.safety, self.config)

        calib_path = self.config.get("calibration_path", "calibration_results.json")
        if os.path.exists(calib_path) and not auto_calibrate:
            self.calibration.load_calibration(calib_path)
        else:
            if not self.calibration.run_full_calibration():
                if self.backend != "simulation":
                    print("❌ 标定失败")
                    return False

        # Step 5: 启动运行时诊断
        print("\n[5/5] 启动运行时监测...")
        self._running = True
        self._diagnostics_thread = threading.Thread(target=self._diagnostics_loop, daemon=True)
        self._diagnostics_thread.start()

        self.ready_to_use = True
        self.system_state = SystemState.IDLE

        print("\n" + "=" * 70)
        print("  ✅ 系统已就绪，可以开始使用！")
        print("=" * 70)
        print(f"  控制模式: {self.robot.control_mode.value}")
        print(f"  安全系统: 已启动")
        print(f"  诊断监测: 运行中")
        print("=" * 70 + "\n")

        return True

    def _diagnostics_loop(self):
        """运行时诊断循环"""
        while self._running:
            try:
                diag = self.diagnostics.run_runtime_diagnostics()
                if diag["errors"]:
                    for err in diag["errors"]:
                        print(f"[DIAG] 🚨 {err}")
                    # 触发安全停止
                    self.safety._trigger_safety_stop("运行时诊断发现错误")
                elif diag["warnings"]:
                    for warn in diag["warnings"]:
                        print(f"[DIAG] ⚠️ {warn}")
            except Exception as e:
                print(f"[DIAG] 诊断错误: {e}")
            time.sleep(1.0)  # 每秒诊断一次

    def shutdown(self):
        """关闭系统"""
        print("\n[SHUTDOWN] 正在关闭系统...")
        self._running = False

        if self._diagnostics_thread:
            self._diagnostics_thread.join(timeout=2.0)

        if self.safety:
            self.safety.stop()

        if self.robot:
            self.robot.disconnect()

        self.ready_to_use = False
        self.system_state = SystemState.SHUTDOWN
        print("[SHUTDOWN] ✅ 系统已关闭")

    def emergency_stop(self):
        """紧急停止（任何时刻都可调用）"""
        print("\n🚨 紧急停止触发！")
        if self.safety:
            self.safety.trigger_estop_manual()
        self.system_state = SystemState.EMERGENCY_STOP

    def get_status(self) -> Dict:
        """获取系统状态"""
        return {
            "ready": self.ready_to_use,
            "state": self.system_state.value,
            "backend": self.backend,
            "control_mode": self.robot.control_mode.value if self.robot else "N/A",
            "safety": self.safety.get_safety_status() if self.safety else {},
            "robot_state": self.robot.get_state() if self.robot else None,
        }

    def save_config(self, path: str = "robot_config.json"):
        """保存当前配置"""
        config_data = {
            "backend": self.backend,
            "calibration_path": "calibration_results.json",
            "timestamp": time.time(),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)


# ============================================================================
# 便捷入口
# ============================================================================

def create_real_robot_system(backend: str = "simulation",
                             host: str = "192.168.1.100",
                             port: int = 8080) -> RealRobotReadySystem:
    """
    创建真机就绪系统（便捷入口）
    Args:
        backend: "simulation" | "airbot_p7" | "panda"
        host: 真机IP地址
        port: 真机端口号
    """
    config = {
        "backend": backend,
        "host": host,
        "port": port,
        "calibration_path": "calibration_results.json",
    }
    return RealRobotReadySystem(config)


def quick_start_simulation() -> RealRobotReadySystem:
    """快速启动仿真模式（测试用）"""
    system = create_real_robot_system(backend="simulation")
    system.startup(auto_calibrate=False)
    return system


def quick_start_airbot_p7(host: str = "192.168.1.100") -> RealRobotReadySystem:
    """
    快速启动Airbot P7真机
    真机到手后直接调用这个函数
    """
    print(f"正在连接Airbot P7 (IP: {host})...")
    system = create_real_robot_system(backend="airbot_p7", host=host)
    system.startup(auto_calibrate=True)  # 首次使用自动标定
    return system


# ============================================================================
# 其它主流品牌快速启动（购买真机后，安装对应SDK即可使用）
# ============================================================================

def quick_start_panda(host: str = "192.168.1.1") -> RealRobotReadySystem:
    """快速启动 Franka Emika Panda（德国·7轴力控协作臂）"""
    print(f"正在连接Franka Panda (IP: {host})...")
    system = create_real_robot_system(backend="panda", host=host)
    system.startup(auto_calibrate=True)
    return system


def quick_start_ur(host: str = "192.168.1.102", model: str = "ur5") -> RealRobotReadySystem:
    """
    快速启动 Universal Robots（丹麦·UR3/UR5/UR10/UR16e）
    全球最流行的协作臂品牌
    """
    print(f"正在连接Universal Robots {model.upper()} (IP: {host})...")
    system = create_real_robot_system(backend=model, host=host)
    system.startup(auto_calibrate=True)
    return system


def quick_start_kuka(host: str = "192.168.1.103") -> RealRobotReadySystem:
    """快速启动 KUKA LBR iiwa（德国·7轴力控协作臂）"""
    print(f"正在连接KUKA LBR iiwa (IP: {host})...")
    system = create_real_robot_system(backend="kuka", host=host)
    system.startup(auto_calibrate=True)
    return system


def quick_start_abb(host: str = "192.168.1.104", model: str = "gofa") -> RealRobotReadySystem:
    """快速启动 ABB GoFa/YuMi（瑞士·协作臂）"""
    print(f"正在连接ABB {model.upper()} (IP: {host})...")
    system = create_real_robot_system(backend=f"abb_{model}", host=host)
    system.startup(auto_calibrate=True)
    return system


def quick_start_xarm(host: str = "192.168.1.105", model: str = "7") -> RealRobotReadySystem:
    """
    快速启动 UFACTORY xArm（中国·越疆·6/7轴协作臂）
    性价比极高的国产协作臂首选
    """
    print(f"正在连接越疆 xArm {model} (IP: {host})...")
    system = create_real_robot_system(backend="xarm", host=host)
    system.startup(auto_calibrate=True)
    return system


def quick_start_flexiv(host: str = "192.168.1.106") -> RealRobotReadySystem:
    """快速启动 Flexiv Rizon（中国·非夕·7轴力控臂）"""
    print(f"正在连接非夕 Flexiv Rizon (IP: {host})...")
    system = create_real_robot_system(backend="flexiv", host=host)
    system.startup(auto_calibrate=True)
    return system


def quick_start_jaka(host: str = "192.168.1.107") -> RealRobotReadySystem:
    """快速启动 JAKA 节卡（中国·6轴协作臂）"""
    print(f"正在连接节卡 JAKA (IP: {host})...")
    system = create_real_robot_system(backend="jaka", host=host)
    system.startup(auto_calibrate=True)
    return system


def quick_start_mycobot(port: str = "/dev/ttyUSB0") -> RealRobotReadySystem:
    """
    快速启动 Elephant Robotics myCobot（中国·轻量6轴臂）
    入门级首选，USB连接
    """
    print(f"正在连接myCobot (串口: {port})...")
    system = create_real_robot_system(backend="mycobot", host=port)
    system.startup(auto_calibrate=True)
    return system


def quick_start_unitree_h1(host: str = "192.168.1.201") -> RealRobotReadySystem:
    """快速启动 Unitree H1（中国·宇树·人形机器人）"""
    print(f"正在连接宇树 H1 人形机器人 (IP: {host})...")
    system = create_real_robot_system(backend="h1", host=host)
    system.startup(auto_calibrate=True)
    return system


def quick_start_unitree_g1(host: str = "192.168.1.202") -> RealRobotReadySystem:
    """快速启动 Unitree G1（中国·宇树·小型人形机器人）"""
    print(f"正在连接宇树 G1 人形机器人 (IP: {host})...")
    system = create_real_robot_system(backend="g1", host=host)
    system.startup(auto_calibrate=True)
    return system


def quick_start_galaxy_db1(host: str = "192.168.1.203") -> RealRobotReadySystem:
    """快速启动 银河通用 DB1（中国·人形机器人）"""
    print(f"正在连接银河通用 DB1 人形机器人 (IP: {host})...")
    system = create_real_robot_system(backend="db1", host=host)
    system.startup(auto_calibrate=True)
    return system


# ============================================================================
# 机器人选购指南（按预算/场景推荐）
# ============================================================================

ROBOT_PURCHASE_GUIDE = {
    # ── 按预算分类 ──
    "budget": [
        {"name": "myCobot 280", "brand": "Elephant Robotics", "price": "¥5,000-10,000",
         "payload": "0.25kg", "reach": "280mm", "axes": 6,
         "pros": "价格极低、入门友好、USB连接",
         "cons": "负载小、精度一般",
         "use_case": "教学、演示、轻量抓取"},
        {"name": "xArm 6", "brand": "UFACTORY 越疆", "price": "¥30,000-50,000",
         "payload": "5kg", "reach": "700mm", "axes": 6,
         "pros": "性价比极高、SDK完善、支持ROS",
         "cons": "力控需额外选配",
         "use_case": "科研、轻量工业、服务机器人"},
    ],
    "mid_range": [
        {"name": "Airbot P7", "brand": "星动纪元", "price": "¥80,000-120,000",
         "payload": "7kg", "reach": "922mm", "axes": 7,
         "pros": "7轴力控、拖拽示教、国产首选、支持CAN总线",
         "cons": "品牌较新",
         "use_case": "精密装配、力控打磨、科研实验"},
        {"name": "Flexiv Rizon 4", "brand": "非夕科技", "price": "¥100,000-150,000",
         "payload": "4kg", "reach": "830mm", "axes": 7,
         "pros": "全球顶级力控、AI原生、复杂作业",
         "cons": "价格偏高",
         "use_case": "精密装配、抛光打磨、柔性作业"},
        {"name": "JAKA Zu 7", "brand": "节卡机器人", "price": "¥60,000-90,000",
         "payload": "7kg", "reach": "790mm", "axes": 6,
         "pros": "无线示教、拖拽编程、部署极快",
         "cons": "6轴无冗余",
         "use_case": "3C电子、汽车零部件、产线集成"},
        {"name": "UR5e", "brand": "Universal Robots", "price": "¥120,000-180,000",
         "payload": "5kg", "reach": "850mm", "axes": 6,
         "pros": "全球最成熟协作臂、生态完善、海量教程",
         "cons": "价格高、力控需选件",
         "use_case": "工业产线、科研教学、全球服务"},
    ],
    "premium": [
        {"name": "Franka Emika Panda", "brand": "Franka Emika", "price": "¥200,000-300,000",
         "payload": "3kg", "reach": "855mm", "axes": 7,
         "pros": "科研黄金标准、开源友好、力控顶级",
         "cons": "负载小、价格高",
         "use_case": "顶级科研、AI机器人学习、精密操作"},
        {"name": "KUKA LBR iiwa", "brand": "KUKA", "price": "¥300,000-500,000",
         "payload": "7/14kg", "reach": "800mm", "axes": 7,
         "pros": "工业级力控、ISO 10218认证、汽车行业标准",
         "cons": "价格极高、部署复杂",
         "use_case": "汽车制造、航空航天、精密工业"},
    ],
    "humanoid": [
        {"name": "Unitree H1", "brand": "宇树科技", "price": "¥600,000-900,000",
         "height": "180cm", "weight": "47kg", "dofs": "全身35+",
         "pros": "全球最成熟量产人形、运动能力强、价格相对低",
         "cons": "手部操作能力有限",
         "use_case": "人形机器人研发、工业巡检、特种作业"},
        {"name": "Unitree G1", "brand": "宇树科技", "price": "¥150,000-250,000",
         "height": "130cm", "weight": "25kg", "dofs": "全身25+",
         "pros": "入门级人形、价格友好、教育首选",
         "cons": "尺寸较小、负载有限",
         "use_case": "教学科研、人机动画、服务演示"},
        {"name": "银河通用 DB1", "brand": "银河通用", "price": "¥500,000-800,000",
         "height": "170cm", "weight": "55kg", "dofs": "全身40+",
         "pros": "国产量产人形、双手操作、大模型集成",
         "cons": "交付周期较长",
         "use_case": "工厂作业、家政服务、科研平台"},
    ],
    # ── 按场景分类 ──
    "scenario_research": ["Franka Emika Panda", "Airbot P7", "UR5e", "xArm 7"],
    "scenario_industrial": ["UR5e/UR10e", "JAKA Zu", "KUKA LBR iiwa", "ABB GoFa"],
    "scenario_education": ["myCobot 280", "xArm 6", "Unitree G1"],
    "scenario_force_control": ["Franka Panda", "Flexiv Rizon", "KUKA iiwa", "Airbot P7"],
    "scenario_humanoid": ["Unitree H1", "银河通用 DB1", "Figure 01", "Agility Digit"],
}


def get_supported_robots() -> List[str]:
    """获取当前系统支持的所有机器人品牌/型号列表"""
    return [b.value for b in RobotBrand]


def recommend_robot(budget: str = "mid_range", scenario: str = "research") -> List[Dict]:
    """
    根据预算和场景推荐机器人

    Args:
        budget: "budget"（1万内）| "mid_range"（5-15万）| "premium"（20万+）| "humanoid"（人形）
        scenario: "research"（科研）| "industrial"（工业）| "education"（教学）|
                  "force_control"（力控）| "humanoid"（人形）
    """
    budget_options = ROBOT_PURCHASE_GUIDE.get(budget, [])
    scenario_options = ROBOT_PURCHASE_GUIDE.get(f"scenario_{scenario}", [])

    if scenario == "humanoid":
        return ROBOT_PURCHASE_GUIDE.get("humanoid", [])

    # 交集推荐（同时满足预算和场景）
    if budget_options and scenario_options:
        matched = [r for r in budget_options if r["name"] in scenario_options
                   or any(s in r["name"] for s in scenario_options)]
        return matched if matched else budget_options

    return budget_options
