# -*- coding: utf-8 -*-
'''全面扫描：【】标签内所有格式的过期日期（<2026-08-20）
格式覆盖：2026年8月X日 / 2026年7月X日 / 2026年X月 / 2026年X月X日 / X月X日 等
'''
import sys, io, re
sys.stdout.reconfigure(encoding='utf-8')

t = io.open(r'F:\个人作品\具身智能\generate_business_ppt.py', encoding='utf-8').read()
lines = t.split('\n')

def extract_tag_dates(line):
    """提取【】标签内的所有日期，返回(日期字符串, 是否过期)列表"""
    results = []
    tags = re.findall(r'【[^】]*】', line)
    for tag in tags:
        # 格式1: 2026年X月X日
        for m in re.finditer(r'2026年(\d{1,2})月(\d{1,2})日', tag):
            month, day = int(m.group(1)), int(m.group(2))
            stale = (month < 8) or (month == 8 and day < 20)
            results.append((f'2026年{month}月{day}日', stale))
        # 格式2: 2026年X月（无日）
        for m in re.finditer(r'2026年(\d{1,2})月(?!\d)', tag):
            month = int(m.group(1))
            # 8月无日期的不算过期（可能是8月20/21的简写），但7月及以前算过期
            stale = month < 8
            results.append((f'2026年{month}月', stale))
        # 格式3: 8月X日（无年份，在标签内）
        for m in re.finditer(r'(?<!2026年)(\d{1,2})月(\d{1,2})日', tag):
            month, day = int(m.group(1)), int(m.group(2))
            stale = (month < 8) or (month == 8 and day < 20)
            results.append((f'{month}月{day}日', stale))
    return results

total_stale = 0
stale_lines = []
for i, l in enumerate(lines):
    if not l.strip().startswith("'【"):
        continue
    dates = extract_tag_dates(l)
    stale_dates = [d for d, s in dates if s]
    if stale_dates:
        total_stale += 1
        stale_lines.append((i+1, stale_dates, l.strip()[:100]))

print(f'全面扫描结果：【】标签内含过期日期的条目 = {total_stale}')
print('=' * 70)
for ln, dates, preview in stale_lines:
    print(f'L{ln} 过期日期{dates}: {preview}...')
