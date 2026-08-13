#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI全景注册表 - V1.2
================================================================
新增内容（V1.2 2026-08-13）：
  - 新增40+项AI产品覆盖19大模块
  - 修复农业模块ID冲突(AG->AGR)
  - 更新版本：V1.1 -> V1.2

历史内容：
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
        description="Manus宣布即将恢复以独立公司形式运营，继续为全球数百万用户服务，"
                    "并筹备一系列新功能拓展通用AI智能体能力边界。近期已更新4项功能："
                    "对话分支Branch、网站自动发布Auto-Publish、"
                    "智能PPT生成、先规划后执行的Plan Mode",
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
        description="千问开放平台正式上线，面向生态伙伴和开发者开放手机、PC、AI眼镜"
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
        description="英伟达与Apollo、黑石、贝莱德GIP、Brookfield、高盛、KKR等"
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
        description="英伟达发布开源模型Nemotron 3.5 Lightning，面向长时运行AI智能体"
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
        description="OpenAI扩展网络防御项目Daybreak，新增Red等级并推出面向授权漏洞"
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
        description="戴盟机器人宣布完成数亿元战略轮融资，蚂蚁集团领投，"
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
        product_id="AGR-001", name="浙里良田高标准农田智能体",
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
        product_id="AGR-002", name="Asymetree单株精准灌溉平台",
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
        product_id="AGR-003", name="低空+AI农事智能服务",
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
    # ==================================================================
    # 2026-08-13 更新：19大模块最新AI产品与技术进展
    # ==================================================================

    # --- 人形机器人 ---
    AIProduct(
        product_id="HR-004", name="擎羽Fi0柔性具身智能机器人",
        category=AICategory.HUMANOID_ROBOT,
        organization="擎羽机器人", country="中国",
        description="柔性具身智能机器人Fi0，引入Cross-view World Encoder跨视角世界编码器，"
                    "通过人类第一视角与机器人腕部视角对齐学习共享世界表示；"
                    "A01/A02/A03三种模块化臂长（459/584/764mm），"
                    "重量760/1500/2300g，实现本体差异下的技能迁移",
        key_metrics={"modular_arms": 3, "cross_view_encoder": True,
                     "world_latent_repr": True, "weight_range_g": "760-2300"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="核心：跨视角世界模型与模块化本体设计，直接服务于具身智能技能迁移",
        deployment_ready=True,
        tags=["柔性机器人", "跨视角世界模型", "模块化臂", "技能迁移"],
    ),
    AIProduct(
        product_id="HR-005", name="深圳人形机器人多场景规模化部署",
        category=AICategory.HUMANOID_ROBOT,
        organization="中国机器人企业", country="中国",
        description="深圳人形机器人在餐饮送餐、邮政包裹分拣、交通指挥、冰淇淋制作等"
                    "多场景实现常态化部署，人形机器人从实验室走进日常工作与生活",
        key_metrics={"deployment_scenarios": ["restaurant", "postal", "traffic", "retail"],
                     "city": "深圳"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="直接：人形机器人多场景落地验证，为真机部署提供场景参考",
        deployment_ready=True,
        tags=["人形机器人", "场景部署", "送餐", "分拣", "交通指挥"],
    ),
    AIProduct(
        product_id="HR-006", name="青岛机器人6S体验店",
        category=AICategory.HUMANOID_ROBOT,
        organization="青岛智能机器人产业", country="中国",
        description="山东青岛首家机器人6S体验店推行六位一体运营模式，"
                    "集合销售、零配件、售后服务、信息反馈、租赁、个性化定制六大功能，"
                    "推动智能机器人走出实验室走进大众日常生活",
        key_metrics={"business_model": "6S", "functions": 6,
                     "location": "青岛"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="产业化：机器人消费端商业化通道打通",
        deployment_ready=True,
        tags=["机器人6S店", "消费机器人", "六位一体", "个性化定制"],
    ),

    # --- AI智能体 ---
    AIProduct(
        product_id="AG-005", name="DeepSeek Harness代码智能体团队",
        category=AICategory.AI_AGENT,
        organization="深度求索", country="中国",
        description="DeepSeek正式组建Harness专项团队，主攻代码智能体产品，"
                    "对标Claude Code与OpenAI Codex，"
                    "推动AI从对话辅助走向复杂任务自主交付",
        key_metrics={"focus": "code_agent", "benchmark_target": "Claude Code/Codex"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="工具链：代码智能体可加速机器人控制代码开发与调试",
        deployment_ready=False,
        tags=["代码智能体", "Harness", "自主编程", "DeepSeek"],
    ),
    AIProduct(
        product_id="AG-006", name="智谱ZCode编程智能体用户破百万",
        category=AICategory.AI_AGENT,
        organization="智谱AI", country="中国",
        description="智谱AI编程产品ZCode全面升级，Goal/Subagents/Remote Control/"
                    "闲时任务正式上线，Coding Agent从对话辅助走向复杂任务自主交付，"
                    "用户数突破100万",
        key_metrics={"users": 1000000, "features": ["Goal", "Subagents", "Remote Control"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="开发工具：智能体编程可加速机器人软件开发",
        deployment_ready=True,
        tags=["编程智能体", "ZCode", "自主交付", "多智能体"],
    ),
    AIProduct(
        product_id="AG-007", name="英伟达NeMo Switchyard模型路由库",
        category=AICategory.AI_AGENT,
        organization="英伟达", country="美国",
        description="开源智能体路由库，根据任务复杂度自动将请求分配给不同模型，"
                    "前沿模型负责复杂推理，轻量模型负责高频执行，"
                    "被称为模型的交通调度系统",
        key_metrics={"routing": "automatic", "open_source": True,
                     "cost_reduction": "significant"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="架构参考：多模型协同调度可用于机器人云端/边缘算力分配",
        deployment_ready=True,
        tags=["模型路由", "智能体编排", "多模型协同", "开源"],
    ),
    AIProduct(
        product_id="AG-008", name="Cloudflare Kitesurf智能体浏览器",
        category=AICategory.AI_AGENT,
        organization="Cloudflare", country="美国",
        description="Agent-first浏览器，运行于Workers V8隔离环境，"
                    "CPU和内存消耗比Chromium低3-7倍，"
                    "为AI智能体提供安全高效的网页交互环境",
        key_metrics={"cpu_reduction": "3-7x", "runtime": "V8 isolates",
                     "agent_native": True},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="工具链：智能体浏览器可辅助机器人获取网络信息",
        deployment_ready=False,
        tags=["智能体浏览器", "V8隔离", "低资源", "Cloudflare"],
    ),

    # --- AI算力 ---
    AIProduct(
        product_id="CP-004", name="阿里云灵骏真武M890超节点",
        category=AICategory.AI_COMPUTE,
        organization="阿里云", country="中国",
        description="国内首个成功运行超2万亿参数大模型的超节点算力，"
                    "64卡高速互联，卡间带宽800GB/s，支持FP8/FP4低精度计算，"
                    "智能驾驶/具身智能训练性能提升3倍",
        key_metrics={"max_params_trillion": 2, "gpu_count": 64,
                     "interconnect_bandwidth_gbs": 800, "training_speedup": 3},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="算力基座：支持具身智能大模型训练",
        deployment_ready=True,
        tags=["超节点", "万亿参数", "64卡互联", "具身智能训练"],
    ),
    AIProduct(
        product_id="CP-005", name="乌兰察布星河算电协同基地",
        category=AICategory.AI_COMPUTE,
        organization="中国算力企业", country="中国",
        description="全球最大单体智算中心投产，20个足球场大小，160兆瓦供电能力，"
                    "百万卡并行、百万P算力规模，80%绿电直供，"
                    "一度绿电可转化为近30秒AI文生视频",
        key_metrics={"power_mw": 160, "green_power_pct": 80,
                     "scale": "million_cards", "area_fields": 20},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="算力基础设施：大规模算力支撑机器人模型训练",
        deployment_ready=True,
        tags=["智算中心", "算电协同", "绿电", "百万卡"],
    ),
    AIProduct(
        product_id="CP-006", name="寒武纪AI芯片半年报营收翻倍",
        category=AICategory.AI_COMPUTE,
        organization="寒武纪", country="中国",
        description="2026年上半年营收59.96亿元同比增长108%，"
                    "净利润23.11亿元同比增长122%，"
                    "国产AI芯片进入规模化盈利阶段",
        key_metrics={"revenue_billion": 5.996, "revenue_growth_pct": 108,
                     "profit_billion": 2.311, "profit_growth_pct": 122},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="国产算力：AI芯片为机器人提供自主可控推理算力",
        deployment_ready=True,
        tags=["AI芯片", "国产算力", "营收翻倍", "规模化盈利"],
    ),

    # --- AI芯片 ---
    AIProduct(
        product_id="CH-003", name="芯擎科技天工100车规AI芯片量产",
        category=AICategory.AI_CHIP,
        organization="芯擎科技", country="中国",
        description="国内首款面向端侧智能体AI应用的独立车规大模型加速芯片，"
                    "7nm工艺，96 TOPS INT8算力，外挂式设计无需替换主控，"
                    "支持3B-7B大模型本地推理，成本下探至千元级",
        key_metrics={"process_nm": 7, "tops_int8": 96,
                     "model_support": "3B-7B", "cost_level": "千元级"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="端侧算力：车规AI芯片可迁移至机器人边缘推理",
        deployment_ready=True,
        tags=["车规芯片", "7nm", "AI加速器", "外挂式", "端侧推理"],
    ),
    AIProduct(
        product_id="CH-004", name="爱芯元智下一代大算力AI芯片流片",
        category=AICategory.AI_CHIP,
        organization="爱芯元智", country="中国",
        description="下一代高性能大算力AI芯片完成流片，配备高带宽内存HBM，"
                    "支持两芯或四芯级联，实现满血大模型在边缘侧高性能推理",
        key_metrics={"hbm": True, "cascade_support": "2x/4x",
                     "edge_inference": "full_scale"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="边缘算力：多芯级联为机器人提供可扩展AI算力",
        deployment_ready=False,
        tags=["AI芯片", "流片", "HBM", "多芯级联", "边缘推理"],
    ),

    # --- AI大模型 ---
    AIProduct(
        product_id="LLM-004", name="SpaceX Grok 4.6大模型",
        category=AICategory.AI_LLM,
        organization="SpaceX AI", country="美国",
        description="新一代大模型Grok 4.6，重点提升长程智能体、复杂编程和知识工作能力，"
                    "GDPVal-AA v2评测1753 Elo，高于Claude Fable 5 Max的1741分",
        key_metrics={"elo_score": 1753, "benchmark": "GDPVal-AA v2",
                     "focus": ["long_horizon_agent", "coding", "knowledge_work"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="智能体能力：长程推理可服务于机器人任务规划",
        deployment_ready=True,
        tags=["Grok", "大模型", "长程智能体", "编程"],
    ),
    AIProduct(
        product_id="LLM-005", name="Kimi K3开源2.8万亿参数模型",
        category=AICategory.AI_LLM,
        organization="月之暗面", country="中国",
        description="新一代国产大模型Kimi K3正式开源，2.8万亿参数规模，"
                    "为目前全球参数规模最大的开源模型，人人可下载",
        key_metrics={"params_trillion": 2.8, "open_source": True,
                     "global_rank": "largest_open_source"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="开源基座：大规模开源模型可用于机器人VLA训练",
        deployment_ready=True,
        tags=["Kimi", "开源", "万亿参数", "国产大模型"],
    ),
    AIProduct(
        product_id="LLM-006", name="面壁智能端侧大模型MiniCPM",
        category=AICategory.AI_LLM,
        organization="面壁智能", country="中国",
        description="端侧大模型公司启动A股IPO辅导估值超200亿，MiniCPM模型搭载于"
                    "三星旗舰机型及多款量产车型智能座舱，应用于具身机器人、AI PC等场景",
        key_metrics={"valuation_billion": 20, "deployments": ["samsung", "automotive", "robot"],
                     "model_size_b": "2-4"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="端侧部署：小参数模型适合机器人本地推理",
        deployment_ready=True,
        tags=["端侧大模型", "MiniCPM", "IPO", "具身机器人"],
    ),

    # --- 世界模型 ---
    AIProduct(
        product_id="WM-003", name="NVIDIA Alpamayo 2 Super VLA模型",
        category=AICategory.WORLD_MODEL,
        organization="英伟达", country="美国",
        description="320亿参数基于推理的视觉语言动作(VLA)模型，"
                    "面向L4级Robotaxi，支持因果链推理，"
                    "通过AlpaGym闭环强化学习训练，AlpaSim闭环仿真验证",
        key_metrics={"params_billion": 32, "type": "VLA",
                     "autonomy_level": "L4", "rl_training": True},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="核心：VLA模型架构直接适用于机器人视觉-语言-动作控制",
        deployment_ready=True,
        tags=["VLA", "世界模型", "L4自动驾驶", "因果推理", "闭环RL"],
    ),
    AIProduct(
        product_id="WM-004", name="Momenta R7世界模型量产落地",
        category=AICategory.WORLD_MODEL,
        organization="Momenta", country="中国",
        description="世界模型架构首次在量产车落地，采用预训练+仿真+强化学习三层架构，"
                    "引入自我对弈(Self-Play)机制，仅2048 TOPS算力实现城区NOA，"
                    "从规则驱动转向数据驱动",
        key_metrics={"architecture": "pretrain+sim+rl", "self_play": True,
                     "compute_tops": 2048, "first_mass_production": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="方法论：世界模型+Self-Play训练范式可迁移至机器人",
        deployment_ready=True,
        tags=["世界模型", "量产", "自我对弈", "城区NOA", "数据驱动"],
    ),

    # --- AI通用 ---
    AIProduct(
        product_id="AI-003", name="荣耀全球首款机器人手机",
        category=AICategory.AI_GENERAL,
        organization="荣耀", country="中国",
        description="推出全球首款机器人手机，"
                    "融合AI能力与机器人技术，"
                    "依托中国软硬一体工程化能力实现AI从需求到体验高效落地",
        key_metrics={"world_first": True, "type": "robot_phone",
                     "release_date": "2026-08-12"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="终端融合：手机与机器人技术融合趋势",
        deployment_ready=True,
        tags=["机器人手机", "AI终端", "荣耀", "全球首款"],
    ),
    AIProduct(
        product_id="AI-004", name="AI Harness驾驭框架",
        category=AICategory.AI_GENERAL,
        organization="中国AI产业", country="中国",
        description="AI技术进入以Harness驾驭框架为标志的新时代，"
                    "通过标准化外部控制框架对大模型实现全流程管控，"
                    "打通园区IoT/ERP/能源/安防多系统，具备感知-决策-执行完整闭环",
        key_metrics={"framework": "Harness", "closed_loop": True,
                     "integrated_systems": ["IoT", "ERP", "energy", "security"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="架构参考：Harness框架可用于机器人系统全流程管控",
        deployment_ready=True,
        tags=["Harness", "驾驭框架", "闭环控制", "多系统集成"],
    ),

    # --- 6G网络 ---
    AIProduct(
        product_id="N6-003", name="5G-A商用与6G技术攻坚",
        category=AICategory.NETWORK_6G,
        organization="中国通信产业", country="中国",
        description="2026年处于5G-A商用、6G技术攻坚关键阶段，"
                    "5G-A实现万兆级传输速率、通感一体、超低时延，"
                    "6G核心技术进入研发攻坚，瞄准太赫兹通信、空天地一体化",
        key_metrics={"5ga_speed": "10Gbps", "6g_focus": ["terahertz", "space_air_ground"],
                     "sensing_communication": True},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="通信基础：低时延高可靠网络支撑机器人远程控制",
        deployment_ready=True,
        tags=["5G-A", "6G", "太赫兹", "通感一体", "空天地一体化"],
    ),

    # --- 工业机器人 ---
    AIProduct(
        product_id="IR-003", name="美的智能体工厂AI视觉推理",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="美的集团", country="中国",
        description="广东顺德、湖北武汉美的智能体工厂引入AI视觉推理平台，"
                    "检测节奏完全匹配生产节拍，AI直接参与生产决策，"
                    "大模型迅速转化为生产能力",
        key_metrics={"ai_vision": True, "production_decision": True,
                     "locations": ["顺德", "武汉"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="工业部署：AI视觉+机器人协作产线参考",
        deployment_ready=True,
        tags=["智能体工厂", "AI视觉", "生产决策", "工业AI"],
    ),
    AIProduct(
        product_id="IR-004", name="双臂番茄采摘机器人",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="江苏农科院", country="中国",
        description="双臂番茄采摘机器人单果采摘时间降至9秒，"
                    "整机成本降至20万元以下，"
                    "农业机器人从展示品走向大田标配",
        key_metrics={"pick_time_seconds": 9, "cost_below_wan": 20,
                     "arm_count": 2},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="直接：采摘机器人是具身智能农业典型应用",
        deployment_ready=True,
        tags=["采摘机器人", "双臂", "农业自动化", "低成本"],
    ),

    # --- 新能源 ---
    AIProduct(
        product_id="EN-005", name="宁波分布式光伏装机千万千瓦",
        category=AICategory.RENEWABLE_ENERGY,
        organization="国家电网", country="中国",
        description="全国首个分布式光伏装机突破千万千瓦城市，"
                    "年发电约100亿千瓦时，园区占比84%；"
                    "上线国内首个分布式光伏运行监测系统，虚拟电厂聚合储能与柔性负荷",
        key_metrics={"capacity_gw": 10, "annual_generation_billion_kwh": 100,
                     "park_ratio_pct": 84, "monitoring_system": "domestic_first"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="能源保障：智能电网为机器人充换电提供基础设施",
        deployment_ready=True,
        tags=["分布式光伏", "千万千瓦", "虚拟电厂", "运行监测"],
    ),
    AIProduct(
        product_id="EN-006", name="固态变压器量产效率98.5%",
        category=AICategory.RENEWABLE_ENERGY,
        organization="中国能源装备企业", country="中国",
        description="首款固态变压器产品实现10kV到800V交直流一步变换，"
                    "整机效率最高达98.5%，占地面积较传统方案减少60%以上，"
                    "2.5MVA碳化硅固态变压器同步推出",
        key_metrics={"efficiency_pct": 98.5, "footprint_reduction_pct": 60,
                     "voltage_conversion": "10kV->800V", "sic": True},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="供电技术：高效变电为机器人充电站提供技术支撑",
        deployment_ready=True,
        tags=["固态变压器", "碳化硅", "98.5%效率", "AIDC供电"],
    ),
    AIProduct(
        product_id="EN-007", name="中国移动通算融合虚拟电厂",
        category=AICategory.RENEWABLE_ENERGY,
        organization="中国移动", country="中国",
        description="聚合基站、数据中心等分布式可调资源，"
                    "5000个局站参与电能量市场调峰节电5132万度，"
                    "8000个局站加数据中心参与辅助服务削峰102万度",
        key_metrics={"stations_peak": 5000, "power_saved_million_kwh": 51.32,
                     "stations_ancillary": 8000},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="能源调度：通信设施虚拟电厂模式可参考机器人充换电网络",
        deployment_ready=True,
        tags=["虚拟电厂", "通算融合", "需求响应", "削峰填谷"],
    ),

    # --- 农业 ---
    AIProduct(
        product_id="AGR-004", name="YOLOFuse双光谱农业监测",
        category=AICategory.AGRICULTURE,
        organization="农业AI技术社区", country="全球",
        description="支持RGB与红外双光谱融合的智能检测框架，"
                    "全天候监测作物生长，早期病害识别通过红外温度异常发现，"
                    "精准灌溉指导通过温度分布判断缺水区域",
        key_metrics={"dual_spectrum": True, "modalities": ["RGB", "IR"],
                     "disease_early_detection": True, "irrigation_guidance": True},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="感知技术：双光谱视觉可用于农田巡检机器人",
        deployment_ready=True,
        tags=["双光谱", "YOLO", "病害识别", "精准灌溉", "无人机"],
    ),
    AIProduct(
        product_id="AGR-005", name="沃柑AI全产业链智慧种植",
        category=AICategory.AGRICULTURE,
        organization="南宁正欣农业", country="中国",
        description="3000亩沃柑基地布设气象与土壤墒情监测站，4个无人机基站全域巡检，"
                    "AI算法精准识别病虫害并推送防治方案，200多个土壤传感器实时监测，"
                    "水肥一体化单株精准灌溉，电动轨道运输年省柴油10万元",
        key_metrics={"area_mu": 3000, "drone_stations": 4,
                     "soil_sensors": 200, "ai_pest_detection": True},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="农业机器人：无人机巡检+智能灌溉为农业机器人提供场景",
        deployment_ready=True,
        tags=["智慧种植", "无人机巡检", "病虫害AI识别", "水肥一体化"],
    ),

    # --- 商业 ---
    AIProduct(
        product_id="CO-004", name="千问开放平台三端Agent生态",
        category=AICategory.COMMERCE,
        organization="阿里巴巴", country="中国",
        description="千问开放平台上线，手机/PC/AI眼镜三端同时开放，"
                    "顺丰速运、自如租房、哈啰租车、闪送、飞常准、美的美居等"
                    "十多个领域头部企业第一批接入，一句话完成寄件/租车/家政",
        key_metrics={"platforms": ["phone", "PC", "AI_glasses"],
                     "partners": 10, "launch_date": "2026-08-10"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="服务生态：AI Agent生态可对接机器人服务能力",
        deployment_ready=True,
        tags=["开放平台", "AI Agent", "三端同步", "生活服务"],
    ),

    # --- 水利 ---
    AIProduct(
        product_id="WA-004", name="构网型储能县域电网离网运行",
        category=AICategory.WATER_CONSERVANCY,
        organization="中国电力科学研究院", country="中国",
        description="内蒙古额济纳旗以25MW构网型储能作为支撑电源，"
                    "多次实现县域电网离网稳定运行；联络线意外跳闸后"
                    "系统自动转离网运行，重要负荷全部保住，首次实现非计划并网转离网",
        key_metrics={"storage_mw": 25, "county_grid": True,
                     "unplanned_islanding": "first_success"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="电网韧性：离网运行技术可用于机器人独立供电场景",
        deployment_ready=True,
        tags=["构网型储能", "离网运行", "县域电网", "电网韧性"],
    ),

    # --- 汽车 ---
    AIProduct(
        product_id="AU-004", name="新能源汽车月销占比首破60%",
        category=AICategory.AUTOMOTIVE,
        organization="中国汽车工业协会", country="中国",
        description="2026年7月新能源汽车月度新车销量占比首次突破60%，"
                    "累计占比首次突破50%，涵盖乘用车和商用车、国内销量和出口，"
                    "新能源乘用车国内占比达68.1%，出口连续两月超50%",
        key_metrics={"monthly_share_pct": 60, "cumulative_share_pct": 50,
                     "passenger_domestic_pct": 68.1, "export_share_pct": 50},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="产业趋势：电动化平台为机器人提供电池/电机技术基础",
        deployment_ready=True,
        tags=["新能源汽车", "销量突破", "电动化", "出口"],
    ),
    AIProduct(
        product_id="AU-005", name="城市NOA下探至10万标配",
        category=AICategory.AUTOMOTIVE,
        organization="中国智能驾驶产业", country="中国",
        description="2026年城市NOA从30万以上车型卖点下放至10万以下车型标配，"
                    "L2级新车渗透率达70%，NOA车型渗透率超30%，"
                    "激光雷达批量采购价从8万暴降至千元区间（最低900元）",
        key_metrics={"l2_penetration_pct": 70, "noa_penetration_pct": 30,
                     "lidar_cost_drop": "80000->900"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="传感器降本：激光雷达千元化惠及机器人感知",
        deployment_ready=True,
        tags=["城市NOA", "智能驾驶", "激光雷达", "万元下放"],
    ),

    # --- 数码产品 ---
    AIProduct(
        product_id="DP-004", name="字节跳动成立AI数据与安全一级部门",
        category=AICategory.DIGITAL_PRODUCT,
        organization="字节跳动", country="中国",
        description="成立AI数据与安全一级部门，与Seed/Flow/抖音平行，"
                    "整合多支分散数据团队，直指大模型跨模态数据服务；"
                    "豆包新增酒店等生活服务入口探索AI流量变现",
        key_metrics={"department_level": 1, "parallel_units": ["Seed", "Flow", "Douyin"],
                     "focus": "cross_modal_data"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="数据基础设施：跨模态数据服务支撑机器人训练",
        deployment_ready=True,
        tags=["AI组织", "数据安全", "跨模态", "豆包"],
    ),

    # --- 医疗健康 ---
    AIProduct(
        product_id="HC-004", name="AI新药研发周期从数年缩至数月",
        category=AICategory.HEALTHCARE,
        organization="中国医疗AI产业", country="中国",
        description="分子模拟、临床试验预测AI加速新药从实验室到药房进程，"
                    "研发周期从数年缩短至数月；2025年AI+医疗健康市场规模突破千亿元，"
                    "预计2026年跨越1500亿元，年复合增长率30%以上",
        key_metrics={"market_2025_billion": 100, "market_2026_billion": 150,
                     "cagr_pct": 30, "rd_acceleration": "years_to_months"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="AI for Science：药物研发AI方法可迁移至机器人材料发现",
        deployment_ready=True,
        tags=["AI制药", "AIDD", "分子模拟", "千亿市场"],
    ),
    AIProduct(
        product_id="HC-005", name="端侧AI可穿戴健康监测",
        category=AICategory.HEALTHCARE,
        organization="全球可穿戴产业", country="全球",
        description="2026年Q1全球支持端侧AI的智能手表出货量同比增长70%，"
                    "渗透率达25%；预计2032年每10台可穿戴设备8台搭载端侧AI，"
                    "智能手表监测高血压风险，动态血糖监测纳入多地医保",
        key_metrics={"shipment_growth_pct": 70, "penetration_pct": 25,
                     "2032_ai_ratio": "8/10", "glucose_monitoring": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="传感器融合：可穿戴健康监测技术可用于机器人状态感知",
        deployment_ready=True,
        tags=["可穿戴", "端侧AI", "健康监测", "智能手表"],
    ),
    AIProduct(
        product_id="HC-006", name="达芬奇机器人微创手术突破",
        category=AICategory.HEALTHCARE,
        organization="青大附院", country="中国",
        description="达芬奇机器人完成高难度开放手术微创化创新，"
                    "保留自体肺组织避免全肺切除；"
                    "2022年完成亚洲首例机器人辅助单肺移植、世界首例双肺移植",
        key_metrics={"surgical_robot": "da_vinci", "minimally_invasive": True,
                     "world_first": "double_lung_transplant"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="精密操作：手术机器人精细控制技术可参考",
        deployment_ready=True,
        tags=["手术机器人", "达芬奇", "微创", "肺移植"],
    ),

    # --- 民生 ---
    AIProduct(
        product_id="LV-004", name="腾讯出行接入Robotaxi无人驾驶",
        category=AICategory.LIVELIHOOD,
        organization="腾讯", country="中国",
        description="腾讯出行服务正式接入如祺Robotaxi，成为首个接入的一站式出行平台，"
                    "通过微信小程序提供自动驾驶叫车服务，"
                    "首批覆盖广州南沙、科学城等运营区域",
        key_metrics={"platform": "WeChat_miniprogram", "service": "robotaxi_hailing",
                     "coverage": ["Guangzhou_Nansha", "Science_City"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="出行服务：无人驾驶出租车是轮式机器人重要应用",
        deployment_ready=True,
        tags=["Robotaxi", "无人驾驶", "微信小程序", "智慧出行"],
    ),

    # --- 教育 ---
    AIProduct(
        product_id="ED-004", name="大连海事大学航海教育大模型1.0",
        category=AICategory.EDUCATION,
        organization="大连海事大学", country="中国",
        description="自主研发航海教育大模型1.0系统，聚焦航海技术/轮机工程/船舶电子电气"
                    "3个航海类专业，搭建专业知识库与结构化图谱，"
                    "部署多元应用型智能体集群，提供智能备课/学情分析/适任考试模拟",
        key_metrics={"majors": 3, "knowledge_graph": True,
                     "agent_cluster": True, "exam_simulation": True},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="专业教育：垂直领域大模型方法可用于机器人操作培训",
        deployment_ready=True,
        tags=["教育大模型", "航海教育", "智能备课", "适任考试"],
    ),

    # ===== 最新资讯/内容 =====

    AIProduct(
        product_id="LLM-007", name="DeepSeek V4-Pro-0813旗舰模型",
        category=AICategory.AI_LLM,
        organization="深度求索", country="中国",
        description="发布旗舰级模型，1.6万亿总参数/490亿激活参数，"
                    "100万上下文窗口，384K最大输出。输入0.435美元/百万token，"
                    "输出0.87美元/百万token，在Terminal Bench 2.1/Cybergym/"
                    "DeepSWE/AutomationBench等基准超越Opus 4.8，成本降低约57倍。",
        key_metrics={"total_params": "1.6T", "active_params": "49B",
                     "context_window": "1M", "max_output": "384K",
                     "cost_reduction": "57x"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="大模型推理能力：可用于机器人任务规划与代码生成",
        deployment_ready=True,
        tags=["大模型", "旗舰模型", "高性价比", "百万上下文"],
    ),

    AIProduct(
        product_id="LLM-008", name="Qwen3.8-2.4T-A95B开源大模型",
        category=AICategory.AI_LLM,
        organization="阿里千问", country="中国",
        description="2.4万亿参数MoE架构，950亿激活参数。"
                    "Qwen3.8-Max官方版本支持视觉输入、百万上下文、内置工具调用，"
                    "性能比肩国际顶尖闭源模型。",
        key_metrics={"total_params": "2.4T", "active_params": "95B",
                     "context_window": "1M", "open_source": True},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="开源MoE模型：可部署于机器人端云协同推理",
        deployment_ready=True,
        tags=["开源大模型", "MoE", "多模态", "百万上下文"],
    ),

    AIProduct(
        product_id="AG-009", name="腾讯混元Hy4大模型即将发布",
        category=AICategory.AI_AGENT,
        organization="腾讯", country="中国",
        description="腾讯二季度财报显示AI投入加速，"
                    "混元Hy4大模型近期将发布。WorkBuddy持续领跑国内办公智能体，"
                    "小微智能助手扩大灰测范围，游戏/广告/云业务受AI带动增长。",
        key_metrics={"product_line": "混元", "version": "Hy4",
                     "workbuddy_lead": True},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="智能体生态：办公智能体架构可迁移至机器人任务编排",
        deployment_ready=False,
        tags=["大模型", "办公智能体", "混元", "多端同步"],
    ),

    AIProduct(
        product_id="HR-007", name="国产机器人开辟出海通道",
        category=AICategory.HUMANOID_ROBOT,
        organization="海关总署", country="中国",
        description="今年前7个月工业机器人出口同比增长13.2%。"
                    "自1月增设独立海关税号以来，智能仿生机器人半年出口金额增长超5倍，"
                    "上半年出口量超8000台。海关打造一企一策精准服务，"
                    "建立机器人产品归类数据库覆盖300多款产品。",
        key_metrics={"industrial_export_growth": "13.2%",
                     "humanoid_export_growth": "5x",
                     "h1_humanoid_exports": "8000+",
                     "classified_products": 300},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="产业出海：人形机器人出口通道打通，全球化部署加速",
        deployment_ready=True,
        tags=["机器人出口", "海关税号", "人形机器人", "全球化"],
    ),

    AIProduct(
        product_id="IR-005", name="智能装备赋能海洋产业",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="", country="中国",
        description="智能装备与机器人技术加速赋能海洋产业，"
                    "覆盖海洋勘探、水下作业、海上风电运维等场景，"
                    "无人船、水下机器人、海洋观测装备等实现产业化应用。",
        key_metrics={"domain": "海洋产业", "autonomy": "unmanned"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="特种机器人：水下/海上极端环境机器人技术可迁移",
        deployment_ready=False,
        tags=["海洋机器人", "水下作业", "无人船", "海上风电"],
    ),

    AIProduct(
        product_id="AU-006", name="首部自动驾驶强制性国标GB 44721发布",
        category=AICategory.AUTOMOTIVE,
        organization="国家市场监督管理总局", country="中国",
        description="《智能网联汽车 自动驾驶系统安全要求》"
                    "（GB 44721-2026）强制性国家标准正式发布，2027年7月1日实施。"
                    "适用于L3/L4级载客载货车辆。L2级渗透率达70.5%，"
                    "NOA功能渗透率34.2%，首批L3车型在特定区域上路。",
        key_metrics={"standard": "GB 44721-2026", "effective_date": "2027-07-01",
                     "l2_penetration": "70.5%", "noa_penetration": "34.2%",
                     "level": "L3/L4"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="安全标准：自动驾驶安全框架可直接复用至机器人安全",
        deployment_ready=True,
        tags=["自动驾驶", "强制国标", "L3", "L4", "安全要求"],
    ),

    AIProduct(
        product_id="EN-008", name="亚洲首个柔直海上风电项目发电量超100亿千瓦时",
        category=AICategory.RENEWABLE_ENERGY,
        organization="三峡集团", country="中国",
        description="江苏如东800MW海上风电项目累计输送电量"
                    "突破100亿千瓦时。亚洲首个柔性直流输电海上风电项目，"
                    "±400千伏电压等级，安全运行超1600天，设备可利用率99.5%，"
                    "满足400万户家庭一年用电，节约标准煤300万吨，减碳740万吨。",
        key_metrics={"capacity": "800MW", "voltage": "±400kV",
                     "cumulative_generation": "100亿kWh",
                     "availability": "99.5%", "stable_days": "1600+"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="绿电基础：海上风电为机器人算力设施提供清洁能源",
        deployment_ready=True,
        tags=["海上风电", "柔性直流", "清洁能源", "减碳"],
    ),

    AIProduct(
        product_id="DP-005", name="Google Pixel 11 Gemini系统级AI",
        category=AICategory.DIGITAL_PRODUCT,
        organization="Google", country="美国",
        description="搭载Tensor G6芯片运行Gemini Nano，"
                    "Gemini Intelligence可跨40多个应用处理多步任务，"
                    "支持Rambler主动信息卡、端侧实时翻译，AI从入口变为系统能力。",
        key_metrics={"chip": "Tensor G6", "cross_app": 40,
                     "on_device": "Gemini Nano", "real_time_translate": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="端侧AI：跨应用智能体架构可迁移至机器人多任务执行",
        deployment_ready=True,
        tags=["AI手机", "端侧大模型", "跨应用智能体", "实时翻译"],
    ),

    AIProduct(
        product_id="AI-005", name="SpaceX AI价值预判与算力布局",
        category=AICategory.AI_GENERAL,
        organization="SpaceX", country="美国",
        description="马斯克表示SpaceX未来五年99%价值将来自AI，"
                    "火箭业务将成为副业。目标明年底算力达10吉瓦，"
                    "AI季度收入已近26亿美元。",
        key_metrics={"ai_value_ratio": "99%", "compute_target": "10GW",
                     "quarterly_ai_revenue": "26亿美元"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="算力基础设施：大规模算力为机器人智能提供支撑",
        deployment_ready=False,
        tags=["AI战略", "算力", "商业航天", "Grok"],
    ),

    AIProduct(
        product_id="CH-005", name="氮化镓芯片大规模交付6G空天地一体化网络",
        category=AICategory.AI_CHIP,
        organization="中国电科55所", country="中国",
        description="中国已开始大规模使用新型氮化镓(GaN)芯片"
                    "用于未来6G网络建设，已交付500万片。芯片支撑空天地一体化6G网络，"
                    "每终端集成功率放大芯片向卫星或地面站远距离发送信号。"
                    "GaN-on-Si技术兼顾高性能与低成本。",
        key_metrics={"material": "GaN-on-Si", "delivered": "500万片",
                     "application": "6G NTN", "integration": "空天地一体化"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="通信芯片：6G空天地一体化为机器人全域连接提供基础",
        deployment_ready=True,
        tags=["氮化镓", "6G芯片", "空天地一体化", "卫星通信"],
    ),

    AIProduct(
        product_id="NET-001", name="IMT-2030(6G)推进组星地融合NTN工作组成立",
        category=AICategory.NETWORK_6G,
        organization="工信部IMT-2030推进组", country="中国",
        description="在工信部指导下，"
                    "星地融合(NTN)工作组在北京正式成立。牵引国际技术标准研制，"
                    "统筹6G星地融合网络总体布局，培育卫星通信核心技术，"
                    "涵盖卫星空口接入、卫星终端、星地融合网络与运维应用。",
        key_metrics={"working_group": "NTN", "scope": "6G星地融合",
                     "standard": "国际标准研制"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="星地融合：6G NTN为机器人提供无盲区通信覆盖",
        deployment_ready=False,
        tags=["6G", "NTN", "星地融合", "卫星通信", "标准制定"],
    ),

    AIProduct(
        product_id="HC-007", name="国家医保局公开征集医保数字人形象",
        category=AICategory.HEALTHCARE,
        organization="国家医疗保障局", country="中国",
        description="国家医疗保障局面向社会公开征集医保数字人形象。"
                    "医保数字化加速推进，AI数字人将用于医保政策咨询、"
                    "业务办理引导、智能客服等场景，提升医保服务智能化水平。",
        key_metrics={"digital_human": True, "scope": "全国医保",
                     "application": "政策咨询/业务引导"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="数字人交互：医保数字人技术可复用至机器人服务交互",
        deployment_ready=False,
        tags=["数字人", "智慧医保", "AI客服", "政务服务"],
    ),

    AIProduct(
        product_id="EN-009", name="陆上大兆瓦风电铸件关键技术突破",
        category=AICategory.RENEWABLE_ENERGY,
        organization="", country="中国",
        description="我国在陆上大兆瓦风电铸件领域取得关键性"
                    "技术突破，为大型风电机组国产化提供核心部件支撑，"
                    "推动风电装备降本增效和规模化应用。",
        key_metrics={"breakthrough": "大兆瓦铸件", "domain": "陆上风电"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="绿色制造：风电装备智能制造与机器人产线协同",
        deployment_ready=False,
        tags=["风电铸件", "大兆瓦", "技术突破", "国产装备"],
    ),

    AIProduct(
        product_id="AG-010", name="DeepSeek Harness智能体工具框架",
        category=AICategory.AI_AGENT,
        organization="深度求索", country="中国",
        description="Harness业务线独立组建团队，专门负责将模型转化为智能体的"
                    "工具框架。Harness负责在模型之外调度上下文、工具、任务状态、"
                    "反馈与边界，完成从理解需求到交付代码的完整闭环。"
                    "DeepSeek-V4-Flash正式版已使用Harness极简模式框架测试，"
                    "对标Codex与Claude Code，秉承开放理念支持多模型接入。",
        key_metrics={"project": "DeepSeek Harness", "founded": "2026-05",
                     "scope": "Agent工具框架", "open": True},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="智能体框架：Harness调度模式可直接用于机器人任务编排与工具调用",
        deployment_ready=False,
        tags=["Harness", "智能体框架", "代码智能体", "开放生态"],
    ),

    AIProduct(
        product_id="WM-005", name="索塔无界原生4D物理世界模型落地商超",
        category=AICategory.WORLD_MODEL,
        organization="索塔无界", country="中国",
        description="成立4个月即签约欧洲最大商超集团，3年内部署超千台具身智能"
                    "机器人。自研原生4D物理世界基模，统一4D空间表征、物理约束、"
                    "时空推理、安全评测与动作输出。冷启动获10万小时专有数据，"
                    "正式部署后每年回传超100万小时真实操作数据，启动数据飞轮。",
        key_metrics={"deploy_target": "1000+ robots/3years",
                     "cold_start_data": "100K hours",
                     "annual_data": "1M+ hours",
                     "model_type": "4D物理世界基模"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="世界模型落地：4D物理世界模型直接驱动商超场景具身机器人操作",
        deployment_ready=False,
        tags=["4D世界模型", "物理智能", "商超场景", "数据飞轮", "出海"],
    ),

    AIProduct(
        product_id="AC-007", name="阿里云灵骏真武M890超节点实例上线",
        category=AICategory.AI_COMPUTE,
        organization="阿里云", country="中国",
        description="国内首个成功运行超2万亿参数大模型的超节点形态算力，"
                    "首批在乌兰察布地域开售。企业无需自建机房即可开通64卡高速"
                    "互联算力单元，最高承载十万亿参数级MoE大模型推理。"
                    "Kimi K3和Qwen3.8 Max均已通过该实例对外提供服务。",
        key_metrics={"gpu_per_node": 64, "max_params": "10T MoE",
                     "verified_models": "2T+", "location": "乌兰察布"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="超节点算力：64卡高速互联为机器人大模型推理提供云端算力",
        deployment_ready=True,
        tags=["超节点", "算力基础设施", "2万亿参数", "MoE推理", "国产算力"],
    ),

    AIProduct(
        product_id="HR-008", name="小鹏人形机器人进入小批量试产",
        category=AICategory.HUMANOID_ROBOT,
        organization="小鹏汽车", country="中国",
        description="小鹏人形机器人已在广州工厂正式启动小批量试产，"
                    "量产线进入最终调试阶段。计划2026年实现量产，"
                    "2027年起逐步进入全球门店和商业场景，承担导购、"
                    "讲解等服务。机器人业务整合硬件、AI大模型、"
                    "供应链和营销能力，复用汽车业务积累。",
        key_metrics={"status": "小批量试产", "mass_production": "2026",
                     "commercial": "2027", "factory": "广州"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="车企造机器人：汽车智驾技术与供应链迁移至人形机器人量产",
        deployment_ready=False,
        tags=["人形机器人", "小批量试产", "车企跨界", "商业服务"],
    ),

    AIProduct(
        product_id="AG-011", name="云从科技行云智能体操作系统",
        category=AICategory.AI_AGENT,
        organization="云从科技", country="中国",
        description="向AI基础设施+智能体转型。行云智能体操作系统定位为"
                    "职业学校，负责组织训练、安排协作、管理过程、验收结果；"
                    "魔方智能体实验室作为教科书，沉淀岗位经验、行业知识和"
                    "业务规则。云起ModelHub统一模型服务平台上线，"
                    "支持多模型按用量计费。同时入股广东省具身智能训练场。",
        key_metrics={"platform": "行云智能体OS", "hub": "云起ModelHub",
                     "strategy": "AI基础设施+智能体"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="智能体操作系统：多智能体协作框架可迁移至机器人群体协同",
        deployment_ready=True,
        tags=["智能体操作系统", "多模型服务", "具身智能训练场", "数字员工"],
    ),

    AIProduct(
        product_id="AG-006", name="AI田间地头全链条落地",
        category=AICategory.AGRICULTURE,
        organization="", country="中国",
        description="AI从展台走向田野。四川智数倍AD300智能插秧系统实现"
                    "自动行驶精准插秧；安徽砀山45万亩梨园AI管家节水节肥超三成，"
                    "优质果率提升至85%；河北孪智型育种机器人完成作物表型采集；"
                    "海南种业大模型丰登缩短育种周期；万蜂智能蛋鸡养殖自动化率"
                    "从20%提升至40%。全流程智能指导带动产量平均提升5%、"
                    "成本平均降低10%。",
        key_metrics={"yield_increase": "5%", "cost_reduction": "10%",
                     "orchard_area": "45万亩", "water_fertilizer_save": "30%",
                     "quality_rate": "85%"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="农业机器人：智能插秧、育种机器人、分选设备与具身操作技术相通",
        deployment_ready=True,
        tags=["智慧农业", "AI插秧", "育种机器人", "种业大模型", "精准施肥"],
    ),

    AIProduct(
        product_id="ED-005", name="AI技能培训促进青年就业",
        category=AICategory.EDUCATION,
        organization="", country="中国",
        description="四川深入推进提技能促就业专项行动，首批开设培训班306个，"
                    "预计培训1.2万余人。AI办公工具实操、新媒体短视频制作、"
                    "无人机驾驶操作等新兴领域课程占比超四成。设立人工智能"
                    "训练师等前沿课程，培训期间组织专场招聘会定向推介岗位，"
                    "实现培训即对接、结业即推荐。",
        key_metrics={"sessions": 306, "trainees": "12000+",
                     "emerging_courses": "40%+", "period": "8-10月"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="AI人才培养：人工智能训练师等新职业为机器人产业输送人才",
        deployment_ready=True,
        tags=["AI培训", "技能就业", "人工智能训练师", "产教融合"],
    ),

    AIProduct(
        product_id="LV-005", name="江苏政务服务三化改革与智慧晓苏智能体",
        category=AICategory.LIVELIHOOD,
        organization="江苏省数据局", country="中国",
        description="全面部署政务服务标准化、集成化、数智化改革。"
                    "标准化推动同一事项全省无差别受理；集成化以高效办成"
                    "一件事为牵引，全面集成至苏服办；数智化深化数智技术"
                    "全流程应用，加强智慧晓苏政务服务智能体建设，"
                    "推进电子证照、证明材料共享利用。先期9个部门试点"
                    "扩展至全省，力争一年完成改革目标。",
        key_metrics={"reform": "三化", "pilot_departments": 9,
                     "target": "一年完成", "agent": "智慧晓苏"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="政务智能体：智慧晓苏多轮对话与业务编排技术可复用至服务机器人",
        deployment_ready=False,
        tags=["智慧政务", "政务智能体", "三化改革", "数字政府", "苏服办"],
    ),

    AIProduct(
        product_id="CM-005", name="千问办公助理专业会员付费订阅上线",
        category=AICategory.COMMERCE,
        organization="阿里千问", country="中国",
        description="千问App正式推出办公助理专业会员付费订阅，分高级、"
                    "精英、旗舰三档，连续包月19至128元，均搭载Qwen3.8-Max"
                    "旗舰模型，支持本地与云端模式、手机远程操作、技能调用，"
                    "可直接交付网页、PPT、Word、Excel等文件。豆包月活3.82亿"
                    "居首，千问1.67亿位列第二，AI应用全面进入精细化付费阶段。",
        key_metrics={"price_range": "19-128元/月", "maize_doubao": "3.82亿",
                     "maize_qianwen": "1.67亿", "model": "Qwen3.8-Max"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="AI办公智能体：多文档生成与工具调用能力可迁移至机器人任务执行",
        deployment_ready=True,
        tags=["AI付费", "办公智能体", "千问", "豆包", "分层订阅"],
    ),

    AIProduct(
        product_id="AI-006", name="全球九大CSP资本开支8867亿美元",
        category=AICategory.AI_GENERAL,
        organization="", country="全球",
        description="2026年全球九大云端服务供应商AI服务器出货量年增率"
                    "预期上修至31%，合计资本开支突破8867亿美元，"
                    "同比增长约90%；2027年进一步增至1.32万亿美元。"
                    "投资重心从单纯堆GPU转向全链条升级：液冷散热、"
                    "先进封装、HBM4、1.6T光模组、高速PCB与机柜电源"
                    "进入订单放量阶段。",
        key_metrics={"capex_2026": "8867亿美元", "growth": "90%",
                     "capex_2027": "1.32万亿美元",
                     "server_growth": "31%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="算力基建：AI基础设施大规模投入为机器人智能提供算力底座",
        deployment_ready=True,
        tags=["资本开支", "AI服务器", "液冷", "1.6T光模块", "HBM4"],
    ),

    AIProduct(
        product_id="AG-007", name="AI智能体进入物流仓真实生产",
        category=AICategory.AI_AGENT,
        organization="", country="中国",
        description="AI智能体从辅助决策走向自主执行。天津武清仓内AI智能体"
                    "调度订单并直接交由具身智能机器人完成拣选，已实际运行"
                    "3个月，完成单量占该仓总单量10%。京东物流AI智能体应用"
                    "于供应链全链路超千个场景，超脑大模型2.0将亿级包裹"
                    "仿真推演压缩至3分钟内，人机协作效率提升超20%。"
                    "中科智源开发53款物流全链条预置智能体。",
        key_metrics={"operation_months": 3, "order_share": "10%",
                     "jd_scenarios": "1000+",
                     "simulation_time": "3min/亿级",
                     "efficiency_gain": "20%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="具身智能落地：AI智能体调度机器人拣选是最直接的具身智能商业落地",
        deployment_ready=True,
        tags=["物流智能体", "具身机器人", "智能拣选", "供应链AI", "仓储自动化"],
    ),

    AIProduct(
        product_id="DP-006", name="Google Pixel 11系列AI手机",
        category=AICategory.DIGITAL_PRODUCT,
        organization="Google", country="美国",
        description="Pixel 11系列搭载Tensor G6处理器运行最新Gemini Nano，"
                    "Gemini Intelligence可跨越40多个应用处理多步任务，"
                    "通过Rambler、主动信息卡和端侧实时翻译将AI嵌入手机日常流程。"
                    "新增Pixel Glow镜头彩灯展示Gemini后台执行状态，"
                    "AI从入口升级为系统级能力。",
        key_metrics={"chip": "Tensor G6", "ai_model": "Gemini Nano",
                     "cross_apps": "40+", "process": "2nm"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="端侧AI：Gemini Nano端侧推理能力为机器人端侧决策提供参考",
        deployment_ready=True,
        tags=["AI手机", "Tensor G6", "Gemini", "端侧AI", "Pixel Glow"],
    ),

    AIProduct(
        product_id="LM-010", name="DeepSeek V4 Pro 0813版上线API",
        category=AICategory.AI_LLM,
        organization="深度求索", country="中国",
        description="DeepSeek官方API模型页将V4 Pro版本切换为0813，"
                    "支持100万上下文、384K最大输出和多种接口。"
                    "国产大模型持续包揽全球调用榜前列，DeepSeek V4 Flash登顶。",
        key_metrics={"context": "1M", "max_output": "384K",
                     "version": "0813", "ranking": "全球调用榜登顶"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="大模型基座：百万上下文长文本理解能力支撑机器人任务规划",
        deployment_ready=True,
        tags=["DeepSeek", "V4 Pro", "百万上下文", "API", "国产大模型"],
    ),

    AIProduct(
        product_id="DP-007", name="荣耀Robot Phone全球首款机器人手机",
        category=AICategory.DIGITAL_PRODUCT,
        organization="荣耀", country="中国",
        description="全球首款机器人手机，四自由度钛合金云台支持自动构图、"
                    "人物跟拍与直播追焦，可按自然语言指令调整拍摄角度。"
                    "系统级智能体架构下YOYO Pro联动摄像头、麦克风与云台"
                    "实现手势识别和环境感知，携手阿里适配千问大模型。"
                    "影像与ARRI联合开发，配2亿像素云台主摄。"
                    "机械执行机构写进AI手机定义，AI从算法+屏幕进入算法+机械执行阶段。",
        key_metrics={"dof": 4, "camera": "2亿像素",
                     "price_start": 9999, "ai_agent": "YOYO Pro",
                     "partner": "千问大模型"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="Agentic设备：智能体驱动机械云台是AI操控物理世界的消费级验证",
        deployment_ready=True,
        tags=["机器人手机", "机械云台", "YOYO智能体", "Agentic设备", "千问"],
    ),

    AIProduct(
        product_id="RE-006", name="宁波分布式光伏装机突破千万千瓦",
        category=AICategory.RENEWABLE_ENERGY,
        organization="", country="中国",
        description="宁波成为全国首个分布式光伏装机达千万千瓦的城市，"
                    "全部扎根工业园区、公共楼宇与居民屋顶等碎片化空间，"
                    "园区占比84%。年发电约100亿千瓦时，减排500万吨。"
                    "搭建电力气象预测模型，新能源出力预测准确率达96%；"
                    "市级虚拟电厂聚合百万千瓦可调资源，数分钟内完成储能补能"
                    "与负荷调节。国内首个分布式光伏运行监测系统实时识别正反向潮流。",
        key_metrics={"capacity": "10GW", "industrial_ratio": "84%",
                     "annual_output": "100亿kWh", "co2_reduction": "500万吨",
                     "forecast_accuracy": "96%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="能源调度：虚拟电厂聚合调度模式与机器人多关节协同调度同源",
        deployment_ready=True,
        tags=["分布式光伏", "虚拟电厂", "千万千瓦", "电力气象", "潮流监测"],
    ),

    AIProduct(
        product_id="WC-004", name="数字孪生赋能智慧防汛立体感知",
        category=AICategory.WATER_CONSERVANCY,
        organization="水利部", country="中国",
        description="天空地水工一体化智能感知平台为防汛装上智慧大脑。"
                    "气象卫星、水利测雨雷达、4615处雨量站、438处水文站"
                    "构建三道监测防线，SAR卫星遥感、无人机巡测、ADCP流速"
                    "测量投入实战。全国产化洪水预报系统将预见期从3天"
                    "延长至4-7天，提前30小时锁定特大洪水、提前60小时"
                    "预判1号洪水。数字孪生防洪调度系统模拟各类暴雨情景"
                    "洪水演进，推演多套泄洪方案。",
        key_metrics={"rain_stations": 4615, "hydro_stations": 438,
                     "forecast_days": "4-7天", "advance_lock": "30-60小时",
                     "satellite_phones": 121},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="数字孪生：洪水演进仿真与机器人世界模型物理推演技术相通",
        deployment_ready=True,
        tags=["智慧防汛", "数字孪生", "天空地水工", "洪水预报", "国产化"],
    ),

    AIProduct(
        product_id="AU-007", name="smart精灵1号搭载千亿参数WAM世界模型",
        category=AICategory.AUTOMOTIVE,
        organization="", country="中国",
        description="全新一代smart精灵1号搭载满血版千里浩瀚H5辅助驾驶系统，"
                    "采用英伟达Orin Y芯片，基于内置千亿参数WAM世界行为模型"
                    "赋能的G-ASD 4.0解决方案，配合含激光雷达在内的31个"
                    "感知硬件，领航辅助覆盖城市和高速场景。全系标配800V"
                    "碳化硅高压平台，AI空调自主感知调节座舱环境。",
        key_metrics={"chip": "Orin Y", "model": "WAM世界模型",
                     "sensors": 31, "voltage": "800V",
                     "charge_time": "12min(10%-80%)"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="车载世界模型：WAM世界行为模型直接赋能自动驾驶物理场景推演",
        deployment_ready=True,
        tags=["智能汽车", "WAM世界模型", "Orin Y", "800V", "G-ASD"],
    ),

    AIProduct(
        product_id="AU-008", name="地平线与大众深化AI大模型合作",
        category=AICategory.AUTOMOTIVE,
        organization="地平线/大众集团", country="中德",
        description="通过合资公司酷睿程，大众基于白盒授权模式，"
                    "依托地平线AI基础大模型能力自主开发统一AI驾驶方案。"
                    "大模型与在研系统级芯片C7H及GAIA世界模型数据平台"
                    "深度协同，全面赋能大众L3/L4自动驾驶能力，"
                    "为未来乘用车和自动驾驶出租车奠定技术基础。",
        key_metrics={"chip": "C7H", "platform": "GAIA世界模型",
                     "level": "L3/L4", "model": "白盒授权"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="智驾芯片+世界模型：C7H+GAIA方案为机器人端侧推理提供参考",
        deployment_ready=False,
        tags=["地平线", "大众", "C7H", "GAIA", "L3/L4", "白盒授权"],
    ),

    AIProduct(
        product_id="DP-008", name="千问开放AI眼镜生态",
        category=AICategory.DIGITAL_PRODUCT,
        organization="阿里千问", country="中国",
        description="千问向开发者开放AI眼镜端能力，开发者用自然语言"
                    "即可打造随身AI助手。开放手机、PC及AI眼镜等终端能力，"
                    "接入酒旅、打车、物流、闪送等十余项生活服务。"
                    "AI眼镜竞争从硬件规格转向AI模型迭代深度和生态开放。",
        key_metrics={"terminals": "手机/PC/眼镜", "services": "10+",
                     "dev_method": "自然语言"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="可穿戴AI：眼镜端多模态感知与自然语言交互可迁移至机器人头部",
        deployment_ready=True,
        tags=["AI眼镜", "千问", "开放生态", "随身助手", "多终端"],
    ),

    AIProduct(
        product_id="AC-008", name="英特尔启动150亿美元配股重注AI",
        category=AICategory.AI_CHIP,
        organization="Intel", country="美国",
        description="英特尔正式启动总额150亿美元有偿配股计划，"
                    "为上市以来首次大规模配股，资金重点投向AI芯片研发。"
                    "同时苹果调整M系芯片路线，取消M6 Pro/Max/Ultra，"
                    "集中资源研发M7，顶配M7 Ultra AI算力目标对标"
                    "英伟达专业AI加速芯片。",
        key_metrics={"funding": "150亿美元", "scope": "AI芯片研发",
                     "type": "首次大规模配股"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="算力芯片：AI芯片军备竞赛为机器人提供更强端侧算力选择",
        deployment_ready=True,
        tags=["英特尔", "配股", "AI芯片", "150亿美元", "M7"],
    ),

    AIProduct(
        product_id="AG-012", name="Manus恢复独立运营",
        category=AICategory.AI_AGENT,
        organization="Manus", country="中国",
        description="AI智能体公司Manus宣布恢复独立运营，部分用户数据"
                    "将按规定迁移。作为通用AI智能体代表性产品，"
                    "Manus的独立运营标志着AI Agent赛道从平台依附"
                    "走向独立发展，智能体产品商业化路径持续探索。",
        key_metrics={"status": "恢复独立运营", "type": "通用AI智能体"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="通用智能体：Manus的多步骤任务自主执行框架可用于机器人任务规划",
        deployment_ready=False,
        tags=["Manus", "AI智能体", "独立运营", "通用Agent"],
    ),

    AIProduct(
        product_id="LM-011", name="腾讯混元4大模型训练中",
        category=AICategory.AI_LLM,
        organization="腾讯", country="中国",
        description="腾讯正在训练更大参数版本的混元4，预计今年晚些发布。"
                    "Hy3正式版日均Token用量是preview版的7倍，持续位列"
                    "全球前三。腾讯形成多层次模型体系，WorkBuddy PC端"
                    "访问量突破2000万居国内同类第一。二季度资本开支527.8亿元"
                    "同比增176%，算力优先用于训练自研模型。",
        key_metrics={"capex_q2": "527.8亿元", "growth": "176%",
                     "token_growth": "7x", "workbuddy_pv": "2000万",
                     "next_model": "混元4"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="模型体系：多层次模型按成本效益分配任务的策略适用于机器人算力调度",
        deployment_ready=True,
        tags=["腾讯", "混元4", "WorkBuddy", "Token", "资本开支"],
    ),

    AIProduct(
        product_id="BB-007", name="蚌埠智能传感产业半年产值50.49亿元",
        category=AICategory.BENGBU_LOCAL,
        organization="", country="中国",
        description="今年上半年蚌埠市82家智能传感规上工业企业产值达"
                    "50.49亿元，同比增长15%。蚌埠深耕智能传感优势赛道，"
                    "持续完善产业链条、优化产业生态，创新成果加速落地。"
                    "国显科技建成新型物联网移动显示模组智能工厂，"
                    "设备联网率100%、产线自动化率80%，获国家级卓越级智能工厂。"
                    "广鼎科技研发智鼎数字人、仿生人形机器人及智能巡检机器狗。",
        key_metrics={"enterprises": 82, "output": "50.49亿元",
                     "growth": "15%", "networking_rate": "100%",
                     "automation_rate": "80%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="本地传感产业：智能传感器是机器人感知层核心硬件，蚌埠产业直接配套",
        deployment_ready=True,
        tags=["蚌埠", "智能传感", "50.49亿", "智能工厂", "数字人", "机器狗"],
    ),

    AIProduct(
        product_id="AI-007", name="物理AI进入规模化验证期",
        category=AICategory.AI_GENERAL,
        organization="", country="全球",
        description="物理AI赛道迈入产业化验证阶段。最近18个月超百亿美元"
                    "涌入，2026年92%资金集中投向有落地订单的头部企业。"
                    "宇树科技上半年营收10.52-11.28亿元，实现盈利。"
                    "Momenta搭载量产车突破100万台、定点车型超210款，"
                    "获德国L4测试许可。物理AI以47.2%年复合增速成长，"
                    "2040年全球关联产业规模有望达3.25万亿美元。"
                    "数据、场景、闭环成为核心竞争要素。",
        key_metrics={"funding_18m": "100亿美元+", "unitree_revenue": "10.52亿",
                     "momenta_vehicles": "100万", "cagr": "47.2%",
                     "market_2040": "3.25万亿美元"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="产业风向标：物理AI即具身智能，规模化验证标志机器人商业化拐点",
        deployment_ready=True,
        tags=["物理AI", "具身智能", "宇树", "Momenta", "规模化验证", "数据飞轮"],
    ),

    AIProduct(
        product_id="RE-007", name="上半年储能电池销量同比增长53%",
        category=AICategory.RENEWABLE_ENERGY,
        organization="", country="中国",
        description="2026年上半年国内储能电池销量同比增长53%，"
                    "大储电池贡献主要增量。温控市场规模同比增41%，"
                    "消防系统增38%，PCS系统增45%。储能出口额同比增48%。"
                    "行业从拼价格进入拼技术、拼交付、拼安全阶段，"
                    "独立储能商业模式逐步跑通，储能从成本项转向收益项。",
        key_metrics={"battery_growth": "53%", "thermal_growth": "41%",
                     "fire_growth": "38%", "pcs_growth": "45%",
                     "export_growth": "48%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="储能技术：高安全储能系统为移动机器人长时续航提供能源方案",
        deployment_ready=True,
        tags=["储能", "销量增长53%", "独立储能", "温控消防", "出口"],
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
