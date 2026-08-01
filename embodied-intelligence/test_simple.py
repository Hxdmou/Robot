
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

import sys
import os


if __name__ == '__main__':
    print("Python:", sys.version)
    print("CWD:", os.getcwd())

    try:
        import pybullet as p
        print("PyBullet: OK")
    except Exception as e:
        print("PyBullet FAIL:", e)

    try:
        import gymnasium as gym
        print("Gymnasium: OK")
    except Exception as e:
        print("Gymnasium FAIL:", e)

    try:
        from stable_baselines3 import PPO
        print("SB3: OK")
    except Exception as e:
        print("SB3 FAIL:", e)

    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "embodied-intelligence"))
    try:
        from robot_reach_env_optimized import RobotReachEnvOptimized
        print("Env import: OK")
    except Exception as e:
        print("Env import FAIL:", e)
        import traceback
        traceback.print_exc()

    print("DONE")
