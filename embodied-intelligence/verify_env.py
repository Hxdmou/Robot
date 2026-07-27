"""
验证环境是否正常工作 - 用旧模型测试新环境
"""

import sys
import os

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
os.environ['PYBULLET_DISABLE_WARNINGS'] = '1'

from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

sys.stderr = old_stderr

# 加载旧模型
print("加载旧模型 ppo_robot_reach_final_5m_enhanced ...", flush=True)
model = PPO.load("ppo_robot_reach_final_5m_enhanced")

# 测试1：课程学习进度 0.0（无增强）
print("\n=== Test 1: Curriculum Progress 0.0 (No Enhancement) ===", flush=True)
sys.stderr = open(os.devnull, 'w')

test_env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
test_env.set_curriculum_progress(0.0)

success_count = 0
total_reward = 0.0

for i in range(50):
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

avg_reward = total_reward / 50
success_rate = success_count / 50 * 100

sys.stderr = old_stderr
print(f'\nSuccess Rate: {success_count}/50 ({success_rate:.1f}%)', flush=True)
print(f'Average Reward: {avg_reward:.2f}', flush=True)

# 测试2：课程学习进度 1.0（最大增强）
print("\n=== Test 2: Curriculum Progress 1.0 (Max Enhancement) ===", flush=True)
sys.stderr = open(os.devnull, 'w')

test_env2 = RobotReachEnvOptimized(render_mode=None, max_steps=600)
test_env2.set_curriculum_progress(1.0)

success_count2 = 0
total_reward2 = 0.0

for i in range(50):
    obs, info = test_env2.reset()
    done = False
    episode_reward = 0.0
    
    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = test_env2.step(action)
        episode_reward += reward
        done = terminated or truncated
    
    total_reward2 += episode_reward
    success_count2 += 1 if terminated else 0

avg_reward2 = total_reward2 / 50
success_rate2 = success_count2 / 50 * 100

sys.stderr = old_stderr
print(f'\nSuccess Rate: {success_count2}/50 ({success_rate2:.1f}%)', flush=True)
print(f'Average Reward: {avg_reward2:.2f}', flush=True)
