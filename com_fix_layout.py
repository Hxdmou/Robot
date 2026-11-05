# -*- coding: utf-8 -*-
'''V3.25安全校准：懒加载防护 + 迭代收敛
- 读数防护：有效读数须满足 40<=B<=H*2，否则重试，仍异常则跳过该形状（绝不写入脏值）
- 溢出：sa=0下裁剪最长段直到 B0<=H-2
- 空隙：迭代收敛段间距sa，目标 B=H-1（留1pt安全边距），容差±2pt
对无水印版和水印版分别执行，就地保存'''
import sys
sys.stdout.reconfigure(encoding='utf-8')
import win32com.client
import time

FILES = [
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260817_商务汇报_无水印_v29.pptx",
    r"F:\个人作品\具身智能\具身智能AI产业最新进展_20260817_商务汇报_水印版_v29.pptx",
]

def read_bound(tr, H, rounds=3):
    """懒加载防护读取BoundHeight：每轮读5次取有效读数最大值（保守防溢出），
    有效读数须满足 40<=B<=H*2，全部异常则重试，仍异常返回None（调用方跳过该形状）"""
    for _ in range(rounds):
        vals = []
        for _ in range(5):
            try:
                b = tr.BoundHeight
            except Exception:
                b = -1
            if 40 <= b <= H * 2:
                vals.append(b)
            time.sleep(0.08)
        if len(vals) >= 3:
            return max(vals)
        time.sleep(0.5)
    return None

def trim_paragraph(pr, chars):
    """用Characters API从段尾删除chars个字符，保留各run原有格式（金色标签不丢失）"""
    t = pr.Text
    core = t[:-1] if t.endswith('\r') else t
    L = len(core)
    if chars >= L - 42:
        chars = L - 42
    if chars <= 0:
        return 0
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

def apply_sa(tr, n, sa):
    pf = tr.ParagraphFormat
    pf.SpaceAfter = sa
    tr.Paragraphs(n).ParagraphFormat.SpaceAfter = 0.0

def fix_box(shape):
    acts = []
    tf = shape.TextFrame
    try:
        tf.AutoSize = 0  # ppAutoSizeNone 固定形状高度
    except Exception:
        pass
    tr = tf.TextRange
    n = tr.Paragraphs().Count
    if n < 2:
        try:
            tf.VerticalAnchor = 3  # 单行文本框垂直居中
        except Exception:
            pass
        return acts
    H = shape.Height
    W = shape.Width
    chars_per_line = max(int(W / 10.6), 20)
    pf = tr.ParagraphFormat
    # 第一步：sa=0测自然高度
    pf.SpaceAfter = 0.0
    time.sleep(0.3)
    B0 = read_bound(tr, H)
    if B0 is None:
        acts.append('跳过:读数异常')
        return acts
    # 第二步：真实溢出则保格式裁剪最长段，直到B0<=H-2
    guard = 0
    while B0 > H - 2 and guard < 60:
        guard += 1
        overflow_lines = (B0 - H + 2) / 11.0
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
        time.sleep(0.2)
        nb = read_bound(tr, H)
        if nb is None:
            acts.append('跳过:裁剪后读数异常')
            return acts
        B0 = nb
    # 第三步：迭代收敛段间距，目标B=H-1（容差±2pt）
    sa = max(0.0, min((H - 1 - B0) / (n - 1), 40.0))
    apply_sa(tr, n, sa)
    for _ in range(4):
        time.sleep(0.25)
        B = read_bound(tr, H)
        if B is None:
            break
        diff = (H - 1) - B
        if abs(diff) <= 2.0:
            break
        sa = max(0.0, min(sa + diff / (n - 1), 40.0))
        apply_sa(tr, n, sa)
    acts.append('sa=%.2f' % sa)
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
    skip_cnt = 0
    for si in range(1, Presentation.Slides.Count + 1):
        slide = Presentation.Slides(si)
        try:
            slide.Select()  # 激活幻灯片强制布局
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
                    elif a.startswith('跳过'):
                        skip_cnt += 1
            except Exception as e:
                print(f'  页{si} 异常 {e}')
    Presentation.Save()
    Presentation.Close()
    time.sleep(1)
    print(f'  完成，裁剪{trim_cnt}次，跳过异常形状{skip_cnt}个')

Application.Quit()
print('双版本COM校准全部完成！')
