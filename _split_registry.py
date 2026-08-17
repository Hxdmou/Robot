# -*- coding: utf-8 -*-
"""一次性脚本：把（3）.py尾部（ROB-086起）拆分到新（4）.py，保证两文件<2000行"""
import ast
from pathlib import Path

p3 = Path(r"F:\个人作品\新内容资讯\ai_landscape_registry（3）.py")
lines = p3.read_text(encoding="utf-8").splitlines(keepends=True)

start = None
for i, ln in enumerate(lines):
    if 'product_id="ROB-086"' in ln:
        start = i - 1  # 空行+AIProduct( 起始
        break
end = None
for i in range(len(lines) - 1, -1, -1):
    if lines[i].strip() == "]":
        end = i
        break
assert start is not None and end is not None, (start, end)

tail = lines[start:end]
header = [ln.replace("PART3", "PART4").replace("持续新增内容（3）", "持续新增内容（4）")
          for ln in lines[:80]]
p4 = Path(r"F:\个人作品\新内容资讯\ai_landscape_registry（4）.py")
p4.write_text("".join(header) + "".join(tail) + "]\n", encoding="utf-8")
p3.write_text("".join(lines[:start]) + "]\n", encoding="utf-8")

for f in (p3, p4):
    ast.parse(f.read_text(encoding="utf-8"))
    print(f.name, len(f.read_text(encoding="utf-8").splitlines()), "行 语法OK")
