# -*- coding: utf-8 -*-
'''彻底扫描：任何包含【】标签且含过期日期的内容行（含'[前缀），不修改文件'''
import sys, io, re
sys.stdout.reconfigure(encoding='utf-8')

FILE = r'F:\个人作品\具身智能\generate_business_ppt.py'
t = io.open(FILE, encoding='utf-8').read()
lines = t.split('\n')

def stale_dates_in_line(line):
    """返回行内【】标签中的所有过期日期字符串"""
    results = []
    tags = re.findall(r'【[^】]*】', line)
    for tag in tags:
        for m in re.finditer(r'2026年(\d{1,2})月(\d{1,2})日', tag):
            month, day = int(m.group(1)), int(m.group(2))
            if (month < 8) or (month == 8 and day < 20):
                results.append(f'2026年{month}月{day}日')
        for m in re.finditer(r'2026年(\d{1,2})月(?!\d)', tag):
            if int(m.group(1)) < 8:
                results.append(f'2026年{m.group(1)}月')
        for m in re.finditer(r'(?<!2026年)(\d{1,2})月(\d{1,2})日', tag):
            month, day = int(m.group(1)), int(m.group(2))
            if (month < 8) or (month == 8 and day < 20):
                results.append(f'{month}月{day}日')
    return results

count = 0
for i, l in enumerate(lines):
    s = l.strip()
    # 匹配所有内容行：'【 或 ['【 或 "【 或 ["【
    is_content = (s.startswith("'【") or s.startswith('"【') or
                  s.startswith("['【") or s.startswith('["【'))
    if not is_content:
        continue
    stale = stale_dates_in_line(l)
    if stale:
        count += 1
        tag = re.findall(r'【[^】]*】', s)
        print(f'L{i+1} 过期{stale} {tag[0] if tag else "?"} :: {s[:60]}')
print('='*50)
print(f'彻底扫描过期总数: {count}')
