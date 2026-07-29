""" 
工作空间分析日志与报告模块 
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

def generate_workspace_report(report_filename, log_filename, 
                              reachable_points, unreachable_points, 
                              total_points, 
                              boundary_x, boundary_y, boundary_z, 
                              recommended_positions, 
                              x_range, y_range, z_range, 
                              x_samples, y_samples, z_samples, 
                              ik_max_iterations, ik_residual_threshold): 
    """ 
    生成工作空间分析报告 
    """ 
    # ===== 写CSV日志 ===== 
    with open(log_filename, 'w', newline='', encoding='utf-8') as f: 
        writer = csv.writer(f) 
        header = ["point_x", "point_y", "point_z", "reachable", "error_mm"] 
        writer.writerow(header) 

        for p in reachable_points: 
            writer.writerow([p["pos"][0], p["pos"][1], p["pos"][2], 1, p["error"] * 1000]) 
        for p in unreachable_points: 
            writer.writerow([p["pos"][0], p["pos"][1], p["pos"][2], 0, p["error"] * 1000]) 

    # ===== 生成文本报告 ===== 
    with open(report_filename, 'w', encoding='utf-8') as f: 
        f.write("=== PyBullet 机械臂工作空间分析报告 ===\n\n") 

        f.write("--- 采样配置 ---\n") 
        f.write(f"  X 范围: {x_range} m, 采样数: {x_samples}\n") 
        f.write(f"  Y 范围: {y_range} m, 采样数: {y_samples}\n") 
        f.write(f"  Z 范围: {z_range} m, 采样数: {z_samples}\n") 
        f.write(f"  总采样点: {x_samples * y_samples * z_samples}\n") 
        f.write(f"  IK 最大迭代: {ik_max_iterations}\n") 
        f.write(f"  IK 残差阈值: {ik_residual_threshold}\n\n") 

        f.write("--- 采样结果 ---\n") 
        f.write(f"  总采样点: {total_points}\n") 
        f.write(f"  可达点: {len(reachable_points)}\n") 
        f.write(f"  不可达点: {len(unreachable_points)}\n") 
        f.write(f"  可达率: {len(reachable_points)/total_points*100:.1f}%\n\n") 

        f.write("--- 可达区域边界 ---\n") 
        f.write(f"  X 轴: {boundary_x[0]:.3f} ~ {boundary_x[1]:.3f} m\n") 
        f.write(f"  Y 轴: {boundary_y[0]:.3f} ~ {boundary_y[1]:.3f} m\n") 
        f.write(f"  Z 轴: {boundary_z[0]:.3f} ~ {boundary_z[1]:.3f} m\n\n") 

        if recommended_positions: 
            f.write("--- 推荐放置位置（已验证可达） ---\n") 
            for i, pos in enumerate(recommended_positions): 
                f.write(f"  位置 {i+1}: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}] m\n") 
        else: 
            f.write("--- 未找到推荐放置位置 ---\n") 
            f.write("  建议：调整采样范围或增加采样密度\n") 

        f.write("\n--- 诊断结论 ---\n") 
        if len(reachable_points) / total_points > 0.5: 
            f.write("  ✅ 可达区域覆盖率 > 50%，工作空间充足\n") 
            f.write("     可用于后续抓取-放置操作\n") 
        elif len(reachable_points) / total_points > 0.3: 
            f.write("  ⚠️ 可达区域覆盖率 30-50%，建议检查采样范围\n") 
        else: 
            f.write("  ❌ 可达区域覆盖率低于 30%，需扩大采样范围\n") 

        f.write("\n  💡 使用建议:\n") 
        f.write("     1. 将物体的抓取和放置位置设置在可达区域内\n") 
        f.write("     2. 避免在边界位置进行精细操作\n") 
        f.write("     3. 为后续动态场景预留足够的工作空间余量\n")