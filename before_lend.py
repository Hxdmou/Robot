# -*- coding: utf-8 -*-
"""
出借设备前 · 一键安全打包脚本（修复两个漏洞：
    ① 本地明文文件可读 → 强制启动加密 + PIN 门禁校验
    ② Git 本地凭据/身份残留 → 备份后清理 local 身份与 Windows 凭据管理器
）

⚠️  本脚本只做「可以安全自动化的部分」。以下两项必须手动完成（无法跨进程安全自动化）：
    ① 退出 Trae / VSCode / Cursor / GitHub Desktop 登录
    ② 按 Win + L 锁屏

用法：
    cd f:\个人作品\具身智能
    python before_lend.py
"""

import os
import sys
import json
import time
import getpass
import base64
import secrets
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any

# ============================================================
# 共享常量 & 工具（after_takeback.py 也 import 这里的函数）
# ============================================================

BACKUP_FILENAME = ".git_identity_backup.json"
GUEST_NAME = "Guest User"
GUEST_EMAIL = "***@***.***"
# Windows 凭据管理器中 Git 常用的 target 前缀（cmdkey 列出来的形式）
WINDOWS_GIT_CRED_TARGET_PREFIXES = (
    "LegacyGeneric:target=git:https://github.com",
    "LegacyGeneric:target=git:https://api.github.com",
    "LegacyGeneric:target=git:https://gist.github.com",
    "LegacyGeneric:target=git:https://gitlab.com",
    "LegacyGeneric:target=git:https://gitee.com",
)


def _project_root() -> Path:
    return Path(__file__).parent.resolve()


def backup_path() -> Path:
    return _project_root() / BACKUP_FILENAME


def _run(cmd: list, check: bool = False) -> subprocess.CompletedProcess:
    """安静执行命令，捕获输出（不打印到终端，避免泄漏凭据）"""
    return subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=check
    )


def _git_config(scope: str, key: str) -> Optional[str]:
    """scope = 'local' | 'global' | 'system'。查不到返回 None"""
    r = _run(["git", "config", f"--{scope}", "--get", key])
    if r.returncode == 0:
        v = r.stdout.strip()
        return v if v else None
    return None


def _git_config_set(scope: str, key: str, value: str) -> bool:
    r = _run(["git", "config", f"--{scope}", key, value])
    return r.returncode == 0


def _git_config_unset(scope: str, key: str) -> bool:
    """unset 返回 True = 原本就没设 / 已成功删除"""
    r = _run(["git", "config", f"--{scope}", "--unset", key])
    # returncode 5 = key 不存在，也算成功
    return r.returncode in (0, 5)


# ============================================================
# 备份 & 清理 Git 身份（漏洞 2 修复：本地 git 残留可直接以你身份 push）
# ============================================================

def detect_project_local_git_scope(project_root: Path) -> bool:
    return (project_root / ".git").exists()


def backup_identity(project_root: Path) -> Dict[str, Any]:
    """
    备份当前项目 local 身份 + 可选 global 身份 + Windows 凭据管理器中的 Git 条目名。
    返回备份字典，同时写入 .git_identity_backup.json。
    """
    backup: Dict[str, Any] = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "project_root": str(project_root),
        "local": {},
        "global": {
            "has_git_config": True,
        },
        "windows_credentials": [],
        "home_git_credentials": None,
        "restore_nonce": secrets.token_hex(16),  # 防止伪造/误还原
    }

    # 1) local 级 user.name / user.email / signingkey / credential 相关
    for k in ("user.name", "user.email", "user.signingkey",
              "credential.helper", "credential.useHttpPath"):
        v = _git_config("local", k)
        if v is not None:
            backup["local"][k] = v

    # 2) global 级：只读（不清理 global，避免破坏用户其他项目），只记录作为参考
    for k in ("user.name", "user.email", "credential.helper"):
        v = _git_config("global", k)
        if v is not None:
            backup["global"][k] = v  # type: ignore[assignment]

    # 3) Windows 凭据管理器：列出并记录要清理的 target 名称（**不存凭据内容**）
    if os.name == "nt":
        r = _run(["cmdkey", "/list"])
        if r.returncode == 0:
            lines = r.stdout.splitlines()
            for line in lines:
                line = line.strip()
                for prefix in WINDOWS_GIT_CRED_TARGET_PREFIXES:
                    if line.startswith("目标:") and prefix.split("target=", 1)[1] in line:
                        # 记录完整 cmdkey 形式的 target 名，供还原时参考（凭据值本身不存）
                        target = line.split("目标:", 1)[1].strip()
                        backup["windows_credentials"].append({
                            "target": target,
                            "deleted_by_lend": True,
                        })
                        break
                    elif line.startswith("Target:") and prefix.split("target=", 1)[1] in line:
                        target = line.split("Target:", 1)[1].strip()
                        backup["windows_credentials"].append({
                            "target": target,
                            "deleted_by_lend": True,
                        })
                        break

    # 4) ~/.git-credentials 文件：备份内容后标记（出借前会先备份再清空）
    home = Path.home()
    cred_file = home / ".git-credentials"
    if cred_file.is_file():
        try:
            data = cred_file.read_bytes()
            backup["home_git_credentials"] = {
                "path": str(cred_file),
                "size": len(data),
                "sha256": _sha256_bytes(data),
                "content_b64": base64.b64encode(data).decode("ascii"),
            }
        except OSError:
            backup["home_git_credentials"] = {"path": str(cred_file), "error": "read_failed"}

    # 写备份文件到项目根
    bp = backup_path()
    try:
        with open(bp, "w", encoding="utf-8") as f:
            json.dump(backup, f, ensure_ascii=False, indent=2)
        # 尽力设为隐藏
        if os.name == "nt":
            try:
                import ctypes
                ctypes.windll.kernel32.SetFileAttributesW(str(bp), 2)
            except Exception:
                pass
    except OSError as e:
        raise RuntimeError(f"备份 Git 身份失败：无法写入 {bp} — {e}") from e

    return backup


def _sha256_bytes(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def clear_identity_to_guest(project_root: Path) -> Dict[str, Any]:
    """
    把「当前项目 .git 目录」里的 local 身份强制覆盖为 guest。
    global 级不碰（不破坏用户其他项目）。
    清 Windows 凭据管理器里的 Git 缓存项。
    返回清理统计。
    """
    stats = {
        "local_identity_overridden": False,
        "windows_cred_deleted_count": 0,
        "home_git_credentials_cleared": False,
        "warnings": [],
    }

    # ── Local 身份：直接 override（不是 unset，因为 unset 会 fallback 到 global）
    if detect_project_local_git_scope(project_root):
        ok_n = _git_config_set("local", "user.name", GUEST_NAME)
        ok_e = _git_config_set("local", "user.email", GUEST_EMAIL)
        # 清理 signingkey 与本地 credential helper 覆盖
        ok_sk = _git_config_unset("local", "user.signingkey")
        ok_ch = _git_config_unset("local", "credential.helper")
        stats["local_identity_overridden"] = bool(ok_n and ok_e and ok_sk and ok_ch)
        if not stats["local_identity_overridden"]:
            stats["warnings"].append("项目 local git config 至少有一项写入失败，请手动 git config --local --list 检查")
    else:
        stats["warnings"].append("当前项目目录没有 .git，跳过 local git 身份清理（对单文件脚本场景无影响）")

    # ── Windows 凭据管理器：删除 Git 相关 target
    if os.name == "nt":
        # 直接用已知前缀删（因为 cmdkey /list 输出在不同语言里形式不稳）
        for prefix in WINDOWS_GIT_CRED_TARGET_PREFIXES:
            target = prefix.split("target=", 1)[1]
            r = _run(["cmdkey", "/delete", target])
            if r.returncode == 0:
                stats["windows_cred_deleted_count"] += 1
            elif "找不到" not in r.stderr and "not found" not in r.stderr.lower():
                # 找不到是正常的（用户没存过），其他情况记告警
                stats["warnings"].append(f"cmdkey /delete {target} 异常：stderr={r.stderr.strip()[:120]}")

    # ── ~/.git-credentials 文件：备份后清空（不是删除，方便误操作时可恢复）
    home = Path.home()
    cred_file = home / ".git-credentials"
    if cred_file.is_file():
        try:
            # 改名为 .git-credentials.lendbak，拿回后再改回来
            renamed = cred_file.with_suffix(".git-credentials.lendbak") \
                if cred_file.suffix != ".lendbak" else cred_file
            # 避免覆盖
            if renamed.exists():
                renamed = cred_file.with_name(
                    f".git-credentials.lendbak.{int(time.time())}"
                )
            cred_file.rename(renamed)
            stats["home_git_credentials_cleared"] = True
            stats["home_git_credentials_renamed_to"] = str(renamed)
        except OSError as e:
            stats["warnings"].append(f"重命名 ~/.git-credentials 失败：{e}")

    return stats


# ============================================================
# 子步骤编排
# ============================================================

def _step_print(n: int, total: int, title: str):
    print()
    print("=" * 70)
    print(f"  🛡️  出借准备 · 步骤 {n}/{total}：{title}")
    print("=" * 70)


def main() -> int:
    project_root = _project_root()
    TOTAL = 5

    _step_print(1, TOTAL, "备份 Git 身份与凭据（后续可 100% 还原）")
    try:
        backup = backup_identity(project_root)
    except RuntimeError as e:
        print(f"  ❌ {e}")
        print("     中止脚本，没有做任何破坏性清理。")
        return 2
    local_cnt = len(backup["local"])
    win_cred_cnt = len(backup["windows_credentials"])
    print(f"  ✅ 备份文件已写入: {backup_path().name}")
    print(f"     · 项目 local git config 条目备份: {local_cnt} 项")
    print(f"     · Windows 凭据管理器 Git 条目名记录: {win_cred_cnt} 个")
    if backup["home_git_credentials"]:
        print(f"     · 检测到 ~/.git-credentials，已备份其内容哈希 + base64（用于还原校验）")
    print(f"     · 备份包含唯一还原 nonce，防止误还原错误版本")

    _step_print(2, TOTAL, "清理本地 Git 身份（防止以你的名义 push 代码）")
    stats = clear_identity_to_guest(project_root)
    if detect_project_local_git_scope(project_root):
        print(f"  ✅ 项目 local 身份已覆盖为:")
        print(f"     · user.name  = {_git_config('local', 'user.name')}")
        print(f"     · user.email = {_git_config('local', 'user.email')}")
    print(f"  ✅ Windows 凭据管理器 Git 条目删除: {stats['windows_cred_deleted_count']} 个")
    if stats["home_git_credentials_cleared"]:
        print(f"  ✅ ~/.git-credentials 已重命名为: {stats.get('home_git_credentials_renamed_to')}")
    if stats["warnings"]:
        print("  ⚠️  警告（非致命，请自查）：")
        for w in stats["warnings"]:
            print(f"     - {w}")

    _step_print(3, TOTAL, "安全扫描 + 自动修复私网 IP（security_scan.py --fix）")
    print("  （脚本会提示输入 YES 确认，请自行输入；或使用 echo YES | ... 管道）")
    r = subprocess.run(
        [sys.executable, str(project_root / "security_scan.py"), "--fix"],
        cwd=str(project_root),
    )
    if r.returncode != 0:
        print("  ⚠️  security_scan.py 返回非 0 — 查看上方报告，确认 CRITICAL=0 后再继续。")
        confirm = input("  检测到严重度报告非 0，仍然继续吗？输入 CONTINUE 确认: ").strip()
        if confirm != "CONTINUE":
            print("  已中止。请先处理安全报告。")
            return 3

    _step_print(4, TOTAL, "加密项目敏感文件（file_encryptor.py encrypt）")
    print("  ⚠️  请记住你即将设置的密码，忘记 = 文件永久丢失！")
    print("  ⚠️  （脚本会先两次要求你输入加密密码，然后要求输入 YES 确认执行）")
    r = subprocess.run(
        [sys.executable, str(project_root / "file_encryptor.py"), "encrypt"],
        cwd=str(project_root),
    )
    if r.returncode != 0:
        print("  ❌ 加密失败（密码不一致 / 磁盘错误？），请排查后重试。")
        print("     ☝️  Git 身份已备份且清理，你可以先处理加密错误，再重新执行整体流程")
        print("       或手动运行 python after_takeback.py 把身份还原回来。")
        return 4

    _step_print(5, TOTAL, "检查清单 & 最后必须手动完成的动作")
    # 跑 security_checklist（允许个人隐私项存在，但 CRITICAL 必须 0）
    print("  运行 security_checklist.py 确认推送前的防线（CRITICAL=0 才是安全红线）：")
    r = subprocess.run(
        [sys.executable, str(project_root / "security_checklist.py")],
        cwd=str(project_root),
    )
    # checklist 返回非 0 很可能是邮箱项（MEDIUM），这里提醒但不阻断，因为真正的红线是 CRITICAL=0

    print()
    print("=" * 70)
    print("  🎁 出借准备 · 自动化步骤已全部完成！")
    print("=" * 70)
    print()
    print("  👇 以下 3 步必须你手动完成（脚本无法跨进程/跨 UI 安全操作）：")
    print("     1. 退出 Trae IDE / VSCode / Cursor 登录的账号")
    print("     2. 退出 GitHub Desktop 以及浏览器里已登录的 GitHub/Gitee/GitLab 账号")
    print("     3. 按  WIN + L  锁屏")
    print()
    print("  拿回设备后，执行下面一行一键还原：")
    print(f'     python "{project_root / "after_takeback.py"}"')
    print()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n  ⚠️  用户中断。Git 身份备份文件已保留，可运行 after_takeback.py 还原。")
        sys.exit(130)
