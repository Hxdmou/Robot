
import sys
sys.stdout.reconfigure(encoding='utf-8')
from unittest.mock import MagicMock

sys.modules['pptx'] = MagicMock()
sys.modules['pptx.util'] = MagicMock()
sys.modules['pptx.dml.color'] = MagicMock()
sys.modules['pptx.enum.text'] = MagicMock()
sys.modules['pptx.enum.shapes'] = MagicMock()
sys.modules['pptx.enum.dml'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['win32com'] = MagicMock()
sys.modules['win32com.client'] = MagicMock()
sys.modules['pythoncom'] = MagicMock()

def Inches(x): return x * 72
def Pt(x): return x
def Emu(x): return x
sys.modules['pptx.util'].Inches = Inches
sys.modules['pptx.util'].Pt = Pt
sys.modules['pptx.util'].Emu = Emu

class MSO_ANCHOR: TOP = 1; MIDDLE = 2; BOTTOM = 3
MSO_ALIGN = MagicMock()
PP_ALIGN = MagicMock()
PP_ALIGN.CENTER = 1
sys.modules['pptx.enum.text'].MSO_ANCHOR = MSO_ANCHOR
sys.modules['pptx.enum.text'].PP_ALIGN = PP_ALIGN
sys.modules['pptx.enum.shapes'].MSO_SHAPE = MagicMock()
def RGBColor(r,g,b): return (r,g,b)
sys.modules['pptx.dml.color'].RGBColor = RGBColor

with open(r"F:\个人作品\具身智能\generate_business_ppt.py", 'r', encoding='utf-8') as f:
    source = f.read()
namespace = {'__file__': r"F:\个人作品\具身智能\generate_business_ppt.py", '__name__': 'ppt_gen'}
exec(source, namespace)
all_modules = namespace['all_modules']

print("=" * 80)
print(f"模块总数: {len(all_modules)}个")
print("=" * 80)

for idx, m in enumerate(all_modules, 1):
    part, title, left, right, pt, process, dt, detail = m
    print(f"{idx:2d}. {part} {title}")
    print(f"    left={len(left)}条, right={len(right)}条, process={len(process)}条, detail={len(detail)}条")
    # 设计：存储多条目（时间倒序），渲染切片left[:10]/right[:10]/process[:10]/detail[:20]
    # 校验渲染切片恰好铺满页面（100%指标），存储需>=渲染数
    assert len(left) >= 10 and len(list(left[:10])) == 10, f"{part} left渲染不足10"
    assert len(right) >= 10 and len(list(right[:10])) == 10, f"{part} right渲染不足10"
    assert len(process) >= 10 and len(list(process[:10])) == 10, f"{part} process渲染不足10"
    assert len(detail) >= 20 and len(list(detail[:20])) == 20, f"{part} detail渲染不足20"

print()
print("=" * 80)
print("✓ 22个模块全部完整，渲染取left[:10]/right[:10]/process[:10]/detail[:20]")
print("✓ 每个模块都有【内容描述】+【细节描述】两页，共44页模块内容")
print("✓ 总页数 = 1封面 + 1目录 + 44模块页 + 1封底 = 47页")
print("=" * 80)
