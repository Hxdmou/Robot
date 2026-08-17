
# ========== 第一步：直接解析Python文件检查所有模块条目数 ==========
import re
import ast

print("=" * 80)
print("【第一步】源代码模块条目数严格检查")
print("=" * 80)

with open(r"F:\个人作品\具身智能\generate_business_ppt.py", 'r', encoding='utf-8') as f:
    source = f.read()

# 找到modules列表定义
# 简单方法：执行代码但屏蔽pptx
import sys
from unittest.mock import MagicMock

# Mock所有pptx相关模块
sys.modules['pptx'] = MagicMock()
sys.modules['pptx.util'] = MagicMock()
sys.modules['pptx.dml.color'] = MagicMock()
sys.modules['pptx.enum.text'] = MagicMock()
sys.modules['pptx.enum.shapes'] = MagicMock()
sys.modules['pptx.enum.dml'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['win32com'] = MagicMock()
sys.modules['win32com.client'] = MagicMock()
sys.modules['pythoncom'] = MagicMock()

# Inches和Pt需要返回数值
def Inches(x): return x * 72
def Pt(x): return x
def Emu(x): return x
sys.modules['pptx.util'].Inches = Inches
sys.modules['pptx.util'].Pt = Pt
sys.modules['pptx.util'].Emu = Emu

# MSO_ANCHOR mock
class MSO_ANCHOR:
    TOP = 1
    MIDDLE = 2
    BOTTOM = 3
MSO_ALIGN = MagicMock()
sys.modules['pptx.enum.text'].MSO_ANCHOR = MSO_ANCHOR
sys.modules['pptx.enum.text'].PP_ALIGN = MSO_ALIGN
sys.modules['pptx.enum.shapes'].MSO_SHAPE = MagicMock()

# RGBColor
def RGBColor(r,g,b): return (r,g,b)
sys.modules['pptx.dml.color'].RGBColor = RGBColor

# 执行文件
namespace = {}
exec(source, namespace)
modules = namespace['all_modules']

error_count = 0
print(f"共找到 {len(modules)} 个模块\n")

for idx, m in enumerate(modules, start=1):
    part, title, left_list, right_list, process_title, process_list, detail_title, detail_list = m
    left_n = len(left_list)
    right_n = len(right_list)
    process_n = len(process_list)
    detail_n = len(detail_list)
    
    ok = True
    problems = []
    
    if left_n != 10:
        problems.append(f"left={left_n}条(应10)")
        ok = False
    if right_n != 10:
        problems.append(f"right={right_n}条(应10)")
        ok = False
    if process_n != 10:
        problems.append(f"process={process_n}条(应10)")
        ok = False
    if detail_n != 20:
        problems.append(f"detail={detail_n}条(应20)")
        ok = False
    
    status = "✓ PASS" if ok else "✗ FAIL"
    print(f"模块{idx:2d} {part} {title[:18]:18s} left={left_n:2d} right={right_n:2d} process={process_n:2d} detail={detail_n:2d} {status}")
    
    if not ok:
        print(f"       问题: {', '.join(problems)}")
        error_count += 1

print()
if error_count == 0:
    print("✓ 所有模块条目数正确：left=10 right=10 process=10 detail=20")
else:
    print(f"✗ 发现 {error_count} 个模块条目数错误！")

# ========== 第二步：PowerPoint COM实际检查溢出 + 估算空隙 ==========
print()
print("=" * 80)
print("【第二步】PowerPoint COM 实际渲染检查（溢出+空隙）")
print("=" * 80)

import win32com.client
import os

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v25.pptx"

Application = win32com.client.Dispatch("PowerPoint.Application")
Application.Visible = True
Presentation = Application.Presentations.Open(ppt_path, ReadOnly=True)

overflow_total = 0
big_gap_total = 0

for slide_idx, slide in enumerate(Presentation.Slides, start=1):
    slide_overflow = 0
    slide_big_gap = 0
    gap_details = []
    
    for shape_idx, shape in enumerate(slide.Shapes, start=1):
        if shape.HasTextFrame:
            tf = shape.TextFrame
            try:
                # 检查溢出
                if tf.HasOverflowText:
                    slide_overflow += 1
                    overflow_total += 1
                
                # 计算空隙：文本框高度 - 文本实际边界高度
                shape_h = shape.Height  # 单位是磅
                try:
                    tr = tf.TextRange
                    # BoundTop/BoundLeft/BoundWidth/BoundHeight 是文本实际占据的尺寸
                    text_h = tr.BoundHeight
                    gap_pt = shape_h - text_h
                    # 如果空隙超过28pt（约0.39英寸），标记为明显空隙
                    if gap_pt > 28 and shape_h > 80:
                        slide_big_gap += 1
                        big_gap_total += 1
                        text_preview = tr.Text[:30].replace('\n', ' ').replace('\r', '')
                        gap_details.append(f"    形状{shape_idx}: 空隙={gap_pt:.1f}pt={gap_pt/72:.2f}in 预览:{text_preview}...")
                except Exception as e:
                    pass
            except:
                pass
    
    if slide_overflow > 0 or slide_big_gap > 0:
        print(f"第{slide_idx:2d}页: 溢出={slide_overflow} 明显空隙={slide_big_gap}")
        for d in gap_details:
            print(d)
    else:
        print(f"第{slide_idx:2d}页: ✓ 无溢出+空隙合理")

print()
print("=" * 80)
print("【最终总结】")
print(f"  源代码条目数错误: {error_count} 个")
print(f"  PPT实际溢出文本框: {overflow_total} 个")
print(f"  PPT明显空隙(>28pt≈0.4in): {big_gap_total} 处")
print("=" * 80)

if error_count == 0 and overflow_total == 0 and big_gap_total == 0:
    print("\n✓✓✓ 全部检查完美通过！没有任何问题！✓✓✓")
elif big_gap_total > 0 and overflow_total == 0 and error_count == 0:
    print(f"\n⚠ 无溢出且条目数正确，但有{big_gap_total}处空隙较大，需要调整段间距填满")
else:
    print("\n✗ 存在问题需要立即修复！")

Presentation.Close()
Application.Quit()
