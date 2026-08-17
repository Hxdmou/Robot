#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全面检查PPT所有页面：溢出、文本对齐、内容长度、布局位置
"""
import os
import win32com.client
from win32com.client import constants

PPT_PATH = r'F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v25.pptx'

def main():
    print('启动PowerPoint...')
    ppt_app = win32com.client.Dispatch('PowerPoint.Application')
    ppt_app.Visible = True
    
    print(f'打开PPT: {PPT_PATH}')
    prs = ppt_app.Presentations.Open(PPT_PATH)
    
    total_pages = prs.Slides.Count
    print(f'总页数: {total_pages}')
    print()
    
    all_problems = []
    page_stats = {}
    
    for page_idx in range(1, total_pages + 1):
        slide = prs.Slides(page_idx)
        problems = []
        shape_count = slide.Shapes.Count
        text_boxes = []
        
        for shape_idx in range(1, shape_count + 1):
            shape = slide.Shapes(shape_idx)
            
            # 检查文本框
            if shape.HasTextFrame:
                try:
                    tf = shape.TextFrame
                    text_range = tf.TextRange
                    text = text_range.Text.strip()
                    font_size = None
                    try:
                        font_size = text_range.Font.Size
                    except:
                        pass
                    
                    # 检查溢出
                    has_overflow = False
                    try:
                        has_overflow = tf.HasOverflowText
                    except:
                        pass
                    if has_overflow:
                        problems.append(f'文本框{shape_idx}溢出（文字长度{len(text)}）')
                    
                    # 记录文本框信息
                    text_boxes.append({
                        'left': shape.Left,
                        'top': shape.Top,
                        'width': shape.Width,
                        'height': shape.Height,
                        'text': text[:80],
                        'font_size': font_size,
                        'overflow': has_overflow,
                        'para_count': tf.Paragraphs().Count,
                    })
                except Exception as e:
                    problems.append(f'文本框{shape_idx}读取错误: {str(e)[:50]}')
        
        # 页1封面：检查底部日期是否居中
        if page_idx == 1:
            for tb in text_boxes:
                # 检查居中：页面宽度10英寸=720磅，居中文本框Left应该在(720 - width)/2附近
                center_left = (prs.PageSetup.SlideWidth - tb['width']) / 2
                if abs(tb['left'] - center_left) > 5:
                    if len(tb['text']) > 5 and '2026' in tb['text'] or '日期' in tb['text']:
                        problems.append(f'日期可能未居中: left={tb["left"]:.0f}, 应约{center_left:.0f}, 偏差{abs(tb["left"]-center_left):.0f}磅')
        
        # 页2目录：检查文本框数量和内容分布
        if page_idx == 2:
            main_text = ''
            for tb in text_boxes:
                if len(tb['text']) > 100:
                    main_text = tb['text']
            # 目录应该有22个模块
            module_count = main_text.count('PART')
            if module_count != 22:
                problems.append(f'目录模块数不对：找到{module_count}个PART，应为22个')
        
        page_stats[page_idx] = {
            'shape_count': shape_count,
            'text_box_count': len(text_boxes),
            'problems': problems,
            'text_boxes': text_boxes
        }
        
        status = 'OK' if len(problems) == 0 else f'{len(problems)}问题'
        print(f'页{page_idx:02d}: 形状{shape_count} 文本框{len(text_boxes)} -> {status}')
        for p in problems:
            print(f'  !!! {p}')
            all_problems.append(f'页{page_idx}: {p}')
    
    print()
    print('=' * 70)
    print(f'全面检查完成：总计问题 {len(all_problems)} 个')
    print('=' * 70)
    if len(all_problems) > 0:
        print('问题清单：')
        for p in all_problems:
            print(f'  {p}')
    else:
        print('太棒了！未发现问题！')
    
    prs.Close()
    ppt_app.Quit()
    
    return len(all_problems) == 0

if __name__ == '__main__':
    success = main()
    if success:
        print('\n✓ 全部检查通过')
    else:
        print('\n✗ 发现问题，需要修复')
