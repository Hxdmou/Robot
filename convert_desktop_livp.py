
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

import zipfile
import os
from PIL import Image
from io import BytesIO

def convert_livp_to_png(livp_path, output_dir):
    """将单个LIVP文件转换为PNG"""
    try:
        with zipfile.ZipFile(livp_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            
            for file_name in file_list:
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    with zip_ref.open(file_name) as img_file:
                        img_data = img_file.read()
                        img = Image.open(BytesIO(img_data))
                        
                        # 生成输出文件名
                        base_name = os.path.basename(livp_path)
                        output_name = os.path.splitext(base_name)[0] + '.png'
                        output_path = os.path.join(output_dir, output_name)
                        
                        img.save(output_path, 'PNG')
                        print(f"✅ 已转换: {livp_path} -> {output_path}")
                        return True
        print(f"❌ 未找到图片: {livp_path}")
        return False
    except Exception as e:
        print(f"❌ 转换失败 {livp_path}: {e}")
        return False

def convert_desktop_livp():
    """转换桌面上的所有LIVP文件"""
    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    print(f"📁 桌面路径: {desktop_path}")
    
    # 查找所有LIVP文件
    livp_files = []
    for file in os.listdir(desktop_path):
        if file.lower().endswith('.livp'):
            livp_files.append(os.path.join(desktop_path, file))
    
    if not livp_files:
        print("❌ 桌面上未找到LIVP文件")
        return
    
    print(f"🔍 找到 {len(livp_files)} 个LIVP文件:")
    for i, file in enumerate(livp_files, 1):
        print(f"  {i}. {os.path.basename(file)}")
    
    # 创建输出目录
    output_dir = os.path.join(desktop_path, 'LIVP转换结果')
    os.makedirs(output_dir, exist_ok=True)
    print(f"📂 输出目录: {output_dir}")
    
    # 转换文件
    success_count = 0
    for livp_path in livp_files:
        if convert_livp_to_png(livp_path, output_dir):
            success_count += 1
    
    print(f"\n🎉 转换完成！成功 {success_count}/{len(livp_files)}")
    print(f"📁 结果保存在: {output_dir}")

if __name__ == "__main__":
    convert_desktop_livp()