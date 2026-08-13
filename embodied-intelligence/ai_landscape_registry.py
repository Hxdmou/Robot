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
        organization="Manus", country="新加坡",
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
        organization="远景科技集团", country="中国",
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
        organization="中科曙光/海光信息", country="中国",
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
        organization="上海AI Lab/浙江大学/新加坡国立大学", country="中国",
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
        organization="中国电信（杭州双浦）", country="中国",
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
        organization="苏州灵猴机器人", country="中国",
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
        organization="中国传感谷/中国玻璃谷", country="中国",
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
        organization="蚌埠市工信局", country="中国",
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
        organization="北方微电子研究院/蚌医一附院", country="中国",
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
        organization="安徽华鑫微纳集成电路有限公司", country="中国",
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
        organization="小米生态/蚌埠传感谷企业", country="中国",
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
        organization="蚌埠市人大/经开区", country="中国",
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
    # 更新：19大模块最新AI产品与技术进展
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
                     },
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
        product_id="AGR-022", name="AI田间地头全链条落地",
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
        product_id="AG-020", name="AI智能体进入物流仓真实生产",
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

    # ==================================================================
    # 搜索新增内容
    # ==================================================================

    # --- 人形机器人 ---
    AIProduct(
        product_id="HR-009", name="第二届世界人形机器人运动会",
        category=AICategory.HUMANOID_ROBOT,
        organization="", country="中国",
        description="第二届世界人形机器人运动会将于8月22日在国家速滑馆"
                    "'冰丝带'开幕，由北京市人民政府、中央广播电视总台等"
                    "联合主办。吸引六大洲16个国家666支队伍、2056台机器人"
                    "同台竞技，队伍总量同比增长138%，机器人数量翻两番。"
                    "赛项从首届26个拓展至51个，构建全维度技术练兵场。",
        key_metrics={"countries": 16, "teams": 666, "robots": 2056,
                     "events": 51, "team_growth": "138%"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="国际级赛事加速机器人运动控制、感知决策技术迭代",
        deployment_ready=False,
        tags=["人形机器人运动会", "16国", "51赛项", "冰丝带"],
    ),
    AIProduct(
        product_id="HR-010", name="优必选与哈萨克斯坦战略合作",
        category=AICategory.HUMANOID_ROBOT,
        organization="", country="中国",
        description="优必选与哈萨克斯坦代表团在上海举行高层会晤并正式"
                    "签署全面战略合作备忘录。合作围绕产业落地、科研创新、"
                    "教育普及三大核心维度展开，旨在打造中亚具身智能领域"
                    "标杆企业，推动哈方技术人才培养体系和高端制造业升级。",
        key_metrics={"cooperation_dimensions": 3},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="中国人形机器人技术出海中亚，产业落地+科研+教育三位一体",
        deployment_ready=True,
        tags=["优必选", "哈萨克斯坦", "出海", "中亚"],
    ),
    AIProduct(
        product_id="HR-011", name="柔性电子皮肤感知末端",
        category=AICategory.HUMANOID_ROBOT,
        organization="", country="中国",
        description="浙江清华柔性电子技术研究院研发的柔性触觉感知末端，"
                    "超薄、柔韧、可拉伸，可像电子皮肤无缝贴合机器人指尖、"
                    "手臂等任意曲面，实时感知压力、温度、纹理多维信息。"
                    "配合力控算法实现从轻柔抓取易损物品到稳固夹持重物的"
                    "连续精细调节。已实现最大月产1000只智能感知夹爪交付装机。",
        key_metrics={"monthly_capacity": 1000, "sensing_modes": "压力/温度/纹理"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="解决人形机器人触觉感知盲区，物理交互数据采集入口",
        deployment_ready=True,
        tags=["电子皮肤", "柔性触觉", "力控算法", "感知夹爪", "数据采集"],
    ),

    # --- AI智能体 ---
    AIProduct(
        product_id="AG-013", name="英伟达Nemotron 3.5 Lightning开源智能体模型",
        category=AICategory.AI_AGENT,
        organization="", country="美国",
        description="英伟达发布30B参数MoE开源模型Nemotron 3.5 Lightning，"
                    "激活参数仅3B，专为长时间自主运行的AI智能体设计。"
                    "Token生成速度达同级开源模型4倍，任务完成时间缩短30%。"
                    "开放权重支持本地微调，可在RTX 5090、Jetson等设备运行。"
                    "同步开源NeMo Switchyard路由库，任务完成成本降至Opus 4.8的1/3。",
        key_metrics={"total_params": "30B", "active_params": "3B",
                     "speedup": "4x", "cost_reduction": "3倍"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="轻量高速开源模型可直接部署于机器人端侧智能体",
        deployment_ready=True,
        tags=["英伟达", "Nemotron", "开源", "MoE", "智能体", "本地部署"],
    ),
    AIProduct(
        product_id="AG-014", name="蚂蚁百灵Ling-3.0-tiny端侧开源模型",
        category=AICategory.AI_AGENT,
        organization="", country="中国",
        description="蚂蚁百灵开源端侧轻量模型Ling-3.0-tiny，总参数7.9B，"
                    "激活仅1.3B，融合多家注意力架构优势。FP8精度下在"
                    "M4 Pro MacBook上达86-90 tok/s，8K上下文仅占8.34GB内存，"
                    "数据全程不出本地。提供三个精度版本，支持本地知识引擎复刻。",
        key_metrics={"total_params": "7.9B", "active_params": "1.3B",
                     "tokens_per_sec": "86-90", "memory_8k": "8.34GB"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="超轻量端侧模型适合机器人本体实时推理，隐私安全",
        deployment_ready=True,
        tags=["蚂蚁百灵", "端侧模型", "开源", "本地推理", "隐私"],
    ),
    AIProduct(
        product_id="AG-015", name="DeepSeek Harness官方公众号独立运营",
        category=AICategory.AI_AGENT,
        organization="", country="中国",
        description="DeepSeek Harness官方微信公众号完成注册，为Harness"
                    "业务线首次单独设立官方发布阵地。Harness团队2026年5月"
                    "内部立项，独立组建专项核心团队。Harness负责在模型之外"
                    "调度上下文、工具、任务状态、反馈与边界，完成从理解需求"
                    "到交付代码的完整闭环，秉承开放理念支持多模型接入。",
        key_metrics={"team_established": "2026-05"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="Harness框架可直接用于机器人任务编排与工具调用",
        deployment_ready=False,
        tags=["DeepSeek", "Harness", "代码智能体", "开放生态"],
    ),

    # --- AI算力 ---
    AIProduct(
        product_id="CP-007", name="Omdia上调2026全球半导体增幅至94.1%",
        category=AICategory.AI_COMPUTE,
        organization="", country="全球",
        description="Omdia将2026年全球半导体市场营收增长预测上调至"
                    "同比增长94.1%，预计存储器芯片收入占全球半导体总营收"
                    "50%以上。AI需求持续超过全球供应能力，DRAM和NAND"
                    "市场强劲增长，HBM、先进封装产能瓶颈持续，供应紧张"
                    "局面短期难以缓解。",
        key_metrics={"semiconductor_growth": "94.1%", "memory_share": ">50%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="半导体供应紧张影响机器人算力芯片成本与交付",
        deployment_ready=True,
        tags=["半导体", "存储器", "HBM", "先进封装", "产能瓶颈"],
    ),
    AIProduct(
        product_id="CP-008", name="国产三维近存计算AI芯片架构突破",
        category=AICategory.AI_COMPUTE,
        organization="", country="中国",
        description="中国首款采用软件定义和三维近存计算技术的AI芯片"
                    "正式亮相，14nm工艺实现每秒5.2万亿次浮点运算。"
                    "通过创新底层架构，建立不依赖先进工艺的高端算力"
                    "发展路径。采用软件定义和三维垂直堆叠技术，计算单元"
                    "与存储单元紧密集成，访存带宽达6.4TB/s，从架构层面"
                    "缓解'内存墙'瓶颈。同步发布全栈软件工具链。",
        key_metrics={"process": "14nm", "flops": "5.2TFLOPS",
                     "bandwidth": "6.4TB/s"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="近存计算架构降低机器人芯片对先进制程依赖",
        deployment_ready=False,
        tags=["近存计算", "三维堆叠", "软件定义", "14nm", "内存墙"],
    ),

    # --- AI芯片 ---
    AIProduct(
        product_id="CH-006", name="海光信息进军嵌入式AI市场",
        category=AICategory.AI_CHIP,
        organization="", country="中国",
        description="海光信息在光合组织2026智能计算应用大会上首次完整"
                    "展出数据中心、边缘计算、物理端侧全场景AI计算方案，"
                    "宣布进军嵌入式原生AI场景。海光CPU与DCU已应用于"
                    "曙光8000十万卡AI超集群落地，验证国产计算和加速芯片"
                    "对大规模算力基础设施的支持能力。",
        key_metrics={"scenarios": "数据中心/边缘/端侧"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="嵌入式AI芯片直接服务于机器人端侧推理",
        deployment_ready=True,
        tags=["海光", "嵌入式AI", "DCU", "全场景算力", "国产"],
    ),

    # --- AI大模型 ---
    AIProduct(
        product_id="LLM-009", name="字节跳动讨论训练超5万亿参数模型",
        category=AICategory.AI_LLM,
        organization="", country="中国",
        description="字节跳动内部正在讨论训练参数规模超过5万亿的全新"
                    "大模型。模型预训练数据和架构已有初步方案，但最终规格"
                    "和发布时间未定，核心训练尚未启动。张一鸣表示'可接受"
                    "暂时落后'，聚焦长期技术积累。",
        key_metrics={"target_params": ">5万亿"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="超大规模模型为机器人通用智能提供基础能力",
        deployment_ready=False,
        tags=["字节跳动", "5万亿参数", "大模型", "预训练"],
    ),
    AIProduct(
        product_id="LLM-010", name="国产大模型包揽OpenRouter全球调用榜前五",
        category=AICategory.AI_LLM,
        organization="", country="中国",
        description="全球模型聚合平台OpenRouter最新周度Token调用榜显示，"
                    "国产大模型包揽前五，DeepSeek V4 Flash登顶。中国模型"
                    "份额一年内从30%飙升至60%，HuggingFace热度榜前三"
                    "全部来自中国团队。中国开源模型全球下载量占比41%居"
                    "世界第一，80%美国AI初创路演使用中国开源模型。",
        key_metrics={"global_share": "60%", "download_share": "41%",
                     "us_startup_usage": "80%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="国产模型全球主导地位降低机器人AI供应链风险",
        deployment_ready=True,
        tags=["OpenRouter", "DeepSeek", "开源", "全球第一", "调用榜"],
    ),

    # --- 世界模型 ---
    AIProduct(
        product_id="WM-006", name="Yann LeCun创立AMI Labs专注世界模型",
        category=AICategory.WORLD_MODEL,
        organization="", country="美国",
        description="图灵奖得主Yann LeCun离开Meta AI后创立专注世界模型"
                    "的AMI Labs，2026年3月获得创纪录的10.3亿美元种子轮"
                    "融资。LeCun认为现有LLM路线彻底错误，单纯预测文本"
                    "无法触及人类级智能，需要能理解物理现实的世界模型。"
                    "李飞飞World Labs同期累计融资12.3亿美元，估值约50亿美元。",
        key_metrics={"seed_funding": "10.3亿美元", "world_labs_valuation": "50亿美元"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="世界模型是机器人理解物理现实、预测行动后果的核心",
        deployment_ready=False,
        tags=["LeCun", "AMI Labs", "世界模型", "物理现实", "种子轮"],
    ),

    # --- 6G网络 ---
    AIProduct(
        product_id="NET-002", name="工信部启动6G部省协同试点",
        category=AICategory.NETWORK_6G,
        organization="", country="中国",
        description="工信部已启动6G创新发展部省协同试点专项行动，"
                    "国内6G研发进入第二阶段，重点推进原型样机研发与"
                    "实景场景测试。第一阶段已完成，累计产出300多项"
                    "关键技术。当前6G样机存在造价高、功耗偏高、散热难、"
                    "稳定性不足等短板，全国统一搭建国家级试验平台集中攻关。"
                    "按规划2029年敲定完整6G国际标准，2030年前后商用。",
        key_metrics={"key_techs_phase1": "300+", "standard_freeze": "2029",
                     "commercial": "2030"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="6G通算融合为机器人提供端边云协同算力网络",
        deployment_ready=False,
        tags=["6G", "部省协同", "原型样机", "通算融合", "2030商用"],
    ),

    # --- 工业机器人 ---
    AIProduct(
        product_id="IR-006", name="上海具身智能机器人产业展览会超500家参展",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="", country="中国",
        description="2026第四届上海具身智能机器人产业展览会在上海新国际"
                    "博览中心举行，超五百家行业主流品牌参展。设立整机机器人、"
                    "核心零部件（关节/灵巧手/传感器/芯片）、大模型与操作系统、"
                    "场景化解决方案（工业/服务/特种/医疗）四大主题展区，"
                    "集中展示人形机器人、四足机器人、协作机器人等最新产品。",
        key_metrics={"exhibitors": "500+"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="产业展会集中展示机器人全产业链最新技术",
        deployment_ready=True,
        tags=["上海", "具身智能展", "500家", "零部件", "场景方案"],
    ),
    AIProduct(
        product_id="IR-007", name="智元机器人累计出货1万台",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="", country="中国",
        description="智元机器人累计出货量达1万台，上半年出货8400台"
                    "占据全球44%市场份额。在南昌3C产线上连续作业超一个月，"
                    "完成连续8小时、两千多项任务零失误作业。清洁领域"
                    "数千台发货量实现盈利转正。采用'一体三智'技术架构，"
                    "生成式运控基座模型让动作不依赖预编排，端到端多模态"
                    "交互大模型将时延压缩至毫秒级。",
        key_metrics={"total_shipment": "10000", "h1_share": "44%",
                     "zero_error_tasks": "2000+"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="万台级出货标志人形机器人进入规模化量产阶段",
        deployment_ready=True,
        tags=["智元", "万台出货", "3C产线", "零失误", "量产"],
    ),

    # --- 蚌埠本地 ---
    AIProduct(
        product_id="BB-008", name="蚌山区与中科大先研院共建具身智能联合实验室",
        category=AICategory.BENGBU_LOCAL,
        organization="", country="中国",
        description="蚌山区与中国科学技术大学先进技术研究院签订具身智能"
                    "联合实验室共建协议。实验室5月22日完成施工图纸送审，"
                    "5月28日进场施工，8月31日全面竣工交付。蚌山区集聚"
                    "凌坤智能（纺纱搬运机器人）、他山科技（人形机器人）、"
                    "仙童智能（工业机器人）等企业，已向蚌山区推送企业2家，"
                    "储备优质企业5家。",
        key_metrics={"completion_date": "2026-08-31", "local_companies": "4+"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="蚌埠本地具身智能产学研基地，机器人产业生态",
        deployment_ready=False,
        tags=["蚌埠", "蚌山区", "中科大", "具身智能实验室", "凌坤", "他山科技"],
    ),
    AIProduct(
        product_id="BB-009", name="第八届MEMS智能传感器产业生态发展大会将在蚌埠举办",
        category=AICategory.BENGBU_LOCAL,
        organization="", country="中国",
        description="第八届MEMS智能传感器产业生态发展大会将在蚌埠举办。"
                    "蚌埠成功入围制造业新型技术改造试点城市。上半年全市"
                    "规上工业增加值增长超过10.1%，居全省第5、皖北第1位。"
                    "爱科智能实验室装备制造基地项目已投产。蚌埠作为"
                    "'中国传感谷'持续完善智能传感器产业链。",
        key_metrics={"industrial_growth": "10.1%", "rank_province": "第5",
                     "rank_north_anhui": "第1"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="MEMS传感器是机器人感知系统核心元器件",
        deployment_ready=True,
        tags=["蚌埠", "MEMS", "智能传感器", "中国传感谷", "技改试点"],
    ),

    # --- 新能源AI ---
    AIProduct(
        product_id="EN-010", name="山西零碳运输通道11.36亿元招标",
        category=AICategory.RENEWABLE_ENERGY,
        organization="", country="中国",
        description="山西省高速公路零碳运输通道建设项目正式进入招标筹备，"
                    "总投资约11.36亿元。依托全省高速公路网络，在收费站、"
                    "服务区及省界收费站布局重型卡车专用充电站，同步配套"
                    "储能系统、变配电设施及附属工程，构建支撑货运电动化的"
                    "基础设施体系。计划2026年9月发布资格预审公告。",
        key_metrics={"investment": "11.36亿元"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="绿色能源基础设施为机器人充换电网络提供参考",
        deployment_ready=False,
        tags=["山西", "零碳运输", "重卡充电站", "储能", "高速"],
    ),
    AIProduct(
        product_id="EN-011", name="晶科能源拉曼微裂纹检测技术获WITec金奖",
        category=AICategory.RENEWABLE_ENERGY,
        organization="", country="中国",
        description="晶科能源联合苏州大学攻克光伏'薄片化'难题，首创"
                    "高分辨拉曼+电学成像技术，实现亚微米级微裂纹与应力"
                    "分布可视化，揭示其与电学衰减的直接关联。助力飞虎3"
                    "组件首年衰减<1%、30年质保领先。荣膺2026年WITec"
                    "论文奖金奖，标志中国光伏基础科研与产业化融合突破。",
        key_metrics={"resolution": "亚微米级", "first_year_degradation": "<1%",
                     "warranty": "30年"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="AI视觉检测技术可迁移至机器人零部件质量检测",
        deployment_ready=True,
        tags=["晶科能源", "拉曼检测", "微裂纹", "光伏组件", "质量控制"],
    ),
    AIProduct(
        product_id="EN-012", name="山东新型储能集中调用1198万千瓦创纪录",
        category=AICategory.RENEWABLE_ENERGY,
        organization="", country="中国",
        description="国网山东电力统筹172座新型储能电站同步放电，最大"
                    "放电功率1198万千瓦，创全国省级电网集中调用纪录。"
                    "此次调用总装机1313万千瓦。储能产业链10余家企业"
                    "发布调价函，储能变流器和充电桩涨价受AI需求崛起"
                    "导致相关芯片供应紧张驱动。",
        key_metrics={"max_discharge": "1198万千瓦", "stations": 172,
                     "total_capacity": "1313万千瓦"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="大规模储能调度技术为机器人能源管理提供参考",
        deployment_ready=True,
        tags=["山东", "储能调用", "1198万千瓦", "创纪录", "芯片涨价"],
    ),

    # --- 农业AI ---
    AIProduct(
        product_id="AGR-006", name="新疆喀什棉田AI自主农业机器人",
        category=AICategory.AGRICULTURE,
        organization="", country="中国",
        description="配备宽幅喷杆和大容量药箱的AI自主农业机器人在"
                    "新疆喀什棉田进行演示，可完成播种、除草和喷药作业。"
                    "展示中国智慧农业在"
                    "新疆棉花主产区的实际应用。AI农业机器人在田间地头"
                    "从展台走向田野，全流程智能指导带动产量平均提升5%、"
                    "成本平均降低10%。",
        key_metrics={"yield_improvement": "5%", "cost_reduction": "10%"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="农业自主机器人是户外移动机器人重要应用场景",
        deployment_ready=True,
        tags=["新疆", "棉花", "农业机器人", "自主作业"],
    ),
    AIProduct(
        product_id="AGR-007", name="万蜂智能蛋鸡养殖自动化率提升至40%",
        category=AICategory.AGRICULTURE,
        organization="", country="中国",
        description="零一万物与正大集团共同成立合资公司'万蜂智能'，"
                    "以蛋鸡养殖为首个验证场。第一阶段预计将自动化率"
                    "从20%提升至40%，死淘率降低5%。麦麦科技集团开放"
                    "300多个作物品类、60多个机器人作业场景、100多个"
                    "机器人模型矩阵。海南种业大模型'丰登'能够'读基因、"
                    "编序列、算组合'，大幅缩短育种周期。",
        key_metrics={"automation_rate": "40%", "mortality_reduction": "5%",
                     "crop_types": "300+", "robot_scenarios": "60+"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="农业机器人作业场景矩阵为具身智能提供训练场",
        deployment_ready=True,
        tags=["万蜂智能", "蛋鸡养殖", "正大", "麦麦科技", "种业大模型"],
    ),

    # --- 商业AI ---
    AIProduct(
        product_id="CO-005", name="DeepSeek V4-Plus涨价约60%",
        category=AICategory.COMMERCE,
        organization="", country="中国",
        description="DeepSeek V4-Plus新价落地：输入3.5元/百万"
                    "tokens、输出12元/百万tokens，涨幅约60%，但首日"
                    "调用量仍涨18%。国产大模型从'打价格战'切换到"
                    "'价值变现+生态分成'阶段。阿里Qwen开始重度商用"
                    "收入分成，Kimi K3.1发布视频原生多模态。",
        key_metrics={"price_increase": "60%", "day1_call_growth": "18%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="大模型定价变化影响机器人AI推理成本",
        deployment_ready=True,
        tags=["DeepSeek", "涨价", "价值变现", "商用分成", "价格战结束"],
    ),

    # --- 水利AI ---
    AIProduct(
        product_id="WA-005", name="浙江人工智能+水利首场政企对接会",
        category=AICategory.WATER_CONSERVANCY,
        organization="", country="中国",
        description="浙江省智慧水利应用场景对接会在杭州青山水库举办，"
                    "为全省首次将真实水利工程场景向市场开放。企业提出："
                    "'无人船+多波束声呐'自动巡航获取水下三维地形；"
                    "综合物探无需钻孔生成大坝内部三维成像；水下机器人"
                    "搭载AI视觉完成坝体裂缝检测；融合机理模型与机器学习"
                    "将洪水预报调度从'小时级'压缩至'分钟级'。",
        key_metrics={"forecast_speedup": "小时级→分钟级"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="水下机器人AI视觉检测技术可迁移至机器人巡检",
        deployment_ready=True,
        tags=["浙江", "智慧水利", "无人船", "水下机器人", "洪水预报", "AI视觉"],
    ),

    # --- 汽车AI ---
    AIProduct(
        product_id="AU-009", name="小鹏G9L第二代VLA 6.3.0驾舱融合",
        category=AICategory.AUTOMOTIVE,
        organization="", country="中国",
        description="小鹏G9L开启预售，搭载第二代VLA智能驾驶系统、"
                    "图灵AI芯片，整车有效算力2250TOPS。第二代VLA"
                    "首次升级至6.3.0版本，端侧模型参数量提升3.5倍，"
                    "感知灵敏度提速300%。VLA+VLM驾舱融合下放Robotaxi"
                    "L4级体验，实现原地起步、靠边停车、园区漫游找车位，"
                    "支持模糊导航、语音靠边停车等交互。",
        key_metrics={"compute": "2250TOPS", "model_params_up": "3.5倍",
                     "perception_speedup": "300%"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="VLA视觉语言动作模型是机器人认知-执行统一架构",
        deployment_ready=True,
        tags=["小鹏", "VLA", "VLM", "驾舱融合", "图灵芯片", "2250TOPS"],
    ),
    AIProduct(
        product_id="AU-010", name="豆包大模型搭载超700万辆汽车",
        category=AICategory.AUTOMOTIVE,
        organization="", country="中国",
        description="火山引擎基于Agentic AI架构发布新一代汽车AI解决方案，"
                    "通过一个AI大脑深度联动整车，打通车控、导航、智驾"
                    "等功能域，实现'感知-推理-执行-记忆-学习'一体化闭环。"
                    "搭载豆包大模型的智能汽车已超700万辆，覆盖超50个"
                    "汽车品牌、145个车型，日均完成超3000万次座舱交互。"
                    "腾讯云混合算力集群利用率达98.4%。",
        key_metrics={"vehicles": "700万", "brands": "50+", "models": "145",
                     "daily_interactions": "3000万", "cluster_utilization": "98.4%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="车载Agentic AI架构可直接复用于机器人决策系统",
        deployment_ready=True,
        tags=["火山引擎", "豆包", "智能座舱", "Agentic AI", "700万辆"],
    ),

    # --- 数码产品AI ---
    AIProduct(
        product_id="DP-009", name="国产OLED pTSF发光材料量产打破日韩垄断",
        category=AICategory.DIGITAL_PRODUCT,
        organization="", country="中国",
        description="小米全新机型搭载国内自研pTSF发光材料屏幕，发光"
                    "效率提升20%、整机功耗下降10%。国内首次实现OLED"
                    "上游核心材料自研量产，加速显示产业链国产替代。"
                    "荣耀Robot Phone售价9999元起，截至发布当晚预定量"
                    "超40万台，四自由度钛合金云台+Agentic OS+YOYO Pro。",
        key_metrics={"efficiency_up": "20%", "power_down": "10%",
                     "robot_phone_price": "9999元", "preorders": "40万"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="显示材料与端侧AI技术服务于机器人交互界面",
        deployment_ready=True,
        tags=["OLED", "pTSF", "国产替代", "荣耀机器人手机", "Agentic OS"],
    ),

    # --- 医疗健康AI ---
    AIProduct(
        product_id="HC-008", name="全国首个医疗多智能体协同标准发布",
        category=AICategory.HEALTHCARE,
        organization="", country="中国",
        description="中国信通院联合复旦大学附属中山医院牵头编制的"
                    "《医疗健康行业智能体协同要求》标准在上海正式发布，"
                    "为国内首个医疗多智能体协同规范。系统规定了架构要求、"
                    "接口协议、安全测评要求等核心内容，为不同技术厂商的"
                    "智能体产品提供统一协同交互规范。宿迁市方案明确2027年"
                    "落地50个以上AI医疗应用场景。",
        key_metrics={"target_scenarios_2027": "50+"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="多智能体协同标准为医疗机器人集群协作提供规范",
        deployment_ready=True,
        tags=["医疗智能体", "协同标准", "信通院", "中山医院", "50场景"],
    ),
    AIProduct(
        product_id="HC-009", name="北京亦庄每年1亿元数据券支持医疗AI",
        category=AICategory.HEALTHCARE,
        organization="", country="中国",
        description="北京经开区印发措施推进词元价值转化，每年发放1亿元"
                    "数据券，采购主体最高支持100万元。对开展模型业务"
                    "企业最高支持2000万元；对多能力聚合服务运营主体"
                    "最高支持5000万元。发布超百项医疗、康养机器人"
                    "'揭榜挂帅'清单，康养领域48项、医疗领域58项。",
        key_metrics={"annual_data_vouchers": "1亿元", "max_model_support": "2000万",
                     "max_platform_support": "5000万", "scenarios": "106"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="医疗康养机器人是具身智能重要落地场景",
        deployment_ready=True,
        tags=["北京亦庄", "数据券", "医疗机器人", "康养机器人", "揭榜挂帅"],
    ),

    # --- 民生AI ---
    AIProduct(
        product_id="LV-006", name="C919国产大飞机执飞国际商业航线",
        category=AICategory.LIVELIHOOD,
        organization="", country="中国",
        description="起，国航北京至蒙古国乌兰巴托航线由国产"
                    "大飞机C919执飞，标志着国产大飞机正式开启国际定期"
                    "商业航线运营。这是自主干线客机首条对普通旅客开放、"
                    "纳入全球售票体系的常态化国际商业航线。浙江同步印发"
                    "脑机接口产学研联动措施，开通医用耗材挂网绿色通道。",
        key_metrics={"first_route": "北京-乌兰巴托"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="高端制造自主可控为机器人产业链国产化提供参考",
        deployment_ready=True,
        tags=["C919", "国际航线", "国产大飞机", "脑机接口", "浙江"],
    ),

    # --- 教育AI ---
    AIProduct(
        product_id="ED-006", name="飞象星球AI教育覆盖5000所学校70万学生",
        category=AICategory.EDUCATION,
        organization="", country="中国",
        description="飞象星球AI教育产品已覆盖全国27个省、264个区域、"
                    "超过5000所学校，人工智能通识课进入多所学校日常课表，"
                    "覆盖70多万学生。教师用自然语言描述教学目标，系统"
                    "直接生成可运行的课堂应用。杭州建兰中学构建校本AI Agent"
                    "评价体系，滨江区全面应用智能作业批阅系统。Datawhale"
                    "与杭州西湖区共建全国首个人工智能开源生态学院。",
        key_metrics={"provinces": 27, "regions": 264, "schools": "5000+",
                     "students": "70万+"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="AI教育培养未来机器人开发者和使用者",
        deployment_ready=True,
        tags=["飞象星球", "AI教育", "5000学校", "70万学生", "开源生态学院"],
    ),

    # --- AI通用 ---
    AIProduct(
        product_id="AI-008", name="OpenAI GPT-5.6 Luna免费开放 Gemini月活破10亿",
        category=AICategory.AI_GENERAL,
        organization="", country="全球",
        description="OpenAI将GPT-5.6 Luna设为ChatGPT免费档默认模型，"
                    "免费用户文字对话基本不限量，新增Think推理按钮。"
                    "谷歌Gemini App月活突破10亿，成谷歌史上增长最快"
                    "产品之一。AI智能体从对话辅助走向复杂任务自主交付，"
                    "'找AI问问题'正在变成免费基础设施。",
        key_metrics={"gemini_mau": "10亿"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="免费基础模型降低机器人AI接入门槛",
        deployment_ready=True,
        tags=["GPT-5.6", "Gemini", "免费", "10亿月活", "AI基础设施"],
    ),

    # ==================================================================
    # 搜索新增内容
    # ==================================================================

    # --- 人形机器人 ---
    AIProduct(
        product_id="HR-012", name="宇树科技科创板申购人形机器人第一股",
        category=AICategory.HUMANOID_ROBOT,
        organization="", country="中国",
        description="宇树科技正式开启科创板申购，发行价150.80元/股，"
                    "对应总市值约609.93亿元，成为A股人形机器人第一股。"
                    "2025年人形整机出货5215台登顶全球纯人形机器人销量榜首，"
                    "人形机器人占主营收入比例从2023年1.88%升至51.78%。"
                    "募资42亿元，一半投向具身智能大模型，年产能从2万台"
                    "提升至10万台。上半年营收10.52-11.28亿元实现盈利。",
        key_metrics={"market_cap": "609.93亿元", "iprice": "150.80元",
                     "shipments_2025": 5215, "revenue_h1": "10.52亿",
                     "capacity_target": "10万台/年", "funding": "42亿"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="人形机器人量产标杆，WMA+VLA双线布局具身大模型",
        deployment_ready=True,
        tags=["宇树科技", "科创板", "人形机器人第一股", "量产", "具身大模型"],
    ),
    AIProduct(
        product_id="HR-013", name="消费级人形机器人量产元年价格下探万元",
        category=AICategory.HUMANOID_ROBOT,
        organization="", country="中国",
        description="2026年是人形机器人量产与场景落地关键年份，国内全年"
                    "整机产量有望突破10万台。消费级人形机器人价格快速下探，"
                    "轻量化机型已降至万元以内。仅6月就有十余家企业发布新品，"
                    "覆盖咖啡馆点单、外卖配送、远程问诊等生活场景。"
                    "人和机器人交互产生海量数据反哺具身智能大模型迭代，"
                    "形成技术与场景双向互促循环。",
        key_metrics={"annual_output": "10万台+", "price_range": "万元以内",
                     "june_launches": "10+"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="消费级市场打开人形机器人规模化落地通道",
        deployment_ready=True,
        tags=["消费级人形机器人", "万元级", "量产元年", "场景落地", "数据飞轮"],
    ),

    # --- AI智能体 ---
    AIProduct(
        product_id="AG-016", name="百度伐谋AI4S科研智能体",
        category=AICategory.AI_AGENT,
        organization="", country="中国",
        description="百度AI Day发布伐谋智能体，定位为能够自我演化、"
                    "擅长解决创新和优化类问题的AI智能体。将目标、规则、"
                    "资源限制和评价标准组织起来，让AI持续生成、筛选、"
                    "验证和改进方案。重点探索四类科研工作：发现规律、"
                    "加速计算、搜索方案、动态决策。在产业场景中帮助企业"
                    "改善经营策略、优化工艺参数。",
        key_metrics={"research_types": 4, },
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="智能体优化搜索框架可用于机器人策略搜索和参数调优",
        deployment_ready=False,
        tags=["百度伐谋", "AI4S", "科研智能体", "自我演化", "方案优化"],
    ),
    AIProduct(
        product_id="AG-017", name="北京加快智能体创新发展十条措施",
        category=AICategory.AI_AGENT,
        organization="", country="中国",
        description="北京市印发《关于加快智能体引领发展的若干措施》，"
                    "围绕技术、应用、产业、生态4个方面出台10条举措。"
                    "北京亦庄同步发布'词元十条'，建设自主可控万卡级"
                    "词元工厂，每年发放算力券、数据券各1亿元，"
                    "对算力租赁费用给予最高30%补贴、2000万元资金支持。"
                    "国家网信办等三部门联合印发智能体规范应用实施意见。",
        key_metrics={"measures": 10, "vouchers": "各1亿/年",
                     "subsidy": "30%", "max_support": "2000万"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="政策支持智能体+算力基础设施，利好机器人AI研发",
        deployment_ready=True,
        tags=["北京", "智能体十条", "词元工厂", "算力券", "政策"],
    ),
    AIProduct(
        product_id="AG-018", name="字节Seedance 2.5视频模型API上线",
        category=AICategory.AI_AGENT,
        organization="", country="中国",
        description="字节火山引擎上线Seedance 2.5 API，原生支持30秒视频"
                    "直出，单次最多参考50个全模态素材。在指令遵循、"
                    "长叙事、真人感、声画质感等维度全面升级，能准确执行"
                    "包含秒级时间轴指令的多场景复杂任务，多角色一致性"
                    "显著增强，兼容十余种语言。",
        key_metrics={"max_duration": "30秒", "max_refs": 50,
                     "languages": "10+"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="视频生成模型可用于机器人训练数据增强和场景模拟",
        deployment_ready=True,
        tags=["字节", "Seedance", "视频生成", "API", "多模态"],
    ),

    # --- AI算力 ---
    AIProduct(
        product_id="CP-009", name="上海十五五规划CPO与GPU/HBM并列攻关",
        category=AICategory.AI_COMPUTE,
        organization="", country="中国",
        description="上海经信委印发软件和信息服务业'十五五'规划，"
                    "高速光互连(CPO)被明确列为与GPU、HBM并列的核心"
                    "攻关环节。提出攻关超大规模智能算力集群组网技术，"
                    "围绕GPU、CPO、HBM及异构服务器提升智算硬件供给能力。"
                    "推动建设集算力调度、模型孵化、应用适配于一体的"
                    "综合性智算公共平台。",
        key_metrics={"core_techs": "GPU/CPO/HBM", "plan": "十五五"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="算力集群组网技术支撑机器人云端训练和边云协同",
        deployment_ready=False,
        tags=["CPO", "GPU", "HBM", "上海十五五", "智算平台"],
    ),
    AIProduct(
        product_id="CP-010", name="全国智能算力规模达去年同期2.8倍",
        category=AICategory.AI_COMPUTE,
        organization="", country="中国",
        description="截至2026年6月底全国智能算力规模达到去年同期的2.8倍，"
                    "国产大模型全球总下载量突破100亿次。曙光8000登峰"
                    "全国产十万卡AI超集群在郑州投用，每秒峰值算力相当于"
                    "全人类持续计算200年。Anthropic与Riot Platforms达成"
                    "91亿美元20年期算力协议。四大CSP 2026年资本开支"
                    "合计上调至7350-7600亿美元。",
        key_metrics={"compute_growth": "2.8倍", "downloads": "100亿次",
                     "anthropic_deal": "91亿美元/20年"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="算力规模爆发为机器人大模型训练提供充足基础设施",
        deployment_ready=True,
        tags=["智能算力", "2.8倍", "曙光8000", "100亿次下载", "算力协议"],
    ),

    # --- AI芯片 ---
    AIProduct(
        product_id="CH-007", name="T1200级碳纤维百吨级量产打破垄断",
        category=AICategory.AI_CHIP,
        organization="", country="中国",
        description="2026年3月中国T1200级超高强度碳纤维实现全球首次"
                    "百吨级量产，强度是钢铁10倍、重量仅1/5，打破日美"
                    "长达40年技术封锁。产品广泛应用于航空航天、人形机器人、"
                    "低空经济、新能源等领域。标志中国高端材料从进口依赖"
                    "转向全球引领。",
        key_metrics={"grade": "T1200", "strength_ratio": "10x钢",
                     "weight_ratio": "1/5钢", "capacity": "百吨级"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="T1200碳纤维可大幅减轻人形机器人本体重量提升负载比",
        deployment_ready=True,
        tags=["T1200碳纤维", "百吨量产", "机器人材料", "轻量化", "打破垄断"],
    ),

    # --- AI大模型 ---
    AIProduct(
        product_id="LLM-011", name="Anthropic为Claude添加隐形水印",
        category=AICategory.AI_LLM,
        organization="", country="美国",
        description="Anthropic开始在Claude生成文本中加入隐形水印，"
                    "通过嵌入可被计算机识别的代码标记内容的AI生成属性。"
                    "此举旨在满足欧盟《人工智能法案》透明度准则要求："
                    "科技公司需以机器可识别方式标注AI生成或编辑内容。"
                    "欧盟8月2日起扩大AI法案适用范围，聊天机器人必须告知"
                    "用户正在与AI互动，深度伪造内容必须强制标识。",
        key_metrics={"watermark": "隐形", "regulation": "欧盟AI法案",
                     "effective": "2026-08-02"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="AI生成内容标识机制可用于机器人输出可信度追溯",
        deployment_ready=True,
        tags=["Claude", "隐形水印", "欧盟AI法案", "透明度", "内容标识"],
    ),

    # --- 世界模型 ---
    AIProduct(
        product_id="WM-007", name="7个月新成立23家世界模型公司",
        category=AICategory.WORLD_MODEL,
        organization="", country="中国",
        description="2026年前7个月中国新成立23家世界模型创业公司，"
                    "超过2025年全年20家。18家在成立数月内完成首轮融资，"
                    "2家种子轮即达独角兽估值。技术路线分为通用世界模型基座、"
                    "4D时空重建、因果推理引擎、科学发现中枢、物流动作模型等。"
                    "前阿里通义千问负责人林俊旸创立语用科技，种子轮估值"
                    "约20亿美元。破壳机器人完成亿美元级Pre-A轮。",
        key_metrics={"new_companies": 23, "funded": 18,
                     "unicorns_seed": 2, "valuation_pragmatic": "20亿美元"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="世界模型是机器人理解物理环境和预测动作后果的核心技术",
        deployment_ready=False,
        tags=["世界模型", "创业潮", "语用科技", "4D重建", "因果推理"],
    ),

    # --- AI通用 ---
    AIProduct(
        product_id="AI-010", name="中国全方位推动AI全球治理走深走实",
        category=AICategory.AI_GENERAL,
        organization="", country="中国",
        description="中国全方位推动人工智能全球治理。"
                    "29国签署协议成立世界人工智能合作组织(WAICO)总部落户上海。"
                    "中国规模以上制造业企业AI普及率超30%，智能经济核心产业"
                    "规模超万亿元，生成式AI用户突破6亿，成为AI专利最大拥有国。"
                    "全球前十大生成式AI专利申请人中6家总部在中国。"
                    "中国开源模型全球下载占比41%居世界第一。",
        key_metrics={"manufacturing_adoption": "30%", "ai_economy": "万亿",
                     "users": "6亿", "patent_rank": "第一",
                     "open_source_share": "41%", "waico_countries": 29},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="AI治理框架和开源生态为机器人产业发展提供制度保障",
        deployment_ready=True,
        tags=["AI治理", "WAICO", "专利第一", "开源41%", "6亿用户"],
    ),
    AIProduct(
        product_id="AI-011", name="AI消费爆发智能外骨骼零售额暴涨458%",
        category=AICategory.AI_GENERAL,
        organization="", country="中国",
        description="商务部监测数据显示上半年智能外骨骼网络零售额暴涨"
                    "458.4%，智能眼镜零售额增长151.7%，AI益智玩具涨幅"
                    "283%。上海AI应用商店500余款产品中80%价格集中在"
                    "1000-1500元。华强北AI产品在电子品类占比从41%升至61%，"
                    "日均8000名外籍客商扫货。2026年全球AI眼镜出货量有望"
                    "突破1600万台。AI从强国科技转向民生科技。",
        key_metrics={"exoskeleton_growth": "458.4%",
                     "glasses_growth": "151.7%", "toy_growth": "283%",
                     "hqb_ai_ratio": "61%", "ai_glasses_2026": "1600万台"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="外骨骼和AI眼镜等消费级机器人相关产品爆发式增长",
        deployment_ready=True,
        tags=["AI消费", "外骨骼", "智能眼镜", "华强北", "民生科技"],
    ),
    AIProduct(
        product_id="AI-012", name="2026中国AI盛典十位年度人物揭晓",
        category=AICategory.AI_GENERAL,
        organization="", country="中国",
        description="中央广播电视总台《2026中国AI盛典》揭晓10位年度AI"
                    "人物：王兴兴、王鹤、朱秋国、闫俊杰、李宏伟、汪玉、"
                    "沈亦晨、张林峰、曾国洋、魏少军，其中4位90后最年轻28岁。"
                    "渐冻症抗争者蔡磊获年度AI特别贡献人物，其团队推动的"
                    "新药RAG-17让29岁渐冻症女孩重新站立。盛典以'AI在一起'"
                    "为主题，展现AI向上向善力量。",
        key_metrics={"persons": 10, "post90s": 4, "youngest": 28,
                     "special_award": "蔡磊"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="多位年度人物来自具身智能和机器人领域，推动产业发展",
        deployment_ready=True,
        tags=["AI盛典", "年度人物", "蔡磊", "渐冻症", "王兴兴", "向上向善"],
    ),

    # --- 6G网络 ---
    AIProduct(
        product_id="NET-003", name="6G R20标准AI/ML空口设计进入最终表决",
        category=AICategory.NETWORK_6G,
        organization="", country="全球",
        description="3GPP R20（6G第一个标准版本）进入高密度工作项目攻坚期。"
                    "2026年3月RAN全会上AI/ML空口设计物理层细节进入最终"
                    "表决阶段，重点解决信道估计AI模型在不同厂商设备间的"
                    "互操作性。网络计算能力和AI推理准确率首次纳入强制性"
                    "指标体系。7-24GHz厘米波段被确定为6G连续覆盖核心频段，"
                    "亚太赫兹短距接入实现400Gbps峰值速率。中国6G专利占比"
                    "40.3%全球第一。",
        key_metrics={"standard": "3GPP R20", "patent_share_cn": "40.3%",
                     "sub_thz_speed": "400Gbps", "core_band": "7-24GHz"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="6G AI原生网络为机器人提供超低时延确定性通信",
        deployment_ready=False,
        tags=["6G", "R20", "AI/ML空口", "厘米波", "专利第一"],
    ),

    # --- 工业机器人 ---
    AIProduct(
        product_id="IR-008", name="华中最大规模工业巡检机器人光谷集中交付",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="", country="中国",
        description="8月6日近百台工业巡检机器人在湖北人形机器人创新中心"
                    "集中交付，将在武汉、上海、无锡等地从事治安巡检。"
                    "首批30台巡1系列四足机器人定位精度达毫米级，"
                    "接到云端任务后可自主导航执行巡逻。这是华中地区"
                    "机器人产业最大规模集中交付，标志工业巡检机器人"
                    "从单台示范走向规模化部署。",
        key_metrics={"delivered": 100, "first_batch": 30,
                     "precision": "毫米级", "region": "华中"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="四足巡检机器人规模化交付验证户外自主导航能力",
        deployment_ready=True,
        tags=["巡检机器人", "四足机器人", "光谷", "规模化交付", "自主导航"],
    ),

    # --- 蚌埠本地 ---
    AIProduct(
        product_id="BB-010", name="蚌埠十五五锚定GDP3400亿智能传感剑指500亿",
        category=AICategory.BENGBU_LOCAL,
        organization="", country="中国",
        description="蚌埠'十五五'目标：2030年GDP突破3400亿元，工业总产值"
                    "突破2300亿元。智能传感产业2025年产值突破100亿元增长29%，"
                    "力争2030年突破500亿元。中国传感谷跻身全国十大高质量"
                    "传感器园区第6位。全市唯一同时具备集成电路与8吋晶圆"
                    "量产能力。将打造车规级传感器、脑机接口柔性传感器、"
                    "机器人感知组件等'蚌埠芯'标志性产品。",
        key_metrics={"gdp_target": "3400亿", "industrial_target": "2300亿",
                     "sensor_2025": "100亿", "sensor_target": "500亿",
                     "rank": "全国第6"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="蚌埠机器人感知组件和传感器直接服务机器人产业",
        deployment_ready=True,
        tags=["蚌埠", "十五五", "智能传感500亿", "中国传感谷", "机器人感知"],
    ),
    AIProduct(
        product_id="BB-011", name="蚌埠加快商业航天与智能传感融合发展",
        category=AICategory.BENGBU_LOCAL,
        organization="", country="中国",
        description="蚌埠市委书记马军调研商业航天产业，察看航星传动"
                    "火箭伺服装置基地和天途无人机研发生产基地。强调推动"
                    "商业航天产业与智能传感、新型显示等产业融合发展，"
                    "大力引进无人机核心零部件企业。蚌埠滕湖机场已正式通航，"
                    "正布局脑机接口、第六代移动通信、先进材料等前沿领域。",
        key_metrics={"frontier_fields": "脑机接口/6G/先进材料"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="商业航天无人机和6G布局为机器人提供通信和空中协同能力",
        deployment_ready=False,
        tags=["蚌埠", "商业航天", "无人机", "产业融合", "滕湖机场"],
    ),

    # --- 新能源 ---
    AIProduct(
        product_id="EN-013", name="水电智能调度运行智能体贵州落地增发8%",
        category=AICategory.RENEWABLE_ENERGY,
        organization="", country="中国",
        description="国务院国资委发布人工智能'焕新社区'2.0，水电智能调度"
                    "运行智能体已在贵州'两江一河'流域9座梯级水电站和"
                    "4个光伏项目落地应用。智能体打造水电领域'调度运行大脑'，"
                    "将传统人工调度升级为智能化运行，2025年优化调度增发率"
                    "达到8%，增发电量9.8亿千瓦时。央企已开放1200个应用场景，"
                    "打造超70个行业垂类模型。",
        key_metrics={"hydropower_stations": 9, "pv_projects": 4,
                     "generation_increase": "8%", "extra_power": "9.8亿kWh",
                     "central_scenarios": 1200},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="智能调度优化算法与机器人多关节协同调度同源",
        deployment_ready=True,
        tags=["水电智能体", "梯级调度", "增发8%", "焕新社区", "央企AI"],
    ),
    AIProduct(
        product_id="EN-014", name="妈祖气象AI预警方案30国落地",
        category=AICategory.RENEWABLE_ENERGY,
        organization="", country="中国",
        description="在2026世界人工智能大会上中国宣布推动气象智能预警方案"
                    "'妈祖'在30个国家落地应用，这是全球首个响应联合国"
                    "全民早期预警倡议的国家级行动方案。深度融合风云气象卫星、"
                    "AI预报模型，搭建'监测-预报-预警-服务'全链条。"
                    "已在7个国家落地，40余国云端应用。四川荣县'AI闪电'"
                    "靶向发布技术25分钟电话通知574名防灾责任人。",
        key_metrics={"target_countries": 30, "landed": 7, "cloud_users": "40+",
                     "notification_speed": "25分钟/574人"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="气象预警AI可赋能户外作业机器人环境感知和决策",
        deployment_ready=True,
        tags=["妈祖", "气象AI", "30国", "风云卫星", "早期预警"],
    ),

    # --- 农业AI ---
    AIProduct(
        product_id="AGR-008", name="中国AI卫星为乌兹别克斯坦印尼提供农业遥感",
        category=AICategory.AGRICULTURE,
        organization="", country="中国",
        description="8月5日捷龙三号运载火箭从山东海阳近海上空发射，"
                    "成功将东方慧眼高光谱卫星01/02星送入轨道。一颗卫星"
                    "为乌兹别克斯坦提供棉花产业全周期监测，另一颗为印尼"
                    "提供作物生长追踪和灾害风险评估。卫星可直接在太空"
                    "执行AI计算任务，灾害预警从传统卫星的数小时缩短至"
                    "数分钟内提供决策指导。",
        key_metrics={"satellites": 2, "partners": "乌兹别克斯坦/印尼",
                     "warning_speed": "分钟级"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="星上AI计算和遥感技术为农业机器人提供全局感知",
        deployment_ready=True,
        tags=["AI卫星", "高光谱", "农业遥感", "太空计算", "一带一路"],
    ),

    # --- 商业AI ---
    AIProduct(
        product_id="CO-006", name="亚马逊Twitch默认用主播内容训练AI引争议",
        category=AICategory.COMMERCE,
        organization="", country="美国",
        description="亚马逊旗下Twitch直播平台宣布将默认使用创作者内容"
                    "训练生成式AI模型，除非创作者手动选择退出。此举在"
                    "直播创作者群体中引发强烈不满。同期Spotify宣布将为"
                    "AI生成歌手推出'AI Persona'标签，9月中旬上线，"
                    "并将其移出算法与编辑推荐。AI训练数据版权和"
                    "AI生成内容标识成为行业焦点。",
        key_metrics={"platform": "Twitch", "opt_out": True,
                     "spotify_label": "AI Persona", "effective": "9月中旬"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="AI训练数据版权框架影响机器人学习数据的合规使用",
        deployment_ready=True,
        tags=["Twitch", "AI训练", "版权", "Spotify", "AI标签"],
    ),

    # --- 截图识别新增 ---
    AIProduct(
        product_id="CO-007", name="科技成果超市科企对接平台",
        category=AICategory.COMMERCE,
        organization="", country="中国",
        description="多地开设硬核科技'成果超市'助力科企对接。"
                    "科研成果以卡片形式按颜色分区'上架'：蓝色为医疗设备与"
                    "科学仪器、绿色为人工智能与机器人、橙色为先进电子与能源"
                    "材料、紫色为合成生物。企业扫描条形码即可查看技术优势并"
                    "带走卡片。平台背后依托10个研究所、4个国家重点实验室、"
                    "2个国家创新中心，累计发表论文超2万篇，申请专利1.85万件，"
                    "2025年平均转化率超过29%。'成果超市'已促成企业委托项目"
                    "签约合同金额近2.5亿元，促成项目成功率提升10%至20%。"
                    "模式已在珠海、江门、宁德、温州、武汉、济南、鄂尔多斯等"
                    "超10个城市落地，江门专区上线216项科研成果，打通'深圳研发+"
                    "江门转化'跨城通道。湖南郴州新能源企业通过平台3天办成共享"
                    "设备，量产后预计提升全营业额25%。",
        key_metrics={"papers": 20000, "patents": 18500,
                     "conversion_rate_pct": 29,
                     "contract_amount_yi": 2.5,
                     "success_rate_uplift_pct": "10-20",
                     "cities": 10, "jiangmen_results": 216,
                     "revenue_uplift_pct": 25},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="绿色专区涵盖人工智能与机器人技术成果转化，"
                              "加速机器人科研成果从实验室走向产业应用",
        deployment_ready=False,
        tags=["成果超市", "科技转化", "科企对接", "AI与机器人",
              "深圳先进院", "10城落地"],
    ),

    # --- 水利AI ---
    AIProduct(
        product_id="WA-006", name="防汛科技立体感知体系投入实战",
        category=AICategory.WATER_CONSERVANCY,
        organization="", country="中国",
        description="2026年防汛中科技新力量全面投入实战。浙江无人机"
                    "5分钟内识别行洪障碍自动派单；福建双光侦察无人机"
                    "全域巡湖精准锁定被困人员；湖南四水流域洪水预报调度"
                    "系统将流程从数小时压缩至10分钟；天津智能应急巡堤"
                    "无人机红外热成像识别渗漏点，单架次巡查10-15公里；"
                    "3.5kg应急通信携行包30秒建立卫星链路覆盖50米范围。",
        key_metrics={"obstacle_id_time": "5分钟", "dispatch_time": "10分钟",
                     "drone_range": "10-15km", "comm_weight": "3.5kg",
                     "comm_setup": "30秒", "comm_range": "50米"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="无人机/无人船立体侦察体系为机器人户外作业提供参考",
        deployment_ready=True,
        tags=["智慧防汛", "无人机巡堤", "红外热成像", "应急通信", "数字孪生"],
    ),

    # --- 汽车AI ---
    AIProduct(
        product_id="AU-011", name="华为乾崑智驾累计辅助驾驶122亿公里",
        category=AICategory.AUTOMOTIVE,
        organization="", country="中国",
        description="华为乾崑智驾累计辅助驾驶里程超122亿公里，搭载车辆"
                    "累计行驶总里程超350亿公里。技术范式全面转向数据驱动的"
                    "端到端大模型架构，'重感知、轻地图'成为行业共识。"
                    "VLA（视觉-语言-动作）大模型正成为打通认知与执行壁垒"
                    "的前沿方向，让系统能看懂交警手势、临时路牌等语义信息。"
                    "L2级渗透率达70.5%，NOA功能渗透率34.2%。",
        key_metrics={"assisted_km": "122亿", "total_km": "350亿",
                     "l2_penetration": "70.5%", "noa_penetration": "34.2%"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="VLA大模型和端到端架构直接复用至机器人控制",
        deployment_ready=True,
        tags=["华为乾崑", "VLA", "端到端", "122亿公里", "重感知轻地图"],
    ),

    # --- 数码产品AI ---
    AIProduct(
        product_id="DP-011", name="荣耀Robot Phone预约破40万台终身AI免费",
        category=AICategory.DIGITAL_PRODUCT,
        organization="", country="中国",
        description="荣耀发布全球首款机器人手机Robot Phone，"
                    "开售前夕全网预约总量突破40万台。内置4DoF钛合金"
                    "灵巧云台，加工精度±0.005mm，核心电机仅2.6g。"
                    "MagicOS升级为Agentic OS伙伴型智能体系统，"
                    "承诺全功能AI智能体终身免费、无订阅费、无算力额度限制。"
                    "支持跨场景自主任务执行、情绪化肢体互动、环境自主感知。"
                    "AI从算法+屏幕进入算法+机械执行阶段。",
        key_metrics={"preorders": "40万", "dof": 4, "precision": "±0.005mm",
                     "motor_weight": "2.6g", "ai_policy": "终身免费"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="智能体驱动机械云台是AI操控物理世界的消费级验证",
        deployment_ready=True,
        tags=["荣耀", "机器人手机", "4DoF云台", "Agentic OS", "终身免费"],
    ),
    AIProduct(
        product_id="DP-010", name="影石GO Ultra上线AI语音助手接入千问",
        category=AICategory.DIGITAL_PRODUCT,
        organization="", country="中国",
        description="影石Insta360为GO Ultra拇指相机上线AI语音助手。"
                    "中国大陆接入阿里千问大模型，海外接入Google Gemini。"
                    "端侧完成声纹识别和意图判断，云端负责复杂推理，"
                    "翻译结果通过机身扬声器直接播报。这是AI大模型向"
                    "小型化消费电子终端渗透的标志性产品。",
        key_metrics={"device": "GO Ultra", "cn_model": "千问",
                     "global_model": "Gemini", "edge_tasks": "声纹/意图"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="端云协同推理架构可复用至机器人语音交互系统",
        deployment_ready=True,
        tags=["影石", "AI语音助手", "千问", "Gemini", "端云协同"],
    ),

    # --- 医疗健康AI ---
    AIProduct(
        product_id="HC-010", name="谷歌AMIE首次展示实时临床视频问诊",
        category=AICategory.HEALTHCARE,
        organization="", country="美国",
        description="谷歌基于Gemini与Project Astra构建的AMIE系统首次在"
                    "真实问诊场景展示专家级AI能力。可解读视觉与听觉线索、"
                    "引导虚拟体格检查并实时诊断推理，能理解医生和患者的"
                    "'非语言信号'。这是多模态理解从实验室走向高价值"
                    "专业场景的关键一步，也是AI医疗可信落地的重要信号。",
        key_metrics={"model": "Gemini+Astra", "capability": "实时视频问诊",
                     "signals": "视觉+听觉+非语言"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="多模态实时理解能力直接服务于医疗陪护机器人",
        deployment_ready=False,
        tags=["AMIE", "Gemini", "临床问诊", "多模态", "非语言信号"],
    ),
    AIProduct(
        product_id="HC-011", name="国家AI应用上海中试基地五大成果九款应用",
        category=AICategory.HEALTHCARE,
        organization="", country="中国",
        description="国家人工智能应用上海中试基地发布五大核心创新成果："
                    "国模用国芯算力底座、6大医疗垂直基础模型、全国示范性"
                    "医疗AI数据基础设施、中文医疗大模型测试平台MedBench 4.0、"
                    "多学科世界级医疗智能应用。同步发布9款医疗智能应用，"
                    "覆盖临床诊疗、器械研发、AI制药、脑机接口。肝胆肿瘤"
                    "智能体已推广至122家医疗机构服务超百万人次。",
        key_metrics={"vertical_models": 6, "apps": 9,
                     "liver_centers": 122, "liver_patients": "百万+",
                     "imaging_cases": "250万"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="医疗AI垂直模型和智能体可直接部署于医疗服务机器人",
        deployment_ready=True,
        tags=["上海中试基地", "MedBench", "医疗大模型", "肝胆智能体", "脑机接口"],
    ),

    # --- 民生AI ---
    AIProduct(
        product_id="LV-007", name="AI消费级产品走进千家万户民生科技转身",
        category=AICategory.LIVELIHOOD,
        organization="", country="中国",
        description="AI正从高端科技概念下沉至日常生活。北京上半年可穿戴"
                    "智能设备零售额大涨超六成，服务机器人产量暴涨2.3倍。"
                    "线下智能门店AI机型成交占比突破62%。外骨骼缓解护工"
                    "体力劳损、AI眼镜解决跨境沟通壁垒、AI玩具填补儿童"
                    "陪伴缺口、AI头盔保障骑手出行安全。上海预测2027年"
                    "本地智能终端产业规模将突破3000亿元。",
        key_metrics={"wearable_growth": "60%+", "robot_growth": "2.3倍",
                     "ai_phone_share": "62%",
                     "shanghai_2027": "3000亿"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="服务机器人和外骨骼等民生产品是机器人技术的直接落地",
        deployment_ready=True,
        tags=["民生科技", "服务机器人", "外骨骼", "AI眼镜", "消费下沉"],
    ),

    # --- 教育AI ---
    AIProduct(
        product_id="ED-007", name="国家数据局系统部署高质量数据集建设",
        category=AICategory.EDUCATION,
        organization="", country="中国",
        description="国家数据局发布《关于推进行业高质量数据集建设行动的"
                    "实施方案》，国家层面首次系统部署数据赋能AI发展。"
                    "围绕数据集供给、流通、应用部署六大专项行动，"
                    "聚焦智能体、具身智能和世界模型等重点方向加快数据集"
                    "建设。引导有条件地区开展数据标注创新试验区建设。"
                    "数据是AI训练核心原料，高质量数据集可加快提升大模型性能。",
        key_metrics={"actions": 6, "focus": "智能体/具身智能/世界模型"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="具身智能和世界模型数据集建设直接支撑机器人AI训练",
        deployment_ready=True,
        tags=["高质量数据集", "具身智能", "世界模型", "数据标注", "国家数据局"],
    ),

    # --- 搜索新增内容 ---
    AIProduct(
        product_id="WM-008", name="WALL-B世界统一模型",
        category=AICategory.WORLD_MODEL,
        organization="", country="中国",
        description="端到端具身大模型，将视觉、语言、触觉、动作和物理预测"
                    "融合在同一神经网络中。采用双机械臂加夹爪方案，全程无人工"
                    "干预完成全自主物流分拣，实现1816件/小时分拣效率，准确率超"
                    "98%，超过海外同类企业1248件/小时约45%，系统成本仅为国外"
                    "约30%。机器人可自主判断物体属性、选择抓取策略、整理面单，"
                    "无需为每种包裹编写规则，以模型能力取代硬件堆叠。",
        key_metrics={"sorting_rate_per_hour": 1816, "accuracy_pct": 98,
                     "efficiency_uplift_pct": 45, "cost_reduction_pct": 70},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="世界统一模型直接驱动机器人完成物理操作任务，"
                              "验证'模型能力取代硬件堆叠'技术路线",
        deployment_ready=False,
        tags=["世界模型", "具身大模型", "物流分拣", "双机械臂", "端到端"],
    ),
    AIProduct(
        product_id="HR-014", name="Gemini Robotics 2全身控制模型",
        category=AICategory.HUMANOID_ROBOT,
        organization="", country="美国",
        description="首次实现22自由度全身统一控制，将摄像头画面和自然语言"
                    "指令直接转化为电机控制信号，驱动机器人完成行走、下蹲、"
                    "避障和物体操作。少量样本即可跨机器人本体迁移，同一大脑可"
                    "驱动不同品牌身体。配套ER 2推理系统支持数百步长任务规划"
                    "和多机器人协同，拧灯泡任务成功率92%；On-Device 2端侧"
                    "版本无需云端算力即可本地运行。",
        key_metrics={"dof": 22, "bulb_success_rate_pct": 92,
                     "migration": "few-shot cross-body"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="22自由度全身控制是具身智能软件层里程碑，"
                              "跨本体迁移大幅降低训练数据门槛",
        deployment_ready=False,
        tags=["全身控制", "跨本体迁移", "端侧部署", "多机器人协同", "22自由度"],
    ),
    AIProduct(
        product_id="HR-015", name="Walker S2自主换电池人形机器人",
        category=AICategory.HUMANOID_ROBOT,
        organization="", country="中国",
        description="全球首款实现自主更换电池的人形机器人。双电池系统支持"
                    "行走约2小时或站立约4小时，电量低时自动行至充电站，用"
                    "双臂取出背部电池包插入充电座，再装入新电池，全程仅需"
                    "数分钟。消除人工充电干预，实现24/7不间断运行。",
        key_metrics={"battery_swap_minutes": 3, "walk_hours": 2,
                     "stand_hours": 4, "autonomy": "24/7"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="自主换电池解决人形机器人续航瓶颈，"
                              "是工厂和公共场所持续作业的关键能力",
        deployment_ready=False,
        tags=["自主换电", "24/7运行", "双电池", "人形机器人"],
    ),
    AIProduct(
        product_id="HR-016", name="Asimov 1开源人形机器人",
        category=AICategory.HUMANOID_ROBOT,
        organization="", country="美国",
        description="售价2万美元的开源人形机器人，需自行组装，定位为机器人"
                    "开发者平台。采用宜家式组装理念，提供完整硬件设计文件和"
                    "软件框架，旨在降低人形机器人开发门槛，推动社区协作创新。",
        key_metrics={"price_usd": 20000, "open_source": True,
                     "assembly_required": True},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="开源低价人形机器人平台降低研发门槛，"
                              "加速机器人应用生态建设",
        deployment_ready=False,
        tags=["开源", "开发者平台", "自组装", "低价人形"],
    ),
    AIProduct(
        product_id="HR-017", name="Orbit多轴关节驱动器",
        category=AICategory.HUMANOID_ROBOT,
        organization="", country="美国",
        description="新型多轴关节驱动器，旨在取代人形机器人肩膀和臀部使用"
                    "的低效堆叠电机方案。单一驱动器即可实现多自由度运动，"
                    "简化机械结构、降低重量和故障点，提升关节集成度。",
        key_metrics={"type": "multi-axis joint actuator",
                     "replaces": "stacked motors"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="关节驱动器是人形机器人核心硬件，"
                              "多轴集成方案可显著提升运动效率和可靠性",
        deployment_ready=False,
        tags=["关节驱动器", "多轴", "人形机器人硬件", "肩关节"],
    ),
    AIProduct(
        product_id="IR-009", name="星动L7物流分拣机器人",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="", country="中国",
        description="面向快递分拣场景的工业机器人，可自主抓取包裹并通过双手"
                    "手腕翻转将快递单面调整至朝上，再稳放到传送带。在堆成"
                    "小山的包裹台上实现连续自主分拣，从赛场冠军技术转化为"
                    "工厂实际生产力。",
        key_metrics={"application": "快递分拣", "capability": "面单翻转"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="物流分拣是工业机器人规模化落地的核心场景，"
                              "面单调整能力体现精细操作水平",
        deployment_ready=False,
        tags=["物流分拣", "面单翻转", "工业机器人", "双臂协作"],
    ),
    AIProduct(
        product_id="AG-021", name="WorkBuddy桌面智能体",
        category=AICategory.AI_AGENT,
        organization="", country="中国",
        description="桌面端AI智能体，支持本地文件读写、Shell命令执行、"
                    "浏览器自动化、文档表格批量处理。预制大量职场技能，"
                    "深度对接企业协作生态，支持日志分析和运维脚本调试。"
                    "采用沙盒安全隔离和高危操作拦截机制。",
        key_metrics={"capabilities": ["文件操作", "命令执行", "浏览器自动化",
                                       "文档处理"], "security": "沙盒隔离"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="智能体自动化能力可迁移至机器人任务规划和"
                              "工具调用场景",
        deployment_ready=True,
        tags=["桌面智能体", "运维", "浏览器自动化", "沙盒安全"],
    ),
    AIProduct(
        product_id="AG-022", name="Muse Code编程智能体",
        category=AICategory.AI_AGENT,
        organization="", country="美国",
        description="首款编程智能体，支持多智能体协作完成软件开发任务。"
                    "可自主进行代码生成、调试、重构和测试，与开发工具链"
                    "深度集成，标志着AI编程进入多智能体协作时代。",
        key_metrics={"type": "coding_agent", "multi_agent": True},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="多智能体协作编程范式可用于机器人控制系统的"
                              "模块化开发和自主调试",
        deployment_ready=False,
        tags=["编程智能体", "多智能体协作", "代码生成", "自动调试"],
    ),
    AIProduct(
        product_id="LM-012", name="Muse Spark 1.2开源模型",
        category=AICategory.AI_LLM,
        organization="", country="美国",
        description="全新开源AI模型，同时上线可在笔记本设备运行的轻量化"
                    "系列。开放模型旨在避免AI技术被少数巨头垄断，方便中小"
                    "企业和开发者获取优质AI工具。内部已组建超级智能实验室，"
                    "后续将持续推出开源模型。",
        key_metrics={"open_source": True, "laptop_runnable": True},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="端侧可运行开源模型为机器人本地推理提供"
                              "轻量化选择",
        deployment_ready=True,
        tags=["开源模型", "端侧部署", "笔记本运行", "多模态"],
    ),
    AIProduct(
        product_id="GN-013", name="WeatherNext Cyclones气旋预报模型",
        category=AICategory.AI_GENERAL,
        organization="", country="美国",
        description="气象AI模型，对热带气旋路径、强度和风圈预报平均增加"
                    "一天以上有效提前量，集合预报可扩展至1000种情景。"
                    "在气旋评估中显著提升预报精度和时效。",
        key_metrics={"lead_time_uplift_hours": 24,
                     "ensemble_scenarios": 1000},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="气象预测能力可支撑户外机器人环境感知和"
                              "作业规划",
        deployment_ready=False,
        tags=["气象AI", "气旋预报", "集合预报", "灾害预警"],
    ),
    AIProduct(
        product_id="GN-014", name="Claude隐形水印内容溯源系统",
        category=AICategory.AI_GENERAL,
        organization="", country="美国",
        description="为所有AI输出嵌入隐形水印与C2PA元数据，实现全球AI"
                    "内容溯源。水印可抗复制粘贴和轻度编辑，检测工具可识别"
                    "AI生成内容。率先响应AI内容标识监管要求。",
        key_metrics={"watermark": "invisible", "standard": "C2PA",
                     "resistant_to": "copy-paste, light edits"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="AI内容溯源机制可应用于机器人决策日志和"
                              "操作记录的可信追溯",
        deployment_ready=True,
        tags=["隐形水印", "内容溯源", "C2PA", "AI安全"],
    ),
    AIProduct(
        product_id="CP-011", name="AI算力基础设施融资平台",
        category=AICategory.AI_COMPUTE,
        organization="", country="美国",
        description="与六家国际头部投资机构签署合作备忘录，建立独立算力"
                    "融资平台，计划动员超5000亿美元第三方资本投入AI基础"
                    "设施建设。将GPU集群按基础设施资产审视，算力使用周期"
                    "可达十年，未来将与电力、宽带一样成为社会运行基础配套。",
        key_metrics={"capital_target_billion_usd": 500,
                     "partners": 6, "asset_lifecycle_years": 10},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="大规模算力融资平台为机器人AI训练和推理"
                              "提供长期基础设施保障",
        deployment_ready=False,
        tags=["算力融资", "AI基建", "GPU集群", "基础设施资产化"],
    ),
    AIProduct(
        product_id="EN-015", name="千万千瓦级水风光AI调度模型",
        category=AICategory.RENEWABLE_ENERGY,
        organization="", country="中国",
        description="部署于雅砻江千万千瓦级水风光综合能源基地的AI运行模型。"
                    "通过实时分析降雨、风力、光照等数据，预测未来数十天"
                    "全流域发电能力，估算雨水汇流时间和水电潜力，集成风电、"
                    "光伏和电网负荷数据生成多种运行方案，解决绿色电力间歇"
                    "性和不稳定性问题。",
        key_metrics={"capacity_kw": 10000000,
                     "forecast_days": 30,
                     "energy_types": ["hydro", "wind", "solar"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="AI能源调度技术可类比机器人多源能量管理"
                              "和任务规划",
        deployment_ready=False,
        tags=["水风光", "AI调度", "清洁能源", "多能互补", "雅砻江"],
    ),
    AIProduct(
        product_id="AGR-020", name="国家人工智能农业中试基地",
        category=AICategory.AGRICULTURE,
        organization="", country="中国",
        description="国家级人工智能应用创新载体，聚焦农作物种植方向。"
                    "规划建设不低于185P全国产化智能算力集群，实现算力、"
                    "网络、存储统一调度，满足农业大模型训练、推理迭代和"
                    "场景研发需求。AI变量施肥带动亩均增产30余斤、肥料减量"
                    "20%、人工成本下降50%；智能灌排覆盖120万亩，累计节水"
                    "1.2亿立方米。",
        key_metrics={"compute_pflops": 185, "irrigation_area_mu": 1200000,
                     "water_saved_m3": 120000000,
                     "yield_uplift_jin_per_mu": 30,
                     "fertilizer_reduction_pct": 20,
                     "labor_reduction_pct": 50},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="农业机器人和智能装备是中试基地重要验证"
                              "场景，农业大模型支撑机器人自主作业",
        deployment_ready=False,
        tags=["农业中试基地", "全国产算力", "智慧农业", "变量施肥",
              "智能灌排"],
    ),
    AIProduct(
        product_id="AGR-021", name="丰登种业大模型",
        category=AICategory.AGRICULTURE,
        organization="", country="中国",
        description="国内首个种业大模型，具备'读基因、编序列、算组合'能力，"
                    "可大幅缩短育种周期。通过AI分析基因组数据，智能推荐"
                    "亲本组合和育种方案，加速新品种培育进程。",
        key_metrics={"capability": ["基因读取", "序列编辑", "组合计算"],
                     "application": "育种"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="种业AI与农业机器人协同，从育种到种植"
                              "全链条智能化",
        deployment_ready=False,
        tags=["种业大模型", "基因分析", "智能育种", "农业AI"],
    ),
    AIProduct(
        product_id="HC-012", name="CARE-X胸部X光视觉语言模型",
        category=AICategory.HEALTHCARE,
        organization="", country="美国",
        description="将报告生成、分类、定位与工具辅助测量集成于同一框架的"
                    "胸部X光视觉语言模型。多项回顾性评测显示性能提升，"
                    "模型可自动定位病灶并进行辅助测量。尚处研究阶段，"
                    "不能直接用于临床诊断。",
        key_metrics={"modality": "chest_xray",
                     "capabilities": ["报告生成", "分类", "定位", "测量"]},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="医疗视觉语言模型技术可迁移至机器人视觉"
                              "感知和异常检测系统",
        deployment_ready=False,
        tags=["医学影像", "视觉语言模型", "胸片", "病灶定位", "辅助测量"],
    ),
    AIProduct(
        product_id="6G-004", name="6G R20亚赫兹频段样机",
        category=AICategory.NETWORK_6G,
        organization="", country="中国",
        description="6G第一个标准版本R20进入高密度攻坚期，AI/ML空口设计"
                    "物理层细节进入最终表决。基于亚太赫兹频段（90-150GHz）"
                    "实现小区内400Gbps峰值速率外场传输，7-24GHz厘米波段"
                    "作为连续覆盖核心承载，128T128R大规模MIMO商业样机"
                    "完成。时延抖动控制在10微秒以内，支持算网融合调度和"
                    "空天地一体化。",
        key_metrics={"sub_thz_peak_gbps": 400, "jitter_us": 10,
                     "mimo": "128T128R", "standard": "3GPP R20"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="6G微秒级确定性时延和通感一体化为机器人"
                              "远程控制和群体协同提供通信基础",
        deployment_ready=False,
        tags=["6G", "R20标准", "亚赫兹", "太赫兹", "通感一体", "空天地一体"],
    ),
    AIProduct(
        product_id="CO-008", name="中科智源物流AI智能体平台",
        category=AICategory.COMMERCE,
        organization="", country="中国",
        description="物流全链条AI服务平台，已开发53款预置智能体，涵盖"
                    "运输路径优化、智能拣货、异常预警、运力匹配等场景。"
                    "AI智能体调度订单并直接交由具身智能机器人完成拣选，"
                    "从辅助决策升级为自主执行。亿级包裹仿真推演压缩至"
                    "3分钟内完成，人机协作效率提升超20%。",
        key_metrics={"preset_agents": 53,
                     "simulation_billion_parcels_minutes": 3,
                     "efficiency_uplift_pct": 20},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="物流智能体与具身机器人协作是AI进入"
                              "工业执行层的典型范式",
        deployment_ready=False,
        tags=["物流AI", "智能体平台", "具身机器人", "路径优化", "仿真推演"],
    ),

    # --- 薄弱模块补充：水利/民生/教育 ---
    AIProduct(
        product_id="WA-008", name="宁波AI水库群联合调度系统",
        category=AICategory.WATER_CONSERVANCY,
        organization="", country="中国",
        description="面向甬江流域的AI防洪调度模型。运行完整防洪情景计算从"
                    "传统5-10分钟缩短至5-10秒，每5分钟根据降雨预报和水位"
                    "变化刷新调度建议，计算泄流量、后期蓄水量和洪峰到达时"
                    "剩余库容。数字孪生平台统一管理16座大中型防洪水库，"
                    "实时显示各库容量状态，支持联调联泄而非单库调度。",
        key_metrics={"scenario_calc_seconds": 10, "traditional_minutes": 10,
                     "refresh_interval_minutes": 5, "reservoirs_managed": 16},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="多目标动态调度算法可迁移至多机器人协同"
                              "任务分配和资源调度",
        deployment_ready=False,
        tags=["AI调度", "数字孪生", "水库群", "防洪", "甬江流域"],
    ),
    AIProduct(
        product_id="WA-009", name="节水精灵AI节水智能体",
        category=AICategory.WATER_CONSERVANCY,
        organization="", country="中国",
        description="依托国产大语言模型打造的AI节水智能体，提供轻量化"
                    "语音交互体验。可快速调取用水数据出具专业诊断结果，"
                    "覆盖用水监测、风险预警、趋势预测全流程。将传统事后"
                    "补救的粗放式用水管理升级为事前主动预判的精细化管理"
                    "模式，支持人机语音互动咨询节水优化方案。",
        key_metrics={"coverage": ["用水监测", "风险预警", "趋势预测"],
                     "interaction": "语音对话",
                     "management_mode": "事前预判"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="智能体语音交互和诊断决策框架可应用于"
                              "机器人运维助手和故障排查场景",
        deployment_ready=False,
        tags=["节水智能体", "国产大模型", "语音交互", "智慧水务", "精细化管理"],
    ),
    AIProduct(
        product_id="WA-010", name="智洋创新天空地水工一体化感知平台",
        category=AICategory.WATER_CONSERVANCY,
        organization="", country="中国",
        description="围绕江河湖库、水文监测、防洪防汛、水资源管理和水利"
                    "工程运行管理，运用人工智能、数字孪生和天空地水工"
                    "一体化感知技术，为风险预警、防洪调度和工程管理提供"
                    "支撑。产品体系包括数字孪生智慧水利、无人机智慧测流"
                    "与巡河、水库现代化运行管理、农村供水数字孪生系统。"
                    "卫星拒止空间具身智能无人机可应用于地下管线涵洞、"
                    "综合管廊等复杂空间智能巡检。",
        key_metrics={"business_areas": ["江河湖库", "水文监测", "防洪防汛",
                                        "水资源管理", "工程运行"],
                     "products": ["数字孪生水利", "无人机测流巡河",
                                  "水库运行管理", "农村供水孪生"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="无人机巡检和具身智能无人机直接涉及机器人"
                              "自主导航和空间感知技术",
        deployment_ready=True,
        tags=["天空地感知", "数字孪生", "无人机巡河", "具身智能无人机",
              "农村供水"],
    ),
    AIProduct(
        product_id="WA-011", name="PCG物理约束深度学习径流预测模型",
        category=AICategory.WATER_CONSERVANCY,
        organization="", country="中国",
        description="融合物理约束的CNN-GAN流域尺度日径流预测模型。通过"
                    "卷积神经网络提取空间特征，生成对抗网络对径流场进行"
                    "约束优化，损失函数中嵌入物理约束，提升模型物理合理性"
                    "与鲁棒性。在数据稀缺流域案例中纳什效率系数维持较高"
                    "水平，综合表现优于基准模型和全球水文模型，为数据稀缺"
                    "地区提供兼具高精度与物理可解释性的径流预测新方法。",
        key_metrics={"architecture": "Physics-constrained CNN-GAN",
                     "metric": "NSE>0.6", "advantage": "物理可解释+高精度",
                     "target": "数据稀缺流域"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="物理约束深度学习方法可迁移至机器人动力学"
                              "建模和物理仿真预测",
        deployment_ready=False,
        tags=["径流预测", "CNN-GAN", "物理约束", "数据稀缺", "可解释AI"],
    ),
    AIProduct(
        product_id="LW-008", name="河小西AI数字社工",
        category=AICategory.LIVELIHOOD,
        organization="", country="中国",
        description="面向基层治理的AI数字社工系统，7×24小时在线响应居民"
                    "服务，累计响应超3.4万轮次，补齐非工作时段服务短板。"
                    "配套社工助手辅助高效处置矛盾纠纷、规范生成业务台账，"
                    "为基层减负。城市管理领域实现132小类问题智能闭环处置，"
                    "事件办结率提升至98.92%，环卫类问题处置时长压缩至"
                    "最快15分钟。安全应急领域AI巡查2.8万余次，隐患整改率"
                    "达88.62%。",
        key_metrics={"response_rounds": 34000, "issue_categories": 132,
                     "closure_rate_pct": 98.92,
                     "fastest_response_minutes": 15,
                     "patrol_count": 28000,
                     "hazard_rectification_pct": 88.62},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="AI社工和基层治理智能体可与社区服务机器人"
                              "协同，形成人机共治的民生服务体系",
        deployment_ready=False,
        tags=["数字社工", "基层治理", "7×24在线", "智能闭环", "智慧应急"],
    ),
    AIProduct(
        product_id="LW-009", name="Terrassa市政AI总体规划2026-2028",
        category=AICategory.LIVELIHOOD,
        organization="", country="西班牙",
        description="首个经市议会民主审批通过的市政人工智能总体规划，"
                    "覆盖2026-2028年。规划从诊断、培训到治理全流程设计，"
                    "包括180名管理层对齐研讨、内部工作组、AI委员会和市级"
                    "数据办公室等监督架构、跨部门协调机制以及指标跟踪"
                    "体系。将AI在市政管理中的应用从零散自发状态升级为"
                    "有意识的结构化整合，重点解决数据保护、使用边界和"
                    "碎片化部署问题。",
        key_metrics={"duration": "2026-2028", "executives_trained": 180,
                     "governance": ["AI委员会", "市级数据办公室",
                                    "跨部门协调"],
                     "approval": "市议会民主通过"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="市政AI治理框架为机器人在公共服务领域的"
                              "规模化部署提供制度参考",
        deployment_ready=False,
        tags=["市政AI", "AI治理", "数据保护", "智慧城市", "民主审批"],
    ),
    AIProduct(
        product_id="LW-010", name="华为潍坊AI CITY智慧城市方案",
        category=AICategory.LIVELIHOOD,
        organization="", country="中国",
        description="面向城市治理、民生服务和产业发展的AI CITY解决方案。"
                    "覆盖数字政府、智能制造、教育、医疗、公共安全、产业"
                    "对接六大领域。依托云网AI技术能力发布企业云平台助力"
                    "全域市场主体数字化转型。联合高校、企业和人形机器人"
                    "创新中心发起全国人工智能创新应用行业产教融合共同体，"
                    "搭建产学研用一体化培育平台。昇腾产业联盟汇聚产业链"
                    "上下游构建开放共享AI产业生态。",
        key_metrics={"domains": 6, "ecosystem": "昇腾产业联盟",
                     "platform": "企业云3.0",
                     "community": "产教融合共同体"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="AI CITY为人形机器人和服务机器人提供"
                              "城市级部署场景和基础设施支撑",
        deployment_ready=False,
        tags=["AI CITY", "智慧城市", "数字政府", "昇腾生态", "产教融合"],
    ),
    AIProduct(
        product_id="ED-008", name="ChatGPT Work教育插件套件",
        category=AICategory.EDUCATION,
        organization="", country="美国",
        description="面向K-12教师、大学教师和大学生的三款教育插件，"
                    "集成于ChatGPT Work和Codex。K-12教师插件支持课程"
                    "差异化资源生成、交互式可视化、评估草稿和家校沟通"
                    "模板；大学教师插件辅助课程设计、教学大纲更新、多"
                    "媒体评估和学生材料适配；大学生插件提供个性化辅导、"
                    "测验生成、抽认卡和可视化讲解。通过ChatGPT Edu"
                    "集中部署，符合FERPA隐私合规，默认不使用师生数据"
                    "训练模型。",
        key_metrics={"plugins": 3, "target_users": ["K-12教师", "大学教师",
                                                    "大学生"],
                     "privacy": "FERPA合规", "data_training": "默认不使用"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="教育智能体插件架构可用于机器人技能教学和"
                              "交互式培训系统",
        deployment_ready=True,
        tags=["教育插件", "ChatGPT Work", "K-12", "高等教育", "FERPA"],
    ),
    AIProduct(
        product_id="ED-009", name="Google Classroom Gemini全学段助手",
        category=AICategory.EDUCATION,
        organization="", country="美国",
        description="Google Classroom中的Gemini功能向全年龄段K-12及"
                    "高等教育学生开放。学生可将课程资料转化为抽认卡、"
                    "练习测验等互动学习工具，同步至Gemini Notebook生成"
                    "学习指南和音频概览。新增情境化引导提示功能，允许"
                    "学生选择特定课程和作业，直接结合作业要求和教学大纲"
                    "进行针对性辅导，AI教育从通用问答升级为课程感知的"
                    "个性化学习伙伴。",
        key_metrics={"coverage": "K-12+高等教育",
                     "tools": ["抽认卡", "练习测验", "学习指南", "音频概览"],
                     "feature": "情境化引导提示"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="课程感知的个性化辅导框架可迁移至机器人"
                              "技能教学和自适应训练系统",
        deployment_ready=True,
        tags=["Google Classroom", "Gemini", "个性化学习", "K-12",
              "情境化辅导"],
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
