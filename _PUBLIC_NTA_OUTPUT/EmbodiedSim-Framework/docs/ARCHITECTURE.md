# 系统架构设计说明（EmbodiedSim-Framework）

## 1. 设计总纲

EmbodiedSim-Framework 定位为「具身智能工程应用框架」，目标是展示**从仿真到部署的全链路工程能力**，而不是算法研究。

设计遵循三大原则：

| 原则 | 说明 |
|------|------|
| **分层解耦** | 6层结构（Core/Engineering/Deployment/Applications/Examples/Docs）清晰拆分，层间只通过标准接口通信 |
| **可替换接口** | 每个核心能力都抽象成基类，真机/仿真/离线场景可以无缝替换实现 |
| **安全优先** | 5层安全防护贯穿所有模块（输入校验→限位→速度→碰撞→急停熔断器） |

---

## 2. 六层结构说明

```
┌──────────────────────────────────────────────────────────┐
│  examples/        可运行演示代码（面向面试官/评审）          │
├──────────────────────────────────────────────────────────┤
│  applications/    成品应用（GUI/LLM SDK/数字孪生/决策系统）│
├──────────────────────────────────────────────────────────┤
│  engineering/     工程工具（安全/碰撞/Sim2Real/记录/监控） │
├──────────────────────────────────────────────────────────┤
│  deployment/      部署适配（健康检查/主流程/通信适配）      │
├──────────────────────────────────────────────────────────┤
│  core/            核心框架（仿真环境/配置/三层接口）        │
├──────────────────────────────────────────────────────────┤
│  docs/            架构与部署文档（本文件所在目录）           │
└──────────────────────────────────────────────────────────┘
```

---

## 3. 核心数据流闭环

```
  ┌──────────────┐   语义化结果    ┌──────────────┐   动作指令
  │ Perception   │ ─────────────▶ │  Decision    │ ─────────────┐
  │ (感知层)     │                │  (决策层)    │              │
  └──────────────┘                └──────────────┘              ▼
         ▲                                                       │
         │ 反馈状态                                       ┌──────────────┐
         │                                                │  Execution   │
         └─────────────────────────────────────────────── │  (执行层)    │
                              状态 & 执行结果              └──────────────┘
                                                               │
                                                               ▼
                                                    ┌──────────────────┐
                                                    │ Digital Twin 系 │
                                                    │ 统: 实体↔孪生同步 │
                                                    └──────────────────┘
```

### 3.1 三层接口的标准消息格式

统一使用 `core.module_interfaces.Message` 类：

| 字段 | 作用 |
|------|------|
| `msg_id` | 唯一ID，用于审计追溯 |
| `source/target` | 来源模块/目标模块 |
| `msg_type` | data/command/event/error 四类 |
| `timestamp_s` | 时间戳 |
| `payload` | 结构化数据（字典） |
| `meta` | 附加元信息（如步数、决策ID等） |

---

## 4. 关键设计模式一览

| 模块 | 采用的设计模式 | 应用说明 |
|------|---------------|---------|
| deploy_adapters.py | **工厂模式** + **策略模式** | AdapterFactory 按协议类型创建对应实现 |
| llm_decision_sdk.py | **责任链模式** + **回退策略** | 多Provider按优先级调用，失败自动Mock兜底 |
| safety_controller.py | **熔断器模式** + **策略链** | 5层校验顺序执行，命中后熔断 |
| digital_twin_system.py | **观察者模式** + **状态源抽象** | 多个 Renderer/Listener 订阅状态变化 |
| module_interfaces.py | **发布-订阅** + **编排器** | Perception 发布，Decision 订阅；Orchestrator 串闭环 |
| domain_randomization.py | **规格-采样分离** | 参数声明与采样逻辑解耦，便于扩展参数 |

---

## 5. 扩展指引（如何在框架上新增功能）

### 5.1 新增一种机器人类型
```
1. 在 core/robot_config.py 的 ROBOT_BRANDS 中新增一条目
2. 补充 urdf_model / default_joint_limits / 支持的 scenes
3. （可选）在 simulation_env.load_robot() 里加对应 URDF 路径映射
```

### 5.2 新增一种通信协议
```
1. 继承 deploy_adapters.CommunicationAdapter 实现 connect/send/recv/disconnect
2. 用 AdapterFactory.register("protocol_name", YourAdapter) 注册
3. 在部署清单中把 protocol 改成新名字即可
```

### 5.3 新增一个决策技能
```
1. 在 applications/llm_decision_sdk.py 的 SkillLibrary.register 新增 FunctionTool
2. 补 JSON Schema 参数 + Python 实现函数
3. 系统会自动把该技能暴露给 LLM Function Calling
```

### 5.4 新增一种数字孪生渲染器
```
1. 继承 digital_twin_system.TwinRenderer 实现 render(state)
2. 用 DigitalTwinSystem.attach_renderer() 挂接即可
3. 可同时挂接多种渲染器（控制台+PyBullet+Web）
```

---

## 6. 本框架「不包含」的内容（去算法说明）

为保持与工程应用定位一致，**以下纯算法内容不在本仓库中**，如项目需要可单独引入专门的算法子模块：

- ❌ PPO / SAC / TD3 / DDPG 等强化学习训练实现
- ❌ RRT / A* / PRM 等路径规划算法源码
- ❌ 逆运动学雅可比解析解推导、动力学辨识算法
- ❌ 学术论文实验对比代码 / 消融实验代码

---

## 7. 代码质量与可维护性

- 所有对外类提供 `__repr__` 与 `summary()`/`report()` 诊断接口
- 关键路径都有异常捕获 + 不抛崩型容错（渲染器/回调/订阅者）
- 数据结构优先使用 `dataclass`，强类型字段名自文档
- 对外入口统一提供 **`from_env()` / `quick()` / 命令行** 三种使用方式
