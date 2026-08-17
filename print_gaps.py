
import win32com.client.dynamic
import os
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v25.pptx"

print("=" * 100)
print("【逐文本框精确空隙数据】shape_h(文本框高度pt), text_h(文本实际高度pt), gap(空隙pt)")
print("=" * 100)

Application = win32com.client.dynamic.Dispatch("PowerPoint.Application")
Application.Visible = True
time.sleep(2)
Presentation = Application.Presentations.Open(ppt_path, ReadOnly=True)
time.sleep(3)

for slide_idx in range(1, Presentation.Slides.Count + 1):
    slide = Presentation.Slides(slide_idx)
    print(f"\n=== 第{slide_idx}页 ===")
    for shape_idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(shape_idx)
        if shape.HasTextFrame:
            tf = shape.TextFrame
            try:
                shape_h = shape.Height
                if shape_h > 100:  # 只看大文本框
                    tr = tf.TextRange
                    text_h = tr.BoundHeight
                    gap = shape_h - text_h
                    preview = tr.Text[:40].replace('\r', ' ').replace('\n', ' ')
                    status = "✓ 好" if gap < 15 else ("⚠ 空隙大" if gap < 40 else "✗ 空隙很大")
                    print(f"  形状{shape_idx:2d}: shape_h={shape_h:6.1f}pt text_h={text_h:6.1f}pt gap={gap:6.1f}pt ({gap/72:.2f}in) {status}")
                    print(f"           内容: {preview}...")
            except Exception as e:
                pass

Presentation.Close()
Application.Quit()
print("\n" + "=" * 100)
