
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
from PIL import Image
from io import BytesIO

def convert_livp_to_png(livp_path, output_path=None, max_cm=5):
    try:
        with open(livp_path, 'rb') as f:
            data = f.read()
        
        start_marker = b'\x89PNG\r\n\x1a\n'
        end_marker = b'IEND\xaeB`\x82'
        
        start_idx = data.find(start_marker)
        if start_idx == -1:
            print(f"警告: {livp_path} 中未找到PNG数据")
            return False
        
        end_idx = data.find(end_marker, start_idx)
        if end_idx == -1:
            print(f"警告: {livp_path} 中PNG数据不完整")
            return False
        
        png_data = data[start_idx:end_idx + 8]
        img = Image.open(BytesIO(png_data))
        
        dpi = 96
        max_pixels = max_cm * 2.54 * dpi
        width, height = img.size
        
        if max(width, height) > max_pixels:
            ratio = max_pixels / max(width, height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(livp_path))[0]
            output_path = os.path.join(os.path.dirname(livp_path), f"{base_name}.png")
        
        img.save(output_path, 'PNG', dpi=(dpi, dpi))
        print(f"转换成功: {livp_path} -> {output_path}")
        return True
    
    except Exception as e:
        print(f"转换失败 {livp_path}: {str(e)}")
        return False

def convert_directory(directory):
    livp_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.livp'):
                livp_files.append(os.path.join(root, file))
    
    if not livp_files:
        print(f"在目录 {directory} 中未找到.livp文件")
        return
    
    print(f"找到 {len(livp_files)} 个.livp文件")
    
    success_count = 0
    for livp_file in livp_files:
        if convert_livp_to_png(livp_file):
            success_count += 1
    
    print(f"\n转换完成: {success_count}/{len(livp_files)} 成功")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.path.expanduser("~/Desktop")
    
    convert_directory(directory)