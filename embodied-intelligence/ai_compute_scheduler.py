#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI算力调度模块 - V1.0
================================================================
新增内容：
  1. ComputeNode（算力节点数据类）
  2. ComputeCluster（算力集群）
  3. ComputeScheduler（算力调度器）
  4. 远景星河基地配置（12万平米，百万卡，百万P，2GW，67%绿电）
  5. 曙光8000登峰配置（十万卡全国产，10万亿参数，400+模型）
  6. create_compute_scheduler（工厂函数）

核心能力：
  - 多算力集群统一管理与调度
  - 按模型规模/显存/延迟需求智能分配节点
  - 绿电比例追踪与负载均衡
  - 全国产化算力链支持
"""

import time
import threading
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class NodeStatus(Enum):
    ONLINE = "online"
    BUSY = "busy"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class ComputeTier(Enum):
    """算力等级。"""
    EDGE = "edge"              # 边缘端
    LOCAL = "local"            # 本地工作站
    DATACENTER = "datacenter"  # 数据中心
    SUPERCOMPUTER = "super"    # 超算中心


@dataclass
class ComputeNode:
    """算力节点。"""
    node_id: str
    name: str
    tier: ComputeTier
    gpu_count: int
    gpu_memory_gb: float
    total_flops_pflops: float
    available_flops_pflops: float
    green_energy_ratio: float
    location: str
    status: NodeStatus = NodeStatus.ONLINE
    max_model_params_b: float = 0.0
    current_load_pct: float = 0.0
    domestic_only: bool = False


@dataclass
class ComputeRequest:
    """算力请求。"""
    request_id: str
    model_params_b: float
    required_gpu_memory_gb: float
    required_flops_pflops: float
    max_latency_ms: float
    prefer_domestic: bool = False
    prefer_green: bool = True


@dataclass
class SchedulerResult:
    """调度结果。"""
    request_id: str
    assigned_node: Optional[ComputeNode]
    success: bool
    reason: str = ""
    estimated_latency_ms: float = 0.0


class ComputeCluster:
    """算力集群。"""

    def __init__(self, cluster_id: str, name: str):
        self.cluster_id = cluster_id
        self.name = name
        self.nodes: List[ComputeNode] = []

    def add_node(self, node: ComputeNode) -> None:
        self.nodes.append(node)

    def available_nodes(self) -> List[ComputeNode]:
        return [n for n in self.nodes if n.status in (NodeStatus.ONLINE,)]

    def total_capacity_pflops(self) -> float:
        return sum(n.total_flops_pflops for n in self.nodes)

    def available_capacity_pflops(self) -> float:
        return sum(n.available_flops_pflops for n in self.available_nodes())


class ComputeScheduler:
    """算力调度器。

    管理多个算力集群，按请求智能分配节点。
    """

    def __init__(self):
        self.clusters: Dict[str, ComputeCluster] = {}
        self._lock = threading.Lock()
        self._request_count = 0

    def register_cluster(self, cluster: ComputeCluster) -> None:
        with self._lock:
            self.clusters[cluster.cluster_id] = cluster

    def schedule(self, request: ComputeRequest) -> SchedulerResult:
        with self._lock:
            self._request_count += 1
            candidates = self._find_candidates(request)
            if not candidates:
                return SchedulerResult(
                    request_id=request.request_id,
                    assigned_node=None,
                    success=False,
                    reason="no_available_node",
                )
            best = self._select_best(candidates, request)
            best.current_load_pct = min(95.0, best.current_load_pct + 10.0)
            best.available_flops_pflops = max(
                0.0, best.available_flops_pflops - request.required_flops_pflops)
            if best.current_load_pct > 80.0:
                best.status = NodeStatus.BUSY
            return SchedulerResult(
                request_id=request.request_id,
                assigned_node=best,
                success=True,
                reason="assigned",
                estimated_latency_ms=self._estimate_latency(best, request),
            )

    def release(self, node_id: str, flops_released: float) -> None:
        with self._lock:
            for cluster in self.clusters.values():
                for node in cluster.nodes:
                    if node.node_id == node_id:
                        node.available_flops_pflops = min(
                            node.total_flops_pflops,
                            node.available_flops_pflops + flops_released)
                        node.current_load_pct = max(0.0, node.current_load_pct - 10.0)
                        if node.current_load_pct < 80.0:
                            node.status = NodeStatus.ONLINE
                        return

    def get_status(self) -> Dict[str, Any]:
        with self._lock:
            all_nodes = [n for c in self.clusters.values() for n in c.nodes]
            return {
                "total_clusters": len(self.clusters),
                "total_nodes": len(all_nodes),
                "online_nodes": sum(1 for n in all_nodes if n.status == NodeStatus.ONLINE),
                "total_capacity_pflops": sum(n.total_flops_pflops for n in all_nodes),
                "available_pflops": sum(n.available_flops_pflops for n in all_nodes),
                "avg_green_ratio": (
                    sum(n.green_energy_ratio for n in all_nodes) / len(all_nodes)
                    if all_nodes else 0.0),
                "domestic_nodes": sum(1 for n in all_nodes if n.domestic_only),
                "total_requests": self._request_count,
            }

    def _find_candidates(self, request: ComputeRequest) -> List[ComputeNode]:
        candidates = []
        for cluster in self.clusters.values():
            for node in cluster.available_nodes():
                if request.prefer_domestic and not node.domestic_only:
                    continue
                if node.gpu_memory_gb < request.required_gpu_memory_gb:
                    continue
                if node.available_flops_pflops < request.required_flops_pflops:
                    continue
                if node.max_model_params_b < request.model_params_b:
                    continue
                candidates.append(node)
        return candidates

    @staticmethod
    def _select_best(candidates: List[ComputeNode],
                     request: ComputeRequest) -> ComputeNode:
        if request.prefer_green:
            return max(candidates, key=lambda n: (n.green_energy_ratio, -n.current_load_pct))
        return min(candidates, key=lambda n: n.current_load_pct)

    @staticmethod
    def _estimate_latency(node: ComputeNode, request: ComputeRequest) -> float:
        if node.available_flops_pflops <= 0:
            return float("inf")
        base = (request.required_flops_pflops / node.available_flops_pflops) * 100
        return max(request.max_latency_ms * 0.1, base)


def create_compute_scheduler() -> ComputeScheduler:
    """工厂函数：创建算力调度器并注册真实算力集群。"""
    scheduler = ComputeScheduler()

    # 远景星河算力基地
    envision_cluster = ComputeCluster(
        cluster_id="envision_starriver",
        name="远景星河绿色算力基地",
    )
    envision_cluster.add_node(ComputeNode(
        node_id="envision_main",
        name="远景星河主算力中心",
        tier=ComputeTier.SUPERCOMPUTER,
        gpu_count=1000000,
        gpu_memory_gb=80000000.0,
        total_flops_pflops=1000000.0,
        available_flops_pflops=1000000.0,
        green_energy_ratio=0.67,
        location="内蒙古乌兰察布",
        max_model_params_b=10000.0,
        domestic_only=False,
    ))
    scheduler.register_cluster(envision_cluster)

    # 曙光8000登峰
    dawn_cluster = ComputeCluster(
        cluster_id="sugon_8000",
        name="曙光8000登峰全国产算力平台",
    )
    dawn_cluster.add_node(ComputeNode(
        node_id="sugon_8000_main",
        name="曙光8000登峰超算节点",
        tier=ComputeTier.SUPERCOMPUTER,
        gpu_count=100000,
        gpu_memory_gb=8000000.0,
        total_flops_pflops=100000.0,
        available_flops_pflops=100000.0,
        green_energy_ratio=0.40,
        location="全国产化算力链",
        max_model_params_b=10000.0,
        domestic_only=True,
    ))
    scheduler.register_cluster(dawn_cluster)

    return scheduler


if __name__ == "__main__":
    sched = create_compute_scheduler()
    status = sched.get_status()
    print(f"算力调度器已创建: {status['total_clusters']}个集群, "
          f"{status['total_nodes']}个节点, "
          f"总算力{status['total_capacity_pflops']} PFLOPS")
