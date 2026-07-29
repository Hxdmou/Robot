#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generalization Baseline Evaluation for best_reach_stable/best_model.zip

Tests three dimensions:
1. Target position generalization (OOD: X[0.20~0.70], Y[-0.25~0.25], Z[0.15~0.55])
2. Physical parameter perturbation (friction, damping, gravity)
3. Initial state diversity (joint angle range)

Outputs:
- eval_generalization_detailed.csv  (per-episode results)
- eval_generalization_summary.csv   (aggregated stats per condition)
- generalization_evaluation.png     (heatmap + bar charts)
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
import csv
import time
import numpy as np
import pybullet as p
import pybullet_data
from stable_baselines3 import PPO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap
from robot_reach_env_optimized import RobotReachEnvOptimized

# Training distribution boundaries
TRAIN_X = (0.40, 0.50)
TRAIN_Y = (-0.10, 0.10)
TRAIN_Z = (0.30, 0.40)


class GeneralizationEvalEnv(RobotReachEnvOptimized):
    """Extended environment for generalization testing without modifying original code."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.eval_target = None          # [x, y, z] or None
        self.eval_joint_range = None     # (low, high) or None
        self.eval_friction = None        # float or None
        self.eval_damping_scale = None   # float or None
        self.eval_gravity = None         # float or None

    def reset(self, seed=None, options=None):
        # Call parent reset: creates sim, plane, robot, random target, random joints
        super().reset(seed=seed)

        # --- Override target position ---
        if self.eval_target is not None:
            self.target_pos = np.array(self.eval_target, dtype=np.float32)

        # --- Override joint initial states ---
        if self.eval_joint_range is not None:
            low, high = self.eval_joint_range
            for i in range(7):
                p.resetJointState(self.robot_id, i, self.np_random.uniform(low, high))

        # --- Apply friction perturbation ---
        if self.eval_friction is not None:
            # Plane lateral friction
            try:
                p.changeDynamics(0, -1, lateralFriction=self.eval_friction)
            except Exception:
                pass
            # Robot link friction (use lateralFriction + linearDamping as proxy)
            for i in range(7):
                try:
                    p.changeDynamics(self.robot_id, i,
                                     lateralFriction=self.eval_friction,
                                     linearDamping=self.eval_friction * 0.1)
                except Exception:
                    pass

        # --- Apply damping perturbation ---
        if self.eval_damping_scale is not None:
            new_damping = 0.1 * self.eval_damping_scale
            for i in range(7):
                try:
                    p.changeDynamics(self.robot_id, i, jointDamping=new_damping)
                except Exception:
                    # Fallback: use linearDamping + angularDamping
                    try:
                        p.changeDynamics(self.robot_id, i,
                                         linearDamping=new_damping,
                                         angularDamping=new_damping)
                    except Exception:
                        pass

        # --- Apply gravity perturbation ---
        if self.eval_gravity is not None:
            p.setGravity(0, 0, self.eval_gravity)

        # Settle physics after modifications
        for _ in range(10):
            p.stepSimulation()

        return self._get_obs(), {}


def run_episodes(env, model, n_episodes):
    """Run n_episodes and return per-episode results."""
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


def save_detailed_csv(results, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'test_type', 'condition', 'episode',
            'success', 'reward', 'distance', 'steps'
        ])
        writer.writeheader()
        writer.writerows(results)


def save_summary_csv(results, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'test_type', 'condition', 'n_episodes',
            'success_rate', 'mean_reward', 'std_reward',
            'mean_distance', 'in_distribution'
        ])
        writer.writeheader()
        writer.writerows(results)


def plot_results(target_data, x_vals, y_vals, z_vals,
                 friction_results, damping_results, gravity_results, joint_results):
    """Generate comprehensive visualization."""

    # Try Chinese font, fallback to English
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
        plt.rcParams['axes.unicode_minus'] = False
    except Exception:
        pass

    fig = plt.figure(figsize=(20, 16))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

    # Custom colormap: red -> yellow -> green
    cmap = LinearSegmentedColormap.from_list('rg', ['#FF4444', '#FFAA00', '#44FF44'], N=100)

    # ========== Row 1: Heatmaps for target positions ==========
    for zi, z in enumerate(z_vals):
        ax = fig.add_subplot(gs[0, zi])
        data = target_data[z]  # shape: (len(y_vals), len(x_vals))

        im = ax.imshow(data, cmap=cmap, vmin=0, vmax=100, aspect='auto',
                       origin='lower',
                       extent=[x_vals[0] - 0.075, x_vals[-1] + 0.075,
                               y_vals[0] - 0.075, y_vals[-1] + 0.075])

        # Annotate cells with success rate
        for yi, y in enumerate(y_vals):
            for xi, x in enumerate(x_vals):
                sr = data[yi, xi]
                color = 'white' if sr < 50 else 'black'
                ax.text(x, y, f'{sr:.0f}', ha='center', va='center',
                        fontsize=10, fontweight='bold', color=color)

        # Mark training distribution area
        rect = Rectangle((TRAIN_X[0], TRAIN_Y[0]),
                         TRAIN_X[1] - TRAIN_X[0], TRAIN_Y[1] - TRAIN_Y[0],
                         linewidth=2, edgecolor='blue', facecolor='none',
                         linestyle='--', label='Training Range')
        ax.add_patch(rect)
        ax.legend(fontsize=8, loc='upper left')

        ax.set_xlabel('X (m)', fontsize=10)
        ax.set_ylabel('Y (m)', fontsize=10)
        ax.set_title(f'Target Position SR (Z={z:.2f}m)', fontsize=12, fontweight='bold')
        ax.set_xticks(x_vals)
        ax.set_yticks(y_vals)
        plt.colorbar(im, ax=ax, label='Success Rate (%)', shrink=0.8)

    # ========== Row 2: Bar charts for physical parameters ==========
    def plot_bar_chart(ax, labels, srs, title, xlabel):
        bars = ax.bar(range(len(labels)), srs,
                      color=[cmap(s / 100) for s in srs], edgecolor='gray', linewidth=0.5)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel('Success Rate (%)', fontsize=10)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_ylim(0, 115)
        ax.axhline(y=100, color='gray', linestyle='--', alpha=0.4)
        for bar, sr in zip(bars, srs):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                    f'{sr:.0f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Friction
    ax2a = fig.add_subplot(gs[1, 0])
    fr_labels = [f'{r[0]:.1f}' for r in friction_results]
    fr_srs = [r[1] for r in friction_results]
    plot_bar_chart(ax2a, fr_labels, fr_srs, 'Friction Perturbation', 'Friction Coefficient')

    # Damping
    ax2b = fig.add_subplot(gs[1, 1])
    dm_labels = [f'{r[0]:.2f}x' for r in damping_results]
    dm_srs = [r[1] for r in damping_results]
    plot_bar_chart(ax2b, dm_labels, dm_srs, 'Joint Damping Perturbation', 'Damping Scale')

    # Gravity
    ax2c = fig.add_subplot(gs[1, 2])
    gr_labels = [r[0] for r in gravity_results]
    gr_srs = [r[1] for r in gravity_results]
    plot_bar_chart(ax2c, gr_labels, gr_srs, 'Gravity Perturbation', 'Gravity')

    # ========== Row 3: Joint init diversity (spanning all 3 columns) ==========
    ax3 = fig.add_subplot(gs[2, :])
    jl = [r[0] for r in joint_results]
    js = [r[1] for r in joint_results]
    bars = ax3.bar(range(len(jl)), js,
                   color=[cmap(s / 100) for s in js], width=0.5, edgecolor='gray', linewidth=0.5)
    ax3.set_xticks(range(len(jl)))
    ax3.set_xticklabels(jl, fontsize=11)
    ax3.set_ylabel('Success Rate (%)', fontsize=10)
    ax3.set_title('Initial Joint State Diversity', fontsize=12, fontweight='bold')
    ax3.set_ylim(0, 115)
    ax3.axhline(y=100, color='gray', linestyle='--', alpha=0.4)
    for bar, sr in zip(bars, js):
        ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                 f'{sr:.0f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Overall title
    fig.suptitle('Generalization Baseline Evaluation\nModel: best_reach_stable/best_model.zip',
                 fontsize=16, fontweight='bold', y=0.98)

    plt.savefig('generalization_evaluation.png', dpi=150, bbox_inches='tight')
    plt.close()


def main():
    os.chdir(PROJECT_ROOT)

    print("=" * 70)
    print("  Generalization Baseline Evaluation")
    print("  Model: ppo_robot_reach_stable_final.zip")
    print("=" * 70)

    # Load model
    print("\n[1/5] Loading model...")
    model = PPO.load("ppo_robot_reach_stable_final.zip", device="cpu")
    print("  OK")

    env = GeneralizationEvalEnv(render_mode=None, max_steps=500)

    N_EP = 50
    detailed_results = []
    summary_results = []
    start_time = time.time()

    # ================================================================
    # Dimension 1: Target Position Generalization
    # ================================================================
    print(f"\n[2/5] Target Position Generalization ({N_EP} eps/condition)...")

    x_vals = [0.20, 0.35, 0.50, 0.65]
    y_vals = [-0.25, -0.10, 0.10, 0.25]
    z_vals = [0.20, 0.35, 0.50]

    target_data = {z: np.zeros((len(y_vals), len(x_vals))) for z in z_vals}

    total_targets = len(x_vals) * len(y_vals) * len(z_vals)
    count = 0

    for z in z_vals:
        for x in x_vals:
            for y in y_vals:
                count += 1

                # Configure env
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

                # Store for heatmap
                yi = y_vals.index(y)
                xi = x_vals.index(x)
                target_data[z][yi, xi] = sr

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

                for ep in range(N_EP):
                    detailed_results.append({
                        'test_type': 'target_position',
                        'condition': cond,
                        'episode': ep + 1,
                        'success': succ[ep],
                        'reward': round(rews[ep], 4),
                        'distance': round(dists[ep], 4),
                        'steps': steps[ep]
                    })

    # ================================================================
    # Dimension 2: Physical Parameter Perturbation
    # ================================================================
    print(f"\n[3/5] Physical Parameter Perturbation...")

    # --- 2a. Friction ---
    print("  [a] Friction (0.3~1.8):")
    friction_vals = [0.3, 0.5, 0.7, 1.0, 1.3, 1.5, 1.8]
    friction_results = []

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

        friction_results.append((fr, sr, mr, sr_std, md))
        tag = " (baseline)" if fr == 1.0 else ""
        print(f"    fr={fr:.1f}: SR={sr:.0f}%, R={mr:.1f}+/-{sr_std:.1f}, D={md:.3f}m{tag}")

        cond = f"friction={fr:.1f}"
        summary_results.append({
            'test_type': 'friction', 'condition': cond, 'n_episodes': N_EP,
            'success_rate': round(sr, 1), 'mean_reward': round(mr, 2),
            'std_reward': round(sr_std, 2), 'mean_distance': round(md, 4),
            'in_distribution': fr == 1.0
        })
        for ep in range(N_EP):
            detailed_results.append({
                'test_type': 'friction', 'condition': cond, 'episode': ep + 1,
                'success': succ[ep], 'reward': round(rews[ep], 4),
                'distance': round(dists[ep], 4), 'steps': steps[ep]
            })

    # --- 2b. Damping ---
    print("  [b] Damping (0.7~1.3x):")
    damping_vals = [0.7, 0.85, 1.0, 1.15, 1.3]
    damping_results = []

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

        damping_results.append((dmp, sr, mr, sr_std, md))
        tag = " (baseline)" if dmp == 1.0 else ""
        print(f"    dmp={dmp:.2f}x: SR={sr:.0f}%, R={mr:.1f}+/-{sr_std:.1f}, D={md:.3f}m{tag}")

        cond = f"damping={dmp:.2f}x"
        summary_results.append({
            'test_type': 'damping', 'condition': cond, 'n_episodes': N_EP,
            'success_rate': round(sr, 1), 'mean_reward': round(mr, 2),
            'std_reward': round(sr_std, 2), 'mean_distance': round(md, 4),
            'in_distribution': dmp == 1.0
        })
        for ep in range(N_EP):
            detailed_results.append({
                'test_type': 'damping', 'condition': cond, 'episode': ep + 1,
                'success': succ[ep], 'reward': round(rews[ep], 4),
                'distance': round(dists[ep], 4), 'steps': steps[ep]
            })

    # --- 2c. Gravity ---
    print("  [c] Gravity (+/-10%):")
    gravity_vals = [-8.83, -9.81, -10.79]
    gravity_labels = ["90%", "100%", "110%"]
    gravity_results = []

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

        gravity_results.append((gravity_labels[gi], sr, mr, sr_std, md))
        tag = " (baseline)" if gr == -9.81 else ""
        print(f"    g={gravity_labels[gi]}: SR={sr:.0f}%, R={mr:.1f}+/-{sr_std:.1f}, D={md:.3f}m{tag}")

        cond = f"gravity={gravity_labels[gi]}"
        summary_results.append({
            'test_type': 'gravity', 'condition': cond, 'n_episodes': N_EP,
            'success_rate': round(sr, 1), 'mean_reward': round(mr, 2),
            'std_reward': round(sr_std, 2), 'mean_distance': round(md, 4),
            'in_distribution': gr == -9.81
        })
        for ep in range(N_EP):
            detailed_results.append({
                'test_type': 'gravity', 'condition': cond, 'episode': ep + 1,
                'success': succ[ep], 'reward': round(rews[ep], 4),
                'distance': round(dists[ep], 4), 'steps': steps[ep]
            })

    # ================================================================
    # Dimension 3: Initial State Diversity
    # ================================================================
    print(f"\n[4/5] Initial State Diversity...")

    joint_configs = [
        ((-0.5, 0.5), "Training(-0.5~0.5)"),
        ((-1.0, 1.0), "OOD-wide(-1.0~1.0)"),
        ((-0.2, 0.2), "Narrow(-0.2~0.2)"),
    ]
    joint_results = []

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

        joint_results.append((jlabel, sr, mr, sr_std, md))
        tag = " (baseline)" if jrange == (-0.5, 0.5) else ""
        print(f"    {jlabel}: SR={sr:.0f}%, R={mr:.1f}+/-{sr_std:.1f}, D={md:.3f}m{tag}")

        cond = f"joint_range={jlabel}"
        summary_results.append({
            'test_type': 'joint_init', 'condition': cond, 'n_episodes': N_EP,
            'success_rate': round(sr, 1), 'mean_reward': round(mr, 2),
            'std_reward': round(sr_std, 2), 'mean_distance': round(md, 4),
            'in_distribution': jrange == (-0.5, 0.5)
        })
        for ep in range(N_EP):
            detailed_results.append({
                'test_type': 'joint_init', 'condition': cond, 'episode': ep + 1,
                'success': succ[ep], 'reward': round(rews[ep], 4),
                'distance': round(dists[ep], 4), 'steps': steps[ep]
            })

    # ================================================================
    # Save Results
    # ================================================================
    print(f"\n[5/5] Saving results...")

    save_detailed_csv(detailed_results, 'eval_generalization_detailed.csv')
    save_summary_csv(summary_results, 'eval_generalization_summary.csv')

    print(f"  Detailed CSV: eval_generalization_detailed.csv ({len(detailed_results)} rows)")
    print(f"  Summary CSV:  eval_generalization_summary.csv ({len(summary_results)} rows)")

    # Generate charts
    plot_results(target_data, x_vals, y_vals, z_vals,
                 friction_results, damping_results, gravity_results, joint_results)
    print(f"  Chart:        generalization_evaluation.png")

    elapsed = time.time() - start_time
    print(f"\n  Total time: {elapsed:.0f}s ({elapsed / 60:.1f} min)")

    # ================================================================
    # Print Summary
    # ================================================================
    print("\n" + "=" * 70)
    print("  EVALUATION SUMMARY")
    print("=" * 70)

    # Target position
    id_srs = [s['success_rate'] for s in summary_results
              if s['test_type'] == 'target_position' and s['in_distribution']]
    ood_srs = [s['success_rate'] for s in summary_results
               if s['test_type'] == 'target_position' and not s['in_distribution']]
    print(f"\n  1. Target Position Generalization:")
    print(f"     In-Distribution:   SR={np.mean(id_srs):.1f}% (n={len(id_srs)} conditions)")
    print(f"     Out-of-Distribution: SR={np.mean(ood_srs):.1f}% (n={len(ood_srs)} conditions)")
    print(f"     Worst OOD: {min(ood_srs):.0f}% | Best OOD: {max(ood_srs):.0f}%")

    # Friction
    fr_srs = [r[1] for r in friction_results]
    print(f"\n  2a. Friction: {min(fr_srs):.0f}% ~ {max(fr_srs):.0f}%")

    # Damping
    dm_srs = [r[1] for r in damping_results]
    print(f"  2b. Damping:  {min(dm_srs):.0f}% ~ {max(dm_srs):.0f}%")

    # Gravity
    gr_srs = [r[1] for r in gravity_results]
    print(f"  2c. Gravity:  {min(gr_srs):.0f}% ~ {max(gr_srs):.0f}%")

    # Joint init
    jl_srs = [r[1] for r in joint_results]
    print(f"  3.  Joint Init: {min(jl_srs):.0f}% ~ {max(jl_srs):.0f}%")

    # Identify weakest areas
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
