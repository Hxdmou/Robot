
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
old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

all_pass = True
for progress in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    sys.stderr = open(os.devnull, 'w')
    test_env = RobotReachEnvOptimized(render_mode=None, max_steps=800)
    test_env.set_curriculum_progress(progress)
    success_count = 0
    total_reward = 0.0
    for i in range(50):
        obs, info = test_env.reset()
        done = False
        ep_reward = 0.0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, term, trunc, _ = test_env.step(action)
            ep_reward += reward
            done = term or trunc
        total_reward += ep_reward
        success_count += 1 if term else 0
    rate = success_count / 50 * 100
    avg_r = total_reward / 50
    status = '[PASS]' if rate >= 90 else '[FAIL]'
    if rate < 90:
        all_pass = False
    sys.stderr = old_stderr
    print('%s Progress %.1f: %2d/50 (%.1f%%) | AvgR: %8.2f | noise=%.5f coll=%.1f delay=%d' % (
        status, progress, success_count, rate, avg_r,
        test_env.noise_gaussian_std, test_env.collision_penalty, test_env.command_delay_steps
    ), flush=True)
    test_env.close()

sys.stderr = old_stderr
print('', flush=True)
print('='*70, flush=True)
if all_pass:
    print('[ALL PASS] All curriculum levels >= 90% success rate!', flush=True)
else:
    print('[PARTIAL] Some levels failed', flush=True)
