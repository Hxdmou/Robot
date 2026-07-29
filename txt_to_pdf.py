
# ============================================================================
# 免责声明与AI使用规范
# ============================================================================
# 本文件仅供技术研究与学习交流使用，不得用于任何非法用途。
#
# AI使用规范：
#   1. 使用本文件相关内容时须遵守所在地法律法规及伦理准则
#   2. 不得用于侵犯他人合法权益、危害网络安全、破坏公共秩序的活动
#   3. 涉及自动化决策的场景须确保人工复核机制与可解释性
#   4. 处理个人信息时须符合数据保护相关法规要求
#
# 风险提示：
#   本文件内容按"现状"提供，不保证绝对准确无误。
#   使用者须自行评估风险，因使用本文件导致的任何损失由使用者承担。
# ============================================================================

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def register_chinese_fonts():
    """
    注册中文字体
    在Windows系统上使用系统自带的中文字体
    """
    # 尝试注册多种中文字体
    font_paths = [
        r'C:\Windows\Fonts\simhei.ttf',      # 黑体
        r'C:\Windows\Fonts\simsun.ttc',      # 宋体
        r'C:\Windows\Fonts\msyh.ttc',        # 微软雅黑
        r'C:\Windows\Fonts\simkai.ttf',      # 楷体
    ]
    
    font_names = ['SimHei', 'SimSun', 'MicrosoftYaHei', 'KaiTi']
    
    for font_path, font_name in zip(font_paths, font_names):
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                print(f"✓ 已注册字体: {font_name}")
                return font_name  # 返回第一个成功注册的字体
            except Exception as e:
                print(f"✗ 注册字体失败 {font_name}: {str(e)}")
    
    # 如果没有找到系统字体，返回默认字体
    print("⚠ 未找到中文字体，将使用默认字体（可能无法正确显示中文）")
    return 'Helvetica'

def convert_txt_to_pdf(txt_path, pdf_path):
    """
    将txt文件转换为PDF文件，支持中文显示
    """
    # 注册中文字体
    chinese_font = register_chinese_fonts()
    
    # 读取txt文件内容
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建PDF文档
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    
    # 自定义标题样式 - 使用中文字体
    title_style = ParagraphStyle(
        'TitleStyle',
        fontName=chinese_font,
        fontSize=16,
        bold=True,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        leading=24
    )
    
    # 自定义子标题样式
    sub_title_style = ParagraphStyle(
        'SubTitleStyle',
        fontName=chinese_font,
        fontSize=14,
        bold=True,
        alignment=TA_LEFT,
        textColor=colors.darkgreen,
        leading=20
    )
    
    # 自定义正文样式
    body_style = ParagraphStyle(
        'BodyStyle',
        fontName=chinese_font,
        fontSize=11,
        alignment=TA_LEFT,
        leading=18
    )
    
    # 自定义列表样式
    list_style = ParagraphStyle(
        'ListStyle',
        fontName=chinese_font,
        fontSize=11,
        alignment=TA_LEFT,
        leading=16
    )
    
    # 自定义联系方式样式
    contact_style = ParagraphStyle(
        'ContactStyle',
        fontName=chinese_font,
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.gray,
        leading=14
    )
    
    # 自定义声明样式
    notice_style = ParagraphStyle(
        'NoticeStyle',
        fontName=chinese_font,
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.red,
        leading=14
    )
    
    elements = []
    
    # 添加主标题
    elements.append(Paragraph("RAG系统演示与接单操作手册", title_style))
    elements.append(Spacer(1, 20))
    
    # 分割内容为行
    lines = content.split('\n')
    
    for line in lines:
        stripped_line = line.strip()
        
        # 跳过空行和标题装饰行
        if not stripped_line or (stripped_line.startswith('===') and stripped_line.endswith('===')):
            elements.append(Spacer(1, 12))
            continue
        
        # 判断是否为子标题（以中文数字开头）
        if stripped_line.startswith('一、') or stripped_line.startswith('二、') or \
           stripped_line.startswith('三、') or stripped_line.startswith('四、') or \
           stripped_line.startswith('五、'):
            elements.append(Paragraph(stripped_line, sub_title_style))
            elements.append(Spacer(1, 8))
            continue
        
        # 判断是否为联系方式部分
        if stripped_line.startswith('知乎账号：') or stripped_line.startswith('邮箱：') or \
           stripped_line.startswith('GitHub链接：'):
            elements.append(Paragraph(stripped_line, contact_style))
            continue
        
        # 判断是否为末尾声明
        if stripped_line == '所有沟通仅限文字，不接受语音/视频。感谢理解。':
            elements.append(Spacer(1, 20))
            elements.append(Paragraph(stripped_line, notice_style))
            continue
        
        # 判断是否为列表项
        if stripped_line.startswith('- '):
            elements.append(Paragraph(stripped_line, list_style))
            continue
        
        # 判断是否为引用内容
        if stripped_line.startswith('"') and stripped_line.endswith('"'):
            elements.append(Paragraph(f'<i>{stripped_line}</i>', list_style))
            continue
        
        # 默认处理为正文
        elements.append(Paragraph(stripped_line, body_style))
    
    # 构建PDF
    doc.build(elements)
    print(f"\n✓ PDF文件已生成: {pdf_path}")

if __name__ == "__main__":
    txt_path = OUTPUT_DIR  # was: 使用指南_变现操作手册.txt
    pdf_path = EXTERNAL_PROJECT_PATH  # external ref
    
    print("=" * 60)
    print("开始转换TXT到PDF（支持中文）")
    print("=" * 60)
    
    # 确保reportlab已安装
    try:
        convert_txt_to_pdf(txt_path, pdf_path)
    except ImportError:
        print("需要安装reportlab库，请运行: pip install reportlab")
    except Exception as e:
        print(f"转换失败: {str(e)}")