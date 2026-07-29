
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

# 测试项目11的数据结构
import re

with open(EXTERNAL_PROJECT_PATH  # external ref, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到项目11的数据部分
start_line = None
end_line = None

for i, line in enumerate(lines):
    if '项目11：总结与未来规划' in line:
        # 找到项目11开始
        for j in range(i, min(i+10, len(lines))):
            if '"data": [' in lines[j]:
                start_line = j + 1  # 数据开始的下一行
                break
    
    if start_line and line.strip() == ']' and end_line is None:
        # 找到数据结束
        end_line = i
        break

print(f"项目11数据范围: 第{start_line+1}行到第{end_line+1}行")
print()

errors = []

for i in range(start_line, end_line):
    line = lines[i]
    # 使用正则提取行内的数据
    match = re.search(r'\[([^\]]+)\]', line)
    if match:
        row_str = match.group(1)
        # 分割列（处理引号内的逗号）
        cols = []
        current_col = ''
        in_quotes = False
        
        for char in row_str:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
                cols.append(current_col.strip().strip('"'))
                current_col = ''
            else:
                current_col += char
        cols.append(current_col.strip().strip('"'))
        
        print(f"第{i+1}行: {len(cols)}列")
        if len(cols) != 15:
            print(f"  ⚠️ 列数不匹配！期望15列，实际{len(cols)}列")
            errors.append((i+1, len(cols)))
        else:
            print(f"  项目: {cols[0]}")
            print(f"  关键技术指标: '{cols[-1]}'")
    print()

if errors:
    print("=== 发现错误 ===")
    for row_num, actual_cols in errors:
        print(f"第{row_num}行: 列数不足，期望15列，实际{actual_cols}列")
else:
    print("=== 所有行都有15列，数据结构完整 ===")
