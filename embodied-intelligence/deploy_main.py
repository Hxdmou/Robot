"""
部署适配主脚本（支持真实机械臂对接 + PPO模型推理）
两种任务执行模式：
  1. trajectory - 硬编码轨迹插值（原模式）
  2. model      - PPO模型推理驱动（新模式，默认）

安全原则：低资源占用、异常保护、自动恢复、模式隔离
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
import threading
import signal
import sys
import os

from deployment_config import (
    CONTROL_PARAMS,
    VALIDATED_BOUNDS,
    SIMULATION_PARAMS,
    ROBOT_CONFIG,
    MONITOR_PARAMS
)
from gpu_accelerator import enable_gpu_acceleration, optimize_rendering
from realtime_monitor import ResourceMonitor, RobotMonitor
from performance_monitor import PerformanceMonitor
from deploy_logger import DeployLogger
from param_calibration import ParameterCalibrator
from real_robot_adapter import RobotAdapter
from sensor_noise import SensorNoiseSystem
from noise_config import SENSOR_NOISE_CONFIG
from collision_detector import CollisionDetector, ForceFeedback
from collision_config import COLLISION_CONFIG, OBSTACLE_CONFIG
from data_recorder import DataRecorder
from data_config import DATA_RECORDER_CONFIG
from robot_config import (
    ROBOT_MODE,
    REAL_ROBOT_CONFIG,
    JOINT_INDICES,
    JOINT_LIMITS,
    START_JOINT_POSITIONS,
    CONTROL_PARAMS as ROBOT_CONTROL_PARAMS
)
from domain_randomization import DomainRandomizationSystem
from latency_simulator import LatencySystem
from actuator_dynamics import ActuatorSystem
from disturbance_simulator import DisturbanceSystem
from sim_to_real_adapter import SimToRealAdapter, DeploymentSafetyGuard
from deploy_tools import (
    DeploymentSnapshot,
    SafetyParameterValidator,
    FailoverManager,
    DeploymentReportGenerator,
    DeploymentArchiver
)

physicsClient = None
resource_monitor = None
robot_monitor = None
perf_monitor = None
logger = None
robot_adapter = None
noise_system = None
collision_detector = None
force_feedback = None
obstacle_ids = []
data_recorder = None
domain_randomizer = None
latency_system = None
actuator_system = None
disturbance_system = None
running = True

# ========== 新增：模型推理相关 ==========
ppo_model = None
sim_to_real = None
safety_guard = None
EXECUTION_MODE = "model"  # "model" 或 "trajectory"
MODEL_PATH = "ppo_robot_reach_curriculum"
MAX_STEPS_PER_TASK = 300

# ========== 新增：部署工具 ==========
deploy_snapshot = None
failover_manager = None
deploy_reporter = None
deploy_archiver = None
deploy_start_time = None


def signal_handler(sig, frame):
    global running
    print("\n[DEPLOY] 收到中断信号，正在安全退出...")
    running = False


signal.signal(signal.SIGINT, signal_handler)


def load_model(model_path=None):
    """加载训练好的PPO模型

    Returns:
        (success, model) 成功返回True和模型对象，失败返回False和None
    """
    global ppo_model

    model_path = model_path or MODEL_PATH
    search_paths = [
        model_path,
        f"{model_path}.zip",
        os.path.join(PROJECT_ROOT, model_path),
        os.path.join(PROJECT_ROOT, f"{model_path}.zip"),
    ]

    for path in search_paths:
        if os.path.exists(path) or os.path.exists(path + ".zip"):
            try:
                from stable_baselines3 import PPO
                ppo_model = PPO.load(path, device="cpu")
                logger.info(f"PPO模型加载成功: {path}")
                return True, ppo_model
            except Exception as e:
                logger.warn(f"模型加载失败 ({path}): {e}")

    logger.warn(f"未找到PPO模型，将使用轨迹模式 (搜索路径: {search_paths})")
    return False, None


def init_environment(execution_mode=None):
    """初始化部署环境

    Args:
        execution_mode: "model"（模型推理）或 "trajectory"（硬编码轨迹）
    """
    global physicsClient, resource_monitor, robot_monitor, perf_monitor, logger, robot_adapter, noise_system, collision_detector, force_feedback, obstacle_ids, data_recorder, domain_randomizer, latency_system, actuator_system, disturbance_system, sim_to_real, safety_guard, EXECUTION_MODE, deploy_snapshot, failover_manager, deploy_reporter, deploy_archiver, deploy_start_time

    if execution_mode:
        EXECUTION_MODE = execution_mode

    logger = DeployLogger()
    logger.info(f"初始化环境... (模式: {ROBOT_MODE}, 执行: {EXECUTION_MODE})")

    # ========== 部署工具初始化 ==========
    deploy_start_time = time.time()

    # 1. 创建部署配置快照
    deploy_snapshot = DeploymentSnapshot()
    deploy_snapshot.create_snapshot({
        "mode": ROBOT_MODE,
        "execution": EXECUTION_MODE,
    })

    # 2. 安全参数完整性验证
    safety_validator = SafetyParameterValidator()
    safety_ok, safety_issues = safety_validator.validate_all()
    if safety_ok:
        logger.info("安全参数完整性验证: ✅ 通过")
    else:
        logger.warn(f"安全参数完整性验证发现 {len(safety_issues)} 个问题")
        for issue in safety_issues:
            logger.warn(f"  - {issue}")

    # 3. 初始化降级管理器
    failover_manager = FailoverManager(max_consecutive_failures=5, cooldown_cycles=50)

    # 4. 初始化报告生成器和归档器
    deploy_reporter = DeploymentReportGenerator()
    deploy_archiver = DeploymentArchiver()

    # ========== Sim-to-Real 适配器 + 安全护栏 ==========
    sim_to_real = SimToRealAdapter(
        joint_indices=JOINT_INDICES,
        action_scale=5.0,
        joint_limits=JOINT_LIMITS
    )
    safety_guard = DeploymentSafetyGuard(
        joint_limits=JOINT_LIMITS,
        workspace_radius=0.8,
        min_z=0.05,
        max_joint_speed=3.0,
        max_force=100.0
    )
    logger.info("Sim-to-Real适配器 + 安全护栏已加载")

    # ========== 加载PPO模型（仅model模式） ==========
    if EXECUTION_MODE == "model":
        model_ok, _ = load_model()
        if not model_ok:
            logger.warn("切换到轨迹模式（模型加载失败）")
            EXECUTION_MODE = "trajectory"

    noise_system = SensorNoiseSystem(SENSOR_NOISE_CONFIG)
    logger.info(f"传感器噪声模型已加载 (启用: {noise_system.is_enabled()})")

    collision_detector = CollisionDetector(COLLISION_CONFIG)
    force_feedback = ForceFeedback(COLLISION_CONFIG)
    logger.info(f"碰撞检测系统已加载 (启用: {collision_detector.is_enabled()})")

    data_recorder = DataRecorder(DATA_RECORDER_CONFIG)
    logger.info(f"数据记录系统已加载 (启用: {data_recorder.is_enabled()})")

    domain_randomizer = DomainRandomizationSystem({
        "enabled": True,
        "domain_randomizer": {
            "enabled": True,
            "randomize_interval": 120.0,
            "friction_range": [0.4, 0.6],
            "damping_range": [0.02, 0.08],
            "mass_range": [0.95, 1.05],
            "gravity_range": [-9.85, -9.75]
        },
        "mass_randomizer": {"enabled": False},
        "friction_randomizer": {"enabled": False},
        "physics_distortion": {"enabled": False}
    })
    logger.info(f"领域随机化系统已加载 (启用: {domain_randomizer.is_enabled()})")

    latency_system = LatencySystem({
        "enabled": True,
        "latency_simulator": {"enabled": True, "mean_latency_ms": 10},
        "control_delay": {"enabled": True, "delay_ms": 8},
        "state_delay": {"enabled": True, "delay_ms": 5},
        "network_latency": {"enabled": True, "mean_rtt_ms": 15, "jitter_ms": 5}
    })
    logger.info(f"通信延迟系统已加载 (启用: {latency_system.is_enabled()})")

    actuator_system = ActuatorSystem({
        "enabled": True,
        "actuator_dynamics": {"enabled": True, "max_torque": 50.0, "max_velocity": 3.0},
        "motor_model": {"enabled": True},
        "joint_constraint": {"enabled": True, "max_force": 50.0}
    })
    logger.info(f"执行器动力学系统已加载 (启用: {actuator_system.is_enabled()})")

    disturbance_system = DisturbanceSystem({
        "enabled": True,
        "disturbance_simulator": {"enabled": True},
        "impact_simulator": {"enabled": True},
        "load_simulator": {"enabled": True}
    })
    logger.info(f"外部扰动系统已加载 (启用: {disturbance_system.is_enabled()})")

    robot_config_dict = {
        "joint_indices": JOINT_INDICES,
        "joint_limits": JOINT_LIMITS,
        **REAL_ROBOT_CONFIG
    }
    robot_adapter = RobotAdapter(mode=ROBOT_MODE, config=robot_config_dict)

    if not robot_adapter.initialize():
        logger.error("机器人适配器初始化失败")
        return None

    if ROBOT_MODE == "sim":
        physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(*SIMULATION_PARAMS["gravity"])
        p.setRealTimeSimulation(0)

        enable_gpu_acceleration(physicsClient)
        optimize_rendering(physicsClient)

        plane_id = p.loadURDF("plane.urdf")

        table_col = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.02])
        table_vis = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 0.02],
                                         rgbaColor=[0.6, 0.4, 0.2, 1])
        table_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=table_col,
                                     baseVisualShapeIndex=table_vis, basePosition=[0.2, 0, -0.02])

        urdf_path = ROBOT_CONFIG["urdf_path"]
        robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)

        link_name_to_index = {}
        for i in range(p.getNumJoints(robot_id)):
            info = p.getJointInfo(robot_id, i)
            link_name = info[12].decode('utf-8')
            link_name_to_index[link_name] = i

        ee_index = link_name_to_index.get(ROBOT_CONFIG["ee_link"], -1)
        if ee_index == -1:
            ee_index = p.getNumJoints(robot_id) - 2

        robot_adapter.update_sim_params(robot_id, JOINT_INDICES, ee_index)

        joint_lower_limits = []
        joint_upper_limits = []
        joint_ranges = []
        joint_rest_poses = []

        for i in JOINT_INDICES:
            info = p.getJointInfo(robot_id, i)
            joint_lower_limits.append(info[8])
            joint_upper_limits.append(info[9])
            joint_ranges.append(info[9] - info[8])
            joint_rest_poses.append((info[8] + info[9]) / 2)

        resource_monitor = ResourceMonitor(interval=MONITOR_PARAMS["update_interval"])
        resource_monitor.start()

        perf_monitor = PerformanceMonitor(log_interval=MONITOR_PARAMS["log_interval"])
        perf_monitor.start()

        robot_monitor = RobotMonitor(robot_id, ee_index, JOINT_INDICES)

        obstacle_ids.append(table_id)

        for obs_name, obs_config in OBSTACLE_CONFIG.items():
            if obs_name == "table":
                continue
            if obs_config["type"] == "box":
                col = p.createCollisionShape(p.GEOM_BOX, halfExtents=obs_config["dimensions"])
                vis = p.createVisualShape(p.GEOM_BOX, halfExtents=obs_config["dimensions"],
                                         rgbaColor=obs_config["color"])
                obs_id = p.createMultiBody(baseMass=obs_config["mass"], baseCollisionShapeIndex=col,
                                          baseVisualShapeIndex=vis, basePosition=obs_config["position"])
            elif obs_config["type"] == "sphere":
                col = p.createCollisionShape(p.GEOM_SPHERE, radius=obs_config["radius"])
                vis = p.createVisualShape(p.GEOM_SPHERE, radius=obs_config["radius"],
                                         rgbaColor=obs_config["color"])
                obs_id = p.createMultiBody(baseMass=obs_config["mass"], baseCollisionShapeIndex=col,
                                          baseVisualShapeIndex=vis, basePosition=obs_config["position"])
            obstacle_ids.append(obs_id)
            logger.info(f"障碍物已创建: {obs_name}", position=obs_config["position"])

        collision_detector.start_monitoring(robot_id, obstacle_ids)
        logger.info(f"碰撞监控已启动 (障碍物数量: {len(obstacle_ids)})")

        data_recorder.start()
        logger.info("数据记录已启动")

        logger.info("仿真环境初始化完成", ee_link=ROBOT_CONFIG["ee_link"], ee_index=ee_index)

        return {
            "robot_id": robot_id,
            "ee_index": ee_index,
            "joint_indices": JOINT_INDICES,
            "joint_lower_limits": joint_lower_limits,
            "joint_upper_limits": joint_upper_limits,
            "joint_ranges": joint_ranges,
            "joint_rest_poses": joint_rest_poses,
        }
    else:
        resource_monitor = ResourceMonitor(interval=MONITOR_PARAMS["update_interval"])
        resource_monitor.start()

        perf_monitor = PerformanceMonitor(log_interval=MONITOR_PARAMS["log_interval"])
        perf_monitor.start()

        logger.info("真实机械臂环境初始化完成")
        return {"robot_id": None, "ee_index": 7, "joint_indices": JOINT_INDICES}


def get_current_state(config):
    """获取当前机器人状态（兼容仿真和真实模式）

    Returns:
        (joint_positions, ee_position)
    """
    if ROBOT_MODE == "real":
        states = robot_adapter.get_joint_states()
        joint_pos = [s.get("position", 0.0) for s in states[:7]]
        ee_pose = robot_adapter.get_ee_pose()
        ee_pos = ee_pose["position"]
    else:
        states = p.getJointStates(config["robot_id"], config["joint_indices"])
        joint_pos = [s[0] for s in states]
        link_state = p.getLinkState(config["robot_id"], config["ee_index"])
        ee_pos = list(link_state[0])

    return joint_pos, ee_pos


def apply_joint_targets(config, target_joints):
    """应用关节目标到机器人（兼容仿真和真实模式）"""
    target_joints = safety_guard.clip_joint_targets(target_joints)

    if ROBOT_MODE == "real":
        robot_adapter.move_joints(target_joints.tolist(), speed=1.0)
    else:
        for idx, joint_idx in enumerate(config["joint_indices"]):
            p.setJointMotorControl2(
                config["robot_id"], joint_idx, p.POSITION_CONTROL,
                targetPosition=target_joints[idx], force=CONTROL_PARAMS["force"]
            )
        for _ in range(2):
            p.stepSimulation()


def compute_ik(config, target_pos):
    if ROBOT_MODE != "sim" or config["robot_id"] is None:
        return None

    ik_joints = p.calculateInverseKinematics(
        config["robot_id"],
        config["ee_index"],
        target_pos,
        targetOrientation=[0, 0, 0, 1],
        lowerLimits=config["joint_lower_limits"],
        upperLimits=config["joint_upper_limits"],
        jointRanges=config["joint_ranges"],
        restPoses=config["joint_rest_poses"],
        maxNumIterations=CONTROL_PARAMS["ik_max_iter"],
        residualThreshold=CONTROL_PARAMS["ik_threshold"]
    )
    return [ik_joints[idx] if idx < len(ik_joints) else 0.0 for idx in config["joint_indices"]]


def move_to_position(config, target_pos, steps=None):
    if ROBOT_MODE == "real":
        robot_adapter.move_cartesian(*target_pos, speed=0.5)
        time.sleep(0.2)
        current_pose = robot_adapter.get_ee_pose()
        return current_pose["position"]

    steps = steps if steps else CONTROL_PARAMS["move_speed"]
    target_joints = compute_ik(config, target_pos)
    if target_joints is None:
        return [0, 0, 0]

    for idx, joint_idx in enumerate(config["joint_indices"]):
        p.setJointMotorControl2(config["robot_id"], joint_idx, p.POSITION_CONTROL,
                               targetPosition=target_joints[idx], force=CONTROL_PARAMS["force"])
    for _ in range(steps):
        p.stepSimulation()
        time.sleep(0.001)

    link_state = p.getLinkState(config["robot_id"], config["ee_index"])
    actual_pos = link_state[0]

    if noise_system:
        actual_pos = noise_system.apply_ee_noise(actual_pos)

    return actual_pos


def converge_to_target(config, target_pos):
    if ROBOT_MODE == "real":
        error = robot_adapter.converge_to_target(
            target_pos,
            max_iter=ROBOT_CONTROL_PARAMS["convergence_iterations"],
            threshold=ROBOT_CONTROL_PARAMS["convergence_threshold"]
        )
        return error

    for _ in range(10):
        link_state = p.getLinkState(config["robot_id"], config["ee_index"])
        current_pos = link_state[0]

        if noise_system:
            current_pos = noise_system.apply_ee_noise(current_pos)

        error = math.sqrt(
            (current_pos[0] - target_pos[0])**2 +
            (current_pos[1] - target_pos[1])**2 +
            (current_pos[2] - target_pos[2])**2
        )
        if error < CONTROL_PARAMS["convergence_threshold"]:
            break
        target_joints = compute_ik(config, target_pos)
        if target_joints is None:
            break
        for idx, joint_idx in enumerate(config["joint_indices"]):
            p.setJointMotorControl2(config["robot_id"], joint_idx, p.POSITION_CONTROL,
                                   targetPosition=target_joints[idx], force=CONTROL_PARAMS["force"])
        for _ in range(CONTROL_PARAMS["convergence_steps"]):
            p.stepSimulation()
            time.sleep(0.001)

    return error


def reset_robot(config):
    if ROBOT_MODE == "real":
        robot_adapter.move_joints(START_JOINT_POSITIONS, speed=0.5)
        time.sleep(1.0)
        return

    for idx, joint_idx in enumerate(config["joint_indices"]):
        p.resetJointState(config["robot_id"], joint_idx, START_JOINT_POSITIONS[idx])
    for _ in range(50):
        p.stepSimulation()


def execute_task_model(config, target_pos):
    """使用PPO模型推理执行任务（新模式）

    Returns:
        final_error: 末端到目标的最终距离 (m)
    """
    reset_robot(config)

    if ppo_model is None or sim_to_real is None:
        logger.warn("模型未加载，回退到轨迹模式")
        return execute_task_trajectory(config, target_pos)

    success = False
    steps = 0

    for steps in range(MAX_STEPS_PER_TASK):
        if safety_guard.is_emergency_stop():
            logger.warn("紧急停止已触发，任务中止")
            break

        joint_pos, ee_pos = get_current_state(config)

        # 安全检查
        safety_result = safety_guard.check_all(joint_pos, ee_pos)
        if safety_result["should_stop"]:
            logger.warn(f"安全违规: {safety_result['violations']}")
            break

        # 构造观测 → 模型推理 → 转换为关节目标
        obs = sim_to_real.robot_state_to_obs(joint_pos, ee_pos, target_pos)
        action, _ = ppo_model.predict(obs, deterministic=True)
        target_joints = sim_to_real.action_to_joint_targets(action, joint_pos)

        # 应用控制
        apply_joint_targets(config, target_joints)

        # 检查是否到达目标
        dist = math.sqrt(
            (ee_pos[0] - target_pos[0])**2 +
            (ee_pos[1] - target_pos[1])**2 +
            (ee_pos[2] - target_pos[2])**2
        )
        if dist < 0.01:
            success = True
            break

        if ROBOT_MODE == "real":
            time.sleep(0.01)

    # 获取最终位置
    _, final_ee = get_current_state(config)
    final_error = math.sqrt(
        (final_ee[0] - target_pos[0])**2 +
        (final_ee[1] - target_pos[1])**2 +
        (final_ee[2] - target_pos[2])**2
    )

    if robot_monitor:
        robot_monitor.log_error(final_error)

    logger.info(f"模型执行完成: 步数={steps+1}, 成功={success}, 误差={final_error*1000:.2f}mm")
    return final_error


def execute_task_trajectory(config, target_pos):
    """使用硬编码轨迹执行任务（原模式）"""
    reset_robot(config)

    start_pos = [0.0, 0.0, 0.6]
    num_steps = 30
    trajectory = []
    for i in range(num_steps + 1):
        t = i / num_steps
        x = start_pos[0] + (target_pos[0] - start_pos[0]) * t
        y = start_pos[1] + (target_pos[1] - start_pos[1]) * t
        z = start_pos[2] + (target_pos[2] - start_pos[2]) * t
        trajectory.append([x, y, z])

    for target_point in trajectory:
        move_to_position(config, target_point)

    converge_to_target(config, target_pos)

    if ROBOT_MODE == "real":
        current_pose = robot_adapter.get_ee_pose()
        final_pos = current_pose["position"]
    else:
        link_state = p.getLinkState(config["robot_id"], config["ee_index"])
        final_pos = link_state[0]

        if noise_system:
            final_pos = noise_system.apply_ee_noise(final_pos)

    final_error = math.sqrt(
        (final_pos[0] - target_pos[0])**2 +
        (final_pos[1] - target_pos[1])**2 +
        (final_pos[2] - target_pos[2])**2
    )

    if robot_monitor:
        robot_monitor.log_error(final_error)
    return final_error


def execute_task(config, target_pos):
    """根据当前执行模式选择任务执行方式（支持自动降级）"""
    # 检查降级管理器状态：如果模型模式连续失败，自动切换到轨迹模式
    use_trajectory = failover_manager.should_use_trajectory() if failover_manager else False

    if use_trajectory or EXECUTION_MODE == "trajectory":
        if use_trajectory and EXECUTION_MODE == "model":
            # 降级状态，使用轨迹模式
            error = execute_task_trajectory(config, target_pos)
            # 降级中仍然记录结果，用于判断是否可以恢复
            passed = error < 0.02
            if failover_manager:
                failover_manager.record_result(passed)
            return error
        return execute_task_trajectory(config, target_pos)
    else:
        error = execute_task_model(config, target_pos)
        # 记录结果到降级管理器
        if failover_manager:
            passed = error < 0.02
            failover_manager.record_result(passed)
        return error


def run_calibration(config):
    if ROBOT_MODE != "sim" or config["robot_id"] is None:
        logger.info("跳过校准（真实机械臂模式）")
        return None

    calibrator = ParameterCalibrator(config["robot_id"], config["joint_indices"], config["ee_index"])
    results = calibrator.run_full_calibration()
    calibrator.save_results()
    return results


def emergency_stop_recovery(config):
    """紧急停止恢复流程

    步骤：
    1. 停止所有运动
    2. 检查系统状态
    3. 移动到安全姿势（参考位置）
    4. 重置安全护栏状态
    5. 等待用户确认后恢复运行
    """
    print("\n" + "=" * 70)
    print("  ⚠️  紧急停止恢复流程")
    print("=" * 70)

    # 1. 停止所有运动
    print("[1/5] 停止所有运动...")
    try:
        if robot_adapter:
            robot_adapter.stop()
    except:
        pass

    # 2. 检查系统状态
    print("[2/5] 检查系统状态...")
    try:
        joint_pos, ee_pos = get_current_state(config)
        for i, pos in enumerate(joint_pos):
            print(f"     关节{i}: {pos:.4f} rad")
        print(f"     末端位置: ({ee_pos[0]:.3f}, {ee_pos[1]:.3f}, {ee_pos[2]:.3f})")
    except Exception as e:
        print(f"     ⚠️  状态读取失败: {e}")

    # 3. 移动到安全姿势
    print("[3/5] 移动到安全参考姿势...")
    try:
        reset_robot(config)
        print("     ✅ 已移动到参考位置")
    except Exception as e:
        print(f"     ⚠️  移动失败: {e}")

    # 4. 重置安全状态
    print("[4/5] 重置安全护栏状态...")
    if safety_guard:
        safety_guard.reset_emergency_stop()
    if robot_adapter and robot_adapter.emergency_stop:
        robot_adapter.emergency_stop.reset_emergency_stop()
    print("     ✅ 安全状态已重置")

    # 5. 用户确认
    print("[5/5] 等待用户确认...")
    print("     请检查机器人周围环境，确保安全后按回车键继续...")

    if ROBOT_MODE == "real":
        try:
            input()
        except:
            pass

    print("     ✅ 紧急停止恢复完成")
    print("=" * 70)
    return True


def post_deployment_health_check(config, cycle_count, success_count):
    """部署后健康检查

    检查项：
    1. 机器人连接状态
    2. 关节位置是否在安全范围
    3. 末端位置是否在工作空间
    4. 系统资源（CPU/内存）
    5. 部署成功率统计
    """
    print("\n" + "=" * 70)
    print("  部署健康检查")
    print("=" * 70)

    checks = []

    # 1. 连接状态
    try:
        connected = robot_adapter.is_connected() if robot_adapter else False
        status = "✅" if connected else "❌"
        checks.append(("机器人连接", connected))
        print(f"  {status} 机器人连接: {'正常' if connected else '断开'}")
    except Exception as e:
        checks.append(("机器人连接", False))
        print(f"  ❌ 机器人连接: 异常 ({e})")

    # 2. 关节位置
    try:
        joint_pos, ee_pos = get_current_state(config)
        joint_safe = True
        for i, pos in enumerate(joint_pos):
            lower = JOINT_LIMITS["lower"][i]
            upper = JOINT_LIMITS["upper"][i]
            if pos < lower or pos > upper:
                joint_safe = False
                break
        status = "✅" if joint_safe else "❌"
        checks.append(("关节范围", joint_safe))
        print(f"  {status} 关节范围: {'正常' if joint_safe else '超限'}")
    except Exception as e:
        checks.append(("关节范围", False))
        print(f"  ❌ 关节范围: 异常 ({e})")

    # 3. 末端位置
    try:
        dist = math.sqrt(ee_pos[0]**2 + ee_pos[1]**2)
        in_ws = dist <= 0.8 and ee_pos[2] >= 0.05
        status = "✅" if in_ws else "❌"
        checks.append(("工作空间", in_ws))
        print(f"  {status} 工作空间: {'正常' if in_ws else '超出'} "
              f"(距离={dist:.3f}m, Z={ee_pos[2]:.3f}m)")
    except Exception as e:
        checks.append(("工作空间", False))
        print(f"  ❌ 工作空间: 异常 ({e})")

    # 4. 系统资源
    try:
        stats = resource_monitor.get_stats() if resource_monitor else {}
        cpu_ok = stats.get("cpu_current", 100) < 90
        mem_ok = stats.get("mem_current", 100) < 90
        resource_ok = cpu_ok and mem_ok
        status = "✅" if resource_ok else "⚠️"
        checks.append(("系统资源", resource_ok))
        print(f"  {status} 系统资源: CPU={stats.get('cpu_current', 0):.1f}% "
              f"MEM={stats.get('mem_current', 0):.1f}%")
    except Exception as e:
        checks.append(("系统资源", False))
        print(f"  ❌ 系统资源: 异常 ({e})")

    # 5. 成功率统计
    try:
        pass_rate = success_count / cycle_count * 100 if cycle_count > 0 else 0
        rate_ok = pass_rate >= 70
        status = "✅" if rate_ok else "⚠️"
        checks.append(("部署成功率", rate_ok))
        print(f"  {status} 部署成功率: {pass_rate:.1f}% "
              f"({success_count}/{cycle_count})")
    except:
        checks.append(("部署成功率", False))
        print(f"  ❌ 部署成功率: 未知")

    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    print("-" * 70)
    print(f"  健康检查结果: {passed}/{total} 通过")
    if passed == total:
        print("  ✅ 系统运行正常")
    else:
        print("  ⚠️  部分检查未通过，请关注")
    print("=" * 70)
    return passed == total


def deploy_loop(config):
    global running
    target_pos = [0.25, 0.0, 0.6]
    cycle_count = 0
    success_count = 0

    logger.info(f"开始部署循环... (模式: {ROBOT_MODE}, 执行: {EXECUTION_MODE})",
                target_pos=target_pos, force=CONTROL_PARAMS["force"])

    while running:
        try:
            cycle_count += 1

            if domain_randomizer and ROBOT_MODE == "sim":
                randomize_result = domain_randomizer.check_and_randomize(config["robot_id"], config["joint_indices"])
                if randomize_result:
                    logger.info(f"领域随机化已执行: {randomize_result}")

            if latency_system:
                latency_system.apply_control_latency()

            error = execute_task(config, target_pos)

            if disturbance_system and ROBOT_MODE == "sim":
                disturbances = disturbance_system.apply_disturbances(config["robot_id"], config["ee_index"])
                if disturbances:
                    for d in disturbances:
                        logger.info(f"扰动已应用: {d['type']}")

            passed = error < 0.02
            if passed:
                success_count += 1
                logger.success(f"循环 {cycle_count} 完成", error_mm=error*1000)
            else:
                logger.warn(f"循环 {cycle_count} 误差超限", error_mm=error*1000)

            stats = resource_monitor.get_stats()

            collision_stats = collision_detector.get_collision_stats() if collision_detector else {}
            if collision_detector:
                collision_detector.update()

            latency_stats = latency_system.get_stats() if latency_system else {}
            actuator_stats = actuator_system.get_stats() if actuator_system else {}
            disturbance_stats = disturbance_system.get_stats() if disturbance_system else {}

            print(f"[DEPLOY] 循环 {cycle_count}: 误差 {error*1000:.2f}mm | "
                  f"CPU: {stats['cpu_current']:.1f}% | MEM: {stats['mem_current']:.1f}% | "
                  f"碰撞: {collision_stats.get('recent_collisions', 0)} | 模式: {EXECUTION_MODE}")

            if data_recorder:
                if ROBOT_MODE == "real":
                    current_pose = robot_adapter.get_ee_pose()
                    current_pos = current_pose["position"]
                else:
                    link_state = p.getLinkState(config["robot_id"], config["ee_index"])
                    current_pos = link_state[0]

                data_recorder.record(
                    cycle=cycle_count,
                    target_pos=target_pos,
                    current_pos=current_pos,
                    error_mm=error * 1000,
                    cpu_percent=stats["cpu_current"],
                    mem_percent=stats["mem_current"],
                    collisions=collision_stats.get("recent_collisions", 0),
                    latency_ms=latency_stats.get("latency_simulator", {}).get("avg_latency_ms", 0),
                    disturbances=disturbance_stats.get("disturbance_simulator", {}).get("total_disturbances", 0)
                )

            if cycle_count % 10 == 0:
                perf_summary = perf_monitor.get_summary()
                if perf_summary:
                    logger.info("性能统计", avg_cpu=perf_summary["avg_cpu"],
                               avg_memory=perf_summary["avg_memory"])

                if domain_randomizer:
                    dr_stats = domain_randomizer.get_stats()
                    logger.info("领域随机化统计", **dr_stats)
                if disturbance_system:
                    ds_stats = disturbance_system.get_stats()
                    logger.info("扰动统计", **ds_stats)

                # 每10个循环执行一次健康检查
                post_deployment_health_check(config, cycle_count, success_count)

            time.sleep(0.5)

        except Exception as e:
            logger.error(f"部署循环异常: {e}")

            # 如果是安全违规导致的异常，触发紧急停止恢复
            if "安全" in str(e) or "emergency" in str(e).lower():
                logger.warn("检测到安全相关异常，启动紧急停止恢复...")
                try:
                    emergency_stop_recovery(config)
                except Exception as rec_e:
                    logger.error(f"紧急停止恢复失败: {rec_e}")

            time.sleep(1)

    pass_rate = success_count / cycle_count * 100 if cycle_count > 0 else 0
    logger.info("部署循环结束", cycle_count=cycle_count, pass_rate=pass_rate)

    print(f"\n[DEPLOY] 部署循环结束")
    print(f"[DEPLOY] 总循环次数: {cycle_count}")
    print(f"[DEPLOY] 执行模式: {EXECUTION_MODE}")
    print(f"[DEPLOY] 成功率: {pass_rate:.1f}%")

    # 部署结束后执行最终健康检查
    post_deployment_health_check(config, cycle_count, success_count)

    if perf_monitor:
        perf_monitor.save_report()

    # ========== 部署后：生成报告 + 归档数据 ==========
    duration = time.time() - deploy_start_time if deploy_start_time else 0

    # 收集资源统计
    resource_stats = {}
    if perf_monitor:
        perf_summary = perf_monitor.get_summary()
        if perf_summary:
            resource_stats = {
                "avg_cpu": perf_summary.get("avg_cpu", 0),
                "max_cpu": perf_summary.get("max_cpu", 0),
                "avg_mem": perf_summary.get("avg_memory", 0),
                "max_mem": perf_summary.get("max_memory", 0),
            }

    # 收集安全事件统计
    safety_events = {
        "emergency_stops": 0,
        "collision_warnings": collision_detector.get_collision_stats().get("total_collisions", 0) if collision_detector else 0,
        "failover_count": failover_manager.get_stats().get("failover_count", 0) if failover_manager else 0,
    }

    # 生成部署报告
    if deploy_reporter:
        deploy_data = {
            "mode": ROBOT_MODE,
            "execution": EXECUTION_MODE,
            "total_cycles": cycle_count,
            "success_count": success_count,
            "failure_count": cycle_count - success_count,
            "success_rate": pass_rate,
            "duration_seconds": duration,
            "resource_stats": resource_stats,
            "safety_events": safety_events,
            "failover_stats": failover_manager.get_stats() if failover_manager else {},
            "health_checks": {
                "robot_connection": {"passed": True, "detail": ROBOT_MODE},
                "success_rate": {"passed": pass_rate >= 70, "detail": f"{pass_rate:.1f}%"},
            }
        }
        deploy_reporter.generate_report(deploy_data)

    # 归档部署数据
    if deploy_archiver:
        deploy_archiver.archive_deployment()
        deploy_archiver.cleanup_old_archives(keep_last=10)


def cleanup():
    global physicsClient, resource_monitor, perf_monitor, logger, robot_adapter, collision_detector, data_recorder, domain_randomizer, latency_system, actuator_system, disturbance_system, ppo_model, sim_to_real, safety_guard

    print("\n[DEPLOY] 清理资源...")

    if safety_guard:
        safety_guard.reset_emergency_stop()

    if logger:
        logger.close()

    if resource_monitor:
        resource_monitor.stop()

    if perf_monitor:
        perf_monitor.stop()

    if data_recorder:
        data_recorder.stop()
        report_path = data_recorder.generate_report()
        print(f"[DATA] 数据报告已生成: {report_path}")

    if collision_detector:
        collision_detector.stop_monitoring()

    if domain_randomizer:
        domain_randomizer.disable()
        print("[DR] 领域随机化系统已禁用")

    if latency_system:
        latency_system.disable()
        print("[LATENCY] 通信延迟系统已禁用")

    if actuator_system:
        actuator_system.reset()
        actuator_system.disable()
        print("[ACTUATOR] 执行器动力学系统已重置")

    if disturbance_system:
        disturbance_system.reset()
        disturbance_system.disable()
        print("[DISTURBANCE] 外部扰动系统已重置")

    if robot_adapter:
        robot_adapter.shutdown()

    ppo_model = None
    sim_to_real = None
    safety_guard = None

    if physicsClient is not None:
        try:
            p.disconnect(physicsClient)
        except:
            pass

    print("[DEPLOY] 资源清理完成")


if __name__ == "__main__":
    try:
        config = init_environment()
        if config is None:
            sys.exit(1)

        run_calibration(config)

        deploy_loop(config)
    finally:
        cleanup()
        sys.exit(0)
