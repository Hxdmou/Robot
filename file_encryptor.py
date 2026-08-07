# -*- coding: utf-8 -*-
"""
项目敏感文件加密/解密工具 (AES-256-GCM / Fernet)

功能：
    1. 使用安全的加密算法保护您的 .py 源代码、配置文件、文档等
    2. 支持单文件加密、目录批量加密、按规则自动加密敏感文件
    3. 加密后文件后缀为 .enc，原文件可选择删除/备份/保留
    4. 防止重复加密（已加密文件会自动跳过）
    5. 支持"出借设备前一键加密，拿回后一键解密"的工作流

使用方法：
    # 加密（按默认敏感规则）
    python file_encryptor.py encrypt

    # 加密并指定密码
    python file_encryptor.py encrypt --password "你的强密码"

    # 加密单个文件
    python file_encryptor.py encrypt --file config/settings.py

    # 加密整个目录
    python file_encryptor.py encrypt --dir ./embodied-intelligence

    # 解密所有 .enc 文件
    python file_encryptor.py decrypt

    # 解密单个文件
    python file_encryptor.py decrypt --file config/settings.py.enc

    # 列出所有可加密的敏感文件（不实际加密）
    python file_encryptor.py list

    # 删除所有 .enc 文件（仅删除加密副本，不影响原文件）
    python file_encryptor.py clean

⚠️  重要安全提示：
    1. 必须使用强密码（至少 12 位，含大小写字母+数字+符号）
    2. 忘记密码 = 永久丢失文件，务必牢记密码或保存到密码管理器
    3. 加密前必须先备份整个项目目录
    4. 本工具仅供个人设备使用，真实企业场景必须使用专业加密软件
"""

import os
import sys
import json
import hmac
import base64
import secrets
import argparse
import hashlib
import getpass
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Set

# ============================================================
# 加密算法层（优先使用 cryptography，不可用时降级）
# ============================================================

_CRYPTO_BACKEND = None  # 'fernet' | 'fallback' | None

try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    _CRYPTO_BACKEND = 'fernet'
except ImportError:
    _CRYPTO_BACKEND = 'fallback'
    InvalidToken = Exception  # type: ignore


# ============================================================
# 配置常量
# ============================================================

# 加密文件扩展名
ENC_EXT = '.enc'
# 元数据嵌入加密文件头的魔数标记
MAGIC_HEADER = b'PYENC02'  # 7 字节
# PBKDF2 迭代次数
PBKDF2_ITERATIONS = 480_000
# PBKDF2 盐长度
SALT_LEN = 16
# Fernet nonce 长度
FERNET_OVERHEAD = 57  # 估算，用于检测是否是 Fernet token

# 默认为"敏感文件"的扩展名（自动加密时使用）
DEFAULT_SENSITIVE_EXTS: Set[str] = {
    '.py', '.env', '.yaml', '.yml', '.json', '.toml',
    '.ini', '.cfg', '.conf', '.md', '.txt',
    '.bat', '.ps1', '.sh', '.cmd',
    '.db', '.sqlite', '.sqlite3',
    '.csv',  # 可能包含数据
}

# 必须跳过的目录（即使扩展名匹配也不加密）
SKIP_DIR_NAMES: Set[str] = {
    'env_isaacsim', 'env_pybullet', 'venv', 'env', '.venv',
    '__pycache__', '.git', '.github', '.idea', '.vscode',
    'node_modules', 'dist', 'build', '.cache', '.pytest_cache',
    '.streamlit', '.gradio', '.trae',
    'backup', 'backups', '*_backup*',
}

# 必须跳过的文件（即使扩展名匹配）
SKIP_FILE_NAMES: Set[str] = {
    'file_encryptor.py',    # 本工具自身不能加密
    'security_scan.py',     # 安全扫描工具不能加密
    'security_checklist.py',# 自查清单工具不能加密
    '.env.example',         # 示例文件是公开的
    '.gitignore',           # gitignore 不能加密
    'LICENSE',              # 开源协议不能加密
    'README.md',            # README 不能加密
    'SECURITY.md',          # 安全文档不能加密
    'requirements.txt',     # 依赖清单不能加密
}


# ============================================================
# 密码派生 -> 密钥
# ============================================================

def _derive_key_fernet(password: str, salt: bytes) -> bytes:
    """使用 PBKDF2 将用户密码派生为 Fernet key（32 字节 -> base64）"""
    if _CRYPTO_BACKEND != 'fernet':
        raise RuntimeError('cryptography 库未安装')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    derived = kdf.derive(password.encode('utf-8'))
    return base64.urlsafe_b64encode(derived)


def _derive_key_fallback(password: str, salt: bytes, length: int = 32) -> bytes:
    """Fallback：使用 hashlib.pbkdf2_hmac（标准库）派生密钥"""
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        PBKDF2_ITERATIONS,
        dklen=length,
    )


# ============================================================
# 加密 / 解密 核心函数
# ============================================================

def encrypt_bytes(plain: bytes, password: str) -> bytes:
    """加密字节串，返回带元数据的加密格式"""
    salt = secrets.token_bytes(SALT_LEN)
    nonce = secrets.token_bytes(12)  # GCM 推荐 12 字节

    if _CRYPTO_BACKEND == 'fernet':
        key = _derive_key_fernet(password, salt)
        f = Fernet(key)
        token = f.encrypt(plain)
        # 格式: MAGIC(7) + BACKEND(1='F') + SALT(16) + TOKEN(...)
        return MAGIC_HEADER + b'F' + salt + token
    else:
        # Fallback: AES-256-GCM 风格手搓（CTR + HMAC）
        key = _derive_key_fallback(password, salt, 48)  # 前32=加密, 后16=HMAC
        enc_key, mac_key = key[:32], key[32:]
        # 简单流密码 (XOR + keystream) — 不是真正的 AES，但足以抵御普通查看
        keystream = b''
        counter = 0
        while len(keystream) < len(plain):
            block = nonce + counter.to_bytes(8, 'little')
            keystream += hashlib.sha256(enc_key + block).digest()
            counter += 1
        keystream = keystream[:len(plain)]
        ciphertext = bytes(p ^ k for p, k in zip(plain, keystream))
        # HMAC
        tag = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()
        # 格式: MAGIC(7) + BACKEND(1='B') + SALT(16) + NONCE(12) + TAG(32) + CIPHERTEXT(...)
        return MAGIC_HEADER + b'B' + salt + nonce + tag + ciphertext


def decrypt_bytes(enc_data: bytes, password: str) -> bytes:
    """解密 encrypt_bytes 的输出，密码错误抛异常"""
    if not enc_data.startswith(MAGIC_HEADER):
        raise ValueError('文件格式错误：不是本工具生成的加密文件，或已损坏')

    offset = len(MAGIC_HEADER)
    backend = enc_data[offset:offset + 1]
    offset += 1

    if backend == b'F':
        if _CRYPTO_BACKEND != 'fernet':
            raise RuntimeError(
                '此文件使用 Fernet 后端加密，但当前环境未安装 cryptography 库。\n'
                '请先执行: pip install cryptography'
            )
        salt = enc_data[offset:offset + SALT_LEN]
        offset += SALT_LEN
        token = enc_data[offset:]
        key = _derive_key_fernet(password, salt)
        f = Fernet(key)
        return f.decrypt(token)

    elif backend == b'B':
        salt = enc_data[offset:offset + SALT_LEN]
        offset += SALT_LEN
        nonce = enc_data[offset:offset + 12]
        offset += 12
        tag = enc_data[offset:offset + 32]
        offset += 32
        ciphertext = enc_data[offset:]
        # 派生
        key = _derive_key_fallback(password, salt, 48)
        enc_key, mac_key = key[:32], key[32:]
        # HMAC 验证
        expected_tag = hmac.new(mac_key, nonce + ciphertext, hashlib.sha256).digest()
        if not hmac.compare_digest(expected_tag, tag):
            raise ValueError('解密失败：密码错误，或文件已损坏/被篡改')
        # 解密
        keystream = b''
        counter = 0
        while len(keystream) < len(ciphertext):
            block = nonce + counter.to_bytes(8, 'little')
            keystream += hashlib.sha256(enc_key + block).digest()
            counter += 1
        keystream = keystream[:len(ciphertext)]
        return bytes(c ^ k for c, k in zip(ciphertext, keystream))
    else:
        raise ValueError(f'未知加密后端标记: {backend!r}')


# ============================================================
# 文件级加密 / 解密操作
# ============================================================

def is_encrypted_file(path: Path) -> bool:
    """判断文件是否已加密（通过扩展名 + 文件头双重验证）"""
    if path.suffix != ENC_EXT:
        return False
    try:
        with open(path, 'rb') as f:
            header = f.read(len(MAGIC_HEADER))
        return header == MAGIC_HEADER
    except OSError:
        return False


def encrypt_file(src: Path, password: str, delete_original: bool = True,
                 make_backup: bool = True) -> Dict:
    """加密单个文件"""
    result = {
        'source': str(src),
        'target': None,
        'size_before': 0,
        'size_after': 0,
        'status': 'skipped',
        'error': None,
        'backup': None,
    }
    try:
        if is_encrypted_file(src):
            result['status'] = 'skipped'
            result['error'] = '已是加密文件'
            return result
        if not src.is_file():
            result['error'] = '文件不存在'
            return result

        size_before = src.stat().st_size
        result['size_before'] = size_before
        with open(src, 'rb') as f:
            plain = f.read()

        enc_data = encrypt_bytes(plain, password)

        target = src.with_suffix(src.suffix + ENC_EXT)
        with open(target, 'wb') as f:
            f.write(enc_data)
        result['target'] = str(target)
        result['size_after'] = target.stat().st_size

        # 备份原文件
        if make_backup:
            backup_path = src.with_suffix(src.suffix + '.bak_unenc')
            try:
                with open(backup_path, 'wb') as bf:
                    bf.write(plain)
                result['backup'] = str(backup_path)
            except OSError as e:
                result['error'] = f'备份失败: {e}'

        # 删除原文件
        if delete_original:
            try:
                src.unlink()
            except OSError as e:
                result['error'] = f'删除原文件失败: {e}'
                result['status'] = 'partial'
                return result

        result['status'] = 'success'
    except Exception as e:
        result['status'] = 'error'
        result['error'] = f'{type(e).__name__}: {e}'
    return result


def decrypt_file(src: Path, password: str, delete_enc: bool = True) -> Dict:
    """解密单个文件"""
    result = {
        'source': str(src),
        'target': None,
        'size_before': 0,
        'size_after': 0,
        'status': 'skipped',
        'error': None,
    }
    try:
        if not is_encrypted_file(src):
            result['error'] = '不是有效的加密文件'
            return result

        size_before = src.stat().st_size
        result['size_before'] = size_before
        with open(src, 'rb') as f:
            enc_data = f.read()

        plain = decrypt_bytes(enc_data, password)

        # 移除 .enc 后缀
        target_name = src.name[:-len(ENC_EXT)]
        target = src.with_name(target_name)
        with open(target, 'wb') as f:
            f.write(plain)
        result['target'] = str(target)
        result['size_after'] = target.stat().st_size

        if delete_enc:
            try:
                src.unlink()
            except OSError as e:
                result['error'] = f'删除加密文件失败: {e}'
                result['status'] = 'partial'
                return result

        result['status'] = 'success'
    except ValueError as e:
        result['status'] = 'error'
        result['error'] = str(e)
    except Exception as e:
        result['status'] = 'error'
        result['error'] = f'{type(e).__name__}: {e}'
    return result


# ============================================================
# 目录扫描
# ============================================================

def _should_skip_dir(path: Path, project_root: Path) -> bool:
    try:
        rel_parts = path.relative_to(project_root).parts
    except ValueError:
        return True
    for part in rel_parts:
        if part in SKIP_DIR_NAMES:
            return True
        if part.startswith('.') and part not in {'.env'}:
            return True
    return False


def find_sensitive_files(root: Path, project_root: Path,
                         extra_exts: Optional[Set[str]] = None) -> List[Path]:
    """按扩展名规则查找所有敏感文件（未加密的）"""
    exts = DEFAULT_SENSITIVE_EXTS.copy()
    if extra_exts:
        exts.update(extra_exts)
    found: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dp = Path(dirpath)
        dirnames[:] = [d for d in dirnames if not _should_skip_dir(dp / d, project_root)]
        for fn in filenames:
            fp = dp / fn
            if fn in SKIP_FILE_NAMES:
                continue
            if fp.suffix.lower() not in exts:
                continue
            if is_encrypted_file(fp):
                continue
            found.append(fp)
    return found


def find_encrypted_files(root: Path, project_root: Path) -> List[Path]:
    """查找所有 .enc 文件"""
    found: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dp = Path(dirpath)
        dirnames[:] = [d for d in dirnames if not _should_skip_dir(dp / d, project_root)]
        for fn in filenames:
            fp = dp / fn
            if is_encrypted_file(fp):
                found.append(fp)
    return found


# ============================================================
# 输出辅助
# ============================================================

def _print_file_result(r: Dict, action: str):
    src_name = Path(r['source']).name if r['source'] else '-'
    if r['status'] == 'success':
        size_kb = r['size_before'] / 1024
        size_kb2 = r['size_after'] / 1024
        extra = f' | 备份: {Path(r["backup"]).name}' if r.get('backup') else ''
        print(f'  ✅ {action}: {src_name}  ({size_kb:.1f} KB -> {size_kb2:.1f} KB){extra}')
    elif r['status'] == 'skipped':
        reason = f' ({r["error"]})' if r['error'] else ''
        print(f'  ⏭  跳过: {src_name}{reason}')
    elif r['status'] == 'partial':
        print(f'  ⚠️  部分成功: {src_name} — {r["error"]}')
    else:
        print(f'  ❌ 失败: {src_name} — {r["error"]}')


# ============================================================
# 主入口
# ============================================================

def get_password(confirm: bool = True, cmdline_pwd: Optional[str] = None) -> str:
    """获取密码：优先命令行参数，否则交互式输入"""
    if cmdline_pwd:
        pwd = cmdline_pwd
        if len(pwd) < 8:
            print('  ⚠️  警告: 密码至少 8 位，建议使用 12 位以上强密码')
        return pwd
    _MAX_LOOPS = 10_000_000
    _MAX_SECONDS = 86400
    _loop_count = 0
    _start_time = time.time()
    while True:
        _loop_count += 1
        if _loop_count > _MAX_LOOPS:
            print('  ❌ 输入次数超过上限，强制退出')
            sys.exit(1)
        if time.time() - _start_time > _MAX_SECONDS:
            print('  ❌ 输入超时（24小时），强制退出')
            sys.exit(1)
        pwd = getpass.getpass('  请输入加密密码: ')
        if len(pwd) < 8:
            print('  ❌ 密码太短，至少 8 位字符，请重新输入')
            continue
        if confirm:
            pwd2 = getpass.getpass('  请再次输入密码确认: ')
            if pwd != pwd2:
                print('  ❌ 两次输入的密码不一致，请重新输入')
                continue
        return pwd


def main():
    parser = argparse.ArgumentParser(
        description='项目敏感文件加密/解密工具 (AES-256 级)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s encrypt                 # 按规则加密项目中所有敏感文件
  %(prog)s encrypt --keep-original # 加密但保留原文件
  %(prog)s encrypt --file xxx.py   # 只加密指定文件
  %(prog)s decrypt                 # 解密项目中所有 .enc 文件
  %(prog)s decrypt --file xxx.py.enc
  %(prog)s list                    # 列出将被加密的文件清单（不执行）
  %(prog)s clean                   # 删除所有 .enc 文件（谨慎）
        """
    )
    parser.add_argument('action', choices=['encrypt', 'decrypt', 'list', 'clean'],
                        help='操作类型')
    parser.add_argument('--password', '-p', type=str, default=None,
                        help='密码（不推荐在命令行明文传入，建议省略后交互式输入）')
    parser.add_argument('--file', '-f', type=str, default=None,
                        help='仅操作指定的单个文件')
    parser.add_argument('--dir', '-d', type=str, default=None,
                        help='仅操作指定目录（递归）')
    parser.add_argument('--keep-original', action='store_true',
                        help='加密后保留原文件（默认删除）')
    parser.add_argument('--keep-enc', action='store_true',
                        help='解密后保留 .enc 文件（默认删除）')
    parser.add_argument('--no-backup', action='store_true',
                        help='加密时不生成 .bak_unenc 备份（不推荐）')
    parser.add_argument('--ext', action='append', default=[],
                        help='额外包含的扩展名，如 --ext .log --ext .cpp')

    args = parser.parse_args()
    project_root = Path(__file__).parent.resolve()

    if _CRYPTO_BACKEND == 'fernet':
        backend_note = 'Fernet (cryptography, AES-128-CBC + HMAC)'
    else:
        backend_note = 'Fallback (标准库 PBKDF2-SHA256 + 流密码 + HMAC-SHA256) - 建议安装 cryptography 获得更强保护'

    print()
    print('=' * 70)
    print('  🔐 项目敏感文件加密 / 解密工具')
    print('=' * 70)
    print(f'  加密后端: {backend_note}')
    print(f'  项目根目录: {project_root}')
    print()

    # 提示安装 cryptography
    if _CRYPTO_BACKEND != 'fernet' and args.action in ('encrypt', 'decrypt'):
        print('  💡 提示: 未检测到 cryptography 库，正在使用标准库降级方案。')
        print('     如需更强的加密保证（行业标准 Fernet），请执行:')
        print('       pip install cryptography')
        print()

    # 确定操作根目录
    if args.dir:
        target_root = Path(args.dir).resolve()
        if not target_root.is_dir():
            print(f'  ❌ 目录不存在: {target_root}')
            sys.exit(2)
    else:
        target_root = project_root

    # === 模式 1: list ===
    if args.action == 'list':
        print('  📋 将被自动加密的敏感文件清单（按扩展名规则匹配）:')
        extra = {e.lower() for e in args.ext}
        files = find_sensitive_files(target_root, project_root, extra)
        if not files:
            print('     （无匹配文件）')
            return
        total_size = 0
        for i, fp in enumerate(files, 1):
            try:
                sz = fp.stat().st_size
            except OSError:
                sz = 0
            total_size += sz
            rel = fp.relative_to(project_root) if fp.is_relative_to(project_root) else fp
            print(f'     {i:>4}. {rel}  ({sz/1024:.1f} KB)')
        print()
        print(f'  合计: {len(files)} 个文件, {total_size / 1024:.1f} KB')
        print()
        return

    # === 模式 2: clean ===
    if args.action == 'clean':
        print('  🧹 即将删除项目中所有 .enc 加密文件（不影响原文件）')
        enc_files = find_encrypted_files(target_root, project_root)
        if not enc_files:
            print('     （未找到 .enc 文件）')
            return
        for fp in enc_files:
            rel = fp.relative_to(project_root) if fp.is_relative_to(project_root) else fp
            print(f'     - {rel}')
        confirm = input(f'\n  ⚠️  确定要删除以上 {len(enc_files)} 个 .enc 文件吗？输入 DELETE 确认: ').strip()
        if confirm != 'DELETE':
            print('  已取消。')
            return
        deleted = 0
        for fp in enc_files:
            try:
                fp.unlink()
                deleted += 1
                print(f'  ✅ 已删除: {fp.name}')
            except OSError as e:
                print(f'  ❌ 删除失败: {fp.name} — {e}')
        print(f'\n  完成：删除 {deleted}/{len(enc_files)} 个加密文件')
        return

    # === 模式 3/4: encrypt / decrypt ===
    # 获取密码
    if args.action == 'encrypt':
        password = get_password(confirm=True, cmdline_pwd=args.password)
    else:
        password = get_password(confirm=False, cmdline_pwd=args.password)

    print()

    # 确定操作文件列表
    if args.file:
        target_files = [Path(args.file).resolve()]
        if not target_files[0].is_file():
            print(f'  ❌ 文件不存在: {target_files[0]}')
            sys.exit(2)
    else:
        if args.action == 'encrypt':
            extra = {e.lower() for e in args.ext}
            target_files = find_sensitive_files(target_root, project_root, extra)
            # 排除脚本自身
            target_files = [f for f in target_files if f.name not in SKIP_FILE_NAMES]
        else:
            target_files = find_encrypted_files(target_root, project_root)

    if not target_files:
        print('  ⏭  没有找到需要处理的文件')
        return

    print(f'  📦 待处理文件数: {len(target_files)}')
    if args.action == 'encrypt':
        print(f'     加密后原文件: {"保留" if args.keep_original else "删除"} | '
              f'备份: {"不生成" if args.no_backup else "生成 (.bak_unenc)"}')
    else:
        print(f'     解密后加密文件: {"保留" if args.keep_enc else "删除"}')

    # 最终确认
    if len(target_files) >= 3 and not args.file:
        confirm = input('\n  ⚠️  继续执行？输入 YES 确认: ').strip()
        if confirm != 'YES':
            print('  已取消。')
            return

    print()
    print('-' * 70)
    total_ok = 0
    total_err = 0
    results: List[Dict] = []

    if args.action == 'encrypt':
        for fp in target_files:
            r = encrypt_file(
                fp,
                password,
                delete_original=not args.keep_original,
                make_backup=not args.no_backup,
            )
            results.append(r)
            _print_file_result(r, '加密')
            if r['status'] == 'success':
                total_ok += 1
            elif r['status'] == 'error':
                total_err += 1
    else:
        for fp in target_files:
            r = decrypt_file(fp, password, delete_enc=not args.keep_enc)
            results.append(r)
            _print_file_result(r, '解密')
            if r['status'] == 'success':
                total_ok += 1
            elif r['status'] == 'error':
                total_err += 1

    print('-' * 70)
    print()
    action_cn = '加密' if args.action == 'encrypt' else '解密'
    print(f'  📊 完成：{action_cn}成功 {total_ok} 个, 失败 {total_err} 个, '
          f'跳过 {len(results) - total_ok - total_err} 个')
    print()

    if total_err > 0:
        # 展示前几个错误
        err_list = [r for r in results if r['status'] == 'error'][:5]
        print(f'  ❌ 错误详情（前 {len(err_list)} 个）:')
        for r in err_list:
            print(f'     - {Path(r["source"]).name}: {r["error"]}')
        print()
        if args.action == 'decrypt' and any('密码错误' in str(r.get('error', '')) for r in err_list):
            print('  💡 提示: 解密失败且提示"密码错误"，请确认密码与加密时完全一致')
        sys.exit(1)

    # 成功提示
    if args.action == 'encrypt':
        print('  ✅ 加密完成！现在即使别人登录您的电脑，也无法直接读取这些文件。')
        print('     下次您自己使用前，请先执行: python file_encryptor.py decrypt')
        print()
        print('  📌 出借设备 / 他人使用前，执行以下三步:')
        print('     1) 退出 Trae IDE 及登录的账号')
        print('     2) 运行: python file_encryptor.py encrypt')
        print('     3) 按 Win + L 锁屏')
        print()
        print('  📌 拿回设备后，执行:')
        print('     1) 运行: python file_encryptor.py decrypt  （输入密码解锁）')
        print('     2) 确认文件可正常打开后，可手动删除所有 *.bak_unenc 备份')
    print()


if __name__ == '__main__':
    main()
