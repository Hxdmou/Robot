# -*- coding: utf-8 -*-
"""诊断news交叉校验未命中标题（一次性脚本）"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.resolve()
EI = ROOT / "embodied-intelligence"
NEWS_DIR = Path(r"F:\个人作品\新内容资讯")

sys.path.insert(0, str(EI))
import ai_landscape_registry as reg
import ai_landscape_registry_r9 as r9

db = list(reg.AI_LANDSCAPE_DB) + list(r9.AI_LANDSCAPE_DB_R9)
db_text = "|".join((p.name + getattr(p, "description", "")) for p in db)

news_files = list(NEWS_DIR.glob("ai-news*.md")) + list(EI.glob("news/*.md"))
miss = []
total = 0
for nf in news_files:
    txt = nf.read_text(encoding="utf-8", errors="replace")
    for head in re.findall(r"^#{2,4}\s*(.+)$", txt, re.M):
        total += 1
        hit = False
        for run in re.findall(r"[\u4e00-\u9fa5]{4,}", head):
            grams = {run[i:i + 4] for i in range(0, len(run) - 3)}
            if any(g in db_text for g in grams):
                hit = True
                break
        if not hit:
            miss.append((nf.name, head.strip()))

print(f"总标题={total} 未命中={len(miss)}")
print("=" * 60)
for fn, h in miss:
    print(f"[{fn}] {h}")
