
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
import traceback

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import numpy as np
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

# 用原始预训练模型（100%成功率）
model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

for progress in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    try:
        sys.stderr = open(os.devnull, 'w')
        test_env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
        test_env.set_curriculum_progress(progress)
        success_count = 0
        total_reward = 0.0
        steps_list = []
        for i in range(30):
            obs, info = test_env.reset()
            done = False
            episode_reward = 0.0
            step_count = 0
            while not done:
                action, _states = model.predict(obs, deterministic=True)
                obs, reward, terminated, truncated, info = test_env.step(action)
                episode_reward += reward
                step_count += 1
                done = terminated or truncated
            total_reward += episode_reward
            steps_list.append(step_count)
            success_count += 1 if terminated else 0
        avg_reward = total_reward / 30
        success_rate = success_count / 30 * 100
        avg_steps = np.mean(steps_list)
        sys.stderr = old_stderr
        result = 'Progress %.1f: Success %2d/30 (%.1f%%) | Avg Reward: %8.2f | Avg Steps: %.0f' % (progress, success_count, success_rate, avg_reward, avg_steps)
        print(result, flush=True)
    except Exception as e:
        sys.stderr = old_stderr
        print('Progress %.1f: ERROR %s' % (progress, str(e)), flush=True)
