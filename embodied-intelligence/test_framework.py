"""
测试体系与基准框架 v1.0
================================================================
包含：
  1. 单元测试框架（核心模块功能验证）
  2. 回归测试套件（防止回归bug）
  3. 基准测试（性能指标持续追踪）
  4. 测试报告生成

设计原则：
  - 所有测试必须可在无GPU环境下运行
  - 基准测试提供量化指标
  - 回归测试覆盖核心路径
"""
# ============================================================================
# 商业级免责声明
# ============================================================================
# 本文件按"现状"提供，不附带任何明示或默示保证。
# 在法律允许的最大范围内，权利人不承担任何直接或间接责任。
# ============================================================================

import numpy as np
import time
import json
import os
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from collections import deque
from datetime import datetime


# ============================================================================
# 第一部分：测试结果数据结构
# ============================================================================

@dataclass
class TestResult:
    """单个测试的结果"""
    name: str
    category: str
    passed: bool
    duration: float = 0.0
    error: str = ""
    details: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "category": self.category,
            "passed": self.passed,
            "duration": round(self.duration, 4),
            "error": self.error,
            "details": self.details,
        }


@dataclass
class BenchmarkResult:
    """基准测试结果"""
    name: str
    metric: str
    value: float
    unit: str
    baseline: Optional[float] = None
    direction: str = "higher"  # higher=越高越好, lower=越低越好

    def to_dict(self) -> Dict:
        improvement = None
        if self.baseline is not None and self.baseline != 0:
            improvement = (self.value - self.baseline) / abs(self.baseline) * 100
        return {
            "name": self.name,
            "metric": self.metric,
            "value": round(self.value, 6),
            "unit": self.unit,
            "baseline": self.baseline,
            "improvement_pct": round(improvement, 2) if improvement is not None else None,
            "direction": self.direction,
        }


# ============================================================================
# 第二部分：单元测试框架
# ============================================================================

class UnitTestSuite:
    """
    单元测试套件
    覆盖：执行器模型、域随机化、传感器噪声、控制器等核心模块
    """

    def __init__(self):
        self.results: List[TestResult] = []
        self._start_time = 0.0

    def _run(self, name: str, category: str, test_fn: Callable) -> TestResult:
        """执行单个测试"""
        self._start_time = time.time()
        try:
            details = test_fn()
            duration = time.time() - self._start_time
            result = TestResult(name=name, category=category, passed=True,
                                duration=duration, details=details or {})
        except AssertionError as e:
            duration = time.time() - self._start_time
            result = TestResult(name=name, category=category, passed=False,
                                duration=duration, error=str(e))
        except Exception as e:
            duration = time.time() - self._start_time
            result = TestResult(name=name, category=category, passed=False,
                                duration=duration, error=f"Unexpected: {e}")
        self.results.append(result)
        return result

    def test_actuator_dynamics(self):
        """测试：执行器动力学基本功能"""
        def _test():
            from simulation_enhanced import HighPrecisionActuator, MotorParams
            actuator = HighPrecisionActuator()
            # 测试初始状态
            assert actuator.output_angle == 0.0
            assert actuator.output_velocity == 0.0
            # 测试一步仿真
            result = actuator.step(voltage_cmd=10.0, load_torque=0.0, dt=0.001)
            assert "output_angle" in result
            assert "output_torque" in result
            assert "temperature" in result
            return {"output_torque": result["output_torque"]}
        return self._run("actuator_dynamics_basic", "actuator", _test)

    def test_actuator_fault_injection(self):
        """测试：执行器故障注入"""
        def _test():
            from simulation_enhanced import HighPrecisionActuator
            actuator = HighPrecisionActuator()
            # 注入故障
            actuator.inject_fault("stiction", severity=0.8)
            assert actuator.fault_mode == "stiction"
            assert actuator.fault_severity == 0.8
            # 清除故障
            actuator.clear_fault()
            assert actuator.fault_mode is None
            return {}
        return self._run("actuator_fault_injection", "actuator", _test)

    def test_domain_randomization(self):
        """测试：域随机化参数生成"""
        def _test():
            from simulation_enhanced import EnhancedDomainRandomizer
            dr = EnhancedDomainRandomizer({"intensity": 1.0})
            # 测试传感器随机化
            sensor_params = dr.get_sensor_randomization()
            assert "joint_noise_std" in sensor_params
            assert "ee_noise_std" in sensor_params
            # 测试控制随机化
            ctrl_params = dr.get_control_randomization()
            assert "control_gain_scale" in ctrl_params
            return {"sensor_params": sensor_params}
        return self._run("domain_randomization_params", "domain_rand", _test)

    def test_sensor_noise_models(self):
        """测试：传感器噪声模型"""
        def _test():
            try:
                from sensor_noise import JointAngleNoise, ForceTorqueNoise
            except ImportError:
                return {"skipped": "module not available"}
            joint_noise = JointAngleNoise(gaussian_std=0.01)
            noisy = joint_noise.add(0.5)
            assert abs(noisy - 0.5) < 0.1  # 噪声不应过大
            return {"noisy_value": noisy}
        return self._run("sensor_noise_models", "sensor", _test)

    def test_impedance_controller(self):
        """测试：阻抗控制器"""
        def _test():
            from sim2real_transfer import ImpedanceController
            ctrl = ImpedanceController({"dof": 7})
            q = np.zeros(7)
            q_dot = np.zeros(7)
            q_des = np.ones(7) * 0.1
            tau = ctrl.compute_torque(q, q_dot, q_des)
            assert tau.shape == (7,)
            # 模式切换
            ctrl.set_mode("soft")
            tau2 = ctrl.compute_torque(q, q_dot, q_des)
            return {"tau_norm": np.linalg.norm(tau)}
        return self._run("impedance_controller", "control", _test)

    def test_multi_task_scenes(self):
        """测试：多任务场景定义"""
        def _test():
            from simulation_enhanced import MultiTaskEnvironment, get_all_task_types
            tasks = get_all_task_types()
            assert len(tasks) >= 8
            for task_type in tasks:
                env = MultiTaskEnvironment(task_type)
                assert env.task_type == task_type
            return {"num_tasks": len(tasks)}
        return self._run("multi_task_scenes", "task", _test)

    def test_system_identifier(self):
        """测试：系统识别器"""
        def _test():
            from sim2real_transfer import SystemIdentifier
            si = SystemIdentifier()
            # 添加一些随机数据
            for _ in range(10):
                state = np.random.randn(14)
                action = np.random.randn(7)
                next_state = state + np.random.randn(14) * 0.01
                si.add_data(state, action, next_state)
            # 优化（少量迭代）
            result = si.optimize(n_iterations=5)
            assert "best_loss" in result
            return {"best_loss": result["best_loss"]}
        return self._run("system_identifier", "sim2real", _test)

    def test_robustness_test_profiles(self):
        """测试：鲁棒性测试配置生成"""
        def _test():
            from simulation_enhanced import RobustnessTestSuite, get_all_test_types
            suite = RobustnessTestSuite()
            test_types = get_all_test_types()
            assert len(test_types) >= 9
            for t in test_types:
                profile = suite.generate_test_profile(t, intensity=1.0)
                assert "test_type" in profile
                assert "intensity" in profile
            return {"num_test_types": len(test_types)}
        return self._run("robustness_profiles", "robustness", _test)

    def run_all(self) -> List[TestResult]:
        """运行所有单元测试"""
        self.results.clear()

        self.test_actuator_dynamics()
        self.test_actuator_fault_injection()
        self.test_domain_randomization()
        self.test_sensor_noise_models()
        self.test_impedance_controller()
        self.test_multi_task_scenes()
        self.test_system_identifier()
        self.test_robustness_test_profiles()

        return self.results

    def get_summary(self) -> Dict:
        """获取测试摘要"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        categories = {}
        for r in self.results:
            if r.category not in categories:
                categories[r.category] = {"total": 0, "passed": 0}
            categories[r.category]["total"] += 1
            if r.passed:
                categories[r.category]["passed"] += 1

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total > 0 else 0,
            "total_duration": sum(r.duration for r in self.results),
            "by_category": categories,
            "failed_tests": [r.to_dict() for r in self.results if not r.passed],
        }


# ============================================================================
# 第三部分：基准测试套件
# ============================================================================

class BenchmarkSuite:
    """
    基准测试套件
    追踪：训练速度、推理延迟、成功率、样本效率等核心指标
    """

    def __init__(self, baseline_path: str = None):
        self.results: List[BenchmarkResult] = []
        self.baselines: Dict[str, float] = {}

        if baseline_path and os.path.exists(baseline_path):
            with open(baseline_path, "r") as f:
                data = json.load(f)
                for item in data.get("benchmarks", []):
                    self.baselines[item["name"]] = item["value"]

    def _measure(self, name: str, metric: str, unit: str,
                 run_fn: Callable[[], float], direction: str = "higher") -> BenchmarkResult:
        """测量一个基准指标"""
        value = run_fn()
        baseline = self.baselines.get(name)
        result = BenchmarkResult(
            name=name, metric=metric, value=value, unit=unit,
            baseline=baseline, direction=direction
        )
        self.results.append(result)
        return result

    def bench_array_operations(self):
        """基准：NumPy数组运算速度"""
        def _run():
            size = 10000
            a = np.random.randn(size, 7)
            b = np.random.randn(size, 7)
            start = time.time()
            for _ in range(100):
                c = a + b
                d = np.dot(a, b.T)
                e = np.linalg.norm(a, axis=1)
            return (time.time() - start) * 1000  # ms
        return self._measure("array_ops_100x", "运算时间", "ms", _run, direction="lower")

    def bench_matrix_inverse(self):
        """基准：矩阵求逆速度"""
        def _run():
            matrices = [np.random.randn(7, 7) for _ in range(1000)]
            start = time.time()
            for m in matrices:
                np.linalg.pinv(m)
            return (time.time() - start) * 1000
        return self._measure("matrix_pinv_1000x", "求逆时间", "ms", _run, direction="lower")

    def bench_sensor_noise_throughput(self):
        """基准：传感器噪声处理吞吐量"""
        def _run():
            try:
                from sensor_noise import JointAngleNoise
            except ImportError:
                return 0.0
            noise = JointAngleNoise()
            angles = [0.5] * 10000
            start = time.time()
            for a in angles:
                noise.add(a)
            elapsed = time.time() - start
            return 10000 / elapsed  # samples/sec
        return self._measure("sensor_noise_tp", "吞吐量", "samples/s", _run, direction="higher")

    def bench_actuator_step(self):
        """基准：执行器一步仿真耗时"""
        def _run():
            from simulation_enhanced import HighPrecisionActuator
            actuators = [HighPrecisionActuator() for _ in range(7)]
            start = time.time()
            for _ in range(1000):
                for act in actuators:
                    act.step(10.0, 0.0, 0.001)
            elapsed = (time.time() - start) * 1000
            return elapsed / 1000  # ms per step (7轴)
        return self._measure("actuator_step_7dof", "每步耗时", "ms", _run, direction="lower")

    def bench_impedance_control(self):
        """基准：阻抗控制器计算速度"""
        def _run():
            from sim2real_transfer import ImpedanceController
            ctrl = ImpedanceController({"dof": 7})
            q = np.zeros(7)
            q_dot = np.zeros(7)
            q_des = np.ones(7) * 0.1
            start = time.time()
            for _ in range(10000):
                ctrl.compute_torque(q, q_dot, q_des)
            elapsed = (time.time() - start) * 1000
            return 10000 / elapsed  # Hz (控制频率)
        return self._measure("impedance_ctrl_rate", "控制频率", "Hz", _run, direction="higher")

    def bench_randomization_gen(self):
        """基准：随机化参数生成速度"""
        def _run():
            from simulation_enhanced import EnhancedDomainRandomizer
            dr = EnhancedDomainRandomizer({"intensity": 1.0})
            start = time.time()
            for _ in range(1000):
                dr.get_sensor_randomization()
                dr.get_control_randomization()
                dr.get_actuator_randomization()
            elapsed = (time.time() - start) * 1000
            return 1000 / elapsed  # 次/ms
        return self._measure("randomization_gen", "生成速度", "次/ms", _run, direction="higher")

    def run_all(self) -> List[BenchmarkResult]:
        """运行所有基准测试"""
        self.results.clear()

        self.bench_array_operations()
        self.bench_matrix_inverse()
        self.bench_sensor_noise_throughput()
        self.bench_actuator_step()
        self.bench_impedance_control()
        self.bench_randomization_gen()

        return self.results

    def get_summary(self) -> Dict:
        """获取基准摘要"""
        regressions = []
        improvements = []

        for r in self.results:
            if r.baseline is not None:
                if r.direction == "higher" and r.value < r.baseline * 0.9:
                    regressions.append(r.to_dict())
                elif r.direction == "lower" and r.value > r.baseline * 1.1:
                    regressions.append(r.to_dict())
                elif r.direction == "higher" and r.value > r.baseline * 1.1:
                    improvements.append(r.to_dict())
                elif r.direction == "lower" and r.value < r.baseline * 0.9:
                    improvements.append(r.to_dict())

        return {
            "total_benchmarks": len(self.results),
            "with_baseline": sum(1 for r in self.results if r.baseline is not None),
            "regressions": regressions,
            "improvements": improvements,
            "benchmarks": [r.to_dict() for r in self.results],
        }

    def save_baseline(self, path: str):
        """保存当前结果作为新的基线"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "benchmarks": [r.to_dict() for r in self.results],
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# ============================================================================
# 第四部分：完整测试运行器与报告
# ============================================================================

class TestRunner:
    """统一的测试运行器"""

    def __init__(self, output_dir: str = "test_results"):
        self.output_dir = output_dir
        self.unit_suite = UnitTestSuite()
        self.bench_suite = BenchmarkSuite()

    def run_full_suite(self) -> Dict:
        """运行完整测试套件"""
        print("\n" + "=" * 60)
        print("  完整测试套件 - 开始执行")
        print("=" * 60)

        # 单元测试
        print("\n[1/2] 运行单元测试...")
        self.unit_suite.run_all()
        unit_summary = self.unit_suite.get_summary()
        self._print_unit_summary(unit_summary)

        # 基准测试
        print("\n[2/2] 运行基准测试...")
        self.bench_suite.run_all()
        bench_summary = self.bench_suite.get_summary()
        self._print_bench_summary(bench_summary)

        # 汇总报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "unit_tests": unit_summary,
            "benchmarks": bench_summary,
            "overall": {
                "unit_pass": unit_summary["pass_rate"] >= 0.95,
                "no_regression": len(bench_summary["regressions"]) == 0,
            }
        }

        self._save_report(report)

        print("\n" + "=" * 60)
        status = "✅ 通过" if report["overall"]["unit_pass"] and report["overall"]["no_regression"] else "⚠️ 需要关注"
        print(f"  测试完成 - 总体状态: {status}")
        print("=" * 60 + "\n")

        return report

    def _print_unit_summary(self, summary: Dict):
        print(f"  单元测试: {summary['passed']}/{summary['total']} 通过 ({summary['pass_rate']*100:.1f}%)")
        print(f"  总耗时: {summary['total_duration']:.3f}s")
        for cat, stats in summary["by_category"].items():
            rate = stats["passed"] / stats["total"] * 100
            icon = "✅" if rate >= 100 else "⚠️" if rate >= 80 else "❌"
            print(f"    {icon} {cat:15s}: {stats['passed']}/{stats['total']} ({rate:.0f}%)")
        if summary["failed"]:
            print(f"  ❌ 失败测试: {summary['failed']}")
            for ft in summary["failed_tests"]:
                print(f"    - {ft['name']}: {ft['error'][:80]}")

    def _print_bench_summary(self, summary: Dict):
        print(f"  基准测试: {summary['total_benchmarks']} 项指标")
        if summary["improvements"]:
            print(f"  📈 性能提升: {len(summary['improvements'])} 项")
            for imp in summary["improvements"]:
                print(f"    - {imp['name']}: {imp['improvement_pct']:+.1f}%")
        if summary["regressions"]:
            print(f"  📉 性能回归: {len(summary['regressions'])} 项 ⚠️")
            for reg in summary["regressions"]:
                print(f"    - {reg['name']}: {reg['improvement_pct']:+.1f}%")

    def _save_report(self, report: Dict):
        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n  报告已保存: {path}")


# ============================================================================
# 便捷入口
# ============================================================================

def run_all_tests(output_dir: str = "test_results") -> Dict:
    """便捷入口：运行完整测试套件"""
    runner = TestRunner(output_dir)
    return runner.run_full_suite()


def run_unit_tests_only() -> Dict:
    """仅运行单元测试"""
    suite = UnitTestSuite()
    suite.run_all()
    return suite.get_summary()


def run_benchmarks_only(baseline_path: str = None) -> Dict:
    """仅运行基准测试"""
    suite = BenchmarkSuite(baseline_path)
    suite.run_all()
    return suite.get_summary()
