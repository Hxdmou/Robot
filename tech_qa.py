import streamlit as st
import os
import tempfile
from rag import (
    load_multiple_documents,
    chunk2vector,
    llm_chain,
    get_embeddings,
    get_llm
)
from langchain_community.vectorstores import FAISS
from config.settings import Config, SYSTEM_CONFIGS
from chat_history import save_chat_history, load_chat_history, delete_chat_history, format_conversation
from logger import get_operation_logger
from export_utils import export_conversation_to_markdown, export_conversation_to_text, create_backup, restore_backup, list_backups
from batch_processor import create_batch_interface

SYSTEM_NAME = "tech"
DEFAULT_INDEX_DIR = "tech_faiss_index"

op_logger = get_operation_logger(SYSTEM_NAME)

def save_uploaded_file(uploaded_file):
    try:
        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"文件保存失败: {str(e)}")
        return None

def load_default_index():
    if os.path.exists(DEFAULT_INDEX_DIR):
        try:
            embeddings = get_embeddings()
            vector_store = FAISS.load_local(DEFAULT_INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
            return vector_store, True, f"成功加载预置索引"
        except Exception as e:
            return None, False, f"加载预置索引失败: {str(e)}"
    return None, False, "未找到预置索引目录"

def save_index_to_disk(vector_store, index_dir=DEFAULT_INDEX_DIR):
    try:
        vector_store.save_local(index_dir)
        return True, f"索引已保存到 {index_dir}"
    except Exception as e:
        return False, f"保存索引失败: {str(e)}"

def process_files(file_paths):
    try:
        docs = load_multiple_documents(file_paths)
        if docs:
            if st.session_state.get("vector_store"):
                new_vector = chunk2vector(docs, get_embeddings())
                st.session_state.vector_store.merge_from(new_vector)
            else:
                st.session_state.vector_store = chunk2vector(docs, get_embeddings())

            st.session_state.current_files.extend([os.path.basename(p) for p in file_paths])
            st.session_state.engine_initialized = True
            st.session_state.index_load_status = "已加载文档"
            op_logger.log_document_loaded(len(file_paths), [os.path.basename(p) for p in file_paths])
            return True, f"成功添加 {len(docs)} 个文档"
        return False, "未找到有效文档内容"
    except Exception as e:
        op_logger.log_error("PROCESS_FILES", str(e))
        return False, f"处理失败: {str(e)}"

def interactive():
    config = SYSTEM_CONFIGS["tech"]

    st.set_page_config(
        page_title=f"{config['name']}",
        page_icon=config["icon"],
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * { font-family: 'Inter', sans-serif; }

        .main-header {
            background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
            padding: 2.5rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(33, 147, 176, 0.3);
        }

        .main-header h1 {
            color: white;
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }

        .main-header p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2rem;
            font-weight: 300;
        }

        .feature-card {
            background: linear-gradient(145deg, #ffffff, #e3f2fd);
            border: 1px solid #bbdefb;
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .feature-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(33, 147, 176, 0.15);
            border-color: #2193b0;
        }

        .feature-title {
            color: #2193b0;
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .disclaimer-card {
            background: linear-gradient(145deg, #fff3e0, #ffe0b2);
            border: 1px solid #ffcc80;
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 1.5rem;
        }

        .disclaimer-card h4 { color: #e65100; margin-bottom: 0.5rem; }

        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .status-ready { background: #e8f5e9; color: #2e7d32; }
        .status-warning { background: #fff3e0; color: #e65100; }
        .status-info { background: #e3f2fd; color: #1976d2; }

        .sidebar-section { margin-bottom: 1.5rem; }
        .sidebar-section h3 {
            font-size: 1rem;
            font-weight: 600;
            color: #555;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e0e0e0;
        }

        .source-card {
            background: #f8f9fa;
            border-left: 3px solid #2193b0;
            padding: 0.75rem;
            margin: 0.5rem 0;
            border-radius: 0 8px 8px 0;
            font-size: 0.85rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="main-header">
            <h1>{config['icon']} {config['name']}</h1>
            <p>{config['description']} | 版本: {Config.VERSION}</p>
        </div>
    """, unsafe_allow_html=True)

    # 法律免责声明：法律/医疗/金融使用红框醒目标注，其他使用黄框
    high_risk_systems = ["legal", "medical", "finance"]
    if SYSTEM_NAME in high_risk_systems:
        disclaimer_color = "#ffebee"
        border_color = "#ef5350"
        title_color = "#c62828"
        disclaimer_title = "⚠️ 重要法律免责声明"
        if SYSTEM_NAME == "legal":
            disclaimer_text = "本系统提供的法律信息仅供参考学习，不构成法律意见或律师服务。遇到具体法律问题请咨询执业律师，切勿仅凭本系统回答做出决策。"
        elif SYSTEM_NAME == "medical":
            disclaimer_text = "本系统提供的医疗健康信息仅供健康知识普及参考，绝对不能替代执业医师的诊断和治疗。身体不适请立即前往正规医院就诊，切勿自行诊断用药。"
        elif SYSTEM_NAME == "finance":
            disclaimer_text = "本系统提供的金融信息仅供知识学习参考，绝对不构成任何投资建议或买卖推荐。投资有风险，入市需谨慎，投资决策请自行判断并承担风险。"
    else:
        disclaimer_color = "#fff9e6"
        border_color = "#ffe082"
        title_color = "#f57c00"
        disclaimer_title = "⚠️ 使用免责声明"
        disclaimer_text = "本系统提供的信息仅供参考学习，不构成任何专业建议。重要决策请咨询相关领域专业人士，开发者不对因使用本系统产生的任何后果承担责任。"
    
    st.markdown(f"""
        <div style="background: {disclaimer_color}; border: 2px solid {border_color}; border-radius: 12px; padding: 1.2rem; margin-bottom: 1.5rem;">
        <h4 style="color: {title_color}; margin-top: 0; margin-bottom: 0.5rem;">{disclaimer_title}</h4>
        <p style="font-size: 0.9rem; color: #333; margin: 0; font-weight: 500;">
        {disclaimer_text}
        </p>
        </div>
    """, unsafe_allow_html=True)

    session_defaults = {
        'messages': [],
        'vector_store': None,
        'current_files': [],
        'engine_initialized': False,
        'show_history': False,
        'show_batch': False,
        'show_backup': False,
        'retrieval_mode': "hybrid",
        'temperature': 0.7,
        'top_k': 5,
        'index_load_status': "未加载"
    }

    for key, default_val in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_val

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 💬 科技问答")

        for message in st.session_state.messages:
            avatar = "👤" if message["role"] == "user" else "💻"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
                if message.get("sources"):
                    with st.expander("📑 查看引用来源"):
                        for i, src in enumerate(message["sources"][:3], 1):
                            if isinstance(src, tuple) and len(src) >= 2:
                                doc, score = src
                                score_pct = 1 / (1 + score)
                                st.markdown(f"""
                                <div class="source-card">
                                <strong>来源 {i}</strong> (相关度: {score_pct:.1%})<br/>
                                {doc.page_content[:200]}...
                                </div>
                                """, unsafe_allow_html=True)

        if prompt := st.chat_input("请输入您的科技问题..."):
            if not st.session_state.engine_initialized:
                st.warning("⚠️ 请先加载知识库或上传文档")
            else:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)

                with st.chat_message("assistant", avatar="💻"):
                    with st.spinner("🤔 正在思考中..."):
                        try:
                            chain = llm_chain(
                                st.session_state.vector_store,
                                temperature=st.session_state.temperature,
                                top_k=st.session_state.top_k,
                                retrieval_mode=st.session_state.retrieval_mode
                            )
                            result = chain.invoke(prompt)

                            if isinstance(result, dict):
                                answer = result.get('answer', str(result))
                                sources = result.get('sources', [])
                            else:
                                answer = str(result)
                                sources = []

                            st.markdown(answer)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": answer,
                                "sources": sources
                            })

                            op_logger.log_query(prompt, len(sources))
                        except Exception as e:
                            error_msg = f"生成回答失败: {str(e)}"
                            st.error(error_msg)
                            op_logger.log_error("QUERY", str(e))

    with col2:
        st.subheader("📋 系统功能")

        features = [
            ("📚 科技知识库", "一键加载预置的科技知识库"),
            ("📁 文档上传", "支持多种格式科技文档上传"),
            ("⚙️ 灵活配置", "可调节温度、Top-K 等参数"),
            ("💾 对话历史", "保存和恢复历史对话"),
            ("📋 批量处理", "批量问答导出"),
            ("� 备份恢复", "数据备份功能"),
            ("📊 引用评分", "显示来源相关度"),
            ("🔒 隐私保护", "所有数据本地处理")
        ]

        for title, desc in features:
            st.markdown(f"""
                <div class="feature-card">
                <div class="feature-title">{title}</div>
                <p style="color: #666; font-size: 0.85rem; margin: 0;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📊 系统状态")

        status_color = "status-warning"
        status_text = "⚠️ 等待初始化"
        if st.session_state.engine_initialized:
            status_color = "status-ready"
            status_text = "✅ 系统就绪"

        st.markdown(f'<span class="status-badge {status_color}">{status_text}</span>', unsafe_allow_html=True)
        st.info(f"📚 已加载文档: {len(st.session_state.current_files)}")
        st.markdown(f'<span class="status-badge status-info">🔄 {st.session_state.index_load_status}</span>', unsafe_allow_html=True)

        st.markdown("---")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💾 保存对话", use_container_width=True):
                if st.session_state.messages:
                    success = save_chat_history(st.session_state.messages, SYSTEM_NAME)
                    if success:
                        st.success("✅ 对话已保存")
                    else:
                        st.error("❌ 保存失败")

        with col_btn2:
            if st.button("📝 历史记录", use_container_width=True):
                st.session_state.show_history = not st.session_state.show_history

        col_btn3, col_btn4 = st.columns(2)
        with col_btn3:
            if st.button("� 批量问答", use_container_width=True):
                st.session_state.show_batch = not st.session_state.show_batch

        with col_btn4:
            if st.button("🔄 重置系统", use_container_width=True):
                st.session_state.vector_store = None
                st.session_state.current_files = []
                st.session_state.engine_initialized = False
                st.session_state.messages = []
                st.session_state.index_load_status = "未加载"
                st.rerun()

        col_btn5, col_btn6 = st.columns(2)
        with col_btn5:
            if st.button("📤 导出对话", use_container_width=True):
                if st.session_state.messages:
                    output_path = export_conversation_to_markdown({
                        'system': config['name'],
                        'timestamp': st.session_state.messages[0]['content'] if st.session_state.messages else 'N/A',
                        'messages': st.session_state.messages
                    })
                    st.success(f"✅ 已导出到: {output_path}")

        with col_btn6:
            if st.button("💾 备份系统", use_container_width=True):
                st.session_state.show_backup = not st.session_state.show_backup

    if st.session_state.show_batch:
        st.markdown("---")
        create_batch_interface(lambda q: llm_chain(
            st.session_state.vector_store,
            temperature=st.session_state.temperature,
            top_k=st.session_state.top_k
        ).invoke(q))

    if st.session_state.show_backup:
        st.markdown("---")
        st.subheader("💾 备份与恢复")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**创建备份**")
            if st.button("� 创建新备份", use_container_width=True):
                with st.spinner("正在创建备份..."):
                    backup_path, manifest = create_backup()
                    st.success(f"✅ 备份已创建: {manifest['backup_name']}")

        with col2:
            st.markdown("**恢复备份**")
            backups = list_backups()
            if backups:
                backup_options = [f"{b['name']} ({b['size']//1024}KB)" for b in backups]
                selected = st.selectbox("选择备份", backup_options)
                if st.button("📥 恢复备份", use_container_width=True):
                    selected_backup = next(b for b in backups if f"{b['name']} ({b['size']//1024}KB)" == selected)
                    success, msg = restore_backup(selected_backup['path'])
                    if success:
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")
            else:
                st.info("暂无备份记录")

    if st.session_state.show_history:
        st.markdown("---")
        st.subheader("📝 历史对话记录")

        history = load_chat_history(SYSTEM_NAME)

        if history:
            history.reverse()

            for conv in history:
                with st.expander(f"📅 {conv['timestamp'][:19]} | {len(conv['messages'])} 条消息"):
                    st.code(format_conversation(conv), language='text')

                    col_save, col_delete = st.columns(2)
                    with col_save:
                        if st.button(f"🔄 恢复 {conv['id'][:8]}", use_container_width=True):
                            st.session_state.messages = conv['messages'].copy()
                            st.session_state.show_history = False
                            st.success("✅ 对话已恢复")
                            st.rerun()
                    with col_delete:
                        if st.button(f"🗑️ 删除 {conv['id'][:8]}", use_container_width=True):
                            delete_chat_history(SYSTEM_NAME, conv['id'])
                            st.success("✅ 已删除")
                            st.rerun()

            if st.button("🗑️ 清空所有历史", type="primary", use_container_width=True):
                delete_chat_history(SYSTEM_NAME)
                st.success("✅ 已清空所有历史")
                st.rerun()
        else:
            st.info("暂无历史对话记录")

    st.markdown("---")
    st.markdown(f"""
        <div style="text-align: center; color: #888; font-size: 0.85rem;">
        <strong>{config['icon']} {config['name']}</strong> | 版本 {Config.VERSION}
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.header("🎛️ 系统控制面板")

        with st.expander("📂 预置知识库", expanded=True):
            st.markdown("""<div class="sidebar-section"><h3>加载预训练索引</h3></div>""", unsafe_allow_html=True)

            if st.button("🔄 加载预置索引", use_container_width=True):
                with st.spinner("正在加载..."):
                    vector_store, success, msg = load_default_index()
                    if success and vector_store:
                        st.session_state.vector_store = vector_store
                        st.session_state.engine_initialized = True
                        st.session_state.current_files = ["预置知识库"]
                        st.session_state.index_load_status = "已加载预置索引"
                        op_logger.log_index_loaded(DEFAULT_INDEX_DIR)
                        st.success(f"✅ {msg}")
                    else:
                        st.warning(f"⚠️ {msg}")

            index_exists = os.path.exists(DEFAULT_INDEX_DIR)
            st.info(f"📂 预置索引: {'已存在' if index_exists else '不存在'}")

            if st.session_state.engine_initialized and st.session_state.vector_store:
                if st.button("💾 保存当前索引", use_container_width=True):
                    success, msg = save_index_to_disk(st.session_state.vector_store)
                    if success:
                        op_logger.log_index_saved(DEFAULT_INDEX_DIR)
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")

        with st.expander("⚙️ 参数设置", expanded=True):
            st.markdown("""<div class="sidebar-section"><h3>模型参数</h3></div>""", unsafe_allow_html=True)

            st.session_state.temperature = st.slider(
                "🌡️ 温度参数",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.temperature,
                step=0.1,
                help="值越高回答越多样化，越低越确定性"
            )

            st.session_state.top_k = st.slider(
                "📊 检索数量",
                min_value=1,
                max_value=10,
                value=st.session_state.top_k,
                step=1,
                help="每次检索返回的文档数量"
            )

            st.session_state.retrieval_mode = st.selectbox(
                "🔍 检索模式",
                ["hybrid", "vector", "bm25"],
                index=["hybrid", "vector", "bm25"].index(st.session_state.retrieval_mode),
                help="hybrid: 混合检索（推荐）"
            )

        with st.expander("📁 文档上传", expanded=True):
            st.markdown("""<div class="sidebar-section"><h3>上传文档</h3></div>""", unsafe_allow_html=True)

            uploaded_files = st.file_uploader(
                "选择文件 (支持 txt/pdf/word/xlsx)",
                type=Config.SUPPORTED_FILE_TYPES,
                accept_multiple_files=True,
                help=f"支持格式: {', '.join(Config.SUPPORTED_FILE_TYPES)}"
            )

            if uploaded_files:
                st.info(f"已选择 {len(uploaded_files)} 个文件")
                for file in uploaded_files:
                    st.write(f"- 📄 {file.name}")

                if st.button("🚀 处理并添加", use_container_width=True):
                    with st.spinner("正在处理文档..."):
                        file_paths = []
                        for uploaded_file in uploaded_files:
                            tmp_path = save_uploaded_file(uploaded_file)
                            if tmp_path:
                                file_paths.append(tmp_path)

                        if file_paths:
                            success, msg = process_files(file_paths)
                            if success:
                                st.success(f"✅ {msg}")
                                for path in file_paths:
                                    try:
                                        os.unlink(path)
                                    except:
                                        pass
                            else:
                                st.error(f"❌ {msg}")

        with st.expander("📂 本地文件", expanded=False):
            st.markdown("""<div class="sidebar-section"><h3>从本地路径加载</h3></div>""", unsafe_allow_html=True)

            local_path = st.text_input(
                "文件或文件夹路径",
                placeholder="C:/Documents/ 或 /home/user/docs/",
                help="支持单个文件或整个文件夹"
            )

            if local_path and st.button("📂 加载本地文件", use_container_width=True):
                with st.spinner("正在加载..."):
                    if os.path.isfile(local_path):
                        success, msg = process_files([local_path])
                    elif os.path.isdir(local_path):
                        file_paths = []
                        for root, _, files in os.walk(local_path):
                            for file in files:
                                ext = os.path.splitext(file)[1].lower()[1:]
                                if ext in Config.SUPPORTED_FILE_TYPES:
                                    file_paths.append(os.path.join(root, file))
                        if file_paths:
                            success, msg = process_files(file_paths)
                        else:
                            success, msg = False, "文件夹中没有支持的文件"
                    else:
                        success, msg = False, "路径不存在"

                    if success:
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")

if __name__ == "__main__":
    interactive()