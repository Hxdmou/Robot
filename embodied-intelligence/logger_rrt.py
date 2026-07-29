"""
RRT 避障路径规划日志与报告模块（优化版）
新增：安全距离、路径点插值信息
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

def generate_rrt_report(report_filename, log_filename,
                         path_points, actual_positions,
                         joint_positions_history,
                         start_pos, target_pos,
                         obstacle_pos, obstacle_radius,
                         safety_margin,
                         rrt_iterations, rrt_step_size, goal_bias,
                         collision_detected, move_speed,
                         nodes_count, goal_reached,
                         raw_path_len, interp_points, final_path_len):
    """
    生成 RRT 避障路径规划报告
    """
    # ===== 写CSV日志 =====
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
        f.write("=== PyBullet RRT 避障路径规划报告（优化版） ===\n\n")
        f.write(f"起点位置: {start_pos}\n")
        f.write(f"终点目标: {target_pos}\n")
        f.write(f"障碍物位置: {obstacle_pos}, 物理半径: {obstacle_radius} m\n")
        f.write(f"碰撞安全距离: {obstacle_radius * safety_margin:.3f} m（{safety_margin}倍半径）\n")
        f.write(f"RRT 迭代次数: {rrt_iterations}\n")
        f.write(f"RRT 步长: {rrt_step_size} m\n")
        f.write(f"终点偏置率: {goal_bias * 100}%\n")
        f.write(f"原始路径点数: {raw_path_len}\n")
        f.write(f"插值点数/间隔: {interp_points}\n")
        f.write(f"最终路径点数: {final_path_len}\n")
        f.write(f"RRT 树节点数: {nodes_count}\n")
        f.write(f"目标到达: {'是' if goal_reached else '否'}\n\n")

        # 误差统计
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

        # 碰撞检测结果
        f.write("--- 碰撞检测结果 ---\n")
        if collision_detected:
            f.write("  ❌ 碰撞检测触发！路径存在碰撞风险。\n")
            f.write("  建议：增大安全距离或增加路径点密度。\n\n")
        else:
            f.write("  ✅ 未发生碰撞，避障路径安全。\n\n")

        # 路径长度分析
        if len(path_points) > 1:
            path_length = 0
            for i in range(len(path_points) - 1):
                dx = path_points[i+1][0] - path_points[i][0]
                dy = path_points[i+1][1] - path_points[i][1]
                dz = path_points[i+1][2] - path_points[i][2]
                path_length += math.sqrt(dx*dx + dy*dy + dz*dz)

            straight_length = math.sqrt(
                (target_pos[0] - start_pos[0])**2 +
                (target_pos[1] - start_pos[1])**2 +
                (target_pos[2] - start_pos[2])**2
            )

            f.write("--- 路径长度分析 ---\n")
            f.write(f"  规划路径长度: {path_length:.4f} m\n")
            f.write(f"  直线路径长度: {straight_length:.4f} m\n")
            f.write(f"  路径增加比例: {(path_length / straight_length - 1) * 100:.1f}%\n\n")

        # 诊断结论
        f.write("--- 诊断结论 ---\n")
        if collision_detected:
            f.write("  ❌ 碰撞检测未通过，路径不安全。\n")
            f.write("  建议：增大安全距离系数或调整障碍物位置。\n")
        elif not goal_reached:
            f.write("  ⚠️ 未找到到达终点的路径。\n")
            f.write("  建议：增加迭代次数或减小步长。\n")
        elif final_error > 0.01:
            f.write(f"  ⚠️ 终点误差 {final_error*1000:.1f}mm，略大于目标值。\n")
            f.write("  建议：检查终点IK验证逻辑。\n")
        else:
            f.write(f"  ✅ RRT 避障路径规划成功！\n")
            f.write(f"     - 路径安全，无碰撞（安全距离 {obstacle_radius * safety_margin:.3f}m）\n")
            f.write(f"     - 终点误差 {final_error*1000:.1f}mm\n")
            f.write(f"     - 路径长度增加 {(path_length / straight_length - 1) * 100:.1f}%\n")
            f.write(f"     - 原始路径点 {raw_path_len} 个 → 插值后 {final_path_len} 个\n")
            f.write("  可以基于此方案进一步扩展：\n")
            f.write("    1. 多障碍物场景\n")
            f.write("    2. 动态障碍物实时重规划\n")
            f.write("    3. 路径平滑（B样条/贝塞尔曲线）\n")