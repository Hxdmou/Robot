import sys, os
old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import numpy as np
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

for progress in [0.6, 0.8, 1.0]:
    try:
        sys.stderr = open(os.devnull, 'w')
        test_env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
        test_env.set_curriculum_progress(progress)
        success_count = 0
        total_reward = 0.0
        for i in range(30):
            obs, info = test_env.reset()
            done = False
            ep_reward = 0.0
            while not done:
                action, _ = model.predict(obs, deterministic=True)
                obs, reward, term, trunc, _ = test_env.step(action)
                ep_reward += reward
                done = term or trunc
            total_reward += ep_reward
            success_count += 1 if term else 0
        rate = success_count / 30 * 100
        avg_r = total_reward / 30
        sys.stderr = old_stderr
        print('Progress %.1f: Success %2d/30 (%.1f%%) | Avg Reward: %8.2f | noise=%.5f coll=%.1f delay=%d' % (
            progress, success_count, rate, avg_r,
            test_env.noise_gaussian_std, test_env.collision_penalty, test_env.command_delay_steps
        ), flush=True)
        test_env.close()
    except Exception as e:
        sys.stderr = old_stderr
        print('Progress %.1f ERROR: %s' % (progress, str(e)), flush=True)
