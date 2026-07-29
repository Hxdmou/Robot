"""
J盘增量备份脚本 - Python版本
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


import os
import sys
import json
import hashlib
import shutil
from datetime import datetime

SOURCE_DIR = PROJECT_ROOT
BACKUP_ROOT = r"J:\embodied-intelligence-backup"

EXCLUDE_DIRS = {"env_isaacsim", "env_pybullet", "venv", ".venv", "env", "__pycache__", ".git", "node_modules"}
EXCLUDE_EXTS = {".tmp", ".bak", ".log", ".pyc", ".pyo", ".pyd", ".egg-info", ".egg"}

def get_file_hash(filepath):
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def collect_files():
    files = []
    for root, dirs, filenames in os.walk(SOURCE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXCLUDE_EXTS:
                continue
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, SOURCE_DIR)
            files.append((rel, full))
    return files

def main():
    print("[J-BACKUP] Starting incremental backup to J drive...")
    
    if not os.path.exists(BACKUP_ROOT):
        os.makedirs(BACKUP_ROOT)
        print(f"[J-BACKUP] Created backup root: {BACKUP_ROOT}")
    
    system_backup_dir = os.path.join(BACKUP_ROOT, "system")
    if not os.path.exists(system_backup_dir):
        os.makedirs(system_backup_dir)
    
    all_files = collect_files()
    hash_file = os.path.join(system_backup_dir, "file_hashes.json")
    previous_hashes = {}
    
    if os.path.exists(hash_file):
        try:
            with open(hash_file, "r", encoding="utf-8") as f:
                previous_hashes = json.load(f)
        except:
            previous_hashes = {}
    
    current_hashes = {}
    changed_files = []
    
    for rel, full in all_files:
        try:
            fh = get_file_hash(full)
        except:
            continue
        current_hashes[rel] = fh
        if rel not in previous_hashes or previous_hashes[rel] != fh:
            changed_files.append((rel, full))
    
    if not changed_files:
        print("[J-BACKUP] No changes, skipping backup")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(system_backup_dir, f"backup_{timestamp}")
        os.makedirs(backup_dir, exist_ok=True)
        
        total_size = 0
        for rel, full in changed_files:
            target = os.path.join(backup_dir, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            try:
                shutil.copy2(full, target)
                total_size += os.path.getsize(full)
            except Exception as e:
                print(f"  [WARN] Failed to copy {rel}: {e}")
        
        with open(hash_file, "w", encoding="utf-8") as f:
            json.dump(current_hashes, f, indent=2, ensure_ascii=False)
        
        backup_info = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": SOURCE_DIR,
            "backup_path": backup_dir,
            "file_count": len(changed_files),
            "total_size_bytes": total_size,
            "total_size_human": f"{total_size/1024/1024:.2f} MB",
            "total_files_in_project": len(all_files)
        }
        
        with open(os.path.join(backup_dir, "backup_info.json"), "w", encoding="utf-8") as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        
        print(f"[J-BACKUP] Created backup: backup_{timestamp}")
        print(f"[J-BACKUP] Files copied: {len(changed_files)} (total: {len(all_files)})")
        print(f"[J-BACKUP] Total size: {total_size/1024/1024:.2f} MB")
    
    print("[J-BACKUP] Done")
    print(f"[J-BACKUP] Location: {BACKUP_ROOT}")

if __name__ == "__main__":
    main()
