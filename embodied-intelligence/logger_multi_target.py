"""
多目标点连续运动日志与报告模块
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
import os

def generate_multi_target_report(report_filename, log_filename,
                                  target_sequence,
                                  all_path_points, all_actual_positions,
                                  all_joint_positions, all_segment_errors,
                                  segment_collision_status,
                                  obstacles, safety_multiplier,
                                  rrt_iterations, rrt_step_size, goal_bias):
    """
    生成多目标点连续运动报告
    """
    with open(log_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["segment", "step_in_segment", "target_x", "target_y", "target_z",
                  "actual_x", "actual_y", "actual_z",
                  "error_x", "error_y", "error_z", "error_mag"]
        writer.writerow(header)

        global_step = 0
        for seg_idx, (path_points, actual_positions) in enumerate(
            zip(all_path_points, all_actual_positions)
        ):
            for i, (target, actual) in enumerate(zip(path_points, actual_positions)):
                error = [actual[j] - target[j] for j in range(3)]
                error_mag = math.sqrt(error[0]**2 + error[1]**2 + error[2]**2)
                row = [seg_idx, i] + target + list(actual) + error + [error_mag]
                writer.writerow(row)

    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=== PyBullet 多目标点连续运动报告 ===\n\n")
        f.write(f"目标点序列: {len(target_sequence)} 个点\n")
        for i, pos in enumerate(target_sequence):
            f.write(f"  点 {i}: {pos}\n")
        f.write(f"障碍物数量: {len(obstacles)}\n")
        for idx, obs in enumerate(obstacles):
            f.write(f"  障碍物 {idx+1}: 位置 {obs['pos']}, 半径 {obs['radius']}m\n")
        f.write(f"安全距离系数: {safety_multiplier}\n")
        f.write(f"RRT 迭代次数: {rrt_iterations}\n")
        f.write(f"RRT 步长: {rrt_step_size} m\n")
        f.write(f"终点偏置率: {goal_bias * 100}%\n")
        f.write(f"总段数: {len(all_path_points)}\n\n")

        f.write("--- 各段误差统计 ---\n")
        for seg_idx, errors in enumerate(all_segment_errors):
            max_err = max(errors)
            avg_err = sum(errors) / len(errors)
            final_err = errors[-1]
            status = "❌ 碰撞" if segment_collision_status[seg_idx] else "✅ 安全"
            f.write(f"  段 {seg_idx+1}: 最大误差 {max_err*1000:.2f}mm, "
                    f"平均误差 {avg_err*1000:.2f}mm, "
                    f"终点误差 {final_err*1000:.2f}mm, {status}\n")

        all_errors = [e for segment in all_segment_errors for e in segment]
        if all_errors:
            overall_max = max(all_errors)
            overall_avg = sum(all_errors) / len(all_errors)
            overall_final = all_segment_errors[-1][-1] if all_segment_errors else 0
        else:
            overall_max = overall_avg = overall_final = 0

        f.write("\n--- 总体误差统计 ---\n")
        f.write(f"  总体最大误差: {overall_max*1000:.2f}mm\n")
        f.write(f"  总体平均误差: {overall_avg*1000:.2f}mm\n")
        f.write(f"  最终终点误差: {overall_final*1000:.2f}mm\n")

        any_collision = any(segment_collision_status)
        f.write("\n--- 碰撞检测汇总 ---\n")
        if any_collision:
            f.write("  ❌ 存在碰撞段\n")
        else:
            f.write("  ✅ 所有段均无碰撞\n")

        total_path_length = 0
        for path_points in all_path_points:
            if len(path_points) > 1:
                seg_length = 0
                for i in range(len(path_points) - 1):
                    dx = path_points[i+1][0] - path_points[i][0]
                    dy = path_points[i+1][1] - path_points[i][1]
                    dz = path_points[i+1][2] - path_points[i][2]
                    seg_length += math.sqrt(dx*dx + dy*dy + dz*dz)
                total_path_length += seg_length

        straight_length = 0
        for i in range(len(target_sequence) - 1):
            dx = target_sequence[i+1][0] - target_sequence[i][0]
            dy = target_sequence[i+1][1] - target_sequence[i][1]
            dz = target_sequence[i+1][2] - target_sequence[i][2]
            straight_length += math.sqrt(dx*dx + dy*dy + dz*dz)

        f.write("\n--- 路径长度汇总 ---\n")
        f.write(f"  规划总路径长度: {total_path_length:.4f} m\n")
        f.write(f"  直线总路径长度: {straight_length:.4f} m\n")
        f.write(f"  路径增加比例: {(total_path_length / straight_length - 1) * 100:.1f}%\n")

        f.write("\n--- 诊断结论 ---\n")
        if any_collision:
            f.write("  ❌ 存在碰撞，需要调整避障参数\n")
        elif overall_final > 0.01:
            f.write(f"  ⚠️ 最终终点误差 {overall_final*1000:.2f}mm，略大\n")
        else:
            f.write("  ✅ 多目标点连续运动成功！\n")
            f.write(f"     - 共 {len(all_path_points)} 段，全部无碰撞\n")
            f.write(f"     - 最终终点误差 {overall_final*1000:.2f}mm\n")
            f.write(f"     - 路径增加比例 {(total_path_length / straight_length - 1) * 100:.1f}%\n")
            f.write("  可以进一步扩展：\n")
            f.write("    1. 路径平滑（B样条/贝塞尔曲线）\n")
            f.write("    2. 动态障碍物\n")
            f.write("    3. 夹爪控制（抓取）\n")