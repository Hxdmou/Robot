# -*- coding: utf-8 -*-
"""诊断：重复ID文件归属 + price_top_rmb使用位置"""
import re
from pathlib import Path
from collections import defaultdict

NEWS = Path(r"F:\个人作品\新内容资讯")
EI = Path(r"f:\个人作品\具身智能\embodied-intelligence")
files = [NEWS / f"ai_landscape_registry（{i}）.py" for i in (1, 2, 3, 4)] + [EI / "ai_landscape_registry.py"]

loc = defaultdict(list)
for f in files:
    if not f.is_file():
        continue
    for m in re.finditer(r'product_id="([^"]+)"', f.read_text(encoding="utf-8", errors="replace")):
        loc[m.group(1)].append(f.name)

dups = {k: v for k, v in loc.items() if len(v) > 1}
print(f"活动链内重复ID数: {len(dups)}")
by_pair = defaultdict(list)
for k, v in sorted(dups.items()):
    by_pair[tuple(sorted(set(v)))].append(k)
for pair, ids in by_pair.items():
    print(f"  {' + '.join(pair)}: {len(ids)}个 例: {ids[:5]}")

print("\nprice_top_rmb 使用位置:")
for f in files:
    if not f.is_file():
        continue
    n = f.read_text(encoding="utf-8", errors="replace").count("price_top_rmb")
    if n:
        print(f"  {f.name}: {n}处")
