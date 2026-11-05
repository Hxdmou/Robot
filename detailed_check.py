#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
详细检测PPT所有页面所有文本框的填充情况，主动找出空隙问题
"""
import win32com.client as win32
import os

def check_all_text_boxes(ppt_path):
    print(f"=== 主动检查PPT所有页面填充情况 ===\n")
    print(f"文件: {ppt_path}\n")
    
    app = win32.gencache.EnsureDispatch("PowerPoint.Application")
    app.Visible = True
    
    pres = app.Presentations.Open(os.path.abspath(ppt_path), ReadOnly=True)
    
    problems = []
    
    for slide_idx in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(slide_idx)
        
        page_name = ""
        if slide_idx == 1:
            page_name = "封面"
        elif slide_idx == 2:
            page_name = "目录"
        elif slide_idx == pres.Slides.Count:
            page_name = "封底"
        elif slide_idx % 2 == 1:
            page_name = f"内容页 PART{(slide_idx-3)//2 + 1}"
        else:
            page_name = f"细节页 PART{(slide_idx-4)//2 + 1}"
        
        for shape_idx in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(shape_idx)
            if not shape.HasTextFrame:
                continue
            tf = shape.TextFrame
            if not tf.HasText:
                continue
            
            # 跳过页眉页脚等小文本框
            if shape.Height < 40:
                continue
            
            try:
                box_h_pt = shape.Height
                margin_t = tf.MarginTop
                margin_b = tf.MarginBottom
                avail_h = box_h_pt - margin_t - margin_b
                text_h = tf.TextRange.BoundHeight
                fill_ratio = text_h / avail_h if avail_h > 0 else 0
                
                has_overflow = tf.HasOverflowText
                
                # 问题判定：填充率<85%有空隙，或溢出
                problem = ""
                if has_overflow == -1:
                    problem = "❌ 溢出"
                elif fill_ratio < 0.85:
                    problem = f"⚠️  空隙大，填充率{fill_ratio:.0%}"
                
                if problem:
                    # 判断区域
                    pos = ""
                    if page_name.startswith("内容页"):
                        if shape.Left < 300:
                            pos = "左栏"
                        elif shape.Left > 500:
                            pos = "右栏"
                        else:
                            pos = "下部通栏"
                    else:
                        pos = "通栏"
                    
                    problems.append({
                        "page": slide_idx,
                        "page_name": page_name,
                        "pos": pos,
                        "fill_ratio": fill_ratio,
                        "box_h": box_h_pt,
                        "text_h": text_h,
                        "overflow": has_overflow == -1,
                        "problem": problem
                    })
                    print(f"第{slide_idx}页 {page_name} {pos}: {problem}")
                    print(f"  文本框高度: {box_h_pt:.0f}pt ({box_h_pt/72:.2f}英寸)")
                    print(f"  文字实际高度: {text_h:.0f}pt ({text_h/72:.2f}英寸)")
                    print(f"  空隙高度: {(avail_h - text_h):.0f}pt ({(avail_h - text_h)/72:.2f}英寸)")
                    print()
            except Exception as e:
                pass
    
    print("\n" + "="*60)
    print(f"检查完成！共发现 {len(problems)} 个问题位置：")
    print("="*60)
    
    for p in problems:
        status = "溢出" if p["overflow"] else f"填充{p['fill_ratio']:.0%}"
        print(f"第{p['page']}页 {p['page_name']} {p['pos']}: {status}")
    
    pres.Close()
    
    return problems

if __name__ == '__main__':
    ppt_path = r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v19.pptx'
    check_all_text_boxes(ppt_path)
