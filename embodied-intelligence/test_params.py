import sys, os

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import numpy as np
import pybullet as p
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

def test_custom(name, reset_modifier=None):
    sys.stderr = open(os.devnull, 'w')
    
    class TestEnv(RobotReachEnvOptimized):
        def reset(self, seed=None, options=None):
            obs, info = super().reset(seed=seed, options=options)
            if reset_modifier:
                reset_modifier(self)
            return obs, info
    
    test_env = TestEnv(render_mode=None, max_steps=600)
    test_env.set_curriculum_progress(0.0)  # 基础
    
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
    result = '%s: Success %2d/30 (%.1f%%) | Avg Reward: %8.2f' % (name, success_count, success_rate, avg_reward)
    print(result, flush=True)

# 基准
test_custom('BASE')

# 仅重力变化
def only_gravity(env):
    p.setGravity(0, 0, -9.80)  # 极轻微变化

test_custom('Gravity -9.80', only_gravity)

# 仅阻尼变化
def only_damping(env):
    for i in range(7):
        p.changeDynamics(env.robot_id, i, linearDamping=0.06, angularDamping=0.06)

test_custom('Damping 0.06', only_damping)

# 仅摩擦变化
def only_friction(env):
    for i in range(7):
        p.changeDynamics(env.robot_id, i, lateralFriction=1.1)

test_custom('Friction 1.1', only_friction)

# 仅质量变化
def only_mass(env):
    for i in range(7):
        p.changeDynamics(env.robot_id, i, mass=1.05)

test_custom('Mass 1.05', only_mass)

# 阻尼更大
def high_damping(env):
    for i in range(7):
        p.changeDynamics(env.robot_id, i, linearDamping=0.1, angularDamping=0.1)

test_custom('Damping 0.10', high_damping)
