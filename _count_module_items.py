# -*- coding: utf-8 -*-
'''清点22模块条数：内容(left+right)与细节(detail)是否各达20条（V3.25铁律）'''
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

src = open(r"F:\个人作品\具身智能\generate_business_ppt.py", encoding="utf-8").read()

# 提取 all_modules.append(('PART xx', ...)) 块
# 简单方法：按 "all_modules.append(('PART" 切分
blocks = re.split(r"all_modules\.append\(\('PART ", src)[1:]
results = []
for blk in blocks:
    part_num = blk[:2]
    # 找该块内的所有顶层列表 [ ... ]（用括号深度解析）
    # 简化：统计以 "    ['" 或 "    [" 开头的列表项数量不可靠，改用ast
    results.append((part_num, blk))

# 用ast精确解析整个文件的all_modules结构
import ast
tree = ast.parse(src)
counts = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for tgt in node.targets:
            if isinstance(tgt, ast.Name) and tgt.id == 'all_modules':
                # all_modules = [] 或 append调用
                pass
# 直接找所有 all_modules.append 调用
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        if node.func.attr == 'append' and isinstance(node.func.value, ast.Name) and node.func.value.id == 'all_modules':
            if node.args and isinstance(node.args[0], ast.Tuple):
                tup = node.args[0].elts
                part = tup[0].value if isinstance(tup[0], ast.Constant) else '?'
                lists = [e for e in tup if isinstance(e, ast.List)]
                list_lens = [len(e.elts) for e in lists]
                counts.append((part, list_lens))

print(f"{'模块':<8} {'各列表条数':<30} {'内容(left+right)':<16} {'细节(detail)':<12} {'达标'}")
for part, lens in counts:
    if len(lens) >= 4:
        content = lens[0] + lens[1]
        detail = lens[3] if len(lens) > 3 else lens[-1]
        ok = '✓' if content >= 20 and detail >= 20 else '✗不足'
        print(f"{part:<8} {str(lens):<30} {content:<16} {detail:<12} {ok}")
    else:
        print(f"{part:<8} {str(lens):<30} 结构异常")

# PART 13-22: make_detail_module 使用 categories 列表（每个dict含left/right/process/detail）
print("\n=== PART 13-22（make_detail_module categories） ===")
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for tgt in node.targets:
            if isinstance(tgt, ast.Name) and tgt.id == 'categories':
                if isinstance(node.value, ast.List):
                    for idx, d in enumerate(node.value.elts):
                        if isinstance(d, ast.Dict):
                            lens = {}
                            for k, v in zip(d.keys, d.values):
                                if isinstance(k, ast.Constant) and isinstance(v, ast.List):
                                    lens[k.value] = len(v.elts)
                            content = lens.get('left', 0) + lens.get('right', 0)
                            detail = lens.get('detail', 0)
                            ok = '✓' if content >= 20 and detail >= 20 else '✗不足'
                            print(f"PART {13+idx:<4} {str(lens):<55} 内容{content:<4} 细节{detail:<4} {ok}")
