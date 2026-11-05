# -*- coding: utf-8 -*-
'''预扫描：用与_batch_replace2相同的逻辑列出全部过期行，不修改文件'''
import sys, io, re
sys.stdout.reconfigure(encoding='utf-8')

FILE = r'F:\个人作品\具身智能\generate_business_ppt.py'
t = io.open(FILE, encoding='utf-8').read()
lines = t.split('\n')

def is_stale_line(line):
    tags = re.findall(r'【[^】]*】', line)
    for tag in tags:
        for m in re.finditer(r'2026年(\d{1,2})月(\d{1,2})日', tag):
            month, day = int(m.group(1)), int(m.group(2))
            if (month < 8) or (month == 8 and day < 20):
                return True
        for m in re.finditer(r'2026年(\d{1,2})月(?!\d)', tag):
            if int(m.group(1)) < 8:
                return True
        for m in re.finditer(r'(?<!2026年)(\d{1,2})月(\d{1,2})日', tag):
            month, day = int(m.group(1)), int(m.group(2))
            if (month < 8) or (month == 8 and day < 20):
                return True
    return False

def get_part(ln):
    if 600 <= ln <= 750: return 'PART01'
    elif 750 < ln <= 850: return 'PART03'
    elif 1100 <= ln <= 1250: return 'PART09'
    elif 1250 < ln <= 1450: return 'PART12'
    elif 1800 <= ln <= 1950: return 'PART21'
    return 'OTHER'

count = 0
from collections import Counter
pc = Counter()
for i, l in enumerate(lines):
    s = l.strip()
    if not (s.startswith("'【") or s.startswith('"【')):
        continue
    if is_stale_line(l):
        count += 1
        part = get_part(i+1)
        pc[part] += 1
        tag = re.findall(r'【[^】]*】', s)
        print(f'L{i+1} [{part}] {tag[0] if tag else "?"} :: {s[:50]}')
print('='*50)
print(f'总计过期: {count}')
for k, v in sorted(pc.items()):
    print(f'  {k}: {v}')
