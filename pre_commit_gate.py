# -*- coding: utf-8 -*-
"""
Git Pre-Commit 安全门禁（针对 staged 文件做轻量检查，速度优先）
功能：
    1. 对即将提交的源码做敏感信息扫描（复用 security_scan 规则）
       - 私网 IP 硬编码 (CRITICAL)
       - 凭证硬编码 / 密钥前缀 (CRITICAL)
       - 邮箱/手机号/身份证 (HIGH)
    2. 对 staged 的 .py 文件执行 py_compile 语法验证
    3. 总结报告，CRITICAL / HIGH > 0 → exit 非零阻止提交

用法（被 pre-commit 钩子调用，一般不手动运行）：
    python pre_commit_gate.py
"""

import os
import re
import sys
import json
import py_compile
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

PROJECT_ROOT = Path(__file__).parent.resolve()
GIT_DIR = PROJECT_ROOT / ".git"

# ============================================================
# 扫描规则（与 security_scan.py 保持一致，仅提取 CRITICAL/HIGH）
# ============================================================

SCAN_EXTS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.c', '.cpp', '.h', '.cs',
    '.go', '.rs', '.rb', '.php', '.sh', '.bat', '.ps1', '.cmd',
    '.yaml', '.yml', '.json', '.toml', '.ini', '.cfg', '.conf', '.md', '.txt', '.env'
}

PRIVATE_IP = re.compile(
    r'\b(?:192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
    r'172\.(?:1[6-9]|2[0-9]|3[01])\.\d{1,3}\.\d{1,3})\b'
)

CREDENTIAL = re.compile(
    r'(api[_-]?key|access[_-]?token|secret[_-]?key|password|passwd|pwd|'
    r'bearer|authorization|client[_-]?secret|private[_-]?key|auth[_-]?token|'
    r'token|secret|db[_-]?password)\s*(=|:|=>)\s*["\']([^"\']{8,})["\']',
    re.IGNORECASE
)

KEY_PREFIX = re.compile(
    r'\b(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|'
    r'xox[baprse]-[A-Za-z0-9-]{10,}|p[sk]_live_[A-Za-z0-9]{20,}|'
    r'A[SK]IA[0-9A-Z]{16}|AIza[0-9A-Za-z\-_]{20,}|'
    r'-----BEGIN\s+(?:RSA|DSA|EC|OPENSSH|PGP|ENCRYPTED|PRIVATE)\s+(?:PRIVATE\s+)?KEY-----)'
)

PII = re.compile(
    r'(?:[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}|'
    r'(?<!\d)1[3-9]\d{9}(?!\d)|'
    r'(?<!\d)[2-6]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?!\d))'
)

ALLOWED_PII_FRAGMENTS = [
    'example.com', 'test.com', 'foo.com', 'bar.com', 'noreply', 'no-reply',
    'admin@', 'root@', 'user@', '13800138', '0000', '***'
]
ALLOWED_CRED_FRAGMENTS = [
    'your-', 'your_', 'example', 'placeholder', 'dummy', 'changeme',
    'todo', '***', '[redacted]', 'redacted', 'null', 'none', 'test'
]


def _mask(text: str, keep=4) -> str:
    text = text.strip()
    if len(text) <= keep * 2 + 3:
        return '*' * len(text)
    return text[:keep] + '***' + text[-keep:]


# ============================================================
# 获取 staged 文件列表
# ============================================================

def get_staged_files() -> List[Path]:
    """通过 git diff --cached --name-only 取暂存区文件（绝对路径）"""
    if not GIT_DIR.exists():
        return []
    try:
        r = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=str(PROJECT_ROOT), capture_output=True, text=True,
            encoding="utf-8", errors="replace"
        )
    except (OSError, subprocess.SubprocessError):
        return []
    files: List[Path] = []
    for line in r.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        fp = PROJECT_ROOT / line
        if fp.is_file():
            files.append(fp)
    return files


# ============================================================
# 扫描单个文件
# ============================================================

def scan_file(fp: Path) -> List[Dict]:
    issues: List[Dict] = []
    try:
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except (OSError, PermissionError):
        return issues
    rel = str(fp.relative_to(PROJECT_ROOT)) if fp.is_relative_to(PROJECT_ROOT) else str(fp)
    for ln, line in enumerate(lines, 1):
        orig = line.rstrip("\n")
        if not orig.strip():
            continue

        # 1. 私网 IP → CRITICAL
        for m in PRIVATE_IP.finditer(orig):
            if m.group().startswith("127."):
                continue
            issues.append({
                "severity": "critical", "category": "私网IP硬编码",
                "file": rel, "line": ln,
                "match": m.group(),
                "context": _mask(orig[:120])
            })

        # 2. 凭证硬编码 → CRITICAL
        for m in CREDENTIAL.finditer(orig):
            val = (m.group(3) if m.lastindex and m.lastindex >= 3 else "").lower()
            if any(frag in val for frag in ALLOWED_CRED_FRAGMENTS):
                continue
            if len(val) < 10:
                continue
            issues.append({
                "severity": "critical", "category": "硬编码凭证",
                "file": rel, "line": ln,
                "match": _mask(m.group(1) if m.lastindex else m.group()),
                "context": _mask(orig[:120])
            })

        # 3. 密钥前缀 → CRITICAL
        for m in KEY_PREFIX.finditer(orig):
            issues.append({
                "severity": "critical", "category": "密钥前缀泄露",
                "file": rel, "line": ln,
                "match": _mask(m.group()[:8] + "..."),
                "context": _mask(orig[:120])
            })

        # 4. PII → HIGH
        for m in PII.finditer(orig):
            match_lower = m.group().lower()
            if any(frag in match_lower for frag in ALLOWED_PII_FRAGMENTS):
                continue
            issues.append({
                "severity": "high", "category": "个人隐私信息",
                "file": rel, "line": ln,
                "match": _mask(m.group()),
                "context": _mask(orig[:120])
            })
    return issues


# ============================================================
# py_compile 语法验证（仅 .py）
# ============================================================

def syntax_check(py_files: List[Path]) -> List[Dict]:
    results: List[Dict] = []
    for fp in py_files:
        rel = str(fp.relative_to(PROJECT_ROOT)) if fp.is_relative_to(PROJECT_ROOT) else str(fp)
        try:
            py_compile.compile(str(fp), doraise=True)
            results.append({"file": rel, "ok": True, "error": None})
        except py_compile.PyCompileError as e:
            results.append({
                "file": rel, "ok": False,
                "error": str(e).replace(str(fp), rel)
            })
        except Exception as e:
            results.append({
                "file": rel, "ok": False,
                "error": f"{type(e).__name__}: {e}"
            })
    return results


# ============================================================
# 主入口
# ============================================================

def main() -> int:
    staged = get_staged_files()
    if not staged:
        print("[Pre-Commit Gate] ⚪  暂存区为空，跳过门禁")
        return 0

    ext_filtered = [f for f in staged if f.suffix.lower() in SCAN_EXTS]
    py_only = [f for f in staged if f.suffix.lower() == ".py"]

    # 排除工具自身体 & 报告文件
    ext_filtered = [f for f in ext_filtered if f.name not in {
        "security_scan.py", "file_encryptor.py", "security_checklist.py",
        "pre_commit_gate.py", "commit_msg_gate.py", "before_lend.py",
    } and not (f.name.startswith("security_report_") or f.name.startswith("security_checklist_")
               or f.name.endswith(".bak_before_fix") or f.name.endswith(".bak_unenc"))]

    print()
    print("=" * 64)
    print("  🔒  Pre-Commit 安全门禁（针对暂存区文件）")
    print("=" * 64)
    print(f"  暂存区文件总数: {len(staged)}")
    print(f"  需扫描的源码:   {len(ext_filtered)}")
    print(f"  需语法验证 .py: {len(py_only)}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # ---- 扫描 ----
    all_issues: List[Dict] = []
    for fp in ext_filtered:
        all_issues.extend(scan_file(fp))
    critical = sum(1 for x in all_issues if x["severity"] == "critical")
    high = sum(1 for x in all_issues if x["severity"] == "high")

    print("  --- 敏感信息扫描 ---")
    if critical == 0 and high == 0:
        print("  ✅ 通过：CRITICAL=0, HIGH=0")
    else:
        print(f"  ❌ 未通过：CRITICAL={critical}, HIGH={high}")
        for it in all_issues[:30]:
            tag = f"[{it['severity'].upper():8s}]"
            print(f"     {tag} {it['file']}:{it['line']}  {it['category']} → {it['match']}")
        if len(all_issues) > 30:
            print(f"     ... 其余 {len(all_issues) - 30} 条省略")
    print()

    # ---- 语法 ----
    syntax_results = syntax_check(py_only)
    syntax_fail = [r for r in syntax_results if not r["ok"]]
    print("  --- Python 语法验证 ---")
    if not syntax_results:
        print("  ⚪ 无 staged .py 文件，跳过")
    elif not syntax_fail:
        print(f"  ✅ 通过：{len(syntax_results)} 个文件语法正确")
    else:
        print(f"  ❌ 未通过：{len(syntax_fail)} 个文件存在语法错误")
        for r in syntax_fail[:15]:
            err = (r["error"] or "")[:200]
            print(f"     - {r['file']}: {err}")
    print()

    # ---- 汇总 ----
    blocked = (critical > 0) or (high > 0) or (len(syntax_fail) > 0)
    print("-" * 64)
    if blocked:
        print("  🚫 提交已被安全门禁阻止！请修复上方问题后再提交。")
        print("     (需要临时绕过？ git commit --no-verify 仅限紧急情况)")
    else:
        print("  ✅ 安全门禁通过，允许提交。")
    print("=" * 64)
    print()
    return 1 if blocked else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[Pre-Commit Gate] 用户中断，默认阻止提交")
        sys.exit(1)
