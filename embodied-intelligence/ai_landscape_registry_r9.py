#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 代理加载文件：新内容统一存放于 F:\个人作品\新内容资讯\ 目录
# 文件命名规则（V3.14 用户亲定·中文括号）：
#   ai_landscape_registry（1）.py = 原始基础内容（一万多行）
#   ai_landscape_registry（2）.py = V3.9后新增内容
#   ai_landscape_registry（3）.py = 后续继续添加...（每个文件≤2000行）
# 新增文件时，在下方追加对应的加载行即可
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
# === 在此处追加新文件（中文括号编号） ===
_parts.extend(_load_registry_part("ai_landscape_registry（2）.py"))

AI_LANDSCAPE_DB_R9 = _parts
