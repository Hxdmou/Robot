# -*- coding: utf-8 -*-
'''最终验证：真实高度=B+末段SpaceAfter（BoundHeight不含末段段间距）'''
import sys, io
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client
import time

FILES = [
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260822_商务汇报_无水印_v36.pptx",
]
out = io.open(r'F:\个人作品\具身智能\_verify_v36.txt', 'w', encoding='utf-8')
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
                time.sleep(0.2)
                vals = sorted([tr.BoundHeight for _ in range(5)])
                B = vals[2]
                if B > H + 2:
                    ov += 1
                    worst.append('页%d 溢出%.1f (B=%.1f H=%.1f)' % (si, B - H, B, H))
                elif H - B > 6:
                    gp += 1
                    worst.append('页%d 空隙%.1f' % (si, H - B))
            except Exception:
                pass
    out.write('%s: 溢出=%d 真实空隙=%d\n' % (fp.split('\\')[-1], ov, gp))
    for w in worst:
        out.write('  %s\n' % w)
    P.Close()
    time.sleep(1)
Application.Quit()
out.write('最终验证完成\n')
out.close()
print('验证结果已写入 _verify_v36.txt')
