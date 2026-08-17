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
        category=AICategory.AI_GENERAL,
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
        category=AICategory.AI_LLM,
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
        category=AICategory.AI_LLM,
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
        category=AICategory.AI_LLM,
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
        category=AICategory.AI_LLM,
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

    AIProduct(
        product_id="AGR-001", name="长春理工大学第四代智能激光除草机器人 纯电自行走作物识别率99.5%除草率95%",
        category=AICategory.AGRICULTURE,
        organization="长春理工大学+宁波一彬电子+吉林长华汽车部件", country="中国",
        description="历时三年四代迭代，投入超2000万元研发经费，核心技术全面国产化，预计2026年底批量投产。"
                    "纯电驱动自行走底盘，搭载多作物AI视觉识别系统，构建玉米、大豆、马铃薯、油菜、中草药等10余类作物图像数据库。"
                    "田间作业时AI实时区分作物与杂草，毫米级激光束精准灼烧杂草分生组织，全程不碰一株秧苗。"
                    "已申报7项国家发明专利，4项核心专利授权，覆盖激光器封装、激光除草整机、相机振镜标定、杂草精准定位四大关键环节。"
                    "量产后将推出大型拖挂式（适配东北万亩大田）和小型自行走式（适配大棚/中草药基地）两大系列。",
        key_metrics={"product": "第四代智能激光除草机器人", "power": "纯电驱动",
                     "crops_supported": ["玉米", "大豆", "马铃薯", "油菜", "中草药"],
                     "crop_recognition_rate": "99.5%", "weed_removal_rate": "95%+",
                     "response_time_ms": 10, "positioning_accuracy_mm": "±2",
                     "max_speed_kmh": 3.6, "weeds_per_hour": "5-10万株",
                     "daily_area_mu": 50, "efficiency_multiplier": "人工除草50倍",
                     "rnd_investment": "超2000万元", "patents": "7项发明申请/4项授权",
                     "production_date": "2026年底", "series": ["大型拖挂式", "小型自行走式"],
                     "market_estimate_ne_mu": "东北2.37亿亩玉米对应70-140万台设备需求/千亿元市场",
                     "features": ["无除草剂零污染", "昼夜全天候作业", "模块化激光单元积木式组合",
                                  "陀螺仪+编码器抗震动稳定瞄准", "自适应调速根据杂草密度"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-07",
        relevance_to_robotics="农业机器人核心是视觉识别+精准执行+复杂地形自主行走三大能力，"
                              "激光除草机器人的AI视觉+动态瞄准+模块化设计为田间作业机器人提供完整技术栈参考，"
                              "10ms响应±2mm精度可迁移至工业精密分拣/装配场景",
        deployment_ready=True,
        tags=["激光除草机器人", "第四代", "作物识别率99.5%", "除草率95%", "5万株/小时", "50亩/天", "纯电", "10ms响应", "东北黑土地"]
    ),

    AIProduct(
        product_id="MED-001", name="术锐蛇形臂单孔腔镜手术机器人落地欧洲顶级医院 完成12岁男孩肾结石手术",
        category=AICategory.MEDICAL_DEVICE,
        organization="北京术锐机器人股份有限公司", country="中国",
        description="落地西班牙排名第一的瓦尔德希伯伦大学医院，是该院历史上首次引进中国整机手术机器人。"
                    "连续体蛇形臂采用镍钛合金柔性骨架+专属驱控算法，在单一2.5厘米微小切口内三支蛇形器械+3D摄像系统协同操作，"
                    "多角度灵活弯折自主避让，解决单孔手术器械相互碰撞的行业难题。"
                    "10个工作日内完成医护团队系统化培训，如期实施11例多学科复杂微创手术。"
                    "已落地德国多家医疗机构，2026上半年中国手术机器人出口额4.8亿元，同比增长3.3倍，覆盖49个国家和地区，"
                    "蛇形臂手术机器人95%零部件国产化，成本仅为海外同行1/3~1/2。",
        key_metrics={"product": "术锐蛇形臂单孔腔镜手术机器人", "company": "北京术锐机器人（专精特新小巨人）",
                     "core_tech": "连续体蛇形臂（镍钛合金柔性骨架+专属驱控算法）",
                     "incision_size_cm": 2.5, "instruments": "3支蛇形器械+3D摄像系统",
                     "key_advantages": ["滤除人手天然震颤", "单孔多器械不碰撞", "3D高清放大视野",
                                        "血管脏器间精细分离缝合"],
                     "deployment_hospital": "西班牙瓦尔德希伯伦大学医院（西班牙综合第一）",
                     "training_days": 10, "surgeons_trained": 10, "cases_completed": 11,
                     "case_example": "12岁男孩肾脏多发结石手术，术后48小时出院",
                     "localization_rate": "95%零部件国产化", "cost_ratio": "海外同行1/3~1/2",
                     "china_export_h1_2026": {"amount_rmb_yi": 4.8, "yoy_growth": "+330%",
                                             "countries": 49}},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-07",
        relevance_to_robotics="蛇形臂连续体机器人技术是柔性机器人、微创介入机器人、狭窄空间检测机器人的核心共性技术，"
                              "镍钛合金骨架+驱控算法可迁移至管道检测、搜救机器人、精密装配等场景",
        deployment_ready=True,
        tags=["术锐机器人", "蛇形臂手术机器人", "单孔腔镜", "欧洲顶级医院", "95%国产化", "成本1/3", "出口3.3倍", "西班牙首例", "4.8亿出口"]
    ),

    AIProduct(
        product_id="MED-002", name="全球首个多通道术中协同及质控机器人云南投入临床 北京专家2000公里外200ms延时指导",
        category=AICategory.MEDICAL_DEVICE,
        organization="北京安贞医院+北京航空航天大学", country="中国",
        description="全球首个多通道术中协同及质控机器人，由1.8米机械臂+多个高清摄像设备组成，"
                    "整合监护仪、腔镜、术中超声等20类设备数据为实时加密数据流，经5G专用网络传回北京，"
                    "实现云南保山-北京安贞医院2000公里远程手术指导，延时低于200毫秒。"
                    "AI预警核心能力：实时分析数据流捕捉异常信号、测算风险并发出预警，为手术团队争取处置时间。"
                    "手术每项操作和数据完整留存，堪称手术室'黑匣子'，可供术后复盘。"
                    "在云南省保山市人民医院完成首例心脏二尖瓣置换手术远程指导，后续将在多省份试点推广。",
        key_metrics={"product": "多通道术中协同及质控机器人", "institutions": ["北京安贞医院", "北航", "保山人民医院"],
                     "arm_length_m": 1.8, "camera_resolution": "毫米级血管细节",
                     "integrated_devices": 20, "distance_km": 2000, "latency_ms": "<200",
                     "ai_features": ["实时异常信号捕捉", "风险测算", "术前预警", "全流程数据记录"],
                     "first_case": "心脏二尖瓣置换手术远程指导", "application": "全国多省份试点推广",
                     "core_value": ["国家级专家远程站在基层医生身后保驾护航", "手术室黑匣子完整复盘",
                                    "AI预警致命异常争取抢救时间"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-07",
        relevance_to_robotics="远程医疗机器人是遥操作机器人的典型应用，5G低延迟+多源数据融合+AI预警+机械臂视觉引导技术"
                              "可直接迁移至远程排爆、深空探测、深海作业、核电站维护等极限场景遥操作机器人系统",
        deployment_ready=True,
        tags=["术中协同质控机器人", "全球首个", "1.8米机械臂", "20类设备整合", "5G 200ms延时", "AI预警", "手术室黑匣子", "2000公里远程指导"]
    ),

    AIProduct(
        product_id="MED-003", name="如身机器人亿元Pre-A轮 全球首个载人与服务双模态具身养老护理机器人七自由度20kg力控臂",
        category=AICategory.HEALTHCARE,
        organization="如身机器人", country="中国",
        description="全球首个载人与服务双模态具身养老护理机器人，专门针对失能/半失能老人照护场景设计。"
                    "搭载七自由度20kg大负载力控柔顺机械臂，实现喂饭、递送、搬运、护理辅助等高频服务动作自主化。"
                    "完成亿元Pre-A轮融资，资金用于产品量产和养老院规模化部署。",
        key_metrics={"company": "如身机器人", "round": "Pre-A轮", "amount": "亿元级",
                     "product": "载人与服务双模态具身养老护理机器人",
                     "robot_arm_dof": 7, "payload_kg": 20, "control": "力控柔顺控制",
                     "core_capabilities": ["喂饭", "递送物品", "搬运", "护理辅助", "载人移动"],
                     "target_scene": "失能/半失能老人养老照护", "application_status": "产品研发完成/量产准备中"},
        maturity=MaturityLevel.PROTOTYPE,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08",
        relevance_to_robotics="养老护理机器人是人形机器人/服务机器人最大刚需场景之一，"
                              "七自由度力控臂+双模态（载人+服务）设计为家庭服务机器人、医疗护理机器人提供产品形态参考",
        deployment_ready=False,
        tags=["如身机器人", "亿元Pre-A", "养老护理机器人", "载人与服务双模态", "七自由度机械臂", "20kg负载", "力控柔顺", "失能照护"]
    ),

    AIProduct(
        product_id="MED-004", name="三友医疗春风化雨8iRobotics全球首款多臂人形智能化脊柱手术机器人完成欧洲首台装机",
        category=AICategory.MEDICAL_DEVICE,
        organization="三友医疗（688085）+法国Implanet", country="中国/法国",
        description="全球首款多臂人形智能化脊柱手术机器人，集成先进电磁导航、集成数字显微镜、多臂协同、"
                    "水木天蓬超声骨刀技术等顶尖核心手术机器人技术。"
                    "已在法国亚眠-皮卡第大学医疗中心完成欧洲首台装机，启动脊柱外科/神经外科临床评估及欧盟CE认证。"
                    "目前已在北美、亚洲、欧洲五家医院完成科研临床装机。",
        key_metrics={"product": "春风化雨8iRobotics多臂人形智能化脊柱手术机器人",
                     "company": "三友医疗控股法国Implanet",
                     "core_tech": ["电磁导航", "集成数字显微镜", "多臂协同控制", "水木天蓬超声骨刀"],
                     "deployment": "法国亚眠-皮卡第大学医疗中心（欧洲首台）",
                     "clinical_status": "欧亚北美5家医院科研临床装机",
                     "certification": "欧盟CE认证推进中",
                     "application": "脊柱外科、神经外科手术"},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-07",
        relevance_to_robotics="多臂协同手术机器人是多机器人协作、精密力控、医学影像导航技术的集大成者，"
                              "电磁导航+多臂协同可迁移至工业多机器人协同装配场景",
        deployment_ready=True,
        tags=["三友医疗", "8iRobotics", "多臂人形脊柱手术机器人", "欧洲首台装机", "电磁导航", "超声骨刀", "欧盟CE认证", "5家医院"]
    ),

    AIProduct(
        product_id="AUT-001", name="零跑A05正式上市 6.39万元起激光雷达200TOPS算力43项智驾510km续航2.5C快充16分钟补能",
        category=AICategory.AUTOMOTIVE,
        organization="零跑汽车", country="中国",
        description="零跑全球化车型，定位智能灵动精品两厢纯电轿车，五款配置，CLTC 405km/510km两种续航。"
                    "车身尺寸4200×1800×1560mm，轴距2605mm，四轮四角布局，最小转弯半径4.9米。"
                    "全系标配高通骁龙8295旗舰座舱芯片，8.88英寸仪表+14.6英寸2.5K悬浮中控屏，Leapmotor OS+AI大模型。"
                    "底盘LMC一体化运动控制系统+采埃孚Onebox集成制动。"
                    "激光雷达版本搭载128线激光雷达+高通8650智驾芯片，等效算力200TOPS，支持车位到车位全场景辅助驾驶，"
                    "HPA记忆泊车、120米循迹倒车等43项智驾功能，实现地库出库-道路通行-自动泊入完整闭环。",
        key_metrics={"model": "零跑A05", "positioning": "智能灵动精品两厢纯电轿车",
                     "price_range": "6.39-9.09万元",
                     "dimensions_mm": [4200, 1800, 1560], "wheelbase_mm": 2605,
                     "storage": {"regular_l": 474, "max_l": 1308, "storage_points": 34},
                     "powertrain": {"405km": {"motor_kw": 70, "battery_kwh": 39.8, "battery_type": "磷酸铁锂"},
                                    "510km": {"motor_kw": 90, "battery_kwh": 53, "charge_rate": "2.5C",
                                              "fast_charge_30_80_min": 16}},
                     "cockpit_chip": "高通骁龙8295", "screens": "8.88寸仪表+14.6寸2.5K中控",
                     "audio": "12扬声器+无麦车载K歌", "v2l": "3.3kW对外放电",
                     "smart_drive_base": "纯视觉L2全速域ACC+车道居中",
                     "smart_drive_lidar": {"lidar_lines": 128, "chip": "高通8650", "computing_power_tops": 200,
                                           "functions": 43, "key_features": ["车位到车位全场景", "HPA记忆泊车",
                                                                          "120米循迹倒车", "地库-道路-泊入闭环"]},
                     "colors": ["摩根粉", "雾凇米", "深空黑", "510S专属撞色"],
                     "turning_radius_m": 4.9},
        ram_gb=0, rom_gb=0, price_start_rmb=63900, price_top_rmb=90900,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08",
        relevance_to_robotics="200TOPS算力智驾+128线激光雷达下放到6万级小车，标志高阶自动驾驶感知计算硬件成本大幅下降，"
                              "相关传感器、计算平台、规控算法可迁移至机器人自主导航系统降低成本",
        deployment_ready=True,
        tags=["零跑A05", "6.39万起", "128线激光雷达", "200TOPS", "43项智驾", "510km续航", "2.5C快充16分钟", "高通8295", "4.9米转弯半径"]
    ),

    AIProduct(
        product_id="AUT-002", name="2027款比亚迪海豹06上市 9.99万起DM-i纯电续航320km综合2370km EV 630km零百5.9秒天神之眼B",
        category=AICategory.AUTOMOTIVE,
        organization="比亚迪", country="中国",
        description="海洋网车型，DM-i插混+EV纯电两套动力共12款配置，DM-i 9.99-14.19万元，EV 10.99-15.59万元。"
                    "车身4870/1890/1495mm，轴距2820mm，B级空间。DM-i首次与EV统一车身规格。"
                    "DM-i搭载第五代DM超级混动，CLTC纯电最高320km，NEDC亏电油耗2.59L/100km，满油满电综合续航2370km。"
                    "EV搭载原生闪充平台+第二代刀片电池，最高630km CLTC，高功率电机峰值240kW，零百加速5.9秒，全系极速闪充。"
                    "高配搭载云辇-C智能阻尼车身控制+路面预瞄，前麦弗逊+后五连杆独立悬架。"
                    "天神之眼B激光雷达智驾方案，支持城市NOA、高速领航、全场景自动泊车。"
                    "DiLink高阶智能系统，15.6英寸自适应旋转大屏，AI大模型连续语音交互。",
        key_metrics={"model": "2027款海豹06", "brand": "比亚迪海洋网",
                     "dmi_price": "9.99-14.19万元", "ev_price": "10.99-15.59万元",
                     "dimensions_mm": [4870, 1890, 1495], "wheelbase_mm": 2820,
                     "dmi_powertrain": {"dm_generation": "第五代", "ev_range_km": 320,
                                        "fuel_consumption_l100km": 2.59, "combined_range_km": 2370},
                     "ev_powertrain": {"battery": "第二代刀片电池", "max_range_km": 630,
                                       "peak_power_kw": 240, "zero_100_s": 5.9, "charging": "原生闪充平台"},
                     "chassis": {"front_suspension": "麦弗逊", "rear_suspension": "五连杆独立",
                                 "high_config": "云辇-C智能阻尼+路面预瞄"},
                     "smart_drive": "天神之眼B激光雷达方案（城市NOA+高速领航+全场景泊车）",
                     "cockpit": "DiLink+15.6寸旋转大屏+AI大模型连续语音+FOTA",
                     "comfort_options": ["座椅通风/加热/按摩", "全景天幕", "智能冷暖冰箱", "多扬声器音响"]},
        ram_gb=0, rom_gb=0, price_start_rmb=99900, price_top_rmb=155900,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08",
        relevance_to_robotics="第五代DM混动极低油耗+刀片电池+云辇-C底盘控制+天神之眼智驾系统，"
                              "其线控底盘、域控制器、多传感器融合方案为轮式机器人、移动机器人底盘提供成熟车规级技术参考",
        deployment_ready=True,
        tags=["比亚迪海豹06", "9.99万起", "DM-i 320km纯电", "综合续航2370km", "EV 630km", "零百5.9秒", "云辇-C", "天神之眼B", "刀片电池"]
    ),

    AIProduct(
        product_id="AUT-003", name="小鹏G9L预售25.98万起 纯电/超增程双动力5C超充9分钟450km双腔空悬VLA智驾6.3",
        category=AICategory.AUTOMOTIVE,
        organization="小鹏汽车", country="中国",
        description="黄金大五座科技旗舰，SEPA3.0全域智能架构，纯电+超级增程双动力四配置六车型预售价25.98万起。"
                    "车身5120/1999/1782mm，轴距3100mm，前法拉利设计师胡安马团队操刀。"
                    "百万像素AI数字投影大灯，最远识别600米，支持地面光影交互+ADB自适应远光；全系智能四电动门+电动侧踏+1.4㎡迎宾光毯。"
                    "全球首发全体型AI主动贴合座椅，多传感器实时感知身形动态调节支撑，一二排一键成床+前后排零重力同步舒躺；"
                    "后备厢常规1152L+230L下沉。双温区冰箱+33扬声器音响+遮阳天幕。"
                    "全系5C高压超充，最快9分钟补450km CLTC；纯电续航660-755km，四驱零百4.45秒；"
                    "超增程纯电435km综合1602km支持92号汽油，四驱零百4.95秒。"
                    "标配前双叉臂+后H臂多连杆+双腔空悬+CDC+X-VMC融合控制+线控后轮转向最小转弯半径5.4米。"
                    "第二代VLA智驾6.3.0版本，端侧大模型参数+3.5倍，座舱智驾深度融合，下放Robotaxi能力。",
        key_metrics={"model": "小鹏G9L", "positioning": "黄金大五座科技旗舰", "presale_start": 25.98,
                     "architecture": "SEPA3.0全域智能架构", "powertrain_options": ["纯电", "超级增程"],
                     "dimensions_mm": [5120, 1999, 1782], "wheelbase_mm": 3100,
                     "designer": "前法拉利胡安马团队",
                     "lighting": "百万像素AI数字投影大灯（识别600米+ADB+地面交互）",
                     "doors": "智能四电动门+电动侧踏+1.4㎡光毯",
                     "seats": "全体型AI主动贴合（多传感器动态调节）+一二排一键成床+双零重力",
                     "trunk_l": {"regular": 1152, "underfloor": 230},
                     "comfort": "双温区冰箱+33扬声器+遮阳天幕",
                     "charging": "5C高压超充（9分钟补450km）",
                     "ev_range": "660-755km（四驱零百4.45s）",
                     "erev_range": {"ev_km": 435, "combined_km": 1602, "fuel": "92号汽油", "zero_100_s": 4.95},
                     "chassis": {"front": "双叉臂", "rear": "H臂多连杆", "air_spring": "双腔空悬",
                                "cdc": True, "x_vmc": True, "rear_wheel_steering": "线控后轮转向",
                                "turning_radius_m": 5.4},
                     "smart_drive": "第二代VLA智驾6.3.0（端侧大模型参数+3.5倍+Robotaxi能力下放+模糊语义导航）",
                     "safety": "全球四大五星标准+一体压铸+11安全气囊+多重冗余"},
        ram_gb=0, rom_gb=0, price_start_rmb=259800,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08",
        relevance_to_robotics="VLA视觉语言动作智驾大模型+双腔空悬+线控后轮转向+5C超充是机器人感知决策控制、高性能底盘、能源补给的标杆参考，"
                              "Robotaxi能力下放技术栈可直接迁移至户外自主移动机器人",
        deployment_ready=True,
        tags=["小鹏G9L", "25.98万预售", "5C超充9分钟450km", "双腔空悬", "线控后轮转向", "VLA智驾6.3", "超增程1602km", "全体型AI座椅", "33扬声器"]
    ),

    AIProduct(
        product_id="AUT-004", name="英伟达Alpamayo 2 Super开源340亿参数智驾VLA模型 视觉骨干320亿动作专家23亿开放商用",
        category=AICategory.AI_LLM,
        organization="NVIDIA", country="美国",
        description="面向自动驾驶汽车与无人出租车的开源推理模型，基于Cosmos 3 Super Reasoner构建，强化学习优化，"
                    "OpenMDW-1.1许可协议下开放商业使用，允许车企/卡车制造商/供应商微调衍生商业化部署。"
                    "VLA视觉语言动作架构：320亿参数视觉语言骨干理解场景，23亿参数动作专家输出控制，理解侧权重是执行侧近14倍。"
                    "具备深度思考能力，可生成车辆行驶轨迹、决策推理链、驾驶意图、训练标注、视觉问答，帮助验证决策过程。"
                    "2026年1月CES发布Alpamayo 1，七个月后从研究开源到开放商用。国内L2渗透率70.5%，NOA渗透率34.2%。",
        key_metrics={"model": "Alpamayo 2 Super", "release_date": "2026-08-04",
                     "total_params_bn": 34, "vl_backbone_bn": 32, "action_expert_bn": 2.3,
                     "architecture": "VLA视觉语言动作", "base_model": "Cosmos 3 Super Reasoner",
                     "training": "强化学习优化",
                     "capabilities": ["场景理解与深度思考", "行驶轨迹生成", "决策推理链", "驾驶意图识别",
                                      "训练标注生成", "视觉问答", "决策过程可解释验证"],
                     "license": "OpenMDW-1.1（允许商业化微调/部署）",
                     "users_alpamayo_1": ["捷豹路虎", "Lucid", "Uber", "伯克利DeepDrive"],
                     "china_market": {"l2_penetration": "70.5%", "noa_penetration": "34.2%",
                                      "l3_start": "首批L3车型特定区域上路",
                                      "l2_mandatory_standard": "GB标准2027-01-01实施"}},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-04",
        relevance_to_robotics="340亿参数VLA架构（理解大权重/执行小权重）是机器人通用大脑的标准范式——感知理解用大模型，"
                              "实时控制用小专家模型，该架构可直接迁移至人形机器人、工业机器人通用智能控制方案",
        deployment_ready=True,
        tags=["英伟达Alpamayo 2", "340亿参数", "VLA智驾", "320亿视觉+23亿动作", "开源商用", "Cosmos 3", "深度思考推理链", "OpenMDW"]
    ),

    AIProduct(
        product_id="AUT-005", name="自动驾驶强制性国标GB 44721-2026发布 2027年7月1日实施 系统安全不低于人类驾驶员水平",
        category=AICategory.AI_GENERAL,
        organization="国家市场监督管理总局/国家标准化管理委员会", country="中国",
        description="《智能网联汽车自动驾驶系统安全要求》（GB 44721—2026）强制性国家标准正式发布，2027年7月1日实施。"
                    "核心要求：自动驾驶系统安全水平至少达到合格且专注的人类驾驶员水平。"
                    "抬高L3+智驾量产门槛，无冗余架构、DSSAD黑匣子、安全档案工程化能力的车企/纯算法供应商将被挡在量产赛道外。"
                    "配套L2组合驾驶辅助系统强制性国标已于6月27日发布，2027年1月1日实施。"
                    "两部门目标：到2030年充电基础设施总量超过4000万个。",
        key_metrics={"standard": "GB 44721-2026《智能网联汽车自动驾驶系统安全要求》",
                     "standard_type": "强制性国家标准", "release_date": "2026-08",
                     "implementation_date": "2027-07-01",
                     "core_requirement": "自动驾驶系统安全水平≥合格且专注的人类驾驶员水平",
                     "required_capabilities": ["系统冗余架构", "DSSAD事故数据记录系统（黑匣子）", "安全档案工程化能力"],
                     "l2_standard": "GB L2组合辅助标准2027-01-01实施",
                     "policy_targets": {"charging_piles_2030_wan": 4000}},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08",
        relevance_to_robotics="安全标准是机器人商业化的前提——自动驾驶安全框架（冗余架构、黑匣子、安全档案、人类水平基线）"
                              "同样适用于服务机器人、医疗机器人、工业协作机器人的安全认证体系建设",
        deployment_ready=True,
        tags=["自动驾驶国标GB 44721", "强制性国标", "2027年7月实施", "安全≥人类驾驶员", "冗余架构", "DSSAD黑匣子", "L3+门槛抬高"]
    ),

    AIProduct(
        product_id="HOM-001", name="华为Vision智慧屏6 SE RGB发布 首款RGB-MiniLED电视55/65/75寸3499元起105% BT.2020",
        category=AICategory.HOME_APPLIANCE,
        organization="华为", country="中国",
        description="华为首款RGB-MiniLED电视，8月3日发布8月5日开售，55/65/75三种尺寸，起售价3499元。"
                    "4K分辨率RGB-MiniLED屏幕，色域覆盖105% BT.2020，自研鸿鹄光色同控芯片同步优化亮度与色彩。"
                    "原生120Hz刷新率，最高300Hz倍频刷新（适配PC/游戏主机高帧率信号）。"
                    "四核处理器：双核A53+双核A73，3GB RAM+64GB ROM，HarmonyOS 4.3。"
                    "支持4K超级投屏、鸿蒙AI、智能门锁等鸿蒙生态设备无缝协同。"
                    "75寸版本内置100W大功率音响系统。",
        key_metrics={"product": "华为Vision智慧屏6 SE RGB", "release_date": "2026-08-03",
                     "sale_date": "2026-08-05", "sizes_inch": [55, 65, 75], "price_start": 3499,
                     "display_type": "RGB-MiniLED", "resolution": "4K", "color_gamut": "105% BT.2020",
                     "chip": "自研鸿鹄光色同控芯片",
                     "refresh_rate": {"native_hz": 120, "max_motion_hz": 300},
                     "processor": "四核（双核A53+双核A73）", "ram_gb": 3, "rom_gb": 64,
                     "os": "HarmonyOS 4.3",
                     "audio_75inch": "100W大功率音响",
                     "features": ["4K超级投屏", "鸿蒙AI能力", "鸿蒙生态设备协同", "智能门锁联动"]},
        ram_gb=3, rom_gb=64, price_start_rmb=3499,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-03",
        relevance_to_robotics="RGB-MiniLED显示技术、鸿鹄光色同控芯片可迁移至机器人交互界面、"
                              "服务机器人显示屏、工业机器人HMI界面提升色彩和动态显示效果",
        deployment_ready=True,
        tags=["华为Vision智慧屏6 SE RGB", "RGB-MiniLED", "3499元起", "105% BT.2020", "120Hz原生/300Hz倍频", "鸿鹄光色同控", "HarmonyOS 4.3", "3+64GB"]
    ),

    AIProduct(
        product_id="HOM-002", name="小米8月11日在法发布三款大家电 621L对开门冰箱8kg洗烘一体机8kg滚筒379欧元起",
        category=AICategory.HOME_APPLIANCE,
        organization="小米集团", country="中国/法国",
        description="2026年8月11日在法国市场发布三款米家大家电：Mijia对开门美式冰箱621L、Mijia 8kg洗烘一体机、Mijia 8kg滚筒洗衣机。"
                    "冰箱621L容量分18个储物区，Ag⁺ Fresh银离子除菌净化（99.99%大肠杆菌去除/除异味），360°风冷双压缩机，"
                    "支持Xiaomi Home APP远程控制、Google Assistant/Alexa语音，售价849欧元（首发优惠799欧元至9月11日）。"
                    "洗烘一体机比欧盟A级能效还节能30%，30+程序含15分钟快洗+3D智能烘干，Wash & Care 180分钟完整洗烘，"
                    "99.99%蒸汽除菌，自动称重控水，售价559欧元（首发479欧元）。"
                    "滚筒洗衣机（无烘干）同洗衣功能，499欧元（首发449欧元）。",
        key_metrics={"release_market": "法国", "release_date": "2026-08-11",
                     "fridge": {"model": "Mijia Réfrigérateur Américain 621L Side-by-Side",
                                "capacity_l": 621, "compartments": 18,
                                "sterilization": "Ag⁺ Fresh银离子（99.99%除菌除味）",
                                "cooling": "360°风冷+双压缩机",
                                "smart_control": ["Xiaomi Home APP", "Google Assistant", "Alexa"],
                                "price_eur": 849, "launch_offer_eur": 799,
                                "offer_valid": "2026-08-11至09-11"},
                     "washer_dryer": {"model": "Mijia Lave-linge séchant Hublot 8kg",
                                      "capacity_kg": 8, "energy_efficiency": "比欧盟A级高30%",
                                      "programs": "30+（含15分钟快洗+3D智能烘干）",
                                      "wash_care_cycle_min": 180, "sterilization": "99.99%蒸汽除菌",
                                      "smart_features": "自动称重调水调时",
                                      "price_eur": 559, "launch_offer_eur": 479},
                     "washer": {"model": "Mijia Lave-linge Hublot 8kg", "capacity_kg": 8,
                                "price_eur": 499, "launch_offer_eur": 449}},
        ram_gb=0, rom_gb=0, price_start_rmb=3600,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-11",
        relevance_to_robotics="智能大家电是家庭服务机器人的核心控制节点和协作对象，"
                              "多设备互联+AI节能+自动感知称重等智能功能为家庭服务机器人与家电协同提供场景基础",
        deployment_ready=True,
        tags=["小米米家大家电", "法国发布", "621L对开门冰箱", "Ag+除菌", "双压缩机", "8kg洗烘一体", "A级+30%节能", "180分钟洗烘", "智能家电出海"]
    ),

    AIProduct(
        product_id="EDU-001", name="进化者机器人小胖教师助手E07/E08 45-48自由度1.28/1.65米10万/13万进驻1.2万园1000校",
        category=AICategory.EDUCATION,
        organization="进化者机器人", country="中国",
        description="十年技术沉淀，2026年初完成8000万元A+轮融资。全球唯一可规模化进校园授课的具身智能产品。"
                    "自研高性能低成本关节模组+灵巧手绳腱驱动执行器，机械臂+灵巧手成本压缩至行业平均1/3，目标手+臂总成本<3000元。"
                    "evolve VLA模型针对上课教学垂类场景优化，轻量化可直接在普通手机/PAD运行，无需高端本地算力芯片。"
                    "累计200+项专利软著：53项国内发明、13项国际发明、50项软著，论文25+篇SCI他引335+次。"
                    "小学版E07：128cm身高45自由度2个灵巧手，零售价<10万元，无屏实物编程课程。"
                    "中学/职高/大学版E08：1.65米全尺寸类女性设计48自由度，零售价<13万元，实验演示/技能教学。"
                    "已进驻超1.2万家幼儿园、1000家小学，累计课程超500万节覆盖400万学生，入校率/周均上课频次/满意度三项全球第一。",
        key_metrics={"company": "进化者机器人", "round": "A+轮", "amount_wan": 8000,
                     "core_tech": {"joint_actuator": "自研高性能低成本关节模组",
                                   "dexterous_hand": "绳腱驱动灵巧手",
                                   "arm_hand_cost_target": "<3000元（行业1/3）",
                                   "vla_model": "evolve VLA（垂类优化，手机/PAD可运行）",
                                   "patents": "200+（53国内发明+13国际发明+50软著）",
                                   "papers_citations": "25篇SCI，他引335+"},
                     "e07_primary": {"height_cm": 128, "dof": 45, "dexterous_hands": 2,
                                     "price_wan": "<10", "feature": "无屏实物编程课程"},
                     "e08_secondary_plus": {"height_cm": 165, "dof": 48, "design": "全尺寸类女性",
                                            "price_wan": "<13", "feature": "实验演示/技能教学"},
                     "deployment": {"kindergartens": "1.2万+", "primary_schools": 1000,
                                    "lessons": "500万+节", "students": 400, "wan": True,
                                    "rankings": ["入校率全球第一", "周均上课频次全球第一", "学校满意度全球第一"]},
                     "plan_2026": "进军海外，目标年增长50%"},
        ram_gb=0, rom_gb=0, price_start_rmb=100000,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-01",
        relevance_to_robotics="教育机器人是人形机器人成本下探和规模落地的先头场景，"
                              "E07/E08低成本关节+轻量化VLA+大规模进校验证的技术路径，为消费级人形机器人量产提供参考",
        deployment_ready=True,
        tags=["进化者小胖", "教师助手机器人", "E07 128cm 10万", "E08 1.65米 13万", "45-48自由度", "evolve VLA", "1.2万园1000校", "500万节课"]
    ),

    AIProduct(
        product_id="EDU-002", name="深圳龙岗AI龙老师覆盖50+中小学 作业学情采集197万份AI作文批改19万人次",
        category=AICategory.EDUCATION,
        organization="深圳市龙岗区教育局", country="中国",
        description="龙岗区构建\"1+2+6+N\"AI教育体系，\"AI龙老师\"个性化学习项目覆盖50+中小学，"
                    "累计智能采集作业学情超197万份，AI作文批改超19万人次，生成个性化学习手册超7万册。"
                    "龙岗目标人工智能与机器人产业规模达千亿元，坂田机器人街区全球首家人工智能6S店开业，"
                    "工业端推出\"龙师傅\"AI搭子聚焦电子/模具/汽车/具身机器人四大行业。"
                    "全国首个AI原生城市治理智能体\"龙小二\"具备自感知/自思考/自执行/自进化能力，融合政务/视频/网络民意数据，部署超百种算法，"
                    "可调度机器狗自主导航执行城市治理任务。",
        key_metrics={"region": "深圳龙岗区", "education_system": "1+2+6+N AI教育体系",
                     "ai_teacher": "AI龙老师个性化学习项目",
                     "schools_covered": "50+", "homework_collected_wan": 197,
                     "essay_correction_wan": 19, "personalized_manuals_wan": 7,
                     "ai_industry_target_yi": 1000,
                     "industrial_ai": "龙师傅AI搭子（电子/模具/汽车/具身机器人四行业）",
                     "urban_ai": "龙小二AI原生城市治理智能体（自感知/思考/执行/进化，100+算法，可调度机器狗）",
                     "robotics_infrastructure": ["坂田机器人街区", "全球首家AI 6S店", "机器人大道", "12个机器人展示盒子"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-12",
        relevance_to_robotics="区域级AI+机器人全域应用示范区模式：教育/工业/城市治理三大场景同时落地，"
                              "教育AI采集大规模学生行为数据、工业AI生产数据、城市治理机器狗调度数据，为机器人算法训练提供丰富真实场景数据",
        deployment_ready=True,
        tags=["深圳龙岗", "AI龙老师", "50+学校", "197万作业", "19万作文批改", "千亿产业目标", "龙小二城市治理智能体", "机器狗调度", "龙师傅工业AI"]
    ),

    AIProduct(
        product_id="DIG-033", name="华为WATCH GT 7/GT 7 Pro发布 21天超长续航滑雪骑行模式1688元起钛合金纳米微晶陶瓷2688元",
        category=AICategory.DIGITAL_PRODUCT,
        organization="华为", country="中国",
        description="华为全场景新品发布会同期发布WATCH GT 7和WATCH GT 7 Pro两款智能手表，8月14日开售。"
                    "WATCH GT 7主打身体状态准备度评估、全新滑雪&骑行运动模式，21天超长续航，售价1688元起。"
                    "WATCH GT 7 Pro采用钛合金表体+纳米微晶陶瓷表圈高端材质，定位户外进阶运动，同样21天续航，售价2688元起。",
        key_metrics={"models": ["WATCH GT 7", "WATCH GT 7 Pro"],
                     "gt7": {"price_start": 1688, "features": ["身体状态准备度评估", "全新滑雪模式", "全新骑行模式"],
                             "battery_days": 21},
                     "gt7_pro": {"price_start": 2688,
                                 "materials": ["钛合金表体", "纳米微晶陶瓷表圈"],
                                 "positioning": "户外进阶运动", "battery_days": 21},
                     "sale_date": "2026-08-14"},
        ram_gb=0, rom_gb=0, price_start_rmb=1688, price_top_rmb=2688,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="智能手表的运动姿态识别、健康监测传感器、低功耗21天续航技术可迁移至机器人腕部可穿戴示教器、"
                              "机器人运维人员状态监测、人机交互腕部控制器等场景",
        deployment_ready=True,
        tags=["华为WATCH GT 7", "1688元", "GT 7 Pro 2688元", "21天续航", "身体状态准备度", "滑雪骑行模式", "钛合金陶瓷"]
    ),

    AIProduct(
        product_id="DIG-034", name="华为自带线全能充智能移动电源100W 12000mAh 首批2026新国标3C认证双向快充399元",
        category=AICategory.DIGITAL_PRODUCT,
        organization="华为", country="中国",
        description="华为100W 12000mAh自带线全能充智能移动电源，首批获2026新国标3C认证，"
                    "支持双向100W高功率超级快充，具备离线查找智慧提醒功能，售价399元。"
                    "适配手机、平板、笔记本电脑多设备超级快充需求。",
        key_metrics={"product": "华为自带线全能充智能移动电源", "capacity_mah": 12000,
                     "power_w": 100, "charging": "双向100W超级快充",
                     "certification": "首批2026新国标3C认证",
                     "features": ["自带线材", "离线查找智慧提醒", "多设备兼容"],
                     "price": 399, "compatible": ["手机", "平板", "笔记本"]},
        ram_gb=0, rom_gb=0, price_start_rmb=399,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="高功率密度快充电池技术、离线查找UWB定位技术可迁移至机器人电池快充、"
                              "机器人资产定位管理等应用场景",
        deployment_ready=True,
        tags=["华为移动电源", "100W 12000mAh", "双向超级快充", "新国标3C认证", "离线查找", "399元", "自带线全能充"]
    ),

    AIProduct(
        product_id="DIG-035", name="华为MatePad Pro 2026开售 麒麟T93芯片4.7mm厚10400mAh续航最长平板5999元起",
        category=AICategory.DIGITAL_PRODUCT,
        organization="华为", country="中国",
        description="华为MatePad Pro 2026于8月14日正式首销，搭载麒麟T93芯片，机身厚度仅4.7mm，"
                    "配备10400mAh超大容量电池，是华为续航最长的平板，支持144Hz高刷屏和手写笔，起售价5999元。",
        key_metrics={"model": "华为MatePad Pro 2026", "chip": "麒麟T93", "thickness_mm": 4.7,
                     "battery_mah": 10400, "screen_refresh_hz": 144, "stylus": True,
                     "positioning": "华为续航最长平板", "price_start": 5999, "sale_date": "2026-08-14"},
        ram_gb=0, rom_gb=0, price_start_rmb=5999,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="超薄大电池平板的低功耗芯片+高能量密度电池技术，"
                              "为机器人手持示教终端、移动运维平板提供产品设计和技术参考",
        deployment_ready=True,
        tags=["华为MatePad Pro 2026", "麒麟T93", "4.7mm超薄", "10400mAh", "华为续航最长平板", "144Hz高刷", "手写笔", "5999元起"]
    ),

    AIProduct(
        product_id="NET-001", name="广东电网AI调度员明月 多智能体协同PINN-GNN物理嵌入省级电网秒级决策落地",
        category=AICategory.AI_AGENT,
        organization="深圳市人工智能与机器人研究院（AIRS）+广东电网", country="中国",
        description="超大规模省级电网多智能体协同AI调度员\"明月\"，入选国家\"AI+能源电力\"典型成果案例（AI+调度类仅2项）。"
                    "国内首个集感知-决策-控制于一体的省级大电网AI智能调度产品，在广东电网全面推广。"
                    "架构：多智能体协同+大小模型协同。三大核心创新："
                    "①全域全息感知：多模态大模型+VLM-BLIP+知识图谱，异构量测/图像/调度知识统一语义空间；"
                    "②物理-因果双重引导调度大模型：PINN-GNN把电网物理规律嵌入图神经网络，Physics-DPO物理一致性偏好对齐，"
                    "输出不仅\"看起来合理\"且受物理规律约束，是大模型进入不容许试错的决策回路前提；"
                    "③分层多智能体知识嵌入学习框架：针对源-网-荷天然分层结构，知识嵌入压缩探索空间，"
                    "从领域知识出发而非从零学习。"
                    "解决省级电网难点：百万设备全天候监控、秒级决策、物理硬约束不可违背、不容许在线试错、源网荷分层分布式协同。",
        key_metrics={"product": "AI调度员\"明月\"", "institutions": ["AIRS深圳人工智能与机器人研究院", "广东电网"],
                     "award": "国家\"AI+能源电力\"典型成果（调度类仅2项）",
                     "architecture": "多智能体协同+大小模型协同",
                     "scale": "省级大电网（百万设备全天候监控）",
                     "core_innovations": {
                         "1_perception": "全域全息感知（多模态大模型+VLM-BLIP+知识图谱，统一语义空间）",
                         "2_physics_ai": "PINN-GNN（物理嵌入图神经网络）+Physics-DPO（物理一致性偏好对齐）——大模型进入不容错决策回路关键",
                         "3_hierarchical_control": "分层多智能体知识嵌入学习框架（源网荷分层，知识嵌入压缩探索空间）"
                     },
                     "key_challenges_solved": ["百万级状态空间", "秒级决策要求", "物理硬约束不可违", "不容许在线试错",
                                              "源网荷分层分布式协同"],
                     "deployment": "广东电网全面推广"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-07",
        relevance_to_robotics="PINN物理嵌入神经网络+分层多智能体+知识嵌入学习是机器人控制大模型落地的核心技术路径——"
                              "机器人同样有物理约束（运动学/动力学）、分层控制（感知/规划/执行）、不容许试错（安全），技术栈完全通用",
        deployment_ready=True,
        tags=["AI调度员明月", "广东电网", "多智能体协同", "PINN-GNN物理嵌入", "Physics-DPO", "省级大电网", "秒级决策", "物理约束AI", "国家典型成果"]
    ),

    AIProduct(
        product_id="ROB-078", name="DJI大疆Agras T50农业无人机 40kg喷药50kg播撒IP67 5万+部署全球100国售价15000美元",
        category=AICategory.AGRICULTURE,
        organization="大疆创新（DJI）", country="中国",
        description="全球排名第一的专业农业无人机，RoboScore评分84.6/100。"
                    "40kg喷洒药箱+50kg播撒箱双负载，IP67防尘防水等级。"
                    "已在全球100+国家部署超过5万台，是全球应用最广泛的农业无人机产品。"
                    "支持全自主作业航线规划、地形跟随、多机协同、AI作物识别等功能。",
        key_metrics={"model": "DJI Agras T50", "ranking": "全球农业机器人#1（RoboScore 84.6）",
                     "spray_tank_kg": 40, "spread_tank_kg": 50, "ip_rating": "IP67",
                     "countries": "100+", "deployed_units": "5万+",
                     "price_usd": 15000,
                     "features": ["全自主作业规划", "地形跟随", "多机协同", "AI作物识别"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026",
        relevance_to_robotics="农业无人机是大规模商用最成功的空中机器人系统，其飞控、视觉避障、自主规划、多机协同技术"
                              "可迁移至工业巡检无人机、物流配送无人机、应急救援无人机等各类空中机器人平台",
        deployment_ready=True,
        tags=["大疆Agras T50", "农业无人机", "40kg喷药/50kg播撒", "IP67", "5万+部署", "100+国家", "1.5万美元", "全球第一"]
    ),

    AIProduct(
        product_id="ROB-079", name="John Deere See & Spray Ultimate AI精准除草 36摄像头12mph作业减药77%售价50万美元",
        category=AICategory.AGRICULTURE,
        organization="John Deere（约翰迪尔）", country="美国",
        description="全球排名第二的农业机器人产品，RoboScore评分84.2/100。"
                    "AI深度学习识别杂草与作物，精准对杂草喷施除草剂，可减少77%化学药剂使用。"
                    "36个摄像头横跨120英尺（约36.6米）喷杆，作业速度12mph（约19.3km/h）。"
                    "技术源自2017年John Deere以3.05亿美元收购Blue River Technology。",
        key_metrics={"model": "John Deere See & Spray Ultimate", "ranking": "全球农业机器人#2（RoboScore 84.2）",
                     "ai_core": "深度学习杂草识别", "cameras": 36, "boom_width_ft": 120,
                     "speed_mph": 12, "chemical_reduction": "77%",
                     "acquisition": "Blue River Technology（$3.05亿收购）",
                     "price_usd": 500000},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026",
        relevance_to_robotics="大规模多摄像头实时视觉识别+精准执行是工业机器人高速分拣、"
                              "质检机器人、公路维护机器人等场景的核心技术，作业速度和识别精度可作为行业Benchmark",
        deployment_ready=True,
        tags=["John Deere See & Spray", "AI精准除草", "36摄像头", "减药77%", "120英尺喷杆", "12mph作业", "3.05亿收购", "50万美元"]
    ),

    AIProduct(
        product_id="REN-063", name="美国Carbon Robotics LaserWeeder 2激光除草机器人 30个CO2激光每小时20万杂草零化学",
        category=AICategory.AGRICULTURE,
        organization="Carbon Robotics", country="美国",
        description="拖拉机牵引式自主除草系统，使用高功率激光消灭杂草，零化学药剂。"
                    "AI实时识别杂草并摧毁，每小时可消灭20万株杂草，配备30个CO2激光器实现毫米级精度。"
                    "RoboScore评分81.6/100，全球农业机器人排名第6。"
                    "纯物理除草方式完全避免化学除草剂对土壤和作物的污染。",
        key_metrics={"model": "Carbon Robotics LaserWeeder 2",
                     "type": "拖拉机牵引式自主激光除草",
                     "ai": "实时杂草识别AI", "lasers": "30个CO2激光器",
                     "weeds_per_hour": 200000, "precision": "毫米级",
                     "chemical_free": True,
                     "roboscore": 81.6, "ranking": "全球农业机器人#6"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026",
        relevance_to_robotics="激光除草的AI实时识别+激光精准打击技术组合可迁移至激光加工机器人、"
                              "工业激光清洗、精密激光切割等工业机器人场景",
        deployment_ready=True,
        tags=["Carbon Robotics", "LaserWeeder 2", "激光除草", "30个CO2激光", "20万株/小时", "毫米精度", "零化学药剂", "物理除草"]
    ),

    AIProduct(
        product_id="ROB-080", name="北京人形开源青龙通用人形机器人 1.85米80kg 43自由度396Nm峰值扭矩400TOPS五感融合",
        category=AICategory.HUMANOID_ROBOT,
        organization="国家地方共建人形机器人创新中心（北京）", country="中国",
        description="全球首款通用人形机器人开源公版机，由工信部和上海市政府2024年5月共同授牌中心打造。"
                    "科研团队硕博士占比约80%，核心研发团队是国内最早开展仿生腿足式机器人研究团队之一，"
                    "核心技术经过十多年技术沉淀，构建仿生机器人核心技术体系，建立控制/感知/交互核心技术群。"
                    "现场可实现行走、对话、做家务（识别桌面面包水果、分类摆放）等能力，"
                    "包含人形机器人平台技术、具身智能、数据集和智能训练场四大技术板块全部开源。"
                    "搭载'朱雀'具身大脑（多模态大模型指挥调度中心，感知/任务理解/记忆能力）和'玄武'小脑模型。",
        key_metrics={"product": "青龙（Blue Dragon）开源公版人形机器人",
                     "announce_venue": "2024世界人工智能大会",
                     "organization": "国家地方共建人形机器人创新中心（浦东）",
                     "team_composition": "硕博士占比约80%",
                     "rnd_history_years": "10+年技术沉淀（国内最早仿生腿足团队之一）",
                     "open_source_modules": ["人形机器人平台技术", "具身智能模型", "数据集", "智能训练场"],
                     "height_m": 1.85, "weight_kg": 80,
                     "dof_total": 43, "joint_types": "10种共31个关节模组",
                     "peak_torque_nm": 396, "peak_torque_density_nmkg": 200,
                     "leg_design": "轻量化高刚度低惯量+高扭矩密度轴向电机（复杂地形稳态行走）",
                     "arm_hand": "7自由度机械臂+集成触觉感知五指灵巧手（精细操作）",
                     "power": "能量回收系统+输出稳压管理电源，续航3-4小时（复杂工况）",
                     "computing_tops": 400, "sensors_fusion": "视/听/触/嗅/动五感融合",
                     "brain_models": {"cerebrum": "朱雀具身大脑（多模态大模型指挥调度）",
                                      "cerebellum": "玄武小脑模型"},
                     "capabilities_demo": ["行走", "自然语言对话", "桌面物体识别（面包/水果）",
                                           "分类摆放物品", "做家务"],
                     "technology_modules": ["行走与驱动系统", "操纵与作业系统", "感知与控制系统"]},
        maturity=MaturityLevel.OPEN_SOURCE,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2024-08",
        relevance_to_robotics="青龙作为全球首个人形机器人开源公版机，其10年技术沉淀的硬件设计（关节模组/驱动/灵巧手）"
                              "和大小脑软件架构（朱雀大脑+玄武小脑）为整个人形机器人行业提供基础参考平台，开源模式加速技术迭代",
        deployment_ready=True,
        tags=["北京人形青龙", "开源公版机", "1.85米80kg", "43自由度", "396Nm", "200Nm/kg", "400TOPS", "五感融合", "朱雀大脑玄武小脑", "10年研发"]
    ),

    AIProduct(
        product_id="ROB-081", name="越疆鹿萌DOBOT LUMO全球首款具身全栖人形陪伴机器人 1.3米空弈大模型多模态情绪感知四栖能力",
        category=AICategory.HUMANOID_ROBOT,
        organization="越疆科技（DOBOT）", country="中国",
        description="2026年8月5日正式亮相，全球首款具身全栖人形机器人，定位C端消费陪伴市场，"
                    "标志越疆完成工业/商用/文旅/消费全场景生态闭环。越疆作为国内少有的覆盖全场景具身智能企业，"
                    "将深耕多年的工业级运动控制、机器视觉、安全交互技术系统性降维应用至消费级场景。"
                    "依托全栈自研'空弈'具身大模型，突破传统语音陪伴产品'只闻其声、不见其形、不能行动'的行业瓶颈，"
                    "实现多模态情绪感知、三维空间理解与主动行动、自主学习与长期进化三大核心突破。"
                    "产品主张'智生非凡，渐入家境'。",
        key_metrics={"product": "越疆鹿萌 DOBOT LUMO", "launch_date": "2026-08-05",
                     "category": "全球首款具身全栖陪伴人形机器人",
                     "height_m": 1.3,
                     "company_background": "工业协作机器人+多足巡检+超仿生文旅全场景布局，"
                                           "工业级运动控制/机器视觉/安全交互技术降维",
                     "ai_model": "空弈具身大模型（全栈自研）",
                     "core_breakthroughs": ["多模态情绪感知", "三维空间理解与主动行动", "自主学习与长期进化"],
                     "four_amphibious_dimensions": {
                         "space": "空间全栖：自主导航+三维空间感知+复杂地形适配，自由穿梭家庭/办公/校园/公共场景",
                         "role": "角色全栖：独居人群生活搭子/年轻家庭育儿助手/学龄儿童科普伙伴/校园AI教学载体",
                         "capability": "能力全栖：视觉情绪识别+环境动态感知+语音交互+自主移动+肢体交互，"
                                       "从被动应答升级为主动感知与服务",
                         "lifecycle": "周期全栖：真实场景数据闭环+算法迭代，伴随用户成长持续进化"
                     },
                     "scenes": ["职场生活", "家庭陪护", "儿童成长", "校园教育"],
                     "ipo_status": "越疆科技创业板IPO 2026-07-22过会（申报到过会仅86天）"},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-05",
        relevance_to_robotics="工业级技术降维到消费级是人形机器人成本下降、走向家庭的关键路径；"
                              "四栖（空间/角色/能力/周期）产品定义框架为服务机器人/陪伴机器人产品设计提供范式参考",
        deployment_ready=True,
        tags=["越疆鹿萌LUMO", "具身全栖机器人", "1.3米陪伴人形", "空弈大模型", "多模态情绪感知", "主动服务", "自主学习进化", "四栖定义", "工业技术降维"]
    ),

    AIProduct(
        product_id="ROB-082", name="1X NEO挪威美国家用人形机器人 167cm 30kg 75自由度仿生肌腱驱动22dB超静$20000/月$499",
        category=AICategory.HUMANOID_ROBOT,
        organization="1X Technologies（原Halodi Robotics）", country="挪威/美国",
        description="全球首款面向私人家庭的消费级人形机器人，OpenAI领投超1.25亿美元融资，估值100亿美元。"
                    "2014年5月创立于挪威莫斯，创始人Bernt Oivind Bornich（机器人与纳米电子学背景）。"
                    "刻意偏离主流重负载工业人形路线，定位消费级家用，优先安全、静音、自然人机交互。"
                    "NEO Beta 2024年8月发布，NEO Gamma 2025年2月改进，2025年10月28日开放消费者预订，2026年美国交付。"
                    "人在回路远程操作模式：当前板载AI独立完成60-70%家庭任务，不熟悉任务可预约VR远程操作员完成，系统同时学习。"
                    "2026年1月发布1X World Model物理基础生成视频模型（通过看视频学新任务）；4月Hayward工厂投产（美国垂直整合度最高人形机器人厂，"
                    "首年产能1万台，2027年底目标10万台/年）；6月成立World Model Lab；7月9日发布25自由度肌腱驱动灵巧手量产版（物理世界API）。",
        key_metrics={"product": "1X NEO", "company": "1X Technologies（原Halodi Robotics）",
                     "founding": "2014年5月 挪威莫斯", "founder": "Bernt Oivind Bornich",
                     "investors": ["OpenAI", "Samsung Next", "EQT Ventures", "Tiger Global"],
                     "funding_total_usd_yi": ">1.25亿", "valuation_2025_usd_yi": 100,
                     "preorder_date": "2025-10-28", "first_delivery": "2026年美国交付",
                     "factory": "NEO Factory 美国加州Hayward（2026年4月）",
                     "factory_capacity_year1": 10000, "capacity_target_2027": 100000,
                     "height_cm": 167, "weight_kg": 30,
                     "dof_total": 75, "hand_dof": "25（22手指/手掌+3手腕）",
                     "actuation": "肌腱驱动Tendon Drive（仿生设计）",
                     "exterior": "柔软防夹伤外壳soft pinch-free exterior",
                     "noise_db": 22, "computer": "1X NEO Cortex（NVIDIA Jetson Thor）",
                     "battery_hours": 5.5,
                     "autonomy_launch": "60-70%任务无需人工介入",
                     "teleop": "VR头显远程操作员+人在回路学习",
                     "pricing": {"early_access_usd": 20000, "subscription_monthly_usd": 499},
                     "versions": ["NEO Beta 2024-08", "NEO Gamma 2025-02", "2026量产灵巧手 2026-07-09"],
                     "world_model": "1X World Model 2026-01（物理基础视频生成模型，看视频学任务）",
                     "world_model_lab": "2026-06成立",
                     "design_philosophy": "刻意区别于重载工业人形，优先安全/安静/自然人机交互，专为家庭设计",
                     "future_directions": ["提升板载AI自主率至90%+", "量产10万台/年",
                                           "扩大World Model Lab研发通用家庭自主能力",
                                           "灵巧手作为'物理世界API'开发生态"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2025-10预订/2026交付",
        relevance_to_robotics="NEO代表人形机器人从工业场景向家庭场景跨越的标杆路线：轻量化（30kg）+仿生肌腱驱动+超静音（22dB）"
                              "+人在回路学习+世界模型视频训练，为消费级人形机器人产品形态、技术路线、商业模式（订阅制）提供完整参考",
        deployment_ready=True,
        tags=["1X NEO", "家用人形机器人", "167cm 30kg", "75自由度", "仿生肌腱驱动", "22dB超静音", "$20000/$499月", "OpenAI投资", "人在回路", "World Model视频学习", "Hayward工厂"]
    ),

    AIProduct(
        product_id="ROB-083", name="众擎T800重载级全尺寸通用人形机器人 1.73米75kg41自由度固态电池铝合金覆盖件18万元起批量交付",
        category=AICategory.HUMANOID_ROBOT,
        organization="众擎机器人", country="中国",
        description="众擎机器人旗下首款重载级全尺寸通用人形机器人，2025年8月世界机器人大会首次公开亮相，"
                    "2025年12月2日正式发布定价，2026年7月24日郑州云智智能制造基地批量下线发运客户。"
                    "1.73米黄金成人身高、75kg优化自重拟人化形态，搭载41个高自由度关节，"
                    "配备固态电池与铝合金外覆盖件，可在重载及高动态场景下持续稳定作业。"
                    "多传感器融合感知系统集成视觉/触觉/力觉等多种传感器，依托内置高性能运算单元快速精准决策。"
                    "推出基础版/生态版（开源版）/锐化版（Pro版）/旗舰版（Max版）四大梯度产品覆盖不同场景。"
                    "2026年8月完成B轮2亿元融资。",
        key_metrics={"product": "众擎T800", "company": "众擎机器人",
                     "first_show": "2025-08 WRC世界机器人大会",
                     "release_date": "2025-12-02", "mass_delivery": "2026-07-24 郑州基地批量下线",
                     "round_b": "2亿元 2026-08",
                     "height_m": 1.73, "weight_kg": 75,
                     "dof": 41,
                     "materials": {"outer_panels": "铝合金外覆盖件",
                                   "battery": "行业首款人形机器人专用固态动力电池"},
                     "battery_life_hours": "4-5小时稳定续航",
                     "sensors": "多传感器融合（视觉+触觉+力觉）",
                     "performance": "重载及高动态场景下持续稳定作业",
                     "versions": [{"name": "基础版", "price_wan": 18, "target": "基础应用"},
                                  {"name": "生态版（开源版）", "target": "开发者/科研/二次开发"},
                                  {"name": "锐化版Pro", "target": "进阶工业/商业应用"},
                                  {"name": "旗舰版Max", "target": "高端重载/科研"}],
                     "price_start_wan": 18,
                     "scenes": ["智慧交管", "商业服务", "工业智造", "科研教育", "全域场景"],
                     "events": ["2025-12机甲拳王格斗赛核心机型", "2026-01 CES亮相", "2026-07批量交付"],
                     "design_optimizations": ["黄金成人身高1.73m", "75kg优化自重", "拟人化形态"],
                     "future_directions": ["持续扩大量产产能", "拓展工业/商业/科研多场景部署", "开源生态建设"]},
        maturity=MaturityLevel.MASS_PRODUCTION,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2025-12发布/2026-07批量交付",
        relevance_to_robotics="T800作为重载级全尺寸人形18万元起定价、固态电池首次搭载、四大版本梯度覆盖全场景、2026年7月批量下线，"
                              "标志中国人形机器人从样机阶段正式进入批量交付元年，固态电池应用为后续人形机器人能源方案提供新选择",
        deployment_ready=True,
        tags=["众擎T800", "重载全尺寸人形", "1.73米75kg", "41自由度", "固态电池", "铝合金覆盖件", "18万元起", "四版本梯度", "2026-07批量交付", "B轮2亿"]
    ),

    AIProduct(
        product_id="COMP-001", name="华为MateBook Fold非凡大师鸿蒙折叠电脑 18寸双层OLED UTG玻璃40微米玄武水滴锆基液态金属铰链7.3mm/1.16kg 24999元",
        category=AICategory.MOBILE_COMPUTER,
        organization="华为", country="中国",
        description="华为首款鸿蒙折叠屏PC，2026年8月5日发布会发布、8月14日全面开售。"
                    "定位折叠形态大屏生产力工具，补齐折叠PC原生手写交互空白，硬件/软件/生态同步升级，"
                    "适配商务办公/专业设计/金融分析多行业场景。华为折叠屏技术多年积累从手机延伸到大尺寸PC，"
                    "从材料、铰链、屏幕到软件全栈自研。",
        key_metrics={"product": "华为MateBook Fold非凡大师", "release_date": "2026-08-05",
                     "sale_date": "2026-08-14",
                     "positioning": "18英寸手写折叠屏鸿蒙电脑 非凡大师旗舰",
                     "design": {"design_language": "非凡大师高端商务设计",
                                "colors": ["流光金", "天际白", "幻影黑"],
                                "morphology": "折叠形态（18寸展开/13寸折叠便携）",
                                "stand": "业内首款隐藏式支架转轴",
                                "ergonomics": "支持100-120度无级悬停，适配书写/观影/办公多姿态"},
                     "materials": {"screen_glass": "大尺寸量产UTG超薄玻璃（40μm厚度）",
                                   "screen_panel": "双层OLED（双发光层堆叠）",
                                   "hinge_main_shaft": "锆基液态金属材料",
                                   "hinge_structure": "MIM高强钢结构件",
                                   "hinge_architecture": "榫卯阻尼三段式架构（传统榫卯工艺理念融合）"},
                     "manufacturing_rnd": {"hinge_name": "玄武水滴铰链",
                                           "hinge_precision": "12个精密机加工钛合金组件（海外版本）/榫卯架构",
                                           "cycle_test": "20万次开合零像素衰减（远超行业20万次基准）",
                                           "screen_process": "UTG玻璃全新复合结构",
                                           "cooling": "超薄逆重力散热架构",
                                           "antenna": "双模叠层天线+无线桥接技术",
                                           "rnd_effort": "折叠屏技术多年积累从手机到PC全栈延伸"},
                     "specs": {"unfolded_screen_inch": 18, "folded_screen_inch": 13,
                               "thickness_unfolded_mm": 7.3, "thickness_closed_mm": 14.9,
                               "thickness_avg_mm": 11.2, "weight_kg": 1.16,
                               "weight_with_accessories_kg": 1.637,
                               "resolution": "3.3K（3296×2472 4:3展开）",
                               "folded_resolution": "2472×1648（3:2 双屏独立）",
                               "refresh_rate": "LTPO自适应（90Hz动态/10Hz静态）",
                               "peak_brightness_nits": 1600, "screen_ratio": "92%屏占比",
                               "ar_coating_reflectivity": "2.5%（AR镀膜）",
                               "pwm_dimming": "1440Hz高频PWM调光",
                               "panel_efficiency_gain": "+30%能效（双层对比单层）",
                               "panel_lifespan_gain": "3倍寿命",
                               "screen_durability": {"impact_resistance_gain": "+90%抗冲击",
                                                     "bending_resistance_gain": "10倍抗弯曲形变",
                                                     "compression_gain": "+30%抗挤压",
                                                     "stylus_taps": "500000次手写点击",
                                                     "certification": "瑞士SGS金标五星屏幕抗跌落冲击认证"},
                               "processor": "麒麟X90 Plus", "tdp_w": 28,
                               "performance_gain": "+25%整机综合性能",
                               "ram_gb": [24, 32], "ssd_tb": [0.5, 1, 2],
                               "battery_wh": 75, "fast_charge_w": 140, "reverse_charge_w": 66,
                               "video_playback_h": 14, "cloud_meeting_h": 12,
                               "camera_front_mp": 8, "os": "HarmonyOS 6.1",
                               "stylus": "HUAWEI M-Pen 3（纯平书写/分屏书写/远场空鼠三模式）",
                               "audio": "联合声场渲染360度移动全景声"},
                     "pricing": {"24GB+512GB": 24999, "24GB+1TB": 26999, "32GB+2TB": 29999},
                     "software_optimizations": {"ark_engine": ["WPS大文件打开+30%", "悟空图像处理+25%",
                                                              "剪映剪辑速度+23%"],
                                                "hyper_memory_compression": "+50%压缩效率/同时开大文件+40%",
                                                "xiaoyi_meeting": "本地离线模型语音降噪/转写/发言人区分/自动纪要",
                                                "xiaoyi_research": "多行业专家智能体协同分析",
                                                "native_apps": ["华为笔记（无界画布/全景智记）",
                                                                "天生会画PC首秀（1000+专业笔刷/完整图层/调色）"],
                                                "third_party": ["WPS双屏演讲者视图", "中望CAD双屏审图标注",
                                                                "博思白板分屏协同", "东方财富双屏盯盘标注",
                                                                "悟空图像双屏闪绘（上屏AI/下屏手绘）",
                                                                "剪映"]},
                     "future_directions": ["持续扩展鸿蒙PC原生生态", "优化折叠形态手写体验",
                                           "更多行业软件双屏深度适配", "下一代更轻更薄产品迭代"]},
        ram_gb=32, rom_gb=2048, price_start_rmb=24999, price_top_rmb=29999,
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-05发布/08-14开售",
        relevance_to_robotics="玄武水滴铰链（锆基液态金属+MIM高强钢+榫卯架构+20万次开合）、UTG 40微米超薄玻璃、"
                              "双层OLED LTPO、逆重力散热等精密制造与材料技术，可迁移至机器人关节精密制造、"
                              "机器人柔性显示屏、可穿戴机器人交互终端等场景；鸿蒙分布式技术为机器人多终端协同提供参考",
        deployment_ready=True,
        tags=["华为MateBook Fold非凡大师", "18寸双层OLED", "UTG玻璃40μm", "玄武水滴铰链", "锆基液态金属", "MIM高强钢", "榫卯架构", "麒麟X90 Plus", "7.3mm/1.16kg", "M-Pen 3手写", "24999元起", "SGS五星认证"]
    ),

    AIProduct(
        product_id="ROB-084", name="陶世智能微型环面包络正交减速器 体积-40%±0.5弧分精度1300MPa强度1万小时寿命10万台灵巧手订单",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="陶世智能科技（深圳）", country="中国",
        description="精密减速器企业，2016年成立总部深圳，研发生产正交90度微型减速器及机器人关节模组。"
                    "核心产品微型环面包络蜗轮蜗杆减速器，把减速与转角功能集成单一结构，更小体积更高精度动力传输。"
                    "2026年8月完成超亿元融资（国创集团/海川聚义/杭州众燊/新智资本，德太资本FA），资金用于产品研发/产线扩建/市场拓展。"
                    "成立初期面向工业自动化，2024年获航天领域首笔订单后进入消费电子制造龙头供应链，"
                    "2025年重点转向机器人关节模组，推出高度集成灵巧手关节模组兼容直驱/连杆/腱绳/混合驱动。"
                    "已与近百家机器人企业合作，灵巧手领域签署10万台关节模组供货协议。",
        key_metrics={"company": "陶世智能", "founded": "2016", "headquarters": "深圳",
                     "round": "超亿元融资（2026-08）",
                     "investors": ["国创集团", "海川聚义", "杭州众燊", "新智资本"],
                     "fa": "德太资本",
                     "core_product": "微型环面包络蜗轮蜗杆减速器（正交90度）",
                     "design_principle": "传统蜗轮蜗杆单齿啮合→优化齿面接触结构+环面包络设计→多齿同时啮合",
                     "advantages_vs_traditional": {"volume_reduction": "-40%体积（省去额外转角器）",
                                                   "no_angle_needed": "集成90度转向无需额外转角机构",
                                                   "precision_arcmin": "±0.5弧分",
                                                   "tensile_strength_mpa": 1300,
                                                   "life_hours": 10000},
                     "manufacturing_self_developed": {"equipment": "进口设备重新设计开发7轴5联动磨削方案（解决环面蜗杆高精度加工难题）",
                                                      "testing": "自主搭建测试设备验证精度/寿命/可靠性",
                                                      "materials_lubrication": "优化材料和润滑体系提高效率与寿命"},
                     "factory_base": {"current_area_m2": 20000, "current_output": "年产值5亿元/年产50-70万关键模组",
                                      "new_factory": "建设中，投产后年产能100-150万关键模组"},
                     "history": {"2016-founded": "成立，工业自动化起步",
                                 "2024-aerospace": "获航天领域首笔订单，进入消费电子龙头供应链",
                                 "2025-humanoid": "研发重点转向机器人关节模组，推出灵巧手高度集成关节模组",
                                 "2026-august": "完成超亿元融资，灵巧手10万台订单",
                                 "customers": "近百家机器人企业合作/果链/头部灵巧手企业供货"},
                     "dexterous_hand_module": {"compatibility": ["直驱", "连杆驱动", "腱绳驱动", "混合驱动"],
                                               "signed_order_units": 100000},
                     "industry_context": {"actuator_cost_ratio": "执行器系统（电机/减速器/丝杠）占人形整机成本45%",
                                          "sensor_ratio": "传感器占15%，合计核心零部件>60%",
                                          "localization": "减速器是国产替代核心环节"},
                     "future_directions": ["扩建产能至100-150万模组/年", "拓展人形机器人关节全系列产品",
                                           "深化灵巧手领域头部客户合作", "持续材料工艺优化提升寿命精度"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08",
        relevance_to_robotics="微型正交减速器是灵巧手狭小空间集成的关键突破——陶世环面包络设计在±0.5弧分精度、1300MPa强度、"
                              "1万小时寿命基础上体积缩小40%，解决了灵巧手关节小型化、高精度、正交传动三大难题，"
                              "7轴5联动自研磨削工艺、材料润滑体系自建为核心零部件国产化提供完整路径参考",
        deployment_ready=True,
        tags=["陶世智能", "微型正交减速器", "环面包络蜗轮蜗杆", "体积-40%", "±0.5弧分", "1300MPa", "1万小时", "7轴5联动磨削", "10万台灵巧手订单", "超亿元融资", "深圳2016"]
    ),

    AIProduct(
        product_id="ROB-085", name="HONPINE宏品HPJM一体化人形关节模组 PRO谐波版六合一集成192Nm/kg扭矩密度31.5mm中空120mm外径减重1/3",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="HONPINE宏品", country="中国",
        description="2026年5月8-11日郑州工业装备博览会发布HPJM一体化关节模组系列，面向下一代人形机器人设计。"
                    "采用高度集成结构设计理念，将驱动器/无框力矩电机/减速器/制动器/编码器/传感器六大核心组件深度集成于单一紧凑单元。"
                    "模块化平台策略提供50+种关节模组规格，支持不同性能等级和成本结构灵活开发，大幅降低人形机器人开发门槛。"
                    "分PRO系列（自研超薄谐波减速器）两大技术路线，针对人形上肢精密作业优化，"
                    "通过柔轮优化和材料创新解决传统谐波减速器体积大/发热/寿命有限等问题。",
        key_metrics={"product": "HONPINE HPJM一体化关节模组系列", "exhibition": "2026郑州工博会（5月8-11日）",
                     "design_concept": "六核合一高度集成（驱动器+无框力矩电机+减速器+制动器+编码器+传感器）",
                     "platform_strategy": "模块化平台50+规格适配不同性能/成本需求",
                     "pro_series": {"reducer": "自研超薄谐波减速器",
                                    "optimization_target": "人形上肢精密作业/负载需求",
                                    "traditional_issues_solved": ["体积大", "发热严重", "寿命有限"],
                                    "solutions": ["柔轮结构优化", "材料创新"]},
                     "thermal_management": "高效散热结构，防止过热性能衰减",
                     "hollow_shaft": {"design": "中空走线设计",
                                      "hollow_ratio": ">11%",
                                      "bore_mm": 31.5,
                                      "benefit": "方便线缆走线，减少线缆磨损，满足人形布线可靠性要求"},
                     "encoder": {"type": "自研24位双编码器",
                                 "features": ["多圈绝对值断电记忆", "高精度定位", "重启无需重新回零校准"]},
                     "brake": {"type": "凸极磁路永磁制动器",
                               "design": "电机与制动器一体化结构",
                               "benefits": ["节省轴向安装空间", "提升制动扭矩", "增强关节安全可靠性"]},
                     "specs": {"peak_torque_density_nmkg": 192,
                               "outer_diameter_mm": 120,
                               "hollow_bore_mm": 31.5,
                               "weight_reduction": "比传统方案减重>1/3",
                               "energy_consumption": "整体能耗显著降低",
                               "volume_optimization": "同扭矩下体积极致优化"},
                     "motion_capabilities": ["跑步", "跳跃", "动态平衡"],
                     "future_directions": ["拓展全系列关节模组覆盖人形全身关节",
                                           "进一步提升扭矩密度至200+Nm/kg",
                                           "优化散热支持更高持续功率输出",
                                           "扩大中空比方便更复杂走线",
                                           "大规模量产降本"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-05",
        relevance_to_robotics="六合一高度集成+192Nm/kg峰值扭矩密度+31.5mm大中空+减重1/3，"
                              "代表了人形机器人关节模组集成化、轻量化、高性能的明确发展方向，"
                              "中空走线设计解决人形布线痛点，24位双编码器断电记忆免去重新校准大幅提升实用性",
        deployment_ready=True,
        tags=["HONPINE宏品", "HPJM关节模组", "六合一集成", "PRO超薄谐波", "192Nm/kg", "31.5mm中空", "120mm外径", "减重1/3", "24位双编码器", "凸极磁路制动", "50+规格"]
    ),

    AIProduct(
        product_id="ROB-086", name="人形机器人2026交付元年产业数据 全球H1出货1.91万台+272%中国占97%进厂验证规模化启动",
        category=AICategory.HUMANOID_ROBOT,
        organization="行业综合数据（Smart Analytics/工信部/高工机器人）", country="全球/中国",
        description="2026年是人形机器人从'展会样机'走向'交付元年'的转折点，8月被称为'机器人超级月'——"
                    "世界机器人大会8月19-23日北京亦庄、宇树科技8月下旬A股上市、特斯拉Optimus量产产线安装调试三件大事密集落地。"
                    "产业叙事从空翻跳舞视频切换到进厂验证、高工时计费、量产爬坡的真实商业化阶段。",
        key_metrics={"period": "2026年上半年（交付元年）",
                     "global_shipments_units": 19100, "yoy_growth": "+272%",
                     "china_share": ">97%全球出货量",
                     "top6_all_china_share": "87.87%（前六全部中国厂商）",
                     "china_production": {"2025_total": "约2万台", "2026_h1": ">4万台", "2026_full_year_ggii": "10-20万台"},
                     "application_structure": {"industrial_commercial_share": ">70%", "previous_year_share": "50%"},
                     "leading_production_capacity": {"unitree_g1": "杭州工厂月产200台，Q4目标500台/月；累计下线约12500台",
                                                     "ubtech_walker_s": "月产150台，2026目标3000台",
                                                     "agibot_a2": "月产100台", "fourier_gr2": "月产80台"},
                     "factory_deployments": {"ubtech_in_neo": "蔚来合肥工厂3个月验证获量产准入，首批20台编入生产序列执行车门锁检测/安全带安装",
                                             "byd": "比亚迪尧舜禹150台样机实训，深圳工厂50台宇树G1运营，年底扩至200台",
                                             "ubtech_in_foxconn": "Walker S进驻富士康，零部件分拣/视觉检测",
                                             "jd_cainiao": "最后一公里配送+仓储分拣试点"},
                     "government_procurement": {"state_grid": "年内计划采购8500台特种机器人，约68亿元"},
                     "unitree_ipo": {"price": "150.80元/股", "market_cap_yi": 610,
                                    "oversubscription": "45%超募", "ps_ratio": "35.89倍（2025收入）",
                                    "ipo_subscribers_wan": 978.46,
                                    "oversubscription_times": 8288, "winning_rate": "0.0181%",
                                    "funds_use": {"42亿募资": "50%具身大模型研发/50%扩产（2万→10万台年产能）"},
                                    "strategic_investors": ["全国社保基金", "DeepSeek深度求索（约1.41亿元）",
                                                           "中国石油集团", "腾讯"]},
                     "ipo_pipeline": {"dobot": "越疆创业板7月22日过会（86天）",
                                      "leju_yunshenchu": "乐聚/云深处5月底已问询",
                                      "agibot_galbot_zhongqing": "智元/银河通用/众擎资本化推进中"},
                     "valuation": {"apac_pe_median": 22, "us_pe_median": 28},
                     "key_quotes": {"song_yan": "松延动力田丰：2026是从'高流量视频'走向'高工时计费'的分水岭，拐点不在于空翻，"
                                                "在于能否顶住夜班、把笨活做稳、失手可控、交付可复制、责任算得清",
                                    "huayan_securities": "华源证券：产业从0到1验证期全面迈入1到10量产爬坡新阶段"},
                     "future_directions": ["2026全年产量突破10万台（工信部口径）",
                                           "进厂验证从单机测试向多机协同产线升级",
                                           "核心零部件（减速器/电机/灵巧手/传感器）国产替代加速",
                                           "消费级人形机器人（如1X NEO）开始家庭交付",
                                           "宇树上市带动全产业链估值重估（类比宁德时代带动锂电）"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="2026年人形机器人'交付元年'完整数据画像：出货量/产能/进厂场景/IPO/政策/估值全维度呈现，"
                              "清晰展示产业从样机到量产爬坡的关键转折，70%工业商业应用、97%中国份额、10-20万台全年预期、"
                              "进厂验证标准（夜班稳/笨活/失手可控/可复制/责任清晰）"
                              "为产业研究、投资判断、技术路线选择提供基准数据",
        deployment_ready=True,
        tags=["人形机器人交付元年", "H1全球1.91万台", "+272%增长", "中国占97%", "宇树IPO 610亿", "进厂验证", "蔚来/比亚迪/富士康", "国家电网68亿采购", "WRC2026超级月", "高工时计费"]
    ),

    AIProduct(
        product_id="EMB-032", name="第四届中国具身智能机器人产业大会（上海8.12-14）场景落地年 台科电感编码器/今飞智朗合金压铸件/魔迅HZ-EG1PRO电磁动捕手套集体亮相",
        category=AICategory.HUMANOID_ROBOT,
        organization="中国具身智能机器人产业大会组委会+多家展商", country="中国",
        description="8月12-14日上海举行第四届中国具身智能机器人产业大会暨展览会，标志着产业从技术原理/原型样机展示阶段进入场景落地年——"
                    "'十五五'规划纲要将具身智能列为未来产业之一，大会直击落地难题，围绕技术验证、成本压降、场景规模化三条主线搭建协作桥梁。"
                    "整机方面多台人形/双臂协作/四足机器人展示智能避障/精密装配/物料分拣实操能力；"
                    "上游核心零部件：深圳台科微电子自主研发电感编码器具有成本低/环境适应性强/系统简单三大优势，助力全球机器人长出'中国关节'；"
                    "浙江今飞智朗科技展出铝合金/镁合金压铸件产品，覆盖人形机器人关节/躯干/足部关键部位，兼顾减重与机械性能，解决复杂型腔/薄壁/高精度装配制造痛点，提供定制化零部件整体解决方案；"
                    "杭州魔迅科技发布HZ-EG1PRO新品电磁动作捕捉手套，采用电磁技术替代原有惯性技术，指尖采集精度达2毫米，破解传统采集设备精度不足、无效数据指数级上升问题，"
                    "支撑灵巧手算法验证、机器人整机及手部训练；全能具身智能已在小区门岗部署人形机器人替代保安、公园布局机器狗，与医院合作开发导诊机器人，落地场景拓展至工业/安防/康养/商业；"
                    "无锡锡山区东北塘街道携锡山智能机器人产业园亮相，依托当地高端装备/电动车/新能源八大产业集群+7000+工业企业集聚优势，重点发力工业机器人/协作机器人/智能制造关键零部件。",
        key_metrics={"event": "第四届中国具身智能机器人产业大会暨展览会", "location": "上海", "date": "2026-08-12至14",
                     "industry_stage": "从实验室走向生产线+场景落地年", "policy_context": "'十五五'规划具身智能列为未来产业",
                     "exhibits": ["整机（人形/双臂协作/四足）：智能避障/精密装配/物料分拣",
                                  "台科微电子电感编码器：成本低/环境适应性强/系统简单 助力'中国关节'",
                                  "今飞智朗铝合金/镁合金压铸件：覆盖关节/躯干/足部 兼顾减重机械性能 定制化方案",
                                  "魔迅HZ-EG1PRO电磁动作捕捉手套：电磁替代惯性 指尖精度2mm 解决无效数据问题",
                                  "全能具身：小区门岗保安/公园机器狗/医院导诊 工业/安防/康养/商业全场景",
                                  "无锡锡山智能机器人产业园：7000+工业企业支撑 重点发力工业/协作机器人及关键零部件"],
                     "conference_theme": "技术验证+成本压降+场景规模化", "future_directions": ["B端先行由易到难规模化应用", "特种服务场景优先试点", "配套仿真/调试/运维一体化服务包"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="大会集中展示了具身智能从技术原型到场景落地的完整产业图景，电感编码器/合金压铸件/电磁动捕手套三款核心零部件的亮相，"
                              "填补了关节传感、轻量化结构件、灵巧手数据采集三个关键环节的国产空白，为规模化量产奠定硬件底座",
        deployment_ready=True,
        tags=["第四届具身智能大会", "上海8.12-14", "场景落地年", "台科微电子电感编码器", "中国关节", "今飞智朗镁铝合金压铸件", "魔迅HZ-EG1PRO电磁动捕手套", "指尖精度2mm", "无锡锡山产业园", "B端先行"]
    ),

    AIProduct(
        product_id="ROB-086", name="时耘科技RD3 Ultra全尺寸特种人形机器人量产下线 174cm标准人身形7×24小时特种作业尖兵 天津河西764具身园首条产线投产",
        category=AICategory.HUMANOID_ROBOT,
        organization="时耘科技（天津）有限公司", country="中国",
        description="8月13日时耘科技首批全尺寸人形机器人RD3 Ultra下线仪式在天津河西区764具身智能产业主题园举行，"
                    "标志着时耘科技总部落户河西后在研发制造领域实现关键产业化突破。"
                    "时耘科技专注特种行业与高危作业场景机器人应用，构建研发/制造/销售/服务全产业链体系。"
                    "RD3 Ultra面向特种作业场景打造工业级全功能全尺寸人形机器人，174CM标准人身形可无缝适配人类作业环境与既有工器具，"
                    "全新本体架构叠加全球领先模型能力，拥有全时自主作业、全域复杂环境通行、全链路安全可控三大核心实力，号称'7×24小时在岗的特种作业尖兵'。"
                    "生态合作：与京东机器人合作开发的养老康养场景已在河西区正式落地，为'具身智能+医养陪护'提供标准化解决方案；"
                    "天津卡乐文化产业集团合作推进文旅客串、科普展演，人形机器人进商街进校园。"
                    "特色环节：'格斗大师'人格斗场景首次在北方地区亮相，两台全尺寸机器人展现出色动态平衡与抗冲击控制能力，精准复现人类出拳/侧身躲闪复杂动作，被击中后迅速调整姿态保持平衡，"
                    "展示复杂高危环境替代人工硬核实力；嘉宾参观天津地区首条特种全尺寸机器人生产线和整机测试中心，近距离观摩零部件组装/精密调试/整机测试全流程。"
                    "政策支持：天津市工信局/发改委/科技局联合出台《天津市智能机器人产业创新发展行动方案（2026-2028）》，明确支持河西区打造具身智能产业主题产业园。",
        key_metrics={"product": "时耘RD3 Ultra全尺寸特种人形机器人", "launch_date": "2026-08-13",
                     "hq_location": "天津河西区764具身智能产业主题园", "positioning": "特种行业高危作业场景工业级全功能全尺寸",
                     "specs": {"height_cm": 174, "form_factor": "标准人身形适配人类作业环境+既有工器具",
                               "core_capabilities": ["全时自主作业7×24小时", "全域复杂环境通行", "全链路安全可控"]},
                     "ecosystem_partners": [{"partner": "京东机器人", "cooperation": "养老康养场景落地河西 医养陪护标准化方案"},
                                            {"partner": "天津卡乐文化", "cooperation": "文旅融合/科普展演/进商街进校园"}],
                     "demo_features": "格斗大师北方首秀 动态平衡+抗冲击控制 出拳/躲闪/被击中后姿态恢复",
                     "production_line": "天津首条特种全尺寸机器人产线+整机测试中心 零部件组装→精密调试→整机测试全流程",
                     "policy": "天津市智能机器人产业创新发展行动方案（2026-2028）支持河西764具身园",
                     "future_directions": ["持续提升研发创新能力", "夯实规模化量产支撑", "赋能千行百业"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="RD3 Ultra量产标志着特种作业人形机器人从研发走向批量交付，174cm标准人身形+全时自主+全链路安全三大设计方向为特种人形（替代高危人工）树立了产品基准，"
                              "格斗场景动态平衡展示也验证了抗冲击控制技术成熟度，京东康养/卡乐文旅合作拓展了B端G端落地场景",
        deployment_ready=True,
        tags=["时耘RD3 Ultra", "特种人形量产", "174cm标准人身形", "7×24特种作业", "天津河西764具身园", "格斗大师北方首秀", "京东康养合作", "天津2026-2028机器人方案"]
    ),

    AIProduct(
        product_id="ROB-087", name="NVIDIA ScheduleStream通用时序规划框架+Kinova Gen3双臂协同 GPU加速1.9秒完成规划vs CPU31.4秒快16倍 任务成功率99%",
        category=AICategory.INDUSTRIAL_ROBOT,
        organization="NVIDIA Research + Kinova", country="美国/加拿大",
        description="NVIDIA最新发布ScheduleStream通用时序规划框架，首次在Kinova Gen3双机械臂实物平台完成全场景落地验证。"
                    "长期以来即便硬件拥有双机械臂，绝大多数规划算法只能串行作业（一臂操作一臂闲置），硬件潜力被严重浪费。"
                    "ScheduleStream依靠GPU并行采样、时序持续动作建模、惰性流Lazy-Stream采样算法三大创新，实现双臂异步并行无碰撞调度，任务总耗时平均减半，多物体杂乱场景规划成功率逼近99%。"
                    "Kinova Gen3七轴协作机械臂作为验证平台，拥有7个可无限旋转关节（区别于普通六轴），冗余自由度在双臂工作空间重叠时可灵活调整关节姿态规避碰撞，完美匹配动态臂间碰撞检测逻辑；"
                    "单臂自重仅10kg，最大持续负载4kg，既能抓取苹果/零件小件也可协同搬运堆叠重载，覆盖分拣/装箱/组装全场景；"
                    "可选集成深度视觉模块搭配GroundingDINO开源检测算法完成开放场景识别，内置关节扭矩传感器持续检测双臂交互碰撞，与ScheduleStream运行时动态碰撞约束形成双重安全保障；"
                    "支持快速模块化组装30分钟内完成双臂平台搭建，IP54防尘防水可拓展至移动双臂机器人研究，对比Franka Panda等竞品环境适应性更强。",
        key_metrics={"framework": "NVIDIA ScheduleStream通用时序规划框架",
                     "hardware_platform": "Kinova Gen3 7自由度双臂协作平台",
                     "core_innovations": ["GPU并行采样（cuRobo CUDA内核 逆解/碰撞检测批量计算毫秒级）",
                                          "时序持续动作建模（启动条件/运行约束/结束条件三阶段 双臂异步执行）",
                                          "Lazy-Stream惰性流调度（先骨架占位后按需采样 采样调用-62% 31.6s→6.8s）",
                                          "GPU批量球体碰撞检测（臂-物/臂-臂并行求交）"],
                     "kinova_gen3_specs": {"dof": "7（冗余自由度 臂间避碰）", "self_weight_kg": 10, "payload_kg": 4,
                                          "infinite_rotation_joints": 7, "ip_rating": "IP54防尘防水",
                                          "assembly_time_min": 30, "vision": "可选深度视觉+GroundingDINO",
                                          "safety": "关节扭矩传感器+算法层碰撞预判双重保障",
                                          "ecosystem": "Kortex API原生Python绑定 无需中间层"},
                     "performance": {"planning_success_rate": "GPU版99% vs 分层算法64% vs 串行99%（仅串行）vs原生Lazy 91%",
                                     "avg_planning_time_sec": {"gpu_accelerated": 1.9, "cpu_only": 31.4, "hierarchical": 28.3, "traditional_tamp": 6.5},
                                     "complex_4object_task_sec": {"gpu": 4.4, "hierarchical": 101.4, "success_rate_hier": "<10%"},
                                     "makespan_reduction": "平均缩短近一半 水果分拣串行4.2s→并行2.2s"},
                     "real_world_validation": "5大类仿真任务+21组实物演示 分拣/装箱/堆叠/物体交接/重抓取10类实操 连续百次重复无碰撞失败率<1%",
                     "project_site": "schedulestream.github.io", "language": "全Python开发 无PDDL直接代码定义",
                     "future_directions": ["大模型与调度框架深度融合", "简化任务交互", "拓展柔性分拣/轻型装配/移动服务机器人更多落地场景"]},
        maturity=MaturityLevel.RESEARCH,
        source="", source_tier=SourceTier.TIER2,
        publish_date="2026-08-14",
        relevance_to_robotics="ScheduleStream解决了双臂机器人长期串行作业的算力浪费难题——GPU加速将规划耗时从30秒级压缩至1.9秒（实时控制级），"
                              "99%成功率+Makespan减半+全Python开源生态大幅降低双臂协作落地门槛，"
                              "为柔性分拣/轻型装配/移动服务机器人等场景提供通用规划方案，标志着多臂协同从实验室走向实物验证",
        deployment_ready=False,
        tags=["NVIDIA ScheduleStream", "时序规划框架", "Kinova Gen3双臂", "GPU加速", "Lazy-Stream惰性采样", "1.9秒规划", "99%成功率", "Makespan减半", "GroundingDINO", "cuRobo", "开源Python", "柔性分拣/轻型装配"]
    ),

    AIProduct(
        product_id="EMB-033", name="中央企业机器人创新联合体将在WRC2026揭牌 国家队共研共用共享 国网六足巡检/北自所核电钢筋绑扎/中国电建5000台采购集中落地",
        category=AICategory.HUMANOID_ROBOT,
        organization="国务院国资委+工信部+多家央企", country="中国",
        description="具身智能机器人正从翻跟头/跳街舞的'炫技派'转变为特高压巡检/重载搬运/智能加油的'实战派'，在电力/石化/钢铁等重点工业领域生产一线加速落地。"
                    "2026世界机器人大会期间，国务院国资委将揭牌成立中央企业机器人创新联合体，整合全行业央企资源，补齐全具身智能量产短板。"
                    "此前工信部与国务院国资委已联合启动2026年度人形机器人与具身智能实景实训专项行动，提出到今年底'开启作业模式''带动形成万台级规模落地能力'。"
                    "典型落地案例："
                    "①国家电网：推出国内首款电力场景专用六足仿生巡检机器人，融合多源传感检测/5G量子加密/光明大模型智能分析技术，复杂狭矮空间通过率100%，"
                    "可精准识别局放/六氟化硫泄漏/设备漏液三类缺陷，实现数据加密回传/故障自动识别/隐患智能研判及处置建议自动生成；"
                    "②核电施工：机器人凭借'履带脚'和'麒麟臂'自主完成钢筋抓取/定位/旋拧高难度动作，人机协同下水平竖向钢筋绑扎效率提升4倍，预埋件安装效率提升8倍，质量合格率99.8%，推动工人从高强度体力劳动转型为技术管理者；"
                    "③北自所（北京机械工业自动化研究所）：区别于通用人形追求动作展示路线，依托系统集成优势与真实工业场景深度融合，针对食品行业复杂环境研发轮臂人形机器人，"
                    "集视觉感知/灵活操作/自主导航/人机协同于一体，适配肉类分割场景潮湿低温工况，弥补传统自动化设备柔性不足短板，近200人专职研发团队攻关具身智能/高精度运动控制/人机协同，"
                    "将中试验证/工程化适配前置到研发环节，系统性破解工程适配/成本控制/批量量产三大核心难题；"
                    "④中国电建5000台采购：6月雄安中国电建供应链合作大会上，成都人形机器人创新中心+中国电建成都院+某大型央企+智成睿锦共同签署5000台具身智能机器人产品战略采购订单，"
                    "核心产品为AI智能化长距离胶带机机器人监测运维整体解决方案，面向水利水电/交通工程/绿色矿山工程建设场景；"
                    "创新联合体模式：构建'央企出场景出需求+民企出技术出产品+科研院所出人才出算法'协同平台，共研解决'卡脖子'、场景共用解决'没处试'、成果共享解决'重复造轮子'三大痛点，"
                    "推动产业从单打独斗迈入国家统筹全链协同新阶段，央企发挥'压舱石'作用。",
        key_metrics={"initiative": "中央企业机器人创新联合体（WRC2026期间揭牌）", "policy": "工信部+国资委2026实景实训专项 年底万台级规模作业模式",
                     "core_model": "共研共用共享 央企出场景+民企出技术+科研出人才",
                     "pain_points_solved": ["卡脖子技术联合攻关", "没处试场景共用", "重复造轮子成果共享"],
                     "key_cases": [{"company": "国家电网", "product": "电力专用六足仿生巡检机器人", "capabilities": "狭矮空间100%通过/局放/SF6泄漏/漏液识别/5G量子加密/光明大模型分析"},
                                   {"application": "核电施工", "tech": "履带脚+麒麟臂", "effect": "钢筋绑扎效率+4倍/预埋件+8倍/合格率99.8% 工人转型技术管理"},
                                   {"company": "北自所", "rd_team": "近200人专职研发", "product": "食品行业轮臂人形机器人", "target": "肉类分割潮湿低温工况 前置中试/工程化 解决工程适配/成本/量产三难题"},
                                   {"order": "中国电建5000台战略采购", "partner": "成都人形创新中心+智成睿锦", "product": "AI长距离胶带机监测运维方案 水利水电/交通/绿色矿山"}],
                     "industry_context": "国家电网数百万公里输电线路/中石油数万公里油气管道/中车庞大轨道交通装备 真实场景需求迫切",
                     "future_directions": ["从炫技到实战深度赋能产业一线", "央企压舱石推动全链协同", "服务国家重大工程 成为高端制造出口新名片"]},
        maturity=MaturityLevel.FIELD_TRIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-14",
        relevance_to_robotics="央企创新联合体的成立标志着中国具身智能产业从民企单打独斗进入国家统筹阶段——国网/核电/电建等真实高危场景提供海量稀缺真机数据，"
                              "解决了仿真数据与现实工况脱节、核心零部件高投入长周期两大瓶颈，'训练-迭代-应用-再优化'产业闭环加速形成，万台级规模落地进入实质推进阶段",
        deployment_ready=True,
        tags=["央企机器人创新联合体", "WRC2026揭牌", "共研共用共享", "国网六足巡检机器人", "核电麒麟臂绑扎效率+4倍", "北自所食品轮臂人形", "中国电建5000台采购", "万台级实景实训", "卡脖子/没处试/重复造轮子", "产业闭环"]
    ),

    AIProduct(
        product_id="POL-001", name="安徽新一代信息技术产业破万亿 布局半导体+6G双赛道 显示驱动全球#1/硅基OLED#2/AMOLED#3/DRAM#4 池州130+半导体企业300亿产值",
        category=AICategory.AI_CHIP,
        organization="安徽省政府", country="中国",
        description="8月6日安徽省新一代信息技术暨新一代半导体、第六代移动通信产业推进会召开。"
                    "新一代信息技术是安徽省'十四五''十五五'持续推进的十大新兴产业之一，新一代半导体和6G是重点赛道也是'十五五'重点布局未来产业，定位为'物理基石（半导体）+神经网络（6G）'底层动能。"
                    "产业规模：2025年营收首次突破万亿元同比增长14%；2026年上半年营收6176.7亿元同比增长35%，利润707.6亿元同比暴增674.1%；上市公司达到44家（国仪量子/视涯科技/晶合集成/芯碁微装等）。"
                    "全球地位：显示驱动芯片代工市占率全球第1、消费类硅基OLED市占率第2、AMOLED智能手机面板出货量第3、DRAM芯片产能全球第4。"
                    "半导体方向：摩尔定律逼近物理极限，华为发布'韬定律'以时间缩微替代几何缩微，安徽将在加速建设存储高地同时，在封装测试/异构集成/芯粒/存算一体环节加快布局加大投入，推动从'单点突破'向'系统集成'升级。"
                    "6G方向：依托中国科大/中科院/中电科等高能级创新平台，新型频谱使用/网络测试/光电一体化已形成一批技术突破，提出'3+3'发展重点——"
                    "聚焦光通信/地面移动通信/测试与安全三大优势赛道，发力卫星通信/新型智能终端/量子融合三大未来细分领域；短板：关键环节缺少龙头牵引、生态引领力不强、产业规模不大、集聚效应未形成。"
                    "融合方向：推动新一代半导体和6G与智能网联新能源汽车/量子科技/具身智能等产业深度融合，安徽将瞄准量子科技/具身智能/脑机接口领域动态发布融合应用需求清单，前瞻布局技术产品研发。"
                    "区域案例：池州经开区集聚上下游企业130余家产值突破300亿元；阜阳安徽觅拓材料突破光刻胶核心原料光敏剂实现高端电子原材料自主可控；蚌埠中电科思仪抢抓6G机遇打造通信测试一流企业。",
        key_metrics={"region": "安徽省", "policy_meeting": "新一代信息技术暨半导体+6G推进会 2026-08-06",
                     "industry_scale": {"2025_revenue": "首次突破万亿元 +14%", "2026h1_revenue": "6176.7亿元 +35%", "2026h1_profit": "707.6亿元 +674.1%", "listed_companies": 44},
                     "global_rankings": {"display_driver_foundry": "#1", "consumer_silicon_based_oled": "#2", "amoled_smartphone_panel": "#3", "dram_capacity": "#4"},
                     "semiconductor_strategy": "存储高地+封装测试/异构集成/芯粒/存算一体 单点突破→系统集成 响应华为韬定律时间缩微",
                     "6g_strategy": {"3_core_advantages": ["光通信", "地面移动通信", "测试与安全"],
                                    "3_future_growth": ["卫星通信", "新型智能终端", "量子融合"],
                                    "shortcomings": ["缺龙头牵引", "生态引领弱", "规模不大", "集聚未形成"]},
                     "cross_fusion": ["智能网联新能源汽车", "量子科技", "具身智能", "脑机接口"],
                     "regional_cases": {"chizhou": "半导体集群130+企业300亿产值",
                                        "fuyang_mituo": "光刻胶光敏剂突破 高端电子原材料自主可控",
                                        "bengbu_siyi": "中电科思仪 6G通信测试一流企业"},
                     "future_directions": ["平台型企业生态化招商", "梯次培育优质企业矩阵", "中试验证集成孵化平台", "车芯联动6G车路云协同"]},
        maturity=MaturityLevel.COMMERCIAL,
        source="", source_tier=SourceTier.TIER1,
        publish_date="2026-08-13",
        relevance_to_robotics="安徽将具身智能列为半导体/6G重点融合方向，44家上市公司+完整半导体产业链+全球前四显示/存储产能为机器人算力芯片、传感器、显示交互模组提供本土供应链支撑，"
                              "池州/蚌埠等产业集群300亿产值规模有助于核心零部件成本压降，车芯联动经验可迁移至机器人产业生态建设",
        deployment_ready=True,
        tags=["安徽万亿信息产业", "半导体6G双赛道", "显示驱动全球#1", "硅基OLED#2", "DRAM#4", "2026H1利润+674%", "池州半导体130+企业300亿", "觅拓光刻胶光敏剂", "中电科思仪6G测试", "具身智能融合"]
    ),

]

