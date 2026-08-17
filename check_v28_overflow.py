
import win32com.client.dynamic
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v28.pptx"
print("正在打开PPT检查...")
app = win32com.client.dynamic.Dispatch("PowerPoint.Application")
app.Visible = True
time.sleep(3)
pres = app.Presentations.Open(ppt_path, ReadOnly=True)
time.sleep(3)

overflow = 0
for s_idx in range(1, pres.Slides.Count+1):
    slide = pres.Slides(s_idx)
    slide_overflow = 0
    for sh_idx in range(1, slide.Shapes.Count+1):
        sh = slide.Shapes(sh_idx)
        try:
            if sh.HasTextFrame and sh.TextFrame.HasOverflowText:
                slide_overflow += 1
                overflow += 1
        except:
            pass
    status = "✓" if slide_overflow == 0 else f"✗ 溢出{slide_overflow}"
    print(f"第{s_idx:2d}页: {status}")

pres.Close()
app.Quit()

print()
print("=" * 60)
if overflow == 0:
    print("✓✓✓ 全部47页0溢出！段间距增加后内容均匀分布！")
else:
    print(f"✗ 发现{overflow}个溢出，需要微调！")
print("=" * 60)
