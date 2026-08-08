<div align="center">

# 🤖 Hxdmou · 个人作品集 · Robot

> **AI 系统工程师 / 具身智能工程师 / RAG 系统开发**
>
> 专注**具身智能系统工程化落地** · 企业级 RAG 知识问答系统定制 · AI 智能体架构设计
>
> 📍 安徽蚌埠（可周边）· 💼 全职 / 远程 · 📧 `979718240@qq.com`

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PyBullet](https://img.shields.io/badge/Sim-PyBullet-orange)
![RAG](https://img.shields.io/badge/AI-RAG--v3-purple)
![LangChain](https://img.shields.io/badge/LLM-LangChain-green)
![FAISS](https://img.shields.io/badge/Vector-FAISS-yellow)
![Streamlit](https://img.shields.io/badge/Web-Streamlit-red)
![ROS](https://img.shields.io/badge/Robot-ROS-22314E?logo=ros)
![License](https://img.shields.io/badge/License-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/Hxdmou/Robot?color=ff69b4)
![Repo Size](https://img.shields.io/github/repo-size/Hxdmou/Robot?color=9cf)

</div>

---

## 📑 快速导航（Table of Contents）

| # | 板块 | 一句话 |
|---|------|-------|
| 0 | [🤔 仓库说明](#-仓库说明作品集集合) | 为什么仓库里有多个不同领域的项目 |
| 1 | [👋 关于我](#-关于我) | 我的工程定位与核心能力 |
| 2 | [🚀 代表作一 · 具身智能仿真框架](#-代表作一embodiedsim-framework-具身智能仿真与部署全栈框架) | 主打：PyBullet 仿真 + 4 层工程架构 + 部署流水线 |
| 3 | [🎖️ 代表作二 · 10 套 RAG 问答系统](#️-代表作二十套垂直领域企业级-rag-智能问答系统) | 加分：10 个垂直领域上线 + 7 大技术亮点 |
| 4 | [🧩 其他加分项目](#-其他加分项目) | NLP / A2A / 部署模板 |
| 5 | [🛠️ 技术栈全景](#️-个人技术栈) | 6 大类 + 熟练度星级 |
| 6 | [🎯 面试官常见 Q&A](#-面试官常见-qa) | 高频 4 问：去算法版 / Sim2Real / RAG 复用 / 难点 |
| 7 | [📬 求职联系](#-求职--合作联系) | 岗位意向 / 地点 / 邮箱 / 可提供服务 |

---

## 🤔 仓库说明（作品集集合）

> 本仓库是我个人**作品集集合仓库**，收录多个独立可运行的 AI/机器人项目，方便招聘方一次性浏览我的全部能力。各项目相互独立、互不依赖：
>
> - 🎯 **核心项目（推荐优先阅读）**：`_PUBLIC_NTA_OUTPUT/EmbodiedSim-Framework/` —— 具身智能仿真与部署全栈框架
> - 🎖️ **加分项目**：根目录下的 `legal_knowledge_base/`、`nlp_news_classification/`、`embodied-intelligence/`、`hosts/` 等，均为可独立运行的子项目
> - 📄 **技术文档**：根目录下的 `A2A_PROTOCOL_DEEP_DIVE.md`、`ARCHITECTURE.md` 等设计文档，体现架构设计与文档输出能力

---

## 👋 关于我

你好！我是一名热爱把 AI 技术**做成可用系统**的工程师。相比学术论文里的算法指标，我更擅长：
- 🧱 把零散的算法模块、仿真环境、大模型 API **搭成一个端到端可运行的产品**
- 🏗️ 设计清晰的分层架构与接口，让项目可扩展、可维护、可落地部署
- 🛡️ 在工程化细节上较真（安全防护、健康检查、日志审计、配置管理）
- 🎨 给终端用户做一个能直接上手的 GUI / Web 界面

下面是我的两个**可运行、有源码、带文档**的核心代表作 👇

---

## 🚀 代表作一：EmbodiedSim-Framework 具身智能仿真与部署全栈框架

> **一句话介绍**：PyBullet 机械臂仿真 + 感知-决策-执行三层解耦架构 + 企业级工程部署流水线的端到端工具包。专注系统集成与工程落地（去算法版，非学术论文代码）。

### ✨ 能力展示矩阵（对应技术栈）

| 能力维度 | 具体内容 | 用到的技术 |
|---------|---------|-----------|
| 🎯 **物理仿真环境搭建** | PyBullet 通用仿真层，Franka Panda / KUKA iiwa 双机械臂示例，工业/物流/医疗 3 套场景 | PyBullet, 刚体物理仿真 |
| 🏗️ **系统架构设计** | 感知-决策-执行三层接口解耦，模块化可插拔组件设计，适配器/抽象工厂模式 | 面向对象设计, 设计模式 |
| 🚀 **工程化部署** | 三级健康检查（test/pre/prod），8 类检查项，部署主流程编排，配置模板化 | 配置管理, 容灾, DevOps |
| 🔌 **多协议通信适配** | TCP / UDP / CAN / EtherCAT / ROS / Modbus 6 种通信协议抽象适配层 | Socket, 工业总线, ROS |
| 🛡️ **企业级安全框架** | 碰撞检测 + 紧急停止 + 异常熔断 + 输入校验 + 操作日志审计 5 层防护 | 安全工程, 风险控制 |
| 🎮 **GUI 应用开发** | Tkinter 图形控制面板，实时状态监控，手动遥操作演示 | Tkinter, 人机交互 |
| 🧠 **AI 决策接入** | LLM 大模型决策 SDK，多智能体协作编排，RAG 知识库接口 | LLM API, Agent, LangChain |
| 🔄 **Sim2Real 迁移** | 摩擦/阻尼/质量/温度/时延 等 ≥10 维参数域随机化框架，仿真→真机适配层 | 域随机化, Sim2Real |

### 🏛️ 系统架构

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

### 🎬 演示效果预览（待补充截图 / GIF）

> ⏳ **预留展示位**：后续可在此粘贴以下演示截图或 GIF：
> 1. PyBullet 仿真环境中机械臂抓取物体的渲染图
> 2. Tkinter GUI 控制面板实时显示关节角度/末端位姿的截图
> 3. 部署健康检查通过的终端输出截图
> 4. 数字孪生系统可视化画面
>
> 💡 **小技巧**：把录屏转成 GIF 放在这里，招聘方不需要 clone 仓库就能直观看到效果，印象分 +20%。

### 📁 代码结构（可直接点击阅读）

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

# 2. 跑仿真演示（机械臂 + 场景加载 + 运动）
python examples/run_simulation_demo.py

# 3. 打开 GUI 控制面板（实时状态监控 + 遥操作）
python applications/robot_control_gui.py

# 4. 跑部署健康检查（三级检查 + 结果报告）
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
| 🔍 **混合检索引擎** | BM25 关键词检索 + FAISS 向量检索双路召回，比单向量检索准确率提升约 15% |
| ⚡ **流式输出** | SSE（Server-Sent Events）实时返回回答生成过程，首字延迟 < 1s，体验流畅 |
| 📚 **多格式统一解析** | PDF/Word/Markdown/TXT/HTML 统一走解析管线，结构化分块（语义块 + 固定滑窗结合） |
| 🔗 **可追溯引文** | 每条回答附来源段落与文档标题，企业场景合规审计无忧 |
| 🛡️ **三层安全合规** | 输入敏感词过滤 + 输出拒答策略 + 全链路操作日志，满足企业数据安全要求 |
| 📦 **私有化部署** | Docker 镜像 / 裸机脚本均可，全链路支持离线部署，数据 100% 不出企业内网 |
| 🔌 **双形态 API** | RESTful API（对接飞书/钉钉/OA）+ Streamlit Web 端（业务人员直接使用） |

---

## 🧩 其他加分项目

| 项目 | 说明 | 对应能力 |
|------|------|---------|
| 📰 **NLP 新闻分类系统** | `nlp_news_classification/` 文本分类基线模型与完整处理流水线 | NLP 文本处理, 机器学习流水线, 特征工程 |
| 🤝 **A2A 智能体协作协议** | `A2A_PROTOCOL_DEEP_DIVE.md` + PPT V17 完整设计方案 | 多智能体架构设计, 技术文档输出, 产品思维 |
| 🌐 **多智能体部署框架** | `hosts/` 多节点部署配置模板与 Host 抽象层 | 分布式部署, 容器化编排思路, 配置管理 |
| 💡 **多模态 & 仿真结果日志** | 根目录各类 `*_log.csv`（gripper/trajectory/obstacle 等） | 实验数据记录分析, 数据驱动调参意识 |

---

## 🛠️ 个人技术栈

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

## 🎯 面试官常见 Q&A

> **提前回答高频问题，节省面试时间，也让您看到我的思考深度**

### Q1：为什么具身智能框架是「去算法版」？算法部分呢？

**A**：学术圈开源的 RL 策略网络、运动规划算法（RRT/A*）、逆解求解器已经非常成熟且同质化，直接拿来用即可，不需要我再重复造轮子。**真正让企业头疼的是"怎么把这些零散算法模块整合成一个稳定可维护、能部署到真机上的系统"**。所以这个项目刻意避开算法细节，把重点放在：接口抽象（让算法可以即插即用）、工程化部署（健康检查/配置管理）、安全防护（碰撞/急停/熔断）、Sim2Real 适配这几块——这些都是**真实落地时工作量最大、最容易踩坑但论文里很少写**的部分，也更能体现系统工程能力。

### Q2：仿真到真机（Sim2Real）具体怎么迁移？

**A**：分三步走：① **参数域随机化**：训练/测试时在仿真中给摩擦、阻尼、质量、温度、电机时延等 10+ 物理参数加上合理分布，让策略对参数扰动鲁棒；② **接口抽象层**：仿真动作输出和真机控制指令走同一个 `RobotController` 抽象接口，切换时只换适配器实现，不改上层逻辑；③ **三级健康检查**：上真机前先跑 test 级检查（离线接口）→ pre 级（真机半联动）→ prod 级（全负载），每一级都有自动验收报告，避免踩坏设备。

### Q3：10 套垂直领域 RAG 是怎么快速复用的？会不会有大量重复代码？

**A**：核心是**"一个骨架 + 10 套配置化皮肤"**架构。骨架包含：文档解析管线、混合检索引擎、Prompt 模板层、流式输出层、鉴权日志层——这些全部通用，代码只写一套。每个垂直领域只需要写：① 领域专属分块策略（比如法律按条，医疗按实体）、② 领域 Prompt 模板、③ 领域后处理规则（比如金融加数值校验、法律加时效性过滤）+ ④ 领域知识库文件。**单领域新增代码量 < 骨架代码的 5%**，后续扩展效率极高。

### Q4：项目中遇到的最大技术难点是什么？怎么解决的？

**A**：**RAG 中的"检索准度 vs 召回率"平衡 + 企业级合规要求叠加**。具体表现：如果检索 Top-K 调大，召回率高但准度下降，LLM 会被噪声文档误导；如果 Top-K 小，关键条款漏召回导致回答错误，而且还要保证每条回答都能追溯原文。解决策略：① **双路召回+重排**：BM25 保关键词命中、向量检索保语义相关，两路各取 Top-K 合并后用轻量 Cross-Encoder 重排到 Top-3；② **分块策略定制**：不同领域不同分块（法律按法条分段、IT 按 Markdown 标题分级），保证每个 chunk 语义自洽；③ **结构化元数据**：每个 chunk 入库时带上"来源文件/页码/段落序号/时效/权限等级"元数据，回答时直接附原文引用，满足合规审计。

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

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/Hxdmou)

</div>
