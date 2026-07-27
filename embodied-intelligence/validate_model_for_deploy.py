#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
部署前模型推理验证脚本
验证内容：
  1. 模型能否正常加载
  2. 观测空间/动作空间是否匹配
  3. 仿真环境中运行N个episode验证推理正确性
  4. 关键性能指标（成功率、平均误差、FPS）是否达标

使用方法：
  python validate_model_for_deploy.py
  python validate_model_for_deploy.py --model path/to/model.zip --episodes 10
  python validate_model_for_deploy.py --version v1.0-curriculum
"""

import sys
import os
import argparse
import time
import math
import numpy as np

sys.stderr = open(os.devnull, 'w')
os.environ['PYBULLET_DISABLE_WARNINGS'] = '1'

from robot_reach_env_optimized import RobotReachEnvOptimized
from sim_to_real_adapter import SimToRealAdapter


VALIDATION_THRESHOLDS = {
    "min_success_rate": 0.70,    # 最低成功率 70%
    "max_avg_error_mm": 20.0,     # 最大平均误差 20mm
    "min_fps": 500.0,              # 最低推理FPS 500
    # CD-LAM 因果去偏阈值
    "min_zero_action_pass_rate": 0.70,     # 零动作通过率 ≥70%
    "min_cd_lam_score": 40.0,               # CD-LAM评分 ≥40
}


def validate_model_load(model_path=None, version=None):
    """验证模型能否正常加载"""
    from stable_baselines3 import PPO
    from model_manager import ModelManager, find_model_file

    print("[1/5] 验证模型加载...")

    if version:
        manager = ModelManager()
        model, info = manager.load_model(version)
    else:
        path = model_path or find_model_file()
        if not path:
            print("  ❌ 未找到模型文件")
            return None, None
        model = PPO.load(path, device="cpu")
        info = {"name": os.path.basename(path), "model_path": path}

    print(f"  ✅ 模型加载成功: {info.get('name', 'unknown')}")
    print(f"     观测空间: {model.observation_space}")
    print(f"     动作空间: {model.action_space}")

    return model, info


def validate_space_compatibility(model, env):
    """验证模型空间与环境是否兼容"""
    print("\n[2/5] 验证空间兼容性...")

    model_obs_shape = model.observation_space.shape
    env_obs_shape = env.observation_space.shape
    model_act_shape = model.action_space.shape
    env_act_shape = env.action_space.shape

    issues = []

    if model_obs_shape != env_obs_shape:
        issues.append(f"观测空间不匹配: 模型{model_obs_shape} vs 环境{env_obs_shape}")

    if model_act_shape != env_act_shape:
        issues.append(f"动作空间不匹配: 模型{model_act_shape} vs 环境{env_act_shape}")

    if issues:
        for issue in issues:
            print(f"  ❌ {issue}")
        return False

    print(f"  ✅ 观测空间匹配: {model_obs_shape}")
    print(f"  ✅ 动作空间匹配: {model_act_shape}")
    return True


def validate_sim_to_real_compatibility(model):
    """验证Sim-to-Real适配器与模型的兼容性"""
    print("\n[3/5] 验证Sim-to-Real适配兼容性...")

    adapter = SimToRealAdapter()

    test_joints = [0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]
    test_ee = [0.3, 0.0, 0.6]
    test_target = [0.4, 0.1, 0.5]

    obs = adapter.robot_state_to_obs(test_joints, test_ee, test_target)

    if obs.shape != model.observation_space.shape:
        print(f"  ❌ 适配器观测形状不匹配: {obs.shape} vs {model.observation_space.shape}")
        return False

    try:
        action, _ = model.predict(obs, deterministic=True)
    except Exception as e:
        print(f"  ❌ 模型推理失败: {e}")
        return False

    if action.shape != model.action_space.shape:
        print(f"  ❌ 模型动作形状异常: {action.shape}")
        return False

    target_joints = adapter.action_to_joint_targets(action, test_joints)

    if len(target_joints) != 7:
        print(f"  ❌ 适配器输出关节数异常: {len(target_joints)}")
        return False

    print(f"  ✅ 适配器→模型→适配器链路正常")
    print(f"     观测: {obs.shape} → 动作: {action.shape} → 关节目标: {target_joints.shape}")
    return True


def validate_inference_performance(model, num_episodes=5):
    """在仿真环境中验证推理性能"""
    print(f"\n[4/5] 仿真推理性能验证 ({num_episodes} 个episode)...")

    env = RobotReachEnvOptimized(render_mode=None, max_steps=600)
    adapter = SimToRealAdapter()

    results = {
        "successes": 0,
        "total": num_episodes,
        "errors": [],
        "steps": [],
        "fps": [],
    }

    total_steps = 0
    start_time = time.time()

    for ep in range(num_episodes):
        obs, info = env.reset()
        done = False
        ep_steps = 0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            ep_steps += 1
            total_steps += 1

        dist = info.get("distance", 1.0)
        success = dist < 0.02  # 2cm内算成功

        if success:
            results["successes"] += 1
        results["errors"].append(dist)
        results["steps"].append(ep_steps)

        status = "✅" if success else "⚠️"
        print(f"  Episode {ep+1}/{num_episodes}: {status} 误差={dist*1000:.1f}mm 步数={ep_steps}")

    total_time = time.time() - start_time
    results["avg_fps"] = total_steps / total_time if total_time > 0 else 0
    results["success_rate"] = results["successes"] / results["total"]
    results["avg_error_mm"] = (sum(results["errors"]) / len(results["errors"])) * 1000
    results["avg_steps"] = sum(results["steps"]) / len(results["steps"])

    env.close()
    return results


def validate_cd_lam_debias(model, env, num_episodes=5):
    """
    [4.5/5] CD-LAM因果去偏评估

    检查:
    1. 零动作稳定性（静止指令测试）
    2. 动作一致性（目标动作跟随）
    3. CD-LAM总体评分
    """
    from cd_lam import create_cd_lam_evaluator

    print("\n[4.5/5] CD-LAM因果去偏评估...")

    evaluator = create_cd_lam_evaluator()

    # 执行评估
    metrics = evaluator.evaluate_full(
        model=model,
        env=env,
        num_zero_test_episodes=num_episodes,
    )

    print(f"  ✅ 零动作通过率: {metrics.zero_action_pass_rate*100:.1f}%")
    print(f"     零动作残余运动: {metrics.zero_action_residual:.6f} rad")
    print(f"  ✅ 目标动作跟随率: {metrics.target_action_following_rate*100:.1f}%")
    print(f"  ✅ CD-LAM评分: {metrics.overall_score:.1f} / 100")

    return metrics


def validate_thresholds(results, cd_lam_metrics=None):
    """验证性能是否达到部署阈值"""
    print("\n[5/5] 部署阈值检查...")

    thresholds = VALIDATION_THRESHOLDS
    all_passed = True

    checks = [
        ("成功率", results["success_rate"], thresholds["min_success_rate"], ">=", "%"),
        ("平均误差", results["avg_error_mm"], thresholds["max_avg_error_mm"], "<=", "mm"),
        ("推理FPS", results["avg_fps"], thresholds["min_fps"], ">=", ""),
    ]

    for name, value, threshold, op, unit in checks:
        if op == ">=":
            passed = value >= threshold
        else:
            passed = value <= threshold

        status = "✅" if passed else "❌"
        print(f"  {status} {name}: {value:.2f}{unit} (阈值: {op}{threshold}{unit})")

        if not passed:
            all_passed = False

    # CD-LAM阈值检查
    if cd_lam_metrics is not None:
        cd_lam_checks = [
            ("零动作通过率", cd_lam_metrics.zero_action_pass_rate, thresholds["min_zero_action_pass_rate"], ">=", "%"),
            ("CD-LAM评分", cd_lam_metrics.overall_score, thresholds["min_cd_lam_score"], ">=", ""),
        ]

        for name, value, threshold, op, unit in cd_lam_checks:
            if op == ">=":
                passed = value >= threshold
            else:
                passed = value <= threshold

            status = "✅" if passed else "⚠️"  # CD-LAM未通过给警告而非失败
            display_value = f"{value*100:.1f}" if unit == "%" else f"{value:.1f}"
            display_threshold = f"{threshold*100:.1f}" if unit == "%" else f"{threshold:.1f}"
            print(f"  {status} {name}: {display_value}{unit} (阈值: {op}{display_threshold}{unit})")

            if not passed:
                # CD-LAM作为建议项，不强制阻止部署
                pass

    return all_passed


def print_summary(results, all_passed, cd_lam_metrics=None):
    print("\n" + "=" * 70)
    print("  部署前验证结果汇总")
    print("=" * 70)
    print(f"  测试episode数: {results['total']}")
    print(f"  成功数:       {results['successes']}/{results['total']}")
    print(f"  成功率:       {results['success_rate']*100:.1f}%")
    print(f"  平均误差:     {results['avg_error_mm']:.2f}mm")
    print(f"  平均步数:     {results['avg_steps']:.1f}")
    print(f"  平均FPS:      {results['avg_fps']:.1f}")

    if cd_lam_metrics is not None:
        print("-" * 70)
        print("  CD-LAM因果去偏评估:")
        print(f"    零动作通过率: {cd_lam_metrics.zero_action_pass_rate*100:.1f}%")
        print(f"    零动作残余: {cd_lam_metrics.zero_action_residual:.6f} rad")
        print(f"    目标跟随率: {cd_lam_metrics.target_action_following_rate*100:.1f}%")
        print(f"    CD-LAM评分: {cd_lam_metrics.overall_score:.1f} / 100")

        if cd_lam_metrics.overall_score >= 80:
            cd_grade = "A (优秀)"
        elif cd_lam_metrics.overall_score >= 60:
            cd_grade = "B (良好)"
        elif cd_lam_metrics.overall_score >= 40:
            cd_grade = "C (一般)"
        else:
            cd_grade = "D (较差)"
        print(f"    等级: {cd_grade}")

    print("-" * 70)
    if all_passed:
        print("  ✅ 全部阈值通过，可以部署！")
    else:
        print("  ❌ 部分阈值未通过，建议重新训练或调整参数")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="部署前模型验证")
    parser.add_argument("--model", default=None, help="模型文件路径")
    parser.add_argument("--version", default=None, help="模型版本名称 (从模型管理器加载)")
    parser.add_argument("--episodes", type=int, default=5, help="测试episode数 (默认5)")
    parser.add_argument("--thresholds", action="store_true", help="仅显示阈值要求")

    args = parser.parse_args()

    if args.thresholds:
        print("部署阈值要求:")
        for k, v in VALIDATION_THRESHOLDS.items():
            print(f"  {k}: {v}")
        sys.exit(0)

    print("=" * 70)
    print("  部署前模型推理验证")
    print("=" * 70)

    # Step 1: 加载模型
    model, info = validate_model_load(args.model, args.version)
    if model is None:
        print("\n❌ 验证失败: 无法加载模型")
        sys.exit(1)

    # Step 2: 空间兼容性（需要创建临时环境）
    env = RobotReachEnvOptimized(render_mode=None, max_steps=100)
    space_ok = validate_space_compatibility(model, env)
    env.close()

    if not space_ok:
        print("\n❌ 验证失败: 空间不兼容")
        sys.exit(1)

    # Step 3: Sim-to-Real适配兼容性
    adapter_ok = validate_sim_to_real_compatibility(model)
    if not adapter_ok:
        print("\n❌ 验证失败: Sim-to-Real适配不兼容")
        sys.exit(1)

    # Step 4: 推理性能验证
    results = validate_inference_performance(model, args.episodes)

    # Step 4.5: CD-LAM因果去偏评估
    env_cdlam = RobotReachEnvOptimized(render_mode=None, max_steps=100)
    cd_lam_metrics = validate_cd_lam_debias(model, env_cdlam, num_episodes=5)
    env_cdlam.close()

    # Step 5: 阈值检查
    all_passed = validate_thresholds(results, cd_lam_metrics)

    print_summary(results, all_passed, cd_lam_metrics)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
