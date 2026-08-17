# -*- coding: utf-8 -*-
"""用tokenize安全识别字符串，替换字符串内部的半角双引号为单引号"""
import tokenize
import io

file_path = r"F:\个人作品\具身智能\generate_business_ppt.py"
with open(file_path, 'rb') as f:
    tokens = list(tokenize.tokenize(f.readline))

new_tokens = []
for tok in tokens:
    tok_type, tok_str, start, end, line = tok
    if tok_type == tokenize.STRING:
        # 这是一个字符串字面量
        if tok_str.startswith('"') and tok_str.endswith('"') and not tok_str.startswith('"""'):
            # 双引号包裹的普通字符串，不是三引号
            # 提取内部内容，把内部的"替换为'
            inner = tok_str[1:-1]
            if '"' in inner:
                inner = inner.replace('"', "'")
                tok_str = '"' + inner + '"'
    new_tokens.append((tok_type, tok_str, start, end, line))

# 重新写回文件
new_content = tokenize.untokenize(new_tokens)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ tokenize安全处理完成，字符串内部引号已替换")
