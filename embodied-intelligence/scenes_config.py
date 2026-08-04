"""
AI场景全覆盖配置中心
覆盖21大应用场景、100个子场景
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
                "reward_scale": 1.2,
            },
            "handling": {
                "name": "搬运码垛",
                "description": "物料搬运、箱子码垛",
                "robots": ["码垛机器人", "AGV/AMR", "协作臂"],
                "difficulty": 2,
                "reward_scale": 1.1,
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
                "reward_scale": 1.2,
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
                "reward_scale": 1.2,
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
                "reward_scale": 1.2,
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
                "reward_scale": 1.2,
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
                "reward_scale": 1.2,
            },
            "food_processing": {
                "name": "食品加工",
                "description": "肉类加工、烘焙、包装",
                "robots": ["协作臂", "Delta机器人", "SCARA"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "livestock": {
                "name": "畜牧养殖",
                "description": "奶牛挤奶、饲料投放",
                "robots": ["农业机器人", "四足机器人", "AMR"],
                "difficulty": 2,
                "reward_scale": 1.1,
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
                "reward_scale": 1.1,
            },
            "catering": {
                "name": "餐饮服务",
                "description": "送餐、调酒、咖啡制作",
                "robots": ["送餐机器人", "协作臂", "人形机器人"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "hotel": {
                "name": "酒店服务",
                "description": "前台接待、行李搬运、客房服务",
                "robots": ["服务机器人", "人形机器人", "AMR"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "cleaning": {
                "name": "清洁保洁",
                "description": "地面清洁、玻璃清洁",
                "robots": ["清洁机器人", "人形机器人"],
                "difficulty": 2,
                "reward_scale": 1.1,
            },
            "ai_content_compliance": {
                "name": "AI内容合规",
                "description": "AI生成内容标识、算法推荐管理、内容审核、智能终端合规",
                "robots": ["AI审核系统", "内容生成AI", "智能终端", "可穿戴设备"],
                "difficulty": 4,
                "reward_scale": 1.3,
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
                "reward_scale": 1.1,
            },
            "training": {
                "name": "技能培训",
                "description": "工业机器人操作培训",
                "robots": ["六轴机械臂", "协作臂"],
                "difficulty": 3,
                "reward_scale": 1.2,
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
                "reward_scale": 1.0,
            },
            "companion": {
                "name": "家庭陪伴",
                "description": "儿童陪伴、老人陪护",
                "robots": ["人形机器人", "陪伴机器人"],
                "difficulty": 2,
                "reward_scale": 1.1,
            },
            "ai_glasses": {
                "name": "AI眼镜",
                "description": "AR眼镜、智能眼镜",
                "robots": ["AI眼镜"],
                "difficulty": 2,
                "reward_scale": 1.1,
            },
            "ai_phone": {
                "name": "AI手机",
                "description": "AI终端、智能终端",
                "robots": ["AI手机"],
                "difficulty": 1,
                "reward_scale": 1.0,
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
                "reward_scale": 1.2,
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
                "reward_scale": 1.2,
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
                "reward_scale": 1.2,
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
                "reward_scale": 1.2,
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
                "reward_scale": 1.2,
            },
            "cloud_gaming": {
                "name": "云渲染/云游戏",
                "description": "GPU云、实时渲染、云串流",
                "robots": ["GPU服务器", "AI芯片"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "wafer_scale": {
                "name": "晶圆级计算",
                "description": "整片晶圆AI芯片、存算一体、多芯粒集成、大模型训练超算",
                "robots": ["晶圆级芯片", "存算一体", "多芯粒系统", "大模型训练"],
                "difficulty": 5,
                "reward_scale": 1.5,
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
                "reward_scale": 1.2,
            },
            "data_platform": {
                "name": "数据标注平台",
                "description": "具身数据采集、自动化标注、数据治理",
                "robots": ["人形机器人", "协作臂", "AI芯片"],
                "difficulty": 3,
                "reward_scale": 1.2,
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
                "reward_scale": 1.2,
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

    # ========== 16. 海洋工程 ==========
    "marine": {
        "name": "海洋工程",
        "description": "海洋探测、深海作业、海上作业",
        "sub_scenes": {
            "ocean_exploration": {
                "name": "海洋探测",
                "description": "深海探测、海底地形测绘、海洋资源勘探",
                "robots": ["水下机器人", "无人船", "水下无人机"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "offshore_operation": {
                "name": "海上作业",
                "description": "海上平台维护、海底管道铺设、海上风电安装",
                "robots": ["水下机器人", "机械臂", "无人船"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "aquaculture": {
                "name": "深海养殖",
                "description": "深海网箱养殖、自动化投喂、水质监测",
                "robots": ["水下机器人", "无人船", "机械臂"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "salvage": {
                "name": "水下打捞",
                "description": "沉船打捞、水下救援、水下焊接切割",
                "robots": ["水下机器人", "机械臂", "水下无人机"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "marine_biology": {
                "name": "海洋生物研究",
                "description": "海洋生物观测、珊瑚礁监测、鲸鱼追踪",
                "robots": ["水下机器人", "水下无人机", "传感器"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
        },
    },

    # ========== 17. 航空航天 ==========
    "aerospace": {
        "name": "航空航天",
        "description": "航天器维护、卫星服务、航空制造",
        "sub_scenes": {
            "spacecraft_maintenance": {
                "name": "航天器维护",
                "description": "空间站维护、卫星修理、太空垃圾清理",
                "robots": ["航天机器人", "机械臂", "人形机器人"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "satellite_service": {
                "name": "卫星服务",
                "description": "卫星在轨服务、燃料补给、轨道调整",
                "robots": ["航天机器人", "机械臂"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "aircraft_manufacturing": {
                "name": "航空制造",
                "description": "飞机装配、发动机制造、复合材料加工",
                "robots": ["协作臂", "六轴机械臂", "AGV/AMR"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "airport_operations": {
                "name": "机场运营",
                "description": "飞机牵引、行李搬运、跑道巡检",
                "robots": ["AGV/AMR", "四足机器人", "无人机"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "uav_delivery": {
                "name": "无人机物流",
                "description": "城市配送、偏远地区运输、紧急物资投送",
                "robots": ["无人机", "eVTOL", "AGV/AMR"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
        },
    },

    # ========== 18. 应急救援 ==========
    "emergency": {
        "name": "应急救援",
        "description": "灾害救援、消防灭火、事故处理",
        "sub_scenes": {
            "earthquake_rescue": {
                "name": "地震救援",
                "description": "废墟搜救、生命探测、伤员转移",
                "robots": ["四足机器人", "无人机", "蛇形机器人"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "fire_fighting": {
                "name": "消防灭火",
                "description": "高层建筑灭火、森林火灾扑救、化工厂灭火",
                "robots": ["消防机器人", "无人机", "四足机器人"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "flood_rescue": {
                "name": "洪涝救援",
                "description": "洪水搜救、堤坝巡检、水上救援",
                "robots": ["无人船", "无人机", "水下机器人"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "chemical_accident": {
                "name": "危化品事故",
                "description": "化学品泄漏处理、核事故应急、有毒环境作业",
                "robots": ["防爆机器人", "四足机器人", "无人机"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "mountain_rescue": {
                "name": "山地救援",
                "description": "登山者救援、雪崩搜救、悬崖救援",
                "robots": ["无人机", "四足机器人", "人形机器人"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
        },
    },

    # ========== 19. 环保监测 ==========
    "environmental": {
        "name": "环保监测",
        "description": "环境监测、污染治理、生态保护",
        "sub_scenes": {
            "air_quality": {
                "name": "空气质量监测",
                "description": "大气污染监测、工业排放监测、室内空气质量",
                "robots": ["无人机", "传感器", "四足机器人"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "water_monitoring": {
                "name": "水质监测",
                "description": "河流湖泊监测、饮用水监测、污水排放监测",
                "robots": ["无人船", "水下机器人", "传感器"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "waste_sorting": {
                "name": "垃圾分类",
                "description": "智能垃圾分类、可回收物分拣、有害垃圾处理",
                "robots": ["协作臂", "Delta机器人", "AI视觉系统"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "ecological_protection": {
                "name": "生态保护",
                "description": "野生动物监测、森林巡护、湿地保护",
                "robots": ["无人机", "四足机器人", "传感器"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "pollution_cleanup": {
                "name": "污染治理",
                "description": "土壤修复、水体净化、油污清理",
                "robots": ["四足机器人", "无人机", "机械臂"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
        },
    },

    # ========== 20. 数字孪生 ==========
    "digital_twin": {
        "name": "数字孪生",
        "description": "虚拟仿真、虚实映射、预测优化",
        "sub_scenes": {
            "factory_simulation": {
                "name": "工厂仿真",
                "description": "虚拟工厂建模、产线仿真、工艺优化",
                "robots": ["协作臂", "AGV/AMR", "AI芯片"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "city_modeling": {
                "name": "城市建模",
                "description": "智慧城市数字孪生、交通仿真、城市规划",
                "robots": ["无人机", "AI芯片", "服务器"],
                "difficulty": 5,
                "reward_scale": 1.3,
            },
            "product_testing": {
                "name": "产品测试",
                "description": "虚拟产品测试、性能仿真、可靠性验证",
                "robots": ["协作臂", "AI芯片", "传感器"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "predictive_maintenance": {
                "name": "预测性维护",
                "description": "设备健康监测、故障预测、维护优化",
                "robots": ["传感器", "AI芯片", "四足机器人"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
            "virtual_commissioning": {
                "name": "虚拟调试",
                "description": "设备虚拟调试、控制算法验证、系统集成测试",
                "robots": ["协作臂", "人形机器人", "AI芯片"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "data_pipeline": {
                "name": "数据管线",
                "description": "多源数据采集、清洗、标注、训练数据生成、数据飞轮闭环",
                "robots": ["AI芯片", "传感器", "服务器", "云端平台"],
                "difficulty": 5,
                "reward_scale": 1.2,
            },
        },
    },

    # ========== 21. AI基础设施 ==========
    "ai_infrastructure": {
        "name": "AI基础设施",
        "description": "AI算力中心、推理引擎、模型服务",
        "sub_scenes": {
            "inference_engine": {
                "name": "推理引擎部署",
                "description": "SGLang/vLLM/RadixArk等推理引擎部署与优化、KV Cache管理、连续批处理",
                "robots": ["AI芯片", "GPU服务器", "推理加速卡"],
                "difficulty": 5,
                "reward_scale": 1.3,
            },
            "phyai_framework": {
                "name": "PhyAI推理加速框架",
                "description": "π系列VLA模型硬件适配、5090平台2倍+推理加速、模型硬件解耦一次适配多模型复用",
                "robots": ["AI芯片", "RTX 5090服务器", "推理框架"],
                "difficulty": 5,
                "reward_scale": 1.2,
            },
            "edge_vla_deployment": {
                "name": "端侧VLA模型部署",
                "description": "1.5B/0.9B参数具身模型端侧部署、120ms决策延迟、断网离线跟踪、敏感画面本地处理",
                "robots": ["人形机器人", "四足机器人", "端侧AI芯片"],
                "difficulty": 5,
                "reward_scale": 1.3,
            },
        },
    },

    # ========== 22. 智慧药房/医疗零售 ==========
    "smart_pharmacy": {
        "name": "智慧药房与医疗零售",
        "description": "机器人智慧药房、无人药店、药品分拣配送、医疗零售自动化",
        "sub_scenes": {
            "robot_pharmacy_workflow": {
                "name": "机器人药房全流程",
                "description": "问诊→取药→传送→打包→出库全程机器人协同、90秒全流程闭环、三台异构机器人各司其职",
                "robots": ["人形机器人", "协作臂", "移动机器人", "LingBot-VLA 2.0"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "night_pharmacy_duty": {
                "name": "夜间药房值班",
                "description": "融入现有门店布局无需改造、店员顾客共处一室、高频重复分拣任务分担、24小时无人值守",
                "robots": ["药房人形机器人", "协作臂", "安全传感器"],
                "difficulty": 3,
                "reward_scale": 1.1,
            },
            "multi_vendor_adaptation": {
                "name": "多品牌异构机器人适配",
                "description": "单套具身大模型驾驭17家厂商20余种构型、免重复开发控制方案、统一API编排调度",
                "robots": ["乐聚机器人", "星海图机器人", "自研R-2", "多构型机器人"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "chain_store_expansion": {
                "name": "连锁门店规模化铺开",
                "description": "国大药房上海店实际运营、2026年计划铺至20-50家门店、快速复制标准化方案",
                "robots": ["部署平台", "云边协同系统", "运营管理后台"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
        },
    },

    # ========== 23. 即时零售无人店 ==========
    "instant_retail": {
        "name": "即时零售与无人便利店",
        "description": "具身智能机器人小店、无人零售、前置仓自动化、写字楼/景区即时服务",
        "sub_scenes": {
            "robot_convenience_store": {
                "name": "机器人无人便利店",
                "description": "机器人自主识别商品→抓取→补货→整理货架→盘点库存→用户扫码购买全流程无人干预",
                "robots": ["人形机器人", "移动抓取平台", "SenseNova大模型"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "office_scene_deployment": {
                "name": "写字楼即时零售",
                "description": "茶水间/大堂无人货架、高频消费品即时补给、库存自动预警补货、消费数据闭环",
                "robots": ["补货机器人", "库存盘点系统", "无人收银终端"],
                "difficulty": 3,
                "reward_scale": 1.1,
            },
            "scenic_area_retail": {
                "name": "景区/场馆零售",
                "description": "人流高峰应对、游客扫码自助、纪念品/饮料/零食分类、旅游旺季7×24小时运营",
                "robots": ["零售机器人", "多模态导购终端", "移动支付系统"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "front_warehouse_automation": {
                "name": "前置仓自动化",
                "description": "30分钟达即时配送前置仓、SKU冷热区智能摆放、效期管理临期预警、拣货打包一体化",
                "robots": ["AMR/AGV", "协作分拣臂", "视觉质检系统"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
        },
    },

    # ========== 24. 工厂产线人形作业 ==========
    "factory_production_line": {
        "name": "工厂产线人形机器人作业",
        "description": "人形机器人进厂拧螺丝、拆垛上料、搬运装配、产线无人化拐点场景",
        "sub_scenes": {
            "carton_unpalletizing": {
                "name": "拆纸箱垛拆塑料箱垛",
                "description": "产线1:1复刻三台并行、纸箱垛/塑料箱垛/小件上料各司其职、流水线动作无停顿无人员介入",
                "robots": ["工业人形机器人", "视觉定位系统", "力控夹爪"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "continuous_long_running": {
                "name": "8-10小时连续不间断运行",
                "description": "日运行目标8-10小时、真实工厂验证3-4个月、实时计时器显示连续运行时长、零停机故障率",
                "robots": ["工业人形机器人", "热管理系统", "电池快充系统"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "stack_national_solution": {
                "name": "全栈国产化解决方案",
                "description": "工业/商服/科研/训练场四大场景、大脑小脑本体全链路自主可控、客户一汽中兴长虹海晨等",
                "robots": ["全栈人形机器人", "国产控制器", "国产伺服电机", "国产传感器"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "small_parts_feeding": {
                "name": "金属小件上料装配",
                "description": "轴承座/法兰/紧固件等小件精准取放、公差配合微米级、3D视觉定位加力控装配",
                "robots": ["工业人形机器人", "3D视觉", "力控夹爪", "上料台"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
        },
    },

    # ========== 25. 小儿外科微创医疗 ==========
    "pediatric_minimally_invasive_surgery": {
        "name": "小儿外科单孔微创手术",
        "description": "蛇形臂单孔手术机器人赋能小儿泌尿外科普外科、极致微创无痕、高难度术式突破",
        "sub_scenes": {
            "single_port_urology": {
                "name": "单孔泌尿外科高难度术式",
                "description": "肾盂成形术、双侧输尿管再植术、精索静脉曲张结扎术、1.8cm单孔鞘管三器械加3D镜协同",
                "robots": ["术锐蛇形臂单孔机器人", "3D高清内窥镜", "主从操作控制台"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "pediatric_spleen_resection": {
                "name": "小儿普外科单孔脾切除",
                "description": "遗传性球形红细胞增多症脾切除、脐部3cm切口疤痕天然隐藏、一家三口三代术式见证20cm→无痕",
                "robots": ["术锐单孔机器人", "电凝钩器械", "吻合器"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "bladder_augmentation_9yo": {
                "name": "首例儿童单孔膀胱扩大术",
                "description": "9岁男孩七年漏尿顽疾、膀胱容量50ml→恢复、左肾萎缩+双输尿管反流、失血仅50ml国内外首例",
                "robots": ["术锐单孔机器人", "精密分离器械", "缝合持针器"],
                "difficulty": 5,
                "reward_scale": 1.6,
            },
            "five_cases_single_day": {
                "name": "单日五连台无缝接续",
                "description": "不同病种跨亚专业无缝接续、微调鞘管角度覆盖全腹无需整机移位重校准、日均4-5台常态化",
                "robots": ["术锐单孔机器人", "快速对接推车", "手术团队协同系统"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "cross_border_pediatric_case": {
                "name": "巴基斯坦跨国儿科救治",
                "description": "4岁女童左肾积水多年、慕名专程上海就医、术后第四天出院标准、国产机器人国际担当",
                "robots": ["术锐单孔机器人", "国际远程会诊平台", "术后康复随访系统"],
                "difficulty": 5,
                "reward_scale": 1.6,
            },
        },
    },

    # ========== 26. 特种极端环境巡检 ==========
    "special_extreme_inspection": {
        "name": "特种极端环境巡检作业",
        "description": "矿山/能源/石油石化/危险巡检/防汛/极端环境、普通人永远进不去的危险区域",
        "sub_scenes": {
            "underground_substation": {
                "name": "变电站夹层地下管廊",
                "description": "狭小复杂人进不去空间、特种小型轮足灵巧钻入、四防能力继承、先头探路急先锋",
                "robots": ["好奇者S01轮足", "地下管廊机器人", "气体/温湿度传感器"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "mine_petrochemical": {
                "name": "矿山能源石油石化",
                "description": "粉尘积水陡坡高温环境、IP67防护加高效散热、扛设备连续走静态支撑应对突发冲击",
                "robots": ["MOVENEW P系列轮足", "山猫M20S轮足", "防爆气体传感器"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "flood_control_emergency": {
                "name": "防汛勇士应急救援",
                "description": "行业首个AI防汛机器狗、1米水深泡30分钟照常、9m/s极限冲锋、沙袋/救生圈投送",
                "robots": ["山猫M20S重载轮足", "防汛专用挂载", "水声通信模块"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "12h_full_shift_patrol": {
                "name": "12小时完整班次独立巡检",
                "description": "自研能量回收系统、从展品变工具、独立顶完一个完整班次无需充电换班",
                "robots": ["MOVENEW P系列轮足", "自研能量回收模组", "低功耗控制系统"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "35kg_load_heavy_haul": {
                "name": "35公斤重载户外安防",
                "description": "扛重物长距离奔袭、挂载消防水带/应急通信/侦查设备、越恶劣环境越稳",
                "robots": ["山猫M20S轮足", "重载挂载接口", "红外热像侦查设备"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
        },
    },

    # ========== 27. 接触智能触觉力控 ==========
    "contact_intelligence": {
        "name": "接触智能触觉力控",
        "description": "从看见走到摸到之后怎么办、灵巧手触觉力控、软物体形变操作、折气球等高难度",
        "sub_scenes": {
            "balloon_folding_dexterity": {
                "name": "折气球灵巧操作",
                "description": "气球太软抓轻滑抓重爆、接触点摩擦力形变实时变化、持续判断实时调整力度、比拧螺丝抓杯子难数倍",
                "robots": ["OmniHand 3 Ultra-M灵巧手", "双臂人形机器人", "300点触觉阵列"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "0_005n_force_resolution": {
                "name": "0.005牛级法向力分辨",
                "description": "一张纸轻压力度即可感知、指尖微型视觉传感器加300+三维触觉点、全直驱无齿轮传动20自由度",
                "robots": ["OmniHand 3 Ultra-M灵巧手", "指尖视觉传感器", "触觉感知算法"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "imitation_learning_dataset": {
                "name": "力觉模仿学习数据集",
                "description": "主臂遥操作实时复刻动作、接触摩擦碰撞力觉数据同步保存、用于后续模仿学习和力控模型训练",
                "robots": ["Diana3+Diana7 G2力反馈系统", "数据采集平台", "模仿学习训练集群"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "40000_units_data_flywheel": {
                "name": "4万台部署物理数据飞轮",
                "description": "工业场景部署4万台机器每日干活、工厂医疗物流能源产真实交互数据、物理数据壁垒比语言模型更深",
                "robots": ["工业部署机器群", "力觉视觉数据管线", "物理世界大模型训练平台"],
                "difficulty": 5,
                "reward_scale": 1.6,
            },
        },
    },

    # ========== 28. 情感陪伴长记忆消费 ==========
    "emotional_companion_consumer": {
        "name": "情感陪伴长记忆消费机器人",
        "description": "AI情感陪伴宠物、家庭陪伴、长记忆关系型交互、老年陪护儿童陪伴",
        "sub_scenes": {
            "ai_pet_long_memory": {
                "name": "AI宠物长期关系记忆",
                "description": "摸它有反应多触点、多轮对话自然流畅、放进AI宠物变成关系而非功能、区别功能型机器人",
                "robots": ["iMoochi AI宠物", "多模态情感对话系统", "长期记忆向量库"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "elder_children_companion": {
                "name": "老人儿童情感陪护",
                "description": "独居老人24小时陪伴、儿童讲故事互动游戏、健康提醒情绪疏导、家庭关系数字化",
                "robots": ["情感陪伴机器人", "健康监测传感器", "家庭安全守护系统"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "wearable_ai_ears": {
                "name": "耳夹式AI助手穿戴",
                "description": "不用掏手机看屏幕、AI从屏幕挪到耳朵交互范式革新、同声传译会议纪要健康记录随时在线",
                "robots": ["千问AI耳夹耳机", "Bose声学团队调音", "低功耗穿戴芯片"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "home_wheel_assistant": {
                "name": "家庭轮式移动助理",
                "description": "语音操控你好XX、移动抓取物品取快递拿饮料、颜色分类整理玩具、办公室家庭双场景",
                "robots": ["思灵H10-W轮式机器人", "语音助手", "移动抓取底盘"],
                "difficulty": 3,
                "reward_scale": 1.1,
            },
        },
    },

    # ========== 29. 机器人手机物理交互 ==========
    "robot_phone_embodied_interaction": {
        "name": "机器人手机物理交互",
        "description": "从智能体手机迈向机器人手机、机械云台身体性、动作肢体语言交互新范式",
        "sub_scenes": {
            "gimbal_body_language": {
                "name": "4自由度云台肢体语言",
                "description": "机身顶部专业级机械云台、主动转向说话人跟拍移动主体、放桌上自主观察周围环境动作表达反馈",
                "robots": ["荣耀Robot Phone", "4自由度微云台", "环境感知多摄系统"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "cross_app_continuous_tasks": {
                "name": "跨应用连续长程任务",
                "description": "听懂复杂指令自动办跨应用连续任务、系统级GUI Agent架构看懂屏幕内容、像人手指跨应用点来点去",
                "robots": ["NaviX Ultra手机", "荣耀Robot Phone", "STEPX Neo手机"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "permission_governance_system": {
                "name": "智能体权限治理体系",
                "description": "Agent行为透明可回滚每次调用访问执行入日志、执行动作一键撤回安全兜底、精细授权始终用户决策",
                "robots": ["Amoo助手系统", "豆包手机助手", "荣耀Agentic OS"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "100ms_realtime_response": {
                "name": "100ms级实时交互",
                "description": "操作体验临界线约200ms、100ms级实时响应够快够安全、隐私不出设备端到端加密",
                "robots": ["STEPX Neo Step AOS系统", "端侧大模型推理引擎", "隐私计算模块"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
        },
    },

    # ========== 30. 集群协同表演与展示 ==========
    "swarm_collab_exhibition": {
        "name": "集群协同表演与展示",
        "description": "多机器人集群同步控制、协同齐舞翻跃、大型展会巡演、文旅商演规模化运营",
        "sub_scenes": {
            "10plus_quadruped_synchronized": {
                "name": "10+四足集群同步表演",
                "description": "十几只灵猫双展馆同时亮相、720°连续后空翻侧空翻群舞协同7组动作、集群调度下同步控制水平",
                "robots": ["Cyberling灵猫四足", "集群调度系统", "5G/WiFi6时间同步网络"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "boxing_match_two_humanoids": {
                "name": "双人形擂台拳击对抗",
                "description": "两台G1人形擂台拳击对练、武术动作切换、全身协调控制扛复杂对抗、快速动作切换动态平衡",
                "robots": ["宇树G1人形", "动作捕捉系统", "擂台安全防护系统"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "full_matrix_three_form": {
                "name": "全矩阵三形态同台展示",
                "description": "轮足山猫系列+四足绝影系列+人形DR02系列三形态全矩阵、电力/应急/安防/消防/林草/教育六大行业方案",
                "robots": ["山猫S10/M20S", "绝影四足系列", "DR02人形", "六大行业方案套件"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "rental_sharing_platform": {
                "name": "机器人共享租赁调度",
                "description": "擎天租共享租赁加平台化调度、文旅演出企业年会商业活动按需获取、卖服务替代卖产品",
                "robots": ["租赁机器人群", "擎天租平台", "标准化交付流程"],
                "difficulty": 3,
                "reward_scale": 1.2,
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
