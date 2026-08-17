
# 统计完美模块（PART19真机部署）的每条字数作为基准
import sys
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
sys.modules['pptx.enum.text'].MSO_ANCHOR = MSO_ANCHOR
sys.modules['pptx.enum.text'].PP_ALIGN = MSO_ALIGN
sys.modules['pptx.enum.shapes'].MSO_SHAPE = MagicMock()
def RGBColor(r,g,b): return (r,g,b)
sys.modules['pptx.dml.color'].RGBColor = RGBColor

with open(r"F:\个人作品\具身智能\generate_business_ppt.py", 'r', encoding='utf-8') as f:
    source = f.read()
namespace = {}
exec(source, namespace)
all_modules = namespace['all_modules']

print("=" * 80)
print("【字数统计基准】PART19真机部署（detail完美gap=1.1pt）")
print("=" * 80)

# PART19是索引18（0-based）
part19 = all_modules[18]
part19_left = part19[2]
part19_right = part19[3]
part19_process = part19[5]
part19_detail = part19[7]

def count_chars(lst, name):
    print(f"\n--- {name} ({len(lst)}条) ---")
    lengths = []
    for i, s in enumerate(lst):
        # 去掉【】标签里的字算正文？不，全算
        l = len(s)
        lengths.append(l)
        print(f"  {i+1:2d}. {l:3d}字: {s[:50]}...")
    avg = sum(lengths)/len(lengths)
    print(f"  平均: {avg:.1f}字/条, 最短{min(lengths)}字, 最长{max(lengths)}字")
    return avg, min(lengths), max(lengths)

avg_detail, min_d, max_d = count_chars(part19_detail, "PART19 detail (完美gap=1pt)")
avg_left, min_l, max_l = count_chars(part19_left, "PART19 left")
avg_right, min_r, max_r = count_chars(part19_right, "PART19 right")
avg_process, min_p, max_p = count_chars(part19_process, "PART19 process")

print("\n" + "=" * 80)
print("【基准字数总结】")
print(f"  detail页(20条): 平均{avg_detail:.1f}字/条 (目标75-85字)")
print(f"  内容页left(10条): 平均{avg_left:.1f}字/条 (目标70-80字)")
print(f"  内容页right(10条): 平均{avg_right:.1f}字/条 (目标70-80字)")
print(f"  内容页process(10条): 平均{avg_process:.1f}字/条 (目标80-90字)")
print("=" * 80)

# 再统计所有模块当前字数
print("\n" + "=" * 80)
print("【所有模块当前字数】")
print("=" * 80)
for idx, m in enumerate(all_modules):
    part, title, left, right, pt, process, dt, detail = m
    avg_l = sum(len(s) for s in left)/10
    avg_r = sum(len(s) for s in right)/10
    avg_p = sum(len(s) for s in process)/10
    avg_d = sum(len(s) for s in detail)/20
    print(f"{part} {title[:20]:20s} L:{avg_l:.0f} R:{avg_r:.0f} P:{avg_p:.0f} D:{avg_d:.0f}")
