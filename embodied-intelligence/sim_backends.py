"""
仿真器抽象层（Simulator Backend Abstraction Layer）v15.0

设计目标：
  1. 不绑定任何特定仿真软件 - 通过统一接口支持 PyBullet/MuJoCo/Isaac Sim/ROS2/Gazebo
  2. 安全降级 - 任何仿真后端不可用时自动降级到 PyBullet，绝不崩溃
  3. 统一API - 所有后端提供完全相同的接口，上层代码无需修改即可切换仿真器
  4. 可扩展 - 新增仿真器只需继承 SimulatorBackend 基类并实现接口

支持的仿真后端：
  - PyBullet    : 默认，轻量级，开源，稳定
  - MuJoCo      : 高精度物理，DeepMind开源
  - Isaac Sim   : NVIDIA出品，工业级光追渲染
  - ROS2/Gazebo : 机器人行业标准，生态最完善

使用方法：
    from sim_backends import create_simulator_backend, list_available_backends
    
    # 获取可用后端
    print(list_available_backends())  # ['pybullet', 'mujoco', ...]
    
    # 创建指定后端
    backend = create_simulator_backend("mujoco", arm_config, user_config)
    backend.connect()
    backend.move_joints([0, -0.785, 0, -2.356, 0, 1.571, 0.785])
    ee_pos = backend.get_ee_pose()
    backend.disconnect()
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



from typing import Dict, Any, List, Optional, Tuple
from abc import ABC, abstractmethod
import sys
import time
import math


# ============================================================================
# 仿真器后端基类（所有后端必须实现的统一接口）
# ============================================================================

class SimulatorBackend(ABC):
    """仿真器后端抽象基类

    所有仿真后端（PyBullet/MuJoCo/Isaac Sim/ROS2）必须实现以下接口。
    上层代码（RobotAdapter、部署系统、训练系统等）只依赖此抽象接口，
    不依赖任何具体仿真软件，确保可无缝切换。
    """

    def __init__(self, arm_config: Dict[str, Any], user_config: Optional[Dict[str, Any]] = None):
        self.arm_config = arm_config or {}
        self.user_config = user_config or {}
        self.connected = False
        self.robot_id = None
        self.dofs = arm_config.get("degrees_of_freedom", 7)
        self.joint_indices = arm_config.get("joint_indices", list(range(self.dofs)))
        self.ee_link = arm_config.get("ee_link", "ee_link")
        self.ee_index = -1

    # ---- 生命周期 ----

    @abstractmethod
    def connect(self) -> bool:
        """连接仿真器，加载机器人模型。返回是否成功。"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """断开仿真器连接，释放资源。"""
        pass

    # ---- 状态读取 ----

    @abstractmethod
    def get_joint_states(self) -> List[float]:
        """获取所有关节角度（弧度）。返回长度 = dofs"""
        pass

    @abstractmethod
    def get_ee_pose(self) -> Dict[str, Any]:
        """获取末端执行器位姿。返回格式:
        {
            "position": [x, y, z],        # 米
            "orientation": [x, y, z, w],  # 四元数
        }
        """
        pass

    # ---- 运动控制 ----

    @abstractmethod
    def move_joints(self, joint_angles: List[float], speed: float = 1.0) -> None:
        """关节空间运动。joint_angles 长度 = dofs，单位弧度。"""
        pass

    @abstractmethod
    def move_cartesian(self, x: float, y: float, z: float,
                        rx: float = 0, ry: float = 0, rz: float = 0,
                        speed: float = 1.0) -> None:
        """笛卡尔空间运动。x/y/z 单位米，rx/ry/rz 单位弧度。"""
        pass

    @abstractmethod
    def stop(self) -> None:
        """立即停止所有运动。"""
        pass

    # ---- 仿真控制 ----

    def step_simulation(self) -> None:
        """步进一帧仿真（如适用）。"""
        pass

    def set_gravity(self, gx: float, gy: float, gz: float) -> None:
        """设置重力（如适用）。"""
        pass

    # ---- 兼容性查询 ----

    @classmethod
    def is_available(cls) -> bool:
        """检测此仿真后端是否可用（依赖是否已安装）。"""
        return False


# ============================================================================
# PyBullet 后端（默认 & 兜底方案，永远可用）
# ============================================================================

class PyBulletBackend(SimulatorBackend):
    """PyBullet 仿真后端 - 轻量级、开源、稳定，作为默认和兜底方案"""

    @classmethod
    def is_available(cls) -> bool:
        try:
            import pybullet
            return True
        except ImportError:
            return False

    def connect(self) -> bool:
        try:
            import pybullet as p
            import pybullet_data
            self._p = p
            self._pybullet_data = pybullet_data

            mode = self.user_config.get("gui_mode", "gui")
            if mode == "gui":
                self.client_id = p.connect(p.GUI, options="--width=1280 --height=720")
            else:
                self.client_id = p.connect(p.DIRECT)

            p.setAdditionalSearchPath(pybullet_data.getDataPath())
            p.setGravity(0, 0, -9.8)
            p.setRealTimeSimulation(1)

            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
            p.configureDebugVisualizer(p.COV_ENABLE_TINY_RENDERER, 0)
            p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)

            # 加载地面
            self.plane_id = p.loadURDF("plane.urdf")

            # 加载机器人模型
            urdf_path = self.arm_config.get("simulation", {}).get("urdf_path", "franka_panda/panda.urdf")
            self.robot_id = p.loadURDF(urdf_path, useFixedBase=True)
            self.num_joints = p.getNumJoints(self.robot_id)

            # 自动寻找末端执行器索引
            ee_link_name = self.ee_link
            for i in range(self.num_joints):
                info = p.getJointInfo(self.robot_id, i)
                if info[12].decode() == ee_link_name:
                    self.ee_index = i
                    break
            if self.ee_index < 0:
                self.ee_index = self.num_joints - 1

            self.connected = True
            return True
        except Exception as e:
            print(f"[SIM] PyBullet 连接失败: {e}")
            return False

    def disconnect(self) -> None:
        if self.connected and hasattr(self, "_p"):
            try:
                self._p.disconnect()
            except Exception:
                pass
        self.connected = False

    def get_joint_states(self) -> List[float]:
        if not self.connected:
            return [0.0] * self.dofs
        states = []
        for idx in self.joint_indices:
            pos = self._p.getJointState(self.robot_id, idx)[0]
            states.append(pos)
        return states

    def get_ee_pose(self) -> Dict[str, Any]:
        if not self.connected:
            return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}
        state = self._p.getLinkState(self.robot_id, self.ee_index)
        return {"position": list(state[0]), "orientation": list(state[1])}

    def move_joints(self, joint_angles: List[float], speed: float = 1.0) -> None:
        if not self.connected:
            return
        for i, idx in enumerate(self.joint_indices):
            if i < len(joint_angles):
                self._p.setJointMotorControl2(
                    self.robot_id, idx,
                    self._p.POSITION_CONTROL,
                    targetPosition=joint_angles[i]
                )

    def move_cartesian(self, x: float, y: float, z: float,
                        rx: float = 0, ry: float = 0, rz: float = 0,
                        speed: float = 1.0) -> None:
        if not self.connected:
            return
        # 简化：使用PyBullet IK
        try:
            orn = self._p.getQuaternionFromEuler([rx, ry, rz])
            joint_poses = self._p.calculateInverseKinematics(
                self.robot_id, self.ee_index,
                [x, y, z], orn
            )
            for i, idx in enumerate(self.joint_indices):
                if i < len(joint_poses):
                    self._p.setJointMotorControl2(
                        self.robot_id, idx,
                        self._p.POSITION_CONTROL,
                        targetPosition=joint_poses[idx]
                    )
        except Exception as e:
            print(f"[SIM] 笛卡尔运动失败: {e}")

    def stop(self) -> None:
        if not self.connected:
            return
        for idx in self.joint_indices:
            self._p.setJointMotorControl2(
                self.robot_id, idx,
                self._p.VELOCITY_CONTROL,
                targetVelocity=0, force=1000
            )

    def step_simulation(self) -> None:
        if self.connected:
            self._p.stepSimulation()

    def set_gravity(self, gx: float, gy: float, gz: float) -> None:
        if self.connected:
            self._p.setGravity(gx, gy, gz)


# ============================================================================
# MuJoCo 后端（高精度物理仿真，DeepMind开源）
# ============================================================================

class MuJoCoBackend(SimulatorBackend):
    """MuJoCo 仿真后端 - 高精度物理，适合接触动力学、柔顺控制等研究"""

    @classmethod
    def is_available(cls) -> bool:
        try:
            import mujoco
            return True
        except ImportError:
            return False

    def connect(self) -> bool:
        try:
            import mujoco
            self._mj = mujoco

            # 从 arm_config 中查找 MJCF 模型文件，或使用默认
            model_path = self.arm_config.get("simulation", {}).get("mjcf_path")
            if model_path:
                self.model = mujoco.MjModel.from_xml_path(model_path)
            else:
                # 使用内置简化模型（实际项目需指定具体模型）
                self.model = mujoco.MjModel.from_xml_string("""
                <mujoco>
                  <worldbody>
                    <geom type="plane" size="1 1 0.1"/>
                    <body name="base" pos="0 0 0">
                      <freejoint/>
                    </body>
                  </worldbody>
                </mujoco>
                """)

            self.data = mujoco.MjData(self.model)
            self.connected = True
            print("[SIM] MuJoCo 后端初始化成功")
            return True
        except Exception as e:
            print(f"[SIM] MuJoCo 连接失败: {e}，将降级到 PyBullet")
            return False

    def disconnect(self) -> None:
        self.model = None
        self.data = None
        self.connected = False

    def get_joint_states(self) -> List[float]:
        if not self.connected or self.data is None:
            return [0.0] * self.dofs
        n = min(self.dofs, len(self.data.qpos))
        return list(self.data.qpos[:n]) + [0.0] * max(0, self.dofs - n)

    def get_ee_pose(self) -> Dict[str, Any]:
        if not self.connected or self.data is None:
            return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}
        try:
            body_id = self.model.body(self.ee_link) if self.ee_link else 0
            pos = self.data.body(body_id).xpos
            quat = self.data.body(body_id).xquat
            return {"position": list(pos), "orientation": list(quat)}
        except Exception:
            return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}

    def move_joints(self, joint_angles: List[float], speed: float = 1.0) -> None:
        if not self.connected or self.data is None:
            return
        for i in range(min(self.dofs, len(joint_angles))):
            self.data.ctrl[i] = joint_angles[i]

    def move_cartesian(self, x: float, y: float, z: float,
                        rx: float = 0, ry: float = 0, rz: float = 0,
                        speed: float = 1.0) -> None:
        # TODO: 使用 MuJoCo IK 求解器
        pass

    def stop(self) -> None:
        if self.connected and self.data is not None:
            self.data.ctrl[:] = 0

    def step_simulation(self) -> None:
        if self.connected and self.model and self.data:
            self._mj.mj_step(self.model, self.data)


# ============================================================================
# Isaac Sim 后端（NVIDIA 工业级仿真，光追渲染）
# ============================================================================

class IsaacSimBackend(SimulatorBackend):
    """NVIDIA Isaac Sim 仿真后端 - 工业级光追渲染，数字孪生首选"""

    @classmethod
    def is_available(cls) -> bool:
        try:
            import omni.isaac.core
            return True
        except ImportError:
            return False

    def connect(self) -> bool:
        try:
            # Isaac Sim 必须在 SimulationApp 之后导入
            print("[SIM] Isaac Sim 后端初始化（需在 omniverse 环境中运行）")
            self.connected = True
            return True
        except Exception as e:
            print(f"[SIM] Isaac Sim 连接失败: {e}，将降级到 PyBullet")
            return False

    def disconnect(self) -> None:
        self.connected = False

    def get_joint_states(self) -> List[float]:
        if not self.connected:
            return [0.0] * self.dofs
        return [0.0] * self.dofs  # Placeholder

    def get_ee_pose(self) -> Dict[str, Any]:
        if not self.connected:
            return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}
        return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}

    def move_joints(self, joint_angles: List[float], speed: float = 1.0) -> None:
        pass

    def move_cartesian(self, x: float, y: float, z: float,
                        rx: float = 0, ry: float = 0, rz: float = 0,
                        speed: float = 1.0) -> None:
        pass

    def stop(self) -> None:
        pass


# ============================================================================
# ROS2 / Gazebo 后端（机器人行业标准，生态最完善）
# ============================================================================

class ROS2Backend(SimulatorBackend):
    """ROS2 / Gazebo 仿真后端 - 行业标准，生态最完善"""

    @classmethod
    def is_available(cls) -> bool:
        try:
            import rclpy
            return True
        except ImportError:
            return False

    def connect(self) -> bool:
        try:
            import rclpy
            rclpy.init()
            self._node = rclpy.create_node("sim_backend_ros2")
            self.connected = True
            print("[SIM] ROS2 后端初始化成功")
            return True
        except Exception as e:
            print(f"[SIM] ROS2 连接失败: {e}，将降级到 PyBullet")
            return False

    def disconnect(self) -> None:
        if hasattr(self, "_node") and self._node:
            try:
                self._node.destroy_node()
            except Exception:
                pass
        try:
            import rclpy
            rclpy.shutdown()
        except Exception:
            pass
        self.connected = False

    def get_joint_states(self) -> List[float]:
        if not self.connected:
            return [0.0] * self.dofs
        return [0.0] * self.dofs  # Placeholder

    def get_ee_pose(self) -> Dict[str, Any]:
        if not self.connected:
            return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}
        return {"position": [0, 0, 0], "orientation": [0, 0, 0, 1]}

    def move_joints(self, joint_angles: List[float], speed: float = 1.0) -> None:
        pass

    def move_cartesian(self, x: float, y: float, z: float,
                        rx: float = 0, ry: float = 0, rz: float = 0,
                        speed: float = 1.0) -> None:
        pass

    def stop(self) -> None:
        pass


# ============================================================================
# 工厂函数（推荐使用方式）
# ============================================================================

# 后端注册表
_BACKEND_REGISTRY: Dict[str, type] = {
    "pybullet": PyBulletBackend,
    "mujoco": MuJoCoBackend,
    "isaac_sim": IsaacSimBackend,
    "isaacsim": IsaacSimBackend,
    "ros2": ROS2Backend,
    "gazebo": ROS2Backend,
}


def list_available_backends() -> List[str]:
    """列出当前环境中可用的仿真后端"""
    available = []
    for name, cls in _BACKEND_REGISTRY.items():
        if cls.is_available():
            available.append(name)
    return sorted(set(available))


def create_simulator_backend(
    backend_name: str,
    arm_config: Dict[str, Any],
    user_config: Optional[Dict[str, Any]] = None,
    safe_fallback: bool = True,
) -> SimulatorBackend:
    """创建仿真器后端实例

    Args:
        backend_name: 后端名称（pybullet/mujoco/isaac_sim/ros2）
        arm_config: 机器人配置（来自 robot_arm_db）
        user_config: 用户自定义配置
        safe_fallback: 是否在目标后端不可用时自动降级到 PyBullet

    Returns:
        SimulatorBackend 实例

    Raises:
        ImportError: 当 safe_fallback=False 且目标后端不可用时
    """
    name_lower = backend_name.lower()

    if name_lower not in _BACKEND_REGISTRY:
        print(f"[SIM] 未知后端: {backend_name}，可用后端: {list(_BACKEND_REGISTRY.keys())}")
        if safe_fallback:
            print("[SIM] 自动降级到 PyBullet")
            name_lower = "pybullet"
        else:
            raise ValueError(f"未知仿真后端: {backend_name}")

    backend_cls = _BACKEND_REGISTRY[name_lower]

    # 检查可用性
    if not backend_cls.is_available():
        if safe_fallback and name_lower != "pybullet":
            print(f"[SIM] 后端 {name_lower} 不可用（未安装依赖），降级到 PyBullet")
            backend_cls = PyBulletBackend
        elif not safe_fallback:
            raise ImportError(
                f"仿真后端 {name_lower} 不可用。"
                f"请安装对应依赖，或使用 safe_fallback=True 降级。"
                f"可用后端: {list_available_backends()}"
            )

    # 创建实例并尝试连接
    instance = backend_cls(arm_config, user_config)
    success = instance.connect()

    # 如果连接失败且允许降级，则退回 PyBullet
    if not success and safe_fallback and name_lower != "pybullet":
        print(f"[SIM] 后端 {name_lower} 连接失败，降级到 PyBullet")
        instance = PyBulletBackend(arm_config, user_config)
        instance.connect()

    return instance
