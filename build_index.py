
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

from dotenv import load_dotenv
load_dotenv(override=True)
import os
import shutil
from rag import load_multiple_documents, chunk2vector, get_embeddings
from config.settings import SYSTEM_CONFIGS

def build_index_for_system(system_name, doc_paths):
    """为指定系统构建知识库索引"""
    index_dir = f"{system_name}_faiss_index"

    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
        print(f"已删除旧索引: {index_dir}")

    if not doc_paths or len(doc_paths) == 0:
        print(f"警告: {system_name} 没有文档文件可用于构建索引")
        return False

    try:
        print(f"正在为 {system_name} 加载文档...")
        docs = load_multiple_documents(doc_paths)

        if not docs:
            print(f"警告: {system_name} 文档加载为空")
            return False

        print(f"正在分割 {len(docs)} 个文档...")
        chunks = []
        from langchain.text_splitter import CharacterTextSplitter
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50, separator="\n")
        for doc in docs:
            chunked = text_splitter.split_documents([doc])
            chunks.extend(chunked)
        print(f"文档分割完成，共 {len(chunks)} 个 chunks")

        print(f"正在为 {system_name} 创建向量索引...")
        vector_store = chunk2vector(chunks, get_embeddings())
        vector_store.save_local(index_dir)

        print(f"✅ {system_name} 知识库索引构建成功，共 {len(docs)} 份文档")
        return True
    except Exception as e:
        print(f"❌ {system_name} 索引构建失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_knowledge_base():
    """创建各系统的示例知识库文档"""
    os.makedirs("knowledge_bases", exist_ok=True)

    medical_content = """# 医疗健康知识手册
## 常见疾病
### 感冒
- 症状：发烧、咳嗽、流鼻涕、喉咙痛
- 治疗：多喝水、休息、服用感冒药
- 预防：勤洗手、保持通风、接种疫苗
"""
    with open("knowledge_bases/medical_health.txt", "w", encoding="utf-8") as f:
        f.write(medical_content)

    education_content = """# 教育学习指南
## 学习方法
### 主动学习
- 积极提问，主动思考
- 做笔记，整理知识体系
- 讲解给他人听，检验理解
"""
    with open("knowledge_bases/education_guide.txt", "w", encoding="utf-8") as f:
        f.write(education_content)

    finance_content = """# 金融投资知识
## 投资原则
### 风险与收益
- 高风险高回报，低风险低回报
- 根据风险承受能力选择投资产品
"""
    with open("knowledge_bases/finance_investment.txt", "w", encoding="utf-8") as f:
        f.write(finance_content)

    tech_content = """# IT技术手册
## 编程基础
### Python
- 简洁易读，适合初学者
- 广泛应用于数据分析、人工智能
"""
    with open("knowledge_bases/tech_guide.txt", "w", encoding="utf-8") as f:
        f.write(tech_content)

    print("✅ 示例知识库文档创建完成")

def main():
    print("=" * 60)
    print("开始为所有系统构建知识库索引")
    print("=" * 60)

    create_sample_knowledge_base()

    systems = {
        "general": {
            "name": "通用RAG智能问答系统",
            "docs": [
                "knowledge_bases/medical_health.txt",
                "knowledge_bases/education_guide.txt",
                "knowledge_bases/finance_investment.txt",
                "knowledge_bases/tech_guide.txt"
            ]
        },
        "legal": {
            "name": "法律知识问答系统",
            "docs": [os.path.join("legal_knowledge_base", f) for f in os.listdir("legal_knowledge_base") if f.endswith(".pdf")]
        },
        "medical": {
            "name": "医疗健康问答系统",
            "docs": ["knowledge_bases/medical_health.txt"]
        },
        "education": {
            "name": "教育学习问答系统",
            "docs": ["knowledge_bases/education_guide.txt"]
        },
        "finance": {
            "name": "金融投资问答系统",
            "docs": ["knowledge_bases/finance_investment.txt"]
        },
        "tech": {
            "name": "IT技术问答系统",
            "docs": ["knowledge_bases/tech_guide.txt"]
        },
        "e_commerce": {
            "name": "电商零售问答系统",
            "docs": ["knowledge_bases/e_commerce_guide.txt"]
        },
        "government": {
            "name": "政务服务问答系统",
            "docs": ["knowledge_bases/government_guide.txt"]
        },
        "hr": {
            "name": "人力资源问答系统",
            "docs": ["knowledge_bases/hr_guide.txt"]
        },
        "academic": {
            "name": "科研学术问答系统",
            "docs": ["knowledge_bases/academic_guide.txt"]
        }
    }

    success_count = 0
    total_count = len(systems)

    for system_key, system_info in systems.items():
        print(f"\n--- 正在处理: {system_info['name']} ---")
        if build_index_for_system(system_key, system_info['docs']):
            success_count += 1

    print("\n" + "=" * 60)
    print(f"索引构建完成！成功: {success_count}/{total_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
