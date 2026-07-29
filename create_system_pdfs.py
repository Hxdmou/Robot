
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

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Chinese font
font_path = r"C:\Windows\Fonts\msyh.ttc"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('MicrosoftYaHei', font_path))
    CHINESE_FONT = 'MicrosoftYaHei'
    CHINESE_FONT_BOLD = 'MicrosoftYaHei'
else:
    CHINESE_FONT = 'Helvetica'
    CHINESE_FONT_BOLD = 'Helvetica-Bold'

PRIMARY_COLOR = HexColor('#1a73e8')
SECONDARY_COLOR = HexColor('#34a853')
DARK_COLOR = HexColor('#202124')
GRAY_COLOR = HexColor('#5f6368')
LIGHT_GRAY = HexColor('#f1f3f4')
ACCENT_COLOR = HexColor('#ea4335')

def create_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='MainTitle', fontSize=26, textColor=PRIMARY_COLOR, spaceAfter=12, alignment=TA_CENTER, fontName=CHINESE_FONT_BOLD))
    styles.add(ParagraphStyle(name='SubTitle', fontSize=12, textColor=GRAY_COLOR, spaceAfter=20, alignment=TA_CENTER, fontName=CHINESE_FONT))
    styles.add(ParagraphStyle(name='SectionTitle', fontSize=14, textColor=PRIMARY_COLOR, spaceBefore=15, spaceAfter=8, fontName=CHINESE_FONT_BOLD))
    styles.add(ParagraphStyle(name='CustomBody', fontSize=10, textColor=DARK_COLOR, spaceAfter=6, alignment=TA_JUSTIFY, leading=14, fontName=CHINESE_FONT))
    styles.add(ParagraphStyle(name='TableHeader', fontSize=10, textColor=white, fontName=CHINESE_FONT_BOLD))
    styles.add(ParagraphStyle(name='TableCell', fontSize=9, textColor=DARK_COLOR, leading=12, fontName=CHINESE_FONT))
    styles.add(ParagraphStyle(name='TableCellBold', fontSize=9, textColor=DARK_COLOR, fontName=CHINESE_FONT_BOLD))
    styles.add(ParagraphStyle(name='FeatureTitle', fontSize=11, textColor=SECONDARY_COLOR, fontName=CHINESE_FONT_BOLD, spaceAfter=4))
    styles.add(ParagraphStyle(name='FeatureItem', fontSize=9, textColor=DARK_COLOR, leading=12, leftIndent=10, fontName=CHINESE_FONT))
    styles.add(ParagraphStyle(name='CoverText', fontSize=11, textColor=GRAY_COLOR, alignment=TA_CENTER, leading=16, fontName=CHINESE_FONT))
    styles.add(ParagraphStyle(name='Footer', fontSize=9, textColor=GRAY_COLOR, alignment=TA_CENTER, fontName=CHINESE_FONT))
    styles.add(ParagraphStyle(name='BulletItem', fontSize=9, textColor=DARK_COLOR, leading=13, leftIndent=15, fontName=CHINESE_FONT))
    return styles

def create_header_table(styles, system_name, system_file, system_port):
    data = [
        [Paragraph('<b>系统名称</b>', styles['TableCell']), Paragraph(system_name, styles['TableCell'])],
        [Paragraph('<b>启动文件</b>', styles['TableCell']), Paragraph(system_file, styles['TableCell'])],
        [Paragraph('<b>默认端口</b>', styles['TableCell']), Paragraph(system_port, styles['TableCell'])],
    ]
    table = Table(data, colWidths=[3*cm, 13*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    return table

def create_feature_table(styles, features):
    data = [[Paragraph(f'{i+1}. {feature}', styles['BulletItem'])] for i, feature in enumerate(features)]
    table = Table(data, colWidths=[16*cm])
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.lightgrey),
    ]))
    return table

def create_use_case_table(styles, use_cases):
    data = [[Paragraph(f'{i+1}. {uc}', styles['BulletItem'])] for i, uc in enumerate(use_cases)]
    table = Table(data, colWidths=[16*cm])
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.lightgrey),
    ]))
    return table

def generate_pdf(output_path, system_name, system_file, system_port, description, features, use_cases, tech_specs, advantages):
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
    styles = create_styles()
    story = []
    
    # Cover
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(system_name, styles['MainTitle']))
    story.append(Paragraph("产品介绍文档", styles['SubTitle']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph('<font size="10" color="#5f6368">基于RAG检索增强生成技术的企业级智能问答系统</font>', styles['CoverText']))
    story.append(Spacer(1, 2*cm))
    
    # Quick info
    info_data = [
        [Paragraph('<b>版本</b>', styles['TableCell']), Paragraph('v1.0', styles['TableCell'])],
        [Paragraph('<b>发布日期</b>', styles['TableCell']), Paragraph('2026-05-17', styles['TableCell'])],
        [Paragraph('<b>技术架构</b>', styles['TableCell']), Paragraph('RAG + FAISS向量数据库', styles['TableCell'])],
        [Paragraph('<b>支持模型</b>', styles['TableCell']), Paragraph('阿里云百炼 / OpenAI GPT', styles['TableCell'])],
    ]
    info_table = Table(info_data, colWidths=[3*cm, 13*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("2026 RAG智能问答系统 | 基于检索增强生成技术构建", styles['Footer']))
    story.append(PageBreak())
    
    # System overview
    story.append(Paragraph("1. 系统概述", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=10))
    story.append(Paragraph(description, styles['CustomBody']))
    story.append(Spacer(1, 0.5*cm))
    
    # System info
    story.append(Paragraph("2. 基本信息", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=10))
    story.append(create_header_table(styles, system_name, system_file, system_port))
    story.append(Spacer(1, 0.5*cm))
    
    # Use cases
    story.append(Paragraph("3. 适用场景", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=10))
    story.append(create_use_case_table(styles, use_cases))
    story.append(Spacer(1, 0.5*cm))
    
    # Core features
    story.append(Paragraph("4. 核心功能", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=10))
    story.append(create_feature_table(styles, features))
    story.append(Spacer(1, 0.5*cm))
    story.append(PageBreak())
    
    # Technical specs
    story.append(Paragraph("5. 技术规格", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=10))
    tech_data = [[Paragraph(f'<b>{spec[0]}</b>', styles['TableCell']), Paragraph(spec[1], styles['TableCell'])] for spec in tech_specs]
    tech_table = Table(tech_data, colWidths=[4*cm, 12*cm])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 0.5*cm))
    
    # Advantages
    story.append(Paragraph("6. 系统优势", styles['SectionTitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=10))
    story.append(create_feature_table(styles, advantages))
    story.append(Spacer(1, 1*cm))
    
    # Footer
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("联系邮箱: [contact_email_placeholder] | 项目地址: https://github.com/Hxdmou/legal-rag-qa-system", styles['Footer']))
    story.append(Paragraph("Copyright 2026 RAG智能问答系统. 保留所有权利。", styles['Footer']))
    
    doc.build(story)
    print(f"PDF generated: {output_path}")

# E-commerce QA System
generate_pdf(
    OUTPUT_DIR  # was: 电商零售问答系统介绍.pdf,
    "电商零售问答系统",
    "e_commerce_qa.py",
    "7874",
    "电商零售问答系统是一款基于RAG检索增强生成技术的企业级智能问答解决方案。该系统专为电商零售行业设计，能够帮助企业快速构建智能客服体系，提升客户服务质量和效率。系统支持商品知识查询、运营策略咨询、营销活动策划等多种应用场景，助力电商企业实现数字化转型。",
    ["商品知识库管理与智能检索", "电商运营策略智能咨询", "客服话术自动生成与优化", "营销活动策划建议与方案生成", "商品推荐与搭配建议", "订单处理流程智能引导", "用户评论分析与情感识别", "竞品信息查询与对比分析"],
    ["电商平台客服接待与问题解答", "商品详情页信息查询与推荐", "促销活动策划与执行方案", "客户订单问题处理与跟踪", "售后服务咨询与解决方案", "商品选品与供应链咨询"],
    [
        ("系统架构", "B/S架构，Streamlit Web框架"),
        ("向量数据库", "FAISS分布式向量索引"),
        ("Embedding模型", "text-embedding-3-small / 阿里云百炼"),
        ("LLM模型支持", "GPT-4 / GPT-3.5 / 通义千问"),
        ("部署方式", "Docker容器化部署 / 本地私有化部署"),
        ("系统配置", "CPU: 4核+ / 内存: 8GB+ / 硬盘: 50GB+"),
        ("API接口", "RESTful API，支持第三方系统集成"),
        ("数据安全", "本地化处理，数据不出企业内网"),
    ],
    ["开箱即用，预置行业知识库，上线周期短", "私有化部署，数据安全可控", "支持自定义知识库，灵活适配业务需求", "多轮对话能力，理解复杂咨询意图", "7x24小时不间断服务，提升客户满意度", "持续学习优化，越用越智能"]
)

# Government QA System
generate_pdf(
    OUTPUT_DIR  # was: 政务服务问答系统介绍.pdf,
    "政务服务问答系统",
    "government_qa.py",
    "7875",
    "政务服务问答系统是一款专为政府机构设计的智能问答解决方案，基于RAG检索增强生成技术构建。系统能够为民众提供政策法规咨询、办事流程指引、政务信息查询等服务，有效提升政务服务效率和群众满意度。该系统支持政策解读、表格下载、在线办事入口导航等多种功能，是智慧政务建设的重要工具。",
    ["政策法规智能解读与问答", "办事流程可视化指引", "政务表格在线查询与下载", "常见问题自动回复", "在线办事入口智能导航", "政务信息实时查询与更新", "群众意见建议智能收集", "政务服务满意度调查分析"],
    ["市民政务咨询与问题解答", "政策法规查询与解读", "办事流程与材料准备指引", "政务服务大厅业务引导", "公共服务设施查询", "政务投诉与建议处理"],
    [
        ("系统架构", "B/S架构，Streamlit Web框架"),
        ("向量数据库", "FAISS分布式向量索引"),
        ("Embedding模型", "text-embedding-3-small / 阿里云百炼"),
        ("LLM模型支持", "GPT-4 / GPT-3.5 / 通义千问"),
        ("部署方式", "政务云部署 / 私有化部署"),
        ("系统配置", "CPU: 4核+ / 内存: 8GB+ / 硬盘: 50GB+"),
        ("API接口", "RESTful API，支持政务平台集成"),
        ("数据安全", "符合等保三级安全要求"),
    ],
    ["政策解读准确，引用权威来源", "7x24小时政务服务不间断", "多渠道接入，支持网站/APP/小程序", "数据本地化存储，保障政务信息安全", "智能分流，减轻人工客服压力", "持续更新政策库，保持时效性"]
)

# HR QA System
generate_pdf(
    OUTPUT_DIR  # was: 人力资源问答系统介绍.pdf,
    "人力资源问答系统",
    "hr_qa.py",
    "7876",
    "人力资源问答系统是一款基于RAG技术的企业级智能问答解决方案，专为企业人力资源管理部门和员工设计。系统能够处理招聘咨询、培训查询、绩效考核政策解读、员工福利咨询等多种HR事务，有效提升HR工作效率和员工满意度。系统支持对接企业现有HR系统，实现数据互通和流程协同。",
    ["招聘流程管理与进度查询", "员工培训计划与课程查询", "绩效考核政策智能解读", "劳动合同与法规咨询", "员工福利方案详细介绍", "请假考勤制度解答", "职级晋升通道指引", "离职流程与手续办理"],
    ["新员工入职手续咨询", "招聘岗位与要求查询", "培训课程与时间安排", "绩效考核结果解读", "薪资福利政策咨询", "劳动法规与合同问题", "员工关系与投诉处理", "职业发展规划建议"],
    [
        ("系统架构", "B/S架构，Streamlit Web框架"),
        ("向量数据库", "FAISS分布式向量索引"),
        ("Embedding模型", "text-embedding-3-small / 阿里云百炼"),
        ("LLM模型支持", "GPT-4 / GPT-3.5 / 通义千问"),
        ("部署方式", "企业内网部署 / SaaS云服务"),
        ("系统配置", "CPU: 4核+ / 内存: 8GB+ / 硬盘: 50GB+"),
        ("API接口", "RESTful API，支持HR系统对接"),
        ("数据安全", "企业内网部署，数据完全自主可控"),
    ],
    ["HR事务处理效率提升80%以上", "员工自助查询，减少HR重复工作", "政策解读一致，避免执行偏差", "7x24小时服务，提升员工体验", "操作日志完整，审计可追溯", "可对接企业微信/钉钉等多平台"]
)

# Academic QA System
generate_pdf(
    OUTPUT_DIR  # was: 科研学术问答系统介绍.pdf,
    "科研学术问答系统",
    "academic_qa.py",
    "7877",
    "科研学术问答系统是一款面向科研人员和学术机构的智能问答解决方案，基于RAG检索增强生成技术构建。系统整合了海量学术文献、研究成果和科研规范知识，能够为用户提供文献检索、论文写作指导、研究方法咨询等学术服务。系统支持多种引用格式自动生成，是科研人员开展学术研究的得力助手。",
    ["学术文献智能检索与推荐", "论文结构与写作规范指导", "研究方法与实验设计咨询", "学术规范与伦理审查解读", "论文格式模板自动生成", "参考文献引用格式转换", "学术术语解释与百科查询", "研究热点与前沿动态追踪"],
    ["文献资料查询与获取指导", "论文开题报告撰写咨询", "实验设计与方法论指导", "学术论文润色与修改建议", "期刊投稿与审稿意见回复", "学术会议信息查询", "科研项目申报指南", "学术不端行为防范咨询"],
    [
        ("系统架构", "B/S架构，Streamlit Web框架"),
        ("向量数据库", "FAISS分布式向量索引"),
        ("Embedding模型", "text-embedding-3-small / 阿里云百炼"),
        ("LLM模型支持", "GPT-4 / GPT-3.5 / 通义千问"),
        ("部署方式", "高校私有云部署 / 机构本地部署"),
        ("系统配置", "CPU: 4核+ / 内存: 8GB+ / 硬盘: 100GB+"),
        ("API接口", "RESTful API，支持学术平台集成"),
        ("数据安全", "机构内网部署，研究数据安全"),
    ],
    ["海量学术资源整合，知识覆盖面广", "智能文献推荐，发现相关研究", "写作辅助功能，提升论文质量", "多引用格式支持，自动转换", "保护研究隐私，数据安全可靠", "持续更新学术库，保持前沿性"]
)

print("\nAll PDFs generated successfully!")