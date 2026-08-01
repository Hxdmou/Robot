"""
配置文件：机械臂类型、仿真步数、目标姿态等
可根据需要修改
"""
# ============================================================================
# 免责声明与AI使用规范
# ============================================================================
# 本文件仅供技术研究与学习交流使用，不得用于任何非法用途。
#
# AI使用规范：
#   1. 使用本文件相关内容时须遵守所在地法律法规及伦理准则
#   2. 不得用于侵犯他人合法权益、危害网络安全、破坏公共秩序的活动
#   3. 涉及自动化决策的场景须确保人工复核机制与可解释性
#   4. 处理个人信息时须符合数据保护相关法规要求
#
# 风险提示：
#   本文件内容按"现状"提供，不保证绝对准确无误。
#   使用者须自行评估风险，因使用本文件导致的任何损失由使用者承担。
# ============================================================================



# ================== 机械臂类型选择 ==================
# True  = KUKA iiwa
# False = Franka Panda（默认）
USE_KUKA = False

# ================== 仿真参数 ==================
SIMULATION_STEPS = 10000   # 总仿真步数
LOG_INTERVAL = 1          # 每1步记录一次

# ================== 目标关节角（直立姿态参考） ==================
# 这些值用于初始化机械臂位置，以及计算姿态偏差。
# 注意：这些是近似值，可根据实际模型调整。
if USE_KUKA:
    # KUKA iiwa 近似直立姿态
    TARGET_JOINT_POSITIONS = [0, -0.5, 0, -1.8, 0, 1.2, 0.8]
else:
    # Franka Panda 直立姿态（IK求解结果）
    TARGET_JOINT_POSITIONS = [-1.0247, -1.3870, 0.0000, -3.3847, 0.0000, -1.1439, -1.3315]

# ================== 末端目标位置（用于偏差计算） ==================
# 直立时末端执行器的近似位置 (x, y, z)
if USE_KUKA:
    TARGET_EE_POS = [0.3, 0, 0.5]
else:
    TARGET_EE_POS = [0, 0, 0.6]


# ============================================================================
# 工业化扩展配置
# ============================================================================

# ================== 安全参数 ==================
SAFETY_CONFIG = {
    "torque_limit_ratio": 0.7,       # 力矩限制比例(0.1-1.0)
    "velocity_limit_ratio": 0.7,     # 速度限制比例(0.1-1.0)
    "enable_collision_detection": True,  # 碰撞检测
    "emergency_stop_active": False,   # 紧急停止状态
    "max_operation_hours": 24,        # 最大连续运行小时数
}

# ================== 通信参数 ==================
COMM_CONFIG = {
    "connection_timeout_ms": 5000,    # 连接超时(毫秒)
    "response_timeout_ms": 2000,      # 响应超时(毫秒)
    "heartbeat_interval_ms": 1000,    # 心跳间隔(毫秒)
    "max_retry_count": 3,             # 最大重试次数
    "retry_interval_ms": 500,         # 重试间隔(毫秒)
    "protocol": "TCP/IP",             # 通信协议: TCP/IP, UDP, Serial, EtherCAT
}

# ================== API服务器 ==================
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "enable_cors": True,
    "enable_docs": True,
    "workers": 1,
}

# ================== 日志配置 ==================
LOG_CONFIG = {
    "level": "INFO",                   # DEBUG, INFO, WARNING, ERROR
    "enable_file_log": True,
    "log_dir": "logs",
    "max_file_size_mb": 10,
    "backup_count": 5,
    "enable_console_log": True,
    "enable_operation_log": True,      # 操作日志(审计追踪)
    "enable_error_log": True,          # 错误日志
}

# ================== 数据记录 ==================
DATA_CONFIG = {
    "enable_recording": True,
    "recording_dir": "data",
    "record_interval_ms": 10,          # 记录间隔(毫秒)
    "save_format": "csv",              # csv, json, pickle
    "max_recording_hours": 8,          # 最大记录时长(小时)
    "auto_save_minutes": 30,           # 自动保存间隔(分钟)
}

# ================== 校准配置 ==================
CALIBRATION_CONFIG = {
    "auto_calibrate_on_start": True,   # 启动时自动校准
    "joint_zero_tolerance": 0.001,     # 关节零点容差(弧度)
    "payload_calibration": True,        # 负载校准
    "temperature_compensation": True,   # 温度补偿
    "periodic_calibration_hours": 8,   # 定期校准间隔(小时)
}

# ================== 部署配置 ==================
DEPLOY_CONFIG = {
    "mode": "simulation",               # simulation, real_robot, hybrid
    "robot_brand": "auto_detect",       # auto_detect, kuka, panda, airbot
    "connection_ip": "192.168.1.100", # 机器人IP
    "connection_port": 5000,           # 机器人端口
    "enable_gui": True,                 # 启用GUI
    "enable_monitor": True,             # 启用监控
    "auto_start_services": True,        # 自动启动服务
}


def get_config_summary():
    """获取配置摘要"""
    return {
        "robot_type": "KUKA iiwa" if USE_KUKA else "Franka Panda",
        "simulation_steps": SIMULATION_STEPS,
        "deploy_mode": DEPLOY_CONFIG["mode"],
        "safety_enabled": SAFETY_CONFIG["enable_collision_detection"],
        "api_port": API_CONFIG["port"],
    }


if __name__ == "__main__":
    print("=" * 60)
    print("  工业化配置中心")
    print("=" * 60)
    summary = get_config_summary()
    for k, v in summary.items():
        print(f"  {k:25s}: {v}")
    print("=" * 60)
