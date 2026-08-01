
if __name__ == '__main__':
    """
    课程学习各进度成功率全面验证
    """
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


    import sys
    import os

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "embodied-intelligence"))
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "embodied-intelligence"))

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
