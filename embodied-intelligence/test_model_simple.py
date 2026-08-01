#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    """
    Simple model evaluation test
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
    import numpy as np
    from stable_baselines3 import PPO
    from robot_reach_env_optimized import RobotReachEnvOptimized

    sys.stdout.reconfigure(line_buffering=True)
    os.chdir(PROJECT_ROOT)

    print("Loading model...", flush=True)
    model = PPO.load("ppo_robot_reach_final_5m_enhanced.zip", device="cpu")
    print("Model loaded!", flush=True)

    env = RobotReachEnvOptimized(render_mode=None, max_steps=150)

    test_targets = [
        (0.45, 0.0, 0.35),  
        (0.25, -0.25, 0.20),  
        (0.65, 0.25, 0.55),  
        (0.35, -0.10, 0.50),  
        (0.50, 0.20, 0.25),  
    ]

    print(f"\nTesting {len(test_targets)} target positions...", flush=True)

    for i, (x, y, z) in enumerate(test_targets):
        successes = []
        rewards = []
        for ep in range(5):
            obs, info = env.reset()
            env.target_pos = np.array([x, y, z], dtype=np.float32)
            ep_reward = 0.0
            terminated = False
        
            while not terminated:
                action, _ = model.predict(obs, deterministic=True)
                obs, reward, terminated, truncated, info = env.step(action)
                ep_reward += reward
                if truncated:
                    break
        
            successes.append(int(terminated))
            rewards.append(ep_reward)
    
        sr = np.mean(successes) * 100
        mr = np.mean(rewards)
        print(f"  [{i+1}/{len(test_targets)}] ({x:.2f},{y:.2f},{z:.2f}): SR={sr:.0f}%, R={mr:.1f}", flush=True)

    print("\nTesting joint init diversity...", flush=True)
    joint_ranges = [(-0.5, 0.5), (-1.0, 1.0), (-0.2, 0.2)]
    for low, high in joint_ranges:
        successes = []
        for ep in range(5):
            obs, info = env.reset()
            for j in range(7):
                import pybullet as p
                p.resetJointState(env.robot_id, j, env.np_random.uniform(low, high))
            ep_reward = 0.0
            terminated = False
        
            while not terminated:
                action, _ = model.predict(obs, deterministic=True)
                obs, reward, terminated, truncated, info = env.step(action)
                ep_reward += reward
                if truncated:
                    break
        
            successes.append(int(terminated))
    
        sr = np.mean(successes) * 100
        print(f"  Range ({low},{high}): SR={sr:.0f}%", flush=True)

    env.close()
    print("\nDone!", flush=True)
