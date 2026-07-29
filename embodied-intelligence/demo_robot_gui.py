
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
import numpy as np
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QSlider, QProgressBar, QShortcut)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QImage, QPixmap, QKeySequence
from ollama_client import OllamaClient

class RobotThread(QThread):
    status_update = pyqtSignal(np.ndarray, np.ndarray, float)
    log_update = pyqtSignal(str)
    image_update = pyqtSignal(QImage)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.target_pos = np.array([0.45, 0.0, 0.35])
        self.trail_points = []
        
        self.cam_pos = np.array([0.8, 0.6, 0.8])
        self.cam_target = np.array([0.45, 0.0, 0.35])
        self.cam_up = np.array([0, 0, 1])
    
    def run(self):
        client = p.connect(p.DIRECT)
        data_path = pybullet_data.getDataPath()
        p.setAdditionalSearchPath(data_path)
        p.setGravity(0, 0, -9.81)
        
        plane = p.loadURDF("plane.urdf")
        
        urdf_path = f"{data_path}/kuka_iiwa/model.urdf"
        robot = p.loadURDF(urdf_path, useFixedBase=True)
        
        joint_indices = []
        for j in range(p.getNumJoints(robot)):
            info = p.getJointInfo(robot, j)
            if info[2] == p.JOINT_REVOLUTE:
                joint_indices.append(j)
        
        end_effector_idx = 6
        
        goal_id = p.createVisualShape(p.GEOM_SPHERE, radius=0.03, rgbaColor=[1, 0, 0, 1])
        goal_body = p.createMultiBody(baseVisualShapeIndex=goal_id)
        p.resetBasePositionAndOrientation(goal_body, self.target_pos, [0,0,0,1])
        
        obstacle_id = p.createVisualShape(p.GEOM_CYLINDER, radius=0.08, length=0.5, rgbaColor=[0.7, 0.7, 0.7, 1])
        obstacle_body = p.createMultiBody(baseVisualShapeIndex=obstacle_id)
        p.resetBasePositionAndOrientation(obstacle_body, [0.40, 0.0, 0.25], [0,0,0,1])
        
        def get_end_pos():
            link_state = p.getLinkState(robot, end_effector_idx)
            return np.array(link_state[0])
        
        self.log_update.emit("✅ 机械臂仿真已启动")
        self.log_update.emit("ℹ️ 大模型: qwen3:8b (使用时自动连接)")
        
        frame_count = 0
        while self.running:
            p.resetBasePositionAndOrientation(goal_body, self.target_pos, [0,0,0,1])
            
            end_pos = get_end_pos()
            
            try:
                ik_solution = p.calculateInverseKinematics(robot, end_effector_idx, list(self.target_pos))
                for i, idx in enumerate(joint_indices):
                    p.setJointMotorControl2(robot, idx, p.POSITION_CONTROL, 
                                          targetPosition=ik_solution[i], force=240)
            except:
                pass
            
            self.trail_points.append(end_pos.copy())
            if len(self.trail_points) > 50:
                self.trail_points.pop(0)
            
            for i in range(len(self.trail_points) - 1):
                p.addUserDebugLine(list(self.trail_points[i]), list(self.trail_points[i+1]), 
                                  [0, 0, 1], lineWidth=3, lifeTime=0.05)
            
            dist = np.linalg.norm(end_pos - self.target_pos)
            self.status_update.emit(end_pos, self.target_pos, dist)
            
            p.stepSimulation()
            
            frame_count += 1
            if frame_count % 5 == 0:
                img_arr = p.getCameraImage(width=800, height=600, 
                                          viewMatrix=p.computeViewMatrix(list(self.cam_pos), 
                                                                          list(self.cam_target), 
                                                                          list(self.cam_up)),
                                          projectionMatrix=p.computeProjectionMatrixFOV(fov=60, aspect=800/600, 
                                                                                     nearVal=0.01, farVal=100))
                
                w, h, rgba, depth, seg = img_arr
                rgba_np = np.array(rgba, dtype=np.uint8).reshape(h, w, 4)
                rgba_np = rgba_np[:, :, :3]
                qimage = QImage(rgba_np.tobytes(), w, h, QImage.Format_RGB888)
                self.image_update.emit(qimage)
            
            time.sleep(1/240)
        
        p.disconnect(client)
    
    def set_target(self, x, y, z):
        self.target_pos = np.array([x, y, z])
    
    def rotate_camera(self, dx, dy):
        cam_dir = self.cam_pos - self.cam_target
        dist = np.linalg.norm(cam_dir)
        cam_dir_norm = cam_dir / dist
        
        right = np.cross(cam_dir_norm, self.cam_up)
        right = right / np.linalg.norm(right)
        
        up = np.cross(right, cam_dir_norm)
        
        angle_y = dx * 0.01
        angle_x = dy * 0.01
        
        rot_y = np.array([
            [np.cos(angle_y), 0, np.sin(angle_y)],
            [0, 1, 0],
            [-np.sin(angle_y), 0, np.cos(angle_y)]
        ])
        
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(angle_x), -np.sin(angle_x)],
            [0, np.sin(angle_x), np.cos(angle_x)]
        ])
        
        new_dir = rot_y @ cam_dir
        new_dir = rot_x @ new_dir
        
        self.cam_pos = self.cam_target + new_dir
        
    def pan_camera(self, dx, dy):
        cam_dir = self.cam_pos - self.cam_target
        dist = np.linalg.norm(cam_dir)
        cam_dir_norm = cam_dir / dist
        
        right = np.cross(cam_dir_norm, self.cam_up)
        right = right / np.linalg.norm(right)
        
        up = np.cross(right, cam_dir_norm)
        
        pan_speed = dist * 0.002
        self.cam_pos += right * dx * pan_speed - up * dy * pan_speed
        self.cam_target += right * dx * pan_speed - up * dy * pan_speed
    
    def zoom_camera(self, dz):
        cam_dir = self.cam_pos - self.cam_target
        dist = np.linalg.norm(cam_dir)
        cam_dir_norm = cam_dir / dist
        
        zoom_speed = dist * 0.001
        new_dist = max(0.3, dist + dz * zoom_speed)
        
        self.cam_pos = self.cam_target + cam_dir_norm * new_dist
    
    def reset_camera(self):
        self.cam_pos = np.array([0.8, 0.6, 0.8])
        self.cam_target = np.array([0.45, 0.0, 0.35])
        self.cam_up = np.array([0, 0, 1])
    
    def reset(self):
        self.target_pos = np.array([0.45, 0.0, 0.35])
        self.trail_points = []
    
    def stop(self):
        self.running = False

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.last_mouse_pos = None
        self.dragging_left = False
        self.dragging_right = False
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging_left = True
            self.last_mouse_pos = event.pos()
        elif event.button() == Qt.RightButton:
            self.dragging_right = True
            self.last_mouse_pos = event.pos()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging_left = False
        elif event.button() == Qt.RightButton:
            self.dragging_right = False
    
    def mouseMoveEvent(self, event):
        if self.last_mouse_pos is not None:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            
            if self.dragging_left:
                self.parent().parent().rotate_camera(dx, dy)
            elif self.dragging_right:
                self.parent().parent().pan_camera(dx, dy)
            
            self.last_mouse_pos = event.pos()
    
    def wheelEvent(self, event):
        dz = event.angleDelta().y()
        self.parent().parent().zoom_camera(dz)

class RobotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 机械臂Ollama智能控制")
        self.setGeometry(50, 50, 1400, 900)
        
        self.end_pos = np.array([0.0, 0.0, 0.0])
        self.goal_pos = np.array([0.45, 0.0, 0.35])
        self.distance = 0.0
        
        self.init_ui()
        self.start_robot()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(360)
        
        model_group = QGroupBox("🤖 大模型状态")
        model_layout = QVBoxLayout(model_group)
        self.model_label = QLabel("模型: qwen3:8b | 状态: 已就绪")
        self.model_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.model_label.setStyleSheet("color: #00d4ff;")
        model_layout.addWidget(self.model_label)
        model_bar = QProgressBar()
        model_bar.setRange(0, 100)
        model_bar.setValue(100)
        model_bar.setStyleSheet("QProgressBar { background-color: #333; } QProgressBar::chunk { background-color: #00d4ff; }")
        model_layout.addWidget(model_bar)
        left_layout.addWidget(model_group)
        
        slider_group = QGroupBox("🎚️ 目标位置控制")
        slider_layout = QVBoxLayout(slider_group)
        
        x_layout = QHBoxLayout()
        x_label = QLabel("X:")
        x_label.setFixedWidth(30)
        self.x_slider = QSlider(Qt.Horizontal)
        self.x_slider.setRange(25, 65)
        self.x_slider.setValue(45)
        self.x_slider.valueChanged.connect(self.on_slider_change)
        self.x_val = QLabel("0.450")
        self.x_val.setFixedWidth(60)
        x_layout.addWidget(x_label)
        x_layout.addWidget(self.x_slider)
        x_layout.addWidget(self.x_val)
        slider_layout.addLayout(x_layout)
        
        y_layout = QHBoxLayout()
        y_label = QLabel("Y:")
        y_label.setFixedWidth(30)
        self.y_slider = QSlider(Qt.Horizontal)
        self.y_slider.setRange(-25, 25)
        self.y_slider.setValue(0)
        self.y_slider.valueChanged.connect(self.on_slider_change)
        self.y_val = QLabel("0.000")
        self.y_val.setFixedWidth(60)
        y_layout.addWidget(y_label)
        y_layout.addWidget(self.y_slider)
        y_layout.addWidget(self.y_val)
        slider_layout.addLayout(y_layout)
        
        z_layout = QHBoxLayout()
        z_label = QLabel("Z:")
        z_label.setFixedWidth(30)
        self.z_slider = QSlider(Qt.Horizontal)
        self.z_slider.setRange(20, 55)
        self.z_slider.setValue(35)
        self.z_slider.valueChanged.connect(self.on_slider_change)
        self.z_val = QLabel("0.350")
        self.z_val.setFixedWidth(60)
        z_layout.addWidget(z_label)
        z_layout.addWidget(self.z_slider)
        z_layout.addWidget(self.z_val)
        slider_layout.addLayout(z_layout)
        
        reset_btn = QPushButton("🔄 重置位置")
        reset_btn.clicked.connect(self.on_reset)
        reset_btn.setStyleSheet("QPushButton { background-color: #6366f1; color: white; padding: 8px; border-radius: 4px; }")
        slider_layout.addWidget(reset_btn)
        left_layout.addWidget(slider_group)
        
        status_group = QGroupBox("📊 机械臂状态")
        status_layout = QVBoxLayout(status_group)
        
        end_group = QGroupBox("末端位置 (白色)")
        end_layout = QVBoxLayout(end_group)
        self.end_x = QLabel("X: 0.000")
        self.end_x.setStyleSheet("color: white;")
        self.end_y = QLabel("Y: 0.000")
        self.end_y.setStyleSheet("color: white;")
        self.end_z = QLabel("Z: 0.000")
        self.end_z.setStyleSheet("color: white;")
        end_layout.addWidget(self.end_x)
        end_layout.addWidget(self.end_y)
        end_layout.addWidget(self.end_z)
        status_layout.addWidget(end_group)
        
        goal_group = QGroupBox("目标位置 (红色)")
        goal_layout = QVBoxLayout(goal_group)
        self.goal_x = QLabel("X: 0.450")
        self.goal_x.setStyleSheet("color: #ef4444;")
        self.goal_y = QLabel("Y: 0.000")
        self.goal_y.setStyleSheet("color: #ef4444;")
        self.goal_z = QLabel("Z: 0.350")
        self.goal_z.setStyleSheet("color: #ef4444;")
        goal_layout.addWidget(self.goal_x)
        goal_layout.addWidget(self.goal_y)
        goal_layout.addWidget(self.goal_z)
        status_layout.addWidget(goal_group)
        
        dist_group = QGroupBox("距离目标 (绿色)")
        dist_layout = QVBoxLayout(dist_group)
        self.dist_label = QLabel("0.0000m")
        self.dist_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.dist_label.setStyleSheet("color: #22c55e; background-color: #1f2937; padding: 15px; border-radius: 8px;")
        self.dist_label.setAlignment(Qt.AlignCenter)
        dist_layout.addWidget(self.dist_label)
        status_layout.addWidget(dist_group)
        left_layout.addWidget(status_group)
        
        cmd_group = QGroupBox("⚡ 快捷指令")
        cmd_layout = QVBoxLayout(cmd_group)
        
        btn_row = QHBoxLayout()
        quick_cmds = ["回家", "左", "右", "高", "低"]
        for cmd in quick_cmds:
            btn = QPushButton(cmd)
            btn.clicked.connect(lambda checked, c=cmd: self.send_command(c))
            btn.setStyleSheet("QPushButton { background-color: #3b82f6; color: white; padding: 8px 12px; border-radius: 4px; }")
            btn_row.addWidget(btn)
        cmd_layout.addLayout(btn_row)
        
        shortcut_label = QLabel("快捷键: H(回家) ←(左) →(右) ↑(高) ↓(低) R(重置) ESC(退出)")
        shortcut_label.setStyleSheet("color: #94a3b8; font-size: 11px;")
        shortcut_label.setAlignment(Qt.AlignCenter)
        cmd_layout.addWidget(shortcut_label)
        left_layout.addWidget(cmd_group)
        
        input_group = QGroupBox("✉️ 自然语言指令")
        input_layout = QVBoxLayout(input_group)
        self.cmd_input = QLineEdit()
        self.cmd_input.returnPressed.connect(self.send_from_input)
        self.cmd_input.setPlaceholderText("输入指令，如: 移动到位置 X 0.45 Y 0.0 Z 0.35")
        input_layout.addWidget(self.cmd_input)
        send_btn = QPushButton("发送")
        send_btn.clicked.connect(self.send_from_input)
        send_btn.setStyleSheet("QPushButton { background-color: #10b981; color: white; padding: 8px; border-radius: 4px; }")
        input_layout.addWidget(send_btn)
        left_layout.addWidget(input_group)
        
        log_group = QGroupBox("📝 交互日志")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("QTextEdit { background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas; font-size: 11px; }")
        log_layout.addWidget(self.log_text)
        left_layout.addWidget(log_group)
        
        main_layout.addWidget(left_panel)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        title_label = QLabel("🎮 机械臂仿真视图")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #fbbf24;")
        title_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title_label)
        
        self.image_label = ImageLabel()
        self.image_label.setStyleSheet("background-color: #000; border: 2px solid #475569; border-radius: 8px;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 600)
        right_layout.addWidget(self.image_label)
        
        cam_tips = QLabel("🖱️ 左键拖动: 旋转视角 | 右键拖动: 平移视角 | 滚轮: 缩放 | C: 重置视角")
        cam_tips.setStyleSheet("color: #94a3b8; font-size: 12px;")
        cam_tips.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(cam_tips)
        
        tips_label = QLabel("💡 提示: 拖动滑块控制机械臂，点击快捷按钮快速移动")
        tips_label.setStyleSheet("color: #64748b; font-size: 12px;")
        tips_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(tips_label)
        
        main_layout.addWidget(right_panel)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #0f172a; }
            QWidget { background-color: #0f172a; color: white; }
            QGroupBox { border: 1px solid #334155; border-radius: 8px; margin-top: 10px; padding-top: 10px; background-color: #1e293b; }
            QGroupBox::title { color: #fbbf24; font-weight: bold; padding-left: 8px; }
            QLabel { color: white; }
            QLineEdit { background-color: #374151; border: 1px solid #4b5563; color: white; padding: 5px; }
            QSlider::groove:horizontal { height: 8px; background: #374151; border-radius: 4px; }
            QSlider::handle:horizontal { background: #3b82f6; width: 18px; margin: -5px 0; border-radius: 9px; }
        """)
        
        QShortcut(QKeySequence(Qt.Key_H), self, lambda: self.send_command("回家"))
        QShortcut(QKeySequence(Qt.Key_Left), self, lambda: self.send_command("左"))
        QShortcut(QKeySequence(Qt.Key_Right), self, lambda: self.send_command("右"))
        QShortcut(QKeySequence(Qt.Key_Up), self, lambda: self.send_command("高"))
        QShortcut(QKeySequence(Qt.Key_Down), self, lambda: self.send_command("低"))
        QShortcut(QKeySequence(Qt.Key_R), self, self.on_reset)
        QShortcut(QKeySequence(Qt.Key_C), self, self.reset_camera_view)
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.close)
    
    def rotate_camera(self, dx, dy):
        if hasattr(self, 'robot_thread'):
            self.robot_thread.rotate_camera(dx, dy)
    
    def pan_camera(self, dx, dy):
        if hasattr(self, 'robot_thread'):
            self.robot_thread.pan_camera(dx, dy)
    
    def zoom_camera(self, dz):
        if hasattr(self, 'robot_thread'):
            self.robot_thread.zoom_camera(dz)
    
    def reset_camera_view(self):
        if hasattr(self, 'robot_thread'):
            self.robot_thread.reset_camera()
        self.log_text.append("<span style='color:#6366f1;'>>>> 视角已重置</span>")
    
    def on_slider_change(self):
        x = self.x_slider.value() / 100.0
        y = self.y_slider.value() / 100.0
        z = self.z_slider.value() / 100.0
        
        self.x_val.setText(f"{x:.3f}")
        self.y_val.setText(f"{y:.3f}")
        self.z_val.setText(f"{z:.3f}")
        
        self.goal_x.setText(f"X: {x:.3f}")
        self.goal_y.setText(f"Y: {y:.3f}")
        self.goal_z.setText(f"Z: {z:.3f}")
        
        if hasattr(self, 'robot_thread'):
            self.robot_thread.set_target(x, y, z)
    
    def on_reset(self):
        self.x_slider.setValue(45)
        self.y_slider.setValue(0)
        self.z_slider.setValue(35)
        if hasattr(self, 'robot_thread'):
            self.robot_thread.reset()
        self.log_text.append("<span style='color:#6366f1;'>>>> 位置已重置</span>")
    
    def send_command(self, cmd):
        self.log_text.append(f"<span style='color:#3b82f6;'>>>> {cmd}</span>")
        
        presets = {
            "回家": [0.45, 0.0, 0.35],
            "左": [0.35, 0.15, 0.30],
            "右": [0.35, -0.15, 0.30],
            "高": [0.45, 0.0, 0.45],
            "低": [0.45, 0.0, 0.25],
        }
        
        if cmd in presets:
            x, y, z = presets[cmd]
            self.x_slider.setValue(int(x * 100))
            self.y_slider.setValue(int(y * 100))
            self.z_slider.setValue(int(z * 100))
            return
        
        self.process_ollama(cmd)
    
    def send_from_input(self):
        cmd = self.cmd_input.text().strip()
        if cmd:
            self.send_command(cmd)
            self.cmd_input.clear()
    
    def process_ollama(self, cmd):
        self.model_label.setText("模型: qwen3:8b | 状态: 思考中...")
        self.model_label.setStyleSheet("color: #f97316;")
        
        def run_ollama():
            try:
                client_ollama = OllamaClient(model="qwen3:8b")
                prompt = f"""
你是一个机械臂控制助手。用户说："{cmd}"
请从以下指令中选择并输出最合适的动作：
- "goto X Y Z"（例如 goto 0.45 0.0 0.35）
- "reset"（回到初始姿态）
- "unknown"（无法理解）
只输出动作，不要多余内容。
"""
                response = client_ollama.generate(prompt, temperature=0.1, max_tokens=50)
                self.log_text.append(f"<span style='color:#a855f7;'>Ollama 返回: {response}</span>")
                
                if response.startswith("goto"):
                    parts = response.split()
                    if len(parts) >= 4:
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        self.x_slider.setValue(int(x * 100))
                        self.y_slider.setValue(int(y * 100))
                        self.z_slider.setValue(int(z * 100))
                        self.log_text.append(f"<span style='color:#fbbf24;'>目标已更新至: ({x:.3f}, {y:.3f}, {z:.3f})</span>")
                
                self.model_label.setText("模型: qwen3:8b | 状态: 已就绪")
                self.model_label.setStyleSheet("color: #00d4ff;")
            except Exception as e:
                self.log_text.append(f"<span style='color:#ef4444;'>大模型错误: {e}</span>")
                self.model_label.setText("模型: qwen3:8b | 状态: 已就绪")
                self.model_label.setStyleSheet("color: #00d4ff;")
        
        import threading
        t = threading.Thread(target=run_ollama, daemon=True)
        t.start()
    
    def update_status(self, end_pos, goal_pos, distance):
        self.end_pos = end_pos
        self.goal_pos = goal_pos
        self.distance = distance
        
        self.end_x.setText(f"X: {end_pos[0]:.3f}")
        self.end_y.setText(f"Y: {end_pos[1]:.3f}")
        self.end_z.setText(f"Z: {end_pos[2]:.3f}")
        
        self.dist_label.setText(f"{distance:.4f}m")
        
        if distance < 0.02:
            self.dist_label.setStyleSheet("color: #22c55e; background-color: #166534; padding: 15px; border-radius: 8px; font-size: 28px; font-weight: bold;")
        elif distance < 0.1:
            self.dist_label.setStyleSheet("color: #eab308; background-color: #854d0e; padding: 15px; border-radius: 8px; font-size: 28px; font-weight: bold;")
        else:
            self.dist_label.setStyleSheet("color: #ef4444; background-color: #7f1d1d; padding: 15px; border-radius: 8px; font-size: 28px; font-weight: bold;")
    
    def update_image(self, qimage):
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
    
    def update_log(self, text):
        colors = {
            "✅": "#22c55e",
            "到达": "#22c55e",
            "目标": "#fbbf24",
            "机械臂": "#06b6d4",
        }
        
        color = "#e2e8f0"
        for key, col in colors.items():
            if key in text:
                color = col
                break
        
        self.log_text.append(f"<span style='color:{color};'>{text}</span>")
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())
    
    def start_robot(self):
        self.robot_thread = RobotThread()
        self.robot_thread.status_update.connect(self.update_status)
        self.robot_thread.image_update.connect(self.update_image)
        self.robot_thread.log_update.connect(self.update_log)
        self.robot_thread.start()
    
    def closeEvent(self, event):
        if hasattr(self, 'robot_thread'):
            self.robot_thread.stop()
            self.robot_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotGUI()
    window.show()
    sys.exit(app.exec_())