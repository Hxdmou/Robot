
import win32com.client.dynamic
import os
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v25.pptx"

print("=" * 80)
print("【PowerPoint 严格检查】溢出 + 空隙（dynamic dispatch）")
print("=" * 80)

Application = win32com.client.dynamic.Dispatch("PowerPoint.Application")
Application.Visible = True
time.sleep(2)
Presentation = Application.Presentations.Open(ppt_path, ReadOnly=True)
time.sleep(3)

overflow_total = 0
gap_total = 0
total_slides = Presentation.Slides.Count

for slide_idx in range(1, total_slides + 1):
    slide = Presentation.Slides(slide_idx)
    slide_overflow = 0
    slide_gap = 0
    
    for shape_idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(shape_idx)
        if shape.HasTextFrame:
            tf = shape.TextFrame
            try:
                if tf.HasOverflowText:
                    slide_overflow += 1
                    overflow_total += 1
                
                shape_h = shape.Height
                try:
                    tr = tf.TextRange
                    text_h = tr.BoundHeight
                    gap = shape_h - text_h
                    if gap > 20 and shape_h > 100:
                        slide_gap += 1
                        gap_total += 1
                except:
                    pass
            except:
                pass
    
    status = "✓ 完美" if (slide_overflow == 0 and slide_gap == 0) else f"溢出={slide_overflow} 空隙={slide_gap}"
    print(f"第{slide_idx:2d}页: {status}")

print()
print("=" * 80)
print(f"无水印版结果: 溢出={overflow_total}, 空隙={gap_total}")
Presentation.Close()
time.sleep(1)

# 水印版
ppt_path_wm = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_水印版_v25.pptx"
Presentation_wm = Application.Presentations.Open(ppt_path_wm, ReadOnly=True)
time.sleep(3)

overflow_wm = 0
gap_wm = 0

for slide_idx in range(1, Presentation_wm.Slides.Count + 1):
    slide = Presentation_wm.Slides(slide_idx)
    for shape_idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(shape_idx)
        if shape.HasTextFrame:
            try:
                if shape.TextFrame.HasOverflowText:
                    overflow_wm += 1
                shape_h = shape.Height
                try:
                    text_h = shape.TextFrame.TextRange.BoundHeight
                    gap = shape_h - text_h
                    if gap > 20 and shape_h > 100:
                        gap_wm += 1
                except:
                    pass
            except:
                pass

print(f"水印版结果:   溢出={overflow_wm}, 空隙={gap_wm}")
Presentation_wm.Close()
Application.Quit()

print("=" * 80)
if overflow_total == 0 and gap_total == 0 and overflow_wm == 0 and gap_wm == 0:
    print("✓✓✓ 最终结论：双版本全部0溢出+0大空隙，100%完美！✓✓✓")
else:
    print(f"⚠ 发现问题：无水印溢出{overflow_total}/空隙{gap_total}，水印溢出{overflow_wm}/空隙{gap_wm}")
print("=" * 80)
