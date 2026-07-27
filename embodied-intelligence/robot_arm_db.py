"""
机械臂配置数据库
支持多种品牌/型号的真实机械臂部署配置
包含：关节参数、工作空间、通信协议、安全限制、部署条件等

使用方法：
    from robot_arm_db import RobotArmDB, get_arm_config
    config = get_arm_config("franka_panda")
    # 或自定义选择
    db = RobotArmDB()
    config = db.get_config("kuka_iiwa")
"""

from typing import Dict, Any, List, Optional, Tuple
import json
import os


# ============================================================
# 机械臂配置数据库（内置主流型号）
# ============================================================

ARM_DATABASE = {
    # ============================================================
    # Franka Emika (7轴协作臂)
    # ============================================================
    "franka_panda": {
        "brand": "Franka Emika",
        "model": "Panda",
        "type": "collaborative",
        "degrees_of_freedom": 7,
        "payload_kg": 3.0,
        "reach_mm": 855,
        "weight_kg": 18.0,

        # 关节参数
        "joint_indices": [0, 1, 2, 3, 4, 5, 6],
        "joint_names": [
            "panda_joint1", "panda_joint2", "panda_joint3",
            "panda_joint4", "panda_joint5", "panda_joint6", "panda_joint7"
        ],
        "joint_limits": {
            "lower": [-2.967, -1.832, -2.967, -3.141, -2.967, -0.087, -2.967],
            "upper": [2.967, 1.832, 2.967, -0.069, 2.967, 3.822, 2.967],
            "speed": [2.175, 2.175, 2.175, 2.175, 2.610, 2.610, 2.610],  # rad/s
            "effort": [87.0, 87.0, 87.0, 87.0, 12.0, 12.0, 12.0],  # Nm
        },
        "start_joint_positions": [0, -0.785, 0, -2.356, 0, 1.571, 0.785],
        "ee_link": "panda_link8",

        # 工作空间
        "workspace": {
            "radius_m": 0.855,
            "min_z_m": 0.0,
            "max_z_m": 1.2,
        },

        # 通信配置
        "communication": {
            "protocol": "libfranka",  # Franka官方C++库
            "default_host": "192.168.3.100",
            "default_port": 8080,
            "alternative_ports": [5000, 80, 443],
            "required_packages": ["libfranka", "franka_ros"],
            "connection_type": "ethernet",
        },

        # 仿真配置
        "simulation": {
            "urdf_path": "franka_panda/panda.urdf",
            "pybullet_available": True,
        },

        # 安全限制
        "safety": {
            "max_joint_speed": 2.175,  # rad/s
            "max_cartesian_speed": 2.0,  # m/s
            "max_force_translational": 100.0,  # N
            "max_force_rotational": 10.0,  # Nm
            "max_payload": 3.0,  # kg
            "collision_sensitivity": "high",
            "has_self_collision_guard": True,
            "has_torque_sensors": True,
        },

        # 部署条件
        "deployment_requirements": {
            "power_voltage": "24V DC",
            "power_current": "10A",
            "network": "Gigabit Ethernet",
            "environment_temp": "10-35°C",
            "humidity": "20-80% (non-condensing)",
            "min_compute_requirements": {
                "cpu_cores": 4,
                "ram_gb": 8,
                "os": "Linux (Ubuntu 20.04+) 或 Windows 10/11",
            },
        },
    },

    # ============================================================
    # KUKA iiwa (7轴协作臂)
    # ============================================================
    "kuka_iiwa14": {
        "brand": "KUKA",
        "model": "iiwa 14 R820",
        "type": "collaborative",
        "degrees_of_freedom": 7,
        "payload_kg": 14.0,
        "reach_mm": 820,
        "weight_kg": 29.9,

        "joint_indices": [0, 1, 2, 3, 4, 5, 6],
        "joint_names": [
            "iiwa_joint_1", "iiwa_joint_2", "iiwa_joint_3",
            "iiwa_joint_4", "iiwa_joint_5", "iiwa_joint_6", "iiwa_joint_7"
        ],
        "joint_limits": {
            "lower": [-2.967, -2.094, -2.967, -2.094, -2.967, -2.094, -3.054],
            "upper": [2.967, 2.094, 2.967, 2.094, 2.967, 2.094, 3.054],
            "speed": [1.710, 1.710, 1.745, 2.234, 2.443, 3.142, 3.142],
            "effort": [320, 320, 176, 176, 110, 40, 40],
        },
        "start_joint_positions": [0, 0.35, 0, -1.57, 0, 1.20, 0],
        "ee_link": "iiwa_link_ee",

        "workspace": {
            "radius_m": 0.820,
            "min_z_m": -0.1,
            "max_z_m": 1.3,
        },

        "communication": {
            "protocol": "FRI (Fast Robot Interface)",
            "default_host": "192.168.1.10",
            "default_port": 30200,
            "alternative_ports": [30201, 30202],
            "required_packages": ["kuka_fri", "iiwa_stack"],
            "connection_type": "ethernet",
        },

        "simulation": {
            "urdf_path": "kuka_iiwa/iiwa14.urdf",
            "pybullet_available": True,
        },

        "safety": {
            "max_joint_speed": 3.142,
            "max_cartesian_speed": 1.5,
            "max_force_translational": 150.0,
            "max_force_rotational": 15.0,
            "max_payload": 14.0,
            "collision_sensitivity": "medium",
            "has_self_collision_guard": True,
            "has_torque_sensors": True,
        },

        "deployment_requirements": {
            "power_voltage": "48V DC / 3x400V AC",
            "power_current": "16A",
            "network": "Gigabit Ethernet",
            "environment_temp": "5-45°C",
            "humidity": "10-90%",
            "min_compute_requirements": {
                "cpu_cores": 4,
                "ram_gb": 8,
                "os": "Linux (Ubuntu 18.04+) 或 Windows 10",
            },
        },
    },

    # ============================================================
    # Universal Robots UR5e (6轴协作臂)
    # ============================================================
    "ur_ur5e": {
        "brand": "Universal Robots",
        "model": "UR5e",
        "type": "collaborative",
        "degrees_of_freedom": 6,
        "payload_kg": 5.0,
        "reach_mm": 850,
        "weight_kg": 20.6,

        "joint_indices": [0, 1, 2, 3, 4, 5],
        "joint_names": [
            "shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint",
            "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"
        ],
        "joint_limits": {
            "lower": [-3.142, -3.142, -3.142, -3.142, -3.142, -3.142],
            "upper": [3.142, 3.142, 3.142, 3.142, 3.142, 3.142],
            "speed": [3.142, 3.142, 3.142, 6.283, 6.283, 6.283],
            "effort": [150, 150, 150, 28, 28, 28],
        },
        "start_joint_positions": [0, -1.57, 1.57, -1.57, -1.57, 0],
        "ee_link": "wrist_3_link",

        "workspace": {
            "radius_m": 0.850,
            "min_z_m": -0.1,
            "max_z_m": 1.3,
        },

        "communication": {
            "protocol": "RTDE (Real-Time Data Exchange)",
            "default_host": "192.168.56.101",
            "default_port": 30004,
            "alternative_ports": [29999, 30001, 30002, 30003, 30005, 30006],
            "required_packages": ["ur_rtde", "ur_robot_driver"],
            "connection_type": "ethernet",
        },

        "simulation": {
            "urdf_path": "ur_description/ur5e.urdf",
            "pybullet_available": True,
        },

        "safety": {
            "max_joint_speed": 6.283,
            "max_cartesian_speed": 1.5,
            "max_force_translational": 110.0,
            "max_force_rotational": 10.0,
            "max_payload": 5.0,
            "collision_sensitivity": "high",
            "has_self_collision_guard": True,
            "has_torque_sensors": True,
        },

        "deployment_requirements": {
            "power_voltage": "48V DC",
            "power_current": "10A",
            "network": "100 Mbps Ethernet",
            "environment_temp": "0-50°C",
            "humidity": "0-90%",
            "min_compute_requirements": {
                "cpu_cores": 2,
                "ram_gb": 4,
                "os": "Linux 或 Windows",
            },
        },
    },

    # ============================================================
    # ABB YuMi (双14轴协作臂)
    # ============================================================
    "abb_yumi": {
        "brand": "ABB",
        "model": "YuMi IRB 14000",
        "type": "collaborative_dual_arm",
        "degrees_of_freedom": 14,
        "payload_kg": 0.5,
        "reach_mm": 559,
        "weight_kg": 38.0,

        "joint_indices": list(range(14)),
        "joint_names": [f"yumi_joint_{i}" for i in range(14)],
        "joint_limits": {
            "lower": [-2.94, -2.50, -2.94, -2.15, -2.94, -1.92, -2.94] * 2,
            "upper": [2.94, 0.75, 2.94, 1.39, 2.94, 2.27, 2.94] * 2,
            "speed": [2.51] * 14,
            "effort": [35.0, 35.0, 15.0, 15.0, 8.0, 8.0, 4.0] * 2,
        },
        "start_joint_positions": [0, -1.2, 0, -0.9, 0, 0.8, 0] * 2,
        "ee_link": "gripper_center_link",

        "workspace": {
            "radius_m": 0.559,
            "min_z_m": 0.0,
            "max_z_m": 1.0,
        },

        "communication": {
            "protocol": "EGM (Externally Guided Motion)",
            "default_host": "192.168.125.1",
            "default_port": 6510,
            "alternative_ports": [6511],
            "required_packages": ["abb_libegm", "abb_robot_driver"],
            "connection_type": "ethernet",
        },

        "simulation": {
            "urdf_path": "abb_irb14000/yumi.urdf",
            "pybullet_available": True,
        },

        "safety": {
            "max_joint_speed": 2.51,
            "max_cartesian_speed": 1.0,
            "max_force_translational": 50.0,
            "max_force_rotational": 5.0,
            "max_payload": 0.5,
            "collision_sensitivity": "high",
            "has_self_collision_guard": True,
            "has_torque_sensors": True,
        },

        "deployment_requirements": {
            "power_voltage": "24V DC",
            "power_current": "8A",
            "network": "Gigabit Ethernet",
            "environment_temp": "5-45°C",
            "humidity": "20-80%",
            "min_compute_requirements": {
                "cpu_cores": 4,
                "ram_gb": 8,
                "os": "Linux (Ubuntu 18.04+)",
            },
        },
    },

    # ============================================================
    # Dobot Magician (4轴教育/轻量臂)
    # ============================================================
    "dobot_magician": {
        "brand": "Dobot",
        "model": "Magician",
        "type": "educational_lightweight",
        "degrees_of_freedom": 4,
        "payload_kg": 0.5,
        "reach_mm": 320,
        "weight_kg": 3.7,

        "joint_indices": [0, 1, 2, 3],
        "joint_names": ["base_joint", "shoulder_joint", "elbow_joint", "wrist_joint"],
        "joint_limits": {
            "lower": [-3.142, -2.618, -2.618, -3.142],
            "upper": [3.142, 2.618, 2.618, 3.142],
            "speed": [3.142, 2.094, 2.094, 6.283],
            "effort": [10.0, 10.0, 5.0, 2.0],
        },
        "start_joint_positions": [0, 0.5, -1.0, 0],
        "ee_link": "end_effector_link",

        "workspace": {
            "radius_m": 0.320,
            "min_z_m": -0.05,
            "max_z_m": 0.5,
        },

        "communication": {
            "protocol": "Dobot Protocol (Serial)",
            "default_host": "COM3",
            "default_port": 115200,
            "alternative_ports": [9600, 57600, 230400],
            "required_packages": ["pyserial", "dobot"],
            "connection_type": "usb_serial",
        },

        "simulation": {
            "urdf_path": None,  # 无内置URDF
            "pybullet_available": False,
        },

        "safety": {
            "max_joint_speed": 6.283,
            "max_cartesian_speed": 0.5,
            "max_force_translational": 20.0,
            "max_force_rotational": 2.0,
            "max_payload": 0.5,
            "collision_sensitivity": "low",
            "has_self_collision_guard": False,
            "has_torque_sensors": False,
        },

        "deployment_requirements": {
            "power_voltage": "12V DC",
            "power_current": "3A",
            "network": "USB 2.0",
            "environment_temp": "0-40°C",
            "humidity": "20-80%",
            "min_compute_requirements": {
                "cpu_cores": 1,
                "ram_gb": 1,
                "os": "Windows 7+ 或 Linux 或 macOS",
            },
        },
    },

    # ============================================================
    # AIRBOT P7 (七轴科研级机械臂 - 内置旭日5 AI芯片)
    # ============================================================
    "airbot_p7": {
        "brand": "AIRBOT (求之科技)",
        "model": "P7",
        "type": "research_intelligent",
        "degrees_of_freedom": 7,
        "payload_kg": 3.0,
        "reach_mm": 640,
        "weight_kg": 5.0,
        "repeatability_mm": 0.1,
        "protection_rating": "IP54",
        "power_consumption_w": 60,

        # 关节参数（J1-J7七轴）
        "joint_indices": [0, 1, 2, 3, 4, 5, 6],
        "joint_names": ["J1", "J2", "J3", "J4", "J5", "J6", "J7"],
        "joint_limits": {
            "lower": [-3.142, -3.142, -3.142, -3.142, -3.142, -3.142, -3.142],
            "upper": [3.142, 3.142, 3.142, 3.142, 3.142, 3.142, 3.142],
            "speed": [3.142] * 7,  # rad/s
            "effort": [30.0] * 7,   # Nm
        },
        "start_joint_positions": [0, -1.57, 0, 1.57, 0, -1.57, 0],
        "ee_link": "end_effector_link",

        # 工作空间
        "workspace": {
            "radius_m": 0.640,
            "min_z_m": -0.1,
            "max_z_m": 0.9,
        },

        # 通信配置（多接口）
        "communication": {
            "protocol": "AIRBOT SDK (Python/C++/ROS2)",
            "default_host": "192.168.1.100",
            "default_port": 8080,
            "alternative_ports": [3000, 5000, 9090],
            "required_packages": ["airbot_sdk", "rclpy", "python-can"],
            "connection_type": "ethernet",
            "interfaces": {
                "end_effector": ["USB Type-C 3.0", "USB Type-C 2.0"],
                "base": ["Ethernet", "CAN FD", "Power 24-48V/5A"],
            },
            "supported_bus": ["CAN FD", "Ethernet TCP/IP"],
        },

        # 内置AI计算能力
        "edge_ai": {
            "chip": "旭日5 (Sunrise 5)",
            "ai_tops": 10.0,
            "cpu_cores": 8,
            "cpu_type": "ARM Cortex-A55",
            "native_supported_models": ["Transformer", "ViT", "CNN"],
            "standalone_capabilities": [
                "目标检测",
                "深度估算",
                "操作策略推理",
                "视觉伺服控制",
            ],
            "deployment_modes": {
                "edge_only": "仅使用内置AI算力（无需外置计算设备）",
                "edge_plus_pc": "内置AI+PC混合计算",
                "pc_only": "纯外置PC计算（传统模式）",
            },
        },

        # 控制模式
        "control_modes": {
            "position": {
                "name": "位置控制",
                "description": "关节位置/笛卡尔空间位置控制",
                "supported": True,
            },
            "velocity": {
                "name": "速度控制",
                "description": "关节速度/笛卡尔空间速度控制",
                "supported": True,
            },
            "torque": {
                "name": "力矩控制",
                "description": "关节力矩控制/力反馈控制",
                "supported": True,
            },
            "gravity_compensation": {
                "name": "重力补偿",
                "description": "全域重力补偿，支持柔顺拖动示教",
                "supported": True,
            },
            "drag_teach": {
                "name": "拖动示教",
                "description": "手动拖拽录制操作流程，支持回放",
                "supported": True,
            },
        },

        # 仿真配置
        "simulation": {
            "urdf_path": "airbot_p7/airbot_p7.urdf",
            "pybullet_available": True,
        },

        # 安全限制
        "safety": {
            "max_joint_speed": 3.142,
            "max_cartesian_speed": 1.0,
            "max_force_translational": 80.0,
            "max_force_rotational": 8.0,
            "max_payload": 3.0,
            "collision_sensitivity": "medium",
            "has_self_collision_guard": True,
            "has_torque_sensors": True,
            "has_brake_lock": True,
            "brake_lock_description": "全关节内置抱闸，意外断电自动锁止",
        },

        # 末端执行器支持
        "end_effectors": {
            "g2p_gripper": {
                "name": "G2P二指夹爪",
                "type": "gripper",
                "brand": "AIRBOT (求之科技)",
                "series": "G2系列",
                "gripper_type": "平行二指夹爪",
                "degrees_of_freedom": 1,
                "actuation": "电机驱动",
                "weight_g": 200,
                "stroke_mm": 95,
                "max_force_n": 30,
                "repeatability_mm": 0.1,
                "close_time_s": 0.3,
                "control": {
                    "interface": "CAN",
                    "position_control": True,
                    "force_control": True,
                },
                "power": {
                    "voltage_v": 24,
                    "current_nominal_a": 1.15,
                },
                "sensors": {
                    "position": True,
                    "current": True,
                },
                "mount_type": "quick_change",
                "features": [
                    "平行二指结构",
                    "电机驱动开合",
                    "30N最大夹持力",
                    "95mm最大行程",
                    "CAN总线接口",
                    "快换安装方式",
                    "位置/力混合控制",
                ],
            },
            "inspire_hand": {
                "name": "因时灵巧手 (RH5DG2)",
                "type": "dexterous_hand",
                "brand": "因时机器人 (Inspire Robots)",
                "series": "RH5DG2系列",
                "fingers": 5,
                "degrees_of_freedom": 13,
                "joints": 18,
                "weight_g": 990,
                "repeatability_mm": 0.2,
                "grip_force": {
                    "thumb_n": 20,
                    "four_fingers_n": 10,
                    "resolution_n": 0.1,
                },
                "speed": {
                    "thumb_lateral_rotation": "60°-165°",
                    "palm_close_time_s": 0.8,
                },
                "sensors": {
                    "tactile": True,
                    "tactile_count": 8,
                    "tactile_range_n": 30,
                    "force": True,
                    "position": True,
                    "temperature": True,
                },
                "control_interface": ["EtherCAT", "CAN FD"],
                "power": {
                    "voltage": "14V-48V",
                    "current_static_mA": 290,
                    "current_max_A": 7.5,
                },
                "passive_load_kg": 8,
                "mount_type": "quick_change",
                "features": [
                    "13自由度18关节",
                    "8组多维触觉传感器(力觉+位置+温度)",
                    "±0.2mm指尖重复定位精度",
                    "≥20N拇指抓握力",
                    "8kg指尖被动载荷",
                    "≤0.8s手掌闭合时间",
                ],
            },
            "ql_brain_hand": {
                "name": "强脑灵巧手 (Revo 2)",
                "type": "dexterous_hand",
                "brand": "强脑科技 (BrainCo)",
                "series": "Revo 2系列",
                "fingers": 5,
                "degrees_of_freedom": 11,
                "active_joints": 6,
                "weight_g": 383,
                "repeatability_deg": 0.1,
                "grip_force": {
                    "five_finger_n": 50,
                    "pinch_n": 15,
                    "total_load_kg": 20,
                },
                "control": {
                    "frequency_hz": 1000,
                    "modes": ["位置", "速度", "电流"],
                },
                "sensors": {
                    "tactile": {
                        "pressure": True,
                        "friction": True,
                        "direction": True,
                        "proximity": True,
                    },
                    "position": True,
                    "current": True,
                },
                "control_interface": ["RS485", "CAN FD", "EtherCAT"],
                "power": {
                    "voltage": "12V-64V",
                    "protection": ["过流保护", "堵转保护", "高温保护", "防撞保护"],
                },
                "mount_type": "quick_change",
                "versions": {
                    "basic": {"voltage": "12-28V", "interface": "485, CAN FD"},
                    "pro": {"voltage": "12-64V", "interface": "485, CAN FD, EtherCAT"},
                    "tactile": {"voltage": "12-64V", "interface": "485, CAN FD, EtherCAT", "tactile": True},
                },
                "features": [
                    "11自由度(6个主动关节)",
                    "383g超轻重量",
                    "≥50N五指握力",
                    "≥15N单手捏力",
                    "≥20kg单手承载",
                    "1KHz通讯频率",
                    "0.1°控制精度",
                    "Python/C SDK, ROS支持",
                    "OTA在线升级",
                ],
            },
            "critical_point_hand": {
                "name": "临界点灵巧手 (OmniHand 3 Ultra-T)",
                "type": "dexterous_hand",
                "brand": "临界点 (AGILINK/智元)",
                "series": "OmniHand 3系列",
                "fingers": 5,
                "degrees_of_freedom": 25,
                "active_dof": 22,
                "passive_dof": 3,
                "weight_g": 500,
                "payload_kg": 5,
                "payload_to_weight_ratio": "10:1",
                "close_time_s": 0.3,
                "grip_force": {
                    "rated_output_n": 300,
                    "single_finger_kg": 5,
                },
                "structure": {
                    "material": "航空级镁钛合金骨架",
                    "drive_type": "绳驱+行星滚柱丝杠微型电缸",
                    "cable_quick_change_min": 10,
                    "lifetime_cycles": 1000000,
                },
                "sensors": {
                    "tactile": {
                        "full_hand_3d": True,
                        "tactile_points": 300,
                        "fingertip_visuotactile": True,
                    },
                    "palm_camera": True,
                    "wrist_range_mul": 2,
                },
                "control_interface": ["CAN FD", "EtherCAT", "RS485"],
                "mount_type": "quick_change",
                "product_line": {
                    "ultra_t": {
                        "name": "OmniHand 3 Ultra-T",
                        "dof": "22+3",
                        "features": ["绳驱", "极速开合0.3s", "10:1负载自重比", "掌内相机"],
                    },
                    "ultra_m": {
                        "name": "OmniHand 3 Ultra-M",
                        "dof": 20,
                        "features": ["全直驱", "高精度力矩反馈", ">300个三维触觉点"],
                    },
                    "lite": {
                        "name": "OmniHand 3 Lite",
                        "price": "千元级",
                        "features": ["普惠型小型灵巧手"],
                    },
                    "picker": {
                        "name": "OmniPicker 3",
                        "type": "工业夹爪",
                        "features": ["基于万台级出货经验升级"],
                    },
                },
                "features": [
                    "22+3个主动自由度",
                    "0.3秒极速开合",
                    "10:1负载自重比(5kg负载/500g自重)",
                    "航空级镁钛合金骨架",
                    "300N额定输出力(行星滚柱丝杠)",
                    "全手分布三维触觉感知",
                    "掌内相机(视觉盲区补齐)",
                    "腱绳快拆机制(<10分钟更换)",
                    "百万次寿命",
                    "腕部运动范围为行业平均2倍",
                ],
            },
        },

        # 相机支持
        "cameras": {
            "rgb_camera": {
                "name": "RGB相机",
                "type": "rgb",
                "resolution": "1920x1080",
                "mount_type": "wrist",
            },
            "rgbd_camera": {
                "name": "RGB-D相机",
                "type": "rgbd",
                "resolution": "1280x720",
                "depth_range": "0.1-10m",
                "mount_type": "wrist",
            },
        },

        # 部署要求
        "deployment_requirements": {
            "power_voltage": "24-48V DC",
            "power_current": "5A",
            "network": "Gigabit Ethernet / CAN FD",
            "environment_temp": "-10°C 至 55°C",
            "humidity": "10-90% (非凝结)",
            "protection": "IP54",
            "min_compute_requirements": {
                "cpu_cores": 2,
                "ram_gb": 4,
                "os": "Linux (Ubuntu 20.04+) 或 Windows 10/11",
                "note": "使用边缘模式时无需高性能PC，P7内置旭日5芯片可独立推理",
            },
            "edge_deployment_note": "内置10TOPS AI算力，支持独立完成目标检测、深度估算、操作策略推理",
        },
    },
}


# ============================================================
# 数据库管理类
# ============================================================

class RobotArmDB:
    """机械臂配置数据库管理类"""

    def __init__(self):
        self._configs = ARM_DATABASE.copy()
        self._custom_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "custom_arm_configs"
        )
        os.makedirs(self._custom_dir, exist_ok=True)
        self._load_custom_configs()

    def _load_custom_configs(self):
        """加载用户自定义的机械臂配置"""
        for fname in os.listdir(self._custom_dir):
            if fname.endswith('.json'):
                try:
                    with open(os.path.join(self._custom_dir, fname), 'r') as f:
                        config = json.load(f)
                        name = config.get("model_key", fname.replace('.json', ''))
                        self._configs[name] = config
                        print(f"[ARM_DB] 已加载自定义机械臂配置: {name}")
                except Exception as e:
                    print(f"[ARM_DB] ⚠️  加载自定义配置失败 {fname}: {e}")

    def list_available_arms(self) -> List[str]:
        """列出所有可用的机械臂型号"""
        return sorted(self._configs.keys())

    def get_config(self, arm_key: str) -> Optional[Dict[str, Any]]:
        """获取指定机械臂的完整配置"""
        return self._configs.get(arm_key)

    def get_summary(self, arm_key: str) -> Optional[Dict[str, Any]]:
        """获取机械臂的摘要信息（快速浏览用）"""
        cfg = self._configs.get(arm_key)
        if not cfg:
            return None
        return {
            "key": arm_key,
            "brand": cfg.get("brand", "Unknown"),
            "model": cfg.get("model", "Unknown"),
            "type": cfg.get("type", "Unknown"),
            "dof": cfg.get("degrees_of_freedom", 0),
            "payload_kg": cfg.get("payload_kg", 0),
            "reach_mm": cfg.get("reach_mm", 0),
            "protocol": cfg.get("communication", {}).get("protocol", "Unknown"),
            "sim_available": cfg.get("simulation", {}).get("pybullet_available", False),
        }

    def print_all_summaries(self):
        """打印所有可用机械臂的摘要"""
        print("\n" + "=" * 90)
        print(f"{'型号Key':<25} {'品牌':<18} {'型号':<22} {'类型':<15} {'轴数':>4} {'负载kg':>6} {'工作半径mm':>8}")
        print("-" * 90)
        for key in self.list_available_arms():
            s = self.get_summary(key)
            print(f"{key:<25} {s['brand']:<18} {s['model']:<22} {s['type']:<15} {s['dof']:>4} {s['payload_kg']:>6.1f} {s['reach_mm']:>8.0f}")
        print("=" * 90)
        print(f"共 {len(self._configs)} 种机械臂配置\n")

    def add_custom_config(self, arm_key: str, config: Dict[str, Any]) -> bool:
        """添加自定义机械臂配置"""
        try:
            self._configs[arm_key] = config
            config["model_key"] = arm_key
            save_path = os.path.join(self._custom_dir, f"{arm_key}.json")
            with open(save_path, 'w') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"[ARM_DB] ✅ 自定义配置已保存: {arm_key}")
            return True
        except Exception as e:
            print(f"[ARM_DB] ❌ 保存自定义配置失败: {e}")
            return False

    def detect_arm_type(self, joint_count: int = None,
                        protocol: str = None,
                        host: str = None) -> List[str]:
        """根据特征推测可能的机械臂类型"""
        candidates = []
        for key, cfg in self._configs.items():
            match_score = 0
            if joint_count and cfg.get("degrees_of_freedom") == joint_count:
                match_score += 3
            if protocol and protocol.lower() in cfg.get("communication", {}).get("protocol", "").lower():
                match_score += 2
            if host:
                default_host = cfg.get("communication", {}).get("default_host", "")
                if default_host.split('.')[:2] == host.split('.')[:2]:
                    match_score += 1
            if match_score > 0:
                candidates.append((key, match_score))
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in candidates]


# ============================================================
# 便捷函数
# ============================================================

def get_arm_config(arm_key: str) -> Optional[Dict[str, Any]]:
    """便捷函数：获取机械臂配置"""
    db = RobotArmDB()
    return db.get_config(arm_key)


def list_arms() -> List[str]:
    """便捷函数：列出所有可用机械臂"""
    db = RobotArmDB()
    return db.list_available_arms()


if __name__ == "__main__":
    db = RobotArmDB()
    db.print_all_summaries()

    # 测试获取配置
    test_key = "franka_panda"
    cfg = db.get_config(test_key)
    if cfg:
        print(f"\n{test_key} 通信协议: {cfg['communication']['protocol']}")
        print(f"{test_key} 自由度: {cfg['degrees_of_freedom']}")
        print(f"{test_key} 工作半径: {cfg['workspace']['radius_m']}m")
