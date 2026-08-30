# -*- coding: utf-8 -*-
'''
A2A PPT V52：按具身智能标准流程重做（填满无空隙）
- 8项目×4页：内容(1)(2)+细节(3)(4)，每维36条长条目池，_resolve自动裁剪填满+整数段距
- 标题格式：项目N: XXX（2026-2035·2031起只作为参考依据）(1)/(2)/(3)/(4)
'''
import sys
sys.stdout.reconfigure(encoding='utf-8')
import os, json
print('V52脚本启动', flush=True)

TPL = r'F:\个人作品\具身智能\generate_business_ppt.py'
src = open(TPL, encoding='utf-8').read()
cut = src.index('def generate(')
src = src[:cut]
g = {'__file__': TPL, '__name__': 'a2a_tpl'}
exec(src, g)

g['FOOTER_TEXT'] = 'A2A协议与AI智能体生态 · 2026年8月29日 · 内部资料 仅供参考'
_saved_name = __name__
globals().update(g)
__name__ = _saved_name

OUT_DIR = r'F:\个人作品\具身智能'
sys.path.insert(0, OUT_DIR)
from _a2a_v52_data1 import M1_CONTENT, M1_DETAIL, M2_CONTENT, M2_DETAIL, M3_CONTENT, M3_DETAIL, M4_CONTENT, M4_DETAIL
from _a2a_v52_data2 import M5_CONTENT, M5_DETAIL, M6_CONTENT, M6_DETAIL, M7_CONTENT, M7_DETAIL, M8_CONTENT, M8_DETAIL

TEXT_JSON = os.path.join(OUT_DIR, '_tmp_a2a_textpages.json')
if not os.path.exists(TEXT_JSON):
    print('缺少textpages json，先提取')
    import win32com.client
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    prs0 = app.Presentations.Open(os.path.join(OUT_DIR, 'A2A协议2.0_AI智能体演进路线图_2026_V50_无水印版.pptx'), ReadOnly=True)
    data = {}
    for i in range(10, 15):
        slide = prs0.Slides(i)
        shapes = []
        for j in range(1, slide.Shapes.Count + 1):
            sh = slide.Shapes(j)
            if sh.HasTextFrame and sh.TextFrame.HasText and sh.TextFrame.TextRange.Text.strip():
                shapes.append({'top': sh.Top, 'left': sh.Left, 'width': sh.Width, 'height': sh.Height,
                               'text': sh.TextFrame.TextRange.Text,
                               'size': sh.TextFrame.TextRange.Font.Size if sh.TextFrame.TextRange.Font.Size else 10})
        data[str(i)] = shapes
    prs0.Close()
    app.Quit()
    with open(TEXT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

MODULES = [
    ('项目1', '项目1: A2A协议核心架构演进（2026-2035·2031起只作为参考依据）', M1_CONTENT, M1_DETAIL),
    ('项目2', '项目2: 价值维度评估体系（2026-2035·2031起只作为参考依据）', M2_CONTENT, M2_DETAIL),
    ('项目3', '项目3: 安全组件体系（2026-2035·2031起只作为参考依据）', M3_CONTENT, M3_DETAIL),
    ('项目4', '项目4: 部署策略规划（2026-2035·2031起只作为参考依据）', M4_CONTENT, M4_DETAIL),
    ('项目5', '项目5: AI创造能力演进（2026-2035·2031起只作为参考依据）', M5_CONTENT, M5_DETAIL),
    ('项目6', '项目6: 性能指标体系（2026-2035·2031起只作为参考依据）', M6_CONTENT, M6_DETAIL),
    ('项目7', '项目7: 生态系统建设（2026-2035·2031起只作为参考依据）', M7_CONTENT, M7_DETAIL),
    ('项目8', '项目8: 技术方案对比（2026-2035·2031起只作为参考依据）', M8_CONTENT, M8_DETAIL),
]

def a2a_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, DARK_BLUE)
    tb(slide, 0.5, 2.1, 12.33, 1.0, '【A2A协议与AI智能体生态】PPT完整升级内容', sz=32, b=True, c=ACCENT_BLUE, al=PP_ALIGN.CENTER, an=MSO_ANCHOR.MIDDLE)
    tb(slide, 0.5, 3.2, 12.33, 0.4, '版本：V52.0 | 更新日期：2026年8月29日 | 基于2026年最新AI技术演进', sz=12, c=LGRAY, al=PP_ALIGN.CENTER)
    tb(slide, 2, 4.0, 9.33, 0.1, '═' * 60, sz=8, c=ACCENT_BLUE, al=PP_ALIGN.CENTER)
    tb(slide, 0.5, 4.4, 12.33, 0.8, '© 2026 A2A协议联盟 | 版权所有', sz=10, c=MGRAY, al=PP_ALIGN.CENTER)
    tb(slide, 0, FOOTER_Y, SLIDE_W, SLIDE_H - FOOTER_Y, FOOTER_TEXT, sz=7, c=MGRAY, al=PP_ALIGN.CENTER, an=MSO_ANCHOR.MIDDLE)

def a2a_toc(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, DARK_BLUE)
    tb(slide, 0, 0.3, SLIDE_W, 0.6, '【目录】8大项目 · 每项目4页（内容2页+细节2页）', sz=22, b=True, c=GOLD, al=PP_ALIGN.CENTER)
    y = 1.2
    for m in MODULES:
        tb(slide, 1.5, y, 10.33, 0.45, m[1], sz=13, c=WHITE, al=PP_ALIGN.CENTER)
        y += 0.62
    tb(slide, 0, FOOTER_Y, SLIDE_W, SLIDE_H - FOOTER_Y, FOOTER_TEXT, sz=7, c=MGRAY, al=PP_ALIGN.CENTER, an=MSO_ANCHOR.MIDDLE)

def a2a_back(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, DARK_BLUE)
    tb(slide, 0.5, 2.6, 12.33, 0.8, '感谢观看', sz=36, b=True, c=ACCENT_BLUE, al=PP_ALIGN.CENTER)
    tb(slide, 0.5, 3.6, 12.33, 0.4, 'A2A协议与AI智能体生态 · 2026年8月29日', sz=12, c=LGRAY, al=PP_ALIGN.CENTER)
    tb(slide, 0, FOOTER_Y, SLIDE_W, SLIDE_H - FOOTER_Y, FOOTER_TEXT, sz=7, c=MGRAY, al=PP_ALIGN.CENTER, an=MSO_ANCHOR.MIDDLE)

def render_text_page(prs, part_num, title, shapes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, DARK_BLUE)
    add_page_header(slide, part_num, title)
    for sh in shapes:
        if sh['top'] < 30:
            continue
        x = sh['left'] / 72.0
        y = sh['top'] / 72.0
        w = sh['width'] / 72.0
        sz = int(sh['size']) if sh['size'] else 10
        text = sh['text'].replace('\x0b', '\n')
        lines = text.split('\n')
        n = len(lines)
        # 填满无空隙铁律：整数段距分配，把内容铺到底部钳制线（CONTENT_BOTTOM-0.12）
        top_pt = sh['top']
        natural = n * 12.0
        target = (CONTENT_BOTTOM - 0.12) * 72 - top_pt
        sa_list = [0] * n
        if n > 1 and target - natural > 30:
            remaining = target - natural - 1.0
            base = int(remaining // (n - 1))
            extra = int(round(remaining - base * (n - 1)))
            sa_list = [base + 1 if i < extra else base for i in range(n - 1)] + [0]
            sa_list = [max(0, min(s, 20)) for s in sa_list]
        h = (natural + sum(sa_list)) / 72.0
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Pt(0); tf.margin_right = Pt(0); tf.margin_top = Pt(0); tf.margin_bottom = Pt(0)
        tf.vertical_anchor = MSO_ANCHOR.TOP
        for li, line in enumerate(lines):
            p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
            p.line_spacing = Pt(12)
            p.space_after = Pt(sa_list[li])
            p.space_before = Pt(0)
            run = p.add_run()
            run.text = line
            run.font.size = Pt(sz)
            run.font.color.rgb = WHITE
            run.font.name = '微软雅黑'
    tb(slide, 0, FOOTER_Y, SLIDE_W, SLIDE_H - FOOTER_Y, FOOTER_TEXT, sz=7, c=MGRAY, al=PP_ALIGN.CENTER, an=MSO_ANCHOR.MIDDLE)

def a2a_generate(enable_watermark=False):
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    a2a_cover(prs)
    a2a_toc(prs)
    for m in MODULES:
        pn, title, content, detail = m
        content_page_1(prs, pn, title + '（1）', content, [], [])
        content_page_2(prs, pn, title + '（2）', content, [], [])
        detail_page_1(prs, pn, title + '（3）', '▎核心细节 · 技术参数 · 落地路径', detail)
        detail_page_2(prs, pn, title + '（4）', '▎核心细节 · 技术参数 · 落地路径', detail)
    with open(TEXT_JSON, encoding='utf-8') as f:
        tp = json.load(f)
    render_text_page(prs, '全景1', '【AI能力全景图】截止2026年8月29日（1）', tp['10'])
    render_text_page(prs, '全景2', '【AI能力全景图】决策·协作·进化·维度（2）', tp['11'])
    render_text_page(prs, '趋势', '【2027年至2035年AI最新发展动态和趋势】', tp['12'])
    render_text_page(prs, '法律', '【法律声明】', tp['13'])
    render_text_page(prs, '免责', '【免责条款】', tp['14'])
    a2a_back(prs)
    if enable_watermark:
        add_watermark(prs)
    return prs

def a2a_measure_pass(measure_file):
    # 模板函数来自exec的g字典，必须改g['MEASURE_MODE']才生效
    g['MEASURE_MODE'] = True
    prs = a2a_generate(enable_watermark=False)
    g['MEASURE_MODE'] = False
    prs.save(measure_file)
    import win32com.client
    import time
    App = win32com.client.Dispatch("PowerPoint.Application")
    App.Visible = True
    time.sleep(1)
    Prs = App.Presentations.Open(measure_file, ReadOnly=True)
    time.sleep(2)
    for si in range(3, 3 + len(MODULES) * 4):
        slide = Prs.Slides(si)
        m_idx = (si - 3) // 4
        page = (si - 3) % 4
        suffix = ('C1', 'C2', 'D1', 'D2')[page]
        key = MODULES[m_idx][0] + suffix
        for shape in slide.Shapes:
            if not shape.HasTextFrame:
                continue
            if not (shape.Top > 0.4 * 72 and shape.Height > 2.0 * 72):
                continue
            tr = shape.TextFrame.TextRange
            B0 = tr.BoundHeight
            pc = tr.Paragraphs().Count
            para_lines = []
            for pi in range(2, pc + 1):
                p = tr.Paragraphs(pi)
                para_lines.append(max(1, int(round(p.BoundHeight / 14.0))))
            MEASURED[key] = {'B0': B0, 'para_lines': para_lines}
    Prs.Close()
    App.Quit()

if __name__ == '__main__':
    ver = 'V52'
    print('正在生成测量版...', flush=True)
    mf = os.path.join(OUT_DIR, '_a2a_measure_tmp.pptx')
    a2a_measure_pass(mf)
    print('测量完成：' + str(len(MEASURED)) + '页实测数据', flush=True)
    m = MEASURED.get('项目1C1')
    if m:
        print('DEBUG 项目1C1 B0=%.1f para_lines=%s' % (m['B0'], m['para_lines']), flush=True)
    prs1 = a2a_generate(enable_watermark=False)
    f1 = os.path.join(OUT_DIR, 'A2A协议2.0_AI智能体演进路线图_2026_' + ver + '_无水印版.pptx')
    prs1.save(f1)
    print('无水印版已保存', flush=True)
    prs2 = a2a_generate(enable_watermark=True)
    f2 = os.path.join(OUT_DIR, 'A2A协议2.0_AI智能体演进路线图_2026_' + ver + '_带水印增强保护.pptx')
    prs2.save(f2)
    print('水印版已保存', flush=True)
    os.remove(mf)
    print('全部完成', flush=True)
