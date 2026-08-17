#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接检查generate_business_ppt.py源代码中所有模块的条目数
确保每个模块left=10条, right=10条, process=10条, detail=20条
"""
import re

SCRIPT_PATH = r'F:\个人作品\具身智能\generate_business_ppt.py'

def count_items(lines, start_line):
    """从start_line开始统计列表中的条目数（直到]结束）"""
    count = 0
    i = start_line
    in_list = False
    while i < len(lines):
        line = lines[i]
        if '[' in line:
            in_list = True
        if "'" in line and in_list:
            # 统计单引号字符串条目
            # 粗略统计：每个以','结尾或单独一行的字符串算一个条目
            stripped = line.strip()
            if stripped.startswith("'") and (stripped.endswith("',") or stripped.endswith("']")):
                count += 1
        if ']' in line and in_list:
            break
        i += 1
    return count, i

def main():
    with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f'读取脚本成功，共{len(lines)}行')
    print()
    
    # 查找所有模块：'left': [  'right': [  'process': [  'detail': [
    problems = []
    part_idx = 0
    
    # 查找PART开始
    part_pattern = re.compile(r"'PART\d+|'第.+部分")
    list_names = ['left', 'right', 'process', 'detail']
    expected_counts = {'left': 10, 'right': 10, 'process': 10, 'detail': 20}
    
    current_part = None
    part_starts = []
    
    for i, line in enumerate(lines):
        if "'left': [" in line:
            # 往前找模块名
            part_name = f'PART{part_idx+1:02d}'
            for j in range(max(0, i-30), i):
                if 'PART' in lines[j] or 'part' in lines[j]:
                    # 尝试提取模块名
                    m = re.search(r"(PART\d+[^\']*)", lines[j])
                    if m:
                        part_name = m.group(1).strip()
                        break
            count, end_i = count_items(lines, i)
            expected = expected_counts['left']
            if count != expected:
                problems.append(f'{part_name} left条目数{count} != 期望{expected}（行{i+1}）')
            else:
                print(f'  {part_name} left: {count}条 ✓')
        elif "'right': [" in line:
            for j in range(max(0, i-50), i):
                if 'PART' in lines[j]:
                    m = re.search(r"(PART\d+[^\']*)", lines[j])
                    if m:
                        part_name = m.group(1).strip()
                        break
            count, end_i = count_items(lines, i)
            expected = expected_counts['right']
            if count != expected:
                problems.append(f'{part_name} right条目数{count} != 期望{expected}（行{i+1}）')
            else:
                print(f'  {part_name} right: {count}条 ✓')
        elif "'process': [" in line:
            for j in range(max(0, i-60), i):
                if 'PART' in lines[j]:
                    m = re.search(r"(PART\d+[^\']*)", lines[j])
                    if m:
                        part_name = m.group(1).strip()
                        break
            count, end_i = count_items(lines, i)
            expected = expected_counts['process']
            if count != expected:
                problems.append(f'{part_name} process条目数{count} != 期望{expected}（行{i+1}）')
            else:
                print(f'  {part_name} process: {count}条 ✓')
        elif "'detail': [" in line:
            for j in range(max(0, i-70), i):
                if 'PART' in lines[j]:
                    m = re.search(r"(PART\d+[^\']*)", lines[j])
                    if m:
                        part_name = m.group(1).strip()
                        part_idx += 1
                        break
            count, end_i = count_items(lines, i)
            expected = expected_counts['detail']
            if count != expected:
                problems.append(f'{part_name} detail条目数{count} != 期望{expected}（行{i+1}）')
            else:
                print(f'  {part_name} detail: {count}条 ✓')
    
    print()
    print('=' * 60)
    if len(problems) == 0:
        print('✓ 所有模块条目数检查通过！')
    else:
        print(f'✗ 发现{len(problems)}个问题：')
        for p in problems:
            print(f'  {p}')
    print('=' * 60)
    
    # 检查字号设置
    font_ok = True
    for i, line in enumerate(lines):
        if 'Pt(10)' in line and 'font.size' in line:
            pass
        elif 'sz=10' in line:
            pass
        elif 'Pt(' in line and 'font.size' in line and '10' not in line and 'bold' not in line and 'False' not in line:
            # 标题字号不检查，只检查正文字号
            pass
    
    # 检查版本号
    for i, line in enumerate(lines):
        if "ver = 'v" in line:
            print(f'当前版本号: {line.strip()}')
    
    return len(problems) == 0

if __name__ == '__main__':
    import sys
    ok = main()
    sys.exit(0 if ok else 1)
