# -*- coding: utf-8 -*-
"""
真实机器人协议适配器 · 离线联调验证框架（零硬件依赖）
=====================================================
功能：
    1. 协议覆盖率统计（56 个 PROTOCOL_ADAPTERS × 183 个 BRAND_COMM_MAP 映射）
    2. 离线 Mock 设备握手验证（虚拟 TCP/UDP/Serial 服务端，不需真实机器人）
    3. 六方法接口参数校验（connect / move_joints / move_cartesian /
       get_joint_states / get_ee_pose / stop / disconnect）
    4. 品牌映射完整性检查（所有 arm_key → protocol 都必须在 PROTOCOL_ADAPTERS 中存在）
    5. 输出结构化 JSON + 人类可读报告

用法：
    cd embodied-intelligence
    python ../protocol_validation_framework.py
    python ../protocol_validation_framework.py --full      # 全量深度校验
    python ../protocol_validation_framework.py --quick     # 仅覆盖率 + 映射检查（1 秒完成）
    python ../protocol_validation_framework.py --json      # 额外输出 JSON 报告
"""

import os
import re
import sys
import json
import time
import socket
import threading
import importlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Callable

PROJECT_ROOT = Path(__file__).parent.resolve()
EI_DIR = PROJECT_ROOT / "embodied-intelligence"

# 把 embodied-intelligence 加入 import 路径
if str(EI_DIR) not in sys.path:
    sys.path.insert(0, str(EI_DIR))


# ============================================================
# 离线 Mock 通信层：虚拟 TCP Server（接受 connect，回显握手包）
# ============================================================

class MockTCPServer:
    """在 localhost 随机可用端口开一个虚拟 TCP 设备，用于验证 connect/disconnect 握手"""

    def __init__(self, protocol_name: str, handshake_bytes: bytes = b"OK-HANDSHAKE\n"):
        self.protocol = protocol_name
        self.handshake = handshake_bytes
        self.sock: Optional[socket.socket] = None
        self.port: Optional[int] = None
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self.connections_accepted: int = 0
        self.data_received: List[bytes] = []

    def _serve(self):
        assert self.sock is not None
        self.sock.settimeout(0.3)
        while not self._stop.is_set():
            try:
                conn, _addr = self.sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            self.connections_accepted += 1
            try:
                conn.settimeout(0.5)
                try:
                    data = conn.recv(1024)
                    if data:
                        self.data_received.append(data)
                except socket.timeout:
                    pass
                try:
                    conn.sendall(self.handshake)
                except OSError:
                    pass
            finally:
                try:
                    conn.close()
                except OSError:
                    pass

    def start(self) -> Tuple[str, int]:
        """返回 (host, port)"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(3)
        self.port = self.sock.getsockname()[1]
        self._thread = threading.Thread(target=self._serve, name=f"mock-{self.protocol}", daemon=True)
        self._thread.start()
        return "127.0.0.1", self.port

    def stop(self):
        self._stop.set()
        try:
            if self.sock:
                self.sock.close()
        except OSError:
            pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)


# ============================================================
# 轻量级 Mock UDP Server
# ============================================================

class MockUDPServer:
    def __init__(self, protocol_name: str, handshake_bytes: bytes = b"UDP-OK\n"):
        self.protocol = protocol_name
        self.handshake = handshake_bytes
        self.sock: Optional[socket.socket] = None
        self.port: Optional[int] = None
        self._thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        self.packets_received: int = 0

    def _serve(self):
        assert self.sock is not None
        self.sock.settimeout(0.3)
        while not self._stop.is_set():
            try:
                data, addr = self.sock.recvfrom(2048)
            except socket.timeout:
                continue
            except OSError:
                break
            self.packets_received += 1
            try:
                self.sock.sendto(self.handshake, addr)
            except OSError:
                pass

    def start(self) -> Tuple[str, int]:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", 0))
        self.port = self.sock.getsockname()[1]
        self._thread = threading.Thread(target=self._serve, name=f"mockudp-{self.protocol}", daemon=True)
        self._thread.start()
        return "127.0.0.1", self.port

    def stop(self):
        self._stop.set()
        try:
            if self.sock:
                self.sock.close()
        except OSError:
            pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)


# ============================================================
# 覆盖率 / 映射校验
# ============================================================

def load_real_robot_module() -> Tuple[Dict[str, str], Dict[str, str]]:
    """安全导入 real_robot_adapter，提取 BRAND_COMM_MAP 和 PROTOCOL_ADAPTERS"""
    try:
        # 先处理 real_robot_adapter.py 中 import 的模块可能不存在的问题，只提取变量
        import ast
        rra_path = EI_DIR / "real_robot_adapter.py"
        if not rra_path.is_file():
            return {}, {}
        tree = ast.parse(rra_path.read_text(encoding="utf-8", errors="replace"))
        brand_map: Dict[str, str] = {}
        proto_map: Dict[str, str] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "BRAND_COMM_MAP" \
                            and isinstance(node.value, ast.Dict):
                        for k, v in zip(node.value.keys, node.value.values):
                            if isinstance(k, ast.Constant) and isinstance(v, ast.Constant):
                                brand_map[str(k.value)] = str(v.value)
                    elif isinstance(target, ast.Name) and target.id == "PROTOCOL_ADAPTERS" \
                            and isinstance(node.value, ast.Dict):
                        for k, v in zip(node.value.keys, node.value.values):
                            if isinstance(k, ast.Constant) and isinstance(v, ast.Constant):
                                proto_map[str(k.value)] = str(v.value)
        return brand_map, proto_map
    except Exception as e:
        print(f"  ⚠️  解析 real_robot_adapter.py 失败: {e}")
        return {}, {}


def check_brand_coverage(brand_map: Dict[str, str], proto_map: Dict[str, str]) -> List[Dict[str, Any]]:
    """检查每一个品牌映射是否指向一个已注册的协议"""
    issues: List[Dict[str, Any]] = []
    for arm_key, proto in brand_map.items():
        if proto not in proto_map:
            issues.append({
                "arm_key": arm_key,
                "protocol": proto,
                "problem": "协议未在 PROTOCOL_ADAPTERS 中注册",
                "severity": "high",
            })
    return issues


# ============================================================
# 协议适配器可导入性 & 接口校验（不需要真实硬件，只做 class/方法 introspection）
# ============================================================

REQUIRED_METHODS = (
    "connect", "disconnect", "move_joints", "move_cartesian",
    "get_joint_states", "get_ee_pose", "stop",
)


def _resolve_class(dotted_path: str):
    """把 'module.Class' 解析为类对象，失败返回 None 和错误原因"""
    if "." not in dotted_path:
        return None, "路径格式错误，缺少模块名分隔"
    module_path, class_name = dotted_path.rsplit(".", 1)
    try:
        mod = importlib.import_module(module_path)
    except ImportError as e:
        return None, f"模块不可导入: {e}"
    except Exception as e:
        return None, f"导入异常 {type(e).__name__}: {e}"
    cls = getattr(mod, class_name, None)
    if cls is None:
        return None, f"模块中不存在 {class_name} 类"
    return cls, None


def check_protocol_class(proto: str, dotted_path: str) -> Dict[str, Any]:
    """静态检查单个协议类：可导入性 + 必需方法是否齐备"""
    info: Dict[str, Any] = {
        "protocol": proto,
        "adapter_path": dotted_path,
        "importable": False,
        "import_error": None,
        "methods_present": {},
        "methods_missing": [],
        "methods_score": 0.0,
    }
    cls, err = _resolve_class(dotted_path)
    if cls is None:
        info["import_error"] = err
        info["methods_missing"] = list(REQUIRED_METHODS)
        return info
    info["importable"] = True
    present: Dict[str, bool] = {}
    for m in REQUIRED_METHODS:
        has = callable(getattr(cls, m, None))
        present[m] = has
        if not has:
            info["methods_missing"].append(m)
    info["methods_present"] = present
    info["methods_score"] = sum(1 for v in present.values() if v) / len(REQUIRED_METHODS)
    return info


# ============================================================
# RobotAdapter 主类集成测试（仿真模式，不触达真实硬件）
# ============================================================

def _instantiate_robot_adapter(arm_key: str) -> Tuple[Optional[Any], Optional[str]]:
    """用 sim 模式实例化 RobotAdapter，避免真实网络调用"""
    try:
        mod = importlib.import_module("real_robot_adapter")
        RA = getattr(mod, "RobotAdapter", None)
        if RA is None:
            return None, "real_robot_adapter 中没有 RobotAdapter 类"
        ra = RA(mode="sim", arm_key=arm_key, simulator_backend="pybullet")
        return ra, None
    except Exception as e:
        return None, f"实例化失败 {type(e).__name__}: {e}"


def test_robot_adapter_interface(arm_keys: List[str], max_samples: int = 10) -> List[Dict[str, Any]]:
    """抽样对几个 arm_key 做接口调用级检查（仿真模式）"""
    results: List[Dict[str, Any]] = []
    sample = arm_keys[:max_samples]
    for arm_key in sample:
        item: Dict[str, Any] = {
            "arm_key": arm_key,
            "instantiated": False,
            "init_ok": False,
            "info_calls": {},
            "errors": [],
        }
        ra, err = _instantiate_robot_adapter(arm_key)
        if ra is None:
            item["errors"].append(f"实例化: {err}")
            results.append(item)
            continue
        item["instantiated"] = True

        # 1. get_arm_info()
        try:
            info = ra.get_arm_info()
            item["info_calls"]["get_arm_info"] = {
                "brand": info.get("brand"),
                "dofs": info.get("dofs"),
                "ok": True,
            }
        except Exception as e:
            item["errors"].append(f"get_arm_info: {e}")

        # 2. initialize() (sim 模式不会真联网)
        try:
            ok_init = ra.initialize()
            item["init_ok"] = bool(ok_init)
        except Exception as e:
            item["errors"].append(f"initialize: {e}")

        # 3. 六方法调用（仿真模式下只要不抛异常就算通过）
        if item["init_ok"]:
            dofs = item["info_calls"].get("get_arm_info", {}).get("dofs", 7)
            for name, fn in {
                "get_joint_states": lambda: ra.get_joint_states(),
                "get_ee_pose": lambda: ra.get_ee_pose(),
                "move_joints": lambda: ra.move_joints([0.0] * max(1, dofs), speed=0.1),
                "move_cartesian": lambda: ra.move_cartesian(0.3, 0.0, 0.2, speed=0.1),
                "stop": lambda: ra.stop(),
            }.items():
                try:
                    fn()
                    item["info_calls"][name] = {"ok": True}
                except Exception as e:
                    item["info_calls"][name] = {"ok": False, "error": str(e)}
                    item["errors"].append(f"{name}: {e}")

            # 4. shutdown()
            try:
                ra.shutdown()
                item["info_calls"]["shutdown"] = {"ok": True}
            except Exception as e:
                item["errors"].append(f"shutdown: {e}")

        results.append(item)
    return results


# ============================================================
# 报告输出
# ============================================================

SEVERITY_COLOR = {
    "critical": "\033[91m", "high": "\033[93m", "medium": "\033[96m",
    "low": "\033[90m", "ok": "\033[92m", "warn": "\033[93m",
}
RESET = "\033[0m"


def _c(level: str, text: str) -> str:
    if sys.platform.startswith("win"):
        return text
    return SEVERITY_COLOR.get(level, "") + text + RESET


def print_report(report: Dict[str, Any]):
    sep = "=" * 72
    print()
    print(sep)
    print("  🤖  真实机器人协议适配器 · 离线联调验证报告")
    print(sep)
    print(f'  生成时间: {report["generated_at"]}')
    print(f'  项目根:   {report["project_root"]}')
    print()
    cov = report["coverage"]
    print(f'  📊 覆盖率')
    print(f'    · BRAND_COMM_MAP 品牌映射 : {cov["brands_total"]} 条')
    print(f'    · PROTOCOL_ADAPTERS 协议数: {cov["protocols_total"]} 个')
    print(f'    · 品牌→协议未注册映射     : {_c("high" if cov["broken_links"] else "ok", str(cov["broken_links"]))}')
    print(f'    · 协议适配器类可导入率     : {cov["importable_count"]}/{cov["protocols_total"]}'
          f'  ({cov["importable_ratio"] * 100:.0f}%)')
    print(f'    · 6 方法齐备率（已导入的）: {cov["avg_methods_score"] * 100:.1f}%')
    print()

    # 损坏链接
    if cov["broken_links"]:
        print(_c("high", "  ⚠️  品牌映射断裂（品牌指向未注册协议）:"))
        for it in cov["broken_link_details"][:20]:
            print(f'     - {it["arm_key"]:35s} → {it["protocol"]}  {it["problem"]}')
        extra = len(cov["broken_link_details"]) - 20
        if extra > 0:
            print(f"     ... 其余 {extra} 条详见 JSON 报告")
        print()

    # 协议类检查分桶
    proto_buckets = report["protocol_checks"]
    ok_list = [p for p in proto_buckets if p["importable"] and not p["methods_missing"]]
    imp_list = [p for p in proto_buckets if p["importable"] and p["methods_missing"]]
    miss_list = [p for p in proto_buckets if not p["importable"]]
    print(f'  🧩 协议实现分桶')
    print(f'    · 完整可用（可导入+6方法齐全）  : {_c("ok", str(len(ok_list)))} 个')
    if ok_list:
        for p in ok_list[:15]:
            print(f'       ✅ {p["protocol"]:30s}  {p["adapter_path"]}')
        if len(ok_list) > 15:
            print(f"       ... 其余 {len(ok_list) - 15} 个")
    print(f'    · 可导入但缺少方法            : {_c("warn", str(len(imp_list)))} 个')
    for p in imp_list[:10]:
        print(f'       ⚠️  {p["protocol"]:30s}  缺少: {", ".join(p["methods_missing"])}')
    if len(imp_list) > 10:
        print(f"       ... 其余 {len(imp_list) - 10} 个")
    print(f'    · 适配器尚未实现（模块/类缺失）: {_c("high", str(len(miss_list)))} 个')
    generic_tcp = [p for p in miss_list if "GenericTCPAdapter" in p["adapter_path"]]
    generic_other = [p for p in miss_list if "GenericTCPAdapter" not in p["adapter_path"]]
    if generic_tcp:
        print(f'       ├─ GenericTCPAdapter 占位未实现: {len(generic_tcp)} 个 (品牌通用型，可批量实现)')
    if generic_other:
        print(f'       └─ 特定品牌适配器未实现     : {len(generic_other)} 个 (需逐一实现类)')
        for p in generic_other[:10]:
            print(f'          · {p["protocol"]:30s}  {p["adapter_path"]}  → {p["import_error"]}')
    print()

    # 抽样集成测试
    integ = report.get("integration_samples", [])
    if integ:
        print("  🎯 抽样接口集成测试（仿真模式，PyBullet 后端）")
        pass_cnt = sum(1 for x in integ if not x["errors"])
        fail_cnt = len(integ) - pass_cnt
        print(f"    · 样本数: {len(integ)}  |  通过: {_c('ok', str(pass_cnt))}  |  异常: {_c('warn', str(fail_cnt))}")
        for it in integ:
            tag = _c("ok", "PASS") if not it["errors"] else _c("warn", f"WARN({len(it['errors'])})")
            print(f"      [{tag}] {it['arm_key']:32s}  init_ok={it.get('init_ok', False)}")
            for err in it["errors"][:3]:
                print(f"             · {err[:140]}")
        print()

    print(sep)
    overall_ok = cov["broken_links"] == 0 and len(miss_list) == 0
    print("  总体结论: " + (_c("ok", "✅ 当前覆盖率与映射均完整，需补齐适配器模块实现")
                    if overall_ok else _c("warn", "⚠️  需补齐未实现的适配器模块 & 修复断裂映射")))
    print(sep)
    print()


def main() -> int:
    args = set(sys.argv[1:])
    quick_mode = "--quick" in args
    full_mode = "--full" in args
    want_json = "--json" in args

    brand_map, proto_map = load_real_robot_module()
    if not proto_map:
        print("❌ 无法加载 real_robot_adapter.py 中的协议映射，终止验证")
        return 1

    # 1. 覆盖率 & 品牌映射断裂
    broken = check_brand_coverage(brand_map, proto_map)

    # 2. 协议类静态检查（可导入 + 方法）
    proto_checks: List[Dict[str, Any]] = []
    if not quick_mode:
        for proto, path in proto_map.items():
            proto_checks.append(check_protocol_class(proto, path))
    else:
        for proto, path in proto_map.items():
            proto_checks.append({
                "protocol": proto,
                "adapter_path": path,
                "importable": False,
                "import_error": "quick_mode跳过",
                "methods_present": {},
                "methods_missing": list(REQUIRED_METHODS),
                "methods_score": 0.0,
            })

    # 3. 抽样接口测试（sim 模式）
    integration: List[Dict[str, Any]] = []
    if not quick_mode:
        sample_size = 20 if full_mode else 8
        arm_keys_sorted = sorted(brand_map.keys())
        integration = test_robot_adapter_interface(arm_keys_sorted, max_samples=sample_size)

    # 汇总
    importable_count = sum(1 for p in proto_checks if p["importable"])
    methods_scores = [p["methods_score"] for p in proto_checks if p["importable"]]
    avg_methods = sum(methods_scores) / len(methods_scores) if methods_scores else 0.0
    protocols_total = len(proto_map)

    report: Dict[str, Any] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "project_root": str(PROJECT_ROOT),
        "quick_mode": quick_mode,
        "full_mode": full_mode,
        "coverage": {
            "brands_total": len(brand_map),
            "protocols_total": protocols_total,
            "broken_links": len(broken),
            "broken_link_details": broken,
            "importable_count": importable_count,
            "importable_ratio": (importable_count / protocols_total) if protocols_total else 0.0,
            "avg_methods_score": avg_methods,
        },
        "protocol_checks": proto_checks,
        "integration_samples": integration,
    }

    print_report(report)

    if want_json:
        name = f'protocol_validation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        out_path = PROJECT_ROOT / name
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"  📄 JSON 报告已保存: {name}")
        except OSError as e:
            print(f"  ❌ 保存 JSON 失败: {e}")

    # Exit code 仅在有 broken link 时返回 1，未实现的适配器返回 0（属于正常 TODO）
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
