#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyBullet 真机部署级测试脚本（Realistic Sim-to-Real Testing）
================================================================
在没有真机的情况下，通过在PyBullet中叠加100%强度的5大真实世界模拟器，
对训练好的模型进行【真实部署级别】的验证。

5大Sim-to-Real增强模块（100%强度全开）：
  1. 域随机化 - 摩擦0.1~1.0 / 阻尼0.02~0.3 / 质量±15% / 增益±20% / 重力±0.2m/s²
  2. 通信延迟 - 控制8ms + 状态5ms + 网络15ms抖动 + 指令缓冲区5条
  3. 执行器动力学 - 扭矩上限50N·m / 速度3rad/s / 加速度10rad/s² / 10ms低通 / 死区 / 摩擦
  4. 外部扰动 - 周期力5N / 随机冲击力1~10N / 负载变化0~3kg / 50Hz地面振动
  5. 传感器噪声 - 关节角度1mrad / 末端位置1mm / 力矩0.05N·m

测试维度（9大维度 × 50 episodes = 450轮综合测试）：
  A. 基线（0%真实度）- 成功率参考
  B. 纯域随机化 - 物理参数不确定性
  C. 纯通信延迟 - 控制周期/网络
  D. 纯执行器限制 - 电机物理边界
  E. 纯外部扰动 - 环境干扰
  F. 纯传感器噪声 - 感知不确定性
  G. 综合50%真实度 - 中度真实条件
  H. 综合100%真实度 - 真实部署等价环境
  I. 极端强度120% - 超出真实环境的鲁棒性测试（合格≥60%）

合格标准（真机就绪判定）：
  ✅ 100%真实度（H类）成功率 ≥ 80%
  ✅ 120%极端强度（I类）成功率 ≥ 60%
  ✅ 5大单项模块（B~F类）平均成功率 ≥ 85%
  ✅ 平均每episode用时不超过600步（高效性）
  以上4条全部通过才输出【真机就绪: YES】，否则输出改进建议

用法：
  python pybullet_realistic_test.py                     # 完整9维测试
  python pybullet_realistic_test.py --model <path.zip>  # 自定义模型路径
  python pybullet_realistic_test.py --fast              # 快速模式（每个维度20episodes）
  python pybullet_realistic_test.py --intensity 1.0     # 只跑指定强度
"""
# ============================================================================
# 免责声明与AI使用规范
# ============================================================================
# 本文件仅供技术研究与学习交流使用，不得用于任何非法用途。
# AI使用规范：遵守所在地法律法规，涉及自动化决策须人工复核，数据处理须合规。
# 风险提示：本文件按"现状"提供，使用者自行评估风险。
# ============================================================================

import sys
import os
import time
import argparse
import numpy as np

# 复用训练脚本中的真实环境包装器
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

try:
    from pybullet_realistic_train import RealisticEnvWrapper
except ImportError as e:
    print(f"[ERROR] 无法导入真实环境包装器: {e}", flush=True)
    sys.exit(1)


# ============================================================================
# 9大测试维度配置
# ============================================================================
TEST_CASES = [
    # (key, name, intensity, realistic_mode, n_episodes, description)
    ("A", "基线(0%真实度)",  0.0, False, 50, "纯PyBullet仿真（无任何增强）作为参考基线"),
    ("B", "仅域随机化",      1.0, True,  50, "只开域随机化，验证对物理参数变化的鲁棒性"),
    ("C", "仅通信延迟",      1.0, True,  50, "只开通信延迟，验证控制周期与网络抖动"),
    ("D", "仅执行器限制",    1.0, True,  50, "只开执行器动力学，验证电机物理边界"),
    ("E", "仅外部扰动",      1.0, True,  50, "只开外部扰动，验证环境干扰下的稳定性"),
    ("F", "仅传感器噪声",    1.0, True,  50, "只开传感器噪声，验证感知不确定性"),
    ("G", "综合50%真实度",   0.5, True,  50, "所有模块50%强度，中等真实条件"),
    ("H", "综合100%真实度",  1.0, True,  50, "所有模块100%强度，== 真实部署等价环境 =="),
    ("I", "极端120%强度",    1.2, True,  50, "所有模块超强度120%，验证极限鲁棒性"),
]


def _mini_env(intensity, realistic_mode):
    """创建一个包装好的环境（局部配置模式）"""
    from robot_reach_env_optimized import RobotReachEnvOptimized
    base = RobotReachEnvOptimized(render_mode=None, max_steps=600)
    base.set_curriculum_progress(1.0)
    # 精细控制：通过set_intensity后关闭/开启对应子模块（简化版：整体intensity即可）
    return RealisticEnvWrapper(base, intensity=min(1.2, max(0.0, float(intensity))),
                               realistic_mode=realistic_mode)


def _apply_single_module(wrapped, module_name):
    """测试B~F类时，只保留一个模块开启，其他强制关闭"""
    if module_name == "B":
        wrapped.latency_sim = None
        wrapped.actuator_dyn = None
        wrapped.disturbance_sim = None
        wrapped.sensor_noise = None
    elif module_name == "C":
        wrapped.domain_randomizer = None
        wrapped.actuator_dyn = None
        wrapped.disturbance_sim = None
        wrapped.sensor_noise = None
    elif module_name == "D":
        wrapped.domain_randomizer = None
        wrapped.latency_sim = None
        wrapped.disturbance_sim = None
        wrapped.sensor_noise = None
    elif module_name == "E":
        wrapped.domain_randomizer = None
        wrapped.latency_sim = None
        wrapped.actuator_dyn = None
        wrapped.sensor_noise = None
    elif module_name == "F":
        wrapped.domain_randomizer = None
        wrapped.latency_sim = None
        wrapped.actuator_dyn = None
        wrapped.disturbance_sim = None
    return wrapped


def run_test_case(case_key, name, intensity, realistic_mode, n_episodes, model, desc):
    """执行单个测试维度"""
    print("", flush=True)
    print("-" * 70, flush=True)
    print(f"  [{case_key}] {name}   (强度={int(intensity*100)}%, episodes={n_episodes})", flush=True)
    print(f"       {desc}", flush=True)
    print("-" * 70, flush=True)

    env = _mini_env(intensity, realistic_mode)
    if case_key in ("B", "C", "D", "E", "F"):
        env = _apply_single_module(env, case_key)

    success_count = 0
    total_reward = 0.0
    total_steps = 0
    min_dist_list = []
    dist_threshold = 0.03

    t0 = time.time()
    for ep in range(n_episodes):
        obs, info = env.reset()
        ep_reward = 0.0
        ep_min_dist = 1e9
        ep_steps = 0
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, r, term, trunc, info = env.step(action)
            ep_reward += r
            ep_steps += 1
            # 计算末端到目标距离
            try:
                tgt = env.env.target_pos
                ee = env.env.ee_pos
                if tgt is not None and ee is not None:
                    d = float(np.linalg.norm(np.array(tgt) - np.array(ee)))
                    ep_min_dist = min(ep_min_dist, d)
            except Exception:
                pass
            done = term or trunc
        total_reward += ep_reward
        total_steps += ep_steps
        if ep_min_dist < dist_threshold:
            success_count += 1
        min_dist_list.append(ep_min_dist)
        if (ep + 1) % 10 == 0:
            sr_so_far = success_count / (ep + 1) * 100
            print(f"    进度 {ep+1:>3}/{n_episodes}  当前成功率 {sr_so_far:>5.1f}%  最近最小距离 {ep_min_dist*1000:.1f}mm", flush=True)

    elapsed = time.time() - t0
    env.close()

    success_rate = success_count / max(1, n_episodes)
    avg_reward = total_reward / max(1, n_episodes)
    avg_steps = total_steps / max(1, n_episodes)
    mean_min_dist = float(np.mean(min_dist_list)) if min_dist_list else 999.0
    median_min_dist = float(np.median(min_dist_list)) if min_dist_list else 999.0

    symbol = "✅" if (case_key != "I" and success_rate >= 0.80) or \
                    (case_key == "I" and success_rate >= 0.60) else "⚠️"

    print(f"    {symbol} 结果: 成功率 {success_rate*100:>5.1f}% | 平均奖励 {avg_reward:.2f} | "
          f"平均步数 {avg_steps:.0f} | 平均最小距离 {mean_min_dist*1000:.1f}mm (中位数 {median_min_dist*1000:.1f}mm) | 用时 {elapsed:.1f}s", flush=True)

    return {
        "key": case_key, "name": name, "intensity": intensity,
        "n_episodes": n_episodes, "success_rate": success_rate,
        "avg_reward": avg_reward, "avg_steps": avg_steps,
        "mean_min_dist_mm": mean_min_dist * 1000,
        "median_min_dist_mm": median_min_dist * 1000,
        "elapsed_s": elapsed,
    }


def judge_ready(results):
    """真机就绪判定 + 改进建议"""
    by_key = {r["key"]: r for r in results}
    sr_H = by_key["H"]["success_rate"]
    sr_I = by_key["I"]["success_rate"]
    singles = [by_key[k]["success_rate"] for k in ("B", "C", "D", "E", "F")]
    avg_singles = float(np.mean(singles))
    avg_steps_H = by_key["H"]["avg_steps"]

    cond1 = sr_H >= 0.80          # 100%真实度 ≥ 80%
    cond2 = sr_I >= 0.60          # 120%极端 ≥ 60%
    cond3 = avg_singles >= 0.85   # 单项平均 ≥ 85%
    cond4 = avg_steps_H <= 600    # 高效性

    passed = cond1 and cond2 and cond3 and cond4
    suggestions = []
    if not cond1:
        suggestions.append(f"· 100%真实度成功率不足80%（当前 {sr_H*100:.1f}%）：建议继续跑 realistic-train 增加100%强度阶段步数至500,000步以上，或增加episode数量训练")
    if not cond2:
        suggestions.append(f"· 极端强度鲁棒性不足60%（当前 {sr_I*100:.1f}%）：建议扩大域随机化范围（摩擦0.05~1.2）并在训练中加入更高强度的随机冲击")
    if not cond3:
        worst_k = min(("B", "C", "D", "E", "F"), key=lambda k: by_key[k]["success_rate"])
        suggestions.append(f"· 5大单项模块平均不足85%（当前 {avg_singles*100:.1f}%），最差维度是[{worst_k}]{by_key[worst_k]['name']} {by_key[worst_k]['success_rate']*100:.1f}%：建议单独针对性增加该模块强度训练")
    if not cond4:
        suggestions.append(f"· 平均步数过多（当前 {avg_steps_H:.0f}/600步）：建议缩短max_steps或增加密度奖励以提升收敛速度")

    return passed, suggestions


def main():
    parser = argparse.ArgumentParser(description="PyBullet真机部署级综合测试（9维度450轮）")
    parser.add_argument("--model", type=str, default="ppo_realistic_deploy_ready_best.zip",
                        help="被测模型路径（默认 ppo_realistic_deploy_ready_best.zip）")
    parser.add_argument("--fast", action="store_true", help="快速模式：每维度20episodes，验证流程")
    parser.add_argument("--intensity", type=float, default=None,
                        help="仅跑指定强度的综合测试（0.0~1.2，覆盖完整9维流程）")
    parser.add_argument("--episodes", type=int, default=None,
                        help="自定义每维度episodes数")
    args = parser.parse_args()

    os.chdir(SCRIPT_DIR)

    # 加载模型
    model_path = args.model
    if not os.path.exists(model_path):
        # 尝试默认最终模型
        fallback = "ppo_realistic_deploy_ready.zip"
        if os.path.exists(fallback):
            model_path = fallback
            print(f"[WARN] {args.model} 不存在，改用 {model_path}", flush=True)
        else:
            # 最后回退：基础模型（允许用来测试包装器逻辑）
            base = "ppo_robot_reach_final_5m_enhanced.zip"
            if os.path.exists(base):
                model_path = base
                print(f"[WARN] {args.model} 和 fallback 都不存在，改用 {model_path}（这是基础模型，未经过真实度训练，成功率会偏低）", flush=True)
            else:
                print(f"[ERROR] 找不到任何可用模型（{args.model} / ppo_realistic_deploy_ready.zip / ppo_robot_reach_final_5m_enhanced.zip）", flush=True)
                print(f"[建议] 先运行训练：python main.py realistic-train", flush=True)
                sys.exit(1)

    try:
        from stable_baselines3 import PPO
    except ImportError:
        print("[ERROR] stable_baselines3未安装", flush=True)
        sys.exit(1)

    print(f"[INFO] 加载模型: {model_path}", flush=True)
    model = PPO.load(model_path, device="cpu")
    print("[INFO] 模型加载成功", flush=True)

    # 单强度模式 vs 完整9维模式
    if args.intensity is not None:
        inten = max(0.0, min(1.2, float(args.intensity)))
        eps = args.episodes or (20 if args.fast else 50)
        cases = [("CUSTOM", f"自定义强度 {int(inten*100)}%", inten, True, eps, "用户指定强度的综合测试")]
    else:
        cases = []
        factor = 0.4 if args.fast else 1.0
        for c in TEST_CASES:
            eps = max(10, int(c[4] * factor))
            if args.episodes:
                eps = args.episodes
            cases.append((c[0], c[1], c[2], c[3], eps, c[5]))

    print("", flush=True)
    print("=" * 70, flush=True)
    print("  PyBullet 真机部署级综合测试（9维度 Sim-to-Real 验证）", flush=True)
    print("=" * 70, flush=True)
    print(f"  被测模型:       {model_path}", flush=True)
    print(f"  测试维度:       {len(cases)}", flush=True)
    total_eps = sum(c[4] for c in cases)
    print(f"  总回合数:       {total_eps} episodes", flush=True)
    print(f"  快速模式:       {'是' if args.fast else '否'}", flush=True)
    print("  合格标准（真机就绪）:", flush=True)
    print("    ✅ [H] 综合100%真实度 成功率 ≥ 80%", flush=True)
    print("    ✅ [I] 极端120%强度    成功率 ≥ 60%", flush=True)
    print("    ✅ [B~F] 5大单项模块   平均成功率 ≥ 85%", flush=True)
    print("    ✅ [H] 平均步数 ≤ 600 步/episode", flush=True)
    print("=" * 70, flush=True)

    # 执行所有测试
    all_results = []
    t_total = time.time()
    for c in cases:
        r = run_test_case(c[0], c[1], c[2], c[3], c[4], model, c[5])
        all_results.append(r)
    total_elapsed = time.time() - t_total

    # 最终报告
    print("", flush=True)
    print("=" * 70, flush=True)
    print("  真机部署级综合测试报告", flush=True)
    print("=" * 70, flush=True)
    print(f"  被测模型:       {model_path}", flush=True)
    print(f"  总回合数:       {total_eps}", flush=True)
    print(f"  总耗时:         {total_elapsed:.1f} 秒 ({total_elapsed/60:.1f} 分钟)", flush=True)
    print("-" * 70, flush=True)
    print(f"  {'#':>2}  {'名称':<18}  {'强度%':>5}  {'回合':>4}  {'成功率':>7}  {'平均奖励':>8}  {'平均步':>6}  {'平均距离mm':>9}", flush=True)
    print("-" * 70, flush=True)
    for r in all_results:
        inten_str = f"{int(r['intensity']*100)}" if r["key"] != "A" else "0"
        print(f"  {r['key']:>2}  {r['name']:<18}  {inten_str:>5}  {r['n_episodes']:>4}  "
              f"{r['success_rate']*100:>6.1f}%  {r['avg_reward']:>8.2f}  "
              f"{r['avg_steps']:>6.0f}  {r['mean_min_dist_mm']:>9.1f}", flush=True)
    print("-" * 70, flush=True)

    # 真机就绪判定（仅9维完整模式时给出）
    passed = False
    suggestions = []
    if args.intensity is None and len(all_results) == 9:
        passed, suggestions = judge_ready(all_results)
        print("", flush=True)
        if passed:
            print("  🎉🎉🎉  真机就绪: YES  🎉🎉🎉", flush=True)
            print("  当前模型在PyBullet真实部署模拟环境中已全面达标！", flush=True)
            print("  真机到手后可直接加载该模型进行部署。", flush=True)
        else:
            print("  ⚠️  真机就绪: NO （尚未完全满足标准）", flush=True)
            if suggestions:
                print("", flush=True)
                print("  改进建议:", flush=True)
                for s in suggestions:
                    print(f"    {s}", flush=True)
    else:
        print("  [INFO] 非完整9维模式，跳过真机就绪判定（运行无--intensity/--fast才能获得YES/NO结论）", flush=True)

    print("", flush=True)
    print("=" * 70, flush=True)
    print("  后续操作建议:", flush=True)
    print(f"    1. 结果不满意 → 加强训练: python main.py realistic-train", flush=True)
    print(f"    2. 真机到手 → 直接部署:   python main.py deploy", flush=True)
    print(f"    3. 自定义强度验证 →      python {os.path.basename(__file__)} --intensity 0.9", flush=True)
    print("=" * 70, flush=True)

    return 0 if (args.intensity is not None or passed) else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[INFO] 用户中断 (Ctrl+C)", flush=True)
        sys.exit(0)
