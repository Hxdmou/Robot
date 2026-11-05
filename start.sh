#!/bin/bash
set -e

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    RAG智能知识问答系统 - 企业级一键启动${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "版本: 2.0.0"
echo -e "模式: 企业级部署模式"
echo ""

# ========================================
# 环境检查
# ========================================
echo -e "${YELLOW}🧪 正在检查运行环境...${NC}"

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到 Python3，请先安装 Python 3.10+${NC}"
    echo -e "   下载地址: https://www.python.org/downloads/"
    exit 1
fi

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✅ Python 版本: ${PYTHON_VERSION}${NC}"

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${GREEN}✅ 当前在虚拟环境中运行${NC}"
else
    echo -e "${YELLOW}⚠️ 警告: 建议在虚拟环境中运行，避免依赖冲突${NC}"
fi

# 检查关键依赖是否安装
echo -e "${YELLOW}📦 检查核心依赖...${NC}"
if python3 -c "import streamlit; import langchain; import faiss" &> /dev/null; then
    echo -e "${GREEN}✅ 核心依赖已安装${NC}"
else
    echo -e "${YELLOW}⚠️ 警告: 部分依赖缺失，正在尝试安装...${NC}"
    pip3 install streamlit langchain faiss-cpu -i https://pypi.tuna.tsinghua.edu.cn/simple
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 依赖安装失败，请手动安装 requirements.txt${NC}"
        exit 1
    fi
fi

# 检查端口是否被占用
echo -e "${YELLOW}🔍 检查端口占用情况...${NC}"
PORTS="7861 7869 7870 7871 7872 7873"
PORT_CONFLICT=""
for PORT in $PORTS; do
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        PORT_CONFLICT="$PORT_CONFLICT $PORT"
    fi
done

if [ -n "$PORT_CONFLICT" ]; then
    echo -e "${YELLOW}⚠️ 警告: 以下端口已被占用:$PORT_CONFLICT${NC}"
    echo -e "   请关闭占用端口的程序，或修改启动端口"
fi

echo ""
echo -e "${BLUE}========================================${NC}"

# ========================================
# 启动服务
# ========================================
echo -e "${YELLOW}🚀 正在启动所有服务...${NC}"
echo ""

# 创建日志目录
mkdir -p logs

# 启动通用RAG智能问答系统
echo -e "[1/6] 启动 📚 通用RAG智能问答系统..."
nohup streamlit run run.py --server.port 7861 > logs/rag-general.log 2>&1 &
echo -e "${GREEN}✅ 已启动${NC}"
sleep 3

# 启动法律知识问答系统
echo -e "[2/6] 启动 ⚖️ 法律知识问答系统..."
nohup streamlit run legal_qa.py --server.port 7869 > logs/rag-legal.log 2>&1 &
echo -e "${GREEN}✅ 已启动${NC}"
sleep 3

# 启动教育知识问答系统
echo -e "[3/6] 启动 🎓 教育知识问答系统..."
nohup streamlit run education_qa.py --server.port 7870 > logs/rag-education.log 2>&1 &
echo -e "${GREEN}✅ 已启动${NC}"
sleep 3

# 启动医疗健康问答系统
echo -e "[4/6] 启动 🏥 医疗健康问答系统..."
nohup streamlit run medical_qa.py --server.port 7871 > logs/rag-medical.log 2>&1 &
echo -e "${GREEN}✅ 已启动${NC}"
sleep 3

# 启动金融知识问答系统
echo -e "[5/6] 启动 💰 金融知识问答系统..."
nohup streamlit run finance_qa.py --server.port 7872 > logs/rag-finance.log 2>&1 &
echo -e "${GREEN}✅ 已启动${NC}"
sleep 3

# 启动IT技术问答系统
echo -e "[6/6] 启动 💻 IT技术问答系统..."
nohup streamlit run tech_qa.py --server.port 7873 > logs/rag-tech.log 2>&1 &
echo -e "${GREEN}✅ 已启动${NC}"
sleep 3

echo ""
echo -e "${YELLOW}⏳ 服务正在启动中，请稍候...${NC}"
sleep 10

echo ""
echo -e "${YELLOW}🌐 正在打开浏览器...${NC}"
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:7861
    xdg-open http://localhost:7869
elif command -v open &> /dev/null; then
    open http://localhost:7861
    open http://localhost:7869
else
    echo -e "${YELLOW}⚠️ 请手动打开浏览器访问:${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}           启动完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "📋 系统列表："
echo -e "📚 通用RAG智能问答系统:    http://localhost:7861"
echo -e "⚖️ 法律知识问答系统:        http://localhost:7869"
echo -e "🎓 教育知识问答系统:        http://localhost:7870"
echo -e "🏥 医疗健康问答系统:        http://localhost:7871"
echo -e "💰 金融知识问答系统:        http://localhost:7872"
echo -e "💻 IT技术问答系统:          http://localhost:7873"
echo ""
echo -e "📌 企业级功能："
echo -e "    - 统一配置管理"
echo -e "    - 企业级日志系统"
echo -e "    - 安全管理模块"
echo -e "    - 对话历史管理"
echo -e "    - 核心RAG引擎"
echo ""
echo -e "⚠️ 重要提示："
echo -e "    - 首次启动可能需要下载模型，请耐心等待"
echo -e "    - 如果服务无法启动，请检查端口是否被占用"
echo -e "    - 日志文件位于 logs/ 目录下"
echo ""
echo -e "🔧 常用命令："
echo -e "    - 查看所有服务: ps aux | grep streamlit"
echo -e "    - 停止所有服务: pkill -f streamlit"
echo -e "    - 查看日志: tail -f logs/rag-general.log"
echo ""
echo -e "${BLUE}========================================${NC}"
