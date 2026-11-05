# 部署流程与规范（EmbodiedSim-Framework）

## 1. 部署等级定义

| 等级 | 典型使用场景 | 健康检查严格度 | GUI默认 | 自动恢复 |
|------|-------------|---------------|---------|---------|
| **test** | 开发机调试 / 单元演示 | 允许 WARN 继续 | ✅ 启用 | ❌ 关闭 |
| **pre**  | 预发环境 / 现场联调前 | 允许 WARN 继续 | ✅ 启用 | ⚠️ 可选 |
| **prod** | 真机量产部署 / 长期运行 | FAIL 即中止 | ❌ 关闭 | ✅ 强制启用 |

---

## 2. 一次标准部署的 6 阶段流程

本框架在 `deployment/deploy_main.py` 中实现了标准流水线：

| 阶段 | 名称 | 工作内容 | 通过条件 |
|------|------|---------|---------|
| 1 | 健康检查预检 | 系统/配置/安全/通信/AI/数据/性能/硬件 8大类检查 | prod等级FAIL=0 |
| 2 | 配置装配 | 注入项目版本、部署等级、机器人/场景、开关位 | 非空即可 |
| 3 | 通信适配 | 按协议创建 Adapter、连接、回环自测 | 连接成功/Mock |
| 4 | 仿真/真机启动 | 冒烟测试：创建→加载→步进到安全位姿→关闭 | 无异常 |
| 5 | 三层编排启动 | Perception/Decision/Execution 8 周期闭环 | 全部成功 |
| 6 | 监控守护 | 心跳输出+监控指标采集（生产模式下无限循环） | 演示通过 |

### 命令行执行方式

```bash
# 单步 test 等级
python -m deployment.deploy_main test

# 预发 / 生产
python -m deployment.deploy_main pre
python -m deployment.deploy_main prod
```

---

## 3. 健康检查 8 大类条目

详细实现在 `deployment/health_check.py`：

| 类 | 代表条目 | 说明 |
|----|---------|------|
| 系统环境 | OS/Python版本、内存、磁盘 | 基本环境可用性 |
| 配置 | .env.example 存在、requirements.txt 存在 | 工程完整性 |
| 安全防护 | 紧急停止标志位、日志目录可写 | 生产部署的基础安全 |
| 通信 | 基础网络连通（默认 8.8.8.8:53） | 离线部署可SKIP |
| AI模型 | .env 中 API Key 是否配置 | 纯仿真可SKIP |
| 数据 | 项目根目录可读 | 代码访问权限 |
| 性能 | CPU瞬时负载 | 保护过载机器 |
| 真机硬件 | （公共示例默认SKIP） | 对接关节回零/示教点位后启用 |

---

## 4. 部署产物与归档

每次部署会自动在 `logs/deploy_{等级}_{时间戳}/` 目录生成 2 类文件：

| 文件 | 用途 |
|------|------|
| `deploy_{deploy_id}.log` | 逐行带阶段/严重级别的完整部署日志（含异常栈） |
| `deploy_summary.json` | 部署清单 + 最后 200 条事件 + 元信息归档（便于可视化分析） |

日志格式示例：
```
2026-08-08 08:10:00 [INFO] ℹ️ Engine               :: 部署任务启动 | id=deploy_1723...
2026-08-08 08:10:00 [PHASE] 🚦 PhaseEngine          :: ──── [1/6] 进入阶段 PHASE_1_PRECHECK ────
2026-08-08 08:10:01 [OK] ✅ PreCheck             :: 健康检查阶段通过
```

---

## 5. 安全部署规范（强制执行）

- **绝不**把真实 `.env` / 私钥 / 机器人 IP 提交到 Git（`.gitignore` 已包含）
- **prod 等级部署前**健康检查中 FAIL 必须清零，禁止用 `--force` 绕过
- **真机部署前**必须先用 test 等级在同机器跑通 Phase 1~5
- 任何涉及末端速度/力控的参数调整必须在 test 等级仿真验证通过后再上真机
- 所有紧急停止入口：GUI红色大按钮 / 回车键 / Python `safety_controller.trigger_emergency_stop()` / 真实硬件IO，必须并联合规

---

## 6. 故障处理指引（常见问题）

| 现象 | 排查路径 |
|------|---------|
| 健康检查 `SYS_DISK` FAIL | 清理磁盘到 5GB 以上空间后重试 |
| 健康检查 `SAFE_LOG_DIR` FAIL | 确认项目目录写权限；手动 `mkdir -p logs` |
| 健康检查 `CFG_REQUIREMENTS` FAIL | 确认项目根目录下存在 `requirements.txt` |
| Phase 4 仿真启动失败 | 先确认 `pip install pybullet numpy` 已装；无GUI环境加 `--direct` |
| Phase 3 通信连接失败 | 公共示例默认用 Mock；真机需用 AdapterFactory.register 注册新协议实现 |
| 部署日志缺失 | 检查 `logs/` 目录权限；DeployLogger 自带异常兜底但需避免磁盘满 |
