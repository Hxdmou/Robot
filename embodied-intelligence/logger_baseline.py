"""
基线精度日志与报告模块
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

def generate_baseline_report(report_filename, log_filename,
                            final_errors, max_errors, avg_errors,
                            trajectory, actual_positions,
                            target_pos, num_repeats, num_points, move_speed,
                            pass_2cm, pass_5mm,
                            mean_final, std_final, mean_max, std_max,
                            mean_avg, std_avg, min_final, max_final):
    """
    生成基线精度报告
    """
    # ===== 写CSV日志 =====
    with open(log_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["repeat", "step", "target_x", "target_y", "target_z",
                  "actual_x", "actual_y", "actual_z", "error_mm"]
        writer.writerow(header)

        for repeat_idx in range(num_repeats):
            # 每个重复测试对应一组路径数据
            for step_idx in range(len(trajectory)):
                target = trajectory[step_idx]
                actual = actual_positions[step_idx]
                err = math.sqrt(
                    (actual[0] - target[0])**2 +
                    (actual[1] - target[1])**2 +
                    (actual[2] - target[2])**2
                )
                writer.writerow([repeat_idx, step_idx] +
                               list(target) + list(actual) + [err * 1000])

    # ===== 生成文本报告 =====
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=== PyBullet 控制策略基线精度测试报告 ===\n\n")

        f.write("--- 测试配置 ---\n")
        f.write(f"  重复测试次数: {num_repeats}\n")
        f.write(f"  目标位置: {target_pos}\n")
        f.write(f"  轨迹点数: {num_points}\n")
        f.write(f"  每点仿真步数: {move_speed}\n\n")

        f.write("--- 基线精度统计 ---\n")
        f.write(f"  终点误差均值: {mean_final*1000:.2f} mm\n")
        f.write(f"  终点误差标准差: {std_final*1000:.2f} mm\n")
        f.write(f"  终点误差范围: {min_final*1000:.2f} ~ {max_final*1000:.2f} mm\n")
        f.write(f"  最大误差均值: {mean_max*1000:.2f} mm\n")
        f.write(f"  最大误差范围: {np.min(max_errors)*1000:.2f} ~ {np.max(max_errors)*1000:.2f} mm\n")
        f.write(f"  平均误差均值: {mean_avg*1000:.2f} mm\n\n")

        f.write("--- 阈值判断 ---\n")
        f.write(f"  通过2cm阈值: {'✅ 是' if pass_2cm else '❌ 否'}\n")
        f.write(f"  通过5mm阈值: {'✅ 是' if pass_5mm else '❌ 否'}\n\n")

        # 各次测试详细结果
        f.write("--- 各次测试详细结果 ---\n")
        for i in range(num_repeats):
            f.write(f"  测试 {i+1}: 终点误差 {final_errors[i]*1000:.2f}mm, 最大误差 {max_errors[i]*1000:.2f}mm\n")

        # 诊断结论
        f.write("\n--- 诊断结论 ---\n")
        if pass_2cm:
            f.write("  ✅ 基线精度达到2cm阈值，控制策略本身成立\n")
            f.write("     0%通过率的原因是参数偏移范围过大或测试条件过严\n")
            f.write("     建议: 缩小参数偏移范围重新验证\n")
        else:
            f.write("  ❌ 基线精度未达到2cm阈值，控制策略本身需要优化\n")
            f.write("     建议: 增加仿真步数、调整控制参数或增加IK迭代次数\n")

        if pass_5mm:
            f.write("  ✅ 基线精度达到5mm阈值，精度裕量充足\n")
            f.write("     进一步参数偏移验证可设定更严格的标准\n")
