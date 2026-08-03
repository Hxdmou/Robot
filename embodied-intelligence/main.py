#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
机械臂仿真系统 - 统一入口
支持：训练 / 评估 / 部署 / 调试
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


def print_usage():
    print("=" * 60)
    print("  机械臂仿真系统 - 统一入口")
    print("=" * 60)
    print("")
    print("  用法: python main.py <命令> [参数]")
    print("")
    print("  可用命令:")
    print("    train           启动课程学习训练")
    print("    evaluate        评估模型泛化能力")
    print("    test            测试所有课程进度成功率")
    print("    deploy          启动部署模式（含真实机械臂对接）")
    print("    benchmark       性能基准测试（FPS等）")
    print("    smoke           回归测试套件（12项核心功能验证）")
    print("    api             启动REST API服务器（工业化接口）")
    print("    health          运行健康检查")
    print("    calibrate       启动参数校准")
    print("    monitor         启动实时监控")
    print("    gui             启动桌面GUI控制")
    print("    validate        验证部署就绪状态")
    print("    models          列出所有可用模型")
    print("    digital-twin    启动数字孪生系统")
    print("    remote          启动远程监控与运维")
    print("    agent           启动AI智能体自主决策")
    print("    edge            启动边缘计算部署")
    print("")
    print("  示例:")
    print("    python main.py train")
    print("    python main.py test")
    print("    python main.py evaluate")
    print("    python main.py api          # 启动API服务器: http://localhost:8000")
    print("    python main.py health       # 健康检查")
    print("    python main.py calibrate    # 参数校准")
    print("")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if command == "train":
        print("[INFO] 启动课程学习训练...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "train_curriculum.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "test":
        print("[INFO] 测试所有课程进度成功率（50轮/级）...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "test_final_all.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "evaluate":
        print("[INFO] 评估模型泛化能力...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "evaluate_generalization.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "deploy":
        print("[INFO] 启动部署模式...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "deploy_main.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "benchmark":
        print("[INFO] 性能基准测试...", flush=True)
        os.chdir(script_dir)
        import time
        import sys as _sys
        old_stderr = _sys.stderr
        _sys.stderr = open(os.devnull, "w")
        from stable_baselines3 import PPO
        from robot_reach_env_optimized import RobotReachEnvOptimized
        model = PPO.load("ppo_robot_reach_final_5m_enhanced", device="cpu")
        env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
        env.set_curriculum_progress(1.0)
        obs, _ = env.reset()
        start_time = time.time()
        n_steps = 2000
        for _ in range(n_steps):
            action, _ = model.predict(obs, deterministic=True)
            obs, _, term, trunc, _ = env.step(action)
            if term or trunc:
                obs, _ = env.reset()
        elapsed = time.time() - start_time
        fps = n_steps / elapsed
        _sys.stderr = old_stderr
        print("")
        print("=" * 50, flush=True)
        print("  性能基准测试结果", flush=True)
        print("=" * 50, flush=True)
        print("  总步数:      %d" % n_steps, flush=True)
        print("  总耗时:      %.2f 秒" % elapsed, flush=True)
        print("  FPS:         %.1f 步/秒" % fps, flush=True)
        print("  课程进度:    1.0 (最大强度 - 14个模块)", flush=True)
        print("  启用模块:    全部14大模块", flush=True)
        print("=" * 50, flush=True)
        env.close()

    elif command == "smoke":
        print("[INFO] 运行回归测试套件（12项核心功能验证）...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "test_smoke.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "api":
        print("[INFO] 启动REST API服务器...", flush=True)
        print("[INFO] API文档: http://localhost:8000/docs", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "api_server.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "health":
        print("[INFO] 运行健康检查...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "health_check.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "calibrate":
        print("[INFO] 启动参数校准...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "param_calibration.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "monitor":
        print("[INFO] 启动实时监控...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "realtime_monitor.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "gui":
        print("[INFO] 启动桌面GUI控制...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "robot_control_gui.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "validate":
        print("[INFO] 验证部署就绪状态...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "validate_model_for_deploy.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "models":
        print("[INFO] 列出所有可用模型...", flush=True)
        os.chdir(script_dir)
        models = []
        for f in sorted(os.listdir(script_dir)):
            if f.startswith("ppo_") and f.endswith(".zip"):
                path = os.path.join(script_dir, f)
                size_kb = round(os.path.getsize(path) / 1024, 1)
                models.append((f.replace(".zip", ""), size_kb))
        print("")
        print("=" * 50, flush=True)
        print(f"  可用模型: {len(models)} 个", flush=True)
        print("=" * 50, flush=True)
        for name, size in models:
            print(f"    ✅ {name}  ({size} KB)", flush=True)
        print("=" * 50, flush=True)

    elif command == "digital-twin":
        print("[INFO] 启动数字孪生系统...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "digital_twin_system.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "remote":
        print("[INFO] 启动远程监控与运维...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "remote_monitoring_system.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "agent":
        print("[INFO] 启动AI智能体自主决策...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "autonomous_decision_system.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command == "edge":
        print("[INFO] 启动边缘计算部署...", flush=True)
        os.chdir(script_dir)
        import subprocess
        result = subprocess.run([sys.executable, "edge_deployment_system.py"], capture_output=False)
        sys.exit(result.returncode)

    elif command in ["help", "-h", "--help"]:
        print_usage()

    else:
        print("[ERROR] 未知命令: %s" % command, flush=True)
        print("")
        print_usage()


if __name__ == "__main__":
    main()
