
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

import re

files_to_update = {
    'government_qa.py': {
        'SYSTEM_NAME': 'government',
        'DEFAULT_INDEX_DIR': 'government_faiss_index',
        'title': '🏛️ 政务服务智能问答系统',
        'sidebar': '🏛️ 政务服务问答系统',
        'header': '🏛️ 政务服务智能问答系统',
        'desc': '基于RAG技术的政务服务知识问答平台'
    },
    'hr_qa.py': {
        'SYSTEM_NAME': 'hr',
        'DEFAULT_INDEX_DIR': 'hr_faiss_index',
        'title': '👔 人力资源智能问答系统',
        'sidebar': '👔 人力资源问答系统',
        'header': '👔 人力资源智能问答系统',
        'desc': '基于RAG技术的人力资源知识问答平台'
    },
    'academic_qa.py': {
        'SYSTEM_NAME': 'academic',
        'DEFAULT_INDEX_DIR': 'academic_faiss_index',
        'title': '📚 科研学术智能问答系统',
        'sidebar': '📚 科研学术问答系统',
        'header': '📚 科研学术智能问答系统',
        'desc': '基于RAG技术的科研学术知识问答平台'
    }
}

for filename, replacements in files_to_update.items():
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('SYSTEM_NAME = "e-commerce"', f'SYSTEM_NAME = "{replacements["SYSTEM_NAME"]}"')
    content = content.replace('DEFAULT_INDEX_DIR = "e_commerce_faiss_index"', f'DEFAULT_INDEX_DIR = "{replacements["DEFAULT_INDEX_DIR"]}"')
    content = content.replace('page_title="🛒 电商零售智能问答系统"', f'page_title="{replacements["title"]}"')
    content = content.replace('st.markdown("## 🛒 电商零售问答系统")', f'st.markdown("## {replacements["sidebar"]}")')
    content = content.replace('<h1 class="main-header">🛒 电商零售智能问答系统</h1>', f'<h1 class="main-header">{replacements["header"]}</h1>')
    content = content.replace('基于RAG技术的电商零售知识问答平台', replacements['desc'])

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'{filename} 已更新')
