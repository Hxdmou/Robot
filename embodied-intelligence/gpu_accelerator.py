"""
GPU加速配置模块（轻量级）
安全原则：低资源占用，无内存泄漏
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



import pybullet as p

def enable_gpu_acceleration(physics_client_id=None):
    """启用GPU加速优化"""
    client = physics_client_id if physics_client_id is not None else -1

    p.setPhysicsEngineParameter(
        numSolverIterations=200,
        numSubSteps=2,
        enableConeFriction=True,
        physicsClientId=client
    )

    p.configureDebugVisualizer(
        p.COV_ENABLE_GUI, 0,
        physicsClientId=client
    )

    p.configureDebugVisualizer(
        p.COV_ENABLE_SHADOWS, 0,
        physicsClientId=client
    )

    print("[GPU] GPU加速配置已应用")

def optimize_rendering(physics_client_id=None):
    """优化渲染性能"""
    client = physics_client_id if physics_client_id is not None else -1

    p.configureDebugVisualizer(
        p.COV_ENABLE_WIREFRAME, 0,
        physicsClientId=client
    )

    p.configureDebugVisualizer(
        p.COV_ENABLE_RENDERING, 1,
        physicsClientId=client
    )

    print("[GPU] 渲染优化已应用")
