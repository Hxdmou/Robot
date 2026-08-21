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


AI_LANDSCAPE_DB_PART3: List[AIProduct] = [

]
