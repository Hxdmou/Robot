"""
测试不同课程学习强度下的成功率
"""

import sys
import os

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
os.environ['PYBULLET_DISABLE_WARNINGS'] = '1'

import numpy as np
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

sys.stderr = old_stderr

model = PPO.load("ppo_robot_reach_curriculum", device="cpu")

progress_levels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

for progress in progress_levels:
    sys.stderr = open(os.devnull, 'w')
    
    test_env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
    test_env.set_curriculum_progress(progress)
    
    success_count = 0
    total_reward = 0.0
    steps_list = []
    
    for i in range(20):
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
    
    avg_reward = total_reward / 20
    success_rate = success_count / 20 * 100
    avg_steps = np.mean(steps_list)
    
    sys.stderr = old_stderr
    print(f'Progress {progress:.1f}: Success {success_count:2d}/20 ({success_rate:5.1f}%) | Avg Reward: {avg_reward:8.2f} | Avg Steps: {avg_steps:.0f}', flush=True)
