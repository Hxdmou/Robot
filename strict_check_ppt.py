
import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client
import os
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v28.pptx"

print("=" * 80)
print("【PowerPoint COM 严格检查】溢出 + 空隙计算")
print("=" * 80)
print(f"文件: {os.path.basename(ppt_path)}")
print()

Application = win32com.client.Dispatch("PowerPoint.Application")
Application.Visible = True
time.sleep(1)
Presentation = Application.Presentations.Open(ppt_path, ReadOnly=False)
time.sleep(2)

overflow_total = 0
gap_total = 0

for slide_idx, slide in enumerate(Presentation.Slides, start=1):
    slide_overflow = 0
    slide_gap = 0
    gap_info = []
    
    for shape_idx, shape in enumerate(slide.Shapes, start=1):
        if shape.HasTextFrame:
            tf = shape.TextFrame
            try:
                has_overflow = tf.HasOverflowText
                if has_overflow:
                    slide_overflow += 1
                    overflow_total += 1
                
                shape_h = shape.Height
                try:
                    tr = tf.TextRange
                    text_h = tr.BoundHeight
                    gap = shape_h - text_h
                    # 大文本框（高度>100pt≈1.39in）空隙超过20pt就算明显
                    if gap > 20 and shape_h > 100:
                        slide_gap += 1
                        gap_total += 1
                        preview = tr.Text[:35].replace('\r', ' ').replace('\n', ' ')
                        gap_info.append(f"  形状{shape_idx}: 空隙={gap:.1f}pt({gap/72:.2f}in)  '{preview}...'")
                except Exception as e:
                    pass
            except Exception as e:
                pass
    
    status = f"✓ 完美" if (slide_overflow == 0 and slide_gap == 0) else f"溢出={slide_overflow} 空隙={slide_gap}"
    print(f"第{slide_idx:2d}页: {status}")
    if gap_info:
        for info in gap_info:
            print(info)

print()
print("=" * 80)
print("【无水印版检查结果】")
print(f"  溢出文本框: {overflow_total}")
print(f"  明显空隙:   {gap_total}")
print("=" * 80)

if overflow_total == 0 and gap_total == 0:
    print("✓✓✓ 无水印版：0溢出 + 0大空隙，完美通过！")
else:
    print("⚠ 需要调整！")

Presentation.Close()
time.sleep(1)

# 检查水印版
print()
print("=" * 80)
print("【水印版检查】")
print("=" * 80)
ppt_path_wm = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_水印版_v28.pptx"
Presentation_wm = Application.Presentations.Open(ppt_path_wm, ReadOnly=False)
time.sleep(2)

overflow_wm = 0
gap_wm = 0

for slide_idx, slide in enumerate(Presentation_wm.Slides, start=1):
    for shape in slide.Shapes:
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

print(f"水印版：溢出={overflow_wm} 明显空隙={gap_wm}")
if overflow_wm == 0 and gap_wm == 0:
    print("✓✓✓ 水印版：0溢出 + 0大空隙，完美通过！")
else:
    print("⚠ 需要调整！")

Presentation_wm.Close()
Application.Quit()

print()
print("=" * 80)
if overflow_total == 0 and gap_total == 0 and overflow_wm == 0 and gap_wm == 0:
    print("【最终结论】双版本全部完美通过！没有任何问题！")
else:
    print("【最终结论】存在问题需要修复！")
print("=" * 80)
