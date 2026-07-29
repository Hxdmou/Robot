"""
PyBullet 笛卡尔空间 RRT 避障路径规划（优化版）
功能：使用 RRT 算法规划无碰撞路径并跟踪执行
新增优化：
  1. 碰撞安全距离（1.5倍障碍物半径）
  2. 路径点插值（相邻点间插2个点，提升轨迹平滑度）
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

from config_rrt import (
    START_EE_POS, TARGET_END_POS, OBSTACLE_POS, OBSTACLE_RADIUS,
    RRT_MAX_ITERATIONS, RRT_STEP_SIZE, GOAL_BIAS, MOVE_SPEED, USE_KUKA,
    SAFETY_MARGIN, INTERPOLATION_POINTS
)
from logger_rrt import generate_rrt_report

# ================== 初始化仿真环境 ==================
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
p.setRealTimeSimulation(0)

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

print(f"[RRT] 加载机械臂: {urdf_path}")

num_joints_total = p.getNumJoints(robot_id)
ee_index = num_joints_total - 1

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

# ================== 加载障碍物（使用安全距离） ==================
sphere_radius = OBSTACLE_RADIUS
sphere_pos = OBSTACLE_POS
obstacle_id = p.createCollisionShape(p.GEOM_SPHERE, radius=sphere_radius)
obstacle_body = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=obstacle_id, basePosition=sphere_pos)

safe_radius = sphere_radius * SAFETY_MARGIN
print(f"[RRT] 障碍物已加载: 位置 {sphere_pos}, 物理半径 {sphere_radius}, 安全半径 {safe_radius}")

detect_radius = sphere_radius

# ================== 设置起点 ==================
START_JOINT_POSITIONS = [-1.0247, -1.3870, 0.0000, -3.3847, 0.0000, -1.1439, -1.3315]

for idx, joint_idx in enumerate(joint_indices):
    p.resetJointState(robot_id, joint_idx, START_JOINT_POSITIONS[idx])

for _ in range(100):
    p.stepSimulation()

print(f"[RRT] 起点: {START_EE_POS}, 终点: {TARGET_END_POS}")

# ================== 碰撞检测函数（使用安全距离） ==================
def check_point_collision(pos):
    safe_radius = 0.12
    dx = pos[0] - sphere_pos[0]
    dy = pos[1] - sphere_pos[1]
    dz = pos[2] - sphere_pos[2]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
    return dist < safe_radius

def check_path_collision(pos1, pos2, num_checks=10):
    for i in range(num_checks + 1):
        t = i / num_checks
        x = pos1[0] + (pos2[0] - pos1[0]) * t
        y = pos1[1] + (pos2[1] - pos1[1]) * t
        z = pos1[2] + (pos2[2] - pos1[2]) * t
        if check_point_collision([x, y, z]):
            return True
    return False

# ================== RRT 核心函数 ==================
class RRTNode:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent

def distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def steer(from_pos, to_pos, step_size):
    dist = distance(from_pos, to_pos)
    if dist < step_size:
        return to_pos.copy()
    ratio = step_size / dist
    x = from_pos[0] + (to_pos[0] - from_pos[0]) * ratio
    y = from_pos[1] + (to_pos[1] - from_pos[1]) * ratio
    z = from_pos[2] + (to_pos[2] - from_pos[2]) * ratio
    return [x, y, z]

def sample_free_space():
    for _ in range(100):
        x = random.uniform(min(START_EE_POS[0], TARGET_END_POS[0]) - 0.15,
                           max(START_EE_POS[0], TARGET_END_POS[0]) + 0.15)
        y = random.uniform(-0.25, 0.25)
        z = random.uniform(0.45, 0.75)
        candidate = [x, y, z]
        if not check_point_collision(candidate):
            return candidate
    return None

# ================== RRT 路径搜索 ==================
print("[RRT] 开始 RRT 路径搜索...")

nodes = [RRTNode(START_EE_POS.copy())]
goal_reached = False
goal_node = None

for iteration in range(RRT_MAX_ITERATIONS):
    if random.random() < GOAL_BIAS:
        sample_pos = TARGET_END_POS.copy()
    else:
        sample_pos = sample_free_space()
        if sample_pos is None:
            continue

    nearest = min(nodes, key=lambda node: distance(node.pos, sample_pos))
    new_pos = steer(nearest.pos, sample_pos, RRT_STEP_SIZE)

    if not check_path_collision(nearest.pos, new_pos, num_checks=10):
        if not check_point_collision(new_pos):
            new_node = RRTNode(new_pos, nearest)
            nodes.append(new_node)

            if distance(new_pos, TARGET_END_POS) < RRT_STEP_SIZE * 1.5:
                goal_reached = True
                goal_node = new_node
                print(f"[RRT] 找到路径！迭代次数: {iteration + 1}, 节点数: {len(nodes)}")
                break

    if (iteration + 1) % 50 == 0:
        print(f"[RRT] 迭代 {iteration + 1}/{RRT_MAX_ITERATIONS}, 节点数: {len(nodes)}")

# ================== 提取路径 ==================
if not goal_reached:
    print("[RRT] 未找到有效路径，使用备选路径...")
    mid_pos = [(START_EE_POS[0] + TARGET_END_POS[0]) / 2,
               (START_EE_POS[1] + TARGET_END_POS[1]) / 2 + 0.15,
               (START_EE_POS[2] + TARGET_END_POS[2]) / 2 + 0.05]
    raw_path = [START_EE_POS.copy(), mid_pos, TARGET_END_POS.copy()]
else:
    raw_path = []
    current = goal_node
    while current is not None:
        raw_path.append(current.pos)
        current = current.parent
    raw_path.reverse()

print(f"[RRT] 原始路径点数量: {len(raw_path)}")

if goal_reached and distance(raw_path[-1], TARGET_END_POS) > 0.01:
    raw_path.append(TARGET_END_POS.copy())
    print(f"[RRT] 添加终点到路径，当前路径点数量: {len(raw_path)}")

# ================== 路径点插值（增加平滑性） ==================
def interpolate_path(path, num_interp):
    if len(path) < 2:
        return path
    new_path = []
    for i in range(len(path) - 1):
        new_path.append(path[i])
        current_interp = num_interp
        if i == len(path) - 2:
            current_interp = 5
        for j in range(1, current_interp + 1):
            t = j / (current_interp + 1)
            x = path[i][0] + (path[i+1][0] - path[i][0]) * t
            y = path[i][1] + (path[i+1][1] - path[i][1]) * t
            z = path[i][2] + (path[i+1][2] - path[i][2]) * t
            new_path.append([x, y, z])
    new_path.append(path[-1])
    return new_path

path_points = interpolate_path(raw_path, INTERPOLATION_POINTS)
print(f"[RRT] 插值后路径点数量: {len(path_points)}")

# ================== 终点验证（不修改路径） ==================
end_ik_joints = p.calculateInverseKinematics(
    robot_id,
    ee_index,
    TARGET_END_POS,
    targetOrientation=[0, 0, 0, 1],
    lowerLimits=joint_lower_limits,
    upperLimits=joint_upper_limits,
    jointRanges=joint_ranges,
    restPoses=joint_rest_poses,
    maxNumIterations=3000,
    residualThreshold=1e-7
)

for idx, joint_idx in enumerate(joint_indices):
    p.resetJointState(robot_id, joint_idx, end_ik_joints[idx])
for _ in range(50):
    p.stepSimulation()

link_state = p.getLinkState(robot_id, ee_index)
actual_end_pos = link_state[0]
end_error = distance(actual_end_pos, TARGET_END_POS)

print(f"[RRT] 终点验证误差: {end_error*1000:.2f} mm")

# ================== 轨迹跟踪 ==================
actual_positions = []
joint_positions_history = []
step_count = 0
collision_detected = False

print("[RRT] 开始避障路径跟踪...")

for i, target_pos in enumerate(path_points):
    ik_joints = p.calculateInverseKinematics(
        robot_id,
        ee_index,
        target_pos,
        targetOrientation=[0, 0, 0, 1],
        lowerLimits=joint_lower_limits,
        upperLimits=joint_upper_limits,
        jointRanges=joint_ranges,
        restPoses=joint_rest_poses,
        maxNumIterations=3000,
        residualThreshold=1e-7
    )

    target_joints = []
    for idx in joint_indices:
        if idx < len(ik_joints):
            target_joints.append(ik_joints[idx])
        else:
            target_joints.append(0.0)

    for idx, joint_idx in enumerate(joint_indices):
        p.resetJointState(robot_id, joint_idx, target_joints[idx])

    for _ in range(MOVE_SPEED):
        p.stepSimulation()
        step_count += 1

        link_state = p.getLinkState(robot_id, ee_index)
        actual_pos = link_state[0]
        dx = actual_pos[0] - sphere_pos[0]
        dy = actual_pos[1] - sphere_pos[1]
        dz = actual_pos[2] - sphere_pos[2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < detect_radius:
            collision_detected = True
            print(f"[RRT] ⚠️ 碰撞检测触发于步 {step_count}")

    link_state = p.getLinkState(robot_id, ee_index)
    actual_pos = link_state[0]
    actual_positions.append(actual_pos)
    joint_positions_history.append(target_joints)

    if (i + 1) % 5 == 0:
        print(f"[RRT] 路径点 {i + 1}/{len(path_points)} 完成")

# ================== 生成报告 ==================
generate_rrt_report(
    report_filename=os.path.join(PROJECT_ROOT, "rrt_report.txt"),
    log_filename=os.path.join(PROJECT_ROOT, "rrt_log.csv"),
    path_points=path_points,
    actual_positions=actual_positions,
    joint_positions_history=joint_positions_history,
    start_pos=START_EE_POS,
    target_pos=TARGET_END_POS,
    obstacle_pos=OBSTACLE_POS,
    obstacle_radius=OBSTACLE_RADIUS,
    safety_margin=SAFETY_MARGIN,
    rrt_iterations=RRT_MAX_ITERATIONS,
    rrt_step_size=RRT_STEP_SIZE,
    goal_bias=GOAL_BIAS,
    collision_detected=collision_detected,
    move_speed=MOVE_SPEED,
    nodes_count=len(nodes),
    goal_reached=goal_reached,
    raw_path_len=len(raw_path),
    interp_points=INTERPOLATION_POINTS,
    final_path_len=len(path_points)
)

print("[RRT] 报告已生成: {output_path}/rrt_report.txt")
print("[RRT] 日志已保存: {output_path}/rrt_log.csv")
print(f"[RRT] 避障路径规划完成。目标到达: {'是' if goal_reached else '否'}, 碰撞检测: {'发生碰撞' if collision_detected else '未发生碰撞'}")
print("[RRT] 按 Ctrl+C 退出。")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("[RRT] 用户中断，程序退出。")
    p.disconnect()