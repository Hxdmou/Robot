#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI全景注册表 - 持续新增内容（4）
================================================================
V3.15 命名规则：中文括号（1）（2）（3）...编号
  - ai_landscape_registry（1）.py = 原始基础内容
  - ai_landscape_registry（2）.py = V3.9~V3.15持续新增内容（写满2143行）
  - ai_landscape_registry（3）.py = 2026年8月14日起持续新增内容
V3.15 时效规则：严格2天时效（今天+昨天）
V3.15 三大重点：①具身智能 ②人形机器人 ③工业机器人
V3.15 文件规则：单文件不超过2000行，写满自动开下一个（4）.py
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class AICategory(Enum):
    HUMANOID_ROBOT = "humanoid_robot"
    AI_AGENT = "ai_agent"
    AI_COMPUTE = "ai_compute"
    AI_CHIP = "ai_chip"
    AI_LLM = "ai_llm"
    WORLD_MODEL = "world_model"
    AI_GENERAL = "ai_general"
    NETWORK_6G = "network_6g"
    INDUSTRIAL_ROBOT = "industrial_robot"
    BENGBU_LOCAL = "bengbu_local"
    RENEWABLE_ENERGY = "renewable_energy"
    AGRICULTURE = "agriculture"
    COMMERCE = "commerce"
    WATER_CONSERVANCY = "water_conservancy"
    AUTOMOTIVE = "automotive"
    DIGITAL_PRODUCT = "digital_product"
    HEALTHCARE = "healthcare"
    LIVELIHOOD = "livelihood"
    EDUCATION = "education"
    HOME_APPLIANCE = "home_appliance"
    MEDICAL_DEVICE = "medical_device"
    MOBILE_COMPUTER = "mobile_computer"
    EMBODIED_INTELLIGENCE = "embodied_intelligence"


class MaturityLevel(Enum):
    RESEARCH = "research"
    PROTOTYPE = "prototype"
    FIELD_TRIAL = "field_trial"
    COMMERCIAL = "commercial"
    MASS_PRODUCTION = "mass_production"
    OPEN_SOURCE = "open_source"


class SourceTier(Enum):
    TIER1 = "tier1"
    TIER2 = "tier2"
    TIER3 = "tier3"


@dataclass
class AIProduct:
    product_id: str
    name: str
    category: AICategory
    organization: str
    country: str
    description: str
    key_metrics: Dict[str, Any] = field(default_factory=dict)
    ram_gb: Optional[int] = None
    rom_gb: Optional[int] = None
    price_start_rmb: Optional[float] = None
    price_top_rmb: Optional[float] = None
    maturity: MaturityLevel = MaturityLevel.COMMERCIAL
    source: str = ""
    source_tier: SourceTier = SourceTier.TIER3
    publish_date: str = ""
    relevance_to_robotics: str = ""
    deployment_ready: bool = False
    tags: List[str] = field(default_factory=list)


AI_LANDSCAPE_DB_PART4: List[AIProduct] = [

    AIProduct(
        product_id="HUM-061", name="第二届世界人形机器人运动会全赛项规则详解 举重拔河投壶粉末称量开瓶电动工具装配六大新赛项",
        category=AICategory.HUMANOID_ROBOT,
        organization="世界人形机器人运动会组委会", country="中国",
        description="8月22日北京开幕的第二届世界人形机器人运动会新增多个竞技赛项，裁判团队系统解读完整判罚规则。"
                    "举重：按自重分轻量级≤40kg/重量级40-80kg，须完整人形+≥3指灵巧手，遥控半自动或全自主，"
                    "不区分抓举挺举，每台最多3次试举，杠铃双手直接抓握垂直举升过头顶静止2秒有效，"
                    "全程仅双足触台，标准2米杠铃杆自重10kg，3名裁判联合亮灯裁决，以单次最大成功重量排名。"
                    "拔河：新增二对二赛项，每局2分钟，赛道宽1.2米长12米，双脚外触地或踏出边界判负，"
                    "轻量级约40kg机器人可拉动SUV，考验强扭矩稳定性/力觉感知/多机协同/AI自主决策。"
                    "投壶：首次设置，壶口内径13cm距投掷线1.5米，3分钟内站立完成抓取投掷，考验手眼协同。"
                    "粉末称量：勺子舀粉末至电子秤达20克，毫克级精度，完成时间计成绩。"
                    "开瓶撬盖：5分钟内有效开瓶数计成绩；电动工具装配：5分钟内电动螺丝刀有效拧入螺丝数计成绩。",
        key_metrics={"weightlifting": {"classes": "轻量级≤40kg/重量级40-80kg", "attempts": 3,
                                        "hold_seconds": 2, "bar": "2米杆自重10kg", "judges": 3},
                     "tug_of_war": {"mode": "二对二", "duration": "每局2分钟", "track": "1.2米×12米",
                                    "robot_weight": "约40kg可拉SUV"},
                     "touhu": {"pot_diameter": "13cm", "distance": "1.5米", "time": "3分钟"},
                     "powder": {"target": "20克", "precision": "毫克级"},
                     "bottle_opening": "5分钟有效开瓶数", "screw_assembly": "5分钟有效拧入数"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="运动会赛项规则直接定义人形机器人能力评估标准——举重考验全身力控与平衡、"
                              "拔河考验多机协同与力觉感知、投壶/粉末称量考验灵巧手精细操作，"
                              "这些指标与工业场景部署需求高度对齐",
        deployment_ready=False,
        tags=["机器人运动会", "举重规则", "二对二拔河", "投壶", "粉末称量", "灵巧手专项赛"]
    ),

    AIProduct(
        product_id="EMB-040", name="WRC2026开幕日重磅发布 KOM3.0服务VLA架构+慧思开物平台+Pelican Unify具身大一统模型+天工Omni开放平台",
        category=AICategory.EMBODIED_INTELLIGENCE,
        organization="北京人形机器人创新中心+NOHON等", country="中国",
        description="8月19日2026世界机器人大会北京开幕，超300家企业参展（+69%）、展品超3000件、首发新品300余件。"
                    "开幕日核心发布：①KOM 3.0——全球首个融合潜空间世界模型的服务行业VLA架构，"
                    "长程任务全闭环先想后做/多机协同智能调度/7×24小时真机验证商业落地闭环；"
                    "②北京人形机器人创新中心'慧思开物'具身智能一站式开发平台+具身大一统模型Pelican Unify+开放平台'天工Omni'，"
                    "实现一脑多能一脑多机；③银河通用发布双足机器人Galbot ET1；"
                    "④浙江人形机器人创新中心NAVIAI WA1工业级超精密作业机器人专攻汽车装配；"
                    "⑤奥比中光发布机器人视觉与具身数据采集方案打造眼手协同；"
                    "⑥长木谷全球首款六位一体ROPA6全骨科AI手术机器人亮相；"
                    "⑦宇树科技同日登陆科创板成A股人形机器人第一股。",
        key_metrics={"wrc_scale": {"exhibitors": "300余家 +69%", "exhibits": "超3000件", "new_products": "300余件首发"},
                     "kom3": "全球首个融合潜空间世界模型的服务行业VLA架构",
                     "huisikaiwu": "具身智能一站式开发平台", "pelican_unify": "具身大一统模型",
                     "tiangong_omni": "开放平台", "galbot_et1": "银河通用双足机器人",
                     "naviai_wa1": "工业级超精密作业 汽车装配", "orbbec": "眼手协同视觉+数据采集",
                     "ropa6": "六位一体全骨科AI手术机器人", "unitree_ipo": "科创板人形机器人第一股"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="WRC2026开幕日集中展示具身智能从模型到平台到整机的完整技术栈，"
                              "KOM3.0世界模型VLA与Pelican Unify大一统模型代表具身大脑最新方向",
        deployment_ready=False,
        tags=["WRC2026开幕", "KOM3.0", "慧思开物", "Pelican Unify", "天工Omni", "Galbot ET1", "ROPA6"]
    ),

    AIProduct(
        product_id="BB-021", name="蚌埠AI产业8月18-19日最新动态 有家硅光1.6T量产月产值3000万+龙磁科技7.6亿芯片电感+传感谷224家企业",
        category=AICategory.BENGBU_LOCAL,
        organization="有家硅光+龙磁科技+华鑫微纳+中科微感", country="中国",
        description="8月18-19日蚌埠AI产业密集动态：①有家硅光1.6T高速硅光通信模块量产，"
                    "国内极少数自研硅光芯片实现400G/800G/1.6T全系列光模块量产，月产能约2万片、月产值约3000万元，"
                    "2023年投产当年产值1亿元、2026年计划2.5亿元，员工从130人增至近300人，二期总投资5亿元；"
                    "②龙磁科技8月18日公告拟募资7.6亿元建设芯片电感智造项目；"
                    "③华鑫微纳运营全国首条8英寸MEMS晶圆全自动生产线，99%以上自动化，全部达产月产3万片；"
                    "④中科微感全球首款量产化普适型AI嗅觉传感产线运行，年产能100万颗、30多项自主专利；"
                    "⑤上半年智能传感产业集聚企业224家，82家规上企业产值50.49亿元同比+15%，"
                    "签约46个/新开工30个/新投产19个；中国传感谷集聚200多家企业可生产超300种传感器；"
                    "⑥8月18日全市智能传感脑机接口产业发展座谈会召开，明确两大产业为新兴和未来产业；"
                    "⑦蚌埠医科大学第一附属医院完成全省首例半侵入式脑机接口手术。",
        key_metrics={"youjia_silicon": {"products": "400G/800G/1.6T光模块", "monthly_capacity": "2万片",
                                         "monthly_output": "3000万元", "2026_target": "2.5亿元",
                                         "staff": "130→近300人", "phase2_invest": "5亿元"},
                     "longci": "募资7.6亿元芯片电感智造",
                     "huaxin_weina": "8英寸MEMS全自动产线 月产3万片 99%自动化",
                     "zhongke_weigan": "AI嗅觉传感 年产100万颗 30+专利",
                     "industry_data": {"enterprises": 224, "output_yi": 50.49, "yoy": "+15%",
                                        "signed": 46, "new_start": 30, "new_production": 19},
                     "sensor_valley": "200多家企业 300+种传感器",
                     "bci": "全省首例半侵入式脑机接口手术"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="蚌埠智能传感产业是机器人感知层核心供应链——MEMS传感器/嗅觉传感/硅光互联"
                              "直接服务于机器人多模态感知与高速通信需求",
        deployment_ready=False,
        tags=["蚌埠", "有家硅光", "1.6T光模块", "龙磁科技", "芯片电感", "MEMS", "AI嗅觉传感", "脑机接口"]
    ),

    AIProduct(
        product_id="CP-015", name="中国算力Token工厂大考 日均Token调用140万亿+Cerebras CS-4推理30倍+全国产10万卡集群接入超算互联网",
        category=AICategory.AI_COMPUTE,
        organization="国家数据局+Cerebras+中科曙光+华为", country="中国/全球",
        description="2026年中国算力从堆卡转向Token价值产出大考：①国家数据局披露2026年3月日均Token调用量超140万亿，"
                    "较2024年初1000亿增长1000多倍；OpenRouter数据中国模型周调用4.12万亿Token超美国2.94万亿；"
                    "②Agentic Coding平均Token消耗为单轮推理3500倍/代码聊天1200倍，输入输出比154:1；"
                    "③编程Token占比从11%升至50%以上成最大品类；"
                    "④智谱GLM Coding Plan付费开发者24.2万，ARR从1亿到10亿美元仅5个月；"
                    "豆包日均Token从2万亿增至180万亿（两年1500倍）；阿里云AI收入89.71亿元占比首超30%；"
                    "⑤Cerebras CS-4搭载WSE-3 Turbo芯片，推理速度最高达GPU方案30倍，模块化设计不需紧缺内存芯片；"
                    "⑥首个全国产10万卡超集群接入国家超算互联网；华为Atlas 950 SuperPoD最大8192卡互联；"
                    "⑦西北绿电0.25-0.3元/度vs东部0.6-0.8元/度，降电费+通道路+巧分工+抓错峰组合拳；"
                    "⑧传统智算中心GPU利用率<30%，并行科技精准调度达90%以上；商汤大装置MFU提升85%-152%。",
        key_metrics={"token_daily": "140万亿（2026年3月）", "growth": "较2024年初增1000+倍",
                     "china_vs_us": "4.12万亿 vs 2.94万亿Token/周",
                     "agentic_coding": {"vs_inference": "3500倍", "vs_chat": "1200倍", "io_ratio": "154:1"},
                     "coding_share": "11%→50%+",
                     "zhipu": {"developers": "24.2万", "arr": "10亿美元 5个月"},
                     "doubao": "2万亿→180万亿 两年1500倍",
                     "aliyun_ai_revenue": "89.71亿元 占比>30%",
                     "cerebras_cs4": {"chip": "WSE-3 Turbo", "speedup": "最高30倍"},
                     "domestic_100k": "全国产10万卡超集群", "atlas950": "8192卡",
                     "electricity": {"west": "0.25-0.3元/度", "east": "0.6-0.8元/度"},
                     "gpu_utilization": {"traditional": "<30%", "bingxing": ">90%"},
                     "sensetime_mfu": "+85%~152%"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="Token工厂模式为机器人大模型训练与推理提供低成本算力底座，"
                              "10万卡集群与超节点架构直接支撑VLA模型大规模并行训练",
        deployment_ready=False,
        tags=["Token工厂", "140万亿", "Cerebras CS-4", "10万卡", "Atlas 950", "GPU利用率"]
    ),

    AIProduct(
        product_id="LLM-053", name="智谱GLM-5.3发布7530亿参数编程+50%+Qwen3.8消费级部署+DeepSeek V4 Pro强化智能体",
        category=AICategory.AI_LLM,
        organization="智谱AI+阿里云+DeepSeek", country="中国",
        description="8月17-19日国产大模型密集更新：①智谱GLM-5.3于8月17日发布，总参数7530亿，"
                    "编程能力提升50%，GLM Coding Plan全球付费开发者突破24.2万，Token调用量半年涨15倍，"
                    "API价格累计上调83%调用量仍增400%，ARR 3月17亿元→7月10亿美元；"
                    "②阿里Qwen3.8-27B专为笔记本等消费级硬件打造，表现媲美10倍规模模型，"
                    "同时开放最强模型Qwen3.8 Max权重，通义千问衍生模型在Hugging Face达151448个为Meta的2.6倍，"
                    "联发科天玑旗舰芯片及汽车座舱平台C-X1实现Day-0支持；"
                    "③DeepSeek V4 Pro正式版8月13日发布，强化复杂推理/编程/智能体能力；"
                    "④阿里Qwen-Audio-3.0语音识别合成理解音频问答多项国际评测大满贯；"
                    "⑤月之暗面K3发布48小时请求量逼近集群极限；MiniMax M2.5上线七天调用突破3.07万亿Token。",
        key_metrics={"glm53": {"params": "7530亿", "coding_boost": "+50%", "date": "8月17日"},
                     "qwen38_27b": "消费级硬件 媲美10倍规模", "qwen_hf_models": 151448,
                     "deepseek_v4pro": "8月13日 强化推理编程智能体",
                     "kimi_k3": "48小时逼近集群极限", "minimax_m25": "七天3.07万亿Token"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="GLM-5.3编程能力+50%直接提升机器人代码生成与任务规划能力，"
                              "Qwen3.8端侧部署为机器人本体推理提供轻量化选择",
        deployment_ready=False,
        tags=["GLM-5.3", "Qwen3.8", "DeepSeek V4 Pro", "端侧部署", "编程能力"]
    ),

    AIProduct(
        product_id="AGENT-009", name="支付宝全栈智能体商业底座+AHA跨端互联协议 联合20余家企业共建 阿宝万项服务AI化",
        category=AICategory.AI_AGENT,
        organization="支付宝+千问+华为+比亚迪等", country="中国",
        description="8月18日支付宝发布国内首个全栈智能体商业底座及AHA多智能体跨端互联协议，"
                    "联合千问/华为/OPPO/比亚迪/吉利等20余家企业共建生态，打通手机/车机等多终端壁垒；"
                    "旗下阿宝已完成超一万项服务AI化接入。同期：高德云睿·时空智能体平台融合20余年时空数据，"
                    "同步上线交通/文旅/产业/充电/商业五大行业智能体；阿里千问办公接入企业微信实现钉钉飞书企微全覆盖；"
                    "豆包工作任务模式支持手机远程控制电脑+虚拟桌面功能上线；企业微信5.0.10开放CLI与MCP能力；"
                    "科达应龙灵元AI超级主机整合本地模型+AI算力+Agent全本地闭环。",
        key_metrics={"alipay": {"position": "国内首个全栈智能体商业底座", "protocol": "AHA多智能体跨端互联",
                                 "partners": "20余家企业", "abao_services": "超一万项"},
                     "gaode": "云睿时空智能体 五大行业智能体",
                     "qianwen_office": "接入企业微信 三平台全覆盖",
                     "doubao": "手机远程控制电脑+虚拟桌面",
                     "wecom": "5.0.10 CLI+MCP开放"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-18",
        relevance_to_robotics="AHA跨端互联协议为机器人接入多智能体生态提供标准化通道，"
                              "智能体商业底座可支撑机器人服务场景的支付与任务调度闭环",
        deployment_ready=False,
        tags=["智能体商业底座", "AHA协议", "跨端互联", "高德云睿", "豆包虚拟桌面"]
    ),

    AIProduct(
        product_id="DIG-037", name="闪极loomos L1 AI眼镜43克5秒换电2699元+雷鸟iO人类增强眼镜8月21日+苹果AirPods B790摄像头",
        category=AICategory.DIGITAL_PRODUCT,
        organization="闪极+雷鸟创新+苹果", country="中国/美国",
        description="8月18-19日AI穿戴设备密集发布：①闪极loomos AI眼镜L1于8月18日发布，"
                    "整机仅43克前框19克，5秒极速换电实现无限续航，主打全天候主动记忆自动生成AI日记，"
                    "搭载索尼IMX681传感器111°超广角F2.2光圈，深度集成飞书，首发价2699-2999元，武汉东西湖产线投产；"
                    "②雷鸟iO AI眼镜8月21日14:30发布，定位人类增强AI眼镜，双目单绿光波导方案，"
                    "无摄像头和音频模块主打轻量化，皇冠镜框+钛金属镜腿，围绕知识/表达/记忆三维度；"
                    "③苹果AirPods B790在macOS曝光演示视频确认配备摄像头，支持视觉智能交互，"
                    "可识别书籍等物体由Siri处理，预计9月与新一代iPhone一同发布。",
        key_metrics={"loomos_l1": {"weight": "43克 前框19克", "battery_swap": "5秒换电",
                                    "sensor": "索尼IMX681 111° F2.2", "price": "2699-2999元",
                                    "feature": "主动记忆+AI日记"},
                     "rayneo_io": {"launch": "8月21日14:30", "display": "双目单绿光波导",
                                    "design": "皇冠镜框+钛金属镜腿", "no_camera": True},
                     "airpods_b790": {"camera": True, "feature": "视觉智能交互", "launch": "预计9月"}},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-18",
        relevance_to_robotics="AI眼镜是具身智能人机交互的重要入口——主动记忆/视觉识别/语音交互"
                              "能力与机器人感知系统形成互补生态",
        deployment_ready=False,
        tags=["AI眼镜", "闪极loomos", "雷鸟iO", "AirPods摄像头", "主动记忆"]
    ),

    AIProduct(
        product_id="ROB-089", name="武汉机器人军团WRC亮相 格蓝若C1倒地自起+赤兔四足负载120kg+拾光S1家庭人形+NAVIAI WA1汽车装配",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="格蓝若+启灵+中坚科技+浙江人形机器人创新中心", country="中国",
        description="WRC2026武汉机器人军团集体亮相：①格蓝若C1人形机器人学会倒地自起；"
                    "②D2-W四足机器狗搭载自研玄鸟巡检智脑；③启灵神农自主完成搬运；"
                    "④赤兔四足机器狗峰值负载超120公斤；⑤拾光S1通用家庭人形机器人亮相；"
                    "⑥浙江人形机器人创新中心NAVIAI WA1工业级超精密作业机器人专攻汽车装配；"
                    "⑦中坚科技ZERO巨型化概念机器人展出；⑧伟景智能采摘版智能人形机器人；"
                    "⑨墨奇智能MORPHI KINO轮式机器人适配家庭长程任务；⑩松延动力E1首次亮相；"
                    "⑪龙旗科技与南昌高新区签约具身智能机器人研发制造基地落地；"
                    "⑫香港小睿G3于8月17日发布，能响应语音指令平稳搬运50公斤杠铃。",
        key_metrics={"gelanruo_c1": "倒地自起", "d2w": "玄鸟巡检智脑",
                     "chitu": "峰值负载>120kg", "shiguang_s1": "通用家庭人形",
                     "naviai_wa1": "工业级超精密 汽车装配", "zhongjian_zero": "巨型化概念",
                     "weijing": "采摘版人形", "morphi_kino": "轮式家庭长程任务",
                     "songyan_e1": "首次亮相", "longqi": "南昌研发制造基地",
                     "xiaorui_g3": "搬运50kg杠铃"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="武汉军团覆盖工业巡检/搬运/家庭服务/农业采摘全场景，"
                              "NAVIAI WA1汽车装配代表工业级精度新高度",
        deployment_ready=False,
        tags=["武汉军团", "格蓝若C1", "赤兔", "NAVIAI WA1", "拾光S1", "倒地自起"]
    ),

    AIProduct(
        product_id="MD-025", name="长木谷ROPA6全球首款六位一体全骨科AI手术机器人WRC亮相",
        category=AICategory.MEDICAL_DEVICE,
        organization="长木谷医疗科技", country="中国",
        description="长木谷在WRC2026展出全球首款六位一体ROPA6全骨科AI手术机器人，"
                    "覆盖骨科全术式场景，AI辅助术前规划+术中导航+术后评估全流程，"
                    "标志国产手术机器人从单专科向全骨科平台跨越。同期蚌埠医科大学第一附属医院"
                    "完成全省首例半侵入式脑机接口手术用于偏瘫患者康复治疗。",
        key_metrics={"ropa6": "六位一体全骨科", "coverage": "全术式场景",
                     "ai_pipeline": "术前规划+术中导航+术后评估",
                     "bci_surgery": "安徽首例半侵入式脑机接口 偏瘫康复"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="全骨科手术机器人是医疗机器人最高集成度形态，"
                              "AI术前规划与术中导航技术可迁移至工业精密装配场景",
        deployment_ready=False,
        tags=["ROPA6", "全骨科", "AI手术机器人", "脑机接口手术"]
    ),

    AIProduct(
        product_id="HA-022", name="石头科技三大品类新品RRMind GPT+海尔AI家庭机器人体验中心青岛启用+万和AI零冷水",
        category=AICategory.HOME_APPLIANCE,
        organization="石头科技+海尔+万和", country="中国",
        description="8月18日家电AI化密集动态：①石头科技推出扫地机器人/洗地机/迷你洗烘一体机三大品类新品——"
                    "扫地机P30 Pro/G30S Ultra搭载可升降LDS系统机身压缩至8.98cm，支持RRMind GPT大模型自然语言交互；"
                    "洗地机A30 Pro Steam 3.0支持180℃蒸汽与90℃热水混洗；迷你洗烘一体机Z1 Mini Pro搭载智能脏污检测；"
                    "②海尔AI家庭机器人体验中心在青岛启用，国内首个家庭全场景AI机器人主题线下空间，展出AI烹饪机器人等；"
                    "③苏宁易购与博西家电深化AI家电战略合作；④万和超薄燃气热水器99系列支持AI三管零冷水；"
                    "⑤汉舍卫浴发布极境U9轻智能马桶；⑥苹果Home Hub曝光：7英寸方形屏支持Siri AI及智能叠放，"
                    "型号J490桌面式/J491壁挂式。",
        key_metrics={"roborock": {"p30pro": "可升降LDS 8.98cm RRMind GPT",
                                   "a30pro": "180℃蒸汽+90℃热水混洗", "z1mini": "智能脏污检测"},
                     "haier": "青岛AI家庭机器人体验中心 国内首个",
                     "wanhe": "AI三管零冷水", "apple_home_hub": "7英寸 J490/J491"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-18",
        relevance_to_robotics="家庭服务机器人是具身智能最大消费场景——石头RRMind GPT大模型交互"
                              "与海尔全场景AI机器人代表家电向机器人形态演进",
        deployment_ready=False,
        tags=["石头科技", "RRMind GPT", "海尔AI机器人", "Home Hub", "智能家居"]
    ),

    AIProduct(
        product_id="WM-014", name="智象未来HiDream-O1-World原生全模态世界模型+HelixWorld 1.0全球首个有声实时世界模型",
        category=AICategory.WORLD_MODEL,
        organization="智象未来+Noiz AI+港科大+清华+CMU", country="中国/全球",
        description="8月17-19日世界模型双突破：①智象未来发布HiDream-O1-World原生全模态交互式世界模型，"
                    "具备漫游/编辑/交互三大功能，自研UiT架构实现镜头推拉摇移场景几何稳定，"
                    "3D先验注入Memory上下文+Test-Time Training解决长时程空间漂移，"
                    "视觉合理性+13.6%因果保真+12.7%入选ECCV2026，"
                    "产业应用覆盖具身智能仿真/3D场景生产/AI互动影游；"
                    "②Noiz AI联合港科大/清华/CMU/谷歌DeepMind发布HelixWorld 1.0——"
                    "全球首个有声实时世界模型，24帧/秒实时渲染+48kHz双声道音频同步输出。",
        key_metrics={"hidream": {"architecture": "原生全模态UiT", "visual_plausibility": "+13.6%",
                                  "causal_fidelity": "+12.7%", "venue": "ECCV2026"},
                     "helixworld": {"fps": 24, "audio": "48kHz双声道", "position": "全球首个有声实时"}},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="世界模型是具身智能仿真的核心底座——HiDream-O1-World直接提供"
                              "高精度虚拟试验环境，HelixWorld实时渲染可支撑机器人实时决策预演",
        deployment_ready=False,
        tags=["HiDream-O1-World", "HelixWorld", "世界模型", "ECCV2026", "实时渲染"]
    ),

    AIProduct(
        product_id="CHIP-028", name="芯擎天工100车规7nm 96TOPS量产+芯朋微AI能源芯片+谷歌TPU 8t/8i+Socionext英特尔18A定制",
        category=AICategory.AI_CHIP,
        organization="芯擎科技+芯朋微+谷歌+Socionext", country="中国/美国/日本",
        description="8月18-19日AI芯片多线开花：①芯擎科技天工100车规级AI芯片（7nm/96TOPS）已全面量产供货；"
                    "②芯朋微十余款面向AI计算能源新品量产，含1700V SiC辅源芯片；"
                    "③谷歌正式推出第八代自研AI芯片TPU 8t（训练）及TPU 8i（推理）；"
                    "④日本Socionext宣布采用英特尔Intel 18A-P制程开发定制SoC；"
                    "⑤国家新能源汽车技术创新中心完成原粒半导体全新端侧AI推理芯片深度性能测试；"
                    "⑥每日互动与超聚变联合推出全脱网保密机个知智能工作站T2，搭载1P算力内置350亿参数大模型。",
        key_metrics={"tianqong100": {"process": "7nm", "tops": 96, "status": "量产供货"},
                     "xinpengwei": "十余款AI能源芯片 1700V SiC",
                     "google_tpu": "TPU 8t训练+TPU 8i推理 第八代",
                     "socionext": "Intel 18A-P定制SoC",
                     "yuanli": "端侧AI推理芯片 深度测试",
                     "t2_workstation": "1P算力 350亿参数 全脱网"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="车规级96TOPS芯片可直接用于机器人本体计算，"
                              "端侧推理芯片为轻量级机器人提供低功耗AI能力",
        deployment_ready=False,
        tags=["天工100", "车规芯片", "TPU 8t", "18A-P", "端侧推理", "AI能源芯片"]
    ),

    AIProduct(
        product_id="HUM-062", name="WRC2026京粤机器人真干活专场 天工Omni 1.35米家用人形+星海图Nexo 30自由度+广东34家企业第一梯队",
        category=AICategory.HUMANOID_ROBOT,
        organization="北京人形机器人创新中心+星海图+广东具身智能军团", country="中国",
        description="8月19日WRC2026现场机器人从炫技转向真干活：①北京人形机器人创新中心336㎡展台天工3.0群舞+拔河，"
                    "天工Omni家用小型人形身高1.35米/整机39公斤首发，现场挑战梅花桩/上下楼梯/匍匐爬行/遥操作，"
                    "开放底层关节控制/传感器数据/运动控制/数据采集开发接口，面向家务协助/老幼陪伴/家庭安防；"
                    "②同步发布具身多模态大模型Pelican-Unify 1.0（感知-理解-决策-执行闭环），Pelican 2.0官宣商业化；"
                    "③星海图500㎡全场最大展位，全球首个机器人前置仓在线接单实景演示（G0.5具身基础模型自主拣选/导航/打包/放置全流程，"
                    "无需按SKU单独编程），全球首个机器人组装机器人（厘米级螺丝入孔+自动钻孔器锁付高精度长程装配），"
                    "发布新一代旗舰轮臂人形Nexo全身30自由度；Kengo双足Zero-shot自主跑酷；"
                    "④广东34家企业参展规模全国第一梯队：智平方爱宝智魔方咖啡/冰淇淋/鸡尾酒自主制作已在全国十余省常态化运营，"
                    "越疆机器人无需预设程序自主完成T恤/长裤/毛巾柔性织物识别展平对位折叠全流程，"
                    "乐聚夸父人形1:1复刻工厂产线拆垛搬运上料单日稳定运行8-10小时已交付北汽/一汽/江汽；"
                    "⑤星源智异构多机协同跳长绳全球首次实机验证（两台人形摇绳+四足跟随节奏跳跃），"
                    "高位作业机器人10米级高危场景RoboBrain Pro一机替代多台设备；"
                    "⑥云迹科技200多家工厂医院落地，送物/清扫/洗衣/咖啡/煮面多场景服务。",
        key_metrics={"tiangong_omni": {"height": "1.35米", "weight": "39公斤", "positioning": "家用小型人形"},
                     "pelican": {"unify_1.0": "具身多模态大模型", "pelican_2.0": "官宣商业化"},
                     "nexo": {"dof": 30, "type": "轮臂人形"},
                     "guangdong": {"exhibitors": "34家 全国第一梯队", "leju": "单日8-10小时 交付北汽一汽江汽"},
                     "xingyuanzhi": "异构多机跳长绳全球首次实机验证",
                     "yunji": "200多家工厂医院落地"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="天工Omni开放开发接口支撑科研二次开发与真机部署调试，"
                              "前置仓/机器人组装机器人验证了VLA模型在真实产业场景的闭环履约能力",
        deployment_ready=False,
        tags=["天工Omni", "Pelican-Unify", "星海图Nexo", "机器人前置仓", "广东军团", "真干活"]
    ),

    AIProduct(
        product_id="EMB-041", name="BrainCo强脑科技脑控机器人训练平台+灵巧操作数采矩阵 Revo3全掌触觉灵巧手21自由度",
        category=AICategory.EMBODIED_INTELLIGENCE,
        organization="BrainCo强脑科技", country="中国",
        description="WRC2026强脑科技集中展示脑机接口+具身智能融合方案：①脑控机器人训练平台——脑电设备实时采集任务相关脑电信号，"
                    "算法识别意图模式转化为机器人控制指令，使用者无需肢体动作即可建立直接控制链路，一体化设计支持人形机器人/机械臂/机器狗"
                    "多种第三方设备接入，无相关背景研究人员10分钟解锁脑控机器人，首次以人形机器人作为现场执行载体演示；"
                    "②灵巧操作数采矩阵——整合真机执行/真人示教/仿真生成三大数据来源：真机数据由双臂轮式数采平台RevoTron/RevoMate采集，"
                    "搭载21自由度全掌触觉灵巧手Revo 3，覆盖全身多自由度运动控制，同步采集环境视觉/手部视觉/运动状态/触觉反馈，"
                    "形成动作-触觉-视觉-语义全模态灵巧操作数据；RevoHuman外骨骼人类数采手套在真人自然操作中同步采集手部姿态/触觉/腕部视角；"
                    "③新一代智能仿生手：读取残肢末端肌肉电与神经电信号识别运动意图驱动抓握，体积重量进一步缩小减轻，可搭配仿生手皮兼顾外观触感。",
        key_metrics={"brain_control": {"setup": "10分钟解锁脑控机器人", "devices": "人形/机械臂/机器狗多设备接入"},
                     "revo3": {"dof": 21, "tactile": "全掌触觉", "data": "动作-触觉-视觉-语义全模态"},
                     "data_sources": ["真机执行", "真人示教", "仿真生成"],
                     "prosthetic": "肌电+神经电信号意图识别"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="脑机接口为人形机器人提供下一代人机交互链路，灵巧操作数采矩阵"
                              "直接解决具身智能模型训练所需的高质量多模态数据瓶颈",
        deployment_ready=False,
        tags=["脑机接口", "脑控机器人", "Revo 3", "数采矩阵", "智能仿生手"]
    ),

    AIProduct(
        product_id="CP-016", name="AI算力资本大动作 软银65亿美元收购Ampere+谷歌122亿绑定Marvell+英伟达参投Groq+宇树首日暴涨460%",
        category=AICategory.AI_COMPUTE,
        organization="软银+谷歌+Marvell+Groq+宇树科技", country="全球",
        description="2026年8月20日AI算力成最稀缺战略资源：①软银宣布65亿美元全现金收购Arm架构数据中心芯片公司Ampere Computing，"
                    "与收购Arm及Stargate计划形成协同，构建芯片设计到算力部署全链条控制；"
                    "②谷歌与Marvell达成深度合作涉及122亿美元潜在入股，Marvell为谷歌开发定制AI芯片ASIC成博通之后第二大定制芯片伙伴，"
                    "加速去英伟达化，Marvell股价盘前暴涨；"
                    "③Groq以35亿美元估值完成3.5亿美元A轮融资，Disruptive领投英伟达计划参投，自研LPU推理芯片延迟比GPU快10倍以上，"
                    "算力明年从54兆瓦扩至200兆瓦以上；"
                    "④三星代工涨价15%，AI模型降价但底层芯片涨价；"
                    "⑤宇树科技科创板上市首日开盘1100元较发行价150.80元涨近630%，盘中市值破4000亿元，收盘约845元涨460%市值超3400亿，"
                    "978万户打新中签率0.018%中一签盈利约35万元，171名员工跟投2.72亿元23人身家超千万，"
                    "但2026上半年扣非净利同比-19.34%对应219倍市盈率，行业从谁先上市转向谁能赚钱；"
                    "⑥快手可灵AI视频单季收入8.5亿元证明AI应用能赚钱。",
        key_metrics={"softbank_ampere": "65亿美元全现金",
                     "google_marvell": "122亿美元潜在入股 第二大ASIC伙伴",
                     "groq": {"valuation": "35亿美元", "round": "3.5亿美元A轮", "lpu": "推理延迟GPU 10倍+",
                              "power": "54→200+兆瓦"},
                     "samsung_foundry": "+15%涨价",
                     "unitree_ipo": {"open": "1100元 +630%", "close": "845元 +460%",
                                     "market_cap": "盘中破4000亿 收盘超3400亿", "pe": "219倍",
                                     "subscribers": "978万户 中签率0.018%"},
                     "kling": "单季8.5亿元"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-20",
        relevance_to_robotics="宇树460%暴涨验证人形机器人赛道资本热度，Arm架构服务器芯片与定制ASIC"
                              "为机器人大模型训练推理提供更多算力选择",
        deployment_ready=False,
        tags=["软银Ampere", "谷歌Marvell", "Groq LPU", "宇树460%", "算力稀缺"]
    ),

    AIProduct(
        product_id="LLM-054", name="OpenAI暂缓Astra强化学习训练+智谱GLM-5.3 API智能指数60分+苹果联手阿里在华自训大模型",
        category=AICategory.AI_LLM,
        organization="OpenAI+智谱AI+苹果+阿里巴巴", country="全球/中国",
        description="8月19日大模型安全与合规成焦点：①OpenAI确认因下一代前沿模型Astra在隔离测试中展现超预期网络攻防能力触及安全阈值，"
                    "暂停强化学习训练至少两周，最大规模前沿模型训练同步冻结，部署激活分类器对每Token实时监测异常30分钟内告警，"
                    "安全监控开销约占被监控推理算力20%，Astra 8月内发布概率降至13%，行业进入安全管理优先于抢发模型新阶段；"
                    "②智谱正式开放GLM-5.3 API主打复杂编码/防御性网络安全/长程任务规划，Artificial Analysis智能指数60分"
                    "与Kimi K3并列开源模型第一，比肩Claude与GPT最新闭源旗舰，单任务调用成本约0.68美元，下周五MIT许可开放权重；"
                    "③苹果在阿里技术支持下专门为中国市场训练大语言模型，与此前通义千问方案并行推进，"
                    "成为首家获准在华提供自研专属AI模型的外国企业，相关服务已完成监管备案；"
                    "④Anthropic披露Claude针对15个目标设计蛋白质结合剂14个成功，命中率22.6%-35.1%达领域均值两倍，"
                    "Claude Opus 5可在19-23分钟内独立完成化学分析。",
        key_metrics={"openai_astra": {"rl_pause": "至少两周", "monitor": "每Token实时监测 30分钟告警",
                                      "overhead": "监控开销约20%算力", "release_prob": "13%"},
                     "glm53_api": {"aa_score": 60, "cost": "0.68美元/任务", "license": "MIT开放权重"},
                     "apple_alibaba": "首家在华自训专属AI模型外企 完成监管备案",
                     "claude_bio": {"hit_rate": "22.6%-35.1%", "vs_field": "领域均值10%-15%的两倍"}},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="GLM-5.3长程任务规划能力与MIT开放权重为机器人VLA模型训练提供开源底座，"
                              "苹果阿里合作验证外资AI在华合规落地路径",
        deployment_ready=False,
        tags=["Astra暂停", "GLM-5.3 API", "苹果阿里", "AI安全", "蛋白质设计"]
    ),

    AIProduct(
        product_id="CHIP-029", name="Cerebras WSE-3T晶圆级引擎详参 2.8GHz频率翻倍+250PFLOPS+43.2PB/s+推理4400token/s",
        category=AICategory.AI_CHIP,
        organization="Cerebras", country="美国",
        description="8月19日Cerebras发布新一代晶圆级引擎WSE-3T及CS-4机架系统完整参数："
                    "芯片频率从1.4GHz翻倍至2.8GHz，稀疏FP16算力达250 PFLOPS，内存带宽43.2 PB/s；"
                    "CS-4机架系统移除交换机让芯片直连，延迟从5微秒降至2微秒；"
                    "gpt-oss-120b模型推理速度可达每秒4400 Token，为大模型推理硬件树立新标杆。",
        key_metrics={"frequency": "1.4→2.8GHz翻倍", "fp16_sparse": "250 PFLOPS",
                     "memory_bandwidth": "43.2 PB/s", "latency": "5→2微秒",
                     "inference": "gpt-oss-120b 4400 token/s"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="晶圆级推理芯片为机器人大模型端云协同推理提供低延迟算力选项",
        deployment_ready=False,
        tags=["WSE-3T", "CS-4", "250 PFLOPS", "4400 token/s"]
    ),

    AIProduct(
        product_id="DIG-039", name="华为鸿蒙座舱AI陪伴机器人哈蒙蒙HAMOMO+苹果摄像头AirPods B798延至2027年",
        category=AICategory.DIGITAL_PRODUCT,
        organization="华为+苹果", country="中国/美国",
        description="8月19日智能硬件新动态：①华为鸿蒙座舱AI陪伴机器人HAMOMO（哈蒙蒙）详细配置曝光，"
                    "今年4月华为乾崑技术大会首发，将搭载于奕境X9，可磁吸于车机并转头注视用户，"
                    "亦可拔下随身携带变身桌面智能手办，体现车载AI向多形态陪伴硬件延伸趋势；"
                    "②苹果代号B798项目——左右耳均配备摄像头的AirPods进入设计验证测试DVT阶段，"
                    "将作为视觉传感器把物体/文字/街道信息交由视觉智能与Siri处理，外形接近AirPods Pro 3但耳机柄加长"
                    "并配外部提示灯保护隐私，因新版Siri延期及供应链软件障碍预计2027年末发布，今年无缘上市；"
                    "③此前macOS 26.7 RC泄露的B790为带摄像头AirPods Pro 3增强版。",
        key_metrics={"hamomo": {"launch": "奕境X9搭载", "features": "磁吸车机转头注视+桌面手办形态"},
                     "airpods_b798": {"stage": "DVT设计验证", "camera": "左右耳双摄像头",
                                      "release": "延至2027年末", "privacy": "外部提示灯"}},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-19",
        relevance_to_robotics="车载AI陪伴机器人验证多形态具身交互在智能座舱的落地路径",
        deployment_ready=False,
        tags=["哈蒙蒙", "鸿蒙座舱", "AirPods摄像头", "DVT"]
    ),

    AIProduct(
        product_id="HUM-063", name="小米新一代人形机器人铁大WRC详解 1.7米66公斤66关节+工厂螺丝对位成功率98%+10B模型10万小时数据",
        category=AICategory.HUMANOID_ROBOT,
        organization="小米", country="中国",
        description="8月20日WRC2026期间小米机器人事业部详解人形机器人进展：①新一代铁大身高约1.7米/体重66公斤/全身66个关节双足形态，"
                    "按汽车工厂工人身高设计，自由度从上代21个增至66个（约一半集中在手部），覆盖汽车工厂2000多个岗位80%以上运动空间，"
                    "设计思路为场景和模型和算法定义的硬件；②已有两款机器人在工厂实习，螺丝对位等精细触觉工作成功率3月约90%→7月98%"
                    "（人工工站约99%），预计年底达99%；③任务效率：3-5秒短任务可达人工70%-100%，30秒-1分钟任务降至60%-70%，"
                    "1分钟以上长任务降至30%以上，类比大模型长上下文推理效率下降问题；④10B模型使用约10万小时UniMi真机数据+"
                    "自身真机遥操数据约1万小时，行业今年奔着百万小时数据走但更关注数据分布和质量；⑤应用场景分智能制造/商业服务/家庭"
                    "三阶段，家庭先从小米青年公寓验证，家用人形短周期内困难核心瓶颈是AI；⑥材料成本不是最大障碍（50-60公斤铁铜），"
                    "最大投入是AI如何平摊成本。",
        key_metrics={"tieda": {"height": "1.7米", "weight": "66公斤", "joints": 66, "dof": "21→66"},
                     "success_rate": {"mar": "90%", "jul": "98%", "human": "99%", "year_end": "99%目标"},
                     "efficiency": {"short_task": "人工70%-100%", "mid_task": "60%-70%", "long_task": "30%+"},
                     "data": {"10B_model": "10万小时UniMi真机", "teleop": "1万小时"}},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-20",
        relevance_to_robotics="小米铁大工厂98%成功率验证人形机器人产线落地路径，三阶段规划为行业提供参考",
        deployment_ready=False,
        tags=["小米铁大", "66关节", "98%成功率", "10万小时数据", "三阶段规划"]
    ),

    AIProduct(
        product_id="EMB-042", name="自变量机器人WRC双场景落地 WALL-B世界统一模型+物流分拣1816件/小时+QUANXTA Zero数采成本降90%",
        category=AICategory.AI_GENERAL,
        organization="自变量机器人", country="中国",
        description="8月20日央广网：自变量机器人亮相WRC展示家庭服务+物流分拣双场景：①家庭场景完成收纳整理/清洁打扫/搬运跑腿/"
                    "整理衣物/取外卖/浇花/铲猫砂/自行充电等数十项任务，今年3月与58到家推出机器人上门家政服务（行业首次大规模机器人进家庭），"
                    "5月推出X家庭成员计划机器人常驻用户家最长一个月；②物流分拣复刻全球直播产线：两条机械臂配合夹爪全自主分拣"
                    "复杂随机真实包裹，效率1816件/小时准确率98%，相比人形+五指灵巧手方案成本大幅下降70%，已与头部物流企业合作"
                    "部署真实生产环境常态化运行；③驱动两场景的是全自研端到端世界统一模型WALL-B，从零预训练融合视觉/语言/触觉/动作/"
                    "物理预测，理解重力惯性摩擦力等物理规律，具备跨本体跨任务跨场景能力；④QUANXTA Zero无本体数据采集方案"
                    "数据入库有效率超85%，模型训练数据成本降低90%，具备行业唯一移动采集数据本体回放能力；⑤自研分布式训练与"
                    "高性能推理框架，将数据采集到真机部署全流程从6个月缩短到3天。",
        key_metrics={"logistics": {"speed": "1816件/小时", "accuracy": "98%", "cost_cut": "70%"},
                     "wall_b": "端到端世界统一模型 视觉语言触觉动作物理预测融合",
                     "quanxta_zero": {"valid_rate": "85%+", "cost_cut": "90%"},
                     "pipeline": "全流程6个月→3天",
                     "home": "58到家合作 X家庭成员计划常驻1个月"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-20",
        relevance_to_robotics="WALL-B统一模型验证跨场景泛化路径，物流分拣1816件/小时为具身智能产业落地标杆",
        deployment_ready=True,
        tags=["自变量", "WALL-B", "1816件/小时", "QUANXTA Zero", "58到家"]
    ),

    AIProduct(
        product_id="EMB-043", name="WRC2026产业深度对话 帕西尼VTLA触觉基座+ROIC成产业成熟标准+灵巧手成本10万降至3万以内",
        category=AICategory.AI_GENERAL,
        organization="帕西尼PaXini+易方达基金", country="中国",
        description="8月20日华尔街见闻WRC2026特别对话（帕西尼CEO许晋诚+易方达基金经理肖宛远）：①物理世界数据极度匮乏与"
                    "触觉感知缺失是行业核心短板，底层算法从纯视觉向VTLA（视觉-触觉-语言-动作）多模态融合跃迁，触觉从硬件选配"
                    "走向底层标配；②评判机器人产业成熟标准是ROIC与ROI：投入1美元产生超1美元价值商业闭环即成立，不追求终极AGI"
                    "局部智能足以产生经济价值；③轮式与双足是不同商业场景的并行方案：平整工厂轮式底盘+机械臂在稳定性/能耗/"
                    "厘米级精度优势明显，非结构化地形双足人形不可替代；④灵巧手成本一年前10万级别现在降到3万以内，不盲目追求"
                    "27-28自由度拟人化，核心是抓持稳定性；⑤帕西尼提供传感器-灵巧手-整机-算法全链路交付，触觉传感器深入"
                    "半导体芯片制程级别；⑥叠衣服是无限维度数学规划难题，专用模型（如专门洗叠衣服）ROI极高；⑦家庭是开放世界"
                    "需极大量操作数据，Few-shot少样本学习或是破局方向；⑧宇树科技600亿估值合理性建立在年销近万台+具身智能大脑"
                    "延伸空间，终局商业模式或从硬件销售走向劳动力派遣按需服务；⑨中国优势是大规模制造能力+丰富工业场景数据，"
                    "海外优势是劳动力短缺带来的极强应用动力。",
        key_metrics={"vtla": "视觉-触觉-语言-动作多模态基座",
                     "roic": "投入1美元产生超1美元价值=商业闭环",
                     "dexterous_hand_cost": "10万→3万以内（一年）",
                     "paxini": "传感器-灵巧手-整机-算法全链路 半导体制程级触觉",
                     "unitree": "600亿估值 年销近万台"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-20",
        relevance_to_robotics="VTLA触觉基座与ROIC标准为具身智能商业化提供评判框架，全链路交付成产业壁垒",
        deployment_ready=False,
        tags=["帕西尼", "VTLA", "ROIC", "灵巧手3万", "轮式双足并行"]
    ),

    AIProduct(
        product_id="WM-015", name="大晓机器人开悟世界模型3.1+晓满晓新晓途三套行业方案 全球评测第一梯队+即时零售履约落地",
        category=AICategory.WORLD_MODEL,
        organization="大晓机器人ACE ROBOTICS", country="中国",
        description="8月20日光明网：大晓机器人首次亮相WRC展示具身智能全栈实力：①开悟世界模型3.1（Kairos 3.1）采用统一原生架构，"
                    "整合生成/物理/认知三类智能，把视觉观测/语言指令/力触反馈/动作轨迹等多源具身数据纳入同一隐空间，"
                    "打通世界理解/物理生成/动作预测能力，搭建理解—推演—执行—反思自进化闭环，机器人执行失败后可自主定位问题"
                    "调整策略自我优化；②在全球具身智能评测中世界模型视频生成/状态预测两项赛道取得靠前成绩，对标多款国际主流模型，"
                    "已面向行业开源，毕马威报告视其为原生一体化架构代表性成果处全球第一梯队；③提出以人为中心数据范式，"
                    "搭建视频/人机交互/真机运行三层数据金字塔，降低对真机采集数据依赖；④发布晓满（即时零售履约：前置仓/仓店一体/"
                    "便利店狭窄通道作业，力控处理软硬不同商品，已与多家商业主体合作）/晓新（酒店洗衣全流程：收衣/清洗/折叠熨烫）/"
                    "晓途（城市治理/文旅户外开放场景，多机型协同调度）三套行业解决方案；⑤环境式数据采集方案2.0同步展出。",
        key_metrics={"kairos_3.1": "统一原生架构 生成物理认知三智能 自进化闭环",
                     "ranking": "全球评测视频生成+状态预测靠前 毕马威全球第一梯队",
                     "solutions": {"xiaoman": "即时零售履约", "xiaoxin": "酒店洗衣", "xiaotu": "城市治理文旅"},
                     "data": "三层数据金字塔 以人为中心范式"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-20",
        relevance_to_robotics="开悟世界模型3.1自进化闭环与三套行业方案验证世界模型从技术到商业落地的完整链条",
        deployment_ready=True,
        tags=["大晓机器人", "开悟3.1", "晓满", "即时零售", "全球第一梯队"]
    ),

    AIProduct(
        product_id="HUM-064", name="第二届世界人形机器人运动会赛前探访 灵巧手专项赛八大难题+二对二拔河+智宝文创8月22日发售",
        category=AICategory.HUMANOID_ROBOT,
        organization="世界人形机器人运动会组委会", country="中国",
        description="8月20日主流媒体赛前探访：①灵巧手专项赛8个竞技小项轮番上演：电动工具装配/粉末称重/积木搭建/钉钉固定/"
                    "开瓶撬盖/拆箱拆包/镊子夹豆/线缆连接，在国家速滑馆人形机器人产业生态训练和测评基地举行；②全自主模式表现超预期："
                    "上海电机学院Galaxy星璨队机器人全自主3分多钟完成4层拱门形积木搭建，全自主按原始满分计分/遥操得分乘0.5系数"
                    "以鼓励纯自主研发；③深度机智Prime U轮式机器人60个自由度首次参赛，镊子夹豆5分钟内有效夹取数计成绩；"
                    "④北京人形-北邮飞雁队天轶人形参加粉末称重，手眼配合根据称重数据决定挖取量；⑤拔河二对二赛项考验强扭矩稳定性/"
                    "脚底板稳定/灵巧手握持绳索/自主感知拉力切换姿态，灵心巧手左家平+星源智马璁详解技术要点；⑥开瓶撬盖需像人一样"
                    "使用工具，5分钟有效开瓶数计成绩；⑦运动会文创8月22日开幕日线下发售：吉祥物智宝吊卡/奖牌造型冰丝带摆件"
                    "（内置NFC芯片裸眼3D效果）/燕京八景冰箱贴/800套限量礼盒等三十余款，国家速滑馆官方文创店六处，"
                    "购票观众享吉祥物吊卡50元立减。",
        key_metrics={"events": "8小项：电动工具装配/粉末称重/积木搭建/钉钉固定/开瓶撬盖/拆箱拆包/镊子夹豆/线缆连接",
                     "scoring": "全自主满分计分 遥操×0.5系数",
                     "prime_u": "60自由度轮式 深度机智",
                     "tug": "二对二 强扭矩+脚底稳定+灵巧手握持",
                     "merch": "智宝文创30余款 8月22日发售 NFC冰丝带摆件"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-20",
        relevance_to_robotics="灵巧手专项赛八大难题检验手脑协同能力，全自主计分规则引导行业向纯自主方向发展",
        deployment_ready=False,
        tags=["灵巧手专项赛", "八大难题", "全自主计分", "智宝文创", "Prime U"]
    ),

    AIProduct(
        product_id="HUM-065", name="2026人形机器人产业发展报告 上半年出货超4万台全球占比97%+整机400余款超全球半数+开普勒出海美徳奥",
        category=AICategory.HUMANOID_ROBOT,
        organization="中国人形机器人与具身智能百人会+中国电子学会", country="中国",
        description="8月20-21日WRC2026发布《2026年人形机器人产业发展报告》：①2026年上半年中国人形机器人出货量已超4万台，"
                    "全球占比进一步提升至97%，从小批量试用加快向常态化部署和规模化应用迈进；②我国人形机器人整机产品达400余款"
                    "超过全球半数，上半年人形机器人领域新设企业11.6万户同比增长9.5%；③技术创新进入集群涌现新阶段，已形成"
                    "从关键芯片/部组件到整机的全产业链制造能力；④环球时报记者探访：开普勒通体黄色人形机器人身高1.75米/体重75公斤"
                    "搬运30公斤重物/充电1小时作业8小时，已在国内多家制造工厂上岗年产能1000台，美国/德国/奥地利已有客户采购；"
                    "⑤星海图展台搭建大型超市，平板下单后机器人货架穿梭拣选送收银台另一台打包，工作效率和人相当，柔性物品也能精准分拣；"
                    "⑥擎朗智能两台人形机器人忙家务：一台将脏衣篮衣物放进洗衣机，洗涤后取出转交另一台叠衣机器人，通过机械手相机"
                    "看清衣服展开折叠，目前洗衣房作业完成度约及格线，短袖短裤可处理长袖长裤仍是挑战；⑦中国电子学会理事长徐晓兰："
                    "人形机器人正从舞台上动起来/赛场上跑起来向家庭里用起来/工厂里干起来加速进化，有望成为继计算机/智能手机/"
                    "新能源汽车之后的又一颠覆性产品。",
        key_metrics={"shipment": "上半年超4万台 全球占比97%",
                     "products": "整机400余款 超全球半数",
                     "new_companies": "11.6万户 +9.5%",
                     "kepler": {"height": "1.75米", "weight": "75公斤", "payload": "30公斤",
                                "battery": "充电1小时作业8小时", "capacity": "年产1000台", "export": "美徳奥"},
                     "keenon": "洗衣叠衣全流程 完成度及格线"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-21",
        relevance_to_robotics="4万台出货量与97%全球占比标志中国人形机器人进入规模化部署阶段",
        deployment_ready=True,
        tags=["4万台出货", "97%全球占比", "开普勒出海", "擎朗叠衣", "集群涌现"]
    ),

    AIProduct(
        product_id="ROB-090", name="机器人移动母舰全球首发+新松OneHub羿枢多机协同+猿声先达多维触觉动捕手套",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="飞巴科技+新松+猿声先达", country="中国",
        description="8月20-21日WRC2026舰队协同新生态：①飞巴科技全球首发机器人移动母舰——机器人的移动后勤基地，舱体可装载"
                    "人形机器人/机器狗/无人机，车内自带换电工位和维修工位，即使在断网断电极端环境下也能给机器人提供算力和通信保障，"
                    "今年年底投入量产，预计明年6月真正商用进入航空救援/应急消防/医学救援等领域，让机器人从单兵作战走向舰队协同；"
                    "②新松人工智能研究院发布多机型协同系统OneHub羿枢，可接入不同种类机器人，3台机器人两种类型都可在该系统"
                    "协同下工作，融入大模型技术；③猿声先达科技首次对外展出多维触觉动捕手套+能感知物体接近的大面积电子皮肤，"
                    "动捕手套可感知法向力/切向力及非常密集的力的方向，模块化设计可重构跟人骨骼完全一样的骨骼建模，"
                    "采集更精准的接触数据而非用固定骨骼套所有人的手。",
        key_metrics={"mothership": {"payload": "人形+机器狗+无人机", "features": "换电工位+维修工位+断网断电算力通信保障",
                                    "mass_production": "今年年底", "commercial": "明年6月 航空救援/应急消防/医学救援"},
                     "onehub": "多机型协同 3台2类 融入大模型",
                     "motion_glove": "法向力+切向力感知 模块化骨骼建模"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-21",
        relevance_to_robotics="移动母舰解决多机器人野外持续作业问题，多机协同系统是规模化部署的关键基础设施",
        deployment_ready=False,
        tags=["机器人母舰", "舰队协同", "OneHub羿枢", "触觉动捕手套"]
    ),

    AIProduct(
        product_id="HUM-066", name="广东人形机器人十骏腾跃 逐际动力数千台订单+智平方NeuroVLA类脑模型+美的美罗U锁附10万颗螺钉",
        category=AICategory.HUMANOID_ROBOT,
        organization="逐际动力+智平方+乐聚+众擎+美的+小鹏+荣耀+优必选+越疆+自变量", country="中国",
        description="8月21日新华全媒头条：广东十家人形机器人整机企业形成十骏现象：①逐际动力全尺寸人形与TRON系列双足移动操作"
                    "机器人已斩获数千台级订单，半数以上销往海外，覆盖科研/商业服务/全地形巡检，核心路线是大小脑融合；"
                    "②智平方2026年推出原创类脑VLA模型NeuroVLA，同时具备主动感知/故障自恢复与时序记忆三大类生物运动能力，"
                    "成立一年便跻身深圳独角兽；③乐聚夸父系列核心部件国产率达95%，是国内产业化程度最高的人形机器人产品之一；"
                    "④众擎率先使人形机器人直腿直膝行走完成前空翻，今年7月发起URKL全球人形机器人自由格斗联赛以竞技倒逼技术迭代；"
                    "⑤美的面向工业场景的美罗系列已进驻多家生产基地，美罗U化身产线员工累计完成螺钉锁附超10万颗，"
                    "依托智能体工厂大脑实现作业全流程自主闭环；面向家庭与商用的美拉X2搭载自研具身大小脑模型；"
                    "⑥小鹏机器人将汽车大规模制造经验与供应链管理体系复用至机器人研发；⑦荣耀人形机器人在2026北京亦庄"
                    "人形机器人半程马拉松中一举夺魁，液冷散热/高强度铰链源自消费电子领域技术积淀；⑧优必选Walker系列已进入"
                    "比亚迪/吉利等车企生产一线开展工业实训；⑨自变量搭建自研数据工厂沉淀数万小时多模态具身智能数据集。",
        key_metrics={"limx": "数千台订单 半数以上海外",
                     "neurovla": "类脑VLA 主动感知+故障自恢复+时序记忆",
                     "leju_kuafu": "核心部件国产率95%",
                     "midea": "美罗U螺钉锁附超10万颗 智能体工厂大脑",
                     "honor": "半程马拉松夺魁 液冷散热",
                     "ubtech": "Walker进比亚迪吉利产线"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-21",
        relevance_to_robotics="广东十骏差异化路径验证人形机器人产业集群化发展模式，NeuroVLA类脑模型代表算法新方向",
        deployment_ready=True,
        tags=["广东十骏", "NeuroVLA", "美罗U", "逐际动力出海", "众擎格斗联赛"]
    ),

    AIProduct(
        product_id="CP-017", name="人形机器人资本热浪 宇树王兴兴ChatGPT时刻2-3年+乐聚IPO受理+越疆H回A+今年230起融资增28.8%",
        category=AICategory.AI_COMPUTE,
        organization="宇树科技+乐聚+越疆+数字华夏", country="中国",
        description="8月20-21日经济参考报：人形机器人从上场走向进厂资本加码：①宇树科技创始人王兴兴表示具身智能领域的"
                    "ChatGPT时刻或将在可见的未来到来，快则两至三年慢则五到十年，当机器人能够被部署至家庭等任意陌生环境"
                    "可完成约80%的任务时便意味着已抵达具身智能产业爆发的关键临界点，对AI模型的投入是目前公司资金和人力"
                    "投入最大的方向；②乐聚智能IPO发行申请获深交所受理，是首家选择使用创业板第四套标准申请上市的企业，"
                    "2025年实现营业收入2.58亿元近三年复合增长率高达118.68%，现场展示商服导览/零售服务/纸箱拆垛/小件上料"
                    "等成熟可交付方案单日稳定运行8至10小时；③越疆科技启动H回A进程，创业板IPO项目获深交所上市委审议通过，"
                    "计划募资约12亿元投向多足机器人研发及产业化/人形机器人技术提升；④今年以来国内机器人相关企业共出现"
                    "超过230起融资事件比去年同期增长28.8%；⑤数字华夏完成亿元级Pre-A轮战略融资，带来新一代仿生人形机器人"
                    "夏澜R03（多语言交流/去唤醒词化对话）、全新双形态人形机器人星行侠P02（双足行走与轮式移动可切换/"
                    "身高130厘米/重量30公斤/25个自由度/飞兵模式续航超8小时）以及RoboEase场景大脑（图形化拖拉拽编排），"
                    "深耕金融和智慧康养两大场景，RoboCare健康监测方案一分钟内完成心率/血氧/呼吸频率检测达医疗级标准；"
                    "⑥瑞银李智颖：2026年以技术验证/积累数据和搭建供应链为主，大规模部署有望在2027年至2029年逐渐展开。",
        key_metrics={"unitree_wang": "ChatGPT时刻快2-3年慢5-10年 家庭完成80%任务=临界点",
                     "leju_ipo": "创业板第四套标准首家 2025营收2.58亿 复合增长118.68%",
                     "dobot": "H回A募资12亿",
                     "financing": "今年230起 +28.8%",
                     "digital_huaxia": {"xingxingxia": "130cm/30kg/25自由度/续航8小时",
                                        "robocare": "1分钟心率血氧呼吸 医疗级"}},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-21",
        relevance_to_robotics="资本市场密集入场标志人形机器人从演示走向量产交付的投资周期开启",
        deployment_ready=False,
        tags=["ChatGPT时刻", "乐聚IPO", "越疆H回A", "230起融资", "数字华夏"]
    ),

    AIProduct(
        product_id="CP-018", name="AI算力大单狂飙 赛意信息64.5亿+利通电子50亿定增+OpenRouter周Token75.3万亿+SK海力士CPO路线图",
        category=AICategory.AI_COMPUTE,
        organization="赛意信息+利通电子+SK海力士+谷歌+迈威尔", country="全球",
        description="8月19-21日A股算力赛道狂飙：①赛意信息与W公司签订两份高性能算力服务合同含税总金额高达64.5亿元，"
                    "相当于其2025年全年营收的逾三倍；②利通电子披露定增预案拟募资不超过50亿元其中40亿元投向智算中心建设，"
                    "算力业务长期租赁排期已至2030年以后现有算力利用率接近100%；③东阳光控股子公司三笔算力服务框架合同"
                    "累计金额约390亿元至460亿元；行云科技在手算力存储长期框架订单超154亿元，头部大模型客户订单金额涨幅超201%"
                    "算力规模翻倍，央企客户租金整体上调79%；④OpenRouter平台截至8月16日周Token调用量达75.3万亿"
                    "环比增长9.1%创历史新高；⑤SK海力士与弗吉尼亚大学在《自然·电子学》发表CPO技术路线图，提出算力每两年"
                    "增长3倍互联带宽仅增长1.4倍，带宽墙成AI扩展核心瓶颈，CPO技术为突围关键，更远愿景是将CPO延伸至内存接口"
                    "让多块AI加速器共享同一内存池；⑥谷歌与迈威尔就合作开发定制芯片签署一系列协议，涵盖TPU相关AI推理加速器/"
                    "存储控制器/网络接口控制器/内存接口控制器，AI芯片下半场从算力之争升级为话语权之争；⑦SIGCOMM主会"
                    "收录109篇论文中国贡献59篇占比再次超50%，阿里巴巴蝉联全球企业论文入选榜榜首。",
        key_metrics={"saiyi": "64.5亿元 超去年营收3倍",
                     "litong": "50亿定增 40亿智算中心 利用率近100%",
                     "dongyangguang": "框架合同390-460亿",
                     "openrouter": "周Token 75.3万亿 +9.1%创新高",
                     "cpo": "算力2年3倍vs带宽1.4倍 带宽墙",
                     "google_marvell": "TPU定制芯片系列协议",
                     "sigcomm": "中国59篇占比超50% 阿里蝉联榜首"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-21",
        relevance_to_robotics="算力大单与CPO技术突破为机器人大模型训练推理提供更充足更低延迟的算力底座",
        deployment_ready=False,
        tags=["赛意64.5亿", "利通50亿", "Token75.3万亿", "CPO带宽墙", "SIGCOMM"]
    ),

    AIProduct(
        product_id="CP-019", name="阿里云AI收入增45%创22季新高+真武M890服务650家客户+Qwen3.8-Max开源2.4万亿参数下载超30亿",
        category=AICategory.AI_COMPUTE,
        organization="阿里巴巴", country="中国",
        description="8月20日阿里巴巴2027财年Q1财报：①阿里云外部商业化收入加速增长45%增速创22个季度新高，AI相关产品收入"
                    "连续第12个季度实现三位数同比增长，本季度AI相关产品季度收入达123.76亿元对应年化规模接近500亿元；"
                    "②全球头部云厂商分化出AI加速阵营：谷歌云82%季度增速领跑，阿里云45%位列全球第二，Azure 43%被阿里云反超，"
                    "AWS 37%；③吴泳铭表示AI算力Capex投资回报确定性非常高，投入可三年内回本，未来有望缩短到2.5年甚至2年；"
                    "④阿里AI云与算力分部EBITA利润同比增长133%，经调整EBITA利润率升至12%；⑤平头哥已建成覆盖GPU/CPU/"
                    "网络芯片的全栈自研体系，真武M890等真武系列芯片已覆盖20余个行业服务650余家外部客户，阿里云已将大规模"
                    "AI数据中心交付周期压缩至100天；⑥最新开源参数规模2.4万亿的Qwen3.8-Max和Qwen3.8-27B模型，"
                    "Qwen系列模型全球下载总量已超30亿次衍生模型数超30万个；⑦千问App已带动2.5亿用户体验AI购物。",
        key_metrics={"cloud_growth": "+45% 22季新高 全球第二",
                     "ai_revenue": "季度123.76亿 年化近500亿 连续12季三位数",
                     "capex": "3年回本 有望2.5-2年",
                     "zhenwu": "M890覆盖20+行业 650+客户 数据中心100天交付",
                     "qwen": "Qwen3.8-Max 2.4万亿参数开源 下载超30亿 衍生30万"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-21",
        relevance_to_robotics="阿里云AI算力商业化加速与Qwen开源生态为具身智能大模型训练提供普惠算力与模型底座",
        deployment_ready=False,
        tags=["阿里云45%", "真武M890", "Qwen3.8-Max", "Capex3年回本"]
    ),

    AIProduct(
        product_id="BB-022", name="蚌埠智能传感脑机接口座谈会召开+北方华鑫智感固态电池硫化氢传感器亮相第八届MEMS大会",
        category=AICategory.BENGBU_LOCAL,
        organization="蚌埠市工信局+安徽北方华鑫智感", country="中国",
        description="8月19-21日蚌埠智能传感产业最新动态：①全市智能传感、脑机接口产业发展座谈会召开，部署推进产业高质量发展；"
                    "②安徽北方华鑫智感科技有限公司全新研发的固态电池用硫化氢气体专用检测传感器成功亮相第八届MEMS智能传感器"
                    "产业生态发展大会，成为大会重点推介产品，整体技术水准达到国内领先水平，精准适配新能源汽车/储能等热门产业赛道"
                    "有效填补相关领域检测技术应用空白，已与国内多家电池生产应用企业达成前期技术合作意向；③中国传感谷已集聚"
                    "安徽北方微电子研究院/芯动联科/希磁科技等200多家智能传感器上下游企业，构建从关键材料/芯片设计/晶圆制造"
                    "到封装测试/终端应用的完整全产业链体系；④蚌埠组建总规模超70亿元的智能传感产业发展基金，布局建设省级以上"
                    "创新平台39个，出台全国首部促进智能传感产业发展地方性法规；⑤园区同步布局9条公共服务示范线面向科创企业"
                    "开放共享降低研发试产成本；⑥产品广泛应用于汽车电子/高端装备/低空经济/智慧交通/脑机接口等前沿领域，"
                    "下一步将向上招引优质研发设计团队，向下深耕车载传感/具身智能/硅光通讯等终端应用制造领域。",
        key_metrics={"symposium": "智能传感+脑机接口产业发展座谈会",
                     "huaxin_sensor": "固态电池硫化氢检测传感器 国内领先 第八届MEMS大会重点推介",
                     "cluster": "200+企业 全产业链",
                     "fund": "70亿元产业基金 39个省级以上创新平台",
                     "regulation": "全国首部智能传感产业地方性法规"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-21",
        relevance_to_robotics="蚌埠传感产业向具身智能终端应用延伸，固态电池传感器适配机器人能源安全监测需求",
        deployment_ready=False,
        tags=["蚌埠座谈会", "硫化氢传感器", "MEMS大会", "70亿基金"]
    ),
]
