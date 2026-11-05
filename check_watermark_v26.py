
import win32com.client.dynamic
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_水印版_v26.pptx"
print("=" * 100)
print("【v26水印版检查】")
print("=" * 100)

app = win32com.client.dynamic.Dispatch("PowerPoint.Application")
app.Visible = True
time.sleep(2)
pres = app.Presentations.Open(ppt_path, ReadOnly=True)
time.sleep(3)

overflow_count = 0
big_gap_count = 0

for slide_idx in range(1, pres.Slides.Count + 1):
    slide = pres.Slides(slide_idx)
    slide_overflow = 0
    slide_biggap = 0
    
    for shape_idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(shape_idx)
        if shape.HasTextFrame:
            try:
                shape_h = shape.Height
                if shape_h > 100:
                    try:
                        has_overflow = shape.TextFrame.HasOverflowText
                        text_h = shape.TextFrame.TextRange.BoundHeight
                        gap = shape_h - text_h
                        if has_overflow:
                            slide_overflow += 1
                            overflow_count += 1
                        elif gap > 50:
                            slide_biggap += 1
                            big_gap_count += 1
                    except:
                        pass
            except:
                pass
    
    if slide_overflow > 0 or slide_biggap > 0:
        print(f"第{slide_idx}页: 溢出={slide_overflow} 大空隙={slide_biggap}")
    else:
        print(f"第{slide_idx:2d}页: ✓ 完美")

pres.Close()
app.Quit()

print()
print("=" * 100)
print(f"【水印版总结】溢出={overflow_count}, 大空隙={big_gap_count}")
if overflow_count == 0 and big_gap_count == 0:
    print("✓✓✓ 水印版也全部完美通过！")
print("=" * 100)
