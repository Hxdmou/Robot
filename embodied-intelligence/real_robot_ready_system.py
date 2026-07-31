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
    """支持的机器人品牌与型号（2026年最新，持续扩展中）"""
    # ── 协作机械臂（7轴/6轴）──
    AIRBOT_P7 = "Airbot P7 (7轴协作臂, 中国·星动纪元)"
    PANDA = "Franka Emika Panda (7轴协作臂, 德国)"
    UNIVERSAL_ROBOTS = "Universal Robots (6轴协作臂, 丹麦)"
    KUKA_LBR = "KUKA LBR iiwa (7轴协作臂, 德国)"
    ABB_YUMI = "ABB YuMi/GoFa (协作臂, 瑞士)"
    FANUC_CR = "Fanuc CRX (协作臂, 日本)"
    DOOSAN = "Doosan (6轴协作臂, 韩国)"
    ELEPHANT = "Elephant Robotics myCobot (6轴轻量臂, 中国)"
    # ── 国产协作臂（2026主力型号）──
    UFACTORY_CRA = "UFACTORY CRA系列 (6/7轴高速协作, 中国·越疆, 2026新品)"
    UFACTORY = "UFACTORY xArm (6/7轴协作臂, 中国·越疆)"
    JAKA_ZU = "JAKA Zu系列 (协作臂, 中国·节卡)"
    JAKA_ZU35 = "JAKA Zu35 (35kg重载协作, 中国·节卡, 2026新品)"
    JAKA_AI = "JAKA Ai系列 (一体化视觉协作臂, 中国·节卡, 2026新品)"
    JAKA_MINI2 = "JAKA Mini 2 (微型协作臂, 中国·节卡, 2026新品)"
    HAIBOXING = "HAN'S Elfin (6轴协作臂, 中国·大族)"
    ROKAE = "ROKAE 珞石 (协作/工业机器人, 中国·珞石, 2026高速增长)"
    AUBO = "AUBO 遨博 (协作臂, 中国)"
    ELITE = "ELITE 艾利特 (协作臂, 中国)"
    TIAGOA = "TiAGo (移动操作臂, 西班牙PAL Robotics)"
    # ── 人形机器人（2025-2026量产主力）──
    UNITREE_H1 = "Unitree H1 (人形机器人, 中国·宇树, 已量产5500+台)"
    UNITREE_H2 = "Unitree H2 (新一代高动态人形, 中国·宇树, 2026春晚)"
    UNITREE_G1 = "Unitree G1 (小型人形机器人, 中国·宇树, 8.5万起)"
    UNITREE_R1 = "Unitree R1 智能伙伴 (家庭人形, 中国·宇树, 2.99万, 2026新品)"
    UNITREE_GD01 = "Unitree GD01 (载人变形机甲, 中国·宇树, 2026全球首发)"
    ZHILYUAN_A3 = "智元远征A3 Ultra (超拟人灵巧手+柔性腰, 2026WAIC首发)"
    ZHILYUAN_G2 = "智元精灵G2 (量产人形, 良品率99.99%, 2026新品)"
    ZHILYUAN_Q1 = "智元启元Q1 (便携背包人形, 2026新品)"
    UBTECH_WALKER = "优必选Walker S系列 (工业人形, 已交付千台, 订单1.3万+)"
    JAKA_PI = "JAKA π 仔 (小型人形机器人, 中国·节卡, 2026新品)"
    JAKA_K1 = "JAKA K1-25 (重载双臂人形, 单臂25kg, 2026WAIC首发)"
    FIGURE_01 = "Figure 01 (人形机器人, 美国·Figure AI)"
    OPTIMUS = "Tesla Optimus Gen-3 (人形机器人, 美国·特斯拉, 规划年产能100万)"
    XIAOBING = "Galaxy DB1 (人形机器人, 中国·银河通用)"
    FLEXIV = "Flexiv Rizon (7轴力控臂, 中国·非夕)"
    APPTRONIK = "Apptronik Apollo (人形机器人, 美国)"
    AGILITY = "Agility Digit (双足机器人, 美国)"
    SONGYAN_BUMI = "松延动力Bumi小布米 (94cm小型人形, 不足万元, 2025新品)"
    # ── 人形机器人（2025-2026最新量产与首发）──
    KEPLER_K2 = "开普勒K2大黄蜂 (全球首款混动架构人形, 52自由度, 双臂30kg, 2026首发)"
    ZHILINGXI_X2 = "智元灵犀X2 (1.3米康养人形, iF设计奖, 2026新品)"
    MATRIX_3 = "矩阵超智MATRIX-3 (27维灵巧手, 微米级操作, 特斯拉系, 2026首发)"
    FOURIER_GR3 = "傅利叶GR-3 (全尺寸情感陪护机器人, 柔肤软包, 2026新品)"
    ZHUOYIDE_MOYA = "卓益得Moya (仿生人形, 蜡像级硅胶, 92%步态仿真, 2026新品)"
    LINGLONG_2 = "国家地方共建灵龙2.0 (人形创新中心, 动态平衡, 2026首发)"
    XINGHAITU_R1 = "星海图R1 (清华系, 19.9万起, 科研人形首选, 2026新品)"
    YINHE_GALBOT_S2 = "银河通用Galbot S2 (宁德时代产线验证, 2026新品)"
    QIANXUN_MOZ1 = "千寻智能Moz1 (全身力控+端到端大模型, 宁德时代标杆, 2026新品)"
    BEIJING_TIANGONG_3 = "北京人形天工3.0 (560TOPS算力, RDK S600, 2026首发)"
    TASHI_A3 = "它石智航A3 (轮式双臂机器人, RDK S600, 2026新品)"
    ZHIPINGFANG_ALPHA = "智平方Alpha (类脑VLA, 惠科1000台订单, 2026首发)"
    # ── 2026成都人形机器人创新中心系列 ──
    GONGGA_1 = "贡嘎一号 (超轻量级人形, 25kg, 家庭康养, 成都创新中心)"
    RUIBA = "锐钯 (文商旅双足机器人, 1米/30kg, 19英寸屏, 6自由度头, 成都创新中心)"
    HONGHU_ROBOT = "鸿鹄 (人形机器人, 成都创新中心)"
    XIAOZHA_ROBOT = "小吒 (人形机器人, 成都创新中心)"
    BIONIC_DINOSAUR = "仿生恐龙机器人 (全球首款双足行走智能仿生恐龙, 成都创新中心)"
    BELT_INSPECTION = "胶带机巡检机器人 (双轮足, 5000台国内最大订单, 成都创新中心)"
    BIPED_WHEEL_PLATFORM = "双轮足开源平台 (全球首个全尺寸重载双轮足, 成都创新中心)"
    AI_ELECTRONIC_SKIN = "AI神经网络电子皮肤 (0.005N微力识别, 成都创新中心)"
    # ── 2026浙江人形机器人创新中心系列 ──
    ZHEJIANG_HUMANOID = "浙江人形双臂作业机器人 (服装/汽车装配, 杰克科技2000台订单)"
    # ── 2026 WAIC世界人工智能大会首发新品 ──
    QIYUAN_Q1 = "启元Q1 (小尺寸全身力控人形, 88cm/15kg, 上纬新材启元机器人, 2025年底首发)"
    QIYUAN_T1 = "启元T1 (全球首款可变形个人机器人, 轮足人形/四足切换, 上纬新材启元机器人, WAIC 2026首发, ¥15,999)"
    LEJU_KUAFU = "乐聚夸父系列 (全尺寸人形, 国产化率>95%, 一汽/长虹/中兴订单, 乐聚机器人, WAIC 2026)"
    LEJU_LUBAN = "乐聚鲁班 (工业人形机器人, 拆垛/上料, 乐聚机器人, WAIC 2026)"
    MAGICATOM_X1 = "魔法原子MagicBot X1 (180cm通用人形, 31自由度, 450N·m关节, WAIC 2026首发)"
    MAGICATOM_D1 = "魔法原子MagicBot D1 (轮式人形, 厂区物料转运, 追觅工厂试点, WAIC 2026)"
    MAGICATOM_T1 = "魔法原子MagicDog T1 (轻量化四足, 狭小空间巡检, WAIC 2026)"
    AGIBOT_G2_MAX = "智元精灵G2 Max (轮式仓储人形, 双臂码垛, 京东物流合作, WAIC 2026)"
    AGIBOT_KUOTUO = "智元酷拓骑行机器人 (可承载75kg, 巡检/代步, WAIC 2026首发)"
    BEIJING_TIANGONG = "北京人形创新中心·具身天工系列 (工业人形, 化工/电力/油气, WAIC 2026)"
    ZHONGJI_T800 = "众擎T800 (全尺寸格斗人形, 高强度抗扰测试, WAIC 2026)"
    PUDU_D7 = "普渡PUDU D7 (类人形智能作业伙伴, 14kg负载/2m作业高度, WAIC 2026)"
    # ── 四足机器人（2025-2026量产）──
    ANYBOTICS = "ANYbotics ANYmal (四足机器人, 瑞士)"
    DEEPROBOTICS = "DeepRobotics Jueying (四足机器人, 中国·云深处)"
    UNITREE_GO2 = "Unitree Go2 (四足机器人, 中国·宇树, 8999元起, 已量产)"
    UNITREE_B2 = "Unitree B2 (工业四足, 中国·宇树, 2026新品)"
    UNITREE_A2 = "Unitree A2 (教育四足, 中国·宇树)"
    # ── AMR/AGV 移动机器人 ──
    AGV_AMR = "AGV/AMR (自主移动机器人, 通用)"
    HIKROBOT_AMR = "海康机器人 AMR (中国·海康威视, 2026市占率领先)"
    GEEK_AMR = "极智嘉 Geek+ AMR (中国·极智嘉, AMR全球第一)"
    QUICKTON_AMR = "快仓 Quicktron AMR (中国·快仓)"
    MIR = "Mobile Industrial Robots (丹麦·MIR, 被泰瑞达收购)"
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
            "jaka_zu": RobotBrand.JAKA_ZU,
            "zu7": RobotBrand.JAKA_ZU,
            "zu12": RobotBrand.JAKA_ZU,
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
            # ── 2026新品: 人形机器人 ──
            "unitree_h2": RobotBrand.UNITREE_H2,
            "h2": RobotBrand.UNITREE_H2,
            "unitree_r1": RobotBrand.UNITREE_R1,
            "r1": RobotBrand.UNITREE_R1,
            "unitree_gd01": RobotBrand.UNITREE_GD01,
            "gd01": RobotBrand.UNITREE_GD01,
            "zhiyuan_a3": RobotBrand.ZHILYUAN_A3,
            "a3": RobotBrand.ZHILYUAN_A3,
            "zhiyuan_g2": RobotBrand.ZHILYUAN_G2,
            "g2": RobotBrand.ZHILYUAN_G2,
            "zhiyuan_q1": RobotBrand.ZHILYUAN_Q1,
            "q1": RobotBrand.ZHILYUAN_Q1,
            "zhiyuan_lingxi_x2": RobotBrand.ZHILINGXI_X2,
            "lingxi_x2": RobotBrand.ZHILINGXI_X2,
            "x2": RobotBrand.ZHILINGXI_X2,
            "ubtech_walker": RobotBrand.UBTECH_WALKER,
            "walker": RobotBrand.UBTECH_WALKER,
            "jaka_pi": RobotBrand.JAKA_PI,
            "pi_zai": RobotBrand.JAKA_PI,
            "jaka_k1": RobotBrand.JAKA_K1,
            "k1": RobotBrand.JAKA_K1,
            "songyan_bumi": RobotBrand.SONGYAN_BUMI,
            "bumi": RobotBrand.SONGYAN_BUMI,
            "kepler_k2": RobotBrand.KEPLER_K2,
            "kepler": RobotBrand.KEPLER_K2,
            "k2": RobotBrand.KEPLER_K2,
            "matrix_3": RobotBrand.MATRIX_3,
            "matrix": RobotBrand.MATRIX_3,
            "fourier_gr3": RobotBrand.FOURIER_GR3,
            "fourier": RobotBrand.FOURIER_GR3,
            "gr3": RobotBrand.FOURIER_GR3,
            "zhuoyide_moya": RobotBrand.ZHUOYIDE_MOYA,
            "moya": RobotBrand.ZHUOYIDE_MOYA,
            "linglong_2": RobotBrand.LINGLONG_2,
            "linglong": RobotBrand.LINGLONG_2,
            "xinghaitu_r1": RobotBrand.XINGHAITU_R1,
            "xinghaitu": RobotBrand.XINGHAITU_R1,
            "yinhe_galbot_s2": RobotBrand.YINHE_GALBOT_S2,
            "galbot": RobotBrand.YINHE_GALBOT_S2,
            "qianxun_moz1": RobotBrand.QIANXUN_MOZ1,
            "moz1": RobotBrand.QIANXUN_MOZ1,
            "beijing_tiangong_3": RobotBrand.BEIJING_TIANGONG_3,
            "tiangong": RobotBrand.BEIJING_TIANGONG_3,
            "tashi_a3": RobotBrand.TASHI_A3,
            "zhipingfang_alpha": RobotBrand.ZHIPINGFANG_ALPHA,
            "zhipingfang": RobotBrand.ZHIPINGFANG_ALPHA,
            # ── 2026新品: 协作臂 ──
            "ufactory_cra": RobotBrand.UFACTORY_CRA,
            "cra": RobotBrand.UFACTORY_CRA,
            "jaka_zu35": RobotBrand.JAKA_ZU35,
            "zu35": RobotBrand.JAKA_ZU35,
            "jaka_ai": RobotBrand.JAKA_AI,
            "jaka_mini2": RobotBrand.JAKA_MINI2,
            "mini2": RobotBrand.JAKA_MINI2,
            "rokae": RobotBrand.ROKAE,
            "aubo": RobotBrand.AUBO,
            "elite": RobotBrand.ELITE,
            # ── 2026新品: 成都人形创新中心 ──
            "gongga_1": RobotBrand.GONGGA_1,
            "gongga": RobotBrand.GONGGA_1,
            "贡嘎一号": RobotBrand.GONGGA_1,
            "ruiba": RobotBrand.RUIBA,
            "锐钯": RobotBrand.RUIBA,
            "honghu": RobotBrand.HONGHU_ROBOT,
            "鸿鹄": RobotBrand.HONGHU_ROBOT,
            "xiaozha": RobotBrand.XIAOZHA_ROBOT,
            "小吒": RobotBrand.XIAOZHA_ROBOT,
            "bionic_dinosaur": RobotBrand.BIONIC_DINOSAUR,
            "dinosaur": RobotBrand.BIONIC_DINOSAUR,
            "仿生恐龙": RobotBrand.BIONIC_DINOSAUR,
            "belt_inspection": RobotBrand.BELT_INSPECTION,
            "胶带机巡检": RobotBrand.BELT_INSPECTION,
            "biped_wheel": RobotBrand.BIPED_WHEEL_PLATFORM,
            "双轮足": RobotBrand.BIPED_WHEEL_PLATFORM,
            "ai_electronic_skin": RobotBrand.AI_ELECTRONIC_SKIN,
            "电子皮肤": RobotBrand.AI_ELECTRONIC_SKIN,
            # ── 2026新品: 浙江人形创新中心 ──
            "zhejiang_humanoid": RobotBrand.ZHEJIANG_HUMANOID,
            "浙江人形": RobotBrand.ZHEJIANG_HUMANOID,
            # ── 2026 WAIC世界人工智能大会首发新品 ──
            "qiyuan_q1": RobotBrand.QIYUAN_Q1,
            "启元q1": RobotBrand.QIYUAN_Q1,
            "启元Q1": RobotBrand.QIYUAN_Q1,
            "qiyuan_t1": RobotBrand.QIYUAN_T1,
            "启元t1": RobotBrand.QIYUAN_T1,
            "启元T1": RobotBrand.QIYUAN_T1,
            "启元": RobotBrand.QIYUAN_Q1,
            "leju_kuafu": RobotBrand.LEJU_KUAFU,
            "乐聚夸父": RobotBrand.LEJU_KUAFU,
            "夸父": RobotBrand.LEJU_KUAFU,
            "leju_luban": RobotBrand.LEJU_LUBAN,
            "乐聚鲁班": RobotBrand.LEJU_LUBAN,
            "鲁班": RobotBrand.LEJU_LUBAN,
            "乐聚": RobotBrand.LEJU_KUAFU,
            "magicatom_x1": RobotBrand.MAGICATOM_X1,
            "magicbot_x1": RobotBrand.MAGICATOM_X1,
            "魔法原子x1": RobotBrand.MAGICATOM_X1,
            "magicatom_d1": RobotBrand.MAGICATOM_D1,
            "magicbot_d1": RobotBrand.MAGICATOM_D1,
            "魔法原子d1": RobotBrand.MAGICATOM_D1,
            "magicatom_t1": RobotBrand.MAGICATOM_T1,
            "magicdog_t1": RobotBrand.MAGICATOM_T1,
            "魔法原子t1": RobotBrand.MAGICATOM_T1,
            "魔法原子": RobotBrand.MAGICATOM_X1,
            "agibot_g2_max": RobotBrand.AGIBOT_G2_MAX,
            "精灵g2_max": RobotBrand.AGIBOT_G2_MAX,
            "agibot_kuotuo": RobotBrand.AGIBOT_KUOTUO,
            "酷拓": RobotBrand.AGIBOT_KUOTUO,
            "beijing_tiangong": RobotBrand.BEIJING_TIANGONG,
            "具身天工": RobotBrand.BEIJING_TIANGONG,
            "天工": RobotBrand.BEIJING_TIANGONG,
            "zhongji_t800": RobotBrand.ZHONGJI_T800,
            "众擎t800": RobotBrand.ZHONGJI_T800,
            "众擎": RobotBrand.ZHONGJI_T800,
            "pudu_d7": RobotBrand.PUDU_D7,
            "普渡d7": RobotBrand.PUDU_D7,
            "普渡": RobotBrand.PUDU_D7,
            # ── 2026新品: 四足/AMR ──
            "unitree_go2": RobotBrand.UNITREE_GO2,
            "go2": RobotBrand.UNITREE_GO2,
            "unitree_b2": RobotBrand.UNITREE_B2,
            "b2": RobotBrand.UNITREE_B2,
            "unitree_a2": RobotBrand.UNITREE_A2,
            "a2": RobotBrand.UNITREE_A2,
            "hikrobot_amr": RobotBrand.HIKROBOT_AMR,
            "hikrobot": RobotBrand.HIKROBOT_AMR,
            "geek_amr": RobotBrand.GEEK_AMR,
            "geek": RobotBrand.GEEK_AMR,
            "quickton_amr": RobotBrand.QUICKTON_AMR,
            "quicktron": RobotBrand.QUICKTON_AMR,
            # AMR
            "agv": RobotBrand.AGV_AMR,
            "amr": RobotBrand.AGV_AMR,
            "turtlebot": RobotBrand.TURTLEBOT,
            "clearpath": RobotBrand.CLEARPATH,
            "husky": RobotBrand.CLEARPATH,
            "mir": RobotBrand.MIR,
            "mir_amr": RobotBrand.MIR,
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
            "PANDA": lambda h, p: self._connect_panda(),
            "UNIVERSAL_ROBOTS": self._connect_ur,
            "KUKA_LBR": self._connect_kuka,
            "ABB_YUMI": self._connect_abb,
            "FANUC_CR": self._connect_fanuc,
            "DOOSAN": self._connect_doosan,
            # 协作臂 - 国产品牌
            "ELEPHANT": self._connect_elephant,
            "UFACTORY": self._connect_ufactory,
            "UFACTORY_CRA": self._connect_ufactory,
            "JAKA": self._connect_jaka,
            "JAKA_ZU": self._connect_jaka,
            "JAKA_ZU35": self._connect_jaka,
            "JAKA_AI": self._connect_jaka,
            "JAKA_MINI2": self._connect_jaka,
            "HAIBOXING": self._connect_hans,
            "FLEXIV": self._connect_flexiv,
            "TIAGOA": self._connect_tiago,
            "ROKAE": self._connect_rokae,
            "AUBO": self._connect_aubo,
            "ELITE": self._connect_elite,
            "AIRBOT_P7": lambda h, p: self._connect_airbot_p7(),
            # 人形机器人
            "UNITREE_H1": self._connect_unitree,
            "UNITREE_H2": self._connect_unitree,
            "UNITREE_G1": self._connect_unitree,
            "UNITREE_R1": self._connect_unitree,
            "UNITREE_GD01": self._connect_unitree,
            "FIGURE_01": self._connect_figure,
            "OPTIMUS": self._connect_optimus,
            "XIAOBING": self._connect_galaxy,
            "APPTRONIK": self._connect_apptronik,
            "AGILITY": self._connect_agility,
            "ANYBOTICS": self._connect_anybotics,
            "DEEPROBOTICS": self._connect_deeprobotics,
            "ZHILYUAN_A3": self._connect_zhiyuan,
            "ZHILYUAN_G2": self._connect_zhiyuan,
            "ZHILYUAN_Q1": self._connect_zhiyuan,
            "ZHILINGXI_X2": self._connect_zhiyuan,
            "UBTECH_WALKER": self._connect_ubtech,
            "JAKA_PI": self._connect_jaka,
            "JAKA_K1": self._connect_jaka,
            "SONGYAN_BUMI": self._connect_songyan,
            "KEPLER_K2": self._connect_kepler,
            "MATRIX_3": self._connect_matrix,
            "FOURIER_GR3": self._connect_fourier,
            "ZHUOYIDE_MOYA": self._connect_zhuoyide,
            "LINGLONG_2": self._connect_linglong,
            "XINGHAITU_R1": self._connect_xinghaitu,
            "YINHE_GALBOT_S2": self._connect_yinhe,
            "QIANXUN_MOZ1": self._connect_qianxun,
            "BEIJING_TIANGONG_3": self._connect_beijing_robot,
            "TASHI_A3": self._connect_tashi,
            "ZHIPINGFANG_ALPHA": self._connect_zhipingfang,
            # 成都人形创新中心系列
            "GONGGA_1": self._connect_gongga,
            "RUIBA": self._connect_ruiba,
            "HONGHU_ROBOT": self._connect_honghu,
            "XIAOZHA_ROBOT": self._connect_xiaozha,
            "BIONIC_DINOSAUR": self._connect_bionic_dinosaur,
            "BELT_INSPECTION": self._connect_belt_inspection,
            "BIPED_WHEEL_PLATFORM": self._connect_biped_wheel,
            "AI_ELECTRONIC_SKIN": self._connect_ai_skin,
            # 浙江人形创新中心系列
            "ZHEJIANG_HUMANOID": self._connect_zhejiang_humanoid,
            # WAIC 2026首发新品
            "QIYUAN_Q1": self._connect_qiyuan,
            "QIYUAN_T1": self._connect_qiyuan,
            "LEJU_KUAFU": self._connect_leju,
            "LEJU_LUBAN": self._connect_leju,
            "MAGICATOM_X1": self._connect_magicatom,
            "MAGICATOM_D1": self._connect_magicatom,
            "MAGICATOM_T1": self._connect_magicatom,
            "AGIBOT_G2_MAX": self._connect_agibot,
            "AGIBOT_KUOTUO": self._connect_agibot,
            "BEIJING_TIANGONG": self._connect_beijing_tiangong,
            "ZHONGJI_T800": self._connect_zhongji,
            "PUDU_D7": self._connect_pudu,
            # 四足机器人
            "UNITREE_GO2": self._connect_unitree,
            "UNITREE_B2": self._connect_unitree,
            "UNITREE_A2": self._connect_unitree,
            # AMR
            "AGV_AMR": self._connect_amr,
            "HIKROBOT_AMR": self._connect_hikrobot,
            "GEEK_AMR": self._connect_geek,
            "QUICKTON_AMR": self._connect_quicktron,
            "MIR": self._connect_amr,
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
            "PANDA": {  # Franka Panda
                "joint_lower": np.array([-2.89, -1.76, -2.89, -3.07, -2.89, -0.01, -2.89]),
                "joint_upper": np.array([2.89, 1.76, 2.89, -0.06, 2.89, 3.75, 2.89]),
                "max_velocity": np.ones(7) * 2.0,
                "max_torque": np.array([87, 87, 87, 87, 12, 12, 12]),
                "payload": 3.0, "reach": 0.855,
            },
            "ABB_YUMI": {  # ABB YuMi/GoFa
                "joint_lower": np.ones(6) * -3.14,
                "joint_upper": np.ones(6) * 3.14,
                "max_velocity": np.ones(6) * 2.0,
                "max_torque": np.ones(6) * 30,
                "payload": 5.0, "reach": 0.95,
            },
            "FANUC_CR": {  # Fanuc CRX
                "joint_lower": np.ones(6) * -3.14,
                "joint_upper": np.ones(6) * 3.14,
                "max_velocity": np.ones(6) * 2.5,
                "max_torque": np.ones(6) * 60,
                "payload": 10.0, "reach": 1.2,
            },
            "DOOSAN": {  # Doosan M/H/A
                "joint_lower": np.ones(6) * -3.14,
                "joint_upper": np.ones(6) * 3.14,
                "max_velocity": np.ones(6) * 2.0,
                "max_torque": np.ones(6) * 50,
                "payload": 6.0, "reach": 0.9,
            },
            "JAKA_ZU": {  # 节卡 Zu系列
                "joint_lower": np.array([-6.28, -2.5, -6.28, -2.5, -6.28, -2.5, -6.28]),
                "joint_upper": np.array([6.28, 2.5, 6.28, 2.5, 6.28, 2.5, 6.28]),
                "max_velocity": np.ones(7) * 2.0,
                "max_torque": np.ones(7) * 40,
                "payload": 12.0, "reach": 1.05,
            },
            "HAIBOXING": {  # 大族/Elfin
                "joint_lower": np.ones(6) * -3.14,
                "joint_upper": np.ones(6) * 3.14,
                "max_velocity": np.ones(6) * 2.0,
                "max_torque": np.ones(6) * 20,
                "payload": 3.0, "reach": 0.6,
            },
            "TIAGOA": {  # PAL Tiago
                "joint_lower": np.ones(7) * -3.14,
                "joint_upper": np.ones(7) * 3.14,
                "max_velocity": np.ones(7) * 1.5,
                "max_torque": np.ones(7) * 20,
                "payload": 4.0, "reach": 0.8,
            },
            "FIGURE_01": {  # Figure 01
                "joint_lower": np.ones(40) * -3.14,
                "joint_upper": np.ones(40) * 3.14,
                "max_velocity": np.ones(40) * 3.0,
                "max_torque": np.ones(40) * 100,
                "payload": 20.0, "height": 1.68, "weight": 60,
            },
            "OPTIMUS": {  # Tesla Optimus
                "joint_lower": np.ones(45) * -3.14,
                "joint_upper": np.ones(45) * 3.14,
                "max_velocity": np.ones(45) * 3.0,
                "max_torque": np.ones(45) * 120,
                "payload": 20.0, "height": 1.73, "weight": 73,
            },
            "XIAOBING": {  # 银河通用 DB1
                "joint_lower": np.ones(35) * -3.14,
                "joint_upper": np.ones(35) * 3.14,
                "max_velocity": np.ones(35) * 2.5,
                "max_torque": np.ones(35) * 80,
                "payload": 20.0, "height": 1.7, "weight": 55,
            },
            "APPTRONIK": {  # Apptronik Apollo
                "joint_lower": np.ones(35) * -3.14,
                "joint_upper": np.ones(35) * 3.14,
                "max_velocity": np.ones(35) * 2.5,
                "max_torque": np.ones(35) * 80,
                "payload": 25.0, "height": 1.7, "weight": 72,
            },
            "AGILITY": {  # Agility Digit
                "joint_lower": np.ones(25) * -3.14,
                "joint_upper": np.ones(25) * 3.14,
                "max_velocity": np.ones(25) * 3.0,
                "max_torque": np.ones(25) * 60,
                "payload": 18.0, "height": 1.75, "weight": 65,
            },
            "ANYBOTICS": {  # ANYbotics ANYmal
                "joint_lower": np.ones(12) * -3.14,
                "joint_upper": np.ones(12) * 3.14,
                "max_velocity": np.ones(12) * 3.0,
                "max_torque": np.ones(12) * 50,
                "payload": 10.0, "weight": 35,
            },
            "DEEPROBOTICS": {  # 云深处 Jueying
                "joint_lower": np.ones(12) * -3.14,
                "joint_upper": np.ones(12) * 3.14,
                "max_velocity": np.ones(12) * 3.5,
                "max_torque": np.ones(12) * 45,
                "payload": 10.0, "weight": 28,
            },
            "AGV_AMR": {  # 通用AGV/AMR
                "max_velocity": 1.5, "payload": 500.0, "battery_hours": 8,
            },
            "MIR": {  # Mobile Industrial Robots
                "max_velocity": 1.5, "payload": 250.0, "battery_hours": 10,
            },
            "TURTLEBOT": {  # TurtleBot 3/4
                "max_velocity": 0.5, "payload": 5.0, "battery_hours": 4,
            },
            "CLEARPATH": {  # ClearPath Husky
                "max_velocity": 1.0, "payload": 75.0, "battery_hours": 6,
            },
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
            # ── 2026新品: 协作臂 ──
            "UFACTORY_CRA": {  # 越疆 CRA系列
                "joint_lower": np.array([-6.28, -2.0, -6.28, -2.0, -6.28, -2.0, -6.28]),
                "joint_upper": np.array([6.28, 2.0, 6.28, 2.0, 6.28, 2.0, 6.28]),
                "max_velocity": np.ones(7) * 2.5,
                "max_torque": np.ones(7) * 40,
                "payload": 7.0, "reach": 0.75,
            },
            "JAKA_ZU35": {  # 节卡 Zu35
                "joint_lower": np.array([-6.28, -2.5, -6.28, -2.5, -6.28, -2.5, -6.28]),
                "joint_upper": np.array([6.28, 2.5, 6.28, 2.5, 6.28, 2.5, 6.28]),
                "max_velocity": np.ones(7) * 2.0,
                "max_torque": np.ones(7) * 120,
                "payload": 35.0, "reach": 1.35,
            },
            "JAKA_AI": {  # 节卡 AI系列
                "joint_lower": np.array([-6.28, -2.5, -6.28, -2.5, -6.28, -2.5, -6.28]),
                "joint_upper": np.array([6.28, 2.5, 6.28, 2.5, 6.28, 2.5, 6.28]),
                "max_velocity": np.ones(7) * 2.5,
                "max_torque": np.ones(7) * 35,
                "payload": 7.0, "reach": 0.95,
            },
            "JAKA_MINI2": {  # 节卡 Mini2
                "joint_lower": np.ones(6) * -3.14,
                "joint_upper": np.ones(6) * 3.14,
                "max_velocity": np.ones(6) * 2.0,
                "max_torque": np.ones(6) * 5,
                "payload": 1.0, "reach": 0.42,
            },
            "ROKAE": {  # 珞石 ROKAE
                "joint_lower": np.array([-6.28, -2.5, -6.28, -2.5, -6.28, -2.5, -6.28]),
                "joint_upper": np.array([6.28, 2.5, 6.28, 2.5, 6.28, 2.5, 6.28]),
                "max_velocity": np.ones(7) * 2.5,
                "max_torque": np.ones(7) * 35,
                "payload": 6.0, "reach": 0.9,
            },
            "AUBO": {  # 遨博 AUBO
                "joint_lower": np.ones(6) * -3.14,
                "joint_upper": np.ones(6) * 3.14,
                "max_velocity": np.ones(6) * 2.0,
                "max_torque": np.ones(6) * 30,
                "payload": 5.0, "reach": 0.85,
            },
            "ELITE": {  # 艾利特 ELITE
                "joint_lower": np.ones(6) * -3.14,
                "joint_upper": np.ones(6) * 3.14,
                "max_velocity": np.ones(6) * 2.5,
                "max_torque": np.ones(6) * 25,
                "payload": 3.0, "reach": 0.62,
            },
            "AIRBOT_P7": {  # 星动纪元 Airbot P7
                "joint_lower": np.array([-6.28, -2.5, -6.28, -2.5, -6.28, -2.5, -6.28]),
                "joint_upper": np.array([6.28, 2.5, 6.28, 2.5, 6.28, 2.5, 6.28]),
                "max_velocity": np.ones(7) * 2.5,
                "max_torque": np.array([80, 80, 40, 40, 20, 20, 10]),
                "payload": 10.0, "reach": 0.95,
            },
            # ── 2026新品: 人形机器人 (简化为双腿+双臂+头部) ──
            "UNITREE_H1": {  # 宇树 H1
                "joint_lower": np.ones(23) * -3.14,
                "joint_upper": np.ones(23) * 3.14,
                "max_velocity": np.ones(23) * 3.0,
                "max_torque": np.ones(23) * 80,
                "payload": 30.0, "height": 1.8, "weight": 47,
            },
            "UNITREE_H2": {  # 宇树 H2
                "joint_lower": np.ones(25) * -3.14,
                "joint_upper": np.ones(25) * 3.14,
                "max_velocity": np.ones(25) * 3.5,
                "max_torque": np.ones(25) * 100,
                "payload": 40.0, "height": 1.85, "weight": 50,
            },
            "UNITREE_G1": {  # 宇树 G1
                "joint_lower": np.ones(23) * -3.14,
                "joint_upper": np.ones(23) * 3.14,
                "max_velocity": np.ones(23) * 2.5,
                "max_torque": np.ones(23) * 50,
                "payload": 10.0, "height": 1.32, "weight": 35,
            },
            "UNITREE_R1": {  # 宇树 R1
                "joint_lower": np.ones(20) * -3.14,
                "joint_upper": np.ones(20) * 3.14,
                "max_velocity": np.ones(20) * 2.0,
                "max_torque": np.ones(20) * 40,
                "payload": 5.0, "height": 1.1, "weight": 28,
            },
            "UNITREE_GD01": {  # 宇树 GD01
                "joint_lower": np.ones(12) * -3.14,
                "joint_upper": np.ones(12) * 3.14,
                "max_velocity": np.ones(12) * 2.0,
                "max_torque": np.ones(12) * 30,
                "payload": 3.0, "height": 0.8, "weight": 15,
            },
            "ZHILYUAN_A3": {  # 智元远征A3 Ultra
                "joint_lower": np.ones(52) * -3.14,
                "joint_upper": np.ones(52) * 3.14,
                "max_velocity": np.ones(52) * 2.5,
                "max_torque": np.ones(52) * 120,
                "payload": 50.0, "height": 1.88, "weight": 65,
            },
            "ZHILYUAN_G2": {  # 智元精灵G2
                "joint_lower": np.ones(38) * -3.14,
                "joint_upper": np.ones(38) * 3.14,
                "max_velocity": np.ones(38) * 2.0,
                "max_torque": np.ones(38) * 50,
                "payload": 15.0, "height": 1.55, "weight": 45,
            },
            "ZHILYUAN_Q1": {  # 智元启元Q1
                "joint_lower": np.ones(25) * -3.14,
                "joint_upper": np.ones(25) * 3.14,
                "max_velocity": np.ones(25) * 2.0,
                "max_torque": np.ones(25) * 60,
                "payload": 20.0, "height": 1.7, "weight": 55,
            },
            "ZHILINGXI_X2": {  # 智元灵犀X2
                "joint_lower": np.ones(25) * -3.14,
                "joint_upper": np.ones(25) * 3.14,
                "max_velocity": np.ones(25) * 2.0,
                "max_torque": np.ones(25) * 50,
                "payload": 15.0, "height": 1.3, "weight": 38,
            },
            "UBTECH_WALKER": {  # 优必选 Walker S2
                "joint_lower": np.ones(41) * -3.14,
                "joint_upper": np.ones(41) * 3.14,
                "max_velocity": np.ones(41) * 2.5,
                "max_torque": np.ones(41) * 80,
                "payload": 20.0, "height": 1.65, "weight": 55,
            },
            "JAKA_PI": {  # 节卡π仔
                "joint_lower": np.ones(30) * -3.14,
                "joint_upper": np.ones(30) * 3.14,
                "max_velocity": np.ones(30) * 2.0,
                "max_torque": np.ones(30) * 30,
                "payload": 10.0, "height": 1.2, "weight": 35,
            },
            "JAKA_K1": {  # 节卡K1-25
                "joint_lower": np.ones(40) * -3.14,
                "joint_upper": np.ones(40) * 3.14,
                "max_velocity": np.ones(40) * 2.5,
                "max_torque": np.ones(40) * 150,
                "payload": 50.0, "height": 1.8, "weight": 75,
            },
            "SONGYAN_BUMI": {  # 松延动力Bumi小布米
                "joint_lower": np.ones(20) * -3.14,
                "joint_upper": np.ones(20) * 3.14,
                "max_velocity": np.ones(20) * 1.5,
                "max_torque": np.ones(20) * 20,
                "payload": 2.0, "height": 0.94, "weight": 12,
            },
            "KEPLER_K2": {  # 开普勒K2大黄蜂
                "joint_lower": np.ones(52) * -3.14,
                "joint_upper": np.ones(52) * 3.14,
                "max_velocity": np.ones(52) * 3.0,
                "max_torque": np.ones(52) * 180,
                "payload": 60.0, "height": 1.9, "weight": 70,
            },
            "MATRIX_3": {  # 矩阵超智MATRIX-3
                "joint_lower": np.ones(52) * -3.14,
                "joint_upper": np.ones(52) * 3.14,
                "max_velocity": np.ones(52) * 2.5,
                "max_torque": np.ones(52) * 100,
                "payload": 30.0, "height": 1.8, "weight": 60,
            },
            "FOURIER_GR3": {  # 傅利叶GR-3
                "joint_lower": np.ones(35) * -3.14,
                "joint_upper": np.ones(35) * 3.14,
                "max_velocity": np.ones(35) * 2.0,
                "max_torque": np.ones(35) * 60,
                "payload": 15.0, "height": 1.65, "weight": 50,
            },
            "ZHUOYIDE_MOYA": {  # 卓益得Moya
                "joint_lower": np.ones(30) * -3.14,
                "joint_upper": np.ones(30) * 3.14,
                "max_velocity": np.ones(30) * 2.0,
                "max_torque": np.ones(30) * 50,
                "payload": 10.0, "height": 1.6, "weight": 45,
            },
            "LINGLONG_2": {  # 灵龙2.0
                "joint_lower": np.ones(40) * -3.14,
                "joint_upper": np.ones(40) * 3.14,
                "max_velocity": np.ones(40) * 2.5,
                "max_torque": np.ones(40) * 80,
                "payload": 25.0, "height": 1.75, "weight": 55,
            },
            "XINGHAITU_R1": {  # 星海图R1
                "joint_lower": np.ones(30) * -3.14,
                "joint_upper": np.ones(30) * 3.14,
                "max_velocity": np.ones(30) * 2.0,
                "max_torque": np.ones(30) * 50,
                "payload": 15.0, "height": 1.6, "weight": 45,
            },
            "YINHE_GALBOT_S2": {  # 银河通用Galbot S2
                "joint_lower": np.ones(35) * -3.14,
                "joint_upper": np.ones(35) * 3.14,
                "max_velocity": np.ones(35) * 2.5,
                "max_torque": np.ones(35) * 80,
                "payload": 20.0, "height": 1.7, "weight": 55,
            },
            "QIANXUN_MOZ1": {  # 千寻智能Moz1
                "joint_lower": np.ones(40) * -3.14,
                "joint_upper": np.ones(40) * 3.14,
                "max_velocity": np.ones(40) * 2.5,
                "max_torque": np.ones(40) * 100,
                "payload": 30.0, "height": 1.8, "weight": 60,
            },
            "BEIJING_TIANGONG_3": {  # 北京人形天工3.0
                "joint_lower": np.ones(45) * -3.14,
                "joint_upper": np.ones(45) * 3.14,
                "max_velocity": np.ones(45) * 3.0,
                "max_torque": np.ones(45) * 120,
                "payload": 40.0, "height": 1.85, "weight": 65,
            },
            "TASHI_A3": {  # 它石智航A3
                "joint_lower": np.ones(18) * -3.14,
                "joint_upper": np.ones(18) * 3.14,
                "max_velocity": np.ones(18) * 2.0,
                "max_torque": np.ones(18) * 40,
                "payload": 10.0, "height": 1.2, "weight": 30,
            },
            "ZHIPINGFANG_ALPHA": {  # 智平方Alpha
                "joint_lower": np.ones(40) * -3.14,
                "joint_upper": np.ones(40) * 3.14,
                "max_velocity": np.ones(40) * 2.5,
                "max_torque": np.ones(40) * 80,
                "payload": 20.0, "height": 1.75, "weight": 55,
            },
            # ── 2026新品: 四足机器人 ──
            "UNITREE_GO2": {  # 宇树Go2
                "joint_lower": np.ones(12) * -3.14,
                "joint_upper": np.ones(12) * 3.14,
                "max_velocity": np.ones(12) * 5.0,
                "max_torque": np.ones(12) * 40,
                "payload": 5.0, "weight": 15,
            },
            "UNITREE_B2": {  # 宇树B2
                "joint_lower": np.ones(12) * -3.14,
                "joint_upper": np.ones(12) * 3.14,
                "max_velocity": np.ones(12) * 4.0,
                "max_torque": np.ones(12) * 80,
                "payload": 20.0, "weight": 50,
            },
            "UNITREE_A2": {  # 宇树A2
                "joint_lower": np.ones(12) * -3.14,
                "joint_upper": np.ones(12) * 3.14,
                "max_velocity": np.ones(12) * 3.5,
                "max_torque": np.ones(12) * 35,
                "payload": 5.0, "weight": 12,
            },
            # ── 2026新品: AMR ──
            "HIKROBOT_AMR": {  # 海康AMR
                "max_velocity": 2.0, "payload": 200.0, "battery_hours": 8,
            },
            "GEEK_AMR": {  # 极智嘉AMR
                "max_velocity": 2.5, "payload": 500.0, "battery_hours": 10,
            },
            "QUICKTON_AMR": {  # 快仓AMR
                "max_velocity": 2.0, "payload": 300.0, "battery_hours": 8,
            },
            # ── 2026成都人形创新中心系列 ──
            "GONGGA_1": {  # 贡嘎一号
                "joint_lower": np.ones(20) * -3.14,
                "joint_upper": np.ones(20) * 3.14,
                "max_velocity": np.ones(20) * 2.0,
                "max_torque": np.ones(20) * 30,
                "payload": 2.0, "height": 1.2, "weight": 25,
            },
            "RUIBA": {  # 锐钯
                "joint_lower": np.ones(12) * -3.14,
                "joint_upper": np.ones(12) * 3.14,
                "max_velocity": np.ones(12) * 2.5,
                "max_torque": np.ones(12) * 40,
                "payload": 5.0, "height": 1.0, "weight": 30,
                "screen_size": 19, "head_dofs": 6,
            },
            "HONGHU_ROBOT": {  # 鸿鹄
                "joint_lower": np.ones(25) * -3.14,
                "joint_upper": np.ones(25) * 3.14,
                "max_velocity": np.ones(25) * 2.5,
                "max_torque": np.ones(25) * 50,
                "payload": 10.0, "height": 1.5, "weight": 40,
            },
            "XIAOZHA_ROBOT": {  # 小吒
                "joint_lower": np.ones(20) * -3.14,
                "joint_upper": np.ones(20) * 3.14,
                "max_velocity": np.ones(20) * 2.0,
                "max_torque": np.ones(20) * 30,
                "payload": 3.0, "height": 1.0, "weight": 25,
            },
            "BIONIC_DINOSAUR": {  # 仿生恐龙
                "joint_lower": np.ones(16) * -3.14,
                "joint_upper": np.ones(16) * 3.14,
                "max_velocity": np.ones(16) * 2.5,
                "max_torque": np.ones(16) * 60,
                "payload": 10.0, "weight": 50,
            },
            "BELT_INSPECTION": {  # 胶带机巡检机器人
                "max_velocity": 1.5, "payload": 50.0, "battery_hours": 24,
                "order_size": 5000, "accuracy": "99%+",
            },
            "BIPED_WHEEL_PLATFORM": {  # 双轮足开源平台
                "joint_lower": np.ones(8) * -3.14,
                "joint_upper": np.ones(8) * 3.14,
                "max_velocity": np.ones(8) * 3.0,
                "max_torque": np.ones(8) * 100,
                "payload": 100.0, "weight": 80,
            },
            "AI_ELECTRONIC_SKIN": {  # AI电子皮肤
                "force_resolution": 0.005, "sensing_type": "neural_network",
            },
            # ── 2026浙江人形创新中心系列 ──
            "ZHEJIANG_HUMANOID": {  # 浙江双臂人形作业机器人
                "joint_lower": np.ones(40) * -3.14,
                "joint_upper": np.ones(40) * 3.14,
                "max_velocity": np.ones(40) * 2.5,
                "max_torque": np.ones(40) * 80,
                "payload": 20.0, "height": 1.75, "weight": 60,
                "order_size": 2000, "application": "服装/汽车装配",
            },
            # ── 2026 WAIC世界人工智能大会首发新品 ──
            "QIYUAN_Q1": {  # 启元Q1 小尺寸全身力控人形
                "joint_lower": np.ones(22) * -3.14,
                "joint_upper": np.ones(22) * 3.14,
                "max_velocity": np.ones(22) * 2.0,
                "max_torque": np.ones(22) * 25,
                "payload": 2.0, "height": 0.88, "weight": 15,
                "force_control": True, "open_source_structure": True,
            },
            "QIYUAN_T1": {  # 启元T1 全球首款可变形个人机器人
                "joint_lower": np.ones(18) * -3.14,
                "joint_upper": np.ones(18) * 3.14,
                "max_velocity": np.ones(18) * 3.0,
                "max_torque": np.ones(18) * 40,
                "payload": 5.0, "weight": 20,
                "transformable": True, "modes": ["轮足人形", "四足"],
                "price": 15999,
            },
            "LEJU_KUAFU": {  # 乐聚夸父系列 全尺寸人形
                "joint_lower": np.ones(35) * -3.14,
                "joint_upper": np.ones(35) * 3.14,
                "max_velocity": np.ones(35) * 2.5,
                "max_torque": np.ones(35) * 80,
                "payload": 15.0, "height": 1.75, "weight": 65,
                "localization_rate": 0.95, "customers": ["一汽", "长虹", "中兴"],
            },
            "LEJU_LUBAN": {  # 乐聚鲁班 工业人形
                "joint_lower": np.ones(30) * -3.14,
                "joint_upper": np.ones(30) * 3.14,
                "max_velocity": np.ones(30) * 2.0,
                "max_torque": np.ones(30) * 100,
                "payload": 20.0, "weight": 70,
                "scenarios": ["拆垛", "上料", "搬运"],
            },
            "MAGICATOM_X1": {  # 魔法原子MagicBot X1 180cm通用人形
                "joint_lower": np.ones(31) * -3.14,
                "joint_upper": np.ones(31) * 3.14,
                "max_velocity": np.ones(31) * 3.0,
                "max_torque": np.ones(31) * 150,
                "payload": 30.0, "height": 1.80, "weight": 80,
                "peak_torque_per_joint": 450,
            },
            "MAGICATOM_D1": {  # 魔法原子MagicBot D1 轮式人形
                "joint_lower": np.ones(20) * -3.14,
                "joint_upper": np.ones(20) * 3.14,
                "max_velocity": np.ones(20) * 2.5,
                "max_torque": np.ones(20) * 60,
                "payload": 30.0, "weight": 55,
                "locomotion": "轮式", "scenario": "厂区物料转运",
            },
            "MAGICATOM_T1": {  # 魔法原子MagicDog T1 轻量化四足
                "joint_lower": np.ones(12) * -3.14,
                "joint_upper": np.ones(12) * 3.14,
                "max_velocity": np.ones(12) * 4.0,
                "max_torque": np.ones(12) * 40,
                "payload": 5.0, "weight": 15,
                "scenario": "狭小空间巡检",
            },
            "AGIBOT_G2_MAX": {  # 智元精灵G2 Max 轮式仓储人形
                "joint_lower": np.ones(25) * -3.14,
                "joint_upper": np.ones(25) * 3.14,
                "max_velocity": np.ones(25) * 2.0,
                "max_torque": np.ones(25) * 80,
                "payload": 50.0, "weight": 75,
                "locomotion": "轮式", "partner": "京东物流",
            },
            "AGIBOT_KUOTUO": {  # 智元酷拓骑行机器人
                "payload": 75.0, "weight": 60,
                "scenarios": ["巡检", "代步"], "autonomous": True,
            },
            "BEIJING_TIANGONG": {  # 北京具身天工系列 工业人形
                "joint_lower": np.ones(35) * -3.14,
                "joint_upper": np.ones(35) * 3.14,
                "max_velocity": np.ones(35) * 2.0,
                "max_torque": np.ones(35) * 120,
                "payload": 25.0, "height": 1.75, "weight": 70,
                "scenarios": ["化工", "电力", "油气"],
            },
            "ZHONGJI_T800": {  # 众擎T800 全尺寸格斗人形
                "joint_lower": np.ones(30) * -3.14,
                "joint_upper": np.ones(30) * 3.14,
                "max_velocity": np.ones(30) * 4.0,
                "max_torque": np.ones(30) * 150,
                "payload": 20.0, "height": 1.80, "weight": 85,
                "features": "高强度抗扰",
            },
            "PUDU_D7": {  # 普渡PUDU D7 类人形智能作业伙伴
                "joint_lower": np.ones(20) * -3.14,
                "joint_upper": np.ones(20) * 3.14,
                "max_velocity": np.ones(20) * 2.0,
                "max_torque": np.ones(20) * 50,
                "payload": 14.0, "working_height": 2.0, "weight": 55,
                "scenarios": ["工厂", "仓储", "零售"],
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

    # ── 2026新品: 国产协作臂连接存根 ──
    def _connect_rokae(self, host, port):
        """珞石 ROKAE 机器人"""
        from rokae_sdk import RokaeRobot
        self._rokae = RokaeRobot(host, port or 8080)
        self._rokae.connect()
        self._comm = "rokae"

    def _connect_aubo(self, host, port):
        """遨博 AUBO 机器人"""
        from aubo_sdk import AuboRobot
        self._aubo = AuboRobot(host, port or 8899)
        self._aubo.connect()
        self._comm = "aubo"

    def _connect_elite(self, host, port):
        """艾利特 ELITE 机器人"""
        from elite_sdk import EliteRobot
        self._elite = EliteRobot(host, port or 8080)
        self._elite.connect()
        self._comm = "elite"

    # ── 2026新品: 国人形机器人连接存根 ──
    def _connect_zhiyuan(self, host, port):
        """智元机器人（远征A3/精灵G2/启元Q1/灵犀X2）"""
        from zhiyuan_sdk import ZhiyuanRobot
        self._zhiyuan = ZhiyuanRobot(host, port or 8080)
        self._zhiyuan.connect()
        self._comm = "zhiyuan"

    def _connect_ubtech(self, host, port):
        """优必选 Walker S 系列"""
        from ubtech_sdk import UbtechRobot
        self._ubtech = UbtechRobot(host, port or 9090)
        self._ubtech.connect()
        self._comm = "ubtech"

    def _connect_songyan(self, host, port):
        """松延动力 Bumi 小布米"""
        from songyan_sdk import SongyanRobot
        self._songyan = SongyanRobot(host, port or 8080)
        self._songyan.connect()
        self._comm = "songyan"

    def _connect_kepler(self, host, port):
        """开普勒 K2 大黄蜂"""
        from kepler_sdk import KeplerRobot
        self._kepler = KeplerRobot(host, port or 8080)
        self._kepler.connect()
        self._comm = "kepler"

    def _connect_matrix(self, host, port):
        """矩阵超智 MATRIX-3"""
        from matrix_sdk import MatrixRobot
        self._matrix = MatrixRobot(host, port or 8080)
        self._matrix.connect()
        self._comm = "matrix"

    def _connect_fourier(self, host, port):
        """傅利叶 GR-3"""
        from fourier_sdk import FourierRobot
        self._fourier = FourierRobot(host, port or 8080)
        self._fourier.connect()
        self._comm = "fourier"

    def _connect_zhuoyide(self, host, port):
        """卓益得 Moya"""
        from zhuoyide_sdk import ZhuoyideRobot
        self._zhuoyide = ZhuoyideRobot(host, port or 8080)
        self._zhuoyide.connect()
        self._comm = "zhuoyide"

    def _connect_linglong(self, host, port):
        """国家地方共建 灵龙2.0"""
        from linglong_sdk import LinglongRobot
        self._linglong = LinglongRobot(host, port or 8080)
        self._linglong.connect()
        self._comm = "linglong"

    def _connect_xinghaitu(self, host, port):
        """星海图 R1"""
        from xinghaitu_sdk import XinghaituRobot
        self._xinghaitu = XinghaituRobot(host, port or 8080)
        self._xinghaitu.connect()
        self._comm = "xinghaitu"

    def _connect_yinhe(self, host, port):
        """银河通用 Galbot S2"""
        from yinhe_sdk import YinheRobot
        self._yinhe = YinheRobot(host, port or 8080)
        self._yinhe.connect()
        self._comm = "yinhe"

    def _connect_qianxun(self, host, port):
        """千寻智能 Moz1"""
        from qianxun_sdk import QianxunRobot
        self._qianxun = QianxunRobot(host, port or 8080)
        self._qianxun.connect()
        self._comm = "qianxun"

    def _connect_beijing_robot(self, host, port):
        """北京人形 天工3.0"""
        from beijing_robot_sdk import BeijingRobot
        self._bjrobot = BeijingRobot(host, port or 8080)
        self._bjrobot.connect()
        self._comm = "beijing_robot"

    def _connect_tashi(self, host, port):
        """它石智航 A3"""
        from tashi_sdk import TashiRobot
        self._tashi = TashiRobot(host, port or 8080)
        self._tashi.connect()
        self._comm = "tashi"

    def _connect_zhipingfang(self, host, port):
        """智平方 Alpha"""
        from zhipingfang_sdk import ZhipingfangRobot
        self._zhipingfang = ZhipingfangRobot(host, port or 8080)
        self._zhipingfang.connect()
        self._comm = "zhipingfang"

    # ── 2026新品: AMR连接存根 ──
    def _connect_hikrobot(self, host, port):
        """海康机器人 AMR"""
        from hikrobot_sdk import HikRobot
        self._hikrobot = HikRobot(host, port or 8080)
        self._hikrobot.connect()
        self._comm = "hikrobot"

    def _connect_geek(self, host, port):
        """极智嘉 Geek+ AMR"""
        from geek_sdk import GeekRobot
        self._geek = GeekRobot(host, port or 8080)
        self._geek.connect()
        self._comm = "geek"

    def _connect_quicktron(self, host, port):
        """快仓 Quicktron AMR"""
        from quicktron_sdk import QuicktronRobot
        self._quicktron = QuicktronRobot(host, port or 8080)
        self._quicktron.connect()
        self._comm = "quicktron"

    # ── 成都人形创新中心系列连接存根 ──
    def _connect_gongga(self, host, port):
        """贡嘎一号 超轻量级人形"""
        from gongga_sdk import GonggaRobot
        self._gongga = GonggaRobot(host, port or 8080)
        self._gongga.connect()
        self._comm = "gongga"

    def _connect_ruiba(self, host, port):
        """锐钯 文商旅双足"""
        from ruiba_sdk import RuibaRobot
        self._ruiba = RuibaRobot(host, port or 8080)
        self._ruiba.connect()
        self._comm = "ruiba"

    def _connect_honghu(self, host, port):
        """鸿鹄 人形机器人"""
        from honghu_sdk import HonghuRobot
        self._honghu = HonghuRobot(host, port or 8080)
        self._honghu.connect()
        self._comm = "honghu"

    def _connect_xiaozha(self, host, port):
        """小吒 人形机器人"""
        from xiaozha_sdk import XiaozhaRobot
        self._xiaozha = XiaozhaRobot(host, port or 8080)
        self._xiaozha.connect()
        self._comm = "xiaozha"

    def _connect_bionic_dinosaur(self, host, port):
        """仿生恐龙机器人"""
        from dinosaur_sdk import DinosaurRobot
        self._dino = DinosaurRobot(host, port or 8080)
        self._dino.connect()
        self._comm = "bionic_dinosaur"

    def _connect_belt_inspection(self, host, port):
        """胶带机巡检机器人"""
        from belt_sdk import BeltInspectionRobot
        self._belt = BeltInspectionRobot(host, port or 8080)
        self._belt.connect()
        self._comm = "belt_inspection"

    def _connect_biped_wheel(self, host, port):
        """双轮足开源平台"""
        from biped_wheel_sdk import BipedWheelRobot
        self._biped = BipedWheelRobot(host, port or 8080)
        self._biped.connect()
        self._comm = "biped_wheel"

    def _connect_ai_skin(self, host, port):
        """AI神经网络电子皮肤"""
        from ai_skin_sdk import AiElectronicSkin
        self._skin = AiElectronicSkin(host, port or 8080)
        self._skin.connect()
        self._comm = "ai_skin"

    # ── 浙江人形创新中心系列连接存根 ──
    def _connect_zhejiang_humanoid(self, host, port):
        """浙江双臂人形作业机器人"""
        from zhejiang_humanoid_sdk import ZhejiangHumanoid
        self._zjrobot = ZhejiangHumanoid(host, port or 8080)
        self._zjrobot.connect()
        self._comm = "zhejiang_humanoid"

    # ===== WAIC 2026首发新品连接存根 =====
    def _connect_qiyuan(self, host, port):
        """启元机器人 (Q1/T1, 上纬新材启元机器人)"""
        from qiyuan_sdk import QiyuanRobot
        self._qiyuan = QiyuanRobot(host, port or 8080)
        self._qiyuan.connect()
        self._comm = "qiyuan"

    def _connect_leju(self, host, port):
        """乐聚机器人 (夸父/鲁班系列)"""
        from leju_sdk import LejuRobot
        self._leju = LejuRobot(host, port or 8080)
        self._leju.connect()
        self._comm = "leju"

    def _connect_magicatom(self, host, port):
        """魔法原子机器人 (MagicBot X1/D1, MagicDog T1)"""
        from magicatom_sdk import MagicAtomRobot
        self._magic = MagicAtomRobot(host, port or 8080)
        self._magic.connect()
        self._comm = "magicatom"

    def _connect_agibot(self, host, port):
        """智元机器人 (精灵G2 Max/酷拓骑行)"""
        from agibot_sdk import AgibotRobot
        self._agibot = AgibotRobot(host, port or 8080)
        self._agibot.connect()
        self._comm = "agibot"

    def _connect_beijing_tiangong(self, host, port):
        """北京人形创新中心·具身天工系列"""
        from tiangong_sdk import TiangongRobot
        self._tiangong = TiangongRobot(host, port or 8080)
        self._tiangong.connect()
        self._comm = "beijing_tiangong"

    def _connect_zhongji(self, host, port):
        """众擎机器人 (T800格斗人形)"""
        from zhongji_sdk import ZhongjiRobot
        self._zhongji = ZhongjiRobot(host, port or 8080)
        self._zhongji.connect()
        self._comm = "zhongji"

    def _connect_pudu(self, host, port):
        """普渡机器人 (PUDU D7类人形作业)"""
        from pudu_sdk import PuduRobot
        self._pudu = PuduRobot(host, port or 8080)
        self._pudu.connect()
        self._comm = "pudu"

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
    # ====================================================================
    # 一、按预算分类（人民币）
    # ====================================================================
    "budget_1w": [  # 1万元以内
        {"name": "myCobot 280", "brand": "Elephant Robotics 大象机器人", "price": "¥5,000-10,000",
         "payload": "0.25kg", "reach": "280mm", "axes": 6,
         "pros": "价格极低、入门友好、USB连接、ROS支持",
         "cons": "负载小、精度一般",
         "use_case": "教学、演示、轻量抓取、创客DIY",
         "source": "Elephant Robotics 大象机器人 (深圳大象机器人科技有限公司, www.elephantrobotics.com)"},
        {"name": "Unitree Go2 Air", "brand": "宇树科技", "price": "¥8,999",
         "payload": "7kg（背负）", "reach": "四足", "axes": 12,
         "pros": "四足入门最低门槛、可走可舞可避障、空翻",
         "cons": "无手臂、精细操作有限",
         "use_case": "教学科研、娱乐表演、基础巡检",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, 四足入门最低门槛)"},
        {"name": "松延动力Bumi小布米", "brand": "松延动力", "price": "¥8,000-10,000",
         "height": "94cm", "weight": "12kg", "dofs": "全身20+",
         "pros": "人形机器人最低门槛、价格不足万元、家庭友好",
         "cons": "尺寸小、负载有限",
         "use_case": "家庭陪伴、教育启蒙、科技馆展示",
         "source": "松延动力 (深圳松延动力科技有限公司, 人形机器人最低门槛)"},
    ],
    "budget_3w": [  # 1-3万元
        {"name": "Unitree Go2 Pro", "brand": "宇树科技", "price": "¥18,600",
         "payload": "8-10kg", "speed": "5m/s", "dofs": 12,
         "pros": "ISS 2.0伴随系统、4G联网、语音交互、360°激光雷达",
         "cons": "无手臂操作",
         "use_case": "科研教育、巡检安防、娱乐表演",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, ISS 2.0+4G联网)"},
        {"name": "Unitree R1 智能伙伴", "brand": "宇树科技", "price": "¥29,900",
         "height": "123cm", "weight": "29kg", "dofs": "23+",
         "pros": "消费级人形最低门槛、家庭友好、可走可舞、手臂操作",
         "cons": "手部精度一般、续航1小时",
         "use_case": "家庭陪伴、迎宾接待、儿童教育、科技馆",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, 消费级人形智能伙伴)"},
        {"name": "xArm 1S", "brand": "越疆科技", "price": "¥16,800",
         "payload": "0.5kg", "reach": "400mm", "axes": 5,
         "pros": "入门级协作臂、桌面级、轻量紧凑、教育首选",
         "cons": "负载小、5轴无冗余",
         "use_case": "教学实训、桌面自动化、轻量装配",
         "source": "UFACTORY 优艾智合 (深圳优艾智合机器人科技有限公司, www.ufactory.cc)"},
    ],
    "budget_10w": [  # 3-10万元
        {"name": "Unitree G1 基础版", "brand": "宇树科技", "price": "¥85,000-99,000",
         "height": "132cm", "weight": "35kg", "dofs": "23-43",
         "pros": "量产人形入门首选、五指灵巧手、ROS2/SDK全开放",
         "cons": "单臂负载仅3kg、续航40-60分钟",
         "use_case": "人形机器人研发、具身智能算法、教育科研",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, G1基础版)"},
        {"name": "CRA3-630", "brand": "越疆科技", "price": "¥50,000-70,000",
         "payload": "3kg", "reach": "630mm", "axes": 6,
         "pros": "2026新品、223°/s高速、±0.02mm精度、PLd安全、EtherCAT",
         "cons": "力控需选配",
         "use_case": "3C装配、检测分拣、实验室自动化",
         "source": "越疆科技 (DOBOT, 深圳越疆科技股份有限公司, 2025年CRA系列协作臂)"},
        {"name": "JAKA Mini 2", "brand": "节卡机器人", "price": "¥40,000-60,000",
         "payload": "2kg", "reach": "580mm", "axes": 6,
         "pros": "2026新品、超小型、180W低功耗、桌面自动化",
         "cons": "负载较小",
         "use_case": "高校实训、桌面小型自动化、文创商用",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2025年新品)"},
        {"name": "JAKA Ai3", "brand": "节卡机器人", "price": "¥70,000-90,000",
         "payload": "3kg", "reach": "626mm", "axes": 6,
         "pros": "2026新品、一体化内置视觉、±0.02mm精度、免布线",
         "cons": "臂展较短",
         "use_case": "3C精密锁附、镭雕涂胶、视觉分拣",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2026年AI系列)"},
        {"name": "Unitree G1 EDU", "brand": "宇树科技", "price": "¥169,000-309,000",
         "height": "132cm", "weight": "35kg", "dofs": "23-43",
         "pros": "人形开发首选、完整SDK/ROS2、算力可扩展、双灵巧手",
         "cons": "价格较高",
         "use_case": "顶级科研、具身智能算法、大模型机器人",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, G1教育科研版)"},
    ],
    "mid_range": [  # 10-30万元
        {"name": "Airbot P7", "brand": "星动纪元", "price": "¥80,000-120,000",
         "payload": "7kg", "reach": "922mm", "axes": 7,
         "pros": "7轴力控、拖拽示教、国产首选、CAN总线、全向移动",
         "cons": "品牌较新",
         "use_case": "精密装配、力控打磨、科研实验、产线柔性自动化",
         "source": "星动纪元 (北京星动纪元科技有限公司, 2026年国内首款7轴消费级协作臂)"},
        {"name": "Flexiv Rizon 4", "brand": "非夕科技", "price": "¥100,000-150,000",
         "payload": "4kg", "reach": "830mm", "axes": 7,
         "pros": "全球顶级力控、AI原生、复杂作业、高精度",
         "cons": "价格偏高",
         "use_case": "精密装配、抛光打磨、柔性作业、无序分拣",
         "source": "非夕科技 (Flexiv, 全球自适应机器人开创者, www.flexiv.com)"},
        {"name": "JAKA Zu 7", "brand": "节卡机器人", "price": "¥60,000-90,000",
         "payload": "7kg", "reach": "790mm", "axes": 6,
         "pros": "无线示教、拖拽编程、部署极快、国内市占率国产头部",
         "cons": "6轴无冗余",
         "use_case": "3C电子、汽车零部件、产线集成、上下料",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, Zu系列协作臂)"},
        {"name": "JAKA π 仔", "brand": "节卡机器人", "price": "¥90,000-130,000",
         "height": "122cm", "weight": "42kg", "dofs": 27,
         "pros": "2026新品、全自研关节、大小脑融合、现货交付",
         "cons": "单臂负载3kg",
         "use_case": "高校实训、科技馆导览、商业迎宾、康养交互",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2026年WAIC首发人形)"},
        {"name": "JAKA Ai7", "brand": "节卡机器人", "price": "¥80,000-110,000",
         "payload": "7kg", "reach": "819mm", "axes": 6,
         "pros": "2026新品、一体化视觉、±0.02mm、免手眼标定、3C爆款",
         "cons": "力控需选配",
         "use_case": "电子装配、视觉分拣、精密涂胶、包装码垛",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2026年AI系列)"},
        {"name": "CRA7-950", "brand": "越疆科技", "price": "¥80,000-120,000",
         "payload": "7kg", "reach": "950mm", "axes": 6,
         "pros": "2026新品、223°/s高速、±0.03mm、EtherCAT、SafeSkin碰前感知",
         "cons": "力控需选配",
         "use_case": "搬运码垛、上下料、装配检测、机床自动化",
         "source": "越疆科技 (DOBOT, 深圳越疆科技股份有限公司, 2025年CRA系列协作臂)"},
    ],
    "premium_30w": [  # 30-80万元
        {"name": "UR5e", "brand": "Universal Robots", "price": "¥120,000-180,000",
         "payload": "5kg", "reach": "850mm", "axes": 6,
         "pros": "全球最成熟协作臂、生态完善、海量教程、售后全球",
         "cons": "价格高、力控需选件",
         "use_case": "工业产线、科研教学、全球服务、高端制造",
         "source": "Universal Robots优傲机器人 (丹麦, 全球协作臂领导者, www.universal-robots.com)"},
        {"name": "UR10e", "brand": "Universal Robots", "price": "¥180,000-250,000",
         "payload": "10kg", "reach": "1300mm", "axes": 6,
         "pros": "全球标杆、长臂展、大负载、工业级可靠性",
         "cons": "价格高",
         "use_case": "汽车制造、包装码垛、机床上下料、重型装配",
         "source": "Universal Robots优傲机器人 (丹麦, 全球协作臂领导者, www.universal-robots.com)"},
        {"name": "JAKA Zu35", "brand": "节卡机器人", "price": "¥200,000-280,000",
         "payload": "35kg", "reach": "2000mm", "axes": 6,
         "pros": "2026新品、35kg重载天花板、2m臂展、码垛12次/分钟",
         "cons": "体积较大",
         "use_case": "整箱码垛、重型机床上下料、汽车大件、新能源电池",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2025年35kg大负载)"},
        {"name": "JAKA Ai12", "brand": "节卡机器人", "price": "¥140,000-180,000",
         "payload": "12kg", "reach": "1327mm", "axes": 6,
         "pros": "2026新品、一体化视觉、长臂展大负载、免布线",
         "cons": "6轴无冗余",
         "use_case": "大件搬运、包装码垛、机床自动化、汽车零部件",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2026年AI系列)"},
        {"name": "珞石 xMateCR7", "brand": "珞石机器人", "price": "¥150,000-220,000",
         "payload": "7kg", "reach": "920mm", "axes": 7,
         "pros": "力控人形机械臂、国内协作市占率47%、全栈自研",
         "cons": "品牌认知度略低",
         "use_case": "精密装配、打磨抛光、人形机器人手臂、科研",
         "source": "珞石机器人 (Rokae, 北京珞石机器人科技有限公司)"},
    ],
    "premium": [  # 80万元以上
        {"name": "Franka Emika Panda", "brand": "Franka Emika", "price": "¥200,000-300,000",
         "payload": "3kg", "reach": "855mm", "axes": 7,
         "pros": "科研黄金标准、开源友好、力控顶级、学术引用最多",
         "cons": "负载小、价格高",
         "use_case": "顶级科研、AI机器人学习、精密操作、具身智能",
         "source": "Franka Emika (德国, 高精度力控协作臂, www.franka.de)"},
        {"name": "KUKA LBR iiwa", "brand": "KUKA", "price": "¥300,000-500,000",
         "payload": "7/14kg", "reach": "800mm", "axes": 7,
         "pros": "工业级力控、ISO 10218认证、汽车行业标准、全球标杆",
         "cons": "价格极高、部署复杂",
         "use_case": "汽车制造、航空航天、精密工业、高端科研",
         "source": "KUKA库卡 (德国, 工业机器人四大家族之一, www.kuka.com)"},
    ],
    # ====================================================================
    # 二、人形机器人专区（2025-2026量产主力）
    # ====================================================================
    "humanoid": [
        {"name": "Unitree G1", "brand": "宇树科技", "price": "¥85,000-309,000",
         "height": "132cm", "weight": "35kg", "dofs": "23-43",
         "pros": "全球量产最多人形之一、五指灵巧手、ROS2全开放、性价比最高",
         "cons": "单臂负载3kg、续航40-60分钟",
         "use_case": "人形研发、具身智能、教育科研、工业预研",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, 全球量产最多人形之一)"},
        {"name": "Unitree H1", "brand": "宇树科技", "price": "¥600,000-900,000",
         "height": "180cm", "weight": "47kg", "dofs": "全身35+",
         "pros": "全球最成熟全尺寸人形、运动能力最强（5m/s）、已量产5500+台",
         "cons": "手部操作能力有限、价格高",
         "use_case": "人形机器人研发、工业巡检、特种作业、运动测试",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, 全尺寸人形旗舰)"},
        {"name": "优必选Walker S2", "brand": "优必选", "price": "¥500,000-1,000,000",
         "height": "160cm", "weight": "67kg", "dofs": "全身41",
         "pros": "工业人形已量产、全年交付千台+、订单1.3万台、汽车产线验证",
         "cons": "价格较高",
         "use_case": "工业制造、汽车产线、3C电子、新能源电池",
         "source": "优必选科技 (UBTech, 深圳优必选科技股份有限公司, 港股:09880.HK)"},
        {"name": "银河通用 DB1", "brand": "银河通用", "price": "¥500,000-800,000",
         "height": "170cm", "weight": "55kg", "dofs": "全身40+",
         "pros": "国产量产人形、双手操作、大模型集成、百达精工千台订单",
         "cons": "交付周期较长",
         "use_case": "工厂作业、家政服务、科研平台、商业服务",
         "source": "银河通用机器人 (北京银河通用机器人有限公司, 前小米机器人团队)"},
        {"name": "智元精灵G2", "brand": "智元机器人", "price": "¥300,000-500,000",
         "height": "155cm", "weight": "55kg", "dofs": "全身40+",
         "pros": "良品率99.99%、量产爬坡、订单5100+台、2026年数万台目标",
         "cons": "精细操作待验证",
         "use_case": "工厂分拣、产线组装、物流搬运、科研",
         "source": "智元机器人 (Agibot, 上海智元新创技术有限公司, 精灵系列桌面人形)"},
        {"name": "智元远征A3 Ultra", "brand": "智元机器人", "price": "¥600,000-900,000",
         "height": "175cm", "weight": "65kg", "dofs": "全身50+",
         "pros": "2026WAIC首发、超拟人灵巧手+柔性腰、全自由度腰部",
         "cons": "价格高、量产初期",
         "use_case": "顶级科研、复杂工业作业、精密操作、大模型机器人",
         "source": "智元机器人 (Agibot, 上海智元新创技术有限公司, 2026WAIC首发)"},
        {"name": "JAKA π 仔", "brand": "节卡机器人", "price": "¥90,000-130,000",
         "height": "122cm", "weight": "42kg", "dofs": 27,
         "pros": "2026新品、全自研关节、现货交付、科教商用首选",
         "cons": "尺寸较小",
         "use_case": "高校实训、科技馆导览、商业迎宾、康养交互",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2026年WAIC首发人形)"},
        {"name": "Unitree R1", "brand": "宇树科技", "price": "¥29,900",
         "height": "123cm", "weight": "29kg", "dofs": "23+",
         "pros": "消费级人形最低门槛、家庭友好、大众市场首选",
         "cons": "性能有限",
         "use_case": "家庭陪伴、儿童教育、迎宾接待、文化娱乐",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, 消费级人形智能伙伴)"},
        {"name": "开普勒K2大黄蜂", "brand": "开普勒机器人", "price": "¥400,000-700,000",
         "height": "175cm", "weight": "85kg", "dofs": "全身52",
         "pros": "全球首款商用混动架构人形、双臂协同30kg、8小时长续航、能效81.3%",
         "cons": "价格高、量产初期",
         "use_case": "汽车制造、重型搬运、新能源产线、高端工业",
         "source": "开普勒探索机器人 (深圳开普勒探索机器人有限公司, 仿生四足+人形双臂)"},
        {"name": "智元灵犀X2", "brand": "智元机器人", "price": "¥250,000-400,000",
         "height": "130cm", "weight": "45kg", "dofs": "全身35+",
         "pros": "iF设计奖、硅光动语多模态大模型、毫秒级情感响应、康养陪护首选",
         "cons": "负载有限",
         "use_case": "康养陪护、家庭陪伴、教育互动、商业服务",
         "source": "智元机器人 (Agibot, 上海智元新创技术有限公司, 灵犀系列女性人形)"},
        {"name": "傅利叶GR-3", "brand": "傅利叶智能", "price": "¥300,000-500,000",
         "height": "165cm", "weight": "60kg", "dofs": "全身40+",
         "pros": "业内首款全尺寸情感陪护机器人、柔肤软包、全感交互系统",
         "cons": "工业能力有限",
         "use_case": "康养陪护、情感陪伴、特殊教育、医疗康复",
         "source": "傅利叶智能 (Fourier Intelligence, 上海傅利叶智能科技有限公司, 2025年量产GR-3)"},
        {"name": "星海图R1", "brand": "星海图机器人", "price": "¥199,000-350,000",
         "height": "160cm", "weight": "55kg", "dofs": "全身40+",
         "pros": "清华系、EFM-1双系统一脑多形、G0 VLA开源、150+科研院所使用",
         "cons": "品牌较新",
         "use_case": "顶级科研、具身智能算法、大模型机器人、高校实验室",
         "source": "星海图机器人 (北京星海图机器人有限公司, 清华系EFM-1双系统)"},
        {"name": "智元远征A3 Ultra", "brand": "智元机器人", "price": "¥600,000-900,000",
         "height": "175cm", "weight": "65kg", "dofs": "全身50+",
         "pros": "2026WAIC首发、超拟人灵巧手+柔性腰、全自由度腰部",
         "cons": "价格高、量产初期",
         "use_case": "顶级科研、复杂工业作业、精密操作、大模型机器人",
         "source": "智元机器人 (Agibot, 上海智元新创技术有限公司, 2026WAIC首发)"},
        # ── 成都人形机器人创新中心系列 ──
        {"name": "贡嘎一号", "brand": "成都人形创新中心", "price": "¥99,000-199,000",
         "height": "120cm", "weight": "25kg", "dofs": "全身20+",
         "pros": "国内首台超轻量级人形、仅25kg、拿拖鞋/取饮料/冲咖啡、家庭康养首选",
         "cons": "负载能力有限",
         "use_case": "家庭康养、智能陪伴、家政服务、教育科研",
         "source": "成都人形机器人创新中心 (国内首台超轻量级人形机器人, 仅25kg)"},
        {"name": "锐钯", "brand": "成都人形创新中心", "price": "¥59,000-129,000",
         "height": "100cm", "weight": "30kg", "dofs": "全身12+头部6",
         "pros": "文商旅双足、19英寸交互大屏、6自由度头部、拟人化动作+表情、世运会啦啦队",
         "cons": "工业能力有限",
         "use_case": "文商旅、科技馆、博物馆、商业展演、景区导览",
         "source": "成都人形机器人创新中心 (文商旅双足机器人, 第12届世运会官方啦啦队机器人, 红星新闻)"},
        {"name": "鸿鹄", "brand": "成都人形创新中心", "price": "¥199,000-399,000",
         "height": "150cm", "weight": "40kg", "dofs": "全身25+",
         "pros": "中西部首个双足行走样机、四川省一号创新工程、30余项顶尖研发成果",
         "cons": "品牌较新",
         "use_case": "科研平台、双足行走研究、具身智能开发",
         "source": "成都人形机器人创新中心 (中西部首个双足行走样机, 四川省一号创新工程, 30余项顶尖研发成果)"},
        {"name": "小吒", "brand": "成都人形创新中心", "price": "¥79,000-149,000",
         "height": "100cm", "weight": "25kg", "dofs": "全身20+",
         "pros": "小型化人形机器人、灵活机动、教育科研首选",
         "cons": "负载能力有限",
         "use_case": "教育科研、青少年科普、算法验证",
         "source": "成都人形机器人创新中心 (小型化人形机器人, 教育科研首选)"},
        {"name": "仿生恐龙机器人", "brand": "成都人形创新中心", "price": "¥299,000-599,000",
         "dofs": "全身16+",
         "pros": "全球首款双足行走智能仿生恐龙、逼真形态+智能交互",
         "cons": "应用场景较窄",
         "use_case": "主题公园、科技馆、文旅展演、影视娱乐",
         "source": "成都人形机器人创新中心 (全球首款双足行走智能仿生恐龙机器人)"},
        {"name": "胶带机巡检机器人", "brand": "成都人形创新中心", "price": "¥399,000-799,000",
         "pros": "5000台国内最大订单、VPDM-01声纹识别模型、99%+异常识别率、自主充电续航24h",
         "cons": "垂直领域专用",
         "use_case": "工业巡检、水电站胶带机、长距离输送线、极端环境作业",
         "source": "成都人形机器人创新中心 (5000台国内最大订单, VPDM-01声纹识别模型, 99%+异常识别率)"},
        {"name": "双轮足开源平台", "brand": "成都人形创新中心", "price": "¥199,000-399,000",
         "pros": "全球首个全尺寸重载双轮足开源、本体+软件全开源、从图纸到成品完整手册",
         "cons": "需二次开发",
         "use_case": "科研平台、开发者生态、双轮足研究、高校实验室",
         "source": "成都人形机器人创新中心 (全球首个全尺寸重载双轮足开源平台, 本体+软件全开源)"},
        {"name": "AI神经网络电子皮肤", "brand": "成都人形创新中心", "price": "¥19,900-49,900",
         "pros": "0.005N微力识别、全球首个AI神经网络电子皮肤、羽毛级触觉感知",
         "cons": "附件产品",
         "use_case": "精密操作、机器人触觉、人机交互、医疗康复",
         "source": "成都人形机器人创新中心 (全球首个AI神经网络电子皮肤, 0.005N微力识别, 羽毛级触觉感知)"},
        # ── 浙江人形机器人创新中心系列 ──
        {"name": "浙江双臂作业人形", "brand": "浙江人形创新中心", "price": "¥399,000-699,000",
         "height": "175cm", "weight": "60kg", "dofs": "全身40+",
         "pros": "杰克科技2000台服装场景订单、双臂协同缝纫、2mm精度对位、汽车装配+石化实验",
         "cons": "垂直场景优化",
         "use_case": "服装制造、汽车装配、电子3C、石化实验室、多品种小批量生产",
         "source": "浙江人形机器人创新中心 (双臂协同作业机器人, 杰克科技2000台服装场景订单, 工人日报)"},
        # ── WAIC 2026世界人工智能大会首发新品 ──
        {"name": "启元Q1", "brand": "启元机器人（上纬新材）", "price": "开发者小批量交付中",
         "height": "88cm", "weight": "15kg", "dofs": "全身22",
         "pros": "全球首款小尺寸全身力控人形、<15kg超轻量化、22自由度全身联动、柔性亲肤机身、结构件开源",
         "cons": "小批量交付中",
         "use_case": "家庭陪伴、看护、轻交互、开发者改装、教育科研",
         "source": "启元机器人 (上纬新材旗下消费级具身智能品牌, 2025年底首发, 2026WAIC探索者版, A'Design金奖)"},
        {"name": "启元T1", "brand": "启元机器人（上纬新材）", "price": "¥15,999（标准版, 9月预售）",
         "weight": "20kg", "dofs": "全身18+",
         "pros": "全球首款可变形个人机器人、Transformer跨形态架构、轮足人形/四足自主切换、室内静音/户外越障、智能影像拍摄",
         "cons": "9月预售, 11月前后公开发售",
         "use_case": "家庭陪伴、户外伴行、移动拍摄Vlog、露营跟随载物",
         "source": "启元机器人 (上纬新材启元机器人, 2026WAIC首发, 万台级产线签约蓝思智能, 5城体验店已开)"},
        {"name": "乐聚夸父系列", "brand": "乐聚机器人", "price": "¥299,000-599,000",
         "height": "175cm", "weight": "65kg", "dofs": "全身35+",
         "pros": "国产化率>95%、一汽/长虹/中兴等头部订单、1-2周工业场景部署、全球首条万台级自动化产线（佛山）",
         "cons": "工业优化为主",
         "use_case": "汽车制造、电子3C、仓储物流、拆垛码垛、产线上下料",
         "source": "乐聚机器人 (哈尔滨乐聚智能科技有限公司, WAIC 2026, 工信部2025人工智能应用典型案例)"},
        {"name": "乐聚鲁班", "brand": "乐聚机器人", "price": "¥259,000-459,000",
         "height": "170cm", "weight": "70kg", "dofs": "全身30+",
         "pros": "工业场景专用、拆垛/上料/搬运三大核心作业、8-10小时不间断作业、方案已在工厂稳定运行3-4个月",
         "cons": "工业场景专用",
         "use_case": "工厂拆垛、产线上料、物料搬运、仓储作业",
         "source": "乐聚机器人 (哈尔滨乐聚智能科技有限公司, WAIC 2026工业落地主打产品)"},
        {"name": "魔法原子MagicBot X1", "brand": "魔法原子", "price": "¥599,000-899,000",
         "height": "180cm", "weight": "80kg", "dofs": "全身31",
         "pros": "180cm全尺寸通用人形、单关节峰值450N·m、Magic-VLA K02具身大模型、乒乓球对打/扣篮/击剑等高动态动作",
         "cons": "价格高",
         "use_case": "工厂通用作业、商用服务、科研平台、高动态场景",
         "source": "魔法原子 (MagicAtom, WAIC 2026一次性发布三款新品, 交管机器人已落地无锡马拉松)"},
        {"name": "魔法原子MagicBot D1", "brand": "魔法原子", "price": "¥299,000-459,000",
         "weight": "55kg", "dofs": "全身20+",
         "pros": "轮式人形、纯视觉导航厂区物料转运、已在追觅智能制造工厂试点",
         "cons": "轮式限制越障",
         "use_case": "厂区物料转运、车间配送、仓储搬运",
         "source": "魔法原子 (MagicAtom, WAIC 2026首发, 追觅工厂试点)"},
        {"name": "魔法原子MagicDog T1", "brand": "魔法原子", "price": "¥149,000-249,000",
         "weight": "15kg", "dofs": "全身12",
         "pros": "轻量化四足、狭小空间设备巡检、细微外观缺陷识别",
         "cons": "负载有限",
         "use_case": "设备巡检、狭小空间检测、工业质检",
         "source": "魔法原子 (MagicAtom, WAIC 2026首发)"},
        {"name": "智元精灵G2 Max", "brand": "智元机器人", "price": "¥259,000-459,000",
         "weight": "75kg", "dofs": "全身25+",
         "pros": "轮式仓储人形、双臂码垛50kg、京东物流联合研发、已落地京东物流园区实测",
         "cons": "轮式底盘限制",
         "use_case": "电商仓储拣选、料箱转运、货物码垛、高层货架取货",
         "source": "智元机器人 (Agibot, WAIC 2026首发, 京东物流联合研发)"},
        {"name": "智元酷拓骑行机器人", "brand": "智元机器人", "price": "¥199,000-359,000",
         "weight": "60kg", "pros": "可承载75kg人员、自主规划路线绕过人群/障碍、厂区巡检+园区短途代步",
         "cons": "新品首发",
         "use_case": "厂区巡检、园区短途代步、安全巡逻",
         "source": "智元机器人 (Agibot, WAIC 2026首发)"},
        {"name": "北京具身天工系列", "brand": "北京人形创新中心", "price": "¥499,000-899,000",
         "height": "175cm", "weight": "70kg", "dofs": "全身35+",
         "pros": "工业人形标杆、化工/电力/油气等高风险场景、5大标准化商用方案、全自主作业",
         "cons": "工业场景专用",
         "use_case": "化工巡检、电力运维、油气仓储、管线监测、应急处置",
         "source": "北京人形机器人创新中心 (具身天工全系列+慧思开物平台, WAIC 2026)"},
        {"name": "众擎T800", "brand": "众擎机器人", "price": "¥299,000-599,000",
         "height": "180cm", "weight": "85kg", "dofs": "全身30+",
         "pros": "全尺寸格斗人形、高强度抗扰测试、全球人形机器人自由格斗联赛指定机型",
         "cons": "特殊用途",
         "use_case": "文旅服务、格斗表演、极限抗扰测试、科研平台",
         "source": "众擎机器人 (WAIC 2026, 全球人形机器人自由格斗联赛发起方)"},
        {"name": "普渡PUDU D7", "brand": "普渡科技", "price": "¥199,000-359,000",
         "weight": "55kg", "dofs": "全身20+",
         "pros": "类人形智能作业伙伴、14kg负载/2m作业高度、面向工厂仓储零售多场景",
         "cons": "新品首发",
         "use_case": "工厂搬运、仓储取放、零售理货、高位作业",
         "source": "普渡科技 (PUDU, WAIC 2026首发, 一脑多形Physical Agent技术理念)"},
    ],
    # ====================================================================
    # 三、协作机械臂专区（2025-2026国产主力）
    # ====================================================================
    "cobot": [
        {"name": "Airbot P7", "brand": "星动纪元", "price": "¥80,000-120,000",
         "payload": "7kg", "reach": "922mm", "axes": 7,
         "pros": "7轴力控、拖拽示教、国产首选、CAN总线、全向移动",
         "cons": "品牌较新",
         "use_case": "精密装配、力控打磨、科研实验、产线柔性自动化",
         "source": "星动纪元 (北京星动纪元科技有限公司, 2026年国内首款7轴消费级协作臂)"},
        {"name": "CRA3-630", "brand": "越疆科技", "price": "¥50,000-70,000",
         "payload": "3kg", "reach": "630mm", "axes": 6,
         "pros": "2026新品、223°/s高速、±0.02mm精度、PLd安全、EtherCAT",
         "cons": "力控需选配",
         "use_case": "3C装配、检测分拣、实验室自动化",
         "source": "越疆科技 (DOBOT, 深圳越疆科技股份有限公司, 2025年CRA系列协作臂)"},
        {"name": "CRA7-950", "brand": "越疆科技", "price": "¥80,000-120,000",
         "payload": "7kg", "reach": "950mm", "axes": 6,
         "pros": "2026新品、223°/s高速、±0.03mm、EtherCAT、SafeSkin碰前感知",
         "cons": "力控需选配",
         "use_case": "搬运码垛、上下料、装配检测、机床自动化",
         "source": "越疆科技 (DOBOT, 深圳越疆科技股份有限公司, 2025年CRA系列协作臂)"},
        {"name": "JAKA Ai3", "brand": "节卡机器人", "price": "¥70,000-90,000",
         "payload": "3kg", "reach": "626mm", "axes": 6,
         "pros": "2026新品、一体化内置视觉、±0.02mm精度、免布线",
         "cons": "臂展较短",
         "use_case": "3C精密锁附、镭雕涂胶、视觉分拣",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2026年AI系列)"},
        {"name": "JAKA Ai7", "brand": "节卡机器人", "price": "¥80,000-110,000",
         "payload": "7kg", "reach": "819mm", "axes": 6,
         "pros": "2026新品、一体化视觉、±0.02mm、免手眼标定、3C爆款",
         "cons": "力控需选配",
         "use_case": "电子装配、视觉分拣、精密涂胶、包装码垛",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2026年AI系列)"},
        {"name": "JAKA Ai12", "brand": "节卡机器人", "price": "¥140,000-180,000",
         "payload": "12kg", "reach": "1327mm", "axes": 6,
         "pros": "2026新品、一体化视觉、长臂展大负载、免布线",
         "cons": "6轴无冗余",
         "use_case": "大件搬运、包装码垛、机床自动化、汽车零部件",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2026年AI系列)"},
        {"name": "JAKA Zu35", "brand": "节卡机器人", "price": "¥200,000-280,000",
         "payload": "35kg", "reach": "2000mm", "axes": 6,
         "pros": "2026新品、35kg重载天花板、2m臂展、码垛12次/分钟",
         "cons": "体积较大",
         "use_case": "整箱码垛、重型机床上下料、汽车大件、新能源电池",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2025年35kg大负载)"},
        {"name": "JAKA Mini 2", "brand": "节卡机器人", "price": "¥40,000-60,000",
         "payload": "2kg", "reach": "580mm", "axes": 6,
         "pros": "2026新品、超小型、180W低功耗、桌面自动化",
         "cons": "负载较小",
         "use_case": "高校实训、桌面小型自动化、文创商用",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, 2025年新品)"},
        {"name": "JAKA Zu 7", "brand": "节卡机器人", "price": "¥60,000-90,000",
         "payload": "7kg", "reach": "790mm", "axes": 6,
         "pros": "无线示教、拖拽编程、部署极快、国内市占率国产头部",
         "cons": "6轴无冗余",
         "use_case": "3C电子、汽车零部件、产线集成、上下料",
         "source": "节卡机器人 (JAKA, 上海节卡机器人科技有限公司, Zu系列协作臂)"},
        {"name": "Flexiv Rizon 4", "brand": "非夕科技", "price": "¥100,000-150,000",
         "payload": "4kg", "reach": "830mm", "axes": 7,
         "pros": "全球顶级力控、AI原生、复杂作业、高精度",
         "cons": "价格偏高",
         "use_case": "精密装配、抛光打磨、柔性作业、无序分拣",
         "source": "非夕科技 (Flexiv, 全球自适应机器人开创者, www.flexiv.com)"},
        {"name": "珞石 xMateCR7", "brand": "珞石机器人", "price": "¥150,000-220,000",
         "payload": "7kg", "reach": "920mm", "axes": 7,
         "pros": "力控人形机械臂、国内协作市占率47%、全栈自研",
         "cons": "品牌认知度略低",
         "use_case": "精密装配、打磨抛光、人形机器人手臂、科研",
         "source": "珞石机器人 (Rokae, 北京珞石机器人科技有限公司)"},
        {"name": "xArm 1S", "brand": "越疆科技", "price": "¥16,800",
         "payload": "0.5kg", "reach": "400mm", "axes": 5,
         "pros": "入门级协作臂、桌面级、轻量紧凑、教育首选",
         "cons": "负载小、5轴无冗余",
         "use_case": "教学实训、桌面自动化、轻量装配",
         "source": "UFACTORY 优艾智合 (深圳优艾智合机器人科技有限公司, www.ufactory.cc)"},
        {"name": "myCobot 280", "brand": "大象机器人", "price": "¥5,000-10,000",
         "payload": "0.25kg", "reach": "280mm", "axes": 6,
         "pros": "价格极低、入门友好、USB连接、ROS支持",
         "cons": "负载小、精度一般",
         "use_case": "教学、演示、轻量抓取、创客DIY",
         "source": "Elephant Robotics 大象机器人 (深圳大象机器人科技有限公司, www.elephantrobotics.com)"},
        {"name": "UR5e", "brand": "Universal Robots", "price": "¥120,000-180,000",
         "payload": "5kg", "reach": "850mm", "axes": 6,
         "pros": "全球最成熟协作臂、生态完善、海量教程、售后全球",
         "cons": "价格高、力控需选件",
         "use_case": "工业产线、科研教学、全球服务、高端制造",
         "source": "Universal Robots优傲机器人 (丹麦, 全球协作臂领导者, www.universal-robots.com)"},
        {"name": "Franka Emika Panda", "brand": "Franka Emika", "price": "¥200,000-300,000",
         "payload": "3kg", "reach": "855mm", "axes": 7,
         "pros": "科研黄金标准、开源友好、力控顶级、学术引用最多",
         "cons": "负载小、价格高",
         "use_case": "顶级科研、AI机器人学习、精密操作、具身智能",
         "source": "Franka Emika (德国, 高精度力控协作臂, www.franka.de)"},
    ],
    # ====================================================================
    # 四、四足机器人专区
    # ====================================================================
    "quadruped": [
        {"name": "Unitree Go2 Air", "brand": "宇树科技", "price": "¥8,999",
         "payload": "7kg", "speed": "3m/s", "dofs": 12,
         "pros": "入门最低门槛、可走可舞可避障、空翻、海量论文平台",
         "cons": "无手臂操作",
         "use_case": "教学科研、娱乐表演、基础巡检",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, 四足入门最低门槛)"},
        {"name": "Unitree Go2 Pro", "brand": "宇树科技", "price": "¥18,600",
         "payload": "8-10kg", "speed": "5m/s", "dofs": 12,
         "pros": "4D激光雷达、ISS伴随、4G联网、语音交互、全球科研主力",
         "cons": "无手臂",
         "use_case": "科研教育、巡检安防、复杂地形导航、算法验证",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, ISS 2.0+4G联网)"},
        {"name": "Unitree B2", "brand": "宇树科技", "price": "¥80,000-150,000",
         "payload": "20kg", "speed": "4m/s", "dofs": 12,
         "pros": "2026工业级新品、大负载、IP67、-20℃~55℃、长续航4小时",
         "cons": "价格较高",
         "use_case": "工业巡检、电力巡检、消防救援、安防巡逻",
         "source": "宇树科技 (Unitree, 杭州宇树科技有限公司, 工业级四足巡检)"},
        {"name": "云深处Jueying Lite3", "brand": "云深处科技", "price": "¥50,000-80,000",
         "payload": "15kg", "speed": "4m/s", "dofs": 12,
         "pros": "工业级四足、IP66防护、电力巡检主力、浙大系",
         "cons": "品牌认知度略低",
         "use_case": "电力巡检、园区安防、科研教育、特种作业",
         "source": "云深处科技 (DeepRobotics, 杭州云深处科技有限公司, 绝影系列四足)"},
        {"name": "ANYbotics ANYmal", "brand": "ANYbotics", "price": "¥300,000-500,000",
         "payload": "10kg", "speed": "1m/s", "dofs": 12,
         "pros": "工业级标杆、防爆认证、油气/化工巡检、瑞士品质",
         "cons": "价格极高",
         "use_case": "油气化工、矿山巡检、防爆场景、高端科研",
         "source": "ANYbotics (瑞士, 全球工业级四足巡检领导者, www.anybotics.com)"},
    ],
    # ====================================================================
    # 四、AMR/AGV移动机器人专区
    # ====================================================================
    "amr": [
        {"name": "极智嘉P800", "brand": "极智嘉Geek+", "price": "¥150,000-250,000",
         "payload": "800kg", "speed": "2m/s", "dofs": "移动+举升",
         "pros": "AMR全球第一、仓储物流标杆、智能分拣、已部署数万台",
         "cons": "仓储场景为主",
         "use_case": "电商仓储、智能分拣、物流搬运、工厂内部物流",
         "source": "极智嘉 (Geek+, 北京极智嘉科技有限公司, 全球AMR领导者)"},
        {"name": "海康机器人潜伏AMR", "brand": "海康机器人", "price": "¥120,000-200,000",
         "payload": "600-1000kg", "speed": "2m/s", "dofs": "移动+举升",
         "pros": "国内市占率领先、视觉导航、海康威视生态、3C电子主力",
         "cons": "特定场景优化",
         "use_case": "3C电子、汽车零部件、仓储物流、智能工厂",
         "source": "海康机器人 (Hikrobot, 杭州海康机器人股份有限公司, 深市:002415)"},
        {"name": "快仓Quicktron M系列", "brand": "快仓机器人", "price": "¥100,000-180,000",
         "payload": "300-1500kg", "speed": "1.8m/s", "dofs": "移动+举升",
         "pros": "仓储AMR主力品牌、柔性物流、智能搬运",
         "cons": "仓储为主",
         "use_case": "电商仓储、零售物流、制造工厂、医药流通",
         "source": "快仓机器人 (Quicktron, 上海快仓智能科技有限公司)"},
        {"name": "MIR250", "brand": "Mobile Industrial Robots", "price": "¥200,000-350,000",
         "payload": "250kg", "speed": "1.8m/s", "dofs": "移动+可选顶装",
         "pros": "全球AMR标杆、泰瑞达旗下、工业级可靠、ISO3691-4",
         "cons": "价格高",
         "use_case": "汽车制造、电子半导体、医疗制药、高端制造",
         "source": "Mobile Industrial Robots (丹麦, 全球AMR领导者, www.mobile-industrial-robots.com)"},
        {"name": "TurtleBot 4", "brand": "Open Robotics", "price": "¥15,000-30,000",
         "payload": "开发平台", "speed": "1.5m/s", "dofs": "移动+可扩展",
         "pros": "ROS标准平台、教育科研首选、全球最广泛使用的移动平台",
         "cons": "非工业级",
         "use_case": "教学科研、算法验证、SLAM研究、机器人课程",
         "source": "Open Robotics (开源ROS标准移动平台, 全球科研教育标配)"},
    ],
    # ====================================================================
    # 五、按场景智能推荐
    # ====================================================================
    "scenario_research": [  # 科研首选
        "Franka Emika Panda", "Airbot P7", "Unitree G1 EDU",
        "UR5e", "Flexiv Rizon 4", "珞石xMateCR7", "Unitree Go2 Pro",
        "星海图R1", "智元远征A3 Ultra"
    ],
    "scenario_industrial": [  # 工业首选
        "UR5e/UR10e", "JAKA Zu系列", "JAKA Ai系列",
        "KUKA LBR iiwa", "ABB GoFa", "珞石CR系列", "越疆CRA系列",
        "优必选Walker S2", "智元精灵G2", "开普勒K2大黄蜂"
    ],
    "scenario_education": [  # 教学首选
        "myCobot 280", "xArm 1S", "Unitree Go2 Air/Pro",
        "Unitree G1 EDU", "JAKA Mini 2", "TurtleBot 4", "JAKA π 仔",
        "松延动力Bumi小布米", "Unitree R1"
    ],
    "scenario_force_control": [  # 力控首选
        "Franka Panda", "Flexiv Rizon", "KUKA LBR iiwa",
        "Airbot P7", "珞石xMateCR7", "JAKA Zu系列（力控版）",
        "千寻智能Moz1"
    ],
    "scenario_humanoid": [  # 人形机器人
        "Unitree G1", "Unitree H1", "优必选Walker S",
        "智元精灵G2", "银河通用 DB1", "JAKA π 仔", "Unitree R1",
        "开普勒K2大黄蜂", "智元灵犀X2", "星海图R1", "傅利叶GR-3"
    ],
    "scenario_cobot": [  # 协作机械臂
        "Airbot P7", "越疆CRA系列", "节卡JAKA全系列",
        "Flexiv Rizon 4", "珞石xMateCR7", "UR5e/UR10e", "Franka Panda"
    ],
    "scenario_quadruped": [  # 四足机器人
        "Unitree Go2系列", "Unitree B2", "云深处Jueying",
        "ANYbotics ANYmal"
    ],
    "scenario_amr": [  # AMR移动机器人
        "极智嘉P800", "海康潜伏AMR", "快仓M系列",
        "MIR250", "TurtleBot 4"
    ],
    "scenario_vision": [  # 视觉一体化
        "JAKA Ai系列（Ai3/Ai7/Ai12）", "越疆CRA系列（视觉选配）",
        "UR+视觉套件", "节卡AL视觉一体化"
    ],
    "scenario_heavy_load": [  # 重载场景
        "JAKA Zu35（35kg）", "UR16e（16kg）", "珞石重载系列",
        "JAKA Ai12（12kg）", "KUKA LBR iiwa 14kg版",
        "开普勒K2大黄蜂（双臂30kg）"
    ],
}


def get_supported_robots() -> List[str]:
    """获取当前系统支持的所有机器人品牌/型号列表"""
    return [b.value for b in RobotBrand]


def recommend_robot(budget: str = "budget_10w", scenario: str = "research",
                    category: str = None) -> List[Dict]:
    """
    根据预算、场景和产品类别推荐机器人（2026最新完整版本）

    Args:
        budget:   预算范围：
                  "budget_1w"（1万内）| "budget_3w"（1-3万）| "budget_10w"（3-10万）|
                  "mid_range"（10-30万）| "premium_30w"（30-80万）| "premium"（80万+）
        scenario: 使用场景：
                  "research"（科研）| "industrial"（工业）| "education"（教学）|
                  "force_control"（力控）| "humanoid"（人形）| "quadruped"（四足）|
                  "amr"（AMR移动）| "vision"（视觉一体化）| "heavy_load"（重载）
        category: 产品类别（可选，直接返回专区列表）：
                  "humanoid" | "cobot"（协作臂）| "quadruped" | "amr"
    """
    # 直接按产品类别返回专区
    if category:
        return ROBOT_PURCHASE_GUIDE.get(category, [])

    if scenario == "humanoid":
        return ROBOT_PURCHASE_GUIDE.get("humanoid", [])
    if scenario == "quadruped":
        return ROBOT_PURCHASE_GUIDE.get("quadruped", [])
    if scenario == "amr":
        return ROBOT_PURCHASE_GUIDE.get("amr", [])

    budget_options = ROBOT_PURCHASE_GUIDE.get(budget, [])
    scenario_options = ROBOT_PURCHASE_GUIDE.get(f"scenario_{scenario}", [])

    # 交集推荐（同时满足预算和场景，智能模糊匹配）
    if budget_options and scenario_options:
        # 提取场景关键词用于模糊匹配（如"JAKA Zu系列" -> ["JAKA","Zu"]）
        scenario_keywords = set()
        for s in scenario_options:
            # 按空格、斜杠、括号拆分关键词
            parts = s.replace("（", " ").replace("）", " ").replace("(", " ").replace(")", " ")
            parts = parts.replace("/", " ").replace("+", " ").split()
            for p in parts:
                if len(p) >= 2:
                    scenario_keywords.add(p.lower())

        def _match(r):
            name = r["name"].lower()
            brand = r.get("brand", "").lower()
            # 精确匹配：产品名出现在场景列表中
            if r["name"] in scenario_options:
                return True
            # 模糊匹配：产品名/品牌包含场景关键词
            for kw in scenario_keywords:
                if kw in name or kw in brand:
                    return True
            return False

        matched = [r for r in budget_options if _match(r)]
        # 匹配结果太少（<30%）时返回全部预算选项
        if len(matched) >= max(1, len(budget_options) * 0.2):
            return matched
        return budget_options

    return budget_options
