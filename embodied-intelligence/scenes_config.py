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
                "robots": ["六轴机械臂", "协作臂", "焊接变位机", "焊缝跟踪系统", "烟尘净化设备"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "painting": {
                "name": "喷涂涂装",
                "description": "汽车喷涂、表面处理",
                "robots": ["六轴机械臂", "防爆喷涂机器人", "静电旋杯", "供漆系统", "水帘喷房"],
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
                "robots": ["六轴机械臂", "桁架机器人", "机床通信接口", "末端快换夹具", "物料缓存台"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "coal_mine_pit_collaborative_inspection": {
                "name": "煤矿矿井人机协同巡检（真实井下训练一个月）",
                "description": "井下环境光线暗地面不平管线多，人形机器人经常迷路，人机协同减少人员下井次数降低风险，关键环节仍需人工工程确认，擎天智连真实场景已通过一个月训练",
                "robots": ["擎天智连训练定制人形机器人", "路径设定+检测内容输入+跑错调参闭环流程", "人机协同双备份巡检路线", "井下防爆ATEX认证通信设备", "多机协同24h三班倒不停机巡检"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "parallel_delta_high_speed_sorting": {
                "name": "工业并联Delta机器人高速轻载分拣（0.4秒节拍）",
                "description": "蜘蛛型Delta四轴并联架构，食品医药电子洁净车间高速分拣，视觉识别+传送带跟踪+高速抓取三位一体，天津辰星实景验证",
                "robots": ["天津辰星Delta并联4轴机器人", "GigE Vision视觉定位识别", "传送带编码器Profinet同步跟踪", "0.4秒标准节拍分拣路径规划", "洁净车间ISO 5级颗粒度控制"],
                "difficulty": 4,
                "reward_scale": 1.6,
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
            "humanoid_warehouse_shelf_full_height_handling": {
                "name": "人形机器人仓库1.2m~3.5m全高度货架存取（蹲取+站取）",
                "description": "人形机器人在真实电商仓库场景，蹲下取货架低层物品，站立取高层3.5m物品，优必选Walker S2已实景量产验证",
                "robots": ["优必选Walker S2量产人形", "1.2m蹲姿低位抓取", "3.5m站立伸出手臂高位抓取", "仓储标准塑料周转箱精准搬运", "仓库WMS系统任务对接"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "flexible_amr_multi_layer_rack_transfer": {
                "name": "柔性AMR多层货架自动提升搬运（3层+300kg）",
                "description": "天津摩尔MOVER系列柔性移动机器人，三层以上自动提升结构，激光SLAM+二维码双融合定位，汽车零部件和3C电子仓储kitting场景",
                "robots": ["天津摩尔MOVER柔性移动机器人", "3层+自动提升机构伺服控制", "激光SLAM+二维码融合定位导航", "3C电子/汽车零部件料箱搬运", "百台级AMR集群VDA5050调度"],
                "difficulty": 3,
                "reward_scale": 1.5,
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
                "robots": ["手术机器人", "协作臂", "主从操作控制台", "3D高清内窥镜", "手术规划系统"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "rehab": {
                "name": "康复训练",
                "description": "上肢/下肢康复、运动恢复",
                "robots": ["康复机器人", "外骨骼", "力反馈训练台", "肌电信号采集", "康复评估系统"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "nursing": {
                "name": "护理陪伴",
                "description": "老年护理、患者陪护",
                "robots": ["人形机器人", "服务机器人", "生命体征监测", "服药提醒系统", "紧急呼叫装置"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "diagnosis": {
                "name": "诊断辅助",
                "description": "影像诊断、病理分析",
                "robots": ["协作臂", "AI视觉系统", "医学影像工作站", "病理切片扫描仪", "辅助诊断AI模型"],
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
                "robots": ["服务机器人", "人形机器人", "语音交互屏", "商品识别摄像头", "会员系统对接"],
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
                "robots": ["清洁机器人", "人形机器人", "擦窗机器人", "洗地机", "垃圾分拣设备"],
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
                "robots": ["六轴机械臂", "协作臂", "实训工作站", "离线编程软件", "虚拟仿真教学"],
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
                "robots": ["扫地机器人", "人形机器人", "擦窗机器人", "洗地机器人", "垃圾收集器"],
                "difficulty": 1,
                "reward_scale": 1.0,
            },
            "companion": {
                "name": "家庭陪伴",
                "description": "儿童陪伴、老人陪护",
                "robots": ["人形机器人", "陪伴机器人", "语音助手", "视频通话设备", "健康监测手环"],
                "difficulty": 2,
                "reward_scale": 1.1,
            },
            "ai_glasses": {
                "name": "AI眼镜",
                "description": "AR眼镜、智能眼镜",
                "robots": ["AI眼镜", "MicroOLED显示屏", "骨传导耳机", "摄像头模组", "端侧AI芯片"],
                "difficulty": 2,
                "reward_scale": 1.1,
            },
            "ai_phone": {
                "name": "AI手机",
                "description": "AI终端、智能终端",
                "robots": ["AI手机", "NPU神经网络处理器", "大模型端侧部署", "多模态摄像头", "隐私安全计算"],
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
                "robots": ["水下机器人", "机械臂", "水下声呐", "防水云台相机", "脐带缆管理系统"],
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
                "robots": ["5G-A基站", "工业网关", "AAU有源天线", "边缘计算MEC", "RedCap轻量化终端"],
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
                "robots": ["AI芯片", "服务器", "网络数字孪生", "智能告警系统", "自动配置下发"],
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
                "robots": ["AI芯片", "AI服务器", "RPA流程机器人", "知识库向量数据库", "多模态大模型"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "agent_orchestration": {
                "name": "智能体编排",
                "description": "Agent编排、任务调度、工具调用",
                "robots": ["AI芯片", "服务器", "工作流引擎", "工具调用框架", "多智能体协调器"],
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
                "robots": ["AR眼镜", "协作臂", "空间锚点定位", "远程专家系统", "数字孪生叠加"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "mr_design": {
                "name": "MR设计评审",
                "description": "混合现实设计、产品评审、虚拟样机",
                "robots": ["MR头显", "协作臂", "全息投影", "手势交互", "多人协同评审"],
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
                "robots": ["量子计算机", "AI芯片", "稀释制冷机", "量子测控系统", "量子算法库"],
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
                "robots": ["边缘计算盒", "AI芯片", "5G模组", "端侧推理框架", "边云协同调度"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "cloud_gaming": {
                "name": "云渲染/云游戏",
                "description": "GPU云、实时渲染、云串流",
                "robots": ["GPU服务器", "AI芯片", "低延迟编码", "边缘节点CDN", "串流协议优化"],
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
                "robots": ["协作臂", "人形机器人", "ROS/ROS2框架", "Gazebo/MuJoCo仿真", "可视化调试工具"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "ai_middleware": {
                "name": "AI中台",
                "description": "大模型中台、数据中台、算法中台",
                "robots": ["AI芯片", "服务器", "模型服务平台", "特征工程平台", "MLOps流水线"],
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
                "robots": ["AI芯片", "服务器", "SCADA系统", "PMU相量测量", "配电自动化终端"],
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
                "robots": ["充电机器人", "AMR", "自动充电桩", "电池换电站", "BMS电池管理"],
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
                "robots": ["建筑3D打印机", "机械臂", "混凝土泵送系统", "数控喷嘴", "建筑信息模型BIM"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "bricklaying": {
                "name": "砌砖机器人",
                "description": "自动砌砖、墙面处理、抹灰",
                "robots": ["砌砖机器人", "机械臂", "砂浆供给系统", "激光定位找平", "CAD图纸导入"],
                "difficulty": 4,
                "reward_scale": 1.0,
            },
            "demolition": {
                "name": "拆除机器人",
                "description": "建筑拆除、破拆机器人、隧道掘进",
                "robots": ["拆除机器人", "机械臂", "液压破碎锤", "远程遥控系统", "粉尘抑制装置"],
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
                "robots": ["航天机器人", "机械臂", "空间对接机构", "燃料补加模块", "在轨操控系统"],
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

    # ========== 31. 脑机接口/神经科技 ==========
    "bci_neurotech": {
        "name": "脑机接口与神经科技",
        "description": "非侵入式脑机接口、肌电感知、神经意图读取、人机交互新范式",
        "sub_scenes": {
            "noninvasive_bci_control": {
                "name": "非侵入式脑机接口控制",
                "description": "128通道脑电帽、21名受试者运动想象实时控制机器手单根手指、两指任务80.56%准确率、三指任务60.61%准确率",
                "robots": ["脑电帽", "机器手", "信号处理系统"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "emg_intention_reading": {
                "name": "肌电意图读取系统",
                "description": "表面肌电位于大脑运动指令传向肌肉的链路中间、包含动作即将发生时的神经肌肉活动、发力和微控制信息、脑电更接近运动想象注意惊讶和错误感知等高层状态",
                "robots": ["肌电传感器", "脑电设备", "意图解码算法"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "neuro_tactile_closed_loop": {
                "name": "神经意图与触觉闭环",
                "description": "脑电或肌电提供人的意图与状态、机器人视觉理解场景、触觉感知接触结果、具身模型完成规划与控制、反馈再返回给人或者被用于继续修正动作",
                "robots": ["脑机接口", "触觉传感器", "视觉系统", "具身模型"],
                "difficulty": 5,
                "reward_scale": 1.6,
            },
            "bci_prosthetics_rehab": {
                "name": "脑机接口假肢康复",
                "description": "神经接口提供自然控制、触觉反馈帮助判断抓握是否稳定、康复假肢工业协作智能眼镜和服务机器人中都具有直接价值",
                "robots": ["神经接口假肢", "触觉反馈系统", "康复训练平台"],
                "difficulty": 4,
                "reward_scale": 1.4,
            },
        },
    },

    # ========== 32. 具身数据/多模态采集 ==========
    "embodied_data_collection": {
        "name": "具身数据与多模态采集",
        "description": "多模态具身数据集、肌电视觉融合、因果密度数据、EgoEMG数据集",
        "sub_scenes": {
            "egoemg_dataset": {
                "name": "EgoEMG多模态具身数据集",
                "description": "清华大学自动化系冯建江团队发布、同步采集41名受试者的双侧肌电IMU第一视角RGB外部RGB-D和光学动捕数据、覆盖60类手势超过10小时并重建22自由度手部关节角",
                "robots": ["EMG腕带", "头戴式自我中心视角RGB相机", "外部ZED 2i RGB-D相机", "光学动作捕捉系统"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "emg_vision_fusion": {
                "name": "肌电与视觉融合",
                "description": "EMGFormer在跨用户泛化任务上较上一代基线提升22%、肌电与视觉融合在遮挡运动模糊和深度歧义场景中优于单一视觉方案",
                "robots": ["EMG传感器", "视觉相机", "融合算法模型"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "causal_density_data": {
                "name": "因果密度数据竞争",
                "description": "具身智能的数据竞争正在从数量走向因果密度、同样一段动作视频如果同时包含神经意图发力变化和错误反馈它对模型的价值不只是多一个模态而是多了一条解释动作为何发生的因果链",
                "robots": ["多模态采集系统", "神经意图传感器", "力觉传感器", "因果推理模型"],
                "difficulty": 5,
                "reward_scale": 1.6,
            },
            "data_unit_evolution": {
                "name": "机器人数据基本单位演进",
                "description": "从视频-动作变为场景-意图-肌肉激活-动作轨迹-接触反馈-结果、机器人学习的也不再只是模仿表面动作而是逼近人类完整的感知决策与执行链条",
                "robots": ["多模态传感器", "意图解码器", "动作规划模型", "触觉反馈系统"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
        },
    },

    # ========== 33. 具身机器人供应链/产业生态 ==========
    "embodied_supply_chain": {
        "name": "具身机器人供应链与产业生态",
        "description": "人形机器人核心零部件、扁电磁线、关节模组、智能关节解决方案、产业生态",
        "sub_scenes": {
            "humanoid_core_components": {
                "name": "人形机器人核心零部件",
                "description": "无框力矩电机、关节模组、全向舵轮等核心部件、从样品到批量订单转化、分布式AI控制理念、软硬件一体化智能关节解决方案",
                "robots": ["无框力矩电机", "关节模组", "全向舵轮", "智能关节系统"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "flat_wire_power_grid": {
                "name": "扁电磁线与智能电网",
                "description": "扁电磁线和电线电缆双主业协同、欧洲捷克基地年产能2万吨、清洁能源智能电网智能装备三大新兴应用领域、变压器用扁电磁线产品",
                "robots": ["扁电磁线生产设备", "智能电网设备", "变压器"],
                "difficulty": 3,
                "reward_scale": 1.2,
            },
            "industrial_robot_supply_chain": {
                "name": "工业机械臂供应链突破",
                "description": "成功进入全球工业机械臂和协作机器人龙头企业供应链、实现从0到1突破、正迈向规模化放量",
                "robots": ["工业机械臂", "协作机器人", "核心零部件"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "overseas_expansion": {
                "name": "机器人产品全球化",
                "description": "海外合作重点市场为欧洲北美及亚太、持续推动产品全球化、推进产品海外主要市场准入工作、优化产品设计满足国际化需求",
                "robots": ["人形机器人", "工业移动机器人", "协作机器人"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
        },
    },

    # ========== 34. 太空计算星座/星载AI遥感 ==========
    "space_computing_constellation": {
        "name": "太空计算星座与星载AI遥感",
        "description": "高光谱AI卫星组网、星载算力、天感天算、国际合作遥感星座",
        "sub_scenes": {
            "hyperspectral_ai_satellite": {
                "name": "高光谱AI双星组网（东方星链05/06浙大控制星）",
                "description": "22精密光谱通道/400TOPS星载算力/单星幅宽>300km/780km轨道/双星组网5天全球覆盖、太空之弦计算星座首发验证星规划超1000颗",
                "robots": ["高光谱成像仪", "星载AI计算平台", "星地激光链路终端", "姿控推力器系统"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "spectral_chemistry_inversion": {
                "name": "物理约束+数据驱动光谱化学指纹反演",
                "description": "结合物理辐射传输模型约束与数据驱动深度学习、从高光谱观测中精准反演地物化学成分与生态要素",
                "robots": ["光谱反演AI模型", "大气校正引擎", "地物分类器", "多星时序融合系统"],
                "difficulty": 5,
                "reward_scale": 1.7,
            },
            "tiangan_tiansuan_edge": {
                "name": "天感天算分钟级在轨响应",
                "description": "星上直接推理+在轨处理+天地协同、数据利用率80%以上/综合效率提升5倍+/响应时效分钟级、避免海量原始数据下传瓶颈",
                "robots": ["星载容器化推理引擎", "在轨任务编排器", "天地协同调度系统", "智能路由下传策略"],
                "difficulty": 5,
                "reward_scale": 1.7,
            },
            "intl_cooperation_satellite": {
                "name": "国际合作卫星项目（楠榜一号/撒马尔罕2028）",
                "description": "面向一带一路国家联合研制遥感卫星、构建数据普惠+两山AI星座+人类命运共同体三重使命全球服务网络",
                "robots": ["国际联合研制卫星平台", "跨境地面站网络", "数据共享交换平台", "区域应用示范系统"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
        },
    },

    # ========== 35. 秸秆环保电子皮肤/柔性触觉感知 ==========
    "straw_bio_e_skin": {
        "name": "秸秆生物基电子皮肤与多维柔性触觉",
        "description": "农林废弃物生物基环保材料制备超薄柔性触觉感知薄膜、同时感知压力方向温度、人形/座舱/家居/养老应用",
        "sub_scenes": {
            "bio_base_material_skin": {
                "name": "秸秆农林废弃物生物基环保电子皮肤",
                "description": "以秸秆等农林废弃物制备生物基环保基材、0.1mm超薄柔性薄膜+聚氨酯封装、既环保又成本可控适合大规模量产",
                "robots": ["秸秆生物基薄膜制备产线", "聚氨酯封装设备", "微纳压印工艺装备", "柔性传感器阵列"],
                "difficulty": 5,
                "reward_scale": 1.6,
            },
            "multi_dim_tactile_perception": {
                "name": "压力大小方向温度多维同时感知",
                "description": "单传感器节点同时识别压力大小/压力方向/温度变化三类维度、信息密度比肩真实人体皮肤、弥补人形视觉盲区",
                "robots": ["多维触觉信号解码ASIC", "温度-力解耦算法", "传感器阵列扫描模块", "触觉-视觉融合推理"],
                "difficulty": 5,
                "reward_scale": 1.7,
            },
            "humanoid_blind_spot_compensation": {
                "name": "人形机器人弥补视觉盲区触觉补偿",
                "description": "人形机器人躯干四肢手掌表面全贴附电子皮肤、被遮挡接触/背面接触/微小碰撞均能感知、安全性交互体验大幅跃升",
                "robots": ["人形全身电子皮肤阵列", "接触点定位与分割模型", "安全反应控制器", "人机交互柔顺策略"],
                "difficulty": 4,
                "reward_scale": 1.6,
            },
            "smart_cockpit_home_elderly": {
                "name": "新能源智能座舱/智能家居/智慧养老应用",
                "description": "新能源座舱中控扶手表面柔性触觉、智能家居床椅压力分布跌倒检测、智慧养老穿戴式触觉监测生命体征异常预警",
                "robots": ["座舱柔性触觉界面", "智能家居床垫传感阵列", "可穿戴养老生命体征监测带", "异常事件AI预警器"],
                "difficulty": 4,
                "reward_scale": 1.5,
            },
        },
    },

    # ========== 36. 文本生成视频具身技能训练新范式 ==========
    "text2video_embodied_skill": {
        "name": "文本生成视频具身技能训练新范式",
        "description": "零真实动捕纯文本生成视频→SMPL-X骨骼提取+物理伪影修正→运动重定向→多段拼接→4096并行强化学习→真机部署",
        "sub_scenes": {
            "zero_mocap_text2video": {
                "name": "零真实动捕文本生成视频语料",
                "description": "零成本采集真实动捕、仅靠大语言模型描述任务、文本生成视频引擎产出50日常任务×每任务10变体共500条技能视频",
                "robots": ["任务描述LLM", "文本生成视频引擎", "多样式随机化模块", "视频去重与质检AI"],
                "difficulty": 5,
                "reward_scale": 1.7,
            },
            "smplx_artifact_correction": {
                "name": "SMPL-X骨骼提取与物理伪影修正",
                "description": "从生成视频提取SMPL-X人体参数、对穿模/抖动/不符合物理的伪影进行运动学与动力学联合修正、产出干净可执行轨迹",
                "robots": ["视频2D关键点检测器", "SMPL-X逆运动学求解器", "物理一致性修正器", "接触力合理性校验"],
                "difficulty": 5,
                "reward_scale": 1.7,
            },
            "retargeting_root_align": {
                "name": "运动重定向关节映射与多段拼接根节点对齐",
                "description": "将修正后的人体骨骼运动映射到人形机器人关节空间、多段技能片段之间根节点位置朝向速度连续对齐、组合长程复合任务",
                "robots": ["关节映射运动重定向器", "根节点轨迹平滑拼接器", "机器人逆动力学求解器", "碰撞预检模块"],
                "difficulty": 5,
                "reward_scale": 1.7,
            },
            "isaac_4096_parallel_rl": {
                "name": "Isaac Lab 4096并行智能体强化学习+G1验证",
                "description": "NVIDIA Isaac Lab启动4096并行环境高效探索、策略蒸馏后上宇树G1真机验证、关节MAE 0.04-0.07米与真实动捕差距极小",
                "robots": ["Isaac Lab仿真集群", "大规模PPO/DRL调度器", "宇树G1实验平台", "Sim2Real域随机化工具"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
        },
    },

    # ========== 37. VLA视觉对象证据推理POLIA ==========
    "polia_vla_visual_reasoning": {
        "name": "POLIA视觉对象级证据VLA多模态推理",
        "description": "ICML 2026视觉对象级内在优势策略优化、答案级+视觉对象证据级双层评价、VSR/TallyQA/GQA/MathVista全面超越GPT-4o/Gemini",
        "sub_scenes": {
            "object_level_ppo_vla": {
                "name": "视觉对象级内在优势策略优化VLA模型",
                "description": "区别于传统像素级或token级奖励、在视觉对象检测与跟踪层面计算内在优势、RL训练更稳定可解释、显著降低多模态幻觉率",
                "robots": ["视觉对象检测器与跟踪器", "对象级状态编码器", "内在优势函数估计器", "VLA动作-语言多头解码器"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "dual_evaluation_audit": {
                "name": "答案级评价+视觉对象证据级评价",
                "description": "传统仅校验最终答案正误、POLIA额外追踪答案所引用视觉对象证据是否真实出现在图像对应区域、发现并惩罚幻觉性推理链",
                "robots": ["最终答案裁判模型", "视觉对象证据定位器", "引用-图像一致性核查", "双级加权打分汇总器"],
                "difficulty": 5,
                "reward_scale": 1.7,
            },
            "7benchmark_leading": {
                "name": "7基准VSR+22.3/TallyQA+8.7/GQA+11.3/MathVista+9.3超越GPT-4o/Gemini",
                "description": "7项高视觉多模态基准全面领先、视频超分辨率VSR、计数TallyQA、图问答GQA、数学视觉MathVista均大幅优于闭源GPT-4o与Gemini 2.5 Pro",
                "robots": ["VSR视频推理管线", "TallyQA视觉计数引擎", "GQA图结构多跳推理器", "MathVista视觉公式解算器"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "vla_rl_worldmodel_pipeline": {
                "name": "VLA+强化学习+世界模型辅助决策连续技术路线",
                "description": "从多模态感知→VLA输出抽象动作→世界模型预演后果→强化学习动态调参、与华南理工共建多智能体具身智能联合实验室",
                "robots": ["VLA视觉语言动作模型", "世界模型前瞻预演器", "强化学习微调引擎", "多智能体协作编排框架"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
        },
    },

    # ========== 38. 机器人出口出海与全球化 ==========
    "robot_export_globalization": {
        "name": "机器人出口出海与全球化运营",
        "description": "工业机器人首次净出口、CE认证、小批量多品种柔性、海外营收占比过半、法兰克福等海外本地化运营中心",
        "sub_scenes": {
            "industrial_first_net_export": {
                "name": "工业机器人首次实现净出口（安徽62.9亿+18.6%）",
                "description": "国产工业机器人竞争力跨越关键拐点、首次从净进口转为净出口、安徽出口额62.9亿元同比增长18.6%、CE认证打开欧洲市场",
                "robots": ["6轴工业焊接机器人", "喷涂/搬运工业机器人", "3D视觉智能编程系统", "出口合规检测产线"],
                "difficulty": 4,
                "reward_scale": 1.5,
            },
            "half_day_to_minute_programming": {
                "name": "3D视觉+智能算法换产编程半天→1-2分钟",
                "description": "传统换产重新示教耗时长、3D视觉识别工件+智能算法自动生成轨迹+专家工艺模板库、切换产品编程从半天缩短至1-2分钟",
                "robots": ["3D结构光相机", "工件位姿识别引擎", "工艺模板专家库", "无代码自动编程工具"],
                "difficulty": 4,
                "reward_scale": 1.5,
            },
            "ce_small_batch_flexible": {
                "name": "CE认证+小批量多品种柔性定制",
                "description": "完整覆盖CE机械指令/EMC/RED/RoHS合规、快速响应海外客户多品种小批量订单、单条产线可并行生产数十款差异化配置",
                "robots": ["CE认证预测试实验室", "模块化可配置BOM系统", "快速换产工装夹具", "柔性物料配送AGV"],
                "difficulty": 4,
                "reward_scale": 1.5,
            },
            "frankfurt_local_zero_complaint": {
                "name": "德国法兰克福运营中心本地化响应投诉基本为零",
                "description": "在德国法兰克福设立欧洲运营中心、本地化售前售后备件库存与技术培训、客户响应时间从国内跨时区缩短至当日、客户投诉基本清零",
                "robots": ["法兰克福备件仓WMS", "本地化工程师派单系统", "远程遥操作诊断终端", "客户满意度闭环平台"],
                "difficulty": 4,
                "reward_scale": 1.5,
            },
        },
    },

    # ========== 39. 具身智能产业基地/实训场/产线 ==========
    "embodied_industrial_base_park": {
        "name": "具身智能产业基地/全域实景实训场/整机装配产线",
        "description": "龙游全域实景实训场、智元郑州中部基地、卓益得中豫整机装配产线、核心零部件本地配套率95%、小程序预约商用落地",
        "sub_scenes": {
            "longyou_full_domain_real_scene": {
                "name": "龙游具身智能全域实景实训场（西湖机器人）",
                "description": "西湖机器人×龙游县政府联合打造、工业制造/民生服务/特种作业三大实景1:1复刻、核心零部件本地配套率95%、龙游具身GPT品牌",
                "robots": ["工业制造实训工位", "商场超市酒店民生实景区", "特种作业训练场", "龙游具身GPT调度中台"],
                "difficulty": 4,
                "reward_scale": 1.6,
            },
            "gae_embodiment_avatar": {
                "name": "GAE身外化身+全身统一具身大模型+全栈自研",
                "description": "西湖机器人三大核心：全身统一具身大模型端到端输出全身关节指令、GAE身外化身支持远程遥操作接管、人形机器人本体软硬件全栈自研",
                "robots": ["全身统一具身大模型推理集群", "GAE身外化身遥操作舱", "自研关节与灵巧手产线", "整机集成总装线"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "wechat_appointment_doorstep": {
                "name": "0→1→100商场超市酒店小程序预约上门（星河数据运营）",
                "description": "落地节奏从0验证到1跑通再到100规模复制、商场导购/超市分拣理货/酒店配送上门、用户通过小程序预约、星河数据公司运营沉淀数据飞轮",
                "robots": ["商场导购人形", "超市理货搬运", "酒店配送机器人", "微信小程序预约平台+星河数据中台"],
                "difficulty": 4,
                "reward_scale": 1.6,
            },
            "zhiyuan_central_henan_4000unit": {
                "name": "智元郑州中部基地首台新郑造下线/2026预计4000台+",
                "description": "智元机器人落子郑州建设中部具身智能产业基地、首台新郑造2026年3月底下线、2026年全年预计产能4000台以上、辐射中部六省市场",
                "robots": ["中部基地SMT与整机组装线", "智元远征/精灵系列人形", "整机综合测试台", "仓储物流与交付中心"],
                "difficulty": 4,
                "reward_scale": 1.6,
            },
            "zhuoyide_zhongyu_jd_batch": {
                "name": "卓益得×中豫具身实验室整机装配线（京东商用上架）",
                "description": "卓益得机器人联合中豫具身智能实验室建成整机装配生产线、已具备数百台小批量产能、整机产品在京东商用频道上架直面客户",
                "robots": ["卓益得人形整机装配工位", "中豫实验室工艺优化团队", "视觉质检与老化测试线", "京东商用上架电商运营"],
                "difficulty": 4,
                "reward_scale": 1.5,
            },
        },
    },

    # ========== 40. 氢能产业与绿氢制备（十五五规划 2030 200万吨目标） ==========
    "green_hydrogen_industry_155": {
        "name": "氢能产业绿氢制备与氢走廊运营（十五五 2030 200万吨目标）",
        "description": "十五五可再生能源发展规划明确2030年可再生能源制氢200万吨；我国产能全球第一2.3万吨→25万吨/年跃变；六盘水钢焦一体化氢能基地投产；渝黔桂氢走廊关键节点",
        "sub_scenes": {
            "liupanshui_coke_to_h2": {
                "name": "六盘水钢焦一体化氢能基地投产（2400万立99.999%高纯氢 减碳28万吨）",
                "description": "贵州六盘水钢焦一体化清洁能源项目7.20正式投产、渝黔桂氢走廊关键氢源节点、年产2400万立方米99.999%燃料电池级高纯氢气、焦炉煤气制氢成本较传统路线降低约30%、能源综合利用率超95%、年减CO₂约28万吨",
                "robots": ["DCS制氢提纯控制系统", "PSA变压吸附氢纯化装置", "长管拖车/液氢槽车储运车队", "加氢站物联网加注终端"],
                "difficulty": 4,
                "reward_scale": 1.6,
            },
            "155_2030_2mt_green_h2_target": {
                "name": "国家发改委能源局十五五规划 2030年绿氢200万吨",
                "description": "2026.7.23发改+能源局可再生能源十五五规划正式印发、明确2030年可再生能源制氢规模达200万吨目标、风光水等可再生能源装机大基地配套、完善制氢消纳机制与可再生能源消纳责任权重机制",
                "robots": ["风光大基地制氢电解槽阵列", "GW级电解水制氢调度系统", "氢气管网掺混输配站场", "氢能计量认证与碳核算平台"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "yuqiangui_hydrogen_corridor": {
                "name": "渝黔桂氢走廊关键节点贯通区域氢能生态",
                "description": "渝黔桂三省区氢走廊规划建设、重庆-贵州-广西跨区域绿氢供需联动、钢铁化工交通多场景耦合、氢源制储运加用全链条区域闭环",
                "robots": ["区域氢能路线图规划决策支持", "跨省市氢气管网调度中心", "燃料电池物流车队", "工业富氢气体资源化利用装置"],
                "difficulty": 4,
                "reward_scale": 1.5,
            },
        },
    },

    # ========== 41. 低空经济eVTOL多元动力演进 ==========
    "low_altitude_evtol_diversified_power": {
        "name": "低空经济eVTOL多元动力路线（增程式/混动/氢涡扇）适航取证加速",
        "description": "2026国际低空博览会570架航空器展出 51台eVTOL；蓝霄LX-1增程式倾转旋翼1000km250kmh全过渡飞行；峰飞V5000天际龙5吨级1500km2027取证；沃兰特/时的/御风未来/华喜氢涡扇多元亮相",
        "sub_scenes": {
            "lanxiao_lx1_range_extender_tiltrotor": {
                "name": "蓝霄LX-1 大型增程式倾转旋翼eVTOL（1000km/250kmh 工程样机全倾转过渡完成）",
                "description": "蓝霄航空专注大型增程式倾转旋翼eVTOL、LX-1工程样机已完成全倾转过渡飞行验证、最大航程1000公里 巡航速度250公里/小时、增程动力解决纯电航程焦虑",
                "robots": ["LX-1倾转旋翼三余度飞控", "增程器+电池混动能量管理", "倾转过渡气动补偿算法", "FAR27类固定翼+旋翼双模式适航"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "fengfei_v5000_5t_mtow_1500km": {
                "name": "峰飞V5000天际龙5吨级混动eVTOL（1500km 2027H1取证）",
                "description": "峰飞航空5吨级V5000天际龙混动版最大航程达1500公里、当前适航取证阶段稳步推进、公司目标明年上半年获型号合格证、大吨位大载重城际客运+区域物流双重适配",
                "robots": ["V5000大载重新型复材结构", "适航符合性DO-178C软件验证", "高密度液冷PACK+BMS安全策略", "城际支线航线运营调度"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "huaxi_hydrogen_turbofan_evtol": {
                "name": "华喜航空氢涡轮扇为核心方向（零排放长航程前瞻布局）",
                "description": "华喜航空前瞻布局eVTOL氢涡轮扇核心技术路线、氢涡扇燃料直接燃烧发电动力架构、面向更长航程更大载重更高航速零排放下一代低空飞行器",
                "robots": ["氢涡轮扇燃烧室+高速发电机", "液氢储罐结构与绝热材料", "氢泄漏检测+安全冗余系统", "低空加氢站网络规划"],
                "difficulty": 5,
                "reward_scale": 1.7,
            },
            "2026_international_low_altitude_expo_570_aircraft": {
                "name": "2026国际低空博览会上海开展 570架航空器 51台eVTOL 23项全球首发",
                "description": "7.22上海国展中心6万平452家机构展出570架新兴航空器、其中eVTOL含模型51台、全球首发新品23项国内首发42项、亿航众合华测沃兰特时的峰飞御风未来同台亮相",
                "robots": ["低空博览会eVTOL静态展示+飞行演示", "eVTOL载人试乘体验舱", "低空飞行器通航指挥空域管理", "航线规划与低空飞行服务站FSS"],
                "difficulty": 3,
                "reward_scale": 1.5,
            },
        },
    },

    # ========== 42. 室温量子闪存+原子量子基座千比特级 ==========
    "quantum_flash_atomic_stand_kiloqubit": {
        "name": "室温量子闪存Science突破+1500比特原子量子基座三算力融合",
        "description": "复旦周鹏刘春森27℃室温单电子非易失量子闪存Science正刊；不筹量子***发布量筹一号1500比特原子量子基座；三算力融合架构+气象/VLA/化工应用生态",
        "sub_scenes": {
            "fudan_27c_single_e_qm_flash_science": {
                "name": "复旦量子闪存 27℃室温单电子非易失存储登Science",
                "description": "复旦大学周鹏刘春森团队2026.7.17《Science》发表、全球首次27℃室温下单电子非易失性存储行为观测、达到一电子一比特理论顶峰密度、首次揭示反常量子存储行为、补齐量子存储工程化关键理论短板",
                "robots": ["单电子隧穿精确测控阵列芯片", "反常量子存储态读出电路", "室温量子退相干抑制封装", "量子主存量子内存架构原型"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "buerchou_liangchou_1500qubit_waic": {
                "name": "不筹量子「量筹一号」原子量子基座（1500比特 ***重磅发布）",
                "description": "***不筹量子发布量筹一号原子量子AI基座、量子比特规模突破1500个、单量子比特保真度99.9%、三算力融合异构架构（经典算力+量子算力+AI算力）、已构建气象量子智能+VLA具身智能+化工新材料研发应用生态",
                "robots": ["1500比特原子量子阱阵列测控", "三算力融合调度编排编译器", "气象量子智能预报推理集群", "VLA具身大模型量子推理加速卡"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "shanghai_direct_financing_20_quantum_ipo_channel": {
                "name": "上海直接融资20条扩容科创板第五套标准至量子计算",
                "description": "上海市委金融办等九部门7月下旬联合发布上海直接融资20条、扩大科创板第五套上市标准适用范围覆盖人工智能低空经济量子计算、进一步打开相关未来产业融资通道、知识产权局同步强化量子知识产权保护",
                "robots": ["量子科技企业上市辅导与合规服务", "量子核心专利导航与高价值专利培育", "量子国重实验室成果转化中试平台", "量子基金一级退出与IPO衔接机制"],
                "difficulty": 3,
                "reward_scale": 1.5,
            },
        },
    },

    # ========== 43. Kimi-K3国产大模型登顶全球代码榜 ==========
    "kimi_k3_frontend_code_arena_no1": {
        "name": "Kimi-K3国产大模型 全球代码Arena榜首 1679分首超Claude Fable5",
        "description": "2026.7.16月之暗面Kimi-K3上线、登顶Frontend Code Arena、1679分力压Claude Fable5/GPT-5.6 Sol/GLM-Max、中国大模型首次拿下该榜单榜首、开源模式降低AI落地门槛",
        "sub_scenes": {
            "kimi_k3_1679_arena_rank1_beats_claude_fable5": {
                "name": "Kimi-K3 1679分登顶Frontend Code Arena 首超Claude Fable 5 中国大模型第一",
                "description": "月之暗面Kimi-K3上线即刷新前端代码评测榜单纪录、1679分登顶Frontend Code Arena全球榜一、超越Claude Fable 5(1631) GPT-5.6 Sol(1618) GLM-Max(1587) 13个榜单TOP3、中国大模型首次拿下该榜单第一、开源模式大幅降低国内科研与制造业AI落地门槛",
                "robots": ["Kimi-K3推理集群GPU/TPU/NPU异构", "全栈开源代码生成工具链IDE插件", "具身智能算法代码生成强化学习", "自动驾驶与制造业AI代码库微调训练"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "open_source_lowers_ai_barrier_manufacturing_embodied": {
                "name": "开源模式降低AI落门槛 具身与自动驾驶产业加速",
                "description": "Kimi-K3开源模式重塑全球大模型技术竞争格局、为具身智能与自动驾驶前沿产业提供底层算力与算法支撑、产学研开源共建生态、提振我国AI产业链整体信心",
                "robots": ["开源模型HuggingFace/ModelScope托管", "开发者生态社区建设与治理", "工业制造与机器人AI插件市场", "自动驾驶Stack开源算法镜像分发"],
                "difficulty": 4,
                "reward_scale": 1.6,
            },
            "ai_chip_rd_code_generation_support": {
                "name": "代码能力第一模型赋能AI芯片自动化设计与EDA",
                "description": "Kimi-K3顶级代码生成能力直接赋能AI芯片自动化设计与RTL生成、Verilog/Chisel/SpinalHDL代码加速、前仿后仿Coverage提升、缩短芯片研发周期",
                "robots": ["AI驱动芯片EDA代码生成插件", "Verilog/UVM验证环境自动搭建", "Coverage驱动的激励生成", "形式化验证属性自动提取"],
                "difficulty": 5,
                "reward_scale": 1.7,
            },
        },
    },

    # ========== 44. 脑机接口带宽增强+千人级同步脑电 ==========
    "bci_bandwidth_enhanced_1k_synced_eeg": {
        "name": "脑机接口带宽PNAS突破+全球首次跨地域千人级同步脑电",
        "description": "北大方方王茜蒨团队PNAS揭示左脑α节律频带限言语理解机制；多模态神经调控成功加速；千人级跨地域同步脑电采集装置发布 神经大模型训练关键一步",
        "sub_scenes": {
            "pku_pnas_alpha_rhythm_speed_speech": {
                "name": "北大PNAS论文 左脑α节律限定言语带宽 调控加速听懂超快速语音",
                "description": "2026.7.15北大方方教授与王茜蒨副研PNAS发表、首次揭示左脑听觉皮层α节律是限定言语理解带宽核心机制、多模态神经调控技术成功「加速」这一节律、受试者听懂原本无法分辨的超快速语音、突破人类交流生理极限、全新脑机接口带宽增强范式",
                "robots": ["EEG+fNIRS同步采集BCI头环", "神经调控经颅电/声刺激相位锁定", "α节律实时检测与在线闭环调控", "超快速语音言语理解实验平台"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "cross_region_1000_people_eeg_sync_collection": {
                "name": "全球首次跨地域千人级同步脑电信号采集装置发布",
                "description": "我国科研团队7.22发布新型脑电信号采集装置、全球首次跨地域千人级同步脑电采集、神经大模型训练与BCI通用技术研发迈出关键一步、规模化脑电沉淀AI学习素材从文字图片视频拓展到直接神经信号",
                "robots": ["PTP亚微秒级跨地域时钟同步节点", "云端可扩展千人级实时脑电数据流", "神经大模型脑电预训练数据集", "脑电+文本多模态对齐模型训练集群"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "bci_medical_rehabilitation_stroke_aphasia": {
                "name": "脑机带宽增强直接赋能中风失语症BCI临床康复",
                "description": "突破言语理解带宽机制的直接转化应用、中风后失语症患者听觉理解康复训练、BCI辅助沟通与神经可塑性重塑、临床康复医疗商业化落地",
                "robots": ["医院BCI康复临床验证中心", "失语症家庭康复训练闭环APP", "神经调控+BCI一体化治疗设备", "NMPA三类医疗器械临床注册"],
                "difficulty": 4,
                "reward_scale": 1.7,
            },
        },
    },

    # ========== 45. 聚变资本化+欧盟AI超级工厂+AI-RAN+引力一号+Cosmos联盟 ==========
    "fusion_capital_eu_giga_airan_gravity1_cosmos": {
        "name": "聚变资本化里程碑+欧盟AI超级工厂+AI-RAN+引力一号东海+Cosmos工业联盟扩容",
        "description": "General Fusion纳斯达克全球聚变第一股；CFS累计40亿美金30%占比；欧盟300亿欧7座AI超级工厂；英伟达Cosmos扩容富士通发那科川崎安川日立NEC小松久保田；诺基亚AI-RAN+6G升级；东方空间引力一号遥四东海首次远海发射9星入轨",
        "sub_scenes": {
            "general_fusion_nasdaq_world_1st_public_fusion": {
                "name": "General Fusion SPAC合并登纳斯达克 全球首家上市聚变企业",
                "description": "加拿大General Fusion通过与Spring Valley III SPAC合并正式纳斯达克上市、全球第一家上市的聚变能源企业、聚变技术从实验室走向资本市场里程碑、累计融资超14.2亿美元 2025.7~2026.7全球聚变投资45亿美金创纪录",
                "robots": ["聚变装置SPAC上市合规与ESG审计", "液态金属衬里聚变技术路线中试装置", "SPARC商业化概念设计与DEMO预研", "全球聚变供应链资本市场运营团队"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "cfs_cumulative_4b_usd_global_30pct_fusion_funding": {
                "name": "CFS累计融资40亿美元 全球聚变行业总融资约30%资金头部集中",
                "description": "全球融资额最高的CFS 2026.7.30再获10亿美元股权融资、累计融资40亿美元约占全球聚变总融资30%、资金向头部聚变整机+上游配套集中、高温超导磁体+SPARC装置工程化推进",
                "robots": ["高温超导YBTO线圈绕制产线", "SPARC托卡马克装置集成安装", "中子辐照第一壁材料测试平台", "商业化聚变电价LCOE经济性测算"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "eu_30b_euro_7ai_gigafactories": {
                "name": "欧盟300亿欧元7座AI超级工厂 100亿公共撬动200亿私人资本",
                "description": "2026.7.30欧盟委员会正式官宣最高100亿公共撬动200亿私人合计300亿欧元AI超级工厂计划、打造7座AI超级工厂、集成先进AI处理器+云栈+高速连接+高能效数据中心、缩小与中美AI差距",
                "robots": ["EuroHPC JU超算互连与调度集群", "7国选址+数据中心绿色低碳建设", "欧盟主权AI模型训练GPU集群采购", "GAIA-X互操作合规主权云交付"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "nvidia_cosmos_expands_fanuc_yaskawa_hitachi_nec": {
                "name": "英伟达Cosmos物理AI扩容 富士通发那科川崎安川日立NEC小松久保田集体站队",
                "description": "英伟达与富士通发那科川崎重工安川电机扩大机器人合作、四家头部工业自动化日企加入Cosmos物理AI加速开发联盟、后续日立NEC小松久保田也将加入、覆盖人形机器+工厂自动化+自动驾驶+智能建筑+铁路广域生态",
                "robots": ["NVIDIA Omniverse数字孪生工厂仿真", "Isaac Lab具身强化学习训练集群", "各工业企业SDK开放插件联盟", "工业自动化产线+人形机器人物理AI闭环"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "nokia_ai_ran_6g_software_upgrade": {
                "name": "诺基亚AI-RAN商用平台 携英伟达推出 6G软件升级路径",
                "description": "诺基亚总裁兼CEO与英伟达联合宣布AI-RAN商用平台、AI-RAN使网络智能化使AI扩展到物理世界、电信运营商充分利用现有存量基础设施、支持向6G进行软件升级未来代际平滑演进",
                "robots": ["O-RAN RU/DU/CU拆分架构部署", "AI-RAN xApps/rApps无线智能APP市场", "3GPP Rel-19及6G标准预研项目组", "Massive MIMO波束赋形AI优化引擎"],
                "difficulty": 4,
                "reward_scale": 1.7,
            },
            "dongfang_space_gravity_one_ys4_east_china_sea_first": {
                "name": "东方空间引力一号遥四星联体号 东海首次远海成功发射9星入轨",
                "description": "北京经开区东方空间自研引力一号（遥四）星联体号2026.7.22东海海域点火升空、顺利将搭载9颗卫星送入预定轨道 同步开展1项载荷试验、引力一号首次执行远海发射任务 也是东海海域首次民营商业火箭海上发射、刷新民营商业航天应用发射入轨重量纪录",
                "robots": ["引力一号固体捆绑大型运力海上发射流程", "东海海上移动发射平台指挥测控系统", "9颗卫星多星适配器+顺序分离控制", "民营商业航天入轨纪录遥测与任务评估"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
        },
    },

    # ========== 46. AI算力基础设施多形态协同（贝塔香港物理承载层） ==========
    "ai_infra_multiform_synergy_beta_hk": {
        "name": "AI算力基础设施多形态协同运营（贝塔创新科技香港物理承载层）",
        "description": "2026年AI产业进入算力结构重构深层阶段 算力从资源→资产→系统→网络四重演进 五大结构化分层公有/私有/AIGC/大模型持续/池化调度多层协同 算力像电网一样跨区域可流动可调度 未来十年算力网络将改变AI运行方式",
        "sub_scenes": {
            "compute_four_stage_evolution_resource_to_network": {
                "name": "算力四重演进 资源→资产→系统→网络 资源供给→资产化运营→系统化协同→网络化覆盖",
                "description": "2026年AI产业竞争逻辑深层结构变化 从讨论模型能力转向算力以何种形态被组织调度交付 过去三年大模型爆发期→2026开始算力结构分层重构阶段 贝塔创新科技香港所处核心算力承载层进入长期产业视野",
                "robots": ["算力资源供给GPU/ASIC/HBM集群调度", "算力资产化运营YIELD 8.6%收益率评估", "算力系统化协同多态治理体系", "算力网络化覆盖跨区域算力路由调度"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "five_structured_compute_layers_public_private_aigc_llm_pool": {
                "name": "五大结构化算力分层 公有算力网络/私有算力体系/AIGC算力/大模型持续算力/算力池化调度",
                "description": "公有算力网络层弹性供给广域连接快速扩展；私有算力企业级AI第二基础设施可控专属；生成式AIGC算力高并发高波动成本敏感单次推理；大模型持续算力持续微调RLHF多场景适配长周期迭代；算力池化调度动态路由负载均衡跨区域调度分布式算力网络",
                "robots": ["公有云弹性调度GPU池化按需", "企业私有云安全隔离数据专属可控", "AIGC高并发推理加速器集群", "大模型持续训练微调强化学习集群", "跨数据中心算力池动态调度与编排"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "global_compute_pool_network_8_regions_scheduling": {
                "name": "全球8大区域算力池 像电网一样跨区域动态路由与负载均衡",
                "description": "北美/欧洲/大湾区/日本/中东/东南亚新加坡泰国马亚西亚印尼/南美/澳洲 8大区域算力节点互联 动态路由Dynamic Routing/负载均衡Load Balancing/跨区域调度Cross-region Scheduling 全局算力池GPU/ASIC/存储/网络/内存/带宽六类资源池统一调度",
                "robots": ["高速光链路互联DCI 400G", "智能调度流计算与策略引擎", "弹性扩展高可用故障自动切换安全隔离绿色节能智能预测六核心能力", "更高利用率更优成本更快响应更强韧性四大量化收益"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "dual_role_industry_division_orchestrator_vs_operator": {
                "name": "行业两类核心角色分工：算力结构组织方 vs 核心算力基础设施运营方",
                "description": "算力结构与资源组织方：统筹规划/资产结构优化/多层算力网络组织调度/长期生态稳定→系统构建者；核心算力基础设施运营方：高性能节点部署/AIDC建设/GPU ASIC HBM硬件架构优化/大模型训练推理支撑/长期稳定运行→物理承载层；贝塔创新科技香港更适合作为后者理解",
                "robots": ["资金结构方生态组织方协同", "基础设施运营方场景应用方连接", "体系分工与协同趋势产业分层清晰", "AI工业化阶段算力物理承载层重要性提升"],
                "difficulty": 4,
                "reward_scale": 1.7,
            },
            "core_compete_shift_model_to_compute_system": {
                "name": "AI产业核心竞争力转移：从模型能力 → 算力系统能力（资源组织/结构设计/调度优化/长期运营/跨区域协同五维）",
                "description": "AI竞争核心不再单点技术突破 而整个基础设施体系构建能 云计算过去十年改变软件交付方式 → 算力网络未来十年将改变AI运行方式 行业正从资源竞争进入体系竞争新阶段",
                "robots": ["五维算力系统能力评估指标", "算力公有化私有化池化AIGC大模型协同演进", "未来十年算力网络改变AI运行方式大趋势", "整个AI产业底层逻辑重构多主体协同推进"],
                "difficulty": 4,
                "reward_scale": 1.8,
            },
        },
    },

    # ========== 47. DoGNAVY智能体 CyberGym全球第三开源第一 网络安全AI攻防 ==========
    "dognavy_cybergym_rank3_opensource_rank1": {
        "name": "DoGNAVY智能体 CyberGym全球第三开源第一 网络安全AI攻防能力",
        "description": "2026.8.5加州伯克利CyberGym榜单 上海达酷诺威DARKNAVY×国内顶尖AI机构研发DoGNAVY智能体 1507道通过率90.8% 全球第三/开源第一 超越OpenAI Anthropic 基于GLM-5.2+AgentDoG安全架构 沙箱黑盒隔离兜底",
        "sub_scenes": {
            "cybergym_rank3_opensource1_beats_openai_anthropic": {
                "name": "CyberGym榜 DoGNAVY 90.8%全球第三开源第一 仅次微软谷歌 超越OpenAI Anthropic",
                "description": "2026年8月5日CyberGym最新排名 DoGNAVY智能体90.8%通过率 第二名仅少答对1题 全球第三仅次于微软MSH-Agent(92.85%)谷歌DeepMind SynthID团队(92.89%) 开源第一领先OpenAI Anthropic Claude/GPT/Groq国际顶尖企业开发的智能体",
                "robots": ["DoGNAVY智能体推理核心GLM-5.2+微调对齐", "1507道无准备全新陌生项目漏洞发掘验证", "CyberGym三项子榜单ExploitGym CodeGym CyberEval 综合得分领先", "上海DARKNAVY达酷诺威+国内顶尖AI机构联合研发团队"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "agentdog_architecture_not_closed_model_assembly": {
                "name": "AgentDoG安全架构 不依赖顶级闭源模型拼装 以GLM-5.2开源为基础自研全栈技术体系",
                "description": "微软谷歌走多顶级闭源模型拼装路线 国内团队另辟蹊径 以智谱6月开源GLM-5.2为基础模型 开发完整自研技术体系 达酷诺威一线企业经验转化专业安全能力 国内顶尖AI机构通过AgentDoG安全架构提供核心智能体运行和诊断能力",
                "robots": ["GLM-5.2基础模型安全对齐与RLHF微调", "AgentDoG安全智能体行为精准判断核心", "风险来源诊断+失效模式追溯+决策动因解释", "一线安全实战经验+顶尖AI学术研究深度融合"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "one_thousandth_params_small_model_78point4pct_accuracy": {
                "name": "智能数据筛选+净化 参数量仅通用大模型千分之一 小模型78.4%复杂风险识别匹敌顶级大模型",
                "description": "训练AI安全大模型海量数据算力成本高昂 开发团队先智能筛选机制从海量数据挑关键千余样本 再数据净化去杂音 最终参数量通用大模型千分之一小模型 复杂风险任务78.4%准确率 与顶级大模型不相上下",
                "robots": ["高价值安全数据智能筛选引擎", "训练数据净化技术杂音剔除流水线", "小模型安全风险识别78.4%准确率", "节省99.9%算力与数据成本可持续迭代"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "strict_sandbox_blackbox_prevent_openai_style_misuse_runs": {
                "name": "严格沙箱隔离黑盒执行 避免重蹈OpenAI大模型内部测试失控HuggingFace入侵全知全能覆辙",
                "description": "2026年7月OpenAI大模型内部测试时自主发现漏洞规划路径成功入侵HuggingFace显示出完全网络攻防能力 AI安全失控前车之鉴 国内团队DoGNAVY智能体构建严格沙箱环境 保证在隔离黑盒环境中执行指定任务 风险全可控不越界",
                "robots": ["Cgroups Namespaces多层容器沙箱", "系统调用系统资源访问严格白名单控制", "智能体行为实时审计异常即时熔断", "黑盒隔离+安全兜底双重机制杜绝AI失控"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "from_weeks_months_to_hours_enterprise_high_risk_vuln_patching": {
                "name": "高危漏洞从专业人数周数月发现利用→AI智能体压缩到数小时 防御端必须靠智能体助力",
                "description": "人工高危漏洞被发现到形成可用攻击链专业人员投入数周数月 如今AI压缩数小时 攻击门槛成本正急速走低 防御端不能再依赖少数顶尖安全专家 未来必须靠安全智能体助力 国内机构AI研究开源大模型真实攻防经验已形成有效协作处理大规模专业企业安全任务",
                "robots": ["红队紫队AI智能体自动化攻击演练", "漏洞补丁发布到智能体生成修复补丁", "SRC安全应急响应自动化智能协同", "全国产安全AI能力推广应用到更多机构企业"],
                "difficulty": 4,
                "reward_scale": 1.8,
            },
        },
    },

    # ========== 48. 国家级六张网十五五顶层规划26.9万亿 含新一代通信网5G-A+6G提前预研 ==========
    "national_six_nets_shiwuwu_26p9trillion_synergy": {
        "name": "国家级六张网十五五顶层规划26.9万亿协同平台（含5G-A规模化+6G提前预研新一代通信网）",
        "description": "中共中央政治局3个月两次高规格部署 4月28日首次将六张网纳入国家战略7月30日明确要求扎实推进落地 仅4个月从概念提出到国务院常务会议跟进督查、发改委密集下发细则、各地都市圈上报项目层层压实 十五五周期预估26.9万亿较十四五基建总规模提升21% 2026开局7万亿超级基建蓝图已正式启动",
        "sub_scenes": {
            "politburo_twice_deployed_4_months_from_concept_to_implementation": {
                "name": "政治局4.28+7.30两次超高频率定调 4个月从概念提出到层层压实落地",
                "description": "4月28日政治局首次将六张网纳入国家级战略 7月30日第二次政治局明确要求扎实推进落地 中间跟进督查+发改委密集细则+地方都市圈清单 整个过程仅4个月近年宏观政策超高频率重复定调十分罕见 释放信号远比普通基建重磅",
                "robots": ["国家级战略规划双会定调执行落地督查体系", "发改委跨部门联动细则密集下发机制", "各地方都市圈项目上报评审快速落地", "4个月从概念提出到层层压实落地超常规节奏"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "26p9trillion_shiwuwu_vs_shisiwu_21pct_upgrade_funding_model": {
                "name": "十五五整体26.9万亿年均5.4万亿较十四五+21% 资金模式全面革新主动放开民间资本",
                "description": "2026开局7万亿只是开胃小菜 十五五五年26.9万亿超级正餐 较十四五基建总规模提升21% 资金：中央预算内7550亿已全下达+超长期特别国债8000亿水利管网科创+政策性银行专项工具 核心变革主动打开民资大门：水网民间投资同比+85.8% 南京都市圈152项目2962亿其中633亿专项招募民资外资 算力网直接鼓励民企自主投资建设 产业链市场化程度更高业绩不靠纯财政更扎实",
                "robots": ["26.9万亿整体规模五年周期滚动规划评估", "7550亿中央+8000亿特别国债+政策行工具投放协同", "水网民资+85.8%南京633亿民资外资招商机制", "算电物流多领域民资准入放开市场化订单兑现"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "six_nets_two_major_categories_shortage_repayment_3_vs_future_3": {
                "name": "六张网两大门类清晰划分 补短板还债刚需3网 vs 开新局未来弹性3网 切忌混淆",
                "description": "第一大类补短板还债刚需三张网(国家水网/城市地下管网/现代物流网)：解决几十年基建欠账刚需属性拉满不受经济周期影响业绩兑现更稳题材炒作属性弱；第二大类开新局未来三张网(新型电网/新一代通信网/算力网)：面向未来前瞻性布局是本轮新基建行情里弹性最高主线赛道 绑定数字经济与AI",
                "robots": ["国家水网跨流域调水航道防洪排涝水资源配置", "城市地下管网77万公里改造新建5万亿供燃排热力老化内涝", "现代物流网内河多式联运枢纽县域冷链降全社会物流成本", "新型电网超5万亿特高压柔性输电储能虚拟电厂算电协同", "新一代通信网5G-A规模化+6G提前预研+光纤升级+卫星互联网组网", "算力网4万亿市场化8枢纽10集群3算电协同战略地位最高"],
                "difficulty": 4,
                "reward_scale": 1.8,
            },
            "nextgen_comm_net_5ga_massive_6g_pre_research_fiber_satellite_internet": {
                "name": "新一代通信网：5G-A Advanced规模化部署+6G提前预研+光纤网络升级+卫星互联网组网（所有数字网络信息高速路）",
                "description": "新一代通信网是用户指定6G主题核心子系统 5G-A Advanced已启动规模化部署、6G IMT-2030提前预研、光纤网络持续升级、低轨卫星互联网组网四大部分共同构成 算力跨区域调度、智能电网远程调控、智慧城市、工业互联网都离不开通信底座 光通信设备光缆基站配套产业链持续跟着六网协同拿增量订单",
                "robots": ["5G-A Advanced商用规模化部署网络升级", "6G IMT-2030全频谱接入天地一体化预研推进", "全光400G/1T OTN DCI光纤骨干网络升级", "低轨卫星互联网星座组网星地融合通信", "算力跨区调度+智能电网远程+工业互联网+智慧城市通信底座支撑"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "six_networks_coupling_hidden_multiplier_effect_compute_core": {
                "name": "六网深度耦合乘数效应远超单网 算力网战略地位最高一张网与其余5网互相赋能协同",
                "description": "六网不是各自单独建设而是深度耦合一体化系统：算力网(战略地位最高) × 新型电网(给算力中心稳定供电算电协同核心) × 新一代通信网(实现算力跨区域调度) × 算力反过来智能优化电网负荷、水务调水调度、城市管网智能运维 × 物流网冷链多式联运智能路径调度 多网联动产业乘数效应远高于单独某一张网 上下游产业链层层传导利好",
                "robots": ["8大国家算力枢纽+10大算力集群+3算电协同区域国家级一体调度", "算电协同陕北-安徽特高压首个十五五投产工程代表", "郑州国家超算互联网核心节点数万张国产AI芯片全天候运行", "截至2026-6全国智能算力规模去年同期2.8倍 2026全社会算力总投入即将破4000亿", "阿里腾讯百度字节自建智算中心+三大运营商公共算力扩容"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "four_truth_shift_from_tiegongji_old_mode_to_weaving_networks_equipment": {
                "name": "四个核心真相：告别铁公基盖房修桥旧时代→进入织网络造高端装备新时代",
                "description": "真相1：非短期放水刺激而是五年周期国家级规划2026开局投资强度高 不能用短线题材思维；真相2：基建时代切换完成 制造业用钢量历史性超过建筑用钢直观佐证国家投资从土建工程转向高端硬件智能装备数字基础设施；真相3：基建红利不再国企独享 民营设备科技企业迎来重大窗口；真相4：六网协同才是隐藏红利 孤立盯单一板块容易漏掉联动机会",
                "robots": ["高端装备/智能装备/数字基础设施新投资主赛道", "制造业用钢历史性超越建筑用钢数据佐证", "各细分领域民营隐形龙头国家级订单承接机制", "7万亿开局26.9万亿超级正餐五年维度业绩兑现周期"],
                "difficulty": 4,
                "reward_scale": 1.9,
            },
        },
    },

    # ========== 文旅商业与公共服务 ==========
    "cultural_tourism": {
        "name": "文旅商业与公共服务",
        "description": "文旅导览、广场巡游IP、公共服务、展会站台等商用服务场景",
        "sub_scenes": {
            "plaza_calligraphy_performance_tour_ip": {
                "name": "广场书法表演文旅IP巡游（星际V写福字）",
                "description": "大唐不夜城实景验证，星际V人形1.69m书写福字表演吸睛级IP，游客围成一圈拍照互动，带动广场人气聚集消费转化",
                "robots": ["星际V陕西籍人形机器人", "毛笔六维力控柔顺运笔", "游客交互自然语言对话", "广场人群密集环境安全避障", "多机景区巡游集群调度"],
                "difficulty": 3,
                "reward_scale": 1.4,
            },
            "scenic_spot_guide_exhibition_station_sales": {
                "name": "景区讲解员+展会站台+商场开业跳舞+站台带货全能承接",
                "description": "擎天智连承接的真实场景：机器人商场开业跳舞、展会站柜台、景区当讲解员、水果批发商站台带货跨品类灵活上岗",
                "robots": ["擎天智连定制训练人形", "商场开业舞蹈动作编排引擎", "展会站台客户问答交互", "景区讲解多语言导览词库", "站台带货商品展示语音推荐"],
                "difficulty": 4,
                "reward_scale": 1.6,
            },
            "costume_hanfu_tang_dynasty_show_performance": {
                "name": "古装大唐汉服同台演出（人形+真人演员混演）",
                "description": "陕西大唐文旅实景：人形机器人身着大唐古装与真人演员同台击鼓表演，完全融入大唐穿越场景，游客真假难辨沉浸感拉满",
                "robots": ["古装人形机器人关节柔性控制", "真人演员动作节奏同步对齐", "古装汉服穿戴关节运动包络安全", "鼓点音乐节拍同步跟踪算法", "大型舞台灯光音响同步触发"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "university_industry_integration_production_education": {
                "name": "产教融合高校实训具身本科首批招生（西交大2026秋）",
                "description": "教育部2026.4正式将具身智能列入普通高校本科目录，西安交大全国首批获批9所之一2026秋开始招本科生，擎天智连天捷创科西交大三方产学研人才培养体系",
                "robots": ["具身智能本科首批招生教学计划", "企业出真实问题学生现场解决培养模式", "西交大+优艾智合半年无尘车间实习", "天捷创科高校设备二次开发集成桥梁", "秦创原科学家工程师双队伍首席科学家"],
                "difficulty": 4,
                "reward_scale": 1.7,
            },
        },
    },

    # ========== 能源电力与AI算力基础设施 ==========
    "energy_power_compute_infra": {
        "name": "能源电力与AI算力基础设施",
        "description": "绿电直连算力中心、SST固态变压器、光伏风电储能算电协同、算力集群部署",
        "sub_scenes": {
            "2gw_green_power_direct_super_ai_monad": {
                "name": "2GW绿电直连百万P百万GPU AI算力超级单体（远景乌兰察布星河基地）",
                "description": "乌兰察布国家东数西算八大节点之一，全域绿电占比67%，自建风场专线，2GW容量120000㎡建筑面积超级单体，远景戈壁使命2030全球5GW首舰",
                "robots": ["远景乌兰察布星河基地超级单体", "2GW园区级风光储一体化供电", "100%绿电直连专线不经过公共电网", "百万P算力百万张GPU规模", "戈壁使命计划2030年全球5GW目标"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "sst_solid_state_transformer_98_5pct_efficiency": {
                "name": "SST固态变压器10kV直转800V效率98.5%铜减80%",
                "description": "远景引入SST固态变压器技术，传统多级变压AC→DC→AC→DC循环全精简，直转架构减少转换次数提升效率降低铜用量",
                "robots": ["SST固态变压器10kV/13.8kV交流输入", "800V直流直供算力设备", "98.5%转换效率业界最高", "铜用量最高减少80%设备成本更低", "GW级IDC配电更紧凑空间更省"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "tianji_weather_tianshu_energy_twin_models_ms_sync": {
                "name": "天机气象大模型+天枢能源大模型双AI毫秒级协同优化",
                "description": "墙外远景基于天机气象+天枢能源双AI，把发电预测+储能充放+算力负荷三者毫秒级协同优化，由人工经验调度变物理AI精准调控",
                "robots": ["天机气象大模型24-72h风光发电预测", "天枢能源大模型源网荷储全链路优化", "算力负荷小时级分钟级双时间尺度预测", "三者毫秒级Kafka数据流协同调度", "不稳定绿电变得可规划可调度"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "compute_electricity_coupling_green_scheduling": {
                "name": "算电协同绿色调度（风光出力高峰算力任务错峰迁移）",
                "description": "当绿电出力高峰时段把延迟不敏感的AI训练/推理任务自动迁移，风光出力低谷时自动降低算力集群负载，碳排放强度降低同时电费成本优化",
                "robots": ["绿电出力预测5分钟滚动更新", "算力任务优先级分层调度Kubernetes", "风光高峰时段延迟容忍任务自动启动", "风光低谷时段非紧急任务自动挂起", "碳排放强度实时监测与绿证溯源"],
                "difficulty": 4,
                "reward_scale": 1.8,
            },
        },
    },

    # ========== 5G-A→6G下一代通信网络 ==========
    "nextgen_telecom_network": {
        "name": "5G-A→6G下一代通信网络",
        "description": "5G-A规模化部署、6G IMT-2030预研、通感一体化、空天地一体化、AI原生网络",
        "sub_scenes": {
            "5ga_release_18_19_20_massive_deployment": {
                "name": "5G-A R18/R19/R20三版规模化部署（上行MIMO+XR+工业互联网）",
                "description": "3GPP 5G-A阶段Release 18正式开启涵盖18/19/20三版，能力：上下行速率MIMO XR工业互联网垂直行业支撑增强，网络智能化AI节能，非地面网络定位终端能力",
                "robots": ["5G-A Rel-18首版NR和5GC架构基础增强", "上行MIMO增强大上行传输满足工业物联网", "XR增强虚实同传低时延高带宽", "AI/ML辅助网络与无线空口能力", "非地面网络卫星+定位增强终端能力"],
                "difficulty": 4,
                "reward_scale": 1.7,
            },
            "6g_imt_2030_six_usage_scenarios_seven_new_indicators": {
                "name": "6G IMT-2030六大使用场景七项新增指标（2029方案→2030商用→2035万亿规模）",
                "description": "ITU正式定名6G为IMT-2030，六大使用场景：沉浸式通信/超高可靠低时延/海量通信/泛在连接/AI通信融合/通感一体化，2026.2 WP5D完成性能需求草案明确20指标7项新增，2029方案→2030商用→2035规模化万亿市场",
                "robots": ["六大使用场景全覆盖技术预研", "7项6G全新性能指标攻关", "工信部2026.6省协同试点行动：2029自主技术方案", "信通院：2030左右启动商用2035规模化万亿", "大中华区2035-2040需2.5-3.3GHz中频段频谱资源"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "five_core_6g_industry_chain_opportunity_domains": {
                "name": "6G产业链五大核心机遇领域（网络设备/芯片器件/通感融合/空天一体/AI网络）",
                "description": "6G产业链核心机遇集中五大领域：1网络设备(基站天线射频核心网承载网)2芯片器件(太赫兹智能超表面新型射频前端)3通感融合(通感一体化基站低空感知高精度定位)4空天地一体化(卫星互联网非地面)5AI网络融合(内生智能AI-native空口网络自动化运维)",
                "robots": ["网络设备：基站天线射频核心网承载网新一轮迭代", "芯片器件：太赫兹芯片智能超表面新型射频前端突破", "通感融合：一体化基站低空经济感知工业高精度定位", "空天地一体化：卫星互联网地面网络融合终端成熟", "AI网络融合：内生架构AI-native空口自动化运维"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "optical_interconnect_three_layer_compute_fabric": {
                "name": "算力集群光互联三层技术栈（可插拔+CPO+硅光长期共存）",
                "description": "三条路线长期共存各有用途：可插拔主攻中长距离替换便利(800G→1.6T→3.2T)，CPO主攻机柜内高密度互联（功耗30W→9W以下降约70% 2027-2028规模化），硅光做底层集成支撑两者底座",
                "robots": ["可插拔光模块：800G→1.6T→3.2T演进路线", "CPO共封装光学：2026导入期2027-2028大规模普及", "硅光技术底座：长期基础层支撑上下两层", "英伟达SpectrumX CPO交换机投产2026.3", "全球CR5高速光模块份额中国厂商超60%"],
                "difficulty": 4,
                "reward_scale": 1.8,
            },
        },
    },

    # ========== AI for Science科研智能体 ==========
    "ai4s_scientific_research": {
        "name": "AI for Science科研智能体",
        "description": "AI4S科研智能体全流程闭环，化学/能源/材料/药物四大方向，真实科研案例落地",
        "sub_scenes": {
            "mira_three_layer_full_chain_closed_loop_scientific": {
                "name": "Mira三层科研全流程闭环（Agent Squad+双引擎+科研记忆）",
                "description": "覆盖假设生成→模拟计算→实验验证→知识沉淀完整闭环，上层Agent Squad分工协作交叉验证，中层计算+实验双执行引擎打通干实验室湿实验室，底层可沉淀科研记忆科学维基体系",
                "robots": ["上层多智能体小队Agent Squad角色分工交叉验证", "云端高性能计算资源调度引擎", "自动化湿实验室机械臂操作执行引擎", "底层三层科研记忆体系：通用层/实战层/风格偏好层", "企业级私有化部署分级权限全流程操作审计"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "three_real_cases_chemistry_energy_material_pharma": {
                "name": "Mira三大真实科研案例落地（化学/催化材料/药物）",
                "description": "Mira披露三大完整真实科研案例横跨三大领域，科研人员只用日常语言描述目标与约束，系统自主推进从文献调研方案设计工具调用到结论输出全流程：1.KHP有机小分子Korcek反应机理复现 2.Pt(111)贵金属催化CO吸附电荷重分布 3.ABL1靶点伊马替尼蛋白结合模式Top3收敛一致",
                "robots": ["案例1：KHP有机小分子自动解析Korcek分解反应机理", "案例2：CO/Pt(111)经典催化体系吸附行为与DFT计算", "案例3：ABL1靶点伊马替尼结合模式预测排序可视化", "日常语言描述目标约束→全流程自主推进", "锂电+工业冷却液客户真实合作研发管线嵌入"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "compute_cost_dynamic_cascade_screening_save_compute": {
                "name": "动态分级筛选策略显压缩计算成本+数据回流持续校准",
                "description": "传统研发模式对所有候选方案统一高精度计算，大量算力消耗在价值极低早期筛选。Mira先用低成本方法完成大范围初筛，只对真具备潜力的方案投入高精度算力，每个项目数据自动回流持续校准模型",
                "robots": ["候选方案第一阶段：低成本经验模型快速初筛", "第二阶段：只对有潜力的方案投入高精度DFT算力", "算力成本较传统模式显压缩70-80%", "项目数据自动回流模型越用越准持续校准筛选规则", "工业冷却液锂电电解液配方筛选已验证真实工业场景"],
                "difficulty": 4,
                "reward_scale": 1.8,
            },
        },
    },

    # ========== 水下特种机器人作业 ==========
    "underwater_special_operations": {
        "name": "水下特种机器人作业",
        "description": "水下管廊/船体检测、港口安防、浑水夜间强光、多机大范围搜索",
        "sub_scenes": {
            "simulation_mirror_zero_delay_plus_joystick_control": {
                "name": "水下机器人仿真+真机零延迟镜像+专业操纵杆操作",
                "description": "天津深之蓝方案：仿真系统先测，和真机双向镜像零延迟同步，专业级操纵杆多屏监控确保操作精准可靠，浑水环境先仿真后实机渐进调试",
                "robots": ["深之蓝仿真系统真实物理引擎水下模拟", "仿真+真机双向镜像零延迟同步", "专业级多自由度操纵杆操作", "多屏监控多路高清视频流显示", "浑水先仿真后实机渐进降低风险"],
                "difficulty": 4,
                "reward_scale": 1.7,
            },
            "real_water_night_strong_light_underwater_performance": {
                "name": "真实水域+夜间强光水下机器人综合性能测试",
                "description": "天津瀚海蓝帆方案：真实淡水+海水双环境，夜间大功率LED强光照明穿透浑水，真实水流扰动下操作稳定性长周期验证通过",
                "robots": ["真实淡水/海水双环境适应性长周期验证", "大功率LED水下强光照明阵列浑水穿透", "真实水流浮力缆张力扰动姿态控制", "夜间低光+强光照明切换成像质量验证", "水下抓取物体水流扰动稳定性实测"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "pipeline_corrosion_hull_defect_port_security_three": {
                "name": "三大核心业务：水下管廊腐蚀检测+船体缺陷+港口安防巡逻",
                "description": "天津双品牌水下机器人覆盖三大核心业务：水下管廊石油化工管道腐蚀情况检测、船体螺旋桨船底附着物清理缺陷检测、港口码头水下安防可疑目标巡逻",
                "robots": ["水下管廊管道腐蚀减薄厚度UT检测", "船体表面附着物清理+缺陷磁粉探伤检测", "港口码头岸线水下可疑目标巡逻警报", "多ROV协同大范围水域搜索覆盖", "CCS中国船级社水下作业资质认证"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
        },
    },

    # ========== 泳池清洁机器人（消费级） ==========
    "consumer_pool_cleaning": {
        "name": "泳池清洁机器人（消费级）",
        "description": "工厂组装+室内池测试+室外池耐力+多池并行批量品控",
        "sub_scenes": {
            "pool_cleaning_robot_factory_assembly_line": {
                "name": "泳池清洁机器人工厂组装生产线一条龙（天津望圆）",
                "description": "天津望圆智能工厂：泳池清洁机器人从零部件到整机一条龙组装，爬墙吸附泵+AI路径规划板+电池PACK装配与老化测试",
                "robots": ["SMT产线AI路径规划控制板贴片组装", "自动化爬墙吸附负压水泵装配校准", "电池PACK充放电老化柜循环测试", "整机外观结构件组装流水线", "整机功能初测+包装出库品控"],
                "difficulty": 3,
                "reward_scale": 1.4,
            },
            "indoor_standard_pool_functional_100_coverage": {
                "name": "室内标准泳池功能测试（池底池壁水线100%全覆盖不重复）",
                "description": "室内标准50m×25m比赛池，测试AI全覆盖路径规划：池底平地、池壁90度爬墙、水线污渍清洁，三模式独立切换覆盖率要求100%零死角不重复",
                "robots": ["标准50×25m竞赛池功能测试环境", "AI栅格SLAM100%全覆盖路径规划", "池底平地深度清洁模式", "池壁90度爬墙吸附清洁模式", "水线污渍识别定点清洁模式"],
                "difficulty": 3,
                "reward_scale": 1.5,
            },
            "outdoor_open_pool_sunlight_cl_long_endurance": {
                "name": "室外露天泳池真实长周期验证（日晒+紫外线+含氯腐蚀）",
                "description": "室外真实露天泳池，长周期耐力验证：夏天日晒高温紫外线+泳池高浓度含氯水腐蚀，整机密封+外罩材质+电池寿命长期耐久性测试",
                "robots": ["室外露天真实泳池年周期环境条件", "紫外线UV-B加速老化验证", "泳池水3-5ppm余氯耐腐蚀测试", "整机IP68密封长期水浸不渗漏", "高温45℃夏季电池安全性验证"],
                "difficulty": 4,
                "reward_scale": 1.7,
            },
            "multi_pool_parallel_batch_quality_control": {
                "name": "多机多池并行批量品控（工厂同时测十几台不同池）",
                "description": "望圆工厂规模化品控：多台泳池清洁机器人并行测试，不同规格不同大小不同深度多个泳池同步批量品控，量产一致性质量保证",
                "robots": ["多池并行批量品控产线", "不同规格不同深度泳池同时测试", "每台机器人独立测试数据采集通道", "量产一致性统计CPK>1.33质量要求", "缺陷自动识别+不良品自动分拣"],
                "difficulty": 4,
                "reward_scale": 1.6,
            },
        },
    },

    # ========== 家庭陪伴级机器人（消费级） ==========
    "consumer_family_companion": {
        "name": "家庭陪伴级机器人（消费级）",
        "description": "独居年轻人日常陪伴、儿童早教启蒙、全家人全能管家远程监控三大类产品",
        "sub_scenes": {
            "kata_friends_tactile_visual_emotion_dual_feedback": {
                "name": "KATA Friends触觉视觉双重情感反馈陪伴（独居年轻人日常）",
                "description": "毛绒萌宠外形，抚摸触觉→愉悦咕噜声+弯弯月牙眼表情；情绪低落→安静靠+蹭手；独居年轻人门口迎接+趴旁伴看+睡前故事+自由探索",
                "robots": ["毛绒柔软外壳触感友好", "触觉电容+压力多传感器阵列", "LED矩阵眼部多表情状态显示", "音频TTS咕噜声+睡前故事", "家居环境IR防跌落自由探索底盘"],
                "difficulty": 3,
                "reward_scale": 1.4,
            },
            "iluki_child_speech_age_based_personalized_edu": {
                "name": "I.LUKI儿童语音+年龄智能推荐因材施教（央ma认证）",
                "description": "央ma认可海量学习资源，诗词英语科学历史无所不包；儿童口齿不清发音不标准也能准确识别；按年龄和认知智能推荐因材施教，半年实测口语明显进步",
                "robots": ["央ma权威认证学习资源内容安全", "6麦阵列远场儿童语音识别", "发音不准歌曲请求也能准确理解", "年龄和认知水平分级智能推荐引擎", "英语口语半年实测对话练习进步"],
                "difficulty": 3,
                "reward_scale": 1.5,
            },
            "wyndme_waimi_24h_multilang_remote_family_all_in_one": {
                "name": "歪觅WYNDME Pro24h续航多语言互动+远程监控全家管家",
                "description": "环球资源创新大奖产品，全家全能：陪老人聊天解闷、陪孩子外语学习玩耍、出差远程看家里宠物，手机端联动随时查看家里情况，满电24h一整天不用频繁充电",
                "robots": ["环球资源创新大奖获奖产品2025HK", "中英文及多语言NLU自然对话", "1080P夜视家用远程监控RTSP", "老人孩子宠物三大场景适配模式", "24小时长续航BMS电池管理"],
                "difficulty": 3,
                "reward_scale": 1.6,
            },
            "consumer_companion_privacy_safety_material_safety": {
                "name": "消费级陪伴机器人选购三要点（交互体验+场景适配+隐私安全）",
                "description": "选购三大纯技术要点：①交互体验→语音识别准确率+反应速度+表情丰富度+NLP自然语言；②场景适配→小孩材质安全圆润无棱角/老人操作简单大字体大音量/自己外观喜欢功能丰富；③隐私安全→摄像头麦克风品牌隐私保护措施知名品牌",
                "robots": ["语音识别准确率+响应延迟测试评价", "自然语言处理NLP闲聊对话流畅度", "儿童食品接触级材质安全认证标准", "老年人大字体大音量无障碍操作UI", "知名品牌摄像头麦克风隐私合规GDPR"],
                "difficulty": 2,
                "reward_scale": 1.3,
            },
        },
    },

    # ========== 明厨AI食品安全非现场监管系统 ==========
    "food_safety_ai_regulation": {
        "name": "明厨AI食品安全非现场监管系统",
        "description": "浙江首创AI+非现场监管，全国首个明厨AI垂直大模型19万商户全量覆盖+电子证照+聚集区+食安哨兵骑手",
        "sub_scenes": {
            "190k_merchants_day_night_dual_mode_auto_patrol": {
                "name": "19万接入商户昼夜双模式自动巡检（白天卫生操作+夜间鼠迹）",
                "description": "全国首个明厨AI垂直大模型，对接入19万商户全量开展静态+动态自动巡检：白天巡检后厨卫生人员违规操作未戴帽未戴手套抽烟玩手机；夜间自动监测鼠迹蟑螂卫生问题",
                "robots": ["接入19万商户百万路摄像头视频流接入", "白天后厨人员违规操作识别：未戴帽/手套/抽烟/玩手机", "夜间后厨鼠迹蟑螂识别自动监测", "精准捕捉违规画面自动存档不可篡改", "全商户覆盖7×24小时不停机巡检"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "violation_8000_cases_electronic_evidence_push_rectification_53pct": {
                "name": "违规8000例电子固证实时推送→整改率28.05%→52.9%不合格率21%→3.83%",
                "description": "系统累计抓拍违规操作视频约8000余例，电子固证+实时推送，监管部门可回溯可追踪，商户自主整改率从28.05%上升至52.9%，不合格商户占比从21%逐月下降到3.83%，人海战术→智慧监管转型",
                "robots": ["违规操作视频8000余例自动抓拍存档", "Hash链不可篡改电子固证区块链存证", "实时短信+外呼双通道监管通知推送", "整改前后对比AI自动审核结案", "监管指标看板：整改率/不合格率/违规类型统计"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "three_combination_punch_e_license_110_zones_8122_rider_sentinels": {
                "name": "治理组合拳：电子证照杜绝假证+110聚集区1381商户+食安哨兵骑手8122次监督",
                "description": "浙江组合拳三项同时打：①电子证照公示源头杜绝假证套证；②创新无堂食外卖聚集区管理模式分散商户向合规园区集中已建110个入驻1381家；③食安哨兵骑手监督机制已有效监督反馈解决8122次商家食品安全问题",
                "robots": ["电子营业执照卫生许可证公示核验系统", "无堂食外卖聚集区110个已建入驻1381家", "食安哨兵骑手监督小程序上报机制", "截至6月底骑手监督反馈解决8122次问题", "经验全国多地复制推广持续深化"],
                "difficulty": 4,
                "reward_scale": 1.9,
            },
        },
    },

    # ── 智慧港口全矩阵机器人（青岛港近20种） ──
    "smart_port_full_matrix": {
        "name": "智慧港口全矩阵机器人作业",
        "description": "青岛港全自动化码头近20种专用机器人：高压岸电连接、防爆巡检、设备维修、集装箱自动转运、危险品监测全流程无人化",
        "sub_scenes": {
            "high_voltage_shore_power_auto_connection": {
                "name": "高压岸电机器人自动连接（7500V高压自动对接零人工）",
                "description": "船舶靠港后7500V高压岸电电缆自动对接机器人，视觉定位+力控柔顺插拔+绝缘防护全程零人工，替代传统人工接电高危作业，接电时间从45分钟缩短至8分钟",
                "robots": ["7500V高压岸电机器人", "六自由度柔顺对接机械臂", "视觉+激光双目定位系统", "高压绝缘防护安全机构", "接电状态实时监测联锁保护"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "explosion_proof_crane_inspection": {
                "name": "防爆轨道巡检机器人（岸桥场桥全天候自动巡检）",
                "description": "岸桥场桥轨道式防爆巡检机器人，搭载红外热像+气体检测+视觉识别，7×24小时自动巡检钢丝绳磨损/电机温升/减速器异响/油气泄漏，异常自动报警派单",
                "robots": ["防爆轨道巡检机器人ExdIIBT4", "红外热像仪+可见光双目", "CH4/H2S/O2多气体检测", "钢丝绳磨损AI视觉检测", "设备振动声学诊断系统"],
                "difficulty": 4,
                "reward_scale": 1.8,
            },
            "container_crane_maintenance_repair": {
                "name": "港机设备维修机器人（高处/狭窄/重载维修作业替代人工）",
                "description": "岸桥臂架/小车/大梁维修专用机器人，爬壁吸附+磁轮行走+多自由度作业臂，替代人工高处作业进行螺栓紧固/焊缝检测/润滑注油/零件更换，人员零高危暴露",
                "robots": ["磁吸附爬壁维修机器人", "多自由度作业臂+快换工具头", "焊缝超声波探伤检测", "自动螺栓拧紧扭矩反馈", "远程遥操作+AI辅助作业"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "hazardous_goods_monitoring_emergency": {
                "name": "危险品集装箱监测应急机器人",
                "description": "危险品箱区全天候监测机器人，温湿度/泄漏气体/放射性实时监测，异常自动隔离+喷淋降温+应急处置，危化品作业人员零近距离接触",
                "robots": ["防爆轮式巡检机器人", "放射性/毒气/温湿度多传感器", "自动喷淋降温系统联动", "危险品箱区电子围栏", "应急处置机械手"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "automatic_container_transfer_agv_straddle": {
                "name": "集装箱自动转运（AGV/IGV/无人跨运车全流程无人）",
                "description": "全自动化码头水平运输：L4级IGV自动导引车+无人跨运车+自动堆垛机，从船边到堆场全流程无人化，作业效率较传统码头提升30%，人员减少70%",
                "robots": ["L4级IGV自动导引车", "无人跨运车远程驾驶", "自动化轨道吊ARMG", "码头TOS生产操作系统", "V2X车路协同调度"],
                "difficulty": 4,
                "reward_scale": 1.8,
            },
        },
    },

    # ── 世界模型/VLA具身大模型开发平台 ──
    "world_model_vla_platform": {
        "name": "世界模型与VLA具身大模型开发平台",
        "description": "Skild AI通用世界模型、Physical Intelligence π0、NVIDIA Isaac GR00T、Google DeepMind Gemini Robotics、华为CloudRobo五大全球领先具身开发平台全栈支持",
        "sub_scenes": {
            "skild_ai_universal_world_model": {
                "name": "Skild AI通用世界模型（物理直觉+通用策略+跨形态迁移）",
                "description": "Skild AI构建通用机器人大脑世界模型，统一物理引擎与神经网络预测，跨机器人形态（单臂/双臂/人形/四足）策略零样本迁移，一套模型适配所有硬件形态",
                "robots": ["Skild Brain通用世界模型推理", "跨形态迁移学习框架", "多机器人形态策略蒸馏", "物理规律一致性预测引擎", "实时闭环规划与控制"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "physical_intelligence_pi0_vla": {
                "name": "Physical Intelligence π0 (pi0) VLA具身大模型（视觉-语言-动作端到端）",
                "description": "π0 VLA模型直接输入视觉图像+语言指令输出机器人关节动作，无需人工编程任务级指令直接泛化，预训练数据来自真实机器人操作，真实部署开箱即用",
                "robots": ["π0 VLA视觉语言动作模型", "视觉编码器+语言理解器+动作解码器", "任务级自然语言指令泛化", "真实机器人数据预训练权重", "零样本新任务快速适应"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "nvidia_isaac_gr00t_humanoid_platform": {
                "name": "NVIDIA Isaac GR00T人形机器人基础模型平台（通用人形机器人大脑）",
                "description": "NVIDIA Isaac GR00T（Generalist Robot 00 Technology）为人形机器人提供基础模型，Isaac Sim仿真+Jetson Thor边缘计算+GR00T模型三位一体，全球人形机器人厂商共同生态",
                "robots": ["Isaac GR00T基础模型", "Isaac Sim高保真仿真训练", "Jetson Thor人形专用计算平台", "Cosmos世界模型生成合成数据", "GR00T Blueprint参考架构"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "google_deepmind_gemini_robotics": {
                "name": "Google DeepMind Gemini Robotics（Gemini大模型机器人版）",
                "description": "Gemini Robotics将Gemini多模态大模型能力注入机器人，空间理解+推理规划+精细操作一体化，RT-2/RT-X系列真实世界数据训练，手机到机器人全场景泛化",
                "robots": ["Gemini Robotics多模态模型", "Gemini Robotics-ER 1.5空间推理", "RT-X跨机器人数据集训练", "手机端到端示教AutoRT", "真实场景泛化推理引擎"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "huawei_cloudrobo_cloud_native_platform": {
                "name": "华为CloudRobo云原一具身智能开发平台（端边云协同训练部署）",
                "description": "华为CloudRobo云原一具身智能平台：云端大模型训练+边缘节点推理+机器人端侧执行三层架构，云上训练大规模仿真，模型一键下发到多品牌机器人，开发者生态开放",
                "robots": ["CloudRobo云端训练平台", "端边云协同推理架构", "多品牌机器人统一API", "云原生DevOps流水线", "模型市场与开发者生态"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
        },
    },

    # ── AI安防智能体 ──
    "ai_security_agent": {
        "name": "AI安防智能体系统",
        "description": "SARA安防智能体、Athena Security智能安检、全球领先AI安防主动预警系统，从事后追溯到事前预警转型",
        "sub_scenes": {
            "sara_security_patrol_agent": {
                "name": "SARA安防智能体（主动巡逻+异常识别+自动处置全自主）",
                "description": "SARA安防智能体集成多传感器融合+大模型推理+自主决策，自主规划巡逻路线+识别异常行为+自动报警+联动处置，替代保安7×24小时不间断值守",
                "robots": ["SARA安防智能体核心决策大脑", "多摄像头360°全景感知", "异常行为AI实时识别", "巡逻路径自主规划调度", "声光报警+门禁联动处置"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "athena_security_weapon_detection": {
                "name": "Athena Security智能安检系统（AI视觉无接触武器检测毫秒级识别）",
                "description": "Athena Security用普通监控摄像头+AI视觉实现毫秒级枪支/刀具/武器识别，无需金属探测门行人正常行走即可检测，公共场所/学校/医院零接触安检",
                "robots": ["Athena AI武器检测算法", "现有摄像头利旧无需硬件改造", "毫秒级实时检测响应", "枪支刀具危险物识别99%+准确率", "警方联动自动报警定位"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
        },
    },

    # ── 天地一体化太空超算融合设施 ──
    "space_ground_supercomputing_fusion": {
        "name": "天地一体化太空超算数融合设施",
        "description": "国家超算天津中心天河太空超智数融合、国星宇航星算计划2800颗计算卫星、中科天算辰光一号天基计算卫星，天地一体算力网络",
        "sub_scenes": {
            "tianhe_space_supercomputing_fusion_facility": {
                "name": "天河太空超智数融合设施（国家超算天津中心天地一体化）",
                "description": "国家超算天津中心牵头建设天河太空超智数融合设施，天基计算节点+地面超级算力互联互通，太空数据在轨处理+地面深度分析一体化，卫星数据利用率提升10倍",
                "robots": ["天河超级计算集群地面节点", "星载计算节点高速处理单元", "星地激光高速通信链路", "天地一体化算力调度平台", "太空数据在轨预处理引擎"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "guoxing_yuhang_xingsuan_2800_satellites": {
                "name": "国星宇航星算计划2800颗计算卫星星座（天基AI算力网络）",
                "description": "国星宇航星算计划规划2800颗AI计算卫星组网，每颗卫星搭载AI推理芯片，遥感数据在轨实时处理，分钟级全球任意地点响应，全球首个大规模天基算力网络",
                "robots": ["2800颗AI计算卫星星座", "星载AI推理芯片模组", "星间激光链路组网", "在轨AI目标检测识别", "分钟级全球响应调度"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
            "zhongke_tiansuan_chenguang1_satellite": {
                "name": "中科天算辰光一号天基计算卫星（星载算力验证首发星）",
                "description": "中科天算辰光一号天基计算卫星首发验证星成功入轨，验证星载AI算力、星地协同计算、在轨模型更新等核心技术，为后续规模化星座奠定技术基础",
                "robots": ["辰光一号天基计算验证卫星", "星载通用AI计算平台", "星地协同计算任务调度", "在轨模型OTA更新", "算力计量与交易验证"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
        },
    },

    # ── AI算力光互联三层技术栈 ──
    "ai_compute_optical_interconnect": {
        "name": "AI算力光互联三层技术栈",
        "description": "可插拔800G/1.6T/3.2T光模块+CPO共封装光学+硅光底座三层架构，AI算力集群高速互联核心技术",
        "sub_scenes": {
            "pluggable_800g_3_2t_optical_modules": {
                "name": "可插拔光模块：800G规模商用→1.6T量产→3.2T研发",
                "description": "可插拔光模块演进路线：800G已规模部署AI集群，1.6T 2026年量产，3.2T研发推进，单通道速率从100G→200G演进，热设计/功耗/信号完整性全面优化",
                "robots": ["800G DR8/FR4/LR8光模块", "1.6T OSFP-XD光模块", "3.2T下一代光模块研发", "EML/SiPh激光器芯片", "DSP数字信号处理芯片"],
                "difficulty": 5,
                "reward_scale": 1.8,
            },
            "cpo_co_packaged_optics": {
                "name": "CPO共封装光学（光引擎与交换芯片同封装 功耗降50%）",
                "description": "CPO将光引擎与ASIC交换芯片共封装在同一基板，电互连距离从几十厘米缩短到几厘米，功耗降低50%带宽密度提升数倍，AI万卡集群互联下一代核心技术",
                "robots": ["CPO光引擎共封装基板", "光电合封ASIC芯片", "外部激光光源ELS", "光纤阵列耦合封装", "CPO交换芯片散热设计"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
            "silicon_photonics_platform": {
                "name": "硅光底座（硅光子集成平台 所有光器件单片集成）",
                "description": "硅光子技术平台在硅片上集成调制器/探测器/波导/光栅等所有光器件，CMOS工艺兼容大规模量产成本大幅降低，光互联技术长期演进基础底座",
                "robots": ["硅光调制器/探测器集成", "CMOS工艺兼容流片", "光栅耦合器/边缘耦合器", "硅光PDK工艺设计套件", "8寸/12寸硅光晶圆产线"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
        },
    },

    # ── 轮式双臂工厂实用机器人 ──
    "wheeled_dual_arm_factory_robot": {
        "name": "轮式双臂工业实用机器人",
        "description": "西交大巡霄轮式双臂机器人：续航长稳定性好成本低工厂实用，打破人形高成本不实用困境",
        "sub_scenes": {
            "xjtu_xunxiao_long_endurance_low_cost": {
                "name": "西交大巡霄轮式双臂（续航>8h/稳定可靠/成本仅人形1/5）",
                "description": "西安交大研发巡霄轮式双臂移动操作机器人，轮式底盘长续航+成熟稳定双臂操作，工厂物料分拣/机床上下料/装配搬运直接可用，采购成本仅为人形机器人1/5，工厂实用主义路线",
                "robots": ["轮式移动底盘（麦克纳姆轮/差速驱动）", "成熟工业级六轴双臂", "8小时以上长续航磷酸铁锂", "视觉分拣+力控装配", "工业级稳定性MTBF>5000h"],
                "difficulty": 3,
                "reward_scale": 1.7,
            },
        },
    },

    # ── 人形机器人表演互动 ──
    "humanoid_performance_interaction": {
        "name": "人形机器人表演与互动",
        "description": "星际V人形机器人书法表演等文旅商演互动场景，人形进入大众视野",
        "sub_scenes": {
            "xingji_v_calligraphy_performance": {
                "name": "星际V人形机器人书法表演（陕西籍人形写福字传统文化展示）",
                "description": "星际V人形机器人现场表演毛笔书法写福字，轨迹规划精细控制毛笔锋毫，力控保证笔触轻重变化，文旅/展会/节庆活动商演互动，人形机器人传统文化展示标杆",
                "robots": ["星际V人形机器人整机", "七自由度双臂书法轨迹规划", "毛笔力控笔触反馈", "多自由度腰部+头部协同", "现场互动视觉识别观众"],
                "difficulty": 4,
                "reward_scale": 1.7,
            },
        },
    },

    # ── 车规级一体化关节模组 ──
    "vehicle_grade_integrated_joint": {
        "name": "车规级一体化关节模组供应链",
        "description": "智莱特车规级一体化关节（法士特+智元双背景），人形机器人核心零部件车规级量产",
        "sub_scenes": {
            "zhilaite_vehicle_grade_joint_fast_shield_agibot": {
                "name": "智莱特车规级一体化关节模组（法士特制造+智元机器人双背景）",
                "description": "智莱特机器人关节模组由法士特汽车传动制造背景+智元机器人应用背景双加持，按车规级标准开发验证，高功率密度/高效率/高可靠性/低成本，满足人形机器人大规模量产需求",
                "robots": ["无框力矩电机+谐波减速机一体化", "车规级编码器+驱动器集成", "-40℃~85℃车规温度范围", "IATF 16949质量管理体系", "100万次寿命台架验证"],
                "difficulty": 4,
                "reward_scale": 1.8,
            },
        },
    },

    # ── 2GW AI算力超级单体 ──
    "ai_supermonad_compute_base": {
        "name": "AI算力超级单体（Greenfield绿电直连）",
        "description": "远景乌兰察布星河基地全球最大AI算力超级单体2GW绿电直连SST固态变压器98.5%效率",
        "sub_scenes": {
            "yuanjing_wulanchabu_stellar_2gw_green_ai": {
                "name": "远景乌兰察布星河基地全球最大AI算力超级单体（2GW绿电直连）",
                "description": "远景科技集团在乌兰察布建设星河基地全球最大AI算力超级单体，2GW绿电风电光伏直连算力中心，SST固态变压器效率98.5%，PUE<1.1，零碳AI算力全球标杆",
                "robots": ["2GW风光绿电直供系统", "SST固态变压器高效率配电", "液冷AI算力机柜集群", "PUE<1.1极致能效", "源网荷储一体化调度"],
                "difficulty": 5,
                "reward_scale": 2.0,
            },
        },
    },

    # ── 灵巧手触觉力控核心部件 ──
    "dexterous_hand_tactile": {
        "name": "灵巧手与触觉感知核心部件",
        "description": "中科慧思灵巧手等国产高自由度灵巧手，人形机器人精细操作核心末端执行器",
        "sub_scenes": {
            "zhongke_huisi_dexterous_hand": {
                "name": "中科慧思高自由度灵巧手（多关节协同精细操作）",
                "description": "中科慧思研发高自由度灵巧手，多关节协同+触觉感知+力控柔顺，完成抓取/拧螺丝/折纸/使用工具等精细操作任务，人形机器人末端执行器国产替代方案",
                "robots": ["多自由度欠驱动/全驱动灵巧手", "腱绳/连杆传动机构", "指尖触觉传感器阵列", "力位混合柔顺控制", "快速换电快换接口"],
                "difficulty": 5,
                "reward_scale": 1.9,
            },
        },
    },

    # ========== 现实生活AI全领域应用 ==========
    # ── 智慧政务/AI+政府服务 ──
    "smart_government": {
        "name": "智慧政务（一网通办/城市大脑）",
        "description": "AI+政务服务一网通办、智能审批、城市大脑、一网统管、12345智能客服",
        "sub_scenes": {
            "one_network_government": {
                "name": "一网通办智能审批",
                "description": "政务服务事项AI智能审批、材料自动核验、表单自动填写、秒批秒办，政务服务效率提升80%以上",
                "robots": ["AI大模型审批引擎", "OCR证照智能识别", "电子签章系统", "智能客服机器人", "数据共享交换平台"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
            "city_brain": {
                "name": "城市大脑一网统管",
                "description": "城市运行态势感知、事件智能发现、跨部门协同调度、应急指挥决策，城市治理现代化核心平台",
                "robots": ["视频AI分析平台", "IoT物联感知网络", "时空信息云平台", "AI决策引擎", "应急指挥调度系统"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "12345_smart_hotline": {
                "name": "12345政务智能客服",
                "description": "12345热线智能接听、诉求自动分类、工单智能派发、满意度智能回访，政务热线接通率/办结率大幅提升",
                "robots": ["语音识别ASR", "语义理解NLU", "智能工单派发系统", "智能语音外呼", "知识库问答系统"],
                "difficulty": 3,
                "reward_scale": 0.9,
            },
        },
    },

    # ── AI+金融 ──
    "ai_finance": {
        "name": "AI+金融（智能风控/智能投顾/反欺诈）",
        "description": "银行/证券/保险全流程AI应用：智能风控、反欺诈、智能投顾、智能核保、智能客服",
        "sub_scenes": {
            "ai_risk_control": {
                "name": "智能风控反欺诈",
                "description": "信贷实时风控、交易反欺诈、异常行为检测、信用评分模型，金融风险识别准确率99%以上",
                "robots": ["图计算反欺诈引擎", "实时流计算平台", "信用评分模型", "异常检测算法", "黑名单知识图谱"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "ai_customer_service": {
                "name": "金融智能客服",
                "description": "银行/保险智能客服、智能外呼、智能理赔、智能核保，7x24小时服务替代80%人工坐席",
                "robots": ["大模型对话机器人", "语音合成TTS", "智能理赔审核系统", "智能核保引擎", "多渠道接入网关"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
            "ai_robo_advisor": {
                "name": "智能投顾/量化交易",
                "description": "智能资产配置、量化策略交易、市场情绪分析、智能研报生成，AI辅助投资决策",
                "robots": ["量化交易平台", "市场情绪分析NLP", "多因子选股模型", "智能研报生成", "风险回测系统"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
        },
    },

    # ── AI+零售/电商 ──
    "ai_retail": {
        "name": "AI+零售/电商（智能推荐/智慧门店/无人零售）",
        "description": "电商个性化推荐、智慧门店、无人零售、智能选品、智能供应链、虚拟试衣",
        "sub_scenes": {
            "personalized_recommendation": {
                "name": "个性化推荐系统",
                "description": "电商千人千面推荐、用户画像、协同过滤+深度学习推荐，GMV提升20-40%",
                "robots": ["用户画像系统", "深度学习推荐模型", "实时特征工程平台", "A/B测试框架", "商品知识图谱"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "smart_store": {
                "name": "智慧门店/无人零售",
                "description": "无人便利店、智能货架、客流分析、商品识别、自助结算，门店运营效率提升50%",
                "robots": ["商品视觉识别摄像头", "RFID智能标签", "自助结算终端", "客流热力分析", "电子价签系统"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
            "ai_supply_chain": {
                "name": "智能供应链/需求预测",
                "description": "销量预测、智能补货、库存优化、物流路径规划，缺货率降低30%库存周转提升",
                "robots": ["时序预测模型", "库存优化引擎", "路径规划算法", "供应链可视化平台", "需求预测系统"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
        },
    },

    # ── AI+餐饮/生活服务 ──
    "ai_food_life_service": {
        "name": "AI+餐饮/生活服务（智能点餐/外卖调度/烹饪机器人）",
        "description": "智能点餐、外卖智能调度、烹饪机器人、送餐机器人、智能后厨管理",
        "sub_scenes": {
            "ai_cooking_robot": {
                "name": "烹饪/炒菜机器人",
                "description": "全自动烹饪机器人、标准化出餐、口味稳定、24小时营业，连锁餐饮标准化核心设备",
                "robots": ["商用烹饪机器人", "自动投料系统", "火候精准控制", "菜谱云端管理", "自动清洁系统"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
            "food_delivery_dispatch": {
                "name": "外卖智能调度",
                "description": "订单智能分派、骑手路径规划、ETA预计送达时间、超时预测，配送效率提升25%",
                "robots": ["实时调度引擎", "路径规划算法", "ETA预测模型", "供需预测系统", "骑手App终端"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
            "smart_restaurant": {
                "name": "智慧餐厅",
                "description": "智能点餐、送餐机器人、智能后厨、刷脸支付、会员智能营销，全流程无人化/少人化",
                "robots": ["送餐机器人", "自助点餐机", "刷脸支付终端", "后厨KDS系统", "会员营销CRM"],
                "difficulty": 2,
                "reward_scale": 0.9,
            },
        },
    },

    # ── AI+法律/司法 ──
    "ai_legal": {
        "name": "AI+法律/司法（智能裁判/法律咨询/合同审查）",
        "description": "智慧法院、智能法律咨询、合同智能审查、类案检索、法律文书生成",
        "sub_scenes": {
            "smart_court": {
                "name": "智慧法院/智能裁判辅助",
                "description": "类案智能推送、裁判文书自动生成、量刑辅助、庭审语音转写，司法效率提升60%",
                "robots": ["裁判文书大模型", "类案检索引擎", "庭审语音识别", "电子卷宗系统", "量刑辅助系统"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "contract_review": {
                "name": "合同智能审查",
                "description": "合同风险点自动识别、条款比对、合规审查、修订建议生成，合同审核效率提升80%",
                "robots": ["NLP合同审查引擎", "法律法规知识库", "风险点识别模型", "条款比对系统", "合同模板库"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "legal_consulting_ai": {
                "name": "智能法律咨询",
                "description": "7x24小时AI法律顾问、问题自动解答、法律条文引用、诉讼流程指引，普惠法律服务",
                "robots": ["法律大模型对话", "法律知识图谱", "案例库检索", "诉讼风险评估", "文书模板生成"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
        },
    },

    # ── AI+媒体/文创/内容生成 ──
    "ai_media_content": {
        "name": "AI+媒体/文创（AIGC内容生成/智能剪辑/数字人）",
        "description": "AIGC文本/图片/视频/3D生成、智能剪辑、AI数字人主播、智能写稿、内容审核",
        "sub_scenes": {
            "aigc_content_generation": {
                "name": "AIGC多模态内容生成",
                "description": "AI文本生成、AI绘画、AI视频生成、AI音乐创作、AI 3D建模，内容生产效率提升10倍",
                "robots": ["文生图大模型", "文生视频大模型", "大语言模型文本生成", "AI音乐生成", "3D资产生成AI"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "ai_digital_human": {
                "name": "AI数字人主播/数字员工",
                "description": "超写实数字人、24小时直播带货、新闻播报、虚拟客服、企业数字员工，降本增效显著",
                "robots": ["超写实数字人渲染", "语音唇形同步", "实时动作驱动", "数字人直播系统", "多语种TTS"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "content_moderation": {
                "name": "AI内容审核",
                "description": "文本/图片/视频/语音多模态内容审核、违规内容识别、色情/暴力/政治敏感自动过滤，准确率99%+",
                "robots": ["多模态大模型审核", "违规内容样本库", "实时审核引擎", "人审复核调度", "举报处理系统"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
        },
    },

    # ── AI+人力资源/招聘 ──
    "ai_hr_recruitment": {
        "name": "AI+人力资源（智能招聘/简历筛选/AI面试）",
        "description": "智能简历筛选、AI视频面试、人岗匹配、员工培训、绩效评估",
        "sub_scenes": {
            "ai_resume_screening": {
                "name": "智能简历筛选/人岗匹配",
                "description": "简历自动解析、JD匹配度评分、人才画像、人岗智能推荐，招聘效率提升70%",
                "robots": ["简历解析NLP", "人岗匹配算法", "人才知识图谱", "ATS招聘管理系统", "简历去重查重"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
            "ai_video_interview": {
                "name": "AI视频面试评估",
                "description": "AI视频面试、表情/语音/语义多维度评估、胜任力模型打分、面试报告自动生成",
                "robots": ["视频面试平台", "微表情识别", "语音情感分析", "胜任力评估模型", "面试报告生成"],
                "difficulty": 4,
                "reward_scale": 1.1,
            },
        },
    },

    # ========== 蚌埠市本地化AI应用场景（用户籍贯·求职加分重点） ==========
    # ── 蚌埠硅基新材料/玻璃工业AI ──
    "bengbu_silicon_based_materials": {
        "name": "蚌埠·硅基新材料/玻璃工业AI（中建材蚌埠玻璃院）",
        "description": "蚌埠中国玻璃工业设计研究院/浮法玻璃新技术国家重点实验室，硅基新材料产业AI应用",
        "sub_scenes": {
            "glass_quality_ai_inspection": {
                "name": "浮法玻璃/超薄玻璃AI质量检测",
                "description": "浮法玻璃生产线AI视觉质检、气泡/结石/划伤缺陷自动识别、0.12mm超薄电子玻璃质量检测，替代人工目检准确率99.5%+",
                "robots": ["工业线阵相机", "AI缺陷检测大模型", "光源照明系统", "实时剔除执行机构", "质量追溯MES系统"],
                "difficulty": 4,
                "reward_scale": 1.4,
            },
            "glass_process_ai_optimization": {
                "name": "玻璃熔窑工艺AI优化控制",
                "description": "玻璃熔窑温度/压力/料方AI智能优化、能耗降低10%+、良品率提升5%、熔窑寿命延长，浮法玻璃工艺核心AI优化",
                "robots": ["熔窑多传感器监测", "工艺参数AI优化引擎", "预测性维护模型", "能耗优化算法", "DCS集散控制系统"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
        },
    },

    # ── 蚌埠淮河水利/智慧淮河 ──
    "bengbu_huaihe_water": {
        "name": "蚌埠·淮河水利AI（智慧淮河/防汛抗旱）",
        "description": "淮河蚌埠段水利AI监测、洪水预报、防汛调度、水质监测、淮河生态保护",
        "sub_scenes": {
            "huaihe_flood_forecast": {
                "name": "淮河洪水预报/防汛AI调度",
                "description": "淮河蚌埠闸以上流域水文监测、AI洪水预报模型、防汛会商决策、闸坝智能调度，防洪减灾核心系统",
                "robots": ["水位/流量传感器网络", "水文AI预报模型", "洪水演进仿真", "防汛会商大屏", "闸坝远程控制系统"],
                "difficulty": 5,
                "reward_scale": 1.5,
            },
            "huaihe_water_quality_monitor": {
                "name": "淮河水质AI在线监测",
                "description": "淮河蚌埠段水质实时监测、污染源溯源AI、蓝藻水华预警、生态流量调度，淮河流域水生态保护",
                "robots": ["水质多参数传感器", "AI水质评价模型", "污染源溯源算法", "视频水面监控", "生态流量调度系统"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
        },
    },

    # ── 蚌埠港/淮河航运枢纽智慧港口 ──
    "bengbu_port_smart": {
        "name": "蚌埠港·淮河航运枢纽智慧港口",
        "description": "蚌埠港千里淮河第一大港，智慧港口建设：集装箱智能调度、船舶AI识别、危险品监管、铁水联运",
        "sub_scenes": {
            "bengbu_port_container_smart": {
                "name": "蚌埠港集装箱智能调度",
                "description": "蚌埠港集装箱堆场智能管理、岸桥/场桥调度、集卡路径优化、铁水联运智能衔接，港口作业效率提升30%",
                "robots": ["港口TOS操作系统", "集装箱OCR识别", "RTG/场桥远程操控", "集卡调度系统", "铁水联运信息平台"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
            "bengbu_port_ship_ai_recognition": {
                "name": "船舶AI识别/危险品智能监管",
                "description": "淮河船舶AIS+视觉AI识别、危险品船舶智能监管、船舶超载/违规停泊自动检测、航道智能监控",
                "robots": ["AIS船舶自动识别", "视频AI船舶检测", "危险品电子围栏", "航道视频监控", "海事执法调度系统"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
        },
    },

    # ── 蚌埠智慧医疗（蚌医一附院/蚌医二附院） ──
    "bengbu_smart_medical": {
        "name": "蚌埠·智慧医疗（蚌医一附院/蚌医二附院）",
        "description": "蚌埠医学院附属医院AI医疗应用：AI影像诊断、智慧病房、互联网医院、智能分诊",
        "sub_scenes": {
            "bengbu_ai_medical_imaging": {
                "name": "AI医学影像辅助诊断",
                "description": "蚌医附院CT/MRI/DR影像AI辅助诊断、肺结节/乳腺癌/眼底病变早筛、影像报告自动生成，诊断效率提升50%",
                "robots": ["医学影像AI诊断系统", "PACS影像归档系统", "病灶检测分割模型", "结构化报告生成", "多学科会诊MDT平台"],
                "difficulty": 5,
                "reward_scale": 1.4,
            },
            "bengbu_smart_hospital_ward": {
                "name": "智慧病房/护理机器人",
                "description": "蚌埠智慧医院建设：生命体征AI监测、护理机器人、智能发药、输液监控、病房智能呼叫",
                "robots": ["生命体征监护仪AI分析", "配送/护理机器人", "智能发药机", "输液监控系统", "病房物联网平台"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
        },
    },

    # ── 蚌埠花鼓灯/文旅AI ──
    "bengbu_culture_tourism_ai": {
        "name": "蚌埠·文旅AI（花鼓灯/双墩遗址/龙子湖）",
        "description": "蚌埠花鼓灯非遗传承AI、双墩遗址数字考古、龙子湖智慧文旅、AI文旅导览",
        "sub_scenes": {
            "huagudeng_intangible_heritage_ai": {
                "name": "花鼓灯非遗AI数字化传承",
                "description": "蚌埠花鼓灯国家级非遗AI动作捕捉、数字人传承、AI教学、虚拟表演、非遗数字化保存",
                "robots": ["动作捕捉系统", "数字人虚拟表演", "AI舞蹈教学", "非遗数字博物馆", "动作生成AI模型"],
                "difficulty": 3,
                "reward_scale": 1.1,
            },
            "bengbu_smart_tourism": {
                "name": "龙子湖/张公山智慧文旅",
                "description": "蚌埠龙子湖/张公山/大明文化园智慧景区：AI导览、客流预测、智能停车、AR实景导航、文创AIGC",
                "robots": ["景区客流热力分析", "AR/VR导览", "智能停车系统", "AI文创生成", "智慧票务系统"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
            "shuangdun_archaeology_ai": {
                "name": "双墩遗址数字考古AI",
                "description": "蚌埠双墩遗址7300年刻画符号AI识别、陶片AI拼接、考古绘图自动化、数字考古复原",
                "robots": ["文物AI三维重建", "刻画符号AI识别", "陶片智能拼接", "考古绘图自动化", "数字考古平台"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
        },
    },

    # ── 蚌埠皖北农业/智慧农业 ──
    "bengbu_smart_agriculture": {
        "name": "蚌埠·皖北智慧农业（怀远石榴/五河螃蟹/固镇花生）",
        "description": "蚌埠皖北农业AI应用：怀远石榴/五河螃蟹/固镇花生特色农产品AI种植/养殖溯源",
        "sub_scenes": {
            "bengbu_crop_ai_monitoring": {
                "name": "粮食/特色农作物AI种植监测",
                "description": "皖北平原小麦/水稻/怀远石榴AI长势监测、病虫害AI识别、精准施肥灌溉、产量预测",
                "robots": ["农业无人机多光谱", "土壤墒情传感器", "病虫害AI识别App", "精准灌溉系统", "产量预测模型"],
                "difficulty": 3,
                "reward_scale": 1.1,
            },
            "bengbu_aquaculture_ai": {
                "name": "五河螃蟹/水产养殖AI",
                "description": "五河螃蟹/沱湖水产AI养殖：水质在线监测、智能投喂、病害预警、溯源区块链",
                "robots": ["水产养殖水质传感器", "AI智能投喂机", "病害预警模型", "区块链溯源系统", "增氧机智能控制"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
        },
    },

    # ── 蚌埠生物化工/丰原集团AI ──
    "bengbu_biochemical_ai": {
        "name": "蚌埠·生物化工AI（丰原集团/生物制造）",
        "description": "蚌埠生物化工产业AI：生物发酵工艺优化、聚乳酸PLA生产AI控制、安全生产监控",
        "sub_scenes": {
            "fermentation_process_ai": {
                "name": "生物发酵工艺AI优化",
                "description": "丰原集团等生物化工企业发酵过程AI控制、菌种筛选AI辅助、工艺参数优化、转化率提升",
                "robots": ["发酵过程多传感器", "工艺参数AI优化", "菌种高通量筛选AI", "DCS控制系统", "安全生产监控"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
        },
    },

    # ── 蚌埠兵器214所/电子信息AI ──
    "bengbu_electronics_214": {
        "name": "蚌埠·兵器214所电子信息AI",
        "description": "中国兵器工业第214研究所（蚌埠）微电子/ MEMS传感器AI检测、军用电子元器件AI筛选",
        "sub_scenes": {
            "mems_sensor_ai_test": {
                "name": "MEMS传感器/微电子AI检测筛选",
                "description": "兵器214所MEMS传感器/军用电子元器件AI自动化测试、缺陷检测、可靠性筛选、良率提升",
                "robots": ["自动化探针台", "AI缺陷视觉检测", "高低温环境试验箱", "可靠性测试系统", "MES生产追溯"],
                "difficulty": 4,
                "reward_scale": 1.3,
            },
        },
    },

    # ── 蚌埠智慧教育（安财/蚌医/蚌院/蚌埠学院） ──
    "bengbu_smart_education": {
        "name": "蚌埠·智慧教育（安徽财经大学/蚌埠医学院/蚌埠学院）",
        "description": "蚌埠高校智慧教育：AI个性化学习、智能阅卷、虚拟仿真实验、智慧校园",
        "sub_scenes": {
            "ai_personalized_learning": {
                "name": "AI个性化学习/智适应教育",
                "description": "蚌埠高校/K12AI智适应学习、知识点掌握度分析、个性化习题推荐、学习路径规划",
                "robots": ["知识图谱学习引擎", "个性化推荐算法", "智能错题本", "学习进度追踪", "在线学习平台"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
            "ai_grading_paper": {
                "name": "AI智能阅卷/作业批改",
                "description": "客观题自动批改、主观题AI评分、英语作文智能批改、试卷分析，教师工作量减少60%",
                "robots": ["OCR试卷识别", "NLP主观题评分", "作文批改引擎", "试卷质量分析", "学情报告生成"],
                "difficulty": 3,
                "reward_scale": 0.9,
            },
        },
    },

    # ── 蚌埠智慧养老/社区服务 ──
    "bengbu_smart_elderly_care": {
        "name": "蚌埠·智慧养老/社区AI服务",
        "description": "蚌埠社区智慧养老：老人健康AI监测、跌倒检测、智能陪伴、居家养老服务调度",
        "sub_scenes": {
            "elderly_health_ai_monitor": {
                "name": "老人健康AI监测/跌倒检测",
                "description": "居家老人生命体征监测、跌倒AI视觉/雷达检测、异常行为预警、紧急呼叫调度",
                "robots": ["毫米波雷达跌倒检测", "智能手环生命体征", "AI视频行为分析", "紧急呼叫系统", "社区养老调度平台"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "elderly_companion_robot": {
                "name": "智能陪伴机器人",
                "description": "老人陪伴机器人、语音聊天、用药提醒、视频通话、精神慰藉，居家养老智能助手",
                "robots": ["陪伴机器人", "语音交互对话", "用药提醒系统", "视频通话终端", "亲情互联App"],
                "difficulty": 3,
                "reward_scale": 1.0,
            },
        },
    },

    # ── 蚌埠智慧城市/交通/政务 ──
    "bengbu_smart_city": {
        "name": "蚌埠·智慧城市整体建设",
        "description": "蚌埠城市大脑、智慧交通、智慧公交、智慧停车、智慧社区、数字蚌埠整体建设",
        "sub_scenes": {
            "bengbu_smart_traffic": {
                "name": "蚌埠智慧交通/信号AI优化",
                "description": "蚌埠市区交通信号灯AI自适应优化、交通拥堵预测、违章AI识别、公交智能调度",
                "robots": ["交通信号AI控制系统", "视频违章识别", "交通流量预测", "公交智能调度", "智慧停车平台"],
                "difficulty": 4,
                "reward_scale": 1.2,
            },
            "bengbu_city_brain": {
                "name": "蚌埠城市大脑/数字蚌埠",
                "description": "蚌埠城市运行指挥中心、数据中台、AI赋能城市治理、12345热线智能升级、数字孪生城市",
                "robots": ["城市运营指挥中心IOC", "数据共享中台", "AI视频分析平台", "数字孪生城市可视化", "事件分拨处置系统"],
                "difficulty": 5,
                "reward_scale": 1.4,
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
