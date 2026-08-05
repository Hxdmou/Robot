# ============================================================================
# 【超严谨模块头】免责声明 · 法律声明 · 隐私保护 · AI安全红线 · 伦理规范
# ============================================================================
# 项目名称：具身智能工程化平台 (Embodied Intelligence Engineering Platform)
# 文件用途：全局统一配置中心（机器人品牌/通信参数/仿真/部署/训练/监控）
#
# ┌────────────────────────────────────────────────────────────────────────┐
# │ 第一部分 · AI使用与法律红线（严格禁止）                                  │
# ├────────────────────────────────────────────────────────────────────────┤
# │  1. 严禁利用本软件（含其算法、模型、接口、数据集、部署产物）从事：       │
# │     - 非法获取、收集、倒卖、出售、泄露任何个人信息、隐私数据、商业秘密； │
# │     - 诈骗、盗窃、网络攻击、入侵、恶意爬虫、钓鱼、勒索、赌博、色情等；   │
# │     - 伪造/冒用他人身份、声音、形象、签名、生物特征或任何人格要素；      │
# │     - 绕过他人平台风控/验证码/速率限制/反作弊获取不正当利益；            │
# │     - 侵犯知识产权、肖像权、名誉权、隐私权、商业秘密等他人合法权益。     │
# │  2. 真实物理设备部署前，必须由具有资质的工程师完成：安全校验、急停验证、 │
# │     风险评估、人工监督预案、现场防护；否则禁止驱动任何真实机器人/机械。  │
# │  3. 严禁用于军事/武器/致命系统/核设施/航空电子/医疗手术等高风险行业，    │
# │     除非取得全部法定许可与独立第三方安全认证。                            │
# │  4. 所有自动化决策强制保留：人工复核 + 一键紧急停止 + 可解释性审计日志。 │
# └────────────────────────────────────────────────────────────────────────┘
#
# ┌────────────────────────────────────────────────────────────────────────┐
# │ 第二部分 · 隐私保护与数据治理                                            │
# ├────────────────────────────────────────────────────────────────────────┤
# │  1. 本项目源码与配置文件默认"零真实个人数据"。任何真实人员/企业/设备的    │
# │     敏感信息（姓名、身份证、手机号、邮箱、住址、内网名、内部IP、密码、   │
# │     密钥、令牌、凭证）禁止直接硬编码写入任何文件，必须通过环境变量、     │
# │     加密密钥管理系统或 .env（已在.gitignore强制忽略）外部注入。          │
# │  2. 处理任何他人数据必须取得充分、明确、可撤回的知情同意，并落实：        │
# │     数据最小化 + 目的限定 + 存储加密 + 访问控制 + 删除权保障。            │
# │  3. 严禁用本软件窃取、还原、拼接、推理、重建他人隐私、生物特征、行踪、   │
# │     关系网络、财产状况等受法律保护的敏感信息。                           │
# │  4. 任何上传、同步、备份、训练所用数据，由使用者自行确保来源合法、       │
# │     授权完整；侵权纠纷、索赔、行政处罚、刑事责任，由数据提供者和         │
# │     实际使用者独立承担。                                                 │
# └────────────────────────────────────────────────────────────────────────┘
#
# ┌────────────────────────────────────────────────────────────────────────┐
# │ 第三部分 · 免责声明与责任限制（按现状提供，最大化权益保护）               │
# ├────────────────────────────────────────────────────────────────────────┤
# │  1. 本软件及其全部衍生内容按"AS IS（现状）"提供，不附带任何明示或默示     │
# │     保证，包括但不限于适销性、特定用途适用性、非侵权性、绝对准确性。     │
# │  2. 在法律允许的最大范围内，版权持有者、贡献者、维护者不因任何原因、     │
# │     任何诉由（合同、侵权、过错、严格责任或其他）对任何人承担任何直接、   │
# │     间接、附带、特殊、惩戒性、惩罚性或后果性损害赔偿责任，包括但不限于   │
# │     利润损失、商誉损失、数据损失、业务中断、替代采购成本或任何其他       │
# │     金钱损失或人身伤害/财产损失，即便已被告知该等损害的可能性。         │
# │  3. 全部累计赔偿责任总额在任何情形下均不超过使用者为软件本身实际支付     │
# │     的对价（如有）；软件免费使用时，全部赔偿责任上限为人民币壹元整（¥1）。│
# │  4. 任何条款被有管辖权的有权机关认定为无效或不可执行的，不影响其余条款   │
# │     的效力；其余条款仍在法律允许的最大范围内完全有效并可执行。           │
# └────────────────────────────────────────────────────────────────────────┘
#
# 接受与使用本软件的任何一部分，即视为已完整阅读、理解并不可撤销地
# 接受上述全部条款。如不接受，请立即删除所有副本并停止使用。
# ============================================================================

import os
import sys

# ============================================================================
# 【安全防线工具】统一环境变量安全读取（密钥/IP/凭证硬编码零容忍）
# ============================================================================
def secure_env(env_name: str, default_value: str = "", cast: str = "str"):
    """
    安全读取环境变量，实现"源码零硬编码敏感信息"的统一防线。

    用法：
        connection_ip   = secure_env("ROBOT_CONNECTION_IP",   "127.0.0.1")
        api_key         = secure_env("ROBOT_CLOUD_API_KEY",    "")
        connection_port = secure_env("ROBOT_CONNECTION_PORT", "5000", cast="int")

    参数 cast 支持: str / int / float / bool（空字符串视为bool=False）
    """
    raw = os.getenv(env_name, default_value)
    if cast == "int":
        try:
            return int(raw)
        except (TypeError, ValueError):
            return int(default_value) if str(default_value).strip() else 0
    if cast == "float":
        try:
            return float(raw)
        except (TypeError, ValueError):
            return float(default_value) if str(default_value).strip() else 0.0
    if cast == "bool":
        if raw is None or str(raw).strip() == "":
            return False
        return str(raw).strip().lower() in ("1", "true", "yes", "y", "on")
    # 默认 str
    return str(raw) if raw is not None else ""

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
# 安全提示：任何真实机器人IP/端口/密钥必须通过环境变量注入，禁止在源码中硬编码
#   export ROBOT_COMM_DEFAULT_HOST=127.0.0.1    # 示例：本机回环；请按实际内网环境替换（仅本机可见）
#   unset  ROBOT_COMM_DEFAULT_HOST                   # 清除自定义
COMM_CONFIG = {
    "default_host": secure_env("ROBOT_COMM_DEFAULT_HOST", "127.0.0.1"),
    "connection_timeout_ms": secure_env("ROBOT_COMM_TIMEOUT_MS", "5000", cast="int"),
    "response_timeout_ms": secure_env("ROBOT_RESP_TIMEOUT_MS", "2000", cast="int"),
    "heartbeat_interval_ms": 1000,    # 心跳间隔(毫秒)
    "max_retry_count": 3,             # 最大重试次数
    "retry_interval_ms": 500,         # 重试间隔(毫秒)
    "protocol": "TCP/IP",             # 通信协议: TCP/IP, UDP, Serial, EtherCAT
}

# ================== API服务器 ==================
# 安全提示：API监听地址/端口统一从环境变量读取，避免暴露真实部署拓扑
API_CONFIG = {
    "host": secure_env("API_SERVER_HOST", "0.0.0.0"),
    "port": secure_env("API_SERVER_PORT", "8000", cast="int"),
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
# 安全提示：真实设备IP/端口从环境变量注入，源码中默认一律使用 127.0.0.1（本地回环）。
# 示例：
#   Linux/Mac : export ROBOT_CONNECTION_IP=127.0.0.1
#   Windows   : $env:ROBOT_CONNECTION_IP="127.0.0.1"
DEPLOY_CONFIG = {
    "mode": "simulation",
    "robot_brand": "auto_detect",
    "connection_ip": secure_env("ROBOT_CONNECTION_IP",   "127.0.0.1"),
    "connection_port": secure_env("ROBOT_CONNECTION_PORT", "5000", cast="int"),
    "enable_gui": True,
    "enable_monitor": True,
    "auto_start_services": True,
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
