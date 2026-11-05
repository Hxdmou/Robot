# -*- coding: utf-8 -*-
'''验证并将结果写入UTF-8文件，精确定位溢出/空隙页码与形状'''
import sys
import win32com.client
import time

FILES = [
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260821_商务汇报_无水印_v31.pptx",
]
out = open(r"F:\个人作品\具身智能\_verify_result.txt", "w", encoding="utf-8")
Application = win32com.client.DispatchEx("PowerPoint.Application")
Application.Visible = True
time.sleep(1)
for fp in FILES:
    P = Application.Presentations.Open(fp, ReadOnly=True)
    time.sleep(2)
    ov = 0
    gp = 0
    out.write(f"\n=== {fp.split(chr(92))[-1]} ===\n")
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
                    preview = tr.Text[:40].replace('\r', ' ')
                    out.write(f"  页{si} 溢出{B-H:.1f}pt 段数{tr.Paragraphs().Count} [{preview}]\n")
                elif H - B > 6:
                    gp += 1
                    preview = tr.Text[:40].replace('\r', ' ')
                    out.write(f"  页{si} 空隙{H-B:.1f}pt 段数{tr.Paragraphs().Count} [{preview}]\n")
            except Exception:
                pass
    out.write(f"汇总: 溢出={ov} 空隙={gp}\n")
    P.Close()
    time.sleep(1)
Application.Quit()
out.write("\n验证完成\n")
out.close()
print("done")
