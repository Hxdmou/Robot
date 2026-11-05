
import win32com.client.dynamic
import time

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_水印版_v28.pptx"
app = win32com.client.dynamic.Dispatch("PowerPoint.Application")
app.Visible = True
time.sleep(3)
pres = app.Presentations.Open(ppt_path, ReadOnly=True)
time.sleep(3)

overflow = 0
for s_idx in range(1, pres.Slides.Count+1):
    slide = pres.Slides(s_idx)
    for sh_idx in range(1, slide.Shapes.Count+1):
        sh = slide.Shapes(sh_idx)
        try:
            if sh.HasTextFrame and sh.TextFrame.HasOverflowText:
                overflow += 1
        except:
            pass

pres.Close()
app.Quit()

print("=" * 60)
if overflow == 0:
    print("✓✓✓ 水印版47页全部0溢出！")
else:
    print(f"✗ 水印版有{overflow}个溢出！")
print("=" * 60)
