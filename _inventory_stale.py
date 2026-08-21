# -*- coding: utf-8 -*-
'''全量盘点：generate_business_ppt.py中所有过期黄标（8月1-19日）按模块归类'''
import sys, io, re
sys.stdout.reconfigure(encoding='utf-8')

t = io.open(r'F:\个人作品\具身智能\generate_business_ppt.py', encoding='utf-8').read()
lines = t.split('\n')

# 找到每个模块的起始行
module_starts = []
for i, l in enumerate(lines):
    m = re.match(r"all_modules\.append\(\('(PART \d+)',\s*'([^']+)'", l)
    if m:
        module_starts.append((i + 1, m.group(1), m.group(2)))

# PART 13-22由module_titles_rest生成
for i, l in enumerate(lines):
    m = re.match(r"\s*\('(PART \d+)',\s*'([^']+)',", l)
    if m and int(m.group(1).split()[-1]) >= 13:
        module_starts.append((i + 1, m.group(1), m.group(2)))

module_starts.sort()

def find_module(lineno):
    cur = 'HEADER/OTHER'
    for start, pid, title in module_starts:
        if lineno >= start:
            cur = f'{pid} {title}'
        else:
            break
    return cur

# 扫描过期日期
stale = []
for i, l in enumerate(lines):
    dates = re.findall(r'2026年8月(\d{1,2})日', l)
    old = [d for d in dates if int(d) < 20]
    if old:
        # 提取该行中的【】标签
        tags = re.findall(r'【[^】]*】', l)
        stale.append((i + 1, find_module(i + 1), old, tags[:3], l.strip()[:100]))

print(f'过期条目总数: {len(stale)}')
print('=' * 80)
by_module = {}
for lineno, mod, dates, tags, snippet in stale:
    by_module.setdefault(mod, []).append((lineno, dates, tags, snippet))

for mod, items in by_module.items():
    print(f'\n### {mod} ({len(items)}处过期)')
    for lineno, dates, tags, snippet in items:
        print(f'  L{lineno} 日期{dates} {tags}')
