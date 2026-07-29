"""
物理因素深化日志与报告模块
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
import numpy as np

def generate_physical_report(report_filename, log_filename,
                             trajectory_points, actual_positions,
                             commanded_positions, joint_velocities_history,
                             errors, tracking_errors,
                             max_error, avg_error, final_error,
                             smoothness_score, total_steps,
                             friction_enabled, sensor_noise_enabled,
                             comm_delay_enabled, gravity_comp_enabled,
                             comm_delay_steps, pos_noise_std, vel_noise_std):
    """
    生成物理因素深化仿真报告
    """
    # ===== 写CSV日志 =====
    with open(log_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["step", "target_x", "target_y", "target_z",
                  "actual_x", "actual_y", "actual_z",
                  "error_x", "error_y", "error_z", "error_mag",
                  "cmd_x", "cmd_y", "cmd_z"]
        writer.writerow(header)

        for i in range(len(actual_positions)):
            if i < len(trajectory_points):
                target = trajectory_points[i]
                actual = actual_positions[i]
                cmd = commanded_positions[i] if i < len(commanded_positions) else [0,0,0]
                err = tracking_errors[i] if i < len(tracking_errors) else [0,0,0]
                err_mag = math.sqrt(err[0]**2 + err[1]**2 + err[2]**2)
                row = [i] + list(target) + list(actual) + list(err) + [err_mag] + list(cmd)
                writer.writerow(row)

    # ===== 生成文本报告 =====
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=== PyBullet 物理因素深化仿真报告 ===\n\n")

        f.write("--- 物理因素状态 ---\n")
        f.write(f"  摩擦力: {'✅ 启用' if friction_enabled else '❌ 禁用'}\n")
        f.write(f"  传感器噪声: {'✅ 启用' if sensor_noise_enabled else '❌ 禁用'}\n")
        f.write(f"  通信延迟: {'✅ 启用' if comm_delay_enabled else '❌ 禁用'}\n")
        f.write(f"  重力补偿: {'✅ 启用' if gravity_comp_enabled else '❌ 禁用'}\n")
        if comm_delay_enabled:
            f.write(f"  通信延迟步数: {comm_delay_steps}\n")
        if sensor_noise_enabled:
            f.write(f"  位置噪声标准差: {pos_noise_std*1000:.2f} mm\n")
            f.write(f"  速度噪声标准差: {vel_noise_std*1000:.2f} mm/s\n")
        f.write("\n")

        f.write("--- 执行结果 ---\n")
        f.write(f"  总步数: {total_steps}\n")
        f.write(f"  轨迹点数: {len(trajectory_points)}\n")
        f.write(f"  实际记录点: {len(actual_positions)}\n")
        f.write(f"  最大误差: {max_error*1000:.2f} mm\n")
        f.write(f"  平均误差: {avg_error*1000:.2f} mm\n")
        f.write(f"  终点误差: {final_error*1000:.2f} mm\n")
        f.write(f"  平滑度评分: {smoothness_score:.4f}\n\n")

        # 误差分布
        if errors:
            errors_sorted = sorted(errors)
            p95 = errors_sorted[int(len(errors_sorted) * 0.95)] if len(errors_sorted) > 0 else 0
            f.write("--- 误差分布 ---\n")
            f.write(f"  95%分位数误差: {p95*1000:.2f} mm\n")
            f.write(f"  误差标准差: {np.std(errors)*1000:.2f} mm\n\n")

        # 诊断结论
        f.write("--- 诊断结论 ---\n")
        if final_error < 0.01:
            f.write("  ✅ 物理因素未显著影响控制精度\n")
            f.write("     控制策略对摩擦、噪声和延迟具有鲁棒性\n")
        elif final_error < 0.05:
            f.write("  ⚠️ 物理因素对控制精度有一定影响\n")
            f.write("     建议：调整控制参数或增加反馈补偿\n")
        else:
            f.write("  ❌ 物理因素显著影响控制精度\n")
            f.write("     建议：重新评估控制策略或减小物理因素强度\n")

        if friction_enabled and sensor_noise_enabled and comm_delay_enabled:
            f.write("\n  💡 当前已模拟完整的真实物理环境：\n")
            f.write("     - 关节摩擦力使启动/停止更平滑\n")
            f.write("     - 传感器噪声模拟真实编码器读数\n")
            f.write("     - 通信延迟模拟真实控制系统的滞后\n")
            f.write("     仿真验证的控制策略更接近真实部署表现\n")
