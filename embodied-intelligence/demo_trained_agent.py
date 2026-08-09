
import os
import sys

os.environ['PYBULLET_DISABLE_WARNINGS'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pybullet as p
import pybullet_data
import time
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

print("=" * 70)
print("  PPO Trained Robot Arm Demo - 5,000,000 Steps 0 Failure")
print("=" * 70)
print()

model_path = os.path.join(os.path.dirname(__file__), "ppo_robot_reach_ultimate2_final")
print(f"Loading model from: {model_path}")

try:
    model = PPO.load(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Trying alternative model path...")
    model_path = os.path.join(os.path.dirname(__file__), "ppo_robot_reach_stable_final")
    model = PPO.load(model_path)
    print(f"Loaded from: {model_path}")

print()
print("Starting simulation...")
print()
print("Controls:")
print("  Mouse Left Drag  - Rotate camera")
print("  Mouse Right Drag - Pan camera")
print("  Mouse Wheel      - Zoom")
print("  Close window     - Exit")
print()

env = RobotReachEnvOptimized(render_mode="human", max_steps=600)
env.domain_randomization = False
env.actuator_dynamics = False
env.external_disturbance = False

p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=50, cameraPitch=-35, cameraTargetPosition=[0.4, 0, 0.3])

episode_count = 0
success_count = 0
total_reward = 0

obs, info = env.reset()
episode_reward = 0
step_count = 0

success_text_id = None
episode_text_id = None
reward_text_id = None

print("Running inference... Press Ctrl+C or close window to exit.")
print()

try:
    while True:
        if not p.isConnected(env.physics_client):
            break
        
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        
        episode_reward += reward
        step_count += 1
        
        if success_text_id is not None:
            p.removeUserDebugItem(success_text_id)
        if episode_text_id is not None:
            p.removeUserDebugItem(episode_text_id)
        if reward_text_id is not None:
            p.removeUserDebugItem(reward_text_id)
        
        if info.get("is_success", False):
            success_text_id = p.addUserDebugText("SUCCESS!", [0.4, 0, 0.6], textColorRGB=[0, 1, 0], textSize=2.0)
        else:
            success_text_id = p.addUserDebugText(f"Dist: {info.get('distance', 0):.4f}", [0.4, 0, 0.6], textColorRGB=[1, 1, 0], textSize=1.5)
        
        episode_text_id = p.addUserDebugText(f"Episode: {episode_count} | Steps: {step_count}", [0.2, -0.4, 0.7], textColorRGB=[1, 1, 1], textSize=1.2)
        reward_text_id = p.addUserDebugText(f"Success: {success_count}/{episode_count} | Reward: {episode_reward:.0f}", [0.2, 0.4, 0.7], textColorRGB=[0.5, 1, 0.5], textSize=1.2)
        
        if terminated or truncated:
            episode_count += 1
            if info.get("is_success", False):
                success_count += 1
            total_reward += episode_reward
            
            print(f"Episode {episode_count}: {'SUCCESS' if info.get('is_success', False) else 'TIMEOUT'} | Steps: {step_count} | Success Rate: {success_count}/{episode_count} ({100*success_count/episode_count:.1f}%)")
            
            obs, info = env.reset()
            episode_reward = 0
            step_count = 0
            time.sleep(0.3)
        
        time.sleep(1.0 / 240.0)

except KeyboardInterrupt:
    pass
finally:
    if episode_count > 0:
        print()
        print("=" * 70)
        print(f"  Demo Summary")
        print(f"  Episodes: {episode_count}")
        print(f"  Successes: {success_count}")
        print(f"  Success Rate: {100*success_count/episode_count:.1f}%")
        print(f"  Avg Reward: {total_reward/episode_count:.0f}")
        print("=" * 70)
    
    env.close()
    print("\nDemo exited.")
