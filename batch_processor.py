
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
import pandas as pd
import io
from typing import List, Dict, Any
from datetime import datetime
from export_utils import export_batch_results

def parse_questions_from_text(text: str) -> List[str]:
    lines = text.strip().split('\n')
    questions = []
    for line in lines:
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
            cleaned = line.lstrip('0123456789.-• )').strip()
            if cleaned:
                questions.append(cleaned)
        elif line and len(line) > 5:
            questions.append(line)
    return questions

def parse_questions_from_excel(file) -> List[str]:
    try:
        df = pd.read_excel(file)
        if 'question' in df.columns:
            return df['question'].dropna().tolist()
        elif len(df.columns) > 0:
            first_col = df.columns[0]
            return df[first_col].dropna().tolist()
    except Exception as e:
        raise ValueError(f"无法读取Excel文件: {str(e)}")
    return []

def process_batch_questions(
    questions: List[str],
    chain_func,
    progress_callback=None
) -> List[Dict[str, Any]]:
    results = []
    total = len(questions)

    for i, question in enumerate(questions):
        try:
            result = chain_func(question)
            sources = []

            if isinstance(result, dict):
                answer = result.get('answer', str(result))
                sources = result.get('sources', [])
            else:
                answer = str(result)

            results.append({
                'question': question,
                'answer': answer,
                'sources': sources,
                'status': 'success'
            })
        except Exception as e:
            results.append({
                'question': question,
                'answer': f"处理失败: {str(e)}",
                'sources': [],
                'status': 'error'
            })

        if progress_callback:
            progress_callback((i + 1) / total)

    return results

def render_batch_results(results: List[Dict[str, Any]], show_sources: bool = True):
    success_count = sum(1 for r in results if r['status'] == 'success')
    error_count = len(results) - success_count

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总问题数", len(results))
    with col2:
        st.metric("成功", success_count, delta_color="normal")
    with col3:
        st.metric("失败", error_count, delta_color="inverse")

    for i, result in enumerate(results):
        with st.expander(f"问题 {i+1}: {result['question'][:60]}{'...' if len(result['question']) > 60 else ''}"):
            st.markdown("**问题:**")
            st.info(result['question'])

            st.markdown("**回答:**")
            if result['status'] == 'success':
                st.success(result['answer'])
            else:
                st.error(result['answer'])

            if show_sources and result.get('sources'):
                st.markdown("**引用来源:**")
                for j, source in enumerate(result['sources'][:3], 1):
                    if isinstance(source, tuple) and len(source) >= 2:
                        doc, score = source
                        score_normalized = 1 / (1 + score)
                        st.markdown(f"- 来源{j}: {score_normalized:.1%} 相关度")
                    elif isinstance(source, dict):
                        st.markdown(f"- 来源{j}: {source.get('source', '未知')}")
                    else:
                        st.markdown(f"- 来源{j}: {str(source)[:100]}")

def create_batch_interface(chain_func, vector_store=None):
    st.subheader("📋 批量问答处理")

    tab1, tab2 = st.tabs(["📝 文本输入", "📤 文件导入"])

    with tab1:
        st.markdown("每行输入一个问题，支持以下格式：")
        st.code("""问题1
问题2
问题3
或者:
1. 问题1
2. 问题2
- 问题3""")

        questions_text = st.text_area(
            "输入问题列表",
            height=200,
            placeholder="请输入问题，每行一个..."
        )

        if st.button("🚀 开始批量处理", key="batch_text_process"):
            if questions_text.strip():
                questions = parse_questions_from_text(questions_text)
                if questions:
                    st.info(f"已识别 {len(questions)} 个问题")

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    def progress_callback(progress):
                        progress_bar.progress(progress)
                        status_text.text(f"处理中... {int(progress * 100)}%")

                    results = process_batch_questions(questions, chain_func, progress_callback)

                    status_text.text("处理完成！")
                    progress_bar.progress(1.0)

                    st.markdown("---")
                    st.subheader("📊 处理结果")
                    render_batch_results(results)

                    if st.button("💾 导出结果"):
                        output_path = export_batch_results(results)
                        st.success(f"✅ 结果已导出到: {output_path}")
                else:
                    st.warning("未能识别有效问题，请检查输入格式")
            else:
                st.warning("请输入问题列表")

    with tab2:
        st.markdown("支持 Excel 文件 (.xlsx)，问题应在第一列或名为 'question' 的列")

        uploaded_file = st.file_uploader(
            "选择问题文件",
            type=['xlsx'],
            key="batch_file_uploader"
        )

        if uploaded_file:
            try:
                questions = parse_questions_from_excel(uploaded_file)
                st.info(f"从文件中识别出 {len(questions)} 个问题")

                if st.button("🚀 开始批量处理", key="batch_file_process"):
                    if questions:
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        def progress_callback(progress):
                            progress_bar.progress(progress)
                            status_text.text(f"处理中... {int(progress * 100)}%")

                        results = process_batch_questions(questions, chain_func, progress_callback)

                        status_text.text("处理完成！")
                        progress_bar.progress(1.0)

                        st.markdown("---")
                        st.subheader("📊 处理结果")
                        render_batch_results(results)

                        if st.button("💾 导出结果", key="export_batch_file"):
                            output_path = export_batch_results(results)
                            st.success(f"✅ 结果已导出到: {output_path}")
            except Exception as e:
                st.error(f"读取文件失败: {str(e)}")

def batch_ask_simple(questions: List[str], vector_store, temperature=0.7, top_k=5):
    from rag import llm_chain

    results = []
    for question in questions:
        chain = llm_chain(
            vector_store,
            temperature=temperature,
            top_k=top_k,
            return_sources=False
        )
        answer = chain.invoke(question)
        results.append({
            'question': question,
            'answer': answer,
            'sources': []
        })
    return results
