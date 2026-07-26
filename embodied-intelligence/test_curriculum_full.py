"""
课程学习各进度成功率全面验证
"""
import sys
import os

os.chdir(r"f:\个人作品\具身智能\embodied-intelligence")
sys.path.insert(0, r"f:\个人作品\具身智能\embodied-intelligence")

old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
os.environ['PYBULLET_DISABLE_WARNINGS'] = '1'

from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

sys.stderr = old_stderr
print("=" * 70)
print("  FULL CURRICULUM SUCCESS RATE VALIDATION")
print("=" * 70)

sys.stderr = open(os.devnull, 'w')
model = PPO.load("ppo_robot_reach_final_5m_enhanced", device="cpu")
sys.stderr = old_stderr

progress_levels = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
all_ok = True

for progress in progress_levels:
    sys.stderr = open(os.devnull, 'w')
    env = RobotReachEnvOptimized(render_mode=None, max_steps=800)
    env.set_curriculum_progress(progress)
    
    success = 0
    total_r = 0.0
    
    for i in range(50):
        obs, _ = env.reset()
        done = False
        ep_r = 0.0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, r, term, trunc, _ = env.step(action)
            ep_r += r
            done = term or trunc
        total_r += ep_r
        success += 1 if term else 0
    
    env.close()
    rate = success / 50 * 100
    avg_r = total_r / 50
    ok = rate >= 100.0
    if not ok:
        all_ok = False
    
    sys.stderr = old_stderr
    status = "[OK]" if ok else "[FAIL]"
    print(f"  Progress {progress:3.1f}:  Success {success}/50 ({rate:5.1f}%)  AvgReward {avg_r:10.2f}  {status}")

print("\n" + "=" * 70)
if all_ok:
    print("  [PASS] ALL CURRICULUM LEVELS - 100% SUCCESS RATE!")
else:
    print("  [FAIL] Some curriculum levels failed!")
print("=" * 70)
