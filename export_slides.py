#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
导出PPT所有页面为高清PNG，逐页检查
"""
import win32com.client as win32
import os

def export_all_slides(ppt_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"导出PPT: {ppt_path}")
    app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    app.Visible = True
    
    pres = app.Presentations.Open(os.path.abspath(ppt_path), ReadOnly=True)
    
    total = pres.Slides.Count
    print(f"共{total}页，开始导出高清图片...")
    
    for i in range(1, total + 1):
        slide = pres.Slides(i)
        img_path = os.path.join(output_dir, f"slide_{i:02d}.png")
        # 导出高清：1920x1080 分辨率
        slide.Export(os.path.abspath(img_path), "PNG", 1920, 1080)
        print(f"  导出第{i}页: {img_path}")
    
    pres.Close()
    print(f"\n导出完成！所有图片保存在: {output_dir}")
    return True

if __name__ == '__main__':
    ppt = r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v21.pptx'
    out_dir = r'F:\个人作品\具身智能\slide_images'
    export_all_slides(ppt, out_dir)
