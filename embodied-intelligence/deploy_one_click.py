#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一键部署脚本（支持真实机械臂 / 仿真模式）

使用方法：
  # 仿真模式（默认）
  python deploy_one_click.py

  # 真实机械臂模式
  python deploy_one_click.py --mode real

  # 使用轨迹模式（不用模型）
  python deploy_one_click.py --execution trajectory

  # 只运行验证检查
  python deploy_one_click.py --check-only

部署前验证清单（自动运行）：
  ✅ Python 环境依赖
  ✅ 模型文件存在
  ✅ 配置文件正确
  ✅ (真实模式) 网络连通
  ✅ (真实模式) 机械臂IP可达
"""

import os
import sys
import argparse
import importlib
import socket
import time


CHECKLIST = {
    "python_version": {"name": "Python 版本 (>=3.8)", "passed": False, "detail": ""},
    "pybullet": {"name": "PyBullet 库", "passed": False, "detail": ""},
    "stable_baselines3": {"name": "Stable-Baselines3 库", "passed": False, "detail": ""},
    "numpy": {"name": "NumPy 库", "passed": False, "detail": ""},
    "config_file": {"name": "配置文件 (robot_config.py)", "passed": False, "detail": ""},
    "model_file": {"name": "模型文件 (PPO)", "passed": False, "detail": ""},
    "network": {"name": "(真实模式) 网络连通", "passed": None, "detail": "N/A (仿真模式)"},
    "robot_ip": {"name": "(真实模式) 机械臂IP可达", "passed": None, "detail": "N/A (仿真模式)"},
}


def check_python_version():
    ver = sys.version_info
    ok = ver.major >= 3 and ver.minor >= 8
    CHECKLIST["python_version"]["passed"] = ok
    CHECKLIST["python_version"]["detail"] = f"{ver.major}.{ver.minor}.{ver.micro}"
    return ok


def check_library(name, import_name=None):
    import_name = import_name or name
    try:
        importlib.import_module(import_name)
        mod = sys.modules[import_name]
        version = getattr(mod, "__version__", "unknown")
        CHECKLIST[name]["passed"] = True
        CHECKLIST[name]["detail"] = f"v{version}"
        return True
    except ImportError as e:
        CHECKLIST[name]["passed"] = False
        CHECKLIST[name]["detail"] = f"未安装: {e}"
        return False


def check_config_file():
    path = os.path.join(os.path.dirname(__file__), "robot_config.py")
    ok = os.path.exists(path)
    CHECKLIST["config_file"]["passed"] = ok
    CHECKLIST["config_file"]["detail"] = path if ok else "缺失"
    return ok


def check_model_file():
    model_names = [
        "ppo_robot_reach_curriculum",
        "ppo_robot_reach_curriculum.zip",
        "ppo_robot_reach_stable_final",
        "ppo_robot_reach_stable_final.zip",
        "ppo_robot_reach_final_5m_enhanced",
        "ppo_robot_reach_final_5m_enhanced.zip",
    ]
    base_dirs = [
        os.path.dirname(__file__),
        r"f:\个人作品\具身智能",
    ]
    found = None
    for base in base_dirs:
        for name in model_names:
            full = os.path.join(base, name)
            if os.path.exists(full):
                found = full
                break
        if found:
            break

    CHECKLIST["model_file"]["passed"] = found is not None
    CHECKLIST["model_file"]["detail"] = found if found else "未找到（将使用轨迹模式）"
    return found is not None


def check_network(host, port, timeout=3.0):
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        latency = (time.time() - start) * 1000

        if result == 0:
            CHECKLIST["network"]["passed"] = True
            CHECKLIST["network"]["detail"] = f"延迟 {latency:.1f}ms"
            return True
        else:
            CHECKLIST["network"]["passed"] = False
            CHECKLIST["network"]["detail"] = f"端口{port}未开放"
            return False
    except Exception as e:
        CHECKLIST["network"]["passed"] = False
        CHECKLIST["network"]["detail"] = f"异常: {e}"
        return False


def check_robot_ip(host, timeout=2.0):
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, 8080))
        sock.close()
        latency = (time.time() - start) * 1000

        if result == 0:
            CHECKLIST["robot_ip"]["passed"] = True
            CHECKLIST["robot_ip"]["detail"] = f"{host}:8080 可达 ({latency:.1f}ms)"
            return True
        else:
            # 尝试ping（通过socket测试常见端口）
            for p in [22, 80, 443]:
                try:
                    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s2.settimeout(0.5)
                    r2 = s2.connect_ex((host, p))
                    s2.close()
                    if r2 == 0:
                        CHECKLIST["robot_ip"]["passed"] = True
                        CHECKLIST["robot_ip"]["detail"] = f"{host} 可达 (端口{p})"
                        return True
                except:
                    pass
            CHECKLIST["robot_ip"]["passed"] = False
            CHECKLIST["robot_ip"]["detail"] = f"{host} 不可达"
            return False
    except Exception as e:
        CHECKLIST["robot_ip"]["passed"] = False
        CHECKLIST["robot_ip"]["detail"] = f"异常: {e}"
        return False


def run_checklist(mode, robot_host=None, robot_port=8080):
    print("=" * 70)
    print("  部署前验证清单")
    print("=" * 70)

    check_python_version()
    check_library("pybullet")
    check_library("stable_baselines3", "stable_baselines3")
    check_library("numpy")
    check_config_file()
    check_model_file()

    # 新增：安全参数完整性验证
    try:
        from deploy_tools import SafetyParameterValidator
        validator = SafetyParameterValidator()
        safety_ok, safety_issues = validator.validate_all()
        CHECKLIST["safety_params"] = {
            "name": "安全参数完整性",
            "passed": safety_ok,
            "detail": f"发现{len(safety_issues)}个问题" if not safety_ok else "全部通过"
        }
        if safety_issues:
            for issue in safety_issues[:3]:
                print(f"    ⚠️  {issue}")
    except Exception as e:
        CHECKLIST["safety_params"] = {
            "name": "安全参数完整性",
            "passed": False,
            "detail": f"验证异常: {e}"
        }

    if mode == "real":
        host = robot_host or "192.168.3.100"
        check_robot_ip(host)
        if CHECKLIST["robot_ip"]["passed"]:
            check_network(host, robot_port)
    else:
        CHECKLIST["network"]["passed"] = None
        CHECKLIST["network"]["detail"] = "N/A (仿真模式)"
        CHECKLIST["robot_ip"]["passed"] = None
        CHECKLIST["robot_ip"]["detail"] = "N/A (仿真模式)"

    passed = 0
    total = 0
    for key, item in CHECKLIST.items():
        total += 1
        status = "✅" if item["passed"] is True else ("⚠️" if item["passed"] is None else "❌")
        if item["passed"] is True:
            passed += 1
        print(f"  {status} {item['name']:35s} {item['detail']}")

    print("-" * 70)
    print(f"  通过: {passed}/{total}")

    critical_fails = ["python_version", "pybullet", "numpy", "config_file"]
    critical_ok = all(CHECKLIST[k]["passed"] for k in critical_fails)

    if mode == "real":
        critical_ok = critical_ok and CHECKLIST["robot_ip"]["passed"]

    if critical_ok:
        print("  结果: ✅ 可以部署")
    else:
        print("  结果: ❌ 关键项未通过，请检查")

    print("=" * 70)
    return critical_ok


def print_quick_start_guide(mode):
    print("\n" + "=" * 70)
    print("  快速上手指南")
    print("=" * 70)

    if mode == "sim":
        print("""
  【仿真模式】

  1. 启动部署（已自动完成验证）:
     python deploy_one_click.py

  2. 观察GUI窗口中的机械臂运动
     - 默认使用PPO模型推理执行任务
     - 可以按 Ctrl+C 安全退出

  3. 切换到轨迹模式（不使用模型）:
     python deploy_one_click.py --execution trajectory

  4. 训练新模型:
     python train_curriculum.py
""")
    else:
        print("""
  【真实机械臂模式】

  部署前准备：
  1. 确保机械臂已通电并连接到同一网络
  2. 确认机械臂IP地址（在 robot_config.py 中配置）
  3. 确认周围无障碍物，机械臂工作空间内无人员
  4. 手边有急停按钮或可以随时断电

  启动步骤：
  1. 先运行网络验证:
     python deploy_one_click.py --mode real --check-only

  2. 确认所有检查通过后启动部署:
     python deploy_one_click.py --mode real

  3. 如遇问题立即断电或按急停

  安全说明：
  - 所有关节目标会自动裁剪到安全范围
  - 超过工作空间或力限制会自动停止
  - 可以随时按 Ctrl+C 安全退出
""")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="一键部署脚本（支持多种真实机械臂）")
    parser.add_argument("--mode", choices=["sim", "real"], default="sim",
                        help="部署模式: sim=仿真(默认), real=真实机械臂")
    parser.add_argument("--execution", choices=["model", "trajectory"], default="model",
                        help="执行模式: model=模型推理(默认), trajectory=轨迹插值")
    parser.add_argument("--arm", default=None,
                        help="机械臂型号key (如: franka_panda, ur_ur5e, kuka_iiwa14, abb_yumi, dobot_magician)")
    parser.add_argument("--check-level", choices=["minimal", "standard", "strict"], default="standard",
                        help="部署前检查级别 (默认: standard)")
    parser.add_argument("--list-arms", action="store_true",
                        help="列出所有支持的机械臂型号")
    parser.add_argument("--host", default=None, help="机械臂IP地址（真实模式）")
    parser.add_argument("--port", type=int, default=8080, help="机械臂端口（真实模式）")
    parser.add_argument("--check-only", action="store_true", help="只运行验证检查，不启动部署")
    parser.add_argument("--no-guide", action="store_true", help="不显示快速上手指南")

    args = parser.parse_args()

    # 列出支持的机械臂
    if args.list_arms:
        from robot_arm_db import RobotArmDB
        db = RobotArmDB()
        db.print_all_summaries()
        sys.exit(0)

    # 选择机械臂型号
    arm_key = args.arm or "franka_panda"
    if not args.arm and args.mode == "real":
        # 真实模式下提示选择
        from robot_arm_db import RobotArmDB
        db = RobotArmDB()
        print("\n请选择机械臂型号（默认 franka_panda）：")
        arms = db.list_available_arms()
        for i, key in enumerate(arms, 1):
            s = db.get_summary(key)
            print(f"  {i}. {key} ({s['brand']} {s['model']}, {s['dof']}轴)")
        try:
            choice = input("\n请输入编号 (默认1): ").strip()
            if choice and int(choice) >= 1 and int(choice) <= len(arms):
                arm_key = arms[int(choice) - 1]
        except:
            pass
    print(f"\n[DEPLOY] 目标机械臂: {arm_key}")

    # ========== 1. 运行部署前检查（使用新的动态检查器） ==========
    from deploy_adapters import run_deployment_preflight
    ok = run_deployment_preflight(
        arm_key=arm_key,
        check_level=args.check_level,
        host=args.host,
        port=args.port,
        interactive=not args.no_guide
    )

    # 同时运行原有清单（向后兼容）
    run_checklist(args.mode, args.host, args.port)

    if args.check_only:
        sys.exit(0 if ok else 1)

    if not ok:
        print("\n❌ 关键验证项未通过，已中止部署")
        print("   请修复上述问题后重新运行")
        sys.exit(1)

    # ========== 2. 显示上手指南 ==========
    if not args.no_guide:
        print_quick_start_guide(args.mode)
        print("\n5秒后自动启动部署（按 Ctrl+C 取消）...")
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n已取消")
            sys.exit(0)

    # ========== 3. 修改配置并启动部署 ==========
    print(f"\n🚀 启动部署 (模式: {args.mode}, 执行: {args.execution})")

    # 动态修改 robot_config.py 的配置
    sys.path.insert(0, os.path.dirname(__file__))
    import robot_config
    robot_config.ROBOT_MODE = args.mode
    if args.host:
        robot_config.REAL_ROBOT_CONFIG["host"] = args.host
        robot_config.REAL_ROBOT_CONFIG["port"] = args.port

    # 启动 deploy_main
    os.chdir(os.path.dirname(__file__))

    # 由于 deploy_main 读取的是模块级配置，需要在导入前设置环境变量
    os.environ["DEPLOY_MODE"] = args.mode
    os.environ["DEPLOY_EXECUTION"] = args.execution

    from deploy_main import init_environment, run_calibration, deploy_loop, cleanup

    try:
        config = init_environment(execution_mode=args.execution)
        if config is None:
            print("❌ 环境初始化失败")
            sys.exit(1)

        run_calibration(config)
        deploy_loop(config)
    except KeyboardInterrupt:
        print("\n用户中断")
    finally:
        cleanup()
        sys.exit(0)


if __name__ == "__main__":
    main()
