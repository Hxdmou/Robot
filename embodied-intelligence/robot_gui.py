# -*- coding: utf-8 -*-

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


import sys
import math
import numpy as np
import pybullet as p
import pybullet_data
import time

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QProgressBar, QLabel, QPushButton, QSlider, QGridLayout
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer


class RobotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot GUI - 优化版")
        self.setGeometry(100, 100, 1280, 720)

        self.client_id = p.connect(p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        p.setRealTimeSimulation(1)

        self.plane_id = p.loadURDF("plane.urdf")
        self.robot_id = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)
        self.num_joints = p.getNumJoints(self.robot_id)
        self.end_effector_index = 6

        initial_joint_angles = [0, -0.2, 0, -1.2, 0, 1.2, 0.3, 0.02, 0.02]
        for i in range(min(len(initial_joint_angles), self.num_joints)):
            p.resetJointState(self.robot_id, i, initial_joint_angles[i])

        visual_shape_id = p.createVisualShape(
            shapeType=p.GEOM_SPHERE,
            radius=0.03,
            rgbaColor=[1, 0, 0, 1]
        )
        self.target_body_id = p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=visual_shape_id,
            basePosition=[0.4, 0.0, 0.4]
        )

        self.target_pos = [0.4, 0.0, 0.4]
        self.end_pos = [0.0, 0.0, 0.0]
        self.distance = 1.0
        self.joint_angles = []
        self.reset_requested = False
        self.step_counter = 0
        self.ik_skip = False
        self.ik_skip_steps = 0
        self.waiting_for_user = False

        self._init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self._update_all)
        self.timer.start(50)

        print("Robot GUI 优化版已启动！")

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        left_panel = QFrame()
        left_panel.setFixedWidth(220)
        left_panel.setStyleSheet("background-color: #1a1a2e; border: 2px solid #333;")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignTop)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(12)

        title_left = QLabel("📊 实时状态")
        title_left.setStyleSheet("color: #fff; font-size: 20px; font-weight: bold;")
        title_left.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title_left)

        self.end_pos_label = QLabel("末端位置")
        self.end_pos_label.setStyleSheet("color: #aaa; font-size: 15px;")
        left_layout.addWidget(self.end_pos_label)

        self.end_pos_value = QLabel("X: 0.000  Y: 0.000  Z: 0.000")
        self.end_pos_value.setStyleSheet("color: #fff; font-size: 16px; font-weight: bold; background-color: #222; padding: 6px; border-radius: 4px;")
        left_layout.addWidget(self.end_pos_value)

        self.tgt_pos_label = QLabel("目标位置")
        self.tgt_pos_label.setStyleSheet("color: #aaa; font-size: 15px;")
        left_layout.addWidget(self.tgt_pos_label)

        self.tgt_pos_value = QLabel("X: 0.450  Y: 0.000  Z: 0.350")
        self.tgt_pos_value.setStyleSheet("color: #fff; font-size: 16px; font-weight: bold; background-color: #222; padding: 6px; border-radius: 4px;")
        left_layout.addWidget(self.tgt_pos_value)

        self.dist_value = QLabel("距离目标: 0.0000 m")
        self.dist_value.setStyleSheet("color: #ff6b6b; font-size: 18px; font-weight: bold; background-color: #222; padding: 8px; border-radius: 4px;")
        self.dist_value.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.dist_value)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #444;")
        left_layout.addWidget(line)

        joint_title = QLabel("🦾 关节角度 (前6个)")
        joint_title.setStyleSheet("color: #aaa; font-size: 15px;")
        left_layout.addWidget(joint_title)

        self.joint_values = QLabel("J1: 0.0°  J2: 0.0°  J3: 0.0°\nJ4: 0.0°  J5: 0.0°  J6: 0.0°")
        self.joint_values.setStyleSheet("color: #fff; font-size: 14px; background-color: #222; padding: 6px; border-radius: 4px;")
        left_layout.addWidget(self.joint_values)

        main_layout.addWidget(left_panel)

        center_panel = QFrame()
        center_panel.setStyleSheet("background-color: #0d0d1a; border: 2px solid #333;")
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(10, 10, 10, 10)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.image_label)

        main_layout.addWidget(center_panel)

        right_panel = QFrame()
        right_panel.setFixedWidth(220)
        right_panel.setStyleSheet("background-color: #1a1a2e; border: 2px solid #333;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignTop)
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(12)

        title_right = QLabel("🎮 控制面板")
        title_right.setStyleSheet("color: #fff; font-size: 20px; font-weight: bold;")
        title_right.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title_right)

        progress_label = QLabel("进度")
        progress_label.setStyleSheet("color: #aaa; font-size: 15px;")
        right_layout.addWidget(progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #222;
                border: 2px solid #444;
                border-radius: 5px;
                text-align: center;
                color: white;
                font-size: 16px;
            }
            QProgressBar::chunk {
                background-color: #ff0000;
                border-radius: 3px;
            }
        """)
        right_layout.addWidget(self.progress_bar)

        self.dist_label = QLabel("距离: 0.000m")
        self.dist_label.setStyleSheet("color: #aaa; font-size: 14px;")
        self.dist_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.dist_label)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("color: #444;")
        right_layout.addWidget(line2)

        slider_label_x = QLabel("目标 X")
        slider_label_x.setStyleSheet("color: #aaa; font-size: 14px;")
        right_layout.addWidget(slider_label_x)

        self.slider_x = QSlider(Qt.Horizontal)
        self.slider_x.setRange(25, 65)
        self.slider_x.setValue(45)
        self.slider_x.valueChanged.connect(self._update_target)
        right_layout.addWidget(self.slider_x)

        slider_label_y = QLabel("目标 Y")
        slider_label_y.setStyleSheet("color: #aaa; font-size: 14px;")
        right_layout.addWidget(slider_label_y)

        self.slider_y = QSlider(Qt.Horizontal)
        self.slider_y.setRange(-25, 25)
        self.slider_y.setValue(0)
        self.slider_y.valueChanged.connect(self._update_target)
        right_layout.addWidget(self.slider_y)

        slider_label_z = QLabel("目标 Z")
        slider_label_z.setStyleSheet("color: #aaa; font-size: 14px;")
        right_layout.addWidget(slider_label_z)

        self.slider_z = QSlider(Qt.Horizontal)
        self.slider_z.setRange(20, 55)
        self.slider_z.setValue(35)
        self.slider_z.valueChanged.connect(self._update_target)
        right_layout.addWidget(self.slider_z)

        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setStyleSheet("color: #444;")
        right_layout.addWidget(line3)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        home_btn = QPushButton("HOME")
        home_btn.setStyleSheet("background-color: #4a90d9; color: white; font-size: 16px; font-weight: bold; padding: 10px 20px; border-radius: 5px;")
        home_btn.clicked.connect(self._go_home)
        btn_layout.addWidget(home_btn)

        reset_btn = QPushButton("RESET")
        reset_btn.setStyleSheet("background-color: #d94a4a; color: white; font-size: 16px; font-weight: bold; padding: 10px 20px; border-radius: 5px;")
        reset_btn.clicked.connect(self._reset)
        btn_layout.addWidget(reset_btn)

        right_layout.addLayout(btn_layout)

        main_layout.addWidget(right_panel)

    def _update_target(self):
        if self.waiting_for_user:
            self.waiting_for_user = False
            self.ik_skip = False
        x = self.slider_x.value() / 100.0
        y = self.slider_y.value() / 100.0
        z = self.slider_z.value() / 100.0
        self.target_pos = [x, y, z]
        p.resetBasePositionAndOrientation(self.target_body_id, self.target_pos, [0, 0, 0, 1])

    def _go_home(self):
        self.target_pos = [0.4, 0.0, 0.4]
        self.slider_x.setValue(40)
        self.slider_y.setValue(0)
        self.slider_z.setValue(40)
        p.resetBasePositionAndOrientation(self.target_body_id, self.target_pos, [0, 0, 0, 1])

    def _reset(self):
        print("RESET 请求已记录")
        self.reset_requested = True

    def _do_reset(self):
        print("执行重置...")

        p.removeAllUserDebugItems()

        p.removeBody(self.robot_id)
        self.robot_id = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)
        self.end_effector_index = 11
        self.num_joints = p.getNumJoints(self.robot_id)

        initial_angles = [0, -0.2, 0, -0.5, 0, 0.8, 0.2, 0.02, 0.02]
        for i in range(min(len(initial_angles), self.num_joints)):
            p.resetJointState(self.robot_id, i, initial_angles[i])

        visual_shape_id = p.createVisualShape(
            shapeType=p.GEOM_SPHERE,
            radius=0.03,
            rgbaColor=[1, 0, 0, 1]
        )
        self.target_body_id = p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=visual_shape_id,
            basePosition=[0.0, 0.0, 0.55]
        )

        self.target_pos = [0.0, 0.0, 0.55]

        self.step_counter = 0
        self.ik_skip = True
        self.ik_skip_steps = 0
        self.waiting_for_user = True

        print("重置完成")

    def _update_all(self):
        if self.reset_requested:
            self._do_reset()
            self.reset_requested = False
            self._update_display()
            return

        if self.ik_skip:
            for _ in range(10):
                p.stepSimulation()
            self.step_counter += 10
            if self.step_counter >= 300:
                self.ik_skip = False
                self.waiting_for_user = False
            return

        if self.step_counter >= 300:
            return

        if self.step_counter == 0:
            joint_poses = p.calculateInverseKinematics(
                self.robot_id,
                self.end_effector_index,
                self.target_pos,
                maxNumIterations=500,
                residualThreshold=0.0005
            )
            pose_idx = 0
            for i in range(self.num_joints):
                info = p.getJointInfo(self.robot_id, i)
                if info[2] != p.JOINT_FIXED and pose_idx < len(joint_poses):
                    p.setJointMotorControl2(
                        bodyUniqueId=self.robot_id,
                        jointIndex=i,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=joint_poses[pose_idx],
                        force=2000.0,
                        positionGain=0.08,
                        velocityGain=0.15
                    )
                    pose_idx += 1

        for _ in range(10):
            p.stepSimulation()

        self.step_counter += 10

        if self.step_counter % 30 == 0:
            self._update_display()

        if self.step_counter >= 300:
            return

    def _update_display(self):
        link_state = p.getLinkState(self.robot_id, self.end_effector_index)
        self.end_pos = list(link_state[4])

        dx = self.end_pos[0] - self.target_pos[0]
        dy = self.end_pos[1] - self.target_pos[1]
        dz = self.end_pos[2] - self.target_pos[2]
        self.distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        self.end_pos_value.setText(f"X: {self.end_pos[0]:.3f}  Y: {self.end_pos[1]:.3f}  Z: {self.end_pos[2]:.3f}")
        self.tgt_pos_value.setText(f"X: {self.target_pos[0]:.3f}  Y: {self.target_pos[1]:.3f}  Z: {self.target_pos[2]:.3f}")

        if self.distance < 0.01:
            dist_color = "#00ff00"
        elif self.distance < 0.05:
            dist_color = "#ffff00"
        else:
            dist_color = "#ff6b6b"
        self.dist_value.setStyleSheet(f"color: {dist_color}; font-size: 18px; font-weight: bold; background-color: #222; padding: 8px; border-radius: 4px;")
        self.dist_value.setText(f"距离目标: {self.distance:.4f} m")

        joint_angles = []
        for i in range(min(6, self.num_joints)):
            info = p.getJointInfo(self.robot_id, i)
            if info[2] != p.JOINT_FIXED:
                state = p.getJointState(self.robot_id, i)
                joint_angles.append(math.degrees(state[0]))

        if len(joint_angles) >= 6:
            self.joint_values.setText(
                f"J1: {joint_angles[0]:.1f}°  J2: {joint_angles[1]:.1f}°  J3: {joint_angles[2]:.1f}°\n"
                f"J4: {joint_angles[3]:.1f}°  J5: {joint_angles[4]:.1f}°  J6: {joint_angles[5]:.1f}°"
            )

        max_dist = 0.8
        progress = max(0, min(100, int((1 - self.distance / max_dist) * 100)))
        self.progress_bar.setValue(progress)

        if progress >= 70:
            color = "#00ff00"
        elif progress >= 40:
            color = "#ffff00"
        else:
            color = "#ff0000"

        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #222;
                border: 2px solid #444;
                border-radius: 5px;
                text-align: center;
                color: white;
                font-size: 16px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)

        self.dist_label.setText(f"距离: {self.distance:.3f}m")

        width = 640
        height = 480
        img_arr = p.getCameraImage(
            width=width,
            height=height,
            viewMatrix=p.computeViewMatrix(
                cameraEyePosition=[1.5, 1.5, 1.5],
                cameraTargetPosition=[0, 0, 0.3],
                cameraUpVector=[0, 0, 1]
            ),
            projectionMatrix=p.computeProjectionMatrixFOV(
                fov=60,
                aspect=width/height,
                nearVal=0.1,
                farVal=100
            )
        )

        rgba = img_arr[2]
        rgba_np = np.reshape(rgba, (height, width, 4))
        rgba_np = rgba_np[:, :, :3]
        rgba_np = np.flip(rgba_np, axis=0)
        rgba_np = rgba_np.astype(np.uint8)

        qimage = QImage(rgba_np.tobytes(), width, height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotGUI()
    window.show()
    sys.exit(app.exec_())