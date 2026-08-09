#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
构建10套RAG系统的预置使用说明索引
每个索引包含：系统使用说明 + 对应领域法律免责声明
"""
import os
import sys

# 设置HuggingFace国内镜像（魔搭社区），解决连接超时问题
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from rag import chunk2vector, get_embeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from config.settings import SYSTEM_CONFIGS

# 各系统专属法律免责声明和使用说明
SYSTEM_DOCS = {
    "general": {
        "index_dir": "general_faiss_index",
        "docs": [
            {
                "title": "通用RAG智能问答系统使用说明",
                "content": """通用RAG智能问答系统使用说明：
1. 本系统支持TXT/PDF/DOCX/XLSX/HTML等多种格式文档上传
2. 支持多轮对话、流式输出、对话历史保存
3. 可调节温度参数（0-1）控制回答创造性，调节Top-K参数控制检索文档数量
4. 支持混合检索（BM25关键词+FAISS向量）、纯向量检索、纯BM25检索三种模式
5. 所有数据本地处理，保护隐私安全
6. 本系统仅供学习和参考使用，回答不构成专业建议"""
            },
            {
                "title": "通用系统免责声明",
                "content": """【通用免责声明】
本系统基于人工智能大模型提供问答服务，所有回答仅供参考学习使用，不构成任何专业建议、决策依据或正式意见。
用户在做出任何实际决策前，请咨询相关领域专业人士，并自行核实信息的准确性和适用性。
开发者不对因使用本系统回答而产生的任何直接或间接损失承担责任。"""
            }
        ]
    },
    "legal": {
        "index_dir": "legal_faiss_index",
        "docs": [
            {
                "title": "法律知识问答系统使用说明",
                "content": """法律知识问答系统使用说明：
1. 本系统提供法律条文检索、法律问题咨询、合同条款解读、案例分析参考等功能
2. 支持上传法律文书、合同、法规文件进行分析问答
3. 回答中会引用相关法律条文和来源，方便用户查阅原文
4. 本系统适用于法律学习、普法教育、初步法律咨询参考"""
            },
            {
                "title": "法律系统重要免责声明",
                "content": """【法律领域重要免责声明】
1. 本系统提供的所有法律相关信息仅供参考学习，不构成法律意见、法律建议或律师服务。
2. 本系统回答不能替代执业律师的专业法律服务，遇到具体法律问题请咨询正规律师事务所执业律师。
3. 本系统不对回答内容的准确性、完整性、时效性作任何保证。法律法规可能随时更新，司法实践存在地区差异。
4. 涉及诉讼、仲裁、合同签署等重要法律事务，请务必委托专业律师处理，切勿仅依据本系统回答做出决策。
5. 使用本系统即表示您已阅读并同意本免责声明，开发者不对因使用本系统产生的任何法律后果承担责任。"""
            }
        ]
    },
    "education": {
        "index_dir": "education_faiss_index",
        "docs": [
            {
                "title": "教育知识问答系统使用说明",
                "content": """教育知识问答系统使用说明：
1. 本系统提供教材知识点问答、学习辅导、题目解析、知识拓展等功能
2. 支持上传教材、课件、笔记、题库等文档进行问答
3. 适用于K12教育、高等教育、职业教育等各阶段学习辅导
4. 支持公式显示、多轮问答、学习进度跟踪"""
            },
            {
                "title": "教育系统免责声明",
                "content": """【教育领域免责声明】
本系统提供的教育相关内容仅供学习参考，不构成教学标准或考试标准答案。
学生应在教师指导下学习，作业和考试请独立完成，本系统回答仅供思路参考。
开发者不对因使用本系统内容导致的学习成绩、考试结果承担任何责任。"""
            }
        ]
    },
    "medical": {
        "index_dir": "medical_faiss_index",
        "docs": [
            {
                "title": "医疗健康问答系统使用说明",
                "content": """医疗健康问答系统使用说明：
1. 本系统提供医学知识普及、健康咨询、用药信息参考、疾病知识问答等功能
2. 支持上传医学文献、病历、药品说明书等进行问答分析
3. 适用于健康知识学习、日常健康咨询、就医前信息参考"""
            },
            {
                "title": "医疗系统重要免责声明",
                "content": """【医疗领域重要免责声明】
1. 本系统提供的所有医疗健康信息仅供健康知识普及和参考，绝对不能替代执业医师的专业诊断和治疗建议。
2. 本系统不是医疗机构，不提供医疗诊断服务，不能开具处方。
3. 身体不适请立即前往正规医院就诊，切勿自行诊断用药，以免延误病情。
4. 涉及用药、治疗方案选择、急诊情况请务必遵医嘱，本系统回答不能作为诊疗依据。
5. 使用本系统即表示您已阅读并同意本免责声明，开发者不对因使用本系统导致的任何健康问题承担责任。"""
            }
        ]
    },
    "finance": {
        "index_dir": "finance_faiss_index",
        "docs": [
            {
                "title": "金融知识问答系统使用说明",
                "content": """金融知识问答系统使用说明：
1. 本系统提供金融知识普及、理财产品介绍、投资知识问答、合规查询参考等功能
2. 支持上传金融研报、产品说明书、法规文件等进行问答
3. 适用于金融知识学习、投资者教育、理财信息参考"""
            },
            {
                "title": "金融系统重要免责声明",
                "content": """【金融领域重要免责声明】
1. 本系统提供的所有金融相关信息仅供知识学习和参考，绝对不构成任何投资建议、理财建议、买卖推荐。
2. 投资有风险，入市需谨慎。任何投资决策请您自行判断、自行承担风险。
3. 过往业绩不代表未来表现，金融市场存在不确定性，本系统不对任何投资盈亏承担责任。
4. 购买金融产品请仔细阅读产品说明书和风险揭示书，选择适合自己风险承受能力的产品。
5. 使用本系统即表示您已阅读并同意本免责声明，开发者不对因使用本系统导致的任何投资损失承担责任。"""
            }
        ]
    },
    "tech": {
        "index_dir": "tech_faiss_index",
        "docs": [
            {
                "title": "IT技术问答系统使用说明",
                "content": """IT技术问答系统使用说明：
1. 本系统提供编程技术问答、代码生成参考、API文档查询、技术方案讨论、报错问题排查等功能
2. 支持上传技术文档、代码文件、API手册等进行问答
3. 适用于程序员日常开发、技术学习、问题排查参考
4. 代码建议仅供参考，生产环境使用请务必自行测试验证"""
            },
            {
                "title": "技术系统免责声明",
                "content": """【IT技术免责声明】
本系统提供的代码示例、技术方案和问题排查建议仅供参考学习。
生产环境使用前请务必进行充分测试和安全审计，开发者不对因直接使用本系统代码导致的任何系统故障、数据损失、安全问题承担责任。"""
            }
        ]
    },
    "e_commerce": {
        "index_dir": "e_commerce_faiss_index",
        "docs": [
            {
                "title": "电商零售问答系统使用说明",
                "content": """电商零售问答系统使用说明：
1. 本系统提供商品咨询、运营策略参考、客服话术参考、营销技巧建议、售后政策解答等功能
2. 支持上传商品资料、运营手册、客服规范等文档进行问答
3. 适用于电商运营、客服人员日常工作参考"""
            },
            {
                "title": "电商系统免责声明",
                "content": """【电商领域免责声明】
本系统提供的运营建议、营销方案、客服话术仅供参考学习。
实际经营请遵守国家相关法律法规和平台规则，开发者不对因使用本系统建议产生的经营风险、合规问题承担责任。"""
            }
        ]
    },
    "government": {
        "index_dir": "government_faiss_index",
        "docs": [
            {
                "title": "政务服务问答系统使用说明",
                "content": """政务服务问答系统使用说明：
1. 本系统提供政策解读、办事流程咨询、常见问题解答、表格填写说明等功能
2. 支持上传政策文件、办事指南、通知公告等进行问答
3. 适用于政务服务咨询、政策学习了解、办事前参考"""
            },
            {
                "title": "政务系统免责声明",
                "content": """【政务领域免责声明】
本系统提供的政策解读和办事指南仅供参考，不代表官方意见。
政策可能随时更新，具体办理要求请以当地政府部门官方发布为准，办理业务请前往官方政务服务大厅或官方线上平台。
开发者不对因本系统信息与官方信息不一致导致的问题承担责任。"""
            }
        ]
    },
    "hr": {
        "index_dir": "hr_faiss_index",
        "docs": [
            {
                "title": "人力资源问答系统使用说明",
                "content": """人力资源问答系统使用说明：
1. 本系统提供招聘攻略、培训方案参考、绩效考核建议、劳动合同法规咨询、员工管理参考等功能
2. 支持上传员工手册、公司制度、劳动法规、招聘资料等进行问答
3. 适用于HR日常工作参考、劳动法规学习
4. 支持批量问答、对话导出、数据备份"""
            },
            {
                "title": "人力资源系统免责声明",
                "content": """【人力资源领域免责声明】
本系统提供的人力资源管理建议和劳动法规解读仅供参考学习，不构成法律意见或人力资源管理咨询建议。
涉及劳动纠纷、合同签署、员工辞退等重要人事决策，请咨询专业劳动法律师或人力资源顾问。
开发者不对因使用本系统建议导致的劳动纠纷、管理问题承担责任。"""
            }
        ]
    },
    "academic": {
        "index_dir": "academic_faiss_index",
        "docs": [
            {
                "title": "科研学术问答系统使用说明",
                "content": """科研学术问答系统使用说明：
1. 本系统提供文献检索参考、论文写作指导、研究方法讨论、学术规范咨询等功能
2. 支持上传论文、文献、研究报告等进行问答分析
3. 适用于科研人员、学生学术写作和研究学习参考"""
            },
            {
                "title": "学术系统免责声明",
                "content": """【科研学术免责声明】
本系统提供的学术内容仅供学习参考，请严格遵守学术道德规范，严禁抄袭、剽窃等学术不端行为。
论文写作请正确引用参考文献，本系统产生的内容不能直接作为学术成果提交。
开发者不对因使用本系统导致的学术不端问题承担责任。"""
            }
        ]
    }
}

def build_index(system_key, system_info):
    """构建单个系统的预置索引"""
    index_dir = system_info["index_dir"]
    docs_info = system_info["docs"]
    
    try:
        # 先删除旧索引（如果存在）
        if os.path.exists(index_dir):
            import shutil
            shutil.rmtree(index_dir)
        
        # 构建Document列表
        documents = []
        for doc_info in docs_info:
            doc = Document(
                page_content=doc_info["content"],
                metadata={"source": doc_info["title"], "system": system_key}
            )
            documents.append(doc)
        
        # 生成向量并保存
        print(f"  正在向量化 {len(documents)} 个文档...")
        embeddings = get_embeddings()
        vector_store = chunk2vector(documents, embeddings)
        vector_store.save_local(index_dir)
        
        print(f"  ✅ 成功构建索引: {index_dir}")
        return True
    except Exception as e:
        print(f"  ❌ 构建索引失败: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("  开始构建10套RAG系统的预置使用说明索引")
    print("=" * 60)
    print()
    
    success_count = 0
    fail_count = 0
    
    for system_key, system_info in SYSTEM_DOCS.items():
        system_name = SYSTEM_CONFIGS[system_key]["name"]
        print(f"[{success_count + fail_count + 1}/10] 构建 {system_name} 索引...")
        if build_index(system_key, system_info):
            success_count += 1
        else:
            fail_count += 1
        print()
    
    print("=" * 60)
    print(f"  索引构建完成！成功: {success_count}, 失败: {fail_count}")
    print("=" * 60)
    
    # 验证索引存在
    print("\n验证索引目录:")
    for system_key, system_info in SYSTEM_DOCS.items():
        exists = os.path.exists(system_info["index_dir"])
        files = os.listdir(system_info["index_dir"]) if exists else []
        status = "✅" if exists and len(files) >= 2 else "❌"
        print(f"  {status} {system_info['index_dir']} ({len(files)} 个文件)")

if __name__ == "__main__":
    main()
