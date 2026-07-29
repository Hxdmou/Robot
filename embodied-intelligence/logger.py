"""
日志与报告模块
提供数据采集、偏差计算、报告生成功能
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
import pybullet as p

def log_baseline_data(robot_id, joint_indices, ee_index, num_joints, step_count, USE_KUKA):
    """
    采集当前仿真状态的数据
    返回一行记录（列表）
    """
    # 1. 读取关节状态
    joint_positions = []
    joint_velocities = []
    for j_idx in joint_indices:
        state = p.getJointState(robot_id, j_idx)
        joint_positions.append(state[0])
        joint_velocities.append(state[1])

    # 2. 读取末端位姿
    link_state = p.getLinkState(robot_id, ee_index)
    ee_pos = link_state[0]
    ee_orn = link_state[1]
    ee_euler = p.getEulerFromQuaternion(ee_orn)

    # 3. 计算与直立目标的偏差
    if USE_KUKA:
        target_ee_pos = [0.3, 0, 0.5]
    else:
        target_ee_pos = [0, 0, 0.6]

    deviation = [ee_pos[i] - target_ee_pos[i] for i in range(3)]

    # 组装行数据
    row = [step_count] + joint_positions + joint_velocities + \
          list(ee_pos) + list(ee_euler) + deviation
    return row

def generate_report(report_filename, data_rows, num_joints, USE_KUKA, total_steps, log_interval):
    """
    生成汇总报告
    """
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("=== PyBullet 仿真基线数据采集报告 ===\n")
        f.write(f"机械臂类型: {'KUKA iiwa' if USE_KUKA else 'Franka Panda'}\n")
        f.write(f"仿真步数: {total_steps}\n")
        f.write(f"记录间隔: 每 {log_interval} 步\n")
        f.write(f"总记录数: {len(data_rows)}\n\n")

        if not data_rows:
            f.write("无有效数据记录。\n")
            return

        # 最后一组数据（稳定状态）
        last_row = data_rows[-1]
        joint_pos_last = last_row[1:1+num_joints]
        f.write("--- 稳定状态关节位置 (rad) ---\n")
        for i, pos in enumerate(joint_pos_last):
            f.write(f"  关节 {i}: {pos:.4f}\n")

        ee_pos_last = last_row[1+2*num_joints:1+2*num_joints+3]
        f.write(f"\n--- 稳定状态末端位置 (m) ---\n")
        f.write(f"  x: {ee_pos_last[0]:.4f}, y: {ee_pos_last[1]:.4f}, z: {ee_pos_last[2]:.4f}\n")

        dev_last = last_row[1+2*num_joints+6:1+2*num_joints+9]
        f.write(f"\n--- 与直立目标的偏差 (m) ---\n")
        f.write(f"  dx: {dev_last[0]:.4f}, dy: {dev_last[1]:.4f}, dz: {dev_last[2]:.4f}\n")
        f.write(f"  综合偏差: {math.sqrt(dev_last[0]**2 + dev_last[1]**2 + dev_last[2]**2):.4f} m\n")

        # 全时段偏差统计
        if len(data_rows) > 10:
            dev_x = [row[1+2*num_joints+6] for row in data_rows]
            dev_y = [row[1+2*num_joints+7] for row in data_rows]
            dev_z = [row[1+2*num_joints+8] for row in data_rows]

            mean_x = sum(dev_x) / len(dev_x)
            mean_y = sum(dev_y) / len(dev_y)
            mean_z = sum(dev_z) / len(dev_z)

            std_x = math.sqrt(sum((x - mean_x)**2 for x in dev_x) / len(dev_x))
            std_y = math.sqrt(sum((y - mean_y)**2 for y in dev_y) / len(dev_y))
            std_z = math.sqrt(sum((z - mean_z)**2 for z in dev_z) / len(dev_z))

            f.write("\n--- 偏差统计 (全时段) ---\n")
            f.write(f"  dx 均值: {mean_x:.4f} m, 标准差: {std_x:.4f}\n")
            f.write(f"  dy 均值: {mean_y:.4f} m, 标准差: {std_y:.4f}\n")
            f.write(f"  dz 均值: {mean_z:.4f} m, 标准差: {std_z:.4f}\n")