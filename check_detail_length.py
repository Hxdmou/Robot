#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 统计所有detail条目长度
import re
import sys
sys.path.insert(0, r'F:\个人作品\具身智能')

with open(r'F:\个人作品\具身智能\generate_business_ppt.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到所有detail部分（▎最新行情开头的列表）
idx = 0
problems = 0
for m in re.finditer(r"'▎最新行情.*?\n    \[(.*?)\]\)", content, re.DOTALL):
    list_content = m.group(1)
    # 提取每条字符串
    items = re.findall(r"'(.*?)',?\n", list_content)
    print(f"\n=== 模块Detail，共{len(items)}条 ===")
    for i, item in enumerate(items, 1):
        l = len(item)
        status = "✅" if 160 <= l <= 240 else "⚠️" if 120 <= l < 160 else "❌太短" if l < 120 else "⚠️太长"
        if l < 120:
            problems += 1
        print(f"  {i:2d}. [{l:3d}字] {status} {item[:50]}...")

print(f"\n\n总问题条目（短于120字）: {problems}条")
