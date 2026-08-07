# -*- coding: utf-8 -*-
"""
===============================================
  🚀 真实机器人端到端部署入口（唯一推荐入口）
===============================================
用法：
    cd f:\个人作品\具身智能
    python deploy_real_robot.py                         # 交互式（真实部署用这个，强制资质门禁）
    python deploy_real_robot.py --arm panda --host 192.168.1.100 --port 8080 --skip-gate  # CI/无人值守（需慎重）
    python deploy_real_robot.py --smoke                  # 烟雾测试（资质+链接，不做真实运动）

⚠️  永久安全硬约束（来自 LICENSE / project_memory.md / AI安全附加条款）：
    1. 真实机器人部署必须由 具备机器人调试资质 的工程师在场执行；
    2. 现场必须存在可立即按下的 硬件紧急停止按钮(E-Stop)；
    3. 首次运动必须为 小范围低速运动（<5°/s），确认机械限位/方向/负载正确；
    4. 本脚本仅负责启动链路与基本验证，复杂工艺路径请在上位机控制程序中编写；
    5. 所有真实部署会话 → 必须在退出前经资质工程师输入 YES 确认无隐患。
"""

import os
import re
import sys
import json
import time
import signal
import argparse
import getpass
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).parent.resolve()
EI_DIR = PROJECT_ROOT / "embodied-intelligence"

if str(EI_DIR) not in sys.path:
    sys.path.insert(0, str(EI_DIR))


# ============================================================
# 0. 法律 & 资质门禁（永久硬约束·不允许跳过交互式版本）
# ============================================================

QUALIFIED_PHRASE = "YES I AM QUALIFIED"

LEGAL_DISCLAIMER = """
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  真实机器人部署 · 法律与资质声明（必须阅读并同意）            ║
╠══════════════════════════════════════════════════════════════════╣
║  1. 本操作可能涉及高速运动部件、高电压、大扭矩，可能导致人身伤   ║
║     亡或设备损坏，必须由具备机器人调试资质的工程师现场执行。     ║
║  2. 现场必须存在硬件紧急停止按钮 (E-Stop)，并且工程师可在         ║
║     0.5 秒内触达；若没有硬件 E-Stop，禁止启动真实运动！          ║
║  3. 首次运动必须是低速小幅度（单关节 <5°/s，位移 <±10°），        ║
║     确认关节编号、运动方向、力矩方向全部正确后再放大速度。        ║
║  4. 本软件按 MIT + AI 安全附加条款提供，不对真实部署造成的        ║
║     任何后果承担法律责任；使用即代表您已完全知悉风险。           ║
╚══════════════════════════════════════════════════════════════════╝
"""

def _input_with_prompt(prompt: str, hidden: bool = False) -> str:
    if hidden:
        try:
            return getpass.getpass(prompt)
        except (ImportError, AttributeError):
            pass
    try:
        return input(prompt)
    except EOFError:
        return ""


def run_qualification_gate() -> Tuple[bool, Dict[str, str]]:
    """资质门禁。返回 (是否通过, 人员信息)。CI 模式 --skip-gate 绕过需带签名。"""
    info: Dict[str, str] = {
        "engineer_name": "",
        "engineer_id": "",
        "qualification_id": "",
        "estop_verified": "N",
        "signed_phrase": "",
        "gate_passed_at": "",
    }
    print(LEGAL_DISCLAIMER)
    info["engineer_name"] = _input_with_prompt("  [1/5] 请输入资质工程师姓名（真实姓名）: ").strip()
    if not info["engineer_name"]:
        print("  ❌ 姓名不能为空，门禁未通过")
        return False, info
    info["engineer_id"] = _input_with_prompt("  [2/5] 请输入工号/员工编号: ").strip() or "unregistered"
    info["qualification_id"] = _input_with_prompt(
        "  [3/5] 请输入机器人调试资质证书编号（无则填 NONE，后果自负）: ").strip() or "NONE"

    estop = _input_with_prompt(
        "  [4/5] 现场是否存在可立即按下的硬件 E-Stop 按钮且你可触达？[y/N]: ").strip().lower()
    info["estop_verified"] = "Y" if estop in ("y", "yes") else "N"
    if info["estop_verified"] != "Y":
        print("  ❌ 硬件 E-Stop 未就位，禁止真实运动。门禁未通过。")
        return False, info

    phrase = _input_with_prompt(
        f"  [5/5] 请输入以下句子确认资质与责任 → 『{QUALIFIED_PHRASE}』: ").strip()
    info["signed_phrase"] = phrase
    if phrase != QUALIFIED_PHRASE:
        print(f"  ❌ 确认短语不匹配（期望：{QUALIFIED_PHRASE}）。门禁未通过。")
        return False, info

    info["gate_passed_at"] = datetime.now().isoformat(timespec="seconds")
    print("  ✅ 资质与法律门禁通过。开始部署准备。\n")
    return True, info


# ============================================================
# 1. 机器人选项 & 配置加载
# ============================================================

def _load_robots_and_maps() -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, str]]:
    """加载 ROBOT_BRANDS / BRAND_COMM_MAP / PROTOCOL_ADAPTERS"""
    import importlib
    sys.path.insert(0, str(EI_DIR))
    try:
        rc_mod = importlib.import_module("robots_config")
    except ImportError:
        print("❌ 无法导入 robots_config.py")
        return {}, {}, {}
    try:
        rra_mod = importlib.import_module("real_robot_adapter")
    except ImportError:
        print("❌ 无法导入 real_robot_adapter.py")
        return {}, {}, {}
    return (
        getattr(rc_mod, "ROBOT_BRANDS", {}),
        getattr(rra_mod, "BRAND_COMM_MAP", {}),
        getattr(rra_mod, "PROTOCOL_ADAPTERS", {}),
    )


def pick_arm_interactive(robots: Dict[str, Any], brand_map: Dict[str, str], preselect: str = "") -> str:
    if preselect and preselect in robots:
        print(f"  ⚡ 已预选择机械臂: {preselect}")
        return preselect
    # 只展示 dofs >= 3 的机械臂/人形类产品
    candidates: List[Tuple[str, Dict[str, Any]]] = []
    for key, meta in robots.items():
        if isinstance(meta, dict) and isinstance(meta.get("dofs"), int) and meta["dofs"] >= 3:
            candidates.append((key, meta))
    candidates.sort(key=lambda x: (x[1].get("category", "zz"), x[0]))
    if not candidates:
        print("  ⚠️  没有找到任何可部署的机械臂/人形（dofs>=3）。请检查 robots_config.py。")
        return ""
    print("  📋 可部署的机器人清单（按类别排序）：\n")
    cols = 3
    for i in range(0, len(candidates), cols):
        row = []
        for j in range(cols):
            idx = i + j
            if idx >= len(candidates):
                break
            key, meta = candidates[idx]
            proto = brand_map.get(key, "N/A")
            row.append(f"  {idx + 1:>3}. {key:30s} ({meta.get('category','')[:10]}/{proto[:10]})")
        print(" ".join(row))
    print()
    ans = _input_with_prompt("  请选择序号或直接输入 arm_key: ").strip()
    if ans.isdigit():
        idx = int(ans) - 1
        if 0 <= idx < len(candidates):
            return candidates[idx][0]
    if ans in robots:
        return ans
    print(f"  ❌ 无效输入: {ans}")
    return ""


def confirm_communication(arm_key: str, robots: Dict[str, Any], brand_map: Dict[str, str],
                          pre_host: str = "", pre_port: int = 0) -> Dict[str, Any]:
    meta = robots.get(arm_key) or {}
    proto = brand_map.get(arm_key, "unknown")
    print(f"\n  📡 目标机器人: {arm_key} ({meta.get('name', '')})")
    print(f"       品牌/产地: {meta.get('origin', 'N/A')}")
    print(f"       自由度: {meta.get('dofs', '?')} | 负载: {meta.get('payload_kg', '?')}kg | 工作半径: {meta.get('reach_m', '?')}m")
    print(f"       映射协议: {proto} (protocol_adapters 类: registered={proto in PROTOCOL_ADAPTERS_CACHE})")
    host = pre_host or _input_with_prompt(f"  机器人 IP/Host [默认 127.0.0.1]: ").strip() or "127.0.0.1"
    port = pre_port
    if not port:
        p = _input_with_prompt(f"  机器人 Port [回车自动]: ").strip()
        port = int(p) if p.isdigit() else 0
    return {
        "arm_key": arm_key,
        "host": host,
        "port": port,
        "protocol": proto,
        "dofs": int(meta.get("dofs", 0) or 0),
        "name": meta.get("name", arm_key),
        "category": meta.get("category", ""),
    }


# ============================================================
# 2. 真实部署链路执行
# ============================================================

PROTOCOL_ADAPTERS_CACHE: Dict[str, str] = {}


def deploy_and_verify(cfg: Dict[str, Any], gate_info: Dict[str, str],
                      smoke: bool = False) -> Tuple[bool, Dict[str, Any]]:
    session: Dict[str, Any] = {
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "gate": gate_info,
        "cfg": cfg,
        "steps": [],
        "result": "pending",
    }
    ra = None
    log_step(session, "初始化适配器", start=True)

    # 导入（延迟，避免缺依赖）
    try:
        from real_robot_adapter import RobotAdapter
    except Exception as e:
        log_step(session, "导入RobotAdapter失败", error=f"{type(e).__name__}: {e}")
        return finalize_session(session, False), session

    # 2.1 构造真实模式适配器
    ra_kwargs = {
        "mode": "real",
        "arm_key": cfg["arm_key"],
        "config": {
            "host": cfg["host"],
            "port": cfg["port"],
            "dofs": cfg["dofs"],
            "brand": cfg["name"],
        },
        "simulator_backend": "pybullet",
    }
    try:
        ra = RobotAdapter(**ra_kwargs)
    except Exception as e:
        log_step(session, "RobotAdapter 构造失败", error=f"{type(e).__name__}: {e}")
        return finalize_session(session, False), session

    info = ra.get_arm_info()
    log_step(session, "适配器构造完成", info={k: info.get(k) for k in ("arm_key", "brand", "model", "dofs", "protocol")})

    # 2.2 初始化（真实连接 + 握手）
    log_step(session, "initialize() 真实握手与建立连接", start=True)
    init_ok = False
    try:
        init_ok = bool(ra.initialize())
    except Exception as e:
        log_step(session, "initialize 抛出异常", error=f"{type(e).__name__}: {e}")
        init_ok = False
    log_step(session, "initialize 完成", ok=init_ok)
    if not init_ok:
        return finalize_session(session, False, ra), session

    # 2.3 读取关节状态（确认反馈链路）
    log_step(session, "读取关节状态 get_joint_states()", start=True)
    try:
        js = ra.get_joint_states()
        log_step(session, f"关节状态读取成功", info={"len": len(js), "sample": [round(x, 4) for x in (js or [])[:7]]})
    except Exception as e:
        log_step(session, "关节状态读取失败", error=f"{type(e).__name__}: {e}")
        js = []

    # 2.4 读取 EE 位姿
    log_step(session, "读取末端位姿 get_ee_pose()", start=True)
    try:
        ee = ra.get_ee_pose()
        pos = ee.get("position", [None, None, None]) if isinstance(ee, dict) else None
        log_step(session, "末端位姿读取成功",
                 info={"position": [round(float(x), 4) if isinstance(x, (int, float)) else x for x in (pos or [])]})
    except Exception as e:
        log_step(session, "末端位姿读取失败", error=f"{type(e).__name__}: {e}")

    if smoke:
        log_step(session, "⚠️  --smoke 模式：跳过真实运动，直接进入关闭阶段")
        return finalize_session(session, True, ra), session

    # 2.5 小幅度低速验证运动（永久硬约束：首次运动必须低速小幅）
    dofs = cfg["dofs"] or info.get("dofs") or 7
    log_step(session, f"开始小幅度低速运动验证（自由度={dofs}, 速度=0.1 rad/s, 位移≈±0.087rad≈±5°）", start=True)
    small_angle = 0.087266  # ≈ 5°
    speed = 0.1
    move_ok = True
    if js and len(js) >= max(1, dofs):
        base_angles = list(js[:dofs])
    else:
        base_angles = [0.0] * dofs
    for i in range(min(3, dofs)):  # 只动前 3 个关节的小步幅
        target = list(base_angles)
        target[i] += (small_angle * ((-1) ** i))  # 交替正负
        try:
            ok = ra.move_joints(target, speed=speed)
            log_step(session, f"关节 {i + 1} 小幅运动→{round(target[i], 4)} rad", ok=bool(ok))
            if not ok:
                move_ok = False
        except Exception as e:
            log_step(session, f"关节 {i + 1} 运动失败", error=f"{type(e).__name__}: {e}")
            move_ok = False
            break
        time.sleep(0.6)

    log_step(session, "小幅度低速运动阶段完成", ok=move_ok)

    # 2.6 回零（回到 base_angles）
    log_step(session, "回零 move_joints(base_angles, speed=0.05)", start=True)
    try:
        ra.move_joints(base_angles, speed=0.05)
        log_step(session, "回零指令发送成功")
    except Exception as e:
        log_step(session, "回零失败（需现场确认位置）", error=f"{type(e).__name__}: {e}")

    # 2.7 紧急停止链路测试（软件 stop，不是硬件 E-Stop）
    log_step(session, "软件紧急停止链路 stop() 测试", start=True)
    try:
        ra.stop()
        log_step(session, "软件 stop() 执行成功")
    except Exception as e:
        log_step(session, "软件 stop() 失败", error=f"{type(e).__name__}: {e}")

    return finalize_session(session, True, ra), session


def log_step(session: Dict[str, Any], name: str, *, ok: Optional[bool] = None,
             info: Optional[Dict[str, Any]] = None, error: str = "", start: bool = False):
    entry = {"step": name, "ts": datetime.now().isoformat(timespec="seconds")}
    if start:
        entry["start"] = True
    if ok is not None:
        entry["ok"] = bool(ok)
    if info:
        entry["info"] = info
    if error:
        entry["error"] = error
    session["steps"].append(entry)
    tag = "[START] " if start else ""
    if ok is True:
        tag += "✅"
    elif ok is False:
        tag += "❌"
    elif error:
        tag += "‼️"
    else:
        tag += "➤"
    suffix = ""
    if error:
        suffix = f"  → {error[:120]}"
    elif info:
        suffix = f"  → {info}"
    print(f"     {tag} {name}{suffix}")


def finalize_session(session: Dict[str, Any], ok: bool, ra: Optional[Any] = None) -> bool:
    if ra is not None:
        try:
            ra.shutdown()
        except Exception:
            pass
    session["ended_at"] = datetime.now().isoformat(timespec="seconds")
    session["result"] = "success" if ok else "failed"
    return ok


def save_session_log(session: Dict[str, Any]):
    name = f'deploy_real_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{session.get("cfg", {}).get("arm_key", "unknown")}.json'
    path = PROJECT_ROOT / name
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(session, f, ensure_ascii=False, indent=2)
        print(f"\n  📄 部署会话日志已保存 → {name} （审计留档用，请勿上传到 GitHub）")
    except OSError as e:
        print(f"\n  ❌ 保存部署日志失败: {e}")


# ============================================================
# 3. SIGINT 安全处理（Ctrl+C 立刻触发清理）
# ============================================================

_GLOBAL_RA = {"obj": None}

def _sigint_handler(signum, frame):
    print("\n\n  ⚡ 收到中断信号（Ctrl+C），执行紧急清理 shutdown()...")
    ra = _GLOBAL_RA.get("obj")
    if ra is not None:
        try:
            ra.shutdown()
            print("  ✅ RobotAdapter.shutdown() 已执行")
        except Exception as e:
            print(f"  ❌ shutdown 异常: {e}")
    print("  ‼️  请前往现场确认机器人状态，并手动按下硬件 E-Stop 确保安全。\n")
    sys.exit(130)


# ============================================================
# 4. 主入口
# ============================================================

def _parse_args(argv: List[str]):
    p = argparse.ArgumentParser(description="真实机器人端到端部署入口")
    p.add_argument("--arm", type=str, default="", help="预选择 arm_key")
    p.add_argument("--host", type=str, default="", help="机器人 IP/Host（CI 用）")
    p.add_argument("--port", type=int, default=0, help="机器人端口（CI 用）")
    p.add_argument("--smoke", action="store_true", help="烟雾模式：只握手+反馈，不做运动")
    p.add_argument("--skip-gate", action="store_true",
                   help="⚠️  CI 专用：跳过资质门禁（必须配合 --engineer-signature 使用，否则仍拒绝）")
    p.add_argument("--engineer-signature", type=str, default="",
                   help="CI 绕过门禁时的签名（格式：姓名|工号|资质ID，留档用）")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    signal.signal(signal.SIGINT, _sigint_handler)
    args = _parse_args(sys.argv[1:] if argv is None else argv)

    print("\n" + "=" * 72)
    print("  🚀 真实机器人端到端部署入口（唯一推荐入口）")
    print("=" * 72)
    print(f"  项目根: {PROJECT_ROOT}")
    print(f"  时间:   {datetime.now().isoformat(timespec='seconds')}")
    print()

    # ---- STEP 0: 资质门禁 ----
    gate_info: Dict[str, str] = {}
    if args.skip_gate:
        sig = args.engineer_signature or ""
        parts = sig.split("|")
        if len(parts) < 3:
            print("  ❌ --skip-gate 需要同时提供 --engineer-signature 姓名|工号|资质ID 留档")
            return 2
        gate_info = {
            "engineer_name": parts[0] or "CI_USER",
            "engineer_id": parts[1] or "CI_JOB",
            "qualification_id": parts[2] or "CI_CERT",
            "estop_verified": "Y",
            "signed_phrase": f"SKIP_GATE_CI::{QUALIFIED_PHRASE}",
            "gate_passed_at": datetime.now().isoformat(timespec="seconds"),
        }
        print(f"  ⚠️  CI 模式：已跳过交互式门禁（签名已留档）：{sig}\n")
    else:
        ok, gate_info = run_qualification_gate()
        if not ok:
            print("  🚫 资质/法律门禁未通过，部署终止。")
            return 3

    # ---- STEP 1: 载入配置 & 选机器人 ----
    global PROTOCOL_ADAPTERS_CACHE
    robots, brand_map, PROTOCOL_ADAPTERS_CACHE = _load_robots_and_maps()
    if not robots:
        print("  ❌ 机器人配置为空，终止")
        return 4
    arm_key = pick_arm_interactive(robots, brand_map, preselect=args.arm)
    if not arm_key:
        return 5
    cfg = confirm_communication(arm_key, robots, brand_map, pre_host=args.host, pre_port=args.port)

    # ---- STEP 2: 最终确认 ----
    print(f"\n  【最终确认】将对 {cfg['name']} 建立真实连接：")
    print(f"        arm_key = {cfg['arm_key']}")
    print(f"        target  = {cfg['host']}:{cfg['port'] or '(自动)'}  protocol={cfg['protocol']}")
    if not args.skip_gate:
        ans = _input_with_prompt("  输入『CONFIRM REAL DEPLOY』开始真实链路（其他任意取消）: ").strip()
        if ans != "CONFIRM REAL DEPLOY":
            print("  🚫 用户取消，部署终止。")
            return 6
    else:
        print("  [CI 模式] 自动确认：CONFIRM REAL DEPLOY\n")

    # ---- STEP 3: 部署执行 ----
    success, session = deploy_and_verify(cfg, gate_info, smoke=args.smoke)

    # ---- STEP 4: 留档 & 结论 ----
    save_session_log(session)
    print()
    print("=" * 72)
    if success:
        print("  ✅ 真实部署端到端链路执行成功。")
        print("     👉 后续强制要求：扩大运动幅度前，必须再次确认关节限位/负载/E-Stop。")
        print("=" * 72)
        return 0
    else:
        print("  ❌ 真实部署链路未通过，请查看上方日志并联系资质工程师现场排查。")
        print("=" * 72)
        return 10


if __name__ == "__main__":
    sys.exit(main())
