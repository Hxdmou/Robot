"""
 PyBullet 真实物理参数边界迁移验证 v2
 优化：在轨迹跟踪中增加一步一补偿的闭环反馈
 目标：通信延迟场景下通过率 100%
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
import math
import csv
import random
import numpy as np

from config_real_boundary_fixed_v2 import (
    USE_KUKA,
    TARGET_END_POS,
    MASS_OFFSET_RANGE,
    JOINT_DAMPING_RANGE,
    FRICTION_COEFF_RANGE,
    COMM_DELAY_RANGE,
    NUM_RANDOM_TESTS,
    MOVE_SPEED,
    CONTROL_FORCE,
    VERBOSE
)
from logger_real_boundary_fixed_v2 import generate_boundary_report

# ================== 初始化 ==================
physicsClient = p.connect(p.GUI if VERBOSE else p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
p.setRealTimeSimulation(0)

plane_id = p.loadURDF("plane.urdf")

table_col = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.02])
table_vis = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.02],
                                 rgbaColor=[0.6, 0.4, 0.2, 1])
table_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=table_col,
                             baseVisualShapeIndex=table_vis, basePosition=[0.2, 0, -0.02])

# ================== 加载机械臂 ==================
urdf_path = "franka_panda/panda.urdf"
robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)

link_name_to_index = {}
for i in range(p.getNumJoints(robot_id)):
    info = p.getJointInfo(robot_id, i)
    link_name = info[12].decode('utf-8')
    link_name_to_index[link_name] = i

ee_index = link_name_to_index.get("panda_link8", -1)
if ee_index == -1:
    ee_index = p.getNumJoints(robot_id) - 2

print(f"[BOUNDARY] 末端链接: panda_link8, 索引: {ee_index}")

joint_indices = [0, 1, 2, 3, 4, 5, 6]
num_joints = 7

joint_lower_limits = []
joint_upper_limits = []
joint_ranges = []
joint_rest_poses = []

for i in joint_indices:
    info = p.getJointInfo(robot_id, i)
    lower = info[8]
    upper = info[9]
    range_val = upper - lower
    rest = (lower + upper) / 2
    joint_lower_limits.append(lower)
    joint_upper_limits.append(upper)
    joint_ranges.append(range_val)
    joint_rest_poses.append(rest)

START_JOINT_POSITIONS = [0, -0.785, 0, -2.356, 0, 1.571, 0.785]

# ================== 原始物理参数 ==================
original_masses = {}
original_joint_dampings = {}

def extract_urdf_params():
    for j_idx in joint_indices:
        dyn_info = p.getDynamicsInfo(robot_id, j_idx)
        joint_info = p.getJointInfo(robot_id, j_idx)
        if dyn_info:
            original_masses[j_idx] = dyn_info[0]
            original_joint_dampings[j_idx] = joint_info[6]

extract_urdf_params()
print(f"[BOUNDARY] 原始物理参数已提取")

# ================== 物理参数随机化 ==================
delay_buffer = []

def apply_parameter_offsets(mass_offset, damping_offset, friction_coeff, delay_steps):
    for j_idx in joint_indices:
        base_mass = original_masses.get(j_idx, 0.1)
        new_mass = base_mass * (1.0 + mass_offset)
        p.changeDynamics(robot_id, j_idx, mass=new_mass)

    for j_idx in joint_indices:
        base_damping = original_joint_dampings.get(j_idx, 0.001)
        new_damping = base_damping * (1.0 + damping_offset)
        p.changeDynamics(robot_id, j_idx, jointDamping=new_damping)
    return True

def get_delayed_command(current_command, delay_steps):
    if delay_steps <= 0:
        return current_command
    delay_buffer.append(current_command)
    if len(delay_buffer) > delay_steps + 1:
        delay_buffer.pop(0)
    if delay_buffer[0] is None:
        return current_command
    return delay_buffer[0]

# ================== 控制函数（带反馈补偿） ==================
def compute_ik(target_pos, current_pos=None, feedforward=False):
    if feedforward and current_pos is not None:
        error = [current_pos[i] - target_pos[i] for i in range(3)]
        compensation = [-error[i] * 0.5 for i in range(3)]
        adjusted_target = [target_pos[i] + compensation[i] for i in range(3)]
    else:
        adjusted_target = target_pos

    ik_joints = p.calculateInverseKinematics(
        robot_id,
        ee_index,
        adjusted_target,
        targetOrientation=[0, 0, 0, 1],
        lowerLimits=joint_lower_limits,
        upperLimits=joint_upper_limits,
        jointRanges=joint_ranges,
        restPoses=joint_rest_poses,
        maxNumIterations=2000,
        residualThreshold=1e-6
    )
    target_joints = []
    for idx in joint_indices:
        if idx < len(ik_joints):
            target_joints.append(ik_joints[idx])
        else:
            target_joints.append(0.0)
    return target_joints

def move_to_position(target_pos, steps=MOVE_SPEED, friction_coeff=0.0, current_pos=None):
    target_joints = compute_ik(target_pos, current_pos, feedforward=True)
    for idx, joint_idx in enumerate(joint_indices):
        p.setJointMotorControl2(robot_id, joint_idx, p.POSITION_CONTROL,
                               targetPosition=target_joints[idx], force=CONTROL_FORCE)

    for _ in range(steps):
        if friction_coeff != 0:
            for j_idx in joint_indices:
                joint_state = p.getJointState(robot_id, j_idx)
                vel = joint_state[1]
                if abs(vel) > 0.001:
                    friction_force = -friction_coeff * math.copysign(1, vel) * 0.5
                    p.applyExternalForce(robot_id, j_idx,
                                        [0, 0, 0],
                                        [friction_force * 0.01, 0, 0],
                                        p.LINK_FRAME)
        p.stepSimulation()
        time.sleep(0.001)

    link_state = p.getLinkState(robot_id, ee_index)
    return link_state[0]

def reset_robot():
    for idx, joint_idx in enumerate(joint_indices):
        p.resetJointState(robot_id, joint_idx, START_JOINT_POSITIONS[idx])
    for _ in range(50):
        p.stepSimulation()

def execute_task(target_pos, delay_steps, friction_coeff):
    reset_robot()

    start_pos = [0.0, 0.0, 0.6]
    num_steps = 30
    trajectory = []
    for i in range(num_steps + 1):
        t = i / num_steps
        x = start_pos[0] + (target_pos[0] - start_pos[0]) * t
        y = start_pos[1] + (target_pos[1] - start_pos[1]) * t
        z = start_pos[2] + (target_pos[2] - start_pos[2]) * t
        trajectory.append([x, y, z])

    delay_buffer.clear()
    last_actual = None

    for target_point in trajectory:
        delayed_target = get_delayed_command(target_point, delay_steps)

        # 闭环反馈：用上一次的实际位置补偿目标点
        actual_pos = move_to_position(delayed_target, MOVE_SPEED, friction_coeff, last_actual)
        last_actual = actual_pos

    link_state = p.getLinkState(robot_id, ee_index)
    final_pos = link_state[0]
    final_error = math.sqrt(
        (final_pos[0] - target_pos[0])**2 +
        (final_pos[1] - target_pos[1])**2 +
        (final_pos[2] - target_pos[2])**2
    )
    return final_error

# ================== 边界测试主循环 ==================
print(f"\n[BOUNDARY] 开始物理参数边界验证 v2（闭环反馈）")
print(f"[BOUNDARY] 测试参数范围:")
print(f"  质量偏移: ±{MASS_OFFSET_RANGE*100:.0f}%")
print(f"  阻尼偏移: ±{JOINT_DAMPING_RANGE*100:.0f}%")
print(f"  摩擦系数: 0 ~ {FRICTION_COEFF_RANGE}")
print(f"  通信延迟: 0 ~ {COMM_DELAY_RANGE} 步")
print(f"[BOUNDARY] 随机测试次数: {NUM_RANDOM_TESTS}")
print(f"[BOUNDARY] 末端链接: panda_link8, 控制力: {CONTROL_FORCE}")
print(f"[BOUNDARY] 反馈补偿: 开启 (增益 0.5)\n")

test_results = []
success_count = 0

for test_id in range(NUM_RANDOM_TESTS):
    mass_offset = random.uniform(-MASS_OFFSET_RANGE, MASS_OFFSET_RANGE)
    damping_offset = random.uniform(-JOINT_DAMPING_RANGE, JOINT_DAMPING_RANGE)
    friction_coeff = random.uniform(0, FRICTION_COEFF_RANGE)
    delay_steps = random.randint(0, int(COMM_DELAY_RANGE))

    apply_parameter_offsets(mass_offset, damping_offset, friction_coeff, delay_steps)

    target_pos = TARGET_END_POS
    final_error = execute_task(target_pos, delay_steps, friction_coeff)

    passed = final_error < 0.02
    if passed:
        success_count += 1

    test_results.append({
        "test_id": test_id + 1,
        "mass_offset": mass_offset,
        "damping_offset": damping_offset,
        "friction_coeff": friction_coeff,
        "delay_steps": delay_steps,
        "final_error": final_error,
        "passed": passed
    })

    if (test_id + 1) % 10 == 0:
        print(f"[BOUNDARY] 已完成 {test_id+1}/{NUM_RANDOM_TESTS} 次测试, 当前通过率: {success_count/(test_id+1)*100:.1f}%")

# ================== 恢复原始参数 ==================
print("[BOUNDARY] 恢复原始物理参数...")
for j_idx in joint_indices:
    base_mass = original_masses.get(j_idx, 0.1)
    base_damping = original_joint_dampings.get(j_idx, 0.001)
    p.changeDynamics(robot_id, j_idx, mass=base_mass, jointDamping=base_damping)

# ================== 分析结果 ==================
pass_rate = success_count / NUM_RANDOM_TESTS * 100

passed_results = [r for r in test_results if r["passed"]]
mass_min = min([r["mass_offset"] for r in passed_results]) if passed_results else None
mass_max = max([r["mass_offset"] for r in passed_results]) if passed_results else None
damping_min = min([r["damping_offset"] for r in passed_results]) if passed_results else None
damping_max = max([r["damping_offset"] for r in passed_results]) if passed_results else None
friction_max = max([r["friction_coeff"] for r in passed_results]) if passed_results else 0
delay_max = max([r["delay_steps"] for r in passed_results]) if passed_results else 0

print(f"\n[BOUNDARY] === 迁移验证完成 v2 ===")
print(f"  总测试数: {NUM_RANDOM_TESTS}")
print(f"  通过数: {success_count}")
print(f"  通过率: {pass_rate:.1f}%")

# ================== 生成报告 ==================
generate_boundary_report(
    report_filename=os.path.join(PROJECT_ROOT, "boundary_fixed_v2_report.txt"),
    log_filename=os.path.join(PROJECT_ROOT, "boundary_fixed_v2_log.csv"),
    test_results=test_results,
    pass_rate=pass_rate,
    mass_min=mass_min,
    mass_max=mass_max,
    damping_min=damping_min,
    damping_max=damping_max,
    friction_max=friction_max,
    delay_max=delay_max,
    num_tests=NUM_RANDOM_TESTS,
    mass_range=MASS_OFFSET_RANGE,
    damping_range=JOINT_DAMPING_RANGE,
    friction_range=FRICTION_COEFF_RANGE,
    delay_range=COMM_DELAY_RANGE,
    control_force=CONTROL_FORCE
)

print("[BOUNDARY] 报告已生成: {output_path}/boundary_fixed_v2_report.txt")
print("[BOUNDARY] 按 Ctrl+C 退出。")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("[BOUNDARY] 用户中断，程序退出。")
    p.disconnect()
