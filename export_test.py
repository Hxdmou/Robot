#!/usr/bin/env python
# -*- coding: utf-8 -*-
import win32com.client as win32
import os

ppt_path = r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v22.pptx'
app = win32.gencache.EnsureDispatch("PowerPoint.Application")
app.Visible = True
pres = app.Presentations.Open(os.path.abspath(ppt_path), ReadOnly=True)

# 导出第4页(PART01 detail)和第6页(PART02 detail)测试
for page_num in [4, 6]:
    out = rf'F:\个人作品\具身智能\slide_images\test_page_{page_num}.png'
    pres.Slides(page_num).Export(os.path.abspath(out), "PNG", 1920, 1080)
    print(f"导出第{page_num}页: {out}")

pres.Close()
