# -*- coding: utf-8 -*-
"""一次性去重：活动链(1)(2)(3)(4)内，后出现的重复product_id块整块删除（保留先出现者）"""
import re
import ast
from pathlib import Path

NEWS = Path(r"F:\个人作品\新内容资讯")
files = [NEWS / f"ai_landscape_registry（{i}）.py" for i in (1, 2, 3, 4)]

seen = set()
total_removed = 0
for f in files:
    lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
    out, removed = [], 0
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("AIProduct("):
            # 找块结束：第一个恰好4空格缩进的 '),' 行
            j = i
            while j < len(lines) and lines[j].rstrip() != "    ),":
                j += 1
            block = "".join(lines[i:j + 1])
            m = re.search(r'product_id="([^"]+)"', block)
            pid = m.group(1) if m else None
            if pid and pid in seen:
                removed += 1
                i = j + 1
                continue
            if pid:
                seen.add(pid)
            out.extend(lines[i:j + 1])
            i = j + 1
        else:
            out.append(lines[i])
            i += 1
    if removed:
        f.write_text("".join(out), encoding="utf-8")
        ast.parse(f.read_text(encoding="utf-8"))
    total_removed += removed
    print(f"{f.name}: 删除重复块 {removed} 个, 剩余 {len(out)} 行, 语法OK")
print(f"共删除 {total_removed} 个重复块")
