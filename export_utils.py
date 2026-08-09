
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
import json
from datetime import datetime
from pathlib import Path
import zipfile
import shutil

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def format_conversation_for_export(conv_data, format_type="markdown"):
    if format_type == "markdown":
        lines = [
            f"# 对话导出记录",
            f"",
            f"**系统**: {conv_data.get('system', '未知')}",
            f"**时间**: {conv_data.get('timestamp', '未知')}",
            f"**消息数**: {len(conv_data.get('messages', []))}",
            f"",
            f"---",
            f""
        ]
        for msg in conv_data.get('messages', []):
            role = "👤 用户" if msg.get('role') == 'user' else "🤖 助手"
            lines.append(f"## {role}")
            lines.append(f"{msg.get('content', '')}")
            lines.append(f"")
        return "\n".join(lines)
    elif format_type == "text":
        lines = []
        for msg in conv_data.get('messages', []):
            role = "用户" if msg.get('role') == 'user' else "助手"
            lines.append(f"[{role}]: {msg.get('content', '')}")
            lines.append(f"")
        return "\n".join(lines)
    return ""

def export_conversation_to_markdown(conv_data, output_path=None):
    content = format_conversation_for_export(conv_data, "markdown")
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(EXPORT_DIR, f"conversation_{timestamp}.md")

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else EXPORT_DIR, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return output_path

def export_conversation_to_text(conv_data, output_path=None):
    content = format_conversation_for_export(conv_data, "text")
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(EXPORT_DIR, f"conversation_{timestamp}.txt")

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else EXPORT_DIR, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return output_path

def export_batch_results(results: list, output_path=None):
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(EXPORT_DIR, f"batch_results_{timestamp}.md")

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else EXPORT_DIR, exist_ok=True)

    lines = [
        f"# 批量问答结果导出",
        f"",
        f"**导出时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**问题数量**: {len(results)}",
        f"",
        f"---",
        f""
    ]

    for i, result in enumerate(results, 1):
        lines.append(f"## 问题 {i}")
        lines.append(f"**问题**: {result.get('question', '')}")
        lines.append(f"")
        lines.append(f"**回答**:")
        lines.append(f"{result.get('answer', '')}")
        lines.append(f"")
        if result.get('sources'):
            lines.append(f"**引用来源**:")
            for src in result.get('sources', []):
                lines.append(f"- {src}")
            lines.append(f"")
        lines.append(f"---")
        lines.append(f"")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    return output_path

def create_backup(backup_name: str = None, include_histories: bool = True, include_indices: bool = True):
    if not backup_name:
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    backup_dir = os.path.join("backups", backup_name)
    os.makedirs(backup_dir, exist_ok=True)

    backup_files = []

    if include_histories:
        chat_history_dir = "chat_histories"
        if os.path.exists(chat_history_dir):
            dest = os.path.join(backup_dir, "chat_histories")
            shutil.copytree(chat_history_dir, dest)
            backup_files.append("chat_histories/")

    if include_indices:
        for suffix in ["_faiss_index", "_index"]:
            for item in os.listdir("."):
                if item.endswith(suffix) and os.path.isdir(item):
                    dest = os.path.join(backup_dir, item)
                    shutil.copytree(item, dest)
                    backup_files.append(f"{item}/")

    manifest = {
        "backup_name": backup_name,
        "timestamp": datetime.now().isoformat(),
        "files": backup_files,
        "include_histories": include_histories,
        "include_indices": include_indices
    }

    with open(os.path.join(backup_dir, "manifest.json"), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    zip_path = f"{backup_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(backup_dir))
                zipf.write(file_path, arcname)

    shutil.rmtree(backup_dir)

    return zip_path, manifest

def restore_backup(zip_path: str):
    if not os.path.exists(zip_path):
        return False, "备份文件不存在"

    extract_dir = os.path.join("backups", "temp_restore")
    os.makedirs(extract_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_dir)

        manifest_path = os.path.join(extract_dir, "manifest.json")
        if not os.path.exists(manifest_path):
            return False, "备份文件格式错误，缺少 manifest.json"

        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        for item in manifest.get("files", []):
            src = os.path.join(extract_dir, item)
            dst = item
            if os.path.exists(src):
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)

        shutil.rmtree(extract_dir)
        return True, f"成功恢复备份: {manifest.get('backup_name')}"
    except Exception as e:
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        return False, f"恢复失败: {str(e)}"

def list_backups():
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)

    backups = []
    for item in os.listdir(backup_dir):
        if item.endswith(".zip"):
            path = os.path.join(backup_dir, item)
            stat = os.stat(path)
            backups.append({
                "name": item,
                "path": path,
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            })
    return sorted(backups, key=lambda x: x["created"], reverse=True)
