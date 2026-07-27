# -*- coding: utf-8 -*-
import sys
import math
import json
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QPushButton, QTextEdit, QFrame
)
from PyQt5.QtCore import Qt, QTimer


class RobotControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robot Control")
        self.setGeometry(100, 100, 600, 700)

        self.target_pos = [0.45, 0.0, 0.35]
        self.end_pos = [0, 0, 0]
        self.distance = 1.0

        self._setup_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_state)
        self.timer.start(25)

        print("Control GUI started!")

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        self.status_box = QFrame()
        self.status_box.setFixedHeight(200)
        self.status_box.setStyleSheet("background-color: rgb(255, 0, 0);")
        status_layout = QVBoxLayout(self.status_box)
        status_layout.setContentsMargins(20, 20, 20, 20)
        status_layout.setSpacing(10)

        self.status_text = QLabel("MOVING")
        self.status_text.setStyleSheet("font-size: 48px; font-weight: bold; color: white;")
        self.status_text.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_text)

        self.dist_label = QLabel("DIST: 0.000 m")
        self.dist_label.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        self.dist_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.dist_label)

        self.pos_label = QLabel("END: [0.000, 0.000, 0.000]\nTGT: [0.450, 0.000, 0.350]")
        self.pos_label.setStyleSheet("font-size: 18px; color: white;")
        self.pos_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.pos_label)

        main_layout.addWidget(self.status_box)

        pos_group = QFrame()
        pos_group.setStyleSheet("background-color: #333; border: 2px solid #666;")
        pos_layout = QVBoxLayout(pos_group)
        pos_layout.setContentsMargins(15, 15, 15, 15)
        pos_layout.setSpacing(15)

        title = QLabel("Target Position")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        pos_layout.addWidget(title)

        x_layout = QHBoxLayout()
        x_label = QLabel("X:")
        x_label.setStyleSheet("font-size: 16px; color: white;")
        x_label.setFixedWidth(30)
        self.slider_x = QSlider(Qt.Horizontal)
        self.slider_x.setRange(-50, 80)
        self.slider_x.setValue(45)
        self.slider_x.setStyleSheet("QSlider::groove:horizontal { height: 10px; background: #555; border-radius: 5px; } QSlider::handle:horizontal { background: #fff; width: 20px; margin: -5px 0; border-radius: 10px; }")
        self.slider_x.valueChanged.connect(self.update_target)
        x_val_label = QLabel("0.450")
        x_val_label.setStyleSheet("font-size: 16px; color: white;")
        x_val_label.setFixedWidth(60)
        x_layout.addWidget(x_label)
        x_layout.addWidget(self.slider_x)
        x_layout.addWidget(x_val_label)
        pos_layout.addLayout(x_layout)

        y_layout = QHBoxLayout()
        y_label = QLabel("Y:")
        y_label.setStyleSheet("font-size: 16px; color: white;")
        y_label.setFixedWidth(30)
        self.slider_y = QSlider(Qt.Horizontal)
        self.slider_y.setRange(-50, 50)
        self.slider_y.setValue(0)
        self.slider_y.setStyleSheet("QSlider::groove:horizontal { height: 10px; background: #555; border-radius: 5px; } QSlider::handle:horizontal { background: #fff; width: 20px; margin: -5px 0; border-radius: 10px; }")
        self.slider_y.valueChanged.connect(self.update_target)
        y_val_label = QLabel("0.000")
        y_val_label.setStyleSheet("font-size: 16px; color: white;")
        y_val_label.setFixedWidth(60)
        y_layout.addWidget(y_label)
        y_layout.addWidget(self.slider_y)
        y_layout.addWidget(y_val_label)
        pos_layout.addLayout(y_layout)

        z_layout = QHBoxLayout()
        z_label = QLabel("Z:")
        z_label.setStyleSheet("font-size: 16px; color: white;")
        z_label.setFixedWidth(30)
        self.slider_z = QSlider(Qt.Horizontal)
        self.slider_z.setRange(0, 80)
        self.slider_z.setValue(35)
        self.slider_z.setStyleSheet("QSlider::groove:horizontal { height: 10px; background: #555; border-radius: 5px; } QSlider::handle:horizontal { background: #fff; width: 20px; margin: -5px 0; border-radius: 10px; }")
        self.slider_z.valueChanged.connect(self.update_target)
        z_val_label = QLabel("0.350")
        z_val_label.setStyleSheet("font-size: 16px; color: white;")
        z_val_label.setFixedWidth(60)
        z_layout.addWidget(z_label)
        z_layout.addWidget(self.slider_z)
        z_layout.addWidget(z_val_label)
        pos_layout.addLayout(z_layout)

        main_layout.addWidget(pos_group)

        btn_group = QFrame()
        btn_group.setStyleSheet("background-color: #333; border: 2px solid #666;")
        btn_layout = QHBoxLayout(btn_group)
        btn_layout.setContentsMargins(15, 15, 15, 15)
        btn_layout.setSpacing(20)

        self.btn_home = QPushButton("Home")
        self.btn_home.setStyleSheet("font-size: 18px; padding: 10px 20px; background-color: #444; color: white; border: none;")
        self.btn_home.clicked.connect(self.go_home)
        btn_layout.addWidget(self.btn_home)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet("font-size: 18px; padding: 10px 20px; background-color: #444; color: white; border: none;")
        self.btn_reset.clicked.connect(self.reset_robot)
        btn_layout.addWidget(self.btn_reset)

        main_layout.addWidget(btn_group)

        log_group = QFrame()
        log_group.setStyleSheet("background-color: #333; border: 2px solid #666;")
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(15, 15, 15, 15)

        title3 = QLabel("Log")
        title3.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        log_layout.addWidget(title3)

        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setMaximumHeight(150)
        self.log_edit.setStyleSheet("background-color: #222; color: white; font-size: 14px;")
        log_layout.addWidget(self.log_edit)

        main_layout.addWidget(log_group)

    def update_target(self):
        x = self.slider_x.value() / 100.0
        y = self.slider_y.value() / 100.0
        z = self.slider_z.value() / 100.0
        self.target_pos = [x, y, z]

        try:
            data = {"target": self.target_pos}
            with open("robot_control.json", "w") as f:
                json.dump(data, f)
        except:
            pass

    def update_state(self):
        dx = self.end_pos[0] - self.target_pos[0]
        dy = self.end_pos[1] - self.target_pos[1]
        dz = self.end_pos[2] - self.target_pos[2]
        self.distance = math.sqrt(dx*dx + dy*dy + dz*dz)

        self.pos_label.setText(f"END: [{self.end_pos[0]:.3f}, {self.end_pos[1]:.3f}, {self.end_pos[2]:.3f}]\nTGT: [{self.target_pos[0]:.3f}, {self.target_pos[1]:.3f}, {self.target_pos[2]:.3f}]")
        self.dist_label.setText(f"DIST: {self.distance:.4f} m")

        if self.distance < 0.01:
            bg_color = "rgb(0, 255, 0)"
            status = "DONE"
        elif self.distance < 0.05:
            bg_color = "rgb(255, 255, 0)"
            status = "APPROACH"
        else:
            bg_color = "rgb(255, 0, 0)"
            status = "MOVING"

        text_color = "rgb(0, 0, 0)" if bg_color == "rgb(255, 255, 0)" else "rgb(255, 255, 255)"

        self.status_box.setStyleSheet(f"background-color: {bg_color};")
        self.status_text.setStyleSheet(f"font-size: 48px; font-weight: bold; color: {text_color};")
        self.status_text.setText(status)
        self.dist_label.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {text_color};")
        self.pos_label.setStyleSheet(f"font-size: 18px; color: {text_color};")

    def go_home(self):
        self.slider_x.setValue(40)
        self.slider_y.setValue(0)
        self.slider_z.setValue(35)
        self.log_edit.append("→ Home")

    def reset_robot(self):
        self.slider_x.setValue(45)
        self.slider_y.setValue(0)
        self.slider_z.setValue(35)
        self.log_edit.append("→ Reset")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotControlGUI()
    window.show()
    sys.exit(app.exec_())
