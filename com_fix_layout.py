# -*- coding: utf-8 -*-
'''V3.24终极方案：单文件COM后校正
直接打开最终PPTX，以PowerPoint真实渲染BoundHeight为基准：
- 多段正文框：溢出→降段间距/保格式裁剪最长段；空隙→均匀加段间距填满（差<=3pt收敛）
- 单行文本框：强制垂直居中(VerticalAnchor=3)
对无水印版和水印版分别执行，就地保存'''
import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client
import time

FILES = [
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260817_商务汇报_无水印_v29.pptx",
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260817_商务汇报_水印版_v29.pptx",
]

def trim_paragraph(pr, chars):
    """用Characters API从段尾删除chars个字符，保留各run原有格式（金色标签不丢失）"""
    t = pr.Text
    core = t[:-1] if t.endswith('\r') else t
    L = len(core)
    if chars >= L - 42:
        chars = L - 42
    if chars <= 0:
        return 0
    # 优先在标点处断句
    cut = L - chars
    for k in range(min(L - 1, cut + 15), 40, -1):
        if core[k] in '，、；。：）%':
            cut = k + 1
            break
    remove = L - cut
    if remove <= 0:
        return 0
    pr.Characters(cut + 1, remove).Text = ''
    return remove

def fix_box(shape):
    """返回(动作描述列表)"""
    acts = []
    tf = shape.TextFrame
    # 关键：禁用AutoSize，形状高度固定，否则文本框自动膨胀破坏布局
    try:
        tf.AutoSize = 0  # ppAutoSizeNone
    except Exception:
        pass
    tr = tf.TextRange
    n = tr.Paragraphs().Count
    if n < 2:
        # 单行文本框：垂直居中
        try:
            tf.VerticalAnchor = 3  # msoAnchorMiddle
        except Exception:
            pass
        return acts
    H = shape.Height
    W = shape.Width
    chars_per_line = max(int(W / 10.6), 20)
    pf = tr.ParagraphFormat
    # 确定性法：BoundHeight读数有±5pt波动，读5次取最大值（保守），一次公式解
    pf.SpaceAfter = 0.0
    time.sleep(0.3)  # 等sa=0重排布完成，否则读到脏值
    B0 = max(tr.BoundHeight, tr.BoundHeight, tr.BoundHeight, tr.BoundHeight, tr.BoundHeight)
    # 真实溢出：保格式裁剪最长段直到B0<=H-1（与sa目标H对齐，避免裁剪框反溢出）
    guard = 0
    while B0 > H - 1 and guard < 60:
        guard += 1
        overflow_lines = (B0 - H + 1) / 11.0
        chars = int(overflow_lines * chars_per_line) + 8
        worst, wl = -1, 0
        for i in range(2, n + 1):
            L = len(tr.Paragraphs(i).Text)
            if L > wl:
                wl, worst = L, i
        if worst < 0 or wl <= 45:
            break
        removed = trim_paragraph(tr.Paragraphs(worst), chars)
        if removed <= 0:
            break
        acts.append('裁剪%d字' % removed)
        B0 = max(tr.BoundHeight, tr.BoundHeight)
    # 段间距一次解：末段sa=0（末段sa是底部不可见空白），sa只加在前n-1段
    # 目标：B0+(n-1)*sa = H（填满到框底，消除刻意2pt留白导致的空隙误报）
    if n > 1:
        sa = max(0.0, min((H - B0) / (n - 1), 40.0))
    else:
        sa = 0.0
    pf.SpaceAfter = sa
    tr.Paragraphs(n).ParagraphFormat.SpaceAfter = 0.0
    acts.append('sa=%.2f B0=%.1f' % (sa, B0))
    return acts

Application = win32com.client.DispatchEx("PowerPoint.Application")
Application.Visible = True
time.sleep(1)

for fp in FILES:
    print('=' * 70)
    print('校正:', fp.split('\\')[-1])
    Presentation = Application.Presentations.Open(fp, ReadOnly=False)
    time.sleep(2)
    trim_cnt = 0
    for si in range(1, Presentation.Slides.Count + 1):
        slide = Presentation.Slides(si)
        # 关键：激活幻灯片强制布局，否则BoundHeight读数不准（懒加载）
        try:
            slide.Select()
        except Exception:
            pass
        time.sleep(0.05)
        for shape in slide.Shapes:
            if not shape.HasTextFrame:
                continue
            try:
                tr = shape.TextFrame.TextRange
                if len(tr.Text.strip()) == 0:
                    continue
                acts = fix_box(shape)
                for a in acts:
                    if a.startswith('裁剪'):
                        trim_cnt += 1
            except Exception as e:
                print(f'  页{si} 异常 {e}')
    Presentation.Save()
    Presentation.Close()
    time.sleep(1)
    print(f'  完成，裁剪操作{trim_cnt}次')

Application.Quit()
print('双版本COM后校正全部完成！')
