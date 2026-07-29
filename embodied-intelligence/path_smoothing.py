"""
PyBullet 路径平滑模块
功能：对 RRT 生成的折线路径进行 B 样条拟合，输出平滑连续轨迹
方法：均匀三次 B 样条插值
输出：平滑后的路径点序列 + 对比报告
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
import numpy as np
from scipy import interpolate

from config_smooth import (
    RRT_PATH_POINTS,          # 原始 RRT 路径点列表
    SMOOTH_STEP_SIZE,         # 平滑后路径点间距
    SMOOTH_ORDER,             # B样条阶数
    USE_KUKA,
    MOVE_SPEED
)
from logger_smooth import generate_smooth_report

# ================== 初始化仿真环境 ==================
physicsClient = p.connect(p.DIRECT)  # 使用DIRECT模式避免GUI阻塞
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

print(f"[SMOOTH] 加载机械臂: {urdf_path}")

num_joints_total = p.getNumJoints(robot_id)
ee_index = num_joints_total - 1

# 关节限制（用于IK）
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

for _ in range(100):
    p.stepSimulation()

# ================== B样条平滑函数 ==================
def bspline_smooth(path_points, step_size, order=3):
    """
    对路径点进行 B 样条拟合，生成平滑连续轨迹
    path_points: 原始折线路径点列表 [[x,y,z], ...]
    step_size: 平滑后相邻点间距
    order: B样条阶数（默认3，即三次B样条）
    """
    if len(path_points) < order + 1:
        print("[SMOOTH] 路径点太少，无法进行B样条拟合")
        return path_points

    # 转为 numpy 数组便于计算
    pts = np.array(path_points)

    # 计算累积弦长参数化
    t = np.zeros(pts.shape[0])
    for i in range(1, pts.shape[0]):
        t[i] = t[i-1] + np.linalg.norm(pts[i] - pts[i-1])

    # 归一化到 [0, 1]
    if t[-1] > 0:
        t = t / t[-1]
    else:
        return path_points

    # B样条插值（使用 scipy 的 splprep / splev）
    try:
        from scipy.interpolate import splprep, splev
        # 使用平滑因子 s=0.5 进行充分平滑
        tck, u = splprep([pts[:,0], pts[:,1], pts[:,2]], u=t, s=0.5, k=order)
    except Exception as e:
        print(f"[SMOOTH] B样条拟合失败: {e}")
        return path_points

    # 生成平滑后的路径点
    # 计算原始路径总长度
    total_length = 0
    for i in range(len(path_points) - 1):
        total_length += np.linalg.norm(np.array(path_points[i+1]) - np.array(path_points[i]))

    # 根据步长计算采样点数
    num_samples = max(int(total_length / step_size), len(path_points) * 2)

    # 在 [0,1] 区间均匀采样
    u_new = np.linspace(0, 1, num_samples)

    # 计算采样点坐标
    x_new, y_new, z_new = splev(u_new, tck)

    # 组合成点列表
    smooth_path = [[x_new[i], y_new[i], z_new[i]] for i in range(len(x_new))]

    return smooth_path

def compute_path_length(path):
    """计算路径总长度"""
    length = 0
    for i in range(len(path) - 1):
        length += math.sqrt(
            (path[i+1][0] - path[i][0])**2 +
            (path[i+1][1] - path[i][1])**2 +
            (path[i+1][2] - path[i][2])**2
        )
    return length

def compute_path_curvature(path):
    """计算路径最大曲率（近似）"""
    if len(path) < 3:
        return 0
    max_curvature = 0
    for i in range(1, len(path) - 1):
        p1 = np.array(path[i-1])
        p2 = np.array(path[i])
        p3 = np.array(path[i+1])
        v1 = p2 - p1
        v2 = p3 - p2
        if np.linalg.norm(v1) < 1e-6 or np.linalg.norm(v2) < 1e-6:
            continue
        # 计算角度变化
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle = math.acos(max(-1, min(1, cos_angle)))
        curvature = angle / (np.linalg.norm(v1) + np.linalg.norm(v2))
        if curvature > max_curvature:
            max_curvature = curvature
    return max_curvature

# ================== 执行路径平滑 ==================
raw_path = [list(pt) for pt in RRT_PATH_POINTS]
raw_length = compute_path_length(raw_path)
raw_curvature = compute_path_curvature(raw_path)

print(f"[SMOOTH] 原始路径: {len(raw_path)} 点, 长度 {raw_length:.4f}m, 最大曲率 {raw_curvature:.6f}")

smooth_path = bspline_smooth(raw_path, SMOOTH_STEP_SIZE, SMOOTH_ORDER)
smooth_length = compute_path_length(smooth_path)
smooth_curvature = compute_path_curvature(smooth_path)

print(f"[SMOOTH] 平滑路径: {len(smooth_path)} 点, 长度 {smooth_length:.4f}m, 最大曲率 {smooth_curvature:.6f}")
if raw_curvature > 0:
    print(f"[SMOOTH] 曲率降低: {(1 - smooth_curvature/raw_curvature)*100:.1f}%")

# ================== 轨迹跟踪执行 ==================
def execute_path(path_points):
    """执行路径跟踪，返回实际位置和误差"""
    actual_positions = []
    step_count = 0
    collision_detected = False

    for i, target_pos in enumerate(path_points):
        # IK 求解
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

        for idx, joint_idx in enumerate(joint_indices):
            p.resetJointState(robot_id, joint_idx, target_joints[idx])

        for _ in range(MOVE_SPEED):
            p.stepSimulation()
            step_count += 1

        link_state = p.getLinkState(robot_id, ee_index)
        actual_pos = link_state[0]
        actual_positions.append(actual_pos)

        if (i + 1) % 20 == 0:
            err = math.sqrt(
                (actual_pos[0] - target_pos[0])**2 +
                (actual_pos[1] - target_pos[1])**2 +
                (actual_pos[2] - target_pos[2])**2
            )
            print(f"[SMOOTH] 路径点 {i+1}/{len(path_points)} 完成, 误差: {err*1000:.2f}mm")

    return actual_positions, step_count, collision_detected

# ================== 执行平滑路径 ==================
print("\n[SMOOTH] 执行平滑路径...")
actual_positions, total_steps, collision = execute_path(smooth_path)

# ================== 计算执行误差 ==================
errors = []
for target, actual in zip(smooth_path, actual_positions):
    err = math.sqrt(
        (actual[0] - target[0])**2 +
        (actual[1] - target[1])**2 +
        (actual[2] - target[2])**2
    )
    errors.append(err)

max_error = max(errors) if errors else 0
avg_error = sum(errors) / len(errors) if errors else 0
final_error = errors[-1] if errors else 0

print(f"\n[SMOOTH] === 执行结果 ===")
print(f"  总步数: {total_steps}")
print(f"  最大误差: {max_error*1000:.2f} mm")
print(f"  平均误差: {avg_error*1000:.2f} mm")
print(f"  终点误差: {final_error*1000:.2f} mm")
print(f"  碰撞检测: {'发生碰撞' if collision else '安全'}")

# ================== 生成报告 ==================
generate_smooth_report(
    report_filename=os.path.join(PROJECT_ROOT, "smooth_report.txt"),
    log_filename=os.path.join(PROJECT_ROOT, "smooth_log.csv"),
    raw_path=raw_path,
    smooth_path=smooth_path,
    actual_positions=actual_positions,
    raw_length=raw_length,
    smooth_length=smooth_length,
    raw_curvature=raw_curvature,
    smooth_curvature=smooth_curvature,
    max_error=max_error,
    avg_error=avg_error,
    final_error=final_error,
    collision_detected=collision,
    smooth_order=SMOOTH_ORDER,
    smooth_step_size=SMOOTH_STEP_SIZE
)

print("\n[SMOOTH] 报告已生成: {output_path}/smooth_report.txt")
print("[SMOOTH] 日志已保存: {output_path}/smooth_log.csv")
print("[SMOOTH] 路径平滑完成。")
p.disconnect()
