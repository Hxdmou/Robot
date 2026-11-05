#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
蚌埠传感器供应链对接模块 - V1.0
================================================================
新增内容：
  1. SensorType（传感器类型枚举）
  2. SensorProduct（传感器产品数据类）
  3. SupplierProfile（供应商档案）
  4. SupplyChainInventory（供应链库存）
  5. ProcurementOrder（采购订单）
  6. BengbuSensorSupplyChain（蚌埠传感器供应链管理器）
  7. create_bengbu_supply_chain（工厂函数）

核心能力：
  - 蚌埠中国传感谷200+企业资源对接
  - MEMS/气体/柔性脑机电极/磁电流/AI嗅觉全品类
  - 本地化供应链匹配与采购
  - 库存管理与交付周期追踪
  - 机器人"电子五官"传感器选型推荐
"""

import time
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from network_industry_adapter import (
    BengbuCompany, BengbuIndustryCategory, BENGBU_COMPANIES,
)


class SensorType(Enum):
    """传感器类型（机器人电子五官）。"""
    VISION = "vision"                # 视觉
    FORCE_TORQUE = "force_torque"    # 力/力矩
    IMU = "imu"                      # 惯性测量
    TACTILE = "tactile"             # 触觉
    GAS = "gas"                     # 气体
    TEMPERATURE = "temperature"     # 温度
    PRESSURE = "pressure"           # 压力
    MAGNETIC = "magnetic"           # 磁/电流
    PROXIMITY = "proximity"         # 接近
    OLFACTION = "olfaction"         # 嗅觉（AI电子鼻）
    BRAIN_COMPUTER = "brain_eeg"    # 脑电/脑机
    FLEXIBLE = "flexible"           # 柔性


@dataclass
class SensorProduct:
    """传感器产品。"""
    product_id: str
    name: str
    sensor_type: SensorType
    supplier_name: str
    specifications: Dict[str, Any] = field(default_factory=dict)
    unit_price_cny: float = 0.0
    lead_time_days: int = 7
    in_stock: bool = True
    stock_quantity: int = 0
    robot_part: str = ""            # 对应机器人部位
    domestic: bool = True


@dataclass
class SupplierProfile:
    """供应商档案。"""
    company_name: str
    category: BengbuIndustryCategory
    products: List[str]
    capability: str
    address: str
    robot_relevance: str
    scale: str = ""
    contact_ready: bool = False
    rating: float = 5.0
    verified: bool = True


@dataclass
class ProcurementOrder:
    """采购订单。"""
    order_id: str
    product_id: str
    quantity: int
    supplier_name: str
    unit_price_cny: float
    total_cny: float = 0.0
    status: str = "pending"
    created_at: float = field(default_factory=time.time)
    estimated_delivery_days: int = 7


class BengbuSensorSupplyChain:
    """蚌埠传感器供应链管理器。

    对接中国传感谷本地企业资源，为机器人提供
    全品类传感器的选型、采购、库存管理。
    """

    def __init__(self):
        self.suppliers: Dict[str, SupplierProfile] = {}
        self.products: Dict[str, SensorProduct] = {}
        self.orders: List[ProcurementOrder] = []
        self._order_counter = 0
        self._init_local_suppliers()
        self._init_sensor_catalog()

    def _init_local_suppliers(self) -> None:
        for company in BENGBU_COMPANIES:
            self.suppliers[company.name] = SupplierProfile(
                company_name=company.name,
                category=company.category,
                products=list(company.products),
                capability=company.capability,
                address=company.address,
                robot_relevance=company.robot_relevance,
                scale=company.scale,
                contact_ready=company.contact_ready,
            )

    def _init_sensor_catalog(self) -> None:
        catalog = [
            SensorProduct(
                product_id="BB-IMU-001", name="MEMS惯性测量单元",
                sensor_type=SensorType.IMU,
                supplier_name="安徽华鑫微纳集成电路有限公司",
                specifications={"axes": 6, "range_g": 16, "bandwidth_hz": 200},
                unit_price_cny=280.0, lead_time_days=5,
                stock_quantity=500, robot_part="躯干/关节",
            ),
            SensorProduct(
                product_id="BB-PRES-001", name="MEMS压力传感器",
                sensor_type=SensorType.PRESSURE,
                supplier_name="安徽华鑫微纳集成电路有限公司",
                specifications={"range_kpa": 1000, "accuracy_pct": 0.5},
                unit_price_cny=120.0, lead_time_days=5,
                stock_quantity=1000, robot_part="夹爪/手腕",
            ),
            SensorProduct(
                product_id="BB-GAS-001", name="硫化氢气体检测传感器",
                sensor_type=SensorType.GAS,
                supplier_name="安徽北方华鑫智感科技有限公司",
                specifications={"gas": "H2S", "range_ppm": 100, "response_s": 30},
                unit_price_cny=350.0, lead_time_days=7,
                stock_quantity=200, robot_part="环境感知模块",
            ),
            SensorProduct(
                product_id="BB-OLF-001", name="AI嗅觉电子鼻",
                sensor_type=SensorType.OLFACTION,
                supplier_name="中国传感谷",
                specifications={"channels": 16, "detection_gases": 8},
                unit_price_cny=2800.0, lead_time_days=14,
                stock_quantity=50, robot_part="头部感知",
            ),
            SensorProduct(
                product_id="BB-FLEX-001", name="柔性脑机电极",
                sensor_type=SensorType.BRAIN_COMPUTER,
                supplier_name="中国传感谷",
                specifications={"channels": 64, "material": "柔性聚合物"},
                unit_price_cny=5000.0, lead_time_days=21,
                stock_quantity=20, robot_part="脑机接口",
            ),
            SensorProduct(
                product_id="BB-MAG-001", name="磁电流传感器",
                sensor_type=SensorType.MAGNETIC,
                supplier_name="中国传感谷",
                specifications={"range_a": 50, "accuracy_pct": 1.0},
                unit_price_cny=180.0, lead_time_days=7,
                stock_quantity=300, robot_part="关节电机",
            ),
        ]
        for p in catalog:
            self.products[p.product_id] = p

    def find_sensors_by_type(self, sensor_type: SensorType) -> List[SensorProduct]:
        return [p for p in self.products.values() if p.sensor_type == sensor_type]

    def find_sensors_for_robot_part(self, part: str) -> List[SensorProduct]:
        return [p for p in self.products.values() if part in p.robot_part]

    def recommend_sensor_suite(self, robot_type: str = "humanoid") -> Dict[str, List[SensorProduct]]:
        """为机器人推荐全套传感器方案（电子五官）。"""
        suite = {
            "视觉系统": self.find_sensors_by_type(SensorType.VISION),
            "力觉系统": self.find_sensors_by_type(SensorType.FORCE_TORQUE),
            "惯性导航": self.find_sensors_by_type(SensorType.IMU),
            "触觉系统": self.find_sensors_by_type(SensorType.TACTILE),
            "环境感知": (self.find_sensors_by_type(SensorType.GAS) +
                         self.find_sensors_by_type(SensorType.OLFACTION)),
            "内部监测": (self.find_sensors_by_type(SensorType.TEMPERATURE) +
                         self.find_sensors_by_type(SensorType.PRESSURE) +
                         self.find_sensors_by_type(SensorType.MAGNETIC)),
        }
        return suite

    def place_order(self, product_id: str, quantity: int) -> Optional[ProcurementOrder]:
        product = self.products.get(product_id)
        if not product or not product.in_stock:
            return None
        if quantity > product.stock_quantity:
            return None
        self._order_counter += 1
        total = product.unit_price_cny * quantity
        order = ProcurementOrder(
            order_id=f"PO-BB-{self._order_counter:06d}",
            product_id=product_id,
            quantity=quantity,
            supplier_name=product.supplier_name,
            unit_price_cny=product.unit_price_cny,
            total_cny=total,
            estimated_delivery_days=product.lead_time_days,
        )
        order.status = "confirmed"
        product.stock_quantity -= quantity
        self.orders.append(order)
        return order

    def get_supplier(self, name: str) -> Optional[SupplierProfile]:
        return self.suppliers.get(name)

    def list_suppliers(self, category: Optional[BengbuIndustryCategory] = None) -> List[SupplierProfile]:
        if category:
            return [s for s in self.suppliers.values() if s.category == category]
        return list(self.suppliers.values())

    def get_supply_chain_status(self) -> Dict[str, Any]:
        total_stock = sum(p.stock_quantity for p in self.products.values())
        return {
            "valley_name": "中国传感谷",
            "total_suppliers": len(self.suppliers),
            "contact_ready_suppliers": sum(1 for s in self.suppliers.values() if s.contact_ready),
            "total_product_types": len(self.products),
            "total_stock_units": total_stock,
            "total_orders": len(self.orders),
            "confirmed_orders": sum(1 for o in self.orders if o.status == "confirmed"),
            "output_2025_yi": 100,
            "growth_pct": 29,
            "national_rank": 6,
            "enterprises": 200,
        }


def create_bengbu_supply_chain() -> BengbuSensorSupplyChain:
    """工厂函数：创建蚌埠传感器供应链管理器。"""
    return BengbuSensorSupplyChain()


if __name__ == "__main__":
    chain = create_bengbu_supply_chain()
    status = chain.get_supply_chain_status()
    print(f"蚌埠传感器供应链已创建: {status['total_suppliers']}家供应商, "
          f"{status['total_product_types']}类传感器")
    suite = chain.recommend_sensor_suite()
    print(f"机器人传感器方案: {list(suite.keys())}")
