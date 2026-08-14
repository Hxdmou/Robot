#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI全景注册表 - 持续新增内容（3）
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
    ram_gb: Optional[int] = None
    rom_gb: Optional[int] = None
    price_start_rmb: Optional[float] = None
    maturity: MaturityLevel = MaturityLevel.COMMERCIAL
    source: str = ""
    source_tier: SourceTier = SourceTier.TIER3
    publish_date: str = ""
    relevance_to_robotics: str = ""
    deployment_ready: bool = False
    tags: List[str] = field(default_factory=list)


AI_LANDSCAPE_DB_PART3: List[AIProduct] = [

    AIProduct(
        product_id="WOR-010", name="戴盟机器人Daimon-TWM全球首个触觉锚定世界模型 蚂蚁领投数亿元融资加速3C/汽车产线落地",
        category=AICategory.WORLD_MODEL,
        organization="戴盟机器人", country="中国",
        description="戴盟机器人获蚂蚁集团领投数亿元融资，同步发布全球首个触觉锚定世界模型Daimon-TWM，"
                    "构建物理AI全栈能力，深度融合视觉/触觉/力觉多模态感知，为工业机器人提供高保真物理交互预测能力，"
                    "加速在3C电子、汽车制造等产线场景落地。",
        key_metrics={"model": "Daimon-TWM", "innovation": "全球首个触觉锚定世界模型",
                     "financing": "数亿元（蚂蚁集团领投，老股东超额跟投）",
                     "target_scenes": ["3C电子", "汽车制造", "工业装配"],
                     "capability": "视觉+触觉+力觉多模态融合，高保真物理交互预测"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="触觉锚定世界模型突破纯视觉世界模型物理交互精度不足瓶颈，让工业机器人对接触力、材质质感有真实理解，"
                              "直接提升精密装配、打磨抛光、柔性抓取等场景成功率，是工业具身智能落地核心基础设施",
        deployment_ready=True,
        tags=["Daimon-TWM", "触觉锚定世界模型", "戴盟机器人", "蚂蚁领投", "物理AI全栈", "3C装配", "汽车制造"]
    ),

    AIProduct(
        product_id="HUM-039", name="荣耀Honor Robot Phone全球首款量产具身机器人手机 四自由度钛合金灵巧云台预订破40万台9999元起",
        category=AICategory.HUMANOID_ROBOT,
        organization="荣耀终端有限公司", country="中国",
        description="8月12日晚荣耀在广州发布全球首款量产机器人手机Honor Robot Phone，首创四自由度钛合金灵巧云台，"
                    "电机仅2.6克体积缩小65%，0.8秒弹出360°旋转俯仰横滚，CIPA 5.5级物理防抖；"
                    "搭载第五代骁龙8至尊版、7060mAh青海湖电池、2亿像素云台主摄（联合ARRI电影级色彩）；"
                    "Agentic OS+YOYO Pro 300B参数伙伴智能体支持十几步连续指令跨App自动执行，单轮复杂任务成功率90.4%。",
        key_metrics={"model": "Honor Robot Phone", "version": ["12GB+512GB", "16GB+1TB"],
                     "price": {"12+512": 9999, "16+1TB": 12999},
                     "chip": "第五代骁龙8至尊版", "battery_mah": 7060,
                     "gimbal": "四自由度钛合金灵巧云台，电机2.6g，0.8秒弹出，CIPA 5.5级防抖",
                     "camera": "2亿像素云台主摄，ARRI LogC3电影级色彩，10bit 4K120帧",
                     "ai_agent": "Agentic OS + YOYO Pro 300B参数，单轮复杂任务成功率90.4%",
                     "pre_orders": 400000, "first_sale": "2026-08-18",
                     "benefit": "购机终身免费YOYO AI SVIP会员"},
        ram_gb=16, rom_gb=1024, price_start_rmb=9999,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="手机从'被动工具'升级为'具身伙伴'，四自由度机械云台是微型执行器在消费电子规模化落地的标志性产品，"
                              "Agentic OS跨App自动执行能力为机器人端侧智能体提供了消费级验证场景，开启手机形态第三条进化路线",
        deployment_ready=True,
        tags=["荣耀Robot Phone", "全球首款机器人手机", "四自由度钛合金云台", "第五代骁龙8至尊版", "Agentic OS", "YOYO Pro 300B",
              "预订40万台", "9999元起", "终身AI免费", "具身手机"]
    ),

    AIProduct(
        product_id="CHP-024", name="天数智芯天垓300 SIMT通用GPU架构新一代旗舰AI芯片 面向信息行动探索三大智能趋势",
        category=AICategory.AI_CHIP,
        organization="天数智芯（Daysilicon）", country="中国",
        description="8月14日WAIC 2026天数智芯正式发布新一代通用GPU旗舰产品天垓300，基于SIMT通用计算架构，"
                    "面向'信息、行动、探索'三大智能趋势，在芯片架构、关键算子、系统扩展、软件生态全面升级，"
                    "为大模型训练推理、具身智能、科学计算提供国产算力支撑。",
        key_metrics={"chip": "天垓300（TianGai 300）", "architecture": "SIMT通用计算架构",
                     "target_trends": ["信息智能", "行动智能", "探索智能"],
                     "upgrades": ["芯片架构", "关键算子", "系统扩展", "软件生态"],
                     "applications": ["大模型训练推理", "具身智能计算", "科学计算"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-14",
        relevance_to_robotics="天垓300SIMT架构升级为具身智能机器人训练和仿真提供国产通用GPU算力选项，"
                              "行动智能方向优化直接适配机器人运动控制、VLA模型推理等场景",
        deployment_ready=True,
        tags=["天数智芯", "天垓300", "SIMT通用GPU", "国产AI芯片", "WAIC 2026", "大模型训练", "具身智能算力"]
    ),

    AIProduct(
        product_id="CHP-025", name="联发科Dimensity 9500s/8500 3nm全大核Agentic AI芯片 OPPO/POCO首发",
        category=AICategory.AI_CHIP,
        organization="联发科技（MediaTek）", country="中国台湾",
        description="8月12日联发科发布天玑9500s和天玑8500两款移动AI芯片，旗舰9500s采用3nm工艺全大核架构，"
                    "支持光线追踪、8K Dolby Vision和先进Agentic AI能力；天玑8500采用4nm工艺主打极致能效；"
                    "OPPO、POCO确认将在下一代智能手机首发搭载，推动端侧Agentic AI体验普及。",
        key_metrics={"models": ["Dimensity 9500s", "Dimensity 8500"],
                     "9500s": {"process": "3nm", "architecture": "All-Big Core全大核", "features": ["光线追踪", "8K Dolby Vision", "Agentic AI"]},
                     "8500": {"process": "4nm", "positioning": "能效优先"},
                     "first_customers": ["OPPO", "POCO"], "positioning": "AI智能手机性能重新定义"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="端侧Agentic AI芯片能力持续提升，为机器人端侧大脑提供更高能效的移动计算平台选项，"
                              "全大核架构适配机器人多任务并发处理需求",
        deployment_ready=True,
        tags=["联发科天玑9500s", "天玑8500", "3nm全大核", "Agentic AI", "8K Dolby Vision", "OPPO首发", "端侧AI芯片"]
    ),

    AIProduct(
        product_id="DIG-028", name="谷歌Pixel 11系列Tensor G6改良版3nm 7核C1-Ultra超大核 苹果A20 Pro拿走2nm首发",
        category=AICategory.DIGITAL_PRODUCT,
        organization="Google", country="美国",
        description="谷歌正式发布Pixel 11系列四款机型（Pixel 11/Pro/Pro XL/Pro Fold），首发Tensor G6芯片；"
                    "谷歌确认Tensor G6采用台积电改良版3nm制程（此前误传2nm），7核设计含1颗C1-Ultra超大核（4109MHz）、"
                    "4颗C1-Pro高频大核+2颗C1-Pro低频大核；苹果A20 Pro将成为台积电2nm首发，由iPhone 18 Pro搭载。",
        key_metrics={"phones": ["Pixel 11", "Pixel 11 Pro", "Pixel 11 Pro XL", "Pixel 11 Pro Fold"],
                     "chip": "Tensor G6", "process": "台积电改良版3nm（非2nm）",
                     "cpu": "7核：1×C1-Ultra@4109MHz + 4×C1-Pro高频 + 2×C1-Pro低频",
                     "first_2nm_chip": "苹果A20 Pro（iPhone 18 Pro首发）"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="移动AI芯片工艺迭代为机器人端侧计算平台提供性能升级路径，Tensor G6端侧AI能力可迁移至移动机器人场景",
        deployment_ready=True,
        tags=["Google Pixel 11", "Tensor G6", "台积电3nm", "C1-Ultra超大核4.1GHz", "苹果A20 2nm首发", "AI手机"]
    ),

    AIProduct(
        product_id="IND-046", name="2026上半年全国工业机器人产量53.77万套同比+28.0% 服务机器人1031.92万套+11.9%",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="国家统计局", country="中国",
        description="国家统计局数据显示2026年上半年全国工业机器人产量达53.77万套，同比增长28.0%；"
                    "服务机器人产量达1031.92万套，同比增长11.9%；具身智能纳入国家未来产业布局，"
                    "制造业场景需求爆发，工业机器人从传统机械替代加速向具身智能终端跃迁。",
        key_metrics={"period": "2026年H1",
                     "industrial_robots": {"production": "53.77万套", "yoy_growth": "28.0%"},
                     "service_robots": {"production": "1031.92万套", "yoy_growth": "11.9%"},
                     "density": "2024年523台/万人，预计2030年破1000台/万人",
                     "2024_sales": "34万台，占全球近半份额",
                     "roi_period": "18个月以内",
                     "policy": "2026政府工作报告将具身智能纳入未来产业"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="工业机器人28%高速增长验证机器人产业规模化落地拐点已至，具身智能技术赋能让工业机器人从预编程走向自主决策，"
                              "国产替代加速（本土品牌份额从45%→56%），埃斯顿10.5%市占率登顶中国市场第一",
        deployment_ready=True,
        tags=["2026H1工业机器人53.77万套", "同比+28%", "服务机器人1031万套", "中国市场份额56%", "埃斯顿10.5%登顶",
              "具身智能入未来产业", "ROI 18个月"]
    ),

    AIProduct(
        product_id="AGR-006", name="法拉第未来FF 2026H1机器人业务首现正毛利 营收135万美元同比+264%净亏收窄40%",
        category=AICategory.AI_GENERAL,
        organization="Faraday Future", country="美国/中国",
        description="法拉第未来发布2026财年半年报：上半年营收135万美元同比暴增264.32%，净亏损8128万美元同比收窄40.1%；"
                    "关键突破是机器人业务首次实现正毛利，标志FF从纯电动车企业向'AI+电动车+机器人'科技公司转型取得实质性进展。",
        key_metrics={"period": "2026财年H1",
                     "revenue": "135万美元", "revenue_yoy": "+264.32%",
                     "net_loss": "8128万美元", "loss_yoy": "收窄40.1%",
                     "breakthrough": "机器人业务首次实现正毛利",
                     "transformation": "电动车→AI+电动车+机器人科技公司"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-14",
        relevance_to_robotics="车企跨界机器人业务实现正向毛利，验证汽车级供应链和制造能力向机器人迁移的商业可行性",
        deployment_ready=True,
        tags=["法拉第未来FF", "2026H1机器人正毛利", "营收+264%", "亏损收窄40%", "车企跨界机器人"]
    ),

    AIProduct(
        product_id="AUTO-029", name="希迪智驾2026H1营收8.04亿元同比+97% 无人矿卡出货超1900台毛利现金流双增长",
        category=AICategory.AUTOMOTIVE,
        organization="希迪智驾（CiDi）", country="中国",
        description="希迪智驾发布首份半年报：2026年上半年营收8.04亿元同比增长97%，其中自动驾驶收入7.84亿元占比97.6%；"
                    "毛利、现金流大幅增长，无人矿卡累计出货超1900台，矿区自动驾驶规模化商业化落地验证。",
        key_metrics={"period": "2026H1", "revenue": "8.04亿元", "revenue_yoy": "+97%",
                     "autonomous_driving_rev": "7.84亿元", "ad_rev_ratio": "97.6%",
                     "mine_truck_shipments": 1900,
                     "financial_highlights": ["毛利大幅增长", "现金流大幅改善"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-12",
        relevance_to_robotics="无人矿卡是特种机器人/自动驾驶在工业场景规模化落地标杆，1900台出货+97%营收增长验证封闭场景自动驾驶商业化成熟度，"
                              "为其他工业具身智能场景提供可复制路径",
        deployment_ready=True,
        tags=["希迪智驾", "2026H1营收8亿+97%", "无人矿卡1900台", "自动驾驶收入97.6%", "矿区自动驾驶", "规模化落地"]
    ),

    AIProduct(
        product_id="COM-011", name="微视中国全球首个具身智能机器人直播平台亮相上海EAI展 7×24小时无人值守直播+情绪识别自动互动",
        category=AICategory.COMMERCE,
        organization="微视中国/上海心浪科技", country="中国",
        description="8月12-14日上海EAI具身智能展，中国互联网新闻中心出品、心浪科技运营的《微视中国》全球首个具身智能机器人直播平台亮相；"
                    "构建'流量大脑-算法大脑-物理身体'三位一体闭环，支持7×24小时无人值守开播，情绪识别实时解析弹幕自动互动应答商品推介；"
                    "已落地进博会跨境直播、汽车展厅、文旅景区、养老陪护、文艺演出等场景。",
        key_metrics={"platform": "微视中国机器人直播平台", "architecture": "流量大脑+算法大脑+物理身体三位一体",
                     "capability": ["7×24小时无人值守开播", "情绪识别实时解析弹幕", "自动互动应答/商品推介/打赏回馈"],
                     "scenarios": ["进博会跨境直播", "汽车展厅", "文旅景区", "企业前台", "养老陪护", "文艺演出"],
                     "cross_border": "多语种交互助力中国企业出海",
                     "ecosystem": "资讯/商城/艺术赛事/俱乐部/OPC一人公司系统"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="服务机器人在直播电商场景规模化落地，多模态情绪识别+自主交互决策验证了人形机器人在商业服务场景的实用价值，"
                              "'AI算法+实体硬件+流量入口'闭环模式为消费级/商用服务机器人商业化提供新路径",
        deployment_ready=True,
        tags=["微视中国", "全球首个机器人直播平台", "7×24无人直播", "情绪识别弹幕互动", "三位一体闭环", "上海EAI展", "跨境直播"]
    ),

    AIProduct(
        product_id="AGN-031", name="LangChain Deep Agents开源生产级Agent框架0.7.6发布 长周期多步任务模型无关开箱即用",
        category=AICategory.AI_AGENT,
        organization="LangChain AI", country="美国",
        description="8月14日LangChain Deep Agents开源Agent框架持续更新（最新commit 822f7c9，版本0.7.6），"
                    "定位为'batteries-included'生产级Agent框架，默认参数针对长周期多步任务优化，可扩展可替换任意组件无需fork；"
                    "模型无关设计支持任意工具调用LLM（前沿/开源/本地均可），基于LangGraph构建生产就绪。",
        key_metrics={"framework": "LangChain Deep Agents", "version": "0.7.6",
                     "latest_commit": "2026-08-14", "commits": "3289+",
                     "principles": ["Opinionated长周期任务优化默认参数", "Extensible任意组件可替换无需fork",
                                   "Model-agnostic支持任意工具调用LLM", "Production-ready基于LangGraph"],
                     "license": "开源"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="生产级Agent框架为机器人任务规划、工具调度、长时序作业提供开箱即用的软件基础设施，"
                              "模型无关设计让机器人开发者可灵活接入VLA/LLM/VLM等各类模型",
        deployment_ready=True,
        tags=["LangChain Deep Agents", "开源Agent框架", "生产级", "长周期任务", "模型无关", "LangGraph", "0.7.6版"]
    ),

    AIProduct(
        product_id="LLM-053", name="NVIDIA Nemotron-3.5 Lightning 30B MoE开源常驻Agent模型 3B激活单GPU可跑",
        category=AICategory.AI_LLM,
        organization="NVIDIA", country="美国",
        description="Ollama更新显示NVIDIA Nemotron-3.5 Lightning已上线（更新于2天前），30B MoE架构仅3B激活参数，"
                    "专为常驻Always-on Agent设计，单GPU即可运行，工具调用、长任务执行、故障恢复能力优化。",
        key_metrics={"model": "Nemotron-3.5 Lightning", "organization": "NVIDIA",
                     "architecture": "30B MoE混合专家", "active_params_billion": 3,
                     "target": "Always-on常驻Agent", "deployment": "单GPU可运行",
                     "optimizations": ["工具调用", "长任务执行", "故障恢复"],
                     "availability": "Ollama可拉取", "updated": "2天前（8月12日）"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="3B激活30B MoE架构实现高能力与低算力消耗平衡，常驻Agent设计适合机器人端侧持续运行场景，"
                              "单GPU即可部署大幅降低机器人智能体算力门槛",
        deployment_ready=True,
        tags=["NVIDIA Nemotron-3.5", "30B MoE 3B激活", "常驻Agent", "单GPU可跑", "工具调用优化", "Ollama上线", "端侧Agent"]
    ),

    AIProduct(
        product_id="AGN-032", name="Qwen 3.6持续更新Ollama 3小时前更新 Agentic编码与思考保留能力大幅提升",
        category=AICategory.AI_AGENT,
        organization="阿里巴巴通义实验室", country="中国",
        description="Ollama显示Qwen 3.6于3小时前（8月14日）更新，在Agentic编码和思考保留（thinking preservation）方面"
                    "相比前代Qwen模型实现大幅升级，27B/35B等多规格支持视觉、工具调用、思考模式，开源生态持续快速迭代。",
        key_metrics={"model": "Qwen 3.6", "organization": "阿里巴巴通义实验室",
                     "update_time": "2026-08-14（3小时前）",
                     "improvements": ["Agentic Coding智能体编码能力大幅提升", "Thinking Preservation思考保留能力增强"],
                     "features": ["多模态视觉", "工具调用", "思考模式", "云端/本地部署"],
                     "downloads": "Ollama累计570万+ Pulls",
                     "ecosystem": "开源可商用"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="Qwen 3.6 Agent编码和思考保留能力提升让机器人可以更好地理解任务指令、保留操作中间状态、执行多步复杂任务，"
                              "开源免费可商用降低机器人AI大脑部署成本",
        deployment_ready=True,
        tags=["Qwen 3.6", "通义千问", "Agentic Coding", "思考保留", "多模态", "开源", "Ollama", "2026-08-14更新"]
    ),

    AIProduct(
        product_id="AGR-007", name="鹿明机器人联席CTO丁琰离职任期不足280天 核心团队陆续出走技术路线分歧",
        category=AICategory.AI_GENERAL,
        organization="鹿明机器人", country="中国",
        description="DoNews 8月13日消息，鹿明机器人联席CTO丁琰已于近期离职，任期不足280天，因技术分歧出走；"
                    "其独资公司快米数据已转股退出，丁琰此前带入的团队也已陆续离职，与鹿明及老东家一星机器人存在地域和业务关联。",
        key_metrics={"event": "联席CTO离职", "person": "丁琰",
                     "tenure_days": "<280天", "reason": "技术路线分歧",
                     "team_status": "此前带入团队已陆续出走", "related_company": "快米数据已转股退出",
                     "industry_context": "具身智能创业公司人才流动加速，技术路线分化期"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-13",
        relevance_to_robotics="具身智能创业公司核心技术高管变动反映行业技术路线仍在快速探索分化期，人才流动加速也说明行业竞争白热化",
        deployment_ready=False,
        tags=["鹿明机器人", "CTO丁琰离职", "任期不足280天", "技术分歧", "团队出走", "具身智能人才流动"]
    ),

    AIProduct(
        product_id="AGR-008", name="宇树科技8月10日申购网上中签率仅0.02%-0.05% 发行价150.8元市值约610亿",
        category=AICategory.AI_GENERAL,
        organization="宇树科技（Unitree）", country="中国",
        description="宇树科技8月10日启动申购，发行价150.80元/股，发行市值约609.93亿元，网上中签率仅0.02%-0.05%，"
                    "属高门槛低中签率热门新股；拟募资约60.99亿元投向四大机器人项目；2023-2025年营收复合增速超200%已实现盈利，"
                    "将成'A股人形机器人第一股'。",
        key_metrics={"ipo_date": "2026-08-10申购", "issue_price": 150.80,
                     "market_cap": "约609.93亿元", "fundraising": "约60.99亿元",
                     "online_lottery_rate": "0.02%-0.05%（极低）",
                     "revenue_cagr_2023_2025": ">200%", "profit_status": "已实现盈利",
                     "position": "A股人形机器人第一股",
                     "fund_use": "四大机器人项目"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-10",
        relevance_to_robotics="宇树科技IPO为人形机器人整机企业建立A股估值锚，200%+营收增速+盈利验证四足/人形机器人规模化商业化能力，"
                              "上市后融资将加速产品迭代和产能扩张，带动上游零部件供应链重定价",
        deployment_ready=True,
        tags=["宇树科技IPO", "发行价150.8元", "市值610亿", "中签率0.02-0.05%", "人形机器人第一股", "营收CAGR200%+", "已盈利"]
    ),

    AIProduct(
        product_id="AGR-009", name="原字节跳动机器人负责人孔涛2025年夏加盟小米 任机器人基座模型团队负责人",
        category=AICategory.AI_GENERAL,
        organization="小米集团", country="中国",
        description="8月9日消息，原字节跳动机器人团队负责人孔涛于2025年夏加盟小米，担任机器人基座模型团队负责人，"
                    "该团队高度保密且独立办公，小米加速布局具身智能大模型技术栈，为消费级机器人产品铺路。",
        key_metrics={"person": "孔涛（原字节机器人负责人）", "join_date": "2025年夏",
                     "company": "小米", "position": "机器人基座模型团队负责人",
                     "team_status": "高度保密，独立办公",
                     "significance": "小米加码具身智能大模型，巨头人才争夺白热化"},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-09",
        relevance_to_robotics="互联网大厂AI人才向机器人/具身智能领域流动加速，小米组建独立基座模型团队预示手机厂商将深度布局机器人赛道",
        deployment_ready=False,
        tags=["孔涛", "字节跳动机器人", "小米机器人", "基座模型团队", "巨头人才争夺", "具身智能大模型"]
    ),

    AIProduct(
        product_id="AGR-010", name="前小鹏副总裁陈永海2026年1月加入众擎机器人任运营总裁 B轮2亿美元估值超100亿",
        category=AICategory.AI_GENERAL,
        organization="众擎机器人", country="中国",
        description="前小鹏产品副总裁陈永海于2025年12月离职小鹏，2026年1月加入众擎机器人担任运营总裁；"
                    "众擎机器人成立于2023年下半年，B轮融资2亿美元，估值超100亿元人民币，加速人形机器人量产和商业化落地。",
        key_metrics={"person": "陈永海（前小鹏产品副总裁）", "join_date": "2026年1月",
                     "company": "众擎机器人", "position": "运营总裁",
                     "founded": "2023年下半年", "b_round": "2亿美元",
                     "valuation": ">100亿元人民币",
                     "background": "小鹏汽车高管加盟，车企人才加速流入机器人行业"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-07",
        relevance_to_robotics="车企运营和量产经验向人形机器人行业迁移，众擎100亿估值+B轮2亿美元验证资本对人形机器人赛道持续高热度",
        deployment_ready=True,
        tags=["陈永海", "小鹏副总裁", "众擎机器人", "运营总裁", "B轮2亿美元", "估值超100亿", "车企人才流入"]
    ),

    AIProduct(
        product_id="REN-052", name="阳光电源PowerTitan 2获智利152MW/606MWh储能订单+海辰储能澳大利亚订单合计超1GWh",
        category=AICategory.RENEWABLE_ENERGY,
        organization="阳光电源/海辰储能", country="中国",
        description="8月14日消息中国储能企业出海再突破：阳光电源获智利Verano Energy Observatorio项目152MW/606MWh储能订单，"
                    "采用PowerTitan 2液冷储能系统+135MW光伏SG350HX-20逆变器；海辰储能同期获澳大利亚储能订单，两家合计超1GWh。",
        key_metrics={"orders": {"sungrow": {"project": "智利Observatorio光储项目", "capacity_mwh": 606,
                                            "solution": "PowerTitan 2液冷BESS + SG350HX-20逆变器",
                                            "pv_capacity_mw": 135},
                               "hithium": "澳大利亚储能订单"},
                     "total_gwh": ">1GWh",
                     "background": "2026年1-7月国内储能公开订单861.15GWh，同比+149.30%"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="储能大规模出海为AIDC（AI数据中心）和机器人充电基础设施提供能源底座，液冷储能技术直接适配高算力密度AI数据中心需求",
        deployment_ready=True,
        tags=["阳光电源", "智利606MWh", "PowerTitan 2", "海辰储能", "澳大利亚订单", "合计超1GWh", "储能出海"]
    ),

    AIProduct(
        product_id="REN-053", name="博时储能587Ah大容量长时储能电芯PACK产线贯通 嘉善基地首套产品下线",
        category=AICategory.RENEWABLE_ENERGY,
        organization="博时储能", country="中国",
        description="8月11日博时储能宣布嘉善智造基地587Ah大容量长时储能电芯专用PACK自动化产线完成全线安装调试贯通，"
                    "首套产品正式下线，专为大容量长时储能赛道打造，适配电网侧长时调峰、新能源配储等场景。",
        key_metrics={"company": "博时储能", "cell_capacity_ah": 587,
                     "base": "嘉善智造基地", "event": "PACK自动化产线贯通，首套产品下线",
                     "target_segment": "大容量长时储能",
                     "scenarios": ["电网侧长时调峰", "新能源配储", "工商业储能"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-13",
        relevance_to_robotics="大容量储能电芯技术进步为机器人换电站、移动机器人能源补给、AI工厂备电提供更高能量密度解决方案",
        deployment_ready=True,
        tags=["博时储能", "587Ah电芯", "PACK产线贯通", "嘉善基地", "长时储能", "大容量电芯"]
    ),

    AIProduct(
        product_id="REN-054", name="晶澳科技杭州光储充渠道会签约6家企业 发布光储+X系统方案解构X重构收益",
        category=AICategory.RENEWABLE_ENERGY,
        organization="晶澳科技（JA Solar）", country="中国",
        description="8月14日晶澳联合启盛新材料、史陶比尔在杭州举办光储充渠道交流会，聚焦'解构X·重构收益'，"
                    "直面行业深度调整，提出从'装光伏'到'算收益'转型路径，发布'光储+X'系统融合方案，并签约6家本地企业，"
                    "加速光储智一体化在浙江落地。",
        key_metrics={"event": "晶澳光储充杭州渠道会", "date": "2026-08-14",
                     "theme": "解构X·重构收益，从装光伏到算收益",
                     "partners": ["启盛新材料", "史陶比尔"],
                     "solution": "光储+X系统融合方案", "signings": 6,
                     "region": "浙江杭州"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-14",
        relevance_to_robotics="光储充一体化为机器人充电网络、AI工厂分布式能源提供本地化绿色电力方案",
        deployment_ready=True,
        tags=["晶澳科技", "光储+X", "杭州渠道会", "签约6家", "光储充一体化", "从装光伏到算收益"]
    ),

    AIProduct(
        product_id="REN-055", name="绿能中环分布式光伏四可解决方案7天交付 赋能3000+电站覆盖12省",
        category=AICategory.RENEWABLE_ENERGY,
        organization="绿能中环", country="中国",
        description="《新型电力系统建设'十五五'规划》落地，'四可'（看得见、算得清、管得住、调得动）成分布式光伏并网硬性要求；"
                    "绿能中环推出轻量化、不停产、快交付四可解决方案，7天交付、全协议兼容、南网国网双认证，"
                    "已赋能3000+电站、覆盖12省，助力工商业光伏合规高效接入新型电力系统。",
        key_metrics={"solution": "分布式光伏四可解决方案",
                     "four_ables": ["看得见", "算得清", "管得住", "调得动"],
                     "advantages": ["轻量化", "不停产", "7天交付", "全协议兼容", "南网/国网双认证"],
                     "track_record": {"stations": 3000, "provinces": 12},
                     "policy_basis": "十五五新型电力系统规划硬性要求"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-14",
        relevance_to_robotics="分布式光伏智能化管控为AI工厂、机器人充电站提供本地化智能微网方案，"
                              "'调得动'能力可响应AI算力负荷波动实现源网荷储协同",
        deployment_ready=True,
        tags=["绿能中环", "分布式光伏四可", "7天交付", "3000+电站12省", "南网国网双认证", "十五五规划"]
    ),

    AIProduct(
        product_id="AGR-011", name="安波福2026H1营收63亿美元净利润4.27亿 完成EDS拆分获19亿现金股利加速机器人拓展",
        category=AICategory.AI_GENERAL,
        organization="Aptiv安波福", country="爱尔兰/美国",
        description="安波福发布2026年上半年财报：H1营收63亿美元，Q2营收33亿美元同比+2%，净利润2.98亿美元（H1合计4.27亿）；"
                    "完成EDS（电气分配系统）业务拆分获19亿美元现金股利；非汽车及机器人业务加速拓展。",
        key_metrics={"period": "2026H1", "h1_revenue": "63亿美元", "h1_net_profit": "4.27亿美元",
                     "q2_revenue": "33亿美元（+2%）", "q2_net_profit": "2.98亿美元",
                     "eds_spinoff": "完成拆分，获19亿美元现金股利",
                     "new_business": "非汽车及机器人业务加速拓展"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER3,
        publish_date="2026-08-05",
        relevance_to_robotics="汽车Tier1巨头分拆传统业务并加速机器人领域拓展，汽车线束/电控/传感器技术可向机器人领域迁移",
        deployment_ready=True,
        tags=["安波福Aptiv", "2026H1营收63亿", "净利润4.27亿", "EDS拆分获19亿", "机器人业务加速", "汽车零部件跨界"]
    ),

    AIProduct(
        product_id="REN-056", name="罗马尼亚Dama Solar欧洲最大光储电站扩容至1.2GW 配套储能2028年投产",
        category=AICategory.RENEWABLE_ENERGY,
        organization="Rezolv Energy", country="罗马尼亚",
        description="Rezolv Energy开发的Dama Solar光伏项目获罗马尼亚ANRE建设批准，规划装机从1.04GW扩容至1.2GW，"
                    "配套储能系统，预计2028年投产，建成后将成为欧盟在运规模最大光伏电站，"
                    "项目位于阿拉德县，在罗马尼亚第二次CfD拍卖中获两份差价合约。",
        key_metrics={"project": "Dama Solar", "developer": "Rezolv Energy",
                     "capacity_gw": 1.2, "original_capacity_gw": 1.04,
                     "storage": "配套电池储能系统（罗马尼亚最大）",
                     "commissioning": "2028年", "status": "获ANRE建设批准",
                     "position": "欧盟最大在运光储电站", "location": "罗马尼亚阿拉德县"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-14",
        relevance_to_robotics="欧洲GW级光储电站建设为AI数据中心和高耗能机器人产业提供大规模绿色电力支撑",
        deployment_ready=False,
        tags=["Dama Solar", "1.2GW光储", "欧盟最大", "罗马尼亚", "2028年投产", "Rezolv Energy", "光储大基地"]
    ),

    AIProduct(
        product_id="EMB-037", name="第二届世界人形机器人运动会8月22日冰丝带开幕 16国666队2056台机器人参赛",
        category=AICategory.EMBODIED_INTELLIGENCE,
        organization="世界人形机器人运动会组委会", country="中国",
        description="8月13日新闻发布会宣布，第二届世界人形机器人运动会将于8月22-26日在国家速滑馆'冰丝带'举办，"
                    "设置51个项目、开展1301场比赛，吸引全球16个国家666支队伍、2056台机器人同台竞技，"
                    "参赛队伍较首届增长138%，机器人数量翻两番。新增跳远、举重、拔河、乒乓球等高强度对抗项目，"
                    "灵巧手赛项设粉末称量、镊子夹豆、开瓶撬盖等8个微操作赛项，场景赛覆盖工业、酒店、家庭、物流等9大真实场景。",
        key_metrics={"event": "第二届世界人形机器人运动会", "dates": "2026-08-22至26",
                     "venue": "国家速滑馆冰丝带", "countries": 16, "teams": 666, "robots": 2056,
                     "events": 51, "matches": 1301, "team_growth": "+138%", "robot_growth": "4倍",
                     "new_events": ["跳远", "举重", "拔河", "乒乓球", "灵巧手8项微操"],
                     "scenes": ["工业", "酒店", "家庭", "物流", "应急救援"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="全球顶级人形机器人赛事推动关节电机、减速器、灵巧手等核心零部件技术极限突破，"
                              "'以赛定标、以标促产'加速技术验收标准形成，'得了奖牌就拿订单'加速商业化落地",
        deployment_ready=True,
        tags=["世界人形机器人运动会", "冰丝带", "16国666队", "2056台机器人", "51项目1301场", "灵巧手赛项", "以赛定标"]
    ),

    AIProduct(
        product_id="DIG-030", name="华为nova 16 SE正式开售 麒麟8020+鸿蒙OS 6.1 8500mAh巨鲸电池2499元起",
        category=AICategory.DIGITAL_PRODUCT,
        organization="华为", country="中国",
        description="华为nova 16 SE于8月12日正式开售，起售价2499元。首次将多项旗舰技术下放至2500元价位："
                    "搭载麒麟8020芯片与鸿蒙OS 6.1，整机性能较前代提升约52%；影像引入旗舰同源红枫原色影像，"
                    "后置5000万像素RYYB主摄；内置8500mAh巨鲸电池支持66W快充；支持双向北斗卫星消息，"
                    "将卫星通信能力带入两千元档。屏幕为6.84英寸OLED直屏，120Hz高刷+2160Hz高频PWM调光，峰值亮度8000尼特。",
        key_metrics={"model": "华为nova 16 SE", "chip": "麒麟8020", "os": "鸿蒙OS 6.1",
                     "screen": "6.84英寸OLED直屏 120Hz 2160Hz PWM 峰值8000nit",
                     "battery_mah": 8500, "charging_w": 66,
                     "camera": "5000万像素RYYB主摄（红枫原色影像）",
                     "satellite": "双向北斗卫星消息",
                     "performance_gain": "+52%", "price_start_rmb": 2499},
        ram_gb=12, rom_gb=256, price_start_rmb=2499,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-12",
        relevance_to_robotics="麒麟8020端侧AI算力与鸿蒙OS分布式能力可迁移至机器人边缘计算节点，"
                              "北斗卫星通信为户外作业机器人提供无盲区通信保障",
        deployment_ready=True,
        tags=["华为nova 16 SE", "麒麟8020", "鸿蒙OS 6.1", "8500mAh", "2499元起", "双向北斗卫星", "红枫原色影像"]
    ),

    AIProduct(
        product_id="DIG-031", name="华为三款鸿蒙电脑8月14日正式开售 MateBook Fold非凡大师24999元起",
        category=AICategory.DIGITAL_PRODUCT,
        organization="华为", country="中国",
        description="8月14日华为三款鸿蒙电脑正式开售：MateBook Fold非凡大师起售价24999元，搭载18英寸折叠屏与HarmonyOS 6.1，"
                    "展开最薄7.3mm；MateBook Pro S起售价7999元，仅798g、厚11.9mm，首发麒麟XE90芯片；"
                    "MateBook Pro起售价9999元。鸿蒙电脑生态持续完善，与手机、平板、智能家居实现跨设备无缝协同。",
        key_metrics={"models": ["MateBook Fold非凡大师", "MateBook Pro S", "MateBook Pro"],
                     "fold_price_start": 24999, "pros_price_start": 7999, "pro_price_start": 9999,
                     "fold_screen": "18英寸折叠屏 HarmonyOS 6.1 最薄7.3mm",
                     "pros_chip": "麒麟XE90", "pros_weight_g": 798, "pros_thickness_mm": 11.9,
                     "os": "HarmonyOS 6.1", "sale_date": "2026-08-14"},
        ram_gb=16, rom_gb=512, price_start_rmb=7999,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="鸿蒙分布式操作系统跨设备协同能力为机器人多终端控制、人机交互界面提供成熟技术参考，"
                              "麒麟XE90芯片能效比设计可迁移至机器人嵌入式计算平台",
        deployment_ready=True,
        tags=["华为鸿蒙电脑", "MateBook Fold非凡大师", "24999元起", "MateBook Pro S 798g", "麒麟XE90", "HarmonyOS 6.1", "8月14日开售"]
    ),

    AIProduct(
        product_id="DIG-032", name="小米澎湃OS 4官宣Beta测试招募 清空MIUI冗余流畅度提升40% 超级小爱2.0",
        category=AICategory.AI_SOFTWARE,
        organization="小米集团", country="中国",
        description="8月13日小米官方正式官宣澎湃OS 4，主要升级：①底层流畅大优化，清空MIUI遗留冗余代码，"
                    "内核新增负载精算、内存预载技术，系统精简瘦身，流畅度提升40%；②全新柔光玻璃UI，"
                    "通透柔和双视觉模式，图标重绘、光影随动作动态变化；③AI全面升级，搭载超级小爱2.0+端侧自研大模型，"
                    "可连贯执行多步骤复杂指令，离线AI可用，跨设备互联更顺畅。首批支持小米17系列、REDMI K90系列、小米平板8系列，"
                    "8月14日下午起陆续推送Beta安装包。",
        key_metrics={"os": "小米澎湃OS 4", "announce_date": "2026-08-13",
                     "beta_push": "2026-08-14下午起",
                     "upgrades": {"fluidity_gain": "+40%", "ui": "柔光玻璃UI 双视觉模式",
                                  "ai": "超级小爱2.0 端侧自研大模型 离线AI可用 多步指令连贯执行"},
                     "first_batch_devices": ["小米17系列", "REDMI K90系列", "小米平板8/8 Pro"],
                     "optimizations": ["清空MIUI冗余代码", "负载精算", "内存预载", "系统精简瘦身"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="超级小爱2.0端侧多步指令执行能力、跨设备互联架构可直接迁移至机器人任务规划与多机协同系统，"
                              "内存预载、负载精算技术对机器人实时系统优化具有参考价值",
        deployment_ready=True,
        tags=["小米澎湃OS 4", "流畅度+40%", "超级小爱2.0", "端侧大模型", "离线AI", "MIUI冗余清理", "Beta测试"]
    ),

    AIProduct(
        product_id="LLM-051", name="OpenAI GPT-5.6 Sol Ultrafast模式预览 速度提升14倍每秒750tokens Cerebras硬件支持",
        category=AICategory.LLM,
        organization="OpenAI", country="美国",
        description="8月14日OpenAI CEO Sam Altman通过Twitter预览GPT-5.6 Sol Ultrafast新模式，"
                    "宣称在保持前沿模型能力不变的前提下，运行速度最高提升14倍，输出速度达每秒750个tokens，"
                    "由Cerebras晶圆级系统提供推理硬件支持。该模式将首先通过OpenAI API向特定客户群体推出，"
                    "随着算力容量增长逐步向更多企业开放，目前未披露定价策略及全面开放时间表。",
        key_metrics={"model": "GPT-5.6 Sol Ultrafast", "announce_date": "2026-08-14",
                     "speed_gain": "最高14倍", "tokens_per_second": 750,
                     "hardware": "Cerebras晶圆级推理系统",
                     "capability_note": "保持前沿模型能力不降级（未切换小模型）",
                     "access": "API向特定客户开放 逐步扩大"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="超高推理速度（750tokens/s）使大模型在机器人实时控制、动态避障、即时任务重规划场景中达到实用化延迟要求，"
                              "晶圆级推理硬件方案为机器人高算力低延迟需求提供新路径",
        deployment_ready=True,
        tags=["OpenAI GPT-5.6 Sol", "Ultrafast模式", "速度14倍", "750tokens/s", "Cerebras", "晶圆级推理", "API预览"]
    ),

    AIProduct(
        product_id="LLM-052", name="OpenAI发布GPT-5.6-Cyber安全专用模型 Daybreak Red分级审批95%请求完成率",
        category=AICategory.LLM,
        organization="OpenAI", country="美国",
        description="8月10日OpenAI发布GPT-5.6-Cyber安全专用模型，需通过Daybreak Red项目单独审批，"
                    "面向授权防御性安全研究人员。定价：输入$12.50/百万tokens，输出$75/百万tokens（约为Sol的2.5倍），"
                    "长上下文（>272K）2倍输入+1.5倍输出。内部评测高级安全请求完成率达95%，已发现Chrome V8高危漏洞，"
                    "9月1日起Daybreak账户强制硬件安全密钥。",
        key_metrics={"model": "GPT-5.6-Cyber", "release_date": "2026-08-10",
                     "pricing_input": "$12.50/百万tokens", "pricing_output": "$75/百万tokens",
                     "completion_rate": "95%", "access_control": "Daybreak Red审批制",
                     "use_case": "授权漏洞研究、渗透测试、红队演练、漏洞验证",
                     "security_key": "9月1日起强制硬件安全密钥"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-10",
        relevance_to_robotics="专用模型领域细分思路为机器人安全审计、工控系统漏洞挖掘、机器人网络安全防护提供专业化大模型应用范式",
        deployment_ready=True,
        tags=["GPT-5.6-Cyber", "安全专用模型", "Daybreak Red", "95%完成率", "Chrome漏洞发现", "$12.5/$75定价", "授权防御"]
    ),

    AIProduct(
        product_id="LLM-053", name="Qwen3.8-Max开放权重发布 2.4万亿总参数950亿激活262K上下文",
        category=AICategory.LLM,
        organization="阿里巴巴", country="中国",
        description="8月13日Qwen3.8-Max完成开放权重发布：总参数2.4万亿、单词元激活950亿（MoE架构），"
                    "原生上下文262144词元（256K）并可扩展至约101万。支持可调推理强度，面向数据中心级部署场景，"
                    "是目前开放权重模型中参数规模最大的模型之一。需注意新许可证条款和数据中心级部署成本。",
        key_metrics={"model": "Qwen3.8-Max", "release_date": "2026-08-13",
                     "total_params": "2.4万亿", "active_params": "950亿", "architecture": "MoE混合专家",
                     "context_window": "262144 tokens（原生）/ ~101万（扩展）",
                     "license": "新开放权重许可证（需关注商用条款）",
                     "target": "数据中心级部署"},
        ram_gb=0, rom_gb=0, price_start_rmb=0,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="2.4万亿参数级开放权重模型为机器人云端大脑、多模态感知融合、长时序任务记忆提供超强算力基础选项，"
                              "MoE架构950亿激活参数在能力与推理成本间取得平衡",
        deployment_ready=True,
        tags=["Qwen3.8-Max", "2.4万亿参数", "950亿激活", "MoE", "262K上下文", "开放权重", "数据中心级"]
    ),

    AIProduct(
        product_id="ROB-076", name="英伟达与LG宣布拓展AI基础设施及机器人领域合作 物理AI成重点方向",
        category=AICategory.HUMANOID_ROBOT,
        organization="NVIDIA + LG集团", country="美国/韩国",
        description="8月14日英伟达发布官方消息，欢迎LG集团会长具光谟及高管团队到访，双方宣布将围绕"
                    "AI基础设施、物理AI（Physical AI）和机器人领域拓展合作。英伟达表示对双方团队未来合作成果充满期待，"
                    "具体合作内容、项目细节及投资规模未在本次发布中披露。此前LG已与英伟达在GR00T人形机器人项目有合作基础。",
        key_metrics={"parties": ["NVIDIA", "LG集团"], "announce_date": "2026-08-14",
                     "cooperation_areas": ["AI基础设施", "物理AI Physical AI", "机器人"],
                     "existing_cooperation": "GR00T双足人形机器人项目（2027Q1推出）",
                     "details_released": False},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="全球AI算力龙头与消费电子/家电巨头深化合作，物理AI作为重点方向将加速人形机器人、"
                              "服务机器人在家庭、商业场景的落地进程，LG家电场景+英伟达算力模型形成强协同",
        deployment_ready=True,
        tags=["英伟达LG合作", "AI基础设施", "物理AI", "机器人", "具光谟到访", "GR00T基础", "8月14日宣布"]
    ),

    AIProduct(
        product_id="AIA-028", name="Perplexity推出Agent API 多步研究代码执行内置工具 性能超Sonar两倍",
        category=AICategory.AI_AGENT,
        organization="Perplexity AI", country="美国",
        description="8月14日Perplexity CEO Aravind Srinivas宣布Sonar将迁移至新Agent API，"
                    "在保持接地网页搜索（grounded web search）基础上，新增多步研究、代码执行、内置工具能力，"
                    "可通过单一API访问多个模型。官方声称在BrowseComp和WideSearch基准测试中，"
                    "Agent API得分是Sonar最佳成绩的两倍以上。",
        key_metrics={"product": "Perplexity Agent API", "announce_date": "2026-08-14",
                     "features": ["接地网页搜索", "多步研究", "代码执行", "内置工具", "单一API多模型访问"],
                     "benchmark": "BrowseComp/WideSearch基准超Sonar两倍",
                     "migration": "Sonar将迁移至Agent API"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="Agent API集成多步规划、工具调用、代码执行能力为机器人任务规划、环境探索、"
                              "问题自主解决提供开箱即用的云端Agent基础设施",
        deployment_ready=True,
        tags=["Perplexity Agent API", "多步研究", "代码执行", "内置工具", "性能超Sonar两倍", "BrowseComp基准", "8月14日发布"]
    ),

    AIProduct(
        product_id="AIA-029", name="Google Gemini Spark升级Gemini 3.7 Flash驱动 100万token上下文64K输出",
        category=AICategory.AI_AGENT,
        organization="Google", country="美国",
        description="8月13日谷歌发布Gemini 3.7 Flash模型，8月14日起24/7 AI代理Gemini Spark正式由其驱动，"
                    "面向Google AI Pro和Ultra订阅用户开放，覆盖160+国家。升级带来100万token上下文窗口、"
                    "最高64K输出长度、可调节思考能力；增强Google Workspace工具调用能力，可精准完成供应商信息整理到Sheets、"
                    "起草谈判邮件等任务。基于Antigravity框架构建，云端专用虚拟机后台持续运行。",
        key_metrics={"product": "Gemini Spark", "upgrade_date": "2026-08-14",
                     "backing_model": "Gemini 3.7 Flash", "context_window": "100万tokens",
                     "max_output": "64K tokens", "coverage": "160+国家",
                     "subscriptions": ["Google AI Pro", "Google AI Ultra"],
                     "integrations": ["Gmail", "Calendar", "Docs", "Sheets", "Slides", "MCP协议"],
                     "framework": "Antigravity", "background_execution": True},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="100万token长上下文+后台持续运行+Workspace深度集成模式为机器人长时序任务记忆、"
                              "多工具调度、异步后台作业提供产品化参考范式",
        deployment_ready=True,
        tags=["Gemini Spark", "Gemini 3.7 Flash", "100万上下文", "64K输出", "24/7 AI代理", "Workspace集成", "后台持续运行"]
    ),

    AIProduct(
        product_id="REN-057", name="意大利启动37GW可再生能源支持计划 光伏10GW配额230亿欧元资金NZIA供应链要求",
        category=AICategory.RENEWABLE_ENERGY,
        organization="意大利环境与能源安全部（MASE）", country="意大利",
        description="8月14日消息意大利正式实施FER X可再生能源支持计划，总规模37.15GW有效期至2030年底，"
                    "获欧盟委员会批准配套230亿欧元资金。其中光伏项目配额10GW：1MW以下项目可直接申请补贴；"
                    "1MW以上须参与GSE竞争性招标，参考电价80欧元/MWh（上下限95/65欧元/MWh），石棉屋顶替换、漂浮式有价格上浮。"
                    "大型光伏招标引入欧盟《净零工业法案》（NZIA）供应链韧性准入要求，每年至少30%竞标容量专用于符合NZIA标准项目，"
                    "中标方须36个月内投运。",
        key_metrics={"program": "意大利FER X可再生能源计划", "total_capacity_gw": 37.15,
                     "pv_quota_gw": 10, "budget_billion_eur": 230, "valid_until": "2030年底",
                     "small_pv": "<1MW直接申请补贴", "large_pv": ">1MW招标 参考电价80€/MWh",
                     "nzia_requirement": "每年30%容量需符合NZIA供应链标准",
                     "commissioning_period": "36个月",
                     "incentives": ["石棉屋顶替换上浮", "漂浮式光伏上浮"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-14",
        relevance_to_robotics="欧洲GW级新能源装机为AI数据中心和机器人产业提供绿色电力支撑，NZIA本地化供应链要求"
                              "可能带动光伏制造、储能集成环节的机器人自动化产线需求",
        deployment_ready=True,
        tags=["意大利FER X", "37GW可再生能源", "光伏10GW配额", "230亿欧元", "NZIA供应链", "80欧元/MWh", "2030年"]
    ),

    AIProduct(
        product_id="REN-058", name="古瑞瓦特发布5kW-1.5MW全场景光储方案 杭州光储群英汇解析工商业储能刚性配置",
        category=AICategory.RENEWABLE_ENERGY,
        organization="古瑞瓦特（Growatt）", country="中国",
        description="8月12日古瑞瓦特在杭州举办光储群英汇，聚焦江浙工商业光储新机遇，解析分时电价下储能刚性配置趋势；"
                    "发布覆盖5kW–1.5MW的全场景光储方案，详解直流/交流耦合选型逻辑；同步推出'特省电'扶商政策"
                    "与标准化交付运维体系，助力合作伙伴实现可持续收益增长。",
        key_metrics={"event": "古瑞瓦特杭州光储群英汇", "date": "2026-08-12",
                     "solution_range": "5kW-1.5MW全场景光储",
                     "coupling_options": ["直流耦合", "交流耦合"],
                     "focus": "江浙工商业光储 分时电价下储能刚性配置",
                     "policies": "\"特省电\"扶商政策 标准化交付运维体系"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="工商业光储一体化为AI工厂、机器人充电站提供分布式能源解决方案，"
                              "标准化交付运维体系降低机器人应用场景能源基础设施部署门槛",
        deployment_ready=True,
        tags=["古瑞瓦特", "5kW-1.5MW光储", "工商业储能", "直流/交流耦合", "杭州群英汇", "特省电扶商", "分时电价"]
    ),

    AIProduct(
        product_id="REN-059", name="东方日升储能登榜BNEF 2026 Q3全球Tier 1制造商 4S融合技术三大场景方案",
        category=AICategory.RENEWABLE_ENERGY,
        organization="东方日升新能源（Risen Energy）", country="中国",
        description="8月12日东方日升储能再度入选BNEF 2026年Q3全球储能Tier 1制造商榜单，彰显国际市场认可。"
                    "依托'4S'深度融合技术与'昇家、昇企、昇能'三大场景化光储方案，叠加Risen Cloud智慧能源管理平台，"
                    "加速全球布局推动绿色能源转型。",
        key_metrics={"company": "东方日升储能", "award": "BNEF 2026 Q3全球Tier 1储能制造商",
                     "award_date": "2026-08-12",
                     "core_tech": "4S深度融合技术",
                     "scenario_solutions": ["昇家（户用）", "昇企（工商业）", "昇能（大储/电网侧）"],
                     "platform": "Risen Cloud智慧能源管理平台"},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="全球Tier 1储能厂商提供稳定可靠储能产品，为AI工厂、数据中心、机器人充电网络提供供应链保障",
        deployment_ready=True,
        tags=["东方日升储能", "BNEF Tier 1", "4S融合技术", "昇家昇企昇能", "Risen Cloud", "2026 Q3", "全球认可"]
    ),

    AIProduct(
        product_id="REN-060", name="储能产业链迎涨价潮 AI芯片抢产能+锂电池9月起征2%消费税双重驱动",
        category=AICategory.RENEWABLE_ENERGY,
        organization="储能产业链多家企业", country="中国/全球",
        description="据中关村储能产业技术联盟统计，7月以来亿纬锂能、盛弘股份、领充新能源、绿能慧充、易事特等"
                    "10余家储能产业链企业发布调价函。涨价分三类：①PCS/储能系统/充电桩：AI需求崛起导致相关芯片、"
                    "IGBT、驱动芯片涨幅50%-800%，金银铜锡有色金属涨幅30%-200%；②电芯：2026年9月1日起恢复征收锂电池2%消费税，"
                    "按财政部/海关总署/税务总局2026年第20号公告法定刚性传导。上半年国内储能中标211GWh同比+43.1%，"
                    "2小时系统均价0.552元/Wh同比+4.7%，价格底部确认抬升。",
        key_metrics={"event": "储能产业链涨价潮", "start_time": "2026年7月起",
                     "price_increase_companies": "10余家（亿纬锂能、盛弘股份等）",
                     "pcs_chip_increase": "50%-800%", "metal_increase": "30%-200%",
                     "battery_consumption_tax": "2%（2026-09-01起征）",
                     "h1_2026_bidding_gwh": 211, "h1_growth": "+43.1%",
                     "2h_system_price": "0.552元/Wh（+4.7%）",
                     "tax_basis": "财政部/海关总署/税务总局2026年第20号公告"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="AI算力需求虹吸芯片产能影响储能/充电桩成本，机器人能源基础设施部署需关注供应链价格波动；"
                              "储能涨价侧面反映AI+机器人产业高耗能需求爆发式增长",
        deployment_ready=True,
        tags=["储能涨价潮", "AI芯片虹吸", "锂电池消费税2%", "9月1日起征", "IGBT涨50%-800%", "211GWh中标", "价格底部抬升"]
    ),

    AIProduct(
        product_id="REN-061", name="阳光电源EnerNeo-SST AI电源系列发布 单机1.5-4.5MW发布即签130MW订单",
        category=AICategory.RENEWABLE_ENERGY,
        organization="阳光电源（Sungrow）", country="中国",
        description="2026年7月阳光电源正式推出EnerNeo-SST系列固态变压器（SST）AI电源产品，"
                    "单机功率覆盖1.5MW~4.5MW，最小扩容单元1.5MW，支持自由并联堆叠，功率密度高达312kW/㎡，"
                    "技术能力全球领先。发布首日即签订累计130MW订单，产业化节奏超预期。SST是未来800V直流供电系统下"
                    "AIDC（AI数据中心）电力系统核心，公司同步推进UL认证和35kV电压等级产品研发，计划2027年推向市场。"
                    "阳光电源已与北美头部云厂商共同定义产品规格，形成从源到芯全栈供电系统能力。",
        key_metrics={"product": "EnerNeo-SST系列固态变压器", "release_date": "2026年7月",
                     "power_range_mw": "1.5-4.5", "min_expansion_unit_mw": 1.5,
                     "power_density_kw_m2": 312, "launch_orders_mw": 130,
                     "application": "AIDC AI数据中心 800V直流供电系统核心",
                     "certification": "UL认证推进中 35kV产品2027年推出",
                     "partners": "北美头部云厂商共同定义规格"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-07-20",
        relevance_to_robotics="SST作为AIDC供电核心为AI大模型训练/推理、机器人云端大脑提供高效电力基础设施，"
                              "高功率密度312kW/㎡适配未来机器人计算集群高密度部署需求",
        deployment_ready=True,
        tags=["阳光电源EnerNeo-SST", "固态变压器", "1.5-4.5MW", "312kW/㎡", "发布即签130MW", "AIDC电源", "800V直流", "AI储能"]
    ),

    AIProduct(
        product_id="ROB-077", name="知行机器人完成B+轮近亿元融资 智能末端执行器/机器人手触觉感知模组",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="知行机器人（ChangingTek）", country="中国",
        description="知行机器人科技（苏州）有限公司成立于2018年8月，2026年3月完成B+轮近亿元融资，"
                    "由山东威达、厦门国兴投资、芜湖科创投、上海天使会投资。公司致力于研发智能末端执行器（机器人手）"
                    "产品和视觉抓取解决方案，产品覆盖工业制造、仓储搬运、物流分拣等领域。已开发十余款智能机器人手硬件产品："
                    "1-3公斤工业平动手、3-5公斤负载协作机器人手、50公斤以上重型模块化自适应手，"
                    "并开发配套触觉感知模组。",
        key_metrics={"company": "知行机器人", "founded": "2018-08", "location": "江苏太仓",
                     "round": "B+轮", "amount": "近亿元人民币", "round_date": "2026-03",
                     "investors": ["山东威达", "厦门国兴投资", "芜湖科创投", "上海天使会"],
                     "products": {"1-3kg": "工业平动手", "3-5kg": "协作机器人手", "50kg+": "重型模块化自适应手"},
                     "core_tech": "触觉感知模组 视觉抓取解决方案",
                     "applications": ["工业制造", "仓储搬运", "物流分拣"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-03",
        relevance_to_robotics="智能末端执行器（机器人手）是人形机器人、工业机器人核心零部件，"
                              "触觉感知模组是实现精密装配、柔性抓取、力控操作的关键传感器",
        deployment_ready=True,
        tags=["知行机器人", "B+轮近亿", "智能末端执行器", "机器人手", "触觉感知模组", "50kg重型手", "山东威达投资"]
    ),

    AIProduct(
        product_id="REN-062", name="美国2026上半年光伏组件进口10.76GW同比-39% 非洲崛起埃塞俄比亚1312MW",
        category=AICategory.RENEWABLE_ENERGY,
        organization="美国海关/光伏情报处", country="美国/全球",
        description="据美国海关2026年上半年进口数据，1-6月美国累计进口光伏组件10.76GW，同比大幅下降39%。"
                    "供应格局显著变化：东南亚仍为主力，菲律宾以3455MW居首；非洲国家异军突起，"
                    "埃塞俄比亚（1312MW）、尼日利亚（925MW）等跻身前十。美国拟于2026年12月4日起对含多晶硅的"
                    "进口光伏产品统一加征15%关税，并设定各环节最低进口限价，政策调整深刻影响全球供应链布局。",
        key_metrics={"period": "2026年H1", "us_pv_imports_gw": 10.76, "yoy_change": "-39%",
                     "top_supplier": "菲律宾3455MW",
                     "emerging_suppliers": {"埃塞俄比亚": 1312, "尼日利亚": 925},
                     "new_tariff": "15%（2026-12-04起，含多晶硅产品）",
                     "tariff_measures": ["15%统一关税", "各环节最低进口限价"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-14",
        relevance_to_robotics="光伏供应链区域化重构将带动新兴市场光伏制造产能建设，"
                              "产线自动化、机器人部署需求在非洲等新兴市场有望迎来增长窗口",
        deployment_ready=True,
        tags=["美国光伏进口", "10.76GW H1", "同比-39%", "非洲崛起", "埃塞俄比亚1312MW", "15%关税12月", "供应链重构"]
    ),

    AIProduct(
        product_id="AIA-030", name="Mastra Agent框架推出四项内置工具 WebSearch/WebFetch/SubmitPlan/AskUser",
        category=AICategory.AI_AGENT,
        organization="Mastra", country="全球",
        description="8月14日Mastra团队宣布为其Agent框架推出四项内置工具：WebSearch（基于OpenAI/Anthropic搜索能力）、"
                    "WebFetch（执行常规HTTP请求）、SubmitPlan和AskUserQuestion工具。"
                    "这些工具旨在提升Agent的资源获取与交互能力，使其更加自主和高效。",
        key_metrics={"framework": "Mastra Agent Framework", "release_date": "2026-08-14",
                     "built_in_tools": ["WebSearch（OpenAI/Anthropic搜索）", "WebFetch（HTTP请求）",
                                       "SubmitPlan（计划提交）", "AskUserQuestion（用户询问）"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-14",
        relevance_to_robotics="Agent框架内置网络搜索、信息获取、人机交互工具为机器人环境探索、"
                              "任务规划中信息收集、与人协作确认提供标准化组件",
        deployment_ready=True,
        tags=["Mastra", "Agent框架", "WebSearch", "WebFetch", "SubmitPlan", "AskUserQuestion", "内置工具"]
    ),

    AIProduct(
        product_id="AI-033", name="OpenAI基金会启动1亿美元AI慈善计划 支持非营利组织规模化AI解决方案",
        category=AICategory.AI_GENERAL,
        organization="OpenAI基金会", country="美国",
        description="8月14日OpenAI基金会宣布启动'AI for Civil Society and Philanthropy'计划，"
                    "首个项目投入1亿美元，旨在帮助非营利组织、社区组织及其他可信合作伙伴，"
                    "将先进AI应用于解决紧迫挑战、开发实用解决方案并规模化推广有效做法。消息由OpenAI基金会官方账号发布，Sam Altman转发。",
        key_metrics={"initiative": "AI for Civil Society and Philanthropy", "announce_date": "2026-08-14",
                     "initial_funding": "1亿美元",
                     "targets": ["非营利组织", "社区组织", "可信合作伙伴"],
                     "goals": ["解决紧迫社会挑战", "开发实用AI方案", "规模化推广有效做法"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="公益领域AI投入可推动助老、助残、救灾、教育等场景机器人技术的普惠化应用和落地验证",
        deployment_ready=True,
        tags=["OpenAI基金会", "1亿美元AI慈善", "Civil Society", "非营利组织", "AI公益", "8月14日宣布"]
    ),

    AIProduct(
        product_id="LLM-054", name="Anthropic Opus 5在ARC-AGI3评测首次超越人类专家 Prime Agent达95.5%",
        category=AICategory.LLM,
        organization="Anthropic", country="美国",
        description="8月14日消息，递归语言模型（RLM）与持续工具链（Continual Harness）使Prime Agent"
                    "能够扩展Opus 5的流体智能，在ARC-AGI3公开评测中以95.5%的成绩首次超越人类专家基线（95.4%）。"
                    "ARC-AGI（Abstraction and Reasoning Corpus）是衡量抽象推理能力的经典基准，"
                    "这一突破标志着AI在通用流体智能领域达到新里程碑。",
        key_metrics={"model": "Anthropic Opus 5 + Prime Agent", "benchmark": "ARC-AGI3公开评测",
                     "score": "95.5%", "human_expert_baseline": "95.4%",
                     "achievement": "首次超越人类专家水平",
                     "key_techs": ["递归语言模型RLM", "持续工具链Continual Harness", "Prime Agent"]},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-14",
        relevance_to_robotics="抽象推理能力超越人类专家意味着AI在机器人面对未知环境、新任务时的泛化推理能力达到新高度，"
                              "对机器人自主学习、零样本适应新场景具有重要意义",
        deployment_ready=False,
        tags=["Anthropic Opus 5", "ARC-AGI3", "95.5%首超人类", "Prime Agent", "递归语言模型", "抽象推理", "流体智能"]
    ),

    AIProduct(
        product_id="AIA-031", name="OpenAI为ChatGPT macOS新增Computer History功能 授权应用活动可搜索记忆",
        category=AICategory.AI_AGENT,
        organization="OpenAI", country="美国",
        description="8月14日OpenAI为ChatGPT macOS桌面应用推出Computer History新功能，"
                    "可将用户在已授权的应用和网站上的活动转化为可搜索的时间线和记忆，供ChatGPT和Codex引用。"
                    "该功能旨在让未来交互更个性化，减少用户重复解释上下文的负担。目前仅在macOS桌面端推出。",
        key_metrics={"feature": "Computer History", "platform": "ChatGPT macOS桌面应用",
                     "release_date": "2026-08-14",
                     "capability": "记录已授权应用/网站活动 转化为可搜索时间线记忆 供ChatGPT/Codex引用",
                     "purpose": "个性化交互 减少重复上下文解释", "availability": "macOS桌面端独家"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="计算机使用历史记忆技术可迁移至机器人操作记忆系统，"
                              "记录机器人与物理环境交互历史形成可检索经验库，加速技能学习与任务复用",
        deployment_ready=True,
        tags=["OpenAI Computer History", "ChatGPT macOS", "应用活动记忆", "可搜索时间线", "上下文个性化", "Codex集成"]
    ),

]

