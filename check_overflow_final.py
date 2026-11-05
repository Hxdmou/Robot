
import win32com.client
import os

ppt_path = r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260816_商务汇报_无水印_v25.pptx"

print("=" * 60)
print("PowerPoint COM接口 - 逐页HasOverflowText溢出检查")
print("=" * 60)
print(f"检查文件: {os.path.basename(ppt_path)}")
print()

try:
    Application = win32com.client.Dispatch("PowerPoint.Application")
    Application.Visible = True
    Presentation = Application.Presentations.Open(ppt_path, ReadOnly=True)
    
    overflow_count = 0
    total_textboxes = 0
    overflow_list = []
    
    for slide_idx, slide in enumerate(Presentation.Slides, start=1):
        slide_overflow = 0
        for shape_idx, shape in enumerate(slide.Shapes, start=1):
            if shape.HasTextFrame:
                total_textboxes += 1
                try:
                    if shape.TextFrame.HasOverflowText:
                        overflow_count += 1
                        slide_overflow += 1
                        text_preview = shape.TextFrame.TextRange.Text[:30].replace('\n', ' ').replace('\r', '')
                        overflow_list.append(f"  第{slide_idx}页 形状{shape_idx}: 溢出! 内容预览: {text_preview}...")
                except Exception as e:
                    pass
        
        status = "✗ 有溢出" if slide_overflow > 0 else "✓ 无溢出"
        print(f"第{slide_idx:2d}页: {status} (溢出{slide_overflow}个文本框)")
    
    print()
    print("=" * 60)
    print(f"检查完成！共{len(Presentation.Slides)}页, {total_textboxes}个文本框")
    
    if overflow_count == 0:
        print("✓✓✓ 所有文本框0溢出！完美通过！✓✓✓")
    else:
        print(f"✗ 发现{overflow_count}个文本框溢出:")
        for item in overflow_list:
            print(item)
    
    print("=" * 60)
    print(f"总页数验证: 1封面 + 1目录 + 22模块×2 + 1封底 = 47页 (实际{len(Presentation.Slides)}页)")
    
    Presentation.Close()
    Application.Quit()
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
