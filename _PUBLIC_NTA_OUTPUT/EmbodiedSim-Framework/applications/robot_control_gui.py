"""
机器人控制 GUI 控制面板（Tkinter版）
================================================
展示「工程应用开发」能力：把仿真/真机的关节控制、末端位姿、
状态监控、急停按钮、日志面板整合到一个桌面应用中。

特性：
  - 7关节滑块组 实时手动遥操作
  - 末端位姿 (XYZ) 数字输入 + 单次移动按钮
  - 紧急停止大按钮（红底白字 + 回车快捷键）
  - 机器人状态实时文本监控面板
  - 事件日志输出窗口（带严重等级颜色）
  - 仿真连接/断开按钮
  - 域随机化一键采样按钮（演示 Sim2Real 集成）

说明：本GUI不依赖任何品牌SDK，仅依赖Python标准库 Tkinter + 本项目core层。
      未安装 PyBullet 时自动切到「无仿真 Mock 模式」，界面仍可完整演示。
"""

from __future__ import annotations

import os
import sys
import math
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Dict, List, Optional, Tuple


# ============================================================
# 工具：等级颜色映射
# ============================================================
LEVEL_COLOR = {
    "INFO": "#2d6cdf",
    "OK": "#1c8c3b",
    "WARN": "#c27a00",
    "CRITICAL": "#cf1322",
    "SAFETY": "#cf1322",
    "DEBUG": "#666666",
}


# ============================================================
# 主 GUI 类
# ============================================================
class RobotControlGUI:
    """
    机器人控制主界面（Tkinter）
    ------------------------------------------------
    启动：
        >>> from applications.robot_control_gui import RobotControlGUI
        >>> gui = RobotControlGUI(num_joints=7, title="EmbodiedSim-Framework 控制面板")
        >>> gui.run()
    """

    def __init__(self, num_joints: int = 7, title: str = "具身智能控制平台（公共示例版）"):
        self.num_joints = num_joints
        self.title_text = title
        # 仿真 & 状态
        self._sim = None
        self._sim_connected = False
        self._mock_mode = True  # 默认 Mock（未装 pybullet 也能用）
        # 安全控制器
        self._safety = None
        self._estop_active = False
        # 关节滑块引用
        self._joint_vars: List[tk.DoubleVar] = []
        self._joint_scales: List[tk.Scale] = []
        # 末端位置
        self._ee_vars: Dict[str, tk.DoubleVar] = {}
        # 刷新监控线程
        self._monitor_running = False
        self._monitor_thread: Optional[threading.Thread] = None

        # ---- 顶层窗口 ----
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("1180x780")
        self.root.minsize(1080, 680)
        self.root.configure(bg="#1e1e2e")
        # 全局样式
        self._style = ttk.Style(self.root)
        try:
            self._style.theme_use("clam")
        except Exception:
            pass
        self._style.configure("Title.TLabel", background="#1e1e2e",
                              foreground="#f4f4f5", font=("Microsoft YaHei", 14, "bold"))
        self._style.configure("Sub.TLabel", background="#1e1e2e",
                              foreground="#a9b1d6", font=("Microsoft YaHei", 9))
        self._style.configure("Card.TFrame", background="#24283b")
        self._style.configure("CardTitle.TLabel", background="#24283b",
                              foreground="#7aa2f7", font=("Microsoft YaHei", 11, "bold"))
        self._style.configure("Small.TButton", font=("Microsoft YaHei", 9))

        self._build_layout()
        self._build_shortcuts()
        self._log("INFO", "系统", "GUI启动完成（当前处于 Mock 演示模式）")
        self._log("OK", "系统", "点击左上角「连接仿真」可加载 PyBullet Panda 机械臂（如已安装）")

    # ============== 布局 ==============
    def _build_layout(self) -> None:
        # 顶部：标题 + 紧急停止
        top = tk.Frame(self.root, bg="#1e1e2e")
        top.pack(side="top", fill="x", padx=10, pady=(10, 8))
        ttk.Label(top, text=self.title_text, style="Title.TLabel").pack(side="left")
        # 连接按钮组
        btn_bar = tk.Frame(top, bg="#1e1e2e")
        btn_bar.pack(side="left", padx=20)
        self._btn_connect = ttk.Button(btn_bar, text="🔌 连接仿真",
                                       style="Small.TButton", command=self._on_connect_sim)
        self._btn_connect.pack(side="left", padx=4)
        self._btn_disconnect = ttk.Button(btn_bar, text="⏏️ 断开仿真",
                                          style="Small.TButton",
                                          command=self._on_disconnect_sim, state="disabled")
        self._btn_disconnect.pack(side="left", padx=4)
        ttk.Button(btn_bar, text="🎲 Sim2Real 随机化一键采样",
                   style="Small.TButton",
                   command=self._on_dr_sample).pack(side="left", padx=4)
        # 急停（右对齐，红底）
        self._btn_estop = tk.Button(
            top, text="🚨 紧急停止", font=("Microsoft YaHei", 14, "bold"),
            bg="#cf1322", fg="white", activebackground="#a8071a", activeforeground="white",
            relief="raised", bd=3, width=14, height=1,
            command=self._on_emergency_stop,
        )
        self._btn_estop.pack(side="right")
        ttk.Label(top, text="（快捷键：回车键）", style="Sub.TLabel").pack(side="right", padx=8)

        # 主体左右三栏：控制(关节+末端) | 状态 | 日志
        body = tk.Frame(self.root, bg="#1e1e2e")
        body.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))
        # ---- 左：关节与末端控制 ----
        self._build_control_panel(body)
        # ---- 中：状态监控 ----
        self._build_status_panel(body)
        # ---- 右：日志面板 ----
        self._build_log_panel(body)

        # 底部状态栏
        self._status_var = tk.StringVar(value="就绪")
        status = tk.Label(self.root, textvariable=self._status_var, anchor="w",
                          bg="#11111b", fg="#a6adc8", font=("Consolas", 10),
                          padx=10, pady=4)
        status.pack(side="bottom", fill="x")

    def _build_control_panel(self, parent: tk.Widget) -> None:
        wrap = ttk.Frame(parent, style="Card.TFrame")
        wrap.pack(side="left", fill="both", expand=True, padx=(0, 8))
        ttk.Label(wrap, text="🎮  关节 & 末端控制", style="CardTitle.TLabel").pack(
            anchor="w", padx=12, pady=(10, 4))
        inner = tk.Frame(wrap, bg="#24283b")
        inner.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        # 关节滑块
        joints_card = tk.LabelFrame(inner, text="关节位置控制 (rad)",
                                    bg="#24283b", fg="#7dcfff",
                                    font=("Microsoft YaHei", 10, "bold"), bd=1,
                                    labelanchor="nw", relief="groove")
        joints_card.pack(fill="x", padx=4, pady=6)
        self._joint_vars = []
        self._joint_scales = []
        default_limits = [(-2.9, 2.9)] * self.num_joints  # 通用示例限位
        sliders_frame = tk.Frame(joints_card, bg="#24283b")
        sliders_frame.pack(fill="x", padx=6, pady=6)
        for i in range(self.num_joints):
            lo, hi = default_limits[i] if i < len(default_limits) else (-3.14, 3.14)
            var = tk.DoubleVar(value=0.0)
            self._joint_vars.append(var)
            row = tk.Frame(sliders_frame, bg="#24283b")
            row.pack(fill="x", pady=1)
            tk.Label(row, text=f"J{i+1:02d}", width=4, bg="#24283b", fg="#c0caf5",
                     font=("Consolas", 10, "bold")).pack(side="left")
            sc = tk.Scale(row, variable=var, from_=lo, to=hi, orient="horizontal",
                          resolution=0.001, length=360, showvalue=True,
                          bg="#24283b", fg="#a9b1d6", troughcolor="#1e1e2e",
                          activebackground="#7aa2f7", highlightthickness=0,
                          command=lambda e, idx=i: self._on_joint_changed(idx))
            sc.pack(side="left", fill="x", expand=True, padx=4)
            self._joint_scales.append(sc)
            ttk.Button(row, text="归零", style="Small.TButton", width=6,
                       command=lambda idx=i: self._zero_joint(idx)).pack(side="left")
        # 全归零按钮
        btns = tk.Frame(joints_card, bg="#24283b")
        btns.pack(fill="x", padx=6, pady=(0, 8))
        ttk.Button(btns, text="全部关节归零",
                   style="Small.TButton", command=self._zero_all_joints).pack(side="left")
        ttk.Button(btns, text="应用当前关节 → 发送",
                   style="Small.TButton", command=self._send_joint_cmd).pack(side="left", padx=6)

        # 末端控制
        ee_card = tk.LabelFrame(inner, text="末端位置目标 (m)",
                                bg="#24283b", fg="#7dcfff",
                                font=("Microsoft YaHei", 10, "bold"), bd=1,
                                labelanchor="nw", relief="groove")
        ee_card.pack(fill="x", padx=4, pady=6)
        ee_frm = tk.Frame(ee_card, bg="#24283b")
        ee_frm.pack(fill="x", padx=8, pady=8)
        defaults = {"X": 0.50, "Y": 0.00, "Z": 0.45}
        for i, (axis, val) in enumerate(defaults.items()):
            tk.Label(ee_frm, text=f"{axis}:", bg="#24283b", fg="#c0caf5",
                     font=("Consolas", 10, "bold"), width=3).grid(row=0, column=i*3, padx=(6, 2), pady=2)
            v = tk.DoubleVar(value=val)
            self._ee_vars[axis] = v
            tk.Spinbox(ee_frm, from_=-2.0, to=2.0, increment=0.005,
                       textvariable=v, width=8,
                       font=("Consolas", 10), format="%.3f").grid(
                row=0, column=i*3+1, padx=(0, 8), pady=2)
        ttk.Button(ee_frm, text="▶ 移动末端",
                   style="Small.TButton", command=self._send_ee_cmd).grid(
            row=0, column=9, padx=10)

    def _build_status_panel(self, parent: tk.Widget) -> None:
        wrap = ttk.Frame(parent, style="Card.TFrame")
        wrap.pack(side="left", fill="both", expand=True, padx=8)
        ttk.Label(wrap, text="📊  系统状态监控", style="CardTitle.TLabel").pack(
            anchor="w", padx=12, pady=(10, 4))
        self._status_text = scrolledtext.ScrolledText(
            wrap, wrap="word", height=22,
            bg="#11111b", fg="#c0caf5", insertbackground="#c0caf5",
            font=("Consolas", 10), relief="flat", padx=10, pady=10,
        )
        self._status_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self._status_text.tag_configure("title", foreground="#7aa2f7",
                                        font=("Consolas", 10, "bold"))
        self._status_text.tag_configure("key", foreground="#7dcfff")
        self._status_text.tag_configure("ok", foreground="#9ece6a")
        self._status_text.tag_configure("warn", foreground="#e0af68")
        self._status_text.tag_configure("bad", foreground="#f7768e")
        self._update_status_panel_snapshot()

    def _build_log_panel(self, parent: tk.Widget) -> None:
        wrap = ttk.Frame(parent, style="Card.TFrame")
        wrap.pack(side="left", fill="both", expand=True, padx=(8, 0))
        head = tk.Frame(wrap, bg="#24283b")
        head.pack(fill="x", padx=12, pady=(10, 0))
        ttk.Label(head, text="📝  事件日志", style="CardTitle.TLabel").pack(side="left")
        ttk.Button(head, text="清空", style="Small.TButton",
                   command=self._clear_log).pack(side="right")
        self._log_text = scrolledtext.ScrolledText(
            wrap, wrap="word", height=22,
            bg="#11111b", fg="#c0caf5", insertbackground="#c0caf5",
            font=("Consolas", 9), relief="flat", padx=8, pady=8,
        )
        self._log_text.pack(fill="both", expand=True, padx=10, pady=(4, 10))
        for lv, color in LEVEL_COLOR.items():
            self._log_text.tag_configure(f"lvl_{lv}", foreground=color)
        self._log_text.tag_configure("ts", foreground="#565f89")

    # ============== 快捷键 ==============
    def _build_shortcuts(self) -> None:
        self.root.bind("<Return>", lambda e: self._on_emergency_stop())
        self.root.bind("<Control-r>", lambda e: self._reset_estop())

    # ============== 事件：急停/复位 ==============
    def _on_emergency_stop(self) -> None:
        if self._estop_active:
            return
        self._estop_active = True
        self._btn_estop.config(relief="sunken", bg="#ff4d4f")
        self._status_var.set("🚨 紧急停止已触发！按 Ctrl+R 复位")
        self._log("CRITICAL", "急停", "用户触发紧急停止（Enter键 / 红色大按钮）")
        # 断开仿真
        if self._sim_connected:
            self._on_disconnect_sim(reason="急停触发")

    def _reset_estop(self) -> None:
        if not self._estop_active:
            return
        self._estop_active = False
        self._btn_estop.config(relief="raised", bg="#cf1322")
        self._status_var.set("✔ 紧急停止已复位，可恢复操作")
        self._log("OK", "急停", "紧急停止已复位（Ctrl+R）")

    # ============== 事件：仿真连接 ==============
    def _on_connect_sim(self) -> None:
        if self._estop_active:
            messagebox.showwarning("急停中", "紧急停止已触发，先按 Ctrl+R 复位再连接仿真")
            return
        try:
            from core.simulation_env import PyBulletSimulationEnv, SimConfig
            self._sim = PyBulletSimulationEnv(SimConfig(mode="gui", verbose=True))
            self._sim.load_robot("panda")
            self._sim_connected = True
            self._mock_mode = False
            self._btn_connect.config(state="disabled")
            self._btn_disconnect.config(state="normal")
            self._log("OK", "仿真", "已连接 PyBullet (Panda) GUI 仿真")
            self._status_var.set("🟢 仿真已连接 (Panda GUI)")
            self._start_monitor_thread()
        except Exception as e:
            self._log("WARN", "仿真", f"PyBullet连接失败，自动降级为Mock演示模式: {repr(e)}")
            self._sim_connected = False
            self._mock_mode = True
            self._status_var.set("🟡 Mock演示模式（PyBullet未启动）")

    def _on_disconnect_sim(self, reason: str = "用户操作") -> None:
        if self._sim is not None:
            try:
                self._sim.close()
            except Exception:
                pass
        self._sim = None
        self._sim_connected = False
        self._monitor_running = False
        self._btn_connect.config(state="normal")
        self._btn_disconnect.config(state="disabled")
        self._status_var.set("⚪ 仿真已断开")
        self._log("INFO", "仿真", f"已断开PyBullet连接（原因：{reason}）")

    # ============== 事件：关节/末端 发送 ==============
    def _on_joint_changed(self, idx: int) -> None:
        # 仅记录（拖动时不频繁发），用户点击发送再下发
        self._status_var.set(f"已修改关节 J{idx+1:02d} = {self._joint_vars[idx].get():.3f} rad")

    def _zero_joint(self, idx: int) -> None:
        self._joint_vars[idx].set(0.0)
        self._send_joint_cmd()

    def _zero_all_joints(self) -> None:
        for v in self._joint_vars:
            v.set(0.0)
        self._send_joint_cmd()

    def _send_joint_cmd(self) -> None:
        if self._estop_active:
            self._log("SAFETY", "控制", "⚠ 急停触发，指令被拦截")
            return
        positions = [float(v.get()) for v in self._joint_vars]
        self._log("INFO", "控制", f"下发关节指令 = [{', '.join(f'{p:+.3f}' for p in positions)}]")
        if self._sim_connected and self._sim is not None:
            try:
                self._sim.set_joint_positions(positions)
                self._sim.step(50)
                self._log("OK", "仿真", "关节指令已应用到PyBullet (step×50)")
            except Exception as e:
                self._log("WARN", "仿真", f"应用失败: {repr(e)}")

    def _send_ee_cmd(self) -> None:
        if self._estop_active:
            self._log("SAFETY", "控制", "⚠ 急停触发，指令被拦截")
            return
        target = (self._ee_vars["X"].get(), self._ee_vars["Y"].get(), self._ee_vars["Z"].get())
        self._log("INFO", "控制", f"下发末端目标 = (x={target[0]:.3f}, y={target[1]:.3f}, z={target[2]:.3f}) m")
        if self._sim_connected and self._sim is not None:
            try:
                self._sim.set_end_effector_pose(target)
                self._sim.step(80)
                self._log("OK", "仿真", "末端IK指令已应用 (step×80)")
            except Exception as e:
                self._log("WARN", "仿真", f"应用失败: {repr(e)}")

    # ============== 事件：Sim2Real ==============
    def _on_dr_sample(self) -> None:
        try:
            from engineering.domain_randomization import DomainRandomizationManager
            dr = DomainRandomizationManager(seed=int(time.time() * 1000) % (2**31))
            sample = dr.randomize_episode(episode_id=hash(time.time()) % 1000000)
            lines = sample.summary().split("|")
            self._log("OK", "Sim2Real", f"已采样: {lines[1].strip()}")
            self._log("INFO", "Sim2Real", f"{lines[2].strip() if len(lines) > 2 else ''}")
            # 记录应用日志（仅示意，不碰真实body）
            applied = dr.apply_to_pybullet_body_hints(body_id=1, client_id=0)
            for a in applied[:2]:
                self._log("DEBUG", "Sim2Real", a)
        except Exception as e:
            self._log("WARN", "Sim2Real", f"采样失败: {repr(e)}")

    # ============== 日志 ==============
    def _log(self, level: str, source: str, msg: str) -> None:
        ts = time.strftime("%H:%M:%S") + f".{int((time.time()%1)*1000):03d}"
        tag_level = f"lvl_{level if level in LEVEL_COLOR else 'INFO'}"
        self.root.after(0, self._append_log, ts, level, source, msg, tag_level)

    def _append_log(self, ts: str, level: str, source: str, msg: str, tag_level: str) -> None:
        txt = self._log_text
        txt.insert("end", f"{ts}  ", "ts")
        txt.insert("end", f"[{level:8s}]  ", tag_level)
        txt.insert("end", f"{source:<10s}  ", "key")
        txt.insert("end", f"{msg}\n", tag_level)
        txt.see("end")

    def _clear_log(self) -> None:
        self._log_text.delete("1.0", "end")
        self._log("INFO", "日志", "日志面板已清空")

    # ============== 监控线程 ==============
    def _start_monitor_thread(self) -> None:
        if self._monitor_thread and self._monitor_thread.is_alive():
            return
        self._monitor_running = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop,
                                                name="GUI_Monitor", daemon=True)
        self._monitor_thread.start()

    def _monitor_loop(self) -> None:
        while self._monitor_running and self._sim_connected:
            try:
                if self._sim:
                    state = self._sim.get_robot_state()
                    self.root.after(0, self._apply_state_to_sliders, state)
            except Exception:
                pass
            time.sleep(0.2)

    def _apply_state_to_sliders(self, state) -> None:
        if not state.joint_positions:
            return
        for i, v in enumerate(state.joint_positions[: len(self._joint_vars)]):
            # 仅当用户不在拖动时设置（通过滑块状态简单判定：正常状态）
            try:
                self._joint_vars[i].set(v)
            except Exception:
                pass
        self._update_status_panel_snapshot(state)

    def _update_status_panel_snapshot(self, state=None) -> None:
        t = self._status_text
        t.delete("1.0", "end")
        t.insert("end", "───  系统环境  ───\n", "title")
        t.insert("end", f"  Python版本 : ", "key"); t.insert("end", f"{sys.version.split()[0]}\n", "ok")
        t.insert("end", f"  平台       : ", "key"); t.insert("end", f"{sys.platform}\n", "ok")
        t.insert("end", f"  PID        : ", "key"); t.insert("end", f"{os.getpid()}\n", "ok")
        t.insert("end", "\n───  仿真 / 连接  ───\n", "title")
        mode = "PyBullet-GUI" if self._sim_connected else ("Mock演示" if self._mock_mode else "未连接")
        color = "ok" if self._sim_connected else ("warn" if self._mock_mode else "bad")
        t.insert("end", f"  连接模式   : ", "key"); t.insert("end", f"{mode}\n", color)
        t.insert("end", f"  急停状态   : ", "key"); t.insert("end",
            f"{'🚨 ACTIVE' if self._estop_active else 'OK (未触发)'}\n",
            "bad" if self._estop_active else "ok")
        t.insert("end", "\n───  机器人快照  ───\n", "title")
        if state is not None and state.joint_positions:
            t.insert("end", f"  仿真步数   : ", "key"); t.insert("end",
                f"{getattr(self._sim, '_timestep_count', '?')}\n", "ok")
            t.insert("end", f"  仿真时长   : ", "key"); t.insert("end",
                f"{getattr(self._sim, 'elapsed_sim_time_s', lambda: 0.0)():.3f} s\n", "ok")
            t.insert("end", f"  末端 XYZ   : ", "key"); t.insert("end",
                f"({state.end_effector_pos[0]:.3f}, {state.end_effector_pos[1]:.3f}, {state.end_effector_pos[2]:.3f}) m\n",
                "ok")
            t.insert("end", "  关节角(rad): ", "key")
            t.insert("end", f"[{', '.join(f'{j:+.3f}' for j in state.joint_positions[:7])}]\n", "ok")
            if state.joint_torques:
                t.insert("end", "  关节力矩   : ", "key")
                t.insert("end", f"[{', '.join(f'{j:+.3f}' for j in state.joint_torques[:7])}] N·m\n", "ok")
        else:
            t.insert("end", "  (连接 PyBullet 后每 200ms 自动刷新本节)\n", "warn")
        try:
            import psutil
            mem = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=None)
            t.insert("\n───  性能  ───\n", "title")
            t.insert("end", f"  CPU使用率  : ", "key"); t.insert("end", f"{cpu:.1f} %\n", "warn" if cpu > 75 else "ok")
            t.insert("end", f"  内存使用   : ", "key"); t.insert("end",
                f"{(mem.total-mem.available)/(1024**3):.2f} GiB / {mem.total/(1024**3):.2f} GiB  ({mem.percent}%)\n",
                "warn" if mem.percent > 80 else "ok")
        except Exception:
            pass
        # 滚动到顶部
        t.mark_set("insert", "1.0")

    # ============== 主循环 ==============
    def run(self) -> None:
        # 关闭钩子
        def _on_close():
            self._monitor_running = False
            if self._sim is not None:
                try: self._sim.close()
                except Exception: pass
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW", _on_close)
        self.root.mainloop()


# ============================================================
# 直接运行入口
# ============================================================
if __name__ == "__main__":
    gui = RobotControlGUI(num_joints=7)
    gui.run()
