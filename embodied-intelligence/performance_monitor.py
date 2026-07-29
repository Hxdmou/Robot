"""
性能监控脚本（轻量级）
安全原则：低资源占用、定时采样、自动清理
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



import psutil
import time
import threading
import os

class PerformanceMonitor:
    def __init__(self, log_interval=2.5, max_samples=200):
        self.log_interval = log_interval
        self.max_samples = max_samples
        self.running = False
        self.thread = None
        self.samples = []
        self._lock = threading.Lock()

    def _get_system_metrics(self):
        metrics = {
            "timestamp": time.time(),
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_gb": psutil.virtual_memory().used / (1024**3),
            "memory_total_gb": psutil.virtual_memory().total / (1024**3),
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "network_sent_mb": psutil.net_io_counters().bytes_sent / (1024**2),
            "network_recv_mb": psutil.net_io_counters().bytes_recv / (1024**2),
        }

        try:
            temp = psutil.sensors_temperatures()
            if temp:
                for name, entries in temp.items():
                    if name == 'coretemp':
                        metrics[f"cpu_temp_{name}"] = entries[0].current if entries else 0
        except:
            pass

        return metrics

    def _monitor_loop(self):
        while self.running:
            try:
                metrics = self._get_system_metrics()

                with self._lock:
                    self.samples.append(metrics)
                    if len(self.samples) > self.max_samples:
                        self.samples.pop(0)

                time.sleep(self.log_interval)
            except Exception as e:
                print(f"[PERF] 监控异常: {e}")
                time.sleep(self.log_interval)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            print("[PERF] 性能监控已启动")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[PERF] 性能监控已停止")

    def get_latest_metrics(self):
        with self._lock:
            return self.samples[-1] if self.samples else None

    def get_summary(self):
        with self._lock:
            if not self.samples:
                return None

            cpu_values = [s["cpu_percent"] for s in self.samples]
            mem_values = [s["memory_percent"] for s in self.samples]

            return {
                "avg_cpu": sum(cpu_values) / len(cpu_values),
                "max_cpu": max(cpu_values),
                "min_cpu": min(cpu_values),
                "avg_memory": sum(mem_values) / len(mem_values),
                "max_memory": max(mem_values),
                "min_memory": min(mem_values),
                "sample_count": len(self.samples),
                "latest": self.samples[-1],
            }

    def save_report(self, filepath="performance_report.txt"):
        summary = self.get_summary()
        if not summary:
            return

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"=== 性能监控报告 ===\n")
            f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"采样次数: {summary['sample_count']}\n")
            f.write(f"\n--- CPU 统计 ---\n")
            f.write(f"平均: {summary['avg_cpu']:.1f}%\n")
            f.write(f"最大: {summary['max_cpu']:.1f}%\n")
            f.write(f"最小: {summary['min_cpu']:.1f}%\n")
            f.write(f"\n--- 内存统计 ---\n")
            f.write(f"平均: {summary['avg_memory']:.1f}%\n")
            f.write(f"最大: {summary['max_memory']:.1f}%\n")
            f.write(f"最小: {summary['min_memory']:.1f}%\n")
            f.write(f"\n--- 最新状态 ---\n")
            latest = summary["latest"]
            f.write(f"内存使用: {latest['memory_used_gb']:.2f}GB / {latest['memory_total_gb']:.2f}GB\n")
            f.write(f"磁盘占用: {latest['disk_usage_percent']:.1f}%\n")

        print(f"[PERF] 性能报告已保存: {filepath}")
