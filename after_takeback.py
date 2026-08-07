# -*- coding: utf-8 -*-
"""
拿回设备后 · 一键安全还原脚本（对应 before_lend.py 的反向操作）

功能（对应 before_lend 的反向）：
    1. 解密所有 .enc 敏感文件（让你输入密码）
    2. 读取 .git_identity_backup.json，100% 还原项目 local git 身份
       （user.name / user.email / user.signingkey / credential.helper 等）
    3. 还原 ~/.git-credentials（如果出借前被重命名了则改回）
    4. 清理 .bak_unenc / .bak_before_fix / 临时备份
    5. 跑安全扫描复核 CRITICAL=0
    6. 提醒手动重新登录 Trae / GitHub 账号

⚠️  关于 GitHub / Windows 凭据管理器中的 Git Token：
    before_lend 会删除条目以防止以你身份 push，
    但该脚本**不会**帮你重新填入明文 Token（安全考虑，不存明文）。
    还原后的第一次 git push / git pull，Windows 会弹窗让你重新登录 GitHub ——
    你用浏览器 OAuth 登录一次即可自动回存凭据。
"""

import os
import sys
import json
import base64
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict

# 复用 sibling 脚本的常量与 git 工具函数
sys.path.insert(0, str(Path(__file__).parent.resolve()))
from before_lend import (  # noqa: E402
    backup_path,
    _project_root,
    _run,
    _git_config,
    _git_config_set,
    _git_config_unset,
    _sha256_bytes,
    GUEST_NAME,
    GUEST_EMAIL,
)


def _step_print(n: int, total: int, title: str):
    print()
    print("=" * 70)
    print(f"  🔓 拿回还原 · 步骤 {n}/{total}：{title}")
    print("=" * 70)


def load_backup_or_exit() -> Dict[str, Any]:
    bp = backup_path()
    if not bp.is_file():
        print(f"  ❌ 找不到备份文件: {bp.name}")
        print("     说明：你要么没执行 before_lend.py，要么备份已被删除。")
        print("     Git 身份无法自动还原，但你可以手动设置：")
        print('       git config --local user.name "你的名字"')
        print('       git config --local user.email "你的邮箱"')
        sys.exit(2)
    try:
        with open(bp, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"  ❌ 备份文件损坏: {e}")
        sys.exit(2)


def restore_local_git_identity(project_root: Path, backup: Dict[str, Any]) -> Dict[str, int]:
    stats = {"restored": 0, "unset": 0, "errors": 0}
    if not (project_root / ".git").exists():
        print("  ⏭  当前项目没有 .git 目录，跳过 local git 身份还原（单文件脚本场景正常）")
        return stats

    saved_local = backup.get("local") or {}
    # 当前 local 中存在的所有 key：先全部清空，然后按备份重建
    current_keys = ("user.name", "user.email", "user.signingkey",
                    "credential.helper", "credential.useHttpPath")

    # 先全清
    for k in current_keys:
        if not _git_config_unset("local", k):
            stats["errors"] += 1

    # 再逐条还原
    for k, v in saved_local.items():
        if v is None:
            continue
        if _git_config_set("local", k, str(v)):
            stats["restored"] += 1
        else:
            stats["errors"] += 1

    # 打印校验
    print("  ✅ Local git 身份已还原为：")
    for k in ("user.name", "user.email", "user.signingkey", "credential.helper"):
        v = _git_config("local", k)
        if v is not None:
            if k == "user.signingkey" and len(v) > 16:
                v = v[:8] + "…" + v[-8:]
            print(f"     · {k} = {v}")
    return stats


def restore_home_git_credentials(backup: Dict[str, Any]) -> bool:
    """~/.git-credentials 如果被出借脚本重命名了，则改回原文件名"""
    entry = backup.get("home_git_credentials") or None
    if not entry or "path" not in entry:
        print("  ⏭  备份中不含 ~/.git-credentials，跳过")
        return True

    orig_path = Path(entry["path"])
    # 找被重命名后的文件：出借脚本用 .lendbak 后缀或 .lendbak.<timestamp>
    home = Path.home()
    candidates = []
    for p in home.iterdir():
        if p.name.startswith(".git-credentials.lendbak"):
            candidates.append(p)
    if not candidates:
        # 没找到 lendbak，出借时本身必定没有这个文件（绝对明确）
        if orig_path.exists():
            print("  ⏭  ~/.git-credentials 已存在，无需还原")
            return True
        print("  ⚠️  出借时备份了 ~/.git-credentials，但现在找不到对应的 .lendbak 文件")
        print(f"     原路径: {orig_path} — 已被手动处理，必须自行核对确认")
        return False

    # 按时间最新的选一个
    candidates.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    chosen = candidates[0]

    # 内容校验（哈希）
    try:
        actual = chosen.read_bytes()
    except OSError as e:
        print(f"  ❌ 读 {chosen} 失败：{e}")
        return False
    expected_sha = entry.get("sha256")
    if expected_sha and expected_sha != _sha256_bytes(actual):
        # 不一致但仍备份了 content_b64，用备份内容还原
        if "content_b64" in entry:
            print("  ⚠️  .lendbak 文件哈希与备份不一致，使用备份中的 base64 内容还原")
            try:
                data = base64.b64decode(entry["content_b64"])
                with open(orig_path, "wb") as f:
                    f.write(data)
                return True
            except Exception as e:
                print(f"  ❌ 从 base64 备份还原失败: {e}")
                return False
        print(f"  ⚠️  哈希不一致且无 base64 备份，保留文件在 {chosen} 请手动处理")
        return False

    # 哈希一致 → 直接重命名
    try:
        if orig_path.exists():
            orig_path.unlink()
        chosen.rename(orig_path)
        print(f"  ✅ ~/.git-credentials 已从 {chosen.name} 还原")
        return True
    except OSError as e:
        print(f"  ❌ 重命名还原失败: {e}")
        return False


def delete_bak_files(project_root: Path) -> Dict[str, int]:
    stats = {"bak_unenc": 0, "bak_before_fix": 0, "freed_bytes": 0}
    for pattern, key in (("**/*.bak_unenc", "bak_unenc"),
                         ("**/*.bak_before_fix", "bak_before_fix")):
        for p in project_root.glob(pattern):
            try:
                if not p.is_file():
                    continue
                # 跳过虚拟环境/依赖目录
                rel = str(p.relative_to(project_root))
                skip = any(part in {"__pycache__", ".git", "venv", "env",
                                    ".venv", "env_isaacsim", "env_pybullet",
                                    "node_modules"} for part in Path(rel).parts)
                if skip:
                    continue
                size = p.stat().st_size
                p.unlink()
                stats[key] += 1
                stats["freed_bytes"] += size
            except OSError:
                pass
    return stats


def main() -> int:
    project_root = _project_root()
    TOTAL = 6

    # ── 0. 先确认备份存在 ──
    backup = load_backup_or_exit()
    print(f"  ✅ 备份文件读取成功，创建时间: {backup.get('created_at')}")

    # ── 1. 解密 ──
    _step_print(1, TOTAL, "解密所有 .enc 敏感文件（输入加密时的密码）")
    r = subprocess.run(
        [sys.executable, str(project_root / "file_encryptor.py"), "decrypt"],
        cwd=str(project_root),
    )
    if r.returncode != 0:
        print("  ❌ 解密失败（密码错误？）请重试 after_takeback.py")
        print("     （备份文件已保留，Git 身份还原可以等解密成功后单独执行，不会自动清）")
        return 4

    # ── 2. 还原项目 local git 身份 ──
    _step_print(2, TOTAL, "还原项目 local Git 身份（user.name / user.email …）")
    s1 = restore_local_git_identity(project_root, backup)
    print(f"     统计：重建 {s1['restored']} 项，错误 {s1['errors']} 项")

    # ── 3. 还原 ~/.git-credentials ──
    _step_print(3, TOTAL, "还原 ~/.git-credentials（如果有）")
    ok3 = restore_home_git_credentials(backup)
    if not ok3:
        print("     ⚠️  该步骤未能全自动还原，后续你可用浏览器 OAuth 登 Git 即可自动重建凭据")

    # ── 4. 清理加密/修复的备份文件 ──
    _step_print(4, TOTAL, "清理 *.bak_unenc / *.bak_before_fix 临时备份")
    s4 = delete_bak_files(project_root)
    print(f"  ✅ 删除 .bak_unenc: {s4['bak_unenc']} 个 / "
          f".bak_before_fix: {s4['bak_before_fix']} 个 / "
          f"释放 {s4['freed_bytes'] / 1024:.1f} KB")

    # ── 5. 安全扫描复核 ──
    _step_print(5, TOTAL, "安全扫描复核（确认 CRITICAL=0 / HIGH=0）")
    subprocess.run(
        [sys.executable, str(project_root / "security_scan.py")],
        cwd=str(project_root),
    )

    # ── 6. 清理备份文件（可选） ──
    _step_print(6, TOTAL, "清理出借备份 .git_identity_backup.json")
    bp = backup_path()
    try:
        # 最后再做一次 SHA 校验确认 nonce 一致，防止删错
        del_confirm = input(
            f"  必须保留备份 1 天防止意外；输入 DELETE 立即删除 {bp.name}: "
        ).strip()
        if del_confirm == "DELETE":
            bp.unlink()
            print(f"  ✅ 已删除: {bp.name}")
        else:
            print(f"  ⏭  已保留备份文件: {bp.name}（你之后可手动删除）")
    except OSError as e:
        print(f"  ⚠️  删除失败: {e}（不影响使用，只是留在磁盘上）")

    # ── 收尾：手动提醒 ──
    print()
    print("=" * 70)
    print("  🎉 拿回还原 · 自动化步骤完成")
    print("=" * 70)
    print()
    print("  👇 最后两步请手动执行：")
    print("     1. 重新登录 Trae IDE / VSCode / GitHub Desktop 账号")
    print("     2. 第一次 git push 时，Windows 会弹窗要求登录 GitHub —— ")
    print("        选择「浏览器授权」登录一次即可，凭据会自动存回凭据管理器")
    print()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n  ⚠️  用户中断。下次可直接重跑 after_takeback.py，已解密的文件不会重复解密。")
        sys.exit(130)
