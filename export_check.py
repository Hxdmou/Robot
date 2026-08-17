#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
逐页导出PPT为PNG图片 + 检查所有文本框溢出
"""
import os
import win32com.client
from win32com.client import constants

PPT_PATH = r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v25.pptx'
OUT_DIR = r'F:\个人作品\具身智能\page_check_v25'

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    print('启动PowerPoint...')
    ppt_app = win32com.client.Dispatch('PowerPoint.Application')
    ppt_app.Visible = True
    
    print(f'打开PPT: {PPT_PATH}')
    prs = ppt_app.Presentations.Open(PPT_PATH)
    
    total_pages = prs.Slides.Count
    print(f'总页数: {total_pages}')
    print()
    
    overflow_count = 0
    overflow_info = []
    
    # 逐页导出图片并检查溢出
    for i in range(1, total_pages + 1):
        slide = prs.Slides(i)
        
        # 检查溢出
        page_overflow = []
        for j, shape in enumerate(slide.Shapes):
            if shape.HasTextFrame:
                try:
                    if shape.TextFrame.HasOverflowText:
                        overflow_count += 1
                        text = ''
                        try:
                            text = shape.TextFrame.TextRange.Text[:50]
                        except:
                            text = '[无法读取文本]'
                        info = f'页{i} 形状{j} 溢出: {text}'
                        page_overflow.append(info)
                        overflow_info.append(info)
                except:
                    pass
        
        # 导出为PNG
        out_path = os.path.join(OUT_DIR, f'page_{i:02d}.png')
        slide.Export(out_path, 'PNG', 1920, 1080)
        
        status = 'OK' if len(page_overflow) == 0 else f'溢出{len(page_overflow)}处'
        print(f'页{i:02d}: 导出完成 -> {status}')
        for ov in page_overflow:
            print(f'  !!! {ov}')
    
    print()
    print('=' * 60)
    print(f'检查完成：总计溢出 {overflow_count} 处')
    if overflow_count > 0:
        print('溢出详情：')
        for info in overflow_info:
            print(f'  {info}')
    else:
        print('太棒了！没有发现文本框溢出！')
    print('=' * 60)
    print(f'所有页面图片已导出到: {OUT_DIR}')
    
    prs.Close()
    ppt_app.Quit()

if __name__ == '__main__':
    main()
