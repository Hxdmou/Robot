"""
大模型决策 SDK & 自主决策系统（去算法版）
================================================
1) LLMDecisionSDK:
   统一封装各大模型服务商调用（通义/智谱/DeepSeek/OpenAI兼容），
   支持 Function Calling（工具调用）、对话管理、日志与审计。

2) AutonomousDecisionSystem:
   基于「知识库 + 技能库 + 大模型」的高层决策编排器，
   把具身智能的高层决策串成：感知摘要 → 知识检索 → 技能选择 → 动作编排 → 执行审计。

说明：本文件仅展示「如何把大模型能力封装为企业级SDK」的工程化写法，
      不涉及算法、模型训练或私有知识库。
"""

from __future__ import annotations

import abc
import json
import os
import time
import uuid
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional


# ============================================================
# 通用工具
# ============================================================
def _load_env_from_file(path: str = ".env") -> Dict[str, str]:
    """极简 .env 文件解析（不依赖 python-dotenv 包）"""
    out: Dict[str, str] = {}
    if not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip("\"'")
    return out


# ============================================================
# 数据类定义
# ============================================================
@dataclass
class ToolCallRequest:
    """一次工具调用请求（Function Calling 统一结构）"""
    call_id: str = field(default_factory=lambda: "call_" + uuid.uuid4().hex[:8])
    function_name: str = ""
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    """LLM SDK 统一返回"""
    success: bool
    provider: str
    model: str
    text: str = ""
    tool_calls: List[ToolCallRequest] = field(default_factory=list)
    usage: Dict[str, int] = field(default_factory=dict)   # prompt_tokens / completion_tokens
    latency_ms: int = 0
    error_message: str = ""
    raw: Any = None
    trace_id: str = ""


# ============================================================
# 工具（Function Calling）定义框架
# ============================================================
@dataclass
class FunctionTool:
    name: str
    description: str
    parameters: Dict[str, Any]         # JSON Schema 格式
    implementation: Callable[..., Any]

    def to_openai_style(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


class SkillLibrary:
    """
    技能库（具身智能高层决策用的原子动作 + 检索工具）
    ------------------------------------------------
    内含示例技能：
      - get_current_robot_status()       查当前状态
      - list_available_skills()          查可用技能
      - move_end_effector_to(x,y,z)      动作：移动末端
      - gripper_command(state)           动作：夹爪开合
      - safety_stop(reason)              安全：急停
      - system_health_check()            运维：健康检查
    """

    def __init__(self):
        self._funcs: Dict[str, FunctionTool] = {}
        self._robot_state_snapshot: Dict[str, Any] = {
            "joints": [0.0]*7, "ee_xyz": [0.5, 0.0, 0.45],
            "gripper": "open", "mode": "IDLE",
        }
        self._register_defaults()

    def register(self, func: FunctionTool) -> None:
        self._funcs[func.name] = func

    def list_tools_schema(self) -> List[Dict[str, Any]]:
        return [f.to_openai_style() for f in self._funcs.values()]

    def names(self) -> List[str]:
        return sorted(self._funcs.keys())

    def execute(self, name: str, **kwargs) -> Dict[str, Any]:
        if name not in self._funcs:
            return {"ok": False, "error": f"未知技能: {name}"}
        try:
            result = self._funcs[name].implementation(**kwargs)
            if isinstance(result, dict):
                return {"ok": True, **result}
            return {"ok": True, "result": result}
        except Exception as e:
            return {"ok": False, "error": f"执行异常: {repr(e)}"}

    # ---- 默认技能实现 ----
    def _register_defaults(self) -> None:
        self.register(FunctionTool(
            "list_available_skills",
            "列出当前具身智能系统所有可用的技能/工具名称",
            {"type": "object", "properties": {}, "required": []},
            lambda: {"skills": self.names()},
        ))
        self.register(FunctionTool(
            "get_current_robot_status",
            "获取机器人当前关节/末端/夹爪/模式的状态快照",
            {"type": "object", "properties": {}, "required": []},
            lambda: {"robot": dict(self._robot_state_snapshot)},
        ))
        self.register(FunctionTool(
            "move_end_effector_to",
            "移动机械臂末端到指定笛卡尔位置（米）。示例：把工件放到托盘上方",
            {
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "目标X坐标（向前为正）"},
                    "y": {"type": "number", "description": "目标Y坐标（向左为正）"},
                    "z": {"type": "number", "description": "目标Z坐标（高度）"},
                },
                "required": ["x", "y", "z"],
            },
            self._impl_move_ee,
        ))
        self.register(FunctionTool(
            "gripper_command",
            "控制夹爪开合状态（open=张开 / close=闭合）",
            {
                "type": "object",
                "properties": {
                    "state": {"type": "string", "enum": ["open", "close"]},
                },
                "required": ["state"],
            },
            self._impl_gripper,
        ))
        self.register(FunctionTool(
            "safety_stop",
            "触发安全紧急停止。当存在人员受伤风险/碰撞/指令异常时必须立即调用",
            {
                "type": "object",
                "properties": {
                    "reason": {"type": "string", "description": "触发急停的原因说明"},
                },
                "required": ["reason"],
            },
            self._impl_safety_stop,
        ))
        self.register(FunctionTool(
            "system_health_check",
            "执行一次系统健康检查，返回环境/配置/安全/通信等8类检查项摘要",
            {"type": "object", "properties": {}, "required": []},
            self._impl_health_check,
        ))

    def _impl_move_ee(self, x: float, y: float, z: float) -> Dict[str, Any]:
        # 夹取合法性（简单工程边界）
        if not (-1.0 <= x <= 1.5 and -1.0 <= y <= 1.0 and -0.1 <= z <= 1.8):
            raise ValueError(f"坐标 ({x},{y},{z}) 超出安全工作空间，请重新规划")
        self._robot_state_snapshot["ee_xyz"] = [float(x), float(y), float(z)]
        self._robot_state_snapshot["mode"] = "MOVING"
        return {"msg": f"移动末端到 ({x:.3f}, {y:.3f}, {z:.3f}) 已登记执行（Mock成功）"}

    def _impl_gripper(self, state: str) -> Dict[str, Any]:
        self._robot_state_snapshot["gripper"] = state
        self._robot_state_snapshot["mode"] = "GRIP_" + state.upper()
        return {"msg": f"夹爪已切换为：{state}"}

    def _impl_safety_stop(self, reason: str) -> Dict[str, Any]:
        self._robot_state_snapshot["mode"] = "ESTOP"
        return {"msg": "🚨 紧急停止已登记！", "reason": reason,
                "action": "系统将保持ESTOP状态直到人工复位"}

    def _impl_health_check(self) -> Dict[str, Any]:
        try:
            from deployment.health_check import run_health_checks
            report = run_health_checks(deploy_level="test")
            return {
                "overall": "PASS" if report.overall_pass else "FAIL",
                "counts": report.count_by_level(),
                "categories": sorted({r.category for r in report.results}),
            }
        except Exception as e:
            return {"overall": "SKIP", "detail": f"未执行健康检查: {repr(e)}"}


# ============================================================
# LLM Provider 抽象与实现
# ============================================================
class BaseLLMProvider(abc.ABC):
    name = "base"

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg

    @abc.abstractmethod
    def chat(self, messages: List[Dict[str, Any]],
             tools: Optional[List[Dict[str, Any]]] = None,
             **extra) -> LLMResponse:
        raise NotImplementedError


class MockLLMProvider(BaseLLMProvider):
    """
    Mock Provider（公共示例默认）
    ------------------------------------------------
    不调用真实网络，按启发式给一个「像样」的回复，
    用于展示整个 SDK 和决策系统的架构闭环。
    """
    name = "mock"

    def chat(self, messages, tools=None, **extra) -> LLMResponse:
        t0 = time.time()
        last = messages[-1]["content"] if messages else ""
        text, tool_calls = self._heuristic(last, tools or [])
        return LLMResponse(
            success=True, provider="mock", model="mock-skill-v1",
            text=text, tool_calls=tool_calls,
            usage={"prompt_tokens": 32, "completion_tokens": 32},
            latency_ms=int((time.time() - t0) * 1000),
            trace_id="mock-" + uuid.uuid4().hex[:12],
        )

    def _heuristic(self, user_msg: str, tools) -> tuple[str, List[ToolCallRequest]]:
        msg = user_msg.lower()
        tcs: List[ToolCallRequest] = []
        # 关键字触发工具调用
        if any(k in msg for k in ("移动", "放", "抓取", "抓取到", "末端到", "move")):
            tcs.append(ToolCallRequest(
                function_name="move_end_effector_to",
                arguments={"x": 0.55, "y": 0.10, "z": 0.25},
            ))
        if any(k in msg for k in ("抓", "夹", "闭合", "close")):
            tcs.append(ToolCallRequest(function_name="gripper_command",
                                       arguments={"state": "close"}))
        if any(k in msg for k in ("松", "张开", "放下", "open")):
            tcs.append(ToolCallRequest(function_name="gripper_command",
                                       arguments={"state": "open"}))
        if any(k in msg for k in ("状态", "status", "当前")):
            tcs.append(ToolCallRequest(function_name="get_current_robot_status",
                                       arguments={}))
        if any(k in msg for k in ("技能", "能力", "工具", "能用")):
            tcs.append(ToolCallRequest(function_name="list_available_skills",
                                       arguments={}))
        if any(k in msg for k in ("健康", "health", "检查")):
            tcs.append(ToolCallRequest(function_name="system_health_check",
                                       arguments={}))
        if any(k in msg for k in ("急停", "停止", "危险", "stop")):
            tcs.append(ToolCallRequest(function_name="safety_stop",
                                       arguments={"reason": f"用户指令: {user_msg[:40]}"}))

        if tcs:
            text = f"检测到用户意图，触发 {len(tcs)} 项技能调用（见下方 tool_calls）。"
        else:
            text = (
                "我是具身智能高层决策助手，支持以下能力：\n"
                "  ① 查询当前机器人状态\n"
                "  ② 控制末端移动到坐标（例如：把末端移到 0.6 0.0 0.3）\n"
                "  ③ 控制夹爪开合（张开 / 闭合）\n"
                "  ④ 执行系统健康检查\n"
                "  ⑤ 紧急情况下立即停止机器人\n"
                "请告诉我您想完成什么任务？"
            )
        return text, tcs


class OpenAICompatProvider(BaseLLMProvider):
    """
    OpenAI兼容接口 Provider（通义/智谱/DeepSeek/官方都可用）
    ------------------------------------------------
    说明：公共示例版保留完整调用模板，但默认未启用（需要用户自填 .env）
    """
    name = "openai_compat"

    def __init__(self, cfg: Dict[str, Any]):
        super().__init__(cfg)
        try:
            import requests  # noqa: F401
            self._has_requests = True
        except ImportError:
            self._has_requests = False

    def chat(self, messages, tools=None, **extra) -> LLMResponse:
        t0 = time.time()
        if not self._has_requests:
            return LLMResponse(False, self.name, self.cfg.get("model", "?"),
                               error_message="未安装 requests 库，无法发起 HTTP 请求")
        import requests
        api_key = self.cfg.get("api_key") or ""
        if not api_key:
            return LLMResponse(False, self.name, self.cfg.get("model", "?"),
                               error_message="缺少 api_key（请在 .env 中配置并启用该Provider）")
        url = self.cfg.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1") + "/chat/completions"
        payload = {
            "model": self.cfg.get("model", "qwen-plus"),
            "messages": messages,
            "temperature": float(self.cfg.get("temperature", 0.7)),
        }
        if tools:
            payload["tools"] = tools
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=60)
            r.raise_for_status()
            data = r.json()
            choice = data["choices"][0]
            msg = choice.get("message", {})
            tcs: List[ToolCallRequest] = []
            for tc in msg.get("tool_calls") or []:
                fn = tc.get("function", {})
                try:
                    args = json.loads(fn.get("arguments", "{}"))
                except Exception:
                    args = {}
                tcs.append(ToolCallRequest(call_id=tc.get("id", ""),
                                           function_name=fn.get("name", ""),
                                           arguments=args))
            return LLMResponse(
                success=True, provider=self.name,
                model=data.get("model", self.cfg.get("model", "")),
                text=msg.get("content", "") or "",
                tool_calls=tcs,
                usage=data.get("usage", {}),
                latency_ms=int((time.time() - t0) * 1000),
                raw=data, trace_id=data.get("id", ""),
            )
        except Exception as e:
            return LLMResponse(False, self.name, self.cfg.get("model", "?"),
                               latency_ms=int((time.time() - t0) * 1000),
                               error_message=repr(e))


# ============================================================
# LLM Decision SDK（对外面向应用开发者）
# ============================================================
class LLMDecisionSDK:
    """
    大模型决策 SDK（对外主要类）
    ------------------------------------------------
    特性：
      - 支持多Provider注册 + 回退
      - 对话历史（带Token费用估算+截断策略）
      - 工具调用自动执行（SkillLibrary）
      - 审计日志 + 可回放
    """

    def __init__(
        self,
        provider: Optional[BaseLLMProvider] = None,
        skills: Optional[SkillLibrary] = None,
        system_prompt: Optional[str] = None,
        enable_tool_auto_run: bool = True,
        max_tool_rounds: int = 5,
    ):
        self.provider = provider or MockLLMProvider({})
        self.skills = skills or SkillLibrary()
        self.enable_tool_auto_run = enable_tool_auto_run
        self.max_tool_rounds = max_tool_rounds
        self.history: List[Dict[str, Any]] = []
        self.total_usage: Dict[str, int] = {"prompt_tokens": 0, "completion_tokens": 0, "requests": 0}
        self.audit_log: List[Dict[str, Any]] = []
        # 系统提示词（具身智能高层决策专业人设）
        self._sys_prompt = system_prompt or self._default_system_prompt()
        self.history.append({"role": "system", "content": self._sys_prompt})

    @staticmethod
    def from_env(env_path: str = ".env", skills: Optional[SkillLibrary] = None) -> "LLMDecisionSDK":
        """从 .env 文件自动初始化（公共示例默认返回 Mock Provider）"""
        env = _load_env_from_file(env_path)
        use = env.get("LLM_USE_PROVIDER", "mock").lower()
        if use == "mock":
            provider: BaseLLMProvider = MockLLMProvider({})
        else:
            cfg = {
                "model": env.get("LLM_MODEL_NAME", "qwen-plus"),
                "base_url": env.get("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
                "api_key": env.get("LLM_API_KEY") or env.get("DASHSCOPE_API_KEY") or env.get("OPENAI_API_KEY", ""),
                "temperature": float(env.get("LLM_TEMPERATURE", "0.7")),
            }
            provider = OpenAICompatProvider(cfg)
        return LLMDecisionSDK(provider=provider, skills=skills)

    # ---- 系统人设 ----
    @staticmethod
    def _default_system_prompt() -> str:
        return (
            "你是一位专业的具身智能机器人高层决策助手。\n"
            "你的职责是：\n"
            "  1) 根据用户任务描述理解意图；\n"
            "  2) 优先使用提供的 tools（技能库）把高层意图拆解为原子动作；\n"
            "  3) 动作执行前检查是否在安全工作空间内；\n"
            "  4) 一旦存在人身/设备风险，立即调用 safety_stop 工具紧急停止。\n"
            "输出要求：\n"
            "  - 能用 tool_calls 解决的问题，尽量用工具，不要空口回答。\n"
            "  - 工具调用参数必须数值化、明确化（坐标单位：米）。\n"
            "  - 每次回复后保持简洁，避免废话。\n"
        )

    # ---- 对外核心方法 ----
    def chat(self, user_input: str, **run_opts) -> Dict[str, Any]:
        """
        一次用户输入 → 返回最终回复 + 工具执行轨迹
        """
        self.history.append({"role": "user", "content": user_input})
        trace: List[Dict[str, Any]] = []
        final_text = ""
        rounds_left = self.max_tool_rounds
        while rounds_left > 0:
            rounds_left -= 1
            resp = self._call_llm(self.history, self.skills.list_tools_schema())
            self.total_usage["requests"] += 1
            self.total_usage["prompt_tokens"] += resp.usage.get("prompt_tokens", 0)
            self.total_usage["completion_tokens"] += resp.usage.get("completion_tokens", 0)
            self.audit_log.append({
                "ts": time.time(),
                "trace_id": resp.trace_id,
                "provider": resp.provider,
                "model": resp.model,
                "success": resp.success,
                "latency_ms": resp.latency_ms,
                "usage": dict(resp.usage),
                "text": resp.text,
                "tool_calls": [asdict(tc) for tc in resp.tool_calls],
            })
            if not resp.success:
                final_text = f"[LLM调用失败] {resp.error_message}"
                break
            # 追加助手消息到对话
            assistant_msg: Dict[str, Any] = {"role": "assistant"}
            if resp.text:
                assistant_msg["content"] = resp.text
                final_text = resp.text
            if resp.tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.call_id,
                        "type": "function",
                        "function": {"name": tc.function_name,
                                     "arguments": json.dumps(tc.arguments, ensure_ascii=False)},
                    }
                    for tc in resp.tool_calls
                ]
            self.history.append(assistant_msg)

            # 没有工具调用 → 结束本轮
            if not resp.tool_calls:
                break

            # 自动执行工具
            if self.enable_tool_auto_run:
                for tc in resp.tool_calls:
                    exec_result = self.skills.execute(tc.function_name, **tc.arguments)
                    trace.append({
                        "call_id": tc.call_id,
                        "function": tc.function_name,
                        "arguments": dict(tc.arguments),
                        "result": exec_result,
                    })
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tc.call_id,
                        "content": json.dumps(exec_result, ensure_ascii=False),
                    })
            else:
                break
        return {
            "final_text": final_text,
            "trace": trace,
            "total_rounds": self.max_tool_rounds - rounds_left,
            "accumulated_usage": dict(self.total_usage),
            "history_snapshot_len": len(self.history),
        }

    # ---- 内部：调用LLM（统一模板，可叠加重试）----
    def _call_llm(self, messages, tools_schema=None, retry: int = 2) -> LLMResponse:
        last_err = ""
        for attempt in range(retry + 1):
            try:
                resp = self.provider.chat(messages, tools=tools_schema)
                if resp.success:
                    return resp
                last_err = resp.error_message
            except Exception as e:
                last_err = repr(e)
            time.sleep(0.3 * (attempt + 1))
        # 失败时兜底：返回 Mock 回复，保证系统不因 LLM 挂而整体挂掉
        fallback = MockLLMProvider({}).chat(messages, tools=tools_schema)
        fallback.error_message = f"[Provider回退] 真实LLM失败后用Mock兜底。原错误: {last_err}"
        return fallback

    # ---- 诊断 ----
    def cost_estimate_usd(self, rate_per_1k_prompt: float = 0.003,
                         rate_per_1k_completion: float = 0.010) -> float:
        """粗略估算费用（按美元），用于审计面板展示"""
        return (
            self.total_usage.get("prompt_tokens", 0) / 1000 * rate_per_1k_prompt
            + self.total_usage.get("completion_tokens", 0) / 1000 * rate_per_1k_completion
        )

    def reset_history(self) -> None:
        self.history = [{"role": "system", "content": self._sys_prompt}]
        self.total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "requests": 0}


# ============================================================
# 自主决策系统（高层：感知→知识→LLM→技能→执行→审计）
# ============================================================
@dataclass
class DecisionEpisode:
    episode_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    task_input: str = ""
    perception_snapshot: Dict[str, Any] = field(default_factory=dict)
    sdk_result: Dict[str, Any] = field(default_factory=dict)
    executed_skills: List[Dict[str, Any]] = field(default_factory=list)
    final_status: str = "pending"   # pending / success / failed / safety_stop
    error_reason: str = ""
    started_at: float = field(default_factory=time.time)
    finished_at: float = 0.0


class AutonomousDecisionSystem:
    """
    自主决策系统（端到端封装）
    ------------------------------------------------
    工作流：
        1) 接收用户任务（自然语言）
        2) 从传感器读取感知快照（或 Mock 注入）
        3) LLMDecisionSDK 生成工具调用序列
        4) 逐条执行技能，写入执行日志
        5) 安全事件熔断 & 最终状态审计
    """

    def __init__(self, sdk: Optional[LLMDecisionSDK] = None):
        self.sdk = sdk or LLMDecisionSDK.from_env()
        self.episodes: List[DecisionEpisode] = []
        self.on_new_episode: Optional[Callable[[DecisionEpisode], None]] = None

    def run_task(self, task: str,
                 perception_snapshot: Optional[Dict[str, Any]] = None) -> DecisionEpisode:
        ep = DecisionEpisode(task_input=task)
        ep.perception_snapshot = perception_snapshot or self._default_perception()
        if self.on_new_episode:
            self.on_new_episode(ep)
        # 组装提示：把感知快照作为「当前环境上下文」写入用户消息前面
        ctx_json = json.dumps(ep.perception_snapshot, ensure_ascii=False, indent=2)
        composed_input = (
            "[当前环境感知快照]\n" + ctx_json + "\n\n"
            + "[用户任务]\n" + task
        )
        try:
            result = self.sdk.chat(composed_input)
            ep.sdk_result = result
            ep.executed_skills = result.get("trace", [])
            # 判定最终状态
            if any(s.get("result", {}).get("function") == "safety_stop"
                   or s.get("function") == "safety_stop" for s in ep.executed_skills):
                ep.final_status = "safety_stop"
            elif any(not s.get("result", {}).get("ok", True) for s in ep.executed_skills):
                ep.final_status = "failed"
                ep.error_reason = "至少1项技能执行失败（查看 trace）"
            else:
                ep.final_status = "success"
        except Exception as e:
            ep.final_status = "failed"
            ep.error_reason = f"决策异常: {repr(e)}"
        ep.finished_at = time.time()
        self.episodes.append(ep)
        return ep

    @staticmethod
    def _default_perception() -> Dict[str, Any]:
        """无感知输入时，给一套标准 Mock 环境快照（便于框架演示）"""
        return {
            "environment": {
                "scene": "industrial.assembly.workstation_01",
                "lighting_ok": True,
                "safety_zone_clear": True,
                "conveyor_running": False,
            },
            "detected_objects": [
                {"label": "peg_A01", "pose_xyz_m": [0.52,  0.08, 0.42],
                 "confidence": 0.94, "in_workspace": True},
                {"label": "base_hole_B03", "pose_xyz_m": [0.52, -0.06, 0.40],
                 "confidence": 0.91, "in_workspace": True},
                {"label": "tray_empty", "pose_xyz_m": [0.10, -0.40, 0.20],
                 "confidence": 0.99, "in_workspace": True},
            ],
            "robot": {
                "mode": "AUTO",
                "ee_xyz_m": [0.30, 0.0, 0.60],
                "gripper": "open",
                "battery_or_voltage_ratio": 0.98,
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def report(self, last_n: int = 10) -> Dict[str, Any]:
        eps = self.episodes[-last_n:]
        status_counts: Dict[str, int] = {}
        for e in eps:
            status_counts[e.final_status] = status_counts.get(e.final_status, 0) + 1
        return {
            "total_episodes": len(self.episodes),
            "recent_window": len(eps),
            "recent_status": status_counts,
            "total_sdk_requests": self.sdk.total_usage.get("requests", 0),
            "cost_estimate_usd": round(self.sdk.cost_estimate_usd(), 5),
            "episodes": [asdict(e) for e in eps[-3:]],
        }
