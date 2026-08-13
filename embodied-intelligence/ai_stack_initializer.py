#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI智能栈统一初始化 - V1.1
================================================================
将17个独立功能模块注册到VLA工厂、世界模型工厂，
并初始化算力调度、工厂部署、6G网络、蚌埠供应链，
以及11大行业AI模块（新能源/农业/商业/水利/汽车/数码/医疗/民生/教育/家电/医疗设备）。

新增内容：
  1. register_all_vla_backends() - 注册DeepSeek-V4/Nemotron专用后端
  2. register_all_world_engines() - 注册Cosmos3专用引擎
  3. init_compute_scheduler() - 初始化算力调度器
  4. init_factory_deployment() - 初始化工厂部署
  5. init_sixg_network() - 初始化6G网络
  6. init_bengbu_supply_chain() - 初始化蚌埠供应链
  7. init_renewable_energy() - 初始化新能源AI
  8. init_agriculture() - 初始化农业AI
  9. init_commerce() - 初始化商业AI
  10. init_water_conservancy() - 初始化水利AI
  11. init_automotive() - 初始化汽车AI
  12. init_digital_product() - 初始化数码产品AI
  13. init_healthcare() - 初始化医疗健康AI
  14. init_livelihood() - 初始化民生AI
  15. init_education() - 初始化教育AI
  16. init_home_appliance() - 初始化家用电器AI
  17. init_medical_device() - 初始化医疗设备AI
  18. init_mobile_computer() - 初始化手机和电脑AI
  19. initialize_all() - 一键初始化全部AI智能栈
"""

import os
import sys
from typing import Dict, Any, Optional

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if _BASE_DIR not in sys.path:
    sys.path.insert(0, _BASE_DIR)


def register_all_vla_backends() -> Dict[str, bool]:
    """注册所有独立VLA后端到工厂。"""
    results = {}
    try:
        from vla_model_backends import VLABackendFactory
        from deepseek_v4_backend import DeepSeekV4Backend
        VLABackendFactory.register_external_backend("deepseek_v4", DeepSeekV4Backend)
        results["deepseek_v4"] = True
    except Exception as e:
        results["deepseek_v4"] = False
        results["deepseek_v4_error"] = str(e)[:100]

    try:
        from vla_model_backends import VLABackendFactory
        from nemotron_nvidia_backend import NemotronLightningBackend
        VLABackendFactory.register_external_backend("nemotron_35", NemotronLightningBackend)
        results["nemotron_35"] = True
    except Exception as e:
        results["nemotron_35"] = False
        results["nemotron_35_error"] = str(e)[:100]

    return results


def register_all_world_engines() -> Dict[str, bool]:
    """注册所有独立世界模型引擎到工厂。"""
    results = {}
    try:
        from world_model_engines import WorldModelFactory
        from cosmos3_engine import Cosmos3Engine
        WorldModelFactory.register_external_engine("cosmos3", Cosmos3Engine)
        results["cosmos3"] = True
    except Exception as e:
        results["cosmos3"] = False
        results["cosmos3_error"] = str(e)[:100]

    return results


def init_compute_scheduler():
    """初始化算力调度器。"""
    from ai_compute_scheduler import create_compute_scheduler
    return create_compute_scheduler()


def init_factory_deployment():
    """初始化人形机器人工厂部署。"""
    from humanoid_factory_deployment import create_factory_deployment
    return create_factory_deployment()


def init_sixg_network():
    """初始化6G网络适配器。"""
    from sixg_network_adapter import create_sixg_adapter
    adapter = create_sixg_adapter()
    adapter.connect()
    return adapter


def init_bengbu_supply_chain():
    """初始化蚌埠传感器供应链。"""
    from bengbu_sensor_supply_chain import create_bengbu_supply_chain
    return create_bengbu_supply_chain()


def init_renewable_energy():
    """初始化新能源AI调度器。"""
    from renewable_energy_ai import create_energy_ai_scheduler
    return create_energy_ai_scheduler()


def init_agriculture():
    """初始化农业AI平台。"""
    from agriculture_ai import create_agriculture_ai
    return create_agriculture_ai()


def init_commerce():
    """初始化商业AI平台。"""
    from commerce_ai import create_commerce_ai
    return create_commerce_ai()


def init_water_conservancy():
    """初始化水利AI平台。"""
    from water_conservancy_ai import create_water_conservancy_ai
    return create_water_conservancy_ai()


def init_automotive():
    """初始化汽车AI平台。"""
    from automotive_ai import create_automotive_ai
    return create_automotive_ai()


def init_digital_product():
    """初始化数码产品AI平台。"""
    from digital_product_ai import create_digital_device_ai
    return create_digital_device_ai()


def init_healthcare():
    """初始化医疗健康AI平台。"""
    from healthcare_ai import create_healthcare_ai
    return create_healthcare_ai()


def init_livelihood():
    """初始化民生AI平台。"""
    from livelihood_ai import create_livelihood_ai
    return create_livelihood_ai()


def init_education():
    """初始化教育AI平台。"""
    from education_ai import create_education_ai
    return create_education_ai()


def init_home_appliance():
    """初始化家用电器AI平台。"""
    from home_appliance_ai import create_home_appliance_ai
    return create_home_appliance_ai()


def init_medical_device():
    """初始化医疗设备AI平台。"""
    from medical_device_ai import create_medical_device_ai
    return create_medical_device_ai()


def init_mobile_computer():
    """初始化手机和电脑AI平台。"""
    from mobile_computer_ai import create_mobile_computer_ai
    return create_mobile_computer_ai()


_INDUSTRY_INIT_FUNCS = {
    "renewable_energy": init_renewable_energy,
    "agriculture": init_agriculture,
    "commerce": init_commerce,
    "water_conservancy": init_water_conservancy,
    "automotive": init_automotive,
    "digital_product": init_digital_product,
    "healthcare": init_healthcare,
    "livelihood": init_livelihood,
    "education": init_education,
    "home_appliance": init_home_appliance,
    "medical_device": init_medical_device,
    "mobile_computer": init_mobile_computer,
}


def initialize_all(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """一键初始化全部AI智能栈。

    Returns:
        包含各模块初始化状态和实例的字典。
    """
    config = config or {}
    result = {
        "vla_backends": register_all_vla_backends(),
        "world_engines": register_all_world_engines(),
        "compute_scheduler": None,
        "factory_deployment": None,
        "sixg_network": None,
        "bengbu_supply_chain": None,
        "world_proxy": None,
        "industry_modules": {},
        "errors": [],
    }

    try:
        result["compute_scheduler"] = init_compute_scheduler()
    except Exception as e:
        result["errors"].append(f"compute_scheduler: {e}")

    try:
        result["factory_deployment"] = init_factory_deployment()
    except Exception as e:
        result["errors"].append(f"factory_deployment: {e}")

    try:
        result["sixg_network"] = init_sixg_network()
    except Exception as e:
        result["errors"].append(f"sixg_network: {e}")

    try:
        result["bengbu_supply_chain"] = init_bengbu_supply_chain()
    except Exception as e:
        result["errors"].append(f"bengbu_supply_chain: {e}")

    try:
        from world_proxy_agent import create_world_proxy
        result["world_proxy"] = create_world_proxy()
    except Exception as e:
        result["errors"].append(f"world_proxy: {e}")

    for name, init_fn in _INDUSTRY_INIT_FUNCS.items():
        try:
            result["industry_modules"][name] = init_fn()
        except Exception as e:
            result["industry_modules"][name] = None
            result["errors"].append(f"{name}: {e}")

    result["success"] = len(result["errors"]) == 0
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("AI智能栈统一初始化")
    print("=" * 60)
    r = initialize_all()
    print(f"\nVLA后端注册: {r['vla_backends']}")
    print(f"世界模型注册: {r['world_engines']}")
    print(f"算力调度: {'OK' if r['compute_scheduler'] else 'FAIL'}")
    print(f"工厂部署: {'OK' if r['factory_deployment'] else 'FAIL'}")
    print(f"6G网络: {'OK' if r['sixg_network'] else 'FAIL'}")
    print(f"蚌埠供应链: {'OK' if r['bengbu_supply_chain'] else 'FAIL'}")
    print(f"世界代理: {'OK' if r['world_proxy'] else 'FAIL'}")
    print(f"\n11大行业模块:")
    for name, inst in r["industry_modules"].items():
        print(f"  {name}: {'OK' if inst else 'FAIL'}")
    if r["errors"]:
        print(f"\n错误: {r['errors']}")
    else:
        print("\n全部模块初始化成功")
