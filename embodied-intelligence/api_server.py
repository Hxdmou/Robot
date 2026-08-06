
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

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)
CORS(app)

API_MODE = os.getenv("API_MODE", "false").lower() == "true"

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'RAG QA System API',
        'version': '3.0.0'
    })

@app.route('/api/ask', methods=['POST'])
def ask_question():
    if not API_MODE:
        return jsonify({'error': 'API mode is disabled'}), 403

    data = request.get_json()

    if not data or 'question' not in data:
        return jsonify({'error': 'Missing question parameter'}), 400

    question = data['question']
    system = data.get('system', 'general')
    temperature = data.get('temperature', 0.7)
    top_k = data.get('top_k', 5)

    try:
        if system == 'legal':
            from legal_qa import load_default_index, llm_chain
            vector_store, success, _ = load_default_index()
        elif system == 'medical':
            from medical_qa import load_default_index, llm_chain
            vector_store, success, _ = load_default_index()
        elif system == 'finance':
            from finance_qa import load_default_index, llm_chain
            vector_store, success, _ = load_default_index()
        elif system == 'education':
            from education_qa import load_default_index, llm_chain
            vector_store, success, _ = load_default_index()
        elif system == 'tech':
            from tech_qa import load_default_index, llm_chain
            vector_store, success, _ = load_default_index()
        else:
            from rag import chunk2vector, llm_chain
            from rag import get_embeddings
            from rag import load_multiple_documents

            index_path = "faiss_index"
            if os.path.exists(index_path):
                from langchain_community.vectorstores import FAISS
                from rag import get_embeddings
                vector_store = FAISS.load_local(index_path, get_embeddings(), allow_dangerous_deserialization=True)
            else:
                return jsonify({'error': 'Knowledge base not initialized'}), 400

        if not vector_store:
            return jsonify({'error': 'Failed to load knowledge base'}), 400

        from rag import llm_chain
        chain = llm_chain(vector_store, temperature=temperature, top_k=top_k)
        answer = chain.invoke(question)

        return jsonify({
            'question': question,
            'answer': answer,
            'system': system,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/systems', methods=['GET'])
def list_systems():
    systems = [
        {'id': 'general', 'name': '通用RAG系统', 'port': 7861},
        {'id': 'legal', 'name': '法律知识问答', 'port': 7869},
        {'id': 'medical', 'name': '医疗健康问答', 'port': 7871},
        {'id': 'finance', 'name': '金融投资问答', 'port': 7872},
        {'id': 'education', 'name': '教育学习问答', 'port': 7870},
        {'id': 'tech', 'name': 'IT技术问答', 'port': 7873},
    ]
    return jsonify({'systems': systems})

@app.route('/api/index/status', methods=['GET'])
def index_status():
    system = request.args.get('system', 'general')

    index_map = {
        'general': 'faiss_index',
        'legal': 'legal_faiss_index',
        'medical': 'medical_faiss_index',
        'finance': 'finance_faiss_index',
        'education': 'education_faiss_index',
        'tech': 'tech_faiss_index',
    }

    index_path = index_map.get(system, 'faiss_index')
    exists = os.path.exists(index_path)

    return jsonify({
        'system': system,
        'index_path': index_path,
        'exists': exists,
        'status': 'ready' if exists else 'not_initialized'
    })

def run_api_server(host='0.0.0.0', port=5000):
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    run_api_server()
