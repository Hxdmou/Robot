#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2：部署健康检查演示
================================================
演示部署等级 test → pre → prod 三级健康检查结果对比
输出格式：终端彩色报告 + 写入 JSON 摘要文件
"""

from __future__ import annotations

import json
import os
import sys
import time


def main() -> int:
    from deployment.health_check import run_health_checks, HealthReport

    outputs = {}
    for level in ("test", "pre", "prod"):
        print("\n" + "=" * 66)
        print(f"🏁 正在执行 [{level.upper()}] 等级健康检查...")
        report: HealthReport = run_health_checks(deploy_level=level)
        print(report.summary())
        outputs[level] = report.to_dict()
        time.sleep(0.2)

    out_path = os.path.join(os.path.dirname(__file__), "..", "logs",
                            f"health_checks_{int(time.time())}.json")
    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(outputs, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 66)
    print(f"✅ 三等级健康检查全部执行完成")
    print(f"📄 报告 JSON 已归档：{out_path}")
    print("=" * 66)
    # test/pre 视为演示通过；prod若有FAIL也仅作为信息展示
    return 0


if __name__ == "__main__":
    sys.exit(main())
