
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

import sys, os, traceback
old_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from stable_baselines3 import PPO
from robot_reach_env_optimized import RobotReachEnvOptimized
import pybullet as p

model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')
test_env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
test_env.set_curriculum_progress(1.0)
obs, info = test_env.reset()
sys.stderr = old_stderr

action, _ = model.predict(obs, deterministic=True)

# 手动逐步执行step的代码
import numpy as np
action_scaled = np.clip(action, -1.0, 1.0) * test_env.action_scale
print('Step A: action scaled OK', flush=True)

# 通信延迟缓冲
if test_env.curriculum_progress >= 0.8 and test_env.command_delay_steps > 0:
    test_env._command_buffer.append(action_scaled.copy())
    if len(test_env._command_buffer) > test_env.command_delay_steps:
        actual_action = test_env._command_buffer.pop(0)
    else:
        actual_action = action_scaled.copy()
else:
    actual_action = action_scaled
print('Step B: command buffer OK, delay_steps=%d' % test_env.command_delay_steps, flush=True)

# 死区处理
if test_env.curriculum_progress >= 0.4:
    actual_action = np.where(np.abs(actual_action) < test_env.dead_zone, 0, actual_action)
print('Step C: dead zone OK', flush=True)

states = p.getJointStates(test_env.robot_id, range(7))
current_positions = np.array([s[0] for s in states])
print('Step D: getJointStates OK', flush=True)

target_positions = current_positions + actual_action
if test_env.curriculum_progress >= 0.4:
    delta_pos = actual_action
    max_delta = test_env.velocity_limit * (1 / 240.0)
    delta_pos = np.clip(delta_pos, -max_delta, max_delta)
    target_positions = current_positions + delta_pos
print('Step E: velocity limit OK', flush=True)

for i in range(7):
    force = test_env.torque_limit if test_env.curriculum_progress >= 0.4 else 240
    p.setJointMotorControl2(test_env.robot_id, i, p.POSITION_CONTROL, targetPosition=target_positions[i], force=force)
print('Step F: setMotor OK', flush=True)

p.stepSimulation()
print('Step G: stepSimulation OK', flush=True)

# 外部扰动
if test_env.curriculum_progress >= 0.6:
    if test_env.np_random.random() < test_env.disturbance_prob:
        disturbance = test_env.np_random.uniform(-test_env.disturbance_magnitude, test_env.disturbance_magnitude, size=3)
        p.applyExternalForce(test_env.robot_id, 6, forceObj=disturbance, posObj=np.array(p.getLinkState(test_env.robot_id, 6)[0]), flags=p.WORLD_FRAME)
print('Step H: disturbance OK', flush=True)

test_env.step_count += 1
obs2 = test_env._get_obs()
print('Step I: get_obs OK', flush=True)

# 状态缓冲
if test_env.curriculum_progress >= 0.8 and test_env.state_delay_steps > 0:
    test_env._state_buffer.append(obs2.copy())
    if len(test_env._state_buffer) > test_env.state_delay_steps:
        obs2 = test_env._state_buffer.pop(0)
print('Step J: state buffer OK', flush=True)

ee_pos = np.array(p.getLinkState(test_env.robot_id, 6)[0])
print('Step K: getLinkState OK', flush=True)

# 碰撞检测
if test_env.curriculum_progress >= 0.5 and test_env.collision_penalty > 0:
    print('Step L: checking contacts...', flush=True)
    contacts = p.getContactPoints(test_env.robot_id, -1, -1, -1, 10)
    print('Step L2: contacts=%d' % len(contacts), flush=True)
print('Step M: ALL PASSED!', flush=True)
