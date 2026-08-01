"""
配置文件：机械臂类型、仿真步数、目标姿态等
可根据需要修改

支持：135个机器人品牌全覆盖，44个应用场景全覆盖
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

import os
import sys

# ============================================================================
# 全覆盖配置中心导入
# ============================================================================
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from scenes_config import SCENES, get_scene_config, list_scenes
    SCENES_AVAILABLE = True
except Exception:
    SCENES_AVAILABLE = False
    SCENES = {}

try:
    from robots_config import ROBOT_CATEGORIES, ROBOT_BRANDS, get_robot_config, get_robots_by_category
    ROBOTS_AVAILABLE = True
except Exception:
    ROBOTS_AVAILABLE = False
    ROBOT_CATEGORIES = {}
    ROBOT_BRANDS = {}

# ============================================================================
# 当前选中的机器人（从135个品牌中选择）
# ============================================================================
# 环境变量切换: CURRENT_ROBOT=airbot_p7 python main.py train
# 可用: panda, kuka_lbr, airbot_p7, ufactory_cra, jaka_zu35,
#       unitree_h1, unitree_gd01, zhiyuan_a3, kepler_k2, ubtech_walker,
#       unitree_go2, unitree_b2, geek_amr, hikrobot_amr,
#       moonix_glasses, iflytek_glasses, stepx_neo, honor_robot, ...
# 完整列表: python robots_config.py
CURRENT_ROBOT = os.getenv("CURRENT_ROBOT", "panda")

# ============================================================================
# 当前选中的场景（从44个子场景中选择）
# ============================================================================
# 环境变量切换: CURRENT_SCENE=welding python main.py train
# 可用: assembly, welding, painting, handling, inspection, cnc,
#       picking, storage, loading, delivery,
#       surgery, rehab, nursing, diagnosis,
#       picking_agri, planting, food_processing, livestock,
#       retail, catering, hotel, cleaning,
#       research, teaching, training, competition,
#       home_cleaning, companion, ai_glasses, ai_phone,
#       security, military, space, underwater, mining, ...
# 完整列表: python scenes_config.py
CURRENT_SCENE = os.getenv("CURRENT_SCENE", "assembly")
CURRENT_SCENE_CAT = os.getenv("CURRENT_SCENE_CAT", "industrial")


# ================== 机械臂类型选择（兼容旧配置）==================
# True  = KUKA iiwa
# False = Franka Panda（默认）
# 推荐使用 CURRENT_ROBOT 环境变量选择更多品牌
USE_KUKA = (os.getenv("ROBOT_TYPE", CURRENT_ROBOT).lower() in ["kuka", "iiwa", "kuka_lbr"])


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
    robot_info = f"Franka Panda"
    if ROBOTS_AVAILABLE and CURRENT_ROBOT in ROBOT_BRANDS:
        robot_info = ROBOT_BRANDS[CURRENT_ROBOT]["name"]
    elif USE_KUKA:
        robot_info = "KUKA iiwa"

    scene_info = f"{CURRENT_SCENE_CAT}/{CURRENT_SCENE}"
    if SCENES_AVAILABLE and CURRENT_SCENE_CAT in SCENES:
        cat = SCENES[CURRENT_SCENE_CAT]
        if CURRENT_SCENE in cat["sub_scenes"]:
            scene_info = f"{cat['name']}/{cat['sub_scenes'][CURRENT_SCENE]['name']}"

    return {
        "robot_type": robot_info,
        "robot_key": CURRENT_ROBOT,
        "robot_category": ROBOT_BRANDS[CURRENT_ROBOT]["category"] if (ROBOTS_AVAILABLE and CURRENT_ROBOT in ROBOT_BRANDS) else "N/A",
        "scene": scene_info,
        "scene_key": f"{CURRENT_SCENE_CAT}/{CURRENT_SCENE}",
        "total_robots": len(ROBOT_BRANDS) if ROBOTS_AVAILABLE else 0,
        "total_scenes": sum(len(c["sub_scenes"]) for c in SCENES.values()) if SCENES_AVAILABLE else 0,
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
