# -*- coding: utf-8 -*-
'''一次COM实测校准字符宽度常数（V3.30）
打开v30 PPT，对每个多段文本框：sa=0测BoundHeight→算实际行数→与估算行数对比→求校正系数
输出校正后的全角/半角宽度常数'''
import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client
import time
import unicodedata

FP = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260821_商务汇报_无水印_v30.pptx"
LINE_SPACING = 11.0  # pt

def est_lines(text, box_w_pt, sz_pt, fw, hw):
    """用给定全角fw/半角hw常数估算行数"""
    if not text:
        return 1
    prefix_w = sz_pt * fw * 1.3  # '▸ ' 前缀
    first_w = max(box_w_pt - prefix_w, 1.0)
    total_w = sum(sz_pt * fw if unicodedata.east_asian_width(c) in ('F','W') else sz_pt * hw for c in text)
    if total_w <= first_w:
        return 1
    import math
    return 1 + math.ceil((total_w - first_w) / max(box_w_pt, 1.0))

Application = win32com.client.DispatchEx("PowerPoint.Application")
Application.Visible = True
time.sleep(1)
P = Application.Presentations.Open(FP, ReadOnly=True)
time.sleep(2)

ratios = []
for si in range(1, P.Slides.Count + 1):
    try:
        P.Slides(si).Select()
    except Exception:
        pass
    time.sleep(0.05)
    for shape in P.Slides(si).Shapes:
        if not shape.HasTextFrame:
            continue
        try:
            tr = shape.TextFrame.TextRange
            n = tr.Paragraphs().Count
            if n < 2:
                continue
            # 清零段距测自然高度
            pf = tr.ParagraphFormat
            pf.SpaceAfter = 0.0
            time.sleep(0.15)
            B = tr.BoundHeight
            if B < 20 or B > shape.Height * 3:
                continue
            actual_lines = B / LINE_SPACING
            # 估算行数（用当前常数 fw=1.06 hw=0.58）
            # COM返回的shape.Width单位是pt
            box_w_pt = shape.Width
            est_total = 0
            for i in range(1, n + 1):
                t = tr.Paragraphs(i).Text.strip()
                if t:
                    est_total += est_lines(t, box_w_pt, 10, 1.06, 0.58)
            if est_total > 0:
                ratio = actual_lines / est_total
                ratios.append(ratio)
        except Exception:
            pass

P.Close()
Application.Quit()

if ratios:
    import statistics
    avg = statistics.mean(ratios)
    med = statistics.median(ratios)
    print(f"样本数: {len(ratios)}")
    print(f"平均比值(实际/估算): {avg:.4f}")
    print(f"中位比值: {med:.4f}")
    # 校正系数：实际行数/估算行数 < 1 说明估算偏大
    # 新常数 = 旧常数 × 比值
    new_fw = 1.06 * med
    new_hw = 0.58 * med
    print(f"\n校正后常数:")
    print(f"  全角: 1.06 → {new_fw:.3f}")
    print(f"  半角: 0.58 → {new_hw:.3f}")
else:
    print("未收集到有效样本")
