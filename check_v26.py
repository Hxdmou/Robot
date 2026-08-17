
import win32com.client.dynamic
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v26.pptx"
print("=" * 100)
print("【v26逐文本框gap检查】")
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
    details = []
    
    for shape_idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(shape_idx)
        if shape.HasTextFrame:
            tf = shape.TextFrame
            try:
                shape_h = shape.Height
                if shape_h > 100:  # 只看大文本框
                    try:
                        has_overflow = tf.HasOverflowText
                        tr = tf.TextRange
                        text_h = tr.BoundHeight
                        gap = shape_h - text_h
                        preview = tr.Text[:35].replace('\r', ' ').replace('\n', ' ')
                        if has_overflow:
                            slide_overflow += 1
                            overflow_count += 1
                            details.append(f"  ✗ 溢出! 形状{shape_idx}: gap={gap:.1f}pt '{preview}...'")
                        elif gap > 50:
                            slide_biggap += 1
                            big_gap_count += 1
                            details.append(f"  ⚠ 空隙大: 形状{shape_idx}: gap={gap:.1f}pt({gap/72:.2f}in) '{preview}...'")
                    except:
                        pass
            except:
                pass
    
    if slide_overflow > 0 or slide_biggap > 0:
        print(f"\n第{slide_idx}页: 溢出={slide_overflow} 大空隙={slide_biggap}")
        for d in details:
            print(d)
    else:
        print(f"第{slide_idx:2d}页: ✓ 完美 (0溢出+0大空隙)")

pres.Close()
app.Quit()

print()
print("=" * 100)
print(f"【总结】总溢出={overflow_count}, 大空隙(>50pt)={big_gap_count}")
if overflow_count == 0 and big_gap_count == 0:
    print("✓✓✓ 全部完美通过！")
print("=" * 100)
