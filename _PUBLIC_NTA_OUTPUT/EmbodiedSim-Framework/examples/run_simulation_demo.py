#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1：仿真演示（PyBullet Panda 机械臂基础运行）
================================================
演示：
  - 创建仿真环境（GUI模式）
  - 加载 Panda 机器人 + 工作台 + 工件
  - 循环随机调整关节位置，渲染画面
  - 运行中打印仿真时间 & 末端位姿

说明：未安装 pybullet 时会给出友好提示并安全退出。
"""

from __future__ import annotations

import math
import random
import sys
import time


def run(max_steps: int = 600, show_camera_render: bool = False) -> int:
    try:
        from core.simulation_env import PyBulletSimulationEnv, SimConfig
    except Exception as e:
        print("=" * 64)
        print("❌ 缺少依赖：请先安装 pybullet & numpy")
        print(f"    错误详情: {e}")
        print("    安装命令：pip install pybullet numpy")
        print("=" * 64)
        return 2

    mode = "gui" if "--direct" not in sys.argv else "direct"
    cfg = SimConfig(mode=mode, time_step=0.002)
    print("▶ 启动 PyBullet 仿真演示（Panda）| 模式:", mode)

    step_count = 0
    with PyBulletSimulationEnv(cfg) as env:
        env.load_robot("panda", ee_index=11)
        table_id = env.add_worktable((0.5, 0.0, 0.2))
        red_box = env.add_box("workpiece_red", half_extents=(0.03, 0.03, 0.03),
                              pos=(0.50,  0.08, 0.43), color=(0.85, 0.1, 0.1, 1.0))
        green_box = env.add_box("workpiece_green", half_extents=(0.03, 0.03, 0.03),
                                pos=(0.50, -0.08, 0.43), color=(0.1, 0.8, 0.1, 1.0))
        print(f"  场景对象: {env.list_objects()}")
        print(f"  仿真配置: gravity={cfg.gravity}, time_step={cfg.time_step}s")

        t0 = time.time()
        target_list = [
            ([0.0]*7, "初始姿态"),
            ([0.4, -0.3,  0.2, -1.5, 0.0, 1.3, 0.8], "上方准备"),
            ([0.6, -0.1,  0.1, -2.0, 0.1, 1.9, 0.9], "抓取红色工件"),
            ([0.2, -0.8, -0.1, -1.8, -0.1, 1.0, 0.7], "搬运到左侧"),
            ([0.0]*7, "回到待命"),
            ([-0.4, 0.3,  0.1, -1.6, 0.0, 1.8, -0.7], "抓取绿色工件"),
            ([-0.2, 0.8, -0.1, -1.9, -0.2, 1.1, -0.5], "搬运到右侧"),
        ]
        for joint_target, label in target_list:
            print(f"\n[{label}] 目标关节 = [{', '.join(f'{v:+.3f}' for v in joint_target)}]")
            env.set_joint_positions(joint_target)
            # 跑 80 step ~ 0.16s，让画面稳定
            for _ in range(80):
                env.step()
                step_count += 1
            state = env.get_robot_state()
            print(f"  末端XYZ = ({state.end_effector_pos[0]:+.3f}, "
                  f"{state.end_effector_pos[1]:+.3f}, {state.end_effector_pos[2]:+.3f}) m")

        # 额外：随机摆动一段时间，演示连续运行
        print("\n▶ 连续运行阶段（+{}步随机关节摆动）...".format(max_steps))
        phase = 0.0
        for k in range(max_steps):
            phase += 0.05
            js = [
                0.3 * math.sin(phase + i*0.4) + joint_target[i % 7]*0.1
                for i in range(7)
            ]
            env.set_joint_positions(js)
            env.step(1)
            step_count += 1
            if show_camera_render and (k % 100 == 0):
                _ = env.render_camera_image()  # 不保存，仅触发一次渲染
        dt = time.time() - t0
        print(f"\n▶ 演示完成 | 总步数={step_count} | 耗时={dt:.2f}s | "
              f"平均频率={step_count/dt:.1f} step/s")

    return 0


if __name__ == "__main__":
    sys.exit(run())
