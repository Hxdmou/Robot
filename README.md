<div align="center">

# 🤖 Hxdmou · 个人作品集 · Robot

> **AI 系统工程师 / 具身智能工程师 / RAG 系统开发**
>
> 专注**具身智能系统工程化落地** · 企业级 RAG 知识问答系统定制 · AI 智能体架构设计
>
> � 安徽蚌埠（可周边）· 💼 全职 / 远程 · 📧 `979718240@qq.com`

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PyBullet](https://img.shields.io/badge/Sim-PyBullet-orange)
![RAG](https://img.shields.io/badge/AI-RAG--v3-purple)
![LangChain](https://img.shields.io/badge/LLM-LangChain-green)
![FAISS](https://img.shields.io/badge/Vector-FAISS-yellow)
![Streamlit](https://img.shields.io/badge/Web-Streamlit-red)

</div>

---

## 👋 关于我

你好！我是一名热爱把 AI 技术**做成可用系统**的工程师。相比学术论文里的算法指标，我更擅长：
- 🧱 把零散的算法模块、仿真环境、大模型 API **搭成一个端到端可运行的产品**
- �️ 设计清晰的分层架构与接口，让项目可扩展、可维护、可落地部署
- �️ 在工程化细节上较真（安全防护、健康检查、日志审计、配置管理）
- 🎨 给终端用户做一个能直接上手的 GUI / Web 界面

下面是我的两个**可运行、有源码、带文档**的核心代表作 �

---

## � 代表作一：EmbodiedSim-Framework 具身智能仿真与部署全栈框架

> **一句话介绍**：PyBullet 机械臂仿真 + 感知-决策-执行三层解耦架构 + 企业级工程部署流水线的端到端工具包。专注系统集成与工程落地（去算法版，非学术论文代码）。

### ✨ 能力展示矩阵（对应技术栈）

| 能力维度 | 具体内容 | 用到的技术 |
|---------|---------|-----------|
| 🎯 **物理仿真环境搭建** | PyBullet 通用仿真层，Franka Panda / KUKA iiwa 双机械臂示例，工业/物流/医疗 3 套场景 | PyBullet, 刚体物理仿真 |
| 🏗️ **系统架构设计** | 感知-决策-执行三层接口解耦，模块化可插拔组件设计，适配器/抽象工厂模式 | 面向对象设计, 设计模式 |
| 🚀 **工程化部署** | 三级健康检查（test/pre/prod），8 类检查项，部署主流程编排，配置模板化 | 配置管理, 容灾, DevOps |
| � **多协议通信适配** | TCP / UDP / CAN / EtherCAT / ROS / Modbus 6 种通信协议抽象适配层 | Socket, 工业总线, ROS |
| 🛡️ **企业级安全框架** | 碰撞检测 + 紧急停止 + 异常熔断 + 输入校验 + 操作日志审计 5 层防护 | 安全工程, 风险控制 |
| � **GUI 应用开发** | Tkinter 图形控制面板，实时状态监控，手动遥操作演示 | Tkinter, 人机交互 |
| 🧠 **AI 决策接入** | LLM 大模型决策 SDK，多智能体协作编排，RAG 知识库接口 | LLM API, Agent, LangChain |
| � **Sim2Real 迁移** | 摩擦/阻尼/质量/温度/时延 等 ≥10 维参数域随机化框架，仿真→真机适配层 | 域随机化, Sim2Real |

### �️ 系统架构

```
┌───────────────────────────────────────────────────────────────────┐
│                    Applications 应用层                              │
│  GUI 控制  │  AI决策SDK  │  数字孪生  │  自主决策系统                │
├───────────────────────────────────────────────────────────────────┤
│                    Engineering 工程工具层                           │
│  安全控制  │  碰撞检测  │  域随机化  │  数据记录  │  健康检查         │
├───────────────────────────────────────────────────────────────────┤
│                    Core Framework 核心框架层                        │
│  PyBullet仿真环境  │  机器人配置  │  场景定义  │  三层接口定义         │
├───────────────────────────────────────────────────────────────────┤
│                    Deployment 部署适配层                            │
│  部署主流程  │  通信适配  │  配置管理  │  日志审计                    │
└───────────────────────────────────────────────────────────────────┘
```

### 📁 代码结构（可直接阅读）

| 路径 | 说明 |
|------|------|
| [`_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/core/`](_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/core) | 核心：仿真环境 + 机器人/场景配置 + 三层接口定义 |
| [`_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/engineering/`](_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/engineering) | 工程工具：安全控制 / 碰撞检测 / 域随机化 / 数据记录 |
| [`_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/deployment/`](_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/deployment) | 部署：主流程 + 通信适配器 + 健康检查框架 |
| [`_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/applications/`](_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/applications) | 应用：GUI / AI决策SDK / 数字孪生 |
| [`_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/examples/`](_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/examples) | 3 个可直接运行的演示脚本 |
| [`_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/docs/`](_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/docs) | 架构 / 部署 / 安全 3 份技术设计文档 |

### 🚀 快速运行

```bash
# 1. 安装依赖
cd _PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework
pip install -r requirements.txt

# 2. 跑仿真演示
python examples/run_simulation_demo.py

# 3. 打开 GUI 控制面板
python applications/robot_control_gui.py

# 4. 跑部署健康检查
python examples/deploy_health_check_demo.py
```

---

## 🎖️ 代表作二：十套垂直领域企业级 RAG 智能问答系统

> **一句话介绍**：基于 RAG（检索增强生成）的企业级知识问答系统，10 个垂直领域全部上线可演示，Web 端 + API 双形态，私有化部署。

### 📊 10 个已上线垂直领域

| # | 垂直领域 | 典型应用场景 | 核心技术 |
|---|---------|-------------|---------|
| 1 | ⚖️ **法律** | 法律条文检索、合同问答、案例参考 | BM25+向量双检索, 法条分段 |
| 2 | 🏥 **医疗** | 医学知识问答、健康咨询、用药指导 | 医学实体识别, 拒答策略 |
| 3 | 💰 **金融** | 金融产品介绍、投资问答、合规查询 | 数值抽取, 风控提示 |
| 4 | 💻 **IT 技术** | 技术文档问答、代码检索、报错排错 | 代码块索引, 上下文关联 |
| 5 | 🎓 **教育** | 教材知识点问答、学习辅导、题库解析 | 多模态支持, 引文追溯 |
| 6 | 🛒 **电商零售** | 商品介绍、活动规则、售后政策 | 多轮对话, 推荐关联 |
| 7 | 🏛️ **政务** | 政策解读、办事流程、政务公开 | 政策时效标注, 来源可查 |
| 8 | 👔 **人力资源** | 员工手册、薪酬福利、招聘流程 | 权限分级, 敏感词过滤 |
| 9 | 📚 **科研学术** | 论文检索、学术概念、实验方法 | 参考文献关联, PDF 解析 |
| 10 | 🌐 **通用** | 企业内部知识库、FAQ、Onboarding | 即插即用, 通用模板 |

### 🧠 核心技术亮点

| 特性 | 说明 |
|------|------|
| 🔍 **混合检索引擎** | BM25 关键词检索 + FAISS 向量检索双路召回，提升准确率 |
| ⚡ **流式输出** | SSE 实时返回回答过程，用户体验流畅 |
| 📚 **多格式解析** | PDF/Word/Markdown/TXT/HTML 统一解析，结构化分块 |
| 🔗 **引文追溯** | 每条回答可追溯来源段落，企业审计无忧 |
| �️ **安全合规** | 敏感词过滤 + 拒答策略 + 操作日志三层防护 |
| 📦 **私有化部署** | Docker / 裸机均可，全链路离线部署，数据不出企业 |
| 🔌 **API 形态** | RESTful API + Streamlit Web 端，可对接企业 OA/飞书/钉钉 |

---

## 🧩 其他加分项目

| 项目 | 说明 | 对应能力 |
|------|------|---------|
| 📰 **NLP 新闻分类系统** | `nlp_news_classification/` 文本分类基线模型与流程 | NLP 文本处理, 机器学习流水线 |
| 🤝 **A2A 智能体协作协议** | `A2A_PROTOCOL_DEEP_DIVE.md` + PPT 完整方案 | 多智能体架构设计, 技术文档输出 |
| 🌐 **多智能体部署框架** | `hosts/` 多节点部署配置模板 | 分布式部署, 容器化编排思路 |

---

## �️ 个人技术栈

```
编程语言:   Python ★★★★★ |  C/C++ ★★★☆☆  |  Shell ★★★☆☆ |  JS/TS ★★☆☆☆
AI/ML:     PyTorch | LangChain | RAG Pipeline | Vector DB (FAISS/Milvus)
仿真/机器人: PyBullet | ROS 1/2 | 运动规划基础 | Sim2Real 工程方法
工程部署:   Docker | CI/CD 基础 | 配置管理 | 日志与监控 | 健康检查框架
Web/API:    FastAPI | Streamlit | Gradio | RESTful | SSE 流式
数据库:     SQLite | PostgreSQL 基础 | Redis 基础
架构能力:   分层设计 | 模块化/可插拔 | 设计模式 | 系统集成 | 文档输出
```

---

## 📬 求职 / 合作联系

> 🎯 **求职意向**：AI 系统工程师 · 具身智能工程师 · RAG / LLM 应用开发 · 机器人系统集成
>
> 📍 **工作地点**：安徽蚌埠（可接受合肥/南京等周边城市）· 可远程
>
> 📧 **邮箱**：`979718240@qq.com`（来信必回，24 小时内回复）
>
> 💼 **可提供**：
> - 完整项目代码走读与演示
> - 系统设计思路讲解
> - RAG 系统定制化 POC
> - 具身智能仿真环境搭建
> - 详细版 PDF 简历（附更多项目细节）

---

<div align="center">

💡 **感谢您阅读到这里！** 如果我的项目和能力符合您的招聘需求，欢迎随时邮件联系。
期待有机会把这些系统工程经验，贡献到贵司的 AI / 机器人产品落地中 🙌

</div>
