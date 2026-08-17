# -*- coding: utf-8 -*-
# 只替换布局函数部分
import sys
sys.path.insert(0, r'F:\个人作品\具身智能')

# 读取原文件
with open(r'F:\个人作品\具身智能\generate_business_ppt.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到布局函数开始和结束
start_marker = "# ========== 内容描述页（单数页）：文本框直接拉满卡片 =========="
end_marker = "# ========== 目录页 - 22模块完整填满 =========="

# 新的布局函数代码
new_layout = '''# ========== 内容描述页（单数页）：上部左右10条+下部过程，文本框直接拉满均匀填充 ==========
def content_page(prs, _, part_num, title, left_items, right_items, process_title, process_items):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, DARK_BLUE)
    add_page_header(slide, part_num, title)
    add_page_tag(slide, '内容描述', ACCENT_BLUE)
    
    col_gap = 0.16
    col_w = (CONTENT_W - col_gap) / 2
    upper_y = CONTENT_TOP
    left_x = CONTENT_X
    right_x = CONTENT_X + col_w + col_gap
    bot_y = upper_y + CONTENT_UPPER_H + CONTENT_GAP
    
    # ========== 左栏 ==========
    rrect(slide, left_x, upper_y, col_w, CONTENT_UPPER_H, fc=MID_BLUE)
    rect(slide, left_x, upper_y, 0.05, CONTENT_UPPER_H, fc=ACCENT_BLUE)
    box_l = slide.shapes.add_textbox(Inches(left_x + 0.06), Inches(upper_y + 0.04), Inches(col_w - 0.12), Inches(CONTENT_UPPER_H - 0.08))
    tf_l = box_l.text_frame; tf_l.word_wrap = True
    tf_l.margin_left = Pt(2); tf_l.margin_right = Pt(2); tf_l.margin_top = Pt(0); tf_l.margin_bottom = Pt(0)
    # 标题
    p_tl = tf_l.paragraphs[0]
    p_tl.line_spacing = 1.1
    p_tl.space_after = Pt(2)
    r_tl = p_tl.add_run(); r_tl.text = '▎核心内容'
    r_tl.font.size = Pt(10); r_tl.font.bold = True; r_tl.font.color.rgb = GOLD; r_tl.font.name = '微软雅黑'
    # 10条内容
    add_bullets(tf_l, left_items[:10], start_idx=1, sz=10, line_spacing=1.1, space_after=2)
    
    # ========== 右栏 ==========
    rrect(slide, right_x, upper_y, col_w, CONTENT_UPPER_H, fc=MID_BLUE)
    rect(slide, right_x, upper_y, 0.05, CONTENT_UPPER_H, fc=ACCENT_BLUE)
    box_r = slide.shapes.add_textbox(Inches(right_x + 0.06), Inches(upper_y + 0.04), Inches(col_w - 0.12), Inches(CONTENT_UPPER_H - 0.08))
    tf_r = box_r.text_frame; tf_r.word_wrap = True
    tf_r.margin_left = Pt(2); tf_r.margin_right = Pt(2); tf_r.margin_top = Pt(0); tf_r.margin_bottom = Pt(0)
    p_tr = tf_r.paragraphs[0]
    p_tr.line_spacing = 1.1
    p_tr.space_after = Pt(2)
    r_tr = p_tr.add_run(); r_tr.text = '▎代表动态'
    r_tr.font.size = Pt(10); r_tr.font.bold = True; r_tr.font.color.rgb = GOLD; r_tr.font.name = '微软雅黑'
    add_bullets(tf_r, right_items[:10], start_idx=1, sz=10, line_spacing=1.1, space_after=2)
    
    # ========== 下部通栏 ==========
    rrect(slide, CONTENT_X, bot_y, CONTENT_W, CONTENT_LOWER_H, fc=MID_BLUE)
    rect(slide, CONTENT_X, bot_y, CONTENT_W, 0.04, fc=GOLD)
    box_b = slide.shapes.add_textbox(Inches(CONTENT_X + 0.06), Inches(bot_y + 0.04), Inches(CONTENT_W - 0.12), Inches(CONTENT_LOWER_H - 0.08))
    tf_b = box_b.text_frame; tf_b.word_wrap = True
    tf_b.margin_left = Pt(2); tf_b.margin_right = Pt(2); tf_b.margin_top = Pt(0); tf_b.margin_bottom = Pt(0)
    p_tb = tf_b.paragraphs[0]
    p_tb.line_spacing = 1.1
    p_tb.space_after = Pt(4)
    r_tb = p_tb.add_run(); r_tb.text = process_title
    r_tb.font.size = Pt(10); r_tb.font.bold = True; r_tb.font.color.rgb = GOLD; r_tb.font.name = '微软雅黑'
    add_bullets(tf_b, process_items[:5], start_idx=1, sz=10, line_spacing=1.1, space_after=4)
    
    # 页脚
    tb(slide, 0, CONTENT_BOTTOM + 0.02, SLIDE_W, 0.1, '具身智能&AI产业最新进展 · 2026年8月15日', sz=7, c=MGRAY, al=PP_ALIGN.CENTER)

# ========== 细节描述页（双数页）：通栏20条，文本框直接拉满 ==========
def detail_page(prs, _, part_num, title, detail_title, detail_items):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, DARK_BLUE)
    add_page_header(slide, part_num, title)
    add_page_tag(slide, '细节描述', GOLD)
    
    content_y = CONTENT_TOP
    rrect(slide, CONTENT_X, content_y, CONTENT_W, DETAIL_CONTENT_H, fc=MID_BLUE)
    rect(slide, CONTENT_X, content_y, 0.06, DETAIL_CONTENT_H, fc=GOLD)
    
    box = slide.shapes.add_textbox(Inches(CONTENT_X + 0.07), Inches(content_y + 0.04), Inches(CONTENT_W - 0.12), Inches(DETAIL_CONTENT_H - 0.08))
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = Pt(2); tf.margin_right = Pt(2); tf.margin_top = Pt(0); tf.margin_bottom = Pt(0)
    p_title = tf.paragraphs[0]
    p_title.line_spacing = 1.1
    p_title.space_after = Pt(2)
    run_t = p_title.add_run(); run_t.text = detail_title
    run_t.font.size = Pt(11); run_t.font.bold = True; run_t.font.color.rgb = GOLD; run_t.font.name = '微软雅黑'
    add_bullets(tf, detail_items[:20], start_idx=1, sz=10, line_spacing=1.1, space_after=1)
    
    tb(slide, 0, CONTENT_BOTTOM + 0.02, SLIDE_W, 0.1, '具身智能&AI产业最新进展 · 2026年8月15日 · 最新行情/研发/成果', sz=7, c=MGRAY, al=PP_ALIGN.CENTER)

'''

# 找到位置并替换
start_idx = content.find(start_marker)
end_idx = content.find(end_marker)
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_layout + content[end_idx:]
    with open(r'F:\个人作品\具身智能\generate_business_ppt.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('布局函数替换成功！')
else:
    print(f'未找到标记: start={start_idx}, end={end_idx}')
