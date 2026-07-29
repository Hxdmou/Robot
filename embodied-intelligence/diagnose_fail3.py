
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
import pybullet as p
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized
import numpy as np

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

print('=== 诊断：进度1.0失败目标分析 ===', flush=True)
test_env = RobotReachEnvOptimized(render_mode=None, max_steps=2000)
test_env.set_curriculum_progress(1.0)
fail_count = 0
fail_targets = []
fail_dists = []

for i in range(200):
    obs, info = test_env.reset()
    target = test_env.target_pos.copy()
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, term, trunc, _ = test_env.step(action)
        done = term or trunc
    if not term:
        fail_count += 1
        ee_final = np.array(p.getLinkState(test_env.robot_id, 6)[0])
        dist = np.linalg.norm(ee_final - target)
        fail_targets.append(target)
        fail_dists.append(dist)
        if fail_count <= 5:
            sys.stderr = old_stderr
            print('  失败#%d: target=[%.3f,%.3f,%.3f] final=[%.3f,%.3f,%.3f] dist=%.4f' % (
                fail_count, target[0], target[1], target[2],
                ee_final[0], ee_final[1], ee_final[2], dist
            ), flush=True)
            sys.stderr = open(os.devnull, 'w')
    if fail_count >= 5:
        break

sys.stderr = old_stderr
print('', flush=True)
print('200轮中失败: %d (%.1f%%)' % (fail_count, fail_count/200*100 if fail_count > 0 else 0), flush=True)
if fail_targets:
    targets = np.array(fail_targets)
    print('失败目标范围: X[%.3f,%.3f] Y[%.3f,%.3f] Z[%.3f,%.3f]' % (
        targets[:,0].min(), targets[:,0].max(),
        targets[:,1].min(), targets[:,1].max(),
        targets[:,2].min(), targets[:,2].max()
    ), flush=True)
    print('失败时距离: avg=%.4f  min=%.4f  max=%.4f' % (
        np.mean(fail_dists), np.min(fail_dists), np.max(fail_dists)
    ), flush=True)
print('当前目标范围: X[%.3f,%.3f] Y[%.3f,%.3f] Z[%.3f,%.3f]' % (
    test_env.target_min[0], test_env.target_max[0],
    test_env.target_min[1], test_env.target_max[1],
    test_env.target_min[2], test_env.target_max[2]
), flush=True)
test_env.close()
