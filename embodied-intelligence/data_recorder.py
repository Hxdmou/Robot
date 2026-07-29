"""
数据记录模块（轻量级）
安全原则：异步写入、文件轮转、内存限制
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



import os
import time
import csv
import json
import threading
from datetime import datetime


class DataRecorder:
    def __init__(self, config=None):
        config = config or {}
        self.enabled = config.get("enabled", True)
        self.record_interval = config.get("record_interval", 0.1)
        self.max_file_size = config.get("max_file_size", 10 * 1024 * 1024)
        self.max_files = config.get("max_files", 5)
        self.data_dir = config.get("data_dir", "data")
        
        self.running = False
        self.record_buffer = []
        self.max_buffer_size = 100
        self._lock = threading.Lock()
        self._write_thread = None
        
        self.current_file = None
        self.current_file_size = 0
        
        self._ensure_dir()

    def _ensure_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _generate_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.data_dir, f"robot_data_{timestamp}.csv")

    def _open_new_file(self):
        self.current_file = open(self._generate_filename(), "w", newline="")
        self.current_file_size = 0
        writer = csv.writer(self.current_file)
        writer.writerow([
            "timestamp", "cycle", "target_x", "target_y", "target_z",
            "current_x", "current_y", "current_z", "error_mm",
            "cpu_percent", "mem_percent", "collisions",
            "latency_ms", "disturbances"
        ])
        self.current_file.flush()

    def _rotate_files(self):
        files = sorted([f for f in os.listdir(self.data_dir) 
                       if f.startswith("robot_data_") and f.endswith(".csv")],
                      reverse=True)
        
        while len(files) >= self.max_files:
            oldest = files.pop()
            os.remove(os.path.join(self.data_dir, oldest))

    def _write_worker(self):
        while self.running:
            time.sleep(0.5)
            
            with self._lock:
                if not self.record_buffer:
                    continue
                
                buffer_copy = self.record_buffer.copy()
                self.record_buffer.clear()
            
            for record in buffer_copy:
                try:
                    if self.current_file is None or self.current_file_size >= self.max_file_size:
                        if self.current_file:
                            self.current_file.close()
                        self._rotate_files()
                        self._open_new_file()
                    
                    writer = csv.writer(self.current_file)
                    writer.writerow([
                        record["timestamp"], record["cycle"],
                        record["target_x"], record["target_y"], record["target_z"],
                        record["current_x"], record["current_y"], record["current_z"],
                        record["error_mm"], record["cpu_percent"],
                        record["mem_percent"], record["collisions"],
                        record.get("latency_ms", 0), record.get("disturbances", 0)
                    ])
                    
                    self.current_file_size += 1
                    self.current_file.flush()
                except Exception as e:
                    print(f"[DATA] 写入异常: {e}")

    def record(self, cycle, target_pos, current_pos, error_mm, cpu_percent, mem_percent, collisions=0, latency_ms=0, disturbances=0):
        if not self.enabled:
            return

        record = {
            "timestamp": datetime.now().isoformat(),
            "cycle": cycle,
            "target_x": target_pos[0],
            "target_y": target_pos[1],
            "target_z": target_pos[2],
            "current_x": current_pos[0],
            "current_y": current_pos[1],
            "current_z": current_pos[2],
            "error_mm": error_mm,
            "cpu_percent": cpu_percent,
            "mem_percent": mem_percent,
            "collisions": collisions,
            "latency_ms": latency_ms,
            "disturbances": disturbances
        }

        with self._lock:
            self.record_buffer.append(record)
            if len(self.record_buffer) > self.max_buffer_size:
                self.record_buffer.pop(0)

    def record_joint_states(self, cycle, joint_states):
        if not self.enabled:
            return

        filename = os.path.join(self.data_dir, f"joint_states_{datetime.now().strftime('%Y%m%d')}.csv")
        
        try:
            file_exists = os.path.exists(filename)
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["timestamp", "cycle", "joint_index", "angle", "velocity", "torque"])
                
                timestamp = datetime.now().isoformat()
                for idx, state in enumerate(joint_states):
                    writer.writerow([
                        timestamp, cycle, idx,
                        state.get("angle", 0),
                        state.get("velocity", 0),
                        state.get("torque", 0)
                    ])
        except Exception as e:
            print(f"[DATA] 关节状态记录异常: {e}")

    def start(self):
        if self.running:
            return
        
        self.running = True
        self._open_new_file()
        
        self._write_thread = threading.Thread(target=self._write_worker, daemon=True)
        self._write_thread.start()
        
        print(f"[DATA] 数据记录已启动 (目录: {self.data_dir})")

    def stop(self):
        self.running = False
        
        if self._write_thread:
            self._write_thread.join(timeout=5)
        
        with self._lock:
            for record in self.record_buffer:
                try:
                    if self.current_file:
                        writer = csv.writer(self.current_file)
                        writer.writerow([
                            record["timestamp"], record["cycle"],
                            record["target_x"], record["target_y"], record["target_z"],
                            record["current_x"], record["current_y"], record["current_z"],
                            record["error_mm"], record["cpu_percent"],
                            record["mem_percent"], record["collisions"],
                            record.get("latency_ms", 0), record.get("disturbances", 0)
                        ])
                except:
                    pass
            
            self.record_buffer.clear()
        
        if self.current_file:
            self.current_file.close()
            self.current_file = None
        
        print("[DATA] 数据记录已停止")

    def generate_report(self):
        report = {
            "generated_at": datetime.now().isoformat(),
            "data_files": [],
            "statistics": {}
        }
        
        csv_files = [f for f in os.listdir(self.data_dir) 
                    if f.startswith("robot_data_") and f.endswith(".csv")]
        
        report["data_files"] = csv_files
        
        total_errors = []
        total_cycles = 0
        
        for filename in csv_files:
            filepath = os.path.join(self.data_dir, filename)
            try:
                with open(filepath, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row["error_mm"]:
                            total_errors.append(float(row["error_mm"]))
                        total_cycles += 1
            except:
                pass
        
        if total_errors:
            report["statistics"] = {
                "total_cycles": total_cycles,
                "avg_error_mm": sum(total_errors) / len(total_errors),
                "min_error_mm": min(total_errors),
                "max_error_mm": max(total_errors),
                "success_rate": sum(1 for e in total_errors if e < 20) / len(total_errors) * 100
            }
        
        report_path = os.path.join(self.data_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        return report_path

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_enabled(self):
        return self.enabled
