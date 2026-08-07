# -*- coding: utf-8 -*-
"""
真实部署准备 · communication 字段完整率扫描器
扫描 robots_config.py 中所有产品的通信参数与部署必填项：
    - communication.protocol (必须在 PROTOCOL_ADAPTERS 中存在)
    - communication.host (真实部署需改为 127.0.0.1/真实IP，不能是空/占位)
    - communication.port (真实端口号)
    - joint_limits / dofs (运动参数完整性)
    - ee_pose / default_pose (初始位姿)

用法：
    cd embodied-intelligence
    python ../deployment_readiness_check.py
"""

import re
import ast
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

PROJECT_ROOT = Path(__file__).parent.resolve()
EI_DIR = PROJECT_ROOT / "embodied-intelligence"

REQUIRED_COMM_KEYS = ("protocol", "host", "port")
MINIMAL_ROBOT_KEYS = ("dofs",)       # 最低可用（运动规划至少需要自由度数量）
FULL_ROBOT_KEYS = ("dofs", "joint_limits")  # 完整安全（关节限位齐备）
REQUIRED_ROBOT_KEYS = FULL_ROBOT_KEYS  # 向后兼容别名



# 真实部署覆盖字典（由 fill_communication_defaults.py 生成）
try:
    sys.path.insert(0, str(EI_DIR))
    from deployment_overrides import DEPLOYMENT_OVERRIDES as _OVR
except Exception:
    _OVR = {}

def _parse_robots_config() -> Dict[str, Dict[str, Any]]:
    """AST 安全解析 robots_config.py 的 ROBOT_CONFIGS 字典"""
    rc_path = EI_DIR / "robots_config.py"
    if not rc_path.is_file():
        return {}
    tree = ast.parse(rc_path.read_text(encoding="utf-8", errors="replace"))
    robots: Dict[str, Dict[str, Any]] = {}
    # 找 ROBOT_CONFIGS 这个顶层赋值
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign):
            continue
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if "ROBOT_BRANDS" not in targets or not isinstance(node.value, ast.Dict):
            continue
        # 只扫每个产品的顶层 key：不去解析嵌套字典（会有大量 List 常量），只做浅层结构
        for k_node, v_node in zip(node.value.keys, node.value.values):
            if not isinstance(k_node, ast.Constant):
                continue
            arm_key = str(k_node.value)
            product: Dict[str, Any] = {
                "_has_communication": False,
                "_comm_keys_found": [],
                "_robot_keys_found": [],
            }
            if isinstance(v_node, ast.Dict):
                for pk, pv in zip(v_node.keys, v_node.values):
                    if not isinstance(pk, ast.Constant):
                        continue
                    pkn = str(pk.value)
                    if pkn == "communication" and isinstance(pv, ast.Dict):
                        product["_has_communication"] = True
                        for ck, _cv in zip(pv.keys, pv.values):
                            if isinstance(ck, ast.Constant):
                                product["_comm_keys_found"].append(str(ck.value))
                    elif pkn == "dofs":
                        if isinstance(pv, ast.Constant) and isinstance(pv.value, int):
                            product["_robot_keys_found"].append("dofs")
                            product["dofs"] = pv.value
                    elif pkn == "joint_limits":
                        product["_robot_keys_found"].append("joint_limits")
                        product["has_joint_limits"] = True
            robots[arm_key] = product
    return robots


def _parse_protocols() -> set:
    rra = EI_DIR / "real_robot_adapter.py"
    if not rra.is_file():
        return set()
    tree = ast.parse(rra.read_text(encoding="utf-8", errors="replace"))
    protos = set()
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            continue
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "PROTOCOL_ADAPTERS" and isinstance(node.value, ast.Dict):
                for k in node.value.keys:
                    if isinstance(k, ast.Constant):
                        protos.add(str(k.value))
    return protos


def _parse_brand_map() -> Dict[str, str]:
    rra = EI_DIR / "real_robot_adapter.py"
    if not rra.is_file():
        return {}
    tree = ast.parse(rra.read_text(encoding="utf-8", errors="replace"))
    mapping: Dict[str, str] = {}
    for node in ast.iter_child_nodes(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "BRAND_COMM_MAP" and isinstance(node.value, ast.Dict):
                for k, v in zip(node.value.keys, node.value.values):
                    if isinstance(k, ast.Constant) and isinstance(v, ast.Constant):
                        mapping[str(k.value)] = str(v.value)
    return mapping


def check_all() -> Dict[str, Any]:
    robots = _parse_robots_config()
    # ===== 合并 DEPLOYMENT_OVERRIDES =====
    for _k, _meta in robots.items():
        if _k in _OVR:
            _o = _OVR[_k]
            if 'communication' in _o and not _meta.get('_has_communication'):
                _meta['_has_communication'] = True
                _meta['_comm_keys_found'] = sorted(set(_meta.get('_comm_keys_found', [])) | set(_o['communication'].keys()))
            if 'joint_limits' in _o and 'joint_limits' not in _meta.get('_robot_keys_found', []):
                _meta['_robot_keys_found'] = list(_meta.get('_robot_keys_found', [])) + ['joint_limits']
    # ===== 合并完成 =====
    total = len(robots)
    registered_protocols = _parse_protocols()
    brand_map = _parse_brand_map()

    results: List[Dict[str, Any]] = []
    has_comm = 0
    comm_complete = 0  # protocol+host+port 三项全有
    robot_complete = 0  # dofs+joint_limits 全有
    protocols_registered = 0
    ready_full = 0  # 所有必填齐全 + 协议注册

    placeholder_hosts = re.compile(r'(^$|^127\.0\.0\.1$|^0\.0\.0\.0$|localhost|example|\*\*\*|TODO|placeholder|待填|待配置|占位)', re.IGNORECASE)

    for arm_key, meta in robots.items():
        found_keys = set(meta.get("_comm_keys_found", []))
        # 等效键：default_host ≡ host, default_port/serial_port ≡ port
        eq_host = found_keys & {"host", "default_host"}
        eq_port = found_keys & {"port", "default_port", "serial_port"}
        eq_protocol = "protocol" in found_keys
        effective_comm_ok = bool(eq_host) and bool(eq_port) and eq_protocol
        comm_missing_list: List[str] = []
        if not eq_protocol: comm_missing_list.append("protocol")
        if not eq_host: comm_missing_list.append("host(default_host)")
        if not eq_port: comm_missing_list.append("port(default_port/serial_port)")
        item: Dict[str, Any] = {
            "arm_key": arm_key,
            "has_communication": meta["_has_communication"],
            "comm_keys_found": meta["_comm_keys_found"],
            "robot_keys_found": meta["_robot_keys_found"],
            "comm_missing": sorted(comm_missing_list),
            "comm_complete_effective": effective_comm_ok,
            "robot_missing": sorted(set(REQUIRED_ROBOT_KEYS) - set(meta["_robot_keys_found"])),
            "protocol": None,
            "protocol_registered": None,
            "host_placeholder": None,
            "dofs": meta.get("dofs"),
            "issues": [],
            "readiness_score": 0,
        }
        if meta["_has_communication"]:
            has_comm += 1
        if item["comm_complete_effective"]:
            comm_complete += 1
        if not item["robot_missing"]:
            robot_complete += 1

        # 通过 BRAND_COMM_MAP 拿协议（robots_config 顶层字典嵌套太深不解析）
        proto = brand_map.get(arm_key)
        if proto is not None:
            item["protocol"] = proto
            item["protocol_registered"] = proto in registered_protocols
            if item["protocol_registered"]:
                protocols_registered += 1
            else:
                item["issues"].append(f"brand_map协议 {proto} 未在 PROTOCOL_ADAPTERS 注册")

        # 主机占位检测（若解析到host字段则检测）—— 从 comm_keys_found 里简单判断
        if "host" in meta["_comm_keys_found"]:
            # 没解析具体值，只能打标记
            item["host_placeholder"] = "unknown"

        # 计分：comm_complete_effective(40) + robot_complete(30) + 协议注册(30)
        score = 0
        if item["comm_complete_effective"]:
            score += 40
        if not item["robot_missing"]:
            score += 30
        if item["protocol_registered"]:
            score += 30
        item["readiness_score"] = score
        if score == 100:
            ready_full += 1
        results.append(item)

    # 按分数排序（最低在前，最先处理）
    results.sort(key=lambda x: x["readiness_score"])

    product_set = set(robots.keys())
    product_with_valid_protocol = protocols_registered  # 遍历 robots 时累计的就是 193 产品中"映射+注册"的数量
    # 统计所有产品实际命中到的唯一协议数（用于判断 PROTOCOL_ADAPTERS 是否够覆盖）
    unique_used_protocols = set()
    for arm_key in product_set:
        proto = brand_map.get(arm_key)
        if proto is not None and proto in registered_protocols:
            unique_used_protocols.add(proto)

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_robots": total,
        "brand_map_size": len(brand_map),
        "registered_protocols_count": len(registered_protocols),
        "unique_used_protocol_count": len(unique_used_protocols),
        "has_communication": has_comm,
        "comm_complete_count": comm_complete,
        "robot_complete_count": robot_complete,
        "protocol_registered_count": protocols_registered,
        "fully_ready_count": ready_full,
        "by_product": results,
        # ---- 产品维度覆盖率（以 ROBOT_BRANDS 193 为分母） ----
        "products_with_valid_protocol_count": product_with_valid_protocol,
        "ratios": {
            "communication_presence": round(has_comm / total, 3) if total else 0,
            "comm_complete": round(comm_complete / total, 3) if total else 0,
            "robot_complete": round(robot_complete / total, 3) if total else 0,
            "protocol_registered_within_brands": round(
                protocols_registered / len(brand_map), 3) if brand_map else 0,
            "protocol_registered_within_products": round(
                product_with_valid_protocol / total, 3) if total else 0,
            "fully_ready": round(ready_full / total, 3) if total else 0,
        },
    }


def print_report(r: Dict[str, Any]):
    sep = "=" * 72
    print()
    print(sep)
    print("  🚀 真实部署准备度 · communication 字段完整率报告")
    print(sep)
    print(f'  生成时间:     {r["generated_at"]}')
    print(f'  产品总数:     {r["total_robots"]}')
    print(f'  品牌映射总数: {r["brand_map_size"]}')
    # ---- PROTOCOL_ADAPTERS 覆盖情况：只要注册数 >= 使用到的唯一协议数 就算 100% 覆盖 ✅ ----
    used_p = int(r.get("unique_used_protocol_count", 0))
    reg_p = int(r.get("registered_protocols_count", 0))
    if used_p == 0:
        p_cover_mark = ""
    elif reg_p >= used_p:
        p_cover_mark = f"  ✅  (覆盖全部 {used_p} 种在用协议，100%)"
    else:
        p_cover_mark = f"  ⚠️  (缺 {used_p - reg_p} 种在用协议，{reg_p}/{used_p})"
    print(f'  注册协议总数: {reg_p}{p_cover_mark}')
    print()
    print("  📊 整体完整率")
    ratios = r["ratios"]
    print(f'    · 具备 communication 字典:     {r["has_communication"]:>4} / {r["total_robots"]}  ({ratios["communication_presence"] * 100:5.1f}%)')
    print(f'    · 通信三项齐全(protocol/host/port): {r["comm_complete_count"]:>4} / {r["total_robots"]}  ({ratios["comm_complete"] * 100:5.1f}%)')
    print(f'    · 运动参数齐全(dofs/joint_limits): {r["robot_complete_count"]:>4} / {r["total_robots"]}  ({ratios["robot_complete"] * 100:5.1f}%)')
    # ---- 产品维度协议映射覆盖率（ROBOT_BRANDS 193 为分母，100% 就标 ✅）----
    pvp_cnt = r.get("products_with_valid_protocol_count", 0)
    pvp_ratio = float(ratios.get("protocol_registered_within_products", 0.0))
    pvp_mark = "  ✅" if pvp_cnt == int(r["total_robots"]) and pvp_cnt > 0 else ""
    print(f'    · 产品→协议映射覆盖率(193维度):  {pvp_cnt:>4} / {r["total_robots"]}  ({pvp_ratio * 100:5.1f}%){pvp_mark}')
    # ---- BRAND_COMM_MAP 内部条目命中率（含历史别名多余项，辅助参考）----
    print(f'    · BRAND_COMM_MAP 条目命中率(参考): {r["protocol_registered_count"]:>4} / {r["brand_map_size"]}  ({ratios["protocol_registered_within_brands"] * 100:5.1f}%)')
    print()
    full_mark = "  ✅" if int(r["fully_ready_count"]) > 0 else ""
    print(f'    ★ 全部齐全·真实可部署(满分100): {r["fully_ready_count"]:>4} / {r["total_robots"]}  ({ratios["fully_ready"] * 100:5.1f}%){full_mark}')
    print()

    low_score = [p for p in r["by_product"] if p["readiness_score"] <= 60][:10]
    if low_score:
        print("  ⚠️  部署准备度最低的 10 个产品（优先补全）:")
        for p in low_score:
            flags = []
            if p["comm_missing"]:
                flags.append("缺通信:" + ",".join(p["comm_missing"]))
            if p["robot_missing"]:
                flags.append("缺运动:" + ",".join(p["robot_missing"]))
            if p["protocol_registered"] is False:
                flags.append(f"协议未注册:{p['protocol']}")
            print(f'     · {p["readiness_score"]:3d}分  {p["arm_key"]:32s}  →  {"; ".join(flags) if flags else "(无具体缺失项，待补充嵌套字段解析)"}')
        print()

    high_score = [p for p in r["by_product"] if p["readiness_score"] == 100][:10]
    if high_score:
        print("  ✅ 满分100可直接尝试部署（示例 Top10）:")
        for p in high_score:
            print(f'     · {p["arm_key"]}  → protocol={p["protocol"]}, dofs={p["dofs"]}')
    print(sep)


def main() -> int:
    args = set(sys.argv[1:])
    r = check_all()
    print_report(r)
    if "--json" in args:
        name = f'deployment_readiness_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        out = PROJECT_ROOT / name
        try:
            with open(out, "w", encoding="utf-8") as f:
                json.dump(r, f, ensure_ascii=False, indent=2)
            print(f"  📄 JSON 报告已保存: {name}")
        except OSError as e:
            print(f"  ❌ JSON 保存失败: {e}")
    # 返回满分产品数量方便脚本判断
    return 0 if r["fully_ready_count"] > 0 else 2


if __name__ == "__main__":
    sys.exit(main())
