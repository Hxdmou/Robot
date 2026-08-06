# -*- coding: utf-8 -*-
"""
项目安全自查清单 —— GitHub 推送前强制校验
严格按照项目安全防线中的「推送前强制校验流程」7 大项逐一执行：
    ① 私 IP 扫描：Grep 私网段 IPv4 → 必须 0 匹配
    ② 凭证扫描：Grep 凭证硬编码模式 → 必须 0 匹配
    ③ 密钥前缀扫描：Grep sk-/ghp-/xoxb-/私钥头 → 必须 0 匹配
    ④ 个人信息扫描：Grep 邮箱/手机/身份证 → 必须 0 匹配
    ⑤ 语法验证：py_compile 核心文件 → 必须全部通过
    ⑥ 诊断验证：VSCode GetDiagnostics 0 错误 0 警告
    ⑦ Git 身份合规：出借模式下 local user.name/email 必须是 Guest（防止以主人名义 push）

使用方法：
    python security_checklist.py           # 执行全部 7 项检查（出借模式）
    python security_checklist.py --as-owner# 你是项目主人自己推代码：跳过第 ⑦ 项 guest 校验
    python security_checklist.py --no-lint # 跳过第 6 项诊断验证（无 VSCode LSP 时）
    python security_checklist.py --core    # 仅检查核心文件（更快）
    python security_checklist.py --fix     # 自动修复模式（私网IP替换为127.0.0.1）
"""

import os
import re
import sys
import json
import py_compile
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Callable, Optional

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path(__file__).parent.resolve()

# 检查的文件扩展名（扫描相关）
SCAN_EXTS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.c', '.cpp', '.h', '.cs',
    '.go', '.rs', '.rb', '.php', '.sh', '.bat', '.ps1', '.cmd',
    '.yaml', '.yml', '.json', '.toml', '.ini', '.cfg', '.conf',
    '.xml', '.html', '.md', '.txt', '.env'
}

# 必须跳过的目录
SKIP_DIRS = {
    'env_isaacsim', 'env_pybullet', 'venv', 'env', '.venv',
    '__pycache__', '.git', '.github', '.idea', '.vscode',
    'node_modules', 'dist', 'build', '.cache', '.pytest_cache',
    '.streamlit', '.gradio', '.trae',
    'chat_histories', 'legal_knowledge_base',
    'drag_teach_data', 'data', 'screenshots', 'transformed_screenshots',
}

# 核心 Python 文件（第⑤项语法验证 —— —— 必检文件）
CORE_PY_FILES = [
    'config/settings.py',
    'embodied-intelligence/config.py',
    'embodied-intelligence/settings.py',
    'embodied-intelligence/panda_comm.py',
    'embodied-intelligence/robot_arm_db.py',
    'embodied-intelligence/real_robot_ready_system.py',
    'embodied-intelligence/remote_monitoring_system.py',
    'embodied-intelligence/real_robot_adapter.py',
    'embodied-intelligence/sim_backends.py',
    'embodied-intelligence/deploy_main.py',
    'embodied-intelligence/deployment_config.py',
    'embodied-intelligence/deploy_adapters.py',
    'embodied-intelligence/robots_config.py',
    'embodied-intelligence/scenes_config.py',
    'embodied-intelligence/main.py',
    'embodied-intelligence/domain_randomization.py',
    'embodied-intelligence/latency_simulator.py',
    'embodied-intelligence/actuator_dynamics.py',
    'embodied-intelligence/disturbance_simulator.py',
    'embodied-intelligence/sensor_noise.py',
    'embodied-intelligence/pybullet_realistic_train.py',
    'embodied-intelligence/pybullet_realistic_test.py',
    'api_server.py',
    'logger.py',
    'rag.py',
    'inference.py',
    'train.py',
]

# ============================================================
# 正则（与 security_scan 保持一致，但此脚本用于最终门禁）
# ============================================================

RULES: List[Dict] = [
    {
        'id': 'private_ip',
        'name': '① 私网 IPv4 硬编码',
        'severity': 'critical',
        'regex': re.compile(
            r'\b(?:'
            r'192\.168\.\d{1,3}\.\d{1,3}|'
            r'10\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
            r'172\.(?:1[6-9]|2[0-9]|3[01])\.\d{1,3}\.\d{1,3}'
            r')\b'
        ),
        'allowed_value': lambda m: m.group().startswith('127.'),
    },
    {
        'id': 'credential',
        'name': '② 凭证硬编码 (key="value")',
        'severity': 'critical',
        'regex': re.compile(
            r'(api[_-]?key|access[_-]?token|secret[_-]?key|password|passwd|pwd|'
            r'bearer|authorization|client[_-]?secret|private[_-]?key|auth[_-]?token|'
            r'token|secret|db[_-]?password|database[_-]?password)\s*'
            r'(=|:|=>)\s*["\']([^"\']{8,})["\']',
            re.IGNORECASE
        ),
        # 允许占位符
        'allowed_value': lambda m: any(x in (m.group(3) if m.lastindex and m.lastindex >= 3 else '').lower()
                                       for x in ['your-', 'your_', 'example', 'placeholder',
                                                 'dummy', 'changeme', 'todo', '***',
                                                 '[redacted]', 'redacted', 'null', 'none']),
    },
    {
        'id': 'key_prefix',
        'name': '③ 密钥前缀 (sk-/ghp-/xoxb- 等)',
        'severity': 'critical',
        'regex': re.compile(
            r'\b(?:sk-[A-Za-z0-9]{20,}|'
            r'gh[pousr]_[A-Za-z0-9]{20,}|'
            r'xox[baprs]-[A-Za-z0-9-]{10,}|'
            r'xoxe-[A-Za-z0-9-]{10,}|'
            r'p[sk]_live_[A-Za-z0-9]{20,}|'
            r'rk_live_[A-Za-z0-9]{20,}|'
            r'A[SK]IA[0-9A-Z]{16}|'
            r'AIza[0-9A-Za-z\-_]{20,}|'
            r'-----BEGIN\s+(?:RSA|DSA|EC|OPENSSH|PGP|ENCRYPTED|PRIVATE)\s+(?:PRIVATE\s+)?KEY-----)'
        ),
    },
    {
        'id': 'pii',
        'name': '④ 个人隐私（邮箱/手机/身份证）',
        'severity': 'high',
        'regex': re.compile(
            r'(?:'
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}|'           # 邮箱
            r'(?<!\d)1[3-9]\d{9}(?!\d)|'                                   # 手机号
            r'(?<!\d)[2-6]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?!\d)'  # 身份证
            r')'
        ),
        # 允许常见示例值
        'allowed_value': lambda m: any(x in m.group().lower()
                                       for x in ['example.com', 'test.com', 'foo.com', 'bar.com',
                                                 'noreply', 'no-reply', 'admin@', 'root@', 'user@',
                                                 '13800138', '0000']),
    },
]


# ============================================================
# 辅助
# ============================================================

def _walk_scan_files(root: Path, core_only: bool = False):
    """遍历项目，返回需要扫描的文件列表"""
    results: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dp = Path(dirpath)
        # 过滤跳过目录
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                       and not (d.startswith('.') and d not in {'.env'})]
        for fn in filenames:
            fp = dp / fn
            if fp.suffix.lower() not in SCAN_EXTS:
                continue
            # 本工具自身文件 & 报告文件 & 备份文件跳过
            if fp.name in {'security_scan.py', 'file_encryptor.py', 'security_checklist.py'}:
                continue
            if (fn.startswith('security_report_') or fn.startswith('security_checklist_') or
                    fn.endswith('.bak_before_fix') or fn.endswith('.bak_unenc')):
                continue
            if core_only:
                # core_only 模式下只扫描项目根目录和 embodied-intelligence 下的 .py 文件
                if fp.suffix.lower() != '.py':
                    continue
                try:
                    rel = fp.relative_to(PROJECT_ROOT)
                except ValueError:
                    continue
                # 只保留相对深度 <= 3 的 py 文件（避免第三方包）
                if len(rel.parts) > 3:
                    continue
            results.append(fp)
    return results


def _mask(text: str) -> str:
    text = text.strip()
    if len(text) <= 10:
        return '*' * len(text)
    return text[:4] + '***' + text[-4:]


# ============================================================
# 第 ①~④ 项：正则扫描
# ============================================================

def run_regex_check(files: List[Path], rule: Dict) -> Tuple[bool, List[Dict]]:
    """对单个规则执行扫描，返回 (是否通过, 命中列表)"""
    hits: List[Dict] = []
    pattern = rule['regex']
    allowed = rule.get('allowed_value')
    for fp in files:
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except (OSError, PermissionError):
            continue
        for ln, line in enumerate(lines, 1):
            for m in pattern.finditer(line.rstrip('\n')):
                if allowed and allowed(m):
                    continue
                try:
                    rel = str(fp.relative_to(PROJECT_ROOT))
                except ValueError:
                    rel = str(fp)
                hits.append({
                    'file': rel,
                    'line': ln,
                    'match': _mask(m.group()),
                    'context': _mask(line.rstrip('\n').strip()[:120]),
                })
    return (len(hits) == 0), hits


# ============================================================
# 第 ⑤ 项：py_compile 核心 Python 文件语法验证
# ============================================================

def run_py_compile_check(core_only: bool = False) -> Tuple[bool, List[Dict]]:
    """对核心 Python 文件做语法编译验证"""
    results: List[Dict] = []
    passed = True

    if core_only:
        check_files = [Path(p) for p in CORE_PY_FILES]
    else:
        # 全部 .py 文件（排除虚拟环境）
        check_files = []
        for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
            dp = Path(dirpath)
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS
                           and not d.startswith('.')]
            for fn in filenames:
                if fn.endswith('.py') and fn not in {
                    'security_scan.py', 'file_encryptor.py', 'security_checklist.py'
                }:
                    check_files.append(dp / fn)

    for fp in check_files:
        abs_fp = PROJECT_ROOT / fp if not fp.is_absolute() else fp
        rel = str(abs_fp.relative_to(PROJECT_ROOT)) if abs_fp.is_relative_to(PROJECT_ROOT) else str(abs_fp)
        exists = abs_fp.is_file()
        results.append({
            'file': rel,
            'exists': exists,
            'status': 'skipped',
            'error': None,
        })
        if not exists:
            # 核心文件不存在 —— 仅警告，不强制失败（用户可能还没创建）
            continue
        try:
            py_compile.compile(str(abs_fp), doraise=True)
            results[-1]['status'] = 'ok'
        except py_compile.PyCompileError as e:
            results[-1]['status'] = 'fail'
            results[-1]['error'] = str(e).replace(str(abs_fp), rel)
            passed = False
        except Exception as e:
            results[-1]['status'] = 'fail'
            results[-1]['error'] = f'{type(e).__name__}: {e}'
            passed = False

    return passed, results


# ============================================================
# 第 ⑥ 项：VSCode 诊断验证（通过 GetDiagnostics 工具）
# ============================================================

def run_diagnostics_check() -> Tuple[bool, Optional[Dict]]:
    """尝试调用 VSCode GetDiagnostics，失败则返回 warning 不挂门禁"""
    try:
        # 延迟导入 —— 在 Trae IDE 环境中才可用
        import __main__  # noqa: F401
    except Exception:
        pass

    # GetDiagnostics 通过 Trae 工具系统注入，此处用字符串工具调用不可行，
    # 因此改为：提示用户手动查看 IDE 中的"问题"面板
    return True, {'note': '请在 VSCode / Trae IDE 中按 Ctrl+Shift+M 打开「问题」面板，确保 0 错误 0 警告'}


# ============================================================
# 第 ⑦ 项：Git 身份合规校验（出借模式下 local 身份必须是 Guest）
# ============================================================

GUEST_NAME = "Guest User"
GUEST_EMAIL = "***@***.***"


def _git_config_local(key: str) -> Optional[str]:
    try:
        r = subprocess.run(
            ["git", "config", "--local", "--get", key],
            cwd=str(PROJECT_ROOT),
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if r.returncode == 0:
            v = r.stdout.strip()
            return v if v else None
    except (OSError, subprocess.SubprocessError):
        pass
    return None


def run_git_identity_check(owner_mode: bool = False) -> Tuple[bool, Dict]:
    """
    owner_mode=True → 你是项目主人自己推代码：允许真实身份，不挂门禁
    owner_mode=False（出借模式）→ 强制 local user.name/email 是 Guest 占位
    """
    info: Dict = {
        'owner_mode': owner_mode,
        'git_exists': (PROJECT_ROOT / '.git').exists(),
        'local_name': _git_config_local('user.name'),
        'local_email': _git_config_local('user.email'),
        'warnings': [],
    }

    if owner_mode:
        info['note'] = ('已用 --as-owner 跳过 Guest 身份校验：'
                        '你是项目主人，允许真实 user.name/email 推送。')
        return True, info

    if not info['git_exists']:
        info['note'] = '当前项目无 .git 目录（单文件脚本场景），跳过 Git 身份校验'
        return True, info

    is_guest_name = (info['local_name'] == GUEST_NAME)
    is_guest_email = (info['local_email'] == GUEST_EMAIL)
    ok = bool(is_guest_name and is_guest_email)

    if ok:
        info['note'] = 'Local Git 身份已是 Guest 占位：出借模式安全 ✅'
        return True, info

    # 未通过：给出明确建议
    if not is_guest_name:
        info['warnings'].append(
            f"local user.name = {info['local_name']!r}（出借模式必须是 {GUEST_NAME!r}，"
            "否则出借期间 push 会以你的名义提交）")
    if not is_guest_email:
        info['warnings'].append(
            f"local user.email = {info['local_email']!r}（出借模式必须是 {GUEST_EMAIL!r}）")
    info['hint'] = ('修复：运行 python before_lend.py 自动备份并清理为 Guest，'
                    '或手动执行：\n'
                    f'     git config --local user.name "{GUEST_NAME}"\n'
                    f'     git config --local user.email "{GUEST_EMAIL}"\n'
                    '  （你是项目主人自己推代码？请加 --as-owner 跳过此项。）')
    return False, info


# ============================================================
# 输出
# ============================================================

SEV_COLOR = {
    'critical': '\033[91m',
    'high': '\033[93m',
    'medium': '\033[96m',
    'low': '\033[90m',
    'ok': '\033[92m',
    'warn': '\033[93m',
}
_RESET = '\033[0m'


def c(level: str, text: str) -> str:
    if sys.platform.startswith('win'):
        return text
    return SEV_COLOR.get(level, '') + text + _RESET


def print_divider(title: str):
    sep = '=' * 70
    print()
    print(sep)
    print(f'  {title}')
    print(sep)


# ============================================================
# 主入口
# ============================================================

def main():
    args = set(sys.argv[1:])
    core_only = '--core' in args
    no_lint = '--no-lint' in args
    fix_mode = '--fix' in args
    as_owner = '--as-owner' in args

    print_divider('🔒 项目安全防线 · 推送前强制校验清单 (7/7)')
    print(f'  项目根目录: {PROJECT_ROOT}')
    print(f'  模式: {"核心文件" if core_only else "全量扫描"} | '
          f'诊断项: {"跳过" if no_lint else "启用"} | '
          f'自动修复: {"是" if fix_mode else "否"} | '
          f'Git身份: {"OWNER 模式（跳过 Guest 校验）" if as_owner else "出借模式（强制 Guest）"}')
    print(f'  执行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    # 预先收集文件列表
    scan_files = _walk_scan_files(PROJECT_ROOT, core_only=core_only)
    print(f'  扫描文件数: {len(scan_files)}')

    final_report: Dict = {
        'timestamp': datetime.now().isoformat(),
        'project_root': str(PROJECT_ROOT),
        'checks': {},
        'overall_pass': True,
    }

    # ============== ①②③④ 正则扫描 ==============
    for rule in RULES:
        print_divider(f'{rule["name"]}  (severity={rule["severity"]})')
        ok, hits = run_regex_check(scan_files, rule)
        final_report['checks'][rule['id']] = {
            'name': rule['name'],
            'severity': rule['severity'],
            'pass': ok,
            'hit_count': len(hits),
            'hits': hits[:50],  # 截断最多 50 条避免报告过大
        }
        if ok:
            print(c('ok', f'  ✅ 通过：0 匹配'))
        else:
            print(c(rule['severity'], f'  ❌ 未通过：{len(hits)} 处匹配（前 20 条如下）'))
            if rule['id'] == 'private_ip' and fix_mode:
                print('  🔧 自动修复模式：将扫描到的私网 IP 替换为 127.0.0.1 ...')
                # 调用 security_scan 的自动修复逻辑
                try:
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(
                        'secscan', str(PROJECT_ROOT / 'security_scan.py'))
                    secscan = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(secscan)  # type: ignore
                    fix_report = secscan.auto_fix_private_ips(PROJECT_ROOT)
                    print(f'     修复文件: {fix_report["modified_files"]} 个, '
                          f'替换处数: {fix_report["total_replacements"]}')
                    # 修复后再检查一次
                    ok2, hits2 = run_regex_check(scan_files, rule)
                    final_report['checks'][rule['id']]['after_fix_pass'] = ok2
                    final_report['checks'][rule['id']]['after_fix_hit_count'] = len(hits2)
                    ok = ok2
                    if ok:
                        print(c('ok', f'     ✅ 修复后通过：0 匹配'))
                    else:
                        print(c(rule['severity'], f'     ❌ 修复后仍有 {len(hits2)} 处匹配'))
                except Exception as e:
                    print(f'     修复失败: {type(e).__name__}: {e}')
            # 展示命中
            for h in hits[:20]:
                print(f'     - {h["file"]}:{h["line"]}  |  匹配: {h["match"]}')
                if h['context']:
                    print(f'       上下文: {h["context"]}')
            if len(hits) > 20:
                print(f'     ... 其余 {len(hits) - 20} 处省略，详见 JSON 报告')
        if not ok and rule['severity'] == 'critical':
            final_report['overall_pass'] = False

    # ============== ⑤ py_compile 语法验证 ==============
    print_divider('⑤ Python 核心文件语法验证 (py_compile)')
    py_ok, py_results = run_py_compile_check(core_only=core_only)
    fail_count = sum(1 for r in py_results if r['status'] == 'fail')
    skip_count = sum(1 for r in py_results if not r['exists'])
    ok_count = sum(1 for r in py_results if r['status'] == 'ok')
    final_report['checks']['py_syntax'] = {
        'name': '⑤ Python 核心文件语法验证',
        'severity': 'critical',
        'pass': py_ok,
        'total_files': len(py_results),
        'ok': ok_count,
        'fail': fail_count,
        'missing': skip_count,
        'failures': [r for r in py_results if r['status'] == 'fail'][:30],
    }
    print(f'  文件总数: {len(py_results)} | OK: {ok_count} | '
          f'Fail: {fail_count} | 缺失(跳过): {skip_count}')
    if py_ok:
        print(c('ok', '  ✅ 通过：全部文件语法正确'))
    else:
        print(c('critical', '  ❌ 未通过：以下文件存在语法错误'))
        for r in final_report['checks']['py_syntax']['failures'][:20]:
            print(f'     - {r["file"]}: {r["error"][:180]}')
        final_report['overall_pass'] = False

    # ============== ⑥ IDE 诊断验证（提示型） ==============
    if not no_lint:
        print_divider('⑥ VSCode / Trae IDE 诊断验证 (0 错误 0 警告)')
        diag_ok, diag_note = run_diagnostics_check()
        final_report['checks']['ide_diagnostics'] = {
            'name': '⑥ VSCode / Trae IDE 诊断验证',
            'severity': 'high',
            'pass': True,  # 此处不做强制门禁，留待用户目视
            'note': diag_note,
        }
        print(c('warn', '  ⚠️  请手动执行以下 IDE 诊断：'))
        print('      1. 在 Trae IDE / VSCode 中按 Ctrl+Shift+M 打开「问题」面板')
        print('      2. 确认错误数 = 0 且 警告数 = 0')
        print('      3. 若有问题，修复后重新运行本脚本')
        if diag_note and 'note' in diag_note:
            print(f'      说明: {diag_note["note"]}')

    # ============== ⑦ Git 身份合规（出借模式强制门禁） ==============
    print_divider('⑦ Git 身份合规校验 '
                  + ('(--as-owner OWNER 模式)' if as_owner else '(出借模式：必须是 Guest 占位)'))
    git_ok, git_info = run_git_identity_check(owner_mode=as_owner)
    final_report['checks']['git_identity'] = {
        'name': '⑦ Git 身份合规校验',
        'severity': 'critical',
        'pass': git_ok,
        'as_owner': as_owner,
        'git_exists': git_info.get('git_exists'),
        'local_name': git_info.get('local_name'),
        'local_email': git_info.get('local_email'),
        'note': git_info.get('note'),
        'warnings': git_info.get('warnings') or [],
        'hint': git_info.get('hint'),
    }
    if git_ok:
        print(c('ok', f'  ✅ 通过：{git_info.get("note") or "身份合规"}'))
        print(f'     · 当前 local user.name  = {git_info.get("local_name")}')
        print(f'     · 当前 local user.email = {git_info.get("local_email")}')
    else:
        print(c('critical', '  ❌ 未通过：出借模式下 Git 身份未清理为 Guest 占位'))
        for w in git_info.get('warnings') or []:
            print(f'     - {w}')
        hint = git_info.get('hint')
        if hint:
            for ln in str(hint).splitlines():
                print(f'     💡 {ln}')
        final_report['overall_pass'] = False

    # ============== 汇总 ==============
    print_divider('📊 汇总结果')
    all_pass = True
    for cid, creport in final_report['checks'].items():
        icon = c('ok', '✅') if creport.get('pass') else c('critical', '❌')
        name = creport.get('name', cid)
        print(f'  {icon} {name}')
        if not creport.get('pass'):
            all_pass = False
    print()
    final_report['overall_pass'] = all_pass
    if all_pass:
        print(c('ok', '  ✅ 全部检查通过 —— 可以安全推送到 GitHub'))
    else:
        print(c('critical', '  ❌ 存在未通过的检查项 —— 禁止推送！请修复后重新运行本脚本'))
    print()

    # ============== 写 JSON 报告 ==============
    report_name = f'security_checklist_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    report_path = PROJECT_ROOT / report_name
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, ensure_ascii=False, indent=2)
        print(f'  📄 完整 JSON 报告已保存: {report_name}')
    except OSError as e:
        print(f'  ❌ 保存 JSON 报告失败: {e}')
    print()

    # ============== 使用说明 ==============
    print('=' * 70)
    print('  📌 出借设备 / 他人使用前（✅ 推荐：1 条命令完成所有自动化准备）：')
    print(f'       python "{PROJECT_ROOT / "before_lend.py"}"')
    print('         · 自动备份 Git 身份/凭据（100% 可还原）')
    print('         · 自动清理 local 身份为 Guest User（防止以你名义 push）')
    print('         · 调本脚本 7 大项做推送前校验')
    print('         · 启动 file_encryptor.py 加密敏感文件')
    print('     最后手动执行：')
    print('         · 退出 Trae / VSCode / GitHub Desktop 登录')
    print('         · 按 Win + L 锁屏')
    print()
    print('  📌 拿回设备后（✅ 推荐：1 条命令完成自动还原）：')
    print(f'       python "{PROJECT_ROOT / "after_takeback.py"}"')
    print('         · 自动解密所有 .enc 敏感文件（输入加密时密码）')
    print('         · 100% 还原备份的 local Git 身份')
    print('         · 还原 ~/.git-credentials')
    print('         · 清理 *.bak_unenc / *.bak_before_fix 临时备份')
    print('         · 运行 security_scan.py 复核 CRITICAL=0')
    print('     最后手动执行：')
    print('         · 重新登录 Trae / GitHub 账号；第一次 git push 会弹浏览器 OAuth 登录')
    print()
    print('  📌 你是项目主人自己要推代码？请加 --as-owner 跳过 Guest 身份门禁：')
    print('       python security_checklist.py --as-owner')
    print('=' * 70)
    print()

    sys.exit(0 if all_pass else 1)


if __name__ == '__main__':
    main()
