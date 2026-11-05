# -*- coding: utf-8 -*-
"""一次性：删除指定product_id块（同名产品保留参数更全的新块）"""
import ast
from pathlib import Path

REMOVE = {"MC-014", "MD-015", "MD-016"}
f = Path(r"F:\个人作品\新内容资讯\ai_landscape_registry（1）.py")
lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
out, removed = [], 0
i = 0
while i < len(lines):
    if lines[i].strip().startswith("AIProduct("):
        j = i
        while j < len(lines) and lines[j].rstrip() != "    ),":
            j += 1
        block = "".join(lines[i:j + 1])
        pid = None
        for ln in lines[i:j + 1]:
            if 'product_id="' in ln:
                pid = ln.split('product_id="')[1].split('"')[0]
                break
        if pid in REMOVE:
            removed += 1
            i = j + 1
            continue
        out.extend(lines[i:j + 1])
        i = j + 1
    else:
        out.append(lines[i])
        i += 1
f.write_text("".join(out), encoding="utf-8")
ast.parse(f.read_text(encoding="utf-8"))
print(f"删除 {removed} 个旧块, 剩余 {len(out)} 行, 语法OK")
