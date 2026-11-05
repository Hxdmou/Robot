# 部署指南

本文档详细介绍如何部署 RAG 智能问答系统，支持三种部署方式：手动部署、Docker 部署和 Kubernetes 部署。

## 一、环境要求

### 基础环境
| 组件 | 版本要求 | 说明 |
|------|----------|------|
| Python | >= 3.10 | 推荐 3.10-3.11 |
| Node.js | 可选 | 如需前端定制开发 |
| 内存 | >= 4GB | 推荐 8GB+ |
| 磁盘 | >= 10GB | 存储知识库和索引 |

### GPU 加速（可选）
| 场景 | 是否需要 GPU | 说明 |
|------|-------------|------|
| 仅检索 | ❌ 否 | FAISS 向量检索使用 CPU 即可 |
| 使用本地 LLM | ✅ 是 | 需要 NVIDIA GPU 和 CUDA |
| 使用远程 API | ❌ 否 | OpenAI/智谱等远程调用无需 GPU |

## 二、手动部署

### 2.1 克隆仓库

```bash
git clone https://github.com/Hxdmou/legal-rag-qa-system.git
cd legal-rag-qa-system
```

### 2.2 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2.3 安装依赖

```bash
# 使用国内镜像加速（推荐）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或官方源
pip install -r requirements.txt
```

### 2.4 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置文件
# 设置 API Key、模型选择等参数
```

### 2.5 构建索引

```bash
# 构建所有系统的预置索引
python build_index.py
```

### 2.6 启动服务

```bash
# 启动通用 RAG 系统（默认端口 7861）
streamlit run run.py --server.port 7861

# 启动法律知识问答系统（端口 7869）
streamlit run legal_qa.py --server.port 7869

# 启动教育学习问答系统（端口 7870）
streamlit run education_qa.py --server.port 7870

# 启动医疗健康问答系统（端口 7871）
streamlit run medical_qa.py --server.port 7871

# 启动金融投资问答系统（端口 7872）
streamlit run finance_qa.py --server.port 7872

# 启动 IT 技术问答系统（端口 7873）
streamlit run tech_qa.py --server.port 7873
```

### 2.7 一键启动（Windows）

```bash
# 运行启动脚本
.\启动RAG系统.bat
```

### 2.8 一键启动（Linux/Mac）

```bash
# 创建启动脚本
chmod +x start.sh
./start.sh
```

## 三、Docker 部署

### 3.1 构建镜像

```bash
# 构建 Docker 镜像
docker build -t rag-qa-system:latest .

# 查看镜像
docker images
```

### 3.2 运行单个容器

```bash
# 运行通用 RAG 系统
docker run -d \
  --name rag-general \
  -p 7861:7861 \
  -v ./chat_histories:/app/chat_histories \
  -v ./knowledge_bases:/app/knowledge_bases \
  -v ./run_faiss_index:/app/run_faiss_index \
  rag-qa-system:latest
```

### 3.3 使用 Docker Compose（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

### 3.4 Docker Compose 配置说明

```yaml
version: '3.8'
services:
  rag-general:
    build: .
    ports:
      - "7861:7861"
    volumes:
      - ./chat_histories:/app/chat_histories
      - ./knowledge_bases:/app/knowledge_bases
      - ./run_faiss_index:/app/run_faiss_index
    restart: unless-stopped
```

## 四、Kubernetes 部署

### 4.1 前提条件

- Kubernetes 集群 >= 1.21
- Helm >= 3.0
- 已配置 Ingress Controller

### 4.2 使用 Helm 部署

```bash
# 创建命名空间
kubectl create namespace rag-qa-system

# 安装 Helm Chart
helm install rag-qa-system . \
  --namespace rag-qa-system \
  --set replicaCount=1 \
  --set service.type=ClusterIP \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=rag.example.com
```

### 4.3 Helm Chart 配置

| 参数 | 描述 | 默认值 |
|------|------|--------|
| replicaCount | Pod 副本数 | 1 |
| image.repository | 镜像仓库 | rag-qa-system |
| image.tag | 镜像标签 | latest |
| service.type | 服务类型 | ClusterIP |
| service.port | 服务端口 | 7861 |
| ingress.enabled | 是否启用 Ingress | false |
| resources.requests.cpu | CPU 请求 | 100m |
| resources.requests.memory | 内存请求 | 512Mi |
| resources.limits.cpu | CPU 限制 | 1 |
| resources.limits.memory | 内存限制 | 2Gi |

### 4.4 持久化配置

```yaml
# 使用 PersistentVolumeClaim
persistence:
  enabled: true
  storageClassName: standard
  accessModes:
    - ReadWriteOnce
  size: 10Gi
```

## 五、配置说明

### 5.1 环境变量

| 变量名 | 必填 | 说明 | 默认值 |
|--------|------|------|--------|
| OPENAI_API_KEY | 否 | OpenAI API Key | - |
| ZHIPU_API_KEY | 否 | 智谱 API Key | - |
| EMBEDDING_MODEL | 否 | Embedding 模型 | text-embedding-3-small |
| LLM_MODEL | 否 | LLM 模型 | gpt-3.5-turbo |
| LOG_LEVEL | 否 | 日志级别 | INFO |
| PORT | 否 | 服务端口 | 7861 |

### 5.2 端口配置

| 服务 | 端口 | 说明 |
|------|------|------|
| 通用 RAG | 7861 | 主入口 |
| 法律问答 | 7869 | 法律领域 |
| 教育问答 | 7870 | 教育领域 |
| 医疗问答 | 7871 | 医疗领域 |
| 金融问答 | 7872 | 金融领域 |
| IT技术问答 | 7873 | 技术领域 |

## 六、安全配置

### 6.1 敏感数据保护

1. **不要提交敏感文件**：确保 `.env`、`chat_histories/` 等在 `.gitignore` 中
2. **使用密钥管理**：生产环境推荐使用 HashiCorp Vault 或 Kubernetes Secret
3. **加密存储**：对话历史可使用 SQLite + SQLCipher 加密

### 6.2 访问控制

```bash
# 设置访问密码（Streamlit 社区版）
streamlit run run.py --server.password your_password
```

### 6.3 HTTPS 配置

```bash
# 使用 nginx 反向代理配置 HTTPS
# 配置示例（nginx.conf）
server {
    listen 443 ssl;
    server_name rag.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:7861;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 七、监控与日志

### 7.1 日志配置

```bash
# 查看容器日志
docker logs rag-general -f

# Kubernetes 日志
kubectl logs -n rag-qa-system <pod-name> -f
```

### 7.2 健康检查

```bash
# 检查服务状态
curl http://localhost:7861/health
```

## 八、故障排除

### 8.1 端口冲突

```bash
# 检查端口占用
netstat -ano | findstr :7861  # Windows
lsof -i :7861                 # Linux/Mac

# 杀死占用进程
taskkill /F /PID <pid>        # Windows
kill -9 <pid>                 # Linux/Mac
```

### 8.2 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 安装开发工具（Linux）
sudo apt-get install gcc g++ python3-dev
```

### 8.3 索引加载失败

```bash
# 删除旧索引，重新构建
rm -rf run_faiss_index
python build_index.py
```

---

**版本**: v2.0  
**最后更新**: 2026年
