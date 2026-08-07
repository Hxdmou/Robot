# API调用示例文档

---

## 📡 API接口说明

本系统提供REST API接口，方便您将RAG问答能力集成到自己的应用中。

### 基础信息

- **服务地址**: `http://localhost:5000`
- **API模式**: 需要设置环境变量 `API_MODE=true` 来启用API
- **Content-Type**: `application/json`

---

## 🔌 接口列表

| 接口 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/api/ask` | POST | 问答接口 |
| `/api/systems` | GET | 获取系统列表 |
| `/api/index/status` | GET | 查看索引状态 |

---

## 📝 问答接口使用示例

### 1. 使用 curl 调用

```bash
# 通用RAG系统
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "什么是RAG技术？",
    "system": "general",
    "temperature": 0.7,
    "top_k": 5
  }'

# 法律问答系统
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "什么是合同无效的情形？",
    "system": "legal"
  }'

# 医疗问答系统
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "感冒应该如何治疗？",
    "system": "medical"
  }'
```

### 2. 使用 Python 调用

```python
import requests

# 基础配置
BASE_URL = "http://localhost:5000"

def ask_question(question, system="general", temperature=0.7, top_k=5):
    """
    调用问答API
    
    参数:
        question: str - 用户问题
        system: str - 系统类型 (general/legal/medical/finance/education/tech)
        temperature: float - 温度参数 (0-1)
        top_k: int - 检索数量
    
    返回:
        dict - 包含答案的响应
    """
    url = f"{BASE_URL}/api/ask"
    
    payload = {
        "question": question,
        "system": system,
        "temperature": temperature,
        "top_k": top_k
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text, "status_code": response.status_code}

# 示例使用
if __name__ == "__main__":
    # 调用通用RAG系统
    result = ask_question("什么是人工智能？")
    print("问题:", result.get("question"))
    print("答案:", result.get("answer"))
    
    # 调用法律问答系统
    result = ask_question("劳动合同到期不续签有补偿吗？", system="legal")
    print("\n问题:", result.get("question"))
    print("答案:", result.get("answer"))
    
    # 调用医疗问答系统
    result = ask_question("高血压患者需要注意什么？", system="medical")
    print("\n问题:", result.get("question"))
    print("答案:", result.get("answer"))
```

### 3. 使用 JavaScript/Node.js 调用

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:5000';

async function askQuestion(question, system = 'general', temperature = 0.7, top_k = 5) {
    try {
        const response = await axios.post(`${BASE_URL}/api/ask`, {
            question,
            system,
            temperature,
            top_k
        });
        
        return response.data;
    } catch (error) {
        console.error('API调用失败:', error.message);
        throw error;
    }
}

// 示例使用
(async () => {
    const result = await askQuestion('什么是区块链技术？');
    console.log('问题:', result.question);
    console.log('答案:', result.answer);
})();
```

---

## 📊 响应格式

### 成功响应

```json
{
    "question": "什么是RAG技术？",
    "answer": "RAG（Retrieval-Augmented Generation）即检索增强生成技术...",
    "system": "general",
    "status": "success"
}
```

### 错误响应

```json
{
    "error": "Missing question parameter",
    "status_code": 400
}
```

---

## 🔧 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| question | string | ✅ | - | 用户问题 |
| system | string | ❌ | general | 系统类型 |
| temperature | float | ❌ | 0.7 | 温度参数（0-1） |
| top_k | int | ❌ | 5 | 检索文档数量 |

### 支持的系统类型

| system值 | 系统名称 | 说明 |
|----------|----------|------|
| general | 通用RAG系统 | 通用文档问答 |
| legal | 法律知识问答 | 法律领域问答 |
| medical | 医疗健康问答 | 医疗健康咨询 |
| finance | 金融投资问答 | 金融知识问答 |
| education | 教育学习问答 | 教育知识问答 |
| tech | IT技术问答 | 技术文档问答 |

---

## 🚀 启动API服务

### 方式一：直接运行

```bash
API_MODE=true python api_server.py
```

### 方式二：使用环境变量

```bash
export API_MODE=true
python api_server.py
```

### 方式三：Docker部署

```bash
docker run -e API_MODE=true -p 5000:5000 rag-qa-system
```

---

## 📋 完整示例

### Python完整示例

```python
import requests

def main():
    # 健康检查
    health_response = requests.get("http://localhost:5000/health")
    print("健康状态:", health_response.json())
    
    # 获取系统列表
    systems_response = requests.get("http://localhost:5000/api/systems")
    print("可用系统:", systems_response.json())
    
    # 查看索引状态
    status_response = requests.get("http://localhost:5000/api/index/status?system=legal")
    print("法律系统索引状态:", status_response.json())
    
    # 提问
    questions = [
        {"question": "什么是机器学习？", "system": "general"},
        {"question": "什么是侵权责任？", "system": "legal"},
        {"question": "如何预防糖尿病？", "system": "medical"}
    ]
    
    for q in questions:
        response = requests.post(
            "http://localhost:5000/api/ask",
            json=q
        )
        result = response.json()
        print(f"\n【{result['system']}】")
        print(f"问: {result['question']}")
        print(f"答: {result['answer'][:100]}...")

if __name__ == "__main__":
    main()
```

---

## ⚠️ 注意事项

1. **API模式**: 默认关闭，需要设置 `API_MODE=true` 环境变量启用
2. **知识库初始化**: 使用前需要确保对应系统的知识库已初始化
3. **请求频率**: 建议合理控制调用频率，避免过度请求
4. **错误处理**: 请妥善处理API返回的错误信息

---

## 📧 技术支持

如需更多帮助或定制API接口，请联系：business@rag-qa-system.com
