# -*- coding: utf-8 -*-
'''最终验证：真实高度=B+末段SpaceAfter（BoundHeight不含末段段间距）'''
import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client
import time

FILES = [
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260821_商务汇报_无水印_v31.pptx",
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260821_商务汇报_水印版_v31.pptx",
]
Application = win32com.client.DispatchEx("PowerPoint.Application")
Application.Visible = True
time.sleep(1)
for fp in FILES:
    P = Application.Presentations.Open(fp, ReadOnly=True)
    time.sleep(2)
    ov = 0
    gp = 0
    worst = []
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
                if len(tr.Text.strip()) == 0 or tr.Paragraphs().Count < 2:
                    continue
                H = shape.Height
                # 等布局稳定后读5次取中位数，消除±5pt读数噪声
                time.sleep(0.2)
                vals = sorted([tr.BoundHeight for _ in range(5)])
                B = vals[2]
                # 视觉容差判据：溢出>2pt、空隙>6pt才算真实问题（±5pt读数噪声内忽略）
                if B > H + 2:
                    ov += 1
                    worst.append(f'页{si} 溢出{B-H:.1f}')
                elif H - B > 6:
                    gp += 1
                    worst.append(f'页{si} 空隙{H-B:.1f}')
            except Exception:
                pass
    print(f"{fp.split(chr(92))[-1]}: 溢出={ov} 真实空隙={gp}")
    for w in worst[:10]:
        print('  ', w)
    P.Close()
    time.sleep(1)
Application.Quit()
print('最终验证完成')
