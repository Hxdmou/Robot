
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
try:
    print('Step 1: Import modules...', flush=True)
    from stable_baselines3 import PPO
    from robot_reach_env_optimized import RobotReachEnvOptimized
    print('Step 2: Load model...', flush=True)
    model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')
    print('Step 3: Create env...', flush=True)
    old_stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    test_env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
    sys.stderr = old_stderr
    print('Step 4: Set progress 1.0...', flush=True)
    test_env.set_curriculum_progress(1.0)
    print('Step 5: Reset...', flush=True)
    old_stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    obs, info = test_env.reset()
    sys.stderr = old_stderr
    print('Step 6: obs shape:', obs.shape, flush=True)
    print('Step 7: Predict...', flush=True)
    action, _ = model.predict(obs, deterministic=True)
    print('Step 8: Step...', flush=True)
    old_stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    obs, reward, term, trunc, _ = test_env.step(action)
    sys.stderr = old_stderr
    print('Step 9: Done! reward=%.2f term=%s trunc=%s' % (reward, term, trunc), flush=True)
except Exception as e:
    print('ERROR:', str(e), flush=True)
    traceback.print_exc()
