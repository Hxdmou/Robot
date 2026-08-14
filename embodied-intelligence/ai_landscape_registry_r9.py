#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 代理加载文件：新内容统一存放于 F:\个人作品\新内容资讯\ 目录
# 文件命名规则（V3.15 用户亲定·中文括号·写满2000行再开新文件）：
#   ai_landscape_registry（1）.py = 原始基础内容（13235行，历史归档，不再修改）
#   ai_landscape_registry（2）.py = 当前正在写入的新内容文件（当前976行，写满2000行前一直往这里追加）
#   ai_landscape_registry（3）.py = 等（2）写满2000行后再开新文件
#   以此类推，每个新文件不超过2000行
# 新增内容时：先检查当前活动文件（编号最大的）行数，<2000行就追加到该文件；≥2000行才开下一个编号文件
import sys
import os
import importlib.util

_CONTENT_DIR = r"F:\个人作品\新内容资讯"

def _load_registry_part(filename):
    fpath = os.path.join(_CONTENT_DIR, filename)
    mod_name = f"_reg_part_{filename.replace('（', 'cn').replace('）', '').replace('.py', '')}"
    spec = importlib.util.spec_from_file_location(mod_name, fpath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    db_list = []
    for attr in dir(module):
        if attr.startswith("AI_LANDSCAPE_DB"):
            val = getattr(module, attr)
            if isinstance(val, list):
                db_list.extend(val)
    return db_list

_parts = []
# === 在此处追加新文件（中文括号编号，写满2000行再开下一个） ===
_parts.extend(_load_registry_part("ai_landscape_registry（1）.py"))
_parts.extend(_load_registry_part("ai_landscape_registry（2）.py"))

AI_LANDSCAPE_DB_R9 = _parts
