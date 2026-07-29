
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
import zipfile
from PIL import Image
import io

def convert_livp_to_png(livp_path, output_path=None, max_cm=5):
    try:
        if output_path is None:
            output_path = livp_path.rsplit('.', 1)[0] + '.png'

        with zipfile.ZipFile(livp_path, 'r') as zf:
            file_list = zf.namelist()
            print(f"  Contents: {file_list}")

            image_data = None
            for name in file_list:
                if name.lower().endswith(('.jpg', '.jpeg', '.heic', '.heif')):
                    image_data = zf.read(name)
                    print(f"  Found image: {name}")
                    break

            if image_data is None:
                for name in file_list:
                    if name.lower().endswith('.png'):
                        image_data = zf.read(name)
                        print(f"  Found image: {name}")
                        break

            if image_data is None:
                for name in file_list:
                    content = zf.read(name)
                    if len(content) > 1000 and not name.endswith('.mov'):
                        image_data = content
                        print(f"  Found data: {name}")
                        break

            if image_data:
                img = Image.open(io.BytesIO(image_data))
                img = img.convert('RGB')

                dpi = 96
                max_pixels = max_cm * 2.54 * dpi
                width, height = img.size
                print(f"  Original size: {width}x{height} pixels")

                if max(width, height) > max_pixels:
                    ratio = max_pixels / max(width, height)
                    new_width = int(width * ratio)
                    new_height = int(height * ratio)
                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    print(f"  Resized to: {new_width}x{new_height} pixels ({max_cm}cm max)")

                img.save(output_path, 'PNG')
                file_size = os.path.getsize(output_path) / 1024
                print(f"  Success: {os.path.basename(livp_path)} -> {os.path.basename(output_path)} ({file_size:.2f} KB)")
                return True
            else:
                print(f"  No image found in {os.path.basename(livp_path)}")
                return False

    except Exception as e:
        print(f"  Failed: {os.path.basename(livp_path)} - {e}")
        import traceback
        traceback.print_exc()
        return False

desktop = os.path.join(os.path.expanduser("~"), "Desktop")
livp_files = [f for f in os.listdir(desktop) if f.lower().endswith('.livp')]

print(f"Found {len(livp_files)} .livp files on desktop\n")

for livp_file in livp_files:
    livp_path = os.path.join(desktop, livp_file)
    print(f"Processing: {livp_file}")
    convert_livp_to_png(livp_path, max_cm=5)
    print()

print("Done!")