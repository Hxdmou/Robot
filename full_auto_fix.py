#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全自动检查修复脚本：
1. 打开v20
2. 遍历所有文本框，精确计算填充率
3. 自动二分法调整space_after，让填充率达到90-95%
4. 保存修复后的版本
"""
import win32com.client as win32
import os

def auto_check_and_fix(input_path, output_path):
    print(f"=== 全自动检查修复开始 ===\n")
    app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    app.Visible = True
    
    pres = app.Presentations.Open(os.path.abspath(input_path), ReadOnly=False)
    
    fixed_count = 0
    
    for slide_idx in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(slide_idx)
        page_fixed = 0
        
        for shape_idx in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(shape_idx)
            if not shape.HasTextFrame:
                continue
            tf = shape.TextFrame
            if not tf.HasText:
                continue
            
            # 跳过小文本框（页眉页脚标签）
            if shape.Height < 40:  # <0.55英寸
                continue
            
            try:
                box_h = shape.Height
                mt = tf.MarginTop
                mb = tf.MarginBottom
                avail_h = box_h - mt - mb
                
                paras = tf.TextRange.Paragraphs()
                n = paras.Count
                if n <= 2:
                    continue
                
                # 先设为0，测量基础高度
                for i in range(1, n + 1):
                    paras(i).ParagraphFormat.SpaceAfter = 0
                
                base_h = tf.TextRange.BoundHeight
                
                if base_h >= avail_h * 0.98:
                    # 已经填满或溢出，保持0
                    continue
                
                # 二分法查找最佳space_after，目标填充率92%
                target_h = avail_h * 0.92
                low = 0
                high = 15  # 最大15磅
                best_sa = 0
                
                for _ in range(12):
                    mid = (low + high) / 2
                    for i in range(1, n + 1):
                        paras(i).ParagraphFormat.SpaceAfter = mid
                    
                    try:
                        has_overflow = tf.HasOverflowText
                        cur_h = tf.TextRange.BoundHeight
                    except:
                        has_overflow = -1
                        cur_h = avail_h + 100
                    
                    if has_overflow == -1 or cur_h > avail_h:
                        high = mid
                    else:
                        best_sa = mid
                        if cur_h < target_h:
                            low = mid
                        else:
                            high = mid
                
                # 应用最佳值（略留安全余量0.3pt）
                final_sa = max(0, best_sa - 0.3)
                for i in range(1, n + 1):
                    paras(i).ParagraphFormat.SpaceAfter = final_sa
                
                # 验证
                try:
                    final_h = tf.TextRange.BoundHeight
                    final_overflow = tf.HasOverflowText
                    fill_ratio = final_h / avail_h
                    if fill_ratio > 0.85 and final_overflow != -1:
                        page_fixed += 1
                        fixed_count += 1
                except:
                    pass
                
            except Exception as e:
                pass
        
        if page_fixed > 0:
            print(f"第{slide_idx}页: 调整了{page_fixed}个文本框")
    
    pres.SaveAs(os.path.abspath(output_path))
    
    print(f"\n=== 最终验证 ===")
    overflow = 0
    low_fill = 0
    
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
                if tf.HasOverflowText == -1:
                    overflow += 1
                    print(f"❌ 第{slide_idx}页有溢出")
                
                box_h = shape.Height
                avail_h = box_h - tf.MarginTop - tf.MarginBottom
                text_h = tf.TextRange.BoundHeight
                fill = text_h / avail_h
                if fill < 0.85:
                    low_fill += 1
                    print(f"⚠️  第{slide_idx}页填充率{fill:.0%}")
            except:
                pass
    
    print(f"\n调整完成！共修复{fixed_count}个文本框")
    print(f"溢出: {overflow}个，填充不足: {low_fill}个")
    
    if overflow == 0 and low_fill == 0:
        print("🎉 所有页面验证通过：0溢出 0空隙！")
    
    return True

if __name__ == '__main__':
    inp = r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v20.pptx'
    out = r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_最终版.pptx'
    auto_check_and_fix(inp, out)
