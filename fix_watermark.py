#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对水印版也做自动修复
"""
import win32com.client as win32
import os

def auto_fix_watermark(input_path, output_path):
    print(f"处理水印版: {input_path}")
    app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    app.Visible = True
    
    pres = app.Presentations.Open(os.path.abspath(input_path), ReadOnly=False)
    fixed = 0
    
    for slide_idx in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(slide_idx)
        for shape_idx in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(shape_idx)
            if not shape.HasTextFrame:
                continue
            tf = shape.TextFrame
            if not tf.HasText:
                continue
            if shape.Height < 40:
                continue
            
            try:
                box_h = shape.Height
                avail_h = box_h - tf.MarginTop - tf.MarginBottom
                paras = tf.TextRange.Paragraphs()
                n = paras.Count
                if n <= 2:
                    continue
                
                for i in range(1, n + 1):
                    paras(i).ParagraphFormat.SpaceAfter = 0
                base_h = tf.TextRange.BoundHeight
                
                if base_h >= avail_h * 0.98:
                    continue
                
                target_h = avail_h * 0.92
                low, high, best = 0, 15, 0
                for _ in range(12):
                    mid = (low + high) / 2
                    for i in range(1, n + 1):
                        paras(i).ParagraphFormat.SpaceAfter = mid
                    try:
                        overflow = tf.HasOverflowText
                        cur_h = tf.TextRange.BoundHeight
                    except:
                        overflow = -1
                        cur_h = avail_h + 100
                    if overflow == -1 or cur_h > avail_h:
                        high = mid
                    else:
                        best = mid
                        if cur_h < target_h:
                            low = mid
                        else:
                            high = mid
                
                final_sa = max(0, best - 0.3)
                for i in range(1, n + 1):
                    paras(i).ParagraphFormat.SpaceAfter = final_sa
                fixed += 1
            except:
                pass
    
    pres.SaveAs(os.path.abspath(output_path))
    print(f"水印版处理完成，调整了{fixed}个文本框")
    print(f"保存至: {output_path}")
    
    # 验证
    overflow = 0
    for slide_idx in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(slide_idx)
        for shape_idx in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(shape_idx)
            if shape.HasTextFrame:
                try:
                    if shape.TextFrame.HasOverflowText == -1:
                        overflow += 1
                except:
                    pass
    print(f"水印版溢出: {overflow}个")
    return overflow == 0

if __name__ == '__main__':
    inp = r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_水印版_v20.pptx'
    out = r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_水印版_最终版.pptx'
    auto_fix_watermark(inp, out)
