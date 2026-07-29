
# ============================================================================
# 免责声明与AI使用规范
# ============================================================================
# 本文件仅供技术研究与学习交流使用，不得用于任何非法用途。
#
# AI使用规范：
#   1. 使用本文件相关内容时须遵守所在地法律法规及伦理准则
#   2. 不得用于侵犯他人合法权益、危害网络安全、破坏公共秩序的活动
#   3. 涉及自动化决策的场景须确保人工复核机制与可解释性
#   4. 处理个人信息时须符合数据保护相关法规要求
#
# 风险提示：
#   本文件内容按"现状"提供，不保证绝对准确无误。
#   使用者须自行评估风险，因使用本文件导致的任何损失由使用者承担。
# ============================================================================

import re

# 读取原始markdown文件
with open(EXTERNAL_PROJECT_DIR  # was: A2A_ENTERPRISE_PPT.md, 'r', encoding='utf-8') as f:
    content = f.read()

# 更新第三章内容
chapter3_new_content = """# 第三章：安全与合规体系

## 3.1 企业级安全架构

```
┌─────────────────────────────────────────────────────────┐
│                     安全防护层                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │  API网关    │    │  WAF防火墙  │    │  DDoS防护   │  │
│  │  认证授权   │    │  入侵检测   │    │  流量清洗   │  │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘  │
│         │                  │                  │         │
│         └──────────────────┼──────────────────┘         │
│                            ▼                            │
│  ┌─────────────────────────────────────────────────┐    │
│  │              A2A协议安全层                       │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│    │
│  │  │ OAuth2  │ │  JWT    │ │  mTLS   │ │  RBAC   ││    │
│  │  │ API Key │ │  签名   │ │  加密   │ │  审计   ││    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘│    │
│  └─────────────────────────────────────────────────┘    │
│                            ▼                            │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Agent安全边界                       │    │
│  │  数据隔离 │ 内存保护 │ 代码沙箱 │ 权限控制       │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 3.2 安全组件矩阵

| 安全组件 | 业务价值 | 技术亮点 | 成功指标 | 防护级别 |
|----------|----------|----------|----------|----------|
| **API网关** | API安全成本降低50% | Kong/APISIX/Envoy | 攻击拦截率99% | 高 |
| **WAF防火墙** | Web攻击防护提升95% | ModSecurity/Akamai | OWASP Top10防护 | 极高 |
| **OAuth 2.0** | 认证效率提升3x | 授权码/PKCE/JWT | 认证延迟<3ms | 高 |
| **mTLS** | 通道安全提升100% | 双向证书+证书轮换 | 零中间人攻击 | 极高 |
| **RBAC/ABAC** | 权限管理效率提升4x | 角色/属性权限 | 细粒度控制 | 高 |
| **DDoS防护** | DDoS攻击防护提升99% | Cloudflare/Akamai | 流量清洗率99.9% | 极高 |
| **数据加密** | 数据安全合规100% | AES-256/GPG | 加密覆盖率100% | 极高 |
| **审计日志** | 合规审计效率提升5x | ELK/Splunk/Datadog | 日志不可篡改 | 高 |
| **威胁检测** | 威胁发现快80% | SIEM/EDR | 攻击发现<5min | 高 |
| **密钥管理** | 密钥安全100% | HSM/Cloud KMS | 密钥零泄露 | 极高 |
| **数据脱敏** | 数据隐私保护100% | 动态脱敏+静态脱敏 | 敏感数据零泄露 | 高 |
| **零信任架构** | 安全防护提升100% | 身份验证+最小权限 | 内部攻击防护 | 极高 |
| **隐私计算** | 数据价值释放100% | 联邦学习+安全多方计算 | 数据可用不可见 | 中 |

## 📚 拓展学习资源
- **OAuth 2.0规范**: https://oauth.net/2/
- **JWT官方**: https://jwt.io/
- **mTLS指南**: https://www.cloudflare.com/learning/access-management/what-is-mtls/
- **RBAC模型**: https://en.wikipedia.org/wiki/Role-based_access_control

---

## 3.3 认证与授权机制

### 3.3.1 OAuth 2.0集成

```json
// Agent获取Token
{
  "grant_type": "client_credentials",
  "client_id": "inventory-agent-prod",
  "client_secret": "[REDACTED]",
  "scope": "a2a:send a2a:receive"
}

// 成功响应
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "a2a:send a2a:receive",
  "agent_id": "inventory-agent-prod-001"
}
```

### 3.3.2 JWT Token结构

| 部分 | 内容 | 说明 |
|------|------|------|
| Header | `{"alg":"RS256","typ":"JWT"}` | 算法和类型 |
| Payload | Agent ID、权限范围、过期时间 | 业务信息 |
| Signature | RS256签名 | 防止篡改 |

### 3.3.3 安全测试矩阵

| 测试类型 | 工具 | 覆盖范围 | 频率 |
|----------|------|----------|------|
| SAST | SonarQube/Snyk | 源代码漏洞 | CI/CD |
| DAST | OWASP ZAP/Burp Suite | 运行时漏洞 | 周度 |
| IAST | Contrast Security | 集成测试 | CI/CD |
| 渗透测试 | 手动+自动化 | 完整安全评估 | 季度 |

## 📚 拓展学习资源
- **OAuth 2.0授权框架**: https://datatracker.ietf.org/doc/html/rfc6749
- **OpenID Connect**: https://openid.net/connect/
- **JWT最佳实践**: https://curity.io/resources/learn/jwt-best-practices/

---

## 3.4 数据加密与隐私保护

### 3.4.1 传输加密

| 层级 | 加密方式 | 协议 | 密钥长度 |
|------|----------|------|----------|
| 传输层 | TLS 1.3 | HTTPS/WSS | 256位 |
| 消息层 | AES-256-GCM | 端到端加密 | 256位 |
| 签名 | RSASSA-PSS | 消息完整性 | 2048/4096位 |
| 密钥交换 | X25519 | 椭圆曲线 | 256位 |

### 3.4.2 数据分类保护

| 数据类型 | 处理方式 | 合规要求 | 存储期限 |
|----------|----------|----------|----------|
| 公开数据 | 明文传输 | 无特殊要求 | 永久 |
| 业务数据 | 传输加密 | GDPR/CCPA | 业务周期 |
| 敏感数据 | E2E加密 | HIPAA/PCI-DSS | 最小必要 |
| 机密数据 | 零知识证明 | 企业保密协议 | 按需 |

### 3.4.3 合规认证矩阵

| 认证类型 | 适用场景 | 有效期 | 审计频率 |
|----------|----------|--------|----------|
| SOC2 Type II | SaaS服务 | 1年 | 年度 |
| ISO 27001 | 信息安全管理 | 3年 | 年度 |
| GDPR | 欧盟用户数据 | 持续 | 持续 |
| HIPAA | 医疗健康数据 | 持续 | 年度 |
| PCI-DSS | 支付卡数据 | 1年 | 季度 |

## 📚 拓展学习资源
- **TLS 1.3规范**: https://datatracker.ietf.org/doc/html/rfc8446
- **AES加密标准**: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf
- **GDPR合规**: https://gdpr.eu/
- **零知识证明**: https://z.cash/technology/zksnarks/

---

## 3.5 合规审计体系

### 3.5.1 审计日志规范

```json
{
  "timestamp": "2026-05-07T14:30:00Z",
  "audit_id": "audit-7a3b2c1d-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
  "event_type": "a2a_message_received",
  "actor": {
    "agent_id": "order-agent-prod-002",
    "organization": "ACME Corp",
    "ip_address": "10.0.0.15"
  },
  "target": {
    "agent_id": "inventory-agent-prod-001",
    "endpoint": "/v1/message:send"
  },
  "details": {
    "message_id": "msg-abc123",
    "task_id": "task-8a7b6c5d",
    "status": "success",
    "processing_time_ms": 1247
  },
  "compliance": {
    "gdpr_compliant": true,
    "pci_compliant": true,
    "data_classification": "business"
  }
}
```

### 3.5.2 安全培训体系

| 培训类型 | 目标人群 | 内容 | 频率 |
|----------|----------|------|------|
| 安全意识 | 全体员工 | 钓鱼识别、密码安全 | 年度 |
| 安全开发 | 开发人员 | OWASP Top10、安全编码 | 季度 |
| 安全运维 | 运维人员 | 应急响应、安全配置 | 季度 |
| 合规培训 | 管理层 | 法规要求、合规义务 | 年度 |

## 📚 拓展学习资源
- **SOC2认证**: https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/soc2.html
- **ISO 27001**: https://www.iso.org/isoiec-27001-information-security.html
- **审计日志最佳实践**: https://www.ibm.com/docs/en/qsip/7.4?topic=services-audit-log-best-practices

---

"""

# 更新第五章内容
chapter5_new_content = """# 第五章：性能优化策略

## 5.1 性能瓶颈分析

| 瓶颈类型 | 表现症状 | 根因分析 | 影响范围 |
|----------|----------|----------|----------|
| **网络延迟** | P99延迟高 | 跨区域通信、网络拥塞 | 全局 |
| **消息处理** | 队列积压 | 消息处理速度慢 | 消息层 |
| **资源争用** | CPU/内存飙升 | 并发请求过高 | 计算层 |
| **数据库瓶颈** | 查询慢 | 索引缺失、锁竞争 | 数据层 |
| **序列化开销** | CPU占用高 | JSON序列化耗时 | 传输层 |
| **缓存失效** | DB压力突增 | 缓存命中率低 | 缓存层 |
| **连接池耗尽** | 无法建立连接 | 连接泄漏、配置不足 | 网络层 |
| **GC停顿** | 响应时间抖动 | 内存管理不当 | 运行时 |

## 📚 拓展学习资源
- **性能优化指南**: https://github.com/donnemartin/system-design-primer
- **分布式系统性能**: https://www.oreilly.com/library/view/designing-data-intensive/9781449373320/
- **网络优化**: https://blog.cloudflare.com/performance/

---

## 5.2 优化策略矩阵

| 优化维度 | 策略 | 技术实现 | 预期收益 | 投资回报 |
|----------|------|----------|----------|----------|
| **网络优化** | 边缘部署、协议优化 | HTTP/2、gRPC、QUIC | 延迟降低40% | 6个月 |
| **消息批量** | 批量聚合、背压控制 | Kafka+batching | 吞吐量提升2x | 12个月 |
| **缓存策略** | 多级缓存、预热机制 | Redis+LocalCache | P95延迟降低60% | 6个月 |
| **并发处理** | 异步队列、线程池 | Vert.x/Netty | 并发能力提升5x | 18个月 |
| **序列化** | 高效序列化格式 | Protobuf/FlatBuffers | 数据体积减少60% | 12个月 |
| **CDN加速** | 边缘缓存、内容预热 | CDN+预热 | 边缘延迟降低70% | 6个月 |
| **数据库优化** | 读写分离、索引优化 | Sharding+读写分离 | 查询速度提升2x | 12个月 |
| **负载均衡** | 智能流量分配 | Nginx/LVS/云LB | 流量分配优化99% | 6个月 |
| **熔断降级** | 故障隔离 | Resilience4j/Hystrix | 故障隔离100% | 6个月 |
| **GPU加速** | AI推理加速 | CUDA/TensorRT | 推理速度提升4x | 18个月 |
| **边缘计算** | 边缘部署 | K3s/KubeEdge | 边缘延迟降低60% | 24个月 |
| **压缩优化** | 传输压缩 | GZIP/Brotli/Snappy | 传输效率提升50% | 3个月 |

---

## 5.3 批量消息处理

### 5.3.1 批量请求格式

```json
{
  "jsonrpc": "2.0",
  "id": "batch-req-001",
  "method": "a2a.message.batch",
  "params": {
    "sender": "reporting-agent",
    "recipient": "inventory-agent",
    "messages": [
      {
        "id": "msg-001",
        "method": "inventory.check_stock",
        "params": {"sku": "SKU-ABC123"}
      },
      {
        "id": "msg-002",
        "method": "inventory.reserve_stock",
        "params": {"sku": "SKU-DEF456", "quantity": 10}
      }
    ],
    "timeout": 10000,
    "transactional": true
  }
}
```

### 5.3.2 批量响应格式

```json
{
  "jsonrpc": "2.0",
  "id": "batch-req-001",
  "result": {
    "success": true,
    "results": [
      {
        "id": "msg-001",
        "success": true,
        "result": {"sku": "SKU-ABC123", "quantity": 150, "location": "WH-A01"}
      },
      {
        "id": "msg-002",
        "success": true,
        "result": {"reserved": true, "reservation_id": "res-789"}
      }
    ],
    "processed_at": "2026-05-07T14:35:00Z",
    "processing_time_ms": 456
  }
}
```

## 📚 拓展学习资源
- **Redis缓存**: https://redis.io/
- **MessagePack**: https://msgpack.org/
- **异步编程**: https://realpython.com/async-io-python/
- **数据库优化**: https://use-the-index-luke.com/

---

## 5.4 高级优化技术

### 5.4.1 缓存策略深度解析

| 缓存层级 | 技术 | 特点 | 适用场景 |
|----------|------|------|----------|
| L1缓存 | 进程内存 | 最快、容量小 | 高频热点数据 |
| L2缓存 | Redis集群 | 较快、容量大 | 通用缓存 |
| L3缓存 | CDN | 边缘部署、全球覆盖 | 静态资源 |
| 本地缓存 | Caffeine/Guava | 进程内、低延迟 | 会话数据 |

### 5.4.2 预热机制

```json
{
  "warmup_config": {
    "enabled": true,
    "schedule": "0 3 * * *",
    "targets": [
      {"endpoint": "/v1/catalog/*", "method": "GET", "params": {"category": "hot"}},
      {"endpoint": "/v1/pricing/*", "method": "GET", "params": {"region": "all"}}
    ],
    "concurrency": 10,
    "timeout_ms": 5000
  }
}
```

### 5.4.3 性能监控指标

| 指标类型 | 关键指标 | 阈值 | 告警策略 |
|----------|----------|------|----------|
| 延迟 | P50/P90/P99 | <50ms/<100ms/<200ms | 超过阈值告警 |
| 吞吐量 | QPS/TPS | 根据业务 | 低于阈值告警 |
| 错误率 | 4xx/5xx比例 | <1%/<0.1% | 超过阈值告警 |
| 资源 | CPU/内存/磁盘 | <80% | 超过阈值告警 |
| 数据库 | 查询时间/连接数 | <100ms/<80% | 超过阈值告警 |

## 📚 拓展学习资源
- **Prometheus**: https://prometheus.io/
- **Grafana**: https://grafana.com/
- **OpenTelemetry**: https://opentelemetry.io/
- **Jaeger**: https://www.jaegertracing.io/

---

## 5.5 性能优化实践指南

### 5.5.1 优化流程

```
┌────────────────────────────────────────────────────────────┐
│                    性能优化流程                            │
├────────────────────────────────────────────────────────────┤
│                                                          │
│  监控发现瓶颈  ──►  性能分析定位  ──►  方案设计           │
│         │                  │                  │           │
│         ▼                  ▼                  ▼           │
│  指标收集     ──►  Profiler分析   ──►  方案评估         │
│         │                  │                  │           │
│         └──────────────────┼──────────────────┘           │
│                            ▼                             │
│                     实施优化                              │
│                            │                             │
│                            ▼                             │
│                     验证效果                              │
│                            │                             │
│                            ▼                             │
│                     持续监控                              │
│                                                          │
└────────────────────────────────────────────────────────────┘
```

### 5.5.2 优化优先级矩阵

| 优先级 | 优化项 | 实施难度 | 收益 | 推荐顺序 |
|--------|--------|----------|------|----------|
| P0 | 缓存优化 | 低 | 高 | 1 |
| P0 | 索引优化 | 低 | 高 | 2 |
| P1 | 批量处理 | 中 | 高 | 3 |
| P1 | 异步IO | 中 | 高 | 4 |
| P2 | 代码优化 | 高 | 中 | 5 |
| P2 | 架构重构 | 高 | 高 | 6 |

## 📚 拓展学习资源
- **性能调优实战**: https://github.com/brendangregg/perf-tools
- **JVM调优**: https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html
- **Go性能优化**: https://go.dev/doc/diagnostics
- **Python性能**: https://docs.python.org/3/library/profile.html

---

"""

# 使用正则表达式替换第三章内容
pattern_chapter3 = r'# 第三章：安全与合规体系.*?(?=# 第四章：)'
content = re.sub(pattern_chapter3, chapter3_new_content, content, flags=re.DOTALL)

# 使用正则表达式替换第五章内容
pattern_chapter5 = r'# 第五章：性能优化策略.*?(?=# 第六章：)'
content = re.sub(pattern_chapter5, chapter5_new_content, content, flags=re.DOTALL)

# 写入更新后的文件
with open(EXTERNAL_PROJECT_DIR  # was: A2A_ENTERPRISE_PPT.md, 'w', encoding='utf-8') as f:
    f.write(content)

print("第三章和第五章内容已更新完成！")
