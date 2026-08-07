# 向量数据库学习笔记

## 一、向量数据库基础

### 1.1 什么是向量数据库

向量数据库是专门用于存储、索引和检索高维向量数据的数据库系统。它是RAG系统的核心组件之一。

### 1.2 核心概念

- **向量嵌入（Vector Embedding）**：将文本、图像等数据转换为高维向量
- **相似度搜索**：在向量空间中查找与查询向量最相似的向量
- **距离度量**：用于衡量向量之间的相似程度

### 1.3 常用距离度量

| 距离类型 | 计算公式 | 适用场景 |
|----------|----------|----------|
| 欧氏距离 | √Σ(xi-yi)² | 连续数据、图像特征 |
| 余弦相似度 | (x·y)/(\|x\|\|y\|) | 文本相似度、方向比较 |
| 曼哈顿距离 | Σ\|xi-yi\| | 稀疏数据、高维空间 |

---

## 二、FAISS 入门

### 2.1 FAISS 简介

FAISS（Facebook AI Similarity Search）是Facebook开发的高效相似性搜索库。

### 2.2 安装与使用

```bash
pip install faiss-cpu  # CPU版本
# 或
pip install faiss-gpu  # GPU版本
```

### 2.3 基本操作

```python
import faiss
import numpy as np

# 创建索引
dimension = 768
index = faiss.IndexFlatL2(dimension)

# 添加向量
vectors = np.random.rand(1000, dimension).astype('float32')
index.add(vectors)

# 搜索
query = np.random.rand(1, dimension).astype('float32')
distances, indices = index.search(query, k=5)
```

### 2.4 索引类型选择

| 索引类型 | 特点 | 适用场景 |
|----------|------|----------|
| IndexFlatL2 | 精确搜索，无近似 | 小规模数据 |
| IndexIVFFlat | 倒排索引，近似搜索 | 中等规模 |
| IndexIVFPQ | 乘积量化压缩 | 大规模数据 |
| IndexHNSW | 层次导航小世界 | 高维数据 |

---

## 三、生产环境优化

### 3.1 索引优化策略

1. **选择合适的索引类型**：根据数据规模和精度要求选择
2. **训练量化参数**：使用代表性数据训练PQ参数
3. **设置合理的nlist**：通常设为数据量的平方根

### 3.2 性能调优

```python
# 设置GPU资源
res = faiss.StandardGpuResources()
gpu_index = faiss.index_cpu_to_gpu(res, 0, index)

# 优化搜索参数
index.nprobe = 10  # 增加搜索精度
```

---

## 四、常见问题

### Q1：索引文件过大怎么办？

**解决方案**：
- 使用量化索引（如 IndexIVFPQ）
- 降低向量维度
- 考虑分布式存储

### Q2：搜索精度不够怎么办？

**解决方案**：
- 增加 nprobe 参数
- 使用更精确的索引类型
- 优化嵌入模型

---

*学习笔记更新日期：2026年5月*
