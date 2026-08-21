# -*- coding: utf-8 -*-
'''全量盘点V2：22个模块的内容/细节数量 + 过期黄标分布（日期<20）'''
import sys, io, re
sys.stdout.reconfigure(encoding='utf-8')

t = io.open(r'F:\个人作品\具身智能\generate_business_ppt.py', encoding='utf-8').read()
lines = t.split('\n')

def tag_dates(line):
    return [int(d) for d in re.findall(r'【[^】]*?2026年8月(\d{1,2})日[^】]*】', line)]

def is_stale(line):
    ds = tag_dates(line)
    return any(d < 20 for d in ds)

# ===== PART 01-12 =====
part_starts = []
for i, l in enumerate(lines):
    m = re.match(r"all_modules\.append\(\('(PART \d+)'", l)
    if m:
        part_starts.append((i, m.group(1)))

make_detail_start = None
for i, l in enumerate(lines):
    if 'module_titles_rest' in l and '=' in l:
        make_detail_start = i
        break

print('=' * 70)
print('PART 01-12 模块盘点')
print('=' * 70)

total_stale_01_12 = 0
for idx, (start_line, part_id) in enumerate(part_starts):
    if idx + 1 < len(part_starts):
        end_line = part_starts[idx + 1][0]
    else:
        end_line = make_detail_start if make_detail_start else len(lines)
    
    module_lines = lines[start_line:end_line]
    content_items = [l.strip() for l in module_lines if l.strip().startswith("'【")]
    stale_count = sum(1 for l in content_items if is_stale(l))
    fresh_count = sum(1 for l in content_items if not is_stale(l) and tag_dates(l))
    no_date = sum(1 for l in content_items if not tag_dates(l))
    total_stale_01_12 += stale_count
    
    print(f'{part_id}: 总={len(content_items)}, 过期={stale_count}, 新鲜={fresh_count}, 无日期={no_date}')

# ===== PART 13-22 =====
print('\n' + '=' * 70)
print('PART 13-22 模块盘点')
print('=' * 70)

module_names = ['智慧农业', '医疗健康', '教育AI', '能源电力', '自动驾驶',
                '人形运动会', '真机部署', '物流仓储', '灵巧手', '安防应急']
part_ids = ['PART 13', 'PART 14', 'PART 15', 'PART 16', 'PART 17',
            'PART 18', 'PART 19', 'PART 20', 'PART 21', 'PART 22']

# 找到每个模块注释的行号
module_comment_lines = {}
for i, l in enumerate(lines):
    stripped = l.strip()
    for mn in module_names:
        if stripped == f'# {mn}':
            module_comment_lines[mn] = i

# 按行号排序
sorted_modules = sorted(module_comment_lines.items(), key=lambda x: x[1])

total_stale_13_22 = 0
for idx, (mn, start) in enumerate(sorted_modules):
    if idx + 1 < len(sorted_modules):
        end = sorted_modules[idx + 1][1]
    else:
        # 最后一个模块到文件末尾或make_detail_module函数结束
        end = len(lines)
    
    module_lines = lines[start:end]
    content_items = [l.strip() for l in module_lines if l.strip().startswith("'【")]
    stale_count = sum(1 for l in content_items if is_stale(l))
    fresh_count = sum(1 for l in content_items if not is_stale(l) and tag_dates(l))
    no_date = sum(1 for l in content_items if not tag_dates(l))
    total_stale_13_22 += stale_count
    
    pid = part_ids[module_names.index(mn)]
    print(f'{pid} {mn}: 总={len(content_items)}, 过期={stale_count}, 新鲜={fresh_count}, 无日期={no_date}')
    if stale_count > 0:
        for l in content_items:
            if is_stale(l):
                dates = tag_dates(l)
                print(f'  [过期] 日期{dates}: {l[:70]}...')

# ===== 汇总 =====
print('\n' + '=' * 70)
total_stale = total_stale_01_12 + total_stale_13_22
print(f'PART 01-12 过期: {total_stale_01_12}')
print(f'PART 13-22 过期: {total_stale_13_22}')
print(f'全文件过期黄标总计: {total_stale}')
print(f'注册表(4)新鲜条目: 32')
print(f'缺口: {total_stale - 32} 条需要额外搜索补充')
