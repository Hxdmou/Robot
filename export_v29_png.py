# -*- coding: utf-8 -*-
'''导出v29无水印版全部幻灯片为PNG，用于肉眼复核布局'''
import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client
import os
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v29.pptx"
out_dir = r"F:\个人作品\具身智能\_v29_png"
os.makedirs(out_dir, exist_ok=True)

Application = win32com.client.Dispatch("PowerPoint.Application")
Application.Visible = True
time.sleep(1)
Presentation = Application.Presentations.Open(ppt_path, ReadOnly=True)
time.sleep(2)

n = Presentation.Slides.Count
print(f"共 {n} 页，开始导出PNG...")
for i in range(1, n + 1):
    out_file = os.path.join(out_dir, f"slide_{i:02d}.png")
    Presentation.Slides(i).Export(out_file, "PNG", 1280, 720)
print("导出完成:", out_dir)

Presentation.Close()
Application.Quit()
