"""
轨迹规划日志与报告模块
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



import math
import csv

def generate_trajectory_report(report_filename, log_filename,
                               path_points, actual_positions,
                               joint_positions_history,
                               start_pos, target_pos,
                               interpolation_steps, move_speed):
    """
    生成轨迹跟踪报告和CSV日志
    """
    # ===== 先写CSV日志 =====
    with open(log_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["step", "target_x", "target_y", "target_z",
                  "actual_x", "actual_y", "actual_z",
                  "error_x", "error_y", "error_z", "error_mag"]
        writer.writerow(header)

        for i, (target, actual) in enumerate(zip(path_points, actual_positions)):
            error = [actual[j] - target[j] for j in range(3)]
            error_mag = math.sqrt(error[0]**2 + error[1]**2 + error[2]**2)
            row = [i] + target + list(actual) + error + [error_mag]
            writer.writerow(row)

    # ===== 生成文本报告 =====
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=== PyBullet 笛卡尔空间轨迹规划报告 ===\n\n")
        f.write(f"起点位置: x={start_pos[0]:.4f}, y={start_pos[1]:.4f}, z={start_pos[2]:.4f}\n")
        f.write(f"终点目标: x={target_pos[0]:.4f}, y={target_pos[1]:.4f}, z={target_pos[2]:.4f}\n")
        f.write(f"插值点数: {interpolation_steps}\n")
        f.write(f"运动速度: 每点 {move_speed} 步\n")
        f.write(f"总记录数: {len(path_points)}\n\n")

        # 计算误差统计
        errors = []
        for target, actual in zip(path_points, actual_positions):
            error = [actual[j] - target[j] for j in range(3)]
            error_mag = math.sqrt(error[0]**2 + error[1]**2 + error[2]**2)
            errors.append(error_mag)

        max_error = max(errors)
        avg_error = sum(errors) / len(errors)
        final_error = errors[-1]

        f.write("--- 路径跟踪误差统计 ---\n")
        f.write(f"  最大误差: {max_error:.4f} m\n")
        f.write(f"  平均误差: {avg_error:.4f} m\n")
        f.write(f"  终点误差: {final_error:.4f} m\n\n")

        # 诊断
        f.write("--- 诊断结论 ---\n")
        if final_error < 0.01:
            f.write("  ✅ 轨迹跟踪成功，终点误差小于 1cm。\n")
            f.write("  控制策略能准确跟踪笛卡尔空间直线路径。\n")
        elif final_error < 0.05:
            f.write("  ⚠️ 终点误差在 1-5cm 之间，可接受范围。\n")
            f.write("  建议检查目标点是否在可达空间边界。\n")
        else:
            f.write("  ❌ 终点误差超过 5cm，需要检查：\n")
            f.write("    1. 目标点是否超出机械臂工作空间\n")
            f.write("    2. IK 求解参数是否合理\n")
            f.write("    3. 运动过程中是否存在碰撞\n")

        # 关节角度记录（首、中、末）
        if len(joint_positions_history) >= 3:
            mid_idx = len(joint_positions_history) // 2
            f.write("\n--- 关节角度快照 (首/中/末) ---\n")
            f.write("起始关节角:\n")
            for i, j in enumerate(joint_positions_history[0]):
                f.write(f"  关节 {i}: {j:.4f} rad\n")
            f.write("中间关节角:\n")
            for i, j in enumerate(joint_positions_history[mid_idx]):
                f.write(f"  关节 {i}: {j:.4f} rad\n")
            f.write("终点关节角:\n")
            for i, j in enumerate(joint_positions_history[-1]):
                f.write(f"  关节 {i}: {j:.4f} rad\n")