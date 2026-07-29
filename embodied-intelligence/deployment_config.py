"""
部署适配参数固化配置
基于 v3 版本 100% 通过验证的参数

升级内容:
- 新增三级部署条件 (测试/预生产/生产)
- 新增真实硬件验证指标 (温度/电流/通信延迟)
- 新增 Sim-to-Real 迁移一致性验证
- CD-LAM 因果去偏纳入强制条件
"""

from typing import Dict, Any

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
# 分级部署阈值条件
# ============================================================

DEPLOYMENT_THRESHOLDS: Dict[str, Dict[str, Any]] = {
    "test": {
        "description": "实验室测试环境 - 快速验证模型功能",
        "min_success_rate": 0.60,          # 最低成功率 60%
        "max_avg_error_mm": 30.0,           # 最大平均误差 30mm
        "min_fps": 300.0,                    # 最低推理FPS 300
        "min_zero_action_pass_rate": 0.50,   # 零动作通过率 ≥50%
        "min_cd_lam_score": 30.0,             # CD-LAM评分 ≥30
        "max_joint_temperature_c": 70.0,      # 关节最高温度 70°C
        "max_motor_current_a": 5.0,            # 电机最大电流 5A
        "max_comm_latency_ms": 50.0,           # 最大通信延迟 50ms
        "min_sim_to_real_agreement": 0.60,     # 仿真-真实一致性 ≥60%
        "required_checks": [                    # 必过检查项
            "model_load",
            "space_compatibility",
            "inference_basic",
        ],
    },
    "pre": {
        "description": "预生产环境 - 模拟真实场景验证",
        "min_success_rate": 0.80,          # 最低成功率 80%
        "max_avg_error_mm": 15.0,           # 最大平均误差 15mm
        "min_fps": 500.0,                    # 最低推理FPS 500
        "min_zero_action_pass_rate": 0.75,   # 零动作通过率 ≥75%
        "min_cd_lam_score": 50.0,             # CD-LAM评分 ≥50
        "max_joint_temperature_c": 60.0,      # 关节最高温度 60°C
        "max_motor_current_a": 4.0,            # 电机最大电流 4A
        "max_comm_latency_ms": 30.0,           # 最大通信延迟 30ms
        "min_sim_to_real_agreement": 0.80,     # 仿真-真实一致性 ≥80%
        "required_checks": [
            "model_load",
            "space_compatibility",
            "sim_to_real_adapter",
            "inference_performance",
            "cd_lam_debias",
        ],
    },
    "prod": {
        "description": "生产环境 - 高可靠性要求",
        "min_success_rate": 0.95,          # 最低成功率 95%
        "max_avg_error_mm": 5.0,             # 最大平均误差 5mm
        "min_fps": 800.0,                    # 最低推理FPS 800
        "min_zero_action_pass_rate": 0.95,   # 零动作通过率 ≥95%
        "min_cd_lam_score": 70.0,             # CD-LAM评分 ≥70
        "max_joint_temperature_c": 50.0,      # 关节最高温度 50°C
        "max_motor_current_a": 3.0,            # 电机最大电流 3A
        "max_comm_latency_ms": 15.0,           # 最大通信延迟 15ms
        "min_sim_to_real_agreement": 0.95,     # 仿真-真实一致性 ≥95%
        "required_checks": [
            "model_load",
            "space_compatibility",
            "sim_to_real_adapter",
            "inference_performance",
            "cd_lam_debias",
            "hardware_safety",
            "sim_to_real_transfer",
            "stress_test",
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

# ============================================================
# 分级控制参数
# ============================================================

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
# 已验证的参数边界 (保持向后兼容)
# ============================================================

VALIDATED_BOUNDS = {
    "mass_offset": [-0.184, 0.186],
    "damping_offset": [-0.299, 0.293],
    "friction_coeff": [0, 0.0468],
    "delay_steps": [0, 5],
}

# ============================================================
# 扩展验证边界 (按部署等级)
# ============================================================

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

# ============================================================
# 机器人配置
# ============================================================

ROBOT_CONFIG = {
    "urdf_path": "franka_panda/panda.urdf",
    "ee_link": "panda_link8",
    "joint_indices": [0, 1, 2, 3, 4, 5, 6],
    "start_joint_positions": [0, -0.785, 0, -2.356, 0, 1.571, 0.785],
}

# ============================================================
# 监控参数
# ============================================================

MONITOR_PARAMS = {
    "update_interval": 1.0,
    "log_interval": 5.0,
    "max_history": 100,
}

# ============================================================
# 硬件安全参数 (新增)
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
# 压力测试参数 (新增)
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


def get_thresholds(level: str = "test") -> Dict[str, Any]:
    """获取指定部署等级的阈值配置

    Args:
        level: 部署等级 ("test", "pre", "prod")

    Returns:
        该等级的阈值配置字典
    """
    if level not in DEPLOYMENT_THRESHOLDS:
        level = DEFAULT_DEPLOYMENT_LEVEL
    return DEPLOYMENT_THRESHOLDS[level]


def get_control_params(level: str = "test") -> Dict[str, float]:
    """获取指定部署等级的控制参数

    Args:
        level: 部署等级 ("test", "pre", "prod")

    Returns:
        该等级的控制参数字典
    """
    base = CONTROL_PARAMS.copy()
    if level in CONTROL_PARAMS_BY_LEVEL:
        base.update(CONTROL_PARAMS_BY_LEVEL[level])
    return base


def get_hardware_safety_params(level: str = "test") -> Dict[str, float]:
    """获取指定部署等级的硬件安全参数

    Args:
        level: 部署等级 ("test", "pre", "prod")

    Returns:
        该等级的硬件安全参数字典
    """
    if level not in HARDWARE_SAFETY_PARAMS:
        level = DEFAULT_DEPLOYMENT_LEVEL
    return HARDWARE_SAFETY_PARAMS[level]


def get_stress_test_params(level: str = "test") -> Dict[str, Any]:
    """获取指定部署等级的压力测试参数

    Args:
        level: 部署等级 ("test", "pre", "prod")

    Returns:
        该等级的压力测试参数字典
    """
    if level not in STRESS_TEST_PARAMS:
        level = DEFAULT_DEPLOYMENT_LEVEL
    return STRESS_TEST_PARAMS[level]
