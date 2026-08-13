#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI全景注册表 - V1.1
================================================================
新增内容：
  1. AICategory（19大类别枚举）
  2. MaturityLevel（成熟度枚举）
  3. SourceTier（来源等级枚举）
  4. AIProduct（产品数据类）
  5. AI_LANDSCAPE_DB（产品数据库）
  6. AILandscapeRegistry（查询注册表类）
  7. get_ai_landscape_registry（单例获取函数）

类别名称列表：
  HUMANOID_ROBOT / AI_AGENT / AI_COMPUTE / AI_CHIP / AI_LLM /
  WORLD_MODEL / AI_GENERAL / NETWORK_6G / INDUSTRIAL_ROBOT / BENGBU_LOCAL /
  RENEWABLE_ENERGY / AGRICULTURE / COMMERCE / WATER_CONSERVANCY /
  AUTOMOTIVE / DIGITAL_PRODUCT / HEALTHCARE / LIVELIHOOD / EDUCATION
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


class MaturityLevel(Enum):
    RESEARCH = "research"
    PROTOTYPE = "prototype"
    FIELD_TRIAL = "field_trial"
    COMMERCIAL = "commercial"
    MASS_PRODUCTION = "mass_production"


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
    maturity: MaturityLevel = MaturityLevel.RESEARCH
    source: str = ""
    source_tier: SourceTier = SourceTier.TIER3
    publish_date: str = ""
    relevance_to_robotics: str = ""
    deployment_ready: bool = False
    tags: List[str] = field(default_factory=list)


AI_LANDSCAPE_DB: List[AIProduct] = [
    # ==================================================================
    # 类别1：AI人型机器人最新进展
    # ==================================================================
    AIProduct(
        product_id="HR-001", name="中国人形机器人加速进厂",
        category=AICategory.HUMANOID_ROBOT,
        organization="中国机器人企业", country="中国",
        description="中国人形机器人聚焦重物搬运和经济生产场景，"
                    "单台承重最高50公斤；中国正快速建设专用机器人训练中心，部分机器人已在"
                    "药店等商业场景承担拣选配送。摩根士丹利预计2050年全球人形机器人保有量"
                    "可达10亿台，潜在市场规模超5万亿美元；中国目前制造全球约90%的人形机器人",
        key_metrics={"max_payload_kg": 50, "global_share_pct": 90,
                     "market_2050_usd_tn": 5, "installed_2050_bn": 1.0},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="直接相关：人形机器人工业部署竞赛，汽车制造/物流/电子组装率先应用",
        deployment_ready=True,
        tags=["人形机器人", "进厂", "承重", "训练中心"],
    ),
    AIProduct(
        product_id="HR-002", name="上半年中国人形机器人出货量占全球97%",
        category=AICategory.HUMANOID_ROBOT,
        organization="智元机器人/宇树科技", country="中国",
        description="2026年上半年全球人形机器人出货量约1.91万台，是去年同期"
                    "5100台的三倍多；中国制造商出货量占全球97%以上。智元机器人出货8400台"
                    "占44%登顶，宇树科技5900台占31%，均远超特斯拉、Figure AI、Agility Robotics",
        key_metrics={"global_shipments_h1": 19100, "china_share_pct": 97,
                     "zhiyuan_units": 8400, "zhiyuan_share_pct": 44,
                     "unitree_units": 5900, "unitree_share_pct": 31,
                     "yoy_growth_x": 3},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="直接相关：中国人形机器人量产能力全球领先",
        deployment_ready=True,
        tags=["出货量", "智元", "宇树", "量产"],
    ),
    AIProduct(
        product_id="HR-003", name="全球首个具身智能并线生产落地",
        category=AICategory.HUMANOID_ROBOT,
        organization="智元机器人（南昌智能终端工厂）", country="中国",
        description="在江西南昌智能终端设备生产工厂，四名人形机器人与传统量产化产线并线生产，"
                    "稳定完成流水线取料、高精度放置全闭环操作，可自主发现产线位置偏差并重新放置。"
                    "每台完成一道工序约18秒，每小时约300件，整体作业成功率98.5%以上，"
                    "无需定制专用工具即可快速适配不同型号产品",
        key_metrics={"cycle_time_s": 18, "pieces_per_hour": 300,
                     "success_rate": 0.985, "location": "南昌"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-04-15",
        relevance_to_robotics="直接相关：人形机器人进入工业产线常态化部署标杆",
        deployment_ready=True,
        tags=["并线生产", "工业落地", "全闭环", "南昌"],
    ),

    # ==================================================================
    # 类别2：AI智能体最新进展
    # ==================================================================
    AIProduct(
        product_id="AG-001", name="Manus恢复独立运营剑指通用Agent",
        category=AICategory.AI_AGENT,
        organization="Manus", country="新加坡/全球",
        description="8月12日Manus宣布即将恢复以独立公司形式运营，继续为全球数百万用户服务，"
                    "并筹备一系列新功能拓展通用AI智能体能力边界。7月以来已更新4项功能："
                    "7月9日对话分支Branch、7月13日网站自动发布Auto-Publish、"
                    "7月14日智能PPT生成、7月22日先规划后执行的Plan Mode",
        key_metrics={"users_mn": "millions", "features_july": 4,
                     "features": ["Branch", "Auto-Publish", "PPT", "Plan Mode"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="相关：通用Agent的规划-执行模式可迁移至机器人任务编排",
        deployment_ready=True,
        tags=["通用Agent", "Manus", "Plan Mode", "独立运营"],
    ),
    AIProduct(
        product_id="AG-002", name="千问开放平台上线 三类终端Agent接入",
        category=AICategory.AI_AGENT,
        organization="阿里巴巴（千问）", country="中国",
        description="8月10日千问开放平台正式上线，面向生态伙伴和开发者开放手机、PC、AI眼镜"
                    "三类终端的AI智能体接入能力。首批伙伴覆盖物流、房产、本地生活、理财、"
                    "汽车等十多个领域，包括顺丰速运、自如租房、盈米基金、哈啰租车、闪送等。"
                    "用户一句话即可调用第三方服务完成下单支付全流程",
        key_metrics={"terminals": ["phone", "pc", "ai_glasses"],
                     "partners": 10, "ai_services": 400},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-10",
        relevance_to_robotics="相关：多终端Agent调度与履约闭环架构可借鉴",
        deployment_ready=True,
        tags=["千问", "开放平台", "AI眼镜", "履约闭环"],
    ),
    AIProduct(
        product_id="AG-003", name="Grok Bot开启常驻员工测试",
        category=AICategory.AI_AGENT,
        organization="xAI", country="美国",
        description="xAI推出Grok Bot早期测试，让云端智能体拥有独立计算环境，可跨网站、"
                    "应用与工具持续执行流程并相互协作。首批仅向部分高阶订阅用户开放",
        key_metrics={"compute_env": "isolated_cloud", "access": "premium_tier"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-12",
        relevance_to_robotics="相关：常驻自主智能体是机器人长期自主运行的参考范式",
        deployment_ready=False,
        tags=["Grok Bot", "常驻智能体", "独立计算环境"],
    ),
    AIProduct(
        product_id="AG-004", name="智能体规范应用与创新发展实施意见",
        category=AICategory.AI_AGENT,
        organization="国家网信办/发改委/工信部", country="中国",
        description="三部门联合印发《智能体规范应用与创新发展实施意见》，明确智能体是具备"
                    "自主感知、记忆、决策、交互与执行能力的智能系统，提出科学研究、产业发展、"
                    "民生福祉等19个典型应用场景，智能体发展实现有规可依",
        key_metrics={"scenarios": 19, "agencies": 3},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-05-26",
        relevance_to_robotics="相关：政策框架为机器人智能体合规落地提供依据",
        deployment_ready=True,
        tags=["政策", "智能体规范", "19个场景"],
    ),

    # ==================================================================
    # 类别3：AI算力最新进展
    # ==================================================================
    AIProduct(
        product_id="CP-001", name="远景星河基地全球最大AI算力超级单体投产",
        category=AICategory.AI_COMPUTE,
        organization="远景科技集团", country="中国-内蒙古乌兰察布",
        description="内蒙古乌兰察布"
                    "'远景星河基地'正式投产。超级单体建筑面积12万平方米（约20个标准足球场），"
                    "拥有百万卡并行能力和百万P算力规模，是全球Token产出能力最强的单体AI数据中心，"
                    "园区总规划容量2GW。乌兰察布绿电占比67%，算力输出达同等面积传统数据中心10倍",
        key_metrics={"area_sqm": 120000, "gpu_scale": "million_card",
                     "compute_pflops": "million_P", "total_capacity_gw": 2,
                     "green_power_pct": 67, "density_x": 10},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="核心基础设施：百万卡集群为VLA大模型训练提供国产算力底座",
        deployment_ready=True,
        tags=["算力超级单体", "百万卡", "绿电", "东数西算", "乌兰察布"],
    ),
    AIProduct(
        product_id="CP-002", name="曙光8000登峰全国产十万卡AI超集群落成",
        category=AICategory.AI_COMPUTE,
        organization="中科曙光/海光信息", country="中国-郑州",
        description="中科曙光宣布中国首个全国产"
                    "十万卡AI超集群——曙光8000（登峰）正式落成，同步接入国家超算互联网。"
                    "海光CPU与DCU已应用于十万卡集群，支持10万亿参数大模型训练，"
                    "已提供400+主流模型线上推理服务",
        key_metrics={"gpu_scale": 100000, "domestic_chip": True,
                     "models_served": 400, "max_model_params_tn": 1.0},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-07-11",
        relevance_to_robotics="核心基础设施：全国产算力支撑大模型与机器人策略训练",
        deployment_ready=True,
        tags=["十万卡", "全国产", "海光", "超算互联网"],
    ),
    AIProduct(
        product_id="CP-003", name="英伟达筹建5000亿美元AI算力融资平台",
        category=AICategory.AI_COMPUTE,
        organization="NVIDIA/Apollo/BlackRock等", country="美国",
        description="8月11日英伟达与Apollo、黑石、贝莱德GIP、Brookfield、高盛、KKR等"
                    "六家机构签署合作备忘录，计划建立独立算力融资平台，长期动员逾5000亿美元"
                    "第三方资本建AI工厂。黄仁勋称GPU是'可抵押融资的可投资资产'，"
                    "AI算力加速金融化",
        key_metrics={"target_capital_usd_bn": 500, "partners": 6},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-11",
        relevance_to_robotics="基础设施：全球算力资产化趋势影响机器人云服务成本",
        deployment_ready=True,
        tags=["算力金融化", "GPU资产", "融资平台"],
    ),

    # ==================================================================
    # 类别4：AI芯片最新进展
    # ==================================================================
    AIProduct(
        product_id="CH-001", name="英伟达开源Nemotron 3.5 Lightning",
        category=AICategory.AI_CHIP,
        organization="NVIDIA", country="美国",
        description="8月11日英伟达发布开源模型Nemotron 3.5 Lightning，面向长时运行AI智能体"
                    "工作负载，采用混合专家架构总参数300亿、每轮推理激活约30亿参数。"
                    "输出速度较同类模型提升约4倍，智能体任务完成速度提升30%，"
                    "PinchBench准确率86%。同步推出开源智能路由库NeMo Switchyard",
        key_metrics={"total_params_b": 30, "active_params_b": 3,
                     "speedup_x": 4, "agent_speedup_pct": 30,
                     "pinchbench_acc": 0.86, "license": "OpenMDW-1.1"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-12",
        relevance_to_robotics="相关：轻量MoE模型+智能路由适合机器人端侧/边缘推理",
        deployment_ready=True,
        tags=["Nemotron", "MoE", "开源", "智能路由", "Agent"],
    ),
    AIProduct(
        product_id="CH-002", name="苹果调整M系芯片路线 集中研发M7",
        category=AICategory.AI_CHIP,
        organization="Apple", country="美国",
        description="苹果取消M6 Pro/Max/Ultra等高阶版本，M6仅保留基础款，"
                    "研发资源集中投入M7处理器，有望2027年春季提前发布。M7将升级神经网络引擎NPU，"
                    "顶配M7 Ultra的AI算力目标对标英伟达专业AI加速芯片",
        key_metrics={"focus": "M7", "npu_upgrade": True, "target": "NVIDIA_AI_chip"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="相关：端侧NPU升级利好机器人本地推理算力",
        deployment_ready=False,
        tags=["苹果", "M7", "NPU", "端侧AI"],
    ),

    # ==================================================================
    # 类别5：AI大模型最新进展
    # ==================================================================
    AIProduct(
        product_id="LLM-001", name="DeepSeek-V4-Flash周调用量全球第一",
        category=AICategory.AI_LLM,
        organization="深度求索（DeepSeek）", country="中国",
        description="全球大模型单周总调用69万亿Token，"
                    "中国模型合计34.25万亿、环比+21.76%，连续15周全球第一。"
                    "DeepSeek-V4-Flash正式版单周调用8.83万亿Token、环比暴涨570%登顶。"
                    "其核心创新CSA/HCA混合注意力架构，计算量降至前代27%、显存占用仅10%，"
                    "全系标配百万token超长上下文",
        key_metrics={"weekly_tokens_tn": 8.83, "wow_growth_pct": 570,
                     "china_weeks_no1": 15, "compute_pct_prev": 27,
                     "memory_pct_prev": 10, "context_tokens": 1000000},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="核心大脑：高性价比开源大模型适合机器人VLA后端",
        deployment_ready=True,
        tags=["DeepSeek V4", "调用量第一", "CSA/HCA", "百万上下文", "开源"],
    ),
    AIProduct(
        product_id="LLM-002", name="GPT-5.6-Cyber专用安全模型",
        category=AICategory.AI_LLM,
        organization="OpenAI", country="美国",
        description="8月11日OpenAI扩展网络防御项目Daybreak，新增Red等级并推出面向授权漏洞"
                    "研究、渗透测试与事件响应的GPT-5.6-Cyber，基于GPT-5.6 Sol构建，"
                    "仅向埃森哲、IBM、CrowdStrike等获批安全合作方开放。内部高级安全请求"
                    "评测完成率达95%，还发现Chrome V8高危漏洞",
        key_metrics={"completion_rate": 0.95, "access": "whitelist",
                     "base_model": "GPT-5.6 Sol", "vuln_found": "Chrome_V8"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-11",
        relevance_to_robotics="相关：安全专用模型能力分级思路可借鉴机器人安全审查",
        deployment_ready=True,
        tags=["GPT-5.6 Cyber", "网络安全", "Daybreak", "能力分级"],
    ),
    AIProduct(
        product_id="LLM-003", name="Meta开源Muse Glimmer 30B多模态模型",
        category=AICategory.AI_LLM,
        organization="Meta", country="美国",
        description="8月10-11日Meta开源Muse Glimmer 30B及量化权重，Apache 2.0许可，"
                    "支持文本与图像输入、100多种语言及131072 token上下文，"
                    "4bit量化后仅占24GB显存可在单张消费级GPU运行，专攻日程规划、"
                    "文件调度、长周期Agent工作流。扎克伯格同步发布6500字AI愿景长文",
        key_metrics={"params_b": 30, "quantized_vram_gb": 24,
                     "languages": 100, "context_tokens": 131072,
                     "license": "Apache-2.0"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-11",
        relevance_to_robotics="直接相关：消费级GPU可运行的开源多模态模型适合端侧VLA",
        deployment_ready=True,
        tags=["Meta", "Muse Glimmer", "开源", "端侧部署", "多模态"],
    ),

    # ==================================================================
    # 类别6：世界模型最新进展
    # ==================================================================
    AIProduct(
        product_id="WM-001", name="World Proxy以Agent为中心的世界模型新范式",
        category=AICategory.WORLD_MODEL,
        organization="上海AI Lab/浙江大学/新加坡国立大学", country="中国/新加坡",
        description="上海AI Lab、浙大、NUS团队提出'以Agent为中心'的世界模型新范式World Proxy，"
                    "位于Agent与真实环境之间，根据Agent查询/动作返回执行结果、经验技能、奖励"
                    "或验证信号。分三个层级：L1推理时引导、L2训练时优化、L3 Agent-代理共同演化。"
                    "论文arXiv:2608.02713，项目页worldbench.github.io",
        key_metrics={"paper": "arXiv:2608.02713", "levels": ["L1", "L2", "L3"],
                     "paradigm": "agent_centric"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-10",
        relevance_to_robotics="直接相关：世界代理为机器人规划学习提供低成本可控反馈",
        deployment_ready=False,
        tags=["World Proxy", "以Agent为中心", "共同演化", "上海AI Lab"],
    ),
    AIProduct(
        product_id="WM-002", name="NVIDIA Cosmos 3开源物理AI基础模型",
        category=AICategory.WORLD_MODEL,
        organization="NVIDIA", country="美国",
        description="Cosmos 3是首个具备原生推理、世界与动作生成能力的开源omni-model，"
                    "基于Mixture-of-Transformers架构，融合像素、动作、声音、语言。"
                    "可作VLM推理、世界动作模型WAM骨干训练机器人策略、物理闭环仿真、"
                    "合成视频数据生成。模型与代码在HuggingFace/GitHub开源",
        key_metrics={"architecture": "Mixture-of-Transformers",
                     "capabilities": ["VLM", "WAM", "simulation", "video_gen"],
                     "open_source": True},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="直接相关：物理AI世界基础模型直接加速机器人策略学习",
        deployment_ready=True,
        tags=["Cosmos 3", "物理AI", "WAM", "开源", "机器人学习"],
    ),

    # ==================================================================
    # 类别7：AI人工智能综合进展
    # ==================================================================
    AIProduct(
        product_id="AI-001", name="戴盟机器人推全球首个物理交互脑Daimon-TWM",
        category=AICategory.AI_GENERAL,
        organization="戴盟机器人（港科大王煜系）", country="中国",
        description="8月11日戴盟机器人宣布完成数亿元战略轮融资，蚂蚁集团领投，"
                    "同步推出全球首个'物理交互脑'Daimon-TWM。该系统面向机器人与物理世界"
                    "的交互智能，整合感知、决策与动作生成",
        key_metrics={"funding_round": "strategic", "lead_investor": "Ant"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-11",
        relevance_to_robotics="核心相关：物理交互脑直接服务于具身智能",
        deployment_ready=False,
        tags=["物理交互脑", "Daimon-TWM", "戴盟", "蚂蚁领投"],
    ),
    AIProduct(
        product_id="AI-002", name="北京数据集团与华为战略合作算力集群",
        category=AICategory.AI_GENERAL,
        organization="北京数据集团/华为", country="中国",
        description="北京数据集团与华为达成战略合作意向，在自主创新算力集群与城市级算力"
                    "基础设施建设、可信数据空间、数据要素流通、垂直行业数据价值化、"
                    "数据安全等方面深度合作，旗下铜牛信息参与北京市城市级算力基础设施建设",
        key_metrics={"cooperation_areas": 6},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="基础设施：城市级算力与数据空间支撑机器人云脑",
        deployment_ready=True,
        tags=["算力集群", "城市级算力", "可信数据空间", "华为"],
    ),

    # ==================================================================
    # 类别8：6G网络最新进展
    # ==================================================================
    AIProduct(
        product_id="6G-001", name="中国6G加速跑进入第二阶段实战练兵",
        category=AICategory.NETWORK_6G,
        organization="工信部/IMT-2030(6G)推进组", country="中国",
        description="5月工信部批复6GHz频段（6425-7125MHz）"
                    "共700MHz连续带宽6G试验频率使用许可，为全球首个；6月启动部省协同试点；"
                    "7月江苏成立6G产业联盟、湖北发布行动方案。第一阶段已完成，形成超300项"
                    "关键技术储备，6G专利申请量占全球40.3%稳居第一，预计2030年商用",
        key_metrics={"spectrum_mhz": 700, "band": "6GHz", "tech_reserves": 300,
                     "patent_share_pct": 40.3, "commercial_year": 2030,
                     "global_first_license": True},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-10",
        relevance_to_robotics="基础设施：6G通感算智一体化、0.1ms时延支撑机器人云控协同",
        deployment_ready=False,
        tags=["6G", "6GHz", "300项技术", "专利40.3%", "2030商用"],
    ),
    AIProduct(
        product_id="6G-002", name="工信部加快推进第二阶段6G技术试验",
        category=AICategory.NETWORK_6G,
        organization="工信部", country="中国",
        description="上半年已批复6GHz频段6G试验频率"
                    "使用许可，加快推进第二阶段6G技术试验。同期AI手机/电脑、智能机器人、"
                    "AI眼镜、AI玩具等成为信息消费新热点",
        key_metrics={"phase": 2, "trial_freq": "6GHz"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-07-20",
        relevance_to_robotics="基础设施：6G试验为机器人低时延通信铺路",
        deployment_ready=False,
        tags=["6G", "第二阶段", "工信部"],
    ),
    AIProduct(
        product_id="6G-003", name="5G-A大上行示范区支撑数百台机器人协同",
        category=AICategory.NETWORK_6G,
        organization="中国电信（杭州双浦）", country="中国-杭州",
        description="杭州双浦建成5G-A×AI大上行示范区，5G-A网络实现毫秒级时延，"
                    "云端大脑决策指令瞬间下达，数百台人形机器人在同一区域协同作业网络不拥堵。"
                    "目前5G-A已覆盖全国330个城市，'十五五'将建50万个5G-A基站",
        key_metrics={"latency_ms": 1, "cities_covered": 330,
                     "planned_5ga_stations": 500000,
                     "concurrent_robots": 200},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-05-22",
        relevance_to_robotics="直接相关：5G-A毫秒级时延已支撑当前机器人云控部署",
        deployment_ready=True,
        tags=["5G-A", "大上行", "毫秒级时延", "机器人协同", "杭州"],
    ),

    # ==================================================================
    # 类别9：工业机器人最新进展
    # ==================================================================
    AIProduct(
        product_id="IR-001", name="新新三样出海 全品类机器人全球市场爆发",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="中国机器人企业", country="中国",
        description="'新新三样'出海中国机器人圈粉全球，"
                    "从技术闯关、标准突围到深耕服务，全品类机器人出口量逐年增长。"
                    "国产手术机器人获欧盟CE认证，落地德国慕尼黑最大公立医院之一并成功开展"
                    "多例临床手术",
        key_metrics={"export_growth": True, "ce_certified": True,
                     "deployment": "Germany_Munich_hospital"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-05",
        relevance_to_robotics="直接相关：国产工业/手术机器人全球竞争力提升",
        deployment_ready=True,
        tags=["新新三样", "出海", "CE认证", "手术机器人"],
    ),
    AIProduct(
        product_id="IR-002", name="灵猴机器人完成超亿元C轮融资",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="苏州灵猴机器人", country="中国-苏州",
        description="苏州灵猴机器人官宣完成超亿元C轮融资，由宁德时代系产业投资平台晨道资本"
                    "领投，工业母机产业投资基金、豫信电科信产基金等联合跟投。折射新能源巨头"
                    "向智能制造产业链上游深度布局",
        key_metrics={"round": "C", "amount_cny_yi": 1, "lead": "晨道资本"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="相关：工业机器人核心零部件获产业资本加注",
        deployment_ready=True,
        tags=["灵猴机器人", "C轮融资", "宁德时代", "工业机器人"],
    ),

    # ==================================================================
    # 类别10：蚌埠本地AI产品
    # ==================================================================
    AIProduct(
        product_id="BB-001", name="中国传感谷全品类智能传感器产业集群",
        category=AICategory.BENGBU_LOCAL,
        organization="中国传感谷/中国玻璃谷", country="中国-蚌埠",
        description="展出MEMS芯片、柔性脑机电极、"
                    "磁电流传感器、AI嗅觉电子鼻等全品类智能传感器。2025年全市智能传感产业"
                    "产值突破100亿元、同比增长29%，跻身全国MEMS十大高质量传感器园区第6位",
        key_metrics={"output_2025_yi": 100,
                     "growth_pct": 29, "national_rank": 6,
                     "enterprises": 200},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-10",
        relevance_to_robotics="直接相关：传感器是机器人'电子五官'，蚌埠提供本地化感知供应链",
        deployment_ready=True,
        tags=["蚌埠", "传感谷", "MEMS", "电子五官"],
    ),
    AIProduct(
        product_id="BB-002", name="上半年蚌埠82家智能传感规上企业产值50.49亿元",
        category=AICategory.BENGBU_LOCAL,
        organization="蚌埠市工信局", country="中国-蚌埠",
        description="今年上半年全市82家智能传感规模以上工业企业"
                    "产值达50.49亿元、同比增长15%。已集聚200多家上下游企业，本地配套率"
                    "持续提升。北方华鑫智感全新研发固态电池用硫化氢气体专用检测传感器，"
                    "技术国内领先",
        key_metrics={"enterprises_above_scale": 82, "h1_output_yi": 50.49,
                     "growth_pct": 15, "total_enterprises": 200},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-10",
        relevance_to_robotics="直接相关：规模化传感器产业支撑机器人感知层量产",
        deployment_ready=True,
        tags=["蚌埠", "规上企业", "50.49亿", "气体传感器"],
    ),
    AIProduct(
        product_id="BB-003", name="蚌埠脑机接口产业先导区临床落地",
        category=AICategory.BENGBU_LOCAL,
        organization="北方微电子研究院/蚌医一附院", country="中国-蚌埠",
        description="北方微电子研究院突破柔性电极、脑电采集芯片关键技术，"
                    "非侵入式凝胶电极接触阻抗达行业先进水平已批量销售。蚌医一附院挂牌脑机接口"
                    "与神经调控专用病房，完成国内首例磁共振引导无创脑机接口急性脑梗康复治疗、"
                    "全省首例半侵入式脑机植入偏瘫手术，累计开展无创脑机临床治疗70余例，"
                    "患者康复效率平均提升20%",
        key_metrics={"clinical_cases": 70, "rehab_efficiency_pct": 20,
                     "breakthroughs": ["柔性电极", "脑电采集芯片", "凝胶电极"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="前沿相关：脑机接口可用于假肢/外骨骼/康复机器人控制",
        deployment_ready=False,
        tags=["蚌埠", "脑机接口", "神经康复", "半侵入式", "临床"],
    ),
    AIProduct(
        product_id="BB-004", name="华鑫微纳8英寸MEMS晶圆线月产3万片",
        category=AICategory.BENGBU_LOCAL,
        organization="安徽华鑫微纳集成电路有限公司", country="中国-蚌埠",
        description="国内首条8英寸MEMS晶圆全自动生产线昼夜运转，满产后月产晶圆3万片，"
                    "产能稳居国内第一梯队，产出温度、压力、惯性等多品类传感器，"
                    "精准适配低空经济、智慧交通、具身智能等新兴产业。蚌埠是全省唯一、"
                    "全国为数不多同时拥有集成电路及MEMS晶圆生产线的城市",
        key_metrics={"wafer_size_inch": 8, "monthly_capacity": 30000,
                     "sensor_types": ["temperature", "pressure", "inertial"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-09",
        relevance_to_robotics="直接相关：MEMS传感器是机器人关节/IMU/触觉核心器件",
        deployment_ready=True,
        tags=["蚌埠", "8英寸MEMS", "月产3万片", "具身智能", "晶圆"],
    ),
    AIProduct(
        product_id="BB-005", name="全国首个米小庭智慧社区投入运营",
        category=AICategory.BENGBU_LOCAL,
        organization="小米生态/蚌埠传感谷企业", country="中国-蚌埠",
        description="全国首个小米生态全体系智慧社区今年投入运营，既是人才公寓也是智能传感"
                    "产品应用场。蚌埠至博光纤监测仪捕捉管网漏失，华鑫智感AI燃气安全阀泄漏报警，"
                    "中科微感环保卫士监测甲醛TVOC，芒果传感水质检测仪把关饮水安全",
        key_metrics={"coverage": "full_community",
                     "sensor_products": ["光纤监测", "燃气安全", "环境监测", "水质检测"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-07-30",
        relevance_to_robotics="应用场景：智慧社区是服务机器人落地的典型场景",
        deployment_ready=True,
        tags=["蚌埠", "米小庭", "智慧社区", "小米生态", "传感器应用"],
    ),
    AIProduct(
        product_id="BB-006", name="全国首部智能传感产业地方性法规施行",
        category=AICategory.BENGBU_LOCAL,
        organization="蚌埠市人大/经开区", country="中国-蚌埠",
        description="《蚌埠市促进智能传感产业发展条例》作为全国首部智能传感领域地方性法规，"
                    "为产业发展筑牢法治根基，清晰划定市县两级政府职责、明确全产业链培育路径，"
                    "专门设立'尽职免责'条款为先行先试创新主体松绑容错。已建成9条公共中试示范线、"
                    "40余家专精特新企业",
        key_metrics={"pilot_lines": 9, "specialized_new": 40,
                     "national_first": True, "legislation": True},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="直接相关：法治保障的传感产业链降低机器人零部件本地采购风险",
        deployment_ready=True,
        tags=["蚌埠", "地方性法规", "尽职免责", "中试示范线", "专精特新"],
    ),

    # ==================================================================
    # 类别11：新能源AI
    # ==================================================================
    AIProduct(
        product_id="EN-001", name="分布式光伏智能巡控系统",
        category=AICategory.RENEWABLE_ENERGY,
        organization="国家电网", country="中国",
        description="基于光明电力大模型部署光伏异常识别、反向重过载原因分析、"
                    "调控策略制订、动态调优4个智能体，形成'云端智能研判+现场自动巡控'闭环，"
                    "自动调度空气能等柔性负荷参与电网削峰填谷",
        key_metrics={"ai_agents": 4, "control_loop": "cloud_edge",
                     "flexible_load_dispatch": True},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="能源基础设施：机器人充电站智能调度可复用",
        deployment_ready=True,
        tags=["光伏", "智能巡控", "电力大模型", "反向重过载"],
    ),
    AIProduct(
        product_id="EN-002", name="光储一体商超绿色供电方案",
        category=AICategory.RENEWABLE_ENERGY,
        organization="晶科能源", country="中国",
        description="'晴天365'光储一体解决方案覆盖大型商超冷库冷站、充电站、"
                    "数据中心等场景，中国企业已建成全球最大的光伏智慧运维体系，"
                    "运营效率较行业平均提升20%",
        key_metrics={"efficiency_gain_pct": 20, "scenes": ["cold_storage", "charging", "data_center"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="绿色能源：机器人作业站点光储供能参考",
        deployment_ready=True,
        tags=["光储一体", "商超", "智慧运维", "绿色供电"],
    ),
    AIProduct(
        product_id="EN-003", name="800V直流AIDC固态变压器SST",
        category=AICategory.RENEWABLE_ENERGY,
        organization="阳光电源", country="中国",
        description="发布480V/800V直流AIDC智能供电整体解决方案，首发375kW SST产品，"
                    "单柜效率达98%，实现分布式光伏、储能、算力负荷直直交互，"
                    "为AI算力中心提供高效绿电",
        key_metrics={"dc_voltage_v": 800, "sst_power_kw": 375,
                     "efficiency_pct": 98, "grid_following": False},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="算力供能：机器人训练集群绿电直供",
        deployment_ready=True,
        tags=["固态变压器", "800V直流", "AIDC", "绿电"],
    ),
    AIProduct(
        product_id="EN-004", name="驭理电力AI研究员",
        category=AICategory.RENEWABLE_ENERGY,
        organization="南方电网", country="中国",
        description="电力行业自主可控AI基础模型，面向电力调度、设备运维、"
                    "客户服务等核心业务场景提供智能决策支持，"
                    "实现电网运行状态的实时感知与优化",
        key_metrics={"industry": "power", "autonomous": True,
                     "scenarios": ["dispatch", "maintenance", "service"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="基础设施AI：工业级决策系统架构参考",
        deployment_ready=True,
        tags=["电力大模型", "自主可控", "智能调度", "设备运维"],
    ),

    # ==================================================================
    # 类别12：农业AI
    # ==================================================================
    AIProduct(
        product_id="AG-001", name="浙里良田高标准农田智能体",
        category=AICategory.AGRICULTURE,
        organization="浙江省农业农村厅", country="中国",
        description="基于450万组土壤试验数据、1200万条测土配方施肥记录、"
                    "3500万个农户调查数据构建智能决策体系，为农户提供"
                    "土壤分析、施肥建议、病虫害预警、种植规划等全流程服务",
        key_metrics={"soil_trials": 4500000, "fertilizer_records": 12000000,
                     "farmer_surveys": 35000000, "coverage": "zhejiang"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="农业机器人：土壤分析与作业决策数据源",
        deployment_ready=True,
        tags=["高标准农田", "智能体", "土壤数据", "测土配方"],
    ),
    AIProduct(
        product_id="AG-002", name="Asymetree单株精准灌溉平台",
        category=AICategory.AGRICULTURE,
        organization="Asymetree", country="西班牙",
        description="通过LiDAR生成3D树冠模型计算冠幅体积，结合SAQIA-IR无线"
                    "红外传感器检测树冠温度判断水分胁迫，实现按单株按需灌溉，"
                    "已在橄榄、柑橘、杏仁、阿月浑子等经济林场商业化部署",
        key_metrics={"sensor": "SAQIA-IR", "model": "3d_lidar",
                     "crops": ["olive", "citrus", "almond", "pistachio"],
                     "irrigation_unti": "per_tree"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="精准农业：机器人单株作业感知与决策参考",
        deployment_ready=True,
        tags=["精准灌溉", "LiDAR", "热红外", "单株管理"],
    ),
    AIProduct(
        product_id="AG-003", name="低空+AI农事智能服务",
        category=AICategory.AGRICULTURE,
        organization="金东区农业农村局", country="中国",
        description="整合50余项AI模型能力，无人机5分钟采集180亩小麦苗情病虫信息，"
                    "飞行成本较传统人工巡查下降80%，实现病虫害早发现、早预警、早处置",
        key_metrics={"ai_models": 50, "scan_area_mu": 180, "scan_time_min": 5,
                     "cost_reduction_pct": 80},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="低空经济：无人机+AI巡检与机器人协同",
        deployment_ready=True,
        tags=["低空经济", "无人机", "病虫害", "智慧农业"],
    ),

    # ==================================================================
    # 类别13：商业AI
    # ==================================================================
    AIProduct(
        product_id="CO-001", name="对话式AI购物入口",
        category=AICategory.COMMERCE,
        organization="淘宝", country="中国",
        description="用户用自然语言表达购物需求，AI自动理解意图、筛选商品、"
                    "对比方案并完成推荐，无需在海量商品中翻找，"
                    "实现从'人找货'到'AI找货'的转变",
        key_metrics={"interaction": "conversational", "intent_understanding": True,
                     "auto_filtering": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="人机交互：自然语言指令理解与任务执行",
        deployment_ready=True,
        tags=["对话式购物", "AI推荐", "自然语言", "电商"],
    ),
    AIProduct(
        product_id="CO-002", name="GLAM美妆AI推荐平台",
        category=AICategory.COMMERCE,
        organization="Ulta Beauty", country="美国",
        description="基于200+维度AI用户画像，购买、收藏、分享商品直接生成"
                    "个性化推荐清单，结合AR试妆实现线上线下融合消费体验",
        key_metrics={"ai_dimensions": 200, "ar_tryon": True,
                     "signals": ["purchase", "favorite", "share"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="多模态推荐：机器人个性化服务参考",
        deployment_ready=True,
        tags=["AI推荐", "用户画像", "AR试妆", "美妆零售"],
    ),
    AIProduct(
        product_id="CO-003", name="Allplan建筑智能体",
        category=AICategory.COMMERCE,
        organization="智谱AI", country="中国",
        description="空间智能+垂直智能体协作架构，建模效率提升80%，"
                    "造价偏差率压缩至3%，支持25种语言，覆盖建筑设计、"
                    "结构计算、造价管控全流程",
        key_metrics={"efficiency_gain_pct": 80, "cost_deviation_pct": 3,
                     "languages": 25, "architecture": "multi_agent"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="空间智能：机器人建筑场景理解与导航",
        deployment_ready=True,
        tags=["建筑智能体", "空间智能", "多智能体协作", "造价管控"],
    ),

    # ==================================================================
    # 类别14：水利AI
    # ==================================================================
    AIProduct(
        product_id="WA-001", name="天空地水工一体化监测平台",
        category=AICategory.WATER_CONSERVANCY,
        organization="水利部", country="中国",
        description="集成卫星遥感、航空测量、地面传感器、地下水位监测、"
                    "工程工况感知五维数据，AI洪水预报演进与淹没推演，"
                    "实现流域水工程联合调度",
        key_metrics={"dimensions": 5, "data_sources": ["satellite", "aerial", "ground",
                                                        "underground", "engineering"],
                     "forecast": "flood_evolution"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="环境感知：多源融合监测架构可复用",
        deployment_ready=True,
        tags=["智慧水利", "天空地水工", "洪水预报", "联合调度"],
    ),
    AIProduct(
        product_id="WA-002", name="堤防管涌智能巡查装备",
        category=AICategory.WATER_CONSERVANCY,
        organization="湖北省水利厅", country="中国",
        description="多模态视觉识别技术自动检测管涌、渗漏、裂缝等堤防隐患，"
                    "发现风险后秒级声光报警并上报经纬度坐标，"
                    "堤防巡查效率较人工提升50倍",
        key_metrics={"defect_types": ["piping", "seepage", "crack"],
                     "alert_latency_s": 1.0, "efficiency_x": 50},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="巡检机器人：堤坝自动巡查技术直接复用",
        deployment_ready=True,
        tags=["堤防巡查", "管涌识别", "秒级报警", "多模态视觉"],
    ),
    AIProduct(
        product_id="WA-003", name="智慧水务3.0大模型调度",
        category=AICategory.WATER_CONSERVANCY,
        organization="武威市水务局", country="中国",
        description="'互联网+城乡供水'智慧水务3.0+大模型，AI智能调度管理"
                    "1732万方水资源，服务5.2万城乡用户，实现从水源到龙头的"
                    "全链条精细化管控",
        key_metrics={"water_managed_m3": 17320000, "users": 52000,
                     "chain": "source_to_tap"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="资源调度：多目标优化算法参考",
        deployment_ready=True,
        tags=["智慧水务", "城乡供水", "AI调度", "大模型"],
    ),

    # ==================================================================
    # 类别15：汽车AI
    # ==================================================================
    AIProduct(
        product_id="AU-001", name="Alpamayo 2 Super物理交互世界模型",
        category=AICategory.AUTOMOTIVE,
        organization="NVIDIA", country="美国",
        description="6B参数物理交互世界基础模型，800万视频片段训练，"
                    "自动驾驶推理token减少7倍，开源支持全行业二次开发，"
                    "实现高保真物理世界交互仿真",
        key_metrics={"params_b": 6, "training_videos_m": 8,
                     "token_reduction_x": 7, "open_source": True},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="直接相关：世界模型可用于机器人轨迹预测与安全验证",
        deployment_ready=True,
        tags=["世界模型", "自动驾驶", "物理交互", "开源"],
    ),
    AIProduct(
        product_id="AU-002", name="超级Eva车载智能体",
        category=AICategory.AUTOMOTIVE,
        organization="吉利汽车", country="中国",
        description="多模态车载智能体，支持自然语音交流、儿童/老人识别、"
                    "疲劳驾驶监测，融合车辆状态与驾驶场景提供主动服务，"
                    "实现人车自然交互",
        key_metrics={"modalities": ["voice", "vision", "gesture"],
                     "driver_monitoring": True, "active_service": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="人机交互：多模态主动服务架构参考",
        deployment_ready=True,
        tags=["车载智能体", "多模态", "疲劳监测", "自然语音"],
    ),
    AIProduct(
        product_id="AU-003", name="LEAP3.5数字底盘架构",
        category=AICategory.AUTOMOTIVE,
        organization="零跑汽车", country="中国",
        description="全线控数字底盘集成线控转向、线控制动、线控驱动，"
                    "支持中央超算平台集中控制，为高阶智能驾驶提供"
                    "精确车辆执行能力",
        key_metrics={"by_wire": ["steering", "braking", "throttle"],
                     "central_compute": True, "architecture": "digital_chassis"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="线控底盘：移动机器人执行层技术参考",
        deployment_ready=True,
        tags=["数字底盘", "线控", "中央计算", "智能驾驶"],
    ),

    # ==================================================================
    # 类别16：数码产品AI
    # ==================================================================
    AIProduct(
        product_id="DP-001", name="Galaxy Z Fold8 AI折叠旗舰",
        category=AICategory.DIGITAL_PRODUCT,
        organization="三星", country="韩国",
        description="搭载端侧大模型，支持AI影像编辑、语义搜图、"
                    "实时翻译、智能摘要，折叠屏多任务AI协同",
        key_metrics={"foldable": True, "on_device_llm": True,
                     "ai_features": ["image_editing", "semantic_search",
                                     "translation", "summarization"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="端侧AI：低功耗模型部署参考",
        deployment_ready=True,
        tags=["折叠屏", "端侧AI", "AI影像", "实时翻译"],
    ),
    AIProduct(
        product_id="DP-002", name="Mate 90系列AI手机",
        category=AICategory.DIGITAL_PRODUCT,
        organization="华为", country="中国",
        description="搭载GPU Turbo Agent智能调度引擎，端侧大模型支持"
                    "AI修图、语义搜索、视觉问答，配合AI眼镜实现跨设备协同",
        key_metrics={"gpu_turbo_agent": True, "ai_glasses_support": True,
                     "cross_device": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="跨设备协同：手机-机器人联动参考",
        deployment_ready=True,
        tags=["AI手机", "GPU加速", "跨设备", "AI眼镜"],
    ),
    AIProduct(
        product_id="DP-003", name="MagicBook Pro 16 AI PC",
        category=AICategory.DIGITAL_PRODUCT,
        organization="荣耀", country="中国",
        description="搭载PC端侧14B大模型，支持本地代码生成、文档摘要、"
                    "AI绘图，NPU算力达80TOPS，Turbo X引擎优化性能调度",
        key_metrics={"on_device_model_b": 14, "npu_tofps": 80,
                     "features": ["code_generation", "summarization", "image_gen"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="边缘计算：本地大模型运行环境参考",
        deployment_ready=True,
        tags=["AI PC", "端侧大模型", "NPU", "代码生成"],
    ),

    # ==================================================================
    # 类别17：医疗健康AI
    # ==================================================================
    AIProduct(
        product_id="HC-001", name="医学影像AI辅助诊断系统",
        category=AICategory.HEALTHCARE,
        organization="联影智能", country="中国",
        description="覆盖CT/MRI/X光/病理/眼底多模态影像分析，"
                    "联邦学习训练保护患者隐私，肺结节检测准确率96%，"
                    "病理切片分析准确率97%",
        key_metrics={"modalities": ["ct", "mri", "xray", "pathology", "fundus"],
                     "lung_nodule_acc": 0.96, "pathology_acc": 0.97,
                     "federated_learning": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="医疗机器人：影像引导手术与诊断参考",
        deployment_ready=True,
        tags=["医学影像", "辅助诊断", "联邦学习", "多模态"],
    ),
    AIProduct(
        product_id="HC-002", name="AIDD人工智能药物发现平台",
        category=AICategory.HEALTHCARE,
        organization="晶泰科技", country="中国",
        description="AI全流程药物研发：靶点识别→虚拟筛选→分子生成→"
                    "ADMET预测→临床试验匹配，候选药物发现时间缩短18个月，"
                    "研发成本降低60%",
        key_metrics={"pipeline": ["target_id", "virtual_screening", "molecule_gen",
                                  "admet", "trial_match"],
                     "time_saved_months": 18, "cost_reduction_pct": 60},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="AI科研：自动化实验机器人决策参考",
        deployment_ready=True,
        tags=["药物研发", "AIDD", "虚拟筛选", "ADMET"],
    ),
    AIProduct(
        product_id="HC-003", name="临床决策支持系统CDSS",
        category=AICategory.HEALTHCARE,
        organization="讯飞医疗", country="中国",
        description="基于5万条临床指南知识图谱，症状分析→鉴别诊断→"
                    "检查建议→用药提醒，药物相互作用智能审查，"
                    "辅助医生提升诊疗质量",
        key_metrics={"knowledge_base": 50000, "functions": ["symptom_analysis",
                     "differential_diagnosis", "test_recommendation",
                     "drug_interaction"], "guidelines_version": "2026.08"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="决策系统：多因素推理引擎参考",
        deployment_ready=True,
        tags=["临床决策", "知识图谱", "用药安全", "辅助诊断"],
    ),

    # ==================================================================
    # 类别18：民生AI
    # ==================================================================
    AIProduct(
        product_id="LV-001", name="城市安全风险综合监测预警平台",
        category=AICategory.LIVELIHOOD,
        organization="应急管理部", country="中国",
        description="融合交通、安防、环境、市政多源数据，城市大脑"
                    "实时监测燃气、供水、桥梁、隧道安全风险，"
                    "AI自动研判预警并联动应急指挥调度",
        key_metrics={"domains": ["traffic", "safety", "environment", "utilities"],
                     "monitoring": ["gas", "water", "bridge", "tunnel"],
                     "response": "automatic_dispatch"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="智慧城市：机器人城市服务调度参考",
        deployment_ready=True,
        tags=["城市大脑", "安全监测", "应急指挥", "多源融合"],
    ),
    AIProduct(
        product_id="LV-002", name="AI交通信号优化系统",
        category=AICategory.LIVELIHOOD,
        organization="阿里云", country="中国",
        description="实时交通流量分析驱动AI信号自适应优化，"
                    "拥堵预测准确率90%，主干道通行效率提升15%，"
                    "区域信号协同调度",
        key_metrics={"congestion_prediction_acc": 0.90,
                     "efficiency_gain_pct": 15, "adaptive": True,
                     "scope": "regional_coordination"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="路径规划：多智能体交通调度参考",
        deployment_ready=True,
        tags=["智慧交通", "信号优化", "拥堵预测", "自适应"],
    ),
    AIProduct(
        product_id="LV-003", name="12345智能分派与智慧养老",
        category=AICategory.LIVELIHOOD,
        organization="各地政务服务/民政部门", country="中国",
        description="AI自动分类市民诉求并精准派单，居家养老跌倒检测、"
                    "用药提醒、定期关怀，社区网格化智能管理",
        key_metrics={"dispatch_ai": True, "fall_detection": True,
                     "medication_reminder": True, "grid_management": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="服务机器人：社区/养老场景直接落地",
        deployment_ready=True,
        tags=["智慧政务", "智慧养老", "跌倒检测", "社区网格"],
    ),

    # ==================================================================
    # 类别19：教育AI
    # ==================================================================
    AIProduct(
        product_id="ED-001", name="AI苏格拉底辅导老师",
        category=AICategory.EDUCATION,
        organization="好未来", country="中国",
        description="不直接给答案，通过苏格拉底式提问引导学生思考，"
                    "覆盖数学、物理、化学等多学科，自适应调整提问难度，"
                    "培养独立思考能力",
        key_metrics={"method": "socratic", "subjects": ["math", "physics", "chemistry"],
                     "adaptive_difficulty": True, "answer_given": False},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="人机教学：机器人技能传授交互参考",
        deployment_ready=True,
        tags=["AI辅导", "苏格拉底", "自适应", "多学科"],
    ),
    AIProduct(
        product_id="ED-002", name="个性化学习路径引擎",
        category=AICategory.EDUCATION,
        organization="猿辅导", country="中国",
        description="基于知识图谱和学习者画像，诊断知识薄弱点，"
                    "规划最优学习路径，AI生成分层练习，"
                    "学习效率提升40%",
        key_metrics={"knowledge_graph": True, "adaptive_path": True,
                     "exercise_generation": True, "efficiency_gain_pct": 40},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="技能学习：机器人知识图谱与任务规划参考",
        deployment_ready=True,
        tags=["个性化学习", "知识图谱", "学习路径", "分层练习"],
    ),
    AIProduct(
        product_id="ED-003", name="智能批改与教育智能体",
        category=AICategory.EDUCATION,
        organization="科大讯飞", country="中国",
        description="客观题自动批改+作文AI评分反馈+代码作业自动测试，"
                    "教育智能体自动备课生成教案，课堂行为分析提升教学质量",
        key_metrics={"grading_types": ["objective", "essay", "coding"],
                     "lesson_plan_generation": True, "classroom_analytics": True,
                     "ai_agent": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="自动化：机器人任务评估与教学辅助参考",
        deployment_ready=True,
        tags=["智能批改", "作文评分", "教育智能体", "课堂分析"],
    ),
]


class AILandscapeRegistry:
    def __init__(self):
        self._db = AI_LANDSCAPE_DB
        self._index_by_category: Dict[str, List[AIProduct]] = {}
        self._index_by_country: Dict[str, List[AIProduct]] = {}
        self._build_indices()

    def _build_indices(self) -> None:
        try:
            for product in self._db:
                cat = product.category.value
                if cat not in self._index_by_category:
                    self._index_by_category[cat] = []
                self._index_by_category[cat].append(product)
                country = product.country
                if country not in self._index_by_country:
                    self._index_by_country[country] = []
                self._index_by_country[country].append(product)
        except Exception:
            pass

    def get_by_category(self, category: AICategory) -> List[AIProduct]:
        try:
            return self._index_by_category.get(category.value, [])
        except Exception:
            return []

    def get_by_country(self, country: str) -> List[AIProduct]:
        try:
            return self._index_by_country.get(country, [])
        except Exception:
            return []

    def get_deployment_ready(self) -> List[AIProduct]:
        try:
            return [p for p in self._db if p.deployment_ready]
        except Exception:
            return []

    def get_bengbu_local(self) -> List[AIProduct]:
        return self.get_by_category(AICategory.BENGBU_LOCAL)

    def get_robotics_relevant(self) -> List[AIProduct]:
        try:
            return [p for p in self._db if p.relevance_to_robotics]
        except Exception:
            return []

    def get_by_source_tier(self, tier: SourceTier) -> List[AIProduct]:
        try:
            return [p for p in self._db if p.source_tier == tier]
        except Exception:
            return []

    def search(self, keyword: str) -> List[AIProduct]:
        try:
            kw = keyword.lower()
            return [p for p in self._db if kw in (p.name + p.description + " ".join(p.tags)).lower()]
        except Exception:
            return []

    def get_summary(self) -> Dict[str, Any]:
        try:
            summary = {
                "total_products": len(self._db),
                "categories": {},
                "countries": {},
                "deployment_ready_count": 0,
                "bengbu_local_count": 0,
                "tier1_sources": 0,
            }
            for p in self._db:
                cat = p.category.value
                summary["categories"][cat] = summary["categories"].get(cat, 0) + 1
                summary["countries"][p.country] = summary["countries"].get(p.country, 0) + 1
                if p.deployment_ready:
                    summary["deployment_ready_count"] += 1
                if p.category == AICategory.BENGBU_LOCAL:
                    summary["bengbu_local_count"] += 1
                if p.source_tier == SourceTier.TIER1:
                    summary["tier1_sources"] += 1
            return summary
        except Exception:
            return {"total_products": 0}

    def get_all(self) -> List[AIProduct]:
        return list(self._db)


_registry: Optional[AILandscapeRegistry] = None


def get_ai_landscape_registry() -> AILandscapeRegistry:
    global _registry
    if _registry is None:
        _registry = AILandscapeRegistry()
    return _registry
