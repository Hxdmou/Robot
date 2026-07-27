import sys, os

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import numpy as np
import pybullet as p
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')

# 测试1: Progress 0.30，但禁用reset中的领域随机化
sys.stderr = open(os.devnull, 'w')

class TestEnv1(RobotReachEnvOptimized):
    def reset(self, seed=None, options=None):
        # 先调用父类reset
        obs, info = super().reset(seed=seed, options=options)
        # 强制覆盖：不做任何领域随机化
        p.setGravity(0, 0, -9.81)
        return obs, info

test_env = TestEnv1(render_mode=None, max_steps=600)
test_env.set_curriculum_progress(0.30)
success_count = 0
for i in range(30):
    obs, info = test_env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = test_env.step(action)
        done = terminated or truncated
    success_count += 1 if terminated else 0
sys.stderr = old_stderr
print(f'Test 1 (prog 0.30, NO domain rand): Success {success_count}/30', flush=True)

# 测试2: Progress 0.0，但启用领域随机化（用Progress 0.30的参数）
sys.stderr = open(os.devnull, 'w')

class TestEnv2(RobotReachEnvOptimized):
    def reset(self, seed=None, options=None):
        import random
        # 先调用父类reset（会做progress=0.0的处理，即不做领域随机化）
        obs, info = super().reset(seed=seed, options=options)
        # 手动应用Progress 0.30的领域随机化参数
        friction_min, friction_max = 0.985, 1.015
        damping_min, damping_max = 0.047, 0.053
        gravity_min, gravity_max = -9.819, -9.801
        p.setGravity(0, 0, random.uniform(gravity_min, gravity_max))
        for i in range(7):
            p.changeDynamics(self.robot_id, i,
                           linearDamping=random.uniform(damping_min, damping_max),
                           angularDamping=random.uniform(damping_min, damping_max),
                           lateralFriction=random.uniform(friction_min, friction_max))
        return obs, info

test_env2 = TestEnv2(render_mode=None, max_steps=600)
test_env2.set_curriculum_progress(0.0)  # 保持step()中不应用执行器动力学
success_count2 = 0
for i in range(30):
    obs, info = test_env2.reset()
    done = False
    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = test_env2.step(action)
        done = terminated or truncated
    success_count2 += 1 if terminated else 0
sys.stderr = old_stderr
print(f'Test 2 (prog 0.0, MANUAL prog0.30 rand): Success {success_count2}/30', flush=True)
