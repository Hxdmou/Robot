
import win32com.client.dynamic
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v26.pptx"
print("=" * 120)
print("【所有大文本框精确gap打印】(>10pt空隙都显示出来)")
print("=" * 120)

app = win32com.client.dynamic.Dispatch("PowerPoint.Application")
app.Visible = True
time.sleep(2)
pres = app.Presentations.Open(ppt_path, ReadOnly=True)
time.sleep(3)

gaps_all = []

for slide_idx in range(1, pres.Slides.Count + 1):
    slide = pres.Slides(slide_idx)
    print(f"\n--- 第{slide_idx}页 ---")
    for shape_idx in range(1, slide.Shapes.Count + 1):
        shape = slide.Shapes(shape_idx)
        if shape.HasTextFrame:
            try:
                shape_h = shape.Height
                if shape_h > 100:
                    tf = shape.TextFrame
                    try:
                        has_overflow = tf.HasOverflowText
                        tr = tf.TextRange
                        text_h = tr.BoundHeight
                        gap = shape_h - text_h
                        preview = tr.Text[:45].replace('\r', ' ').replace('\n', ' ')
                        gaps_all.append((slide_idx, shape_idx, shape_h, text_h, gap, has_overflow, preview))
                        status = "✓" if (gap >=0 and gap <= 15 and not has_overflow) else ("⚠ 空隙大" if gap > 15 else "✗ 溢出")
                        print(f"  形状{shape_idx:2d}: shape={shape_h:6.1f}pt text={text_h:6.1f}pt gap={gap:7.1f}pt ({gap/72:.2f}in) 溢出={has_overflow} {status}")
                        print(f"          '{preview}...'")
                    except Exception as e:
                        print(f"  形状{shape_idx}: 读取错误 {e}")
            except:
                pass

pres.Close()
app.Quit()

print()
print("=" * 120)
print("【问题汇总】")
overflow = [g for g in gaps_all if g[5]]
big_gap = [g for g in gaps_all if g[4] > 15]
small_gap = [g for g in gaps_all if 0 <= g[4] <= 15]
print(f"  溢出文本框: {len(overflow)}个")
print(f"  gap>15pt空隙: {len(big_gap)}处")
print(f"  0-15pt完美: {len(small_gap)}处")
if overflow:
    print("\n✗ 溢出的:")
    for s in overflow:
        print(f"  第{s[0]}页形状{s[1]}: gap={s[4]:.1f}pt '{s[6]}...'")
if big_gap:
    print("\n⚠ 空隙大的:")
    for s in big_gap:
        print(f"  第{s[0]}页形状{s[1]}: gap={s[4]:.1f}pt({s[4]/72:.2f}in) '{s[6]}...'")
print("=" * 120)
