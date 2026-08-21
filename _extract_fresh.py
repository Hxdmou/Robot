# -*- coding: utf-8 -*-
'''导出注册表(4)新鲜条目到UTF-8文本文件'''
import sys, importlib.util, io
sys.stdout.reconfigure(encoding='utf-8')

f = r'F:\个人作品\新内容资讯\ai_landscape_registry（4）.py'
spec = importlib.util.spec_from_file_location('reg4', f)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

db = mod.AI_LANDSCAPE_DB_PART4
fresh = [p for p in db if p.publish_date in ('2026-08-20', '2026-08-21')]

out = io.open(r'F:\个人作品\具身智能\_fresh_items.txt', 'w', encoding='utf-8')
out.write(f'新鲜条目总数: {len(fresh)}\n')
out.write('=' * 70 + '\n')
for i, p in enumerate(fresh):
    out.write(f"[{i}] {p.product_id} | {p.publish_date} | {p.category.value} | {p.organization}\n")
    out.write(f"name: {p.name}\n")
    out.write(f"desc: {p.description}\n")
    km = '; '.join(f'{k}={v}' for k, v in (p.key_metrics or {}).items())
    out.write(f"metrics: {km[:500]}\n")
    out.write('-' * 70 + '\n')
out.close()
print('导出完成:', len(fresh), '条')
