# Changelog

所有重要的项目变更都将记录在此文件中。

## [Unreleased]

### Added
- 添加独立的《隐私政策》文件 (PRIVACY.md)
- 添加 Dockerfile 和 docker-compose.yml 支持容器化部署
- 添加 CHANGELOG.md 记录版本变更
- 添加 CODE_OF_CONDUCT.md 社区行为准则
- 医疗问答系统添加显著的医疗免责声明
- 金融问答系统添加投资风险提示
- 更新 .env.example，标注必填项和变量用途

### Changed
- 重命名 medical_qa_fixed.py → legal_qa.py，统一文件名
- 更新 README.md，统一服务承诺时间定义
- 更新所有文档中的文件名引用，确保一致性
- 医疗系统 UI 显著位置添加二次风险提醒
- 金融系统补充"不构成盈利承诺"合规表述

### Fixed
- 修复文档内容一致性问题
- 修复启动脚本中的文件名引用错误

## [2.0.0] - 2024-01-15

### Added
- 新增历史对话记录功能
- 新增六个垂直领域问答系统：通用RAG、法律、医疗、教育、金融、IT技术
- 新增预置知识库索引加载功能
- 新增 CONTRIBUTING.md 贡献指南
- 新增 FAQ.md 常见问题文档
- 新增 SECURITY.md 安全与隐私指南
- 新增 LICENSE 文件 (MIT)
- 新增 THIRD_PARTY_NOTICES.md 第三方依赖声明

### Changed
- 重构项目结构，支持多系统并行运行
- 优化启动脚本，支持一键启动所有服务
- 更新 README.md，添加徽章和截图展示

### Fixed
- 修复端口冲突问题
- 修复索引加载问题

## [1.0.0] - 2023-12-01

### Added
- 初始版本发布
- 基础 RAG 问答功能
- 文档上传和处理
- 向量索引构建
