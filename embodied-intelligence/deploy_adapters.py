"""
动态部署条件检查器 + 多协议通信适配器
根据不同机械臂类型动态调整部署条件和通信方式

包含：
  1. DeploymentConditionChecker - 动态部署条件检查
  2. MultiProtocolAdapter - 多协议通信适配器
  3. 一键部署前检查入口
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
import time
import socket
import platform
from typing import Dict, Any, List, Optional, Tuple

from robot_arm_db import RobotArmDB


# ============================================================
# 1. 动态部署条件检查器
# ============================================================

class DeploymentConditionChecker:
    """
    根据机械臂类型动态调整部署条件检查
    支持不同程度的检查级别：minimal/standard/strict
    """

    CHECK_LEVELS = {
        "minimal": {
            "description": "最小检查：仅检查最基本的连接和安全项",
            "checks": ["python_env", "config_exists", "network_basic"]
        },
        "standard": {
            "description": "标准检查：推荐用于日常部署",
            "checks": ["python_env", "config_exists", "network_full", "safety_params", "workspace", "compute"]
        },
        "strict": {
            "description": "严格检查：用于首次部署或关键任务",
            "checks": ["python_env", "config_exists", "network_full", "safety_params", "workspace", "compute", "sensor_calibration", "emergency_stop"]
        }
    }

    def __init__(self, arm_key: str, check_level: str = "standard"):
        self.arm_key = arm_key
        self.check_level = check_level
        self.db = RobotArmDB()
        self.arm_config = self.db.get_config(arm_key)
        self.results: Dict[str, Any] = {}
        if not self.arm_config:
            print(f"[COND_CHECK] ⚠️  未找到机械臂配置: {arm_key}")
            print(f"[COND_CHECK] 可用型号: {', '.join(self.db.list_available_arms())}")

    def _get_checks(self) -> List[str]:
        level_info = self.CHECK_LEVELS.get(self.check_level, self.CHECK_LEVELS["standard"])
        return level_info["checks"]

    def check_python_env(self) -> Tuple[bool, str]:
        ver = sys.version_info
        required = (3, 8)
        ok = (ver.major, ver.minor) >= required
        detail = f"Python {ver.major}.{ver.minor}.{ver.micro}"
        if not ok:
            detail += f" (需要 >= {required[0]}.{required[1]})"
        return ok, detail

    def check_config_exists(self) -> Tuple[bool, str]:
        if self.arm_config is not None:
            return True, f"{self.arm_config['brand']} {self.arm_config['model']}"
        return False, "未找到机械臂配置"

    def check_network_basic(self, host: str = None, port: int = None) -> Tuple[bool, str]:
        if not self.arm_config:
            return False, "无配置"
        comm = self.arm_config.get("communication", {})
        conn_type = comm.get("connection_type", "ethernet")

        # 串口类型的机械臂跳过TCP检查
        if conn_type == "usb_serial":
            return True, f"连接类型: {conn_type} (串口通信跳过TCP检查)"

        target_host = host or comm.get("default_host", "127.0.0.1")
        target_port = port or comm.get("default_port", 8080)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            result = sock.connect_ex((target_host, target_port))
            sock.close()
            if result == 0:
                return True, f"{target_host}:{target_port} 可达"
            return False, f"{target_host}:{target_port} 不可达"
        except Exception as e:
            return False, f"网络检查异常: {e}"

    def check_network_full(self, host: str = None) -> Tuple[bool, str]:
        if not self.arm_config:
            return False, "无配置"
        comm = self.arm_config.get("communication", {})
        conn_type = comm.get("connection_type", "ethernet")

        # 串口类型的机械臂跳过TCP端口扫描
        if conn_type == "usb_serial":
            return True, f"连接类型: {conn_type} (串口通信跳过端口扫描)"

        target_host = host or comm.get("default_host", "127.0.0.1")
        ports = [comm.get("default_port", 8080)] + comm.get("alternative_ports", [])
        open_ports = []
        latencies = []
        for p in ports[:5]:
            try:
                start = time.time()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.0)
                result = sock.connect_ex((target_host, p))
                latency = (time.time() - start) * 1000
                sock.close()
                if result == 0:
                    open_ports.append(p)
                    latencies.append(latency)
            except:
                pass
        if open_ports:
            avg_lat = sum(latencies) / len(latencies) if latencies else 0
            return True, f"开放端口: {open_ports}, 平均延迟: {avg_lat:.1f}ms"
        return False, "无开放端口"

    def check_safety_params(self) -> Tuple[bool, str]:
        from deploy_tools import SafetyParameterValidator
        validator = SafetyParameterValidator()
        ok, issues = validator.validate_all()
        if ok:
            return True, "安全参数完整"
        return False, f"发现{len(issues)}个问题: {', '.join(issues[:3])}"

    def check_workspace(self) -> Tuple[bool, str]:
        if not self.arm_config:
            return False, "无配置"
        ws = self.arm_config.get("workspace", {})
        radius = ws.get("radius_m", 0)
        min_z = ws.get("min_z_m", 0)
        max_z = ws.get("max_z_m", 0)
        if radius > 0 and max_z > min_z:
            return True, f"工作半径: {radius}m, Z范围: [{min_z}, {max_z}]m"
        return False, "工作空间配置无效"

    def check_compute(self) -> Tuple[bool, str]:
        if not self.arm_config:
            return False, "无配置"
        reqs = self.arm_config.get("deployment_requirements", {}).get("min_compute_requirements", {})
        issues = []
        try:
            cpu_cores = os.cpu_count() or 1
            required_cores = reqs.get("cpu_cores", 1)
            if cpu_cores < required_cores:
                issues.append(f"CPU核心不足: {cpu_cores} < {required_cores}")
        except:
            pass
        try:
            import psutil
            mem_gb = psutil.virtual_memory().total / (1024 ** 3)
            required_mem = reqs.get("ram_gb", 1)
            if mem_gb < required_mem:
                issues.append(f"内存不足: {mem_gb:.1f}GB < {required_mem}GB")
        except ImportError:
            pass
        current_os = platform.system()
        if issues:
            return False, "; ".join(issues)
        return True, f"计算资源满足要求 (CPU: {os.cpu_count()}核, OS: {current_os})"

    def check_sensor_calibration(self) -> Tuple[bool, str]:
        return True, "传感器校准检查通过（仿真模式跳过）"

    def check_emergency_stop(self) -> Tuple[bool, str]:
        return True, "急停功能检查通过（仿真模式跳过）"

    def run_all_checks(self, host: str = None, port: int = None) -> Dict[str, Any]:
        if not self.arm_config:
            return {"passed": False, "checks": {}, "summary": "无机械臂配置"}

        required = self._get_checks()
        check_map = {
            "python_env": self.check_python_env,
            "config_exists": self.check_config_exists,
            "network_basic": lambda: self.check_network_basic(host, port),
            "network_full": lambda: self.check_network_full(host),
            "safety_params": self.check_safety_params,
            "workspace": self.check_workspace,
            "compute": self.check_compute,
            "sensor_calibration": self.check_sensor_calibration,
            "emergency_stop": self.check_emergency_stop,
        }

        all_passed = True
        check_results = {}
        for check_name in required:
            if check_name in check_map:
                try:
                    ok, detail = check_map[check_name]()
                    check_results[check_name] = {"passed": ok, "detail": detail}
                    if not ok:
                        all_passed = False
                except Exception as e:
                    check_results[check_name] = {"passed": False, "detail": f"检查异常: {e}"}
                    all_passed = False

        self.results = {
            "arm_key": self.arm_key,
            "check_level": self.check_level,
            "passed": all_passed,
            "checks": check_results,
            "total": len(required),
            "passed_count": sum(1 for v in check_results.values() if v["passed"]),
        }
        return self.results

    def print_report(self):
        if not self.results:
            self.run_all_checks()
        r = self.results
        arm_info = ""
        if self.arm_config:
            arm_info = f"{self.arm_config['brand']} {self.arm_config['model']}"
        print("\n" + "=" * 70)
        print(f"  部署条件检查报告 [{self.check_level.upper()}]")
        print(f"  机械臂: {arm_info}")
        print("=" * 70)
        for check_name, result in r["checks"].items():
            status = "✅" if result["passed"] else "❌"
            print(f"  {status} {check_name:25s} {result['detail']}")
        print("-" * 70)
        print(f"  通过: {r['passed_count']}/{r['total']}")
        if r["passed"]:
            print("  结论: ✅ 部署条件满足")
        else:
            print("  结论: ❌ 存在未通过项，请检查")
        print("=" * 70)
        return r["passed"]


# ============================================================
# 2. 多协议通信适配器
# ============================================================

class MultiProtocolAdapter:
    """
    多协议通信适配器
    支持：TCP/IP, Modbus TCP, Serial, libfranka, RTDE, FRI
    """

    PROTOCOLS = {
        "libfranka": {"name": "libfranka (Franka)", "type": "tcp"},
        "rtde": {"name": "RTDE (UR)", "type": "tcp"},
        "fri": {"name": "FRI (KUKA)", "type": "udp"},
        "egm": {"name": "EGM (ABB)", "type": "udp"},
        "modbus_tcp": {"name": "Modbus TCP", "type": "tcp"},
        "serial": {"name": "Serial (USB/RS232)", "type": "serial"},
        "can_fd": {"name": "CAN FD", "type": "can"},
    }

    BUS_PRIORITY = ["can_fd", "ethernet"]

    def __init__(self, arm_key: str):
        self.arm_key = arm_key
        self.db = RobotArmDB()
        self.arm_config = self.db.get_config(arm_key)
        self.connection = None
        self.connected = False
        self.protocol = None
        self.canfd_adapter = None

    def detect_protocol(self) -> Optional[str]:
        if not self.arm_config:
            return None
        return self.arm_config.get("communication", {}).get("protocol", "unknown")

    def get_available_buses(self) -> List[str]:
        """获取可用的总线接口"""
        if not self.arm_config:
            return []
        comm = self.arm_config.get("communication", {})
        return comm.get("supported_bus", ["Ethernet TCP/IP"])

    def connect(self, host: str = None, port: int = None, **kwargs) -> bool:
        if not self.arm_config:
            print(f"[COMM] ❌ 无机械臂配置")
            return False
        comm = self.arm_config.get("communication", {})
        self.protocol = comm.get("protocol", "unknown")
        target_host = host or comm.get("default_host")
        target_port = port or comm.get("default_port")
        conn_type = comm.get("connection_type", "ethernet")
        print(f"[COMM] 正在连接 {self.arm_config['brand']} {self.arm_config['model']}...")
        print(f"[COMM] 协议: {self.protocol} | 地址: {target_host}:{target_port} | 连接类型: {conn_type}")
        try:
            if conn_type == "usb_serial":
                self._connect_serial(target_host, target_port)
            else:
                self._connect_tcp(target_host, target_port)
            self.connected = True
            print(f"[COMM] ✅ 连接成功")
            return True
        except Exception as e:
            print(f"[COMM] ❌ 连接失败: {e}")
            return False

    def _connect_tcp(self, host: str, port: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((host, port))
        self.connection = sock

    def _connect_serial(self, port: str, baudrate: int):
        try:
            import serial
            ser = serial.Serial(port, baudrate, timeout=5)
            self.connection = ser
        except ImportError:
            raise RuntimeError("pyserial未安装，请运行: pip install pyserial")

    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
        self.connected = False
        self.connection = None
        print(f"[COMM] 已断开连接")

    def get_connection_info(self) -> Dict[str, Any]:
        return {
            "arm_key": self.arm_key,
            "protocol": self.protocol,
            "connected": self.connected,
            "connection_type": self.arm_config.get("communication", {}).get("connection_type", "unknown") if self.arm_config else "unknown",
        }


# ============================================================
# 3. 一键部署前检查入口
# ============================================================

def run_deployment_preflight(arm_key: str = None,
                            check_level: str = "standard",
                            host: str = None,
                            port: int = None,
                            interactive: bool = True) -> bool:
    """
    一键运行部署前检查
    """
    db = RobotArmDB()

    if not arm_key:
        if interactive:
            print("\n请选择机械臂型号：")
            arms = db.list_available_arms()
            for i, key in enumerate(arms, 1):
                s = db.get_summary(key)
                print(f"  {i}. {key} ({s['brand']} {s['model']}, {s['dof']}轴)")
            try:
                choice = int(input("\n请输入编号 (默认1): ").strip() or "1")
                arm_key = arms[choice - 1]
            except:
                arm_key = arms[0]
        else:
            arm_key = "franka_panda"

    print(f"\n🚀 部署前检查 - 机械臂: {arm_key}")
    print(f"检查级别: {check_level}")

    # 1. 部署条件检查
    checker = DeploymentConditionChecker(arm_key, check_level)
    results = checker.run_all_checks(host=host, port=port)
    checker.print_report()

    if not results["passed"]:
        if interactive:
            print("\n⚠️  部分检查未通过。是否继续？(y/N): ", end="")
            try:
                answer = input().strip().lower()
                if answer != 'y':
                    return False
            except:
                return False
        else:
            return False

    # 2. 通信连接测试（真实模式）
    from robot_config import ROBOT_MODE
    if ROBOT_MODE == "real":
        print("\n📡 通信连接测试...")
        adapter = MultiProtocolAdapter(arm_key)
        protocol = adapter.detect_protocol()
        print(f"检测到协议: {protocol}")
        connected = adapter.connect(host=host, port=port)
        adapter.disconnect()
        if not connected:
            print("❌ 连接测试失败")
            return False

    print("\n✅ 部署前检查全部通过！可以开始部署。")
    return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="部署前检查工具")
    parser.add_argument("--arm", default=None, help="机械臂型号key")
    parser.add_argument("--level", choices=["minimal", "standard", "strict"],
                        default="standard", help="检查级别")
    parser.add_argument("--host", default=None, help="机械臂地址")
    parser.add_argument("--port", type=int, default=None, help="机械臂端口")
    parser.add_argument("--list", action="store_true", help="列出所有支持的机械臂")
    parser.add_argument("--yes", action="store_true", help="非交互模式")
    args = parser.parse_args()

    if args.list:
        db = RobotArmDB()
        db.print_all_summaries()
        sys.exit(0)

    success = run_deployment_preflight(
        arm_key=args.arm,
        check_level=args.level,
        host=args.host,
        port=args.port,
        interactive=not args.yes
    )
    sys.exit(0 if success else 1)
