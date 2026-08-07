# -*- coding: utf-8 -*-
"""
PIN 码门禁：调用 AI / 执行敏感脚本 / 搜索文件 之前，像开机 PIN 一样先验密码

⚠️  边界限制（请务必了解）：
    本脚本是「软门禁」，只能保护"从 Python 入口调用的操作"。
    它 **无法拦截 IDE 聊天框里直接和 Trae/Cursor/ChatGPT 机器人的对话**——
    那一层请使用「锁屏 Win+L + 退出 IDE 账号 + 加密敏感文件」三道物理防线。

    适合的保护场景：
    - 你自己写的调用大模型 API 的 Python 脚本（在 main() 入口第一行加 require_pin()）
    - 一键搜索/导出项目文件的工具脚本（调用前加 require_pin()）
    - 包装 shell 命令：python pin_gate.py wrap "dir /s *.py" （先输PIN再执行dir）

功能：
    1. 首次使用：python pin_gate.py setup          # 设置 PIN（仅存不可逆哈希，不存明文）
    2. 改 PIN：    python pin_gate.py change         # 先输旧PIN再输新PIN
    3. 验证：      python pin_gate.py verify         # 手动测门禁
    4. 包命令：    python pin_gate.py wrap "命令"    # 先输PIN，通过才执行命令

API 用法（给其他 Python 脚本调用）：
    from pin_gate import require_pin

    def main():
        require_pin()      # ← 第一行先锁，输不对 PIN 程序直接退出，后面代码永远不会跑
        # ... 你的其他逻辑 ...
"""

import os
import sys
import json
import time
import getpass
import base64
import hashlib
import secrets
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Tuple

# ============================================================
# 常量配置
# ============================================================

PIN_STORE_FILENAME = ".pin_hash.json"
PBKDF2_ITERATIONS = 480_000  # 与 file_encryptor.py 同强度
SALT_LEN = 16
HASH_LEN = 32
DEFAULT_MAX_RETRIES = 3
DEFAULT_COOLDOWN_SEC = 10
DEFAULT_SESSION_TTL_SEC = 30 * 60  # 本次进程内：输对一次，30 分钟内免重输

# 进程内会话缓存（只有本 Python 进程有效，关闭终端即失效）
_SESSION_OK_UNTIL: Optional[float] = None
_CONSECUTIVE_FAILURES = 0


# ============================================================
# 哈希 / 存储 核心
# ============================================================

def _project_root() -> Path:
    return Path(__file__).parent.resolve()


def _pin_store_path() -> Path:
    return _project_root() / PIN_STORE_FILENAME


def _compute_pin_hash(pin: str, salt: bytes, iterations: int) -> bytes:
    """PBKDF2-HMAC-SHA256 派生哈希"""
    return hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        salt,
        iterations,
        dklen=HASH_LEN,
    )


def _constant_time_equal(a: bytes, b: bytes) -> bool:
    """防时序攻击的哈希比对"""
    if len(a) != len(b):
        return False
    return secrets.compare_digest(a, b)


def _load_pin_store() -> Optional[dict]:
    p = _pin_store_path()
    if not p.is_file():
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 关键字段校验
        for k in ("salt_b64", "hash_b64", "iterations"):
            if k not in data:
                raise ValueError(f"缺少字段: {k}")
        return data
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"  ❌ PIN 存储文件损坏或不可读: {e}")
        print(f"     文件路径: {p}")
        print(f"     建议：删除该文件后重新运行 python pin_gate.py setup")
        sys.exit(2)


def _save_pin_store(salt: bytes, pin_hash: bytes, iterations: int) -> None:
    data = {
        "salt_b64": base64.b64encode(salt).decode("ascii"),
        "hash_b64": base64.b64encode(pin_hash).decode("ascii"),
        "iterations": iterations,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "hint": "这是不可逆哈希，无法反推出 PIN 明文；忘记 PIN 请删除此文件后重新 setup。",
    }
    p = _pin_store_path()
    # Windows 修复：若文件已存在且带 HIDDEN 属性，先清除该属性才能写（否则 PermissionError 13）
    attrs_handle = None
    try:
        if os.name == "nt":
            import ctypes
            FILE_ATTRIBUTE_HIDDEN = 2
            FILE_ATTRIBUTE_NORMAL = 0x80
            GetFileAttributesW = ctypes.windll.kernel32.GetFileAttributesW
            SetFileAttributesW = ctypes.windll.kernel32.SetFileAttributesW
            prev = GetFileAttributesW(str(p))
            if prev != 0xFFFFFFFF and (prev & FILE_ATTRIBUTE_HIDDEN):
                # 清除 HIDDEN，保留其余原有属性
                SetFileAttributesW(str(p), prev & ~FILE_ATTRIBUTE_HIDDEN)
                attrs_handle = prev
    except Exception:
        attrs_handle = None
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    finally:
        # 写完后：如果之前是隐藏文件 / 或首次创建 -> 统一设为隐藏
        try:
            if os.name == "nt":
                import ctypes
                FILE_ATTRIBUTE_HIDDEN = 2
                if attrs_handle is not None:
                    # 还原原属性 | HIDDEN（确保隐藏）
                    ctypes.windll.kernel32.SetFileAttributesW(str(p), attrs_handle | FILE_ATTRIBUTE_HIDDEN)
                else:
                    ctypes.windll.kernel32.SetFileAttributesW(str(p), FILE_ATTRIBUTE_HIDDEN)
        except Exception:
            pass


# ============================================================
# 对外 API
# ============================================================

def is_pin_setup_done() -> bool:
    return _load_pin_store() is not None


def verify_pin(pin: str) -> bool:
    """验 PIN 对错（纯函数，无交互）"""
    store = _load_pin_store()
    if store is None:
        return False
    salt = base64.b64decode(store["salt_b64"])
    expected = base64.b64decode(store["hash_b64"])
    iterations = int(store["iterations"])
    actual = _compute_pin_hash(pin, salt, iterations)
    return _constant_time_equal(actual, expected)


def setup_pin(new_pin: str) -> None:
    """设置新 PIN（覆盖旧的）。调用方负责校验强度。"""
    salt = secrets.token_bytes(SALT_LEN)
    pin_hash = _compute_pin_hash(new_pin, salt, PBKDF2_ITERATIONS)
    _save_pin_store(salt, pin_hash, PBKDF2_ITERATIONS)


def require_pin(
    max_retries: int = DEFAULT_MAX_RETRIES,
    cooldown_sec: int = DEFAULT_COOLDOWN_SEC,
    session_ttl_sec: int = DEFAULT_SESSION_TTL_SEC,
    prompt: str = "  🔐 请输入 PIN 码解锁（输错 "
                  f"{DEFAULT_MAX_RETRIES} 次会触发 {DEFAULT_COOLDOWN_SEC} 秒冷却）: ",
    exit_on_fail: bool = True,
) -> bool:
    """
    主门禁函数：在你脚本的 main() 第一行调用。

    返回 True = 放行；返回 False = 没通过（如果 exit_on_fail=True 则直接 sys.exit 不会返回 False）。
    """
    global _SESSION_OK_UNTIL, _CONSECUTIVE_FAILURES

    # 0. 没初始化就提示先 setup
    if not is_pin_setup_done():
        print("  ❌ 还未设置 PIN 码。")
        print("     请先执行：python pin_gate.py setup")
        if exit_on_fail:
            sys.exit(3)
        return False

    # 1. 会话 TTL 内免重输（仅在同 Python 进程内有效）
    now = time.time()
    if _SESSION_OK_UNTIL is not None and now < _SESSION_OK_UNTIL:
        remaining = int(_SESSION_OK_UNTIL - now)
        print(f"  ✅ 会话内已验证，{remaining // 60} 分 {remaining % 60} 秒内无需重输 PIN。")
        return True

    # 2. 循环输 PIN
    failures = 0
    _MAX_LOOPS = 10_000_000
    _MAX_SECONDS = 86400
    _loop_count = 0
    _start_time = time.time()
    while True:
        _loop_count += 1
        if _loop_count > _MAX_LOOPS:
            print("  ❌ 验证次数超过上限，强制退出")
            if exit_on_fail:
                sys.exit(1)
            return False
        if time.time() - _start_time > _MAX_SECONDS:
            print("  ❌ 验证超时（24小时），强制退出")
            if exit_on_fail:
                sys.exit(1)
            return False
        failures += 1
        _CONSECUTIVE_FAILURES += 1

        # 冷却（防止暴力猜）
        if failures > max_retries or _CONSECUTIVE_FAILURES % max_retries == 0:
            print(f"  ⏳ 连续输错 ≥ {max_retries} 次，强制冷却 {cooldown_sec} 秒…")
            time.sleep(cooldown_sec)

        try:
            pin_input = getpass.getpass(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\n  ❌ 已取消。")
            if exit_on_fail:
                sys.exit(1)
            return False

        if verify_pin(pin_input):
            # 输对 → 清失败计数 + 开会话缓存
            _CONSECUTIVE_FAILURES = 0
            _SESSION_OK_UNTIL = time.time() + session_ttl_sec
            print("  ✅ PIN 正确，已解锁。")
            return True

        remaining_tries = max_retries - (failures % max_retries)
        if remaining_tries == 0:
            remaining_tries = max_retries
        print(f"  ❌ PIN 错误（本次第 {failures} 次错，"
              f"距下次冷却还有 {remaining_tries} 次机会）。")


# ============================================================
# 强度校验 + 交互式输入（setup / change 用）
# ============================================================

_MIN_PIN_LEN = 8


def _pin_strength_check(pin: str) -> Tuple[bool, str]:
    """简单强度校验：长度 + 至少 2 类字符（字母/数字/符号）"""
    if len(pin) < _MIN_PIN_LEN:
        return False, f"至少需要 {_MIN_PIN_LEN} 位字符"
    classes = 0
    if any(c.isalpha() for c in pin):
        classes += 1
    if any(c.isdigit() for c in pin):
        classes += 1
    if any(not c.isalnum() for c in pin):
        classes += 1
    if classes < 2:
        return False, "需要至少包含 字母/数字/符号 中的 2 类"
    return True, "OK"


def _interactive_get_new_pin(title: str) -> str:
    print()
    print(f"  🆕 {title}")
    print(f"     要求：至少 {_MIN_PIN_LEN} 位，含 字母/数字/符号 至少 2 类")
    _MAX_LOOPS = 10_000_000
    _MAX_SECONDS = 86400
    _loop_count = 0
    _start_time = time.time()
    while True:
        _loop_count += 1
        if _loop_count > _MAX_LOOPS:
            print("     ❌ 输入次数超过上限，强制退出")
            sys.exit(1)
        if time.time() - _start_time > _MAX_SECONDS:
            print("     ❌ 输入超时（24小时），强制退出")
            sys.exit(1)
        p1 = getpass.getpass("     请输入新 PIN：")
        ok, msg = _pin_strength_check(p1)
        if not ok:
            print(f"     ❌ 强度不够：{msg}，请重新输入")
            continue
        p2 = getpass.getpass("     请再输一遍新 PIN 确认：")
        if p1 != p2:
            print("     ❌ 两次输入不一致，请重来")
            continue
        return p1


# ============================================================
# 命令行子命令
# ============================================================

def _cmd_setup(_args) -> int:
    if is_pin_setup_done():
        confirm = input("  ⚠️  检测到已有 PIN。覆盖会让旧 PIN 失效，输入 OVERWRITE 确认: ").strip()
        if confirm != "OVERWRITE":
            print("  已取消。")
            return 0
    pin = _interactive_get_new_pin("设置项目 PIN 码")
    setup_pin(pin)
    print(f"  ✅ PIN 设置成功，哈希已保存到: {_pin_store_path().name}")
    print("     （文件是隐藏属性 + 只存不可逆哈希，无法反推出 PIN 明文）")
    return 0


def _cmd_change(_args) -> int:
    if not is_pin_setup_done():
        print("  ❌ 还未设置 PIN，请先运行：python pin_gate.py setup")
        return 2
    # 先验旧 PIN
    old = getpass.getpass("  🔐 请输入当前旧 PIN：")
    if not verify_pin(old):
        print("  ❌ 旧 PIN 错误，拒绝修改。")
        return 1
    new_pin = _interactive_get_new_pin("修改项目 PIN 码")
    setup_pin(new_pin)
    # 清会话缓存，强制下次重输
    global _SESSION_OK_UNTIL
    _SESSION_OK_UNTIL = None
    print("  ✅ PIN 已修改成功。会话缓存已清空，下次调用会要求重新输入。")
    return 0


def _cmd_verify(_args) -> int:
    ok = require_pin(max_retries=3, cooldown_sec=5, session_ttl_sec=0,
                     prompt="  🔐 请输入 PIN 进行验证（会话 TTL=0，每次都会问）: ",
                     exit_on_fail=False)
    print()
    if ok:
        print("  🎯 验证通过：门禁正常工作。")
        return 0
    print("  🚫 验证失败：门禁拦截生效。")
    return 1


def _cmd_wrap(args) -> int:
    if len(args) < 2 or not args[1]:
        print("  ❌ 用法：python pin_gate.py wrap \"你要执行的命令\"")
        print("     示例：python pin_gate.py wrap \"python file_encryptor.py list\"")
        return 2
    shell_cmd = args[1]
    require_pin(prompt=f"  🔐 执行命令需要 PIN：")
    print()
    print(f"  ▶️  放行，开始执行: {shell_cmd}")
    print("-" * 60)
    # 用 check=False 保留原命令退出码
    result = subprocess.run(shell_cmd, shell=True, check=False)
    print("-" * 60)
    print(f"  🛑 命令结束，退出码: {result.returncode}")
    return result.returncode


_SUBCOMMANDS = {
    "setup": ("初始化 / 覆盖设置 PIN", _cmd_setup),
    "change": ("先验旧 PIN 再设置新 PIN", _cmd_change),
    "verify": ("手动测试门禁拦截逻辑", _cmd_verify),
    "wrap": ("先过 PIN 门禁，再执行你传入的 shell 命令", _cmd_wrap),
}


def _print_help() -> None:
    print()
    print("=" * 60)
    print("  🔐 PIN 码门禁工具")
    print("=" * 60)
    print()
    print("用法: python pin_gate.py <子命令> [参数]")
    print()
    print("子命令:")
    width = max(len(k) for k in _SUBCOMMANDS)
    for name, (desc, _fn) in _SUBCOMMANDS.items():
        print(f"  {name.ljust(width)}    {desc}")
    print()
    print("示例:")
    print("  python pin_gate.py setup                # 第一次：设置你的 PIN")
    print("  python pin_gate.py change               # 换 PIN")
    print("  python pin_gate.py verify               # 验门禁灵不灵")
    print('  python pin_gate.py wrap "python file_encryptor.py list"  # 给任意命令加 PIN 锁')
    print()
    print("给其他 Python 脚本加 PIN 锁（两行）:")
    print("  from pin_gate import require_pin")
    print("  require_pin()   # ← 放 main() 第一行，后面的代码只有输对 PIN 才会跑")
    print()


# ============================================================
# 入口
# ============================================================

def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        _print_help()
        return 0

    cmd = argv[0]
    if cmd not in _SUBCOMMANDS:
        print(f"  ❌ 未知子命令: {cmd}")
        _print_help()
        return 2

    _desc, fn = _SUBCOMMANDS[cmd]
    return fn(argv)


if __name__ == "__main__":
    sys.exit(main())
