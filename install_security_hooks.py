# -*- coding: utf-8 -*-
"""
一键安装 Git 安全钩子（pre-commit + commit-msg）
将两个 bash 脚本写入 .git/hooks/，使 Git 在每次 commit 前自动触发：
    ① pre-commit    → 调用 pre_commit_gate.py  （敏感信息扫描 + 语法验证）
    ② commit-msg    → 调用 commit_msg_gate.py  （格式门禁：仅允许两种极简格式）

用法：
    cd f:\个人作品\具身智能
    python install_security_hooks.py          # 安装（已存在会询问是否覆盖）
    python install_security_hooks.py --force  # 强制覆盖（无人值守）
    python install_security_hooks.py --remove # 卸载钩子（恢复 sample）
"""

import os
import sys
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
HOOKS_DIR = PROJECT_ROOT / ".git" / "hooks"

PRE_COMMIT_HOOK = r'''#!/usr/bin/env bash
# ============================================================
#  安全门禁 pre-commit 钩子（由 install_security_hooks.py 安装）
#  每次 git commit 之前自动执行
# ============================================================

# 定位项目根（.git 所在目录）
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$PROJECT_ROOT" ]; then
  echo "[Hook] ⚠️  不是 Git 仓库，跳过 pre-commit hook"
  exit 0
fi

cd "$PROJECT_ROOT"

# 优先使用虚拟环境里的 python，没有就退回到全局 python
if [ -f "env_pybullet/Scripts/python.exe" ]; then
  PY=env_pybullet/Scripts/python.exe
elif [ -f "env_pybullet/bin/python" ]; then
  PY=env_pybullet/bin/python
elif command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi

GATE_SCRIPT="$PROJECT_ROOT/pre_commit_gate.py"

if [ ! -f "$GATE_SCRIPT" ]; then
  echo "[Hook] ⚪  未找到 pre_commit_gate.py，跳过安全门禁"
  exit 0
fi

"$PY" "$GATE_SCRIPT"
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "[Hook] 🚫 pre-commit 安全门禁未通过（退出码 $EXIT_CODE），阻止提交。"
  echo "       需要临时跳过门禁？  →  git commit --no-verify  （仅限紧急情况）"
  exit $EXIT_CODE
fi

exit 0
'''

COMMIT_MSG_HOOK = r'''#!/usr/bin/env bash
# ============================================================
#  格式门禁 commit-msg 钩子（由 install_security_hooks.py 安装）
#  每次 git commit 编写 message 之后自动校验
# ============================================================

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$PROJECT_ROOT" ]; then
  echo "[Hook] ⚠️  不是 Git 仓库，跳过 commit-msg hook"
  exit 0
fi

cd "$PROJECT_ROOT"

if [ -f "env_pybullet/Scripts/python.exe" ]; then
  PY=env_pybullet/Scripts/python.exe
elif [ -f "env_pybullet/bin/python" ]; then
  PY=env_pybullet/bin/python
elif command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi

MSG_GATE="$PROJECT_ROOT/commit_msg_gate.py"

if [ ! -f "$MSG_GATE" ]; then
  echo "[Hook] ⚪  未找到 commit_msg_gate.py，跳过格式门禁"
  exit 0
fi

"$PY" "$MSG_GATE" "$1"
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "[Hook] 🚫 commit message 格式不合规（退出码 $EXIT_CODE），阻止提交。"
  echo "       需要临时跳过门禁？  →  git commit --no-verify  （仅限紧急情况）"
  exit $EXIT_CODE
fi

exit 0
'''


def _make_executable(hook_file: Path):
    """Windows NTFS 没有 chmod +x，主要在 git-bash 环境中才需要；此处尽力而为。"""
    try:
        if os.name != "nt":
            os.chmod(hook_file, 0o755)
    except OSError:
        pass


def _ask_overwrite(hook_file: Path, force: bool) -> bool:
    if not hook_file.exists():
        return True
    if force:
        print(f"  [force] 已存在 {hook_file.name}，强制覆盖")
        return True
    print(f"  ⚠️  检测到已有 {hook_file.name}")
    ans = input("  是否覆盖？[y/N] ").strip().lower()
    return ans in ("y", "yes")


def install(force: bool) -> int:
    if not HOOKS_DIR.exists():
        try:
            HOOKS_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"❌ 无法创建 hooks 目录 {HOOKS_DIR}: {e}")
            return 1

    print()
    print("=" * 60)
    print("  🛡️   Git 安全钩子安装器")
    print("=" * 60)
    print(f"  项目根目录: {PROJECT_ROOT}")
    print(f"  Git 钩子目录: {HOOKS_DIR}")
    print()

    installed = 0
    for name, content in (("pre-commit", PRE_COMMIT_HOOK), ("commit-msg", COMMIT_MSG_HOOK)):
        target = HOOKS_DIR / name
        if not _ask_overwrite(target, force):
            print(f"  ⏭️  跳过 {name}")
            continue
        try:
            target.write_text(content, encoding="utf-8", newline="\n")
            _make_executable(target)
            print(f"  ✅ 已安装 → {name}")
            installed += 1
        except OSError as e:
            print(f"  ❌ 写入 {name} 失败: {e}")

    print()
    if installed == 2:
        print("  🎉 两个钩子全部安装成功！")
        print()
        print("  功能说明：")
        print("    · pre-commit → 每次 commit 前：敏感信息扫描 + Python 语法验证")
        print("    · commit-msg → 每次写提交信息：仅允许「已修改 N 项内容」/「新增 N 项内容」")
        print()
        print("  紧急绕过时可使用：git commit --no-verify  （不推荐，仅限特殊情况）")
        return 0
    elif installed == 0:
        print("  ❌ 两个钩子都没安装，请检查权限或重试 --force")
        return 2
    else:
        print(f"  ⚠️  只安装了 {installed} 个钩子（缺少 1 个），可能功能不完整。")
        return 3


def remove_hooks() -> int:
    print()
    print("=" * 60)
    print("  🧹  Git 安全钩子卸载")
    print("=" * 60)
    removed = 0
    for name in ("pre-commit", "commit-msg"):
        target = HOOKS_DIR / name
        if target.exists():
            try:
                target.unlink()
                print(f"  ✅ 已删除 → {name}")
                removed += 1
            except OSError as e:
                print(f"  ❌ 删除 {name} 失败: {e}")
        else:
            print(f"  ⚪ 本就没有 {name}，跳过")
    print()
    sample_ref = HOOKS_DIR / "pre-commit.sample"
    if sample_ref.exists():
        print("  (目录中保留的 *.sample 文件是 Git 默认示例，不影响使用)")
    print(f"  共卸载 {removed} 个钩子。")
    return 0 if removed >= 0 else 1


def main() -> int:
    args = set(sys.argv[1:])
    force = "--force" in args or "-f" in args
    remove = "--remove" in args or "--uninstall" in args or "-u" in args

    if not (PROJECT_ROOT / ".git").exists():
        print("❌ 当前目录不是 Git 仓库（未找到 .git 目录）")
        print("   请先 cd 到项目根目录或执行 git init。")
        return 1

    if remove:
        return remove_hooks()
    return install(force)


if __name__ == "__main__":
    sys.exit(main())
