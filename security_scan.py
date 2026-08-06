# -*- coding: utf-8 -*-
"""
项目敏感信息安全扫描工具
功能：
    1. 检测源码中硬编码的私网 IPv4 地址（192.168.* / 10.* / 172.16-31.*）
    2. 检测硬编码的 API Key、密码、Token、凭证
    3. 检测密钥前缀（sk- / ghp_ / xoxb- / pk_ 等）
    4. 检测个人隐私信息（邮箱、手机号、身份证号）
    5. 检测 SSH / SSL 私钥文件内容
    6. 生成详细扫描报告

使用方法：
    python security_scan.py          # 扫描整个项目
    python security_scan.py --fast   # 快速扫描（跳过大文件）
    python security_scan.py --fix    # 自动将私网IP替换为 127.0.0.1（谨慎使用）
"""

import os
import re
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# ============================================================
# 扫描规则配置
# ============================================================

# 需要扫描的文件扩展名
SCAN_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.c', '.cpp', '.h', '.cs',
    '.go', '.rs', '.rb', '.php', '.sh', '.bat', '.ps1', '.cmd',
    '.yaml', '.yml', '.json', '.toml', '.ini', '.cfg', '.conf',
    '.xml', '.html', '.md', '.txt', '.env', '.env.example'
}

# 必须跳过的目录（虚拟环境、依赖包、缓存等）
SKIP_DIRS = {
    'env_isaacsim', 'env_pybullet', 'venv', 'env', '.venv',
    '__pycache__', '.git', '.github', '.idea', '.vscode',
    'node_modules', 'dist', 'build', '.cache', '.pytest_cache',
    '.streamlit', '.gradio', '.trae',
    'chat_histories', 'legal_knowledge_base',
    'drag_teach_data', 'data', 'screenshots', 'transformed_screenshots',
    '*_faiss_index', '*_data', '*_screenshots',
    'backup', 'backup*', '*_backup*', 'old_versions', 'archived',
}

# 大文件跳过阈值（字节）
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# ============================================================
# 正则表达式规则
# ============================================================

# 1. 私网 IPv4 地址（严格匹配，避免误匹配版本号）
PRIVATE_IP_PATTERN = re.compile(
    r'\b(?:'
    r'192\.168\.\d{1,3}\.\d{1,3}|'
    r'10\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
    r'172\.(?:1[6-9]|2[0-9]|3[01])\.\d{1,3}\.\d{1,3}'
    r')\b'
)

# 2. 公网 IPv4（用于提示，不强制报错）
PUBLIC_IP_PATTERN = re.compile(
    r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
    r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
)

# 3. 凭证/密钥硬编码模式（匹配 key = "value" 或 key: "value" 形式）
CREDENTIAL_PATTERNS = [
    (re.compile(
        r'(api[_-]?key|access[_-]?token|secret[_-]?key|password|passwd|pwd|'
        r'bearer|authorization|client[_-]?secret|private[_-]?key|auth[_-]?token|'
        r'token|secret|db[_-]?password|database[_-]?password|redis[_-]?password|'
        r'mongo[_-]?password|mysql[_-]?password|postgres[_-]?password)\s*'
        r'(=|:|=>)\s*["\']([^"\']{8,})["\']',
        re.IGNORECASE
    ), '硬编码凭证'),
]

# 4. 密钥前缀检测（sk- / ghp_ / gho_ / pk_ / xoxb- / xoxp- 等）
KEY_PREFIX_PATTERNS = [
    (re.compile(r'\bsk-[A-Za-z0-9]{20,}\b'), 'OpenAI/Stripe 风格密钥 (sk-)'),
    (re.compile(r'\bghp_[A-Za-z0-9]{20,}\b'), 'GitHub Personal Token (ghp_)'),
    (re.compile(r'\bgho_[A-Za-z0-9]{20,}\b'), 'GitHub OAuth Token (gho_)'),
    (re.compile(r'\bghu_[A-Za-z0-9]{20,}\b'), 'GitHub User Token (ghu_)'),
    (re.compile(r'\bghs_[A-Za-z0-9]{20,}\b'), 'GitHub Server Token (ghs_)'),
    (re.compile(r'\bghr_[A-Za-z0-9]{20,}\b'), 'GitHub Refresh Token (ghr_)'),
    (re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{10,}\b'), 'Slack Token (xoxb-/xoxp-)'),
    (re.compile(r'\bxoxe-[A-Za-z0-9-]{10,}\b'), 'Slack Enterprise Token (xoxe-)'),
    (re.compile(r'\bpk_live_[A-Za-z0-9]{20,}\b'), 'Stripe 公钥生产 (pk_live_)'),
    (re.compile(r'\bsk_live_[A-Za-z0-9]{20,}\b'), 'Stripe 私钥生产 (sk_live_)'),
    (re.compile(r'\brk_live_[A-Za-z0-9]{20,}\b'), 'Stripe 受限密钥 (rk_live_)'),
    (re.compile(r'\bAKIA[0-9A-Z]{16}\b'), 'AWS Access Key ID (AKIA...)'),
    (re.compile(r'\bASIA[0-9A-Z]{16}\b'), 'AWS 临时 Access Key (ASIA...)'),
    (re.compile(r'\bAIza[0-9A-Za-z\-_]{20,}\b'), 'Google API Key (AIza...)'),
    (re.compile(r'\b-----BEGIN\s+(?:RSA|DSA|EC|OPENSSH|PGP|ENCRYPTED|PRIVATE)\s+(?:PRIVATE\s+)?KEY-----'),
     '私钥文件头 (PEM BEGIN PRIVATE KEY)'),
]

# 5. 个人隐私信息
PRIVACY_PATTERNS = [
    (re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    ), '邮箱地址'),
    (re.compile(
        r'(?<!\d)1[3-9]\d{9}(?!\d)'
    ), '手机号码'),
    (re.compile(
        r'(?<!\d)[2-6]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?!\d)'
    ), '身份证号码'),
]

# ============================================================
# 扫描结果类
# ============================================================

class ScanResult:
    def __init__(self):
        self.total_files = 0
        self.scanned_files = 0
        self.skipped_files = 0
        self.issues: List[Dict] = []
        self.scan_start = datetime.now()
        self.scan_end: Optional[datetime] = None

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i['severity'] == 'critical')

    @property
    def high_count(self) -> int:
        return sum(1 for i in self.issues if i['severity'] == 'high')

    @property
    def medium_count(self) -> int:
        return sum(1 for i in self.issues if i['severity'] == 'medium')

    @property
    def low_count(self) -> int:
        return sum(1 for i in self.issues if i['severity'] == 'low')

    def add_issue(self, file_path: str, line_num: int, severity: str,
                  category: str, description: str, content: str):
        self.issues.append({
            'file': str(Path(file_path)),
            'line': line_num,
            'severity': severity,
            'category': category,
            'description': description,
            'content': self._mask_sensitive(content.strip())
        })

    @staticmethod
    def _mask_sensitive(text: str, keep_chars: int = 4) -> str:
        """脱敏显示：只保留前4后4位字符"""
        text = text.strip()
        if len(text) <= keep_chars * 2 + 3:
            return '*' * len(text)
        return text[:keep_chars] + '*' * (len(text) - keep_chars * 2) + text[-keep_chars:]

    def duration_seconds(self) -> float:
        end = self.scan_end or datetime.now()
        return (end - self.scan_start).total_seconds()

# ============================================================
# 核心扫描逻辑
# ============================================================

def should_skip_path(path: Path, project_root: Path) -> bool:
    """判断是否应该跳过该路径"""
    try:
        rel_parts = path.relative_to(project_root).parts
    except ValueError:
        return True
    for part in rel_parts:
        if part in SKIP_DIRS:
            return True
        if part.startswith('.') and part not in {'.env', '.env.example'}:
            return True
    return False

def scan_file(file_path: Path, result: ScanResult, fast_mode: bool = False):
    """扫描单个文件"""
    result.scanned_files += 1

    try:
        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            result.skipped_files += 1
            return
    except OSError:
        return

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except (OSError, PermissionError):
        return

    file_ext = file_path.suffix.lower()

    for line_num, line in enumerate(lines, 1):
        original_line = line.rstrip('\n')
        if not original_line.strip():
            continue

        # ---- 1. 私网 IP 检测（严重级别：critical，违反源码零硬编码红线）----
        for m in PRIVATE_IP_PATTERN.finditer(original_line):
            ip = m.group()
            # 排除 127.0.0.1（本地回环，允许）
            if ip.startswith('127.'):
                continue
            result.add_issue(
                file_path=str(file_path),
                line_num=line_num,
                severity='critical',
                category='私网IP硬编码',
                description=f'检测到私网 IPv4 地址: {ip}（违反源码零硬编码红线，必须通过 config.secure_env 注入）',
                content=original_line
            )

        # ---- 2. 凭证硬编码检测（严重级别：critical）----
        for pattern, desc in CREDENTIAL_PATTERNS:
            for m in pattern.finditer(original_line):
                value = m.group(3) if m.lastindex and m.lastindex >= 3 else m.group()
                # 跳过占位符示例值（如 your-api-key-here、***REDACTED***、[REDACTED] 等）
                if any(x in value.lower() for x in [
                    'your-', 'your_', 'example', 'placeholder', 'dummy',
                    'changeme', 'change_me', 'todo', 'xxx', '***',
                    '[redacted]', 'redacted', 'null', 'none', 'test'
                ]):
                    continue
                # 跳过极短的无意义值
                if len(value) < 10:
                    continue
                result.add_issue(
                    file_path=str(file_path),
                    line_num=line_num,
                    severity='critical',
                    category=f'硬编码凭证 ({desc})',
                    description=f'检测到可能的凭证硬编码: {m.group(1) if m.lastindex else desc}',
                    content=original_line
                )

        # ---- 3. 密钥前缀检测（严重级别：critical，直接就是密钥）----
        for pattern, desc in KEY_PREFIX_PATTERNS:
            for m in pattern.finditer(original_line):
                result.add_issue(
                    file_path=str(file_path),
                    line_num=line_num,
                    severity='critical',
                    category=f'密钥泄露 ({desc})',
                    description=f'检测到真实密钥前缀: {desc}',
                    content=original_line
                )

        # ---- 4. 个人隐私信息检测（级别：medium-high）----
        for pattern, desc in PRIVACY_PATTERNS:
            for m in pattern.finditer(original_line):
                # 仅在非示例文档中警告（.py/.env/.json 等配置文件为 high）
                severity = 'high' if file_ext in {'.py', '.json', '.yaml', '.yml', '.env', '.toml', '.ini'} else 'medium'
                # 跳过示例邮箱（如 example@、test@、noreply@、foo@bar.com）
                match_text = m.group().lower()
                if any(x in match_text for x in [
                    'example.com', 'test.com', 'foo.com', 'bar.com',
                    'noreply', 'no-reply', 'admin@', 'root@', 'user@'
                ]):
                    continue
                # 跳过假手机号（13800138000 等测试号段）
                if desc == '手机号码' and (match_text.startswith('13800138') or '0000' in match_text):
                    continue
                result.add_issue(
                    file_path=str(file_path),
                    line_num=line_num,
                    severity=severity,
                    category=f'个人隐私信息 ({desc})',
                    description=f'检测到可能的{desc}: 建议删除或脱敏',
                    content=original_line
                )

        # ---- 5. 公网 IP 提示（级别：low，仅提示）----
        if not fast_mode:
            for m in PUBLIC_IP_PATTERN.finditer(original_line):
                ip = m.group()
                # 跳过私网段已检测过的
                if PRIVATE_IP_PATTERN.match(ip):
                    continue
                # 跳过本地回环、广播、多播等
                if (ip.startswith('127.') or ip.startswith('0.') or
                    ip.startswith('255.') or ip.startswith('224.') or
                    ip.startswith('239.') or ip.startswith('169.254.')):
                    continue
                # 跳过文档示例（如 IP 1.2.3.4、8.8.8.8 等常见公共 DNS）
                if ip in {'8.8.8.8', '8.8.4.4', '1.1.1.1', '1.0.0.1', '114.114.114.114'}:
                    continue
                result.add_issue(
                    file_path=str(file_path),
                    line_num=line_num,
                    severity='low',
                    category='公网IP提示',
                    description=f'检测到公网 IPv4: {ip}（如用于生产环境请通过环境变量注入）',
                    content=original_line
                )

def scan_project(project_root: Path, fast_mode: bool = False) -> ScanResult:
    """扫描整个项目目录"""
    result = ScanResult()

    for root, dirs, files in os.walk(project_root):
        root_path = Path(root)
        # 过滤掉跳过的目录
        dirs[:] = [d for d in dirs if not should_skip_path(root_path / d, project_root)]

        for fname in files:
            fpath = root_path / fname
            result.total_files += 1
            # 跳过安全工具生成的报告与临时备份
            if (fname.startswith('security_report_') or
                fname.startswith('security_checklist_') or
                fname.endswith('.bak_before_fix') or
                fname.endswith('.bak_unenc')):
                result.skipped_files += 1
                continue
            # 只扫描指定扩展名的文件
            if fpath.suffix.lower() not in SCAN_EXTENSIONS:
                result.skipped_files += 1
                continue
            scan_file(fpath, result, fast_mode=fast_mode)

    result.scan_end = datetime.now()
    return result

# ============================================================
# 自动修复模式（将私网 IP 替换为 127.0.0.1）
# ============================================================

def auto_fix_private_ips(project_root: Path) -> Dict:
    """
    自动修复：将源码中硬编码的私网 IP 替换为 127.0.0.1
    谨慎使用！修改前请确认已备份
    """
    fix_report = {
        'modified_files': 0,
        'total_replacements': 0,
        'changes': []
    }

    for root, dirs, files in os.walk(project_root):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if not should_skip_path(root_path / d, project_root)]
        for fname in files:
            fpath = root_path / fname
            if fpath.suffix.lower() not in SCAN_EXTENSIONS:
                continue
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except (OSError, UnicodeDecodeError):
                continue

            matches = list(PRIVATE_IP_PATTERN.finditer(content))
            matches = [m for m in matches if not m.group().startswith('127.')]
            if not matches:
                continue

            new_content = PRIVATE_IP_PATTERN.sub(
                lambda m: '127.0.0.1' if not m.group().startswith('127.') else m.group(),
                content
            )
            # 备份原文件
            backup_path = fpath.with_suffix(fpath.suffix + '.bak_before_fix')
            try:
                with open(backup_path, 'w', encoding='utf-8') as bf:
                    bf.write(content)
                with open(fpath, 'w', encoding='utf-8') as wf:
                    wf.write(new_content)
                fix_report['modified_files'] += 1
                fix_report['total_replacements'] += len(matches)
                fix_report['changes'].append({
                    'file': str(fpath),
                    'replacements': len(matches),
                    'backup': str(backup_path)
                })
            except OSError as e:
                fix_report['changes'].append({
                    'file': str(fpath),
                    'error': str(e)
                })
    return fix_report

# ============================================================
# 输出报告
# ============================================================

SEVERITY_COLORS = {
    'critical': '\033[91m',  # 红
    'high': '\033[93m',      # 黄
    'medium': '\033[96m',    # 青
    'low': '\033[90m',       # 灰
}
RESET_COLOR = '\033[0m'

def print_report(result: ScanResult, project_root: Path):
    """在终端输出彩色扫描报告"""
    is_windows = sys.platform.startswith('win')
    def c(severity, text):
        if is_windows:
            return text
        return SEVERITY_COLORS.get(severity, '') + text + RESET_COLOR

    sep = '=' * 80
    print()
    print(sep)
    print('  项目敏感信息安全扫描报告')
    print(sep)
    print(f'  项目根目录: {project_root}')
    print(f'  扫描时间: {result.scan_start.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'  耗时: {result.duration_seconds():.2f} 秒')
    print()
    print(f'  总文件数: {result.total_files}')
    print(f'  已扫描:   {result.scanned_files}')
    print(f'  已跳过:   {result.skipped_files}（虚拟环境/依赖/大文件/非目标类型）')
    print()

    # 汇总统计
    print(sep)
    print('  问题汇总')
    print(sep)
    counts = [
        ('CRITICAL（严重）', result.critical_count, 'critical'),
        ('HIGH（高危）', result.high_count, 'high'),
        ('MEDIUM（中危）', result.medium_count, 'medium'),
        ('LOW（低危）', result.low_count, 'low'),
    ]
    for label, cnt, sev in counts:
        print(f'  {c(sev, label):<18}: {cnt}')
    print(f'  {"问题总计":<18}: {len(result.issues)}')
    print()

    # 详细问题列表
    if result.issues:
        print(sep)
        print('  详细问题清单')
        print(sep)
        # 按严重级别排序
        sorted_issues = sorted(result.issues, key=lambda x: {
            'critical': 0, 'high': 1, 'medium': 2, 'low': 3
        }.get(x['severity'], 99))

        current_file = None
        for issue in sorted_issues:
            if issue['file'] != current_file:
                current_file = issue['file']
                try:
                    rel = str(Path(current_file).relative_to(project_root))
                except ValueError:
                    rel = current_file
                print()
                print(f'  📄 文件: {rel}')
            sev_tag = f"[{issue['severity'].upper()}]"
            line_info = f"  L{issue['line']:<5}"
            print(f'    {c(issue["severity"], sev_tag):<14} {line_info} {issue["category"]}')
            print(f'         说明: {issue["description"]}')
            if issue['content']:
                print(f'         内容: {issue["content"]}')
        print()

    # 结论
    print(sep)
    has_critical = result.critical_count > 0 or result.high_count > 0
    if has_critical:
        print(c('critical', '  ⚠️  结论: 检测到严重/高危问题，必须修复后才能推送到 GitHub！'))
    else:
        print(c('low', '  ✅ 结论: 未检测到严重问题，符合安全红线要求。'))
    print(sep)
    print()

    # 输出 JSON 报告文件
    report_path = project_root / f'security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    report_data = {
        'project_root': str(project_root),
        'scan_start': result.scan_start.isoformat(),
        'scan_end': result.scan_end.isoformat() if result.scan_end else None,
        'duration_seconds': result.duration_seconds(),
        'summary': {
            'total_files': result.total_files,
            'scanned_files': result.scanned_files,
            'skipped_files': result.skipped_files,
            'critical': result.critical_count,
            'high': result.high_count,
            'medium': result.medium_count,
            'low': result.low_count,
            'total_issues': len(result.issues),
        },
        'issues': result.issues
    }
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        print(f'  📄 JSON 报告已保存: {report_path.name}')
    except OSError as e:
        print(f'  ❌ JSON 报告保存失败: {e}')
    print()

# ============================================================
# 主入口
# ============================================================

def main():
    project_root = Path(__file__).parent.resolve()
    args = set(sys.argv[1:])

    fast_mode = '--fast' in args
    fix_mode = '--fix' in args

    print()
    print(f'  🔍 启动项目安全扫描 (项目: {project_root.name})')
    print(f'     模式: {"快速扫描" if fast_mode else "完整扫描"} | 自动修复: {"已启用" if fix_mode else "未启用"}')
    print()

    if fix_mode:
        print('  ⚠️  自动修复模式：将硬编码私网IP替换为 127.0.0.1')
        print('     原文件将备份为 *.bak_before_fix')
        confirm = input('     请输入 YES 确认继续: ').strip()
        if confirm != 'YES':
            print('  已取消修复。')
            return
        report = auto_fix_private_ips(project_root)
        print()
        print(f'  修复完成：修改文件 {report["modified_files"]} 个，替换 {report["total_replacements"]} 处')
        for ch in report['changes'][:20]:
            if 'error' in ch:
                print(f'    ❌ {ch["file"]}: {ch["error"]}')
            else:
                print(f'    ✅ {ch["file"]}: {ch["replacements"]} 处替换，备份: {Path(ch["backup"]).name}')
        if len(report['changes']) > 20:
            print(f'    ... 其余 {len(report["changes"]) - 20} 个文件省略显示')
        # 修复后再扫描一次验证结果
        print()
        print('  修复完成，重新扫描验证...')

    result = scan_project(project_root, fast_mode=fast_mode)
    print_report(result, project_root)

    # 返回非零退出码，方便 CI 集成
    if result.critical_count > 0 or result.high_count > 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
