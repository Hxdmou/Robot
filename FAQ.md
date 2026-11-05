# 常见问题

## 🔧 安装与运行

### Q: 如何安装依赖？
**A:** 使用 pip 安装 requirements.txt 中的依赖：
```bash
pip install -r requirements.txt
```

### Q: 系统启动失败怎么办？
**A:** 请检查：
1. Python 版本是否为 3.10+
2. 依赖是否安装完整
3. 端口是否被占用（尝试更换端口）
4. 是否有足够的内存和磁盘空间
5. 环境变量配置是否正确

### Q: 如何启动单个系统？
**A:** 使用以下命令启动：
```bash
# 通用RAG系统
streamlit run run.py --server.port 7861

# 法律知识系统
streamlit run legal_qa.py --server.port 7869

# 教育学习系统
streamlit run education_qa.py --server.port 7870

# 医疗健康系统
streamlit run medical_qa.py --server.port 7871

# 金融投资系统
streamlit run finance_qa.py --server.port 7872

# IT技术系统
streamlit run tech_qa.py --server.port 7873
```

### Q: 如何配置环境变量？
**A:** 复制 `.env.example` 文件为 `.env`，然后根据实际情况修改配置：
```bash
cp .env.example .env
```
编辑 `.env` 文件，设置 API Key 和其他参数。

## 📁 文档处理

### Q: 支持哪些文档格式？
**A:** 支持以下文档格式：
- **PDF**: `.pdf`
- **Word**: `.docx`, `.doc`
- **Excel**: `.xlsx`, `.xls`
- **PowerPoint**: `.pptx`, `.ppt`
- **文本**: `.txt`, `.md`, `.json`, `.csv`
- **HTML**: `.html`, `.htm`

### Q: 扫描件 PDF 能处理吗？
**A:** 目前不支持直接处理扫描件（无文字层的 PDF）。如需处理扫描件，需要额外配置 OCR 工具（如 PaddleOCR）。

### Q: 文档上传失败怎么办？
**A:** 请检查：
1. 文件大小是否超过限制（默认 50MB）
2. 文件格式是否支持
3. 文件是否损坏或加密
4. 是否有足够的磁盘空间

### Q: 如何添加自定义知识库？
**A:** 将文档放入 `knowledge_bases/` 目录，然后运行 `build_index.py` 构建索引：
```bash
python build_index.py
```

## 🤖 问答功能

### Q: 为什么回答不准确？
**A:** 可能的原因：
1. 知识库中没有相关内容
2. 问题表述不够清晰或过于宽泛
3. 检索参数需要优化
4. 文档内容不够详细

### Q: 如何提高问答准确性？
**A:**
1. 添加更多相关文档到知识库
2. 确保问题描述清晰明确
3. 使用更具体的关键词
4. 优化检索参数（如调整 top_k）
5. 定期更新知识库内容

### Q: 如何切换不同的 Embedding 模型？
**A:** 在 `.env` 文件中设置 `EMBEDDING_MODEL` 参数：
```bash
# 使用 OpenAI Embedding
EMBEDDING_MODEL=text-embedding-3-small

# 使用开源模型
EMBEDDING_MODEL=all-MiniLM-L6-v2

# 使用中文模型
EMBEDDING_MODEL=m3e-base
```

### Q: 支持多轮对话吗？
**A:** 是的，系统支持多轮对话，会保持对话上下文。

### Q: 能否完全离线运行？
**A:** 可以，但需要满足以下条件：
1. 使用本地 LLM（如 Ollama + llama3）
2. 使用本地 Embedding 模型（如 sentence-transformers）
3. 预先构建好向量索引

## ⚙️ 模型配置

### Q: 支持哪些 LLM 模型？
**A:** 支持以下模型：
- **OpenAI**: gpt-3.5-turbo, gpt-4, gpt-4-turbo
- **智谱**: glm-3-turbo, glm-4
- **本地模型**: 通过 Ollama 支持 llama3, qwen, baichuan 等

### Q: 如何配置本地 LLM？
**A:**
1. 安装 Ollama: https://ollama.com/
2. 拉取模型: `ollama pull llama3`
3. 在 `.env` 中配置：
```bash
LLM_MODEL=llama3
OPENAI_API_BASE=http://localhost:11434/v1
```

## 💾 数据存储

### Q: 对话记录保存在哪里？
**A:** 对话记录保存在本地 `chat_histories/` 目录下，每个系统有独立的 JSON 文件。

### Q: 如何清理历史记录？
**A:** 在系统页面点击"清空对话"或"清空所有历史"按钮，或直接删除 `chat_histories/` 目录：
```bash
rm -rf ./chat_histories/
```

### Q: 数据会上传到云端吗？
**A:** 不会，所有数据仅在本地处理和存储，保护用户隐私。

### Q: 如何导出对话记录？
**A:** 对话记录以 JSON 格式存储，可以直接复制 `chat_histories/` 目录下的文件。

## 🚀 部署与定制

### Q: 如何进行私有化部署？
**A:** 请联系我们获取商业部署方案：business@rag-qa-system.com

### Q: 支持定制开发吗？
**A:** 是的，我们提供垂直领域定制服务，包括法律、医疗、金融、教育等行业。

### Q: 如何集成到现有系统？
**A:** 提供完整的 API 接口支持，可以与现有系统无缝集成。

### Q: 是否支持 Docker 部署？
**A:** 当前版本暂未提供 Docker 配置，如有需求请联系我们。

## 🔒 安全与隐私

### Q: 数据安全如何保障？
**A:**
1. 端到端加密传输
2. 数据脱敏处理
3. 完善的权限管理体系
4. 本地部署，数据自主可控

### Q: 是否会收集用户数据？
**A:** 不会主动收集用户个人信息，所有数据仅本地存储。

### Q: 如何安全上传包含敏感信息的文档？
**A:**
1. 上传前进行数据脱敏
2. 移除或替换姓名、身份证号、手机号等敏感信息
3. 参考 `SECURITY.md` 中的安全指南

## 📊 性能与扩展

### Q: 系统支持多少并发用户？
**A:** Streamlit 本质是单线程，建议在生产环境中配合 Nginx 负载均衡使用，或使用 FastAPI + 前端分离架构。

### Q: 如何处理大规模知识库？
**A:**
1. 对于大规模动态知识库，建议切换到 Chroma 或 Qdrant
2. 使用增量更新策略，避免每次重建索引
3. 考虑使用分布式向量数据库

## 🔧 常见问题排查

### Q: 出现中文乱码怎么办？
**A:** 请尝试以下解决方案：
1. **设置系统编码**：在启动脚本中添加 `chcp 65001`（Windows）或 `export LANG=zh_CN.UTF-8`（Linux/Mac）
2. **检查文件编码**：确保上传的文档使用 UTF-8 编码
3. **更新依赖版本**：升级 streamlit、langchain 等依赖到最新版本
4. **设置 Python 编码**：在代码开头添加 `# -*- coding: utf-8 -*-`

### Q: 依赖安装失败怎么办？
**A:** 请尝试以下解决方案：
1. **升级 pip**：`pip install --upgrade pip`
2. **使用国内镜像**：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
3. **手动安装失败的包**：单独安装失败的依赖，查看具体错误信息
4. **检查 Python 版本**：确保使用 Python 3.10+ 版本
5. **安装系统依赖**（Linux）：`sudo apt-get install gcc g++ python3-dev`

### Q: 端口冲突怎么办？
**A:** 请尝试以下解决方案：
1. **更换端口启动**：`streamlit run run.py --server.port 8080`
2. **检查端口占用**（Windows）：`netstat -ano | findstr :7861`，然后 `taskkill /F /PID <进程ID>`
3. **检查端口占用**（Linux/Mac）：`lsof -i :7861`，然后 `kill -9 <进程ID>`
4. **使用启动脚本**：运行 `启动RAG系统.bat`（Windows）或 `start.sh`（Linux/Mac），脚本会自动检测可用端口

### Q: 文档上传后无法检索怎么办？
**A:** 请尝试以下解决方案：
1. **检查文档格式**：确保上传的是支持的格式（PDF、DOCX、TXT等）
2. **检查文档内容**：扫描件或加密文档可能无法解析
3. **重建索引**：删除 `faiss_index` 目录，重新上传文档
4. **检查文件大小**：确保文件不超过 50MB 限制

### Q: 启动时提示缺少模块怎么办？
**A:**
1. 确保已安装所有依赖：`pip install -r requirements.txt`
2. 如果提示缺少特定模块，单独安装：`pip install <模块名>`
3. 检查 Python 环境是否正确

## 📞 技术支持

### Q: 遇到问题如何获取帮助？
**A:**
1. 查看文档和 FAQ
2. 在 GitHub Issues 中提交问题
3. 发送邮件联系技术支持：business@rag-qa-system.com

### Q: 是否提供商业技术支持？
**A:** 是的，我们提供 7×24 小时商业技术支持服务。

---

如果您没有找到答案，请随时联系我们！
