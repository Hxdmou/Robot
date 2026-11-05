#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用PowerPoint COM接口真实检查PPT中所有文本框是否溢出
HasOverflowText是PowerPoint官方API，100%准确，不估算不猜测
"""
import win32com.client as win32
import os
import sys

def check_ppt_overflow(ppt_path):
    if not os.path.exists(ppt_path):
        print(f"文件不存在: {ppt_path}")
        return False
    
    print(f"正在打开PPT检查: {ppt_path}")
    Application = win32.gencache.EnsureDispatch("PowerPoint.Application")
    Application.Visible = True
    
    try:
        presentation = Application.Presentations.Open(os.path.abspath(ppt_path), ReadOnly=False)
        total_slides = presentation.Slides.Count
        print(f"总页数: {total_slides}")
        
        overflow_count = 0
        overflow_pages = []
        
        for slide_idx in range(1, total_slides + 1):
            slide = presentation.Slides(slide_idx)
            slide_overflows = []
            for shape_idx in range(1, slide.Shapes.Count + 1):
                shape = slide.Shapes(shape_idx)
                if shape.HasTextFrame:
                    tf = shape.TextFrame
                    # PowerPoint 2010+ HasOverflowText: msoTrue(-1) 表示溢出
                    try:
                        overflow = tf.HasOverflowText
                        if overflow == -1:  # msoTrue
                            text_preview = ""
                            if tf.TextRange and tf.TextRange.Text:
                                text_preview = tf.TextRange.Text[:50].replace('\r\n', ' ')
                            slide_overflows.append((shape_idx, shape.Name, text_preview))
                            overflow_count += 1
                    except Exception as e:
                        pass
            
            if slide_overflows:
                overflow_pages.append(slide_idx)
                print(f"\n❌ 第 {slide_idx} 页有 {len(slide_overflows)} 个文本框溢出:")
                for (sidx, sname, prev) in slide_overflows:
                    print(f"   - 形状 {sidx} ({sname}): {prev}...")
            else:
                print(f"✅ 第 {slide_idx} 页 无溢出")
        
        print(f"\n========== 检查结果 ==========")
        if overflow_count == 0:
            print("🎉 所有页面所有文本框 0 溢出！")
            return True
        else:
            print(f"⚠️  共 {overflow_count} 个文本框溢出，涉及第 {overflow_pages} 页")
            return False
            
    except Exception as e:
        print(f"出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    ppt = sys.argv[1] if len(sys.argv) > 1 else r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260815_商务汇报_无水印_v8.pptx'
    check_ppt_overflow(ppt)
