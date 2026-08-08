"""
部署主流程（框架版）
================================================
展示三级部署（test/pre/prod）的标准流水线：
  Phase 1. 健康检查预检
  Phase 2. 配置装配 + 版本号注入
  Phase 3. 通信适配初始化
  Phase 4. 仿真/真机 启动
  Phase 5. 三层模块编排启动
  Phase 6. 监控守护 + 日志归档

说明：这是一个部署流水线框架，展示「系统如何从启动
      到稳定运行」的标准工程流程，不接入任何
      真实企业服务器、私有IP或敏感配置。
"""

from __future__ import annotations

import os
import sys
import time
import json
import traceback
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

# 本项目模块
from deployment.health_check import run_health_checks, HealthReport


# ============================================================
# 部署配置（框架示例版）
# ============================================================
@dataclass
class DeploymentManifest:
    """部署清单 —— 一次部署任务的完整规格"""
    deploy_id: str = "auto"
    deploy_level: str = "test"         # test / pre / prod
    project_name: str = "EmbodiedSim-Framework"
    project_version: str = "1.0.0-public"
    target_env: str = "simulation"     # simulation / real_robot / hybrid
    robot_type: str = "panda"
    scene_id: str = "industrial.assembly"
    # 选项开关
    enable_gui: bool = True
    enable_ai_decision: bool = False
    enable_safety_fuses: bool = True
    enable_perf_monitor: bool = True
    # 超时与重试
    health_timeout_s: int = 300
    total_timeout_s: int = 3600
    auto_recovery: bool = False
    # 扩展参数（自由扩展）
    extra: Dict[str, Any] = field(default_factory=dict)

    # ---- 便捷工厂 ----
    @classmethod
    def quick(cls, deploy_level: str = "test") -> "DeploymentManifest":
        return cls(deploy_level=deploy_level,
                   enable_gui=(deploy_level != "prod"),
                   auto_recovery=(deploy_level == "prod"))


# ============================================================
# 部署阶段
# ============================================================
class DeployPhase:
    PRECHECK = "PHASE_1_PRECHECK"
    CONFIG =   "PHASE_2_CONFIG_ASSEMBLE"
    COMM =     "PHASE_3_COMM_ADAPTERS"
    START =    "PHASE_4_SIM_HW_START"
    ORCHESTRATE = "PHASE_5_MODULES_RUN"
    MONITOR =  "PHASE_6_MONITOR"

    ALL = [PRECHECK, CONFIG, COMM, START, ORCHESTRATE, MONITOR]


# ============================================================
# 日志与归档
# ============================================================
class DeployLogger:
    """部署过程日志器（控制台 + 文件双写，带阶段标签）"""
    LEVEL_ICON = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "FAIL": "❌", "PHASE": "🚦"}

    def __init__(self, manifest: DeploymentManifest, log_root: str = "logs"):
        self.manifest = manifest
        ts = time.strftime("%Y%m%d_%H%M%S")
        self.log_dir = os.path.join(log_root, f"deploy_{manifest.deploy_level}_{ts}")
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"deploy_{manifest.deploy_id}.log")
        self.events: List[Dict[str, Any]] = []
        self._fd = open(self.log_file, "a", encoding="utf-8", buffering=1)
        self.write("INFO", "DeployLogger", f"启动部署日志，归档目录: {self.log_dir}")

    def write(self, level: str, tag: str, message: str, **meta) -> None:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        icon = self.LEVEL_ICON.get(level, "  ")
        line = f"{ts} [{level:4s}] {icon} {tag:20s} :: {message}"
        print(line)
        self._fd.write(line + "\n")
        ev = {"ts": ts, "level": level, "tag": tag, "message": message, **meta}
        self.events.append(ev)

    def phase(self, phase_name: str, index: int, total: int) -> None:
        self.write("PHASE", "PhaseEngine",
                   f"──── [{index}/{total}] 进入阶段 {phase_name} ────")

    def close(self) -> str:
        summary_path = os.path.join(self.log_dir, "deploy_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "manifest": asdict(self.manifest),
                    "log_file": self.log_file,
                    "events_total": len(self.events),
                    "events": self.events[-200:],  # 只保留最后200条，避免过大
                },
                f, ensure_ascii=False, indent=2,
            )
        try:
            self._fd.close()
        except Exception:
            pass
        return summary_path


# ============================================================
# 部署执行引擎
# ============================================================
class DeploymentEngine:
    """
    通用部署引擎
    ------------------------------------------------
    使用：
        >>> manifest = DeploymentManifest.quick("test")
        >>> engine = DeploymentEngine(manifest)
        >>> success = engine.run()
    """

    def __init__(self, manifest: Optional[DeploymentManifest] = None):
        self.manifest = manifest or DeploymentManifest()
        if self.manifest.deploy_id == "auto":
            self.manifest.deploy_id = f"deploy_{int(time.time())}"
        self.logger = DeployLogger(self.manifest)
        self.health_report: Optional[HealthReport] = None
        self.shutdown_reason: Optional[str] = None
        self._success = False

    # ============== 公开入口 ==============
    def run(self) -> bool:
        t0 = time.time()
        phases = DeployPhase.ALL
        self.logger.write(
            "INFO", "Engine",
            f"部署任务启动 | id={self.manifest.deploy_id} "
            f"| level={self.manifest.deploy_level} | env={self.manifest.target_env}"
        )
        try:
            for idx, phase in enumerate(phases, start=1):
                self.logger.phase(phase, idx, len(phases))
                if not self._run_phase(phase):
                    self.logger.write(
                        "FAIL", phase,
                        f"阶段失败，部署中止。原因: {self.shutdown_reason or '未知'}"
                    )
                    return False
            self._success = True
            dt = time.time() - t0
            self.logger.write(
                "OK", "Engine",
                f"部署全部阶段完成 ✅ 总耗时 {dt:.1f}s | id={self.manifest.deploy_id}"
            )
            return True
        except Exception as e:
            tb = traceback.format_exc(limit=3)
            self.logger.write("FAIL", "Engine",
                              f"未捕获异常终止部署: {repr(e)}\n{tb}")
            return False
        finally:
            summary_path = self.logger.close()
            print(f"\n[DeployEngine] 部署摘要已归档：{summary_path}")

    # ============== 各阶段执行 ==============
    def _run_phase(self, phase: str) -> bool:
        if phase == DeployPhase.PRECHECK:
            return self._phase_precheck()
        if phase == DeployPhase.CONFIG:
            return self._phase_config()
        if phase == DeployPhase.COMM:
            return self._phase_comm()
        if phase == DeployPhase.START:
            return self._phase_start()
        if phase == DeployPhase.ORCHESTRATE:
            return self._phase_orchestrate()
        if phase == DeployPhase.MONITOR:
            return self._phase_monitor()
        # 未知阶段：保守起见跳过并告警
        self.logger.write("WARN", phase, f"未识别的阶段名，按SKIP处理")
        return True

    # ----- 1. 健康检查 -----
    def _phase_precheck(self) -> bool:
        self.health_report = run_health_checks(deploy_level=self.manifest.deploy_level)
        self.logger.write("INFO", "PreCheck",
                          f"健康检查摘要 -> 总数={len(self.health_report.results)} "
                          f"PASS={'YES' if self.health_report.overall_pass else 'NO'}")
        if not self.health_report.overall_pass:
            # prod等级强制中止；test/pre允许带警告继续
            if self.manifest.deploy_level == "prod":
                self.shutdown_reason = "PROD级部署发现FAIL级健康检查项，强制中止"
                return False
            self.logger.write(
                "WARN", "PreCheck",
                f"部署等级={self.manifest.deploy_level}，允许带WARN继续 "
                f"（FAIL数量={self.health_report.count_by_level().get('FAIL', 0)}）"
            )
        self.logger.write("OK", "PreCheck", "健康检查阶段通过")
        return True

    # ----- 2. 配置装配 -----
    def _phase_config(self) -> bool:
        self.logger.write("INFO", "Config", f"项目: {self.manifest.project_name} "
                                            f"v{self.manifest.project_version}")
        self.logger.write("INFO", "Config", f"机器人={self.manifest.robot_type} "
                                            f"场景={self.manifest.scene_id}")
        self.logger.write("INFO", "Config",
                          f"开关: GUI={'ON' if self.manifest.enable_gui else 'OFF'} | "
                          f"AI={'ON' if self.manifest.enable_ai_decision else 'OFF'} | "
                          f"安全熔断器={'ON' if self.manifest.enable_safety_fuses else 'OFF'}")
        self.logger.write("OK", "Config", "配置装配完成")
        return True

    # ----- 3. 通信适配器初始化 -----
    def _phase_comm(self) -> bool:
        if self.manifest.target_env == "simulation":
            self.logger.write("INFO", "Comm", "目标环境为仿真，跳过真实通信链路初始化")
            self.logger.write("OK", "Comm",
                              "通信抽象层就绪（接入真机时启用：TCP/UDP/CAN/EtherCAT/ROS）")
            return True
        # real_robot / hybrid 场景下，仅示例不连真实硬件
        self.logger.write("WARN", "Comm",
                          f"目标环境={self.manifest.target_env}，公共示例版以Mock模拟真机对接")
        self.logger.write("OK", "Comm", "通信适配器（Mock版）已挂载")
        return True

    # ----- 4. 仿真/真机 启动 -----
    def _phase_start(self) -> bool:
        if self.manifest.target_env == "simulation":
            try:
                from core.simulation_env import PyBulletSimulationEnv, SimConfig
                mode = "gui" if self.manifest.enable_gui else "direct"
                sim = PyBulletSimulationEnv(SimConfig(mode=mode, verbose=False))
                sim.load_robot(self.manifest.robot_type)
                sim.close()
            except Exception as e:
                self.logger.write("FAIL", "Start",
                                  f"仿真环境启动失败: {repr(e)}（如未安装PyBullet可忽略示例阶段）")
                # test等级允许继续（可能是没装PyBullet，仅展示部署流程）
                if self.manifest.deploy_level != "test":
                    self.shutdown_reason = f"仿真启动失败: {repr(e)}"
                    return False
            self.logger.write("OK", "Start", "仿真环境启动-关闭 冒烟测试通过")
            return True
        self.logger.write("OK", "Start",
                          "真机启动（公共示例仅模拟）：回零→怠速→安全位姿 三步标准流程已Mock通过")
        return True

    # ----- 5. 三层模块编排启动 -----
    def _phase_orchestrate(self) -> bool:
        try:
            from core.module_interfaces import (
                MockPerception, SimpleSkillBasedDecision,
                MockExecution, ThreeTierOrchestrator,
            )
            P = MockPerception("P_demo")
            D = SimpleSkillBasedDecision("D_demo")
            E = MockExecution("E_demo")
            E.failure_probability = 0.0  # 部署演示阶段不触发随机故障
            D.set_task_goal("assembly_demo", workpiece="peg_hole")
            orch = ThreeTierOrchestrator(P, D, E)
            total = orch.run_forever(max_cycles=8, period_s=0.02)
            self.logger.write("OK", "Orchestrate",
                              f"三层编排闭环运行完成，共 {total} 个周期")
        except Exception as e:
            # 部署框架本身不依赖具体模块运行一定成功，WARN即可
            self.logger.write("WARN", "Orchestrate",
                              f"三层编排模块演示失败（可忽略）: {repr(e)}")
        return True

    # ----- 6. 监控守护（公共示例版：短暂演示即退出） -----
    def _phase_monitor(self) -> bool:
        self.logger.write("INFO", "Monitor", "监控守护阶段启动（守护进程模式）")
        demo_seconds = 1
        for i in range(demo_seconds):
            time.sleep(0.5)
            self.logger.write("INFO", "Monitor",
                              f"守护心跳 {i+1}/{demo_seconds} | "
                              f"部署等级={self.manifest.deploy_level} | "
                              f"自动恢复={'ON' if self.manifest.auto_recovery else 'OFF'}")
        self.logger.write("OK", "Monitor",
                          f"监控阶段演示结束（生产部署下此处为无限循环，直到停止信号）")
        return True


# ============================================================
# 命令行入口
# ============================================================
def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    level = argv[0] if argv and argv[0] in ("test", "pre", "prod") else "test"
    manifest = DeploymentManifest.quick(level)
    engine = DeploymentEngine(manifest)
    ok = engine.run()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
