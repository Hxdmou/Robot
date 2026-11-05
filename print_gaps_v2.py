
import win32com.client.dynamic
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v26.pptx"
print("=" * 120)
print("【所有大文本框精确gap打印】")
print("=" * 120)

app = win32com.client.dynamic.Dispatch("PowerPoint.Application")
app.Visible = True
time.sleep(2)
pres = app.Presentations.Open(ppt_path, ReadOnly=True)
time.sleep(3)

overflow_count = 0
big_gap_count = 0

for slide_idx in range(1, pres.Slides.Count + 1):
    slide = pres.Slides(slide_idx)
    print(f"\n--- 第{slide_idx}页 ---")
    for shape_idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(shape_idx)
        try:
            has_text_frame = shape.HasTextFrame
        except:
            has_text_frame = False
        if not has_text_frame:
            continue
        try:
            shape_h = shape.Height
        except:
            continue
        if shape_h <= 100:
            continue
        try:
            tf = shape.TextFrame
        except:
            continue
        has_overflow = False
        text_h = 0
        preview = ""
        try:
            has_overflow = tf.HasOverflowText
        except:
            has_overflow = False
        try:
            tr = tf.TextRange
            text_h = tr.BoundHeight
            preview = tr.Text[:50].replace('\r', ' ').replace('\n', ' ')
        except:
            pass
        gap = shape_h - text_h
        if has_overflow:
            overflow_count += 1
            print(f"  ✗ 形状{shape_idx:2d}: shape={shape_h:6.1f}pt text={text_h:6.1f}pt gap={gap:7.1f}pt 溢出!")
            print(f"         '{preview}...'")
        elif gap > 15:
            big_gap_count += 1
            print(f"  ⚠ 形状{shape_idx:2d}: shape={shape_h:6.1f}pt text={text_h:6.1f}pt gap={gap:7.1f}pt({gap/72:.2f}in) 空隙")
            print(f"         '{preview}...'")
        elif gap < -5:
            overflow_count += 1
            print(f"  ✗ 形状{shape_idx:2d}: shape={shape_h:6.1f}pt text={text_h:6.1f}pt gap={gap:7.1f}pt 负gap溢出!")
            print(f"         '{preview}...'")
        else:
            print(f"  ✓ 形状{shape_idx:2d}: shape={shape_h:6.1f}pt text={text_h:6.1f}pt gap={gap:7.1f}pt 完美")

pres.Close()
app.Quit()

print()
print("=" * 120)
print(f"【总结】溢出={overflow_count}, 空隙(>15pt)={big_gap_count}")
print("=" * 120)
