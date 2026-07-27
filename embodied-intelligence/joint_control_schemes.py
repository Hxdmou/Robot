"""
关节驱控方案数据库
支持多种关节驱动控制方案的配置与对比
包含：
  - 传统硅基多芯片方案（MCU + 分立硅MOS）
  - CT-2001B ASIC + CT-1902 GaN 双芯方案（中科无线半导体）
"""

from typing import Dict, Any, List, Optional


# ============================================================
# 关节驱控方案数据库
# ============================================================

JOINT_CONTROL_SCHEMES = {
    # ========================================================
    # 传统硅基多芯片方案
    # ========================================================
    "traditional_silicon": {
        "name": "传统硅基多芯片方案",
        "architecture": "MCU + 分立硅MOS + 独立运算单元",
        "chips": ["通用MCU", "独立运算单元", "分立式功率管"],
        "component_count": 250,

        # 性能参数
        "performance": {
            "control_delay_ns": 2.8,          # 三环控制延时
            "current_loop_khz": 50,            # 电流环频率
            "pid_delay_ns": 100,               # PID运算延时（软件）
            "peak_torque_improvement": 0,      # 同体积峰值扭矩提升（基准）
            "continuous_temp_rise_c": 65,      # 满载持续温升
            "board_area_reduction": 0,         # 驱控板面积缩减（基准100%）
        },

        # 芯片参数
        "chips_detail": {
            "mcu": {"type": "通用MCU", "cores": 1, "freq_mhz": 100},
            "mos": {"type": "硅基MOSFET", "count": 6, "package": "分立"},
        },

        # 集成特性
        "features": {
            "hardware_foc": False,
            "auto_tuning": False,
            "ethercat": False,
            "canfd": False,
            "gan_technology": False,
            "builtin_protection": False,
        },

        # 成本
        "cost": {
            "bom_cost_per_joint_rmb": 3000,
            "total_joint_cost_rmb": 70000,
            "rnd_cycle_months": 6,
        },

        # 痛点
        "pain_points": [
            "体积大",
            "发热高",
            "调参复杂",
            "量产成本高",
            "扭矩与小型化无法兼顾",
            "依赖海外芯片供货",
        ],
    },

    # ========================================================
    # CT-2001B ASIC + CT-1902 GaN 双芯方案
    # ========================================================
    "ct2001b_ct1902_gan": {
        "name": "CT-2001B ASIC + CT-1902 GaN 双芯方案",
        "brand": "中科无线半导体",
        "architecture": "CT-2001B 运动控制ASIC + CT-1902 集成GaN驱动",
        "chips": ["CT-2001B ASIC", "CT-1902 GaN"],
        "component_count": 150,  # 缩减40%（从250→150）

        # 芯片详细参数
        "chips_detail": {
            "ct2001b": {
                "full_name": "CT-2001B 专用运动控制ASIC",
                "type": "运动控制ASIC",
                "cores": 2,
                "freq_mhz": 540,
                "architecture": "超标量ASIC + IDPU硬件加速单元",
                "size_mm": "10x10",
                "key_features": [
                    "双核540MHz超标量ASIC架构",
                    "专用IDPU硬件加速单元",
                    "硬件PID运算延时仅0.2ns",
                    "电流环最高450kHz",
                    "内置端侧FOC及原生运动模型算法",
                    "上电自动识别电机极对数",
                    "自动测算电阻电感",
                    "自动整定三环PID",
                    "支持T/S型平滑轨迹规划",
                    "集成ADRC自抗扰算法",
                    "自动补偿齿槽转矩",
                    "自动补偿编码器误差",
                    "原生兼容SPI磁编码器",
                    "原生兼容旋变解码",
                    "内置EtherCAT工业总线",
                    "内置CAN FD工业总线",
                    "支持多关节毫秒级同步",
                    "集成电源管理",
                    "硬件故障诊断",
                ],
            },
            "ct1902": {
                "full_name": "CT-1902 集成GaN氮化镓驱动芯片",
                "type": "GaN HEMT功率驱动",
                "technology": "第三代半导体（氮化镓GaN）",
                "voltage_platform": ["48V", "80V"],
                "integrated_channels": 2,  # 两路GaN HEMT + 栅极驱动
                "size_mm": "5.8x7.2",
                "power_output_w": 1000,
                "key_features": [
                    "专为48V/80V机器人主流供电平台打造",
                    "单芯片集成两路GaN HEMT功率器件",
                    "集成栅极驱动通道",
                    "氮化镓电流密度为硅基5-10倍",
                    "功率电路体积仅传统方案1/3",
                    "同等关节外壳可搭载更大电机与减速器",
                    "同体积峰值扭矩提升35%~45%",
                    "搭载专利栅极米勒钳位技术",
                    "抑制开关尖峰",
                    "双重损耗大幅降低",
                    "关节满载长期工作温升≤35°C",
                    "无需强制风冷",
                    "仅小型散热片即可稳定运行",
                    "支持全密封防尘防水结构",
                    "微秒级硬件安全防护",
                    "集成过流保护",
                    "集成过压保护",
                    "集成过温保护",
                    "集成直通保护",
                    "集成负载异常保护",
                    "故障信号直连CT-2001B硬件中断",
                    "堵转/碰撞瞬间切断功率",
                    "杜绝电机烧毁",
                    "集成完整三相逆变拓扑",
                ],
            },
        },

        # 性能参数
        "performance": {
            "control_delay_ns": 0.2,           # 三环控制延时（硬件加速）
            "current_loop_khz": 450,            # 电流环频率
            "pid_delay_ns": 0.2,                # PID运算延时（硬件）
            "peak_torque_improvement_min": 35,  # 同体积峰值扭矩提升（最低）
            "peak_torque_improvement_max": 45,  # 同体积峰值扭矩提升（最高）
            "continuous_temp_rise_c": 35,       # 满载持续温升
            "board_area_reduction": 65,         # 驱控板面积缩减（%）
            "power_density_improvement": 300,   # 功率密度提升（%）
        },

        # 集成特性
        "features": {
            "hardware_foc": True,
            "auto_tuning": True,
            "ethercat": True,
            "canfd": True,
            "gan_technology": True,
            "builtin_protection": True,
            "self_collision_guard": True,
            "adrc_self_disturbance": True,
        },

        # 应用场景实测数据
        "scenario_results": {
            "humanoid_joint": {
                "name": "人形机器人四肢关节",
                "outer_diameter_reduction": 30,     # 关节外径缩小
                "torque_rating_increase": 35,       # 额定持续扭矩提升
                "peak_torque_nm": 120,              # 单关节峰值扭矩
                "weight_reduction": 8,               # 整机自重下降
            },
            "collaborative_arm": {
                "name": "轻量化重载协作机械臂",
                "driver_board_diameter_mm": 36,     # 驱控板直径
                "continuous_torque_nm": 60,         # 持续输出扭矩
                "external_driver_cabinet": False,    # 无需外置独立驱动柜
            },
            "quadruped_leg": {
                "name": "四足机器人腿部执行器",
                "high_dynamic_response": True,
                "large_current_output": True,
                "high_speed_stability": True,
            },
        },

        # 成本
        "cost": {
            "bom_reduction_percent": 30,         # 硬件BOM降本
            "component_reduction_percent": 40,   # 核心外围器件缩减
            "bom_cost_per_joint_rmb": 2100,     # 关节驱动硬件成本
            "total_joint_cost_rmb": 42000,       # 单台机器人关节总成本
            "total_cost_reduction_percent": 40,   # 整体执行器成本下降
            "rnd_cycle_reduction_months": 3,      # 研发周期缩短
        },

        # 全栈国产自研
        "domestic": {
            "fully_domestic": True,
            "chip_domestic": True,
            "algorithm_domestic": True,
            "power_device_domestic": True,
            "protection_architecture_domestic": True,
            "supply_chain": "国产成熟半导体供应链",
            "support_customization": True,
            "customization_aspects": [
                "电机参数优化",
                "关节结构适配",
                "运动控制需求针对性优化",
                "算法与驱动参数定制",
            ],
            "supported_products": [
                "灵巧手",
                "重载关节",
                "四足机器人",
                "特种执行器",
                "协作机械臂",
                "人形机器人",
            ],
        },

        # 核心优势
        "core_advantages": [
            "纳秒级响应",
            "超高功率密度",
            "低温升",
            "极简集成",
            "全栈国产化",
        ],

        # 解决的核心诉求
        "solved_demands": [
            "整机厂商降本",
            "小型化",
            "高动态作业",
        ],
    },
}


# ============================================================
# 关节驱控方案管理器
# ============================================================

class JointControlSchemeManager:
    """关节驱控方案管理器"""

    def __init__(self):
        self._schemes = JOINT_CONTROL_SCHEMES.copy()

    def list_schemes(self) -> List[str]:
        """列出所有可用方案"""
        return list(self._schemes.keys())

    def get_scheme(self, key: str) -> Optional[Dict[str, Any]]:
        """获取指定方案"""
        return self._schemes.get(key)

    def compare_schemes(self, keys: List[str] = None) -> Dict[str, Any]:
        """对比多个方案"""
        if not keys:
            keys = self.list_schemes()

        comparison = {}
        for key in keys:
            scheme = self._schemes.get(key)
            if scheme:
                perf = scheme.get("performance", {})
                cost = scheme.get("cost", {})
                comparison[key] = {
                    "name": scheme.get("name", key),
                    "architecture": scheme.get("architecture", ""),
                    "component_count": scheme.get("component_count", 0),
                    "control_delay_ns": perf.get("control_delay_ns", 0),
                    "current_loop_khz": perf.get("current_loop_khz", 0),
                    "temp_rise_c": perf.get("continuous_temp_rise_c", 0),
                    "board_area_reduction": perf.get("board_area_reduction", 0),
                    "total_joint_cost_rmb": cost.get("total_joint_cost_rmb", 0),
                    "gan": scheme.get("features", {}).get("gan_technology", False),
                    "domestic": scheme.get("domestic", {}).get("fully_domestic", False),
                }
        return comparison

    def print_comparison(self, keys: List[str] = None):
        """打印方案对比表"""
        comp = self.compare_schemes(keys)
        print("\n" + "=" * 110)
        print(f"{'方案':<35} {'架构':<30} {'器件数':>6} {'延时ns':>8} {'电流环kHz':>10} {'温升°C':>7} {'面积缩%':>8} {'关节成本万':>10} {'GaN':>4} {'国产':>4}")
        print("-" * 110)
        for key, data in comp.items():
            gan = "✅" if data["gan"] else "❌"
            dom = "✅" if data["domestic"] else "❌"
            cost_wan = data["total_joint_cost_rmb"] / 10000
            print(f"{data['name']:<35} {data['architecture']:<30} {data['component_count']:>6} {data['control_delay_ns']:>8.1f} {data['current_loop_khz']:>10} {data['temp_rise_c']:>7.0f} {data['board_area_reduction']:>8} {cost_wan:>10.1f} {gan:>4} {dom:>4}")
        print("=" * 110)


def generate_joint_config(arm_key: str, scheme_key: str, joint_count: int) -> Dict[str, Any]:
    """
    根据机械臂型号和驱控方案生成关节配置
    """
    scheme = JOINT_CONTROL_SCHEMES.get(scheme_key)
    if not scheme:
        return {}

    perf = scheme.get("performance", {})
    cost = scheme.get("cost", {})

    return {
        "control_scheme": scheme_key,
        "scheme_name": scheme.get("name", ""),
        "joint_count": joint_count,
        "per_joint": {
            "board_diameter_mm": perf.get("driver_board_diameter_mm", None) or 36 if scheme_key == "ct2001b_ct1902_gan" else 60,
            "continuous_torque_nm": perf.get("continuous_torque_nm", 60) if scheme_key == "ct2001b_ct1902_gan" else 40,
            "temp_rise_c": perf.get("continuous_temp_rise_c", 35),
        },
        "total": {
            "estimated_cost_rmb": cost.get("total_joint_cost_rmb", 70000) * (joint_count / 6),
            "estimated_weight_reduction_percent": perf.get("weight_reduction", 0) if scheme_key == "ct2001b_ct1902_gan" else 0,
        },
        "bus_interfaces": [
            "EtherCAT" if scheme.get("features", {}).get("ethercat") else None,
            "CAN FD" if scheme.get("features", {}).get("canfd") else None,
        ],
        "features": scheme.get("features", {}),
    }


if __name__ == "__main__":
    manager = JointControlSchemeManager()
    print("关节驱控方案列表:", manager.list_schemes())
    manager.print_comparison()
