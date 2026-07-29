"""
部署适配参数固化配置 (v3.0 行业标准升级)
基于 v3 版本 100% 通过验证的参数

升级内容 (v3.0):
- 整合 WAIC 2026 行业标准：12项多模态感知指标
- 对齐人形机器人五项团体标准 (2026年中发布)
- 新增 OOD (分布外) 泛化测试配置
- 新增长期稳定性测试配置
- 新增本地硬件能力自动检测 (CPU/GPU/内存)
- 新增 GPU 兼容性检测 (RTX 5070 Ti sm_120)
- 新增数据安全与网络安全检查项
- 评判标准从"静态参数"转向"动态行为仿真+真实价值创造"

升级内容 (v2.0):
- 新增三级部署条件 (测试/预生产/生产)
- 新增真实硬件验证指标 (温度/电流/通信延迟)
- 新增 Sim-to-Real 迁移一致性验证
- CD-LAM 因果去偏纳入强制条件
"""

from typing import Dict, Any, Optional
import os


# ============================================================
# 部署等级定义
# ============================================================

DEPLOYMENT_LEVELS = {
    "TEST": "test",           # 实验室测试: 宽松条件, 快速验证
    "PRE_PRODUCTION": "pre",  # 预生产: 中等条件, 模拟真实
    "PRODUCTION": "prod",     # 生产环境: 严格条件, 高可靠性
}

DEFAULT_DEPLOYMENT_LEVEL = "TEST"

# ============================================================
# 本地硬件能力检测 (自动适配)
# ============================================================

def detect_local_hardware() -> Dict[str, Any]:
    """自动检测本地硬件能力，用于自适应部署阈值

    Returns:
        硬件能力信息字典
    """
    info = {
        "cpu_cores": 4,
        "cpu_threads": 4,
        "gpu_available": False,
        "gpu_name": "None",
        "gpu_memory_gb": 0.0,
        "gpu_compute_capability": "0.0",
        "gpu_sm_supported": False,
        "ram_gb": 8.0,
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

            # 检查 PyTorch 是否支持该算力 (通过实际运行CUDA操作来验证)
            try:
                test_tensor = torch.randn(8, 8, device='cuda', dtype=torch.float16)
                _ = test_tensor @ test_tensor
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
            kernel32 = ctypes.windll.kernel32
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong),
                            ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong)]
            ms = MEMORYSTATUSEX()
            ms.dwLength = ctypes.sizeof(ms)
            kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
            info["ram_gb"] = round(ms.ullTotalPhys / 1024**3, 1)
        except Exception:
            pass

    # 给出硬件能力评级
    score = 0
    if info["cpu_threads"] >= 16: score += 2
    elif info["cpu_threads"] >= 8: score += 1
    if info["gpu_available"] and info["gpu_memory_gb"] >= 12: score += 2
    elif info["gpu_available"] and info["gpu_memory_gb"] >= 6: score += 1
    if info["ram_gb"] >= 32: score += 2
    elif info["ram_gb"] >= 16: score += 1

    if score >= 5:
        info["recommendation"] = "high_end"
    elif score >= 3:
        info["recommendation"] = "mid_range"
    elif score >= 1:
        info["recommendation"] = "entry_level"
    else:
        info["recommendation"] = "minimal"

    return info


LOCAL_HARDWARE = detect_local_hardware()


# ============================================================
# 硬件自适应 FPS 阈值
# ============================================================

def _get_adaptive_fps(base_fps: float) -> float:
    """根据本地硬件能力自适应调整 FPS 阈值

    Args:
        base_fps: 基础 FPS 阈值

    Returns:
        调整后的 FPS 阈值
    """
    hw = LOCAL_HARDWARE
    if hw["recommendation"] == "high_end":
        return base_fps * 1.3
    elif hw["recommendation"] == "mid_range":
        return base_fps * 1.0
    elif hw["recommendation"] == "entry_level":
        return base_fps * 0.7
    else:
        return base_fps * 0.5


# ============================================================
# 12项多模态感知指标 (行业标准)
# ============================================================

PERCEPTION_METRICS_THRESHOLDS: Dict[str, Dict[str, Any]] = {
    "test": {
        "visual_localization_accuracy_mm": 10.0,      # 视觉定位精度 ≤10mm
        "target_recognition_robustness": 0.70,          # 目标识别鲁棒性 ≥70%
        "depth_perception_accuracy_mm": 20.0,           # 深度感知精度 ≤20mm
        "voice_false_trigger_rate_per_hour": 5.0,        # 语音误触发率 ≤5次/小时
        "multi_turn_dialog_accuracy": 0.60,               # 多轮对话准确率 ≥60%
        "emotion_recognition_accuracy": 0.50,             # 情感识别准确率 ≥50%
        "force_control_response_latency_ms": 200.0,       # 力控响应延迟 ≤200ms
        "contact_force_accuracy_n": 5.0,                   # 接触力控制精度 ≤5N
        "compliant_control_stability": 0.70,               # 柔顺控制稳定性 ≥70%
        "sensor_fusion_latency_ms": 300.0,                 # 多传感器融合延迟 ≤300ms
        "abnormal_response_time_s": 2.0,                    # 异常工况响应时间 ≤2s
        "autonomous_decision_confidence": 0.60,             # 自主决策可信度 ≥60%
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
        "visual_localization_accuracy_mm": 2.0,       # 对齐 JAKA K1-25 的 ±0.05mm 精度方向
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
# 人形机器人五项团体标准对齐 (2026年中发布)
# ============================================================

FIVE_STANDARDS_CHECK: Dict[str, Dict[str, Any]] = {
    "safety_system": {
        "description": "安全系统标准 (碰撞/跌倒/电气/功能安全)",
        "required_checks": [
            "collision_detection",      # 碰撞安全检测
            "fall_protection",          # 跌倒保护
            "electrical_safety",        # 电气安全
            "functional_safety",        # 功能安全 (ISO 13849)
        ],
    },
    "data_network_security": {
        "description": "数据网络安全标准 (对齐 IEC 62443-3-3)",
        "required_checks": [
            "data_encryption",          # 数据加密
            "privacy_protection",       # 用户隐私保护
            "biometric_data_security",  # 生物特征数据安全
            "remote_control_security",  # 远程控制安全通信
            "secure_boot",              # 安全启动
        ],
    },
    "service_life": {
        "description": "使用寿命标准",
        "required_checks": [
            "accelerated_aging_test",   # 加速老化试验
            "fatigue_life_test",        # 疲劳寿命测试
            "component_reliability",    # 关键部件可靠性评估
        ],
    },
    "harmonic_reducer": {
        "description": "谐波减速器标准",
        "required_checks": [
            "reducer_efficiency",       # 减速器效率
            "reducer_backlash",         # 减速器回程间隙
            "reducer_life",             # 减速器寿命
        ],
    },
    "frameless_torque_motor": {
        "description": "无框力矩电机标准",
        "required_checks": [
            "motor_torque_density",     # 电机转矩密度
            "motor_cogging_torque",     # 电机齿槽转矩
            "motor_efficiency",         # 电机效率
        ],
    },
}


# ============================================================
# OOD (分布外) 泛化测试配置
# ============================================================

OOD_GENERALIZATION_TEST: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": True,
        "extreme_conditions": [
            "low_light",           # 低光照
            "partial_occlusion",   # 部分遮挡
            "background_noise",    # 背景噪声
        ],
        "min_ood_success_rate": 0.40,      # OOD 场景成功率 ≥40%
        "max_performance_drop": 0.40,       # 性能下降 ≤40%
        "safety_degradation_enabled": True, # 是否启用安全降级策略
    },
    "pre": {
        "enabled": True,
        "extreme_conditions": [
            "low_light",
            "partial_occlusion",
            "background_noise",
            "unseen_objects",      # 未见物体
            "lighting_change",     # 光照突变
        ],
        "min_ood_success_rate": 0.65,
        "max_performance_drop": 0.25,
        "safety_degradation_enabled": True,
    },
    "prod": {
        "enabled": True,
        "extreme_conditions": [
            "low_light",
            "partial_occlusion",
            "background_noise",
            "unseen_objects",
            "lighting_change",
            "dynamic_obstacles",   # 动态障碍物
            "sensor_failure",      # 传感器故障模拟
            "adversarial_inputs",  # 对抗样本
        ],
        "min_ood_success_rate": 0.85,
        "max_performance_drop": 0.15,
        "safety_degradation_enabled": True,
    },
}


# ============================================================
# 长期稳定性测试配置
# ============================================================

LONG_TERM_STABILITY_TEST: Dict[str, Dict[str, Any]] = {
    "test": {
        "enabled": False,
        "duration_hours": 2,
        "continuous_operation": True,
        "max_performance_drift": 0.20,        # 性能漂移 ≤20%
        "check_memory_leak": False,
        "check_model_degradation": False,
    },
    "pre": {
        "enabled": True,
        "duration_hours": 8,
        "continuous_operation": True,
        "max_performance_drift": 0.10,
        "check_memory_leak": True,
        "check_model_degradation": True,
    },
    "prod": {
        "enabled": True,
        "duration_hours": 72,                  # 72小时连续运行
        "continuous_operation": True,
        "max_performance_drift": 0.05,         # 性能漂移 ≤5%
        "check_memory_leak": True,
        "check_model_degradation": True,
        "check_behavior_anomaly": True,        # 行为异常检测
        "auto_restart_on_failure": True,       # 失败自动重启
        "max_restarts": 3,                       # 最大重启次数
    },
}


# ============================================================
# 分级部署阈值条件 (硬件自适应增强版)
# ============================================================

DEPLOYMENT_THRESHOLDS: Dict[str, Dict[str, Any]] = {
    "test": {
        "description": "实验室测试环境 - 快速验证模型功能",
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
            "model_load",
            "space_compatibility",
            "inference_basic",
            "hardware_compatibility",   # 新增: 硬件兼容性检测
        ],
    },
    "pre": {
        "description": "预生产环境 - 模拟真实场景验证",
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
            "model_load",
            "space_compatibility",
            "sim_to_real_adapter",
            "inference_performance",
            "cd_lam_debias",
            "perception_metrics",         # 新增: 12项感知指标
            "ood_generalization",         # 新增: OOD泛化测试
            "data_security",              # 新增: 数据网络安全
        ],
    },
    "prod": {
        "description": "生产环境 - 高可靠性要求 (对齐行业标准)",
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
            "model_load",
            "space_compatibility",
            "sim_to_real_adapter",
            "inference_performance",
            "cd_lam_debias",
            "hardware_safety",
            "sim_to_real_transfer",
            "stress_test",
            "perception_metrics",         # 12项感知指标全通过
            "ood_generalization",         # OOD泛化能力
            "long_term_stability",        # 新增: 长期稳定性
            "safety_system_standard",     # 新增: 五项团体标准-安全系统
            "data_network_security",      # 新增: 五项团体标准-数据安全
            "service_life_standard",      # 新增: 五项团体标准-使用寿命
            "hardware_compatibility",     # GPU/CPU兼容性
        ],
    },
}


# ============================================================
# 控制参数 (保持向后兼容)
# ============================================================

CONTROL_PARAMS = {
    "force": 200.0,
    "move_speed": 15,
    "convergence_steps": 50,
    "convergence_threshold": 0.001,
    "ik_max_iter": 2000,
    "ik_threshold": 1e-6,
}

CONTROL_PARAMS_BY_LEVEL: Dict[str, Dict[str, float]] = {
    "test": {
        "force": 200.0,
        "move_speed": 20,
        "convergence_steps": 30,
        "convergence_threshold": 0.002,
        "max_joint_speed": 3.0,
    },
    "pre": {
        "force": 200.0,
        "move_speed": 15,
        "convergence_steps": 50,
        "convergence_threshold": 0.001,
        "max_joint_speed": 2.0,
    },
    "prod": {
        "force": 150.0,
        "move_speed": 10,
        "convergence_steps": 80,
        "convergence_threshold": 0.0005,
        "max_joint_speed": 1.0,
    },
}


# ============================================================
# 已验证的参数边界
# ============================================================

VALIDATED_BOUNDS = {
    "mass_offset": [-0.184, 0.186],
    "damping_offset": [-0.299, 0.293],
    "friction_coeff": [0, 0.0468],
    "delay_steps": [0, 5],
}

EXTENDED_VALIDATED_BOUNDS: Dict[str, Dict[str, Any]] = {
    "test": {
        "mass_offset": [-0.25, 0.25],
        "damping_offset": [-0.4, 0.4],
        "friction_coeff": [0, 0.08],
        "delay_steps": [0, 8],
        "sensor_noise_level": "high",
    },
    "pre": {
        "mass_offset": [-0.2, 0.2],
        "damping_offset": [-0.35, 0.35],
        "friction_coeff": [0, 0.06],
        "delay_steps": [0, 6],
        "sensor_noise_level": "medium",
    },
    "prod": {
        "mass_offset": [-0.184, 0.186],
        "damping_offset": [-0.299, 0.293],
        "friction_coeff": [0, 0.0468],
        "delay_steps": [0, 5],
        "sensor_noise_level": "low",
    },
}


# ============================================================
# 仿真参数
# ============================================================

SIMULATION_PARAMS = {
    "gravity": [0, 0, -9.8],
    "num_solver_iterations": 200,
    "num_sub_steps": 2,
    "time_step": 1 / 240,
}

ROBOT_CONFIG = {
    "urdf_path": "franka_panda/panda.urdf",
    "ee_link": "panda_link8",
    "joint_indices": [0, 1, 2, 3, 4, 5, 6],
    "start_joint_positions": [0, -0.785, 0, -2.356, 0, 1.571, 0.785],
}

MONITOR_PARAMS = {
    "update_interval": 1.0,
    "log_interval": 5.0,
    "max_history": 100,
}


# ============================================================
# 硬件安全参数
# ============================================================

HARDWARE_SAFETY_PARAMS: Dict[str, Dict[str, float]] = {
    "test": {
        "max_joint_temperature_c": 70.0,
        "max_motor_current_a": 5.0,
        "max_voltage_v": 48.0,
        "min_voltage_v": 42.0,
        "max_comm_retries": 10,
        "watchdog_timeout_s": 1.0,
    },
    "pre": {
        "max_joint_temperature_c": 60.0,
        "max_motor_current_a": 4.0,
        "max_voltage_v": 48.0,
        "min_voltage_v": 44.0,
        "max_comm_retries": 5,
        "watchdog_timeout_s": 0.5,
    },
    "prod": {
        "max_joint_temperature_c": 50.0,
        "max_motor_current_a": 3.0,
        "max_voltage_v": 48.0,
        "min_voltage_v": 46.0,
        "max_comm_retries": 3,
        "watchdog_timeout_s": 0.2,
    },
}


# ============================================================
# 压力测试参数
# ============================================================

STRESS_TEST_PARAMS: Dict[str, Dict[str, Any]] = {
    "test": {
        "num_cycles": 10,
        "max_duration_s": 60,
        "random_targets": True,
        "target_range": {"x": [0.15, 0.45], "y": [-0.3, 0.3], "z": [0.2, 0.8]},
    },
    "pre": {
        "num_cycles": 50,
        "max_duration_s": 300,
        "random_targets": True,
        "target_range": {"x": [0.15, 0.45], "y": [-0.3, 0.3], "z": [0.2, 0.8]},
    },
    "prod": {
        "num_cycles": 200,
        "max_duration_s": 1200,
        "random_targets": True,
        "target_range": {"x": [0.15, 0.45], "y": [-0.3, 0.3], "z": [0.2, 0.8]},
    },
}


# ============================================================
# 评判标准说明 (从静态参数到动态行为仿真)
# ============================================================

EVALUATION_PHILOSOPHY = {
    "core_principle": "从'能否运动'转向'能否在真实环境创造价值'",
    "key_metrics": [
        "真实生产环境的作业成功率",      # 不是展厅跳舞能力
        "标准化工业工况覆盖率",           # 轮式+双臂方案覆盖70-90%
        "投资回报率 (ROI)",               # 能否闭环
        "长期运行稳定性",                 # 不是一次性展示
        "人机共存安全性",                 # 开放动态环境
    ],
    "market_insights": [
        "轮式底盘+双臂 = 70-90% 标准化工业工况 (高盛)",
        "双足人形 = 大多仍在 POC/数据采集阶段",
        "评判标准 = 在真实生产环境中创造价值",
    ],
}


# ============================================================
# 便捷函数
# ============================================================

def get_thresholds(level: str = "test") -> Dict[str, Any]:
    if level not in DEPLOYMENT_THRESHOLDS:
        level = DEFAULT_DEPLOYMENT_LEVEL
    return DEPLOYMENT_THRESHOLDS[level]


def get_control_params(level: str = "test") -> Dict[str, float]:
    base = CONTROL_PARAMS.copy()
    if level in CONTROL_PARAMS_BY_LEVEL:
        base.update(CONTROL_PARAMS_BY_LEVEL[level])
    return base


def get_hardware_safety_params(level: str = "test") -> Dict[str, float]:
    if level not in HARDWARE_SAFETY_PARAMS:
        level = DEFAULT_DEPLOYMENT_LEVEL
    return HARDWARE_SAFETY_PARAMS[level]


def get_stress_test_params(level: str = "test") -> Dict[str, Any]:
    if level not in STRESS_TEST_PARAMS:
        level = DEFAULT_DEPLOYMENT_LEVEL
    return STRESS_TEST_PARAMS[level]


def get_perception_metrics(level: str = "test") -> Dict[str, Any]:
    """获取12项多模态感知指标阈值"""
    if level not in PERCEPTION_METRICS_THRESHOLDS:
        level = DEFAULT_DEPLOYMENT_LEVEL
    return PERCEPTION_METRICS_THRESHOLDS[level]


def get_ood_test_config(level: str = "test") -> Dict[str, Any]:
    """获取OOD泛化测试配置"""
    if level not in OOD_GENERALIZATION_TEST:
        level = DEFAULT_DEPLOYMENT_LEVEL
    return OOD_GENERALIZATION_TEST[level]


def get_long_term_test_config(level: str = "test") -> Dict[str, Any]:
    """获取长期稳定性测试配置"""
    if level not in LONG_TERM_STABILITY_TEST:
        level = DEFAULT_DEPLOYMENT_LEVEL
    return LONG_TERM_STABILITY_TEST[level]


def get_hardware_info() -> Dict[str, Any]:
    """获取本地硬件检测结果"""
    return LOCAL_HARDWARE


def print_hardware_report() -> str:
    """打印硬件检测报告"""
    hw = LOCAL_HARDWARE
    report = f"""
============================================================
  本地硬件检测报告
============================================================
  CPU 线程数:    {hw['cpu_threads']}
  GPU 可用:      {hw['gpu_available']}
  GPU 型号:      {hw['gpu_name']}
  GPU 显存:      {hw['gpu_memory_gb']} GB
  GPU 算力:      sm_{hw['gpu_compute_capability']}
  GPU 兼容:      {'✓ 完全支持' if hw['gpu_sm_supported'] else '⚠ 部分支持 (建议升级PyTorch)'}
  系统内存:      {hw['ram_gb']} GB
  硬件评级:      {hw['recommendation']}
============================================================
    """.strip()
    return report
