import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """企业级配置管理"""
    
    # 项目基础配置
    PROJECT_NAME = os.getenv("PROJECT_NAME", "RAG智能知识问答系统")
    VERSION = "3.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # 服务器配置
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 7861))
    
    # 数据库配置
    DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
    VECTOR_STORE_DIR = os.path.join(DATA_DIR, "vector_store")
    CHAT_HISTORY_DIR = os.path.join(DATA_DIR, "chat_history")
    LOG_DIR = os.path.join(DATA_DIR, "logs")
    
    # LLM配置
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "deepseek-chat")
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 4096))
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.1))
    
    # 向量配置
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
    TOP_K = int(os.getenv("TOP_K", 5))
    
    # 安全配置
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", 100))
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 50 * 1024 * 1024))  # 50MB
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 系统配置
    SUPPORTED_FILE_TYPES = ["txt", "pdf", "xlsx", "xls", "docx", "doc"]
    MAX_UPLOAD_FILES = int(os.getenv("MAX_UPLOAD_FILES", 10))
    
    @staticmethod
    def ensure_directories():
        """确保必要目录存在"""
        directories = [
            Config.DATA_DIR,
            Config.VECTOR_STORE_DIR,
            Config.CHAT_HISTORY_DIR,
            Config.LOG_DIR
        ]
        for dir_path in directories:
            os.makedirs(dir_path, exist_ok=True)

# 系统类型配置
SYSTEM_CONFIGS = {
    "general": {
        "name": "通用RAG智能问答系统",
        "icon": "📚",
        "port": 7861,
        "description": "基于检索增强生成技术的通用智能问答系统",
        "features": ["多格式文档支持", "智能问答", "多轮对话", "历史记录"]
    },
    "legal": {
        "name": "法律知识问答系统",
        "icon": "⚖️", 
        "port": 7869,
        "description": "专业法律知识问答系统，预置法律知识库",
        "features": ["法律知识库", "法条引用", "文书解读", "案例分析"]
    },
    "education": {
        "name": "教育知识问答系统",
        "icon": "🎓",
        "port": 7870,
        "description": "学生学习助手，支持教材课件问答",
        "features": ["教材支持", "公式解析", "学习跟踪", "知识问答"]
    },
    "medical": {
        "name": "医疗健康问答系统",
        "icon": "🏥",
        "port": 7871,
        "description": "健康咨询助手，提供专业健康建议",
        "features": ["医学文献", "健康指南", "用药提醒", "免责声明"]
    },
    "finance": {
        "name": "金融知识问答系统",
        "icon": "💰",
        "port": 7872,
        "description": "金融投资助手，提供投资知识问答",
        "features": ["金融法规", "理财指南", "风险提示", "产品分析"]
    },
    "tech": {
        "name": "IT技术问答系统",
        "icon": "💻",
        "port": 7873,
        "description": "程序员技术助手，支持代码生成",
        "features": ["API文档", "代码生成", "技术方案", "问题解答"]
    },
    "e_commerce": {
        "name": "电商零售智能问答系统",
        "icon": "🛒",
        "port": 7874,
        "description": "电商运营助手，提供商品咨询和运营建议",
        "features": ["商品知识", "运营策略", "客服话术", "营销技巧"]
    },
    "government": {
        "name": "政务服务智能问答系统",
        "icon": "🏛️",
        "port": 7875,
        "description": "政务服务助手，提供政策解读和办事指南",
        "features": ["政策解读", "办事指南", "表格下载", "常见问题"]
    },
    "hr": {
        "name": "人力资源智能问答系统",
        "icon": "👔",
        "port": 7876,
        "description": "HR工作助手，提供招聘培训和员工管理支持",
        "features": ["招聘攻略", "培训方案", "绩效考核", "劳动合同"]
    },
    "academic": {
        "name": "科研学术智能问答系统",
        "icon": "📚",
        "port": 7877,
        "description": "学术研究助手，支持论文写作和文献分析",
        "features": ["文献检索", "论文写作", "研究方法", "学术规范"]
    }
}
