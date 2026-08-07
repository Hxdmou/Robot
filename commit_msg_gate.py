# -*- coding: utf-8 -*-
"""
Git Commit Message 格式门禁（永久强制执行·零例外）
严格限制 commit message 仅允许两种极简格式：
    「已修改 N 项内容」   N 为正整数
    「新增 N 项内容」     N 为正整数

用法（被 commit-msg 钩子调用，不手动运行）：
    python commit_msg_gate.py <commit_msg_file_path>

返回码：
    0 = 格式合规，允许 commit
    1 = 格式违规，阻止 commit
"""

import re
import sys
from pathlib import Path
from typing import Optional

# 仅允许的两种模式：中文全角空格/半角空格都兼容，数字为 1-9999
ALLOWED_PATTERN = re.compile(
    r'^\s*(已修改|新增)\s+([1-9]\d{0,3})\s+项内容\s*$'
)


def check_message(msg_text: str) -> tuple[bool, Optional[str]]:
    """
    校验 commit message 主体。返回 (是否通过, 违规原因或None)。
    规则：忽略以 # 开头的注释行和首尾空白行，取第一个非空非注释行校验。
    """
    meaningful: Optional[str] = None
    for raw_line in msg_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            continue
        meaningful = line
        break
    if meaningful is None:
        return False, "commit message 为空或全部是注释行"

    m = ALLOWED_PATTERN.match(meaningful)
    if m:
        return True, None

    # 给出具体违规提示 + 正面示例
    reasons = []
    if not any(meaningful.startswith(p) for p in ("已修改", "新增")):
        reasons.append("必须以「已修改」或「新增」开头")
    if not re.search(r'\d+\s+项内容', meaningful):
        reasons.append("必须包含形如「N 项内容」的数字结构（例：14 项内容）")
    hint = "合法示例：  已修改 14 项内容  或  新增 3 项内容"
    return False, ("；".join(reasons) if reasons else "格式不符合永久规则") + "。" + hint


def main() -> int:
    if len(sys.argv) < 2:
        print("[Commit-Msg Gate] ❌ 用法错误：缺少 commit message 文件路径参数")
        print("                （应被 commit-msg 钩子自动调用，不应手动运行）")
        return 2

    msg_file = Path(sys.argv[1])
    if not msg_file.is_file():
        print(f"[Commit-Msg Gate] ❌ 找不到 message 文件: {msg_file}")
        return 2

    try:
        # utf-8-sig 自动去除 UTF-8 BOM（Windows 编辑器常带 BOM 写入）
        text = msg_file.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as e:
        print(f"[Commit-Msg Gate] ❌ 读取 message 文件失败: {e}")
        return 2

    ok, reason = check_message(text)
    print()
    print("=" * 64)
    print("  📝  Commit Message 格式门禁（永久规则·零例外）")
    print("=" * 64)
    preview = text.strip().splitlines()
    preview = preview[:3]
    print(f"  你的提交信息摘要：")
    for ln in preview:
        print(f"    | {ln[:100]}")
    print()
    if ok:
        print("  ✅ 格式合规，允许通过。")
        print("=" * 64)
        return 0
    else:
        print("  🚫 格式违规，提交已被阻止！")
        print(f"     原因：{reason}")
        print()
        print("     💡 永久规则只允许 2 种格式：")
        print("        ① 已修改 N 项内容   （例：已修改 14 项内容）")
        print("        ② 新增 N 项内容     （例：新增 3 项内容）")
        print("     （N 为正整数，其他任何描述性文字、英文、敏感信息均不允许）")
        print("=" * 64)
        return 1


if __name__ == "__main__":
    sys.exit(main())
