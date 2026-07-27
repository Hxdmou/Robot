import sys, os

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import numpy as np
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

for progress in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
    sys.stderr = open(os.devnull, 'w')
    test_env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
    test_env.set_curriculum_progress(progress)
    success_count = 0
    total_reward = 0.0
    for i in range(30):
        obs, info = test_env.reset()
        done = False
        episode_reward = 0.0
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = test_env.step(action)
            episode_reward += reward
            done = terminated or truncated
        total_reward += episode_reward
        success_count += 1 if terminated else 0
    avg_reward = total_reward / 30
    success_rate = success_count / 30 * 100
    sys.stderr = old_stderr
    print('Progress %.1f: Success %2d/30 (%.1f%%) | Avg Reward: %8.2f' % (progress, success_count, success_rate, avg_reward), flush=True)
