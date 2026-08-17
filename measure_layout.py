#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
精确测量PPT每个文本框的文字高度，计算空隙率
"""
import win32com.client as win32
import os
import sys

def measure_ppt(ppt_path):
    if not os.path.exists(ppt_path):
        print(f"文件不存在: {ppt_path}")
        return
    
    print(f"正在测量: {ppt_path}")
    Application = win32.gencache.EnsureDispatch("PowerPoint.Application")
    Application.Visible = True
    
    presentation = Application.Presentations.Open(os.path.abspath(ppt_path), ReadOnly=True)
    total_slides = presentation.Slides.Count
    print(f"总页数: {total_slides}\n")
    
    problem_pages = []
    
    for slide_idx in range(3, 47, 2):  # 内容页是3,5,7...45
        slide = presentation.Slides(slide_idx)
        print(f"=== 第{slide_idx}页 (内容页) ===")
        
        for shape_idx in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(shape_idx)
            if not shape.HasTextFrame:
                continue
            tf = shape.TextFrame
            if not tf.HasText:
                continue
            
            try:
                box_h = shape.Height  # 磅
                text_h = tf.TextRange.BoundHeight
                margin_t = tf.MarginTop
                margin_b = tf.MarginBottom
                available = box_h - margin_t - margin_b
                fill_ratio = text_h / available if available > 0 else 0
                overflow = tf.HasOverflowText
                
                # 判断是哪个区域
                name = ""
                if shape.Left < 350:  # 左栏 < ~4.86英寸
                    name = "左栏"
                elif shape.Left > 500:  # 右栏 > ~6.94英寸
                    name = "右栏"
                else:
                    name = "下部通栏"
                
                if fill_ratio < 0.7 or overflow == -1:
                    problem = "⚠️  "
                    if fill_ratio < 0.7:
                        problem += f"空隙大(填充{fill_ratio:.0%})"
                    if overflow == -1:
                        problem += "溢出!"
                    print(f"  {name}: {problem}  框高{box_h:.0f}pt 文字高{text_h:.0f}pt 填充{fill_ratio:.0%}")
                    
            except Exception as e:
                pass
    
    print("\n=== 细节页 ===")
    for slide_idx in range(4, 48, 2):
        slide = presentation.Slides(slide_idx)
        for shape_idx in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(shape_idx)
            if not shape.HasTextFrame:
                continue
            tf = shape.TextFrame
            if not tf.HasText:
                continue
            
            try:
                box_h = shape.Height
                text_h = tf.TextRange.BoundHeight
                available = box_h - tf.MarginTop - tf.MarginBottom
                fill_ratio = text_h / available if available > 0 else 0
                overflow = tf.HasOverflowText
                
                if fill_ratio < 0.7 or overflow == -1:
                    problem = "⚠️  "
                    if fill_ratio < 0.7:
                        problem += f"空隙大(填充{fill_ratio:.0%})"
                    if overflow == -1:
                        problem += "溢出!"
                    print(f"  第{slide_idx}页: {problem}  框高{box_h:.0f}pt 文字高{text_h:.0f}pt 填充{fill_ratio:.0%}")
            except:
                pass
    
    presentation.Close()

if __name__ == '__main__':
    ppt = sys.argv[1] if len(sys.argv) > 1 else r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v17.pptx'
    measure_ppt(ppt)
