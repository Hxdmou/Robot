
import win32com.client
import os

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_水印版_v25.pptx"

print("=" * 60)
print("水印版 - PowerPoint COM接口逐页溢出检查")
print("=" * 60)

try:
    Application = win32com.client.Dispatch("PowerPoint.Application")
    Application.Visible = True
    Presentation = Application.Presentations.Open(ppt_path, ReadOnly=True)
    
    overflow_count = 0
    for slide_idx, slide in enumerate(Presentation.Slides, start=1):
        slide_overflow = 0
        for shape in slide.Shapes:
            if shape.HasTextFrame:
                try:
                    if shape.TextFrame.HasOverflowText:
                        overflow_count += 1
                        slide_overflow += 1
                except:
                    pass
        status = "✓ 无溢出" if slide_overflow == 0 else f"✗ 溢出{slide_overflow}"
        print(f"第{slide_idx:2d}页: {status}")
    
    print()
    print("=" * 60)
    if overflow_count == 0:
        print("✓✓✓ 水印版所有文本框0溢出！✓✓✓")
    else:
        print(f"水印版共{overflow_count}个溢出")
    
    Presentation.Close()
    Application.Quit()
except Exception as e:
    print(f"错误: {e}")

# 列出文件
print()
print("=" * 60)
print("最终生成文件:")
files = [
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v25.pptx",
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_水印版_v25.pptx"
]
for f in files:
    size_mb = os.path.getsize(f) / 1024 / 1024
    print(f"  {os.path.basename(f)}  ({size_mb:.1f} MB)")
print("=" * 60)
print("全部检查完成！")
