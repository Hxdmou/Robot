
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

import streamlit as st
import os
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
import json
from datetime import datetime

def render_document_card(doc: Document, index: int = 0, show_metadata: bool = True) -> None:
    source = doc.metadata.get('source', '未知来源')
    page = doc.metadata.get('page', 'N/A')

    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #667eea; font-size: 1rem;">
                📄 文档 {index + 1}
            </strong>
            <span style="
                background: #667eea;
                color: white;
                padding: 0.2rem 0.6rem;
                border-radius: 12px;
                font-size: 0.75rem;
            ">页码: {page}</span>
        </div>
        <p style="color: #495057; font-size: 0.9rem; line-height: 1.6; margin: 0;">
            {doc.page_content[:300]}{'...' if len(doc.page_content) > 300 else ''}
        </p>
        <div style="
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid #dee2e6;
            font-size: 0.8rem;
            color: #6c757d;
        ">
            📂 {source}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_document_tree(docs: List[Document], max_display: int = 10) -> None:
    if not docs:
        st.info("暂无文档")
        return

    st.markdown("### 📚 文档列表")

    grouped_docs: Dict[str, List[Document]] = {}
    for doc in docs:
        source = doc.metadata.get('source', '未知来源')
        if source not in grouped_docs:
            grouped_docs[source] = []
        grouped_docs[source].append(doc)

    for source, source_docs in grouped_docs.items():
        with st.expander(f"📁 {os.path.basename(source)} ({len(source_docs)} 个片段)"):
            for i, doc in enumerate(source_docs[:max_display]):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.text_area(
                        f"片段 {i+1}",
                        value=doc.page_content[:500] + ("..." if len(doc.page_content) > 500 else ""),
                        height=100,
                        disabled=True,
                        key=f"doc_{source}_{i}"
                    )
                with col2:
                    page = doc.metadata.get('page', 'N/A')
                    st.metric("页码", page)

                if i < len(source_docs) - 1:
                    st.markdown("---")

            if len(source_docs) > max_display:
                st.info(f"还有 {len(source_docs) - max_display} 个片段未显示")

def render_document_graph(docs: List[Document]) -> None:
    if not docs:
        st.info("暂无文档用于可视化")
        return

    sources = {}
    for doc in docs:
        source = doc.metadata.get('source', '未知来源')
        if source not in sources:
            sources[source] = {
                'count': 0,
                'total_length': 0,
                'pages': set()
            }
        sources[source]['count'] += 1
        sources[source]['total_length'] += len(doc.page_content)
        if 'page' in doc.metadata:
            sources[source]['pages'].add(doc.metadata['page'])

    st.markdown("### 📊 文档统计")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("文档总数", len(docs))

    with col2:
        st.metric("来源数量", len(sources))

    with col3:
        total_length = sum(s['total_length'] for s in sources.values())
        st.metric("总字符数", f"{total_length:,}")

    st.markdown("### 📈 来源分布")

    chart_data = {
        '来源': [os.path.basename(s) for s in sources.keys()],
        '片段数': [s['count'] for s in sources.values()],
        '总字符': [s['total_length'] for s in sources.values()]
    }

    st.bar_chart(chart_data, x='来源', y='片段数')

    with st.expander("📋 详细来源信息"):
        for source, info in sources.items():
            st.markdown(f"""
            * **{os.path.basename(source)}**
              - 片段数: {info['count']}
              - 总字符: {info['total_length']:,}
              - 页码: {', '.join(map(str, sorted(info['pages']))) if info['pages'] else 'N/A'}
            """)

def render_chunk_preview(doc: Document, chunk_size: int = 200) -> str:
    content = doc.page_content
    if len(content) <= chunk_size:
        return content

    sentences = content.split('。')
    preview = []
    char_count = 0

    for sentence in sentences:
        if char_count + len(sentence) > chunk_size:
            break
        preview.append(sentence)
        char_count += len(sentence)

    return '。'.join(preview) + '。'

def create_document_viewer(docs: List[Document]) -> None:
    if not docs:
        st.warning("没有可显示的文档")
        return

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 文档查看器")

    view_mode = st.sidebar.radio(
        "选择视图模式",
        ["卡片视图", "列表视图", "统计视图"],
        help="选择不同的文档可视化方式"
    )

    if view_mode == "卡片视图":
        st.markdown("### 🃏 卡片视图")
        cols = st.columns(2)
        for i, doc in enumerate(docs[:6]):
            with cols[i % 2]:
                render_document_card(doc, i)
        if len(docs) > 6:
            st.info(f"还有 {len(docs) - 6} 个文档未显示")

    elif view_mode == "列表视图":
        render_document_tree(docs, max_display=15)

    elif view_mode == "统计视图":
        render_document_graph(docs)

def create_document_export(docs: List[Document], output_path: str = None) -> str:
    if not docs:
        return None

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"document_export_{timestamp}.json"

    export_data = {
        'export_time': datetime.now().isoformat(),
        'total_documents': len(docs),
        'documents': [
            {
                'content': doc.page_content,
                'metadata': doc.metadata,
                'chunk_preview': render_chunk_preview(doc)
            }
            for doc in docs
        ]
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    return output_path

def get_document_summary(docs: List[Document]) -> Dict[str, Any]:
    if not docs:
        return {
            'total_count': 0,
            'sources': [],
            'total_chars': 0,
            'avg_chunk_size': 0
        }

    sources = {}
    total_chars = 0

    for doc in docs:
        source = doc.metadata.get('source', '未知来源')
        if source not in sources:
            sources[source] = {'count': 0, 'chars': 0}
        sources[source]['count'] += 1
        sources[source]['chars'] += len(doc.page_content)
        total_chars += len(doc.page_content)

    return {
        'total_count': len(docs),
        'sources': list(sources.keys()),
        'source_details': sources,
        'total_chars': total_chars,
        'avg_chunk_size': total_chars // len(docs) if docs else 0
    }