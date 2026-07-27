import sys, os
old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')
test_env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
test_env.set_curriculum_progress(1.0)
success_count = 0
for i in range(10):
    obs, info = test_env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, term, trunc, _ = test_env.step(action)
        done = term or trunc
    success_count += 1 if term else 0
sys.stderr = old_stderr
print('Progress 1.0: %d/10 success' % success_count, flush=True)
print('noise_std=%.5f coll_pen=%.1f cmd_delay=%d' % (
    test_env.noise_gaussian_std, test_env.collision_penalty, test_env.command_delay_steps
), flush=True)
