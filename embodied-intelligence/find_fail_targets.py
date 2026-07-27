import sys, os
old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import pybullet as p
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized
import numpy as np

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')
test_env = RobotReachEnvOptimized(render_mode=None, max_steps=2000)
test_env.set_curriculum_progress(1.0)

print('=== 进度1.0：找10个失败目标 ===', flush=True)
fail_count = 0
fail_targets = []

for i in range(500):
    obs, info = test_env.reset()
    target = test_env.target_pos.copy()
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, term, trunc, _ = test_env.step(action)
        done = term or trunc
    if not term:
        fail_count += 1
        fail_targets.append(target.copy())
        if fail_count <= 10:
            sys.stderr = old_stderr
            print('  失败#%d: target=[%.3f,%.3f,%.3f]' % (fail_count, target[0], target[1], target[2]), flush=True)
            sys.stderr = open(os.devnull, 'w')
    if fail_count >= 10:
        break

sys.stderr = old_stderr
if fail_targets:
    targets = np.array(fail_targets)
    print('', flush=True)
    print('失败目标范围: X[%.3f,%.3f] Y[%.3f,%.3f] Z[%.3f,%.3f]' % (
        targets[:,0].min(), targets[:,0].max(),
        targets[:,1].min(), targets[:,1].max(),
        targets[:,2].min(), targets[:,2].max()
    ), flush=True)
    print('当前目标范围: X[%.3f,%.3f] Y[%.3f,%.3f] Z[%.3f,%.3f]' % (
        test_env.target_min[0], test_env.target_max[0],
        test_env.target_min[1], test_env.target_max[1],
        test_env.target_min[2], test_env.target_max[2]
    ), flush=True)
test_env.close()
