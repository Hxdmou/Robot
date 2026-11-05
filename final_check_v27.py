
import win32com.client.dynamic
import time

def check_ppt(ppt_path, label):
    print("=" * 100)
    print(f"【{label}检查】")
    print("=" * 100)
    app = win32com.client.dynamic.Dispatch("PowerPoint.Application")
    app.Visible = True
    time.sleep(2)
    pres = app.Presentations.Open(ppt_path, ReadOnly=True)
    time.sleep(3)
    
    overflow = 0
    bad_gap = 0
    perfect = 0
    total_content_boxes = 0
    
    for slide_idx in range(1, pres.Slides.Count + 1):
        slide = pres.Slides(slide_idx)
        slide_problems = []
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
                text = tr.Text
                text = text.replace('\r', '').replace('\n', '').strip()
                # 跳过空的背景框
                if len(text) < 10:
                    continue
                total_content_boxes += 1
                text_h = tr.BoundHeight
                has_overflow = tf.HasOverflowText
                gap = shape_h - text_h
                preview = text[:40]
                if has_overflow or gap < -5:
                    overflow += 1
                    slide_problems.append(f"  ✗ 溢出 形状{shape_idx} gap={gap:.1f}pt '{preview}...'")
                elif gap > 20:
                    bad_gap += 1
                    slide_problems.append(f"  ⚠ 空隙 形状{shape_idx} gap={gap:.1f}pt({gap/72:.2f}in) '{preview}...'")
                else:
                    perfect += 1
            except Exception as e:
                pass
        if slide_problems:
            print(f"\n第{slide_idx}页:")
            for p in slide_problems:
                print(p)
        else:
            print(f"第{slide_idx:2d}页: ✓ 完美")
    
    pres.Close()
    app.Quit()
    
    print()
    print("=" * 100)
    print(f"【{label}总结】总内容文本框={total_content_boxes}, 溢出={overflow}, 空隙>20pt={bad_gap}, 完美={perfect}")
    if overflow == 0 and bad_gap == 0:
        print("✓✓✓ 全部完美通过！")
    print("=" * 100)
    return overflow, bad_gap

o1, g1 = check_ppt(r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v27.pptx", "无水印版v27")
print()
o2, g2 = check_ppt(r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_水印版_v27.pptx", "水印版v27")
print()
print("=" * 100)
if o1 == 0 and g1 == 0 and o2 == 0 and g2 == 0:
    print("【最终结论】双版本全部完美！0溢出 + 0大空隙！")
print("=" * 100)
