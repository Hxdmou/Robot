#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI全景注册表 - V1.2
================================================================
新增内容（V1.2 2026-08-13）：
  - 新增40+项AI产品覆盖22大模块
  - 修复农业模块ID冲突(AG->AGR)
  - 更新版本：V1.1 -> V1.2

历史内容：
  1. AICategory（22大类别枚举）
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
    HOME_APPLIANCE = "home_appliance"
    MEDICAL_DEVICE = "medical_device"
    MOBILE_COMPUTER = "mobile_computer"


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
        product_id="HR-000", name="2026年人形机器人产业链全景数据汇总",
        category=AICategory.HUMANOID_ROBOT,
        organization="高工机器人/工信部/各企业发布会", country="中国",
        description="2026年人形机器人行业核心数据全景汇总："
                    "核心零部件成本结构：精密减速器占36%、专用传感器11%、"
                    "高性能伺服电机10%、芯片9%、电池及其他34%；"
                    "减速器、伺服电机、控制器三大核心系统合计占总成本约70%。"
                    "市场预测：2026年全球人形机器人销量有望达40-50万台，"
                    "2030年达280-450万台；2030年市场规模有望破千亿。"
                    "国产替代与产能：当前人形机器人核心零部件国产化率约"
                    "40%-45%，减速器/伺服电机/控制器等卡脖子环节正加速突破，"
                    "有望2027年前后实现65%国产化目标。"
                    "企业产能：宇树科技2026年5月中旬人形机器人日产能达51台，"
                    "月产能超1500台，2026全年产能规划5000台；智元机器人"
                    "2025年9月启动上海数据人工厂（年产1万台整机+2万套关节），"
                    "2026年5月成立无锡产能基地（年产能10万台）；"
                    "优必选2025年底人形机器人年产能达1万台，规划2026年达3万台，"
                    "旗下Walker系列出货超3000台居全球第一。"
                    "资本动态：宇树科技2026年8月科创板IPO申购，被称为"
                    "人形机器人第一股；智元/优必选/银河通用纷纷启动上市进程。"
                    "政策时间线：2023年11月工信部《人形机器人创新发展指导意见》；"
                    "2025年12月26个省份落地人形机器人产业政策；"
                    "2026年人形机器人首次写入政府工作报告、全国两会热点；"
                    "2026年8月WRC2026在北京举行，超160家企业500+展品参展。",
        key_metrics={"cost_structure": {"精密减速器": 36, "专用传感器": 11,
                                      "高性能伺服电机": 10, "芯片": 9,
                                      "电池及其他": 34},
                     "core_three_cost_pct": 70,
                     "sales_2026_low_high": [400000, 500000],
                     "sales_2030_low_high": [2800000, 4500000],
                     "market_scale_2030": "破千亿",
                     "domestic_rate_current_pct": "40-45",
                     "domestic_rate_2027_target_pct": 65,
                     "unitree_daily_capacity": 51,
                     "unitree_monthly_capacity": 1500,
                     "unitree_2026_capacity": 5000,
                     "agibot_shanghai_capacity": "1万台整机+2万套关节",
                     "agibot_wuxi_capacity": 100000,
                     "ubtech_2025_capacity": 10000,
                     "ubtech_2026_target": 30000,
                     "ubtech_walker_shipped": 3000,
                     "policy_timeline": ["2023.11工信部指导意见",
                                       "2025.12 26省产业政策",
                                       "2026年写入政府工作报告",
                                       "2026两会热点",
                                       "2026.8 WRC2026北京"],
                     "wrc2026_companies": 160,
                     "wrc2026_exhibits": 500,
                     "ipo_companies": ["宇树科技(科创板)", "智元", "优必选", "银河通用"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="全面的产业链数据为项目BOM成本估算、"
                              "核心零部件选型、供应链规划、产能评估"
                              "提供权威数据支撑",
        deployment_ready=True,
        tags=["人形机器人产业链", "成本结构", "市场规模预测",
              "国产化率", "产能规划", "宇树IPO", "WRC2026",
              "政策时间线", "核心零部件"],
    ),
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
        description="上半年全球人形机器人出货量约1.91万台，是去年同期"
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
                    "研发资源集中投入M7处理器，有望明年春季提前发布。M7将升级神经网络引擎NPU，"
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
                    "磁电流传感器、AI嗅觉电子鼻等全品类智能传感器。全市智能传感产业"
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
    # 更新：22大模块最新AI产品与技术进展
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
        description="上半年营收59.96亿元同比增长108%，"
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
        product_id="CH-004", name="爱芯元智边缘AI芯片AX615",
        category=AICategory.AI_CHIP,
        organization="爱芯元智", country="中国",
        description="面向物理AI时代的边缘算力芯片，覆盖终端感知、边缘"
                    "算力、车载芯片完整底座。下一代高性能大算力AI芯片"
                    "完成流片，配备HBM高带宽内存，支持两芯或四芯级联，"
                    "实现满血大模型边缘侧高性能推理。2026上半年营收4.02"
                    "亿元同比增长181.8%，毛利率提升至29%。终端计算销量"
                    "翻倍，黑光系列增速超200%；车载SoC出货42万颗，合作"
                    "主机厂25家含7家国际品牌。M57平台已量产上车，M97"
                    "高阶智驾芯片完成工程样片交付。AX615系列已向具身"
                    "机器人、工业视觉领域渗透。现金储备约21.7亿元。",
        key_metrics={"hbm": True, "cascade_support": "2x/4x",
                     "edge_inference": "full_scale",
                     "revenue_2026h1_billion_rmb": 0.402,
                     "revenue_growth_pct": 181.8, "gross_margin_pct": 29,
                     "automotive_soc_shipments": 420000,
                     "automakers": 25, "cash_billion_rmb": 2.17},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="边缘算力：多芯级联为机器人提供可扩展AI算力，"
                              "AX615已进入具身机器人领域",
        deployment_ready=True,
        tags=["AI芯片", "爱芯元智", "AX615", "HBM", "多芯级联",
              "边缘推理", "车载SoC", "具身机器人", "黑光系列"],
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
    AIProduct(
        product_id="WM-005", name="比亚迪HyWorldVLA视觉语言动作模型",
        category=AICategory.WORLD_MODEL,
        organization="比亚迪", country="中国",
        description="比亚迪基于2300万智驾车队实现核心智驾算法数据闭环，"
                    "训练推出的统一VLA视觉语言动作模型，标志着国产"
                    "车企在具身智能VLA技术领域实现重要突破。依托"
                    "大规模真实路采数据闭环训练，可在复杂道路环境下"
                    "实现端到端感知-决策-动作一体化输出，支持L2+到L4"
                    "不同级别自动驾驶。模型架构可向人形机器人运动控制迁移。",
        key_metrics={"fleet_size_million": 23,
                     "data_closed_loop": True,
                     "type": "VLA(视觉语言动作)",
                     "autonomy_support": ["L2+", "L4"],
                     "migration_to_robot": True,
                     "training_data": "2300万智驾车真实路采数据"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="2300万车队数据闭环训练VLA模型，"
                              "架构可直接迁移至人形机器人运动控制，"
                              "是国产端到端具身智能模型重要进展",
        deployment_ready=True,
        tags=["比亚迪", "HyWorldVLA", "视觉语言动作模型", "2300万车队",
              "数据闭环", "端到端", "自动驾驶", "具身智能迁移"],
    ),
    AIProduct(
        product_id="WM-006", name="华为openJiuwen世界模型/具身智能平台",
        category=AICategory.WORLD_MODEL,
        organization="华为", country="中国",
        description="华为推出的openJiuwen开源世界模型与具身智能技术平台，"
                    "支持物理世界精准建模、多模态感知融合、因果推理"
                    "和跨具身迁移。依托昇腾算力底座实现高效训练与端侧"
                    "部署，已在工业巡检、物流分拣、家庭服务等场景验证。"
                    "开放模型权重和开发工具链，降低机器人开发者门槛。",
        key_metrics={"type": "开源世界模型/具身智能平台",
                     "open_source": True,
                     "compute_base": "昇腾NPU",
                     "capabilities": ["物理世界建模", "多模态感知融合",
                                      "因果推理", "跨具身迁移"],
                     "scenarios": ["工业巡检", "物流分拣", "家庭服务"],
                     "open_components": ["模型权重", "开发工具链"]},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="开源世界模型+昇腾算力底座为国产"
                              "人形机器人提供低成本可用的大脑方案，"
                              "工具链开放降低开发门槛",
        deployment_ready=False,
        tags=["华为", "openJiuwen", "开源世界模型", "具身智能平台",
              "昇腾算力", "跨具身迁移", "多模态融合"],
    ),

    # --- AI通用 ---
    AIProduct(
        product_id="AI-003", name="荣耀全球首款量产机器人手机(Robot Phone)",
        category=AICategory.AI_GENERAL,
        organization="荣耀", country="中国",
        description="全球首款实现量产的机器人手机，2026年8月12日发布，"
                    "将四自由度机械臂与盾构钢电机集成至9.59mm机身，"
                    "详情参见MC-040。发布YOYO技能商店，100+系统资源开放，"
                    "与矽递科技开源机器人方案，支持3D打印外壳+Robot kit打造自有机器人。",
        key_metrics={"world_first_mass_production": True,
                     "release_date": "2026-08-12",
                     "mechanical_dof": 4,
                     "thickness_mm": 9.59,
                     "weight_g": 248,
                     "yoyo_skill_store": True,
                     "open_resources": 100,
                     "open_source_partner": "矽递科技",
                     "detail_entry": "MC-040"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="四自由度机械臂+灵巧云台直接应用机器人级"
                              "机械结构，开源方案可直接用于机器人二次开发",
        deployment_ready=False,
        tags=["荣耀Robot Phone", "机器人手机", "四自由度机械臂",
              "盾构钢电机", "YOYO技能商店", "开源机器人", "全球首款量产"],
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
        description="当前处于5G-A商用、6G技术攻坚关键阶段，"
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
        description="新能源汽车月度新车销量占比首次突破60%，"
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
        description="城市NOA从30万以上车型卖点下放至10万以下车型标配，"
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
                    "研发周期从数年缩短至数月；AI+医疗健康市场规模突破千亿元，"
                    "预计跨越1500亿元，年复合增长率30%以上",
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
        description="Q1全球支持端侧AI的智能手表出货量同比增长70%，"
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
                    "（GB 44721-2026）强制性国家标准正式发布，次年7月1日实施。"
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
                    "量产线进入最终调试阶段。计划今年实现量产，"
                    "明年起逐步进入全球门店和商业场景，承担导购、"
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
        description="全球九大云端服务供应商AI服务器出货量年增率"
                    "预期上修至31%，合计资本开支突破8867亿美元，"
                    "同比增长约90%；明年进一步增至1.32万亿美元。"
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
                    "涌入，全年92%资金集中投向有落地订单的头部企业。"
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
        description="上半年国内储能电池销量同比增长53%，"
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
                    "业务线首次单独设立官方发布阵地。Harness团队5月"
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
        description="Omdia将全球半导体市场营收增长预测上调至"
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
                    "的AMI Labs，当年3月获得创纪录的10.3亿美元种子轮"
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
                    "基础设施体系。计划9月发布资格预审公告。",
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
                    "组件首年衰减<1%、30年质保领先。荣膺WITec"
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
                    "智能体产品提供统一协同交互规范。宿迁市方案明确明年"
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
                    "人形整机出货5215台登顶全球纯人形机器人销量榜首，"
                    "人形机器人占主营收入比例从早期1.88%升至51.78%。"
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
        description="今年是人形机器人量产与场景落地关键年份，国内全年"
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
        description="截至年中全国智能算力规模达到去年同期的2.8倍，"
                    "国产大模型全球总下载量突破100亿次。曙光8000登峰"
                    "全国产十万卡AI超集群在郑州投用，每秒峰值算力相当于"
                    "全人类持续计算200年。Anthropic与Riot Platforms达成"
                    "91亿美元20年期算力协议。四大CSP今年资本开支"
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
    AIProduct(
        product_id="CP-011", name="Google第八代TPU 8t/8i训练推理双芯片",
        category=AICategory.AI_COMPUTE,
        organization="Google", country="美国",
        description="Google发布第八代TPU芯片，首次训练推理彻底分家："
                    "TPU 8t（博通合作）专攻大模型训练，TPU 8i（联发科合作）"
                    "聚焦推理服务，均采用台积电2nm制程，搭配谷歌自研Arm"
                    "架构Axion CPU，第四代液冷。TPU 8t单逻辑集群可容纳"
                    "9600枚芯片共享2PB超大带宽内存，芯片间互联带宽翻番，"
                    "总算力121 ExaFlops；整体性能比第七代Ironwood提升近3倍，"
                    "每瓦性能最高翻2倍；自带SparseCore加速器，原生支持FP4"
                    "精度；搭载实时遥测监控+光路电路交换OCS，自动检测绕过"
                    "故障链路重构拓扑。TPU 8i专为破解推理内存墙设计，"
                    "配备288GB高带宽HBM+384MB片上SRAM（SRAM容量为上代3倍），"
                    "模型核心工作集驻留片上延迟砍半；分层Boardfly网络拓扑，"
                    "4芯片为基础单元/36单元成集群，任意两芯片通信最多7跳，"
                    "集合通信加速引擎使片上通信延迟再降5倍；相比上代性价比"
                    "提升80%，每瓦性能提升117%。首次原生支持PyTorch 2.x。"
                    "2026年下半年开放使用，2027年底量产，支撑Gemini系列。",
        key_metrics={"generation": "第八代",
                     "process_node": "台积电2nm",
                     "train_model": "TPU 8t（与博通合作）",
                     "infer_model": "TPU 8i（与联发科合作）",
                     "t8_cluster_chips": 9600,
                     "t8_cluster_memory_pb": 2,
                     "t8_total_flops": "121 ExaFlops FP8",
                     "t8_perf_gain_x": 3,
                     "t8_perf_per_watt_gain_x": 2,
                     "t8_sparsecore": True,
                     "t8_fp4_native": True,
                     "t8_self_healing": "OCS光路电路交换自动重构",
                     "i8_hbm_gb": 288,
                     "i8_sram_mb": 384,
                     "i8_sram_gain_x": 3,
                     "i8_latency_reduction_pct": 50,
                     "i8_boardfly_topology": True,
                     "i8_collective_comm_latency_reduction_x": 5,
                     "i8_cost_perf_gain_pct": 80,
                     "i8_perf_per_watt_gain_pct": 117,
                     "pytorch_2_native": True,
                     "cpu": "自研Axion Arm CPU",
                     "cooling": "第四代液冷",
                     "availability": "2026下半年开放使用",
                     "mass_production": "2027年底",
                     "ai_capex_2026_usd_bn": "1750-1850",
                     "ai_generated_code_pct": 75,
                     "supporting_models": "Gemini系列大模型"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="训练推理芯片分工趋势为机器人端侧推理"
                              "芯片设计提供参考，高算力TPU为大规模"
                              "VLA模型训练提供基础设施",
        deployment_ready=True,
        tags=["Google TPU", "TPU 8t", "TPU 8i", "第八代TPU",
              "训练推理分离", "HBM4", "MXFP4/MXFP8", "65536芯片Pod",
              "Gemini", "AI算力芯片"],
    ),

    # --- AI芯片 ---
    AIProduct(
        product_id="CH-007", name="T1200级碳纤维百吨级量产打破垄断",
        category=AICategory.AI_CHIP,
        organization="", country="中国",
        description="当年3月中国T1200级超高强度碳纤维实现全球首次"
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
        description="前7个月中国新成立23家世界模型创业公司，"
                    "超过去年全年20家。18家在成立数月内完成首轮融资，"
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
                    "日均8000名外籍客商扫货。全球AI眼镜出货量有望"
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
                    "当年3月RAN全会上AI/ML空口设计物理层细节进入最终"
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
                    "突破2300亿元。智能传感产业产值突破100亿元增长29%，"
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
                    "将传统人工调度升级为智能化运行，优化调度增发率"
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
                    "平均转化率超过29%。'成果超市'已促成企业委托项目"
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
        description="防汛中科技新力量全面投入实战。浙江无人机"
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
                    "陪伴缺口、AI头盔保障骑手出行安全。上海预测明年"
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
        product_id="HR-018", name="易百纳教学科研商用一体化智能机械臂",
        category=AICategory.HUMANOID_ROBOT,
        organization="易百纳", country="中国",
        description="易百纳发布的教学科研商用一体化智能机械臂，"
                    "基于海鸥派Hi3403核心板打造。领导臂+从动臂双机械臂"
                    "配置，支持6轴精准联动（5Dof+夹爪基础控制）。"
                    "结构采用PLA光敏树脂3D打印件，领导臂697g/"
                    "从动臂704g，尺寸111×239×525mm/111×173×532mm。"
                    "搭载本地AI视觉模型：海鸥派3403驱动，支持物体"
                    "分拣、标签识别、人脸识别与手势姿态追踪；支持视觉"
                    "引导下精准抓取不规则/柔性物体，多帧点云融合技术"
                    "提升识别精度与环境适应性。舵机采用STS3215系列"
                    "总线舵机（领导臂7.4V 19kg·cm/从动臂12V 30kg·cm）。"
                    "控制器Hi3403核心板：四核ARM Cortex-A55 CPU + "
                    "10.4TOPS INT8 NPU算力。支持Windows/Linux/"
                    "Ubuntu 22.04（ROS2环境），Python/C++编程，"
                    "USB串口(UART)/Wi-Fi/以太网通信。适用场景："
                    "高校机械工程/自动化/AI专业教学实验与科研创新；"
                    "新零售奶茶/咖啡制作、无人售卖店取物等轻量商用。",
        key_metrics={"product_line": "领导臂+从动臂+控制器(海鸥派)",
                     "dof": 6,
                     "structure_material": "PLA光敏树脂3D打印件",
                     "leader_arm_size_mm": "111×239×525",
                     "follower_arm_size_mm": "111×173×532",
                     "leader_arm_weight_g": 697,
                     "follower_arm_weight_g": 704,
                     "work_temp_c": "0~40",
                     "servo": "STS3215总线舵机",
                     "servo_leader": "7.4V 19kg·cm",
                     "servo_follower": "12V 30kg·cm",
                     "power_leader": "5V DC",
                     "power_follower": "12V DC",
                     "controller": "Hi3403核心板(海鸥派3403)",
                     "cpu": "四核ARM Cortex-A55",
                     "npu_tops": 10.4,
                     "npu_precision": "INT8",
                     "vision_ai": ["物体分拣", "标签识别", "人脸识别",
                                   "手势姿态追踪", "不规则/柔性物体抓取"],
                     "vision_tech": "多帧点云融合",
                     "communication": ["USB UART", "Wi-Fi", "以太网"],
                     "os_support": ["Windows", "Linux", "Ubuntu 22.04(ROS2)"],
                     "programming": ["Python", "C++"],
                     "scenarios": ["高校教学科研", "奶茶/咖啡制作", "无人售卖取物"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="10.4TOPS本地NPU视觉模型+6轴联动"
                              "+ROS2支持，是理想的机器人教学与"
                              "二次开发平台，成本可控适合批量部署",
        deployment_ready=False,
        tags=["易百纳", "智能机械臂", "Hi3403", "10.4TOPS NPU",
              "本地AI视觉", "教学科研商用", "ROS2", "6轴联动",
              "物体分拣", "柔性物体抓取"],
    ),
    AIProduct(
        product_id="HR-019", name="应手Y-HandM2仿生灵巧手/信手X-HandM1/博文W-Bot2.0",
        category=AICategory.HUMANOID_ROBOT,
        organization="吉林省仿生机器人创新中心", country="中国",
        description="吉林省仿生机器人创新中心（任露泉院士团队）核心技术成果，"
                    "2025年4月经省工信厅批准正式授牌，建成全国首个仿生机器人"
                    "人工智能+多生态融合示范平台——吉林省仿生机器人MALL。"
                    "应手Y-HandM2仿生灵巧手：38个超高自由度，整手握力达330N，"
                    "可完成33类类人灵巧操控，成功率达96%。"
                    "信手X-HandM1：单手拥有472个触觉传感单元。"
                    "博文W-Bot2.0：全球最小底盘的全尺寸轮式人形机器人。"
                    "仿生四足机器人逐日、追月：广泛应用于电网巡检、"
                    "应急救援等场景。从大脑决策到小脑协调，从肢体执行"
                    "到皮肤感知，全栈技术链条自主可控。",
        key_metrics={"org": "吉林省仿生机器人创新中心",
                     "founder": "任露泉院士",
                     "approval_date": "2025年4月",
                     "platform": "吉林省仿生机器人MALL(全国首个AI+多生态融合示范)",
                     "yhand_name": "应手Y-HandM2",
                     "yhand_dof": 38,
                     "yhand_grip_force_n": 330,
                     "yhand_task_types": 33,
                     "yhand_success_rate_pct": 96,
                     "xhand_name": "信手X-HandM1",
                     "xhand_tactile_sensors": 472,
                     "wbot_name": "博文W-Bot2.0",
                     "wbot_feature": "全球最小底盘全尺寸轮式人形",
                     "quadruped_names": ["逐日", "追月"],
                     "quadruped_scenarios": ["电网巡检", "应急救援"],
                     "tech_stack": ["大脑决策", "小脑协调", "肢体执行", "皮肤感知"],
                     "tech_self_controlled": True},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="38自由度灵巧手(330N握力/96%成功率)"
                              "和472触觉传感单元代表国内仿生手"
                              "顶尖水平，全栈自主可控技术链为人形"
                              "机器人核心零部件国产替代提供关键支撑",
        deployment_ready=False,
        tags=["吉林仿生机器人创新中心", "应手Y-HandM2", "38自由度灵巧手",
              "330N握力", "96%成功率", "信手X-HandM1", "472触觉传感",
              "博文W-Bot2.0", "逐日追月四足", "任露泉院士"],
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
        product_id="HR-020", name="优必选U1消费级全尺寸超仿生人形机器人",
        category=AICategory.HUMANOID_ROBOT,
        organization="优必选", country="中国",
        description="优必选Walker U系列首款消费级全尺寸超仿生人形机器人，"
                    "以消费电子级量产标准打造，对标万元级高配手机市场定价。"
                    "实现高自由度仿生肢体运动、高灵敏环境感知、自然流畅"
                    "人机交互。依托优必选Walker系列工业级双足人形机器人"
                    "技术积累，将核心能力下沉至消费级市场。",
        key_metrics={"series": "Walker U系列",
                     "segment": "消费级全尺寸超仿生人形",
                     "positioning": "对标万元级高配手机",
                     "mass_production_standard": "消费电子级量产"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="标志着全尺寸人形机器人正式进入消费级市场，"
                              "采用消费电子级量产标准将大幅降低成本",
        deployment_ready=False,
        tags=["优必选U1", "消费级人形", "全尺寸超仿生", "Walker U系列",
              "万元级人形机器人", "消费电子级量产"],
    ),
    AIProduct(
        product_id="HR-021", name="宇树科技×DeepSeek战略合作（IPO基石配售）",
        category=AICategory.HUMANOID_ROBOT,
        organization="宇树科技×DeepSeek", country="中国",
        description="双方确立双向优先采购与长期技术协同机制：DeepSeek"
                    "将为宇树具身智能业务提供全系列大模型优先供应与"
                    "专项技术支持，宇树则将DeepSeek列为机器人场景首选"
                    "模型合作伙伴，协同推进多模态感知、运动控制、VLA"
                    "大模型在机器人端侧落地。",
        key_metrics={"cooperation_scope": ["双向优先采购", "长期技术协同",
                                            "模型优先供应", "专项技术支持"],
                     "preferred_partner_mutual": True,
                     "focus_areas": ["多模态感知", "运动控制", "VLA大模型",
                                     "端侧部署"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="中国头部具身智能硬件企业与头部大模型企业"
                              "深度绑定，形成软硬件协同生态，加速VLA落地",
        deployment_ready=True,
        tags=["宇树DeepSeek", "战略合作", "基石配售", "双向优先采购",
              "VLA大模型", "端侧部署", "软硬协同"],
    ),
    AIProduct(
        product_id="HR-022", name="蓝芯算力LX500/RISC-V机器人大脑方案",
        category=AICategory.HUMANOID_ROBOT,
        organization="蓝芯算力（元脑新动力）", country="中国",
        description="基于进迭时空RISC-V芯片推出的具身大脑平台方案，"
                    "以LX500主板、扩展板和载板为核心形态，支持多形态"
                    "机器人产品快速打造，可覆盖从小型教育机器人到大型"
                    "工业人形机器人的全场景需求。LX500主板采用K3核心板，"
                    "板载自研高带宽算力总线，搭载64TOPS算力和丰富接口"
                    "资源，支持多板级联扩展，算力可堆叠至200TOPS以上。"
                    "板卡最小仅手掌大小，支持Wi-Fi6E、2.5G网络、视频"
                    "输入输出，预留miniPCIE和M.2 E-key拓展接口。已适配"
                    "OpenClaw、Ollama、ROS机器人操作系统。",
        key_metrics={"core_chip": "进迭时空K3",
                     "core_board": "LX500主板",
                     "form_factor": "主板+扩展板+载板",
                     "single_board_tops": 64,
                     "stacked_tops": "200TOPS+（多板级联）",
                     "bus": "自研高带宽算力总线",
                     "size": "手掌大小",
                     "connectivity": ["Wi-Fi6E", "2.5G网络", "视频输入输出"],
                     "expansion": ["miniPCIE", "M.2 E-key"],
                     "software_compat": ["OpenClaw", "Ollama", "ROS"],
                     "scenarios": ["教育机器人", "工业人形机器人",
                                   "全场景机器人"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="基于RISC-V的全栈具身大脑方案，开放生态，"
                              "支持ROS，覆盖全尺寸人形机器人算力需求",
        deployment_ready=True,
        tags=["蓝芯算力LX500", "RISC-V具身大脑", "进迭时空K3", "64TOPS",
              "200TOPS级联", "ROS", "OpenClaw", "Ollama"],
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

    # --- 第二十大模块：家用电器AI ---
    AIProduct(
        product_id="HA-001", name="海尔智家全屋智慧家庭L4级主动服务",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="智慧家庭L4级主动服务系统，实现从被动响应到主动预判"
                    "的质变。多模态感知层通过AI视觉识别300种食材、毫米波"
                    "雷达精准定位人体位置；用户建模层持续学习使用习惯并"
                    "主动推送食材采买建议；自主决策层准确率达95%以上，"
                    "无需人工指令即可完成闭环服务。Seeker套系已入驻珠穆朗玛"
                    "科考基地，在-30℃低气压环境中燃气灶主动补氧、冰箱"
                    "为不同食材精准匹配保鲜模式。2026上半年全球智慧家庭"
                    "发明专利2319件，实现15连冠。",
        key_metrics={"smart_level": "L4", "ingredient_recognition": 300,
                     "decision_accuracy_pct": 95, "patents": 2319,
                     "championship_years": 15,
                     "extreme_test_temp_c": -30},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="家电的感知-决策-执行闭环与机器人控制架构"
                              "同源，多模态感知和主动服务技术可迁移至家庭"
                              "服务机器人",
        deployment_ready=True,
        tags=["智慧家庭", "L4主动服务", "多模态感知", "全屋智能", "海尔智家"],
    ),
    AIProduct(
        product_id="HA-002", name="AI家电L1-L5智能分级国标",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="智能家用电器智能分级国家标准，从智能能力和场景效果"
                    "两个维度考核，将家电智能水平分为L1至L5级。L4级为"
                    "当前消费级市场最高水准，要求从被动响应跃升为主动服务。"
                    "标准要求企业明确标注功能效用和隐私风险提示，消费者可"
                    "像看能效标识一样一眼判断智能水平。同步发布的《智能"
                    "家用电器质量安全风险分类评价指南》（GB/T 47777—2026）"
                    "将风险分为电器安全、功能安全、信息安全、数据与隐私"
                    "保护四大类别，覆盖网络入侵、系统漏洞、隐私泄露等"
                    "数字化风险。",
        key_metrics={"standard": "L1-L5分级", "top_level": "L4",
                     "risk_categories": 4,
                     "gb_standard": "GB/T 47777-2026"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="智能分级标准为机器人自主能力分级提供参考"
                              "框架，信息安全和隐私保护要求同样适用于"
                              "家庭服务机器人",
        deployment_ready=True,
        tags=["智能分级", "国标", "L4主动服务", "信息安全", "隐私保护"],
    ),
    AIProduct(
        product_id="HA-003", name="美的智能家居互联互通平台",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="智能家居互联互通标准核心编制单位，联合家电院、信通院、"
                    "电子四院等权威机构推进局域网互联互通标准，聚焦产品"
                    "发现、会话管理、权限分享、业务交互等关键技术，破解"
                    "产品生态割裂、交互不畅的行业痛点。美的集团位列2026"
                    "《财富》世界500强第231位，营收4585亿元、"
                    "净利润439.5亿元。智慧家庭覆盖空调、冰箱、洗衣机等"
                    "全品类，AI视觉推理平台已在智能体工厂落地，检测节奏"
                    "匹配生产节拍。",
        key_metrics={"fortune_500_rank": 231, "revenue_2025_billion": 458.5,
                     "net_profit_billion": 43.95,
                     "standard_role": "核心编制单位",
                     "interconnection_features": ["产品发现", "会话管理",
                                                  "权限分享", "业务交互"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="互联互通标准是机器人与智能家居设备协同"
                              "工作的通信基础，机器人需接入家庭物联网"
                              "生态",
        deployment_ready=True,
        tags=["互联互通", "美的", "智能家居标准", "世界500强", "全品类"],
    ),
    AIProduct(
        product_id="HA-004", name="格力AI节能空调",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="搭载AI算法的智能空调，可根据天气变化自动切换运行"
                    "模式：梅雨天自动除湿，高温天自动加强制冷。毫米波"
                    "雷达检测室内无人时自动进入节能待机模式。实测三月"
                    "电费较同期降低近50%。同时深耕高端装备领域，实现"
                    "工业母机技术自主突围，赋能制造业升级。空调行业"
                    "2026新冷年延续经销商淡季打款进货策略。",
        key_metrics={"energy_saving_pct": 50,
                     "sensors": ["毫米波雷达", "温湿度传感器"],
                     "modes": ["自动除湿", "智能制冷", "节能待机"],
                     "industrial_machine": "工业母机自主突围"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="毫米波雷达人体感知和AI节能决策算法可迁移"
                              "至机器人环境感知和自主节能调度",
        deployment_ready=True,
        tags=["AI空调", "毫米波雷达", "节能待机", "格力", "智能温控"],
    ),
    AIProduct(
        product_id="HA-005", name="AI冰箱视觉食材管理系统",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="搭载AI视觉识别技术的智能冰箱，可识别300种以上食材"
                    "种类和数量，主动检测食材保质期并弹出提醒，根据"
                    "库存食材推荐菜谱。AI之眼为不同食材精准匹配保鲜"
                    "模式，调节温度、湿度和气体浓度。支持与生鲜电商"
                    "联动，食材不足时自动生成采购清单。从被动储物"
                    "升级为主动食材管家。",
        key_metrics={"ingredient_recognition": 300,
                     "features": ["保质期提醒", "菜谱推荐", "自动采购清单",
                                  "精准保鲜"],
                     "sensors": ["AI摄像头", "温湿度传感器", "气体传感器"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="冰箱内机械臂取放食材是家庭机器人典型"
                              "操作场景，视觉识别和物品管理技术直接"
                              "支撑机器人厨房作业",
        deployment_ready=True,
        tags=["AI冰箱", "视觉识别", "食材管理", "智能保鲜", "菜谱推荐"],
    ),
    AIProduct(
        product_id="HA-006", name="一体化电视AI语音交互系统",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="将机顶盒功能软件化内置到电视中，无需外接机顶盒，"
                    "一台电视即可使用直播、时移、回看、点播等全部电视"
                    "服务。实现开机看直播、一个遥控器操控、智能语音"
                    "交互、超高清播放。四大运营商面向全国有线电视与"
                    "IPTV用户规模化推广数千万台，彻底整治电视套娃收费"
                    "和操作繁琐问题。AI语音支持自然语言换台、搜索内容、"
                    "控制智能家居设备。",
        key_metrics={"settop_box_builtin": True,
                     "operators": 4, "scale": "数千万台",
                     "features": ["开机看直播", "单遥控器", "智能语音",
                                  "超高清播放"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="电视语音交互中枢可作为家庭服务机器人的"
                              "入口和显示终端，机器人通过电视与家庭成员"
                              "交互",
        deployment_ready=True,
        tags=["一体化电视", "AI语音", "套娃收费治理", "智能家居中枢", "IPTV"],
    ),
    AIProduct(
        product_id="HA-007", name="AI洗衣机污渍识别自动程序",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="搭载AI视觉和传感器的智能洗衣机，可自动识别咖啡渍、"
                    "油渍、血渍等常见污渍类型，根据面料材质和污渍程度"
                    "自动匹配洗涤程序、水温、转速和洗涤剂用量。内置"
                    "称重传感器自动感知衣物重量调节水位。AI算法持续"
                    "学习用户洗涤偏好优化程序。从用户手动选择程序升级"
                    "为机器自主判断。",
        key_metrics={"stain_types": ["咖啡渍", "油渍", "血渍"],
                     "auto_features": ["程序匹配", "水温调节", "转速控制",
                                       "洗涤剂定量"],
                     "sensors": ["AI摄像头", "称重传感器", "浊度传感器"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="污渍视觉识别和柔性物料处理技术可迁移至"
                              "机器人清洁和衣物整理任务",
        deployment_ready=False,
        tags=["AI洗衣机", "污渍识别", "自动程序", "智能投放", "视觉检测"],
    ),

    # --- 第二十一模块：医疗设备AI ---
    AIProduct(
        product_id="MD-001", name="图迈腔镜手术机器人",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="自主研发的腔镜手术机器人，获欧盟CE MDR认证，"
                    "全球商业化订单突破300台，覆盖60多个国家和地区，"
                    "品牌影响力位居全球前二。创造近70项全球首例纪录，"
                    "在全球近30个国家累计完成远程人体临床手术超1000例，"
                    "占全球远程手术总量50%，手术实施成功率100%。"
                    "可用于泌尿外科、普通外科、胸外科、妇科机器人远程手术。"
                    "欧盟首次以法规文件形式确认远程手术医疗模式。",
        key_metrics={"global_orders": 300, "countries": 60,
                     "remote_surgeries": 1000,
                     "remote_share_pct": 50, "success_rate_pct": 100,
                     "global_firsts": 70, "certifications": ["CE MDR", "NMPA"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="腔镜手术机器人是具身智能在精密操作领域的"
                              "典型应用，多臂协调、力反馈、远程操控技术"
                              "直接支撑机器人精细操作能力",
        deployment_ready=True,
        tags=["腔镜手术机器人", "远程手术", "CE认证", "微创外科", "国产替代"],
    ),
    AIProduct(
        product_id="MD-002", name="蛇形臂手术机器人",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="95%零部件国产化的蛇形臂手术机器人，成本仅为海外"
                    "同行1/3至1/2。2026上半年手术机器人出口额4.8亿元、"
                    "同比增长3.3倍，覆盖49个国家和地区。已落地德国、"
                    "西班牙等欧洲顶级医院。蛇形臂设计可在人体自然腔道"
                    "和狭窄解剖空间中灵活穿行，实现深部手术的微创入路。",
        key_metrics={"localization_pct": 95, "cost_ratio": 0.33,
                     "export_2026h1_billion_rmb": 0.48,
                     "export_growth_pct": 330, "countries": 49},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="蛇形臂连续体机器人是特种机器人的重要"
                              "分支，柔性控制和路径规划技术可迁移至"
                              "工业检测和救援机器人",
        deployment_ready=True,
        tags=["蛇形臂", "手术机器人", "国产化95%", "出口暴增", "欧洲医院"],
    ),
    AIProduct(
        product_id="MD-003", name="博睿康NEO-ONE侵入式脑机接口",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="全球首款获国家药监局批准上市的侵入式脑机接口"
                    "医疗器械。128通道全植入式脑机接口系统多中心临床"
                    "试验由北京天坛医院担任组长单位启动。高位截瘫患者"
                    "已实现意念操控轮椅与机器狗，意念控制气动手套完成"
                    "抓握、取物、喝水等日常动作。今年成为中国脑机"
                    "接口商业化元年。",
        key_metrics={"channels": 128, "implant_type": "全植入式",
                     "approval": "NMPA批准上市",
                     "clinical_lead": "北京天坛医院",
                     "applications": ["意念轮椅", "机器狗控制",
                                      "气动手套", "日常动作"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="脑机接口是机器人控制的终极交互方式，"
                              "意念控制直接打通大脑与机器人的通信链路",
        deployment_ready=True,
        tags=["脑机接口", "侵入式", "NMPA首批", "意念控制", "神经康复"],
    ),
    AIProduct(
        product_id="MD-004", name="联影元智医疗大模型uMetaImaging",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="整合文本、影像、视觉、语音多模态数据的医疗大模型，"
                    "已开发10余款智能体。uMetaImaging影像智能体一次"
                    "胸部CT扫描可检出37种疾病，AUC达0.92。覆盖影像、"
                    "病理、中医药、科研等多元临床场景，多款医疗大模型"
                    "达国际领先水平。依托全国示范性医疗AI数据基础设施，"
                    "汇聚海量优质三医数据。",
        key_metrics={"modalities": ["文本", "影像", "视觉", "语音"],
                     "agents": 10, "ct_diseases": 37, "auc": 0.92,
                     "test_platform": "MedBench 4.0"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="多模态医学影像理解是机器人辅助诊断和"
                              "手术导航的核心感知能力",
        deployment_ready=False,
        tags=["医疗大模型", "多模态", "CT影像", "37种疾病", "联影"],
    ),
    AIProduct(
        product_id="MD-005", name="祥生乳腺AI超声机器人",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="自主研发的乳腺人工智能超声机器人，已获得医疗器械"
                    "检测报告。集成触摸屏、电动检查床、六自由度机械臂、"
                    "超声影像自动传输和AI辅助阅片一体化设计，可实现"
                    "大规模扫查与数据跟踪管理，构建筛查-转诊-治疗全"
                    "闭环管理模式。在视觉深度点云数据分割算法、力控"
                    "算法和超声图像伺服控制算法领域处于行业领先。"
                    "围绕AI技术生态（大脑）—高清探头（眼）—超声"
                    "机器人（手）三位一体协同体系。",
        key_metrics={"dof": 6, "components": ["触摸屏", "电动检查床",
                                              "六自由度机械臂", "AI阅片"],
                     "workflow": "筛查-转诊-治疗全闭环",
                     "algorithms": ["点云分割", "力控", "超声伺服"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="六自由度机械臂+力控+视觉伺服是典型的"
                              "机器人技术栈，直接体现具身智能在医疗"
                              "场景的落地",
        deployment_ready=False,
        tags=["超声机器人", "乳腺筛查", "六自由度", "力控算法", "AI阅片"],
    ),
    AIProduct(
        product_id="MD-006", name="强生Ottava软组织手术机器人",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="美国",
        description="获FDA营销授权的软组织机器人辅助手术系统，正式"
                    "进入软组织机器人辅助手术市场，直接对标达芬奇。"
                    "将推进日本、西欧审批。三模合一手术机器人同步获"
                    "FDA批准，标志着手术机器人从单科室向多科室通用"
                    "平台演进。直觉外科同步启动达芬奇降本转型，国产"
                    "替代迎来关键变局。",
        key_metrics={"approval": "FDA营销授权", "target": "软组织手术",
                     "competitor": "达芬奇", "next_markets": ["日本", "西欧"],
                     "mode": "三模合一"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="软组织手术机器人对力反馈、柔组织建模"
                              "和自主缝合技术要求极高，推动机器人精细"
                              "操作能力边界",
        deployment_ready=True,
        tags=["Ottava", "软组织手术", "FDA批准", "三模合一", "强生"],
    ),
    AIProduct(
        product_id="MD-007", name="龙点睛AI经皮穿刺导航机器人",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="国内首款AI经皮穿刺导航机器人，基于术前CT/MRI"
                    "影像和AI算法自动规划最佳穿刺路径，术中通过光学"
                    "导航实时跟踪穿刺针位置，动态修正呼吸位移。"
                    "一次性到位成功率提升45%，显著减少CT扫描次数和"
                    "手术时间。适用于肝、肾、肺等器官的活检和消融"
                    "治疗。核心专利覆盖10余国，获国家级知识产权密集型"
                    "产品认证。",
        key_metrics={"first_pass_improvement_pct": 45,
                     "navigation": "光学实时跟踪",
                     "targets": ["肝", "肾", "肺"],
                     "procedures": ["活检", "消融"],
                     "patent_countries": 10},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="穿刺导航是机器人空间定位和路径规划的"
                              "典型应用，呼吸运动补偿技术对机器人动态"
                              "跟踪有参考价值",
        deployment_ready=True,
        tags=["穿刺导航", "AI路径规划", "光学跟踪", "呼吸补偿", "首款"],
    ),
    AIProduct(
        product_id="MD-008", name="如身具身养老护理机器人",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="全球首个载人与服务双模态具身养老护理机器人，"
                    "搭载七自由度20kg大负载力控柔顺机械臂，实现喂饭、"
                    "递送、搬运、护理辅助等高频服务动作自主化。完成"
                    "亿元Pre-A轮融资。作为科技人形护理机器人天枢、天玑"
                    "集成跨设备智能联动、厘米级灵巧操作、多模态拟人"
                    "情感陪护等六大核心能力，覆盖失能照护六大场景。"
                    "国内首个具身智能康复示范基地落地上海，已累计服务"
                    "超4600名康复治疗者。",
        key_metrics={"dof": 7, "payload_kg": 20,
                     "mode": "载人+服务双模态",
                     "funding": "亿元Pre-A轮",
                     "rehab_patients": 4600,
                     "care_scenarios": 6},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="护理机器人是具身智能在民生领域的核心"
                              "应用，力控柔顺机械臂和情感交互直接体现"
                              "机器人服务能力",
        deployment_ready=False,
        tags=["护理机器人", "具身智能", "七自由度", "养老", "力控柔顺"],
    ),

    # --- AI芯片补充 ---
    AIProduct(
        product_id="CH-009", name="昆仑芯P800国产AI训练芯片",
        category=AICategory.AI_CHIP,
        organization="", country="中国",
        description="百度系第三代自研AI芯片，采用XPU-P异构并行架构，"
                    "FP16/BF16峰值算力345 TFLOPS，为英伟达H20的2.3倍。"
                    "96GB HBM3显存，显存带宽2.4TB/s。单机8卡可运行"
                    "DeepSeek-V3/R1 671B满血版模型，32台服务器支持"
                    "全参训练。万卡集群线性加速比达96%，支持3.2万卡"
                    "规模部署。7nm工艺，单卡功耗400W，同等算力成本"
                    "仅为国际大厂60%。已点亮国内首个全自研三万卡集群。",
        key_metrics={"fp16_tflops": 345, "memory_gb": 96,
                     "memory_bandwidth_tbs": 2.4, "process_nm": 7,
                     "power_w": 400, "max_cluster_cards": 32000,
                     "linear_speedup_pct": 96, "cost_ratio": 0.6},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="高算力国产芯片为具身智能大模型训练和"
                              "端侧推理提供自主可控的算力底座",
        deployment_ready=True,
        tags=["昆仑芯", "P800", "国产替代", "XPU架构", "万卡集群", "DeepSeek适配"],
    ),
    AIProduct(
        product_id="CH-011", name="曲速科技Polaris-H SRAM推理芯片",
        category=AICategory.AI_CHIP,
        organization="", country="中国",
        description="国内首款SRAM架构推理专用芯片，2021年量产累计出货"
                    "超10万颗。片上SRAM容量超550MB为全球首款，芯片面积"
                    "超800mm²，片内带宽超30TB/s，良率超80%。大模型"
                    "推理权重可驻留片上，大幅减少片外DRAM访问，降低"
                    "推理延迟和功耗。推理能效比和低延迟优势显著，适合"
                    "推理集中、延迟敏感场景。550MB SRAM容量领先Cerebras"
                    "（44MB晶圆级）和Groq（LPU架构）。",
        key_metrics={"sram_mb": 550, "die_area_mm2": 800,
                     "onchip_bandwidth_tbs": 30, "yield_pct": 80,
                     "cumulative_shipments": 100000,
                     "architecture": "SRAM推理专用",
                     "mass_production_year": 2021},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="低延迟推理芯片适合机器人实时决策和"
                              "端侧大模型部署场景",
        deployment_ready=True,
        tags=["SRAM", "推理芯片", "曲速科技", "低延迟", "片上存储"],
    ),

    # --- 世界模型补充 ---
    AIProduct(
        product_id="WM-009", name="MoWorld-3D交互式三维世界模型",
        category=AICategory.WORLD_MODEL,
        organization="", country="中国",
        description="国家人工智能应用中试基地联合华为、魔芯科技发布，"
                    "全栈基于昇腾NPU构建的交互式三维世界模型。28B参数"
                    "MoE混合专家架构，用户可通过图像、文本生成具备空间"
                    "结构的三维场景，支持相机六自由度运动作为物理信号，"
                    "可在生成的世界中行走、转身、环绕观测。建筑结构、"
                    "道路走向、物体位置均贴合真实空间规律。推理综合成本"
                    "仅为同等规模进口GPU方案30%。向全行业开放能力，"
                    "支撑具身智能规模化训练。",
        key_metrics={"parameters_b": 28, "architecture": "MoE",
                     "compute": "昇腾NPU", "cost_ratio": 0.3,
                     "interaction": "6DoF物理信号",
                     "applications": ["具身智能", "自动驾驶", "数字孪生"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="3D世界模型为机器人提供可交互的物理仿真"
                              "训练环境，直接降低真机训练成本",
        deployment_ready=False,
        tags=["MoWorld-3D", "昇腾NPU", "3D交互", "MoE", "数字孪生训练场"],
    ),
    AIProduct(
        product_id="WM-011", name="心智世界模型MWM",
        category=AICategory.WORLD_MODEL,
        organization="", country="全球",
        description="牛津大学和新加坡国立大学联合提出的心智世界建模框架，"
                    "登顶Hugging Face Daily Papers日榜第一。将信念、目标、"
                    "情绪、人际关系等心智变量纳入世界状态，构建物理-心智"
                    "耦合的全局模拟器。解决传统世界模型只能预测物理状态"
                    "却无法正确预测人行为的问题。目标智能体只能观察到"
                    "全局状态经过转换的第一人称视角，模型生成针对该"
                    "智能体的局部观测并基于此采取行动。开源代码Mentis"
                    "已发布。",
        key_metrics={"institution": ["牛津大学", "新加坡国立大学"],
                     "paper_rank": "HuggingFace日榜第一",
                     "framework": "Mental World Modeling",
                     "open_source": "Mentis",
                     "core_innovation": "物理-心智耦合状态",
                     "mental_variables": ["信念", "目标", "情绪",
                                          "人际关系", "社会责任"]},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="心智建模使服务机器人能理解用户意图、"
                              "情绪和社会规范，实现真正的人机协作",
        deployment_ready=False,
        tags=["心智世界模型", "MWM", "心智理论", "人机协作", "开源"],
    ),

    # --- 6G网络补充 ---
    AIProduct(
        product_id="6G-010", name="英伟达AI-RAN 6G智能基站",
        category=AICategory.NETWORK_6G,
        organization="", country="美国",
        description="英伟达推动的AI原生无线接入网，让基站同时承担通信"
                    "连接和AI计算任务，从传输管道升级为算力节点。已投资"
                    "10亿美元认购诺基亚约2.9%股份，联合诺基亚、爱立信、"
                    "T-Mobile、德国电信、软银等提出开放软件定义AI原生"
                    "6G平台。在中国寻找基站厂商合作方开发6G基站，希望"
                    "2027-2028年进入试验网。AI-RAN测试已实现基站同时"
                    "提供5G连接和边缘AI任务。高通判断谁拿下边缘AI谁就"
                    "更可能赢下AI时代。",
        key_metrics={"nokia_investment_billion_usd": 1.0,
                     "nokia_stake_pct": 2.9,
                     "partners": ["诺基亚", "爱立信", "T-Mobile",
                                  "德国电信", "软银"],
                     "target_trial_year": "2027-2028",
                     "concept": "AI-RAN",
                     "china_base_station_share_pct": 65},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="AI-RAN基站为机器人提供边缘计算节点，"
                              "实现低延迟AI推理和通信一体化",
        deployment_ready=False,
        tags=["AI-RAN", "英伟达", "6G基站", "边缘AI", "诺基亚", "算力节点"],
    ),

    # --- 家用电器补充 ---
    AIProduct(
        product_id="HA-008", name="科沃斯AI扫地机器人地宝X9",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="搭载AI视觉导航和双线激光3D避障的扫地机器人，"
                    "支持AI物体识别分类（鞋子、电线、宠物粪便等200+"
                    "障碍物），自动标记禁区。滚筒活洗系统实现扫拖洗"
                    "一体，基站自动集尘、热水洗拖布、热风烘干、自动"
                    "补水。支持语音控制和App远程管理，建图精度达厘米"
                    "级。2026上半年服务机器人销量增长35%，线下渠道"
                    "销售额同比增长45%。",
        key_metrics={"obstacle_types": 200, "navigation": "AI视觉+双线激光",
                     "features": ["自动集尘", "热水洗拖布", "热风烘干",
                                  "自动补水", "语音控制"],
                     "mapping_accuracy_cm": 1,
                     "sales_growth_pct": 35},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="扫地机器人是家庭服务机器人的成熟形态，"
                              "SLAM导航和避障技术直接支撑室内机器人"
                              "自主移动",
        deployment_ready=True,
        tags=["扫地机器人", "AI导航", "激光避障", "扫拖一体", "科沃斯"],
    ),
    AIProduct(
        product_id="HA-009", name="卡萨帝AI大师灶",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="搭载AI之眼2.0智感烹饪技术与原创五环直喷大师火系统，"
                    "实现炖煮防溢锅、爆炒火力旺还防炙烤。AI视觉实时监测"
                    "锅温和食物状态，自动调节火候。推动智慧家庭战略在"
                    "厨房场景快速落地，提供AI家电、AI场景、AI生活"
                    "完整解决方案。",
        key_metrics={"ai_version": "AI之眼2.0",
                     "burner_system": "五环直喷大师火",
                     "features": ["防溢锅", "防炙烤", "自动调火",
                                  "视觉监测"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="厨房场景的AI视觉与火候控制涉及传感器融合"
                              "和闭环控制，是家庭服务机器人在厨房场景的"
                              "技术基础",
        deployment_ready=True,
        tags=["AI厨电", "卡萨帝", "AI之眼", "智能烹饪", "防溢锅"],
    ),
    AIProduct(
        product_id="HA-010", name="美的MevoX自进化AI智能体",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="美的全屋智能战略核心，构建AI Agent能力、智能家居"
                    "家电融合矩阵和人车家生态三位一体智能版图。MevoX"
                    "自进化智能体搭配家庭智航系统MIA 1.0，实现多设备"
                    "统一调度与主动决策。技术栈融合AI大模型、IoT与"
                    "分布式OS，基于OpenHarmony打造家鸿OS支持断网"
                    "本地联动。小美AI支持10余种方言识别，准确率超95%，"
                    "设备协同响应0.3秒。全球联网智能家电超1.4亿台，"
                    "主导80余项国家标准。",
        key_metrics={"connected_devices": 140000000,
                     "dialects": 10, "dialect_accuracy_pct": 95,
                     "response_latency_s": 0.3,
                     "standards_led": 80, "os": "家鸿OS(OpenHarmony)",
                     "ecosystem": "人·车·家"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="家庭AI大脑和多设备调度系统为服务机器人"
                              "提供家庭环境感知和跨设备协同的基础设施",
        deployment_ready=True,
        tags=["MevoX", "AI智能体", "MIA 1.0", "家鸿OS", "人车家", "美的"],
    ),
    AIProduct(
        product_id="HA-011", name="海尔国家AI应用中试基地(消费领域)",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="海尔智家承建聚焦消费领域·家居家电方向的国家人工智能"
                    "应用中试基地。L4级主动服务通过中家院认证，毫米波"
                    "雷达人体定位误差≤10cm，AI之眼2.0识别300种食材，"
                    "决策准确率95%以上。全球智慧家庭注册用户超1.3亿，"
                    "APP月活增幅46%。2319件专利连续15年行业第一。"
                    "微信AI Agent首批适配，支持自然语言直接控制家电。",
        key_metrics={"registered_users": 130000000,
                     "mau_growth_pct": 46, "patents": 2319,
                     "patent_rank_years": 15,
                     "l4_certified": True,
                     "radar_accuracy_cm": 10,
                     "ingredient_types": 300},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="L4级主动服务和多模态感知为家庭服务机器人"
                              "提供成熟的感知-决策-执行技术栈",
        deployment_ready=True,
        tags=["国家中试基地", "海尔", "L4认证", "AI之眼", "微信AI"],
    ),
    AIProduct(
        product_id="HA-012", name="石头A30 Pro Combo 2.0五合一洗地机",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="五合一全能清洁设备，集洗地机、吸尘器、除螨仪、"
                    "随手吸、缝隙吸五种清洁形态于一体。AI智能识别"
                    "地面材质和脏污程度，自动调节吸力和水量。热水"
                    "自清洁滚筒，热风烘干防异味。支持App智能规划"
                    "清洁路径，边角覆盖率达99.5%。",
        key_metrics={"modes": 5, "edge_coverage_pct": 99.5,
                     "features": ["AI脏污识别", "热水自清洁",
                                  "热风烘干", "智能路径规划"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="多形态切换和AI脏污识别涉及机器人末端"
                              "工具切换和环境感知技术",
        deployment_ready=True,
        tags=["洗地机", "石头科技", "五合一", "AI清洁", "自清洁"],
    ),
    AIProduct(
        product_id="HA-013", name="微信AI Agent家电生态",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="微信开放AI Agent能力，美的、海尔作为首批完成适配的"
                    "头部品牌，用户可通过自然语言在微信内直接控制设备。"
                    "美的接入空调、热水器、洗衣机、空气净化器、烟机"
                    "五大类别，海尔接入挂式/立式空调、燃气/电热水器。"
                    "指令执行延迟约0.5秒，支持复杂场景编排如"
                    "\"早晨模式\"联动多设备。标志着家电控制从App"
                    "向对话式AI交互跃迁。",
        key_metrics={"first_batch_brands": ["美的", "海尔"],
                     "execution_latency_s": 0.5,
                     "interaction": "自然语言对话",
                     "midea_categories": 5,
                     "ecosystem": "微信AI Agent"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="对话式AI控制为机器人提供更自然的人机"
                              "交互入口，降低用户使用门槛",
        deployment_ready=False,
        tags=["微信AI", "AI Agent", "自然语言控制", "美的", "海尔"],
    ),

    # --- 医疗设备补充 ---
    AIProduct(
        product_id="MD-009", name="MedBench 4.0中文医疗大模型测试平台",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="国家人工智能应用上海中试基地打造的全球领先中文"
                    "医疗大模型测试平台，建立权威、统一的行业测评标准。"
                    "覆盖影像、病理、中医药、科研等多元临床场景评测。"
                    "中试基地同时推出6大医疗垂直基础模型，构建全栈"
                    "自主可控多模态大模型矩阵，多款达国际领先水平。"
                    "建成全国示范性医疗AI数据基础设施，汇聚海量优质"
                    "三医数据。",
        key_metrics={"version": "4.0",
                     "vertical_models": 6,
                     "modalities": ["影像", "病理", "中医药", "科研"],
                     "infrastructure": "全国示范性医疗AI数据底座",
                     "computing": "国模用国芯"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="医疗大模型评测标准为机器人在医疗场景的"
                              "AI能力提供量化评估基准",
        deployment_ready=False,
        tags=["MedBench", "医疗大模型", "评测平台", "上海中试基地", "多模态"],
    ),
    AIProduct(
        product_id="MD-010", name="肝胆肿瘤与胸部影像临床智能体",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="国家AI应用上海中试基地推出的临床智能体矩阵。"
                    "肝胆肿瘤智能体已推广至122家医疗机构，服务超"
                    "百万人次。胸部影像一扫多查智能体累计处理病例"
                    "超250万例，覆盖全国20余家医院。心血管病"
                    "\"观心\"智能体实现心血管疾病AI辅助诊断。"
                    "临床效率与诊疗精准度显著提升，推动医疗AI从"
                    "单点突破迈向系统集成。",
        key_metrics={"liver_organs": 122,
                     "liver_patients": 1000000,
                     "chest_cases": 2500000,
                     "chest_hospitals": 20,
                     "agents": ["肝胆肿瘤", "胸部影像", "心血管观心",
                                "金牌编码员", "电子病历生成"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="临床智能体的多模态诊断能力可迁移至"
                              "机器人辅助诊断和手术导航系统",
        deployment_ready=True,
        tags=["临床智能体", "肝胆肿瘤", "胸部影像", "心血管", "上海中试基地"],
    ),
    AIProduct(
        product_id="MD-011", name="春风化雨8iRobotics脊柱手术机器人",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="三友医疗控股法国Implanet联合研发的全球首款多臂"
                    "人形智能化脊柱手术机器人。已在欧亚北美五家医院"
                    "完成科研临床装机，完成欧洲首台装机并推进脊柱/"
                    "神经外科临床评估及欧盟CE认证。与法国亚眠-皮卡第"
                    "大学医疗中心达成临床合作。多臂协同实现脊柱螺钉"
                    "置入的高精度导航和实时力反馈，手术精度达亚毫米级。",
        key_metrics={"type": "多臂人形脊柱手术机器人",
                     "installed_hospitals": 5,
                     "regions": ["欧洲", "亚洲", "北美"],
                     "certification_target": "CE",
                     "partner": "法国Implanet",
                     "accuracy": "亚毫米级"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="多臂人形手术机器人是具身智能在精密外科"
                              "的前沿应用，多臂协同和力反馈技术直接"
                              "推动机器人精细操作能力",
        deployment_ready=False,
        tags=["脊柱手术机器人", "多臂协同", "三友医疗", "CE认证", "中欧合作"],
    ),
    AIProduct(
        product_id="MD-012", name="脑虎科技植入式脑机接口系统",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="植入式脑机接口手部运动功能代偿系统正式启动GCP"
                    "注册临床试验。采用柔性电极微创植入技术，在"
                    "保证信号质量的同时大幅降低脑组织损伤。与清华"
                    "大学NEO系统共同推进全球首个植入脑机接口多中心"
                    "注册临床。高位截瘫患者已实现意念操控轮椅与"
                    "机器狗，意念控制气动手套完成抓握、取物、喝水"
                    "等日常动作。湘雅医院完成全国首例侵入式BCI视觉"
                    "重建临床试验。",
        key_metrics={"trial_type": "GCP注册临床",
                     "electrode": "柔性微创",
                     "applications": ["意念轮椅", "机器狗控制",
                                      "气动手套", "视觉重建"],
                     "partners": ["清华大学", "湘雅医院",
                                  "华山医院", "天坛医院"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="脑机接口建立大脑与机器人的直接通信链路，"
                              "是机器人控制的终极交互方式",
        deployment_ready=False,
        tags=["脑机接口", "脑虎科技", "柔性电极", "GCP临床", "意念控制", "视觉重建"],
    ),
    AIProduct(
        product_id="MD-013", name="Vivim外科AI术中血管导航系统",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="南方医科大学珠江医院联合中科院深圳先进院、香港"
                    "科技大学（广州）自主研发的外科人工智能模型。"
                    "首次将动态手术视频解析算法应用于腹腔镜肝切除"
                    "手术，可在术中实时识别并勾勒关键血管边界，"
                    "实现\"术中实时导航\"功能。AI自动识别肝静脉、"
                    "门静脉等关键解剖结构，辅助医生避开大出血风险"
                    "区域，提升手术安全性和肿瘤切缘精度。",
        key_metrics={"application": "腹腔镜肝切除",
                     "function": "术中实时血管导航",
                     "capabilities": ["动态视频解析", "血管边界勾勒",
                                      "解剖结构识别", "出血风险预警"],
                     "developers": ["南方医科大学珠江医院",
                                    "中科院深圳先进院",
                                    "香港科技大学广州"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="术中实时视频解析和血管边界识别是手术"
                              "机器人自主导航和安全操作的核心感知能力",
        deployment_ready=False,
        tags=["Vivim", "术中导航", "腹腔镜", "血管识别", "AI手术视频", "珠江医院"],
    ),
    AIProduct(
        product_id="MD-014", name="华为WATCH D2医疗级血压手表",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="全球首款通过NMPA/CE MDR医疗器械认证的腕部动态"
                    "血压监测手表。24小时动态血压监测、HRV压力评估、"
                    "微体检报告生成，本地端侧AI处理保障数据隐私。"
                    "示波法血压测量达到医疗级精度，支持房颤筛查和"
                    "睡眠呼吸暂停检测，准确率超90%。跌倒检测80ms"
                    "内自动呼救。全球出货量登顶智能手表市场。",
        key_metrics={"price_start_rmb": 2988,
                     "certifications": ["NMPA", "CE MDR"],
                     "features": ["24h动态血压", "HRV", "房颤筛查",
                                  "OSA检测", "跌倒检测", "ECG"],
                     "fall_detection_ms": 80,
                     "screening_accuracy_pct": 90,
                     "processing": "端侧AI",
                     "screen_inch": 1.5,
                     "battery_days": 6,
                     "weight_g": 54,
                     "waterproof_5atm": True},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="可穿戴医疗设备为护理机器人提供连续"
                              "健康监测数据流，支撑主动健康干预",
        deployment_ready=True,
        tags=["华为", "WATCH D2", "血压监测", "NMPA认证", "房颤筛查", "端侧AI"],
    ),

    # --- 手机和电脑 ---
    AIProduct(
        product_id="MC-001", name="荣耀Robot Phone机器人手机",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="全球首款具身智能机器人手机，首创四自由度钛合金灵巧"
                    "云台，加工精度±0.005mm，电机仅2.6g，扭矩密度120"
                    "N·m/L。搭载Agentic OS内核+YOYO Pro机器人模式，"
                    "联合阿里千问深度共创终端大模型，支持连续100+步复杂"
                    "任务。与百年电影品牌ARRI联合调校影像，驭光H1自研"
                    "芯片支持14档动态范围、ARRI LogC3曲线。第五代骁龙8"
                    "至尊版，7060mAh电池，120W快充。9.59mm/248g。"
                    "12GB+512GB版9999元，16GB+1TB版12999元。",
        key_metrics={"price_start_rmb": 9999, "price_top_rmb": 12999,
                     "platform": "骁龙8至尊版Gen5", "battery_mah": 7060,
                     "fast_charge_w": 120, "wireless_charge_w": 50,
                     "thickness_mm": 9.59, "weight_g": 248,
                     "dof": 4, "motor_weight_g": 2.6,
                     "precision_mm": 0.005, "torque_density": "120N·m/L",
                     "camera_main_mp": 200, "display_inch": 6.31,
                     "peak_brightness_nits": 6800,
                     "ai_model": "千问终端大模型",
                     "os": "Agentic OS", "task_steps": 100},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="四自由度机械云台是机器人关节技术微型化的"
                              "消费级落地，Agentic OS实现感知-推理-规划-"
                              "执行-反馈完整AI闭环，手机可作为机器人中控",
        deployment_ready=True,
        tags=["机器人手机", "荣耀", "钛合金云台", "Agentic OS", "YOYO Pro",
              "ARRI", "千问", "驭光H1", "具身智能终端"],
    ),
    AIProduct(
        product_id="MC-002", name="小米澎湃OS 4+MiMo端侧大模型",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="小米澎湃OS 4首批Beta版发布，底层用Rust重写核心"
                    "模块，流畅度提升40%，后台保活率提高35%，安装包"
                    "缩小30%。超级小爱升级至2.0接入MiMo端侧大模型，"
                    "可自主执行多步骤任务。全新柔光玻璃智能材质感知"
                    "环境颜色和触控操作，前置主动AI感知和AI感色融色UI，"
                    "功耗由NPU协同处理极低。首批覆盖小米17系列，正式版"
                    "随小米18系列9月发布。彻底摆脱Android依赖，迈向"
                    "全场景智能操作系统。",
        key_metrics={"smoothness_improvement_pct": 40,
                     "background_retention_pct": 35,
                     "package_size_reduction_pct": 30,
                     "language": "Rust",
                     "ai_model": "MiMo端侧大模型",
                     "assistant_version": "超级小爱2.0",
                     "first_batch": "小米17系列",
                     "stable_release": "小米18系列(9月)",
                     "features": ["柔光玻璃", "AI感色融色UI",
                                  "主动AI感知", "NPU低功耗"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="Rust重写的底层OS和端侧大模型为机器人提供"
                              "高可靠、低延迟的系统软件基础，多步骤自主"
                              "任务执行直接对应机器人任务规划能力",
        deployment_ready=False,
        tags=["澎湃OS 4", "MiMo", "Rust", "超级小爱", "端侧大模型", "小米18"],
    ),
    AIProduct(
        product_id="MC-003", name="华为Pura X Max阔折叠旗舰",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="首创大阔折形态，外屏5.4英寸、内屏7.7英寸。搭载"
                    "麒麟9030 Pro芯片，后置四摄，5300mAh电池。"
                    "首销三个月销量突破60万台，累计约64.47万台，"
                    "在万元级高端市场表现突出。起售价10999元，提供"
                    "典藏版和标准版。带动苹果、三星等品牌跟进阔折叠"
                    "形态。即将推出新配色，与Mate 90系列同台亮相。",
        key_metrics={"price_start_rmb": 10999,
                     "price_top_rmb": 13999,
                     "chip": "麒麟9030 Pro",
                     "form_factor": "大阔折叠",
                     "battery_mah": 5300, "sales_3months": 644700,
                     "cameras": 4,
                     "ram_gb": "12GB/16GB",
                     "rom_gb": "256GB/512GB/1TB",
                     "storage_options": ["12GB+256GB 10999元",
                                        "12GB+512GB 11999元",
                                        "16GB+512GB典藏版 12999元",
                                        "16GB+1TB典藏版 13999元"],
                     "wired_charge_w": 66, "wireless_charge_w": 50,
                     "rear_camera_main": "5000万像素超聚光主摄（F1.4-F4.0十档可变光圈，OIS光学防抖）",
                     "rear_camera_ultrawide": "4000万像素超广角摄像头",
                     "rear_camera_telephoto": "5000万像素超聚光长焦摄像头（OIS光学防抖，3.5倍光学变焦）",
                     "rear_camera_spectrum": "红枫原色摄像头（多光谱传感器）",
                     "rear_camera_count": 4,
                     "front_camera_main": "1300万像素超广角摄像头（F2.0光圈，自动对焦）",
                     "front_camera_depth": "3D深感摄像头",
                     "front_camera_count": 2,
                     "outer_screen_inch": 5.4,
                     "inner_screen_inch": 7.7,
                     "inner_screen_type": "OLED阔折叠大屏",
                     "outer_screen_type": "OLED外屏",
                     "hinge": "天工铰链",
                     "weight_g": 235,
                     "waterproof": "IPX8",
                     "os": "HarmonyOS",
                     "colors": ["零度白", "月影灰", "鸢尾紫", "鎏光黑"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="折叠屏形态创新和大屏交互为机器人手持"
                              "终端和远程操控界面提供设计参考",
        deployment_ready=True,
        tags=["华为", "Pura X Max", "阔折叠", "麒麟9030 Pro", "万元旗舰"],
    ),
    AIProduct(
        product_id="MC-004", name="三星Galaxy Z Fold8 Ultra折叠旗舰",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="韩国",
        description="三星首款Ultra命名折叠屏手机，8英寸超大主屏，展开"
                    "厚度仅4.1mm超纤薄机身。2亿像素主摄+5000万超广角，"
                    "支持8K APV编解码器和电影级LUT。钛缓震层技术结合"
                    "增强型钛金属板与钛合金薄膜，淡化折痕。第五代骁龙8"
                    "至尊版(for Galaxy)，5000mAh电池，石墨冷却结构。"
                    "Galaxy AI围绕折叠屏深度适配，即圈即搜升级支持"
                    "图片主体识别和关键信息提取。",
        key_metrics={"main_screen_inch": 8, "thickness_unfolded_mm": 4.1,
                     "camera_main_mp": 200, "camera_ultrawide_mp": 50,
                     "video": "8K APV", "chip": "骁龙8至尊版Gen5",
                     "battery_mah": 5000, "cooling": "石墨冷却",
                     "ai_features": ["即圈即搜", "主体识别",
                                     "信息提取", "照片助手"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="大屏多任务和AI信息提取能力可迁移至"
                              "机器人操作终端和远程监控界面",
        deployment_ready=True,
        tags=["三星", "Z Fold8 Ultra", "折叠屏", "2亿像素", "Galaxy AI", "钛缓震"],
    ),
    AIProduct(
        product_id="MC-005", name="REDMI K100 Pro Max性能旗舰",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="185Hz高刷屏+第五代骁龙8至尊版+AI独显芯片。"
                    "首发价4199元起，叠加国家补贴后实际入手价低至"
                    "3699元起。定位性能旗舰，AI独显芯片支持游戏"
                    "超分超帧和AI画质增强。在两千元至四千元价位段"
                    "提供旗舰级AI算力和游戏体验。",
        key_metrics={"price_start_rmb": 4199, "price_subsidy_rmb": 3699,
                     "refresh_rate_hz": 185, "platform": "骁龙8至尊版Gen5",
                     "ai_chip": "AI独显芯片",
                     "features": ["游戏超分", "超帧", "AI画质增强"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="高刷屏和AI独显芯片为机器人可视化调试"
                              "和仿真渲染提供高性价比终端方案",
        deployment_ready=True,
        tags=["REDMI", "K100 Pro Max", "185Hz", "AI独显", "国补"],
    ),
    AIProduct(
        product_id="MC-006", name="Apple MacBook Pro M5 Max AI PC",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="美国",
        description="搭载M5 Pro和M5 Max芯片，每核均配备神经网络加速器，"
                    "统一内存带宽大幅提升，性能较前代最高4倍、较M1最高"
                    "8倍。支持最高128GB统一内存，可本地运行大语言模型。"
                    "配备Apple N1芯片支持Wi-Fi 7和蓝牙6。14/16英寸"
                    "两种尺寸，深空黑色与银色。M5 Pro起步1TB，M5 Max"
                    "起步2TB。Apple Intelligence深度集成，AI本地推理"
                    "能力行业领先。",
        key_metrics={"chip": "M5 Pro/M5 Max",
                     "performance_vs_prev": "4x",
                     "performance_vs_m1": "8x",
                     "max_memory_gb": 128, "npu": "每核神经网络加速器",
                     "wifi": "Wi-Fi 7", "bluetooth": "BT 6",
                     "sizes": ["14英寸", "16英寸"],
                     "ai": "Apple Intelligence",
                     "storage_start_tb": 1},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="128GB统一内存可本地运行大模型，为机器人"
                              "AI推理和仿真训练提供强大的本地算力平台",
        deployment_ready=True,
        tags=["MacBook Pro", "M5 Max", "Apple Intelligence", "128GB", "Wi-Fi 7"],
    ),
    AIProduct(
        product_id="MC-007", name="联想小新Pro 16 GT AI元启版",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="搭载第三代酷睿Ultra X9 388H处理器，预装天禧个人"
                    "超级智能体3.5。16英寸OLED星耀舒适屏，2880x1800"
                    "分辨率，峰值亮度1100尼特，ΔE<1专业色准，七档"
                    "色域切换。99.9Wh超大电池，丝绸铝冲铸一体机身，"
                    "1.72kg/15.9mm。6.2英寸触控板，全尺寸键盘+数字"
                    "区。HDMI2.1+双雷电4接口。12大项可靠性认证。",
        key_metrics={"processor": "Intel Core Ultra X9 388H",
                     "display_inch": 16, "resolution": "2880x1800",
                     "peak_brightness_nits": 1100, "color_delta_e": 0.78,
                     "battery_wh": 99.9, "weight_kg": 1.72,
                     "thickness_mm": 15.9, "ai_agent": "天禧3.5",
                     "ports": ["HDMI 2.1", "Thunderbolt 4 x2",
                               "USB-A x2", "SD", "3.5mm"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="大屏OLED和高色准为机器人可视化编程、"
                              "仿真调试和数据标注提供优质显示终端",
        deployment_ready=True,
        tags=["联想", "小新Pro 16", "AI元启", "酷睿Ultra", "OLED", "天禧智能体"],
    ),
    AIProduct(
        product_id="MC-008", name="Intel Core Ultra Series 3 (18A)",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="美国",
        description="Intel首款基于18A工艺的移动处理器平台，美国本土"
                    "设计和制造的最先进半导体工艺。NPU驱动的Hybrid AI"
                    "架构，Copilot+ PC标准NPU算力40-50 TOPS。数百款"
                    "OEM设计覆盖Acer、ASUS、Dell、HP、Lenovo、LG、"
                    "MSI、Samsung等全球品牌。Intel Arc显卡含12个"
                    "Xe核心，为Intel最高性能集显。推动AI PC从概念"
                    "走向主流普及。",
        key_metrics={"process_nm": 18, "npu_tops": "40-50",
                     "standard": "Copilot+ PC",
                     "gpu_cores": 12, "gpu_arch": "Intel Arc Xe2",
                     "oem_partners": ["Acer", "ASUS", "Dell", "HP",
                                      "Lenovo", "LG", "MSI", "Samsung"],
                     "ai_features": "Hybrid AI"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="x86生态的AI PC平台为机器人开发和"
                              "边缘部署提供最广泛的软硬件兼容基础",
        deployment_ready=True,
        tags=["Intel", "Core Ultra", "18A", "NPU", "Copilot+ PC", "AI PC"],
    ),
    AIProduct(
        product_id="MC-009", name="ThinkPad X14 AI 2026商旅本",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="全场景便携AI商旅本，碳纤维机身1.2kg/15mm。至高"
                    "酷睿Ultra X9处理器，16核16线程最高睿频5.1GHz，"
                    "整机180TOPS AI算力，NPU峰值50TOPS。74Wh电池"
                    "15.5小时办公续航，1小时快充80%。2.8K屏1000nits，"
                    "ΔE<1硬件校色。MIL-STD-810H 26项军标测试。"
                    "首发9499元起，国补8074元起。",
        key_metrics={"weight_kg": 1.2, "thickness_mm": 15,
                     "processor": "Core Ultra X9",
                     "ai_tops_total": 180, "npu_tops": 50,
                     "battery_wh": 74, "battery_life_h": 15.5,
                     "fast_charge_pct": 80, "fast_charge_min": 60,
                     "display": "2.8K 1000nits", "color_delta_e": 1,
                     "military_standard": "MIL-STD-810H 26项",
                     "price_start_rmb": 9499,
                     "price_subsidy_rmb": 8074},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="军标耐用性和便携性适合现场机器人"
                              "调试和部署，180TOPS算力支撑本地AI",
        deployment_ready=True,
        tags=["ThinkPad", "X14 AI", "商旅本", "180TOPS", "军标", "酷睿Ultra"],
    ),
    AIProduct(
        product_id="MC-010", name="Apple MacBook Neo入门AI本",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="美国",
        description="Apple迄今最实惠笔记本电脑，起售价4599元。无风扇"
                    "静音设计，13英寸Liquid视网膜显示屏，最长16小时"
                    "电池续航。可驱动各类app的AI功能，1080p FaceTime"
                    "摄像头和双麦克风。铝金属机身提供桃粉、靛蓝、银色、"
                    "柑橘黄四色。Apple Intelligence入门体验，降低"
                    "AI PC门槛。",
        key_metrics={"price_start_rmb": 4599, "display_inch": 13,
                     "battery_life_h": 16, "fanless": True,
                     "camera": "1080p FaceTime",
                     "colors": ["桃粉", "靛蓝", "银色", "柑橘黄"],
                     "ai": "Apple Intelligence",
                     "body": "铝金属"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="低价AI PC降低机器人开发者的入门硬件"
                              "门槛，无风扇设计适合安静实验室环境",
        deployment_ready=True,
        tags=["MacBook Neo", "Apple", "入门AI本", "无风扇", "4599元"],
    ),

    # --- 华为8月5日全场景新品发布会 ---
    AIProduct(
        product_id="AU-012", name="鸿蒙智行尊界V800旗舰MPV",
        category=AICategory.AUTOMOTIVE,
        organization="", country="中国",
        description="国产百万级超豪华MPV，车长5495mm/轴距3430mm，"
                    "舱内有效空间3.9m，2+2+3七座布局。搭载1.5T增程器"
                    "+前后双电机四驱，系统综合功率390kW，65kWh 6C三元锂"
                    "电池，CLTC纯电340km，综合续航1335km。基于途灵龙行平台，"
                    "全系标配双腔空簧+双阀CDC+±12°后轮转向，行政版/领航版"
                    "标配800V全主动悬架（单轮举升力12000N、行程80mm）。"
                    "华为乾崑智驾ADS 5，6激光雷达+40传感器，L3冗余架构。"
                    "三联屏（12.3寸仪表+双17.2寸3.4K中控/副驾），41扬声器"
                    "HUAWEI SOUND ULTIME，灵云AI座椅20点按摩，41.6寸投影"
                    "巨幕，卷轴星空顶1608颗灯珠。售价76.6万-101.6万元。",
        key_metrics={"price_start_rmb": 766000, "price_top_rmb": 1016000,
                     "length_mm": 5495, "wheelbase_mm": 3430,
                     "power_kw": 390, "battery_kwh": 65,
                     "ev_range_km": 340, "total_range_km": 1335,
                     "lidar_count": 6, "sensors": 40,
                     "ads_version": "ADS 5", "speakers": 41,
                     "seats": 7, "rear_steer_deg": 12,
                     "active_suspension": "800V全主动悬架"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="6激光雷达+40传感器的L3冗余架构是自动驾驶"
                              "机器人感知系统的标杆，全主动悬架线控技术"
                              "与机器人运动控制同源",
        deployment_ready=True,
        tags=["尊界V800", "华为", "MPV", "ADS 5", "6激光雷达",
              "全主动悬架", "增程", "百万级", "途灵龙行平台"],
    ),
    AIProduct(
        product_id="AU-013", name="鸿蒙智行尊界V680旗舰MPV",
        category=AICategory.AUTOMOTIVE,
        organization="", country="中国",
        description="尊界品牌第二款车型，车长5320mm/轴距3290mm，"
                    "与V800同平台共享动力总成和智驾系统。1.5T增程器"
                    "+双电机四驱390kW，65kWh电池，CLTC纯电340km，"
                    "综合续航1208km。全系标配双腔空簧+CDC+后轮转向，"
                    "华为乾崑ADS 5+6激光雷达+40传感器。二排双零重力"
                    "座椅（16点按摩）、21.4寸后排娱乐屏、41扬声器、"
                    "电动隐私帷幔。入门即豪华，售价64.8万元。",
        key_metrics={"price_start_rmb": 648000,
                     "length_mm": 5320, "wheelbase_mm": 3290,
                     "power_kw": 390, "battery_kwh": 65,
                     "ev_range_km": 340, "total_range_km": 1208,
                     "lidar_count": 6, "sensors": 40,
                     "ads_version": "ADS 5", "speakers": 41,
                     "seats": 7, "rear_steer_deg": 12},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="同V800共享L3智驾冗余架构和线控底盘，"
                              "是高性价比自动驾驶研究参考平台",
        deployment_ready=True,
        tags=["尊界V680", "华为", "MPV", "ADS 5", "6激光雷达",
              "增程", "64.8万", "途灵龙行平台"],
    ),
    AIProduct(
        product_id="AU-014", name="鸿蒙智行享界G9硬派豪华SUV",
        category=AICategory.AUTOMOTIVE,
        organization="", country="中国",
        description="鸿蒙智行首款硬派豪华SUV，首发华为全地形途灵平台，"
                    "标配±12°后轮转向，横向响应更干净。提供五座/六座"
                    "布局，增程和纯电两种动力。寰宇三联屏+鸿蒙智行专属"
                    "HarmonyOS车机。预售24小时小订破1万台，Ultra及以上"
                    "版本占比90%，72小时订单突破1.5万台。预售价43.98万元起。",
        key_metrics={"price_start_rmb": 439800,
                     "platform": "华为全地形途灵平台",
                     "rear_steer_deg": 12,
                     "seats_options": [5, 6],
                     "powertrain": ["增程", "纯电"],
                     "presale_24h_orders": 10000,
                     "presale_72h_orders": 15000,
                     "ultra_ratio_pct": 90},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="全地形途灵平台和后轮转向技术对越野"
                              "机器人和无人地面车辆运动控制有参考价值",
        deployment_ready=False,
        tags=["享界G9", "华为", "硬派SUV", "全地形途灵平台",
              "后轮转向", "预售", "鸿蒙智行"],
    ),
    AIProduct(
        product_id="MC-011", name="华为MateBook Fold非凡大师折叠电脑",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="第二代鸿蒙折叠屏电脑，18英寸双层OLED折叠屏"
                    "（3.3K/1600nit/92%屏占比/200万:1对比度），"
                    "首次原生支持HUAWEI M-Pen 3手写笔。40μm超薄UTG"
                    "玻璃抗冲击提升90%，SGS五星抗跌落认证。玄武水滴铰链"
                    "锆基液态金属主轴，100°-120°无级悬停。麒麟X90 Plus"
                    "处理器28W TDP，整机性能提升25%。HarmonyOS 6.1，"
                    "小艺慧记端侧离线会议纪要，小艺深度研究多智能体协同，"
                    "全球首款原生AI换脸伪造检测电脑。75Wh电池/14h视频/"
                    "140W快充。双模叠层天线Wi-Fi信号领先3dB。提供"
                    "24GB+512GB、24GB+1TB、32GB+2TB三种配置，"
                    "售价24999-29999元。",
        key_metrics={"price_start_rmb": 24999, "price_top_rmb": 29999,
                     "screen_inch": 18, "resolution": "3.3K",
                     "peak_brightness_nits": 1600,
                     "screen_ratio_pct": 92,
                     "contrast_ratio": "2000000:1",
                     "processor": "麒麟X90 Plus", "tdp_w": 28,
                     "performance_gain_pct": 25,
                     "battery_wh": 75, "video_playback_h": 14,
                     "fast_charge_w": 140, "reverse_charge_w": 66,
                     "weight_kg": 1.16, "thickness_unfolded_mm": 7.3,
                     "os": "HarmonyOS 6.1",
                     "utg_thickness_um": 40,
                     "impact_resistance_gain_pct": 90,
                     "stylus": "M-Pen 3",
                     "hinge_angle": "100-120度无级悬停",
                     "ai_features": ["小艺慧记离线转写",
                                     "多智能体协同研究",
                                     "AI换脸检测", "小艺任务Agent"],
                     "ram_gb": "24GB/32GB",
                     "rom_gb": "512GB/1TB/2TB",
                     "storage_options": ["24GB+512GB 24999元",
                                         "24GB+1TB 26999元",
                                         "32GB+2TB 29999元"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="折叠屏+手写笔的大屏交互为机器人示教"
                              "编程和远程操控提供创新界面，端侧AI"
                              "换脸检测可用于机器人安全身份验证",
        deployment_ready=True,
        tags=["MateBook Fold", "非凡大师", "华为", "折叠电脑",
              "麒麟X90 Plus", "M-Pen 3", "18英寸OLED", "鸿蒙6.1",
              "AI换脸检测", "玄武水滴铰链"],
    ),
    AIProduct(
        product_id="MC-012", name="华为MateBook Pro S超轻薄本",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="全球最轻14英寸金属笔记本，仅798g/11.9mm。"
                    "镁锂合金无螺丝一体化机身（榫卯结构抗变形提升500%），"
                    "首创微绒金属工艺。麒麟XE90处理器，单核性能提升23%、"
                    "能效提升25%、NPU算力提升40%，20W性能释放。业界首款"
                    "柔性OLED灵盾防窥屏（一区双像素架构，一键防窥不糊），"
                    "14.2英寸3.1K/264PPI/1600nit/ΔE<1，AI智能感知身后"
                    "有人提醒防窥。3D 6麦克风10米拾音+AI同声分离。"
                    "四天线Wi-Fi 7+最远1km联网。18h视频续航/66W反向快充。"
                    "提供标准版、柔光版、防窥版和典藏版，售价7999-14999元。",
        key_metrics={"price_start_rmb": 7999, "price_top_rmb": 14999,
                     "weight_g": 798, "thickness_mm": 11.9,
                     "screen_inch": 14.2, "resolution": "3120x2080",
                     "ppi": 264, "peak_brightness_nits": 1600,
                     "color_delta_e": 1, "processor": "麒麟XE90",
                     "single_core_gain_pct": 23,
                     "efficiency_gain_pct": 25,
                     "npu_gain_pct": 40, "tdp_w": 20,
                     "battery_h": 18, "fast_charge_w": 66,
                     "material": "镁锂合金",
                     "structure": "榫卯一体化无螺丝",
                     "wifi": "Wi-Fi 7+", "max_range_m": 1000,
                     "antennas": 4, "microphones": 6,
                     "pickup_range_m": 10,
                     "ram_gb": "16GB/32GB",
                     "rom_gb": "512GB/1TB/2TB",
                     "storage_options": ["16GB+512GB 7999元",
                                         "16GB+1TB 9999元",
                                         "32GB+1TB 11999元",
                                         "32GB+2TB 14999元"],
                     "privacy_screen": "灵盾防窥屏",
                     "colors": ["晨曦黄", "仲夏紫", "丝绒白",
                                "烟云灰", "羽砂黑"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="798g超轻量+NPU 40%提升适合作为机器人"
                              "调试终端和移动监控站，灵盾防窥屏保护"
                              "机器人控制数据安全",
        deployment_ready=True,
        tags=["MateBook Pro S", "华为", "798g", "麒麟XE90",
              "灵盾防窥屏", "镁锂合金", "Wi-Fi 7", "超轻薄",
              "鸿蒙6.1", "小艺任务"],
    ),
    AIProduct(
        product_id="MC-013", name="华为MatePad Pro 2026平板",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="华为续航最长平板，仅439g/4.7mm厚，10英寸以上"
                    "全球最轻。12英寸OLED屏幕，云隼架构三段式主板布局，"
                    "全金属一体化机身。搭载麒麟T93芯片，首次在平板"
                    "搭载北斗卫星短报文功能，无地面网络可收发消息。"
                    "搭配二代M-Pencil手写笔。售价5999元起（悦享款5699元）。",
        key_metrics={"price_start_rmb": 5699,
                     "price_top_rmb": 7699,
                     "weight_g": 439, "thickness_mm": 4.7,
                     "screen_inch": 12, "screen_type": "OLED",
                     "refresh_hz": 144,
                     "processor": "麒麟T93",
                     "ram_gb": "12GB/16GB",
                     "rom_gb": "256GB/512GB/1TB",
                     "storage_options": ["12GB+256GB 5699元（悦享款）",
                                         "12GB+512GB 6199元",
                                         "16GB+512GB 6699元",
                                         "16GB+1TB 7699元"],
                     "battery_mah": 12000,
                     "charge_w": 100,
                     "satellite_msg": True,
                     "stylus": "二代M-Pencil",
                     "speakers": 6,
                     "os": "HarmonyOS",
                     "architecture": "云隼架构"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="北斗卫星短报文功能可用于无网络环境"
                              "下机器人远程通信和应急指令传输",
        deployment_ready=True,
        tags=["MatePad Pro", "华为", "439g", "麒麟T93",
              "北斗卫星消息", "OLED", "M-Pencil"],
    ),
    AIProduct(
        product_id="MC-014", name="华为nova 16 SE手机",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="中端定位新机，搭载麒麟8020芯片，下放旗舰原色"
                    "影像系统。8500mAh超大电池+66W快充，主打长续航"
                    "人像拍摄。支持北斗卫星消息和星闪音频（NearLink "
                    "E2.0）。提供128GB/256GB/512GB三个版本，售价"
                    "2499-3199元，国补到手2124元起。樱雪晴空、天际白、"
                    "星空黑、破晓橙四色。",
        key_metrics={"price_start_rmb": 2499, "price_top_rmb": 3199,
                     "price_subsidy_rmb": 2124,
                     "chip": "麒麟8020", "battery_mah": 8500,
                     "fast_charge_w": 66,
                     "ram_gb": "8GB",
                     "storage_options": ["8GB+128GB 2499元",
                                         "8GB+256GB 2699元",
                                         "8GB+512GB 3199元"],
                     "satellite_msg": True,
                     "nearlink": "E2.0",
                     "colors": ["樱雪晴空", "天际白", "星空黑", "破晓橙"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="超大电池和北斗卫星消息适合作为机器人"
                              "户外遥控器和应急通信终端",
        deployment_ready=True,
        tags=["nova 16 SE", "华为", "麒麟8020", "8500mAh",
              "北斗消息", "星闪", "国补", "中端AI手机"],
    ),
    AIProduct(
        product_id="MD-015", name="华为WATCH GT 7智能手表",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="华为新一代智能手表标准版，46mm竞速版与41mm"
                    "轻薄版双尺寸。升级健康感知系统，支持心率、血管"
                    "健康监测、睡眠呼吸暂停筛查。新增纳米微晶陶瓷表圈。"
                    "多配色满足商务和运动需求。售价1588元起。",
        key_metrics={"price_start_rmb": 1488,
                     "price_top_rmb": 2188,
                     "sizes": ["46mm竞速版", "41mm轻薄版"],
                     "health_features": ["心率监测", "血管健康",
                                         "睡眠呼吸暂停筛查",
                                         "血氧监测", "压力监测"],
                     "bezel_material": "纳米微晶陶瓷",
                     "screen_inch": 1.43,
                     "battery_days_46mm": 14,
                     "battery_days_41mm": 7,
                     "waterproof_5atm": True,
                     "sports_modes": 100},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="可穿戴健康监测数据可接入机器人"
                              "健康监护系统，实现人体状态感知",
        deployment_ready=True,
        tags=["WATCH GT 7", "华为", "健康监测", "纳米微晶陶瓷",
              "血管健康", "智能手表"],
    ),
    AIProduct(
        product_id="MD-016", name="华为WATCH GT 7 Pro智能手表",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="Pro版采用航天级钛合金表壳+纳米微晶陶瓷表圈+"
                    "蓝宝石玻璃表镜，屏幕峰值亮度3000尼特。松霜绿、"
                    "境野黄、碳晶黑三色。EasyCross易扣表带，户外属性"
                    "更强。最长续航21天，支持专业运动模式和健康监测。"
                    "售价2688元。",
        key_metrics={"price_start_rmb": 2688,
                     "price_top_rmb": 3288,
                     "case_material": "航天级钛合金",
                     "bezel_material": "纳米微晶陶瓷",
                     "glass": "蓝宝石玻璃",
                     "screen_inch": 1.5,
                     "peak_brightness_nits": 3000,
                     "battery_life_days": 21,
                     "waterproof_5atm": True,
                     "diving_m": 40,
                     "gnss": "双频五星",
                     "sports_modes": 100,
                     "colors": ["松霜绿", "境野黄", "碳晶黑"],
                     "band": "EasyCross易扣表带"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="钛合金+蓝宝石的耐用设计可参考"
                              "机器人传感器外壳防护方案",
        deployment_ready=True,
        tags=["WATCH GT 7 Pro", "华为", "钛合金", "蓝宝石玻璃",
              "21天续航", "3000nit", "户外健康手表"],
    ),
    AIProduct(
        product_id="HA-014", name="华为Vision智慧屏6 SE RGB电视",
        category=AICategory.HOME_APPLIANCE,
        organization="", country="中国",
        description="华为首款RGB-MiniLED电视，55英寸售价3499元，"
                    "75英寸售价5799元。RGB-MiniLED背光技术带来更"
                    "高对比度和更纯色彩表现。搭载鸿蒙系统，支持"
                    "全场景智慧互联。",
        key_metrics={"price_start_rmb": 3499,
                     "price_top_rmb": 5799,
                     "backlight": "RGB-MiniLED",
                     "sizes": ["55英寸", "75英寸"],
                     "os": "HarmonyOS",
                     "refresh_hz": 144,
                     "peak_brightness_nits": 3000,
                     "dimming_zones": "千级分区",
                     "speakers": "HUAWEI SOUND",
                     "features": ["AI画质", "鸿蒙互联",
                                  "灵犀指向遥控",
                                  "超级终端"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="MiniLED背光和鸿蒙互联可用于"
                              "机器人可视化大屏显示终端",
        deployment_ready=True,
        tags=["Vision智慧屏", "华为", "RGB-MiniLED",
              "鸿蒙电视", "55英寸", "75英寸"],
    ),
    AIProduct(
        product_id="MC-015", name="华为Pura 90标准版",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="Pura 90系列标准版，6.8英寸直屏，弦律几何设计"
                    "语言。搭载麒麟9010S芯片（非9030），第二代红枫"
                    "影像系统，5000万像素超聚光主摄。6500mAh大电池"
                    "+100W有线快充+50W无线快充。HarmonyOS 6.1，"
                    "小艺看世界、小艺时光机等AI功能。12GB+256GB"
                    "4699元起，罗兰紫/丝绒黑/雪域白三色。",
        key_metrics={"price_start_rmb": 4699,
                     "price_top_rmb": 5699,
                     "screen_inch": 6.8,
                     "screen_type": "OLED直屏",
                     "refresh_hz": "1-120Hz LTPO自适应",
                     "peak_brightness_nits": 2500,
                     "pwm_dimming_hz": 2160,
                     "chip": "麒麟9010S",
                     "performance_gain_pct": 25,
                     "ram_gb": "12GB/16GB",
                     "rom_gb": "256GB/512GB",
                     "storage_options": ["12GB+256GB 4699元",
                                         "12GB+512GB 5199元",
                                         "16GB+512GB 5699元"],
                     "rear_camera_main": "5000万像素超聚光主摄（F1.4-F4.0十档可变光圈，OIS光学防抖）",
                     "rear_camera_ultrawide": "4000万像素超广角摄像头（F2.2光圈）",
                     "rear_camera_telephoto": "1200万像素潜望式长焦摄像头（F3.4光圈，OIS光学防抖，5倍光学变焦）",
                     "rear_camera_spectrum": "第二代红枫原色摄像头",
                     "rear_camera_count": 4,
                     "front_camera_main": "1300万像素超广角摄像头（F2.0光圈，自动对焦）",
                     "front_camera_count": 1,
                     "photo_features": ["AI色彩引擎", "AI姿势推荐",
                                        "3D动态照片", "小艺看世界",
                                        "小艺时光机"],
                     "battery_mah": 6500,
                     "wired_charge_w": 100,
                     "wireless_charge_w": 50,
                     "weight_g": 208,
                     "back_material": "玻璃",
                     "frame_material": "铝合金",
                     "waterproof": "IP68",
                     "os": "HarmonyOS 6.1",
                     "ai_features": ["小艺看世界", "小艺时光机",
                                    "AI扩图", "AI消除"],
                     "colors": ["罗兰紫", "丝绒黑", "雪域白"],
                     "design": "弦律几何直屏"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="端侧AI影像能力可用于机器人视觉"
                              "识别和场景理解参考",
        deployment_ready=True,
        tags=["Pura 90", "华为", "麒麟9010S", "红枫影像",
              "HarmonyOS 6", "标准版"],
    ),
    AIProduct(
        product_id="MC-016", name="华为Pura 90 Pro",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="Pura 90 Pro，6.6英寸单挖孔直屏，粉红芭乐、"
                    "橘子汽水、椰青白、桑果黑四款配色。麒麟9030S"
                    "处理器，图像理解能力提升200%。5000万像素"
                    "超聚光主摄（1/1.28英寸大底、十档物理可变光圈）"
                    "+5000万像素超聚光微距长焦。AI色彩引擎提升43%，"
                    "光感无界主题。5499元起。",
        key_metrics={"price_start_rmb": 5499,
                     "price_top_rmb": 7499,
                     "screen_inch": 6.6,
                     "screen_type": "OLED单挖孔直屏",
                     "refresh_hz": "1-120Hz LTPO自适应",
                     "peak_brightness_nits": 3000,
                     "chip": "麒麟9030S",
                     "ai_image_understanding_pct": 200,
                     "ram_gb": "12GB/16GB",
                     "rom_gb": "256GB/512GB/1TB",
                     "storage_options": ["12GB+256GB 5499元",
                                         "12GB+512GB 5999元",
                                         "16GB+512GB 6499元",
                                         "16GB+1TB 7499元"],
                     "rear_camera_main": "5000万像素超聚光主摄（1/1.28英寸大底，F1.4-F4.0十档物理可变光圈，OIS光学防抖）",
                     "rear_camera_ultrawide": "4000万像素超广角摄像头（F2.2光圈）",
                     "rear_camera_telephoto": "5000万像素超聚光微距长焦摄像头（F2.1光圈，OIS光学防抖，3.5倍光学变焦）",
                     "rear_camera_spectrum": "第二代红枫原色摄像头",
                     "rear_camera_count": 4,
                     "front_camera_main": "1300万像素超广角摄像头（F2.0光圈，自动对焦）",
                     "front_camera_count": 1,
                     "ai_image_boost_pct": 43,
                     "photo_features": ["AI色彩引擎", "光感无界主题",
                                        "AI姿势推荐", "3D动态照片",
                                        "小艺看世界"],
                     "battery_mah": 6000,
                     "wired_charge_w": 66,
                     "wireless_charge_w": 50,
                     "weight_g": 220,
                     "back_material": "玻璃",
                     "frame_material": "铝合金",
                     "waterproof": "IP68",
                     "os": "HarmonyOS 6.1",
                     "colors": ["粉红芭乐", "橘子汽水",
                                "椰青白", "桑果黑"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="十档可变光圈技术可迁移至机器人"
                              "视觉感知系统的光照自适应",
        deployment_ready=True,
        tags=["Pura 90 Pro", "华为", "麒麟9030S",
              "可变光圈", "AI色彩", "Pro"],
    ),
    AIProduct(
        product_id="MC-017", name="华为Pura 90 Pro Max",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="Pura 90系列顶配，6.9英寸超大屏，橘子海、"
                    "霞光紫、翡翠湖、晨曦金、曜石黑五款配色。"
                    "搭载1/1.28英寸超大底2亿像素长焦传感器，"
                    "支持20倍光学品质高清视频。主摄支持LOFIC"
                    "高动态技术，RYYB滤镜。抗反光耐刮昆仑玻璃，"
                    "屏幕反光下降70%。6499元起。",
        key_metrics={"price_start_rmb": 6499,
                     "price_top_rmb": 8499,
                     "screen_inch": 6.9,
                     "screen_type": "OLED曲面屏",
                     "refresh_hz": "1-120Hz LTPO自适应",
                     "peak_brightness_nits": 4000,
                     "chip": "麒麟9030S",
                     "ram_gb": "12GB/16GB",
                     "rom_gb": "256GB/512GB/1TB",
                     "storage_options": ["12GB+256GB 6499元",
                                         "12GB+512GB 6999元",
                                         "16GB+512GB 7499元",
                                         "16GB+1TB 8499元"],
                     "rear_camera_main": "5000万像素超聚光主摄（1/1.28英寸大底，LOFIC高动态技术+RYYB滤镜，F1.4-F4.0十档可变光圈，OIS光学防抖）",
                     "rear_camera_ultrawide": "4000万像素超广角摄像头（F2.2光圈）",
                     "rear_camera_telephoto": "2亿像素超聚光长焦摄像头（1/1.28英寸大底，F2.6光圈，OIS光学防抖，支持20倍光学品质高清视频）",
                     "rear_camera_spectrum": "第二代红枫原色摄像头",
                     "rear_camera_count": 4,
                     "front_camera_main": "1300万像素超广角摄像头（F2.0光圈，自动对焦）",
                     "front_camera_count": 1,
                     "photo_features": ["LOFIC高动态", "RYYB高感光",
                                        "AI色彩引擎43%", "抗反光昆仑玻璃",
                                        "AI姿势推荐", "3D动态照片"],
                     "glass": "抗反光昆仑玻璃",
                     "glass_reflection_cut_pct": 70,
                     "battery_mah": 6000,
                     "wired_charge_w": 100,
                     "wireless_charge_w": 80,
                     "weight_g": 235,
                     "back_material": "素皮/玻璃",
                     "frame_material": "铝合金",
                     "waterproof": "IP68",
                     "os": "HarmonyOS 6.1",
                     "colors": ["橘子海", "霞光紫", "翡翠湖",
                                "晨曦金", "曜石黑"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="2亿像素长焦和LOFIC高动态技术"
                              "可参考用于机器人远距离精细识别",
        deployment_ready=True,
        tags=["Pura 90 Pro Max", "华为", "2亿像素长焦",
              "LOFIC", "昆仑玻璃", "Pro Max"],
    ),
    AIProduct(
        product_id="MC-018", name="华为Mate 80 RS非凡大师",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="Mate 80系列顶级超高端版本，RS非凡大师"
                    "定位。6.9英寸双层OLED灵珑屏，第三代玄武"
                    "钢化昆仑玻璃，高亮钛合金中框。搭载麒麟"
                    "9030 Pro旗舰芯片，20GB超大内存。五摄"
                    "红枫影像（含超长焦），6000mAh电池+100W"
                    "有线+80W无线快充。槿紫/皓白/玄黑三色，"
                    "11999元起。",
        key_metrics={"price_start_rmb": 11999,
                     "price_top_rmb": 12999,
                     "series": "Mate 80",
                     "tier": "RS非凡大师",
                     "chip": "麒麟9030 Pro",
                     "performance_gain_pct": 42,
                     "screen_inch": 6.9,
                     "screen_type": "双层OLED灵珑屏",
                     "refresh_hz": "1-120Hz LTPO自适应",
                     "peak_brightness_nits": 8000,
                     "glass": "第三代玄武钢化昆仑玻璃",
                     "frame_material": "高亮钛合金中框",
                     "back_material": "陶瓷/素皮",
                     "ram_gb": "20GB",
                     "rom_gb": "512GB/1TB",
                     "storage_options": ["20GB+512GB 11999元",
                                         "20GB+1TB 12999元"],
                     "rear_camera_main": "5000万像素超聚光主摄（F1.4-F4.0十档可变光圈，OIS光学防抖，RYYB传感器）",
                     "rear_camera_ultrawide": "4000万像素超广角摄像头（F2.2光圈）",
                     "rear_camera_telephoto": "5000万像素超聚光微距长焦摄像头（OIS光学防抖）",
                     "rear_camera_periscope": "4800万像素超长焦摄像头（OIS光学防抖，支持100倍数字变焦）",
                     "rear_camera_spectrum": "第二代红枫原色摄像头",
                     "rear_camera_count": 5,
                     "front_camera_main": "1300万像素超广角摄像头（F2.0光圈，自动对焦）",
                     "front_camera_depth": "3D深感摄像头",
                     "front_camera_count": 2,
                     "photo_features": ["第二代红枫影像", "AI扩图40%",
                                        "AI光影引擎", "动感摇拍",
                                        "电影效果"],
                     "battery_mah": 6000,
                     "wired_charge_w": 100,
                     "wireless_charge_w": 80,
                     "reverse_charge_w": 10,
                     "waterproof": "IP68 6米抗水 + IP69K高温高压喷水",
                     "satellite": "天通卫星通话+北斗卫星消息",
                     "offline_comm": "2.4GHz无网通信（最远7公里）",
                     "outdoor_mode": "户外探索模式（13天极限续航+摩斯码警报）",
                     "os": "HarmonyOS 6",
                     "ai": "鸿蒙AI（小艺+隔空传送+魔法表情）",
                     "colors": ["槿紫", "皓白", "玄黑"],
                     "positioning": "超高端商务旗舰"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="高端工艺材质和结构设计可为"
                              "机器人外壳制造提供参考",
        deployment_ready=True,
        tags=["Mate 80 RS", "华为", "非凡大师",
              "麒麟9030 Pro", "20GB", "超高端", "RS"],
    ),
    AIProduct(
        product_id="MC-019", name="华为Mate 80 Pro Max旗舰手机",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="Mate 80系列顶配Pro Max，6.9英寸超透亮"
                    "灵珑屏（峰值8000nit），全金属玄武架构+"
                    "第二代昆仑玻璃。搭载麒麟9030 Pro旗舰芯片，"
                    "整机性能提升42%。第二代红枫五摄，6000mAh"
                    "电池+100W快充。支持卫星通信、户外探索模式，"
                    "HarmonyOS 6。7999元起，极昼金/极光青/"
                    "极地银/极夜黑四色。",
        key_metrics={"price_start_rmb": 7999,
                     "price_top_rmb": 8999,
                     "series": "Mate 80",
                     "tier": "Pro Max",
                     "chip": "麒麟9030 Pro",
                     "performance_gain_pct": 42,
                     "screen_inch": 6.9,
                     "screen_type": "超透亮灵珑屏（双层OLED）",
                     "refresh_hz": "1-120Hz LTPO自适应",
                     "peak_brightness_nits": 8000,
                     "glass": "第二代昆仑玻璃",
                     "architecture": "全金属玄武架构",
                     "ram_gb": "16GB",
                     "rom_gb": "512GB/1TB",
                     "storage_options": ["16GB+512GB 7999元",
                                         "16GB+1TB 8999元"],
                     "rear_camera_main": "5000万像素超聚光主摄（F1.4-F4.0十档可变光圈，OIS光学防抖，RYYB传感器）",
                     "rear_camera_ultrawide": "4000万像素超广角摄像头（F2.2光圈）",
                     "rear_camera_telephoto": "5000万像素超聚光微距长焦摄像头（OIS光学防抖）",
                     "rear_camera_periscope": "4800万像素超长焦摄像头（OIS光学防抖）",
                     "rear_camera_spectrum": "第二代红枫原色摄像头",
                     "rear_camera_count": 5,
                     "front_camera_main": "1300万像素超广角摄像头（F2.0光圈，自动对焦）",
                     "front_camera_depth": "3D深感摄像头",
                     "front_camera_count": 2,
                     "photo_features": ["第二代红枫影像", "AI扩图40%",
                                        "AI光影引擎", "动感摇拍",
                                        "电影效果"],
                     "battery_mah": 6000,
                     "wired_charge_w": 100,
                     "wireless_charge_w": 80,
                     "reverse_charge_w": 10,
                     "weight_g": 230,
                     "waterproof": "IP68 6米抗水 + IP69K高温高压喷水",
                     "satellite": "北斗卫星消息+天通卫星通话",
                     "offline_comm": "2.4GHz无网通信（最远7公里）",
                     "outdoor_mode": "户外探索模式（极限续航13天+摩斯码警报+33h熄屏导航）",
                     "os": "HarmonyOS 6",
                     "ai": "鸿蒙AI（小艺+隔空传送+魔法表情）",
                     "colors": ["极昼金", "极光青",
                                "极地银", "极夜黑"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="卫星通信能力可作为机器人"
                              "远程控制的备选通信链路",
        deployment_ready=True,
        tags=["Mate 80 Pro Max", "华为", "麒麟9030 Pro",
              "卫星通信", "8000nit", "商务旗舰", "Pro Max"],
    ),
    AIProduct(
        product_id="MC-020", name="华为畅享90 Pro Max千元长续航",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="畅享系列顶配，6.84英寸OLED直屏，搭载"
                    "麒麟8000芯片，运行HarmonyOS 6.0。8500mAh"
                    "巨鲸电池+40W Turbo快充，主打超长续航。"
                    "5000万像素RYYB超感知主摄，星闪E1.0。"
                    "8GB+128GB 1699元起，飞天青/晨曦金/"
                    "雪域白/曜金黑四色。定位入门级市场。",
        key_metrics={"price_start_rmb": 1699,
                     "price_top_rmb": 2399,
                     "series": "畅享90",
                     "tier": "Pro Max",
                     "chip": "麒麟8000",
                     "screen_inch": 6.84,
                     "screen_type": "OLED直屏",
                     "refresh_hz": 120,
                     "peak_brightness_nits": 1500,
                     "ram_gb": "8GB",
                     "rom_gb": "128GB/256GB/512GB",
                     "storage_options": ["8GB+128GB 1699元",
                                         "8GB+256GB 1999元",
                                         "8GB+512GB 2399元"],
                     "rear_camera_main": "5000万像素RYYB超感知主摄（F1.8光圈）",
                     "rear_camera_ultrawide": "200万像素景深摄像头",
                     "rear_camera_macro": "200万像素微距摄像头",
                     "rear_camera_count": 3,
                     "front_camera_main": "800万像素前置摄像头（F2.0光圈）",
                     "front_camera_count": 1,
                     "battery_mah": 8500,
                     "wired_charge_w": 40,
                     "reverse_charge_w": 5,
                     "nearlink": "E1.0",
                     "weight_g": 214,
                     "back_material": "玻璃",
                     "frame_material": "塑料",
                     "waterproof": "IP53生活防泼溅",
                     "os": "HarmonyOS 6.0",
                     "colors": ["飞天青", "晨曦金",
                                "雪域白", "曜金黑"],
                     "positioning": "千元长续航"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="8500mAh超大电池方案可参考"
                              "机器人移动终端的续航设计",
        deployment_ready=True,
        tags=["畅享90 Pro Max", "华为", "麒麟8000",
              "8500mAh", "千元机", "Pro Max"],
    ),
    AIProduct(
        product_id="MC-021", name="华为nova 16 Pro人像旗舰",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="nova 16系列Pro版，6.84英寸1.5K LTPO屏"
                    "（峰值6000nit），7.1mm航空级铝合金中框+"
                    "昆仑玻璃。搭载麒麟9010S芯片，2亿红枫主摄+"
                    "5000万潜望长焦+5000万超广角，前置5000万"
                    "红枫人像。7000mAh巨鲸电池+100W快充。"
                    "12GB+256GB 3899元起，天际白/幻彩贝母/"
                    "晴空蓝/星空黑四色。",
        key_metrics={"price_start_rmb": 3899,
                     "price_top_rmb": 4999,
                     "series": "nova 16",
                     "tier": "Pro",
                     "chip": "麒麟9010S",
                     "screen_inch": 6.84,
                     "screen_type": "1.5K LTPO OLED直屏",
                     "refresh_hz": "1-120Hz LTPO自适应",
                     "peak_brightness_nits": 6000,
                     "pwm_dimming_hz": 2160,
                     "thickness_mm": 7.1,
                     "ram_gb": "12GB",
                     "rom_gb": "256GB/512GB/1TB",
                     "storage_options": ["12GB+256GB 3899元",
                                         "12GB+512GB 4399元",
                                         "12GB+1TB 4999元"],
                     "rear_camera_main": "2亿像素红枫主摄（1/1.4英寸大底，F1.4-F4.0可变光圈，OIS光学防抖）",
                     "rear_camera_ultrawide": "5000万像素超广角摄像头（F2.2光圈）",
                     "rear_camera_telephoto": "5000万像素潜望式长焦摄像头（F2.4光圈，OIS光学防抖，3倍光学变焦）",
                     "rear_camera_spectrum": "红枫原色摄像头",
                     "rear_camera_count": 4,
                     "front_camera_main": "5000万像素红枫人像摄像头（F2.0光圈，自动对焦，AF自动对焦）",
                     "front_camera_count": 1,
                     "photo_features": ["红枫人像", "AI美颜",
                                        "夜景人像", "舞台光效",
                                        "AI扩图"],
                     "battery_mah": 7000,
                     "wired_charge_w": 100,
                     "weight_g": 205,
                     "frame_material": "航空级铝合金中框",
                     "glass": "昆仑玻璃",
                     "waterproof": "IP65生活防水",
                     "os": "HarmonyOS 6.1",
                     "ai_features": ["AI人像", "AI美颜",
                                    "魔法表情", "趣味主题"],
                     "colors": ["天际白", "幻彩贝母",
                                "晴空蓝", "星空黑"],
                     "focus": "人像拍摄",
                     "positioning": "年轻时尚旗舰"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="人像AI算法可用于机器人"
                              "人机交互中的人物识别",
        deployment_ready=True,
        tags=["nova 16 Pro", "华为", "人像旗舰",
              "年轻时尚", "Pro"],
    ),
    AIProduct(
        product_id="MC-022", name="华为nova 16 Ultra顶配人像",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="nova 16系列顶配Ultra版，6.84英寸LTPO屏"
                    "（6000nit），7.1mm素皮+玻璃拼接机身，昆仑玻璃，"
                    "IP68/IP69防水。搭载麒麟9010S芯片，2亿RYYB"
                    "超大底主摄+5000万潜望长焦+5000万超广角，"
                    "前置5000万红枫人像。7000mAh电池+100W有线+"
                    "50W无线，天通+北斗双卫星通信。12GB+256GB"
                    "4699元起，晴空蓝/天际白/星空黑三色。",
        key_metrics={"price_start_rmb": 4699,
                     "price_top_rmb": 5799,
                     "series": "nova 16",
                     "tier": "Ultra",
                     "chip": "麒麟9010S",
                     "screen_inch": 6.84,
                     "screen_type": "LTPO OLED曲面屏",
                     "refresh_hz": "1-120Hz LTPO自适应",
                     "peak_brightness_nits": 6000,
                     "pwm_dimming_hz": 2160,
                     "thickness_mm": 7.1,
                     "design": "素皮+玻璃拼接机身",
                     "ram_gb": "12GB",
                     "rom_gb": "256GB/512GB/1TB",
                     "storage_options": ["12GB+256GB 4699元",
                                         "12GB+512GB 5199元",
                                         "12GB+1TB 5799元"],
                     "rear_camera_main": "2亿像素RYYB超大底主摄（1/1.4英寸大底，F1.4-F4.0可变光圈，OIS光学防抖）",
                     "rear_camera_ultrawide": "5000万像素超广角摄像头（F2.2光圈）",
                     "rear_camera_telephoto": "5000万像素潜望式长焦摄像头（F2.4光圈，OIS光学防抖，3倍光学变焦）",
                     "rear_camera_spectrum": "红枫原色摄像头",
                     "rear_camera_count": 4,
                     "front_camera_main": "5000万像素红枫人像摄像头（F2.0光圈，自动对焦）",
                     "front_camera_count": 1,
                     "photo_features": ["前后双红枫影像", "AI人像",
                                        "AI美颜", "舞台光效",
                                        "AI扩图"],
                     "battery_mah": 7000,
                     "wired_charge_w": 100,
                     "wireless_charge_w": 50,
                     "reverse_charge_w": 10,
                     "weight_g": 210,
                     "glass": "昆仑玻璃",
                     "waterproof": "IP68/IP69K",
                     "satellite": "天通+北斗双卫星通信",
                     "os": "HarmonyOS 6.1",
                     "colors": ["晴空蓝", "天际白", "星空黑"],
                     "focus": "旗舰人像",
                     "camera": "前后双红枫影像"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="人像识别和美颜算法可"
                              "迁移至机器人情感交互",
        deployment_ready=True,
        tags=["nova 16 Ultra", "华为", "顶配人像",
              "AI影像", "Ultra"],
    ),
    AIProduct(
        product_id="MC-023", name="小米18 Pro骁龙8E6旗舰",
        category=AICategory.MOBILE_COMPUTER,
        organization="小米", country="中国",
        description="小米18系列Pro款旗舰，2026年9月发布。"
                    "全球首发高通骁龙8 Elite Gen6（骁龙8E6），"
                    "台积电N2P改良版2nm GAA工艺，晶体管密度"
                    "较3nm提升30%，同等性能功耗降低36%。"
                    "自研第三代Oryon CPU架构，2颗超大核+3颗"
                    "性能核+3颗能效核三丛集八核，共享16MB L2"
                    "缓存，Adreno 845 GPU，LPDDR5X内存+UFS 5.0"
                    "存储。6.3英寸2K LTPO超级像素极窄四等边"
                    "直屏（LIPO工艺），三星M14发光材料，"
                    "峰值亮度超4000nit，新一代防窥技术。"
                    "妙享背屏（背部横向副屏）保留升级，支持"
                    "不点亮主屏查看信息概要、快捷支付、设备"
                    "控制。全系新增实体AI按键，一键唤醒超级"
                    "小爱，澎湃OS 4完善Agent跨应用能力。"
                    "徕卡双2亿像素影像：2亿像素超大底主摄+"
                    "2亿像素潜望长焦+超广角，徕卡联合调校。"
                    "7000mAh+大电池，100W有线闪充+无线充电。"
                    "配色方案更大胆，含光致变色特殊版。",
        key_metrics={"price_start_rmb": 5499,
                     "series": "小米18",
                     "tier": "Pro",
                     "chip": "骁龙8 Elite Gen6（骁龙8E6）",
                     "process_nm": 2,
                     "process_detail": "台积电N2P改良版2nm GAA",
                     "cpu_arch": "第三代自研Oryon 2+3+3八核",
                     "l2_cache_mb": 16,
                     "gpu": "Adreno 845",
                     "ram": "LPDDR5X",
                     "storage": "UFS 5.0",
                     "screen_inch": 6.3,
                     "screen_type": "2K LTPO极窄四等边直屏",
                     "screen_tech": "LIPO工艺+超级像素排列+新一代防窥",
                     "screen_material": "三星M14",
                     "peak_brightness_nits": 4000,
                     "back_screen": "妙享背屏（横向副屏）",
                     "ai_key": "实体AI按键+超级小爱Agent",
                     "battery_mah": 7000,
                     "wired_charge_w": 100,
                     "wireless_charge": True,
                     "camera_brand": "徕卡",
                     "main_camera_mp": 200,
                     "main_camera_desc": "2亿像素超大底主摄",
                     "telephoto_mp": 200,
                     "telephoto_desc": "2亿像素潜望式长焦",
                     "ultrawide": "超广角镜头",
                     "camera_count": 3,
                     "os": "澎湃OS 4",
                     "color_tech": "光致变色后盖（特殊版）",
                     "release_date": "2026年9月"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="2nm旗舰芯片端侧AI算力"
                              "可运行机器人本地大模型推理，"
                              "妙享背屏可作为机器人辅助交互参考",
        deployment_ready=False,
        tags=["小米18 Pro", "骁龙8E6", "2nm", "双2亿徕卡",
              "妙享背屏", "AI按键", "7000mAh", "澎湃OS 4", "Pro"],
    ),
    AIProduct(
        product_id="MC-024", name="小米18 Pro Max双2亿徕卡影像",
        category=AICategory.MOBILE_COMPUTER,
        organization="小米", country="中国",
        description="小米18系列顶配Pro Max，2026年9月与Pro"
                    "同期发布。独享高通骁龙8 Elite Gen6 Pro"
                    "旗舰芯片（台积电2nm），GPU频率和缓存升级，"
                    "图形性能更强，18MB专属图形缓存。徕卡双2亿"
                    "像素三摄系统：2亿像素LOFIC超大底主摄+"
                    "2亿像素大底潜望长焦+超广角，全焦段徕卡"
                    "联合调校。8000mAh级别超大电池，100W有线"
                    "闪充+无线充电。妙享背屏升级+实体AI按键，"
                    "2K级超清直屏（大R角极窄四等边），新一代"
                    "防窥技术。澎湃OS 4首发，超级小爱Agent能力"
                    "强化，跨应用自动化任务。",
        key_metrics={"price_start_rmb": 6499,
                     "series": "小米18",
                     "tier": "Pro Max",
                     "chip": "骁龙8 Elite Gen6 Pro",
                     "process_nm": 2,
                     "process_detail": "台积电2nm",
                     "gpu_cache_mb": 18,
                     "gpu": "增强版Adreno",
                     "ram": "LPDDR5X",
                     "storage": "UFS 5.0",
                     "screen": "2K LTPO极窄四等边直屏",
                     "screen_tech": "超级像素排列+新一代防窥+大R角",
                     "screen_material": "三星M14",
                     "peak_brightness_nits": 4000,
                     "back_screen": "妙享背屏（升级款）",
                     "ai_key": "实体AI按键+超级小爱Agent",
                     "camera_brand": "徕卡",
                     "main_camera_mp": 200,
                     "main_camera_tech": "LOFIC超大底",
                     "telephoto_mp": 200,
                     "telephoto_type": "大底潜望长焦",
                     "ultrawide": "超广角镜头",
                     "camera_count": 3,
                     "battery_mah": 8000,
                     "wired_charge_w": 100,
                     "wireless_charge": True,
                     "os": "澎湃OS 4",
                     "release_date": "2026年9月"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="双2亿像素+LOFIC方案可为"
                              "机器人高精度视觉模组提供参考，"
                              "8000mAh电池方案为机器人续航设计提供借鉴",
        deployment_ready=False,
        tags=["小米18 Pro Max", "徕卡", "双2亿",
              "LOFIC", "8000mAh", "骁龙8E6 Pro", "Pro Max", "妙享背屏"],
    ),
    AIProduct(
        product_id="MC-025", name="苹果iPhone 18 Pro",
        category=AICategory.MOBILE_COMPUTER,
        organization="Apple", country="美国",
        description="苹果2026年秋季旗舰（9月9日发布），搭载"
                    "全球首发台积电2nm工艺A20 Pro芯片，采用"
                    "全新WMCM晶圆级多芯片模块封装，CPU/GPU/NPU"
                    "集成于同一载板。性能较A19 Pro提升15%，"
                    "功耗降低25-30%，AI算力翻倍。全系标配12GB "
                    "LPDDR5X运行内存。6.3英寸LTPO+高刷屏，"
                    "灵动岛面积缩减35%，屏下Face ID正式落地，"
                    "屏占比大幅提升。4800万像素主摄首次搭载"
                    "机械物理可变光圈，支持f/1.4至f/4.0十档"
                    "无级调节，暗光进光量提升40%。前置摄像头"
                    "升级至2400万像素。通信全面换装苹果自研"
                    "第三代C2 5G基带（彻底告别高通），弱网信号"
                    "强度提升30-40%，电梯/高铁/地下室掉线率"
                    "大幅下降；支持卫星5G直连功能，偏远山区"
                    "或海上也能上网传图。N2无线芯片原生支持"
                    "Wi-Fi 7+蓝牙6.0。电池容量超5000mAh，"
                    "充电功率约40W。一体化磨砂后盖取代双色拼接，"
                    "相机按键简化结构。预装iOS 27，新版Siri"
                    "重构交互逻辑，端侧Apple Intelligence"
                    "深度整合。配色新增深樱桃红（Dark Cherry）"
                    "年度主打色。存储最高2TB。",
        key_metrics={"price_start_rmb": 7999,
                     "price_top_rmb": 12999,
                     "series": "iPhone 18",
                     "tier": "Pro",
                     "chip": "A20 Pro",
                     "process_nm": 2,
                     "process_detail": "台积电首代2nm（N2）",
                     "package": "WMCM晶圆级多芯片模块封装",
                     "performance_gain_pct": 15,
                     "power_save_pct": 30,
                     "ai_compute": "NPU翻倍",
                     "ram_gb": 12,
                     "ram_type": "LPDDR5X",
                     "storage_max_tb": 2,
                     "screen_inch": 6.3,
                     "screen_type": "LTPO+ OLED高刷屏",
                     "dynamic_island": "缩小35%（屏下Face ID）",
                     "face_id": "屏下Face ID",
                     "modem": "苹果自研第三代C2 5G基带",
                     "modem_signal_gain": "弱网信号提升30-40%",
                     "satellite": "卫星5G直连（上网+传图）",
                     "wireless": "N2芯片（Wi-Fi 7+蓝牙6.0）",
                     "main_camera_mp": 4800,
                     "camera_aperture": "物理可变光圈f/1.4-f/4.0十档无级",
                     "camera_low_light_gain": "进光量提升40%",
                     "front_camera_mp": 2400,
                     "camera_key_simplified": True,
                     "battery_mah": "5000+",
                     "charge_w": 40,
                     "back_design": "一体化磨砂后盖（取消双色拼接）",
                     "os": "iOS 27",
                     "ai": "Apple Intelligence（端侧完整）+新版Siri",
                     "special_color": "深樱桃红（Dark Cherry）",
                     "colors": ["深樱桃红", "深空灰", "浅蓝", "银色"],
                     "release_date": "2026年9月9日"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="A20 Pro神经网络引擎可为"
                              "机器人端侧AI推理提供算力参考，"
                              "C2自研基带和卫星5G为机器人远距通信提供方案",
        deployment_ready=False,
        tags=["iPhone 18 Pro", "Apple", "A20 Pro", "2nm",
              "可变光圈", "C2基带", "卫星5G", "屏下Face ID",
              "Wi-Fi 7", "iOS 27", "Pro"],
    ),
    AIProduct(
        product_id="MC-026", name="苹果iPhone 18 Pro Max顶配",
        category=AICategory.MOBILE_COMPUTER,
        organization="Apple", country="美国",
        description="iPhone 18系列大屏顶配（6.9英寸），与Pro"
                    "同期9月9日发布。搭载A20 Pro 2nm芯片+12GB "
                    "LPDDR5X内存，独享6倍光学潜望长焦镜头，"
                    "4800万物理可变光圈主摄（f/1.4-f/4.0十档）+"
                    "超广角+6倍潜望长焦三摄组合。前置2400万像素。"
                    "电池容量较前代提升近10%（超5000mAh），为"
                    "容纳更大电芯机身厚度小幅增加。自研C2基带+"
                    "卫星5G+Wi-Fi 7+蓝牙6.0通信全家桶。灵动岛"
                    "缩小35%，屏下Face ID，一体化磨砂钛金属后盖。"
                    "钛合金中框，改进铝提炼工艺提升耐用性。"
                    "iOS 27+完整Apple Intelligence端侧AI。"
                    "存储最高2TB。40W有线充电。深樱桃红主打色。",
        key_metrics={"price_start_rmb": 8999,
                     "price_top_rmb": 14999,
                     "series": "iPhone 18",
                     "tier": "Pro Max",
                     "chip": "A20 Pro",
                     "process_nm": 2,
                     "ram_gb": 12,
                     "ram_type": "LPDDR5X",
                     "storage_max_tb": 2,
                     "screen_inch": 6.9,
                     "screen_type": "LTPO+ OLED高刷屏",
                     "dynamic_island": "缩小35%（屏下Face ID）",
                     "modem": "苹果自研C2 5G基带",
                     "satellite": "卫星5G直连",
                     "wireless": "Wi-Fi 7+蓝牙6.0（N2芯片）",
                     "main_camera_mp": 4800,
                     "camera_aperture": "物理可变光圈f/1.4-f/4.0十档",
                     "telephoto_x": 6,
                     "telephoto_type": "6倍光学潜望长焦（Pro Max独占）",
                     "ultrawide": "超广角镜头",
                     "camera_count": 3,
                     "front_camera_mp": 2400,
                     "battery_gain_pct": 10,
                     "battery_mah": "5000+",
                     "charge_w": 40,
                     "frame": "钛合金中框（改进铝工艺）",
                     "back_design": "一体化磨砂后盖",
                     "os": "iOS 27",
                     "ai": "Apple Intelligence+新版Siri",
                     "special_color": "深樱桃红",
                     "release_date": "2026年9月9日"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="钛合金工艺和6倍潜望长焦"
                              "技术可参考机器人结构设计与远距视觉方案",
        deployment_ready=False,
        tags=["iPhone 18 Pro Max", "Apple", "A20 Pro", "2nm",
              "钛合金", "6倍潜望长焦", "Apple Intelligence",
              "卫星5G", "Pro Max"],
    ),
    AIProduct(
        product_id="MC-027", name="苹果iPhone Ultra首款折叠屏",
        category=AICategory.MOBILE_COMPUTER,
        organization="Apple", country="美国",
        description="苹果首款横向书本式内折折叠屏手机（iPhone "
                    "Fold/Ultra），或命名iPhone Ultra，与18 Pro"
                    "系列同台亮相但上市可能延至2027年初。外屏"
                    "约5.5英寸，展开后7.8英寸内屏（三星显示"
                    "三年独家供应协议）。折叠状态厚度约9.5mm，"
                    "展开最薄处仅4.5mm。钛合金机身，铰链部分"
                    "使用液态金属，折痕深度控制在0.15mm以内"
                    "（几乎肉眼不可见），铰链折叠角度<2.5度，"
                    "接近无缝体验。为节省空间取消Face ID，"
                    "改用电源键集成侧边Touch ID。后置双摄"
                    "（较Pro系列三摄缩减）。核心配置搭载A20 "
                    "Pro芯片+12GB内存，运行专门适配折叠屏形态"
                    "的iOS 27系统，支持应用分屏和多窗口并行"
                    "操作。电池容量5800mAh。国行起售价预计"
                    "14999元左右（1999-2500美元），顶配版本"
                    "突破2万元。",
        key_metrics={"price_start_rmb": 14999,
                     "price_top_rmb": 20000,
                     "series": "iPhone Ultra",
                     "form_factor": "横向书本式内折",
                     "outer_screen_inch": 5.5,
                     "inner_screen_inch": 7.8,
                     "screen_supplier": "三星显示（三年独家）",
                     "thickness_folded_mm": 9.5,
                     "thickness_open_mm": 4.5,
                     "frame": "钛合金机身",
                     "hinge": "液态金属铰链",
                     "fold_crease_mm": 0.15,
                     "hinge_angle_deg": 2.5,
                     "chip": "A20 Pro",
                     "process_nm": 2,
                     "ram_gb": 12,
                     "biometric": "侧边Touch ID（电源键集成，取消Face ID）",
                     "rear_camera_count": 2,
                     "battery_mah": 5800,
                     "os": "iOS 27（折叠屏专属适配）",
                     "os_features": ["应用分屏", "多窗口并行"],
                     "price_usd": "1999-2500",
                     "release_date": "2026年9月发布/2027年初上市"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="折叠屏铰链和柔性显示"
                              "技术可用于机器人可变形"
                              "交互界面设计，液态金属铰链"
                              "为机器人关节材料提供参考",
        deployment_ready=False,
        tags=["iPhone Ultra", "Apple", "折叠屏",
              "钛合金", "Touch ID", "液态金属铰链",
              "A20 Pro", "史上最贵iPhone"],
    ),
    AIProduct(
        product_id="MC-028", name="华为MateBook 14鸿蒙版",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="华为MateBook 14鸿蒙版，搭载麒麟X90处理器"
                    "（40TOPS NPU），鸿蒙电脑操作系统，与手机"
                    "平板生态无缝流转。14.2英寸2.8K OLED触控屏"
                    "（2880×1920/120Hz），70Wh电池21小时续航，"
                    "100W快充。24GB内存起步，支持小艺智能助手、"
                    "AI文档处理。原野绿/深空灰/樱粉金，6299元起。",
        key_metrics={"price_start_rmb": 6299,
                     "price_top_rmb": 8599,
                     "series": "MateBook 14",
                     "processor": "麒麟X90",
                     "npu_tops": 40,
                     "os": "HarmonyOS PC",
                     "screen_inch": 14.2,
                     "resolution": "2880x1920",
                     "refresh_hz": 120,
                     "ram_gb": "16GB/24GB/32GB",
                     "rom_gb": "512GB/1TB",
                     "storage_options": ["16GB+512GB 6299元",
                                         "24GB+512GB 6599元",
                                         "24GB+1TB 7599元",
                                         "32GB+1TB 8599元"],
                     "battery_wh": 70,
                     "battery_h": 21,
                     "charge_w": 100,
                     "colors": ["原野绿", "深空灰", "樱粉金"],
                     "features": ["多屏协同", "AI文档",
                                  "小艺助手", "OLED触控屏"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="鸿蒙PC端可作为机器人"
                              "上位机控制和编程终端",
        deployment_ready=True,
        tags=["MateBook 14", "华为", "鸿蒙电脑",
              "多屏协同", "AI PC"],
    ),
    AIProduct(
        product_id="MC-029", name="苹果MacBook Air M5 AI本",
        category=AICategory.MOBILE_COMPUTER,
        organization="Apple", country="美国",
        description="MacBook Air搭载M5芯片，速度较M1提升"
                    "9.5倍、较M4提升4倍。每个GPU核心内置"
                    "神经网络加速器，AI任务处理效率极高。"
                    "13/15英寸两款尺寸，1.23kg超轻机身，"
                    "18小时续航。16GB统一内存+512GB起步。"
                    "macOS Tahoe Liquid Glass设计。"
                    "9999元起，支持Apple Intelligence。"
                    "天蓝色、银色、星光色、午夜色四色。",
        key_metrics={"price_start_rmb": 9999,
                     "chip": "M5",
                     "speed_vs_m1": "9.5倍",
                     "speed_vs_m4": "4倍",
                     "sizes": ["13英寸", "15英寸"],
                     "weight_kg": 1.23,
                     "battery_hours": 18,
                     "ram_start_gb": 16,
                     "storage_start_gb": 512,
                     "os": "macOS Tahoe",
                     "colors": ["天蓝色", "银色",
                                "星光色", "午夜色"],
                     "ai": "Apple Intelligence"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="M5芯片神经网络引擎可"
                              "本地运行大模型，适合作为"
                              "机器人开发和调试工作站",
        deployment_ready=True,
        tags=["MacBook Air", "Apple", "M5",
              "18小时续航", "AI PC", "Apple Intelligence"],
    ),
    AIProduct(
        product_id="MC-030", name="华为AI眼镜",
        category=AICategory.DIGITAL_PRODUCT,
        organization="", country="中国",
        description="华为首款鸿蒙AI眼镜，整机仅35.5g，"
                    "镜腿薄至6.25mm。1200万超感光摄像头"
                    "（1/2.8英寸），业界首发HDR Vivid，"
                    "0.7秒AI闪拍。小艺助手支持视觉识别、"
                    "全双工对话、精准指向问答（准确率90%）、"
                    "卡路里识别、扫码支付。12小时续航，"
                    "磁吸快充。钛银灰/摩登黑2499元，"
                    "流光银2899元。",
        key_metrics={"price_start_rmb": 2499,
                     "price_top_rmb": 2899,
                     "weight_g": 35.5,
                     "thickness_mm": 6.25,
                     "camera_mp": 12,
                     "camera_sensor": "1/2.8英寸",
                     "hdr": "HDR Vivid",
                     "ai_shutter_sec": 0.7,
                     "battery_hours": 12,
                     "charging": "磁吸快充",
                     "features": ["HDR Vivid", "AI闪拍",
                                  "小艺视觉识别", "扫码支付",
                                  "全双工对话", "卡路里识别",
                                  "精准指向问答"],
                     "pointing_accuracy_pct": 90,
                     "colors": ["钛银灰", "摩登黑", "流光银"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="第一视角摄像头和视觉识别"
                              "可作为机器人远程操控和"
                              "AR交互参考方案",
        deployment_ready=True,
        tags=["华为AI眼镜", "鸿蒙", "HDR Vivid",
              "35.5g", "小艺", "智能眼镜"],
    ),
    AIProduct(
        product_id="MC-031", name="华为MatePad Pro Max旗舰平板",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="13.2英寸3K柔性OLED屏，云隼架构"
                    "全金属机身薄至4.7mm轻至499g。"
                    "麒麟T93 Pro芯片，性能较上代提升45%。"
                    "高低分频六扬声器，鸿蒙双桌面（平板/"
                    "电脑模式切换），支持教育空间与学而思"
                    "独家合作。凝光蓝/曜石灰/皓月银/深空灰"
                    "四色，5999元起。",
        key_metrics={"price_start_rmb": 5999,
                     "price_top_rmb": 8999,
                     "screen_inch": 13.2,
                     "screen_res": "3K OLED",
                     "refresh_hz": 144,
                     "thickness_mm": 4.7,
                     "weight_g": 499,
                     "chip": "麒麟T93 Pro",
                     "performance_gain_pct": 45,
                     "ram_gb": "12GB/16GB",
                     "rom_gb": "256GB/512GB/1TB",
                     "storage_options": ["12GB+256GB 5999元",
                                         "12GB+512GB 6999元",
                                         "16GB+512GB 7499元",
                                         "16GB+1TB 8999元"],
                     "battery_mah": 12000,
                     "charge_w": 100,
                     "speakers": 6,
                     "os": "HarmonyOS",
                     "desktop_mode": "鸿蒙双桌面",
                     "colors": ["凝光蓝", "曜石灰",
                                "皓月银", "深空灰"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="大屏+双桌面可作为机器人"
                              "调试监控和编程终端",
        deployment_ready=True,
        tags=["MatePad Pro Max", "华为", "麒麟T93 Pro",
              "3K OLED", "4.7mm", "鸿蒙双桌面"],
    ),
    AIProduct(
        product_id="MC-032", name="华为FreeClip 2典藏版耳夹耳机",
        category=AICategory.DIGITAL_PRODUCT,
        organization="", country="中国",
        description="鎏光美学设计，星海蓝与珠光银两色。"
                    "单耳机轻至5.1g，液态硅胶亲肤材质"
                    "柔软度提升25%。AI键一键唤醒，按住"
                    "即说松手即答。智感音量自适应算法，"
                    "超澎湃双擎单元。耳机盒空间提升20%，"
                    "可收纳周大福联名珠宝配饰。1499元起。",
        key_metrics={"price_start_rmb": 1499,
                     "price_top_rmb": 1799,
                     "single_weight_g": 5.1,
                     "silicone_softness_boost_pct": 25,
                     "case_space_boost_pct": 20,
                     "battery_hours": 36,
                     "anc": "智感音量自适应",
                     "features": ["AI键交互", "智感音量自适应",
                                  "双擎单元", "全双工对话",
                                  "IP54防水", "周大福联名收纳"],
                     "colors": ["星海蓝", "珠光银"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="耳夹式佩戴和AI键交互"
                              "可参考机器人语音通信终端",
        deployment_ready=True,
        tags=["FreeClip 2", "华为", "耳夹耳机",
              "AI键", "5.1g", "典藏版"],
    ),
    AIProduct(
        product_id="MC-033", name="Redmi Book 16 2026",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="16英寸2.5K超清镜面屏（2560×1600），"
                    "120Hz高刷，400nit亮度。英特尔酷睿"
                    "Ultra 5 125H，14核18线程，LPDDR5X"
                    "7467MT/s内存，最高32GB+1TB。80Wh"
                    "大电池24.8小时本地视频，100W GaN"
                    "充电器。双风扇双热管60W性能释放，"
                    "1.86kg全金属机身。AI文档处理与"
                    "跨端智联。",
        key_metrics={"screen_inch": 16,
                     "screen_res": "2560x1600",
                     "refresh_hz": 120,
                     "chip": "酷睿Ultra 5 125H",
                     "ram": "LPDDR5X 7467MT/s",
                     "battery_wh": 80,
                     "weight_kg": 1.86,
                     "performance_w": 60,
                     "charge_w": 100},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="大屏+长续航适合作为"
                              "机器人工作站和数据处理终端",
        deployment_ready=True,
        tags=["Redmi Book 16", "小米", "酷睿Ultra",
              "2.5K", "80Wh", "AI PC"],
    ),
    AIProduct(
        product_id="MC-034", name="Redmi Book Pro 2026",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="高性能AI旗舰笔记本，14/16英寸"
                    "双尺寸。酷睿Ultra X7358H处理器，"
                    "集成Arc B390核显，50 TOPS NPU，"
                    "支持XeSS 3.0。LPDDR5X 9600内存，"
                    "92/99Wh大电池接近民航上限，90W"
                    "反向快充。AI个人知识库与深度搜索，"
                    "强化本地AI算力。",
        key_metrics={"chip": "酷睿Ultra X7358H",
                     "gpu": "Arc B390",
                     "npu_tops": 50,
                     "ram": "LPDDR5X 9600",
                     "battery_wh": "92/99",
                     "reverse_charge_w": 90,
                     "ai_features": ["个人知识库",
                                     "深度搜索",
                                     "本地AI算力"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="50 TOPS NPU可运行"
                              "机器人本地AI推理任务",
        deployment_ready=True,
        tags=["Redmi Book Pro", "小米", "50TOPS NPU",
              "AI旗舰", "99Wh", "XeSS 3.0"],
    ),
    AIProduct(
        product_id="MC-035", name="小米平板7",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="11.2英寸3.2K LCD屏（3200×2136），"
                    "3:2比例，144Hz自适应刷新率，800nit"
                    "峰值亮度，12bit色深。骁龙7+ Gen3"
                    "4nm处理器。四扬声器支持杜比全景声，"
                    "8850mAh电池+45W快充。Xiaomi HyperAI"
                    "支持AI搜索、文本生成、图像生成、"
                    "会议记录。工作站模式桌面级体验。",
        key_metrics={"screen_inch": 11.2,
                     "screen_res": "3.2K",
                     "refresh_hz": 144,
                     "peak_brightness_nits": 800,
                     "chip": "骁龙7+ Gen3",
                     "process_nm": 4,
                     "battery_mah": 8850,
                     "charge_w": 45,
                     "ai": "Xiaomi HyperAI"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="高分辨率平板可作为"
                              "机器人远程监控面板",
        deployment_ready=True,
        tags=["小米平板7", "骁龙7+ Gen3", "3.2K",
              "144Hz", "HyperAI", "平板"],
    ),
    AIProduct(
        product_id="MC-036", name="苹果iPad mini 8 OLED",
        category=AICategory.MOBILE_COMPUTER,
        organization="Apple", country="美国",
        description="新一代iPad mini重大升级，首次"
                    "采用OLED显示屏。搭载A20 Pro芯片"
                    "（2nm工艺），支持Apple Intelligence。"
                    "振动式扬声器系统取消扬声器开孔，"
                    "防水设计升级。支持Apple Pencil Pro，"
                    "8.3英寸便携机身，定位口袋级生产力"
                    "工具。",
        key_metrics={"screen_inch": 8.3,
                     "display": "OLED",
                     "chip": "A20 Pro",
                     "process_nm": 2,
                     "pencil": "Apple Pencil Pro",
                     "speaker": "振动式",
                     "waterproof": True,
                     "ai": "Apple Intelligence"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="OLED+A20 Pro的便携"
                              "方案可作为机器人手持"
                              "遥控终端参考",
        deployment_ready=False,
        tags=["iPad mini 8", "Apple", "OLED",
              "A20 Pro", "2nm", "Apple Pencil Pro"],
    ),
    AIProduct(
        product_id="MC-037", name="华为Mate 80标准版",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="Mate 80系列标准款旗舰手机。6.75英寸OLED"
                    "直屏搭载第二代昆仑玻璃，麒麟9020芯片配合"
                    "HarmonyOS 6，整机性能提升。第二代红枫影像"
                    "四摄系统（5000万超光变主摄+4000万超广角+"
                    "1200万潜望长焦+红枫原色），前置1300万超广角"
                    "+3D深感。5750mAh电池+66W超级快充，支持"
                    "北斗卫星消息、2.4GHz无网通信（最远7公里）、"
                    "户外探索模式、摩斯码闪光警报、IP68/IP69防水。",
        key_metrics={"price_start_rmb": 4699,
                     "price_top_rmb": 5699,
                     "series": "Mate 80",
                     "tier": "标准版",
                     "chip": "麒麟9020",
                     "os": "HarmonyOS 6.0",
                     "screen_inch": 6.75,
                     "screen_type": "OLED直屏",
                     "refresh_hz": "1-120Hz LTPO自适应",
                     "pwm_dimming_hz": 1440,
                     "touch_sample_hz": 300,
                     "glass": "第二代昆仑玻璃",
                     "performance_gain_pct": 42,
                     "ram_gb": "12GB/16GB",
                     "rom_gb": "256GB/512GB",
                     "storage_options": ["12GB+256GB 4699元",
                                         "12GB+512GB 5199元",
                                         "16GB+512GB 5699元"],
                     "rear_camera_main": "5000万像素超光变（F1.4-F4.0十档可变光圈，OIS光学防抖，RYYB传感器）",
                     "rear_camera_ultrawide": "4000万像素超广角（F2.2光圈）",
                     "rear_camera_telephoto": "1200万像素潜望式长焦（F3.4光圈，OIS光学防抖，RYYB传感器）",
                     "rear_camera_spectrum": "第二代红枫原色摄像头",
                     "rear_camera_count": 4,
                     "front_camera_main": "1300万像素超广角（F2.0光圈，自动对焦）",
                     "front_camera_depth": "3D深感摄像头",
                     "front_camera_count": 2,
                     "flash": "后置LED闪光灯",
                     "video_max": "4K（3840×2160）AIS防抖",
                     "battery_mah": 5750,
                     "wired_charge_w": 66,
                     "reverse_charge_w": 5,
                     "wireless_charge_w": 50,
                     "weight_g": 217,
                     "back_material": "锦纤材质",
                     "frame_material": "铝合金",
                     "fingerprint": "侧面指纹识别",
                     "waterproof": "IP68 6米抗水 + IP69K高温高压喷水",
                     "satellite": "北斗卫星消息",
                     "offline_comm": "2.4GHz无网通信（最远7公里）",
                     "outdoor_mode": "户外探索模式（极限续航13天，摩斯码闪光警报）",
                     "colors": ["曜石黑", "雪域白", "云杉绿", "晨曦金"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08",
        relevance_to_robotics="卫星通信+无网通信+"
                              "户外传感器能力可为野外"
                              "机器人应急通信提供参考",
        deployment_ready=True,
        tags=["Mate 80", "麒麟9020", "第二代红枫影像",
              "第二代昆仑玻璃", "北斗卫星", "IP68",
              "潜望长焦", "HarmonyOS 6"],
    ),
    AIProduct(
        product_id="MC-038", name="华为Mate 80 Pro",
        category=AICategory.MOBILE_COMPUTER,
        organization="", country="中国",
        description="Mate 80系列Pro款旗舰。6.7英寸四曲屏，"
                    "麒麟9030芯片配合HarmonyOS 6，第二代红枫"
                    "影像升级（超聚光主摄+超聚光微距长焦+4000万"
                    "超广角+红枫原色），第九代ISP数据处理和视频"
                    "降噪大幅提升。第二代昆仑玻璃+锦纤超耐摔，"
                    "IP68 6米+IP69K防水，支持北斗卫星消息、"
                    "无网通信7公里、户外探索模式13天极限续航、"
                    "摩斯码闪光警报、鸿蒙AI。",
        key_metrics={"price_start_rmb": 5999,
                     "price_top_rmb": 7999,
                     "series": "Mate 80",
                     "tier": "Pro",
                     "chip": "麒麟9030",
                     "isp": "第九代ISP",
                     "os": "HarmonyOS 6",
                     "screen_inch": 6.7,
                     "screen_type": "OLED四曲屏",
                     "refresh_hz": "1-120Hz LTPO自适应",
                     "peak_brightness_nits": 3000,
                     "glass": "第二代昆仑玻璃",
                     "back_material": "锦纤材质（抗冲击提升5倍）",
                     "frame_material": "铝合金",
                     "drop_resistance": "整机耐摔提升20倍",
                     "performance_gain_pct": 42,
                     "ram_gb": "12GB/16GB",
                     "rom_gb": "256GB/512GB/1TB",
                     "storage_options": ["12GB+256GB 5999元",
                                         "12GB+512GB 6499元",
                                         "16GB+512GB 6999元",
                                         "16GB+1TB 7999元"],
                     "rear_camera_main": "5000万像素超聚光主摄（F1.4-F4.0十档可变光圈，OIS光学防抖，RYYB传感器）",
                     "rear_camera_ultrawide": "4000万像素超广角摄像头（F2.2光圈）",
                     "rear_camera_telephoto": "5000万像素超聚光微距长焦摄像头（OIS光学防抖，超长焦）",
                     "rear_camera_spectrum": "第二代红枫原色摄像头",
                     "rear_camera_count": 4,
                     "front_camera_main": "1300万像素超广角（F2.0光圈，自动对焦）",
                     "front_camera_depth": "3D深感摄像头",
                     "front_camera_count": 2,
                     "photo_features": ["动感摇拍", "电影效果",
                                        "AI扩图", "AI光影引擎"],
                     "battery_mah": 5800,
                     "wired_charge_w": 80,
                     "wireless_charge_w": 50,
                     "reverse_charge_w": 5,
                     "extreme_battery_days": 13,
                     "offline_tracking_h": 33,
                     "offline_comm": "2.4GHz畅连无网通信（最远7公里）",
                     "satellite": "北斗卫星消息+卫星天气查询",
                     "emergency": "摩斯码闪光警报",
                     "outdoor_routes": "10000+条户外精品路线（花瓣地图+两步路）",
                     "waterproof": "IP68 6米抗水 + IP69K高温高压喷水",
                     "fingerprint": "侧面指纹识别",
                     "ai": "鸿蒙AI（小艺+魔法表情+隔空传送+趣味主题）",
                     "colors": ["晨曦金", "云杉绿", "雪域白", "曜石黑"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08",
        relevance_to_robotics="超聚光长焦+红枫原色"
                              "影像系统为机器人视觉"
                              "色彩还原与远距感知提"
                              "供参考方案",
        deployment_ready=True,
        tags=["Mate 80 Pro", "麒麟9030", "第二代红枫影像",
              "超聚光长焦", "第二代昆仑玻璃", "北斗卫星",
              "IP68", "无网通信", "HarmonyOS 6"],
    ),
    AIProduct(
        product_id="MC-039", name="小米18标准版双2亿徕卡",
        category=AICategory.MOBILE_COMPUTER,
        organization="小米", country="中国",
        description="小米18系列标准版，与Pro系列分开举办发布会，"
                    "2026年第四季度正式上市。首批搭载高通骁龙8E6"
                    "（骁龙8 Elite Gen6标准版），台积电N2P改良版"
                    "2nm工艺，晶体管密度较3nm提升30%，同等性能"
                    "功耗下降36%。第三代自研Oryon CPU 2+3+3八核"
                    "三丛集架构，共享16MB L2缓存，Adreno 845 GPU，"
                    "LPDDR5X内存+UFS 5.0存储。6.4英寸极窄四等边"
                    "直屏（LIPO工艺），首次吃上超级像素排列，方形"
                    "矩阵DECO设计（左上角非对称四筒排列，取消妙享"
                    "背屏）。标准版系列首次引入徕卡联合调校双2亿"
                    "像素三摄：2亿像素超大底主摄+2亿像素潜望长焦+"
                    "超广角，高像素细节还原+大幅裁切二次构图仍清晰，"
                    "像素合并算法优化暗光拍摄，高动态夜景。实体AI"
                    "按键全系标配，一键唤醒超级小爱。五款配色可选："
                    "黑色、白色、粉色、蓝色、红色。受2nm芯片和内存"
                    "成本上涨影响，起售价超5499元，较上代涨幅超1000元。",
        key_metrics={"price_start_rmb": 5499,
                     "series": "小米18",
                     "tier": "标准版",
                     "chip": "骁龙8E6（骁龙8 Elite Gen6标准版）",
                     "process_nm": 2,
                     "process_detail": "台积电N2P改良版2nm",
                     "transistor_density_gain_pct": 30,
                     "power_save_pct": 36,
                     "cpu_arch": "第三代Oryon 2+3+3八核",
                     "l2_cache_mb": 16,
                     "gpu": "Adreno 845",
                     "ram": "LPDDR5X",
                     "storage": "UFS 5.0",
                     "screen_inch": 6.4,
                     "screen_type": "极窄四等边直屏（LIPO工艺）",
                     "screen_tech": "超级像素排列",
                     "camera_layout": "非对称四筒排列（左上角方形DECO）",
                     "back_screen": False,
                     "ai_key": "实体AI按键+超级小爱",
                     "camera_brand": "徕卡",
                     "main_camera_mp": 200,
                     "main_camera_desc": "2亿像素超大底主摄",
                     "telephoto_mp": 200,
                     "telephoto_desc": "2亿像素潜望长焦",
                     "ultrawide": "超广角镜头",
                     "camera_count": 3,
                     "photo_features": ["像素合并暗光优化", "高动态夜景",
                                        "大幅裁切清晰度"],
                     "colors": ["黑色", "白色", "粉色", "蓝色", "红色"],
                     "color_count": 5,
                     "price_increase": "较上代涨超1000元（内存+2nm成本）",
                     "release_date": "2026年第四季度（Q4）"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="2nm中端旗舰芯片为机器人"
                              "主控板提供低功耗高性能参考方案，"
                              "双2亿像素为机器人视觉模组提供高性价比选型",
        deployment_ready=False,
        tags=["小米18", "骁龙8E6", "2nm", "双2亿徕卡",
              "超级像素", "AI按键", "标准版", "5色"],
    ),
    AIProduct(
        product_id="MC-040", name="荣耀Robot Phone量产机器人手机",
        category=AICategory.MOBILE_COMPUTER,
        organization="荣耀", country="中国",
        description="全球首款实现量产的机器人手机，突破传统"
                    "智能手机方正机身设计限制，将机器人级别四自由度"
                    "机械臂集成至轻薄机身内部。自研钛合金灵巧云台为"
                    "整机核心亮点，集成100余个精密零件，核心电机仅重2.6g"
                    "体积比具身灵巧手关节电机缩小34%，加工精度±0.005mm，"
                    "三轴最大控制转速360°/s。闲置时摄像模组完全收纳进机身"
                    "保持简洁一体化；拍摄状态一键弹出，支持多角度灵活"
                    "调整机位，自动构图/AI直播追焦/视频通话追焦。"
                    "首发盾构钢翻转电机，0.5cm³空间堆叠43个零件，5级变速，"
                    "最大扭矩密度120N·m/L。6.31英寸1.5K OLED直屏（深天马"
                    "独家供应天工屏），1-120Hz LTPO自适应刷新率，峰值亮度"
                    "6800nits，4320Hz超高频PWM调光，94.58%屏占比，AI绿洲护眼"
                    "（AI离焦护眼/AI干眼友好/AI助眠显示）。全金属一体成型机身，"
                    "厚度9.59mm。专属多模态具身交互Agentic OS（联合阿里千问"
                    "大模型共创），YOYO机器人模式具备感知-规划-推理-执行-反馈"
                    "完整闭环，支持手势识别/情感识别/随音而舞。影像系统联合"
                    "好莱坞阿莱ARRI调校，引入纯正ARRI LogC3曲线与11种"
                    "ARRI Looks色彩方案，实现好莱坞级电影质感。"
                    "7060mAh新一代青海湖电池。发布YOYO技能商店，一键安装"
                    "即用，超100个系统资源开放。与矽递科技将机器人"
                    "方案开源，用户可3D打印机器人外壳、安装Robot kit、"
                    "加载Robot skill打造自有机器人方案。影像系统将"
                    "延展至9月发布的Magic9系列。8月18日正式开售。",
        key_metrics={"series": "荣耀Robot Phone",
                     "screen_supplier": "深天马独家供应（天工屏高端OLED）",
                     "screen_size": "6.31英寸",
                     "screen_resolution": "1.5K",
                     "screen_type": "OLED直屏",
                     "screen_refresh_hz": "1-120 LTPO自适应",
                     "screen_peak_brightness_nits": 6800,
                     "screen_pwm_hz": 4320,
                     "screen_to_body_ratio_pct": 94.58,
                     "screen_eye_care": ["AI离焦护眼", "AI干眼友好", "AI助眠显示"],
                     "chip": "第五代骁龙8至尊版移动平台",
                     "battery_mah": 7060,
                     "battery_tech": "新一代青海湖电池",
                     "mechanical_dof": 4,
                     "gimbal_material": "钛合金灵巧云台",
                     "gimbal_parts": 100,
                     "gimbal_motor_weight_g": 2.6,
                     "gimbal_motor_vol_reduction_pct": 34,
                     "gimbal_precision_mm": "±0.005",
                     "gimbal_max_speed_dps": 360,
                     "gimbal_storage": "完全收纳进机身（闲置时）",
                     "gimbal_popup": "一键弹出拍摄",
                     "motor_tech": "盾构钢翻转电机",
                     "motor_material": "2100MPa自研盾构钢",
                     "motor_parts_per_cm3": 43,
                     "motor_gears": 5,
                     "motor_torque_density": "120N·m/L",
                     "thickness_mm": 9.59,
                     "ram_gb": [12, 16],
                     "rom_gb": [512, 1024],
                     "storage_options": ["12GB+512GB 9999元", "16GB+1TB 12999元"],
                     "price_start_rmb": 9999,
                     "price_top_rmb": 12999,
                     "onsale_date": "8月18日",
                     "os": "Agentic OS（多模态具身交互，联合千问大模型共创）",
                     "yoyo_mode": "感知-规划-推理-执行-反馈完整闭环",
                     "multimodal_interaction": ["手势识别", "情感识别", "随音而舞"],
                     "camera_partner": "阿莱ARRI（好莱坞百年电影工业）",
                     "arri_logc3": True,
                     "arri_looks_count": 11,
                     "imaging_grade": "好莱坞级电影质感",
                     "ai_imaging": ["自动构图", "AI直播追焦", "视频通话追焦", "你说TA拍自动运镜"],
                     "app_store": "YOYO技能商店",
                     "open_resources": 100,
                     "open_source": "与矽递科技开源机器人方案",
                     "open_source_features": ["3D打印外壳", "Robot kit", "Robot skill"],
                     "communication": "荣耀鸿燕通信系统",
                     "future_products": "Magic9系列（9月发布）延续阿莱影像+聪明YOYO"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="四自由度机械臂+钛合金灵巧云台"
                              "直接应用机器人级精密机械结构（加工精度"
                              "±0.005mm，360°/s转速），Agentic OS"
                              "具身交互系统为机器人-人交互设计提供参考，"
                              "开源机器人方案可直接用于机器人教学与二次开发",
        deployment_ready=False,
        tags=["荣耀Robot Phone", "机器人手机", "四自由度机械臂",
              "钛合金灵巧云台", "盾构钢电机", "120Nm/L扭矩密度",
              "阿莱ARRI", "ARRI LogC3", "Agentic OS", "千问大模型",
              "开源机器人", "YOYO技能商店", "深马天工屏", "7060mAh青海湖电池",
              "9999元起", "8月18日开售"],
    ),
    AIProduct(
        product_id="MD-017", name="华为WATCH ULTIMATE DESIGN非凡大师星钻版",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="超高端智能腕表，24999元起。业界"
                    "首创复合稀土紫色陶瓷表圈（1400℃"
                    "高温淬炼），六段18K黄金手工镶嵌+"
                    "24K纯金字符。非晶锆合金表壳，TC4"
                    "钛合金间金表带。北斗卫星语音消息"
                    "（10秒语音），eSIM独立通信，星闪"
                    "智慧控车。150米深潜+海豚声呐通信。"
                    "X-TAP智感窗健康监测，鸿蒙AI。",
        key_metrics={"price_start_rmb": 24999,
                     "bezel": "复合稀土紫色陶瓷",
                     "gold_detail": "18K/24K黄金",
                     "case": "非晶锆合金",
                     "band": "TC4钛合金间金",
                     "satellite": "北斗语音消息",
                     "diving_m": 150,
                     "communication": ["eSIM", "星闪"],
                     "ai": "鸿蒙AI"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="北斗卫星通信和声呐"
                              "技术可参考机器人水下/"
                              "野外通信方案",
        deployment_ready=True,
        tags=["WATCH ULTIMATE DESIGN", "华为",
              "非凡大师", "北斗卫星", "18K金",
              "150米深潜", "24999元"],
    ),
    AIProduct(
        product_id="MD-018", name="华为WATCH GT Runner 2",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="与奥运马拉松冠军基普乔格共创"
                    "赛道传奇款，首发华为精英训练管理"
                    "平台。专业跑步训练体系，马拉松"
                    "备赛指导。2588元起，专属外观配色，"
                    "跑者精神设计灵感。",
        key_metrics={"price_start_rmb": 2588,
                     "co_brand": "基普乔格",
                     "screen_inch": 1.5,
                     "battery_days": 14,
                     "weight_g": 48,
                     "gnss": "双频五星",
                     "waterproof_5atm": True,
                     "sports_modes": 100,
                     "features": ["精英训练管理平台",
                                  "马拉松备赛",
                                  "专业跑步监测",
                                  "跑力指数",
                                  "训练负荷"],
                     "positioning": "专业跑者腕表"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="运动算法和训练管理"
                              "可参考机器人运动控制"
                              "和步态优化",
        deployment_ready=True,
        tags=["WATCH GT Runner 2", "华为",
              "基普乔格", "马拉松", "跑步腕表"],
    ),
    AIProduct(
        product_id="MD-019", name="小米手表S4 41mm",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="小米首款小尺寸手表，41mm表径，"
                    "9.5mm厚，仅32g。不锈钢中框，"
                    "米兰尼斯款镶嵌6分培育钻石表冠。"
                    "心率准确率提升，新增游泳实时心率"
                    "监测，超150种运动模式。双频GNSS"
                    "五星定位，专业睡眠阶段监测。"
                    "HyperOS人车家全生态，可控制"
                    "手机/电视/智能家居。",
        key_metrics={"size_mm": 41,
                     "thickness_mm": 9.5,
                     "weight_g": 32,
                     "frame": "不锈钢",
                     "sports_modes": 150,
                     "gnss": "双频五星",
                     "swim_hr": True,
                     "ecosystem": "人车家全生态"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="双频GNSS定位和运动"
                              "监测可参考机器人导航"
                              "和人体状态感知",
        deployment_ready=True,
        tags=["小米手表S4", "41mm", "32g",
              "双频GNSS", "游泳心率", "HyperOS"],
    ),
    AIProduct(
        product_id="MD-020", name="小米手环10",
        category=AICategory.MEDICAL_DEVICE,
        organization="", country="中国",
        description="1.72英寸AMOLED跑道屏，行业首次"
                    "2.0mm极窄四等边，73%屏占比，"
                    "1500nit亮度。HyperOS 2.0，150+"
                    "运动模式，新增蓝牙心率广播。"
                    "九轴传感器+AI泳姿识别（准确率95%），"
                    "指南针功能。最长21天续航，AOD 9天。"
                    "多彩中框2.0+蚕丝针织腕带。",
        key_metrics={"screen_inch": 1.72,
                     "screen_type": "AMOLED",
                     "brightness_nits": 1500,
                     "os": "HyperOS 2.0",
                     "sports_modes": "150+",
                     "sensors": "九轴",
                     "swim_ai": True,
                     "battery_days": 21,
                     "weight_g": 15.95},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="九轴传感器和泳姿"
                              "识别算法可参考机器人"
                              "姿态检测和运动识别",
        deployment_ready=True,
        tags=["小米手环10", "AMOLED", "1500nit",
              "九轴", "21天续航", "HyperOS 2.0"],
    ),
    AIProduct(
        product_id="MD-021", name="Apple Watch Series 12",
        category=AICategory.MEDICAL_DEVICE,
        organization="Apple", country="美国",
        description="Apple Watch年度更新，搭载新一代"
                    "S11芯片。可能加入Touch ID和更多"
                    "健康传感器。watchOS 27带来更智能"
                    "Siri和健康洞察。与iPhone 18系列"
                    "同步发布，Apple Intelligence"
                    "深度整合。",
        key_metrics={"chip": "S11",
                     "ai": "Apple Intelligence",
                     "biometric": "Touch ID（传闻）",
                     "os": "watchOS 27",
                     "health_sensors": "升级款"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="健康传感器和Siri"
                              "交互可参考机器人"
                              "人机交互方案",
        deployment_ready=False,
        tags=["Apple Watch Series 12", "Apple",
              "S11", "watchOS 27", "健康监测"],
    ),
    AIProduct(
        product_id="MD-022", name="Apple Watch Ultra 4",
        category=AICategory.MEDICAL_DEVICE,
        organization="Apple", country="美国",
        description="Apple Watch Ultra第四代，"
                    "升级S11芯片。新增卫星功能（Apple "
                    "Maps卫星导航、卫星收发照片）。"
                    "更坚固钛合金表壳，户外专业功能"
                    "强化，更长续航。与iPhone 18系列"
                    "同期发布。",
        key_metrics={"chip": "S11",
                     "case": "钛合金",
                     "satellite_features": ["卫星地图",
                                            "卫星照片"],
                     "positioning": "户外专业",
                     "ai": "Apple Intelligence"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="卫星导航和钛合金"
                              "防护可参考机器人"
                              "户外作业终端",
        deployment_ready=False,
        tags=["Apple Watch Ultra 4", "Apple",
              "钛合金", "卫星导航", "户外"],
    ),
    AIProduct(
        product_id="HA-015", name="苹果HomePod mini 2",
        category=AICategory.HOME_APPLIANCE,
        organization="Apple", country="美国",
        description="第二代HomePod mini智能音箱，"
                    "搭载更新S系列芯片（基于Apple "
                    "Watch Series 10），全新Siri"
                    "智能体验。新增配色选项，可能"
                    "采用N1网络芯片。支持Matter"
                    "智能家居协议、Thread网络、"
                    "UWB超宽带。家庭中枢功能。",
        key_metrics={"chip": "S系列（基于S10）",
                     "smart_assistant": "Siri",
                     "protocols": ["Matter", "Thread",
                                   "UWB", "蓝牙"],
                     "features": ["家庭中枢",
                                  "智能家居控制",
                                  "广播对讲"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="Matter/Thread协议"
                              "和UWB可用于机器人"
                              "智能家居互联",
        deployment_ready=False,
        tags=["HomePod mini 2", "Apple", "Siri",
              "Matter", "Thread", "家庭中枢"],
    ),
    AIProduct(
        product_id="HA-016", name="苹果HomePad家庭中枢",
        category=AICategory.HOME_APPLIANCE,
        organization="Apple", country="美国",
        description="全新品类家庭智能中枢设备，"
                    "配备7英寸iPad风格全显示屏。"
                    "两款型号：壁挂式和带扬声器"
                    "底座式（类似HomePod mini）。"
                    "支持智能家居控制、音乐播放、"
                    "视频通话、天气查询、照片显示、"
                    "日历备忘、Siri语音助手。10月起"
                    "陆续发售。",
        key_metrics={"screen_inch": 7,
                     "form_factors": ["壁挂式",
                                       "扬声器底座式"],
                     "features": ["智能家居控制",
                                  "视频通话", "音乐",
                                  "照片展示", "Siri"],
                     "positioning": "家庭智能中枢"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="家庭中枢显示屏和"
                              "多模态交互可参考"
                              "机器人家用控制台",
        deployment_ready=False,
        tags=["HomePad", "Apple", "家庭中枢",
              "7英寸屏", "Siri", "新品类"],
    ),
    AIProduct(
        product_id="MC-041", name="华为MateBook Fold非凡大师鸿蒙折叠电脑",
        category=AICategory.MOBILE_COMPUTER,
        organization="华为", country="中国",
        description="全球首款鸿蒙折叠形态个人电脑，采用创新铰链结构与柔性屏幕"
                    "技术，在保持极致便携性的同时实现接近传统笔记本的大屏体验，"
                    "有效平衡轻薄形态与高效生产力，是当前同级别唯一采用折叠形态"
                    "的个人电脑。搭载麒麟X90 Plus处理器，运行HarmonyOS 7操作系统，"
                    "支持鸿蒙生态全场景互联，折叠形态满足移动办公、大屏创作双场景"
                    "需求，玄武水滴铰链核心部件采用超强火箭钢，提供超强防护与"
                    "可靠折叠寿命。",
        key_metrics={"series": "MateBook Fold非凡大师",
                     "form_factor": "折叠形态笔记本电脑",
                     "chip": "麒麟X90 Plus",
                     "os": "HarmonyOS 7",
                     "hinge": "玄武水滴铰链",
                     "hinge_material": "超强火箭钢",
                     "positioning": "全球首款鸿蒙折叠电脑",
                     "scenarios": ["移动办公", "大屏创作", "全场景互联"],
                     "ecosystem": "鸿蒙全场景互联"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="折叠屏铰链技术可用于机器人可变形交互界面设计，"
                              "柔性屏幕技术为机器人柔性显示模块提供参考",
        deployment_ready=False,
        tags=["华为MateBook Fold", "折叠电脑", "鸿蒙PC", "麒麟X90 Plus",
              "玄武水滴铰链", "HarmonyOS 7", "非凡大师"],
    ),
    AIProduct(
        product_id="MC-042", name="华为MatePad Pro 2026旗舰平板",
        category=AICategory.MOBILE_COMPUTER,
        organization="华为", country="中国",
        description="华为旗舰平板产品，12.2英寸OLED大屏，支持鸿蒙PC级办公应用，"
                    "搭配星闪手写笔与磁吸键盘，实现创作、办公、娱乐全场景覆盖。"
                    "搭载麒麟旗舰处理器，支持超级终端多设备协同，屏幕支持高"
                    "刷新率与高频PWM调光，办公娱乐两不耽误。",
        key_metrics={"series": "MatePad Pro 2026",
                     "screen_size": "12.2英寸",
                     "screen_type": "OLED",
                     "chip": "麒麟旗舰处理器",
                     "accessories": ["星闪手写笔", "磁吸键盘"],
                     "features": ["PC级办公应用", "超级终端协同", "多设备互联"],
                     "scenarios": ["创作", "办公", "娱乐"],
                     "os": "HarmonyOS 7"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="大尺寸高刷OLED屏可作为机器人控制终端显示方案，"
                              "星闪低延迟连接技术适用于机器人无线控制",
        deployment_ready=False,
        tags=["华为MatePad Pro", "旗舰平板", "12.2英寸OLED", "星闪手写笔",
              "鸿蒙平板", "PC级办公"],
    ),
    AIProduct(
        product_id="MC-043", name="华为MateBook Pro S轻薄本",
        category=AICategory.MOBILE_COMPUTER,
        organization="华为", country="中国",
        description="重新定义轻薄本标准，整机重量仅798克，显著低于主流同类产品，"
                    "标志着移动计算设备在便携性维度上的又一次重要演进，达到"
                    "行业新高度。搭载HarmonyOS 7，支持鸿蒙生态全场景互联，"
                    "在极致轻薄的同时保持性能释放与长续航，满足移动办公高频"
                    "需求。",
        key_metrics={"series": "MateBook Pro S",
                     "weight_g": 798,
                     "weight_benchmark": "行业轻薄本新标杆",
                     "os": "HarmonyOS 7",
                     "chip": "麒麟处理器",
                     "positioning": "超轻薄鸿蒙笔记本",
                     "features": ["极致便携", "长续航", "全场景互联"],
                     "scenarios": ["移动办公", "商务出行"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="极致轻量化结构设计可参考机器人便携控制器减重方案",
        deployment_ready=False,
        tags=["华为MateBook Pro S", "轻薄本", "798克", "鸿蒙PC",
              "HarmonyOS 7", "超轻薄"],
    ),
    AIProduct(
        product_id="MC-044", name="华为nova 16 SE手机",
        category=AICategory.MOBILE_COMPUTER,
        organization="华为", country="中国",
        description="nova系列SE产品线回归全新中端力作，主打超大续航、原色影像、"
                    "流畅鸿蒙体验、轻薄高颜值。6.84英寸OLED直面大屏，1.5K分辨率/"
                    "10.7亿色/P3广色域/120Hz刷新率/2160Hz高频PWM调光/300Hz触控"
                    "采样率/8000nits峰值亮度。首次将旗舰级红枫原色影像系统下放"
                    "至2000元档位，后置5000万像素超感知主摄（RYYB传感器/1/1.56"
                    "英寸底/F1.9光圈），前置3200万像素。搭载8500mAh巨鲸电池"
                    "（nova系列最大）+66W Turbo超级快充，麒麟8020处理器，"
                    "支持北斗卫星通信、星闪E2.0、蓝牙6.0、NFC、红外、IP65防尘"
                    "抗水，侧边指纹解锁，3D光影雕刻工艺/幻彩贝母配色。2499元"
                    "起，8月12日正式开售。",
        key_metrics={"series": "nova 16 SE",
                     "screen_size": "6.84英寸",
                     "screen_resolution": "1.5K",
                     "screen_type": "OLED直面屏",
                     "screen_colors": "10.7亿色/P3广色域",
                     "screen_refresh_hz": 120,
                     "screen_pwm_hz": 2160,
                     "screen_touch_hz": 300,
                     "screen_peak_brightness_nits": 8000,
                     "chip": "麒麟8020",
                     "battery_mah": 8500,
                     "battery_tech": "巨鲸电池（nova系列最大）",
                     "charge_w": 66,
                     "charge_tech": "Turbo超级快充",
                     "rear_camera_main_mp": 50,
                     "rear_camera_main_sensor": "RYYB",
                     "rear_camera_main_size": "1/1.56英寸",
                     "rear_camera_main_aperture": "F1.9",
                     "camera_system": "红枫原色影像系统（旗舰下放）",
                     "front_camera_mp": 3200,
                     "ram_gb": [8, 12],
                     "rom_gb": [256, 512],
                     "storage_options": ["8GB+256GB 2499元", "12GB+512GB 2999元"],
                     "price_start_rmb": 2499,
                     "connectivity": ["北斗卫星通信", "星闪E2.0", "蓝牙6.0", "NFC", "红外"],
                     "waterproof": "IP65防尘抗水",
                     "fingerprint": "侧边指纹解锁",
                     "design": "3D光影雕刻工艺",
                     "color": "幻彩贝母",
                     "os": "HarmonyOS",
                     "features": ["AI防诈", "星盾守护", "侧边快捷按键"],
                     "onsale_date": "8月12日"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="8500mAh大容量电池方案可为移动机器人续航设计提供参考，"
                              "RYYB暗光成像技术可提升机器人弱光环境视觉能力",
        deployment_ready=False,
        tags=["华为nova 16 SE", "8500mAh巨鲸电池", "66W快充", "麒麟8020",
              "红枫原色", "北斗卫星", "2499元起", "星闪E2.0"],
    ),
    AIProduct(
        product_id="DP-012", name="华为MateBook Pro麒麟X90 Plus",
        category=AICategory.DIGITAL_PRODUCT,
        organization="华为", country="中国",
        description="华为高性能鸿蒙笔记本，搭载麒麟X90 Plus处理器，"
                    "HarmonyOS 7花粉Beta版8月中旬开启，与MateBook Fold、"
                    "MateBook 14鸿蒙版共同构成鸿蒙PC完整产品矩阵。",
        key_metrics={"series": "MateBook Pro",
                     "chip": "麒麟X90 Plus",
                     "os": "HarmonyOS 7",
                     "beta_date": "8月中旬花粉Beta",
                     "compatible_models": ["MateBook Fold非凡大师麒麟X90 Plus",
                                           "MateBook Fold非凡大师",
                                           "MateBook Pro麒麟X90 Plus",
                                           "MateBook Pro",
                                           "MateBook Pro S",
                                           "MateBook 14鸿蒙版"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="鸿蒙PC生态为机器人上位机开发提供国产操作系统选项",
        deployment_ready=False,
        tags=["华为MateBook Pro", "麒麟X90 Plus", "HarmonyOS 7", "鸿蒙PC"],
    ),
    AIProduct(
        product_id="MD-023", name="华为WATCH GT 7 Pro智能手表",
        category=AICategory.MEDICAL_DEVICE,
        organization="华为", country="中国",
        description="华为WATCH GT系列专业旗舰款，延续GT系列长续航基因，"
                    "升级健康监测传感器与运动模式，支持ECG心电分析、"
                    "血管健康研究、睡眠呼吸暂停监测等专业健康功能，"
                    "搭配AMOLED高清屏，支持鸿蒙全场景互联。",
        key_metrics={"series": "WATCH GT 7 Pro",
                     "positioning": "专业旗舰智能手表",
                     "display": "AMOLED高清屏",
                     "health_features": ["ECG心电分析", "血管健康研究",
                                         "睡眠呼吸暂停监测", "心率监测",
                                         "血氧监测"],
                     "sports_modes": 100,
                     "battery_life_days": 14,
                     "waterproof": "5ATM+IP68",
                     "os": "HarmonyOS",
                     "connectivity": ["蓝牙", "NFC", "星闪"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="高精度健康传感器与低功耗设计可参考可穿戴机器人"
                              "健康监测模块方案",
        deployment_ready=False,
        tags=["华为WATCH GT 7 Pro", "智能手表", "ECG心电", "长续航",
              "鸿蒙穿戴", "健康监测"],
    ),
    AIProduct(
        product_id="MD-024", name="华为WATCH GT 7智能手表",
        category=AICategory.MEDICAL_DEVICE,
        organization="华为", country="中国",
        description="华为WATCH GT系列标准款，主打超长续航与全面健康运动监测，"
                    "覆盖大众用户日常健康管理与运动记录需求，AMOLED高清彩屏，"
                    "支持心率、血氧、睡眠、压力全方位健康监测，100+运动模式，"
                    "鸿蒙系统流畅体验。",
        key_metrics={"series": "WATCH GT 7",
                     "positioning": "大众旗舰长续航智能手表",
                     "display": "AMOLED高清彩屏",
                     "health_features": ["心率监测", "血氧监测", "睡眠监测",
                                         "压力监测"],
                     "sports_modes": 100,
                     "battery_life_days": 14,
                     "waterproof": "5ATM",
                     "os": "HarmonyOS"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="低功耗可穿戴方案为机器人可穿戴交互模块提供参考",
        deployment_ready=False,
        tags=["华为WATCH GT 7", "智能手表", "长续航", "健康监测", "鸿蒙穿戴"],
    ),
    AIProduct(
        product_id="WA-012", name="华为HarmonyOS 7鸿蒙操作系统",
        category=AICategory.WORLD_MODEL,
        organization="华为", country="中国",
        description="鸿蒙操作系统最新版本，8月中旬开启花粉Beta测试，覆盖"
                    "折叠电脑、MateBook Pro系列、MateBook Pro S、MateBook 14"
                    "鸿蒙版等全系列PC产品，标志着鸿蒙在PC端生态进一步成熟，"
                    "实现手机、平板、PC、穿戴、车机、IoT全场景统一内核。",
        key_metrics={"version": "HarmonyOS 7",
                     "beta_date": "8月中旬花粉Beta",
                     "supported_pcs": ["MateBook Fold非凡大师麒麟X90 Plus",
                                       "MateBook Fold非凡大师",
                                       "MateBook Pro麒麟X90 Plus",
                                       "MateBook Pro",
                                       "MateBook Pro S",
                                       "MateBook 14鸿蒙版"],
                     "ecosystem": "手机/平板/PC/穿戴/车机/IoT全场景统一",
                     "kernel": "微内核分布式架构"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="分布式微内核架构为多机器人协同、机器人-设备互联"
                              "提供统一操作系统基础",
        deployment_ready=False,
        tags=["HarmonyOS 7", "鸿蒙7", "华为PC系统", "全场景互联", "分布式OS"],
    ),
    AIProduct(
        product_id="AU-015", name="尊界V800旗舰MPV",
        category=AICategory.AUTOMOTIVE,
        organization="鸿蒙智行×华为", country="中国",
        description="鸿蒙智行尊界时代旗舰MPV，车长5495mm/宽2006mm/高1850mm，"
                    "轴距3430mm，有效舱内空间长达3856mm/5.7m²地板面积。"
                    "提供曜日金棕/破晓金黑/凌云墨白/瑞雪银红双拼车色+星耀黑/"
                    "云水天青共6种车色，5种内饰选择。配备双百万像素全彩智能"
                    "投影大灯，星环尾灯多层晶钻映射设计/全彩智能交互流光尾灯"
                    "共5032颗灯珠。独创L型加高中岛集成多重功能，8L车载冰箱"
                    "分区储物支持指纹解锁。首创灵云座椅20层叠层设计/恒温加热"
                    "全覆盖/全手工皮质软包/20处按摩点位中央供气式按摩。"
                    "推出尊享版/行政版/领航版三个版本，售价76.6万/86.6万/101.6"
                    "万元，9月启动交付。",
        key_metrics={"series": "尊界V800",
                     "length_mm": 5495, "width_mm": 2006, "height_mm": 1850,
                     "wheelbase_mm": 3430,
                     "cabin_length_mm": 3856,
                     "cabin_floor_area_m2": 5.7,
                     "colors": 6,
                     "interior_options": 5,
                     "headlight": "双百万像素全彩智能投影大灯",
                     "taillight_leds": 5032,
                     "center_console": "L型加高中岛",
                     "fridge_l": 8,
                     "console_features": ["指纹解锁", "分区储物"],
                     "seat_tech": "灵云座椅",
                     "seat_layers": 20,
                     "seat_features": ["恒温加热全覆盖", "全手工皮质软包",
                                       "20点中央供气式按摩"],
                     "storage_options": ["尊享版 76.6万元", "行政版 86.6万元",
                                         "领航版 101.6万元"],
                     "price_start_rmb": 766000,
                     "price_top_rmb": 1016000,
                     "delivery_date": "9月",
                     "pre_orders_before_aug5": 10000,
                     "v800_order_ratio_pct": 80},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="车载智能交互系统、多传感器融合方案可为机器人"
                              "移动平台人机交互设计提供参考",
        deployment_ready=False,
        tags=["尊界V800", "鸿蒙智行", "旗舰MPV", "76.6万起", "灵云座椅",
              "5032颗灯珠", "8L冰箱", "9月交付"],
    ),
    AIProduct(
        product_id="AU-016", name="尊界V680豪华MPV",
        category=AICategory.AUTOMOTIVE,
        organization="鸿蒙智行×华为", country="中国",
        description="鸿蒙智行尊界系列豪华MPV，与V800同期上市，提供星耀黑/"
                    "瑞锦红/破晓金黑/曜日金棕/凌云墨白共5种车色，定位略低于"
                    "V800，满足高端商务MPV市场多层次需求。",
        key_metrics={"series": "尊界V680",
                     "positioning": "豪华MPV",
                     "colors": 5,
                     "color_options": ["星耀黑", "瑞锦红", "破晓金黑",
                                       "曜日金棕", "凌云墨白"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="车载电子架构可参考机器人移动平台设计",
        deployment_ready=False,
        tags=["尊界V680", "鸿蒙智行", "豪华MPV"],
    ),
    AIProduct(
        product_id="AU-017", name="享界G9豪华硬派SUV",
        category=AICategory.AUTOMOTIVE,
        organization="鸿蒙智行×华为", country="中国",
        description="鸿蒙智行豪华硬派SUV，开启预售，预售价43.98万元起，"
                    "硬派越野造型搭配华为智驾系统，填补鸿蒙智行硬派SUV"
                    "产品空白。",
        key_metrics={"series": "享界G9",
                     "segment": "豪华硬派SUV",
                     "preorder_price_start_rmb": 439800,
                     "status": "开启预售",
                     "smart_drive": "华为智驾系统"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="硬派越野底盘控制技术可参考野外作业机器人设计",
        deployment_ready=False,
        tags=["享界G9", "鸿蒙智行", "硬派SUV", "43.98万起", "华为智驾"],
    ),
    AIProduct(
        product_id="CH-012", name="华为升腾950PR AI加速芯片",
        category=AICategory.AI_CHIP,
        organization="华为", country="中国",
        description="华为自研新一代AI推理/训练加速芯片，基于5nm制程工艺，"
                    "配备112GB自研HiBL高带宽内存，FP16/BF16算力达500 TFLOPS，"
                    "FP8算力达1000 TFLOPS，FP4算力达1560 TFLOPS，整卡功耗600W。"
                    "搭载自研HBM内存，FP4性能达Nvidia H20的2.8倍，基于Atlas 350"
                    "加速板卡形态。2026年下半年下一代新品互联带宽达2TB/s，超过"
                    "NVLink5.0的1.8TB/s，整体性能达到A720水平，可满足国内大部分"
                    "推理及部分大模型训练需求。2026年华为升腾芯片出货预计超130万颗。",
        key_metrics={"model": "Ascend 950PR",
                     "process_node": "5nm",
                     "memory_gb": 112,
                     "memory_type": "自研HiBL高带宽内存",
                     "fp16_tflops": 500,
                     "fp8_tflops": 1000,
                     "fp4_tflops": 1560,
                     "tdp_w": 600,
                     "interconnect": "LinQu/HCCS",
                     "board": "Atlas 350加速板卡",
                     "fp4_vs_h20_x": 2.8,
                     "next_gen_interconnect_tbs": 2,
                     "next_gen_perf_target": "A720水平",
                     "2026_shipment_forecast": 1300000,
                     "price_usd": 9600},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="国产高性能AI芯片为机器人端侧推理与VLA模型部署"
                              "提供自主可控算力选项，2TB/s互联带宽支持多机器"
                              "人协同训练集群",
        deployment_ready=True,
        tags=["华为升腾950PR", "Ascend 950PR", "AI芯片", "5nm", "1560 TFLOPS FP4",
              "自研HBM", "Atlas 350", "130万颗出货", "2TB/s互联"],
    ),
    AIProduct(
        product_id="CH-013", name="华为存算一体AI芯片",
        category=AICategory.AI_CHIP,
        organization="华为", country="中国",
        description="华为深度布局存算一体技术，完成从芯片架构设计、流片量产到"
                    "场景落地的全链路打通，改变传统算力运行逻辑，实现存储与计算"
                    "一体化运作，大幅降低数据搬运损耗，完美适配海量边缘终端、"
                    "物联网设备的算力需求，成为国产算力差异化突围的核心赛道。"
                    "2026年已实现规模化量产，良率、稳定性达到商用标准。",
        key_metrics={"technology": "存算一体（Computing-in-Memory）",
                     "architecture_advantage": "消除冯诺依曼瓶颈",
                     "benefits": ["数据搬运功耗大幅降低", "算力利用率提升",
                                  "适配边缘终端低功耗场景"],
                     "production_status": "规模化量产",
                     "yield": "商用标准",
                     "application_scenarios": ["边缘推理", "物联网终端",
                                               "工业终端", "民用智能设备"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="存算一体超低功耗架构为机器人端侧AI推理提供理想"
                              "算力方案，大幅降低机器人功耗提升续航",
        deployment_ready=True,
        tags=["华为存算一体", "CIM芯片", "AI芯片", "国产算力", "边缘推理",
              "低功耗AI", "规模化量产"],
    ),
    AIProduct(
        product_id="CP-012", name="英伟达Vera Rubin R100下一代AI加速芯片",
        category=AICategory.AI_COMPUTE,
        organization="NVIDIA", country="美国",
        description="英伟达下一代旗舰AI加速芯片，3nm制程工艺，3360亿晶体管，"
                    "288GB HBM4高带宽内存，显存带宽达22TB/s，整卡功耗2300W。"
                    "FP16/BF16算力达4000 TFLOPS，FP8算力达17500 TFLOPS，FP4算力"
                    "达50000 TFLOPS（训练）/35000 TFLOPS（推理），采用NVLink 6"
                    "互联，是Blackwell架构之后的全新一代产品，性能实现量级飞跃。",
        key_metrics={"model": "Vera Rubin R100",
                     "process_node": "3nm",
                     "transistors_bn": 336,
                     "memory_gb": 288,
                     "memory_type": "HBM4",
                     "memory_bandwidth_tbs": 22,
                     "tdp_w": 2300,
                     "fp16_tflops": 4000,
                     "fp8_tflops": 17500,
                     "fp4_train_tflops": 50000,
                     "fp4_infer_tflops": 35000,
                     "interconnect": "NVLink 6"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="下一代旗舰算力为超大规模VLA模型训练提供基础设施",
        deployment_ready=False,
        tags=["英伟达Vera Rubin", "R100", "3nm", "HBM4", "22TB/s",
              "17500 TFLOPS FP8", "50000 TFLOPS FP4", "NVLink 6"],
    ),
    AIProduct(
        product_id="CP-013", name="AMD MI455X AI加速芯片",
        category=AICategory.AI_COMPUTE,
        organization="AMD", country="美国",
        description="AMD下一代旗舰AI加速卡，2nm制程工艺，3200亿晶体管，"
                    "432GB HBM4超大容量显存，整卡功耗900W，FP16/BF16算力达"
                    "5000 TFLOPS，FP8算力达20100 TFLOPS，FP4算力达40300 TFLOPS，"
                    "采用UALink/PCIe Gen6互联，MI300X系列之后的全新一代产品，"
                    "算力密度显著领先。AMD 8月6日收购AI推理芯片厂商Taalas"
                    "（加拿大多伦多），进一步强化推理技术栈。",
        key_metrics={"model": "MI455X",
                     "process_node": "2nm",
                     "transistors_bn": 320,
                     "memory_gb": 432,
                     "memory_type": "HBM4",
                     "tdp_w": 900,
                     "fp16_tflops": 5000,
                     "fp8_tflops": 20100,
                     "fp4_tflops": 40300,
                     "interconnect": "UALink/PCIe Gen6",
                     "acquisition": "Taalas推理芯片（8月6日）"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="432GB超大显存可支持超大规模VLA模型单卡运行",
        deployment_ready=False,
        tags=["AMD MI455X", "2nm", "432GB HBM4", "20100 TFLOPS FP8", "UALink",
              "Taalas收购"],
    ),
    AIProduct(
        product_id="HR-023", name="时耘科技RD3 Ultra工业级全功能全尺寸人形机器人",
        category=AICategory.HUMANOID_ROBOT,
        organization="时耘科技", country="中国",
        description="工业级全功能全尺寸人形机器人，在天津空天数字产业园正式量产"
                    "下线，被称作7×24小时在岗的特种作业尖兵。身高174cm，身形"
                    "比例贴合人体，真正全地形适配：草地/地毯/鹅卵石/水泥地/"
                    "瓷砖/玻璃路面均可平稳通行，自主完成爬坡/登台阶/避障。标准"
                    "续航8小时，搭配10秒极速换电，可实现7×24小时不间断连续作业。"
                    "覆盖场站值守（电力/化工/机房全天候安防应急）、工业运维（厂区"
                    "巡检/点位核查/作业引导）、特种巡检（园区巡逻/管廊/野外线路/"
                    "环境监测）、科研实训（高校二次开发/算法验证）、环境勘查（高危"
                    "区域数据采集/采-训-测-推一体化）、应急协同（现场初勘/物资转运/"
                    "人员引导）六大领域。产线具备行走老化测试（单机连续行走1小时+）"
                    "/5度坡度测试/台阶上下坡/复杂工况全覆盖，与京东机器人深度共建"
                    "康养人形方案（医疗问询/情绪陪伴/疗愈辅助），现有百台级量产，"
                    "明年扩充至千台产能。",
        key_metrics={"model": "RD3 Ultra",
                     "height_cm": 174,
                     "terrain_adapt": ["草地", "地毯", "鹅卵石", "水泥地",
                                       "瓷砖", "玻璃路面", "爬坡", "登台阶",
                                       "避障"],
                     "battery_life_h": 8,
                     "battery_swap_s": 10,
                     "operation_mode": "7×24小时不间断作业",
                     "positioning": "特种作业尖兵",
                     "application_fields": 6,
                     "applications": ["场站值守", "工业运维", "特种巡检",
                                      "科研实训", "环境勘查", "应急协同"],
                     "testing_standards": ["单机连续行走1小时+老化测试",
                                           "5度坡度模拟", "台阶/上下坡/后退",
                                           "复杂工况全覆盖"],
                     "partners": "京东机器人（康养赛道共建）",
                     "healthcare_features": ["医疗问询", "情绪陪伴", "疗愈康养辅助"],
                     "current_capacity": "百台级量产",
                     "2027_capacity": "千台产能"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="工业级全尺寸人形量产下线，10秒换电+全地形通行"
                              "为人形机器人工业化落地提供实际参考",
        deployment_ready=True,
        tags=["时耘RD3 Ultra", "工业人形机器人", "天津量产", "174cm",
              "8小时续航", "10秒换电", "7×24作业", "六大领域", "千台产能"],
    ),
    AIProduct(
        product_id="HR-024", name="博银合创BW10重载双臂具身机器人",
        category=AICategory.HUMANOID_ROBOT,
        organization="博银合创", country="中国",
        description="全新工业机型重载双臂具身机器人，负载能力强，支持4分钟"
                    "快换电，支持工厂7×24小时不间断作业，工业实用性大幅提升。",
        key_metrics={"model": "BW10",
                     "type": "重载双臂具身机器人",
                     "battery_swap_min": 4,
                     "operation_mode": "7×24小时不间断作业",
                     "features": ["高负载", "快换电", "工业级稳定性"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="重载双臂+快换电方案解决工业人形机器人连续作业痛点",
        deployment_ready=False,
        tags=["博银合创BW10", "重载双臂", "4分钟快换电", "7×24作业", "工业人形"],
    ),
    AIProduct(
        product_id="HR-025", name="跨维智能DexForce W1 Pro第二代通用人形机器人",
        category=AICategory.HUMANOID_ROBOT,
        organization="跨维智能", country="中国",
        description="国内首款实现AI引擎-视觉-大脑-本体全链路自研的标杆产品，"
                    "由贾奎博士（港中深终身教授/全球Top2%科学家）领衔创办，"
                    "百亿估值具身智能独角兽。搭载全自研双目纯视觉传感器，"
                    "依托首创Sim2Real VLA模型框架与100%合成数据训练体系，"
                    "具备±1mm精准定位、0.1N灵敏力控能力，全身40自由度超高"
                    "灵活度，可独立完成咖啡制作/糖画创作/爆米花制作/精密拧螺丝"
                    "等高低难度复合任务。坚持沿途下蛋实战策略，依托全国50余个"
                    "真实落地场景持续反哺模型迭代，在全国15+城市常态化运营，"
                    "落地1000+项目，毫米级操作任务成功率99.9%以上，覆盖文旅/"
                    "商业/智能制造/政务迎宾多元场景。",
        key_metrics={"model": "DexForce W1 Pro",
                     "generation": "第二代",
                     "founder": "贾奎博士（港中深终身教授/全球Top2%科学家）",
                     "valuation": "百亿估值独角兽",
                     "full_stack_self_research": ["AI引擎", "视觉", "大脑", "本体"],
                     "vision": "全自研双目纯视觉传感器",
                     "vla_framework": "Sim2Real VLA（首创）",
                     "training_data": "100%合成数据",
                     "positioning_accuracy_mm": "±1",
                     "force_control_sensitivity_n": 0.1,
                     "total_dof": 40,
                     "capabilities": ["咖啡制作", "糖画创作", "爆米花制作",
                                      "精密拧螺丝", "高低难度复合任务"],
                     "deployment_cities": 15,
                     "deployment_projects": 1000,
                     "deployment_scenarios": 50,
                     "mm_task_success_rate_pct": 99.9,
                     "application_areas": ["文旅景区", "商业商圈", "智能制造",
                                           "政务迎宾"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="全链路自研+Sim2Real合成数据训练+±1mm/0.1N精度"
                              "为人形机器人精细操作树立标杆，1000+项目落地",
        deployment_ready=True,
        tags=["跨维智能DexForce W1 Pro", "全链路自研", "Sim2Real VLA",
              "±1mm定位", "0.1N力控", "40自由度", "99.9%成功率", "1000+项目落地"],
    ),
    AIProduct(
        product_id="IR-010", name="比亚迪尧舜禹工业人形机器人（小迪）",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="比亚迪", country="中国",
        description="比亚迪自研人形机器人，已累计投放约150台样机在深圳、长沙"
                    "等基地实训，小迪机器人于8月在郑州全球首秀，依托比亚迪"
                    "HyWorldVLA视觉语言动作模型与2300万智驾车队数据闭环训练。",
        key_metrics={"series": "尧舜禹",
                     "deployed_units": 150,
                     "deployed_bases": ["深圳", "长沙"],
                     "xiaodi_debut": "8月郑州全球首秀",
                     "vla_model": "HyWorldVLA",
                     "training_data_miles": "2300万智驾车队数据"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="车企供应链优势赋能人形机器人量产，自动驾驶VLA"
                              "架构迁移至人形机器人",
        deployment_ready=False,
        tags=["比亚迪尧舜禹", "小迪机器人", "150台样机", "HyWorldVLA",
              "郑州首秀", "汽车人形机器人"],
    ),
    AIProduct(
        product_id="IR-011", name="小鹏IRON人形机器人",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="小鹏汽车", country="中国",
        description="小鹏汽车自研人形机器人，已进入广州工厂小批量试产阶段，"
                    "量产进度超预期，依托小鹏汽车智能驾驶与智能制造技术积累。",
        key_metrics={"model": "IRON",
                     "production_status": "广州工厂小批量试产",
                     "tech_source": "小鹏智驾+智能制造积累"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="车企入局人形机器人加速产业规模化，智驾技术迁移",
        deployment_ready=False,
        tags=["小鹏IRON", "人形机器人", "小批量试产", "广州工厂", "车企入局"],
    ),
    AIProduct(
        product_id="LLM-012", name="商汤ACE-Brain具身基础模型",
        category=AICategory.AI_LLM,
        organization="商汤科技", country="中国",
        description="商汤正式开源的具身智能基础模型，适配全品类机器人，大幅"
                    "降低国产具身智能开发门槛，为国产机器人提供统一大模型底座。",
        key_metrics={"model": "ACE-Brain",
                     "type": "具身基础模型",
                     "license": "开源",
                     "compatibility": "全品类机器人适配",
                     "release_date": "8月1日"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="开源具身基础模型为国产机器人大脑提供统一底座，"
                              "降低开发门槛加速生态形成",
        deployment_ready=True,
        tags=["商汤ACE-Brain", "开源具身模型", "全品类机器人适配", "国产大模型"],
    ),
    AIProduct(
        product_id="LLM-013", name="Google Gemini Robotics 2全身统一控制模型",
        category=AICategory.AI_LLM,
        organization="Google DeepMind", country="美国",
        description="全球首个全身统一控制模型，一套AI同时搞定人形机器人走路、"
                    "平衡、手臂精细操作，彻底解决以往软硬件割裂难题，"
                    "标志着机器人控制从分离模块走向端到端统一。",
        key_metrics={"model": "Gemini Robotics 2",
                     "breakthrough": "全球首个全身统一控制模型",
                     "unified_capabilities": ["行走", "平衡", "手臂精细操作"],
                     "advantage": "解决软硬件割裂难题",
                     "architecture": "端到端统一控制"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="全身统一控制模型是具身智能重要技术方向，"
                              "大幅简化机器人控制系统复杂度",
        deployment_ready=False,
        tags=["Gemini Robotics 2", "全身统一控制", "端到端机器人AI", "DeepMind"],
    ),
    AIProduct(
        product_id="AG-023", name="OpenAI ChatGPT 8美元额度重置云服务模式",
        category=AICategory.AI_AGENT,
        organization="OpenAI", country="美国",
        description="OpenAI推动ChatGPT从订阅制转向云服务模式，Plus用户（20美元/月）"
                    "周额度耗尽后可支付8美元立即重置额度，跳过5小时冷却等待期，"
                    "重置后周度周期顺延7天，Codex/ChatGPT Work/智能体工具共享同一"
                    "使用池单次解锁全部产品，标志AI商业模式从纯订阅向订阅+按次"
                    "增购云化转型。",
        key_metrics={"model": "ChatGPT Plus额度重置",
                     "plus_monthly_usd": 20,
                     "reset_cost_usd": 8,
                     "cooling_period_h": 5,
                     "unlocks": ["ChatGPT对话", "Codex", "ChatGPT Work",
                                 "智能体工具"],
                     "business_model_shift": "订阅制→订阅+按次云服务",
                     "nature": "购买时间免除冷却等待"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="AI服务云化计费模式可参考机器人即服务(RaaS)商业模式设计",
        deployment_ready=True,
        tags=["OpenAI", "ChatGPT", "8美元重置", "云服务商业模式", "订阅+按次"],
    ),
    AIProduct(
        product_id="AG-024", name="Google Gemini Omni多模态创作模型",
        category=AICategory.AI_AGENT,
        organization="Google", country="美国",
        description="Google I/O 2026推出的全新创作模型，首次将Gemini推理能力与"
                    "创作能力深度融合，支持图像/文本/音频/视频自由组合输入，"
                    "通过对话式交互直接编辑视频内容，可模拟重力/动能等物理效果，"
                    "支持对话式视频剪辑与实时预览。Gemini Omni Flash首款型号"
                    "已上线Gemini应用。",
        key_metrics={"model": "Gemini Omni",
                     "flash_model": "Gemini Omni Flash",
                     "modalities": ["图像", "文本", "音频", "视频"],
                     "capabilities": ["对话式视频编辑", "物理效果模拟（重力/动能）",
                                     "实时预览", "多模态自由组合输入"],
                     "release_status": "Gemini应用付费用户可用",
                     "milestone": "从理解内容迈向实时创作与操控"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="多模态创作+物理效果模拟能力可用于机器人仿真训练"
                              "场景生成与世界模型构建",
        deployment_ready=True,
        tags=["Gemini Omni", "多模态创作", "视频编辑AI", "物理模拟", "Google I/O 2026"],
    ),
    AIProduct(
        product_id="NET-004", name="中国移动全国统一Token套餐资费",
        category=AICategory.NETWORK_6G,
        organization="中国移动", country="中国",
        description="面向公众市场和政企市场推出全国统一Token套餐资费，聚焦高频场景、"
                    "高价值客户，打造Token、模型、流量、终端、权益灵活组合按需"
                    "订购科技服务组合，加速AIDC（AI数据中心）投产。",
        key_metrics={"initiative": "全国统一Token套餐资费",
                     "target_markets": ["公众市场", "政企市场"],
                     "bundles": ["Token", "模型", "流量", "终端", "权益"],
                     "model": "灵活组合按需订购",
                     "infrastructure": "加速AIDC投产"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="运营商Token化计费为机器人云端AI服务规模化部署"
                              "提供网络+算力一体化商业基础",
        deployment_ready=True,
        tags=["中国移动", "Token套餐", "全国统一资费", "AIDC", "AI服务订阅"],
    ),
    AIProduct(
        product_id="CM-006", name="宇树科技2026年人形机器人累计下线1.25万台",
        category=AICategory.COMMERCE,
        organization="宇树科技", country="中国",
        description="截至8月12日，宇树科技2026年人形机器人累计生产下线数量约"
                    "12500台，月均出货量提升显著。8月10日科创板申购收官，发行价"
                    "150.80元/股，发行市值约610亿元，从受理到申购不到5个月创年内"
                    "最快IPO纪录；网上有效申购978.46万户刷新科创板历史，申购倍数"
                    "8288倍，中签率0.0181%，DeepSeek获配约1.41亿元，腾讯等战略"
                    "投资者入局。",
        key_metrics={"company": "宇树科技",
                     "2026_ytd_units": 12500,
                     "ipo_price_rmb": 150.80,
                     "ipo_market_cap_bn_rmb": 61,
                     "ipo_speed_record": "受理到申购不到5个月",
                     "subscribers_mn": 9.7846,
                     "subscription_multiple": 8288,
                     "winning_rate_pct": 0.0181,
                     "deepseek_allocation_rmb_mn": 141,
                     "strategic_investors": ["DeepSeek", "腾讯"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="万台级年下线标志着人形机器人正式进入规模化量产阶段，"
                              "资本深度绑定加速产业发展",
        deployment_ready=True,
        tags=["宇树科技", "1.25万台下线", "科创板IPO", "610亿市值", "8288倍申购",
              "DeepSeek战略投资", "腾讯投资"],
    ),
    AIProduct(
        product_id="CO-009", name="联想集团AI服务器储备订单3600亿元",
        category=AICategory.COMMERCE,
        organization="联想集团", country="中国",
        description="联想集团2026/27财年Q1营收269.43亿美元（约1834亿元）同比增长"
                    "43%，经调整净利润10.75亿美元（约73亿元）同比增长176%，"
                    "经调整净利润率4%。ISG基础设施方案业务营收579亿元同比增长"
                    "98%，运营利润约53亿元同比增98%，AI服务器储备订单从上季"
                    "1400亿元提高至3600亿元。",
        key_metrics={"company": "联想集团",
                     "quarter": "2026/27财年Q1",
                     "revenue_usd_bn": 26.943,
                     "revenue_yoy_growth_pct": 43,
                     "adj_profit_usd_bn": 1.075,
                     "adj_profit_yoy_growth_pct": 176,
                     "adj_net_margin_pct": 4,
                     "isg_revenue_rmb_bn": 57.9,
                     "isg_revenue_yoy_pct": 98,
                     "isg_op_profit_rmb_bn": 5.3,
                     "isg_op_profit_yoy_pct": 98,
                     "ai_server_backlog_rmb_bn": 360,
                     "prev_backlog_rmb_bn": 140},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="AI服务器储备订单爆发式增长为机器人云端训练与"
                              "推理算力基础设施提供充足供给",
        deployment_ready=True,
        tags=["联想集团", "AI服务器", "3600亿储备订单", "营收增长43%",
              "净利增长176%", "ISG业务翻倍"],
    ),
    AIProduct(
        product_id="AI-013", name="2026年中国AI芯片国产份额达90%",
        category=AICategory.AI_GENERAL,
        organization="中国半导体产业", country="中国",
        description="受美国芯片出口限制和中国本土芯片产能扩张影响，AMD和NVIDIA"
                    "在中国高端AI芯片市场份额2026年将降至10%，国产芯片占据90%。"
                    "2026年中国国产AI芯片出货量预计达到500万片，中芯国际和"
                    "上海华虹制造芯片未来几年出货量年复合增长率可达50%。"
                    "2026年中国AI芯片总供应量约240-260万颗，需求量约450万颗，"
                    "百万颗级供需缺口，2028年前难以闭合。华为升腾超130万颗、"
                    "寒武纪50-60万颗、海光超30万颗。",
        key_metrics={"year": 2026,
                     "nvidia_amd_market_share_pct": 10,
                     "domestic_market_share_pct": 90,
                     "domestic_shipment_mn_units": 5,
                     "smic_hhgrace_cagr_pct": 50,
                     "total_supply_mn_units": "2.4-2.6",
                     "total_demand_mn_units": 4.5,
                     "supply_gap_mn_units": "1.9-2.1",
                     "gap_close_year": 2028,
                     "huawei_ascend_shipment_k": 1300,
                     "cambricon_shipment_k": "500-600",
                     "hygon_shipment_k": 300},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="国产AI芯片90%份额为机器人端侧/云端算力提供"
                              "自主可控供应链保障，百万颗缺口带来产业机遇",
        deployment_ready=True,
        tags=["国产AI芯片", "90%份额", "500万片出货", "华为130万颗",
              "百万颗缺口", "中芯国际", "国产替代"],
    ),
    AIProduct(
        product_id="HC-013", name="ChatGPT健康功能",
        category=AICategory.HEALTHCARE,
        organization="OpenAI", country="美国",
        description="ChatGPT推出全新健康体验，美国18岁以上免费/Go/Plus/Pro用户"
                    "可安全连接受支持健康记录和Apple健康数据，通过仪表板查看健康"
                    "信息并结合个人健康背景提问，支持化验结果/用药/活动/睡眠"
                    "查看，可进行趋势探索/就诊准备/检查结果理解/健康目标追踪，"
                    "对话不用于训练基础模型或定向广告。旨在辅助而非取代医疗服务。",
        key_metrics={"product": "ChatGPT健康",
                     "available_regions": "美国",
                     "eligible_users": ["免费版", "ChatGPT Go", "Plus", "Pro"],
                     "age_requirement": 18,
                     "data_sources": ["健康记录", "Apple健康数据"],
                     "features": ["化验结果查看", "用药管理", "活动追踪",
                                  "睡眠监测", "健康趋势探索", "就诊准备",
                                  "检查结果理解", "健康目标追踪"],
                     "privacy": ["不用于基础模型训练", "不用于定向广告",
                                 "多层隐私安全防护"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="健康数据AI分析模式可为医疗陪护机器人、健康监测"
                              "机器人的人机对话与数据洞察设计提供参考",
        deployment_ready=True,
        tags=["ChatGPT健康", "AI健康助手", "Apple健康集成", "医疗AI",
              "隐私保护"],
    ),
    AIProduct(
        product_id="AGR-023", name="京东×时耘科技康养人形机器人合作",
        category=AICategory.AGRICULTURE,
        organization="京东×时耘科技", country="中国",
        description="京东与时耘科技深度共建，时耘输出机器人本体硬件与运动控制"
                    "能力，京东提供大模型作为智能大脑，共同发力康养赛道，落地"
                    "医疗问询、情绪陪伴、疗愈康养辅助等功能，打造康养人形机器人"
                    "解决方案。",
        key_metrics={"parties": ["京东", "时耘科技"],
                     "hardware": "时耘机器人本体+运动控制",
                     "brain": "京东大模型",
                     "focus_track": "康养赛道",
                     "capabilities": ["医疗问询", "情绪陪伴", "疗愈康养辅助"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="互联网大厂+机器人本体厂商合作模式为具身智能商业化"
                              "落地提供可复制路径",
        deployment_ready=False,
        tags=["京东时耘合作", "康养人形机器人", "医疗问询", "情绪陪伴",
              "大模型+本体"],
    ),
    AIProduct(
        product_id="ED-010", name="优必选U1预售破1.3万台",
        category=AICategory.EDUCATION,
        organization="优必选", country="中国",
        description="优必选Walker U系列首款消费级全尺寸超仿生人形机器人U1"
                    "预售订单突破13000台，Walker S系列在蔚来合肥工厂通过三个"
                    "月实地验证获量产准入资格，首批20台编入生产序列执行车门锁"
                    "检测与安全带安装任务。",
        key_metrics={"model": "Walker U1",
                     "preorder_units": 13000,
                     "walker_s_factory": "蔚来合肥工厂",
                     "walker_s_validation_months": 3,
                     "walker_s_batch": 20,
                     "walker_s_tasks": ["车门锁检测", "安全带安装"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="1.3万台预售+车企产线准入双轮驱动，标志人形机器人"
                              "消费端与工业端同时规模化突破",
        deployment_ready=False,
        tags=["优必选U1", "1.3万台预售", "Walker S蔚来产线", "量产准入",
              "消费级人形"],
    ),
    AIProduct(
        product_id="LW-011", name="中芯国际2026Q2营收30亿美元增长36%",
        category=AICategory.LIVELIHOOD,
        organization="中芯国际", country="中国",
        description="中芯国际2026年第二季度销售收入30.06亿美元同比增长36.06%，"
                    "毛利7.61亿美元，毛利率25.3%（Q1为20.1%，去年同期20.4%），"
                    "国产芯片制造产能持续扩张支撑AI芯片国产化。",
        key_metrics={"company": "中芯国际",
                     "quarter": "2026Q2",
                     "revenue_usd_bn": 3.006,
                     "revenue_yoy_pct": 36.06,
                     "gross_profit_usd_bn": 0.761,
                     "gross_margin_pct": 25.3,
                     "prev_q_margin_pct": 20.1,
                     "yoy_margin_pct": 20.4},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="晶圆代工产能扩张为机器人国产芯片提供制造基础",
        deployment_ready=True,
        tags=["中芯国际", "30亿美元营收", "增长36%", "毛利率25.3%", "国产晶圆代工"],
    ),
    AIProduct(
        product_id="EN-016", name="华为8500mAh巨鲸电池技术",
        category=AICategory.RENEWABLE_ENERGY,
        organization="华为", country="中国",
        description="华为新一代巨鲸电池技术，nova 16 SE首发搭载8500mAh超大容量，"
                    "为nova系列史上最大电池，配合66W Turbo超级快充，在保持机身"
                    "轻薄的同时实现超长续航，正常使用一天一充无压力，轻度使用"
                    "两天续航。",
        key_metrics={"tech": "巨鲸电池技术",
                     "capacity_mah": 8500,
                     "positioning": "nova系列最大电池",
                     "charge_w": 66,
                     "charge_tech": "Turbo超级快充",
                     "battery_life": ["正常使用一天一充", "轻度使用两天"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="高能量密度电池技术为移动机器人续航提升提供参考",
        deployment_ready=True,
        tags=["华为巨鲸电池", "8500mAh", "66W快充", "nova 16 SE首发", "超长续航"],
    ),
    AIProduct(
        product_id="HA-017", name="新思科技Synopsys自主化AI芯片设计工作流",
        category=AICategory.HOME_APPLIANCE,
        organization="新思科技×AMD×微软", country="美国",
        description="新思科技推出面向芯片设计的全新自主化智能体AI工作流，与AMD"
                    "联合开发，可在Microsoft Discovery平台评估，芯片开发周期"
                    "缩短40%，人工智能从根本层面重塑工程格局，加速从芯片到系统"
                    "全链路产品开发。",
        key_metrics={"product": "自主化智能体AI芯片设计工作流",
                     "developer": "新思科技",
                     "co_developer": "AMD",
                     "platform": "Microsoft Discovery",
                     "dev_cycle_reduction_pct": 40,
                     "scope": "从芯片到系统全链路"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="AI辅助芯片设计大幅缩短机器人专用芯片开发周期",
        deployment_ready=True,
        tags=["新思科技", "AI芯片设计", "AMD合作", "开发周期缩短40%", "智能体工作流"],
    ),
    AIProduct(
        product_id="WC-005", name="北京首批31家人形机器人养老服务试点社区",
        category=AICategory.WATER_CONSERVANCY,
        organization="北京", country="中国",
        description="2026世界机器人大会期间，首批31家人形机器人养老服务试点社区"
                    "在北京正式挂牌，人形机器人正式进入社区养老服务场景，提供"
                    "陪护、助行、健康监测等服务。",
        key_metrics={"initiative": "人形机器人养老服务试点社区",
                     "pilot_count": 31,
                     "location": "北京",
                     "services": ["陪护", "助行", "健康监测"],
                     "context": "2026世界机器人大会"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="人形机器人进入社区养老标志家政服务机器人规模化"
                              "落地开始，真实场景反馈加速产品迭代",
        deployment_ready=False,
        tags=["人形机器人养老", "31家试点社区", "北京挂牌", "养老服务机器人",
              "WRC2026"],
    ),
    AIProduct(
        product_id="RE-008", name="浪潮信息2026年超节点利润预计超50亿",
        category=AICategory.RENEWABLE_ENERGY,
        organization="浪潮信息", country="中国",
        description="浪潮信息2026年全年利润预计超50亿元，40倍PE对应约2000亿"
                    "市值预期，AI服务器与超节点整机业务高速增长，在国产超节点"
                    "市场预计占据30%份额。超节点海外单价约800万美元，2026年国内"
                    "超节点渗透率提升至20%，华勤技术超节点收入预计突破100亿。",
        key_metrics={"company": "浪潮信息",
                     "2026_profit_rmb_bn_est": 5,
                     "pe_ratio": 40,
                     "market_cap_rmb_bn_est": 200,
                     "supernode_market_share_pct": 30,
                     "overseas_unit_price_usd_mn": 8,
                     "china_penetration_2026_pct": 20,
                     "huaqin_supernode_rev_rmb_bn": 10},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="AI超节点算力基础设施大规模建设为机器人VLA模型"
                              "训练与集群推理提供算力保障",
        deployment_ready=True,
        tags=["浪潮信息", "50亿利润", "2000亿市值", "超节点30%份额", "AI算力基建"],
    ),
    AIProduct(
        product_id="LM-013", name="Gemini 3.5 Flash成谷歌全系默认模型",
        category=AICategory.WORLD_MODEL,
        organization="Google", country="美国",
        description="Gemini 3.5 Flash正式发布并成为Gemini全系列应用、谷歌搜索AI"
                    "模式全球默认模型，即刻向全球数十亿用户开放，性能超越前代"
                    "Gemini 3.1 Pro，速度快4倍、成本低一半，支持多步骤任务执行、"
                    "自动整理信息、自动调用工具、自动搜索、自动生成代码与应用，"
                    "主打高响应速度与实时交互体验。",
        key_metrics={"model": "Gemini 3.5 Flash",
                     "status": "谷歌全系默认模型",
                     "user_scale": "全球数十亿用户",
                     "perf_vs_31pro": "全面超越",
                     "speed_gain_x": 4,
                     "cost_reduction_pct": 50,
                     "capabilities": ["多步骤任务执行", "自动整理信息",
                                      "自动工具调用", "自动搜索",
                                      "自动代码生成", "应用生成"],
                     "optimization": "高响应速度/实时交互"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="高速低成本多模态模型为机器人实时推理与实时交互"
                              "提供大模型选项",
        deployment_ready=True,
        tags=["Gemini 3.5 Flash", "谷歌默认模型", "快4倍", "成本减半",
              "数十亿用户", "实时交互AI"],
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
