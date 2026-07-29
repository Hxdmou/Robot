#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
回归测试套件 - 快速验证所有核心功能
运行: python test_smoke.py
"""

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


import sys
import os
import time

old_stderr = sys.stderr
PASS = 0
FAIL = 0
RESULTS = []


def test(name, func):
    global PASS, FAIL
    try:
        func()
        PASS += 1
        RESULTS.append("[PASS] %s" % name)
        print("[PASS] %s" % name, flush=True)
    except Exception as e:
        FAIL += 1
        RESULTS.append("[FAIL] %s: %s" % (name, str(e)))
        print("[FAIL] %s: %s" % (name, str(e)), flush=True)


# ==================== 测试1：核心模块导入
def test_imports():
    sys.stderr = open(os.devnull, 'w')
    import pybullet
    import numpy
    from stable_baselines3 import PPO
    sys.stderr = old_stderr


# ==================== 测试2：环境创建
def test_env_create():
    sys.stderr = open(os.devnull, 'w')
    from robot_reach_env_optimized import RobotReachEnvOptimized
    env = RobotReachEnvOptimized(render_mode=None, max_steps=100)
    env.close()
    sys.stderr = old_stderr


# ==================== 测试3：环境重置
def test_env_reset():
    sys.stderr = open(os.devnull, 'w')
    from robot_reach_env_optimized import RobotReachEnvOptimized
    env = RobotReachEnvOptimized(render_mode=None, max_steps=100)
    obs, info = env.reset()
    assert obs.shape == (13,), "观测空间维度错误: %s" % str(obs.shape)
    env.close()
    sys.stderr = old_stderr


# ==================== 测试4：环境步进
def test_env_step():
    sys.stderr = open(os.devnull, 'w')
    from robot_reach_env_optimized import RobotReachEnvOptimized
    import numpy as np
    env = RobotReachEnvOptimized(render_mode=None, max_steps=100)
    env.reset()
    action = np.zeros(7, dtype=np.float32)
    obs, reward, term, trunc, info = env.step(action)
    assert obs.shape == (13,)
    assert isinstance(reward, (int, float))
    env.close()
    sys.stderr = old_stderr


# ==================== 测试5：课程学习（进度0.0）
def test_curriculum_0():
    sys.stderr = open(os.devnull, 'w')
    from robot_reach_env_optimized import RobotReachEnvOptimized
    env = RobotReachEnvOptimized(render_mode=None, max_steps=100)
    env.set_curriculum_progress(0.0)
    assert env.curriculum_progress == 0.0
    obs, _ = env.reset()
    env.step([0]*7)
    env.close()
    sys.stderr = old_stderr


# ==================== 测试6：课程学习（进度1.0，最大强度）
def test_curriculum_1():
    sys.stderr = open(os.devnull, 'w')
    from robot_reach_env_optimized import RobotReachEnvOptimized
    env = RobotReachEnvOptimized(render_mode=None, max_steps=100)
    env.set_curriculum_progress(1.0)
    assert env.curriculum_progress == 1.0
    obs, _ = env.reset()
    env.step([0]*7)
    env.close()
    sys.stderr = old_stderr


# ==================== 测试7：模型加载
def test_model_load():
    sys.stderr = open(os.devnull, 'w')
    from stable_baselines3 import PPO
    model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')
    assert model is not None
    sys.stderr = old_stderr


# ==================== 测试8：模型推理
def test_model_predict():
    sys.stderr = open(os.devnull, 'w')
    from stable_baselines3 import PPO
    from robot_reach_env_optimized import RobotReachEnvOptimized
    import numpy as np
    model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')
    env = RobotReachEnvOptimized(render_mode=None, max_steps=100)
    obs, _ = env.reset()
    action, _ = model.predict(obs, deterministic=True)
    assert action.shape == (7,)
    env.close()
    sys.stderr = old_stderr


# ==================== 测试9：完整episode
def test_full_episode():
    sys.stderr = open(os.devnull, 'w')
    from stable_baselines3 import PPO
    from robot_reach_env_optimized import RobotReachEnvOptimized
    model = PPO.load('ppo_robot_reach_final_5m_enhanced', device='cpu')
    env = RobotReachEnvOptimized(render_mode=None, max_steps=200)
    env.set_curriculum_progress(1.0)
    obs, _ = env.reset()
    done = False
    steps = 0
    while not done and steps < 200:
        action, _ = model.predict(obs, deterministic=True)
        obs, _, term, trunc, _ = env.step(action)
        done = term or trunc
        steps += 1
    env.close()
    sys.stderr = old_stderr


# ==================== 测试10：传感器噪声模块
def test_sensor_noise():
    sys.stderr = open(os.devnull, 'w')
    from sensor_noise import SensorNoiseSystem
    from noise_config import SENSOR_NOISE_CONFIG
    system = SensorNoiseSystem(SENSOR_NOISE_CONFIG)
    noisy = system.apply_joint_noise([0.0]*7)
    assert len(noisy) == 7
    sys.stderr = old_stderr


# ==================== 测试11：碰撞检测模块
def test_collision():
    sys.stderr = open(os.devnull, 'w')
    from collision_detector import CollisionDetector
    from collision_config import COLLISION_CONFIG
    detector = CollisionDetector(COLLISION_CONFIG)
    sys.stderr = old_stderr


# ==================== 测试12：数据记录模块
def test_data_recorder():
    sys.stderr = open(os.devnull, 'w')
    from data_recorder import DataRecorder
    from data_config import DATA_RECORDER_CONFIG
    recorder = DataRecorder(DATA_RECORDER_CONFIG)
    sys.stderr = old_stderr


# ==================== 运行所有测试
def main():
    print("", flush=True)
    print("=" * 60, flush=True)
    print("  机械臂仿真系统 - 回归测试套件", flush=True)
    print("=" * 60, flush=True)
    print("", flush=True)

    start_time = time.time()

    test("核心模块导入", test_imports)
    test("环境创建", test_env_create)
    test("环境重置", test_env_reset)
    test("环境步进", test_env_step)
    test("课程学习进度0.0", test_curriculum_0)
    test("课程学习进度1.0", test_curriculum_1)
    test("模型加载", test_model_load)
    test("模型推理", test_model_predict)
    test("完整Episode(最大强度)", test_full_episode)
    test("传感器噪声模块", test_sensor_noise)
    test("碰撞检测模块", test_collision)
    test("数据记录模块", test_data_recorder)

    elapsed = time.time() - start_time

    print("", flush=True)
    print("=" * 60, flush=True)
    print("  测试结果: %d 通过 / %d 失败 / 共 %d 项" % (PASS, FAIL, PASS + FAIL), flush=True)
    print("  总耗时: %.2f 秒" % elapsed, flush=True)
    print("=" * 60, flush=True)

    sys.stderr = old_stderr
    if FAIL > 0:
        print("", flush=True)
        print("失败项:", flush=True)
        for r in RESULTS:
            if r.startswith("[FAIL]"):
                print("  " + r, flush=True)
        sys.exit(1)
    else:
        print("", flush=True)
        print("所有测试通过！[OK]", flush=True)
        sys.exit(0)


if __name__ == "__main__":
    main()
