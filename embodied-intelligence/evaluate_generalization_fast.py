#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fast Generalization Evaluation for ppo_robot_reach_stable_final.zip
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


import os
import sys
import csv
import time
import numpy as np
import pybullet as p
from stable_baselines3 import PPO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
from robot_reach_env_optimized import RobotReachEnvOptimized

# ============================================================================
# 路径配置
# ============================================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

sys.stdout.reconfigure(line_buffering=True)

TRAIN_X = (0.40, 0.50)
TRAIN_Y = (-0.10, 0.10)
TRAIN_Z = (0.30, 0.40)


class GeneralizationEvalEnv(RobotReachEnvOptimized):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eval_target = None
        self.eval_joint_range = None
        self.eval_friction = None
        self.eval_damping_scale = None
        self.eval_gravity = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        if self.eval_target is not None:
            self.target_pos = np.array(self.eval_target, dtype=np.float32)

        if self.eval_joint_range is not None:
            low, high = self.eval_joint_range
            for i in range(7):
                p.resetJointState(self.robot_id, i, self.np_random.uniform(low, high))

        if self.eval_friction is not None:
            try:
                p.changeDynamics(0, -1, lateralFriction=self.eval_friction)
            except Exception:
                pass
            for i in range(7):
                try:
                    p.changeDynamics(self.robot_id, i,
                                     lateralFriction=self.eval_friction,
                                     linearDamping=self.eval_friction * 0.1)
                except Exception:
                    pass

        if self.eval_damping_scale is not None:
            new_damping = 0.1 * self.eval_damping_scale
            for i in range(7):
                try:
                    p.changeDynamics(self.robot_id, i, jointDamping=new_damping)
                except Exception:
                    try:
                        p.changeDynamics(self.robot_id, i,
                                         linearDamping=new_damping,
                                         angularDamping=new_damping)
                    except Exception:
                        pass

        if self.eval_gravity is not None:
            p.setGravity(0, 0, self.eval_gravity)

        for _ in range(10):
            p.stepSimulation()

        return self._get_obs(), {}


def run_episodes(env, model, n_episodes):
    successes, rewards, distances, steps_list = [], [], [], []

    for ep in range(n_episodes):
        obs, info = env.reset()
        ep_reward = 0.0
        terminated = False

        while True:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            ep_reward += reward
            if terminated or truncated:
                break

        successes.append(int(terminated))
        rewards.append(ep_reward)
        distances.append(float(info.get('distance', 999)))
        steps_list.append(env.step_count)

    return successes, rewards, distances, steps_list


def main():
    os.chdir(PROJECT_ROOT)

    print("=" * 70)
    print("  Fast Generalization Evaluation")
    print("  Model: ppo_dynamic_target.zip")
    print("=" * 70)

    print("\n[1/5] Loading model...")
    model = PPO.load("ppo_dynamic_target.zip", device="cpu")
    print("  OK")

    env = GeneralizationEvalEnv(render_mode=None, max_steps=150)

    N_EP = 20
    summary_results = []
    start_time = time.time()

    # Dimension 1: Target Position Generalization
    print(f"\n[2/5] Target Position Generalization ({N_EP} eps/condition)...")

    x_vals = [0.25, 0.35, 0.50, 0.65]
    y_vals = [-0.25, -0.10, 0.10, 0.25]
    z_vals = [0.20, 0.35, 0.55]

    total_targets = len(x_vals) * len(y_vals) * len(z_vals)
    count = 0

    for z in z_vals:
        for x in x_vals:
            for y in y_vals:
                count += 1

                env.eval_target = [x, y, z]
                env.eval_joint_range = None
                env.eval_friction = None
                env.eval_damping_scale = None
                env.eval_gravity = None

                succ, rews, dists, steps = run_episodes(env, model, N_EP)

                sr = np.mean(succ) * 100
                mr = np.mean(rews)
                sr_std = np.std(rews)
                md = np.mean(dists)

                in_dist = (TRAIN_X[0] <= x <= TRAIN_X[1] and
                           TRAIN_Y[0] <= y <= TRAIN_Y[1] and
                           TRAIN_Z[0] <= z <= TRAIN_Z[1])
                tag = "ID" if in_dist else "OOD"

                cond = f"x={x:.2f},y={y:.2f},z={z:.2f}"
                print(f"  [{count}/{total_targets}] ({x:.2f},{y:.2f},{z:.2f}) [{tag}]: "
                      f"SR={sr:.0f}%, R={mr:.1f}+/-{sr_std:.1f}, D={md:.3f}m")

                summary_results.append({
                    'test_type': 'target_position',
                    'condition': cond,
                    'n_episodes': N_EP,
                    'success_rate': round(sr, 1),
                    'mean_reward': round(mr, 2),
                    'std_reward': round(sr_std, 2),
                    'mean_distance': round(md, 4),
                    'in_distribution': in_dist
                })

    # Dimension 2: Physical Parameter Perturbation
    print(f"\n[3/5] Physical Parameter Perturbation...")

    print("  [a] Friction (0.3~1.8):")
    friction_vals = [0.3, 0.5, 0.7, 1.0, 1.3, 1.5, 1.8]

    for fr in friction_vals:
        env.eval_target = None
        env.eval_joint_range = None
        env.eval_friction = fr
        env.eval_damping_scale = None
        env.eval_gravity = None

        succ, rews, dists, steps = run_episodes(env, model, N_EP)
        sr = np.mean(succ) * 100
        mr = np.mean(rews)
        sr_std = np.std(rews)
        md = np.mean(dists)

        tag = " (baseline)" if fr == 1.0 else ""
        print(f"    fr={fr:.1f}: SR={sr:.0f}%, R={mr:.1f}+/-{sr_std:.1f}, D={md:.3f}m{tag}")

        summary_results.append({
            'test_type': 'friction', 'condition': f"friction={fr:.1f}", 'n_episodes': N_EP,
            'success_rate': round(sr, 1), 'mean_reward': round(mr, 2),
            'std_reward': round(sr_std, 2), 'mean_distance': round(md, 4),
            'in_distribution': fr == 1.0
        })

    print("  [b] Damping (0.7~1.3x):")
    damping_vals = [0.7, 0.85, 1.0, 1.15, 1.3]

    for dmp in damping_vals:
        env.eval_target = None
        env.eval_joint_range = None
        env.eval_friction = None
        env.eval_damping_scale = dmp
        env.eval_gravity = None

        succ, rews, dists, steps = run_episodes(env, model, N_EP)
        sr = np.mean(succ) * 100
        mr = np.mean(rews)
        sr_std = np.std(rews)
        md = np.mean(dists)

        tag = " (baseline)" if dmp == 1.0 else ""
        print(f"    dmp={dmp:.2f}x: SR={sr:.0f}%, R={mr:.1f}+/-{sr_std:.1f}, D={md:.3f}m{tag}")

        summary_results.append({
            'test_type': 'damping', 'condition': f"damping={dmp:.2f}x", 'n_episodes': N_EP,
            'success_rate': round(sr, 1), 'mean_reward': round(mr, 2),
            'std_reward': round(sr_std, 2), 'mean_distance': round(md, 4),
            'in_distribution': dmp == 1.0
        })

    print("  [c] Gravity (+/-10%):")
    gravity_vals = [-8.83, -9.81, -10.79]
    gravity_labels = ["90%", "100%", "110%"]

    for gi, gr in enumerate(gravity_vals):
        env.eval_target = None
        env.eval_joint_range = None
        env.eval_friction = None
        env.eval_damping_scale = None
        env.eval_gravity = gr

        succ, rews, dists, steps = run_episodes(env, model, N_EP)
        sr = np.mean(succ) * 100
        mr = np.mean(rews)
        sr_std = np.std(rews)
        md = np.mean(dists)

        tag = " (baseline)" if gr == -9.81 else ""
        print(f"    g={gravity_labels[gi]}: SR={sr:.0f}%, R={mr:.1f}+/-{sr_std:.1f}, D={md:.3f}m{tag}")

        summary_results.append({
            'test_type': 'gravity', 'condition': f"gravity={gravity_labels[gi]}", 'n_episodes': N_EP,
            'success_rate': round(sr, 1), 'mean_reward': round(mr, 2),
            'std_reward': round(sr_std, 2), 'mean_distance': round(md, 4),
            'in_distribution': gr == -9.81
        })

    # Dimension 3: Initial State Diversity
    print(f"\n[4/5] Initial State Diversity...")

    joint_configs = [
        ((-0.5, 0.5), "Training(-0.5~0.5)"),
        ((-1.0, 1.0), "OOD-wide(-1.0~1.0)"),
        ((-0.2, 0.2), "Narrow(-0.2~0.2)"),
    ]

    for jrange, jlabel in joint_configs:
        env.eval_target = None
        env.eval_joint_range = jrange
        env.eval_friction = None
        env.eval_damping_scale = None
        env.eval_gravity = None

        succ, rews, dists, steps = run_episodes(env, model, N_EP)
        sr = np.mean(succ) * 100
        mr = np.mean(rews)
        sr_std = np.std(rews)
        md = np.mean(dists)

        tag = " (baseline)" if jrange == (-0.5, 0.5) else ""
        print(f"    {jlabel}: SR={sr:.0f}%, R={mr:.1f}+/-{sr_std:.1f}, D={md:.3f}m{tag}")

        summary_results.append({
            'test_type': 'joint_init', 'condition': f"joint_range={jlabel}", 'n_episodes': N_EP,
            'success_rate': round(sr, 1), 'mean_reward': round(mr, 2),
            'std_reward': round(sr_std, 2), 'mean_distance': round(md, 4),
            'in_distribution': jrange == (-0.5, 0.5)
        })

    # Save Results
    print(f"\n[5/5] Saving results...")

    with open('eval_generalization_summary_fast.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'test_type', 'condition', 'n_episodes',
            'success_rate', 'mean_reward', 'std_reward',
            'mean_distance', 'in_distribution'
        ])
        writer.writeheader()
        writer.writerows(summary_results)

    print(f"  Summary CSV: eval_generalization_summary_fast.csv ({len(summary_results)} rows)")

    elapsed = time.time() - start_time
    print(f"\n  Total time: {elapsed:.0f}s ({elapsed / 60:.1f} min)")

    # Print Summary
    print("\n" + "=" * 70)
    print("  EVALUATION SUMMARY")
    print("=" * 70)

    id_srs = [s['success_rate'] for s in summary_results
              if s['test_type'] == 'target_position' and s['in_distribution']]
    ood_srs = [s['success_rate'] for s in summary_results
               if s['test_type'] == 'target_position' and not s['in_distribution']]
    print(f"\n  1. Target Position Generalization:")
    print(f"     In-Distribution:   SR={np.mean(id_srs):.1f}% (n={len(id_srs)} conditions)")
    print(f"     Out-of-Distribution: SR={np.mean(ood_srs):.1f}% (n={len(ood_srs)} conditions)")
    print(f"     Worst OOD: {min(ood_srs):.0f}% | Best OOD: {max(ood_srs):.0f}%")

    fr_srs = [s['success_rate'] for s in summary_results if s['test_type'] == 'friction']
    print(f"\n  2a. Friction: {min(fr_srs):.0f}% ~ {max(fr_srs):.0f}%")

    dm_srs = [s['success_rate'] for s in summary_results if s['test_type'] == 'damping']
    print(f"  2b. Damping:  {min(dm_srs):.0f}% ~ {max(dm_srs):.0f}%")

    gr_srs = [s['success_rate'] for s in summary_results if s['test_type'] == 'gravity']
    print(f"  2c. Gravity:  {min(gr_srs):.0f}% ~ {max(gr_srs):.0f}%")

    jl_srs = [s['success_rate'] for s in summary_results if s['test_type'] == 'joint_init']
    print(f"  3.  Joint Init: {min(jl_srs):.0f}% ~ {max(jl_srs):.0f}%")

    print(f"\n  --- Weakest Conditions (SR < 80%) ---")
    weak = [s for s in summary_results if s['success_rate'] < 80]
    if weak:
        for w in sorted(weak, key=lambda x: x['success_rate']):
            print(f"    {w['test_type']:20s} | {w['condition']:35s} | SR={w['success_rate']:.0f}%")
    else:
        print(f"    None - all conditions achieved SR >= 80%")

    env.close()
    print("\n  Done!")


if __name__ == '__main__':
    main()
