#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
大模型决策层 SDK - V1.0
容灾路由：百炼(Bailian) / 千问(Qianwen) / Deepseek / 聚合AI + Ollama 本地兜底

设计原则：
  1. 云端优先，本地兜底 — 云端模型可用时走云端，全部熔断后自动降级到 Ollama 本地
  2. 健康探测 + 熔断恢复 — 每个 Provider 独立维护健康状态，失败计数→熔断→探测→恢复
  3. 可插拔路由策略 — Priority / RoundRobin / LatencyFirst 三种策略可选
  4. 响应格式统一 — 无论哪家模型返回，上层拿到同一结构
  5. 零配置即可跑 — 默认 Ollama 本地兜底可用，云端 Key 可选通过环境变量注入
"""

# ============================================================================
# 免责声明与AI使用规范
# ============================================================================
# 本文件仅供技术研究与学习交流使用，不得用于任何非法用途。
# 使用者须自行评估风险，因使用本文件导致的任何损失由使用者承担。
# ============================================================================

import os
import time
import json
import random
import threading
from typing import List, Dict, Optional, Any, Callable, Literal
from dataclasses import dataclass, field
from enum import Enum

try:
    import requests
except ImportError:  # 无 requests 时走降级模式
    requests = None


# ============================================================
# 基础类型
# ============================================================
class ProviderName(str, Enum):
    BAILIAN = "bailian"          # 阿里百炼（阿里云百炼平台）
    QIANWEN = "qianwen"          # 阿里千问（DashScope）
    DEEPSEEK = "deepseek"        # Deepseek
    AGGREGATED = "aggregated"    # 聚合AI（第三方聚合网关）
    OLLAMA = "ollama"            # Ollama 本地兜底


class RoutingStrategy(str, Enum):
    PRIORITY = "priority"            # 按优先级依次尝试（默认）
    ROUND_ROBIN = "round_robin"      # 轮询
    LATENCY_FIRST = "latency_first"  # 低延迟优先


@dataclass
class ProviderStatus:
    name: ProviderName
    healthy: bool = True
    consecutive_failures: int = 0
    last_success_at: float = 0.0
    last_failure_at: float = 0.0
    avg_latency_ms: float = 0.0
    total_requests: int = 0
    total_success: int = 0
    # 熔断参数
    circuit_open: bool = False
    circuit_open_at: float = 0.0
    half_open_probe_in_flight: bool = False


@dataclass
class LLMResponse:
    content: str
    provider: ProviderName
    model: str
    success: bool
    latency_ms: float
    error: Optional[str] = None
    token_usage: Optional[Dict[str, int]] = None
    raw: Optional[Any] = None


@dataclass
class ProviderConfig:
    name: ProviderName
    base_url: str
    api_key_env: str                # 环境变量名（缺 Key 时自动降级为不可用）
    default_model: str
    priority: int = 100             # 数值越大优先级越高
    timeout_sec: float = 30.0
    max_consecutive_failures: int = 5
    circuit_break_sec: float = 60.0
    enabled: bool = True
    # 用于健康探测的廉价请求
    probe_prompt: str = "请回复ok，不要输出其他内容"


# ============================================================
# 默认 Provider 配置
# ============================================================
DEFAULT_PROVIDERS: List[ProviderConfig] = [
    ProviderConfig(
        name=ProviderName.BAILIAN,
        base_url="https://bailian.aliyuncs.com/api/v1",
        api_key_env="BAILIAN_API_KEY",
        default_model=os.getenv("BAILIAN_MODEL", "qwen-plus"),
        priority=100,
    ),
    ProviderConfig(
        name=ProviderName.QIANWEN,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key_env="DASHSCOPE_API_KEY",
        default_model=os.getenv("QIANWEN_MODEL", "qwen-plus"),
        priority=90,
    ),
    ProviderConfig(
        name=ProviderName.DEEPSEEK,
        base_url="https://api.deepseek.com/v1",
        api_key_env="DEEPSEEK_API_KEY",
        default_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        priority=80,
    ),
    ProviderConfig(
        name=ProviderName.AGGREGATED,
        base_url=os.getenv("AGGREGATED_AI_BASEURL", "https://api.example-aggregated.com/v1"),
        api_key_env="AGGREGATED_AI_API_KEY",
        default_model=os.getenv("AGGREGATED_AI_MODEL", "auto"),
        priority=70,
    ),
    ProviderConfig(
        name=ProviderName.OLLAMA,
        base_url=os.getenv("OLLAMA_BASEURL", "http://localhost:11434"),
        api_key_env="",  # Ollama 不需要 Key
        default_model=os.getenv("OLLAMA_MODEL", "qwen3:8b"),
        priority=10,    # 优先级最低，仅兜底
    ),
]


# ============================================================
# Provider 请求适配层
# ============================================================
class BaseProviderClient:
    """所有 Provider 客户端的基类，抽象统一的 chat 接口"""

    def __init__(self, cfg: ProviderConfig):
        self.cfg = cfg

    @property
    def api_key(self) -> Optional[str]:
        if not self.cfg.api_key_env:
            return ""
        return os.getenv(self.cfg.api_key_env)

    def is_configured(self) -> bool:
        """是否配置了必要的凭据（Ollama 无需 Key，默认 True）"""
        if self.cfg.name == ProviderName.OLLAMA:
            return True
        return bool(self.api_key)

    def chat(
        self,
        messages: List[Dict[str, str]],
        *,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        raise NotImplementedError


class BailianClient(BaseProviderClient):
    """阿里百炼平台客户端"""

    def chat(self, messages, *, model=None, temperature=0.7, max_tokens=1024):
        model = model or self.cfg.default_model
        url = f"{self.cfg.base_url}/apps/{self.api_key}/completion" \
            if not self.api_key.startswith("sk-") else \
            f"{self.cfg.base_url}/chat/completions"
        # 百炼同时支持两种风格：尝试走 OpenAI 兼容模式
        return self._openai_style(url, messages, model, temperature, max_tokens)

    def _openai_style(self, url, messages, model, temperature, max_tokens):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        t0 = time.time()
        resp = requests.post(url, headers=headers, json=payload, timeout=self.cfg.timeout_sec)
        latency = (time.time() - t0) * 1000
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage")
        return LLMResponse(
            content=content,
            provider=self.cfg.name,
            model=model,
            success=True,
            latency_ms=latency,
            token_usage=usage,
            raw=data,
        )


class QianwenClient(BaseProviderClient):
    """阿里千问（DashScope 兼容 OpenAI 模式）"""

    def chat(self, messages, *, model=None, temperature=0.7, max_tokens=1024):
        model = model or self.cfg.default_model
        url = f"{self.cfg.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        t0 = time.time()
        resp = requests.post(url, headers=headers, json=payload, timeout=self.cfg.timeout_sec)
        latency = (time.time() - t0) * 1000
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return LLMResponse(
            content=content,
            provider=self.cfg.name,
            model=model,
            success=True,
            latency_ms=latency,
            token_usage=data.get("usage"),
            raw=data,
        )


class DeepseekClient(BaseProviderClient):
    """Deepseek API 客户端"""

    def chat(self, messages, *, model=None, temperature=0.7, max_tokens=1024):
        model = model or self.cfg.default_model
        url = f"{self.cfg.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        t0 = time.time()
        resp = requests.post(url, headers=headers, json=payload, timeout=self.cfg.timeout_sec)
        latency = (time.time() - t0) * 1000
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return LLMResponse(
            content=content,
            provider=self.cfg.name,
            model=model,
            success=True,
            latency_ms=latency,
            token_usage=data.get("usage"),
            raw=data,
        )


class AggregatedAIClient(BaseProviderClient):
    """聚合AI网关（格式假定 OpenAI 兼容，实际可按厂商文档调整）"""

    def chat(self, messages, *, model=None, temperature=0.7, max_tokens=1024):
        model = model or self.cfg.default_model
        url = f"{self.cfg.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        t0 = time.time()
        resp = requests.post(url, headers=headers, json=payload, timeout=self.cfg.timeout_sec)
        latency = (time.time() - t0) * 1000
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return LLMResponse(
            content=content,
            provider=self.cfg.name,
            model=model,
            success=True,
            latency_ms=latency,
            token_usage=data.get("usage"),
            raw=data,
        )


class OllamaLocalClient(BaseProviderClient):
    """Ollama 本地兜底客户端 — 零依赖网络，离线仍可用"""

    def is_configured(self) -> bool:
        return True

    def chat(self, messages, *, model=None, temperature=0.7, max_tokens=1024):
        model = model or self.cfg.default_model
        # 把 messages 合并为 prompt（Ollama generate 接口兼容）
        prompt = self._messages_to_prompt(messages)
        system_prompt = None
        if messages and messages[0].get("role") == "system":
            system_prompt = messages[0]["content"]
        url = f"{self.cfg.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        if system_prompt:
            payload["system"] = system_prompt
        t0 = time.time()
        if requests is None:
            # 无 requests 库时，返回离线兜底模拟响应
            content = self._offline_mock_response(messages)
            latency = (time.time() - t0) * 1000
            return LLMResponse(
                content=content,
                provider=self.cfg.name,
                model=model,
                success=True,
                latency_ms=latency,
                error=None,
                token_usage={"prompt_tokens": len(prompt), "completion_tokens": len(content)},
                raw=None,
            )
        try:
            resp = requests.post(url, json=payload, timeout=self.cfg.timeout_sec)
            latency = (time.time() - t0) * 1000
            if resp.status_code != 200:
                raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
            data = resp.json()
            content = data.get("response", "").strip()
            return LLMResponse(
                content=content,
                provider=self.cfg.name,
                model=model,
                success=True,
                latency_ms=latency,
                token_usage={
                    "prompt_tokens": data.get("prompt_eval_count", 0),
                    "completion_tokens": data.get("eval_count", 0),
                },
                raw=data,
            )
        except Exception as e:
            # Ollama 也不可用时，仍然返回离线兜底保证不崩
            latency = (time.time() - t0) * 1000
            content = self._offline_mock_response(messages)
            return LLMResponse(
                content=content,
                provider=self.cfg.name,
                model=f"{model}-offline-mock",
                success=True,
                latency_ms=latency,
                error=f"ollama_unavailable: {e}",
                token_usage=None,
                raw=None,
            )

    @staticmethod
    def _messages_to_prompt(messages: List[Dict[str, str]]) -> str:
        parts = []
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            if role == "system":
                continue  # system 单独走 payload.system
            parts.append(f"{role.upper()}: {content}")
        return "\n\n".join(parts)

    @staticmethod
    def _offline_mock_response(messages: List[Dict[str, str]]) -> str:
        """完全离线时的模拟响应 — 保障链路不断"""
        last_user = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                last_user = m.get("content", "")
                break
        if "你好" in last_user or "hello" in last_user.lower():
            return "你好！我是本地兜底 LLM（离线模拟模式），云端不可用时我仍可工作。"
        if "计划" in last_user or "规划" in last_user:
            return "（离线规划）步骤1. 分析目标；步骤2. 拆解子任务；步骤3. 执行并反馈。"
        if "ok" in last_user.lower():
            return "ok"
        return f"（Ollama 离线兜底响应）收到：{last_user[:50]}"


# ============================================================
# Provider → Client 映射工厂
# ============================================================
def _make_client(cfg: ProviderConfig) -> BaseProviderClient:
    _MAP = {
        ProviderName.BAILIAN: BailianClient,
        ProviderName.QIANWEN: QianwenClient,
        ProviderName.DEEPSEEK: DeepseekClient,
        ProviderName.AGGREGATED: AggregatedAIClient,
        ProviderName.OLLAMA: OllamaLocalClient,
    }
    cls = _MAP.get(cfg.name)
    if not cls:
        raise ValueError(f"Unknown provider: {cfg.name}")
    return cls(cfg)


# ============================================================
# 主 SDK：LLM Decision Router
# ============================================================
class LLMDecisionSDK:
    """
    大模型决策层 SDK（容灾路由 + 本地兜底）

    用法：
        sdk = LLMDecisionSDK()
        resp = sdk.chat([{"role":"user","content":"你好"}])
        print(resp.content, resp.provider.value)
    """

    def __init__(
        self,
        *,
        providers: Optional[List[ProviderConfig]] = None,
        strategy: RoutingStrategy = RoutingStrategy.PRIORITY,
        cloud_probe_interval_sec: float = 60.0,
        enable_background_health_check: bool = True,
    ):
        self._providers_cfg: Dict[ProviderName, ProviderConfig] = {}
        self._clients: Dict[ProviderName, BaseProviderClient] = {}
        self._status: Dict[ProviderName, ProviderStatus] = {}
        self._strategy = strategy
        self._lock = threading.RLock()
        self._rr_cursor = 0  # round-robin 游标

        provider_list = providers or DEFAULT_PROVIDERS
        for cfg in provider_list:
            if not cfg.enabled:
                continue
            self._providers_cfg[cfg.name] = cfg
            self._clients[cfg.name] = _make_client(cfg)
            self._status[cfg.name] = ProviderStatus(name=cfg.name)

        self._stop_evt = threading.Event()
        self._health_thread: Optional[threading.Thread] = None
        self._cloud_probe_interval = cloud_probe_interval_sec
        if enable_background_health_check:
            self._start_health_check_loop()

    # ------------------------------------------------------------
    # 生命周期
    # ------------------------------------------------------------
    def _start_health_check_loop(self):
        def _loop():
            while not self._stop_evt.is_set():
                try:
                    self._health_probe_all()
                except Exception:
                    pass
                self._stop_evt.wait(self._cloud_probe_interval)

        self._health_thread = threading.Thread(target=_loop, daemon=True)
        self._health_thread.start()

    def close(self):
        self._stop_evt.set()

    # ------------------------------------------------------------
    # 健康探测 + 熔断/恢复
    # ------------------------------------------------------------
    def _health_probe_all(self):
        for name in list(self._providers_cfg.keys()):
            if name == ProviderName.OLLAMA:
                continue  # Ollama 不做周期性探测，只在被选中时现场测
            with self._lock:
                st = self._status[name]
                cfg = self._providers_cfg[name]
                now = time.time()
                # 已熔断且冷却期过 → half-open，发送探测
                if st.circuit_open and (now - st.circuit_open_at) >= cfg.circuit_break_sec:
                    st.half_open_probe_in_flight = True
                elif st.circuit_open:
                    continue
                # 如果没配置 Key，跳过
                if not self._clients[name].is_configured():
                    st.healthy = False
                    continue
            try:
                self._try_chat_internal(
                    name,
                    [{"role": "user", "content": cfg.probe_prompt}],
                    max_tokens=8,
                    _is_probe=True,
                )
            except Exception:
                pass

    def _record_success(self, name: ProviderName, latency_ms: float):
        with self._lock:
            st = self._status[name]
            cfg = self._providers_cfg[name]
            st.healthy = True
            st.circuit_open = False
            st.half_open_probe_in_flight = False
            st.consecutive_failures = 0
            st.last_success_at = time.time()
            st.total_requests += 1
            st.total_success += 1
            # EWMA 延迟
            if st.avg_latency_ms <= 0:
                st.avg_latency_ms = latency_ms
            else:
                alpha = 0.2
                st.avg_latency_ms = (1 - alpha) * st.avg_latency_ms + alpha * latency_ms

    def _record_failure(self, name: ProviderName):
        with self._lock:
            st = self._status[name]
            cfg = self._providers_cfg[name]
            st.consecutive_failures += 1
            st.last_failure_at = time.time()
            st.total_requests += 1
            if st.consecutive_failures >= cfg.max_consecutive_failures:
                st.healthy = False
                st.circuit_open = True
                st.circuit_open_at = time.time()
                st.half_open_probe_in_flight = False

    # ------------------------------------------------------------
    # 路由选择
    # ------------------------------------------------------------
    def _select_candidates(self) -> List[ProviderName]:
        with self._lock:
            configured = [
                n for n, c in self._clients.items()
                if (n == ProviderName.OLLAMA) or c.is_configured()
            ]
            # 过滤状态：健康，或 half-open 可探测，且未熔断（half-open 例外）
            candidates = []
            for n in configured:
                st = self._status[n]
                cfg = self._providers_cfg[n]
                if st.circuit_open:
                    # 冷却期过 → 允许单个探测
                    now = time.time()
                    if (now - st.circuit_open_at) >= cfg.circuit_break_sec and \
                            not st.half_open_probe_in_flight:
                        st.half_open_probe_in_flight = True
                        candidates.append(n)
                    continue
                candidates.append(n)

            if not candidates:
                # 全熔断时，强制退回 Ollama（哪怕本地也走 mock 兜底）
                if ProviderName.OLLAMA in configured:
                    return [ProviderName.OLLAMA]
                return list(self._clients.keys())  # 再不行全试一遍

        # 按策略排序
        if self._strategy == RoutingStrategy.PRIORITY:
            candidates.sort(
                key=lambda n: (-self._providers_cfg[n].priority,
                               self._status[n].avg_latency_ms or 1e9)
            )
        elif self._strategy == RoutingStrategy.ROUND_ROBIN:
            with self._lock:
                self._rr_cursor = (self._rr_cursor + 1) % max(1, len(candidates))
                cur = self._rr_cursor
            candidates = candidates[cur:] + candidates[:cur]
        elif self._strategy == RoutingStrategy.LATENCY_FIRST:
            candidates.sort(key=lambda n: (self._status[n].avg_latency_ms or 1e9,
                                           -self._providers_cfg[n].priority))
        # 保证兜底 Ollama 一定包含在候选尾部
        if ProviderName.OLLAMA in self._clients and ProviderName.OLLAMA not in candidates:
            candidates.append(ProviderName.OLLAMA)
        return candidates

    # ------------------------------------------------------------
    # 核心 chat 接口
    # ------------------------------------------------------------
    def _try_chat_internal(
        self,
        name: ProviderName,
        messages: List[Dict[str, str]],
        *,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        _is_probe: bool = False,
    ) -> LLMResponse:
        client = self._clients[name]
        try:
            resp = client.chat(messages, model=model, temperature=temperature,
                               max_tokens=max_tokens)
        except Exception as e:
            self._record_failure(name)
            if _is_probe:
                raise
            return LLMResponse(
                content="",
                provider=name,
                model=model or self._providers_cfg[name].default_model,
                success=False,
                latency_ms=0.0,
                error=str(e),
            )
        # 即使返回码 200，也要判断业务是否真的成功
        if not resp.success:
            self._record_failure(name)
            return resp
        self._record_success(name, resp.latency_ms)
        return resp

    def chat(
        self,
        messages: List[Dict[str, str]],
        *,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        preferred_provider: Optional[ProviderName] = None,
        on_provider_fail: Optional[Callable[[ProviderName, str], None]] = None,
    ) -> LLMResponse:
        """
        发送一次聊天请求，自动容灾降级到可用 provider。

        Args:
            messages: OpenAI 风格消息列表
            model: 指定模型名（不传则使用 provider 的 default_model）
            temperature: 采样温度
            max_tokens: 最大输出 token
            preferred_provider: 优先尝试的 provider（跳过路由排序，放第一位）
            on_provider_fail: 某个 provider 失败时的回调 fn(provider, error_msg)

        Returns:
            LLMResponse：保证 success=True（最差是 Ollama offline-mock）
        """
        candidates = self._select_candidates()
        if preferred_provider and preferred_provider in candidates:
            candidates.remove(preferred_provider)
            candidates.insert(0, preferred_provider)

        last_error = ""
        for name in candidates:
            resp = self._try_chat_internal(
                name, messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            if resp.success:
                return resp
            last_error = resp.error or "unknown"
            if on_provider_fail:
                try:
                    on_provider_fail(name, last_error)
                except Exception:
                    pass

        # 理论上不会到这里（Ollama offline-mock 永真），保险兜底
        return LLMResponse(
            content="（SDK 最终兜底）所有模型均不可用，已返回空安全响应。",
            provider=ProviderName.OLLAMA,
            model="offline-fallback",
            success=True,
            latency_ms=0.0,
            error=last_error or "all_providers_failed",
        )

    # ------------------------------------------------------------
    # 便捷封装
    # ------------------------------------------------------------
    def ask(self, prompt: str, *, system: Optional[str] = None, **kwargs) -> LLMResponse:
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": prompt})
        return self.chat(msgs, **kwargs)

    # ------------------------------------------------------------
    # 可观测性
    # ------------------------------------------------------------
    def status_report(self) -> Dict[str, Any]:
        with self._lock:
            report: Dict[str, Any] = {
                "strategy": self._strategy.value,
                "providers": {},
            }
            for n, st in self._status.items():
                cfg = self._providers_cfg[n]
                cli = self._clients[n]
                report["providers"][n.value] = {
                    "priority": cfg.priority,
                    "default_model": cfg.default_model,
                    "configured": cli.is_configured(),
                    "healthy": st.healthy,
                    "circuit_open": st.circuit_open,
                    "consecutive_failures": st.consecutive_failures,
                    "total_requests": st.total_requests,
                    "success_rate": (
                        f"{st.total_success / max(1, st.total_requests) * 100:.1f}%"
                    ),
                    "avg_latency_ms": f"{st.avg_latency_ms:.1f}ms",
                    "last_success_sec_ago": (
                        f"{time.time() - st.last_success_at:.0f}s"
                        if st.last_success_at > 0 else "never"
                    ),
                }
            return report

    def print_status(self):
        rep = self.status_report()
        print("[LLM Decision SDK] 容灾路由状态:")
        print(f"  · 路由策略: {rep['strategy']}")
        for name, info in rep["providers"].items():
            mark = "✅" if (info["configured"] and info["healthy"] and not info["circuit_open"]) else \
                   "🟡" if info["circuit_open"] else "❌"
            cfg_line = f"{mark} {name:<12} pri={info['priority']:>3} | model={info['default_model']:<18} | configured={'Y' if info['configured'] else 'N'}"
            print(f"  {cfg_line}")
            print(f"      healthy={info['healthy']} circuit_open={info['circuit_open']} "
                  f"fail={info['consecutive_failures']} req={info['total_requests']} "
                  f"succ={info['success_rate']} lat={info['avg_latency_ms']} last={info['last_success_sec_ago']}")


# ============================================================
# Dry-run 自测
# ============================================================
def _dry_run():
    print("=" * 70)
    print("  LLM Decision SDK — 容灾路由 Dry-run")
    print("=" * 70)
    sdk = LLMDecisionSDK(
        strategy=RoutingStrategy.PRIORITY,
        enable_background_health_check=False,  # dry-run 不启动后台线程
    )
    sdk.print_status()

    questions = [
        "你好",
        "帮我规划一下今天的机器人巡检任务",
        "ok",
    ]
    for q in questions:
        print(f"\n>>> 用户：{q}")
        t0 = time.time()
        resp = sdk.ask(q)
        dt = (time.time() - t0) * 1000
        print(f"<<< [{resp.provider.value}/{resp.model}] "
              f"latency={resp.latency_ms:.0f}ms(wall={dt:.0f}ms) "
              f"success={resp.success}")
        if resp.error:
            print(f"    error: {resp.error}")
        print(f"    {resp.content}")

    print("\n" + "-" * 70)
    sdk.print_status()
    sdk.close()
    print("=" * 70)
    print("  Dry-run 完成")
    print("=" * 70)


if __name__ == "__main__":
    _dry_run()
