# ============================================================================
# 具身智能机器人系统 - 健康检查
# 提供系统运行状态监控接口
# ============================================================================

import os
import sys
import time
import threading
from typing import Dict, Any, List
from datetime import datetime

from settings import get_all_config, SIMULATION_CONFIG, SAFETY_CONFIG


class HealthChecker:
    """系统健康检查器"""

    def __init__(self):
        self._start_time = time.time()
        self._checks: Dict[str, bool] = {}
        self._lock = threading.Lock()

    def get_uptime(self) -> float:
        """获取系统运行时间（秒）"""
        return time.time() - self._start_time

    def get_uptime_human(self) -> str:
        """获取人类可读的运行时间"""
        seconds = self.get_uptime()
        days, remainder = divmod(int(seconds), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, secs = divmod(remainder, 60)
        parts = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0:
            parts.append(f"{hours}小时")
        if minutes > 0:
            parts.append(f"{minutes}分钟")
        parts.append(f"{secs}秒")
        return " ".join(parts)

    def check_python_version(self) -> bool:
        """检查Python版本"""
        return sys.version_info >= (3, 9)

    def check_dependencies(self) -> Dict[str, bool]:
        """检查关键依赖是否可用"""
        deps = {
            "numpy": False,
            "pybullet": False,
        }
        try:
            import numpy  # noqa: F401
            deps["numpy"] = True
        except ImportError:
            pass
        try:
            import pybullet  # noqa: F401
            deps["pybullet"] = True
        except ImportError:
            pass
        return deps

    def check_disk_space(self, min_gb: float = 1.0) -> bool:
        """检查磁盘空间（GB）"""
        try:
            stat = os.statvfs(os.getcwd())
            free_gb = (stat.f_frsize * stat.f_bavail) / (1024 ** 3)
            return free_gb >= min_gb
        except Exception:
            return True

    def check_memory(self, min_mb: float = 512.0) -> bool:
        """检查可用内存（MB）"""
        try:
            import psutil
            mem = psutil.virtual_memory()
            return mem.available >= min_mb * 1024 * 1024
        except ImportError:
            return True

    def run_all_checks(self) -> Dict[str, Any]:
        """运行所有健康检查"""
        with self._lock:
            deps = self.check_dependencies()
            checks = {
                "python_version": self.check_python_version(),
                "disk_space_ok": self.check_disk_space(),
                "memory_ok": self.check_memory(),
                **{f"dep_{k}": v for k, v in deps.items()},
            }
            overall = all(checks.values())

            return {
                "status": "healthy" if overall else "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": round(self.get_uptime(), 2),
                "uptime_human": self.get_uptime_human(),
                "overall_ok": overall,
                "checks": checks,
                "config_summary": {
                    "sim_render": SIMULATION_CONFIG.get("render_mode"),
                    "safety_torque_ratio": SAFETY_CONFIG.get("joint_torque_warning_ratio"),
                },
            }


# 全局健康检查器实例
health_checker = HealthChecker()


def health_check_handler() -> Dict[str, Any]:
    """健康检查处理函数（可直接用于Web框架）"""
    return health_checker.run_all_checks()


if __name__ == "__main__":
    result = health_check_handler()
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
