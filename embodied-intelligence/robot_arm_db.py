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
