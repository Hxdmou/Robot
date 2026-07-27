#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
部署校准与验证工具
功能：
  1. 关节零位校准（真实机器人）
  2. 工作空间边界验证
  3. 目标位置可达性验证
  4. 笛卡尔坐标安全性检查

使用方法：
  python deploy_calibration.py --workspace
  python deploy_calibration.py --target 0.3 0.0 0.5
  python deploy_calibration.py --calibrate
  python deploy_calibration.py --full
"""

import sys
import os
import argparse
import math
import numpy as np

sys.stderr = open(os.devnull, 'w')
os.environ['PYBULLET_DISABLE_WARNINGS'] = '1'

from robot_config import JOINT_LIMITS, START_JOINT_POSITIONS, SAFETY_PARAMS


class WorkspaceValidator:
    """工作空间验证器"""

    def __init__(self):
        self.workspace_radius = SAFETY_PARAMS["workspace_radius"]
        self.min_z = SAFETY_PARAMS.get("min_z", 0.05)
        self.max_z = SAFETY_PARAMS.get("max_z", 1.2)

    def is_in_workspace(self, x, y, z):
        """检查点是否在工作空间内"""
        issues = []

        dist_xy = math.sqrt(x**2 + y**2)
        if dist_xy > self.workspace_radius:
            issues.append(f"超出水平工作空间: {dist_xy:.3f}m > {self.workspace_radius}m")

        if z < self.min_z:
            issues.append(f"Z轴过低: {z:.3f}m < {self.min_z}m")

        if z > self.max_z:
            issues.append(f"Z轴过高: {z:.3f}m > {self.max_z}m")

        return len(issues) == 0, issues

    def check_target(self, target_pos):
        """验证目标点的可达性"""
        x, y, z = target_pos
        print(f"\n验证目标点: ({x:.3f}, {y:.3f}, {z:.3f})")

        in_ws, issues = self.is_in_workspace(x, y, z)
        if in_ws:
            print(f"  ✅ 在工作空间内 (水平距离: {math.sqrt(x**2+y**2):.3f}m)")
        else:
            for issue in issues:
                print(f"  ❌ {issue}")

        # 检查是否在机器人前方（避免自碰撞）
        if x < 0:
            print(f"  ⚠️  目标在机器人后方 (x={x:.3f})，可能存在自碰撞风险")

        return in_ws

    def scan_workspace_boundary(self, num_points=20):
        """扫描工作空间边界（可视化用）"""
        print(f"\n工作空间边界扫描 ({num_points}点)...")
        print(f"  水平半径: {self.workspace_radius}m")
        print(f"  Z范围: {self.min_z}m ~ {self.max_z}m")

        safe_points = 0
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            r = self.workspace_radius * 0.95
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            z = 0.5

            safe, _ = self.is_in_workspace(x, y, z)
            if safe:
                safe_points += 1

        print(f"  安全点: {safe_points}/{num_points}")
        return safe_points

    def generate_safe_targets(self, n=5):
        """生成N个安全的随机目标点"""
        targets = []
        attempts = 0
        while len(targets) < n and attempts < 1000:
            r = np.random.uniform(0.1, self.workspace_radius * 0.8)
            angle = np.random.uniform(-math.pi/2, math.pi/2)  # 前方180度
            z = np.random.uniform(0.2, self.max_z * 0.8)

            x = r * math.cos(angle)
            y = r * math.sin(angle)

            safe, _ = self.is_in_workspace(x, y, z)
            if safe:
                targets.append([round(x, 3), round(y, 3), round(z, 3)])
            attempts += 1

        print(f"\n生成 {len(targets)} 个安全目标点:")
        for i, t in enumerate(targets):
            print(f"  {i+1}. ({t[0]:.3f}, {t[1]:.3f}, {t[2]:.3f})")
        return targets


class JointCalibrator:
    """关节零位校准器（真实机器人）"""

    def __init__(self):
        self.joint_limits = JOINT_LIMITS
        self.reference_positions = START_JOINT_POSITIONS
        self.calibration_results = None

    def validate_joint_positions(self, joint_positions, tolerance=0.01):
        """验证关节位置是否在安全范围内"""
        print("\n关节位置验证:")
        all_safe = True

        for i, pos in enumerate(joint_positions):
            lower = self.joint_limits["lower"][i]
            upper = self.joint_limits["upper"][i]

            if pos < lower or pos > upper:
                print(f"  ❌ 关节{i}: {pos:.4f} rad 超出范围 [{lower:.4f}, {upper:.4f}]")
                all_safe = False
            elif pos < lower + tolerance or pos > upper - tolerance:
                print(f"  ⚠️  关节{i}: {pos:.4f} rad 接近限位")
            else:
                print(f"  ✅ 关节{i}: {pos:.4f} rad (安全)")

        return all_safe

    def check_zero_offset(self, measured_positions):
        """检查零位偏移（真实机器人上电后读取）"""
        print("\n零位偏移检查:")
        offsets = []

        for i, (measured, reference) in enumerate(zip(measured_positions, self.reference_positions)):
            offset = measured - reference
            offsets.append(offset)
            if abs(offset) > 0.05:
                print(f"  ❌ 关节{i}: 偏移 {offset:.4f} rad (>{0.05} rad)")
            else:
                print(f"  ✅ 关节{i}: 偏移 {offset:.4f} rad")

        self.calibration_results = {"offsets": offsets}
        return all(abs(o) <= 0.05 for o in offsets)

    def print_joint_ranges(self):
        """打印关节范围"""
        print("\nFranka Panda 关节范围 (rad):")
        print(f"{'关节':<6} {'下限':<10} {'上限':<10} {'参考位置':<12}")
        print("-" * 42)
        for i in range(7):
            print(f"{i:<6} {JOINT_LIMITS['lower'][i]:<10.4f} "
                  f"{JOINT_LIMITS['upper'][i]:<10.4f} "
                  f"{START_JOINT_POSITIONS[i]:<12.4f}")


def run_full_validation(target=None):
    """运行完整的部署校准验证"""
    print("=" * 70)
    print("  部署校准与验证")
    print("=" * 70)

    # 1. 关节范围验证
    calibrator = JointCalibrator()
    calibrator.print_joint_ranges()
    calibrator.validate_joint_positions(START_JOINT_POSITIONS)

    # 2. 工作空间验证
    validator = WorkspaceValidator()
    validator.scan_workspace_boundary(num_points=16)

    # 3. 目标点验证
    if target:
        validator.check_target(target)
    else:
        validator.generate_safe_targets(n=5)

    # 4. 默认部署目标验证
    default_targets = [
        [0.3, 0.0, 0.5],
        [0.25, 0.1, 0.6],
        [0.35, -0.1, 0.4],
        [0.2, 0.2, 0.55],
    ]

    print("\n默认部署目标点验证:")
    for t in default_targets:
        safe, issues = validator.is_in_workspace(*t)
        status = "✅" if safe else "❌"
        print(f"  {status} ({t[0]:.2f}, {t[1]:.2f}, {t[2]:.2f})")

    print("\n" + "=" * 70)
    print("  验证完成")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="部署校准与验证工具")
    parser.add_argument("--workspace", action="store_true", help="验证工作空间")
    parser.add_argument("--target", type=float, nargs=3, metavar=("X", "Y", "Z"),
                        help="验证指定目标点")
    parser.add_argument("--calibrate", action="store_true", help="关节零位校准")
    parser.add_argument("--generate-targets", type=int, metavar="N",
                        help="生成N个安全目标点")
    parser.add_argument("--full", action="store_true", help="运行完整验证 (默认)")

    args = parser.parse_args()

    if args.workspace:
        validator = WorkspaceValidator()
        validator.scan_workspace_boundary()
        validator.generate_safe_targets(n=5)

    elif args.target:
        validator = WorkspaceValidator()
        validator.check_target(args.target)

    elif args.calibrate:
        calibrator = JointCalibrator()
        calibrator.print_joint_ranges()
        calibrator.validate_joint_positions(START_JOINT_POSITIONS)
        print("\n⚠️  真实机器人零位校准需要连接机械臂后执行")
        print("   1. 读取当前关节位置")
        print("   2. 与参考位置比较偏移")
        print("   3. 如果偏移过大，需要手动移动到零位")

    elif args.generate_targets:
        validator = WorkspaceValidator()
        validator.generate_safe_targets(n=args.generate_targets)

    else:
        run_full_validation(args.target)


if __name__ == "__main__":
    main()
