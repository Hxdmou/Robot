
if __name__ == '__main__':
    """
    纯Gym API测试脚本 - 不使用VecEnv，避免自动reset干扰
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

    import numpy as np
    from stable_baselines3 import PPO
    from robot_reach_env_optimized import RobotReachEnvOptimized

    # 创建单个环境（纯Gym API）
    print("Creating single Gym environment...")
    env = RobotReachEnvOptimized(render_mode=None, max_steps=500)
    env.curriculum_progress = 1.0
    env._update_curriculum_target_range()

    # 加载模型（不传递env参数）
    print("Loading model...")
    model = PPO.load('checkpoints_reach_enhanced/ppo_reach_4800000_steps', device='cpu')

    print("\nRunning 50 test episodes (Pure Gym API)...")
    success_count = 0
    total_reward = 0.0

    for i in range(50):
        obs, info = env.reset()  # Gym API返回(obs, info)
        done = False
        episode_reward = 0.0
        steps = 0
    
        while not done:
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)  # Gym API返回5个值
            episode_reward += reward
            steps += 1
            done = terminated or truncated
    
        total_reward += episode_reward
        success_count += 1 if terminated else 0
    
        if (i + 1) % 10 == 0:
            status = 'OK' if terminated else 'FAIL'
            print(f'  Episode {i+1:3d}: [{status}] | Steps: {steps:3d} | Reward: {episode_reward:.2f}')

    print(f'\n[TEST RESULTS]')
    print(f'Success Rate: {success_count}/50 ({success_count/50*100:.1f}%)')
    print(f'Average Reward: {total_reward/50:.2f}')
