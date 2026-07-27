import sys, os

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import numpy as np
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

def test_env(env_name, setup_fn):
    sys.stderr = open(os.devnull, 'w')
    test_env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
    setup_fn(test_env)
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
    result = '%s: Success %2d/30 (%.1f%%) | Avg Reward: %8.2f' % (env_name, success_count, success_rate, avg_reward)
    print(result, flush=True)

# 1. 基准（无增强）
test_env('BASE (no enhancement)', lambda e: e.set_curriculum_progress(0.0))

# 2. 仅领域随机化（中等强度：progress 0.6，但关闭其他模块）
def only_domain_rand(e):
    e.set_curriculum_progress(0.0)
    # 手动设置领域随机化参数（中等强度）
    e.friction_range = (0.95, 1.05)
    e.damping_range = (0.04, 0.06)
    e.mass_range = (0.95, 1.05)
    e.gravity_range = (-9.85, -9.78)
    # 但在reset中需要curriculum_progress >= 0.2才会应用
    e.curriculum_progress = 0.6

test_env('ONLY Domain Randomization', only_domain_rand)

# 3. 仅执行器动力学（中等强度）
def only_actuator(e):
    e.set_curriculum_progress(0.0)
    e.torque_limit = 160.0
    e.velocity_limit = 4.0
    e.dead_zone = 0.003
    e.curriculum_progress = 0.6  # 让step中应用执行器限制

test_env('ONLY Actuator Dynamics', only_actuator)

# 4. 仅外部扰动（中等强度）
def only_disturbance(e):
    e.set_curriculum_progress(0.0)
    e.disturbance_prob = 0.008
    e.disturbance_magnitude = 2.0
    e.curriculum_progress = 0.7  # 让step中应用扰动

test_env('ONLY External Disturbance', only_disturbance)
