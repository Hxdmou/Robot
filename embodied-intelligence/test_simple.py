import sys
import os

print("Python:", sys.version)
print("CWD:", os.getcwd())

try:
    import pybullet as p
    print("PyBullet: OK")
except Exception as e:
    print("PyBullet FAIL:", e)

try:
    import gymnasium as gym
    print("Gymnasium: OK")
except Exception as e:
    print("Gymnasium FAIL:", e)

try:
    from stable_baselines3 import PPO
    print("SB3: OK")
except Exception as e:
    print("SB3 FAIL:", e)

sys.path.insert(0, r"f:\个人作品\具身智能\embodied-intelligence")
try:
    from robot_reach_env_optimized import RobotReachEnvOptimized
    print("Env import: OK")
except Exception as e:
    print("Env import FAIL:", e)
    import traceback
    traceback.print_exc()

print("DONE")
