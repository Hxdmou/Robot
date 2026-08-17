
import win32com.client.dynamic
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v27.pptx"
app = win32com.client.dynamic.Dispatch("PowerPoint.Application")
app.Visible = True
time.sleep(2)
pres = app.Presentations.Open(ppt_path, ReadOnly=True)
time.sleep(3)

print("=" * 100)
print("【v27真实内容文本框gap精确打印】(只显示文字>20字的内容框)")
print("=" * 100)

for slide_idx in range(1, pres.Slides.Count + 1):
    slide = pres.Slides(slide_idx)
    print(f"\n--- 第{slide_idx}页 ---")
    for shape_idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(shape_idx)
        try:
            if not shape.HasTextFrame:
                continue
        except:
            continue
        try:
            shape_h = shape.Height
        except:
            continue
        if shape_h <= 100:
            continue
        try:
            tf = shape.TextFrame
            tr = tf.TextRange
            text = tr.Text.replace('\r', '').replace('\n', '').strip()
            if len(text) < 20:
                continue
            text_h = tr.BoundHeight
            has_overflow = tf.HasOverflowText
            gap = shape_h - text_h
            preview = text[:50]
            status = "✓" if (gap >= 0 and gap <= 30 and not has_overflow) else ("⚠ 空隙" if gap > 30 else "✗ 溢出")
            print(f"  {status} 形状{shape_idx:2d}: shape={shape_h:6.1f}pt text={text_h:6.1f}pt gap={gap:7.1f}pt({gap/72:.2f}in) 文字{len(text):3d}字")
            print(f"         '{preview}...'")
        except Exception as e:
            print(f"  形状{shape_idx}: 错误 {e}")

pres.Close()
app.Quit()
