# -*- coding: utf-8 -*-
"""
PyBullet 仿真视图优化 - 完整版
功能：导入库、类定义、初始化物理引擎与加载模型、UI控制面板、视觉元素更新
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
import sys

class SimOptimizer:
    def __init__(self):
        # 连接物理引擎
        self.client = p.connect(p.GUI)
        if self.client < 0:
            print("PyBullet GUI 连接失败，请检查环境")
            sys.exit(1)
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        p.setRealTimeSimulation(0)
        
        # 加载平面
        self.plane_id = p.loadURDF("plane.urdf")
        
        # 加载机械臂（使用panda.urdf）
        self.robot_id = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)
        if self.robot_id < 0:
            print("机械臂URDF加载失败，请检查路径")
            sys.exit(1)
        
        # 获取机械臂关节信息
        self.num_joints = p.getNumJoints(self.robot_id)
        self.end_effector_index = 11
        
        # 状态变量
        self.end_pos = [0, 0, 0]
        self.target_pos = [0.45, 0.0, 0.35]
        self.distance = 0.0
        self.trajectory_line = -1
        self.status_text = -1
        self.dist_text = -1
        self.coord_lines = []
        self.collision_visible = True
        self.recording = False
        self.record_data = []
        self.target_body_id = -1
        self.status_light_body_id = -1
        
        # 初始化UI
        self._setup_ui()
        
        # 创建目标小球
        self._create_target_ball()
        
        # 更新视觉元素
        self._update_visuals()
        
        print("优化已启动！请查看UI面板进行操作。")

    def _create_target_ball(self):
        """创建目标小球"""
        visual_shape_id = p.createVisualShape(
            shapeType=p.GEOM_SPHERE,
            radius=0.03,
            rgbaColor=[1, 0, 0, 1]
        )
        self.target_body_id = p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=visual_shape_id,
            basePosition=self.target_pos
        )

    def _setup_ui(self):
        """初始化UI控制面板"""
        # ---- 状态灯（红黄绿球体） ----
        visual_shape_id = p.createVisualShape(
            shapeType=p.GEOM_SPHERE,
            radius=0.08,
            rgbaColor=[1, 0, 0, 1]
        )
        self.status_light_body_id = p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=visual_shape_id,
            basePosition=[0.5, 0.5, 0.5]
        )
        
        # ---- 状态文字 ----
        self.status_text = p.addUserDebugText(
            "MOVING",
            [0.65, 0.5, 0.5],
            textColorRGB=[1, 0, 0],
            textSize=1.5,
            lifeTime=0
        )
        
        # ---- 实时距离显示 ----
        self.dist_text = p.addUserDebugText(
            "DIST: 0.000 m",
            [0.5, 0.5, 0.35],
            textColorRGB=[1, 0, 0],
            textSize=1.2,
            lifeTime=0
        )
        
        # ---- 轨迹线（初始为空） ----
        self.trajectory_line = p.addUserDebugLine(
            [0,0,0], [0,0,0],
            lineColorRGB=[0,1,1],
            lineWidth=2,
            lifeTime=0
        )
        
        # ---- 坐标系指示器 ----
        self.coord_lines.append(p.addUserDebugLine(
            [0,0,0], [0.15,0,0],
            lineColorRGB=[1,0,0],
            lineWidth=2,
            lifeTime=0
        ))
        self.coord_lines.append(p.addUserDebugLine(
            [0,0,0], [0,0.15,0],
            lineColorRGB=[0,1,0],
            lineWidth=2,
            lifeTime=0
        ))
        self.coord_lines.append(p.addUserDebugLine(
            [0,0,0], [0,0,0.15],
            lineColorRGB=[0,0,1],
            lineWidth=2,
            lifeTime=0
        ))
        
        # ---- 视角预设按钮 ----
        self.view_front = p.addUserDebugParameter("正视", -1, 0, 0)
        self.view_side = p.addUserDebugParameter("侧视", -1, 0, 0)
        self.view_top = p.addUserDebugParameter("俯视", -1, 0, 0)
        self.view_free = p.addUserDebugParameter("自由视角", -1, 0, 0)
        
        # ---- 碰撞体显示切换 ----
        self.toggle_collision = p.addUserDebugParameter("显示碰撞体", 0, 1, 1)
        
        # ---- 录制控制 ----
        self.record_btn = p.addUserDebugParameter("录制轨迹", 0, 1, 0)
        
        # ---- 位置控制滑块 ----
        self.slider_x = p.addUserDebugParameter("目标X", -0.5, 0.8, self.target_pos[0])
        self.slider_y = p.addUserDebugParameter("目标Y", -0.5, 0.5, self.target_pos[1])
        self.slider_z = p.addUserDebugParameter("目标Z", 0.0, 0.8, self.target_pos[2])

    def _update_visuals(self):
        """更新所有视觉元素"""
        # 获取末端位置
        link_state = p.getLinkState(self.robot_id, self.end_effector_index)
        self.end_pos = list(link_state[4])
        
        # 计算距离
        dx = self.end_pos[0] - self.target_pos[0]
        dy = self.end_pos[1] - self.target_pos[1]
        dz = self.end_pos[2] - self.target_pos[2]
        self.distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        # ---- 更新轨迹线 ----
        p.removeUserDebugItem(self.trajectory_line)
        self.trajectory_line = p.addUserDebugLine(
            self.end_pos, self.target_pos,
            lineColorRGB=[0, 1, 1],
            lineWidth=2,
            lifeTime=0
        )
        
        # ---- 更新状态灯球体颜色 ----
        if self.distance < 0.01:
            light_color = [0, 1, 0, 1]
            light_text = "DONE"
            dist_text = "DIST: %.4f m" % self.distance
            dist_color = [0, 1, 0]
        elif self.distance < 0.05:
            light_color = [1, 1, 0, 1]
            light_text = "APPROACH"
            dist_text = "DIST: %.4f m" % self.distance
            dist_color = [1, 1, 0]
        else:
            light_color = [1, 0, 0, 1]
            light_text = "MOVING"
            dist_text = "DIST: %.4f m" % self.distance
            dist_color = [1, 0, 0]
        
        p.changeVisualShape(
            self.status_light_body_id,
            -1,
            rgbaColor=light_color
        )
        
        # ---- 更新状态文字 ----
        p.removeUserDebugItem(self.status_text)
        self.status_text = p.addUserDebugText(
            light_text,
            [0.65, 0.5, 0.5],
            textColorRGB=light_color[:3],
            textSize=1.5,
            lifeTime=0
        )
        
        # ---- 更新距离文本 ----
        p.removeUserDebugItem(self.dist_text)
        self.dist_text = p.addUserDebugText(
            dist_text,
            [0.5, 0.5, 0.35],
            textColorRGB=dist_color,
            textSize=1.2,
            lifeTime=0
        )

    def _handle_ui_inputs(self):
        """处理UI输入"""
        # ---- 视角控制 ----
        view_front = p.readUserDebugParameter(self.view_front)
        view_side = p.readUserDebugParameter(self.view_side)
        view_top = p.readUserDebugParameter(self.view_top)
        view_free = p.readUserDebugParameter(self.view_free)
        
        if view_front < -0.5:
            p.resetDebugVisualizerCamera(1.0, 0, 0, [0, 0, 0.3])
            p.removeUserDebugParameter(self.view_front)
            self.view_front = p.addUserDebugParameter("正视", -1, 0, 0)
        
        if view_side < -0.5:
            p.resetDebugVisualizerCamera(1.0, 90, 0, [0, 0, 0.3])
            p.removeUserDebugParameter(self.view_side)
            self.view_side = p.addUserDebugParameter("侧视", -1, 0, 0)
        
        if view_top < -0.5:
            p.resetDebugVisualizerCamera(2.0, 0, -90, [0, 0, 0.3])
            p.removeUserDebugParameter(self.view_top)
            self.view_top = p.addUserDebugParameter("俯视", -1, 0, 0)
        
        if view_free < -0.5:
            p.resetDebugVisualizerCamera(1.0, 45, -30, [0, 0, 0.3])
            p.removeUserDebugParameter(self.view_free)
            self.view_free = p.addUserDebugParameter("自由视角", -1, 0, 0)
        
        # ---- 碰撞体显示 ----
        show_collision = p.readUserDebugParameter(self.toggle_collision)
        if show_collision != self.collision_visible:
            self.collision_visible = show_collision
            print(f"碰撞体显示: {'开启' if show_collision else '关闭'}")
        
        # ---- 录制控制 ----
        record_state = p.readUserDebugParameter(self.record_btn)
        if record_state > 0.5 and not self.recording:
            self.recording = True
            self.record_data = []
            print("🎥 开始录制轨迹...")
        elif record_state < 0.5 and self.recording:
            self.recording = False
            print(f"📁 录制完成，共 {len(self.record_data)} 个点")
        
        if self.recording:
            self.record_data.append(self.end_pos.copy())
        
        # ---- 目标位置控制 ----
        x = p.readUserDebugParameter(self.slider_x)
        y = p.readUserDebugParameter(self.slider_y)
        z = p.readUserDebugParameter(self.slider_z)
        self.target_pos = [x, y, z]
        
        # 更新目标小球位置
        p.resetBasePositionAndOrientation(self.target_body_id, self.target_pos, [0, 0, 0, 1])

    def _move_to_target(self):
        """使用逆运动学移动机械臂到目标位置"""
        joint_poses = p.calculateInverseKinematics(
            self.robot_id,
            self.end_effector_index,
            self.target_pos,
            maxNumIterations=100,
            residualThreshold=0.001
        )
        
        # 设置关节目标位置（只设置非固定关节）
        pose_idx = 0
        for i in range(self.num_joints):
            info = p.getJointInfo(self.robot_id, i)
            if info[2] != p.JOINT_FIXED and pose_idx < len(joint_poses):
                p.setJointMotorControl2(
                    bodyUniqueId=self.robot_id,
                    jointIndex=i,
                    controlMode=p.POSITION_CONTROL,
                    targetPosition=joint_poses[pose_idx],
                    force=500
                )
                pose_idx += 1

    def run(self):
        """主循环"""
        try:
            while True:
                # 检查连接状态
                if p.getConnectionInfo(self.client)['isConnected'] == 0:
                    print("连接断开，退出仿真...")
                    break
                
                # 处理UI输入
                self._handle_ui_inputs()
                
                # 移动到目标
                self._move_to_target()
                
                # 步进仿真
                p.stepSimulation()
                
                # 更新视觉元素
                self._update_visuals()
                
                # 控制帧率
                time.sleep(1.0 / 120.0)
                
                # 检查退出（按ESC键退出）
                keys = p.getKeyboardEvents()
                for key, state in keys.items():
                    if key == 27 and state & p.KEY_WAS_RELEASED:
                        print("退出仿真...")
                        break
        except KeyboardInterrupt:
            print("\n退出仿真...")
        finally:
            try:
                p.disconnect()
            except:
                pass

if __name__ == "__main__":
    sim = SimOptimizer()
    sim.run()