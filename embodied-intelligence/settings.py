# ============================================================================
# 具身智能机器人系统 - 全局配置
# 所有硬编码参数集中管理，支持环境变量覆盖
# ============================================================================

import os
from typing import Dict, Any

# ============================================================================
# 基础配置
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = os.getenv("PROJECT_NAME", "Embodied Intelligence Robot System")
VERSION = os.getenv("VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# ============================================================================
# 服务配置
# ============================================================================
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "7861"))
HEALTH_CHECK_ENDPOINT = os.getenv("HEALTH_CHECK_ENDPOINT", "/health")

# ============================================================================
# 仿真配置
# ============================================================================
SIMULATION_CONFIG: Dict[str, Any] = {
    "time_step": float(eval(os.getenv("SIM_TIME_STEP", "1/240"))),
    "gravity": float(os.getenv("SIM_GRAVITY", "-9.81")),
    "max_solver_iterations": int(os.getenv("SIM_MAX_ITER", "200")),
    "render_mode": os.getenv("SIM_RENDER", "direct"),  # direct, gui
    "connection_mode": os.getenv("SIM_CONNECT", "direct"),  # direct, shared_memory
}

# ============================================================================
# 机器人安全参数
# ============================================================================
SAFETY_CONFIG: Dict[str, Any] = {
    "joint_torque_warning_ratio": float(os.getenv("SAFETY_TORQUE_RATIO", "0.7")),
    "joint_velocity_limit_factor": float(os.getenv("SAFETY_VEL_FACTOR", "0.8")),
    "emergency_stop_on_collision": os.getenv("SAFETY_ESTOP_ON_COL", "true").lower() == "true",
    "max_payload_factor": float(os.getenv("SAFETY_PAYLOAD_FACTOR", "0.9")),
}

# ============================================================================
# 日志配置
# ============================================================================
LOG_CONFIG: Dict[str, Any] = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "file": os.getenv("LOG_FILE", "./logs/app.log"),
    "max_bytes": int(os.getenv("LOG_MAX_BYTES", "10485760")),  # 10MB
    "backup_count": int(os.getenv("LOG_BACKUP_COUNT", "5")),
    "format": os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
}

# ============================================================================
# 连接配置
# ============================================================================
CONNECTION_CONFIG: Dict[str, Any] = {
    "default_timeout": float(os.getenv("CONN_TIMEOUT", "10.0")),
    "retry_max_attempts": int(os.getenv("CONN_RETRY_MAX", "3")),
    "retry_delay_seconds": float(os.getenv("CONN_RETRY_DELAY", "2.0")),
    "heartbeat_interval": float(os.getenv("CONN_HEARTBEAT", "5.0")),
}

# ============================================================================
# 模型路径配置
# ============================================================================
MODEL_CONFIG: Dict[str, Any] = {
    "checkpoint_dir": os.getenv("MODEL_CHECKPOINT_DIR", "./checkpoints"),
    "default_reach_model": os.getenv("MODEL_DEFAULT_REACH", "ppo_robot_reach_final_5m_enhanced"),
    "default_grasp_model": os.getenv("MODEL_DEFAULT_GRASP", "kuka_grasp_ppo"),
    "vec_normalize_path": os.getenv("MODEL_VEC_NORM", "vec_normalize_optimized.pkl"),
}

# ============================================================================
# 数据存储配置
# ============================================================================
DATA_CONFIG: Dict[str, Any] = {
    "log_dir": os.getenv("DATA_LOG_DIR", "./logs"),
    "eval_dir": os.getenv("DATA_EVAL_DIR", "./eval_logs"),
    "deploy_dir": os.getenv("DATA_DEPLOY_DIR", "./deploy_archives"),
    "calibration_file": os.getenv("DATA_CALIBRATION", "calibration_results.json"),
}

# ============================================================================
# 获取完整配置字典 (用于健康检查等)
# ============================================================================
def get_all_config() -> Dict[str, Any]:
    return {
        "project": PROJECT_NAME,
        "version": VERSION,
        "debug": DEBUG,
        "host": HOST,
        "port": PORT,
        "simulation": SIMULATION_CONFIG,
        "safety": SAFETY_CONFIG,
        "connection": CONNECTION_CONFIG,
        "model": MODEL_CONFIG,
        "data": DATA_CONFIG,
    }
