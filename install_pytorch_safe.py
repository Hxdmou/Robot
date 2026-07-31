import os
import sys
import urllib.request
import subprocess

print("=" * 60)
print("PyTorch GPU版 安全安装程序")
print("=" * 60)

# 版本配置
PYTORCH_VERSION = "2.11.0"
CUDA_VERSION = "cu128"
PYTHON_VERSION = f"cp{sys.version_info.major}{sys.version_info.minor}"
PLATFORM = "win_amd64"

BASE_URL = f"https://download.pytorch.org/whl/{CUDA_VERSION}"
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "pytorch_install")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

packages = [
    f"torch-{PYTORCH_VERSION}%2B{CUDA_VERSION}-{PYTHON_VERSION}-{PYTHON_VERSION}-{PLATFORM}.whl",
    f"torchvision-0.26.0%2B{CUDA_VERSION}-{PYTHON_VERSION}-{PYTHON_VERSION}-{PLATFORM}.whl",
    f"torchaudio-2.11.0%2B{CUDA_VERSION}-{PYTHON_VERSION}-{PYTHON_VERSION}-{PLATFORM}.whl",
]

print(f"\n下载目录: {DOWNLOAD_DIR}")
print(f"Python版本: {PYTHON_VERSION}")
print(f"目标: PyTorch {PYTORCH_VERSION} + {CUDA_VERSION}\n")

# 第一步：下载所有wheel文件
for pkg in packages:
    url = f"{BASE_URL}/{pkg}"
    local_path = os.path.join(DOWNLOAD_DIR, pkg.replace("%2B", "+"))
    
    if os.path.exists(local_path) and os.path.getsize(local_path) > 100_000_000:
        print(f"[跳过] 已存在: {os.path.basename(local_path)} ({os.path.getsize(local_path)//1024//1024}MB)")
        continue
    
    print(f"[下载] {os.path.basename(local_path)} ...")
    try:
        def report_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, downloaded * 100 // total_size) if total_size > 0 else 0
            mb = downloaded // 1024 // 1024
            total_mb = total_size // 1024 // 1024
            sys.stdout.write(f"\r  进度: {percent}% ({mb}MB / {total_mb}MB)")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, local_path, reporthook=report_progress)
        size_mb = os.path.getsize(local_path) // 1024 // 1024
        print(f"\n[完成] {os.path.basename(local_path)} ({size_mb}MB)")
    except Exception as e:
        print(f"\n[错误] 下载失败: {e}")
        sys.exit(1)

print("\n" + "=" * 60)
print("所有文件下载完成，开始安装...")
print("=" * 60)

# 第二步：安装下载好的wheel
for pkg in packages:
    local_path = os.path.join(DOWNLOAD_DIR, pkg.replace("%2B", "+"))
    print(f"\n[安装] {os.path.basename(local_path)} ...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--no-deps", local_path],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("[成功]")
    else:
        print(f"[警告] {result.stderr.strip()[-200:]}")

print("\n" + "=" * 60)
print("安装依赖...")
print("=" * 60)
subprocess.run([sys.executable, "-m", "pip", "install", "mpmath<1.4", "setuptools<82"], capture_output=True)

print("\n" + "=" * 60)
print("验证安装...")
print("=" * 60)
try:
    import torch
    print(f"PyTorch版本: {torch.__version__}")
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"CUDA可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU名称: {torch.cuda.get_device_name(0)}")
        cap = torch.cuda.get_device_capability(0)
        print(f"GPU计算能力: sm_{cap[0]}{cap[1]}")
        print(f"支持架构: {torch.cuda.get_arch_list()}")
    print("\n✅ 安装成功！")
except Exception as e:
    print(f"\n❌ 验证失败: {e}")
