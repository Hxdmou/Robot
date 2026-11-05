# -*- coding: utf-8 -*-
'''精确核对22模块：PART01-12按all_modules边界，PART13-22按categories字典边界'''
import sys, io, re
sys.stdout.reconfigure(encoding='utf-8')

t = io.open(r'F:\个人作品\具身智能\generate_business_ppt.py', encoding='utf-8').read()
lines = t.split('\n')

FRESH = re.compile(r'2026年8月2[01]日')

# ===== PART 01-12：all_modules.append 边界 =====
parts = {}
for i, l in enumerate(lines):
    m = re.match(r"all_modules\.append\(\('PART (\d+)'", l)
    if m and int(m.group(1)) <= 12:
        parts[int(m.group(1))] = i

print('=== PART 01-12（all_modules结构） ===')
sorted_p = sorted(parts.keys())
for idx, p in enumerate(sorted_p):
    start = parts[p]
    end = parts[sorted_p[idx+1]] if idx+1 < len(sorted_p) else 1380
    seg = '\n'.join(lines[start:end])
    n = len(FRESH.findall(seg))
    print(f'PART {p:02d} | 新鲜条目 {n:>2} | {"OK" if n > 0 else "缺失!"}')

# ===== PART 13-22：make_detail_module 的 categories 列表 =====
# 找到 categories 起始行和每个模块字典的注释/边界
print()
print('=== PART 13-22（make_detail_module categories结构） ===')
cat_start = None
for i, l in enumerate(lines):
    if 'def make_detail_module' in l:
        cat_start = i
        break
# categories内每个模块以注释 "# 智慧农业" 等分隔，或用 {'left': 开头
# 用每个 {'left': [ 作为模块字典起点
module_starts = []
for i in range(cat_start, len(lines)):
    if re.match(r"\s+# (智慧农业|医疗健康|教育AI|能源电力|自动驾驶|人形运动会|真机部署|物流仓储|灵巧手|安防应急)", lines[i]):
        module_starts.append(i)
names = ['智慧农业', '医疗健康', '教育AI', '能源电力', '自动驾驶', '人形运动会', '真机部署', '物流仓储', '灵巧手', '安防应急']
print(f'找到模块注释边界: {len(module_starts)} 个')
for idx, s in enumerate(module_starts):
    e = module_starts[idx+1] if idx+1 < len(module_starts) else len(lines)
    seg = '\n'.join(lines[s:e])
    n = len(FRESH.findall(seg))
    pnum = 13 + idx
    print(f'PART {pnum:02d} {names[idx]} | 新鲜条目 {n:>2} | {"OK" if n > 0 else "缺失!"}')
