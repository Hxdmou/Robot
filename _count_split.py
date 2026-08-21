# -*- coding: utf-8 -*-
'''统计22模块各列表条目数，规划4页拆分'''
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import generate_business_ppt as g

print('%-8s | %4s %4s %4s | %4s' % ('模块', '左栏', '右栏', '过程', '细节'))
print('-' * 45)
for m in g.all_modules:
    part, title = m[0], m[1]
    l, r, p, d = len(m[2]), len(m[3]), len(m[5]), len(m[7])
    print('%-8s | %4d %4d %4d | %4d' % (part, l, r, p, d))
print('总模块数: %d' % len(g.all_modules))
