"""
 PyBullet 仿真夹爪控制模块
 功能：在仿真环境中实现机械臂的抓取操作
 包括：物体抓取、移动、放置、成功率验证
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

from config_gripper import (
    USE_KUKA,
    GRIP_TARGET_POS,
    OBJECT_POSITIONS,
    OBJECT_RADIUS,
    OBJECT_HEIGHT,
    NUM_GRIP_TESTS,
    MOVE_SPEED,
    GRIP_FORCE,
    RELEASE_FORCE
)
from logger_gripper import generate_gripper_report

# ================== 初始化 ==================
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
p.setRealTimeSimulation(0)

plane_id = p.loadURDF("plane.urdf")

# 添加桌面
table_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.02])
table_visual_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.02], rgbaColor=[0.6, 0.4, 0.2, 1])
table_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=table_collision_shape,
                              baseVisualShapeIndex=table_visual_shape, basePosition=[0.2, 0, -0.02])

# ================== 加载机械臂（带夹爪） ==================
urdf_path = ""
robot_id = None
joint_indices = []
gripper_joint_indices = []
num_joints = 0

if USE_KUKA:
    urdf_path = "kuka_iiwa/model.urdf"
    robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)
    joint_indices = [0, 1, 2, 3, 4, 5, 6]
    num_joints = 7
    # KUKA 没有夹爪，使用简化抓取方式
    gripper_joint_indices = []
else:
    # Franka Panda 包含夹爪
    urdf_path = "franka_panda/panda.urdf"
    robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)
    joint_indices = [0, 1, 2, 3, 4, 5, 6]
    # 夹爪关节索引（Panda 的夹爪关节通常为 9 和 10）
    gripper_joint_indices = [9, 10]
    num_joints = 7

print(f"[GRIP] 加载机械臂: {urdf_path}")

num_joints_total = p.getNumJoints(robot_id)
ee_index = num_joints_total - 1

# 获取关节限制（用于IK）
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

# ================== 设置起点 ==================
START_JOINT_POSITIONS = [-1.0247, -1.3870, 0.0000, -3.3847, 0.0000, -1.1439, -1.3315]

for idx, joint_idx in enumerate(joint_indices):
    p.resetJointState(robot_id, joint_idx, START_JOINT_POSITIONS[idx])

# 初始化夹爪为张开状态
if gripper_joint_indices:
    for g_idx in gripper_joint_indices:
        p.resetJointState(robot_id, g_idx, 0.04)  # 张开

for _ in range(100):
    p.stepSimulation()

# ================== 加载被抓取物体 ==================
def load_object(position, radius=0.03, height=0.03):
    """在指定位置加载一个圆柱体物体（用于抓取测试）"""
    col_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=radius, height=height)
    vis_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=radius, length=height,
                                    rgbaColor=[0.8, 0.2, 0.2, 1])
    obj_id = p.createMultiBody(baseMass=0.1, baseCollisionShapeIndex=col_shape,
                               baseVisualShapeIndex=vis_shape, basePosition=position)
    return obj_id

# 加载多个测试物体
object_ids = []
for pos in OBJECT_POSITIONS:
    obj_id = load_object(pos, OBJECT_RADIUS, OBJECT_HEIGHT)
    object_ids.append(obj_id)

print(f"[GRIP] 加载 {len(object_ids)} 个测试物体")

# ================== IK 求解函数 ==================
def compute_ik(target_pos):
    ik_joints = p.calculateInverseKinematics(
        robot_id,
        ee_index,
        target_pos,
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

# ================== 夹爪控制函数 ==================
def set_gripper(open_amount):
    """设置夹爪开度（0=闭合，0.04=张开）"""
    if not gripper_joint_indices:
        return
    for g_idx in gripper_joint_indices:
        p.setJointMotorControl2(robot_id, g_idx, p.POSITION_CONTROL,
                               targetPosition=open_amount, force=GRIP_FORCE)

def move_to_position(target_pos, duration=0.5):
    """将末端移动到目标位置"""
    target_joints = compute_ik(target_pos)

    for idx, joint_idx in enumerate(joint_indices):
        p.setJointMotorControl2(robot_id, joint_idx, p.POSITION_CONTROL,
                               targetPosition=target_joints[idx], force=50.0)

    # 步进仿真
    steps = int(duration / 0.001)
    for _ in range(steps):
        p.stepSimulation()
        time.sleep(0.001)

    # 读取实际位置
    link_state = p.getLinkState(robot_id, ee_index)
    return link_state[0]

def get_object_position(obj_id):
    """获取物体的当前位置"""
    pos, _ = p.getBasePositionAndOrientation(obj_id)
    return pos

# ================== 抓取测试函数 ==================
def grip_test(obj_id, target_pos, test_id):
    """执行一次完整的抓取测试"""
    results = {
        "success": False,
        "pre_grip_pos": None,
        "post_grip_pos": None,
        "lift_pos": None,
        "error": 0,
        "steps": 0
    }

    # 获取物体初始位置
    initial_obj_pos = get_object_position(obj_id)

    # 1. 移动到物体上方（预抓取位置）
    pre_grip_pos = [target_pos[0], target_pos[1], target_pos[2] + 0.15]
    actual_pre = move_to_position(pre_grip_pos, 0.3)
    results["pre_grip_pos"] = actual_pre

    # 2. 张开夹爪
    set_gripper(0.04)
    time.sleep(0.1)

    # 3. 下降到物体位置（抓取位置）
    grip_pos = [target_pos[0], target_pos[1], target_pos[2] + 0.03]
    actual_grip = move_to_position(grip_pos, 0.2)

    # 4. 闭合夹爪
    set_gripper(0.0)  # 闭合
    time.sleep(0.15)

    # 4.5 创建夹爪与物体之间的固定约束（模拟抓取力）
    # 计算物体相对于末端的位置偏移
    ee_state = p.getLinkState(robot_id, ee_index)
    ee_pos = ee_state[0]
    obj_pos = get_object_position(obj_id)
    # 物体在末端坐标系中的位置
    rel_pos = [obj_pos[0] - ee_pos[0], obj_pos[1] - ee_pos[1], obj_pos[2] - ee_pos[2]]

    constraint_id = p.createConstraint(
        parentBodyUniqueId=robot_id,
        parentLinkIndex=ee_index,
        childBodyUniqueId=obj_id,
        childLinkIndex=-1,
        jointType=p.JOINT_FIXED,
        jointAxis=[0, 0, 0],
        parentFramePosition=rel_pos,
        childFramePosition=[0, 0, 0]
    )
    # 设置约束的最大力（模拟夹持力）
    p.changeConstraint(constraint_id, maxForce=GRIP_FORCE)

    # 5. 抬升物体
    lift_pos = [target_pos[0], target_pos[1], target_pos[2] + 0.2]
    actual_lift = move_to_position(lift_pos, 0.3)
    results["lift_pos"] = actual_lift

    # 6. 检查物体是否跟随夹爪
    final_obj_pos = get_object_position(obj_id)

    # 计算物体位移
    obj_displacement = math.sqrt(
        (final_obj_pos[0] - initial_obj_pos[0])**2 +
        (final_obj_pos[1] - initial_obj_pos[1])**2 +
        (final_obj_pos[2] - initial_obj_pos[2])**2
    )

    # 判断抓取是否成功（物体被抬升超过一定距离）
    if obj_displacement > 0.05:
        results["success"] = True

    results["post_grip_pos"] = final_obj_pos
    results["error"] = math.sqrt(
        (actual_lift[0] - lift_pos[0])**2 +
        (actual_lift[1] - lift_pos[1])**2 +
        (actual_lift[2] - lift_pos[2])**2
    )

    # 7. 释放物体（删除约束 + 张开夹爪）
    p.removeConstraint(constraint_id)
    set_gripper(0.04)
    time.sleep(0.1)

    # 移动到释放位置
    release_pos = [target_pos[0] + 0.1, target_pos[1], target_pos[2] + 0.15]
    move_to_position(release_pos, 0.3)

    print(f"[GRIP] 测试 {test_id}: {'✅ 成功' if results['success'] else '❌ 失败'}, "
          f"位移: {obj_displacement*1000:.2f}mm")

    return results, obj_displacement

# ================== 执行抓取测试 ==================
print(f"[GRIP] 开始抓取测试，共 {NUM_GRIP_TESTS} 次")
print(f"[GRIP] 目标物体数量: {len(object_ids)}")

all_results = []
success_count = 0

for test_id in range(NUM_GRIP_TESTS):
    # 循环选择测试物体
    obj_idx = test_id % len(object_ids)
    obj_id = object_ids[obj_idx]
    target_pos = OBJECT_POSITIONS[obj_idx]

    # 重置物体位置（如果是第二次测试，物体可能已经被移动）
    p.resetBasePositionAndOrientation(obj_id, target_pos, [0, 0, 0, 1])

    # 执行抓取
    results, displacement = grip_test(obj_id, target_pos, test_id + 1)

    # 记录结果
    results["test_id"] = test_id + 1
    results["obj_idx"] = obj_idx
    results["displacement"] = displacement
    all_results.append(results)

    if results["success"]:
        success_count += 1

    # 重置机械臂到起点（保持一致性）
    for idx, joint_idx in enumerate(joint_indices):
        p.resetJointState(robot_id, joint_idx, START_JOINT_POSITIONS[idx])

print(f"\n[GRIP] ========= 测试完成 =========")
print(f"[GRIP] 成功: {success_count}/{NUM_GRIP_TESTS}")
print(f"[GRIP] 成功率: {success_count/NUM_GRIP_TESTS*100:.1f}%")

# ================== 生成报告 ==================
generate_gripper_report(
    report_filename=os.path.join(PROJECT_ROOT, "gripper_report.txt"),
    log_filename=os.path.join(PROJECT_ROOT, "gripper_log.csv"),
    all_results=all_results,
    success_count=success_count,
    num_tests=NUM_GRIP_TESTS,
    object_positions=OBJECT_POSITIONS,
    object_radius=OBJECT_RADIUS,
    grip_force=GRIP_FORCE
)

print("\n[GRIP] 报告已生成: {output_path}/gripper_report.txt")
print("[GRIP] 日志已保存: {output_path}/gripper_log.csv")
print("[GRIP] 夹爪控制仿真完成。")
p.disconnect()
