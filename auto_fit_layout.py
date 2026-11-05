#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
精确自适应布局：对每个内容文本框，计算合适的space_after让文字均匀填满
"""
import win32com.client as win32
import os
import sys

def auto_fit_ppt(input_path, output_path):
    print(f"打开PPT: {input_path}")
    app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    app.Visible = True
    
    pres = app.Presentations.Open(os.path.abspath(input_path), ReadOnly=False)
    
    total_adjusted = 0
    
    for slide_idx in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(slide_idx)
        for shape_idx in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(shape_idx)
            if not shape.HasTextFrame:
                continue
            tf = shape.TextFrame
            if not tf.HasText:
                continue
            
            # 跳过太小的文本框（页眉页脚标签等）
            if shape.Height < 40:  # 小于0.55英寸
                continue
            
            try:
                # 可用高度 = 文本框高度 - 上下边距
                avail_h = shape.Height - tf.MarginTop - tf.MarginBottom
                paras = tf.TextRange.Paragraphs()
                n = paras.Count
                if n <= 2:
                    continue
                
                # 先设space_after=0，测量基础文字高度
                for i in range(1, n + 1):
                    paras(i).ParagraphFormat.SpaceAfter = 0
                
                base_h = tf.TextRange.BoundHeight
                
                if base_h >= avail_h:
                    # 内容已经溢出或刚好，保持0
                    continue
                
                # 需要额外分配的空白高度
                extra_h = avail_h - base_h
                # 分配到段落之间（n-1个间隔）
                sa = extra_h / (n - 1)
                # 限制最大8磅，避免太大
                sa = min(sa, 8)
                
                for i in range(1, n + 1):
                    paras(i).ParagraphFormat.SpaceAfter = sa
                
                total_adjusted += 1
            except Exception as e:
                pass
        
        print(f"  第{slide_idx}页处理完成")
    
    pres.SaveAs(os.path.abspath(output_path))
    print(f"\n完成！调整了{total_adjusted}个文本框，保存至: {output_path}")
    
    # 最终溢出检查
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
    if overflow == 0:
        print("🎉 零溢出验证通过！")
    else:
        print(f"⚠️  仍有{overflow}个溢出")
    
    return True

if __name__ == '__main__':
    inp = sys.argv[1] if len(sys.argv) > 1 else r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v18.pptx'
    out = sys.argv[2] if len(sys.argv) > 2 else inp.replace('.pptx', '_最终版.pptx')
    auto_fit_ppt(inp, out)
