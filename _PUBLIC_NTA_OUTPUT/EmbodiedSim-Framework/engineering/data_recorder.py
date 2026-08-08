"""
数据记录与回放系统 + 性能监控模块
================================================
1) DataRecorder：
   把「仿真/真机运行时」的结构化数据（关节状态、决策、事件、
   安全事件）按时间序列写入到 CSV / JSONL 文件，便于事后分析。

2) PerformanceMonitor：
   实时监控 CPU / 内存 / GPU(可选) / 控制环频率 / 延迟抖动
   等工程级指标，支持阈值告警回调。

说明：本文件为通用工程工具实现，不包含任何品牌参数。
"""

from __future__ import annotations

import csv
import json
import os
import time
import threading
import gc
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


# ============================================================
# 1. 数据记录器
# ============================================================
@dataclass
class DataRecord:
    """单条数据记录（统一信封）"""
    timestamp_s: float
    record_type: str               # joint_state / ee_pose / decision / safety / custom
    source: str
    sequence: int = 0
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_row(self) -> Dict[str, Any]:
        return {
            "timestamp_s": f"{self.timestamp_s:.6f}",
            "record_type": self.record_type,
            "source": self.source,
            "sequence": self.sequence,
            "payload_json": json.dumps(self.payload, ensure_ascii=False, sort_keys=True),
        }


class DataRecorder:
    """
    通用数据记录器（CSV + JSONL 双写，自带缓冲与后台刷盘）
    ------------------------------------------------
    用法：
        >>> rec = DataRecorder("./data_records/demo_01")
        >>> rec.start()
        >>> rec.put_joint_state([0.1]*7, source="panda_arm")
        >>> rec.put("custom", {"any": "data"}, source="my_module")
        >>> rec.stop_and_close()  # 返回归档路径
    """

    def __init__(self, output_prefix: str, flush_every: int = 100):
        self.output_prefix = output_prefix
        self.flush_every = flush_every
        os.makedirs(os.path.dirname(os.path.abspath(output_prefix)), exist_ok=True)
        self._csv_path = output_prefix + ".csv"
        self._jsonl_path = output_prefix + ".jsonl"
        # 打开文件句柄（写时创建）
        self._csv_f = open(self._csv_path, "w", encoding="utf-8", newline="", buffering=1)
        self._jsonl_f = open(self._jsonl_path, "w", encoding="utf-8", buffering=1)
        self._csv_writer = csv.DictWriter(
            self._csv_f,
            fieldnames=["timestamp_s", "record_type", "source",
                        "sequence", "payload_json"],
        )
        self._csv_writer.writeheader()
        self._seq_counter = 0
        self._buffer: List[DataRecord] = []
        self._buffer_lock = threading.Lock()
        self._running = False
        self._bg_thread: Optional[threading.Thread] = None
        self._dropped_count = 0
        self._written_count = 0
        self._created_at = time.time()

    # ---- 生命周期 ----
    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._bg_thread = threading.Thread(target=self._flush_loop,
                                           name="DataRecorderBG", daemon=True)
        self._bg_thread.start()

    def stop_and_close(self) -> Dict[str, Any]:
        self._running = False
        if self._bg_thread is not None:
            self._bg_thread.join(timeout=3.0)
        # 最后一次刷缓冲
        with self._buffer_lock:
            buf = list(self._buffer)
            self._buffer.clear()
        self._flush_to_disk(buf)
        try:
            self._csv_f.close()
            self._jsonl_f.close()
        except Exception:
            pass
        return {
            "csv_file": self._csv_path,
            "jsonl_file": self._jsonl_path,
            "written_records": self._written_count,
            "dropped_records": self._dropped_count,
            "duration_s": round(time.time() - self._created_at, 3),
            "csv_size_bytes": os.path.getsize(self._csv_path),
            "jsonl_size_bytes": os.path.getsize(self._jsonl_path),
        }

    # ---- 写入接口 ----
    def put(self, record_type: str, payload: Dict[str, Any], source: str = "") -> None:
        rec = DataRecord(
            timestamp_s=time.time(),
            record_type=record_type, source=source or self.__class__.__name__,
            sequence=self._seq_counter, payload=dict(payload),
        )
        self._seq_counter += 1
        with self._buffer_lock:
            # 防止无限增长：超过100000条时丢弃最旧（极端保护）
            if len(self._buffer) >= 100000:
                self._buffer.pop(0)
                self._dropped_count += 1
            self._buffer.append(rec)

    def put_joint_state(self, positions: List[float], velocities: Optional[List[float]] = None,
                        torques: Optional[List[float]] = None, source: str = "robot") -> None:
        payload = {"positions": list(positions)}
        if velocities is not None:
            payload["velocities"] = list(velocities)
        if torques is not None:
            payload["torques"] = list(torques)
        self.put("joint_state", payload, source=source)

    def put_ee_pose(self, xyz: List[float], quat: Optional[List[float]] = None,
                    source: str = "robot") -> None:
        payload = {"xyz": list(xyz)}
        if quat is not None:
            payload["quat"] = list(quat)
        self.put("ee_pose", payload, source=source)

    def put_decision(self, skill: str, status: str, meta: Optional[Dict[str, Any]] = None,
                     source: str = "decision") -> None:
        self.put("decision", {"skill": skill, "status": status, **(meta or {})},
                 source=source)

    def put_safety_event(self, event_type: str, severity: str, message: str,
                         source: str = "safety") -> None:
        self.put("safety", {"event_type": event_type, "severity": severity,
                            "message": message}, source=source)

    # ---- 后台刷写 ----
    def _flush_loop(self) -> None:
        while self._running:
            time.sleep(0.1)
            with self._buffer_lock:
                if len(self._buffer) < self.flush_every:
                    continue
                buf = list(self._buffer)
                self._buffer.clear()
            self._flush_to_disk(buf)
        # 退出前再刷一次残余
        with self._buffer_lock:
            if self._buffer:
                buf = list(self._buffer)
                self._buffer.clear()
                self._flush_to_disk(buf)

    def _flush_to_disk(self, records: List[DataRecord]) -> None:
        if not records:
            return
        for r in records:
            row = r.to_row()
            self._csv_writer.writerow(row)
            self._jsonl_f.write(json.dumps(row, ensure_ascii=False) + "\n")
        self._written_count += len(records)


# ============================================================
# 2. 性能监控器
# ============================================================
@dataclass
class PerfThresholds:
    cpu_percent: float = 85.0
    memory_percent: float = 85.0
    disk_percent: float = 90.0
    control_hz_min: float = 100.0     # 控制环频率下限
    latency_ms_max: float = 20.0      # 决策-执行延迟上限


@dataclass
class PerfSnapshot:
    timestamp_s: float
    cpu_percent: float
    memory_percent: float
    memory_used_gb: float
    disk_percent: float
    process_rss_mb: float
    thread_count: int
    gc_objects: int
    control_hz: float = 0.0
    avg_latency_ms: float = 0.0


class PerformanceMonitor:
    """
    工程级性能监控器（阈值告警+定期采样+日志回调）
    ------------------------------------------------
    用法：
        >>> mon = PerformanceMonitor(interval_s=1.0)
        >>> mon.on_alert(lambda s, msg: print("ALERT:", msg))
        >>> mon.start()
        >>> time.sleep(5)
        >>> mon.stop()
        >>> for snap in mon.history[-3:]: print(snap)
    """

    def __init__(self, interval_s: float = 1.0,
                 thresholds: Optional[PerfThresholds] = None,
                 path_to_monitor: str = "."):
        if not HAS_PSUTIL:
            raise ImportError("psutil未安装：pip install psutil")
        self.interval_s = max(0.1, float(interval_s))
        self.th = thresholds or PerfThresholds()
        self.path = path_to_monitor
        self._proc = psutil.Process(os.getpid())
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self.history: List[PerfSnapshot] = []
        self._alert_callbacks: List[Callable[[PerfSnapshot, str], None]] = []
        self._custom_metrics: Dict[str, float] = {}
        self._control_timestamps: List[float] = []

    # ---- 配置 ----
    def on_alert(self, cb: Callable[[PerfSnapshot, str], None]) -> None:
        self._alert_callbacks.append(cb)

    def set_control_hz_hint(self, name: str = "default") -> None:
        """在控制循环结束时调用一次，用于统计控制频率"""
        self._control_timestamps.append(time.time())
        self._control_timestamps = self._control_timestamps[-500:]

    def record_latency_ms(self, latency_ms: float) -> None:
        # 简单滑窗平均
        key = "_latency_ms_samples"
        lst: List[float] = self._custom_metrics.setdefault(key, [])  # type: ignore[arg-type]
        lst.append(float(latency_ms))
        self._custom_metrics[key] = lst[-500:]  # type: ignore[assignment]

    # ---- 生命周期 ----
    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, name="PerfMonitor",
                                        daemon=True)
        self._thread.start()

    def stop(self) -> List[PerfSnapshot]:
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        return list(self.history)

    # ---- 核心循环 ----
    def _sample(self) -> PerfSnapshot:
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage(self.path)
        try:
            cpu_percent = self._proc.cpu_percent(interval=0.0)
            # 第一次调用cpu_percent可能返回0，我们再用全局兜底
            if cpu_percent <= 0.01:
                cpu_percent = psutil.cpu_percent(interval=0.0)
        except Exception:
            cpu_percent = float(psutil.cpu_percent(interval=None))
        rss_mb = self._proc.memory_info().rss / (1024 ** 2)
        # 控制频率
        hz = 0.0
        if len(self._control_timestamps) >= 2:
            dt = self._control_timestamps[-1] - self._control_timestamps[0]
            if dt > 0:
                hz = (len(self._control_timestamps) - 1) / dt
        # 延迟均值
        lat_samples: List[float] = self._custom_metrics.get("_latency_ms_samples", [])  # type: ignore[assignment]
        avg_lat = sum(lat_samples) / len(lat_samples) if lat_samples else 0.0
        return PerfSnapshot(
            timestamp_s=time.time(),
            cpu_percent=round(cpu_percent, 2),
            memory_percent=round(mem.percent, 2),
            memory_used_gb=round((mem.total - mem.available) / (1024 ** 3), 3),
            disk_percent=round(disk.percent, 2),
            process_rss_mb=round(rss_mb, 2),
            thread_count=self._proc.num_threads(),
            gc_objects=len(gc.get_objects()),
            control_hz=round(hz, 2),
            avg_latency_ms=round(avg_lat, 3),
        )

    def _check_thresholds(self, s: PerfSnapshot) -> List[str]:
        alerts: List[str] = []
        if s.cpu_percent > self.th.cpu_percent:
            alerts.append(f"CPU使用率 {s.cpu_percent}% > 阈值 {self.th.cpu_percent}%")
        if s.memory_percent > self.th.memory_percent:
            alerts.append(f"内存使用率 {s.memory_percent}% > 阈值 {self.th.memory_percent}%")
        if s.disk_percent > self.th.disk_percent:
            alerts.append(f"磁盘使用率 {s.disk_percent}% > 阈值 {self.th.disk_percent}%")
        if s.control_hz > 0 and s.control_hz < self.th.control_hz_min:
            alerts.append(f"控制环频率 {s.control_hz:.2f}Hz < 下限 {self.th.control_hz_min}Hz")
        if s.avg_latency_ms > self.th.latency_ms_max:
            alerts.append(f"决策-执行延迟 {s.avg_latency_ms:.2f}ms > 上限 {self.th.latency_ms_max}ms")
        return alerts

    def _loop(self) -> None:
        # 预热一次cpu_percent
        try:
            self._proc.cpu_percent(interval=0.0)
        except Exception:
            pass
        while self._running:
            snap = self._sample()
            self.history.append(snap)
            if len(self.history) > 7200:  # 2小时×3600s/interval，上限
                self.history = self.history[-7200:]
            alerts = self._check_thresholds(snap)
            if alerts and self._alert_callbacks:
                msg = " | ".join(alerts)
                for cb in list(self._alert_callbacks):
                    try:
                        cb(snap, msg)
                    except Exception:
                        pass
            time.sleep(self.interval_s)

    # ---- 汇总报表 ----
    def report(self) -> Dict[str, Any]:
        if not self.history:
            return {"samples": 0}
        h = self.history
        def _avg(lst): return sum(lst) / len(lst) if lst else 0.0
        def _p95(lst):
            s = sorted(lst)
            return s[min(len(s)-1, int(len(s)*0.95))] if s else 0.0
        return {
            "samples": len(h),
            "duration_s": round(h[-1].timestamp_s - h[0].timestamp_s, 3),
            "cpu": {
                "avg_percent": round(_avg([s.cpu_percent for s in h]), 2),
                "p95_percent": round(_p95([s.cpu_percent for s in h]), 2),
            },
            "memory": {
                "avg_percent": round(_avg([s.memory_percent for s in h]), 2),
                "avg_used_gb": round(_avg([s.memory_used_gb for s in h]), 3),
                "avg_process_rss_mb": round(_avg([s.process_rss_mb for s in h]), 2),
            },
            "disk": {"avg_percent": round(_avg([s.disk_percent for s in h]), 2)},
            "control_loop": {
                "avg_hz": round(_avg([s.control_hz for s in h if s.control_hz]), 2),
                "avg_latency_ms": round(_avg([s.avg_latency_ms for s in h]), 3),
            },
            "threads_avg": round(_avg([s.thread_count for s in h]), 1),
            "gc_objects_avg": int(_avg([s.gc_objects for s in h])),
        }
