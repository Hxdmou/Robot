# RAG 智能问答系统 Dockerfile

# 使用 Python 3.10 基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p chat_histories knowledge_bases logs faiss_index

# 暴露端口
EXPOSE 7861 7869 7870 7871 7872 7873

# 设置启动命令
CMD ["streamlit", "run", "run.py", "--server.port", "7861", "--server.address", "0.0.0.0"]
