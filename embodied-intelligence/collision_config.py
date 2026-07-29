"""
碰撞检测配置文件
可根据真实场景调整参数
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



COLLISION_CONFIG = {
    "enabled": True,
    
    "safety_distance": 0.01,
    "warning_distance": 0.02,
    "check_interval": 0.01,
    "max_contacts": 100,
    
    "force_threshold": 10.0,
    "max_force": 100.0,
}

COLLISION_LEVELS = {
    "none": {
        "enabled": False,
        "safety_distance": 0.001,
        "warning_distance": 0.002,
        "force_threshold": 0,
        "max_force": 0,
    },

    "low": {
        "enabled": True,
        "safety_distance": 0.015,
        "warning_distance": 0.025,
        "force_threshold": 5.0,
        "max_force": 50.0,
    },

    "medium": {
        "enabled": True,
        "safety_distance": 0.01,
        "warning_distance": 0.02,
        "force_threshold": 10.0,
        "max_force": 100.0,
    },

    "high": {
        "enabled": True,
        "safety_distance": 0.005,
        "warning_distance": 0.01,
        "force_threshold": 20.0,
        "max_force": 150.0,
    },
}

OBSTACLE_CONFIG = {
    "table": {
        "name": "table",
        "type": "box",
        "dimensions": [0.5, 0.5, 0.02],
        "position": [0.2, 0, -0.02],
        "color": [0.6, 0.4, 0.2, 1],
        "mass": 0,
    },
}
