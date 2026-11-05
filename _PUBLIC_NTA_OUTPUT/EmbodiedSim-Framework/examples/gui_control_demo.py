#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3：三层编排 + 自主决策 + 数字孪生 综合演示
================================================
一次跑完一个「装配任务」的闭环：
  1) 实例化 感知Mock / 决策技能库 / 执行Mock → 三层编排
  2) 用 LLMDecisionSDK + 技能库 运行 1 个高层任务
  3) 启动 DigitalTwinSystem（ConsoleRenderer）展示任务进度
"""

from __future__ import annotations

import sys
import time


def main() -> int:
    print("=" * 66)
    print("🤖 具身智能综合演示：三层编排 → AI决策 → 数字孪生")
    print("=" * 66)

    # 1. 三层编排
    print("\n[1/3] 三层编排闭环 (Perception→Decision→Execution)")
    from core.module_interfaces import (
        MockPerception, SimpleSkillBasedDecision, MockExecution,
        ThreeTierOrchestrator,
    )
    P = MockPerception("P_demo")
    D = SimpleSkillBasedDecision("D_demo")
    E = MockExecution("E_demo")
    orch = ThreeTierOrchestrator(P, D, E)
    D.set_task_goal("assembly_peg_in_hole", difficulty="medium")

    def _on_tick(cycle, pm, dm, em):
        skill = dm.payload.get("skill", {}).get("display_name", "?")
        status = "✅" if em.payload.get("success") else "⚠"
        print(f"    Cycle {cycle:02d} | 感知→决策(技能={skill})→执行 {status} | "
              f"耗时 {em.meta.get('execution_latency_ms', '?')}ms")
    orch.on_tick_callback = _on_tick
    count = orch.run_forever(max_cycles=10, period_s=0.02)
    print(f"    → 已完成 {count} 个闭环周期")

    # 2. AI决策 SDK（Mock模式）运行一次用户任务
    print("\n[2/3] 自主决策：AI高层决策 SDK + 技能库")
    from applications.llm_decision_sdk import (
        LLMDecisionSDK, AutonomousDecisionSystem,
    )
    sdk = LLMDecisionSDK.from_env()  # 默认Mock
    ads = AutonomousDecisionSystem(sdk=sdk)
    tasks = [
        "查询当前机器人状态",
        "把末端移动到工件正上方，然后抓取工件，最后放到托盘位置",
        "请执行一次系统健康检查",
    ]
    for idx, task in enumerate(tasks, start=1):
        print(f"  [{idx}] 用户任务: {task!r}")
        ep = ads.run_task(task)
        skills = " → ".join(
            (s.get("function") or "?") + (
                "(FAIL)" if not s.get("result", {}).get("ok", True) else ""
            )
            for s in ep.executed_skills
        ) or "(无工具调用)"
        print(f"      执行技能链: {skills}")
        print(f"      状态: {ep.final_status.upper()}  总轮次: {ep.sdk_result.get('total_rounds', '?')}")
        time.sleep(0.1)

    print("\n  📊 自主决策系统报告:")
    r = ads.report()
    for k, v in r.items():
        if k != "episodes":
            print(f"     - {k}: {v}")

    # 3. 数字孪生控制台
    print("\n[3/3] 数字孪生体实时控制台（Mock数据流）")
    print("      (显示过程会用ANSI色彩，终端支持则像仪表盘)")
    from applications.digital_twin_system import (
        DigitalTwinSystem, MockTwinStateSource, ConsoleRenderer,
    )
    twin = DigitalTwinSystem()
    twin.set_source(MockTwinStateSource(total_steps=50, sleep_s_per_step=0.05))
    twin.attach_renderer(ConsoleRenderer())
    # 简单告警监听：温度超过36度就打印
    def _on_temp_warn(s):
        hot = [(i, t) for i, t in enumerate(s.joint_temperatures_c) if t > 36.0]
        if hot:
            print(f"     [孪生告警] 关节温度偏高: {hot}")
    twin.on_state(_on_temp_warn)
    n = twin.run(max_states=50)
    print(f"\n      → 孪生体共处理 {n} 帧状态")
    rep = twin.report()
    print(f"      → 频率: {rep['avg_hz']} Hz | 安全事件: {rep['safety_events']} 次")

    print("\n" + "=" * 66)
    print("✅ 综合演示全部完成！")
    print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())
