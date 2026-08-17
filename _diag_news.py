# -*- coding: utf-8 -*-
"""诊断news交叉校验：不同匹配口径的命中率"""
import re
import sys
from pathlib import Path

sys.path.insert(0, r"f:\个人作品\具身智能\embodied-intelligence")
import ai_landscape_registry as reg
import ai_landscape_registry_r9 as r9

db = list(reg.AI_LANDSCAPE_DB) + list(r9.AI_LANDSCAPE_DB_R9)
db_text = "|".join((p.name + p.description) for p in db)

NEWS = Path(r"F:\个人作品\新内容资讯")
news_files = list(NEWS.glob("ai-news*.md")) + list(Path(r"f:\个人作品\具身智能\embodied-intelligence\news").glob("*.md"))

strict_miss, loose3_miss, loose2_miss = [], [], []
total = 0
for nf in news_files:
    txt = nf.read_text(encoding="utf-8", errors="replace")
    for head in re.findall(r"^#{2,4}\s*(.+)$", txt, re.M):
        total += 1
        toks = [t for t in re.split(r"[·，,：:（）()\s【】+＋/、\-\d]", head) if len(t) >= 4]
        if not (toks and any(k in db_text for k in toks[:3])):
            strict_miss.append(head)
        toks3 = [t for t in re.split(r"[·，,：:（）()\s【】+＋/、\d]", head) if len(t) >= 3]
        if not any(k in db_text for k in toks3):
            loose3_miss.append(head)
        toks2 = [t for t in re.split(r"[·，,：:（）()\s【】+＋/、\d]", head) if len(t) >= 2]
        if not any(k in db_text for k in toks2):
            loose2_miss.append(head)

print(f"标题总数={total}")
print(f"严格(>=4取前3)未命中={len(strict_miss)}")
print(f"宽松(>=3任一)未命中={len(loose3_miss)}")
print(f"宽松(>=2任一)未命中={len(loose2_miss)}")
print("\n宽松3未命中样例:")
for h in loose3_miss[:15]:
    print("  ", h[:50])
