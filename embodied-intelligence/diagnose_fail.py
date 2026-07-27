import sys, os
old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized
import numpy as np

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

# 测试进度1.0，但把max_steps增加到1200，看看是不是步数不够
print('=== 测试：进度1.0 + max_steps=1200 ===', flush=True)
test_env = RobotReachEnvOptimized(render_mode=None, max_steps=1200)
test_env.set_curriculum_progress(1.0)
success_count = 0
fail_steps = []
for i in range(50):
    obs, info = test_env.reset()
    done = False
    steps = 0
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, term, trunc, _ = test_env.step(action)
        steps += 1
        done = term or trunc
    if term:
        success_count += 1
    else:
        fail_steps.append(steps)
sys.stderr = old_stderr
print('成功率: %d/50 (%.0f%%)' % (success_count, success_count/50*100), flush=True)
if fail_steps:
    print('失败时步数: %s (avg=%.0f, max=%d)' % (fail_steps[:10], np.mean(fail_steps), max(fail_steps)), flush=True)
test_env.close()
