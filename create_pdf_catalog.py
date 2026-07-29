
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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors

PRIMARY_COLOR = HexColor('#1a73e8')
SECONDARY_COLOR = HexColor('#34a853')
DARK_COLOR = HexColor('#202124')
GRAY_COLOR = HexColor('#5f6368')
LIGHT_GRAY = HexColor('#f1f3f4')

SYSTEMS = [
    {"name": "General RAG QA System", "file": "run.py", "port": "7861", "scenario": "Document QA, Knowledge Base, Document Retrieval", "features": ["Multi-document support", "Preset knowledge base loading", "Custom parameter configuration", "Conversation history management", "Batch Q&A processing", "System backup and recovery"]},
    {"name": "Legal Knowledge QA System", "file": "legal_qa.py", "port": "7869", "scenario": "Legal consultation, Compliance services", "features": ["Legal article retrieval", "Case analysis support", "Compliance risk assessment", "Contract review assistance", "Legal Q&A bot", "Legal knowledge base"]},
    {"name": "Medical Health QA System", "file": "medical_qa.py", "port": "7871", "scenario": "Health consultation, Medical knowledge", "features": ["Symptom query diagnosis", "Drug information query", "Health knowledge", "Medical record analysis", "Medical terminology", "Treatment guide"]},
    {"name": "Education Learning QA System", "file": "education_qa.py", "port": "7870", "scenario": "Online learning, Knowledge management", "features": ["Course knowledge Q&A", "Study plan formulation", "Knowledge point retrieval", "Homework tutoring", "Learning progress tracking", "Multi-subject coverage"]},
    {"name": "Finance Investment QA System", "file": "finance_qa.py", "port": "7872", "scenario": "Financial consultation, Investment analysis", "features": ["Product recommendation", "Investment risk assessment", "Financial terminology", "Market analysis", "Financial planning", "Real-time news"]},
    {"name": "IT Technology QA System", "file": "tech_qa.py", "port": "7873", "scenario": "Technical documentation, API consultation", "features": ["Multi-language code support", "API documentation query", "Technical problem diagnosis", "Code example generation", "Architecture design", "Tech stack recommendation"]},
    {"name": "E-commerce Retail QA System", "file": "e_commerce_qa.py", "port": "7874", "scenario": "E-commerce operations, Product knowledge", "features": ["Product knowledge base", "Operation strategy", "Customer service scripts", "Marketing planning", "Product recommendation", "Order processing"]},
    {"name": "Government Services QA System", "file": "government_qa.py", "port": "7875", "scenario": "Policy interpretation, Process guidance", "features": ["Policy interpretation", "Process guidance", "Form download", "FAQ", "Online service portal", "Service navigation"]},
    {"name": "Human Resources QA System", "file": "hr_qa.py", "port": "7876", "scenario": "Recruitment, Employee training", "features": ["Recruitment management", "Training programs", "Performance assessment", "Labor contract", "Employee benefits", "HR policy Q&A"]},
    {"name": "Academic Research QA System", "file": "academic_qa.py", "port": "7877", "scenario": "Literature retrieval, Paper writing", "features": ["Literature retrieval", "Paper writing guidance", "Research methods", "Academic norms", "Paper templates", "Citation format"]}
]

class PDFCatalog:
    def __init__(self, output_path):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm)
        self.styles = getSampleStyleSheet()
        self.story = []
        self._create_styles()

    def _create_styles(self):
        self.styles.add(ParagraphStyle(name='MainTitle', parent=self.styles['Title'], fontSize=24, textColor=PRIMARY_COLOR, spaceAfter=15, alignment=TA_CENTER, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='SubTitle', parent=self.styles['Normal'], fontSize=12, textColor=GRAY_COLOR, spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica'))
        self.styles.add(ParagraphStyle(name='SectionTitle', parent=self.styles['Heading1'], fontSize=14, textColor=PRIMARY_COLOR, spaceBefore=12, spaceAfter=8, fontName='Helvetica-Bold'))
        self.styles.add(ParagraphStyle(name='CustomBody', parent=self.styles['Normal'], fontSize=9, textColor=DARK_COLOR, spaceAfter=4, alignment=TA_JUSTIFY, leading=12, fontName='Helvetica'))
        self.styles.add(ParagraphStyle(name='FeatureTitle', fontSize=11, textColor=SECONDARY_COLOR, fontName='Helvetica-Bold', spaceAfter=4))
        self.styles.add(ParagraphStyle(name='Features', fontSize=8, textColor=DARK_COLOR, leading=11, leftIndent=5, fontName='Helvetica'))
        self.styles.add(ParagraphStyle(name='CoverText', fontSize=10, textColor=GRAY_COLOR, alignment=TA_CENTER, leading=14, fontName='Helvetica'))
        self.styles.add(ParagraphStyle(name='Footer', fontSize=8, textColor=GRAY_COLOR, alignment=TA_CENTER, fontName='Helvetica'))
        self.styles.add(ParagraphStyle(name='TableCell', fontSize=8, textColor=DARK_COLOR, leading=10, fontName='Helvetica'))

    def create_cover(self):
        self.story.append(Spacer(1, 2*cm))
        self.story.append(Paragraph("RAG Intelligent QA System", self.styles['MainTitle']))
        self.story.append(Paragraph("Product Catalog", self.styles['SubTitle']))
        self.story.append(Spacer(1, 0.8*cm))
        self.story.append(Paragraph('<font size="10" color="#5f6368">This catalog details 10 independent enterprise-level intelligent QA systems,<br/>all built on RAG (Retrieval-Augmented Generation) technology.<br/>Supports private deployment and custom development.</font>', self.styles['CoverText']))
        self.story.append(Spacer(1, 1.5*cm))
        summary_data = [['Systems', '10'], ['Architecture', 'RAG + FAISS'], ['Models', 'Alibaba Cloud / OpenAI'], ['Deployment', 'Private'], ['Repository', 'github.com/Hxdmou']]
        summary_table = Table(summary_data, colWidths=[3.5*cm, 11*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
            ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        self.story.append(summary_table)
        self.story.append(Spacer(1, 2*cm))
        self.story.append(Paragraph("2026 RAG Intelligent QA System", self.styles['Footer']))
        self.story.append(PageBreak())

    def create_table_of_contents(self):
        self.story.append(Paragraph("Table of Contents", self.styles['SectionTitle']))
        self.story.append(Spacer(1, 0.3*cm))
        toc_data = [[f"{i}. {sys['name']}", f"Port: {sys['port']}"] for i, sys in enumerate(SYSTEMS, 1)]
        toc_table = Table(toc_data, colWidths=[12*cm, 4*cm])
        toc_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [white, LIGHT_GRAY]),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        self.story.append(toc_table)
        self.story.append(PageBreak())

    def create_system_page(self, sys, index):
        self.story.append(Paragraph(f"{index+1}. {sys['name']}", self.styles['SectionTitle']))
        self.story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=8))
        
        info_data = [
            [Paragraph('<b>Entry File</b>', self.styles['TableCell']), Paragraph(sys['file'], self.styles['TableCell']), 
             Paragraph('<b>Port</b>', self.styles['TableCell']), Paragraph(sys['port'], self.styles['TableCell'])],
            [Paragraph('<b>Use Cases</b>', self.styles['TableCell']), Paragraph(sys['scenario'], self.styles['TableCell']), '', '']
        ]
        info_table = Table(info_data, colWidths=[2.2*cm, 7*cm, 1.5*cm, 5.3*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
            ('BACKGROUND', (2, 0), (2, 0), LIGHT_GRAY),
            ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('SPAN', (1, 1), (3, 1)),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        self.story.append(info_table)
        self.story.append(Spacer(1, 0.3*cm))
        
        self.story.append(Paragraph("Core Features", self.styles['FeatureTitle']))
        features_data = [[Paragraph(f"[+] {feature}", self.styles['TableCell'])] for feature in sys['features']]
        features_table = Table(features_data, colWidths=[16*cm])
        features_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [white, LIGHT_GRAY]),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        self.story.append(features_table)
        self.story.append(Spacer(1, 0.5*cm))
        
        if index < len(SYSTEMS) - 1:
            self.story.append(PageBreak())

    def create_summary(self):
        self.story.append(PageBreak())
        self.story.append(Paragraph("System Summary", self.styles['SectionTitle']))
        self.story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=10))
        
        summary_header = [['No.', 'System Name', 'File', 'Port', 'Use Cases']]
        summary_data = summary_header + [[str(i+1), sys['name'], sys['file'], sys['port'], sys['scenario']] for i, sys in enumerate(SYSTEMS)]
        
        summary_table = Table(summary_data, colWidths=[1*cm, 4.5*cm, 3*cm, 1.2*cm, 6.3*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('TEXTCOLOR', (0, 1), (-1, -1), DARK_COLOR),
            ('ALIGN', (0, 0), (3, -1), 'CENTER'),
            ('ALIGN', (4, 1), (4, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        self.story.append(summary_table)
        
        self.story.append(Spacer(1, 0.8*cm))
        self.story.append(Paragraph("Contact", self.styles['SectionTitle']))
        self.story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=10))
        
        contact_data = [
            [Paragraph('<b>Repository</b>', self.styles['TableCell']), Paragraph('https://github.com/Hxdmou/legal-rag-qa-system', self.styles['TableCell'])],
            [Paragraph('<b>Support</b>', self.styles['TableCell']), Paragraph('Private deployment and custom development available', self.styles['TableCell'])],
            [Paragraph('<b>License</b>', self.styles['TableCell']), Paragraph('MIT License - Welcome to Star and Fork!', self.styles['TableCell'])]
        ]
        contact_table = Table(contact_data, colWidths=[2.5*cm, 13.5*cm])
        contact_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), LIGHT_GRAY),
            ('TEXTCOLOR', (0, 0), (-1, -1), DARK_COLOR),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        self.story.append(contact_table)
        
        self.story.append(Spacer(1, 1.5*cm))
        self.story.append(Paragraph("2026 RAG Intelligent QA System", self.styles['Footer']))

    def build(self):
        self.create_cover()
        self.create_table_of_contents()
        for i, sys in enumerate(SYSTEMS):
            self.create_system_page(sys, i)
        self.create_summary()
        self.doc.build(self.story)
        print(f"PDF generated: {self.output_path}")

if __name__ == "__main__":
    output_path = EXTERNAL_PROJECT_PATH  # external ref
    pdf = PDFCatalog(output_path)
    pdf.build()