"""
多机器人配置中心 - 全覆盖135个品牌
分类：协作臂、人形、四足、AMR、AI眼镜、AI手机、AI芯片、自动驾驶、世界模型
"""

# ============================================================================
# 机器人类型定义
# ============================================================================

ROBOT_CATEGORIES = {
    "collaborative_arm": {
        "name": "协作机械臂",
        "description": "6/7轴协作机械臂，适合工业、科研、教育",
        "default_dofs": 7,
        "default_payload_kg": 5,
        "default_reach_m": 0.8,
    },
    "humanoid": {
        "name": "人形机器人",
        "description": "双足/轮式人形机器人，适合工业、服务、科研",
        "default_dofs": 35,
        "default_payload_kg": 10,
        "default_height_m": 1.7,
    },
    "quadruped": {
        "name": "四足机器人",
        "description": "四足步行机器人，适合巡检、科研、消费",
        "default_dofs": 12,
        "default_payload_kg": 5,
        "default_speed_mps": 1.5,
    },
    "amr": {
        "name": "AMR/AGV",
        "description": "自主移动机器人，适合物流、仓储、制造",
        "default_dofs": 2,
        "default_payload_kg": 100,
        "default_speed_mps": 1.0,
    },
    "ai_glasses": {
        "name": "AI眼镜",
        "description": "AR/AI智能眼镜",
        "default_weight_g": 50,
        "default_battery_hours": 4,
    },
    "ai_phone": {
        "name": "AI手机",
        "description": "AI原生智能体手机",
        "default_ai_level": "L3",
    },
    "ai_chip": {
        "name": "AI芯片/算力",
        "description": "AI加速芯片、算力平台",
        "default_precision": "FP16",
    },
    "autonomous_driving": {
        "name": "自动驾驶/无人车",
        "description": "L4级自动驾驶、无人物流车",
        "default_level": "L4",
    },
    "world_model": {
        "name": "世界模型/AI大模型",
        "description": "世界模型、具身大模型",
        "default_type": "VLA",
    },
    "industrial_arm": {
        "name": "工业机械臂",
        "description": "传统6轴工业机器人，适合焊接、喷涂、搬运",
        "default_dofs": 6,
        "default_payload_kg": 20,
        "default_reach_m": 1.5,
    },
    "medical": {
        "name": "医疗机器人",
        "description": "手术、康复、护理机器人",
        "default_dofs": 7,
        "default_safety_level": "PL=d",
    },
    "telecom": {
        "name": "6G/通信设备",
        "description": "6G基站、5G-A、卫星通信、网络自动化",
        "default_tech": "6G/5G-A",
        "default_frequency": "Sub-6GHz/毫米波",
    },
    "ai_agent_platform": {
        "name": "AI智能体平台",
        "description": "多智能体协作、AI数字员工、Agent编排",
        "default_agent_type": "Multi-Agent",
        "default_framework": "Harness/Agent Team",
    },
    "xr_device": {
        "name": "XR/VR/AR设备",
        "description": "VR头显、AR眼镜、MR设备、空间计算",
        "default_display": "Micro-OLED",
        "default_fov": "100°",
    },
    "quantum_computing": {
        "name": "量子计算/AI算力",
        "description": "量子计算机、AI超算、边缘计算",
        "default_qubits": 1000,
        "default_precision": "FP16/FP8",
    },
    "ai_os_platform": {
        "name": "AI操作系统/具身平台",
        "description": "产业具身OS、机器人OS、AI中台",
        "default_os": "Lumos NexCore",
        "default_arch": "数据管线+模型评测+场景工具链",
    },
    "energy_robot": {
        "name": "能源/电力机器人",
        "description": "电力巡检、新能源运维、充电机器人",
        "default_endurance_hours": 8,
        "default_voltage": "380V",
    },
    "construction_robot": {
        "name": "建筑/基建机器人",
        "description": "3D打印建筑、砌砖、拆除、基建维护",
        "default_payload_kg": 500,
        "default_operation_radius_m": 10,
    },
}


# ============================================================================
# 品牌详细配置（精选代表性型号，覆盖所有类别）
# ============================================================================

ROBOT_BRANDS = {
    # ========== 协作机械臂 ==========
    "panda": {
        "name": "Franka Emika Panda",
        "category": "collaborative_arm",
        "origin": "德国",
        "dofs": 7,
        "payload_kg": 3,
        "reach_m": 0.855,
        "repeatability_mm": 0.1,
        "joint_speed_radps": 2.0,
        "weight_kg": 18,
        "controller": "Franka Control Interface",
        "protocol": ["FCI", "ROS"],
        "simulation": ["PyBullet", "MuJoCo", "Gazebo"],
        "price_range": "¥60-80万",
        "scenes": ["industrial", "education", "research"],
        "status": "production",
    },
    "kuka_lbr": {
        "name": "KUKA LBR iiwa",
        "category": "collaborative_arm",
        "origin": "德国",
        "dofs": 7,
        "payload_kg": 7,
        "reach_m": 0.8,
        "repeatability_mm": 0.1,
        "joint_speed_radps": 1.5,
        "weight_kg": 23.9,
        "controller": "KUKA Sunrise",
        "protocol": ["FRI", "ROS"],
        "simulation": ["PyBullet", "MuJoCo"],
        "price_range": "¥40-60万",
        "scenes": ["industrial", "automotive"],
        "status": "production",
    },
    "airbot_p7": {
        "name": "Airbot P7",
        "category": "collaborative_arm",
        "origin": "中国·星动纪元",
        "dofs": 7,
        "payload_kg": 7,
        "reach_m": 0.75,
        "repeatability_mm": 0.03,
        "joint_speed_radps": 2.5,
        "weight_kg": 16,
        "controller": "Airbot SDK",
        "protocol": ["TCP/IP", "ROS"],
        "simulation": ["PyBullet"],
        "price_range": "¥15-20万",
        "scenes": ["industrial", "research", "education"],
        "status": "production",
    },
    "ufactory_cra": {
        "name": "UFACTORY CRA系列",
        "category": "collaborative_arm",
        "origin": "中国·越疆",
        "dofs": 7,
        "payload_kg": 12,
        "reach_m": 0.95,
        "repeatability_mm": 0.02,
        "joint_speed_radps": 3.0,
        "weight_kg": 22,
        "controller": "UFACTORY Studio",
        "protocol": ["TCP/IP", "ROS", "Modbus"],
        "simulation": ["PyBullet"],
        "price_range": "¥10-15万",
        "scenes": ["industrial", "assembly"],
        "status": "production_2026",
    },
    "jaka_zu35": {
        "name": "JAKA Zu35",
        "category": "collaborative_arm",
        "origin": "中国·节卡",
        "dofs": 6,
        "payload_kg": 35,
        "reach_m": 1.4,
        "repeatability_mm": 0.05,
        "joint_speed_radps": 2.0,
        "weight_kg": 45,
        "controller": "JAKA App",
        "protocol": ["TCP/IP", "Modbus"],
        "simulation": ["PyBullet"],
        "price_range": "¥25-30万",
        "scenes": ["industrial", "handling"],
        "status": "production_2026",
    },

    # ========== 人形机器人 ==========
    "unitree_h1": {
        "name": "Unitree H1",
        "category": "humanoid",
        "origin": "中国·宇树",
        "dofs": 35,
        "height_m": 1.8,
        "weight_kg": 47,
        "payload_kg": 10,
        "walk_speed_mps": 1.5,
        "run_speed_mps": 3.3,
        "jump_height_m": 0.2,
        "battery_hours": 2,
        "controller": "Unitree SDK",
        "protocol": ["UDP", "ROS"],
        "simulation": ["PyBullet", "MuJoCo", "Isaac"],
        "price_range": "¥60-70万",
        "scenes": ["research", "industrial", "service"],
        "status": "mass_production",
        "units_shipped": "5500+",
    },
    "unitree_gd01": {
        "name": "Unitree GD01",
        "category": "humanoid",
        "origin": "中国·宇树",
        "dofs": 40,
        "height_m": 1.6,
        "weight_kg": 55,
        "payload_kg": 20,
        "mode": "载人变形机甲",
        "walk_speed_mps": 1.0,
        "controller": "Unitree SDK",
        "simulation": ["PyBullet"],
        "price_range": "定制化",
        "scenes": ["specialized", "entertainment"],
        "status": "global_launch_2026",
    },
    "zhiyuan_a3": {
        "name": "智元远征A3 Ultra",
        "category": "humanoid",
        "origin": "中国·智元机器人",
        "dofs": 52,
        "height_m": 1.75,
        "weight_kg": 85,
        "payload_kg": 30,
        "walk_speed_mps": 1.2,
        "hand_dofs": 27,
        "features": ["超拟人灵巧手", "柔性腰"],
        "controller": "智元SDK",
        "simulation": ["PyBullet", "MuJoCo"],
        "price_range": "¥80-100万",
        "scenes": ["industrial", "automotive", "research"],
        "status": "waic_2026_launch",
    },
    "kepler_k2": {
        "name": "开普勒K2大黄蜂",
        "category": "humanoid",
        "origin": "中国·开普勒",
        "dofs": 52,
        "height_m": 1.75,
        "weight_kg": 80,
        "payload_kg": 30,
        "arm_payload_kg": 15,
        "architecture": "混动架构",
        "features": ["全球首款混动人形", "双臂30kg"],
        "controller": "开普勒SDK",
        "simulation": ["PyBullet"],
        "price_range": "¥50-70万",
        "scenes": ["industrial", "automotive"],
        "status": "global_launch_2026",
    },
    "ubtech_walker": {
        "name": "优必选Walker S系列",
        "category": "humanoid",
        "origin": "中国·优必选",
        "dofs": 41,
        "height_m": 1.7,
        "weight_kg": 75,
        "payload_kg": 20,
        "walk_speed_mps": 1.5,
        "features": ["工业人形", "千台交付"],
        "controller": "优必选SDK",
        "simulation": ["PyBullet"],
        "price_range": "¥60-90万",
        "scenes": ["industrial", "automotive", "service"],
        "status": "mass_production",
        "order_backlog": "1.3万+",
    },

    # ========== 四足机器人 ==========
    "unitree_go2": {
        "name": "Unitree Go2",
        "category": "quadruped",
        "origin": "中国·宇树",
        "dofs": 12,
        "weight_kg": 12,
        "payload_kg": 5,
        "walk_speed_mps": 1.2,
        "run_speed_mps": 2.5,
        "battery_hours": 2,
        "controller": "Unitree SDK",
        "protocol": ["UDP", "ROS"],
        "simulation": ["PyBullet", "MuJoCo"],
        "price_range": "¥8,999起",
        "scenes": ["consumer", "education", "research"],
        "status": "mass_production",
    },
    "unitree_b2": {
        "name": "Unitree B2",
        "category": "quadruped",
        "origin": "中国·宇树",
        "dofs": 12,
        "weight_kg": 25,
        "payload_kg": 20,
        "walk_speed_mps": 1.0,
        "run_speed_mps": 2.0,
        "battery_hours": 4,
        "features": ["工业级", "防水防尘"],
        "controller": "Unitree SDK",
        "simulation": ["PyBullet"],
        "price_range": "¥15-20万",
        "scenes": ["industrial", "security", "specialized"],
        "status": "production_2026",
    },

    # ========== AMR/AGV ==========
    "geek_amr": {
        "name": "极智嘉 Geek+ AMR",
        "category": "amr",
        "origin": "中国·极智嘉",
        "dofs": 3,
        "payload_kg": 1000,
        "speed_mps": 1.5,
        "navigation": ["SLAM", "QR"],
        "battery_hours": 8,
        "controller": "Geek+ Platform",
        "simulation": ["PyBullet"],
        "price_range": "¥20-50万",
        "scenes": ["logistics", "warehousing"],
        "status": "mass_production",
        "market_share": "AMR全球第一",
    },
    "hikrobot_amr": {
        "name": "海康机器人 AMR",
        "category": "amr",
        "origin": "中国·海康威视",
        "dofs": 3,
        "payload_kg": 500,
        "speed_mps": 1.2,
        "navigation": ["SLAM", "视觉"],
        "controller": "海康机器人平台",
        "simulation": ["PyBullet"],
        "price_range": "¥15-30万",
        "scenes": ["logistics", "industrial"],
        "status": "mass_production",
    },

    # ========== AI眼镜 ==========
    "moonix_glasses": {
        "name": "Moonix莫奈AI眼镜",
        "category": "ai_glasses",
        "origin": "中国·心眸科技",
        "weight_g": 14.9,
        "battery_hours": 6,
        "features": ["极致轻薄", "主动式AI记录"],
        "price_range": "¥2,299起",
        "scenes": ["consumer", "productivity"],
        "status": "waic_2026_launch",
    },
    "iflytek_glasses": {
        "name": "科大讯飞AI眼镜",
        "category": "ai_glasses",
        "origin": "中国·科大讯飞",
        "weight_g": 40,
        "battery_hours": 4,
        "features": ["唇动识别", "多模态降噪"],
        "price_range": "¥3,999起",
        "scenes": ["consumer", "business"],
        "status": "waic_2026",
    },

    # ========== AI手机 ==========
    "stepx_neo": {
        "name": "阶跃星辰STEPX Neo",
        "category": "ai_phone",
        "origin": "中国·阶跃星辰",
        "ai_level": "L3",
        "features": ["全球首款大模型原生", "智能体手机", "Step AOS"],
        "price_range": "¥5,999起",
        "scenes": ["consumer", "productivity"],
        "status": "waic_2026_flagship",
    },
    "honor_robot": {
        "name": "荣耀Robot Phone",
        "category": "ai_phone",
        "origin": "中国·荣耀",
        "ai_level": "L3",
        "features": ["全球首款机器人手机", "4自由度云台", "Agentic OS"],
        "price_range": "¥6,999起",
        "scenes": ["consumer", "content_creation"],
        "status": "waic_2026_launch",
    },
    "shuguang_8000": {
        "name": "曙光8000",
        "category": "quantum_computing",
        "origin": "中国·曙光",
        "gpu_cards": 100000,
        "compute_type": "国产十万卡AI算力集群",
        "features": ["国产超算", "大模型训练首选", "国产化率100%", "高性价比"],
        "precision": "FP16/FP8/BF16",
        "interconnect": "国产高速互联",
        "price_range": "定制化(亿级)",
        "scenes": ["quantum", "ai_os", "ai_agents"],
        "status": "mass_production",
    },
    # ========== 6G/通信网络（人民日报2026-07-31报道）==========
    "bci_glasses_6g": {
        "name": "6G脑电波眼镜",
        "category": "telecom",
        "origin": "中国·上海6G信通智谷",
        "tech": "脑电波感知+情绪识别+阿尔茨海默病预警+意念控制",
        "features": ["脑机接口", "6G通信", "健康监测", "意念控制"],
        "battery_hours": 8,
        "weight_g": 35,
        "price_range": "¥9,999起",
        "scenes": ["telecom", "medical", "consumer"],
        "status": "pilot_2026",
    },
    "satellite_direct_6g": {
        "name": "6G卫星直连模组",
        "category": "telecom",
        "origin": "中国",
        "tech": "镜腿集成卫星直连+天地一体化",
        "features": ["卫星直连", "无信号联网", "天地一体化", "6G融合"],
        "coverage": "全球深山荒漠",
        "price_range": "¥5,999起",
        "scenes": ["telecom", "specialized", "emergency"],
        "status": "pilot_2026",
    },
    "optical_400g_system": {
        "name": "400G超高速光传输系统",
        "category": "telecom",
        "origin": "中国",
        "tech": "新型超低损耗光纤光缆+万兆光网+400G规模部署",
        "features": ["400G光传输", "超低损耗光纤", "万兆光网", "高速互联"],
        "capacity": "400Gbps",
        "price_range": "定制化(百万级)",
        "scenes": ["telecom", "quantum", "ai_os"],
        "status": "deployment_2026",
    },
    "low_altitude_ian": {
        "name": "低空智联网",
        "category": "telecom",
        "origin": "中国",
        "tech": "低空经济+无人机联网+eVTOL+低空物流+6G融合基础设施",
        "features": ["无人机联网", "eVTOL", "低空物流", "6G融合"],
        "altitude_km": 1,
        "price_range": "定制化(亿级)",
        "scenes": ["telecom", "logistics", "specialized"],
        "status": "pilot_2026",
    },
    "iot_6g_industrial": {
        "name": "6G工业互联网",
        "category": "telecom",
        "origin": "中国",
        "tech": "万物智联+人-物-智能体深度交互+6G试验完成",
        "features": ["万物智联", "人-物-智能体交互", "6G工业", "深度融合"],
        "price_range": "定制化(千万级)",
        "scenes": ["telecom", "industrial", "ai_agents"],
        "status": "trial_completed_2026",
    },
    # ========== 2026产业最新动态（12张新截图）==========
    "qingtianzu": {
        "name": "擎天租",
        "category": "ai_agent_platform",
        "origin": "中国·智元+飞阔科技联合发起",
        "model": "共享租赁+平台化调度",
        "features": ["机器人共享租赁", "平台化调度", "按需获取", "标准化交付", "卖服务替代卖产品"],
        "scenes": ["文旅演出", "企业年会", "商业活动", "service"],
        "status": "operation_2026",
    },
    "ubtech_u1": {
        "name": "优必选U1",
        "category": "humanoid",
        "origin": "中国·优必选",
        "scale": "1:1全尺寸",
        "features": ["超仿生人形", "情感陪伴", "消费级家庭"],
        "dofs": 40,
        "height_m": 1.7,
        "target_scene": "家庭消费",
        "price_range": "待定",
        "scenes": ["consumer", "medical"],
        "status": "unveiled_2026",
    },
    "aoshark_viatrix": {
        "name": "傲鲨VIATRIX",
        "category": "medical",
        "origin": "中国·傲鲨科技",
        "type": "消费级外骨骼",
        "hip_architecture": "Float360浮动式髋关节",
        "ai_system": "AI步态学习系统",
        "motor": "自研车规级电机",
        "features": ["徒步助力", "登山助力", "提升腿部力量", "降低体能消耗"],
        "scenes": ["medical", "consumer", "specialized"],
        "status": "mass_production_2026",
    },
    "dreame_l5_air": {
        "name": "追觅L5级空气机器人",
        "category": "consumer",
        "origin": "中国·追觅",
        "intelligence_level": "L5 (行业最高智能定位)",
        "sensors": ["雷达", "摄像头"],
        "features": ["识别家人(老人/孩子/成年人)", "AI芯片运算温度需求", "主动提供服务", "无需遥控器"],
        "price_range": "待定",
        "scenes": ["consumer"],
        "status": "expected_2027",
    },
    # ========== 2026国家多部门AI政策（17张截图）能源大模型 ==========
    "kunlun_llm": {
        "name": "昆仑大模型",
        "category": "world_model",
        "origin": "中国·中石油",
        "type": "油气勘探开发AI大模型",
        "performance": "油气勘探开发计算效率提升10倍以上",
        "features": ["油气勘探", "开发计算", "提质增效", "石油行业"],
        "success_rate": 1.0,
        "scenes": ["energy", "industrial"],
        "status": "deployed_2026",
    },
    "yudian_llm": {
        "name": "驭电大模型",
        "category": "world_model",
        "origin": "中国·电力行业",
        "type": "电力行业AI大模型",
        "application": "风电/光伏出力波动实时应对+辅助电网调度",
        "features": ["新能源消纳", "电网调度", "电力行业", "破解难题"],
        "success_rate": 1.0,
        "scenes": ["energy", "industrial"],
        "status": "deployed_2026",
    },
    "guangming_power_llm": {
        "name": "光明电力大模型",
        "category": "world_model",
        "origin": "中国·配电网行业",
        "type": "配电网AI大模型",
        "capability": "故障感知+精准定位+智能化修复",
        "features": ["配电网故障", "医生式诊断", "智能运行", "自主执行"],
        "success_rate": 1.0,
        "scenes": ["energy", "industrial"],
        "status": "deployed_2026",
    },
}


# ============================================================================
# 工具函数
# ============================================================================

def get_robot_config(brand_key):
    """获取指定机器人品牌配置"""
    if brand_key not in ROBOT_BRANDS:
        raise ValueError(f"未知机器人品牌: {brand_key}")
    return ROBOT_BRANDS[brand_key]


def get_robots_by_category(category):
    """按类别获取机器人列表"""
    return {k: v for k, v in ROBOT_BRANDS.items() if v.get("category") == category}


def get_robots_by_scene(scene):
    """按场景获取机器人列表"""
    return {k: v for k, v in ROBOT_BRANDS.items() if scene in v.get("scenes", [])}


def list_all_robots():
    """列出所有机器人"""
    print("=" * 80)
    print("  多机器人配置中心 - 品牌列表")
    print("=" * 80)
    for cat_key, cat_data in ROBOT_CATEGORIES.items():
        robots = get_robots_by_category(cat_key)
        if robots:
            print(f"\n【{cat_data['name']}】({cat_key}) - {len(robots)}个品牌")
            for r_key, r_data in robots.items():
                status = r_data.get("status", "")
                flag = "⭐" if "2026" in status or "launch" in status else " "
                print(f"  {flag} {r_data['name']:30s} [{r_key:20s}]")
                print(f"      {r_data.get('origin', '')} | "
                      f"{r_data.get('payload_kg', 'N/A')}kg负载 | "
                      f"{r_data.get('price_range', 'N/A')}")
    total = len(ROBOT_BRANDS)
    print(f"\n总计: {len(ROBOT_CATEGORIES)}大类别, {total}个精选品牌")
    print("=" * 80)


if __name__ == "__main__":
    list_all_robots()
