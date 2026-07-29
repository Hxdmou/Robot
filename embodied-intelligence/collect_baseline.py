"""
PyBullet 仿真基线数据采集脚本
功能：采集当前仿真环境下的姿态数据（包括与直立姿态的偏差），
      用于判断姿态倒立的量化程度和控制稳定性。
使用方法：
  1. 将本文件及同目录下的 config.py、logger.py 保存在 F:/具身智能/
  2. 在终端运行：python collect_baseline.py
  3. 查看 F:/具身智能/ 下的 baseline_report.txt 和 baseline_log.csv
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



import pybullet as p
import pybullet_data
import time
import csv
import os
import math

# 导入配置和日志模块（同目录下）
from config import USE_KUKA, SIMULATION_STEPS, LOG_INTERVAL, TARGET_JOINT_POSITIONS
from logger import log_baseline_data, generate_report

# ================== 初始化仿真环境 ==================
physicsClient = p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
p.setRealTimeSimulation(0)

# 加载地面
plane_id = p.loadURDF("plane.urdf")

# ================== 加载机械臂 ==================
urdf_path = ""
robot_id = None
joint_indices = []
num_joints = 0

if USE_KUKA:
    urdf_path = "kuka_iiwa/model.urdf"
    robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)
    joint_indices = [0, 1, 2, 3, 4, 5, 6]
    num_joints = 7
else:
    urdf_path = "franka_panda/panda.urdf"
    robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)
    joint_indices = [0, 1, 2, 3, 4, 5, 6]
    num_joints = 7

print(f"[INFO] 加载机械臂: {urdf_path}")
print(f"[INFO] 使用关节索引: {joint_indices}")
print(f"[INFO] 目标关节角（直立参考）: {TARGET_JOINT_POSITIONS}")

# 设置初始状态为目标姿态
for idx, joint_idx in enumerate(joint_indices):
    p.resetJointState(robot_id, joint_idx, TARGET_JOINT_POSITIONS[idx])

# ================== 准备日志文件 ==================
log_filename = os.path.join(PROJECT_ROOT, "baseline_log.csv")
report_filename = os.path.join(PROJECT_ROOT, "baseline_report.txt")

csv_file = open(log_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

header = ["step"] + [f"joint_{j}_pos" for j in range(num_joints)] + \
         [f"joint_{j}_vel" for j in range(num_joints)] + \
         ["ee_x", "ee_y", "ee_z", "ee_roll", "ee_pitch", "ee_yaw",
          "deviation_x", "deviation_y", "deviation_z"]
csv_writer.writerow(header)

print("[INFO] 开始仿真数据采集...")

# 获取末端执行器索引
num_joints_total = p.getNumJoints(robot_id)
ee_index = num_joints_total - 1

step_count = 0
data_rows = []

# ================== 主仿真循环 ==================
for step in range(SIMULATION_STEPS):
    p.stepSimulation()
    step_count += 1

    if step_count % LOG_INTERVAL == 0:
        row = log_baseline_data(robot_id, joint_indices, ee_index, num_joints, step_count, USE_KUKA)
        csv_writer.writerow(row)
        data_rows.append(row)

    if step_count % 1000 == 0:
        print(f"[INFO] 已采集 {step_count}/{SIMULATION_STEPS} 步")

    time.sleep(0.001)

csv_file.close()
print(f"[INFO] 数据采集完成！共采集 {len(data_rows)} 条记录。")

# ================== 生成报告 ==================
generate_report(report_filename, data_rows, num_joints, USE_KUKA, SIMULATION_STEPS, LOG_INTERVAL)

print(f"[INFO] 日志已保存至: {log_filename}")
print(f"[INFO] 报告已保存至: {report_filename}")
print("[INFO] 脚本执行完毕。按 Ctrl+C 退出。")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("[INFO] 用户中断，程序退出。")
    p.disconnect()