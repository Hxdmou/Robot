#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
机械臂仿真系统 - 统一入口
支持：训练 / 评估 / 部署 / 调试
"""

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
    print("")
    print("  示例:")
    print("    python main.py train")
    print("    python main.py test")
    print("    python main.py evaluate")
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
        exec(open("train_curriculum.py", encoding="utf-8").read())

    elif command == "test":
        print("[INFO] 测试所有课程进度成功率（50轮/级）...", flush=True)
        os.chdir(script_dir)
        exec(open("test_final_all.py", encoding="utf-8").read())

    elif command == "evaluate":
        print("[INFO] 评估模型泛化能力...", flush=True)
        os.chdir(script_dir)
        exec(open("evaluate_generalization.py", encoding="utf-8").read())

    elif command == "deploy":
        print("[INFO] 启动部署模式...", flush=True)
        os.chdir(script_dir)
        exec(open("deploy_main.py", encoding="utf-8").read())

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
        n_steps = 1000
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
        print("  课程进度:    1.0 (最大强度)", flush=True)
        print("  启用模块:    全部8大模块", flush=True)
        print("=" * 50, flush=True)
        env.close()

    elif command == "smoke":
        print("[INFO] 运行回归测试套件（12项核心功能验证）...", flush=True)
        os.chdir(script_dir)
        exec(open("test_smoke.py", encoding="utf-8").read())

    elif command in ["help", "-h", "--help"]:
        print_usage()

    else:
        print("[ERROR] 未知命令: %s" % command, flush=True)
        print("")
        print_usage()


if __name__ == "__main__":
    main()
