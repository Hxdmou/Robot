#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
输出所有内容文本框填充率数据，逐页查看
"""
import win32com.client as win32
import os

def show_all_fill_rates(ppt_path):
    print(f"=== 输出所有内容文本框填充率 ===\n")
    
    app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    app.Visible = True
    
    pres = app.Presentations.Open(os.path.abspath(ppt_path), ReadOnly=True)
    
    print(f"{'页码':<4} {'页面类型':<10} {'区域':<8} {'框高(pt)':<8} {'字高(pt)':<8} {'填充率':<6} {'状态'}")
    print("-" * 70)
    
    for slide_idx in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(slide_idx)
        
        page_type = ""
        if slide_idx == 1:
            page_type = "封面"
        elif slide_idx == 2:
            page_type = "目录"
        elif slide_idx == pres.Slides.Count:
            page_type = "封底"
        elif slide_idx % 2 == 1:
            page_type = f"内容页"
        else:
            page_type = f"细节页"
        
        for shape_idx in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(shape_idx)
            if not shape.HasTextFrame:
                continue
            tf = shape.TextFrame
            if not tf.HasText:
                continue
            
            # 跳过小文本框
            if shape.Height < 40:
                continue
            
            try:
                box_h = shape.Height
                margin_t = tf.MarginTop
                margin_b = tf.MarginBottom
                avail = box_h - margin_t - margin_b
                text_h = tf.TextRange.BoundHeight
                fill = text_h / avail if avail > 0 else 0
                overflow = tf.HasOverflowText
                
                pos = ""
                if page_type == "内容页":
                    if shape.Left < 300:
                        pos = "左栏"
                    elif shape.Left > 500:
                        pos = "右栏"
                    else:
                        pos = "通栏"
                else:
                    pos = "通栏"
                
                status = ""
                if overflow == -1:
                    status = "❌溢出"
                elif fill < 0.8:
                    status = "⚠️空隙"
                
                print(f"{slide_idx:<4} {page_type:<10} {pos:<8} {box_h:<8.0f} {text_h:<8.0f} {fill:<6.0%} {status}")
            except Exception as e:
                pass
    
    pres.Close()

if __name__ == '__main__':
    show_all_fill_rates(r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v19.pptx')
