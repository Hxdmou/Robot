#!/usr/bin/env python3
"""简化版通用RAG系统索引构建脚本"""
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



import os
import sys
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_general_index():
    """为通用RAG系统构建预置索引"""
    index_dir = "general_faiss_index"
    docs_dir = "knowledge_bases"
    
    # 检查文档目录
    if not os.path.exists(docs_dir):
        print(f"❌ 文档目录 {docs_dir} 不存在")
        return False
    
    # 获取所有txt文件
    doc_files = [f for f in os.listdir(docs_dir) if f.endswith('.txt')]
    if not doc_files:
        print(f"❌ {docs_dir} 目录中没有找到txt文档")
        return False
    
    print(f"📄 找到 {len(doc_files)} 个文档文件")
    
    try:
        # 加载文档
        docs = []
        for file_name in doc_files:
            file_path = os.path.join(docs_dir, file_name)
            loader = TextLoader(file_path, encoding='utf-8')
            docs.extend(loader.load())
            print(f"   - {file_name}")
        
        # 分割文档
        text_splitter = CharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separator="\n"
        )
        split_docs = text_splitter.split_documents(docs)
        print(f"\n📝 文档分割完成，共 {len(split_docs)} 个 chunks")
        
        # 创建嵌入模型
        print("🔧 加载本地嵌入模型...")
        embeddings = HuggingFaceEmbeddings(
            model_name="shibing624/text2vec-base-chinese",
            model_kwargs={"device": "cpu"}
        )
        
        # 创建向量索引
        print("📊 创建FAISS向量索引...")
        vector_store = FAISS.from_documents(split_docs, embeddings)
        
        # 保存索引
        vector_store.save_local(index_dir)
        print(f"✅ 索引已保存到 {index_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ 索引构建失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("通用RAG智能问答系统 - 预置索引构建")
    print("=" * 60)
    
    if build_general_index():
        print("\n🎉 索引构建成功！")
        print("您现在可以启动 run.py 使用预置索引了")
    else:
        print("\n❌ 索引构建失败")
        sys.exit(1)
