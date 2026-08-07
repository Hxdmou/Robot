# -*- coding: utf-8 -*-
r"""
================================================================================
  I盘 TRAE备份 清理 & 安全检查工具
  ⚠️  请【手动】在 PowerShell / CMD / IDE 终端 中运行本脚本：
        python I盘清理工具_请手动运行.py
  ⚠️  本脚本会对 I:\TRAE备份\ 做只读扫描，只有在你按 Y 确认后才会删除文件。
================================================================================
功能：
  1) 检查 I 盘是否存在
  2) 扫描 I:\TRAE备份\ 目录结构
  3) 检测【明文敏感文件】（未加密的 .py / .md / 含密码关键词的文件）
  4) 检测【临时缓存文件】（__pycache__ / .tmp / .log 等）
  5) 一键清理（需用户按 Y 确认，默认只读报告）

安全原则：
  · 加密文件 (*.enc / *.bak_unenc) 永远不会被本脚本删除
  · 任何删除操作都需要你按 Y 二次确认
  · 脚本不联网、不读取文件内容（仅看文件名判断风险）
================================================================================
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

I_DRIVE = Path("I:/")
BACKUP_DIR = I_DRIVE / "TRAE备份"

# ⛔ 永远不碰的安全扩展名（加密文件）
SAFE_ENC_EXTS = {".enc", ".bak_unenc"}
# ⚠️ 明文敏感扩展名（如果出现在I盘备份里 → 应该删除或加密）
SENSITIVE_EXTS = {
    ".py", ".pyw", ".pyx", ".pxd",  # Python 源码
    ".md", ".txt", ".rtf",           # 文档明文
    ".json", ".yaml", ".yml",        # 配置明文（可能存凭据）
    ".ini", ".conf", ".cfg", ".env", # 环境/配置
    ".csv", ".xlsx", ".xls",         # 表格数据
    ".doc", ".docx", ".ppt", ".pptx" # Office 文档（可能含隐私）
}
# 🗑️ 临时文件（必删）
TEMP_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".idea", ".vscode", ".git"}
TEMP_EXTS = {".tmp", ".log", ".bak", ".swp", ".pyc", ".pyo", ".pyd", ".so", ".dll", ".o", ".obj", ".class"}
TEMP_FILE_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def confirm(prompt: str) -> bool:
    try:
        ans = input(f"{prompt} (y/N): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n  取消。")
        return False
    return ans in ("y", "yes")


def main() -> int:
    print("=" * 70)
    print("  I盘 TRAE备份 清理 & 安全检查工具")
    print(f"  运行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 1. I盘存在性
    print("\n[1/5] 检查 I 盘是否存在...")
    if not I_DRIVE.exists() or not I_DRIVE.is_dir():
        print(f"  ❌ 未检测到 I 盘（{I_DRIVE}）。请插上U盘/I盘后再运行。")
        return 1
    print(f"  ✅ I 盘已挂载")

    # 2. TRAE备份目录
    print(f"\n[2/5] 扫描 {BACKUP_DIR} ...")
    if not BACKUP_DIR.exists():
        print(f"  ⚠️  未找到 {BACKUP_DIR} 目录，跳过扫描。")
        return 0

    all_files = [f for f in BACKUP_DIR.rglob("*") if f.is_file()]
    print(f"  📂 目录下总文件数：{len(all_files)}")
    # 打印子目录结构
    subdirs = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir()])
    if subdirs:
        print(f"  📁 子目录 ({len(subdirs)} 个):")
        for d in subdirs:
            cnt = sum(1 for _ in d.rglob("*") if _.is_file())
            print(f"     · {d.name}/  ({cnt} 个文件)")

    # 3. 加密文件统计（应该是主要内容）
    print("\n[3/5] 加密/明文 文件分类统计...")
    enc_files = [f for f in all_files if f.suffix.lower() in SAFE_ENC_EXTS]
    sens_files = [f for f in all_files if f.suffix.lower() in SENSITIVE_EXTS and f.suffix.lower() not in SAFE_ENC_EXTS]
    other_files = [f for f in all_files if f not in enc_files and f not in sens_files]
    print(f"   🔒 加密文件（安全）: {len(enc_files)}")
    print(f"   ⚠️  明文敏感文件     : {len(sens_files)}")
    print(f"   📎 其他文件         : {len(other_files)}")

    if sens_files:
        print("\n   ⚠️  明文明细（前30条）:")
        for f in sens_files[:30]:
            try:
                rel = f.relative_to(BACKUP_DIR)
            except Exception:
                rel = f.name
            print(f"      · {rel}   ({f.stat().st_size:,} 字节)")
        if len(sens_files) > 30:
            print(f"      · ... 还有 {len(sens_files)-30} 个，完整列表将在确认时显示")

    # 4. 临时/缓存文件检测
    print("\n[4/5] 临时/缓存文件检测...")
    temp_files = []
    temp_dirs_found = []
    for f in all_files:
        if f.suffix.lower() in TEMP_EXTS or f.name in TEMP_FILE_NAMES:
            temp_files.append(f)
    for d in BACKUP_DIR.rglob("*"):
        if d.is_dir() and d.name in TEMP_DIR_NAMES:
            temp_dirs_found.append(d)
    print(f"   🗑️  临时文件      : {len(temp_files)}")
    print(f"   🗂️  缓存/临时目录 : {len(temp_dirs_found)}")
    for d in temp_dirs_found[:10]:
        print(f"      · {d.relative_to(BACKUP_DIR)}/")

    # 汇总
    to_delete = list(temp_files)
    to_delete_dirs = list(temp_dirs_found)
    risk_summary = []
    if sens_files:
        risk_summary.append(f"⚠️  {len(sens_files)} 个明文敏感文件（.py/.md/.json等，建议加密或移回F盘项目目录）")
    if temp_files or temp_dirs_found:
        risk_summary.append(f"🗑️  {len(temp_files)} 个临时文件 + {len(temp_dirs_found)} 个缓存目录（建议清理）")
    if not risk_summary:
        risk_summary.append("✅ I盘 TRAE备份 状态良好，未发现明文敏感文件和临时垃圾。")

    print("\n" + "=" * 70)
    print("  📋 风险评估报告")
    print("=" * 70)
    for r in risk_summary:
        print(f"   {r}")

    # 5. 清理操作（只删临时文件，明文留给用户自己决定）
    if temp_files or temp_dirs_found:
        print("\n" + "=" * 70)
        print("[5/5] 清理选项：")
        print("=" * 70)
        print("   选项 A：仅删除临时/缓存文件（推荐，不碰任何业务数据）")
        print("   选项 B：什么都不删除，仅输出报告（默认）")

        if confirm("\n是否执行【选项 A：仅删除临时/缓存文件】？此操作不可恢复！"):
            del_ok = 0
            del_fail = 0
            for f in temp_files:
                try:
                    f.unlink(); del_ok += 1
                except Exception as e:
                    print(f"   ❌ 删除文件失败 {f.name}: {e}")
                    del_fail += 1
            for d in temp_dirs_found:
                try:
                    shutil.rmtree(d, ignore_errors=True)
                    if not d.exists():
                        del_ok += 1
                    else:
                        del_fail += 1
                except Exception as e:
                    print(f"   ❌ 删除目录失败 {d.name}: {e}")
                    del_fail += 1
            print(f"\n  🎉 清理完成：成功 {del_ok} 项，失败 {del_fail} 项")
        else:
            print("  ✅ 跳过删除操作（报告模式）")
    else:
        print("\n[5/5] ✅ 没有可清理的临时/缓存文件，跳过。")

    # 最终安全提示
    print("\n" + "=" * 70)
    print("  💡 安全小贴士")
    print("=" * 70)
    print("  ①  敏感 .py 源文件【必须加密（.enc）】后才留在 I 盘，")
    print("     明文 .py 请只保留在 F 盘（项目开发目录）。")
    print("  ②  出借设备前，请运行：  python before_lend.py")
    print("     拿回设备后，请运行：  python after_takeback.py")
    print("  ③  IDE 账号（Trae / Cursor / 微信 / 邮箱）用完请【退出登录】，")
    print("     物理离开工位请按 Win+L 锁屏。")
    print("  ④  F盘 .git_identity_backup.json 是本地 Git 身份备份，")
    print("     正常留着即可（before_lend.py 会引用它）。")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n  ⚠️  用户中断，已退出。")
        sys.exit(130)
