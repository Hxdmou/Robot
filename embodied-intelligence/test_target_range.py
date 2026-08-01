
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

import sys, os

if __name__ == '__main__':
    old_stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    import pybullet as p
    from stable_baselines3 import PPO
    from robot_reach_env_optimized import RobotReachEnvOptimized
    import numpy as np

    model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

    # 逐级扩大目标范围，测试100轮成功率
    test_ranges = [
        ('当前', np.array([0.37, -0.12, 0.30]), np.array([0.53, 0.12, 0.42])),
        ('扩展1', np.array([0.35, -0.13, 0.29]), np.array([0.55, 0.13, 0.43])),
        ('扩展2', np.array([0.33, -0.14, 0.28]), np.array([0.57, 0.14, 0.44])),
        ('扩展3', np.array([0.30, -0.15, 0.27]), np.array([0.60, 0.15, 0.45])),
    ]

    sys.stderr = old_stderr
    print('=== 目标范围扩展测试（100轮/级，进度1.0） ===', flush=True)

    for name, tmin, tmax in test_ranges:
        test_env = RobotReachEnvOptimized(render_mode=None, max_steps=800)
        test_env.set_curriculum_progress(1.0)
        # 手动覆盖目标范围
        test_env.target_min = tmin.astype(np.float32)
        test_env.target_max = tmax.astype(np.float32)
        success_count = 0
        for i in range(100):
            obs, info = test_env.reset()
            # reset()会重置target_min/max，所以每次都要覆盖
            test_env.target_min = tmin.astype(np.float32)
            test_env.target_max = tmax.astype(np.float32)
            test_env.target_pos = test_env.np_random.uniform(test_env.target_min, test_env.target_max).astype(np.float32)
            done = False
            while not done:
                action, _ = model.predict(obs, deterministic=True)
                obs, reward, term, trunc, _ = test_env.step(action)
                done = term or trunc
            success_count += 1 if term else 0
        rate = success_count / 100 * 100
        print('  %s: %d/100 (%.0f%%) | 范围X[%.2f,%.2f] Y[%.2f,%.2f] Z[%.2f,%.2f]' % (
            name, success_count, rate,
            tmin[0], tmax[0], tmin[1], tmax[1], tmin[2], tmax[2]
        ), flush=True)
        test_env.close()
