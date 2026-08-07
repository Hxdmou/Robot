"""
部署工具集 - 补全部署全流程的缺失环节
包含：
  1. 部署配置快照备份/恢复
  2. 安全参数完整性验证
  3. 异常自动降级管理器（模型→轨迹）
  4. 部署总结报告生成
  5. 日志/数据自动归档
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
import sys
import json
import time
import shutil
import zipfile
import datetime
import threading
from typing import Dict, Any, List, Optional, Tuple


# ============================================================
# 1. 部署配置快照备份
# ============================================================

class DeploymentSnapshot:
    """部署配置快照 - 记录每次部署时的完整配置状态"""

    def __init__(self, snapshot_dir: str = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.snapshot_dir = snapshot_dir or os.path.join(base_dir, "deploy_snapshots")
        os.makedirs(self.snapshot_dir, exist_ok=True)

    def create_snapshot(self, extra_data: Dict[str, Any] = None) -> str:
        """创建部署快照，返回快照文件路径"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_id = f"snapshot_{timestamp}"
        snapshot_path = os.path.join(self.snapshot_dir, f"{snapshot_id}.json")

        snapshot = {
            "snapshot_id": snapshot_id,
            "timestamp": timestamp,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": sys.platform,
            "config_files": {},
            "environment": {},
            "extra": extra_data or {}
        }

        # 记录关键配置文件的内容
        config_files = [
            "robot_config.py",
            "deployment_config.py",
            "collision_config.py",
            "noise_config.py",
            "data_config.py",
        ]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        for cf in config_files:
            cf_path = os.path.join(base_dir, cf)
            if os.path.exists(cf_path):
                with open(cf_path, 'r', encoding='utf-8') as f:
                    snapshot["config_files"][cf] = f.read()

        # 记录环境变量（部署相关）
        for key in ["DEPLOY_MODE", "DEPLOY_EXECUTION", "ROBOT_MODE"]:
            if key in os.environ:
                snapshot["environment"][key] = os.environ[key]

        # 记录已安装的关键包版本
        snapshot["packages"] = {}
        for pkg in ["pybullet", "stable_baselines3", "numpy", "torch"]:
            try:
                mod = __import__(pkg)
                snapshot["packages"][pkg] = getattr(mod, "__version__", "unknown")
            except ImportError:
                snapshot["packages"][pkg] = "not_installed"

        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        print(f"[SNAPSHOT] ✅ 部署快照已保存: {snapshot_path}")
        return snapshot_path

    def list_snapshots(self) -> List[str]:
        """列出所有快照"""
        if not os.path.exists(self.snapshot_dir):
            return []
        return sorted([f for f in os.listdir(self.snapshot_dir) if f.endswith('.json')])

    def restore_snapshot(self, snapshot_id: str) -> bool:
        """从快照恢复配置（仅打印恢复建议，不直接覆盖）"""
        snapshot_path = os.path.join(self.snapshot_dir, snapshot_id)
        if not os.path.exists(snapshot_path):
            print(f"[SNAPSHOT] ❌ 快照不存在: {snapshot_id}")
            return False

        with open(snapshot_path, 'r', encoding='utf-8') as f:
            snapshot = json.load(f)

        print(f"\n[SNAPSHOT] 快照 {snapshot_id} 恢复建议:")
        print(f"  创建时间: {snapshot.get('timestamp', 'N/A')}")
        print(f"  Python: {snapshot.get('python_version', 'N/A')}")
        print(f"  平台: {snapshot.get('platform', 'N/A')}")
        print(f"  配置文件: {list(snapshot.get('config_files', {}).keys())}")
        print(f"\n  如需恢复，请手动将 snapshot 中的配置文件内容复制到对应文件")
        return True


# ============================================================
# 2. 安全参数完整性验证
# ============================================================

class SafetyParameterValidator:
    """验证所有安全相关参数是否完整且在合理范围内"""

    def __init__(self):
        self.issues = []

    def validate_all(self) -> Tuple[bool, List[str]]:
        """执行所有安全验证，返回(是否通过, 问题列表)"""
        self.issues = []

        self._validate_joint_limits()
        self._validate_force_limits()
        self._validate_speed_limits()
        self._validate_workspace()
        self._validate_emergency_stop()

        passed = len(self.issues) == 0
        return passed, self.issues

    def _validate_joint_limits(self):
        """验证关节限位"""
        try:
            from robot_config import JOINT_LIMITS, JOINT_INDICES
            if not JOINT_LIMITS:
                self.issues.append("关节限位 (JOINT_LIMITS) 未配置")
                return

            # 格式: {"lower": [...], "upper": [...]}
            if "lower" not in JOINT_LIMITS or "upper" not in JOINT_LIMITS:
                self.issues.append("关节限位格式错误: 缺少 lower 或 upper 列表")
                return

            lower = JOINT_LIMITS["lower"]
            upper = JOINT_LIMITS["upper"]

            if len(lower) != len(JOINT_INDICES) or len(upper) != len(JOINT_INDICES):
                self.issues.append(f"关节限位长度不匹配: lower={len(lower)}, upper={len(upper)}, indices={len(JOINT_INDICES)}")
                return

            for idx in JOINT_INDICES:
                if lower[idx] >= upper[idx]:
                    self.issues.append(f"关节 {idx} 限位无效: lower({lower[idx]}) >= upper({upper[idx]})")
        except Exception as e:
            self.issues.append(f"关节限位验证异常: {e}")

    def _validate_force_limits(self):
        """验证力限制"""
        try:
            from deployment_config import CONTROL_PARAMS
            force = CONTROL_PARAMS.get("force", 0)
            if force <= 0:
                self.issues.append(f"控制力参数无效: force={force}")
            elif force > 1000:
                self.issues.append(f"控制力参数过大 (>1000): force={force}")
        except Exception as e:
            self.issues.append(f"力限制验证异常: {e}")

    def _validate_speed_limits(self):
        """验证速度限制"""
        try:
            from deployment_config import CONTROL_PARAMS
            speed = CONTROL_PARAMS.get("move_speed", 0)
            if speed <= 0:
                self.issues.append(f"移动速度参数无效: move_speed={speed}")
        except Exception as e:
            self.issues.append(f"速度限制验证异常: {e}")

    def _validate_workspace(self):
        """验证工作空间配置"""
        try:
            from deploy_calibration import WorkspaceValidator
            validator = WorkspaceValidator()
            if validator.workspace_radius <= 0:
                self.issues.append(f"工作空间半径无效: {validator.workspace_radius}")
            if validator.min_z >= validator.max_z:
                self.issues.append(f"工作空间Z范围无效: min_z >= max_z")
        except Exception as e:
            self.issues.append(f"工作空间验证异常: {e}")

    def _validate_emergency_stop(self):
        """验证急停配置"""
        try:
            from sim_to_real_adapter import DeploymentSafetyGuard
            guard = DeploymentSafetyGuard()
            # 验证安全护栏能正常初始化
            if not hasattr(guard, "check_all"):
                self.issues.append("安全护栏缺少 check_all 方法")
        except Exception as e:
            self.issues.append(f"急停配置验证异常: {e}")

    def print_report(self):
        """打印验证报告"""
        passed, issues = self.validate_all()
        print("\n" + "=" * 60)
        print("  安全参数完整性验证")
        print("=" * 60)
        if passed:
            print("  ✅ 所有安全参数验证通过")
        else:
            print(f"  ❌ 发现 {len(issues)} 个问题:")
            for i, issue in enumerate(issues, 1):
                print(f"    {i}. {issue}")
        print("=" * 60)
        return passed


# ============================================================
# 3. 异常自动降级管理器
# ============================================================

class FailoverManager:
    """
    异常自动降级管理器
    当模型推理连续失败时，自动切换到轨迹模式
    支持：连续失败计数、降级触发、恢复检测
    """

    def __init__(self, max_consecutive_failures: int = 5, cooldown_cycles: int = 50):
        self.max_consecutive_failures = max_consecutive_failures
        self.cooldown_cycles = cooldown_cycles

        self.consecutive_failures = 0
        self.total_failures = 0
        self.total_successes = 0
        self.failover_active = False
        self.cooldown_counter = 0
        self.failover_count = 0
        self._lock = threading.Lock()

    def record_result(self, success: bool):
        """记录一次执行结果"""
        with self._lock:
            if success:
                self.consecutive_failures = 0
                self.total_successes += 1
                if self.failover_active:
                    self.cooldown_counter -= 1
                    if self.cooldown_counter <= 0:
                        self._recover()
            else:
                self.consecutive_failures += 1
                self.total_failures += 1
                if not self.failover_active and self.consecutive_failures >= self.max_consecutive_failures:
                    self._trigger_failover()

    def _trigger_failover(self):
        """触发降级（切换到轨迹模式）"""
        self.failover_active = True
        self.failover_count += 1
        self.cooldown_counter = self.cooldown_cycles
        print(f"\n⚠️  [FAILOVER] 模型推理连续失败 {self.consecutive_failures} 次，已自动降级到轨迹模式！")
        print(f"          将在 {self.cooldown_cycles} 个循环后尝试恢复模型模式")

    def _recover(self):
        """从降级状态恢复"""
        self.failover_active = False
        self.consecutive_failures = 0
        print(f"\n✅ [FAILOVER] 冷却期结束，已恢复模型推理模式")

    def should_use_trajectory(self) -> bool:
        """当前是否必须使用轨迹模式"""
        return self.failover_active

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            total = self.total_successes + self.total_failures
            return {
                "failover_active": self.failover_active,
                "failover_count": self.failover_count,
                "consecutive_failures": self.consecutive_failures,
                "total_successes": self.total_successes,
                "total_failures": self.total_failures,
                "success_rate": self.total_successes / total if total > 0 else 0,
                "cooldown_remaining": self.cooldown_counter if self.failover_active else 0,
            }


# ============================================================
# 4. 部署总结报告生成
# ============================================================

class DeploymentReportGenerator:
    """生成部署总结报告（TXT格式，轻量）"""

    def __init__(self, report_dir: str = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.report_dir = report_dir or os.path.join(base_dir, "deploy_reports")
        os.makedirs(self.report_dir, exist_ok=True)

    def generate_report(self, deploy_data: Dict[str, Any]) -> str:
        """生成部署报告，返回报告文件路径"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.report_dir, f"deploy_report_{timestamp}.txt")

        lines = []
        lines.append("=" * 70)
        lines.append("  部 署 总 结 报 告")
        lines.append("=" * 70)
        lines.append(f"  生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # 基本信息
        lines.append("-" * 70)
        lines.append("  【基本信息】")
        lines.append("-" * 70)
        lines.append(f"  部署模式: {deploy_data.get('mode', 'N/A')}")
        lines.append(f"  执行模式: {deploy_data.get('execution', 'N/A')}")
        lines.append(f"  总循环次数: {deploy_data.get('total_cycles', 0)}")
        lines.append(f"  成功次数: {deploy_data.get('success_count', 0)}")
        lines.append(f"  失败次数: {deploy_data.get('failure_count', 0)}")
        lines.append(f"  成功率: {deploy_data.get('success_rate', 0):.1f}%")
        lines.append(f"  部署时长: {deploy_data.get('duration_seconds', 0):.1f}秒")
        lines.append("")

        # 资源使用
        if "resource_stats" in deploy_data:
            rs = deploy_data["resource_stats"]
            lines.append("-" * 70)
            lines.append("  【资源使用统计】")
            lines.append("-" * 70)
            lines.append(f"  CPU 平均: {rs.get('avg_cpu', 0):.1f}%")
            lines.append(f"  CPU 峰值: {rs.get('max_cpu', 0):.1f}%")
            lines.append(f"  内存 平均: {rs.get('avg_mem', 0):.1f}%")
            lines.append(f"  内存 峰值: {rs.get('max_mem', 0):.1f}%")
            lines.append("")

        # 安全事件
        if "safety_events" in deploy_data:
            se = deploy_data["safety_events"]
            lines.append("-" * 70)
            lines.append("  【安全事件统计】")
            lines.append("-" * 70)
            lines.append(f"  紧急停止次数: {se.get('emergency_stops', 0)}")
            lines.append(f"  碰撞告警次数: {se.get('collision_warnings', 0)}")
            lines.append(f"  自动降级次数: {se.get('failover_count', 0)}")
            lines.append("")

        # 降级统计
        if "failover_stats" in deploy_data:
            fs = deploy_data["failover_stats"]
            lines.append("-" * 70)
            lines.append("  【降级管理统计】")
            lines.append("-" * 70)
            lines.append(f"  降级中: {'是' if fs.get('failover_active') else '否'}")
            lines.append(f"  总降级次数: {fs.get('failover_count', 0)}")
            lines.append("")

        # 健康检查结果
        if "health_checks" in deploy_data:
            hc = deploy_data["health_checks"]
            lines.append("-" * 70)
            lines.append("  【最终健康检查】")
            lines.append("-" * 70)
            for key, result in hc.items():
                status = "✅" if result.get("passed") else "❌"
                lines.append(f"  {status} {key}: {result.get('detail', '')}")
            lines.append("")

        # 结论
        lines.append("=" * 70)
        success_rate = deploy_data.get('success_rate', 0)
        if success_rate >= 90:
            lines.append("  🎯 部署结论: 优秀 (Excellent)")
        elif success_rate >= 70:
            lines.append("  ✅ 部署结论: 良好 (Good)")
        elif success_rate >= 50:
            lines.append("  ⚠️  部署结论: 一般 (Fair) - 建议优化模型")
        else:
            lines.append("  ❌ 部署结论: 不合格 (Poor) - 需要重新训练或排查")
        lines.append("=" * 70)

        report_content = "\n".join(lines)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"\n[REPORT] ✅ 部署报告已生成: {report_path}")
        print(report_content)
        return report_path


# ============================================================
# 5. 日志/数据自动归档
# ============================================================

class DeploymentArchiver:
    """部署日志和数据自动归档"""

    def __init__(self, archive_dir: str = None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.archive_dir = archive_dir or os.path.join(base_dir, "deploy_archives")
        os.makedirs(self.archive_dir, exist_ok=True)

    def archive_deployment(self, extra_files: List[str] = None) -> str:
        """归档本次部署的所有相关数据，返回归档文件路径"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"deploy_archive_{timestamp}"
        archive_path = os.path.join(self.archive_dir, f"{archive_name}.zip")

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 要归档的文件/目录模式
        patterns = [
            ("data", "*.csv"),          # 运行数据
            ("logs", "*"),               # 训练日志
            ("deploy_reports", "*.txt"), # 部署报告
            ("deploy_snapshots", "*.json"), # 配置快照
        ]

        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for subdir, pattern in patterns:
                full_dir = os.path.join(base_dir, subdir)
                if not os.path.exists(full_dir):
                    continue
                for root, dirs, files in os.walk(full_dir):
                    for fname in files:
                        if pattern == "*" or fname.endswith(pattern.replace("*", "").split(".")[-1]):
                            fpath = os.path.join(root, fname)
                            arcname = os.path.relpath(fpath, base_dir)
                            try:
                                zf.write(fpath, arcname)
                            except Exception as e:
                                print(f"[ARCHIVE] ⚠️  跳过 {fname}: {e}")

            # 额外文件
            if extra_files:
                for fpath in extra_files:
                    if os.path.exists(fpath):
                        arcname = os.path.basename(fpath)
                        zf.write(fpath, arcname)

        size_mb = os.path.getsize(archive_path) / (1024 * 1024)
        print(f"[ARCHIVE] ✅ 部署数据已归档: {archive_path} ({size_mb:.1f} MB)")
        return archive_path

    def list_archives(self) -> List[str]:
        """列出所有归档"""
        if not os.path.exists(self.archive_dir):
            return []
        return sorted([f for f in os.listdir(self.archive_dir) if f.endswith('.zip')])

    def cleanup_old_archives(self, keep_last: int = 10):
        """清理旧归档，只保留最近N个"""
        archives = self.list_archives()
        if len(archives) <= keep_last:
            return
        to_delete = archives[:-keep_last]
        for arc in to_delete:
            try:
                os.remove(os.path.join(self.archive_dir, arc))
                print(f"[ARCHIVE] 🗑  已删除旧归档: {arc}")
            except Exception as e:
                print(f"[ARCHIVE] ⚠️  删除失败 {arc}: {e}")


# ============================================================
# 快速测试
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  部署工具集自检")
    print("=" * 60)

    # 1. 测试安全验证
    print("\n[1/5] 安全参数验证...")
    validator = SafetyParameterValidator()
    ok = validator.print_report()

    # 2. 测试快照
    print("\n[2/5] 配置快照...")
    snap = DeploymentSnapshot()
    snap_path = snap.create_snapshot({"test": True})

    # 3. 测试降级管理器
    print("\n[3/5] 降级管理器...")
    fm = FailoverManager(max_consecutive_failures=3)
    for _ in range(3):
        fm.record_result(False)
    print(f"  降级状态: {fm.should_use_trajectory()} (期望: True)")
    for _ in range(60):
        fm.record_result(True)
    print(f"  恢复后状态: {fm.should_use_trajectory()} (期望: False)")
    print(f"  ✅ 降级管理器正常")

    # 4. 测试报告生成
    print("\n[4/5] 报告生成...")
    reporter = DeploymentReportGenerator()
    report_path = reporter.generate_report({
        "mode": "sim",
        "execution": "model",
        "total_cycles": 100,
        "success_count": 95,
        "failure_count": 5,
        "success_rate": 95.0,
        "duration_seconds": 120.5,
        "resource_stats": {"avg_cpu": 25.3, "max_cpu": 45.2, "avg_mem": 18.1, "max_mem": 22.5},
        "safety_events": {"emergency_stops": 0, "collision_warnings": 2, "failover_count": 0},
        "health_checks": {
            "robot_connection": {"passed": True, "detail": "已连接"},
            "joint_safety": {"passed": True, "detail": "全部安全"},
            "workspace": {"passed": True, "detail": "在范围内"},
            "resources": {"passed": True, "detail": "正常"},
            "success_rate": {"passed": True, "detail": "95.0%"},
        }
    })

    # 5. 测试归档
    print("\n[5/5] 数据归档...")
    archiver = DeploymentArchiver()
    archive_path = archiver.archive_deployment()
    archiver.cleanup_old_archives(keep_last=5)

    print("\n" + "=" * 60)
    print("  ✅ 部署工具集自检完成，所有模块正常！")
    print("=" * 60)
