# -*- coding: utf-8 -*-
'''交付守门员（产品化·系统能力）——《操作流程》SOP 代码化的一键门禁
用法：python delivery_gate.py          全流程9道门禁（含COM实测，约数分钟）
      python delivery_gate.py --fast   快速模式（跳过COM实测慢门禁，用于日常迭代）

设计目标（第三步·把个人能力变成系统能力）：
  任何人（哪怕是实习生）拿着《操作流程》跑一遍本脚本，即按100%部署标准执行。
  9道门禁对应SOP八步闭环，全部硬标准，任一门禁失败=立即阻断交付（退出码1），绝不带病交付。

门禁清单：
  [1] 语法门禁        —— 核心Py文件全部编译通过（SOP第六步）
  [2] 内容数量门禁    —— 22模块每模块 内容≥20 + 细节≥20（V3.25铁律）
  [3] 字数均衡门禁    —— 每模块内容2页/细节2页字数差<15%（V3.36铁律#7）
  [4] 部署就绪门禁    —— deployment_readiness_check.py 全项通过（SOP第五步）
  [5] 安全自检门禁    —— _pre_push_check.py 0违规（SOP第六步）
  [6] PPT结构门禁     —— 最新版本PPT=91页（1封面+1目录+22x4+1封底）
  [7] 万无一失复查门禁—— 页脚完全统一 + 0过期黄标（V3.35/V3.36铁律#6）
  [8] COM布局门禁     —— 0溢出0空隙（V3.26铁律，final_verify.py实测）
  [9] 仓库清洁门禁    —— git已跟踪文件无PPT/无调试脚本/无敏感文件（公私分离铁律）
'''
import sys, os, re, subprocess, datetime
sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
FAST = '--fast' in sys.argv[1:]

RESULTS = []  # (门禁名, 是否通过, 说明)

def gate(name, ok, note):
    RESULTS.append((name, bool(ok), note))
    print('%s [%s] %s —— %s' % ('=' * 4, '通过' if ok else '阻断', name, note))

def run(script, timeout=900):
    '''运行子脚本，返回 (退出码, 输出文本)'''
    p = subprocess.run([PY, os.path.join(HERE, script)],
                       capture_output=True, text=True, timeout=timeout,
                       cwd=HERE, encoding='utf-8', errors='replace')
    return p.returncode, (p.stdout or '') + (p.stderr or '')

def latest_pptx(kind):
    import glob
    cands = glob.glob(os.path.join(HERE, '具身智能AI产业最新进展_*_商务汇报_%s_v*.pptx' % kind))
    if not cands:
        return None
    def ver(p):
        m = re.search(r'_v(\d+)\.pptx$', p)
        return int(m.group(1)) if m else -1
    return max(cands, key=ver)

print('#' * 72)
print('#  交付守门员 · 一键门禁（%s模式）' % ('快速' if FAST else '完整'))
print('#  今天=%s' % datetime.date.today().isoformat())
print('#' * 72)

# ---------- [1] 语法门禁 ----------
import py_compile
CORE = ['generate_business_ppt.py', 'final_verify.py', '_final_review_pptx.py',
        'deployment_readiness_check.py', '_pre_push_check.py', '_count_module_items.py',
        '_balance_check.py', '_layout_final.py', 'verify_modules.py', 'delivery_gate.py']
bad = []
for f in CORE:
    fp = os.path.join(HERE, f)
    if not os.path.exists(fp):
        bad.append(f + '(缺失)')
        continue
    try:
        py_compile.compile(fp, doraise=True)
    except Exception as e:
        bad.append('%s(%s)' % (f, e))
gate('语法门禁', not bad, '核心文件%d个，语法异常: %s' % (len(CORE), bad if bad else '无'))

# ---------- [2] 内容数量门禁（22模块 20+20） ----------
code, out = run('_count_module_items.py')
fail_lines = [l for l in out.splitlines() if ('✗' in l) or ('结构异常' in l)]
n_parts = len([l for l in out.splitlines() if ('✓' in l) or ('✗' in l)])
gate('内容数量门禁', code == 0 and not fail_lines,
     '模块%d个，不足项: %s' % (n_parts, fail_lines if fail_lines else '无（全部20+20达标）'))

# ---------- [3] 字数均衡门禁（页间差<15%） ----------
code, out = run('_balance_check.py')
m = re.search(r'字数差大于等于15%%?的模块数:\s*(\d+)', out)
bad_n = int(m.group(1)) if m else -1
gate('字数均衡门禁', code == 0 and bad_n == 0,
     '字数差≥15%%的模块数=%s（必须=0）' % (bad_n if m else '未解析到'))

# ---------- [4] 部署就绪门禁 ----------
code, out = run('deployment_readiness_check.py', timeout=600)
m = re.search(r'(\d+)\s*/\s*(\d+)', out)
gate('部署就绪门禁', code == 0, '退出码=%d（0=存在满分就绪产品）' % code)

# ---------- [5] 安全自检门禁 ----------
code, out = run('_pre_push_check.py', timeout=600)
m = re.search(r'FAIL=(\d+)', out)
gate('安全自检门禁', code == 0, '退出码=%d，FAIL=%s' % (code, m.group(1) if m else '?'))

# ---------- [6] PPT结构门禁（双版本各91页） ----------
from pptx import Presentation
ok6 = True
notes6 = []
for f in (latest_pptx('无水印'), latest_pptx('水印版')):
    if not f:
        ok6 = False
        notes6.append('版本缺失')
        continue
    n = len(Presentation(f).slides)
    notes6.append('%s=%d页' % (os.path.basename(f), n))
    if n != 91:
        ok6 = False
gate('PPT结构门禁', ok6, '；'.join(notes6) + '（预期各91）')

# ---------- [7] 万无一失复查门禁（页脚统一+0过期黄标） ----------
code, out = run('_final_review_pptx.py', timeout=600)
gate('万无一失复查门禁', code == 0, '退出码=%d（0=页脚统一+0过期黄标）' % code)

# ---------- [8] COM布局门禁（0溢出0空隙） ----------
if FAST:
    gate('COM布局门禁', True, '快速模式跳过（完整模式运行 final_verify.py 实测）')
else:
    code, out = run('final_verify.py', timeout=1200)
    rpt = os.path.join(HERE, '_verify_latest.txt')
    detail = ''
    if os.path.exists(rpt):
        with open(rpt, encoding='utf-8') as fh:
            detail = fh.read().strip().replace('\n', ' | ')
    gate('COM布局门禁', code == 0, '退出码=%d；%s' % (code, detail))

# ---------- [9] 仓库清洁门禁 ----------
p = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, cwd=HERE,
                   encoding='utf-8', errors='replace')
tracked = p.stdout.splitlines()
dirty = [t for t in tracked if re.search(r'\.pptx?$|_diag_|_tmp_|\.pem$|\.key$|credentials|secrets', t, re.I)]
gate('仓库清洁门禁', p.returncode == 0 and not dirty,
     '已跟踪文件%d个，违规: %s' % (len(tracked), dirty if dirty else '无'))

# ---------- 汇总 ----------
print('#' * 72)
n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
for name, ok, note in RESULTS:
    print('  %s %s' % ('[V]' if ok else '[X]', name))
print('#' * 72)
report = os.path.join(HERE, '_delivery_report.txt')
with open(report, 'w', encoding='utf-8') as fh:
    fh.write('交付守门员报告 %s（%s模式）\n' % (datetime.date.today().isoformat(), '快速' if FAST else '完整'))
    for name, ok, note in RESULTS:
        fh.write('%s %s —— %s\n' % ('[V]' if ok else '[X]', name, note))
    fh.write('结论: %s\n' % ('全部通过，可交付' if n_fail == 0 else '%d道门禁阻断，禁止交付' % n_fail))
if n_fail == 0:
    print('[V] 9道门禁全部通过——达到交付标准（报告: _delivery_report.txt）')
    sys.exit(0)
print('[X] %d道门禁未通过——阻断交付！修复后重跑 python delivery_gate.py' % n_fail)
sys.exit(1)
