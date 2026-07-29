"""
路径平滑日志与报告模块
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

def generate_smooth_report(report_filename, log_filename,
                           raw_path, smooth_path, actual_positions,
                           raw_length, smooth_length,
                           raw_curvature, smooth_curvature,
                           max_error, avg_error, final_error,
                           collision_detected,
                           smooth_order, smooth_step_size):
    """
    生成路径平滑报告
    """
    # ===== 写CSV日志 =====
    with open(log_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["step", "target_x", "target_y", "target_z",
                  "actual_x", "actual_y", "actual_z",
                  "error_x", "error_y", "error_z", "error_mag"]
        writer.writerow(header)

        for i, (target, actual) in enumerate(zip(smooth_path, actual_positions)):
            error = [actual[j] - target[j] for j in range(3)]
            error_mag = math.sqrt(error[0]**2 + error[1]**2 + error[2]**2)
            row = [i] + target + list(actual) + error + [error_mag]
            writer.writerow(row)

    # ===== 生成文本报告 =====
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=== PyBullet 路径平滑报告 ===\n\n")
        f.write(f"B样条阶数: {smooth_order}\n")
        f.write(f"平滑步长: {smooth_step_size} m\n\n")

        # 路径对比
        f.write("--- 路径对比 ---\n")
        f.write(f"原始路径点数: {len(raw_path)}\n")
        f.write(f"平滑路径点数: {len(smooth_path)}\n")
        f.write(f"原始路径长度: {raw_length:.4f} m\n")
        f.write(f"平滑路径长度: {smooth_length:.4f} m\n")
        f.write(f"长度变化: {(smooth_length - raw_length) / raw_length * 100:.2f}%\n")
        f.write(f"原始最大曲率: {raw_curvature:.6f}\n")
        f.write(f"平滑最大曲率: {smooth_curvature:.6f}\n")
        if raw_curvature > 0:
            f.write(f"曲率降低: {(1 - smooth_curvature/raw_curvature) * 100:.2f}%\n\n")

        # 执行结果
        f.write("--- 执行结果 ---\n")
        f.write(f"最大误差: {max_error*1000:.2f} mm\n")
        f.write(f"平均误差: {avg_error*1000:.2f} mm\n")
        f.write(f"终点误差: {final_error*1000:.2f} mm\n")
        f.write(f"碰撞检测: {'发生碰撞' if collision_detected else '安全'}\n\n")

        # 诊断结论
        f.write("--- 诊断结论 ---\n")
        if collision_detected:
            f.write("  ❌ 碰撞检测未通过\n")
        elif final_error > 0.01:
            f.write(f"  ⚠️ 终点误差 {final_error*1000:.2f}mm，略大\n")
        else:
            curve_reduction = (1 - smooth_curvature/raw_curvature) * 100 if raw_curvature > 0 else 0
            f.write("  ✅ 路径平滑成功！\n")
            f.write(f"     - 曲率降低 {curve_reduction:.1f}%\n")
            f.write(f"     - 终点误差 {final_error*1000:.2f}mm\n")
            f.write(f"     - 路径长度变化 {(smooth_length - raw_length) / raw_length * 100:.1f}%\n")
            f.write("  平滑后的路径更适合真实部署：\n")
            f.write("    1. 减少机械臂急停和抖动\n")
            f.write("    2. 降低关节磨损\n")
            f.write("    3. 提升运动连续性\n")
