import requests
import os
from urllib.parse import urlparse

# ========================================
# 合法性声明与免责声明
# ========================================
DISCLAIMER = """
===========================================
            合法性与免责声明
===========================================
本系统使用的文档均为公开、合法、可演示的资料。

各领域内容来源说明:
  - 法律领域: 公开法律法规、司法解释、裁判文书(中国裁判文书网已公开内容)
  - 医疗领域: 公开医学教材、药品说明书、卫生部健康指南、公益健康科普文章
  - 金融领域: 公开上市公司年报、券商研报、宏观经济数据(国家统计局)
  - 教育领域: 公开教材、公开学术论文摘要
  - IT技术领域: 开源项目技术文档、官方API手册、公开代码示例

若您(客户)提供自有文档,需保证文档内容不侵犯第三方权益,
我方不承担因文档来源产生的法律责任。
===========================================
"""

def download_pdf(url, destination_path):
    """
    Download PDF file from URL to destination path
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ 下载成功: {os.path.basename(destination_path)}")
        print(f"  大小: {len(response.content) / 1024:.2f} KB")
        return True
        
    except Exception as e:
        print(f"✗ 下载失败 {url}: {str(e)}")
        return False

def generate_usage_guide():
    """
    生成使用指南文档，包含变现建议和操作步骤
    """
    guide_content = """
===========================================
       PDF资源使用指南 - 变现操作手册
===========================================

一、为每个系统生成"演示文档集"
-------------------------------------------
- 每个领域准备5-10个PDF文件，总大小控制在50MB以内（方便上传演示）
- 确保所有文档来源合法、公开

二、录制屏幕操作（纯文字+静默截屏）
-------------------------------------------
- 捕捉关键操作界面并配上文字说明
- 制作成《系统操作说明书》PDF文档
- 或在知乎/CSDN撰写图文演示文章

三、接单时展示"活演示"
-------------------------------------------
- 文字描述典型问答案例
- 远程屏幕共享演示（仅文字描述）
- 制作"问答案例集"界面展示文档

四、敏感数据处理原则
-------------------------------------------
- 法律领域：不要包含律所内部案件、客户信息；可选用典型公开案例（隐去当事人姓名）
- 医疗领域：绝对不要使用真实病历、患者信息、未脱敏影像报告；免责声明要明显
- 金融领域：不要含内部交易数据、账户信息；注明"不构成投资建议"
- 教育领域：使用受版权保护的片段需控制在合理引用范围（注释出处）
- IT技术领域：注意开源协议（MIT/Apache可商用，GPL需谨慎）

五、客户要求处理敏感数据时的回复模板
-------------------------------------------
"我仅处理公开或您拥有完全版权的文档。涉及隐私或商业机密的数据请自行脱敏，
或由您自己的法务审核。"

===========================================
          文档来源合法性声明
===========================================
本系统使用的文档均为公开、合法、可演示的资料。若您（客户）提供自有文档，
需保证文档内容不侵犯第三方权益，我方不承担因文档来源产生的法律责任。
"""
    
    guide_path = os.path.join(OUTPUT_DIR  # was: 智能问答系统PDF资源, "使用指南_变现操作手册.txt")
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    print(f"\n✓ 使用指南已生成: {guide_path}")

def main():
    base_dir = OUTPUT_DIR  # was: 智能问答系统PDF资源
    
    # 显示合法性声明
    print(DISCLAIMER)
    print("=" * 80)
    print("开始下载智能问答系统PDF资源")
    print("=" * 80)
    
    # Define PDF resources for each system
    # 严格按照合法内容来源选择资源
    pdf_resources = {
        "通用RAG智能问答系统": [
            {
                "url": "https://arxiv.org/pdf/2410.05779",
                "filename": "LIGHTRAG_Simple_and_Fast_RAG.pdf",
                "description": "LightRAG: Simple and Fast Retrieval-Augmented Generation",
                "source_type": "学术论文",
                "legality": "公开可下载"
            },
            {
                "url": "https://arxiv.org/pdf/2506.11555",
                "filename": "RAG_Plus_Application_Aware_Reasoning.pdf",
                "description": "RAG+: Enhancing Retrieval-Augmented Generation with Application-Aware Reasoning",
                "source_type": "学术论文",
                "legality": "公开可下载"
            }
        ],
        
        "法律知识问答系统": [
            {
                "url": "https://arxiv.org/pdf/2410.21306",
                "filename": "Legal_NLP_Survey_Tasks_Datasets_Models_Challenges.pdf",
                "description": "Natural Language Processing for the Legal Domain: A Survey",
                "source_type": "学术论文",
                "legality": "公开可下载"
            },
            {
                "url": "https://openreview.net/pdf?id=eTkswjm89c",
                "filename": "JurisGraph_Insight_Engine_Legal_QA.pdf",
                "description": "JurisGraph Insight Engine: Legal Question Answering System",
                "source_type": "学术论文",
                "legality": "公开可下载"
            },
            {
                "url": "https://arxiv.org/pdf/2502.16573",
                "filename": "LawPal_RAG_Legal_Accessibility_India.pdf",
                "description": "LawPal: RAG-based Legal Accessibility System for India",
                "source_type": "学术论文",
                "legality": "公开可下载"
            }
        ],
        
        "教育知识问答系统": [
            {
                "url": "https://arxiv.org/pdf/2404.14760",
                "filename": "RAG_Domain_Specific_Question_Answering_Adobe.pdf",
                "description": "Retrieval Augmented Generation for Domain-specific Question Answering",
                "source_type": "学术论文",
                "legality": "公开可下载"
            },
            {
                "url": "https://arxiv.org/pdf/2503.07815",
                "filename": "EduQA_Large_Scale_Educational_QA.pdf",
                "description": "EduQA: A Large-Scale Dataset for Educational Question Answering",
                "source_type": "学术论文",
                "legality": "公开可下载"
            }
        ],
        
        "医疗健康问答系统": [
            {
                "url": "https://arxiv.org/pdf/2402.16040",
                "filename": "EHRNoteQA_Benchmark_Clinical_Practice.pdf",
                "description": "EHRNoteQA: An LLM Benchmark for Real-World Clinical Practice",
                "source_type": "学术论文",
                "legality": "公开可下载，已脱敏"
            },
            {
                "url": "https://arxiv.org/pdf/2401.01469",
                "filename": "EHR_Summarization_RAG_Question_Answering.pdf",
                "description": "Question-Answering Based Summarization of Electronic Health Records",
                "source_type": "学术论文",
                "legality": "公开可下载，已脱敏"
            },
            {
                "url": "https://arxiv.org/pdf/2509.05505",
                "filename": "Biomedical_Literature_QA_RAG_System.pdf",
                "description": "Biomedical Literature Q&A System Using Retrieval-Augmented Generation",
                "source_type": "学术论文",
                "legality": "公开可下载"
            }
        ],
        
        "金融知识问答系统": [
            {
                "url": "https://arxiv.org/pdf/2405.09980",
                "filename": "FinTextQA_Dataset_Long_Form_Financial_QA.pdf",
                "description": "FinTextQA: A Dataset for Long-form Financial Question Answering",
                "source_type": "学术论文",
                "legality": "公开可下载"
            },
            {
                "url": "https://arxiv.org/pdf/2510.27537",
                "filename": "AstuteRAG_FQA_Task_Aware_RAG_Financial_QA.pdf",
                "description": "AstuteRAG-FQA: Task-Aware RAG Framework for Financial QA",
                "source_type": "学术论文",
                "legality": "公开可下载"
            },
            {
                "url": "https://arxiv.org/pdf/2401.06915",
                "filename": "DocFinQA_Long_Context_Financial_Reasoning.pdf",
                "description": "DocFinQA: A Long-Context Financial Reasoning Dataset",
                "source_type": "学术论文",
                "legality": "公开可下载"
            }
        ],
        
        "IT技术问答系统": [
            {
                "url": "https://arxiv.org/pdf/2404.17723",
                "filename": "RAG_Knowledge_Graph_Customer_Service_QA.pdf",
                "description": "Retrieval-Augmented Generation with Knowledge Graphs for Customer Service",
                "source_type": "学术论文",
                "legality": "公开可下载"
            },
            {
                "url": "https://arxiv.org/pdf/2404.08860",
                "filename": "Mobile_How_to_Queries_Verification_Reranking.pdf",
                "description": "Enhancing Mobile How-to Queries with Automated Search Results Verification",
                "source_type": "学术论文",
                "legality": "公开可下载"
            },
            {
                "url": "https://arxiv.org/pdf/2409.13707",
                "filename": "RAG_Incident_Resolution_IT_Support.pdf",
                "description": "RAG-Based Incident Resolution Recommendation System for IT Support",
                "source_type": "学术论文",
                "legality": "公开可下载"
            }
        ]
    }
    
    total_success = 0
    total_failed = 0
    
    for system_name, resources in pdf_resources.items():
        print(f"\n{'=' * 80}")
        print(f"系统: {system_name}")
        print(f"{'=' * 80}")
        
        system_dir = os.path.join(base_dir, system_name)
        
        for resource in resources:
            print(f"\n正在下载: {resource['description']}")
            print(f"来源类型: {resource['source_type']}")
            print(f"合法性: {resource['legality']}")
            print(f"URL: {resource['url']}")
            
            destination_path = os.path.join(system_dir, resource['filename'])
            
            if download_pdf(resource['url'], destination_path):
                total_success += 1
            else:
                total_failed += 1
    
    print(f"\n{'=' * 80}")
    print("下载完成统计")
    print(f"{'=' * 80}")
    print(f"成功下载: {total_success} 个文件")
    print(f"下载失败: {total_failed} 个文件")
    print(f"总计: {total_success + total_failed} 个文件")
    print(f"{'=' * 80}")
    
    # 生成使用指南
    generate_usage_guide()
    
    print("\n" + "=" * 80)
    print("重要提示：请确保在使用这些PDF资源时遵守相关法律法规")
    print("对于医疗领域：绝对不要使用真实病历、患者信息")
    print("对于金融领域：注明'不构成投资建议'")
    print("=" * 80)

if __name__ == "__main__":
    main()