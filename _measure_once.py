# -*- coding: utf-8 -*-
'''V3.33 一次COM实测（绝不迭代）：
1. 以MEASURE_MODE=True生成sa=0测量版（不裁剪，纯自然高度）
2. COM逐页读取每个内容/细节文本框的真实BoundHeight和每段行数
3. 写入_layout_final.py，供generate_business_ppt.py最终生成时精确反解段间距'''
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import time
import win32com.client

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import generate_business_ppt as g

# ========== 第1步：生成测量版 ==========
g.MEASURE_MODE = True
prs = g.generate(enable_watermark=False)
measure_ppt = os.path.join(HERE, '_measure_v31.pptx')
prs.save(measure_ppt)
print('测量版已生成: ' + measure_ppt)
g.MEASURE_MODE = False

# ========== 第2步：COM实测 ==========
SLIDE_W = 13.333
Application = win32com.client.DispatchEx("PowerPoint.Application")
Application.Visible = True
time.sleep(1)
P = Application.Presentations.Open(measure_ppt, ReadOnly=True)
time.sleep(2)

MEASURED = {}

def read_bound(tr):
    '''V3.33高精度：21次采样取众数（BoundHeight会吸附到离散值），懒加载防护40~2000pt'''
    from collections import Counter
    vals = []
    for _ in range(21):
        try:
            v = tr.BoundHeight
            if 40 <= v <= 2000:
                vals.append(round(v, 1))
        except Exception:
            pass
        time.sleep(0.03)
    if not vals:
        return None
    # 众数优先（最稳定的渲染值），平票时取中位数
    cnt = Counter(vals)
    top = cnt.most_common()
    best = top[0][0]
    return best

n_slides = P.Slides.Count
print('总页数: ' + str(n_slides))
# V3.36四页/模块：第3页起每模块4页（C1内容第一页/C2内容第二页/D1细节第一页/D2细节第二页）
for si in range(3, n_slides):
    module_idx = (si - 3) // 4
    pos = (si - 3) % 4
    part_num = 'PART %02d' % (module_idx + 1)
    try:
        P.Slides(si).Select()
    except Exception:
        pass
    time.sleep(0.5)  # 充分等待该页布局稳定
    for shape in P.Slides(si).Shapes:
        if not shape.HasTextFrame:
            continue
        try:
            tr = shape.TextFrame.TextRange
            if len(tr.Text.strip()) == 0:
                continue
            nparas = tr.Paragraphs().Count
            if nparas < 2:
                continue
            B0 = read_bound(tr)
            if not B0:
                continue
            # 每个bullet段落的实测行数（跳过第1段标题）
            para_lines = []
            for pi in range(2, nparas + 1):
                try:
                    ph = tr.Paragraphs(pi).BoundHeight
                    para_lines.append(max(1, int(round(ph / 11.0))))
                except Exception:
                    para_lines.append(1)
            if pos == 0:
                key = part_num + 'C1'
            elif pos == 1:
                # C2页有两个文本框：上部代表动态(top<2英寸)/下部过程阐述
                if shape.Top / 72.0 < 2.0:
                    key = part_num + 'C2R'
                else:
                    key = part_num + 'C2P'
            elif pos == 2:
                key = part_num + 'D1'
            else:
                key = part_num + 'D2'
            MEASURED[key] = {'B0': round(float(B0), 2), 'para_lines': para_lines}
        except Exception:
            pass

P.Close()
time.sleep(1)
Application.Quit()

# ========== 第3步：写入_layout_final.py ==========
out = os.path.join(HERE, '_layout_final.py')
with open(out, 'w', encoding='utf-8') as f:
    f.write('# -*- coding: utf-8 -*-\n')
    f.write('# V3.33 COM一次实测数据（自动生成，禁止手改）\n')
    f.write('MEASURED = {\n')
    for k in sorted(MEASURED):
        f.write('    %r: %r,\n' % (k, MEASURED[k]))
    f.write('}\n')
print('实测完成: %d 个文本框, 已写入 %s' % (len(MEASURED), out))
