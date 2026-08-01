"""
AI场景全覆盖配置中心
覆盖15大应用场景、63个子场景
"""

# ============================================================================
# 场景定义
# ============================================================================

SCENES = {
    # ========== 1. 工业制造 ==========
    "industrial": {
        "name": "工业制造",
        "description": "面向制造业的全流程自动化",
        "sub_scenes": {
            "assembly": {
                "name": "组装装配",
                "description": "汽车、电子、家电等产品组装",
                "robots": ["协作臂", "人形机器人", "SCARA"],
                "difficulty": 5,
                "reward_scale": 1.0,
            },
            "welding": {
                "name": "焊接切割",
                "description": "电弧焊、激光焊、等离子切割",
                "robots": ["六轴机械臂", "协作臂"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "painting": {
                "name": "喷涂涂装",
                "description": "汽车喷涂、表面处理",
                "robots": ["六轴机械臂"],
                "difficulty": 3,
                "reward_scale": 0.8,
            },
            "handling": {
                "name": "搬运码垛",
                "description": "物料搬运、箱子码垛",
                "robots": ["码垛机器人", "AGV/AMR", "协作臂"],
                "difficulty": 2,
                "reward_scale": 0.6,
            },
            "inspection": {
                "name": "质量检测",
                "description": "视觉检测、尺寸测量、缺陷检测",
                "robots": ["协作臂", "SCARA", "AGV/AMR"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "cnc": {
                "name": "机床上下料",
                "description": "CNC机床、注塑机上下料",
                "robots": ["六轴机械臂", "桁架机器人"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
        },
    },

    # ========== 2. 物流仓储 ==========
    "logistics": {
        "name": "物流仓储",
        "description": "仓储自动化与物流运输",
        "sub_scenes": {
            "picking": {
                "name": "拣选分拣",
                "description": "电商仓储、快递分拣",
                "robots": ["AGV/AMR", "Delta机器人", "协作臂"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "storage": {
                "name": "存储管理",
                "description": "立体仓库、货架存取",
                "robots": ["堆垛机", "AGV/AMR", "四足机器人"],
                "difficulty": 3,
                "reward_scale": 0.8,
            },
            "loading": {
                "name": "装车卸车",
                "description": "卡车装卸、集装箱作业",
                "robots": ["AGV/AMR", "机械臂", "人形机器人"],
                "difficulty": 5,
                "reward_scale": 1.3,
            },
            "delivery": {
                "name": "末端配送",
                "description": "园区配送、楼宇配送",
                "robots": ["配送机器人", "无人机", "AGV/AMR"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "postal_express": {
                "name": "邮政快递",
                "description": "无人机运邮、山区/海岛/高原特殊场景、智慧邮政建设",
                "robots": ["无人机", "配送机器人", "AGV/AMR", "智能终端"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "port_intelligence": {
                "name": "口岸智能化",
                "description": "海关口岸外贸智慧化、智能查验、智能通关",
                "robots": ["巡检机器人", "四足机器人", "无人机", "AI视觉系统"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
            "smart_parking": {
                "name": "智慧停车",
                "description": "枢纽场站智慧停车引导、智慧寻车、智能泊车系统",
                "robots": ["智能泊车机器人", "AGV", "AI视觉系统", "传感器"],
                "difficulty": 3,
                "reward_scale": 0.9,
            },
        },
    },

    # ========== 3. 医疗健康 ==========
    "medical": {
        "name": "医疗健康",
        "description": "医疗手术、康复、护理",
        "sub_scenes": {
            "surgery": {
                "name": "手术辅助",
                "description": "骨科、神经外科、腹腔手术",
                "robots": ["手术机器人", "协作臂"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "rehab": {
                "name": "康复训练",
                "description": "上肢/下肢康复、运动恢复",
                "robots": ["康复机器人", "外骨骼"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "nursing": {
                "name": "护理陪伴",
                "description": "老年护理、患者陪护",
                "robots": ["人形机器人", "服务机器人"],
                "difficulty": 3,
                "reward_scale": 0.8,
            },
            "diagnosis": {
                "name": "诊断辅助",
                "description": "影像诊断、病理分析",
                "robots": ["协作臂", "AI视觉系统"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
        },
    },

    # ========== 4. 农业食品 ==========
    "agriculture": {
        "name": "农业食品",
        "description": "智慧农业、食品加工",
        "sub_scenes": {
            "picking_agri": {
                "name": "采摘收获",
                "description": "水果、蔬菜采摘",
                "robots": ["采摘机器人", "六轴机械臂", "AMR"],
                "difficulty": 5,
                "reward_scale": 1.3,
            },
            "planting": {
                "name": "种植管理",
                "description": "播种、育苗、灌溉",
                "robots": ["农业机器人", "无人机", "四足机器人"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
            "food_processing": {
                "name": "食品加工",
                "description": "肉类加工、烘焙、包装",
                "robots": ["协作臂", "Delta机器人", "SCARA"],
                "difficulty": 3,
                "reward_scale": 0.8,
            },
            "livestock": {
                "name": "畜牧养殖",
                "description": "奶牛挤奶、饲料投放",
                "robots": ["农业机器人", "四足机器人", "AMR"],
                "difficulty": 2,
                "reward_scale": 0.6,
            },
        },
    },

    # ========== 5. 商业服务 ==========
    "service": {
        "name": "商业服务",
        "description": "零售、餐饮、酒店服务",
        "sub_scenes": {
            "retail": {
                "name": "零售导购",
                "description": "商场导购、商品推荐",
                "robots": ["服务机器人", "人形机器人"],
                "difficulty": 2,
                "reward_scale": 0.5,
            },
            "catering": {
                "name": "餐饮服务",
                "description": "送餐、调酒、咖啡制作",
                "robots": ["送餐机器人", "协作臂", "人形机器人"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
            "hotel": {
                "name": "酒店服务",
                "description": "前台接待、行李搬运、客房服务",
                "robots": ["服务机器人", "人形机器人", "AMR"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
            "cleaning": {
                "name": "清洁保洁",
                "description": "地面清洁、玻璃清洁",
                "robots": ["清洁机器人", "人形机器人"],
                "difficulty": 2,
                "reward_scale": 0.5,
            },
        },
    },

    # ========== 6. 科研教育 ==========
    "education": {
        "name": "科研教育",
        "description": "高校科研、职业教育",
        "sub_scenes": {
            "research": {
                "name": "科学研究",
                "description": "机器人学、AI算法研究",
                "robots": ["协作臂", "人形机器人", "四足机器人"],
                "difficulty": 5,
                "reward_scale": 1.0,
            },
            "teaching": {
                "name": "教学演示",
                "description": "机器人教学、STEM教育",
                "robots": ["教育机器人", "协作臂", "人形机器人"],
                "difficulty": 2,
                "reward_scale": 0.5,
            },
            "training": {
                "name": "技能培训",
                "description": "工业机器人操作培训",
                "robots": ["六轴机械臂", "协作臂"],
                "difficulty": 3,
                "reward_scale": 0.6,
            },
            "competition": {
                "name": "竞赛竞技",
                "description": "RoboCup、世界机器人大赛",
                "robots": ["人形机器人", "四足机器人", "协作臂"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
        },
    },

    # ========== 7. 家庭消费 ==========
    "consumer": {
        "name": "家庭消费",
        "description": "消费级机器人与AI产品",
        "sub_scenes": {
            "home_cleaning": {
                "name": "家庭清洁",
                "description": "扫地、拖地、擦窗",
                "robots": ["扫地机器人", "人形机器人"],
                "difficulty": 1,
                "reward_scale": 0.3,
            },
            "companion": {
                "name": "家庭陪伴",
                "description": "儿童陪伴、老人陪护",
                "robots": ["人形机器人", "陪伴机器人"],
                "difficulty": 2,
                "reward_scale": 0.4,
            },
            "ai_glasses": {
                "name": "AI眼镜",
                "description": "AR眼镜、智能眼镜",
                "robots": ["AI眼镜"],
                "difficulty": 2,
                "reward_scale": 0.5,
            },
            "ai_phone": {
                "name": "AI手机",
                "description": "AI终端、智能终端",
                "robots": ["AI手机"],
                "difficulty": 1,
                "reward_scale": 0.3,
            },
        },
    },

    # ========== 8. 特殊行业 ==========
    "specialized": {
        "name": "特殊行业",
        "description": "安防、军事、太空、水下",
        "sub_scenes": {
            "security": {
                "name": "安防巡逻",
                "description": "园区安防、边境巡逻",
                "robots": ["安防机器人", "四足机器人", "无人机"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "military": {
                "name": "军事应用",
                "description": "排爆、侦察、后勤",
                "robots": ["军用机器人", "四足机器人", "人形机器人"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "space": {
                "name": "太空探索",
                "description": "空间站维护、月球/火星探测",
                "robots": ["航天机器人", "人形机器人", "机械臂"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "underwater": {
                "name": "水下作业",
                "description": "水下焊接、管道检测、打捞",
                "robots": ["水下机器人", "机械臂"],
                "difficulty": 5,
                "reward_scale": 1.3,
            },
            "mining": {
                "name": "矿山采掘",
                "description": "井下作业、矿石搬运",
                "robots": ["矿山机器人", "AMR", "机械臂"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
        },
    },

    # ========== 9. 6G/通信网络 ==========
    "telecom": {
        "name": "6G/通信网络",
        "description": "下一代通信网络与元宇宙基础设施",
        "sub_scenes": {
            "6g_ran": {
                "name": "6G无线接入",
                "description": "太赫兹通信、智能超表面、通感一体",
                "robots": ["6G基站", "无人机", "AI芯片"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "5g_advanced": {
                "name": "5G-A演进",
                "description": "5.5G、万兆下行、无源物联",
                "robots": ["5G-A基站", "工业网关"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "satellite": {
                "name": "卫星通信",
                "description": "低轨卫星、天地一体化、星链、卫星直连",
                "robots": ["卫星", "地面站", "天线", "卫星直连模组"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "network_automation": {
                "name": "网络自动化",
                "description": "自智网络、零接触运维、AI运维",
                "robots": ["AI芯片", "服务器"],
                "difficulty": 3,
                "reward_scale": 0.8,
            },
            "bci_glasses": {
                "name": "脑电波眼镜",
                "description": "脑电波感知、情绪识别、阿尔茨海默病早期预警、意念控制",
                "robots": ["脑电波眼镜", "AI眼镜", "传感器"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "wan_optical": {
                "name": "万兆光网",
                "description": "万兆光网试点、FTTR、全光网",
                "robots": ["光模块", "光传输设备", "服务器"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "optical_400g": {
                "name": "400G超高速光传输",
                "description": "400G光传输系统、新型超低损耗光纤光缆",
                "robots": ["400G光模块", "光传输设备", "光纤光缆"],
                "difficulty": 5,
                "reward_scale": 1.3,
            },
            "low_altitude": {
                "name": "低空智联网",
                "description": "低空经济、无人机联网、eVTOL、低空物流",
                "robots": ["无人机", "eVTOL", "低空基站", "AI芯片"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "industrial_iot_6g": {
                "name": "工业互联网(6G)",
                "description": "6G工业互联网、万物智联、人-物-智能体深度交互",
                "robots": ["工业网关", "6G模组", "协作臂", "人形机器人"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
        },
    },

    # ========== 10. AI智能体平台 ==========
    "ai_agents": {
        "name": "AI智能体",
        "description": "多智能体协作、AI Agent平台",
        "sub_scenes": {
            "multi_agent": {
                "name": "多智能体协作",
                "description": "Multi-Agent协同、群体智能",
                "robots": ["人形机器人", "协作臂", "AI芯片"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "ai_workers": {
                "name": "AI数字员工",
                "description": "企业智能体、自动化办公",
                "robots": ["AI芯片", "AI服务器"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
            "agent_orchestration": {
                "name": "智能体编排",
                "description": "Agent编排、任务调度、工具调用",
                "robots": ["AI芯片", "服务器"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "autonomous_decision": {
                "name": "自主决策系统",
                "description": "复杂场景自主决策、强化学习决策",
                "robots": ["人形机器人", "四足机器人", "AI芯片"],
                "difficulty": 5,
                "reward_scale": 1.3,
            },
        },
    },

    # ========== 11. XR/VR/AR/MR ==========
    "xr": {
        "name": "XR/VR/AR/MR",
        "description": "扩展现实、元宇宙、空间计算",
        "sub_scenes": {
            "vr_training": {
                "name": "VR培训",
                "description": "虚拟培训、技能培训、安全教育",
                "robots": ["VR头显", "数据手套", "动作捕捉"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
            "ar_assisted": {
                "name": "AR辅助操作",
                "description": "AR装配指导、远程协作、维修辅助",
                "robots": ["AR眼镜", "协作臂"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "mr_design": {
                "name": "MR设计评审",
                "description": "混合现实设计、产品评审、虚拟样机",
                "robots": ["MR头显", "协作臂"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
            "metaverse": {
                "name": "元宇宙应用",
                "description": "数字孪生、虚拟工厂、元宇宙办公",
                "robots": ["VR/AR设备", "AI芯片", "服务器"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
        },
    },

    # ========== 12. 量子计算/AI算力 ==========
    "quantum": {
        "name": "量子计算/AI算力",
        "description": "量子计算机、算力中心、AI超算",
        "sub_scenes": {
            "quantum_computing": {
                "name": "量子计算",
                "description": "超导量子、光量子、量子AI",
                "robots": ["量子计算机", "AI芯片"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "ai_supercomputing": {
                "name": "AI超算中心",
                "description": "万卡集群、大模型训练、算力网络",
                "robots": ["GPU集群", "AI芯片", "服务器"],
                "difficulty": 5,
                "reward_scale": 1.3,
            },
            "edge_computing": {
                "name": "边缘计算",
                "description": "边缘AI、端侧推理、算力下沉",
                "robots": ["边缘计算盒", "AI芯片"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
            "cloud_gaming": {
                "name": "云渲染/云游戏",
                "description": "GPU云、实时渲染、云串流",
                "robots": ["GPU服务器", "AI芯片"],
                "difficulty": 3,
                "reward_scale": 0.6,
            },
        },
    },

    # ========== 13. AI操作系统/具身平台 ==========
    "ai_os": {
        "name": "AI操作系统/具身平台",
        "description": "产业具身操作系统、机器人OS、AI中台",
        "sub_scenes": {
            "embodied_os": {
                "name": "具身操作系统",
                "description": "机器人OS、具身智能中台、数据管线",
                "robots": ["人形机器人", "协作臂", "AI芯片"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "robotics_platform": {
                "name": "机器人开发平台",
                "description": "ROS、仿真平台、开发工具链",
                "robots": ["协作臂", "人形机器人"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "ai_middleware": {
                "name": "AI中台",
                "description": "大模型中台、数据中台、算法中台",
                "robots": ["AI芯片", "服务器"],
                "difficulty": 3,
                "reward_scale": 0.8,
            },
            "data_platform": {
                "name": "数据标注平台",
                "description": "具身数据采集、自动化标注、数据治理",
                "robots": ["人形机器人", "协作臂", "AI芯片"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
        },
    },

    # ========== 14. 能源/电力 ==========
    "energy": {
        "name": "能源/电力",
        "description": "电力巡检、新能源、智能电网",
        "sub_scenes": {
            "power_inspection": {
                "name": "电力巡检",
                "description": "输电线路巡检、变电站巡检、光伏清扫",
                "robots": ["四足机器人", "无人机", "巡检机器人"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "smart_grid": {
                "name": "智能电网",
                "description": "电网自动化、故障自愈、负荷预测",
                "robots": ["AI芯片", "服务器"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "new_energy": {
                "name": "新能源运维",
                "description": "风机维护、光伏清洗、储能管理",
                "robots": ["四足机器人", "攀爬机器人", "无人机"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
            "charging": {
                "name": "充电机器人",
                "description": "自动充电、换电机器人、储能机器人",
                "robots": ["充电机器人", "AMR"],
                "difficulty": 3,
                "reward_scale": 0.7,
            },
        },
    },

    # ========== 15. 建筑/基建 ==========
    "construction": {
        "name": "建筑/基建",
        "description": "建筑机器人、3D打印、装配式建筑",
        "sub_scenes": {
            "3d_printing": {
                "name": "3D打印建筑",
                "description": "混凝土3D打印、建筑工业化",
                "robots": ["建筑3D打印机", "机械臂"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "bricklaying": {
                "name": "砌砖机器人",
                "description": "自动砌砖、墙面处理、抹灰",
                "robots": ["砌砖机器人", "机械臂"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "demolition": {
                "name": "拆除机器人",
                "description": "建筑拆除、破拆机器人、隧道掘进",
                "robots": ["拆除机器人", "机械臂"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "infrastructure": {
                "name": "基建维护",
                "description": "桥梁检测、隧道巡检、道路维护",
                "robots": ["四足机器人", "无人机", "巡检机器人"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
        },
    },
}


def get_all_scenes():
    """获取所有场景列表"""
    result = []
    for scene_key, scene_data in SCENES.items():
        for sub_key, sub_data in scene_data["sub_scenes"].items():
            result.append({
                "scene": scene_key,
                "scene_name": scene_data["name"],
                "sub_scene": sub_key,
                "sub_scene_name": sub_data["name"],
                "description": sub_data["description"],
                "robots": sub_data["robots"],
                "difficulty": sub_data["difficulty"],
                "reward_scale": sub_data["reward_scale"],
            })
    return result


def get_scene_config(scene_key, sub_scene_key=None):
    """获取指定场景配置"""
    if scene_key not in SCENES:
        raise ValueError(f"未知场景: {scene_key}")
    scene = SCENES[scene_key]
    if sub_scene_key is None:
        return scene
    if sub_scene_key not in scene["sub_scenes"]:
        raise ValueError(f"未知子场景: {sub_scene_key}")
    return scene["sub_scenes"][sub_scene_key]


def list_scenes():
    """列出所有场景"""
    print("=" * 70)
    print("  AI场景全覆盖 - 场景列表")
    print("=" * 70)
    total = 0
    for scene_key, scene_data in SCENES.items():
        sub_count = len(scene_data["sub_scenes"])
        total += sub_count
        print(f"\n【{scene_data['name']}】({scene_key}) - {sub_count}个子场景")
        for sub_key, sub_data in scene_data["sub_scenes"].items():
            diff = "⭐" * sub_data["difficulty"]
            print(f"  • {sub_data['name']:12s} [{sub_key:20s}] 难度:{diff}")
            print(f"    适用机器人: {', '.join(sub_data['robots'])}")
    print(f"\n总计: {len(SCENES)}大场景, {total}个子场景")
    print("=" * 70)


if __name__ == "__main__":
    list_scenes()
