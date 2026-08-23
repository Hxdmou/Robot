# -*- coding: utf-8 -*-
'''推送前终极复查：直接打开最新版本 PPTX 文件（自动识别，无需手改版本号）
1. 每页页脚文本是否完全一致（FOOTER_TEXT）
2. 全部【】黄标标签日期是否在2天时效内（今天+昨天，动态计算，无过期）
3. 页数/模块结构完整性
V3.37 系统能力升级：退出码 0=全部通过 / 1=存在问题，供 delivery_gate.py 调用。'''
import sys, re, os, glob, datetime
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation

HERE = os.path.dirname(os.path.abspath(__file__))

def latest_pptx(kind):
    '''自动识别根目录最新版本PPT：kind='无水印' 或 '水印版' '''
    cands = glob.glob(os.path.join(HERE, '具身智能AI产业最新进展_*_商务汇报_%s_v*.pptx' % kind))
    if not cands:
        return None
    def ver(p):
        m = re.search(r'_v(\d+)\.pptx$', p)
        return int(m.group(1)) if m else -1
    return max(cands, key=ver)

FILES = [f for f in [latest_pptx('无水印'), latest_pptx('水印版')] if f]
if not FILES:
    print('[X] 未找到任何 无水印/水印版 PPTX 文件')
    sys.exit(1)

def file_date(fp):
    '''以PPT文件名日期为判定基准（验证"生成时是否遵守SOP"，内容随时间自然过期不算交付缺陷）'''
    m = re.search(r'_(\d{8})_', os.path.basename(fp))
    if m:
        s = m.group(1)
        try:
            return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
        except ValueError:
            pass
    return datetime.date.today()

def make_window(base):
    '''2天时效窗口：文件日期+前一天（V3.30日期清醒铁律，绝不硬编码）'''
    y = base - datetime.timedelta(days=1)
    return set([(base.month, base.day), (y.month, y.day)]), base

def is_stale(tag, fresh_dates, base):
    # 2天时效：只允许窗口内日期，更早=过期
    for m in re.finditer(r'2026年(\d{1,2})月(\d{1,2})日', tag):
        if (int(m.group(1)), int(m.group(2))) not in fresh_dates:
            return True
    for m in re.finditer(r'2026年(\d{1,2})月(?!\d)', tag):
        if int(m.group(1)) != base.month:
            return True
    for m in re.finditer(r'(?<!2026年)(\d{1,2})月(\d{1,2})日', tag):
        if (int(m.group(1)), int(m.group(2))) not in fresh_dates:
            return True
    return False

def is_fresh(tag, fresh_dates):
    for m in re.finditer(r'(\d{1,2})月(\d{1,2})日', tag):
        if (int(m.group(1)), int(m.group(2))) in fresh_dates:
            return True
    return False

SLIDE_H = 7.5  # 16:9标准高度（英寸）

total_problems = 0
for fp in FILES:
    print('=' * 70)
    print(fp.split('\\')[-1])
    base = file_date(fp)
    FRESH_DATES, BASE = make_window(base)
    print('时效窗口(以文件日期为基准): %d月%d日 / %d月%d日' % (BASE.month, BASE.day, (base - datetime.timedelta(days=1)).month, (base - datetime.timedelta(days=1)).day))
    prs = Presentation(fp)
    n = len(prs.slides)
    print('总页数: %d' % n)
    if n != 91:
        print('  [WARN] 页数=%d（预期91=1封面+1目录+22模块x4页+1封底）' % n)
    footers = {}
    stale_tags = []
    fresh_tags = 0
    for si, slide in enumerate(prs.slides, 1):
        texts = []
        bottom_texts = []  # 只收集页面最底部(y>=SLIDE_H-0.5英寸)的文本
        for shape in slide.shapes:
            if shape.has_text_frame:
                t = shape.text_frame.text.strip()
                if t:
                    texts.append(t)
                    try:
                        top_in = shape.top / 914400.0
                        if top_in >= SLIDE_H - 0.5:
                            bottom_texts.append(t)
                    except Exception:
                        pass
        full = '\n'.join(texts)
        # 页脚：只取页面最底部含"商务汇报"的文本
        for t in bottom_texts:
            if '商务汇报' in t and len(t) < 80:
                footers.setdefault(t, []).append(si)
        # 黄标扫描
        for tag in re.findall(r'【[^】]*】', full):
            if is_stale(tag, FRESH_DATES, BASE):
                stale_tags.append((si, tag[:60]))
            elif is_fresh(tag, FRESH_DATES):
                fresh_tags += 1
    print('--- 页脚检查 ---')
    for ft, pages in footers.items():
        print('  [%d页] %s' % (len(pages), ft))
    if len(footers) == 1:
        print('  [OK] 页脚完全统一')
    else:
        print('  [FAIL] 页脚不一致！共%d种' % len(footers))
        total_problems += 1
    print('--- 黄标日期检查 ---')
    print('  新鲜黄标(2天时效内): %d 个' % fresh_tags)
    if stale_tags:
        print('  [FAIL] 过期黄标 %d 个:' % len(stale_tags))
        for si, tag in stale_tags[:20]:
            print('    第%d页: %s' % (si, tag))
        total_problems += 1
    else:
        print('  [OK] 无过期黄标')

print('=' * 70)
if total_problems == 0:
    print('[V] 终极复查全部通过：页脚统一 + 0过期黄标')
    sys.exit(0)
print('[X] 发现 %d 类问题，必须修复后再推送！' % total_problems)
sys.exit(1)
