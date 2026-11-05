# -*- coding: utf-8 -*-
'''导出全部过期黄标行的完整内容（仅统计【】标签内日期<20的），按行号输出到文件'''
import sys, io, re
sys.stdout.reconfigure(encoding='utf-8')

t = io.open(r'F:\个人作品\具身智能\generate_business_ppt.py', encoding='utf-8').read()
lines = t.split('\n')

out = io.open(r'F:\个人作品\具身智能\_stale_full.txt', 'w', encoding='utf-8')
count = 0
for i, l in enumerate(lines):
    # 只匹配【】标签内的日期
    tag_dates = re.findall(r'【[^】]*?2026年8月(\d{1,2})日[^】]*】', l)
    old = [d for d in tag_dates if int(d) < 20]
    if old:
        count += 1
        out.write(f'=== L{i+1} 标签日期{old} ===\n')
        out.write(l.strip() + '\n\n')
out.close()
print('过期黄标总数(标签内日期<20):', count)
