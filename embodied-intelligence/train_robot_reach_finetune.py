#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fine-tune training script for ppo_robot_reach_stable_final.zip

Target: Improve performance on weak areas (X[0.25,0.40], Y[-0.25,0.25], Z[0.30,0.55])

Strategy:
- 50% of episodes sample from weak regions
- 50% of episodes sample from full range
- Lower learning rate to prevent catastrophic forgetting
- Reachability validation to exclude physically unreachable points
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


import os
import sys
import time
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import EvalCallback
from robot_reach_env_optimized import RobotReachEnvOptimized

sys.stdout.reconfigure(line_buffering=True)

os.chdir(PROJECT_ROOT)

print("=" * 70)
print("  Fine-tune Training: Weak Area Optimization")
print("=" * 70)

print("\n[ENVIRONMENT SETTINGS]")
print("  Target Range: X[0.25,0.65], Y[-0.25,0.25], Z[0.20,0.55]")
print("  Weak Region:  X[0.25,0.40], Y[-0.25,0.25], Z[0.30,0.55] (50% sampling)")
print("  Joint Init:   uniform(-1.0, 1.0)")
print("  Weighted Sampling: Enabled")
print("  Reachability Validation: Enabled")

n_envs = 8
n_eval_envs = 4

print(f"\n[PARALLELIZATION]")
print(f"  Training Envs: {n_envs}")
print(f"  Evaluation Envs: {n_eval_envs}")

def train_env_fn():
    return RobotReachEnvOptimized(render_mode=None, max_steps=150, use_weighted_sampling=True)

def eval_env_fn():
    return RobotReachEnvOptimized(render_mode=None, max_steps=150, use_weighted_sampling=True)

train_env = make_vec_env(train_env_fn, n_envs=n_envs)
eval_env = make_vec_env(eval_env_fn, n_envs=n_eval_envs)

print("\n[LOADING PRE-TRAINED MODEL]")
print("  Model: ppo_robot_reach_stable_final.zip")
model = PPO.load("ppo_robot_reach_stable_final.zip", env=train_env, device="cpu")

print("\n[TRAINING PARAMETERS]")
print(f"  Total Timesteps: 1,500,000")
print(f"  Learning Rate:   {model.learning_rate}")
print(f"  Entropy Coef:    {model.ent_coef}")
print(f"  Clip Range:      {model.clip_range}")

eval_callback = EvalCallback(
    eval_env,
    best_model_save_path="./",
    log_path="./",
    eval_freq=100000,
    n_eval_episodes=100,
    deterministic=True,
    render=False,
)

print("\n[STARTING FINE-TUNE TRAINING]")
start_time = time.time()

total_timesteps = 1_500_000
model.learn(
    total_timesteps=total_timesteps,
    callback=eval_callback,
    progress_bar=True,
    reset_num_timesteps=False,
)

elapsed_time = time.time() - start_time

print("\n[TRAINING COMPLETED]")
print(f"  Total Time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")

model.save("ppo_robot_reach_finetuned")
print(f"  Model Saved: ppo_robot_reach_finetuned.zip")

train_env.close()
eval_env.close()

print("\n[FINAL TEST]")
test_env = RobotReachEnvOptimized(render_mode=None, max_steps=150, use_weighted_sampling=False)
test_model = PPO.load("ppo_robot_reach_finetuned", env=test_env, device="cpu")

weak_points = [
    (0.25, -0.10, 0.35),
    (0.25, 0.10, 0.35),
    (0.25, 0.25, 0.55),
    (0.35, 0.25, 0.55),
    (0.25, -0.25, 0.35),
]

print("\n  Testing weak points:")
for point in weak_points:
    successes = []
    for _ in range(10):
        obs, info = test_env.reset()
        test_env.target_pos = np.array(point, dtype=np.float32)
        terminated = False
        while not terminated:
            action, _ = test_model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = test_env.step(action)
            if truncated:
                break
        successes.append(int(terminated))
    sr = np.mean(successes) * 100
    print(f"    ({point[0]:.2f},{point[1]:.2f},{point[2]:.2f}): SR={sr:.0f}%")

test_env.close()

print("\n[DONE]")
