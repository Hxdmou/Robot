#!/usr/bin/env python3
"""测试所有系统的预置索引加载功能"""
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
from dotenv import load_dotenv
load_dotenv(override=True)

def test_index_load(system_name, index_dir, system_file):
    """测试单个系统的预置索引加载"""
    print(f"\n{'='*60}")
    print(f"测试 {system_name} 系统")
    print('='*60)

    if not os.path.exists(index_dir):
        print(f"❌ 索引目录不存在: {index_dir}")
        return False

    print(f"✅ 索引目录存在: {index_dir}")

    required_files = ['index.faiss', 'index.pkl']
    missing_files = []
    for f in required_files:
        if not os.path.exists(os.path.join(index_dir, f)):
            missing_files.append(f)

    if missing_files:
        print(f"❌ 缺少索引文件: {missing_files}")
        return False

    print(f"✅ 索引文件完整")

    try:
        from langchain_community.vectorstores import FAISS
        from rag import get_embeddings

        embeddings = get_embeddings()
        vector_store = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

        doc_count = len(vector_store.docstore._dict)
        print(f"✅ 索引加载成功，共 {doc_count} 个文档")

        return True
    except Exception as e:
        print(f"❌ 索引加载失败: {str(e)}")
        return False

def main():
    systems = [
        ("通用RAG智能问答系统", "general_faiss_index", "run.py"),
        ("法律知识问答系统", "legal_faiss_index", "legal_qa.py"),
        ("医疗健康问答系统", "medical_faiss_index", "medical_qa.py"),
        ("教育学习问答系统", "education_faiss_index", "education_qa.py"),
        ("金融投资问答系统", "finance_faiss_index", "finance_qa.py"),
        ("IT技术问答系统", "tech_faiss_index", "tech_qa.py"),
        ("电商零售问答系统", "e_commerce_faiss_index", "e_commerce_qa.py"),
        ("政务服务问答系统", "government_faiss_index", "government_qa.py"),
        ("人力资源问答系统", "hr_faiss_index", "hr_qa.py"),
        ("科研学术问答系统", "academic_faiss_index", "academic_qa.py"),
    ]

    print("="*60)
    print("测试所有系统的预置索引加载功能")
    print("="*60)

    results = []
    for name, index_dir, _ in systems:
        success = test_index_load(name, index_dir, _)
        results.append((name, success))

    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    success_count = 0
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status}: {name}")
        if success:
            success_count += 1

    print(f"\n通过: {success_count}/{len(results)}")

    if success_count == len(results):
        print("\n🎉 所有系统的预置索引加载正常！")
        return 0
    else:
        print(f"\n⚠️ 有 {len(results) - success_count} 个系统测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
