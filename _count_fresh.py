# -*- coding: utf-8 -*-
'''清点注册表08-20/21条目数量'''
import sys, re, io, collections
sys.stdout.reconfigure(encoding='utf-8')
files = [r'F:\个人作品\新内容资讯\ai_landscape_registry（1）.py',
         r'F:\个人作品\新内容资讯\ai_landscape_registry（2）.py',
         r'F:\个人作品\新内容资讯\ai_landscape_registry（3）.py',
         r'F:\个人作品\新内容资讯\ai_landscape_registry（4）.py']
cnt = collections.Counter()
total = 0
for f in files:
    try:
        t = io.open(f, encoding='utf-8').read()
    except FileNotFoundError:
        print('不存在:', f)
        continue
    n = len(re.findall(r'AIProduct\(', t))
    total += n
    cnt.update(re.findall(r'publish_date="(2026-08-2[01])"', t))
    print(f.split('\\')[-1], '条目数:', n)
print('总条目:', total)
print('08-20/21条目:', dict(cnt))
