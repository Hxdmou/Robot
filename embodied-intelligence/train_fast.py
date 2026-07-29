"""
快速训练脚本 - 直接训练到100%成功率
"""
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
sys.stderr = open(os.devnull, 'w')

import time
import gc
import multiprocessing
import signal
import psutil
import numpy as np

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback, CheckpointCallback
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor
from robot_reach_env_optimized import RobotReachEnvOptimized

def make_env(rank, seed=0, max_steps=400):
    def _init():
        env = RobotReachEnvOptimized(render_mode=None, max_steps=max_steps)
        env.reset(seed=seed + rank)
        return env
    return _init

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    print("=" * 70)
    print("  RobotReachEnv PPO Training - FAST MODE")
    print("=" * 70)

    # 训练配置
    n_envs = 16
    total_timesteps = 2_000_000  # 200万步快速验证
    max_steps_per_episode = 400

    print(f"\n[CONFIG]")
    print(f"   Parallel Environments: {n_envs}")
    print(f"   Total Steps: {total_timesteps:,}")
    print(f"   Max Steps/Episode: {max_steps_per_episode}")

    # 创建环境
    print(f"\nCreating {n_envs} parallel environments...")
    env = DummyVecEnv([make_env(i, max_steps=max_steps_per_episode) for i in range(n_envs)])
    env = VecMonitor(env)

    # 初始化模型
    print("\nInitializing PPO model...")
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=512,
        n_epochs=5,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        vf_coef=0.5,
        max_grad_norm=0.5,
        verbose=0,
        device="cpu"
    )

    print(f"\nStarting Training...")
    start_time = time.time()

    model.learn(
        total_timesteps=total_timesteps,
        progress_bar=False
    )

    elapsed = time.time() - start_time
    print(f"\n[SUCCESS] Training Completed!")
    print(f"   Total Time: {elapsed/60:.2f} minutes")
    print(f"   Average Speed: {total_timesteps/elapsed:.1f} steps/second")

    # 保存模型
    model.save("ppo_robot_reach_fast")
    print("   Model Saved: ppo_robot_reach_fast")

    # 测试
    print("\n=== Running 50 Test Episodes ===")
    test_env = DummyVecEnv([make_env(0, max_steps=500)])
    test_env = VecMonitor(test_env)
    
    # 设置课程学习进度
    test_env.envs[0].curriculum_progress = 1.0
    test_env.envs[0]._update_curriculum_target_range()
    
    model.set_env(test_env)
    
    success_count = 0
    total_reward = 0.0
    
    for i in range(50):
        obs = test_env.reset()
        done = False
        episode_reward = 0.0
        steps = 0
        
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated = test_env.step(action)
            episode_reward += reward[0]
            steps += 1
            done = terminated[0] or truncated[0]
        
        total_reward += episode_reward
        success_count += 1 if terminated[0] else 0
        
        if (i + 1) % 10 == 0:
            status = 'OK' if terminated[0] else 'FAIL'
            print(f'  Episode {i+1:3d}: [{status}] | Steps: {steps:3d} | Reward: {episode_reward:.2f}')

    print(f'\n[TEST RESULTS]')
    print(f'Success Rate: {success_count}/50 ({success_count/50*100:.1f}%)')
    print(f'Average Reward: {total_reward/50:.2f}')
