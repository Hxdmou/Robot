#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
网络与产业适配层 - V1.0
================================================================
新增内容：
  1. NetworkGeneration（网络制式枚举）
  2. NetworkStatus（网络状态枚举）
  3. NetworkProfile（网络配置数据类）
  4. NetworkHealth（网络健康数据类）
  5. NETWORK_PROFILES（网络制式档案表）
  6. NetworkAdapter（网络适配器类）
  7. IndustrialRobotBrand（工业机器人品牌枚举）
  8. IndustrialRobotProfile（机器人品牌数据类）
  9. INDUSTRIAL_ROBOT_PROFILES（品牌档案表）
  10. IndustrialRobotAdapter（工业机器人适配器类）
  11. BengbuIndustryCategory（蚌埠产业类别枚举）
  12. BengbuCompany（蚌埠企业数据类）
  13. BENGBU_COMPANIES（企业列表）
  14. BengbuIndustryAdapter（蚌埠产业适配器类）
  15. NetworkIndustryAdapter（统一适配层类）

网络制式名称列表：
  ETHERNET / WIFI_6 / WIFI_7 / FIVEG / FIVEG_A / SIXG / LOCAL_ONLY

工业机器人品牌名称列表：
  ESTUN / INOVANCE / HIKROBOT / SIASUN / AUBO / DOOSAN /
  FANUC / ABB / KUKA / YASKAWA / UNIVERSAL / GUOAO / XUNJI

蚌埠产业类别名称列表：
  SENSOR / MEMS_FOUNDRY / BRAIN_COMPUTER / AI_COMPUTING /
  SMART_COMMUNITY / INDUSTRIAL_AI / ROBOTICS
"""

import time
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# 第一部分：6G/5G-A 网络适配
# ============================================================================

class NetworkGeneration(Enum):
    ETHERNET = "ethernet"
    WIFI_6 = "wifi_6"
    WIFI_7 = "wifi_7"
    FIVEG = "5g"
    FIVEG_A = "5g_a"
    SIXG = "6g"
    LOCAL_ONLY = "local_only"


class NetworkStatus(Enum):
    CONNECTED = "connected"
    DEGRADED = "degraded"
    DISCONNECTED = "disconnected"
    SWITCHING = "switching"


@dataclass
class NetworkProfile:
    generation: NetworkGeneration
    name: str
    typical_latency_ms: float
    min_latency_ms: float
    typical_bandwidth_mbps: float
    reliability_pct: float
    supports_urllc: bool = False
    supports_massive_iot: bool = False
    supports_sensing: bool = False
    supports_ai_native: bool = False
    available: bool = True
    notes: str = ""


@dataclass
class NetworkHealth:
    status: NetworkStatus = NetworkStatus.DISCONNECTED
    current_latency_ms: float = 999.0
    current_bandwidth_mbps: float = 0.0
    packet_loss_pct: float = 100.0
    jitter_ms: float = 999.0
    connected_since: float = 0.0
    active_profile: str = ""


NETWORK_PROFILES: Dict[str, NetworkProfile] = {
    "ethernet": NetworkProfile(
        generation=NetworkGeneration.ETHERNET, name="ethernet",
        typical_latency_ms=1.0, min_latency_ms=0.1,
        typical_bandwidth_mbps=1000.0, reliability_pct=99.999,
        supports_urllc=True, available=True,
    ),
    "wifi_6": NetworkProfile(
        generation=NetworkGeneration.WIFI_6, name="wifi_6",
        typical_latency_ms=10.0, min_latency_ms=2.0,
        typical_bandwidth_mbps=300.0, reliability_pct=99.5,
        available=True,
    ),
    "wifi_7": NetworkProfile(
        generation=NetworkGeneration.WIFI_7, name="wifi_7",
        typical_latency_ms=5.0, min_latency_ms=1.0,
        typical_bandwidth_mbps=1000.0, reliability_pct=99.7,
        supports_urllc=True, available=True,
    ),
    "5g": NetworkProfile(
        generation=NetworkGeneration.FIVEG, name="5g",
        typical_latency_ms=20.0, min_latency_ms=5.0,
        typical_bandwidth_mbps=500.0, reliability_pct=99.9,
        supports_urllc=True, supports_massive_iot=True, available=True,
    ),
    "5g_a": NetworkProfile(
        generation=NetworkGeneration.FIVEG_A, name="5g_a",
        typical_latency_ms=10.0, min_latency_ms=1.0,
        typical_bandwidth_mbps=1000.0, reliability_pct=99.99,
        supports_urllc=True, supports_massive_iot=True,
        supports_sensing=True, supports_ai_native=True, available=True,
    ),
    "6g": NetworkProfile(
        generation=NetworkGeneration.SIXG, name="6g",
        typical_latency_ms=1.0, min_latency_ms=0.001,
        typical_bandwidth_mbps=10000.0, reliability_pct=99.999,
        supports_urllc=True, supports_massive_iot=True,
        supports_sensing=True, supports_ai_native=True,
        available=False,
    ),
    "local_only": NetworkProfile(
        generation=NetworkGeneration.LOCAL_ONLY, name="local_only",
        typical_latency_ms=0.0, min_latency_ms=0.0,
        typical_bandwidth_mbps=0.0, reliability_pct=100.0,
        available=True,
    ),
}


class NetworkAdapter:
    FALLBACK_ORDER = ["ethernet", "wifi_7", "wifi_6", "5g_a", "5g", "local_only"]

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.preferred = self.config.get("preferred_network", "ethernet")
        self.health = NetworkHealth()
        self._active = "local_only"
        self._on_switch_callbacks = []

    def initialize(self) -> bool:
        try:
            self._active = self._select_best_available()
            self.health.status = NetworkStatus.CONNECTED
            self.health.active_profile = self._active
            self.health.connected_since = time.time()
            profile = NETWORK_PROFILES.get(self._active)
            if profile:
                self.health.current_latency_ms = profile.typical_latency_ms
                self.health.current_bandwidth_mbps = profile.typical_bandwidth_mbps
                self.health.packet_loss_pct = 0.0
            return True
        except Exception:
            self._active = "local_only"
            self.health.status = NetworkStatus.DISCONNECTED
            return True

    def _select_best_available(self) -> str:
        preferred = self.preferred
        if preferred in NETWORK_PROFILES and NETWORK_PROFILES[preferred].available:
            return preferred
        for net in self.FALLBACK_ORDER:
            if net in NETWORK_PROFILES and NETWORK_PROFILES[net].available:
                return net
        return "local_only"

    def check_health(self) -> NetworkHealth:
        try:
            profile = NETWORK_PROFILES.get(self._active)
            if profile is None:
                self.health.status = NetworkStatus.DISCONNECTED
                return self.health
            if self._active == "local_only":
                self.health.status = NetworkStatus.CONNECTED
                self.health.current_latency_ms = 0.0
            return self.health
        except Exception:
            self.health.status = NetworkStatus.DEGRADED
            return self.health

    def on_network_degraded(self) -> str:
        try:
            current_idx = (
                self.FALLBACK_ORDER.index(self._active)
                if self._active in self.FALLBACK_ORDER else 0
            )
            for net in self.FALLBACK_ORDER[current_idx + 1:]:
                profile = NETWORK_PROFILES.get(net)
                if profile and profile.available:
                    old = self._active
                    self._active = net
                    self.health.status = NetworkStatus.SWITCHING
                    self.health.active_profile = net
                    for cb in self._on_switch_callbacks:
                        try:
                            cb(old, net)
                        except Exception:
                            pass
                    self.health.status = NetworkStatus.CONNECTED
                    return net
            self._active = "local_only"
            return "local_only"
        except Exception:
            self._active = "local_only"
            return "local_only"

    def get_active_profile(self) -> NetworkProfile:
        return NETWORK_PROFILES.get(self._active, NETWORK_PROFILES["local_only"])

    def is_cloud_control_viable(self) -> bool:
        try:
            profile = self.get_active_profile()
            return (profile.typical_latency_ms < 50.0
                    and profile.reliability_pct >= 99.9
                    and self.health.status == NetworkStatus.CONNECTED)
        except Exception:
            return False

    def get_latency_budget_ms(self) -> float:
        try:
            return self.health.current_latency_ms * 1.5
        except Exception:
            return 100.0

    def register_switch_callback(self, callback) -> None:
        self._on_switch_callbacks.append(callback)

    def get_status(self) -> Dict[str, Any]:
        return {
            "active_network": self._active,
            "health": self.health.status.value,
            "latency_ms": self.health.current_latency_ms,
            "bandwidth_mbps": self.health.current_bandwidth_mbps,
            "cloud_viable": self.is_cloud_control_viable(),
        }


# ============================================================================
# 第二部分：工业机器人产业适配
# ============================================================================

class IndustrialRobotBrand(Enum):
    ESTUN = "estun"
    INOVANCE = "inovance"
    HIKROBOT = "hikrobot"
    SIASUN = "siasun"
    AUBO = "aubo"
    DOOSAN = "doosan"
    FANUC = "fanuc"
    ABB = "abb"
    KUKA = "kuka"
    YASKAWA = "yaskawa"
    UNIVERSAL = "universal"
    GUOAO = "guoao"
    XUNJI = "xunji"


@dataclass
class IndustrialRobotProfile:
    brand: IndustrialRobotBrand
    display_name: str
    country: str
    robot_types: List[str]
    controller_protocol: str
    payload_range_kg: Tuple[float, float]
    reach_range_mm: Tuple[float, float]
    repeatability_mm: float
    supports_ai_vision: bool = False
    supports_force_control: bool = False
    supports_collaborative: bool = False
    supports_mobile: bool = False
    sdk_available: bool = False
    local_support_china: bool = False
    notes: str = ""


INDUSTRIAL_ROBOT_PROFILES: Dict[str, IndustrialRobotProfile] = {
    "estun": IndustrialRobotProfile(
        brand=IndustrialRobotBrand.ESTUN, display_name="estun",
        country="CN", robot_types=["six_axis", "scara", "collaborative"],
        controller_protocol="native/modbus_tcp",
        payload_range_kg=(3, 700), reach_range_mm=(500, 3000),
        repeatability_mm=0.02, supports_ai_vision=True,
        supports_force_control=True, supports_collaborative=True,
        sdk_available=True, local_support_china=True,
    ),
    "fanuc": IndustrialRobotProfile(
        brand=IndustrialRobotBrand.FANUC, display_name="fanuc",
        country="JP", robot_types=["six_axis", "scara", "collaborative"],
        controller_protocol="native/tcp",
        payload_range_kg=(0.5, 2300), reach_range_mm=(300, 4000),
        repeatability_mm=0.01, supports_ai_vision=True,
        supports_force_control=True, supports_collaborative=True,
        sdk_available=True, local_support_china=True,
    ),
    "abb": IndustrialRobotProfile(
        brand=IndustrialRobotBrand.ABB, display_name="abb",
        country="CH", robot_types=["six_axis", "collaborative", "dual_arm"],
        controller_protocol="native/tcp",
        payload_range_kg=(0.5, 800), reach_range_mm=(300, 3500),
        repeatability_mm=0.01, supports_ai_vision=True,
        supports_force_control=True, supports_collaborative=True,
        sdk_available=True, local_support_china=True,
    ),
    "kuka": IndustrialRobotProfile(
        brand=IndustrialRobotBrand.KUKA, display_name="kuka",
        country="DE", robot_types=["six_axis", "collaborative", "mobile"],
        controller_protocol="native/tcp",
        payload_range_kg=(3, 1300), reach_range_mm=(500, 3500),
        repeatability_mm=0.02, supports_ai_vision=True,
        supports_force_control=True, supports_collaborative=True,
        supports_mobile=True, sdk_available=True, local_support_china=True,
    ),
    "universal": IndustrialRobotProfile(
        brand=IndustrialRobotBrand.UNIVERSAL, display_name="universal",
        country="DK", robot_types=["collaborative"],
        controller_protocol="rtde/tcp",
        payload_range_kg=(3, 30), reach_range_mm=(500, 1800),
        repeatability_mm=0.03, supports_force_control=True,
        supports_collaborative=True, sdk_available=True,
        local_support_china=True,
    ),
}


class IndustrialRobotAdapter:
    def __init__(self):
        self._profiles = INDUSTRIAL_ROBOT_PROFILES

    def get_supported_brands(self, china_only: bool = False) -> List[IndustrialRobotProfile]:
        try:
            results = list(self._profiles.values())
            if china_only:
                results = [r for r in results if r.country == "CN"]
            return results
        except Exception:
            return []

    def get_brand(self, brand_id: str) -> Optional[IndustrialRobotProfile]:
        return self._profiles.get(brand_id)

    def get_protocol(self, brand_id: str) -> str:
        try:
            profile = self._profiles.get(brand_id)
            return profile.controller_protocol if profile else "unknown"
        except Exception:
            return "unknown"

    def find_compatible(self, payload_kg: float, reach_mm: float,
                        collaborative: bool = False,
                        china_preferred: bool = False) -> List[IndustrialRobotProfile]:
        try:
            results = []
            for p in self._profiles.values():
                if not (p.payload_range_kg[0] <= payload_kg <= p.payload_range_kg[1]):
                    continue
                if p.reach_range_mm[1] > 0 and not (
                    p.reach_range_mm[0] <= reach_mm <= p.reach_range_mm[1]
                ):
                    continue
                if collaborative and not p.supports_collaborative:
                    continue
                results.append(p)
            if china_preferred:
                results.sort(key=lambda x: (x.country != "CN", x.repeatability_mm))
            return results
        except Exception:
            return []

    def get_supply_chain_summary(self) -> Dict[str, Any]:
        try:
            china = [p for p in self._profiles.values() if p.country == "CN"]
            foreign = [p for p in self._profiles.values() if p.country != "CN"]
            return {
                "total_brands": len(self._profiles),
                "china_brands": len(china),
                "foreign_brands": len(foreign),
                "all_sdk_available": all(
                    p.sdk_available for p in self._profiles.values()
                ),
            }
        except Exception:
            return {"total_brands": 0}


# ============================================================================
# 第三部分：蚌埠本地产业适配
# ============================================================================

class BengbuIndustryCategory(Enum):
    SENSOR = "sensor"
    MEMS_FOUNDRY = "mems_foundry"
    BRAIN_COMPUTER = "brain_computer"
    AI_COMPUTING = "ai_computing"
    SMART_COMMUNITY = "smart_community"
    INDUSTRIAL_AI = "industrial_ai"
    ROBOTICS = "robotics"


@dataclass
class BengbuCompany:
    name: str
    category: BengbuIndustryCategory
    products: List[str]
    capability: str
    address: str
    robot_relevance: str
    contact_ready: bool = False
    scale: str = ""


BENGBU_COMPANIES: List[BengbuCompany] = [
    BengbuCompany(
        name="安徽华鑫微纳集成电路有限公司",
        category=BengbuIndustryCategory.MEMS_FOUNDRY,
        products=["8英寸MEMS晶圆", "温度传感器", "压力传感器", "惯性传感器"],
        capability="国内首条8英寸MEMS晶圆全自动生产线，满产月产3万片，产能国内第一梯队",
        address="蚌埠经开区中国传感谷",
        robot_relevance="MEMS晶圆制造温度/压力/惯性传感器，直接供应机器人关节与IMU",
        contact_ready=True,
        scale="月产3万片晶圆",
    ),
    BengbuCompany(
        name="安徽北方华鑫智感科技有限公司",
        category=BengbuIndustryCategory.SENSOR,
        products=["硫化氢气体检测传感器", "AI燃气安全阀", "燃气报警器"],
        capability="固态电池用硫化氢气体专用检测传感器，国内领先，已与多家电池企业达成合作意向",
        address="蚌埠经开区中国传感谷",
        robot_relevance="气体/安全传感器可用于机器人环境感知与安全监测",
        contact_ready=True,
        scale="原创性创新技术",
    ),
    BengbuCompany(
        name="安徽北方微电子研究院集团",
        category=BengbuIndustryCategory.BRAIN_COMPUTER,
        products=["柔性电极", "脑电采集芯片", "非侵入式凝胶电极"],
        capability="突破柔性电极、脑电采集芯片关键技术，凝胶电极接触阻抗达行业先进水平并批量销售，"
                   "自研脑电采集芯片可对标替代国外同类产品",
        address="蚌埠经开区",
        robot_relevance="脑机接口核心器件可用于假肢/外骨骼/康复机器人控制",
        contact_ready=True,
        scale="关键技术突破",
    ),
    BengbuCompany(
        name="蚌埠医科大学第一附属医院",
        category=BengbuIndustryCategory.BRAIN_COMPUTER,
        products=["无创脑机接口康复治疗", "半侵入式脑机植入手术"],
        capability="挂牌脑机接口与神经调控专用病房，完成国内首例磁共振引导无创脑机接口急性脑梗"
                   "康复治疗、全省首例半侵入式脑机植入偏瘫手术，累计无创脑机临床治疗70余例，"
                   "康复效率平均提升20%，开展50项临床试验",
        address="蚌埠市龙子湖区",
        robot_relevance="脑机接口临床落地为康复机器人提供神经控制接口验证",
        contact_ready=False,
        scale="70余例临床",
    ),
    BengbuCompany(
        name="蚌埠至博（光纤监测）",
        category=BengbuIndustryCategory.SENSOR,
        products=["光纤监测仪", "管网漏失监测"],
        capability="米小庭智慧社区部署光纤监测仪，精准捕捉地下供水管网漏失隐患",
        address="蚌埠经开区中国传感谷",
        robot_relevance="分布式光纤传感可用于机器人形变/接触感知",
        contact_ready=False,
        scale="社区级部署",
    ),
    BengbuCompany(
        name="中科微感",
        category=BengbuIndustryCategory.SENSOR,
        products=["环保卫士微型监测仪", "甲醛传感器", "TVOC传感器"],
        capability="实时监测甲醛和TVOC浓度，应用于智慧社区环境监测",
        address="蚌埠经开区中国传感谷",
        robot_relevance="环境气体传感器可集成于服务机器人环境感知模块",
        contact_ready=False,
        scale="社区级部署",
    ),
    BengbuCompany(
        name="芒果传感技术",
        category=BengbuIndustryCategory.SENSOR,
        products=["水质检测仪"],
        capability="米小庭智慧社区水质检测，把关饮水安全",
        address="蚌埠经开区中国传感谷",
        robot_relevance="水质传感可用于巡检/水下机器人",
        contact_ready=False,
        scale="社区级部署",
    ),
    BengbuCompany(
        name="龙湖实验室",
        category=BengbuIndustryCategory.BRAIN_COMPUTER,
        products=["脑机接口创新载体", "揭榜挂帅课题"],
        capability="高能级创新载体，落地段树民院士工作站，组建9支专业化科研团队，"
                   "设立15项揭榜挂帅课题，工信部脑机接口试验检测公共服务平台落户",
        address="蚌埠市",
        robot_relevance="脑机接口与神经工程研究支撑下一代人机交互机器人",
        contact_ready=False,
        scale="9支科研团队",
    ),
]


class BengbuIndustryAdapter:
    def __init__(self):
        self._companies = BENGBU_COMPANIES
        self._sensor_valley_stats = {
            "total_enterprises": 0,
            "specialized_new": 0,
            "pilot_lines": 0,
            "wafer_lines": [],
        }

    def get_all_companies(self) -> List[BengbuCompany]:
        return list(self._companies)

    def get_by_category(self, category: BengbuIndustryCategory) -> List[BengbuCompany]:
        try:
            return [c for c in self._companies if c.category == category]
        except Exception:
            return []

    def get_robotics_relevant(self) -> List[BengbuCompany]:
        try:
            return [c for c in self._companies if "robot" in c.robot_relevance.lower()]
        except Exception:
            return []

    def get_sensor_suppliers(self) -> List[BengbuCompany]:
        return self.get_by_category(BengbuIndustryCategory.SENSOR)

    def get_sensor_valley_summary(self) -> Dict[str, Any]:
        return dict(self._sensor_valley_stats)

    def find_sensor_for_robot(self, sensor_type: str = "") -> List[BengbuCompany]:
        try:
            results = []
            for c in self._companies:
                if c.category in (BengbuIndustryCategory.SENSOR,
                                   BengbuIndustryCategory.MEMS_FOUNDRY):
                    if not sensor_type or any(
                        sensor_type.lower() in p.lower() for p in c.products
                    ):
                        results.append(c)
            return results
        except Exception:
            return []

    def get_local_compute_options(self) -> List[BengbuCompany]:
        return self.get_by_category(BengbuIndustryCategory.AI_COMPUTING)

    def get_deployment_brief(self) -> Dict[str, Any]:
        try:
            return {
                "city": "bengbu",
                "sensor_valley": self._sensor_valley_stats,
                "robotics_companies": len(self.get_robotics_relevant()),
                "sensor_suppliers": len(self.get_sensor_suppliers()),
                "compute_providers": len(self.get_local_compute_options()),
                "total_companies_listed": len(self._companies),
                "local_supply_chain_ready": True,
            }
        except Exception:
            return {"city": "bengbu", "local_supply_chain_ready": False}


# ============================================================================
# 统一适配层
# ============================================================================

class NetworkIndustryAdapter:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.network = NetworkAdapter(self.config.get("network", {}))
        self.industrial = IndustrialRobotAdapter()
        self.bengbu = BengbuIndustryAdapter()

    def initialize(self) -> bool:
        try:
            self.network.initialize()
            return True
        except Exception:
            return False

    def get_full_status(self) -> Dict[str, Any]:
        try:
            return {
                "network": self.network.get_status(),
                "industrial_supply_chain": self.industrial.get_supply_chain_summary(),
                "bengbu": self.bengbu.get_deployment_brief(),
            }
        except Exception:
            return {"error": "status_failed"}

    def get_deployment_recommendations(self) -> Dict[str, Any]:
        try:
            cloud = self.network.is_cloud_control_viable()
            return {
                "control_mode": "cloud_edge_hybrid" if cloud else "edge_autonomous",
                "network_primary": self.network._active,
                "network_fallback": "local_only",
                "robot_brand_strategy": "multi_brand_supported",
                "sensor_supply": "local_sensor_valley",
                "compute_strategy": "cloud_plus_local" if cloud else "local_only",
                "local_partners": len(self.bengbu.get_robotics_relevant()),
            }
        except Exception:
            return {"control_mode": "edge_autonomous"}
