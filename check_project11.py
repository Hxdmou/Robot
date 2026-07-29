
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

import re

# 读取文件
with open(EXTERNAL_PROJECT_PATH  # external ref, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到项目11的数据部分
start = content.find('{"title": "项目11：总结与未来规划')
end = content.find(']\n        }\n    ]\n', start)
if start == -1 or end == -1:
    print("未找到项目11")
    exit()

project11_data = content[start:end]

# 检查数据结构
print('=== 项目11数据检查 ===')
print()

# 统计行数和列数
rows = re.findall(r'\[.*?\]', project11_data)
print(f'总行数: {len(rows)}')
print()

# 检查每一行的列数
for i, row in enumerate(rows):
    cols = row.split(',')
    print(f'第{i+1}行: {len(cols)}列')
    if i == 0:
        print(f'  表头: {[c.strip().strip("\'\"") for c in cols[:5]]}...')
    else:
        print(f'  第一个单元格: {cols[0].strip().strip("\'\"")}')
        # 检查最后一列（关键技术指标）是否有内容
        last_col = cols[-1].strip().strip('"\']') if cols else ''
        if not last_col or last_col == '-':
            print(f'  ⚠️ 关键技术指标为空！')
        else:
            print(f'  关键技术指标: {last_col[:50]}...')
    print()
