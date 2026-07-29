
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
import sys

# 获取桌面路径
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
livp_files = [f for f in os.listdir(desktop) if f.endswith('.livp')]

print(f"找到 {len(livp_files)} 个.livp文件")
print()

converted = 0
failed = 0

for livp_file in livp_files:
    livp_path = os.path.join(desktop, livp_file)
    output_name = os.path.splitext(livp_file)[0] + '.png'
    output_path = os.path.join(desktop, output_name)

    try:
        # .livp文件实际上是ZIP格式
        with zipfile.ZipFile(livp_path, 'r') as zf:
            # 查找HEIC文件
            heic_name = None
            for name in zf.namelist():
                if name.lower().endswith('.heic'):
                    heic_name = name
                    break

            if heic_name:
                # 读取HEIC数据
                heic_data = zf.read(heic_name)

                # 使用PIL打开HEIC（需要heif-python库）
                from PIL import Image
                import io

                # 方法1: 直接用PIL打开（如果支持）
                try:
                    img = Image.open(io.BytesIO(heic_data))
                    img.save(output_path, 'PNG')
                    print(f"✓ 转换成功: {livp_file} -> {output_name}")
                    converted += 1
                except Exception as e1:
                    # 方法2: 尝试用heif库
                    try:
                        import pyheif
                        heif_file = pyheif.read(heic_data)
                        img = Image.frombytes(
                            mode=heif_file.mode,
                            size=heif_file.size,
                            data=heif_file.data
                        )
                        img.save(output_path, 'PNG')
                        print(f"✓ 转换成功: {livp_file} -> {output_name}")
                        converted += 1
                    except Exception as e2:
                        print(f"✗ {livp_file}: 需要安装heif支持 - {e2}")
                        failed += 1
            else:
                # 如果没有HEIC，查找JPEG
                for name in zf.namelist():
                    if name.lower().endswith(('.jpg', '.jpeg')):
                        jpg_data = zf.read(name)
                        img = Image.open(io.BytesIO(jpg_data))
                        img.save(output_path, 'PNG')
                        print(f"✓ 转换成功: {livp_file} -> {output_name}")
                        converted += 1
                        break
                else:
                    print(f"✗ {livp_file}: 未找到图片文件")
                    failed += 1

    except Exception as e:
        print(f"✗ {livp_file}: {str(e)}")
        failed += 1

print()
print(f"转换完成: 成功 {converted}, 失败 {failed}")
print(f"PNG文件保存在桌面")