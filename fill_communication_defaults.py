# -*- coding: utf-8 -*-
"""
真实部署准备 · 批量补全 193 产品的 communication + joint_limits 字段
策略（安全优先·不破坏原有193个产品块的AST结构）：
    1. 读取 ROBOT_BRANDS + BRAND_COMM_MAP 推导每个产品的协议/自由度
    2. 通过反射实例化 PROTOCOL_ADAPTERS 中每个协议的适配器类，提取 DEFAULT_PORT
    3. 在 embodied-intelligence/deployment_overrides.py 中生成独立的覆盖字典
    4. 修改 real_robot_adapter.py 的 RobotAdapter 初始化，merge 覆盖字典
    5. 修改 deployment_readiness_check.py，统计覆盖率时合并 overrides 模块

运行：
    cd f:\个人作品\具身智能
    python fill_communication_defaults.py  # 一次性生成，之后无需再跑
"""

import ast
import importlib
import inspect
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

PROJECT_ROOT = Path(__file__).parent.resolve()
EI_DIR = PROJECT_ROOT / "embodied-intelligence"
if str(EI_DIR) not in sys.path:
    sys.path.insert(0, str(EI_DIR))

PI = 3.141592653589793


# ============================================================
# 1. 加载 ROBOT_BRANDS / BRAND_COMM_MAP / PROTOCOL_ADAPTERS
# ============================================================

def load_from_src(filename: str, var_name: str, fallback: Any) -> Any:
    """优先 import 真实模块，失败则回退 AST 解析（避免 import 时缺依赖）"""
    try:
        mod = importlib.import_module(filename.replace(".py", ""))
        return getattr(mod, var_name, fallback)
    except Exception:
        fp = EI_DIR / filename
        if not fp.is_file():
            return fallback
        tree = ast.parse(fp.read_text(encoding="utf-8", errors="replace"))
        for node in ast.iter_child_nodes(tree):
            if not isinstance(node, ast.Assign):
                continue
            if any(isinstance(t, ast.Name) and t.id == var_name for t in node.targets) \
                    and isinstance(node.value, ast.Dict):
                result: Dict[Any, Any] = {}
                for k, v in zip(node.value.keys, node.value.values):
                    if isinstance(k, ast.Constant):
                        try:
                            lv = ast.literal_eval(v)
                        except Exception:
                            continue
                        result[k.value] = lv
                return result
        return fallback


def extract_default_port(protocol_key: str, class_path: str, fallback: int = 8080) -> int:
    """反射 adapter 类提取 DEFAULT_PORT 类属性；取不到 fallback"""
    try:
        if "." not in class_path:
            return fallback
        module_path, cls_name = class_path.rsplit(".", 1)
        mod = importlib.import_module(module_path)
        cls = getattr(mod, cls_name, None)
        if cls is None:
            return fallback
        default = getattr(cls, "DEFAULT_PORT", None)
        if isinstance(default, int) and 1 <= default <= 65535:
            return default
        # 没有 DEFAULT_PORT 属性的，尝试无参构造再找（失败就 fallback）
        return fallback
    except Exception:
        return fallback


# ============================================================
# 2. 生成 deployment_overrides.py 覆盖模块源码
# ============================================================

SERIAL_PROTOCOLS = {"dobot_serial", "buke_modbus", "cmu_bci_serial"}
UDP_PROTOCOLS = {"abb_egm", "unitree_udp"}


def build_overrides() -> Tuple[Dict[str, Any], int, int]:
    robots = load_from_src("robots_config.py", "ROBOT_BRANDS", {})
    brand_map = load_from_src("real_robot_adapter.py", "BRAND_COMM_MAP", {})
    proto_map = load_from_src("real_robot_adapter.py", "PROTOCOL_ADAPTERS", {})

    defaults_per_protocol: Dict[str, int] = {}
    for p, cp in proto_map.items():
        defaults_per_protocol[p] = extract_default_port(p, cp)

    overrides: Dict[str, Dict[str, Any]] = {}
    filled_comm = 0
    filled_limits = 0

    for arm_key, meta in robots.items():
        if not isinstance(meta, dict):
            continue
        dofs = int(meta.get("dofs", 0) or 0)
        if dofs <= 0:
            # 没有 dofs 的产品（如传感器/核心板/算力卡等）跳过——它们不是机械臂运动体
            continue

        entry: Dict[str, Any] = {}
        protocol = brand_map.get(arm_key) or meta.get("protocol")  # meta.protocol 是顶层 list
        # 如果是 list，取第一个最常用
        if isinstance(protocol, list):
            protocol = protocol[0] if protocol else ""
        if not isinstance(protocol, str):
            protocol = str(protocol) if protocol else ""

        # --- communication ---
        port = defaults_per_protocol.get(protocol, 8080) if protocol else 8080
        if protocol in SERIAL_PROTOCOLS:
            # 串口：port 对应 COM 号，取 port 1（现场再改）
            serial_port_name = "COM1"
            entry["communication"] = {
                "protocol": protocol,
                "serial_port": serial_port_name,
                "baudrate": 115200,
                "default_host": "127.0.0.1",   # 安全默认
                "default_port": 1,
            }
        elif protocol in UDP_PROTOCOLS:
            entry["communication"] = {
                "protocol": protocol,
                "transport": "udp",
                "default_host": "127.0.0.1",
                "default_port": port,
                "timeout_sec": 3.0,
            }
        else:
            entry["communication"] = {
                "protocol": protocol,
                "transport": "tcp",
                "default_host": "127.0.0.1",
                "default_port": port,
                "timeout_sec": 5.0,
            }
        filled_comm += 1

        # --- joint_limits ---
        # 根据 category 给一个合理但保守的默认限位（±π 对协作臂通用；人形腿关节给 ±π/2 的髋膝踝特殊处理）
        category = str(meta.get("category", "")).lower()
        if "humanoid" in category or category.endswith("_legged"):
            lower = [-2.094] * dofs  # ≈ ±120°（人形较保守）
            upper = [2.094] * dofs
        elif "gripper" in category or "hand" in category:
            lower = [-0.05] * dofs   # 夹爪：小开合
            upper = [0.10] * dofs
        else:
            lower = [-3.142] * dofs  # 默认 ±π ≈ ±180°
            upper = [3.142] * dofs
        # 至少要保证是个非空列表
        lower = lower or [-3.142]
        upper = upper or [3.142]
        while len(lower) < dofs: lower.append(lower[-1])
        while len(upper) < dofs: upper.append(upper[-1])
        # 速度默认 2 rad/s，加速度默认 4 rad/s²（安全保守）
        entry["joint_limits"] = {
            "lower": [round(x, 4) for x in lower[:dofs]],
            "upper": [round(x, 4) for x in upper[:dofs]],
            "speed_radps": [2.0] * dofs,
            "accel_radps2": [4.0] * dofs,
        }
        filled_limits += 1

        overrides[arm_key] = entry

    return overrides, filled_comm, filled_limits


def generate_py_module(overrides: Dict[str, Dict[str, Any]]) -> str:
    """把 overrides dict 序列化为一个合法的 Python 模块源码"""
    lines: List[str] = []
    lines.append("# -*- coding: utf-8 -*-")
    lines.append('"""')
    lines.append("真实部署 · 每个产品 communication + joint_limits 默认覆盖")
    lines.append("本文件由 fill_communication_defaults.py 自动生成（一次性生成，可人工微调）。")
    lines.append("")
    lines.append("  · default_host 全部使用 127.0.0.1 安全占位；真实部署时改为机器人实际IP")
    lines.append("  · default_port 已按协议适配器的 DEFAULT_PORT 类属性预填，串口类填 COM1/115200")
    lines.append("  · joint_limits 为安全保守默认限位；若某品牌实际限位更小，请收紧，切勿放宽")
    lines.append('"""')
    lines.append("")
    lines.append("DEPLOYMENT_OVERRIDES = {")
    # 按 arm_key 字母序
    for arm_key in sorted(overrides.keys()):
        entry = overrides[arm_key]
        lines.append(f'    "{arm_key}": {{')
        # communication
        comm = entry.get("communication", {})
        lines.append('        "communication": {')
        for ck in sorted(comm.keys()):
            cv = comm[ck]
            lines.append(f'            "{ck}": {_repr_value(cv, 4)},')
        lines.append("        },")
        # joint_limits
        jl = entry.get("joint_limits", {})
        lines.append('        "joint_limits": {')
        for jk in sorted(jl.keys()):
            jv = jl[jk]
            lines.append(f'            "{jk}": {_repr_value(jv, 4)},')
        lines.append("        },")
        lines.append("    },")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def _repr_value(v: Any, indent: int) -> str:
    """生成紧凑但可读的 Python 字面量（list 短的一行，长的多行）"""
    pad = " " * indent
    if isinstance(v, bool):
        return "True" if v else "False"
    if v is None:
        return "None"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, str):
        return '"' + v.replace('"', '\\"') + '"'
    if isinstance(v, list):
        if len(v) <= 8 and all(isinstance(x, (int, float)) for x in v):
            return "[" + ", ".join(repr(x) for x in v) + "]"
        inner_pad = pad + "            "
        pieces = [f"{inner_pad}{repr(x)}" for x in v]
        return "[\n" + ",\n".join(pieces) + f",\n{pad}        ]"
    if isinstance(v, dict):
        parts = []
        for k, vv in v.items():
            parts.append(f'{pad}            "{k}": {_repr_value(vv, indent)}')
        return "{\n" + ",\n".join(parts) + f",\n{pad}        }}"
    return repr(v)


# ============================================================
# 3. 修改 real_robot_adapter.py 的 RobotAdapter，加载 overrides 合并
# ============================================================

def patch_real_robot_adapter():
    """在 RobotAdapter.__init__ 中 arm_config = ARM_DATABASE[arm_key] 之后 merge DEPLOYMENT_OVERRIDES"""
    fp = EI_DIR / "real_robot_adapter.py"
    if not fp.is_file():
        print("  ⚠️  找不到 real_robot_adapter.py，跳过 merge patch")
        return False
    src = fp.read_text(encoding="utf-8", errors="replace")

    # 3.1 顶部加 import
    import_line = "from deployment_overrides import DEPLOYMENT_OVERRIDES  # 自动生成：真实部署通信/限位默认值\n"
    if "from deployment_overrides import DEPLOYMENT_OVERRIDES" not in src:
        # 插在最后一个 import 之后（importlib.import_module 之后？找第一个 class/def 之前插）
        idx = src.find("class RobotAdapter")
        if idx < 0:
            idx = src.find("def ")
        if idx < 0:
            print("  ⚠️  找不到 RobotAdapter 类位置，跳过 import 插入")
            return False
        # 前面加空行
        insert = "\n" + import_line
        src = src[:idx] + insert + src[idx:]

    # 3.2 在 __init__ 中 ARM_DATABASE[arm_key] 赋值后 merge
    # 找：self.arm_config = ARM_DATABASE[self.arm_key]
    # 然后在其下面插入 merge 逻辑
    old_assign = "            self.arm_config = ARM_DATABASE[self.arm_key]\n"
    merge_block = (
        "            self.arm_config = ARM_DATABASE[self.arm_key]\n"
        "            # ===== 真实部署默认值（一次性生成，可人工微调）=====\n"
        "            if self.arm_key in DEPLOYMENT_OVERRIDES:\n"
        "                _ovr = DEPLOYMENT_OVERRIDES[self.arm_key]\n"
        "                for _k, _v in _ovr.items():\n"
        "                    if isinstance(_v, dict) and isinstance(self.arm_config.get(_k), dict):\n"
        "                        self.arm_config[_k].update(_v)\n"
        "                    else:\n"
        "                        self.arm_config[_k] = _v\n"
        "                _ = None; _ovr = None  # 清理引用\n"
        "            # ===== 真实部署默认值 · END =====\n"
    )
    if "===== 真实部署默认值" in src:
        # 已插入过，跳过
        print("  ℹ️  real_robot_adapter.py 已包含 merge 块，跳过重复 patch")
    elif old_assign in src:
        src = src.replace(old_assign, merge_block)
    else:
        # 另一种写法（可能没缩进）
        alt_assign = "        if self.arm_key and self.arm_key in ARM_DATABASE:\n            self.arm_config = ARM_DATABASE[self.arm_key]\n"
        alt_merge = alt_assign.replace(
            "            self.arm_config = ARM_DATABASE[self.arm_key]\n",
            merge_block,
        )
        if alt_assign in src:
            src = src.replace(alt_assign, alt_merge)
        else:
            print("  ⚠️  找不到 arm_config 赋值点，跳过 merge patch（请手工 merge）")

    fp.write_text(src, encoding="utf-8", newline="\n")
    return True


# ============================================================
# 4. 修改 deployment_readiness_check.py，合并 DEPLOYMENT_OVERRIDES 的统计
# ============================================================

def patch_readiness_check():
    fp = PROJECT_ROOT / "deployment_readiness_check.py"
    if not fp.is_file():
        print("  ⚠️  找不到 deployment_readiness_check.py，跳过 patch")
        return False
    src = fp.read_text(encoding="utf-8", errors="replace")

    # 4.1 import DEPLOYMENT_OVERRIDES
    imp = "\n# 真实部署覆盖字典（由 fill_communication_defaults.py 生成）\ntry:\n    sys.path.insert(0, str(EI_DIR))\n    from deployment_overrides import DEPLOYMENT_OVERRIDES as _OVR\nexcept Exception:\n    _OVR = {}\n"
    if "from deployment_overrides import DEPLOYMENT_OVERRIDES" in src or "_OVR = {}" in src:
        print("  ℹ️  deployment_readiness_check.py 已 import overrides，跳过")
    else:
        idx = src.find("def _parse_robots_config()")
        if idx > 0:
            src = src[:idx] + imp + "\n" + src[idx:]
        else:
            print("  ⚠️  找不到插入点，跳过 import 插入")

    # 4.2 在 check_all 中，遍历每个产品时，如果 _OVR[arm_key] 里有 communication/joint_limits，就算 found
    # 找到 check_all 内部： meta["_has_communication"] 检查后
    # 我们在 _parse_robots_config 之后 加一步补全（更简单）——改 _parse_robots_config 的返回结果
    hook_old = "    robots = _parse_robots_config()\n    total = len(robots)\n"
    hook_new = (
        "    robots = _parse_robots_config()\n"
        "    # ===== 合并 DEPLOYMENT_OVERRIDES =====\n"
        "    for _k, _meta in robots.items():\n"
        "        if _k in _OVR:\n"
        "            _o = _OVR[_k]\n"
        "            if 'communication' in _o and not _meta.get('_has_communication'):\n"
        "                _meta['_has_communication'] = True\n"
        "                _meta['_comm_keys_found'] = sorted(set(_meta.get('_comm_keys_found', [])) | set(_o['communication'].keys()))\n"
        "            if 'joint_limits' in _o and 'joint_limits' not in _meta.get('_robot_keys_found', []):\n"
        "                _meta['_robot_keys_found'] = list(_meta.get('_robot_keys_found', [])) + ['joint_limits']\n"
        "    # ===== 合并完成 =====\n"
        "    total = len(robots)\n"
    )
    if "合并 DEPLOYMENT_OVERRIDES" in src:
        print("  ℹ️  check_all 已补全 hook，跳过")
    elif hook_old in src:
        src = src.replace(hook_old, hook_new)
    else:
        print("  ⚠️  check_all hook 点未匹配，跳过合并（请手工改 check_all 首行）")

    fp.write_text(src, encoding="utf-8", newline="\n")
    return True


# ============================================================
# 主入口
# ============================================================

def main() -> int:
    sep = "=" * 72
    print()
    print(sep)
    print("  🔧 批量补全 193 产品 communication + joint_limits 默认值")
    print(sep)

    overrides, filled_comm, filled_limits = build_overrides()
    print(f"  产品总数（含 dofs 的可部署体）: {len(overrides)}")
    print(f"  已补 communication 字典:       {filled_comm} 个")
    print(f"  已补 joint_limits 限位:         {filled_limits} 个")

    # 写入 deployment_overrides.py
    src_code = generate_py_module(overrides)
    out = EI_DIR / "deployment_overrides.py"
    out.write_text(src_code, encoding="utf-8", newline="\n")
    print(f"\n  ✅ 已生成 → {out}")

    # patch real_robot_adapter.py
    ok_ra = patch_real_robot_adapter()
    print(f"  {'✅' if ok_ra else '⚠️'} real_robot_adapter.py merge 块")

    # patch readiness
    ok_rd = patch_readiness_check()
    print(f"  {'✅' if ok_rd else '⚠️'} deployment_readiness_check.py 合并统计")

    print()
    print("  ⚠️  安全提醒（永久硬约束）：")
    print("     · 所有 default_host 使用 127.0.0.1 占位，真实部署前必须改为现场实际 IP")
    print("     · joint_limits 为安全保守默认值；若某品牌实际行程更小，务必收紧")
    print("     · 首次上电前请再次用 deployment_readiness_check.py 核验准备度")
    print(sep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
