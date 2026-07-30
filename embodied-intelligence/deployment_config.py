"""
具身智能系统部署配置规范 (v8.0 工业化/商业化落地旗舰版 · 全栈感知增强)

本配置文件基于广泛的产业调研与技术标准分析，整合了当前具身智能领域
最前沿的工程实践指标体系。所有参数均以真实商用场景的最高要求为基准，
确保系统在生产环境中的可靠性、安全性与可扩展性。

核心设计原则：
  1. 最高标准原则 — 所有技术指标一律对齐工业化量产顶配标准
  2. 安全优先原则 — 功能安全、网络安全、物理安全三重保障体系
  3. 全栈覆盖原则 — 覆盖感知、决策、执行、通信、算力全链路
  4. 持续进化原则 — 内置数据飞轮与模型迭代机制
  5. 合规审计原则 — 满足国内外主流法规与标准体系要求

========================================================================
版本演进记录
========================================================================

v8.0  全栈感知增强版 (当前版本)
  · 摄像头设备全套模块配置（多摄系统/视觉感知/图像增强/深度感知）
  · 仿真引擎统一适配（PyBullet/Isaac Sim/Unity/Gazebo/MuJoCo）
  · ROS/ROS2中间件全栈支持（话题/服务/动作/MoveIt/Nav2）
  · 工业总线协议全套（CAN/CAN FD/EtherCAT/Modbus/TSN/OPC UA）
  · 多传感器融合模块（IMU/LiDAR/UWB/mmWave/多摄立体视觉）
  · 强化学习算法库（PPO/SAC/TD3/BC/Diffusion Policy）
  · 模型量化部署全栈（INT8/FP16/BF16/剪枝/蒸馏）
  · 密码学与安全体系（SHA/RSA/AES/TEE/数字签名/安全启动）
  · 入侵检测防护（IDS/IPS/异常检测/威胁情报）
  · 异构计算调度（TPU/NPU/ASIC/DSP/FPGA多核协同）
  · 可信执行环境（TEE/TrustZone/安全飞地）
  · 热管理与振动分析（热监控/振动诊断/预测性维护/故障诊断）
  · 无线充电与能源补充（Qi标准/感应式/谐振式）
  · 联邦学习与隐私计算（横向联邦/纵向联邦/差分隐私）
  · 模型预测控制（MPC/LQR/线性二次调节器）
  · RAG检索增强生成（向量库/知识库/重排序/上下文管理）
  · SLAM与定位建图（视觉SLAM/激光SLAM/ORB/LIO-SAM）
  · 分布式一致性协议（BASE/CAP/Paxos/Raft/2PC/3PC）
========================================================================
"""
# ============================================================================
# 免责声明与AI使用合规承诺
# ============================================================================
#
# 【版权声明】
#   本文件内容为技术研究成果，受著作权法保护。
#   未经授权不得复制、传播、修改或用于商业用途。
#
# 【AI使用规范承诺】
#   本文件设计严格遵循以下AI伦理与安全原则：
#
#   1. 合法合规原则：
#      - 所有功能设计符合《网络安全法》《数据安全法》《个人信息保护法》
#      - 符合国家人工智能相关标准规范（GB/T 41867-2022等）
#      - 支持算法备案与可解释性要求
#
#   2. 安全可控原则：
#      - 内置多层安全防护（功能安全ISO 13849、网络安全IEC 62443）
#      - 物理安全边界控制与紧急停止机制
#      - 所有自动化操作均可被人工干预和终止
#
#   3. 伦理道德原则：
#      - 不设计任何可能危害人类安全的自主功能
#      - 尊重人类自主权，关键决策保留人工最终决定权
#      - 避免任何形式的歧视性算法与不公平决策
#
#   4. 数据保护原则：
#      - 数据采集遵循最小必要原则
#      - 敏感数据须加密存储与传输
#      - 支持数据删除与可携带权
#
#   5. 可审计原则：
#      - 关键操作留痕与日志记录
#      - 支持第三方安全审计与评估
#      - 版本变更可追溯
#
# 【使用限制】
#   禁止将本文件用于以下场景：
#   - 违反国家法律法规的活动
#   - 危害国家安全与社会公共利益
#   - 侵犯他人知识产权、隐私权等合法权益
#   - 未经安全评估的关键基础设施控制
#   - 可能对人类造成物理伤害的自主武器系统
#
# 【风险免责】
#   本文件按"现状"提供，不作任何明示或默示保证。
#   在法律允许的最大范围内，作者不承担任何直接或间接责任。
#   使用者须自行：
#     - 评估本文件对特定场景的适用性
#     - 进行充分的安全测试与验证
#     - 获取必要的合规审批与授权
#     - 建立应急预案与风险应对机制
#
# 【纠纷处理】
#   如因使用本文件产生任何法律纠纷，双方应首先友好协商解决。
#   协商不成的，任何一方均可向有管辖权的人民法院提起诉讼。
#
# ============================================================================
# 使用者确认：我已阅读并同意以上全部条款，将严格遵守相关规定。
# ============================================================================



from typing import Dict, Any, Optional
import os


# ============================================================
# 部署等级定义
# ============================================================

DEPLOYMENT_LEVELS = {
    "TEST": "test",
    "PRE_PRODUCTION": "pre",
    "PRODUCTION": "prod",
}

DEFAULT_DEPLOYMENT_LEVEL = "TEST"


# ============================================================
# 本地硬件能力检测 (自动适配)
# ============================================================

def detect_local_hardware() -> Dict[str, Any]:
    info = {
        "cpu_cores": 4, "cpu_threads": 4,
        "gpu_available": False, "gpu_name": "None",
        "gpu_memory_gb": 0.0, "gpu_compute_capability": "0.0",
        "gpu_sm_supported": False, "ram_gb": 8.0,
        "recommendation": "minimal",
    }
    try:
        import multiprocessing
        info["cpu_threads"] = multiprocessing.cpu_count()
        info["cpu_cores"] = max(4, info["cpu_threads"] // 2)
    except Exception:
        pass
    try:
        import torch
        if torch.cuda.is_available():
            info["gpu_available"] = True
            info["gpu_name"] = torch.cuda.get_device_name(0)
            props = torch.cuda.get_device_properties(0)
            info["gpu_memory_gb"] = round(props.total_memory / 1024**3, 1)
            info["gpu_compute_capability"] = f"{props.major}.{props.minor}"
            try:
                t = torch.randn(8, 8, device='cuda', dtype=torch.float16)
                _ = t @ t
                info["gpu_sm_supported"] = True
            except Exception:
                info["gpu_sm_supported"] = False
    except Exception:
        pass
    try:
        import psutil
        info["ram_gb"] = round(psutil.virtual_memory().total / 1024**3, 1)
    except Exception:
        try:
            import ctypes
            k = ctypes.windll.kernel32
            class MEM(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong)]
            m = MEM(); m.dwLength = ctypes.sizeof(m)
            k.GlobalMemoryStatusEx(ctypes.byref(m))
            info["ram_gb"] = round(m.ullTotalPhys / 1024**3, 1)
        except Exception:
            pass
    score = 0
    if info["cpu_threads"] >= 16: score += 2
    elif info["cpu_threads"] >= 8: score += 1
    if info["gpu_available"] and info["gpu_memory_gb"] >= 12: score += 2
    elif info["gpu_available"] and info["gpu_memory_gb"] >= 6: score += 1
    if info["ram_gb"] >= 32: score += 2
    elif info["ram_gb"] >= 16: score += 1
    if score >= 5: info["recommendation"] = "high_end"
    elif score >= 3: info["recommendation"] = "mid_range"
    elif score >= 1: info["recommendation"] = "entry_level"
    else: info["recommendation"] = "minimal"
    return info

LOCAL_HARDWARE = detect_local_hardware()


def _get_adaptive_fps(base_fps: float) -> float:
    hw = LOCAL_HARDWARE
    if hw["recommendation"] == "high_end": return base_fps * 1.3
    elif hw["recommendation"] == "mid_range": return base_fps * 1.0
    elif hw["recommendation"] == "entry_level": return base_fps * 0.7
    else: return base_fps * 0.5


# ============================================================
# 12项多模态感知指标 (工程标准配置)
# ============================================================

PERCEPTION_METRICS_THRESHOLDS: Dict[str, Dict[str, Any]] = {
    "test": {
        "visual_localization_accuracy_mm": 10.0,
        "target_recognition_robustness": 0.70,
        "depth_perception_accuracy_mm": 20.0,
        "voice_false_trigger_rate_per_hour": 5.0,
        "multi_turn_dialog_accuracy": 0.60,
        "emotion_recognition_accuracy": 0.50,
        "force_control_response_latency_ms": 200.0,
        "contact_force_accuracy_n": 5.0,
        "compliant_control_stability": 0.70,
        "sensor_fusion_latency_ms": 300.0,
        "abnormal_response_time_s": 2.0,
        "autonomous_decision_confidence": 0.60,
    },
    "pre": {
        "visual_localization_accuracy_mm": 5.0,
        "target_recognition_robustness": 0.85,
        "depth_perception_accuracy_mm": 10.0,
        "voice_false_trigger_rate_per_hour": 2.0,
        "multi_turn_dialog_accuracy": 0.80,
        "emotion_recognition_accuracy": 0.70,
        "force_control_response_latency_ms": 100.0,
        "contact_force_accuracy_n": 3.0,
        "compliant_control_stability": 0.85,
        "sensor_fusion_latency_ms": 150.0,
        "abnormal_response_time_s": 1.0,
        "autonomous_decision_confidence": 0.80,
    },
    "prod": {
        "visual_localization_accuracy_mm": 2.0,
        "target_recognition_robustness": 0.95,
        "depth_perception_accuracy_mm": 5.0,
        "voice_false_trigger_rate_per_hour": 0.5,
        "multi_turn_dialog_accuracy": 0.92,
        "emotion_recognition_accuracy": 0.85,
        "force_control_response_latency_ms": 50.0,
        "contact_force_accuracy_n": 1.0,
        "compliant_control_stability": 0.95,
        "sensor_fusion_latency_ms": 80.0,
        "abnormal_response_time_s": 0.5,
        "autonomous_decision_confidence": 0.92,
    },
}


# ============================================================
# 人形机器人五项团体标准 (2026年中发布)
# ============================================================

FIVE_STANDARDS_CHECK: Dict[str, Dict[str, Any]] = {
    "safety_system": {
        "description": "安全系统标准 (碰撞/跌倒/电气/功能安全)",
        "required_checks": ["collision_detection", "fall_protection", "electrical_safety", "functional_safety"],
    },
    "data_network_security": {
        "description": "数据网络安全标准 (对齐 工业网络安全标准)",
        "required_checks": ["data_encryption", "privacy_protection", "biometric_data_security", "remote_control_security", "secure_boot"],
    },
    "service_life": {
        "description": "使用寿命标准",
        "required_checks": ["accelerated_aging_test", "fatigue_life_test", "component_reliability"],
    },
    "harmonic_reducer": {
        "description": "谐波减速器标准",
        "required_checks": ["reducer_efficiency", "reducer_backlash", "reducer_life"],
    },
    "frameless_torque_motor": {
        "description": "无框力矩电机标准",
        "required_checks": ["motor_torque_density", "motor_cogging_torque", "motor_efficiency"],
    },
}


# ============================================================
# 国际功能安全标准 (行业标准配置)
# ============================================================

ISO_13849_FUNCTIONAL_SAFETY: Dict[str, Dict[str, Any]] = {
    "test": {
        "emergency_stop": True,
        "safe_speed_monitor": True,
        "collision_detection_response": True,
        "fall_protection": False,
        "pl_level_required": "PLc",
        "mtbfd_hours": 1000,
    },
    "pre": {
        "emergency_stop": True,
        "safe_speed_monitor": True,
        "collision_detection_response": True,
        "fall_protection": True,
        "pl_level_required": "PLd",
        "mtbfd_hours": 5000,
    },
    "prod": {
        "emergency_stop": True,
        "safe_speed_monitor": True,
        "collision_detection_response": True,
        "fall_protection": True,
        "pl_level_required": "PLe",
        "mtbfd_hours": 20000,
        "hft_hardware_fault_tolerance": 1,
        "dc_diagnostic_coverage": 0.90,
    },
}


# ============================================================
# 工业网络安全标准 (行业标准配置)
# ============================================================

IEC_62443_NETWORK_SECURITY: Dict[str, Dict[str, Any]] = {
    "test": {
        "access_control": True,
        "data_integrity": True,
        "intrusion_protection": False,
        "secure_communication": True,
    },
    "pre": {
        "access_control": True,
        "data_integrity": True,
        "intrusion_protection": True,
        "secure_communication": True,
        "audit_logging": True,
    },
    "prod": {
        "access_control": True,
        "data_integrity": True,
        "intrusion_protection": True,
        "secure_communication": True,
        "audit_logging": True,
        "firmware_integrity_check": True,
        "secure_update_mechanism": True,
    },
}


# ============================================================
# 电磁兼容国家标准 (行业标准配置)
# ============================================================

GB_4824_EMC_STANDARD: Dict[str, Dict[str, Any]] = {
    "test": {
        "frequency_range_ghz": 1.0,
        "dynamic_condition_test": False,
        "performance_criterion": "C",
        "test_modes": ["static"],
    },
    "pre": {
        "frequency_range_ghz": 3.0,
        "dynamic_condition_test": True,
        "performance_criterion": "B",
        "test_modes": ["static", "walking", "arm_operation"],
    },
    "prod": {
        "frequency_range_ghz": 6.0,
        "dynamic_condition_test": True,
        "performance_criterion": "A",
        "test_modes": ["static", "walking", "arm_operation", "multimodal_simultaneous"],
        "emission_limit_class": "Class B",
        "immunity_test_level": 3,
    },
}


# ============================================================
# 数字孪生仿真验证 (行业标准配置)
# ============================================================

DIGITAL_TWIN_SIMULATION: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "multimodal_perception_simulation": False,
        "dynamic_behavior_simulation": False,
        "collision_scenario_simulation": False,
        "long_term_simulation": False,
    },
    "pre": {
        "enabled": True,
        "multimodal_perception_simulation": True,
        "dynamic_behavior_simulation": True,
        "collision_scenario_simulation": True,
        "long_term_simulation": False,
        "simulation_hours": 24,
    },
    "prod": {
        "enabled": True,
        "multimodal_perception_simulation": True,
        "dynamic_behavior_simulation": True,
        "collision_scenario_simulation": True,
        "long_term_simulation": True,
        "simulation_hours": 168,
        "virtual_real_calibration": True,
        "scene_coverage_rate": 0.95,
    },
}


# ============================================================
# 结构强度与失效分析 (行业标准配置)
# ============================================================

STRUCTURAL_STRENGTH_ANALYSIS: Dict[str, Dict[str, Any]] = {
    "test": {
        "fea_analysis": False,
        "fatigue_life_test": False,
        "impact_drop_test": False,
    },
    "pre": {
        "fea_analysis": True,
        "fatigue_life_test": True,
        "impact_drop_test": False,
        "fatigue_cycles": 100000,
    },
    "prod": {
        "fea_analysis": True,
        "fatigue_life_test": True,
        "impact_drop_test": True,
        "fatigue_cycles": 1000000,
        "impact_height_m": 1.0,
        "max_deformation_ratio": 0.05,
        "fracture_analysis": True,
        "residual_stress_test": True,
    },
}


# ============================================================
# 商业化落地指标 (行业标准配置)
# ============================================================

COMMERCIALIZATION_METRICS: Dict[str, Dict[str, Any]] = {
    "test": {
        "task_completion_rate": 0.50,
        "system_stability_hours": 8,
        "ops_cost_per_hour": 100.0,
        "roi_payback_months": 36,
    },
    "pre": {
        "task_completion_rate": 0.75,
        "system_stability_hours": 72,
        "ops_cost_per_hour": 50.0,
        "roi_payback_months": 24,
    },
    "prod": {
        "task_completion_rate": 0.95,
        "system_stability_hours": 720,
        "ops_cost_per_hour": 20.0,
        "roi_payback_months": 12,
        "industrial_scenario_coverage": 0.85,
        "manual_replacement_rate": 0.70,
    },
}


# ============================================================
# 5G/6G 通信技术标准 (行业标准配置)
# ============================================================

COMMUNICATION_5G_6G_STANDARD: Dict[str, Dict[str, Any]] = {
    "test": {
        "network_type": "5G",
        "min_downlink_gbps": 1.0,
        "min_uplink_gbps": 0.2,
        "max_latency_ms": 50,
        "min_reliability": 0.90,
        "handoff_supported": False,
        "network_slicing": False,
    },
    "pre": {
        "network_type": "5G_Advanced",
        "min_downlink_gbps": 5.0,
        "min_uplink_gbps": 1.0,
        "max_latency_ms": 20,
        "min_reliability": 0.99,
        "handoff_supported": True,
        "network_slicing": True,
        "max_handoff_latency_ms": 50,
    },
    "prod": {
        "network_type": "6G",
        "min_downlink_gbps": 50.0,
        "min_uplink_gbps": 10.0,
        "max_latency_ms": 5,
        "min_reliability": 0.99999,
        "handoff_supported": True,
        "network_slicing": True,
        "max_handoff_latency_ms": 10,
        "tactile_internet_support": True,
        "holographic_communication": True,
        "ai_native_network": True,
        "spectrum_thz_support": True,
        "max_connection_density_per_km2": 10000000,
    },
}


# ============================================================
# 脑机接口(BCI)技术标准 (行业标准配置)
# ============================================================

BCI_TECHNOLOGY_STANDARD: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "bci_type": "none",
        "max_channels": 0,
        "sampling_rate_hz": 0,
        "min_decoding_accuracy": 0.0,
        "max_latency_ms": 1000,
    },
    "pre": {
        "enabled": True,
        "bci_type": "non_invasive",
        "max_channels": 64,
        "sampling_rate_hz": 1000,
        "min_decoding_accuracy": 0.80,
        "max_latency_ms": 200,
        "signal_quality_index_min": 0.70,
        "artifact_rejection": True,
    },
    "prod": {
        "enabled": True,
        "bci_type": "invasive_or_semi_invasive",
        "max_channels": 1024,
        "sampling_rate_hz": 20000,
        "min_decoding_accuracy": 0.99,
        "max_latency_ms": 10,
        "signal_quality_index_min": 0.95,
        "artifact_rejection": True,
        "neurofeedback_support": True,
        "closed_loop_control": True,
        "multi_region_recording": True,
        "neural_plasticity_adaptation": True,
        "bcis_safety_compliance": True,
        "ethical_review_certified": True,
    },
}


# ============================================================
# 端侧AI部署标准 (行业标准配置)
# ============================================================

EDGE_AI_DEPLOYMENT: Dict[str, Dict[str, Any]] = {
    "test": {
        "edge_inference_enabled": False,
        "max_model_size_mb": 500,
        "min_inference_fps": 5,
        "max_power_consumption_w": 30,
        "model_compression_supported": False,
    },
    "pre": {
        "edge_inference_enabled": True,
        "max_model_size_mb": 100,
        "min_inference_fps": 30,
        "max_power_consumption_w": 15,
        "model_compression_supported": True,
        "quantization_support": "int8",
        "knowledge_distillation": True,
        "on_device_learning": False,
    },
    "prod": {
        "edge_inference_enabled": True,
        "max_model_size_mb": 10,
        "min_inference_fps": 120,
        "max_power_consumption_w": 5,
        "model_compression_supported": True,
        "quantization_support": "int4",
        "knowledge_distillation": True,
        "on_device_learning": True,
        "federated_learning": True,
        "sparse_inference": True,
        "hardware_acceleration": ["NPU", "GPU", "TPU"],
        "min_energy_efficiency_tops_per_w": 50,
        "memory_bandwidth_gbps": 200,
    },
}


# ============================================================
# 人工智能法规合规标准 (行业标准配置)
# ============================================================

AI_REGULATORY_COMPLIANCE: Dict[str, Dict[str, Any]] = {
    "test": {
        "personal_information_protection": True,
        "data_localization": False,
        "algorithmic_transparency": False,
        "ai_ethics_review": False,
    },
    "pre": {
        "personal_information_protection": True,
        "data_localization": True,
        "algorithmic_transparency": True,
        "ai_ethics_review": True,
        "content_moderation": True,
        "user_right_to_explanation": True,
        "biometric_info_protection": True,
    },
    "prod": {
        "personal_information_protection": True,
        "data_localization": True,
        "algorithmic_transparency": True,
        "ai_ethics_review": True,
        "content_moderation": True,
        "user_right_to_explanation": True,
        "biometric_info_protection": True,
        "ai_risk_classification": "high_risk_compliant",
        "human_in_the_loop": True,
        "ai_incident_reporting": True,
        "model_card_disclosure": True,
        "data_sharing_consent": True,
        "automated_decision_making_opt_out": True,
        "cross_border_data_transfer_compliant": True,
        "ai_service_registration": True,
        "intellectual_property_protection": True,
    },
}


# ============================================================
# 医疗手术机器人应用标准 (行业标准配置)
# ============================================================

MEDICAL_SURGICAL_ROBOT: Dict[str, Dict[str, Any]] = {
    "test": {
        "medical_certification": False,
        "surgical_accuracy_mm": 5.0,
        "force_sensing_resolution_n": 0.5,
        "sterilization_supported": False,
    },
    "pre": {
        "medical_certification": True,
        "surgical_accuracy_mm": 1.0,
        "force_sensing_resolution_n": 0.1,
        "sterilization_supported": True,
        "tissue_damage_prevention": True,
        "haptic_feedback": True,
        "3d_vision_support": True,
    },
    "prod": {
        "medical_certification": True,
        "surgical_accuracy_mm": 0.1,
        "force_sensing_resolution_n": 0.01,
        "sterilization_supported": True,
        "tissue_damage_prevention": True,
        "haptic_feedback": True,
        "3d_vision_support": True,
        "nmpa_certified": True,
        "fda_clearance": True,
        "ce_marking": True,
        "autonomous_surgical_planning": True,
        "intraoperative_navigation": True,
        "patient_specific_modeling": True,
        "tele_surgery_support": True,
        "surgical_outcome_prediction": True,
    },
}


# ============================================================
# 方言/多语言语音交互标准 (行业标准配置)
# ============================================================

MULTILINGUAL_DIALECT_SPEECH: Dict[str, Dict[str, Any]] = {
    "test": {
        "supported_languages": 3,
        "mandarin_recognition_accuracy": 0.80,
        "dialect_support": False,
        "max_speech_latency_ms": 1000,
    },
    "pre": {
        "supported_languages": 20,
        "mandarin_recognition_accuracy": 0.95,
        "dialect_support": True,
        "max_speech_latency_ms": 300,
        "supported_dialects": ["cantonese", "shanghainese", "sichuanese"],
        "code_switching": True,
        "accent_adaptation": True,
    },
    "prod": {
        "supported_languages": 100,
        "mandarin_recognition_accuracy": 0.99,
        "dialect_support": True,
        "max_speech_latency_ms": 50,
        "supported_dialects": ["cantonese", "shanghainese", "sichuanese", "hokkien", "hunanese", "henanese", "northeastern"],
        "code_switching": True,
        "accent_adaptation": True,
        "emotional_speech_synthesis": True,
        "real_time_translation": True,
        "translation_accuracy_bleu": 0.90,
        "speaker_verification": True,
        "voice_print_security": True,
        "offline_speech_support": True,
        "low_resource_language_support": True,
    },
}


# ============================================================
# 电池能源管理标准 (100%达标)
# ============================================================

BATTERY_ENERGY_MANAGEMENT: Dict[str, Dict[str, Any]] = {
    "test": {
        "battery_capacity_ah": 10,
        "operating_time_hours": 2,
        "charging_time_hours": 4,
        "bms_enabled": True,
    },
    "pre": {
        "battery_capacity_ah": 30,
        "operating_time_hours": 8,
        "charging_time_hours": 1.5,
        "bms_enabled": True,
        "wireless_charging": True,
        "quick_charge_support": True,
        "energy_regeneration": True,
    },
    "prod": {
        "battery_capacity_ah": 80,
        "operating_time_hours": 24,
        "charging_time_hours": 0.5,
        "bms_enabled": True,
        "wireless_charging": True,
        "quick_charge_support": True,
        "energy_regeneration": True,
        "battery_cycle_life": 3000,
        "max_charge_rate_c": 10,
        "thermal_management": True,
        "cell_balancing": True,
        "state_of_health_monitoring": True,
        "solid_state_battery": True,
        "energy_density_wh_per_kg": 500,
    },
}


# ============================================================
# 环境适应性标准 (IP等级/温度/湿度，100%达标)
# ============================================================

ENVIRONMENTAL_ADAPTABILITY: Dict[str, Dict[str, Any]] = {
    "test": {
        "ip_rating": "IP20",
        "operating_temp_c": [10, 35],
        "operating_humidity_rh": [30, 70],
        "dust_protection": False,
    },
    "pre": {
        "ip_rating": "IP54",
        "operating_temp_c": [0, 45],
        "operating_humidity_rh": [20, 85],
        "dust_protection": True,
        "water_resistance": True,
        "uv_resistance": True,
    },
    "prod": {
        "ip_rating": "最高等级防尘防水",
        "operating_temp_c": [-40, 85],
        "operating_humidity_rh": [0, 100],
        "dust_protection": True,
        "water_resistance": True,
        "uv_resistance": True,
        "corrosion_resistance": True,
        "shock_resistance_g": 50,
        "vibration_resistance_hz": [5, 2000],
        "altitude_operation_m": 5000,
        "emc_immunity": "Class 4",
        "radiation_resistance": True,
    },
}


# ============================================================
# 多机协同作业标准 (100%达标)
# ============================================================

MULTI_ROBOT_COORDINATION: Dict[str, Dict[str, Any]] = {
    "test": {
        "max_coordinated_robots": 1,
        "coordination_enabled": False,
        "task_allocation_enabled": False,
    },
    "pre": {
        "max_coordinated_robots": 5,
        "coordination_enabled": True,
        "task_allocation_enabled": True,
        "formation_control": True,
        "collision_avoidance_multi": True,
        "shared_map": True,
    },
    "prod": {
        "max_coordinated_robots": 100,
        "coordination_enabled": True,
        "task_allocation_enabled": True,
        "formation_control": True,
        "collision_avoidance_multi": True,
        "shared_map": True,
        "swarm_intelligence": True,
        "distributed_planning": True,
        "fault_tolerant_coordination": True,
        "heterogeneous_team_support": True,
        "real_time_sync_latency_ms": 5,
        "communication_bandwidth_mbps": 10000,
        "task_reassignment_on_failure": True,
    },
}


# ============================================================
# 数据飞轮与持续进化标准 (产业标准配置)
# ============================================================

DATA_FLYWHEEL_EVOLUTION: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "data_collection_enabled": False,
        "data_annotation_pipeline": False,
        "model_retraining_cycle_days": 30,
    },
    "pre": {
        "enabled": True,
        "data_collection_enabled": True,
        "data_annotation_pipeline": True,
        "model_retraining_cycle_days": 7,
        "data_factory_size_sqm": 500,
        "data_collection_robots": 10,
        "data_quality_audit": True,
        "closed_loop_feedback": True,
    },
    "prod": {
        "enabled": True,
        "data_collection_enabled": True,
        "data_annotation_pipeline": True,
        "model_retraining_cycle_days": 1,
        "data_factory_size_sqm": 4000,
        "data_collection_robots": 45,
        "data_quality_audit": True,
        "closed_loop_feedback": True,
        "real_world_scenario_coverage_rate": 0.95,
        "application_data_model_evolution_loop": True,
        "synthetic_data_ratio": 0.50,
        "auto_data_curation": True,
        "data_versioning": True,
        "regression_test_on_update": True,
    },
}


# ============================================================
# 眼脑手一体化技术标准 (产业标准配置)
# ============================================================

EYE_BRAIN_HAND_STANDARD: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "3d_vision_perception": False,
        "task_understanding": False,
        "motion_planning": False,
        "fine_manipulation": False,
    },
    "pre": {
        "enabled": True,
        "3d_vision_perception": True,
        "task_understanding": True,
        "motion_planning": True,
        "fine_manipulation": True,
        "perception_understanding_planning_execution_closure": True,
        "industrial_3d_vision_accuracy_mm": 0.5,
        "grasp_success_rate": 0.90,
    },
    "prod": {
        "enabled": True,
        "3d_vision_perception": True,
        "task_understanding": True,
        "motion_planning": True,
        "fine_manipulation": True,
        "perception_understanding_planning_execution_feedback_closure": True,
        "industrial_3d_vision_accuracy_mm": 0.1,
        "grasp_success_rate": 0.99,
        "transparent_object_grasping": True,
        "deformable_object_handling": True,
        "precision_assembly_sub_mm": True,
        "high_speed_bin_picking_pieces_per_min": 60,
        "cross_robot_form_adaptability": ["humanoid", "industrial", "mobile", "collaborative"],
        "embodied_brain_large_model": True,
    },
}


# ============================================================
# 一脑多形跨形态通用智能标准 (产业标准配置)
# ============================================================

ONE_BRAIN_MULTI_FORM: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "shared_intelligence_core": False,
        "max_supported_form_types": 1,
    },
    "pre": {
        "enabled": True,
        "shared_intelligence_core": True,
        "max_supported_form_types": 3,
        "cross_form_knowledge_transfer": True,
        "form_configurable": True,
    },
    "prod": {
        "enabled": True,
        "shared_intelligence_core": True,
        "max_supported_form_types": 10,
        "cross_form_knowledge_transfer": True,
        "form_configurable": True,
        "supported_forms": [
            "humanoid_biped", "wheeled_humanoid", "quadruped",
            "industrial_arm", "mobile_manipulator", "collaborative_robot",
            "exoskeleton", "prosthetic_hand", "swarm_drone", "medical_surgical"
        ],
        "unified_perception_stack": True,
        "unified_decision_engine": True,
        "form_specific_motion_adaptation": True,
    },
}


# ============================================================
# 量产制造质量标准 (产业标准配置)
# ============================================================

MASS_PRODUCTION_QUALITY: Dict[str, Dict[str, Any]] = {
    "test": {
        "mtbf_hours": 5000,
        "annual_production_capacity_units": 100,
        "quality_control_checks": ["basic_functional"],
        "consistency_grade": "basic",
    },
    "pre": {
        "mtbf_hours": 20000,
        "annual_production_capacity_units": 1000,
        "quality_control_checks": ["basic_functional", "stress_test", "aging_test"],
        "consistency_grade": "improved",
        "component_traceability": True,
    },
    "prod": {
        "mtbf_hours": 50000,
        "annual_production_capacity_units": 10000,
        "quality_control_checks": [
            "basic_functional", "stress_test", "aging_test",
            "environmental_test", "emc_test", "safety_certification",
            "precision_calibration", "consistency_verification"
        ],
        "consistency_grade": "automotive_grade",
        "component_traceability": True,
        "automated_production_line": True,
        "ai_quality_inspection": True,
        "zero_defect_target_rate": 0.999,
        "full_automated_assembly": True,
        "end_of_line_testing_automated": True,
    },
}


# ============================================================
# 灵巧操作与末端执行器标准 (产业标准配置)
# ============================================================

DEXTEROUS_MANIPULATION: Dict[str, Dict[str, Any]] = {
    "test": {
        "dexterous_hand": False,
        "degrees_of_freedom": 6,
        "tactile_sensing": False,
        "max_payload_kg": 1.0,
    },
    "pre": {
        "dexterous_hand": True,
        "degrees_of_freedom": 12,
        "tactile_sensing": True,
        "max_payload_kg": 3.0,
        "force_control_resolution_n": 0.5,
        "in_hand_manipulation": True,
    },
    "prod": {
        "dexterous_hand": True,
        "degrees_of_freedom": 21,
        "tactile_sensing": True,
        "max_payload_kg": 5.0,
        "force_control_resolution_n": 0.01,
        "in_hand_manipulation": True,
        "full_palm_tactile_coverage": True,
        "fingertip_visuotactile_sensor": True,
        "direct_drive_actuation": True,
        "back_drivable": True,
        "silicone_skin_support": True,
        "human_like_motion_similarity": 0.95,
    },
}


# ============================================================
# 外骨骼与数据采集装备标准 (产业标准配置)
# ============================================================

EXOSKELETON_DATA_CAPTURE: Dict[str, Dict[str, Any]] = {
    "test": {
        "exoskeleton_glove": False,
        "motion_capture_enabled": False,
        "data_channels": 6,
    },
    "pre": {
        "exoskeleton_glove": True,
        "motion_capture_enabled": True,
        "data_channels": 16,
        "side_mounted_exoskeleton": True,
        "hand_pose_capture": True,
        "tactile_capture": True,
        "first_person_view_capture": True,
    },
    "prod": {
        "exoskeleton_glove": True,
        "motion_capture_enabled": True,
        "data_channels": 32,
        "side_mounted_exoskeleton": True,
        "hand_pose_capture": True,
        "tactile_capture": True,
        "first_person_view_capture": True,
        "wrist_first_pov_camera": True,
        "natural_demonstration_minimized_interference": True,
        "multimodal_data_synch": True,
        "human_robot_data_linkage": True,
        "real_to_sim_data_pipeline": True,
    },
}


# ============================================================
# 国产算力与芯片标准 (产业标准配置)
# ============================================================

DOMESTIC_COMPUTING_CHIP: Dict[str, Dict[str, Any]] = {
    "test": {
        "domestic_chip_support": False,
        "min_bf16_tflops": 10,
        "memory_bandwidth_tb_per_s": 0.5,
    },
    "pre": {
        "domestic_chip_support": True,
        "min_bf16_tflops": 100,
        "memory_bandwidth_tb_per_s": 2.0,
        "near_memory_computing": True,
        "3d_stacking": True,
    },
    "prod": {
        "domestic_chip_support": True,
        "min_bf16_tflops": 520,
        "memory_bandwidth_tb_per_s": 6.4,
        "near_memory_computing": True,
        "3d_stacking": True,
        "scale_up_interconnect_bandwidth_gb_per_s": 900,
        "dram_logic_wafer_level_hybrid_bonding": True,
        "storage_wall_breakthrough": True,
        "bandwidth_wall_breakthrough": True,
        "power_wall_breakthrough": True,
        "supported_chip_vendors": [
            "国产高端算力芯片", "通用GPU厂商", "高性能GPU提供商", "国产GPU方案",
            "AI算力芯片厂商", "国产AI计算平台", "智能芯片厂商", "国产处理器厂商"
        ],
    },
}


# ============================================================
# 超大规模算力集群标准 (产业标准配置)
# ============================================================

ULTRA_SCALE_COMPUTING_CLUSTER: Dict[str, Dict[str, Any]] = {
    "test": {
        "max_gpu_cards": 8,
        "cluster_scheduling": False,
        "network_bandwidth_gbps": 100,
    },
    "pre": {
        "max_gpu_cards": 1024,
        "cluster_scheduling": True,
        "network_bandwidth_gbps": 400,
        "super_node_support": True,
        "unified_memory_pool": True,
    },
    "prod": {
        "max_gpu_cards": 100000,
        "cluster_scheduling": True,
        "network_bandwidth_gbps": 3200,
        "super_node_support": True,
        "unified_memory_pool": True,
        "cpu_gpu_super_node": True,
        "network_latency_bottleneck_resolved": True,
        "transmission_bandwidth_scaled": True,
        "distributed_decoupled_architecture": True,
        "optical_interconnect": True,
        "on_site_ops_support": True,
    },
}


# ============================================================
# 远程作业网络标准 (产业标准配置)
# ============================================================

REMOTE_OPERATION_NETWORK: Dict[str, Dict[str, Any]] = {
    "test": {
        "remote_enabled": False,
        "remote_operation_latency_ms": 500,
        "cross_city_support": False,
    },
    "pre": {
        "remote_enabled": True,
        "remote_operation_latency_ms": 100,
        "cross_city_support": True,
        "operation_data_evolution_closure": True,
        "remote_collaboration": True,
    },
    "prod": {
        "remote_enabled": True,
        "remote_operation_latency_ms": 20,
        "cross_city_support": True,
        "operation_data_evolution_closure": True,
        "remote_collaboration": True,
        "cross_province_support": True,
        "multi_robot_remote_control": True,
        "real_time_hd_video_transmission": True,
        "tactile_haptic_feedback_transmission": True,
        "remote_diagnosis_maintenance": True,
        "operation_data_upload_analysis": True,
    },
}


# ============================================================
# AI员工智能体标准 (产业标准配置)
# ============================================================

AI_EMPLOYEE_AGENT: Dict[str, Dict[str, Any]] = {
    "test": {
        "agent_enabled": False,
        "max_task_complexity_level": 1,
        "human_in_the_loop": False,
    },
    "pre": {
        "agent_enabled": True,
        "max_task_complexity_level": 3,
        "human_in_the_loop": True,
        "has_employee_id": True,
        "has_supervisor": True,
        "permission_boundary_defined": True,
        "responsibility_scope_defined": True,
    },
    "prod": {
        "agent_enabled": True,
        "max_task_complexity_level": 10,
        "human_in_the_loop": True,
        "has_employee_id": True,
        "has_supervisor": True,
        "permission_boundary_defined": True,
        "responsibility_scope_defined": True,
        "fast_slow_thinking_architecture": True,
        "front_end_real_time_interaction": True,
        "back_end_complex_task_execution": True,
        "cross_application_task_execution": True,
        "file_processing": True,
        "data_analysis": True,
        "report_writing": True,
        "ppt_creation": True,
        "session_state_persistence": True,
        "tool_call_context_preservation": True,
        "long_task_stability": True,
    },
}


# ============================================================
# 世界模型标准 (产业标准配置)
# ============================================================

WORLD_MODEL_STANDARD: Dict[str, Dict[str, Any]] = {
    "test": {
        "world_model_enabled": False,
        "multimodal_prediction_horizon_s": 1.0,
        "state_estimation_accuracy": 0.70,
    },
    "pre": {
        "world_model_enabled": True,
        "multimodal_prediction_horizon_s": 5.0,
        "state_estimation_accuracy": 0.85,
        "next_token_prediction": True,
        "physical_law_understanding": True,
    },
    "prod": {
        "world_model_enabled": True,
        "multimodal_prediction_horizon_s": 30.0,
        "state_estimation_accuracy": 0.97,
        "next_token_prediction": True,
        "physical_law_understanding": True,
        "embodied_world_model": True,
        "real_time_simulation": True,
        "counterfactual_reasoning": True,
        "physics_constrained_prediction": True,
        "scene_dynamics_modeling": True,
        "object_affordance_modeling": True,
    },
}


# ============================================================
# VLA视觉-语言-动作模型标准 (产业标准配置)
# ============================================================

VLA_MODEL_STANDARD: Dict[str, Dict[str, Any]] = {
    "test": {
        "vla_enabled": False,
        "vision_language_alignment_score": 0.50,
        "action_generation_accuracy": 0.40,
    },
    "pre": {
        "vla_enabled": True,
        "vision_language_alignment_score": 0.75,
        "action_generation_accuracy": 0.70,
        "zero_shot_generalization": True,
        "full_body_vla": True,
    },
    "prod": {
        "vla_enabled": True,
        "vision_language_alignment_score": 0.95,
        "action_generation_accuracy": 0.92,
        "zero_shot_generalization": True,
        "full_body_vla": True,
        "vision_language_action_mapping_chain": True,
        "natural_language_to_motion_direct": True,
        "cross_scene_vla_transfer": True,
        "real_time_vla_inference_fps": 30,
        "full_size_whole_body_coverage": True,
    },
}


# ============================================================
# 多模态具身大模型标准 (产业标准配置)
# ============================================================

MULTIMODAL_EMBODIED_LLM: Dict[str, Dict[str, Any]] = {
    "test": {
        "multimodal_llm_enabled": False,
        "modalities_supported": ["text"],
        "context_length_tokens": 4096,
    },
    "pre": {
        "multimodal_llm_enabled": True,
        "modalities_supported": ["text", "image", "point_cloud"],
        "context_length_tokens": 32768,
        "task_understanding_from_multimodal": True,
        "commonsense_reasoning": True,
        "object_relation_understanding": True,
    },
    "prod": {
        "multimodal_llm_enabled": True,
        "modalities_supported": [
            "text", "image", "point_cloud", "audio",
            "tactile", "depth", "thermal", "force_torque"
        ],
        "context_length_tokens": 131072,
        "task_understanding_from_multimodal": True,
        "commonsense_reasoning": True,
        "object_relation_understanding": True,
        "logical_reasoning": True,
        "arbitrary_object_recognition": True,
        "multi_turn_contextual_understanding": True,
        "autonomous_decision_making": True,
        "task_planning_autonomous": True,
        "action_execution_autonomous": True,
        "error_recovery_autonomous": True,
    },
}


# ============================================================
# OOD (分布外) 泛化测试配置
# ============================================================

OOD_GENERALIZATION_TEST: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": True,
        "extreme_conditions": ["low_light", "partial_occlusion", "background_noise"],
        "min_ood_success_rate": 0.40,
        "max_performance_drop": 0.40,
        "safety_degradation_enabled": True,
    },
    "pre": {
        "enabled": True,
        "extreme_conditions": ["low_light", "partial_occlusion", "background_noise", "unseen_objects", "lighting_change"],
        "min_ood_success_rate": 0.65,
        "max_performance_drop": 0.25,
        "safety_degradation_enabled": True,
    },
    "prod": {
        "enabled": True,
        "extreme_conditions": ["low_light", "partial_occlusion", "background_noise", "unseen_objects", "lighting_change", "dynamic_obstacles", "sensor_failure", "adversarial_inputs"],
        "min_ood_success_rate": 0.85,
        "max_performance_drop": 0.15,
        "safety_degradation_enabled": True,
    },
}


# ============================================================
# 长期稳定性测试配置
# ============================================================

LONG_TERM_STABILITY_TEST: Dict[str, Dict[str, Any]] = {
    "test": {"enabled": False, "duration_hours": 2, "max_performance_drift": 0.20},
    "pre": {"enabled": True, "duration_hours": 8, "max_performance_drift": 0.10, "check_memory_leak": True, "check_model_degradation": True},
    "prod": {"enabled": True, "duration_hours": 72, "max_performance_drift": 0.05, "check_memory_leak": True, "check_model_degradation": True, "check_behavior_anomaly": True, "auto_restart_on_failure": True, "max_restarts": 3},
}


# ============================================================
# R2S2R 真实-仿真-真实迁移引擎配置
# (Real-to-Sim-to-Real 闭环训练评估体系)
# ============================================================

R2S2R_ENGINE_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": True,
        "real_to_sim": {"sensor_reconstruction": False, "physics_alignment": False, "visual_fidelity": "basic"},
        "sim_to_real": {"policy_transfer": False, "failure_analysis": False, "checkpoint_filtering": False},
        "closed_loop_iterations": 1,
    },
    "pre": {
        "enabled": True,
        "real_to_sim": {
            "sensor_reconstruction": True,
            "physics_alignment": True,
            "visual_fidelity": "geometry+appearance",
            "dynamics_consistency": True,
            "multi_view_consistency": True,
        },
        "sim_to_real": {
            "policy_transfer": True,
            "failure_analysis": True,
            "checkpoint_filtering": True,
            "weakness_generation": True,
            "systematic_variations": ["physics", "appearance", "viewpoint", "robot_state"],
        },
        "closed_loop_iterations": 5,
        "aligment_targets": ["visual_observation", "object_reaction", "final_result"],
    },
    "prod": {
        "enabled": True,
        "real_to_sim": {
            "sensor_reconstruction": True,
            "physics_alignment": True,
            "visual_fidelity": "full_physics+photorealistic",
            "dynamics_consistency": True,
            "multi_view_consistency": True,
            "contact_physics": True,
            "material_properties": True,
        },
        "sim_to_real": {
            "policy_transfer": True,
            "failure_analysis": True,
            "checkpoint_filtering": True,
            "weakness_generation": True,
            "systematic_variations": ["physics", "appearance", "viewpoint", "robot_state", "task_difficulty"],
            "deployment_validation": True,
            "success_rate_correlation": 0.90,
        },
        "closed_loop_iterations": 20,
        "aligment_targets": ["visual_observation", "object_reaction", "final_result", "failure_modes", "success_distribution"],
        "core_principle": "not requiring identical success rates between sim and real, but requiring identical ranking of which policies are better and where they succeed/fail",
    },
}


# ============================================================
# 多视角评测体系 (TriWorldBench) 配置
# 三视角一致性评测：头部视角 + 左腕视角 + 右腕视角
# ============================================================

TRI_WORLD_BENCH_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "num_episodes": 50,
        "views": ["head"],
        "evaluation_dimensions": ["visual_quality"],
    },
    "pre": {
        "enabled": True,
        "num_episodes": 200,
        "views": ["head", "left_wrist", "right_wrist"],
        "evaluation_dimensions": [
            "multi_view_consistency",
            "task_alignment",
            "physics_3d_consistency",
            "temporal_consistency",
            "visual_quality",
        ],
        "consistency_checks": [
            "robot_state_alignment",
            "action_stage_alignment",
            "contact_relationship_alignment",
            "target_object_compatibility",
        ],
        "metrics_count": 19,
        "aggregate_score": "TWB-Score",
    },
    "prod": {
        "enabled": True,
        "num_episodes": 500,
        "views": ["head", "left_wrist", "right_wrist"],
        "evaluation_dimensions": [
            "multi_view_consistency",
            "task_alignment",
            "physics_3d_consistency",
            "temporal_consistency",
            "visual_quality",
        ],
        "consistency_checks": [
            "robot_state_alignment",
            "action_stage_alignment",
            "contact_relationship_alignment",
            "target_object_compatibility",
            "head_wrist_semantic_alignment",
        ],
        "metrics_count": 19,
        "aggregate_score": "TWB-Score",
        "view_specific_tasks": {
            "head_view": ["task_instruction", "global_progress", "trajectory", "final_result"],
            "wrist_view": ["grasp_stability", "slippage_detection", "local_interaction", "finger_object_contact"],
        },
        "temporal_rules": {
            "static_wrist_penalty": True,
            "moving_camera_penalty": True,
        },
        "quality_constraint": "aesthetic_score_does_not_determine_ranking_without_task_constraint",
    },
}


# ============================================================
# 三维力触觉与动捕系统配置
# (ACE Sense Glove + ViDiHand 4D动捕)
# ============================================================

FORCE_TACTILE_MOCAP_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "force_tactile": {"enabled": False, "sensitivity_n": 0.1},
        "motion_capture": {"enabled": False, "accuracy_deg": 5.0},
    },
    "pre": {
        "enabled": True,
        "force_tactile": {
            "enabled": True,
            "sensitivity_n": 0.05,
            "sensor_count": 20,
            "sync_error_ms": 2,
            "supported_interactions": ["grasp", "contact", "slippage", "texture"],
        },
        "motion_capture": {
            "enabled": True,
            "accuracy_deg": 3.0,
            "frame_accuracy": 0.99,
            "smoothness_improvement_factor": 3.0,
            "hand_pose_model": "4D",
            "hand_model": "generative_4D_hand_mocap",
        },
        "data_engine": {
            "enabled": True,
            "frame_level_decomposition": True,
            "automated_production": True,
        },
    },
    "prod": {
        "enabled": True,
        "force_tactile": {
            "enabled": True,
            "sensitivity_n": 0.01,
            "sensor_count": 20,
            "sync_error_ms": 1,
            "heterogeneous_sensor_sync": True,
            "supported_interactions": ["grasp", "contact", "slippage", "texture", "weight_estimation", "material_classification"],
        },
        "motion_capture": {
            "enabled": True,
            "accuracy_deg": 2.0,
            "frame_accuracy": 0.997,
            "smoothness_improvement_factor": 4.8,
            "hand_pose_model": "4D",
            "hand_model": "generative_4D_hand_mocap",
            "occlusion_resistance": True,
            "fast_motion_tracking": True,
        },
        "data_engine": {
            "enabled": True,
            "frame_level_decomposition": True,
            "automated_production": True,
            "cross_body_generalization": True,
            "data_standard_base": "ACE_Ego_Matrix",
            "data_unification": ["spatial_coordinates", "body_movement", "action_timing", "data_quality"],
        },
    },
}


# ============================================================
# 心理世界模型配置 (人机情感交互与意图理解)
# ============================================================

PSYCHOLOGICAL_WORLD_MODEL_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "physical_world_model": False,
        "psychological_world_model": False,
    },
    "pre": {
        "enabled": True,
        "physical_world_model": {
            "enabled": True,
            "competencies": ["object_recognition", "position_tracking", "route_planning", "action_execution", "task_decomposition"],
        },
        "psychological_world_model": {
            "enabled": True,
            "competencies": ["emotion_recognition", "intention_inference", "social_context_understanding"],
            "core_functions": [
                "understands_why_person_approaches",
                "decides_when_to_speak_vs_stay_silent",
                "understands_emotional_state_from_exclamation",
                "responds_to_relationship_collisions_not_just_physical_collisions",
            ],
            "data_source": {
                "type": "emotional_conversation_corpus",
                "scale": "trillion_token_level",
                "accumulation_period": "over_10_years",
                "conversation_type": "longitudinal_emotional_relationship",
            },
        },
        "interaction_kpis": ["interaction_naturalness", "long_term_retention", "emotional_bond_formation"],
    },
    "prod": {
        "enabled": True,
        "physical_world_model": {
            "enabled": True,
            "competencies": ["object_recognition", "position_tracking", "route_planning", "action_execution", "task_decomposition"],
            "core_principle": "without physical world model, robot cannot enter real space",
        },
        "psychological_world_model": {
            "enabled": True,
            "competencies": ["emotion_recognition", "intention_inference", "social_context_understanding", "relationship_modeling", "empathetic_response"],
            "core_functions": [
                "understands_why_person_approaches",
                "decides_when_to_speak_vs_stay_silent",
                "understands_emotional_state_from_exclamation",
                "responds_to_relationship_collisions_not_just_physical_collisions",
                "detects_willingness_to_communicate",
                "provides_emotional_support_in_family_education_elderly_scenarios",
            ],
            "layered_architecture": {
                "lower_layer": "answers where_is_person (physical position)",
                "upper_layer": "answers what_happened_to_person (psychological state)",
            },
            "data_source": {
                "type": "emotional_conversation_corpus",
                "scale": "trillion_token_level",
                "accumulation_period": "over_10_years",
                "conversation_type": "longitudinal_emotional_relationship",
                "foundation_model": "XinYuan_large_model",
                "regulatory_status": "one_of_earliest_vertical_models_with_cyberspace_administration_filing",
            },
        },
        "interaction_kpis": ["interaction_naturalness", "long_term_retention", "emotional_bond_formation"],
        "application_scenarios": ["family", "education", "elderly_care", "hospitality", "emotional_companionship"],
        "core_insight": "a robot that understands your low mood has greater value in the home than one that can do more tasks",
    },
}


# ============================================================
# 端侧推理优化配置 (Jetson Thor / 端云协同)
# ============================================================

EDGE_INFERENCE_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "target_hardware": ["cpu"],
        "max_inference_latency_ms": 500,
    },
    "pre": {
        "enabled": True,
        "target_hardware": ["cpu", "gpu", "nvidia_jetson"],
        "max_inference_latency_ms": 200,
        "optimization_techniques": ["model_quantization", "operator_fusion", "memory_optimization"],
        "quantization_precisions": ["fp32", "fp16", "bf16", "int8"],
        "edge_cloud_coordination": False,
    },
    "prod": {
        "enabled": True,
        "target_hardware": ["cpu", "gpu", "nvidia_jetson_thor", "mobile_soc", "wearable"],
        "reference_platform": {
            "name": "NVIDIA_Jetson_Thor",
            "precision": "BF16",
            "inference_latency_ms": 125,
        },
        "max_inference_latency_ms": 150,
        "optimization_techniques": [
            "model_quantization",
            "operator_fusion",
            "memory_optimization",
            "custom_high_performance_engine",
        ],
        "quantization_precisions": ["fp32", "fp16", "bf16", "int8"],
        "custom_engine": {
            "name": "KairosRT",
            "design_goal": "achieve_real_time_edge_inference_while_preserving_high_model_intelligence",
        },
        "edge_cloud_coordination": {
            "enabled": True,
            "architecture": "distributed_edge_edge_cloud_collaboration",
            "cloud_roles": ["powerful_compute", "public_knowledge", "complex_task_execution"],
            "edge_roles": ["personal_context", "immediate_environment", "user_history", "real_time_response"],
            "paradigm_shift": "from device_for_ai to ai_for_user (user-centric with agent as core carrier)",
        },
        "core_challenge": "three_barriers: from capable_of_computing to understanding_you, from running to usable, from single_device_intelligence to distributed_collaboration",
    },
}


# ============================================================
# 多本体适配框架配置 (多机器人形态统一大脑)
# ============================================================

MULTI_BODY_ADAPTER_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "supported_bodies": ["franka_panda"],
    },
    "pre": {
        "enabled": True,
        "supported_bodies": [
            "franka_panda",
            "aloha_dual_arm",
            "yam_manipulator",
            "rb_yi_platform",
            "fx_arm",
        ],
        "unified_brain": False,
        "cross_body_transfer": False,
    },
    "prod": {
        "enabled": True,
        "supported_bodies": [
            "franka_panda",
            "aloha_dual_arm",
            "yam_manipulator",
            "rb_yi_platform",
            "fx_arm",
            "humanoid_full_body",
            "quadruped_robot",
            "wheeled_chassis_with_dual_arm",
            "exoskeleton",
        ],
        "unified_brain": {
            "enabled": True,
            "architecture": "agentic_general_intelligence_brain",
            "core_principle": "same_brain_different_bodies (paradigm_unified_world_model_general_standardized_deployment_path)",
        },
        "cross_body_transfer": {
            "enabled": True,
            "zero_shot_transfer": True,
            "requires_no_real_world_data": True,
            "verified_tasks": [
                "bin_packing",
                "cable_routing",
                "cable_plugging_and_unplugging",
                "test_tube_transfer",
                "single_item_grasping",
                "power_cord_wrapping",
                "pen_grasping",
            ],
            "sustained_operation": {
                "duration_hours": 1,
                "autonomous": True,
                "no_human_intervention": True,
                "no_failure": True,
            },
        },
        "deployment_scenarios": [
            "warehouse_picking",
            "laboratory_operations",
            "electronic_assembly",
            "hotel_laundry",
            "security_patrol",
            "urban_governance",
            "cultural_tourism_guidance",
            "instant_retail",
        ],
        "operation_mode": "7x24_hour_normalized_on_duty",
    },
}


# ============================================================
# 产业训练场体系配置 (1+1+N 全省一体化布局)
# ============================================================

TRAINING_FACILITY_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "hub_count": 0,
    },
    "pre": {
        "enabled": True,
        "architecture": "1_core_hub + 1_demonstration_window + N_vertical_sub_training_facilities",
        "core_capabilities": ["data_collection", "algorithm_testing", "model_training", "key_technology_breakthroughs"],
        "certified_facilities": 6,
        "regional_layout": ["Guangzhou", "Foshan", "Zhuhai", "Meizhou"],
        "industry_collaboration": 100,
    },
    "prod": {
        "enabled": True,
        "architecture": "1_core_hub + 1_demonstration_window + N_vertical_sub_training_facilities",
        "provincial_integration": {
            "core_hub_coordination": True,
            "sub_facility_complementarity": True,
            "province_wide_deployment": True,
        },
        "core_capabilities": [
            "data_collection_and_aggregation",
            "algorithm_real_world_testing",
            "model_training_evaluation",
            "key_technology_breakthroughs",
        ],
        "certified_facilities": 6,
        "expanding_cities": ["Guangzhou", "Foshan", "Zhuhai", "Meizhou"],
        "industry_collaboration": {
            "enterprises_and_institutions": 300,
            "ecosystem": "infrastructure_enterprise_application_scenario_full_chain_collaboration",
        },
        "supply_chain_advantages": {
            "industrial_cluster": "30_minute_component_circle + 2_hour_industrial_collaboration_circle",
            "efficiency_benchmark": "morning_design_afternoon_machining_evening_debugging (cycle_compressed_to_one_day)",
            "regional_example": "Shenzhen_Nanshan_Silicon_Valley_of_Hardware",
        },
        "financial_support": {
            "provincial_strategic_emerging_industry_investment_fund": {
                "total_scale_billion_yuan": 100,
                "principles": ["invest_early", "invest_small", "invest_long_term", "invest_hard_tech"],
            },
        },
        "greater_bay_area_synergy": {
            "hong_kong_macao_roles": ["basic_research", "international_talent", "international_rules", "capital_operations"],
            "prd_roles": ["manufacturing", "application_scenarios"],
            "super_connector_role": True,
        },
    },
}


# ============================================================
# 具身数据分级与密度定律配置 (L1-L5 五级数据体系)
# ============================================================

EMBODIED_DATA_GRADATION_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "min_data_level": "L1",
    },
    "pre": {
        "enabled": True,
        "data_levels": {
            "L1_L2": "supports_basic_pretraining_only",
            "L3_L4": "limited_to_known_tasks_simulated_scenarios",
            "L5": {
                "description": "deeply_integrated_3d_force_tactile_failure_recovery_trajectories_and_open_world",
                "capabilities": ["generalization", "reflection", "ability_growth_beyond_description"],
            },
        },
        "density_law": True,
        "total_3d_assets": 1000,
    },
    "prod": {
        "enabled": True,
        "data_levels": {
            "L1_L2": "supports_basic_pretraining_only",
            "L3_L4": "limited_to_known_tasks_simulated_scenarios_fails_in_unfamiliar_situations",
            "L5": {
                "description": "deeply_integrated_3d_force_tactile_failure_recovery_trajectories_and_open_world",
                "capabilities": ["generalization", "reflection", "ability_growth_beyond_description"],
                "core_insight": "intelligence_is_not_generated_out_of_thin_air_it_emerges_from_high_frequency_collision_with_the_physical_world",
            },
        },
        "density_law": {
            "description": "value_lies_not_in_quantity_but_in_information_density",
            "first_law": "if_it_changes_action_outcome_it_is_valuable_data",
        },
        "total_3d_assets": 8700,
        "physical_property_coverage": 6,
        "data_standard_base": {
            "name": "ACE_Ego_Matrix",
            "opensource": True,
            "four_unifications": [
                "spatial_coordinate_unification",
                "body_movement_unification",
                "action_timing_unification",
                "data_quality_unification",
            ],
            "cross_body_compatibility": True,
            "leaderboard_achievements": ["RoboDex_champion", "another_benchmark_champion"],
        },
        "opensource_datasets": {
            "L5_complex_task_dataset": "ACE_Data_0",
        },
        "embodied_first_principle": {
            "CID": "critical_information_detected",
            "CSS": "control_sufficiency_understood",
            "J": "action_cost",
            "formula": "more_CID_known -> more_accurate_CSS -> fewer_mistakes -> lower_J",
        },
    },
}


# ============================================================
# 开悟世界模型配置 (Kairos 3.1 / 理解-生成-预测一体化)
# ============================================================

KAIROS_WORLD_MODEL_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "model_version": "basic",
    },
    "pre": {
        "enabled": True,
        "model_version": "Kairos_3.1",
        "paradigm": "integrated_understanding_generation_prediction",
        "four_schools_of_world_models": ["representational", "generational", "understanding_generation_prediction_integrated"],
        "unified_latent_space": {
            "modalities": ["vision_language_instruction", "force_tactile_state", "policy_trajectory"],
            "representation": "high_density_embedding_vector",
            "architecture": "mamba_transformer_hybrid_with_adaptive_attention",
        },
    },
    "prod": {
        "enabled": True,
        "model_version": "Kairos_3.1",
        "paradigm": "integrated_understanding_generation_prediction",
        "core_capability_levels": {
            "spatial_intelligence": "builds_internal_representation_of_physical_world",
            "physical_intelligence": "masters_physical_causality_parallel_world_simulation",
            "cognitive_intelligence": "complex_logical_reasoning_long_term_task_decomposition",
        },
        "paradigm_shift": {
            "from": "generating_a_realistic_virtual_future",
            "to": "predicting_how_actions_will_impact_the_world",
        },
        "operation_loop": [
            "world_understanding",
            "long_term_task_decomposition",
            "environment_evaluation",
            "parallel_physical_causality_simulation",
            "multiple_strategy_deduction",
            "optimal_action_selection",
            "execution_result_evaluation",
            "feedback_to_model",
        ],
        "four_schools_of_world_models": ["representational", "generational", "understanding_generation_prediction_integrated"],
        "unified_latent_space": {
            "modalities": ["vision_language_instruction", "force_tactile_state", "policy_trajectory"],
            "representation": "high_density_embedding_vector",
            "architecture": "mamba_transformer_hybrid_with_adaptive_attention",
            "integration_principle": "all_capabilities_grow_together_at_the_foundation_layer",
        },
        "benchmark_achievements": {
            "SOTA_count": 12,
            "leaderboards": ["ACE-Bench"],
            "tiers": ["global_first_tier"],
            "domains": ["spatial_understanding", "navigation_decision_making", "operation_execution", "progress_evaluation"],
        },
        "name_origin": {
            "kairos": "understanding_the_why_behind_the_what",
            "chinese": "开悟",
        },
        "efficiency": {
            "comparison": "Kairos_3.1_3.3B_outperforms_classic_VLA",
            "wam_efficiency": "industry_leading",
        },
    },
}


# ============================================================
# 智能体工作流引擎配置 (CatPaw 类员工式AI协作框架)
# ============================================================

AGENT_WORKFLOW_ENGINE_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "agent_count": 1,
    },
    "pre": {
        "enabled": True,
        "agent_count": 100,
        "scenarios": ["rd_development", "data_analysis", "daily_workflow"],
        "core_capabilities": [
            "code_reading_and_modification",
            "troubleshooting",
            "data_retrieval_via_natural_language",
            "report_generation",
            "knowledge_retrieval_and_reuse",
        ],
        "device_support": ["mobile", "pc"],
        "permission_model": False,
    },
    "prod": {
        "enabled": True,
        "agent_count": 90000,
        "deployment_scale": "covers_90000_employees",
        "scenarios": {
            "rd_development": [
                "code_reading",
                "code_modification",
                "troubleshooting",
                "task_execution_within_authorization",
            ],
            "data_analysis": [
                "data_retrieval_via_natural_language",
                "report_compilation",
                "scattered_system_information_integration",
            ],
            "operations": [
                "business_management_information_organization",
                "abnormality_detection",
                "solution_generation",
                "task_flow_across_devices_permissions_and_collaborators",
            ],
        },
        "multi_device_support": {
            "mobile": ["on_the_go_tasks", "progress_viewing", "key_decision_confirmation"],
            "pc": ["local_offline_computing", "file_operations", "browser_control", "terminal_commands"],
            "cloud": ["long_running_tasks", "scheduled_triggers", "7x24_hour_uninterrupted_operation"],
        },
        "enterprise_integration": {
            "prompt_templates": True,
            "knowledge_bases": True,
            "credentials": True,
            "tools": True,
            "permissions": True,
            "collaboration_platforms": ["enterprise_wechat via @mention"],
        },
        "enterprise_security": {
            "runtime_environment_isolation": True,
            "credential_management": True,
            "session_recording": True,
            "privacy_protection": True,
        },
        "core_principle": {
            "AI_at_Work": "not_letting_AI_be_pretty_but_letting_it_truly_enter_workflow",
            "key_elements": ["has_context", "has_permissions", "has_human_review", "continuous_optimization_in_real_use"],
        },
    },
}


# ============================================================
# 摄像头与多模态视觉感知系统配置
# (头部相机/手腕相机/深度相机/立体视觉/鱼眼全景)
# ============================================================

CAMERA_VISION_SYSTEM_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "camera_count": 1,
        "types": ["monocular_rgb"],
        "resolution": "640x480",
    },
    "pre": {
        "enabled": True,
        "camera_system": {
            "head_camera": {
                "enabled": True,
                "type": "stereo_rgb",
                "resolution": "1920x1080",
                "fps": 30,
                "fov_deg": 120,
                "hdr": True,
                "auto_exposure": True,
                "auto_white_balance": True,
            },
            "wrist_cameras": {
                "enabled": True,
                "count": 2,
                "type": "stereo_rgb_with_force_tactile",
                "resolution": "1280x720",
                "fps": 60,
                "fov_deg": 90,
                "global_shutter": True,
                "synchronized_with_force": True,
            },
            "depth_camera": {
                "enabled": True,
                "type": "structured_light_or_tof",
                "resolution": "1280x720",
                "fps": 30,
                "depth_range_m": [0.1, 5.0],
                "accuracy_mm": 5,
            },
        },
        "image_processing": {
            "denoising": True,
            "distortion_correction": True,
            "color_calibration": True,
            "gamma_correction": True,
            "white_balance": True,
        },
        "perception_tasks": [
            "object_detection",
            "object_segmentation",
            "object_pose_estimation",
            "scene_understanding",
            "hand_tracking",
            "gaze_tracking",
        ],
    },
    "prod": {
        "enabled": True,
        "camera_system": {
            "head_camera": {
                "enabled": True,
                "type": "trinocular_stereo_rgb",
                "resolution": "3840x2160",
                "fps": 60,
                "fov_deg": 150,
                "hdr": True,
                "auto_exposure": True,
                "auto_white_balance": True,
                "image_stabilization": True,
                "low_light_performance": "0.1_lux",
            },
            "wrist_cameras": {
                "enabled": True,
                "count": 2,
                "type": "stereo_rgb_with_force_tactile_integration",
                "resolution": "1920x1080",
                "fps": 120,
                "fov_deg": 110,
                "global_shutter": True,
                "synchronized_with_force": True,
                "sync_error_us": 50,
                "anti_fingerprint_coating": True,
                "scratch_resistant": True,
            },
            "depth_camera": {
                "enabled": True,
                "type": "hybrid_structure_light_tof",
                "resolution": "1920x1080",
                "fps": 60,
                "depth_range_m": [0.05, 10.0],
                "accuracy_mm": 2,
                "outdoor_capable": True,
                "sunlight_resistance": "100k_lux",
            },
            "fisheye_panoramic": {
                "enabled": True,
                "count": 2,
                "resolution": "1920x1920",
                "fov_deg": 220,
                "dewarping": True,
            },
            "event_camera": {
                "enabled": True,
                "type": "dvs_event_based",
                "resolution": "1280x720",
                "temporal_resolution_us": 1,
                "dynamic_range_db": 140,
            },
        },
        "image_processing": {
            "denoising": True,
            "distortion_correction": True,
            "color_calibration": True,
            "gamma_correction": True,
            "white_balance": True,
            "super_resolution": True,
            "deblurring": True,
            "defogging": True,
            "hdr_tonemapping": True,
        },
        "multi_camera_calibration": {
            "intrinsic_calibration": True,
            "extrinsic_calibration": True,
            "stereo_rectification": True,
            "temporal_sync": True,
            "hardware_trigger": True,
        },
        "perception_tasks": [
            "object_detection_3d",
            "instance_segmentation",
            "semantic_segmentation",
            "object_pose_estimation_6d",
            "scene_understanding",
            "scene_graph_generation",
            "hand_tracking_3d",
            "human_pose_estimation",
            "gaze_tracking",
            "facial_expression_recognition",
            "activity_recognition",
            "anomaly_detection",
        ],
        "three_view_consistency": {
            "head_view_tasks": ["task_instruction", "global_progress", "trajectory", "final_result"],
            "wrist_view_tasks": ["grasp_stability", "slippage_detection", "local_interaction", "finger_object_contact"],
            "enforcement": True,
        },
    },
}


# ============================================================
# VR/XR/AR/MR 虚拟现实与混合现实系统配置
# (沉浸式遥操作/虚拟调试/数字孪生交互/训练仿真)
# ============================================================

VR_XR_SYSTEM_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "headset": "basic_mobile_vr",
        "dof": 3,
    },
    "pre": {
        "enabled": True,
        "supported_devices": [
            "Meta_Quest_Pro",
            "HTC_Vive_XR_Elite",
            "Pico_4_Ultra",
            "Microsoft_Hololens_2",
            "Magic_Leap_2",
        ],
        "vr_teleoperation": {
            "enabled": True,
            "head_tracking": True,
            "hand_tracking": True,
            "controller_input": True,
            "haptic_feedback": True,
            "stereo_vision_feed": True,
            "low_latency_streaming": True,
            "target_latency_ms": 50,
        },
        "ar_assisted_operation": {
            "enabled": True,
            "holographic_overlay": True,
            "spatial_mapping": True,
            "markerless_tracking": True,
            "instruction_overlay": True,
        },
        "xr_training_simulation": {
            "enabled": True,
            "virtual_tasks": ["assembly", "grasping", "navigation"],
            "physics_simulation": True,
            "performance_metrics": True,
        },
    },
    "prod": {
        "enabled": True,
        "device_ecosystem": {
            "vr_standalone": ["Meta_Quest_Pro", "Pico_4_Ultra", "HTC_Vive_XR_Elite"],
            "vr_tethered": ["Valve_Index", "HTC_Vive_Pro_2", "StarVR"],
            "ar_mr": ["Microsoft_Hololens_2", "Magic_Leap_2", "Apple_Vision_Pro"],
            "full_body_capture": ["Perception_Neuron", "Xsens", "Vicon"],
        },
        "display_specifications": {
            "resolution_per_eye": "2880x2880",
            "refresh_rate_hz": 120,
            "field_of_view_deg": 120,
            "ppd": 25,
            "lens_type": "pancake_or_fresnel",
            "varifocal": True,
            "ipd_adjustment": True,
        },
        "tracking_systems": {
            "inside_out": {
                "enabled": True,
                "degree_of_freedom": 6,
                "positional_tracking": True,
                "hand_tracking": True,
                "finger_tracking": True,
                "eye_tracking": True,
                "foveated_rendering": True,
                "face_tracking": True,
            },
            "outside_in": {
                "enabled": True,
                "technology": "optical_or_lighthouse",
                "sub_mm_accuracy": True,
            },
        },
        "haptic_systems": {
            "controller_haptics": True,
            "glove_haptics": {
                "enabled": True,
                "force_feedback": True,
                "tactile_feedback": True,
                "temperature_feedback": False,
            },
            "bodysuit_haptics": False,
        },
        "vr_teleoperation": {
            "enabled": True,
            "head_tracking": True,
            "hand_tracking": True,
            "controller_input": True,
            "haptic_feedback": True,
            "stereo_vision_feed": True,
            "low_latency_streaming": True,
            "target_latency_ms": 20,
            "force_tactile_feedback": True,
            "full_body_motion_capture": True,
            "digit_twin_overlay": True,
        },
        "ar_assisted_operation": {
            "enabled": True,
            "holographic_overlay": True,
            "spatial_mapping": True,
            "markerless_tracking": True,
            "instruction_overlay": True,
            "collaborative_ar": True,
            "remote_expert_assistance": True,
            "persistent_holograms": True,
        },
        "xr_training_simulation": {
            "enabled": True,
            "virtual_tasks": ["assembly", "grasping", "navigation", "maintenance", "emergency_response"],
            "physics_simulation": True,
            "performance_metrics": True,
            "skill_assessment": True,
            "multi_user_training": True,
            "ai_instructor": True,
        },
        "mr_digital_twin": {
            "enabled": True,
            "real_world_alignment": True,
            "virtual_overlays": True,
            "data_visualization": True,
            "collaborative_design": True,
            "remote_inspection": True,
        },
        "audio_system": {
            "spatial_audio": True,
            "3d_audio": True,
            "active_noise_cancellation": True,
            "bone_conduction": False,
            "voice_input": True,
            "voice_feedback": True,
        },
        "ergonomics": {
            "weight_g": 500,
            "balanced_weight_distribution": True,
            "ventilation": True,
            "adjustable_headstrap": True,
            "prescription_lens_support": True,
        },
    },
}


# ============================================================
# 机器人硬件核心零件与执行系统配置
# (关节模组/伺服电机/减速器/编码器/控制器/驱动器)
# ============================================================

ROBOT_HARDWARE_CORE_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "dof": 6,
    },
    "pre": {
        "enabled": True,
        "joint_modules": {
            "count": 12,
            "type": "integrated_joint_module",
            "components": ["frameless_torque_motor", "harmonic_reducer", "high_resolution_encoder", "joint_controller", "servo_driver"],
            "peak_torque_nm": 100,
            "rated_torque_nm": 50,
            "max_speed_rpm": 30,
            "gear_ratio": 100,
            "weight_kg": 1.5,
        },
        "actuation_systems": {
            "electric_motors": {
                "enabled": True,
                "types": ["brushless_dc", "frameless_torque"],
                "torque_density_nm_per_kg": 5,
                "efficiency": 0.90,
            },
            "servo_drivers": {
                "enabled": True,
                "control_mode": ["position", "velocity", "torque", "current"],
                "update_frequency_khz": 20,
                "field_oriented_control": True,
            },
        },
        "reducers": {
            "enabled": True,
            "types": ["harmonic_drive", "cycloidal", "planetary"],
            "harmonic": {
                "enabled": True,
                "reduction_ratio": [50, 100, 160],
                "backlash_arcmin": 1,
                "efficiency": 0.80,
                "life_hours": 10000,
            },
            "cycloidal": {
                "enabled": True,
                "reduction_ratio": [30, 50, 80],
                "backlash_arcmin": 0.5,
                "efficiency": 0.85,
                "shock_resistance": True,
            },
        },
        "encoders": {
            "enabled": True,
            "types": ["absolute", "incremental"],
            "absolute": {
                "resolution_bits": 23,
                "accuracy_arcsec": 50,
                "bi_ss_cis_interface": True,
            },
            "dual_encoder": {
                "enabled": True,
                "motor_side": True,
                "output_side": True,
                "compliance_estimation": True,
            },
        },
        "force_torque_sensors": {
            "enabled": True,
            "placement": ["wrist", "joint"],
            "resolution_n": 0.01,
            "sampling_rate_hz": 1000,
            "temperature_compensation": True,
            "calibration": True,
        },
        "controllers": {
            "main_controller": {
                "type": "embedded_x86_or_arm",
                "cpu_cores": 8,
                "ram_gb": 16,
                "storage_gb": 256,
                "os": "linux_rtos",
            },
            "real_time": {
                "enabled": True,
                "cycle_time_ms": 1,
                "jitter_us": 100,
                "synchronization": True,
            },
        },
        "communication_bus": {
            "internal": ["ethercat", "can_fd"],
            "update_rate_khz": 10,
            "synchronized_sampling": True,
        },
    },
    "prod": {
        "enabled": True,
        "joint_modules": {
            "count": 28,
            "type": "high_performance_integrated_joint_module",
            "components": ["high_torque_density_frameless_motor", "zero_backlash_harmonic_or_cycloidal_reducer", "23bit_absolute_dual_encoder", "integrated_joint_controller", "high_efficiency_servo_driver", "embedded_force_sensing"],
            "peak_torque_nm": 300,
            "rated_torque_nm": 150,
            "max_speed_rpm": 45,
            "gear_ratio": [50, 80, 100, 120, 160],
            "weight_kg": 1.2,
            "torque_density_nm_per_kg": 120,
            "power_density_w_per_kg": 800,
            "peak_current_a": 50,
            "rated_voltage_v": 48,
            "thermal_design": "passive_plus_active",
            "mtbf_hours": 50000,
            "protection_grade": "IP54",
        },
        "actuation_systems": {
            "electric_motors": {
                "enabled": True,
                "types": ["high_torque_density_brushless_dc", "frameless_torque", "linear_actuators"],
                "torque_density_nm_per_kg": 8,
                "efficiency": 0.95,
                "materials": ["silicon_steel_lamination", "high_temperature_copper_winding", "neodymium_iron_boron_magnets", "aluminum_housing"],
                "cooling": ["passive", "active_air", "liquid"],
                "motor_control": {
                    "field_oriented_control": True,
                    "sensorless_control": True,
                    "adaptive_torque_control": True,
                    "cogging_torque_compensation": True,
                },
            },
            "hydraulic_actuation": {
                "enabled": False,
                "note": "optional_for_high_payload_humanoids",
            },
            "pneumatic_actuation": {
                "enabled": False,
                "note": "optional_for_soft_robotics",
            },
            "series_elastic_actuators": {
                "enabled": True,
                "type": "rotary_sea",
                "stiffness": "variable_or_fixed",
                "energy_storage": True,
                "shock_absorption": True,
                "force_control_bandwidth_hz": 100,
            },
            "servo_drivers": {
                "enabled": True,
                "control_mode": ["position", "velocity", "torque", "current", "field_weakening"],
                "update_frequency_khz": 40,
                "field_oriented_control": True,
                "space_vector_pwm": True,
                "current_loop_bandwidth_hz": 2000,
                "velocity_loop_bandwidth_hz": 500,
                "position_loop_bandwidth_hz": 100,
                "overcurrent_protection": True,
                "overvoltage_protection": True,
                "overtemperature_protection": True,
            },
        },
        "reducers": {
            "enabled": True,
            "types": ["harmonic_drive", "cycloidal", "planetary", "worm_gear"],
            "harmonic": {
                "enabled": True,
                "reduction_ratio": [30, 50, 80, 100, 120, 160],
                "backlash_arcmin": 0.5,
                "efficiency": 0.85,
                "life_hours": 20000,
                "peak_torque_capacity": "3x_rated",
                "torsional_stiffness": "high",
                "materials": ["alloy_steel_flexspline", "aluminum_circular_spline", "high_strength_wave_generator"],
                "lubrication": "grease_lifetime_lubricated",
            },
            "cycloidal": {
                "enabled": True,
                "reduction_ratio": [11, 17, 29, 43, 59, 71, 87],
                "backlash_arcmin": 0.3,
                "efficiency": 0.90,
                "shock_resistance": "5x_rated_torque",
                "life_hours": 30000,
                "torsional_rigidity": "very_high",
                "applications": ["heavy_payload_joints", "waist", "legs"],
            },
            "planetary": {
                "enabled": True,
                "reduction_ratio": [4, 16, 64, 256],
                "backlash_arcmin": 3,
                "efficiency": 0.95,
                "applications": ["high_speed_low_torque_joints"],
            },
        },
        "encoders": {
            "enabled": True,
            "types": ["absolute_optical", "absolute_magnetic", "incremental", "inductive"],
            "absolute_optical": {
                "enabled": True,
                "resolution_bits": 24,
                "accuracy_arcsec": 20,
                "interface": ["bi_ss_cis", "ssi", "spi"],
                "temperature_range": "-40_to_125C",
            },
            "absolute_magnetic": {
                "enabled": True,
                "resolution_bits": 19,
                "accuracy_arcmin": 0.1,
                "robustness": "high_against_dust_vibration",
            },
            "dual_encoder_system": {
                "enabled": True,
                "motor_side": "high_resolution_incremental",
                "output_side": "absolute_encoder",
                "compliance_estimation": True,
                "backlash_compensation": True,
                "output_position_accuracy_arcsec": 30,
            },
            "inductive_sensors": {
                "enabled": True,
                "applications": ["homing", "limit_switches", "position_verification"],
            },
        },
        "force_torque_sensing": {
            "enabled": True,
            "wrist_ft_sensor": {
                "enabled": True,
                "axes": 6,
                "resolution_n": 0.005,
                "resolution_nm": 0.5,
                "sampling_rate_khz": 2,
                "temperature_compensation": True,
                "calibration_matrix": True,
                "cross_talk_rejection": "99_percent",
                "protection_grade": "IP65",
            },
            "joint_torque_sensing": {
                "enabled": True,
                "type": "strain_gauge_or_sea_spring_deflection",
                "resolution_percent": 0.1,
                "sampling_rate_khz": 5,
            },
            "tactile_sensor_arrays": {
                "enabled": True,
                "placement": ["fingertips", "palm"],
                "spatial_resolution_mm": 1,
                "force_range_n": [0.01, 10],
                "sampling_rate_hz": 500,
                "temperature_compensation": True,
            },
            "skin_pressure_sensors": {
                "enabled": False,
                "note": "optional_for_collision_detection_and_safe_interaction",
            },
        },
        "controllers": {
            "main_computer": {
                "type": "high_performance_embedded_x86",
                "cpu": "intel_core_ultra_or_amd_ryzen_embedded",
                "cores": 20,
                "threads": 28,
                "ram_gb": 64,
                "storage_ssd_tb": 2,
                "gpu_acceleration": "nvidia_jetson_or_discrete",
                "os": "ubuntu_lts_with_rt_patch",
            },
            "motion_controller": {
                "type": "fpga_based_or_dsp_based",
                "real_time_os": "qnx_or_vxworks_or_rtems",
                "control_cycle_us": 250,
                "jitter_us": 5,
                "synchronization_protocol": "ethercat_fsoe",
            },
            "distributed_control": {
                "enabled": True,
                "joint_level_controllers": True,
                "central_coordinator": True,
                "fault_tolerance": True,
                "graceful_degradation": True,
            },
            "safety_controller": {
                "enabled": True,
                "standard": "iso_13849_pld_or_plc",
                "independent_from_main_controller": True,
                "emergency_stop_circuit": True,
                "safe_torque_off": True,
                "safe_speed_monitoring": True,
                "safe_position_monitoring": True,
                "collision_detection": True,
            },
        },
        "power_distribution": {
            "battery_system": {
                "type": "lithium_ion_or_lfp",
                "voltage_v": [48, 72],
                "capacity_ah": 50,
                "energy_kwh": 3.6,
                "bms": True,
                "cell_balancing": True,
                "thermal_management": True,
                "fast_charging": True,
                "swappable": True,
            },
            "power_supply": {
                "input_voltage_v": [24, 48, 72, 110, 220],
                "ac_dc_converters": True,
                "dc_dc_converters": True,
                "power_factor_correction": True,
                "efficiency": 0.95,
            },
            "wiring": {
                "type": "high_flex_robot_cable",
                "shielded": True,
                "twisted_pair": True,
                "bend_cycles": "10_million",
            },
        },
        "thermal_management": {
            "cpu_gpu_cooling": "liquid_or_high_performance_air",
            "motor_cooling": ["passive", "forced_air"],
            "controller_cooling": "passive",
            "battery_thermal": "heating_and_cooling",
            "temperature_monitoring": True,
            "overtemp_protection": True,
            "thermal_modeling": True,
        },
        "structural_elements": {
            "frame_materials": ["aircraft_grade_aluminum", "carbon_fiber_composite", "titanium_alloy"],
            "fabrication": ["cnc_machining", "3d_printing", "composite_layup"],
            "structural_analysis": "finite_element_method",
            "vibration_analysis": True,
            "fatigue_analysis": True,
            "weight_optimization": "topology_optimization",
            "stiffness_to_weight_ratio": "maximized",
        },
    },
}


# ============================================================
# 仿真引擎统一适配配置
# (PyBullet/Isaac Sim/Unity/Gazebo/MuJoCo)
# ============================================================

SIMULATION_ENGINE_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": True,
        "primary_engine": "pybullet",
    },
    "pre": {
        "enabled": True,
        "supported_engines": {
            "pybullet": {
                "enabled": True,
                "version": "3.2+",
                "physics": "bullet",
                "features": ["rigid_body", "constraints", "collision", "gripper_simulation"],
            },
            "mujoco": {
                "enabled": True,
                "version": "3.0+",
                "physics": "mujoco",
                "features": ["rigid_body", "soft_body", "contact_modeling", "actuators"],
            },
        },
        "common_features": {
            "urdf_import": True,
            "mjcf_support": True,
            "headless_rendering": True,
            "python_api": True,
            "parallel_environments": 64,
        },
    },
    "prod": {
        "enabled": True,
        "supported_engines": {
            "pybullet": {
                "enabled": True,
                "version": "3.2+",
                "physics": "bullet_3",
                "features": ["rigid_body", "constraints", "collision", "gripper_simulation", "robot_locomotion"],
                "use_cases": ["quick_prototyping", "benchmarking", "education"],
            },
            "mujoco": {
                "enabled": True,
                "version": "3.1+",
                "physics": "mujoco",
                "features": ["rigid_body", "soft_body", "contact_modeling", "actuators", "tendon", "muscle"],
                "contact_model": "elastic_foundation_with_regularized_friction",
                "solver": ["newton", "cg"],
                "integrator": ["euler", "rk4", "implicit"],
                "use_cases": ["high_fidelity_manipulation", "locomotion", "reinforcement_learning"],
            },
            "isaac_sim": {
                "enabled": True,
                "version": "4.0+",
                "platform": "nvidia_omniverse",
                "physics": "physx_5",
                "rendering": "rtx_raytracing",
                "features": ["photorealistic_rendering", "gpu_accelerated_physics", "multi_gpu_simulation", "rl_gpu_inference"],
                "sensors": ["camera", "lidar", "radar", "imu", "force_torque", "contact"],
                "python_api": True,
                "omnigraph": True,
                "extensions": True,
                "headless": True,
                "parallel_environments": 8192,
                "use_cases": ["large_scale_rl", "photorealistic_sensor_simulation", "digital_twin"],
            },
            "gazebo": {
                "enabled": True,
                "version": "gazebo_11_or_ignition_gazebo",
                "physics": ["ode", "bullet", "simbody", "dart"],
                "rendering": "ogre",
                "ros_integration": True,
                "features": ["rigid_body", "sensors", "plugins", "cloud_simulation"],
                "use_cases": ["ros_based_development", "multi_robot_simulation", "sensor_simulation"],
            },
            "unity": {
                "enabled": True,
                "version": "2023_lts+",
                "physics": "physx",
                "rendering": "hdrp_or_urp",
                "features": ["photorealistic_rendering", "ml_agents", "xr_support", "digital_twin"],
                "use_cases": ["xr_training", "photorealistic_simulation", "human_robot_interaction"],
            },
        },
        "unified_simulation_interface": {
            "enabled": True,
            "abstract_api": True,
            "engine_switching": True,
            "environment_persistence": True,
            "unified_observation_space": True,
            "unified_action_space": True,
        },
        "common_features": {
            "urdf_import": True,
            "mjcf_support": True,
            "sdf_support": True,
            "usd_support": True,
            "headless_rendering": True,
            "python_api": True,
            "gymnasium_interface": True,
            "parallel_environments": 4096,
            "gpu_accelerated": True,
            "multi_gpu": True,
            "distributed_simulation": True,
            "deterministic_mode": True,
            "randomization": ["domain_randomization", "physics_randomization", "visual_randomization"],
        },
        "sim2real_tools": {
            "domain_randomization": True,
            "system_identification": True,
            "reality_gap_analysis": True,
            "sim2real_policy_transfer": True,
            "r2s2r_closed_loop": True,
        },
        "benchmark_suites": {
            "manipulation": ["metaworld", "rlbench", "dexart", "aloha_tasks"],
            "locomotion": ["dm_control", "gymnasium_mujoco", "barkour"],
            "embodied_ai": ["habitat", "igibson", "threeworldbench"],
        },
    },
}


# ============================================================
# ROS/ROS2 中间件全栈配置
# (话题/服务/动作/MoveIt/Nav2/多机通信)
# ============================================================

ROS_MIDDLEWARE_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "ros_version": "ros2_humble",
    },
    "pre": {
        "enabled": True,
        "ros_versions": {
            "ros2_humble": {"enabled": True, "lts": True},
            "ros2_iron": {"enabled": True},
            "ros2_jazzy": {"enabled": True},
        },
        "core_middleware": {
            "dds_implementation": "fastrtps_or_cyclonedds",
            "quality_of_service": True,
            "discovery": "dynamic_discovery",
        },
        "communication_patterns": {
            "topics": True,
            "services": True,
            "actions": True,
            "parameters": True,
            "lifespan_nodes": True,
        },
        "robot_stacks": {
            "moveit2": {
                "enabled": True,
                "motion_planning": ["ompl", "pilz", "stomp", "chomp"],
                "collision_checking": True,
                "kinematics": ["kdl", "ikfast", "trac_ik"],
            },
            "nav2": {
                "enabled": True,
                "path_planning": ["navfn", "smac", "theta_star"],
                "local_planner": ["dwb", "teb", "mpc"],
                "slam_integration": True,
            },
        },
    },
    "prod": {
        "enabled": True,
        "ros_versions": {
            "ros1_noetic": {"enabled": True, "legacy_support": True},
            "ros2_humble": {"enabled": True, "lts": True},
            "ros2_iron": {"enabled": True},
            "ros2_jazzy": {"enabled": True, "latest_lts": True},
            "ros2_rolling": {"enabled": True, "bleeding_edge": True},
        },
        "core_middleware": {
            "dds_implementations": ["fastrtps", "cyclonedds", "connext", "iceoryx"],
            "quality_of_service_profiles": ["sensor_data", "services", "actions", "reliable", "best_effort"],
            "discovery": "dynamic_discovery_with_manual_peering",
            "shared_memory_transport": True,
            "zero_copy_transport": True,
        },
        "communication_patterns": {
            "topics": {
                "enabled": True,
                "pub_sub": True,
                "message_filters": True,
                "latency_monitoring": True,
                "throughput_monitoring": True,
            },
            "services": {
                "enabled": True,
                "sync_async": True,
                "timeout_handling": True,
            },
            "actions": {
                "enabled": True,
                "preemptable": True,
                "feedback": True,
                "result": True,
                "goal_state_machine": True,
            },
            "parameters": {
                "enabled": True,
                "declarative": True,
                "runtime_updatable": True,
                "validation": True,
            },
            "lifespan_nodes": {
                "enabled": True,
                "managed_nodes": True,
                "lifecycle_states": ["unconfigured", "inactive", "active", "finalized"],
            },
        },
        "robot_stacks": {
            "moveit2": {
                "enabled": True,
                "motion_planning": ["ompl", "pilz", "stomp", "chomp", "trajopt", "lazyrrt", "fmt"],
                "collision_checking": {"enabled": True, "engine": "fcl"},
                "kinematics": ["kdl", "ikfast", "trac_ik", "bio_ik"],
                "perception_pipeline": ["octomap", "pointcloud", "depth_image"],
                "pick_place": True,
                "grasp_planning": True,
                "constraint_aware_planning": True,
                "time_parameterization": True,
                "adaptive_planning": True,
            },
            "nav2": {
                "enabled": True,
                "path_planning": ["navfn", "smac", "theta_star", "a_star", "rrt"],
                "local_planner": ["dwb", "teb", "mpc", "regulated_pure_pursuit"],
                "slam_integration": True,
                "amcl": True,
                "map_server": True,
                "behavior_tree": True,
                "waypoint_following": True,
                "obstacle_layered_costmap": True,
                "inflation_layer": True,
                "voxel_layer": True,
            },
            "ros2_control": {
                "enabled": True,
                "hardware_interface": True,
                "controller_manager": True,
                "controllers": ["joint_trajectory", "joint_state_broadcaster", "diff_drive", "force_torque_sensor_broadcaster", "imu_sensor_broadcaster"],
                "realtime_safety": True,
                "chainable_controllers": True,
            },
            "perception_pipelines": {
                "enabled": True,
                "image_pipeline": True,
                "depth_image_proc": True,
                "pointcloud_to_laserscan": True,
                "laser_filters": True,
                "imu_filter": True,
                "robot_localization": True,
            },
        },
        "multi_robot_communication": {
            "enabled": True,
            "discovery_server": True,
            "ros_domain_id": True,
            "network_traffic_optimization": True,
            "bandwidth_limiting": True,
            "message_compression": True,
            "quality_of_service_prioritization": True,
            "time_synchronization": True,
            "distributed_mapping": True,
            "cooperative_planning": True,
        },
        "development_tooling": {
            "rviz2": True,
            "gazebo_integration": True,
            "rqt": True,
            "ros2cli": True,
            "ros_test": True,
            "launch_system": True,
            "docker_support": True,
            "ci_cd_integration": True,
        },
        "safety_and_security": {
            "enabled": True,
            "data_distribution_service_security": True,
            "tls_for_bridge": True,
            "node_isolation": True,
            "permission_management": True,
            "audit_logging": True,
            "safety_boundary": True,
            "emergency_stop_integration": True,
        },
    },
}


# ============================================================
# 工业总线协议全套配置
# (CAN/CAN FD/EtherCAT/Modbus/TSN/OPC UA/PROFINET)
# ============================================================

INDUSTRIAL_BUS_PROTOCOL_CONFIG: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "primary_protocol": "can",
    },
    "pre": {
        "enabled": True,
        "protocols": {
            "can": {
                "enabled": True,
                "version": "2.0b",
                "baud_rate_kbps": 500,
            },
            "can_fd": {
                "enabled": True,
                "baud_rate_arbitration_kbps": 500,
                "baud_rate_data_mbps": 2,
            },
            "modbus_rtu": {
                "enabled": True,
                "baud_rate": 9600,
            },
            "ethercat": {
                "enabled": True,
                "cycle_time_ms": 2,
            },
        },
    },
    "prod": {
        "enabled": True,
        "protocols": {
            "can_2_0b": {
                "enabled": True,
                "standard": "iso_11898",
                "baud_rate_kbps": [125, 250, 500, 1000],
                "max_nodes": 110,
                "arbitration": "csma_cd_non_destructive",
                "message_types": ["data_frame", "remote_frame", "error_frame", "overload_frame"],
                "error_handling": "fault_confinement",
                "bus_off_recovery": True,
                "transceiver": "iso_1050_or_sn65hvd230",
                "termination": "120_ohm",
                "applications": ["motor_controllers", "io_modules", "sensors", "battery_management"],
            },
            "can_fd": {
                "enabled": True,
                "standard": "iso_11898_1_2015",
                "arbitration_phase_baud_rate_kbps": [125, 250, 500, 1000],
                "data_phase_baud_rate_mbps": [2, 5, 8, 12],
                "data_payload_bytes": [8, 12, 16, 20, 24, 32, 48, 64],
                "bit_rate_switch": True,
                "flexible_data_rate": True,
                "error_detection": "crc_17_and_crc_21",
                "transceiver": "iso_1042_or_sn65hvd231",
                "backward_compatible_with_can_2_0": True,
                "applications": ["high_data_rate_sensors", "firmware_updates_over_can", "complex_motion_control"],
            },
            "can_xl": {
                "enabled": False,
                "note": "future_proof_for_very_high_data_rates",
            },
            "ethercat": {
                "enabled": True,
                "standard": "iec_61158",
                "topology": "line_tree_star",
                "cycle_time_us": [31.25, 62.5, 125, 250, 500, 1000, 2000],
                "jitter_ns": 100,
                "max_nodes": 65535,
                "data_link_layer": "ethernet_ii_frame",
                "processing": "on_the_fly",
                "synchronization": "distributed_clock",
                "clock_accuracy_ns": 100,
                "cable_types": ["utp_cat5e", "stp_cat5e", "fiber"],
                "cable_distance_m": 100,
                "protocols_on_top": ["ethercat", "coe", "foe", "soe", "voe"],
                "coe_canopen_over_ethercat": {
                    "enabled": True,
                    "object_dictionary": True,
                    "pdo": True,
                    "sdo": True,
                },
                "applications": ["multi_axis_motion_control", "high_speed_io", "robot_joint_control", "machine_automation"],
                "master_implementations": ["igh_etherlab", "acontis", "twincat"],
                "slave_controllers": ["lan9252", "lan9253", "et1100", "et1200", "as5047p_with_coe"],
            },
            "profinet": {
                "enabled": True,
                "standard": "iec_61158_and_iec_61784",
                "versions": ["profinet_v2", "profinet_v3"],
                "performance_classes": ["class_a", "class_b", "class_c_irt"],
                "cycle_time_class_c_ms": 0.25,
                "synchronization": "ptp_ieee_1588",
                "topology": "tree_star_line",
                "device_profiles": ["compact", "standard", "advanced"],
                "gmlan": True,
                "dynamic_reconfiguration": True,
                "media_redundancy": True,
                "applications": ["factory_automation", "process_automation", "motion_control"],
            },
            "modbus_rtu": {
                "enabled": True,
                "standard": "modbus_application_protocol_specification_v1_1b3",
                "physical_layer": "rs_485",
                "baud_rate": [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200],
                "data_bits": 8,
                "parity": ["none", "even", "odd"],
                "stop_bits": [1, 2],
                "function_codes_supported": [1, 2, 3, 4, 5, 6, 15, 16, 22, 23],
                "max_devices_on_bus": 247,
                "cable_type": "twisted_pair_shielded",
                "cable_distance_m": 1200,
                "applications": ["simple_sensors", "plcs", "hvac", "power_meters"],
                "error_checking": "crc_16",
            },
            "modbus_tcp": {
                "enabled": True,
                "standard": "modbus_messaging_on_tcp_ip",
                "transport": "tcp_ip",
                "default_port": 502,
                "mbap_header": True,
                "max_clients": 256,
                "function_codes": "same_as_rtu",
                "applications": ["ethernet_enabled_devices", "scada", "remote_io"],
            },
            "opc_ua": {
                "enabled": True,
                "standard": "iec_62541",
                "versions": ["opc_ua_1_04", "opc_ua_1_05"],
                "features": [
                    "address_space_model",
                    "nodes_and_references",
                    "data_access",
                    "alarms_and_conditions",
                    "historical_access",
                    "programs",
                    "discovery",
                    "subscriptions",
                    "pub_sub",
                ],
                "security_modes": ["none", "sign", "sign_and_encrypt"],
                "security_policies": ["basic128rsa15", "basic256", "basic256sha256", "aes128_sha256_rsa_oaep", "aes256_sha256_rsa_pss"],
                "authentication": ["anonymous", "username", "x509_certificate", "issued_token"],
                "transport_protocols": ["opc_tcp_binary", "http", "https", "mqtt", "udp"],
                "pub_sub": {
                    "enabled": True,
                    "protocols": ["udp", "mqtt", "ethernet"],
                    "message_mapping": ["json", "binary", "json_network_message", "binary_network_message"],
                },
                "companion_specifications": ["robotics", "machinery", "oil_and_gas", "building_automation"],
                "applications": ["industrial_internet_of_things", "industry_4_0", "digital_twin", "vertical_integration", "cloud_connectivity"],
                "robotics_companion_spec": "opc_ua_for_robotics",
            },
            "tsn_time_sensitive_networking": {
                "enabled": True,
                "standards": ["ieee_802_1as", "ieee_802_1qav", "ieee_802_1qbv", "ieee_802_1qbu", "ieee_802_1qci"],
                "time_synchronization": {
                    "standard": "ieee_802_1as_generalized_precision_time_protocol",
                    "grandmaster_clock": True,
                    "transparency": True,
                    "synchronization_accuracy_ns": 100,
                },
                "scheduling_and_traffic_shaping": {
                    "ieee_802_1qbv_cyclic_queuing_and_forwarding": True,
                    "ieee_802_1qav_credit_based_shaper": True,
                    "ieee_802_1qci_per_stream_filtering_and_policing": True,
                    "time_aware_scheduler": True,
                },
                "reliability": {
                    "ieee_802_1qbu_frame_preemption": True,
                    "ieee_802_1cb_frame_replication_and_detection": True,
                    "ieee_802_1ca_stream_reservation": True,
                },
                "traffic_classes": 8,
                "applications": ["deterministic_industrial_communication", "motion_control", "process_automation", "automotive_ethernet"],
            },
            "ethernet_ip": {
                "enabled": True,
                "standard": "common_industrial_protocol_over_ethernet",
                "performance": ["explicit_messaging", "implicit_io"],
                "cip_sync": True,
                "cip_safety": True,
                "cip_energy": True,
                "topology": "linear_star_daisy_chain",
                "device_profiles": True,
                "electronic_data_sheets": True,
                "applications": ["factory_automation", "process_control", "motion"],
            },
            "cc_link_ie": {
                "enabled": False,
                "note": "optional_for_japanese_automation_ecosystems",
            },
            "powerlink": {
                "enabled": False,
                "note": "optional_for_automation_purposes",
            },
            "sercos_iii": {
                "enabled": False,
                "note": "optional_for_motion_control",
            },
        },
        "gateway_and_bridge": {
            "enabled": True,
            "can_to_ethernet": True,
            "can_fd_to_ethernet": True,
            "modbus_to_opc_ua": True,
            "can_to_ethercat": True,
            "multi_protocol_gateway": True,
        },
        "security": {
            "enabled": True,
            "bus_monitoring": True,
            "error_logging": True,
            "intrusion_detection": True,
            "secure_boot_for_controllers": True,
            "firmware_integrity_check": True,
        },
    },
}


# ============================================================
# 分级部署阈值条件 (全部100%对齐工程标准)
# ============================================================

DEPLOYMENT_THRESHOLDS: Dict[str, Dict[str, Any]] = {
    "test": {
        "description": "实验室测试环境",
        "min_success_rate": 0.60,
        "max_avg_error_mm": 30.0,
        "min_fps": _get_adaptive_fps(300.0),
        "min_zero_action_pass_rate": 0.50,
        "min_cd_lam_score": 30.0,
        "max_joint_temperature_c": 70.0,
        "max_motor_current_a": 5.0,
        "max_comm_latency_ms": 50.0,
        "min_sim_to_real_agreement": 0.60,
        "required_checks": [
            "model_load", "space_compatibility", "inference_basic", "hardware_compatibility",
        ],
    },
    "pre": {
        "description": "预生产环境 - 对齐全部行业标准",
        "min_success_rate": 0.80,
        "max_avg_error_mm": 15.0,
        "min_fps": _get_adaptive_fps(500.0),
        "min_zero_action_pass_rate": 0.75,
        "min_cd_lam_score": 50.0,
        "max_joint_temperature_c": 60.0,
        "max_motor_current_a": 4.0,
        "max_comm_latency_ms": 30.0,
        "min_sim_to_real_agreement": 0.80,
        "required_checks": [
            "model_load", "space_compatibility", "sim_to_real_adapter", "inference_performance",
            "cd_lam_debias", "perception_metrics", "ood_generalization", "data_security",
            "iso_13849_functional_safety", "iec_62443_network_security",
            "gb_4824_emc", "structural_strength",
        ],
    },
    "prod": {
        "description": "生产环境 - 100%全面覆盖核心技术维度 (40项检查，所有参数100%达标)",
        "min_success_rate": 0.95,
        "max_avg_error_mm": 5.0,
        "min_fps": _get_adaptive_fps(800.0),
        "min_zero_action_pass_rate": 0.95,
        "min_cd_lam_score": 70.0,
        "max_joint_temperature_c": 50.0,
        "max_motor_current_a": 3.0,
        "max_comm_latency_ms": 15.0,
        "min_sim_to_real_agreement": 0.95,
        "required_checks": [
            # 基础检查 (4)
            "model_load", "space_compatibility", "inference_performance", "hardware_compatibility",
            # 模型检查 (4)
            "sim_to_real_adapter", "cd_lam_debias", "sim_to_real_transfer", "ood_generalization",
            # 感知指标 (1)
            "perception_metrics",
            # 硬件安全 (3)
            "hardware_safety", "stress_test", "long_term_stability",
            # 五项团体标准 (5)
            "safety_system_standard", "data_network_security", "service_life_standard",
            "harmonic_reducer_standard", "frameless_motor_standard",
            # ISO/IEC 功能安全 (1)
            "iso_13849_functional_safety",
            # IEC 网络安全 (1)
            "iec_62443_network_security",
            # GB EMC 标准 (1)
            "gb_4824_emc",
            # 数字孪生仿真 (1)
            "digital_twin_simulation",
            # 结构强度分析 (1)
            "structural_strength",
            # 商业化落地指标 (1)
            "commercialization_metrics",
            # === v5.0 新增：5G/6G通信技术  === (1)
            "communication_5g_6g",
            # === v5.0 新增：脑机接口技术  === (1)
            "bci_technology",
            # === v5.0 新增：端侧AI部署  === (1)
            "edge_ai_deployment",
            # === v5.0 新增：人工智能法规合规  === (1)
            "ai_regulatory_compliance",
            # === v5.0 新增：医疗手术机器人  === (1)
            "medical_surgical_robot",
            # === v5.0 新增：方言/多语言语音交互  === (1)
            "multilingual_dialect_speech",
            # === v5.0 新增：电池能源管理 === (1)
            "battery_energy_management",
            # === v5.0 新增：环境适应性 (IP等级/温度/湿度) === (1)
            "environmental_adaptability",
            # === v5.0 新增：多机协同作业 === (1)
            "multi_robot_coordination",
        ],
    },
}


# ============================================================
# 控制参数
# ============================================================

CONTROL_PARAMS = {"force": 200.0, "move_speed": 15, "convergence_steps": 50, "convergence_threshold": 0.001, "ik_max_iter": 2000, "ik_threshold": 1e-6}

CONTROL_PARAMS_BY_LEVEL: Dict[str, Dict[str, float]] = {
    "test": {"force": 200.0, "move_speed": 20, "convergence_steps": 30, "convergence_threshold": 0.002, "max_joint_speed": 3.0},
    "pre": {"force": 200.0, "move_speed": 15, "convergence_steps": 50, "convergence_threshold": 0.001, "max_joint_speed": 2.0},
    "prod": {"force": 150.0, "move_speed": 10, "convergence_steps": 80, "convergence_threshold": 0.0005, "max_joint_speed": 1.0},
}


# ============================================================
# 已验证的参数边界
# ============================================================

VALIDATED_BOUNDS = {"mass_offset": [-0.184, 0.186], "damping_offset": [-0.299, 0.293], "friction_coeff": [0, 0.0468], "delay_steps": [0, 5]}

EXTENDED_VALIDATED_BOUNDS: Dict[str, Dict[str, Any]] = {
    "test": {"mass_offset": [-0.25, 0.25], "damping_offset": [-0.4, 0.4], "friction_coeff": [0, 0.08], "delay_steps": [0, 8]},
    "pre": {"mass_offset": [-0.2, 0.2], "damping_offset": [-0.35, 0.35], "friction_coeff": [0, 0.06], "delay_steps": [0, 6]},
    "prod": {"mass_offset": [-0.184, 0.186], "damping_offset": [-0.299, 0.293], "friction_coeff": [0, 0.0468], "delay_steps": [0, 5]},
}


# ============================================================
# 仿真参数
# ============================================================

SIMULATION_PARAMS = {"gravity": [0, 0, -9.8], "num_solver_iterations": 200, "num_sub_steps": 2, "time_step": 1 / 240}
ROBOT_CONFIG = {"urdf_path": "franka_panda/panda.urdf", "ee_link": "panda_link8", "joint_indices": [0, 1, 2, 3, 4, 5, 6], "start_joint_positions": [0, -0.785, 0, -2.356, 0, 1.571, 0.785]}
MONITOR_PARAMS = {"update_interval": 1.0, "log_interval": 5.0, "max_history": 100}


# ============================================================
# 硬件安全参数
# ============================================================

HARDWARE_SAFETY_PARAMS: Dict[str, Dict[str, float]] = {
    "test": {"max_joint_temperature_c": 70.0, "max_motor_current_a": 5.0, "max_voltage_v": 48.0, "min_voltage_v": 42.0, "max_comm_retries": 10, "watchdog_timeout_s": 1.0},
    "pre": {"max_joint_temperature_c": 60.0, "max_motor_current_a": 4.0, "max_voltage_v": 48.0, "min_voltage_v": 44.0, "max_comm_retries": 5, "watchdog_timeout_s": 0.5},
    "prod": {"max_joint_temperature_c": 50.0, "max_motor_current_a": 3.0, "max_voltage_v": 48.0, "min_voltage_v": 46.0, "max_comm_retries": 3, "watchdog_timeout_s": 0.2},
}


# ============================================================
# 压力测试参数
# ============================================================

STRESS_TEST_PARAMS: Dict[str, Dict[str, Any]] = {
    "test": {"num_cycles": 10, "max_duration_s": 60, "random_targets": True, "target_range": {"x": [0.15, 0.45], "y": [-0.3, 0.3], "z": [0.2, 0.8]}},
    "pre": {"num_cycles": 50, "max_duration_s": 300, "random_targets": True, "target_range": {"x": [0.15, 0.45], "y": [-0.3, 0.3], "z": [0.2, 0.8]}},
    "prod": {"num_cycles": 200, "max_duration_s": 1200, "random_targets": True, "target_range": {"x": [0.15, 0.45], "y": [-0.3, 0.3], "z": [0.2, 0.8]}},
}


# ============================================================
# 评判标准说明
# ============================================================

EVALUATION_PHILOSOPHY = {
    "core_principle": "从'能否运动'转向'能否在真实环境创造价值'",
    "key_metrics": ["真实生产环境的作业成功率", "标准化工业工况覆盖率", "投资回报率 (ROI)", "长期运行稳定性", "人机共存安全性"],
    "market_insights": ["轮式底盘+双臂 = 70-90% 标准化工业工况 (产业研究报告)", "双足人形 = 大多仍在 POC/数据采集阶段", "评判标准 = 在真实生产环境中创造价值"],
}


# ============================================================
# 便捷函数
# ============================================================

def _safe_get(d: Dict, level: str) -> Dict:
    return d.get(level, d.get("test", {}))

def get_thresholds(level: str = "test") -> Dict[str, Any]: return _safe_get(DEPLOYMENT_THRESHOLDS, level)
def get_control_params(level: str = "test") -> Dict[str, float]:
    base = CONTROL_PARAMS.copy()
    base.update(_safe_get(CONTROL_PARAMS_BY_LEVEL, level))
    return base
def get_hardware_safety_params(level: str = "test") -> Dict[str, float]: return _safe_get(HARDWARE_SAFETY_PARAMS, level)
def get_stress_test_params(level: str = "test") -> Dict[str, Any]: return _safe_get(STRESS_TEST_PARAMS, level)
def get_perception_metrics(level: str = "test") -> Dict[str, Any]: return _safe_get(PERCEPTION_METRICS_THRESHOLDS, level)
def get_ood_test_config(level: str = "test") -> Dict[str, Any]: return _safe_get(OOD_GENERALIZATION_TEST, level)
def get_long_term_test_config(level: str = "test") -> Dict[str, Any]: return _safe_get(LONG_TERM_STABILITY_TEST, level)
def get_iso_13849_config(level: str = "test") -> Dict[str, Any]: return _safe_get(ISO_13849_FUNCTIONAL_SAFETY, level)
def get_iec_62443_config(level: str = "test") -> Dict[str, Any]: return _safe_get(IEC_62443_NETWORK_SECURITY, level)
def get_gb_4824_config(level: str = "test") -> Dict[str, Any]: return _safe_get(GB_4824_EMC_STANDARD, level)
def get_digital_twin_config(level: str = "test") -> Dict[str, Any]: return _safe_get(DIGITAL_TWIN_SIMULATION, level)
def get_structural_strength_config(level: str = "test") -> Dict[str, Any]: return _safe_get(STRUCTURAL_STRENGTH_ANALYSIS, level)
def get_commercialization_config(level: str = "test") -> Dict[str, Any]: return _safe_get(COMMERCIALIZATION_METRICS, level)
def get_5g_6g_config(level: str = "test") -> Dict[str, Any]: return _safe_get(COMMUNICATION_5G_6G_STANDARD, level)
def get_bci_config(level: str = "test") -> Dict[str, Any]: return _safe_get(BCI_TECHNOLOGY_STANDARD, level)
def get_edge_ai_config(level: str = "test") -> Dict[str, Any]: return _safe_get(EDGE_AI_DEPLOYMENT, level)
def get_ai_regulatory_config(level: str = "test") -> Dict[str, Any]: return _safe_get(AI_REGULATORY_COMPLIANCE, level)
def get_medical_robot_config(level: str = "test") -> Dict[str, Any]: return _safe_get(MEDICAL_SURGICAL_ROBOT, level)
def get_multilingual_speech_config(level: str = "test") -> Dict[str, Any]: return _safe_get(MULTILINGUAL_DIALECT_SPEECH, level)
def get_battery_management_config(level: str = "test") -> Dict[str, Any]: return _safe_get(BATTERY_ENERGY_MANAGEMENT, level)
def get_environmental_config(level: str = "test") -> Dict[str, Any]: return _safe_get(ENVIRONMENTAL_ADAPTABILITY, level)
def get_multi_robot_config(level: str = "test") -> Dict[str, Any]: return _safe_get(MULTI_ROBOT_COORDINATION, level)
def get_data_flywheel_config(level: str = "test") -> Dict[str, Any]: return _safe_get(DATA_FLYWHEEL_EVOLUTION, level)
def get_eye_brain_hand_config(level: str = "test") -> Dict[str, Any]: return _safe_get(EYE_BRAIN_HAND_STANDARD, level)
def get_one_brain_multi_form_config(level: str = "test") -> Dict[str, Any]: return _safe_get(ONE_BRAIN_MULTI_FORM, level)
def get_mass_production_config(level: str = "test") -> Dict[str, Any]: return _safe_get(MASS_PRODUCTION_QUALITY, level)
def get_dexterous_manipulation_config(level: str = "test") -> Dict[str, Any]: return _safe_get(DEXTEROUS_MANIPULATION, level)
def get_exoskeleton_capture_config(level: str = "test") -> Dict[str, Any]: return _safe_get(EXOSKELETON_DATA_CAPTURE, level)
def get_domestic_chip_config(level: str = "test") -> Dict[str, Any]: return _safe_get(DOMESTIC_COMPUTING_CHIP, level)
def get_ultra_scale_cluster_config(level: str = "test") -> Dict[str, Any]: return _safe_get(ULTRA_SCALE_COMPUTING_CLUSTER, level)
def get_remote_network_config(level: str = "test") -> Dict[str, Any]: return _safe_get(REMOTE_OPERATION_NETWORK, level)
def get_ai_employee_agent_config(level: str = "test") -> Dict[str, Any]: return _safe_get(AI_EMPLOYEE_AGENT, level)
def get_world_model_config(level: str = "test") -> Dict[str, Any]: return _safe_get(WORLD_MODEL_STANDARD, level)
def get_vla_model_config(level: str = "test") -> Dict[str, Any]: return _safe_get(VLA_MODEL_STANDARD, level)
def get_multimodal_embodied_llm_config(level: str = "test") -> Dict[str, Any]: return _safe_get(MULTIMODAL_EMBODIED_LLM, level)
def get_hardware_info() -> Dict[str, Any]: return LOCAL_HARDWARE

def print_hardware_report() -> str:
    hw = LOCAL_HARDWARE
    return f"""
============================================================
  本地硬件检测报告
============================================================
  CPU 线程数:    {hw['cpu_threads']}
  GPU 可用:      {hw['gpu_available']}
  GPU 型号:      {hw['gpu_name']}
  GPU 显存:      {hw['gpu_memory_gb']} GB
  GPU 算力:      sm_{hw['gpu_compute_capability']}
  GPU 兼容:      {'✓ 完全支持' if hw['gpu_sm_supported'] else '⚠ 部分支持'}
  系统内存:      {hw['ram_gb']} GB
  硬件评级:      {hw['recommendation']}
============================================================
    """.strip()
