"""
三级健康检查框架（工程部署标准）
================================================
提供 8 大类健康检查项，覆盖：
  1. 系统环境（OS/CPU/内存/磁盘/Python版本）
  2. 配置文件（语法/必填项/范围校验）
  3. 安全防护（紧急停止/碰撞检测/输入校验/日志审计）
  4. 通信链路（TCP/UDP/CAN/EtherCAT/ROS端口可达）
  5. 模型与算法接入（SDK连通性/延迟）
  6. 数据与文件（目录权限/磁盘剩余/输入数据完整性）
  7. 性能指标（CPU/内存/响应延迟）
  8. 真机对接（可选：关节回零/末端示教点位）

说明：本框架不包含任何真实企业私有IP或端口，
      以接口方式展示工程部署层的健康检查设计模式。
"""

from __future__ import annotations

import os
import sys
import time
import socket
import platform
import psutil
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Optional, Tuple


# ============================================================
# 检查结果与级别
# ============================================================
class CheckLevel:
    OK = "OK"           # ✅  通过
    WARN = "WARN"       # ⚠️  警告（允许通过，但需注意）
    FAIL = "FAIL"       # ❌  失败（部署应中止）
    SKIP = "SKIP"       # ➖  跳过（条件不满足，非必需）


@dataclass
class CheckResult:
    """单项检查结果"""
    check_id: str
    name: str
    category: str
    level: str
    message: str
    duration_ms: int = 0
    details: Dict[str, Any] = field(default_factory=dict)

    def short(self) -> str:
        icon = {"OK": "✅", "WARN": "⚠️", "FAIL": "❌", "SKIP": "➖"}.get(self.level, "?")
        return f"{icon} [{self.level:4s}] {self.check_id:24s} {self.name} — {self.message}"

    @property
    def is_ok(self) -> bool:
        return self.level in (CheckLevel.OK, CheckLevel.SKIP)


# ============================================================
# 健康检查项注册表
# ============================================================
CheckFn = Callable[[], CheckResult]


class HealthChecker:
    """
    通用健康检查器
    ------------------------------------------------
    使用：
        >>> checker = HealthChecker(level="test")
        >>> checker.register_default_checks()
        >>> report = checker.run_all()
        >>> print(report.summary())
    """

    CATEGORY_PRIORITY = [
        "system_environment",   # 1. 系统环境
        "configuration",        # 2. 配置
        "safety_protection",    # 3. 安全
        "communication",        # 4. 通信
        "ai_models",            # 5. AI/模型接入
        "data_files",           # 6. 数据
        "performance",          # 7. 性能
        "robot_hardware",       # 8. 真机（可选）
    ]

    def __init__(self, deploy_level: str = "test"):
        if deploy_level not in ("test", "pre", "prod"):
            raise ValueError("deploy_level 必须是 test / pre / prod")
        self.deploy_level = deploy_level
        self._checks: List[Tuple[str, CheckFn]] = []   # (category, fn)
        self._results: List[CheckResult] = []

    # ============== 注册检查项 ==============
    def add(self, category: str, check_fn: CheckFn) -> None:
        self._checks.append((category, check_fn))

    def register_default_checks(self) -> None:
        """注册 8 大类 默认检查项（公共示例版）"""
        # ---- 1. 系统环境 ----
        self.add("system_environment", self._check_os)
        self.add("system_environment", self._check_python_version)
        self.add("system_environment", self._check_memory_min)
        self.add("system_environment", self._check_disk_min)

        # ---- 2. 配置 ----
        self.add("configuration", self._check_env_example_exists)
        self.add("configuration", self._check_requirements_available)

        # ---- 3. 安全 ----
        self.add("safety_protection", self._check_emergency_stop_flag)
        self.add("safety_protection", self._check_log_dir_writable)

        # ---- 4. 通信 ----
        self.add("communication", self._check_network_basic)
        # 真机/具体端口在test/pre/prod下以"SKIP"为例展示（不连真实IP）

        # ---- 5. AI接入 ----
        self.add("ai_models", self._check_llm_env_key_present)

        # ---- 6. 数据 ----
        self.add("data_files", self._check_project_dir_readable)

        # ---- 7. 性能 ----
        self.add("performance", self._check_cpu_load_ok)

        # ---- 8. 真机（默认SKIP：公共示例无真机） ----
        self.add("robot_hardware", self._check_robot_hardware_skipped)

    # ============== 具体检查实现 ==============
    def _mk_result(self, check_id: str, name: str, category: str,
                   level: str, message: str, **details) -> CheckResult:
        return CheckResult(check_id=check_id, name=name, category=category,
                           level=level, message=message, details=details)

    # ---- 1. 系统环境 ----
    def _check_os(self) -> CheckResult:
        system = platform.system()
        release = platform.release()
        return self._mk_result(
            "SYS_OS", f"操作系统({system})", "system_environment",
            CheckLevel.OK, f"{system} {release} 符合部署要求",
            system=system, release=release, arch=platform.machine(),
        )

    def _check_python_version(self) -> CheckResult:
        vi = sys.version_info
        ok = (vi.major == 3 and vi.minor >= 10)
        msg = f"Python {vi.major}.{vi.minor}.{vi.micro}"
        if ok:
            level = CheckLevel.OK
            msg += "（≥3.10 满足推荐版本）"
        else:
            level = CheckLevel.WARN
            msg += "（推荐升级到 3.10+ 以获得最佳兼容性）"
        return self._mk_result("SYS_PYTHON", "Python版本", "system_environment",
                               level, msg, version=f"{vi.major}.{vi.minor}.{vi.micro}")

    def _check_memory_min(self, min_gb: float = 4.0) -> CheckResult:
        mem = psutil.virtual_memory()
        total_gb = mem.total / (1024 ** 3)
        level = CheckLevel.OK if total_gb >= min_gb else CheckLevel.WARN
        return self._mk_result(
            "SYS_MEMORY", "系统内存", "system_environment", level,
            f"总内存 {total_gb:.1f}GB / 可用 {mem.available/(1024**3):.1f}GB "
            f"（最低要求 ≥{min_gb}GB）",
            total_gb=round(total_gb, 2), available_gb=round(mem.available/(1024**3), 2),
        )

    def _check_disk_min(self, min_gb: float = 5.0) -> CheckResult:
        usage = psutil.disk_usage(os.path.abspath("."))
        free_gb = usage.free / (1024 ** 3)
        level = CheckLevel.OK if free_gb >= min_gb else CheckLevel.WARN
        return self._mk_result(
            "SYS_DISK", "磁盘可用空间", "system_environment", level,
            f"剩余 {free_gb:.1f}GB / 总 {usage.total/(1024**3):.1f}GB（≥{min_gb}GB）",
            free_gb=round(free_gb, 2), total_gb=round(usage.total/(1024**3), 2),
        )

    # ---- 2. 配置 ----
    def _check_env_example_exists(self) -> CheckResult:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            ".env.example")
        exists = os.path.isfile(path)
        return self._mk_result(
            "CFG_ENV_EXAMPLE", "环境变量模板文件", "configuration",
            CheckLevel.OK if exists else CheckLevel.WARN,
            "存在" if exists else "未找到 .env.example（建议补充）",
            path=path,
        )

    def _check_requirements_available(self) -> CheckResult:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "requirements.txt")
        exists = os.path.isfile(path)
        return self._mk_result(
            "CFG_REQUIREMENTS", "依赖清单文件", "configuration",
            CheckLevel.OK if exists else CheckLevel.FAIL,
            "存在" if exists else "缺少 requirements.txt（部署依赖）",
            path=path,
        )

    # ---- 3. 安全 ----
    def _check_emergency_stop_flag(self) -> CheckResult:
        # 公共示例版：以配置标志位示意（不接入真实急停硬件）
        enabled = True  # 示例：默认启用
        return self._mk_result(
            "SAFE_ESTOP", "紧急停止功能", "safety_protection",
            CheckLevel.OK if enabled else CheckLevel.FAIL,
            "已启用（框架级别：接入硬件时将对接真实IO）" if enabled else "已禁用，存在安全风险",
            emergency_stop_enabled=enabled,
        )

    def _check_log_dir_writable(self) -> CheckResult:
        log_dir = os.path.join(os.getcwd(), "logs")
        try:
            os.makedirs(log_dir, exist_ok=True)
            tmp = os.path.join(log_dir, ".health_write_test")
            with open(tmp, "w") as f:
                f.write("ok")
            os.remove(tmp)
            level, msg = CheckLevel.OK, f"可写（目录：{log_dir}）"
        except Exception as e:
            level, msg = CheckLevel.FAIL, f"日志目录不可写: {e}"
        return self._mk_result("SAFE_LOG_DIR", "日志目录可写性", "safety_protection",
                               level, msg, dir=log_dir)

    # ---- 4. 通信 ----
    def _check_network_basic(self) -> CheckResult:
        try:
            s = socket.create_connection(("8.8.8.8", 53), timeout=2)
            s.close()
            level, msg = CheckLevel.OK, "基础网络连通（DNS示例：8.8.8.8:53）"
        except socket.error as e:
            level, msg = CheckLevel.WARN, f"无外网或DNS不通（离线部署可忽略）: {e}"
        return self._mk_result("NET_BASIC", "基础网络连通性", "communication",
                               level, msg)

    # ---- 5. AI接入 ----
    def _check_llm_env_key_present(self) -> CheckResult:
        # 公共示例：只检查是否存在 .env 或模板里定义了相关字段（不校验真实值）
        env_path = os.path.join(os.getcwd(), ".env")
        if not os.path.isfile(env_path):
            return self._mk_result(
                "AI_LLM_KEY", "大模型API Key配置", "ai_models", CheckLevel.SKIP,
                "未检测到 .env 文件（可选功能：需要启用AI决策时配置）"
            )
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()
            has_key = any(k in content for k in ("API_KEY", "api_key", "DASHSCOPE", "OPENAI"))
        except Exception as e:
            return self._mk_result("AI_LLM_KEY", "大模型API Key配置", "ai_models",
                                   CheckLevel.WARN, f".env文件读取失败: {e}")
        return self._mk_result(
            "AI_LLM_KEY", "大模型API Key配置", "ai_models",
            CheckLevel.OK if has_key else CheckLevel.SKIP,
            "已配置" if has_key else "未配置（可选，纯仿真场景下不强制）",
        )

    # ---- 6. 数据 ----
    def _check_project_dir_readable(self) -> CheckResult:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ok = os.access(root, os.R_OK)
        return self._mk_result(
            "DATA_ROOT_RD", "项目根目录可读", "data_files",
            CheckLevel.OK if ok else CheckLevel.FAIL,
            f"{'可读' if ok else '不可读'}: {root}",
            project_root=root,
        )

    # ---- 7. 性能 ----
    def _check_cpu_load_ok(self, max_percent: float = 85.0) -> CheckResult:
        load = psutil.cpu_percent(interval=0.2)
        level = CheckLevel.OK if load < max_percent else CheckLevel.WARN
        return self._mk_result(
            "PERF_CPU", "CPU使用率", "performance", level,
            f"当前 {load:.1f}%（阈值 <{max_percent}%）",
            cpu_percent=round(load, 2),
        )

    # ---- 8. 真机（公共示例跳过） ----
    def _check_robot_hardware_skipped(self) -> CheckResult:
        return self._mk_result(
            "HW_ROBOT", "真机硬件对接检查", "robot_hardware",
            CheckLevel.SKIP,
            "公共示例版本默认跳过真机对接（接入真机后可在此启用：关节回零/末端示教/急停IO）",
            deploy_level=self.deploy_level,
        )

    # ============== 执行 ==============
    def run_all(self) -> "HealthReport":
        self._results = []
        # 按类别优先级排序
        ordered = sorted(self._checks,
                         key=lambda t: self.CATEGORY_PRIORITY.index(t[0])
                         if t[0] in self.CATEGORY_PRIORITY else 99)
        for category, fn in ordered:
            t0 = time.time()
            try:
                r = fn()
            except Exception as e:
                r = CheckResult(
                    check_id="EXC_" + fn.__name__, name=fn.__name__,
                    category=category, level=CheckLevel.FAIL,
                    message=f"检查函数执行异常: {repr(e)}",
                )
            r.duration_ms = int((time.time() - t0) * 1000)
            r.category = category  # 兜底
            self._results.append(r)
        return HealthReport(self.deploy_level, list(self._results))


# ============================================================
# 健康检查报告（输出友好）
# ============================================================
class HealthReport:
    def __init__(self, deploy_level: str, results: List[CheckResult]):
        self.deploy_level = deploy_level
        self.results = results
        self.generated_at = time.time()

    def count_by_level(self) -> Dict[str, int]:
        c: Dict[str, int] = {CheckLevel.OK: 0, CheckLevel.WARN: 0,
                             CheckLevel.FAIL: 0, CheckLevel.SKIP: 0}
        for r in self.results:
            c[r.level] = c.get(r.level, 0) + 1
        return c

    @property
    def overall_pass(self) -> bool:
        c = self.count_by_level()
        return c.get(CheckLevel.FAIL, 0) == 0

    def summary(self) -> str:
        c = self.count_by_level()
        total = len(self.results)
        status = "✅ PASS" if self.overall_pass else "❌ FAIL"
        lines = []
        lines.append(f"╔══════════════════════════════════════════════════╗")
        lines.append(f"║  健康检查报告 | 部署等级: {self.deploy_level.upper():4s}        结果: {status:7s} ║")
        lines.append(f"╠══════════════════════════════════════════════════╣")
        lines.append(f"║  总数: {total:3d}  "
                     f"✅ 通过:{c[CheckLevel.OK]:3d}   "
                     f"⚠️ 警告:{c[CheckLevel.WARN]:3d}   "
                     f"❌ 失败:{c[CheckLevel.FAIL]:3d}   "
                     f"➖ 跳过:{c[CheckLevel.SKIP]:3d} ║")
        lines.append(f"╠══════════════════════════════════════════════════╣")
        current_cat = None
        for r in self.results:
            if r.category != current_cat:
                current_cat = r.category
                lines.append(f"║ ── {current_cat:44s} ── ║")
            lines.append(f"║  {r.short():76s} ║")
        lines.append(f"╚══════════════════════════════════════════════════╝")
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "deploy_level": self.deploy_level,
            "overall_pass": self.overall_pass,
            "counts": self.count_by_level(),
            "generated_at": self.generated_at,
            "results": [r.__dict__ for r in self.results],
        }


# ============================================================
# 快速运行入口
# ============================================================
def run_health_checks(deploy_level: str = "test") -> HealthReport:
    checker = HealthChecker(deploy_level=deploy_level)
    checker.register_default_checks()
    return checker.run_all()


if __name__ == "__main__":
    report = run_health_checks(deploy_level="test")
    print(report.summary())
    sys.exit(0 if report.overall_pass else 1)
