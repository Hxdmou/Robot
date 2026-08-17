# -*- coding: utf-8 -*-
file_path = r"F:\个人作品\具身智能\generate_business_ppt.py"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

line = lines[1042]  # 0-indexed, line 1043 is index 1042
print("Line 1043:")
print(repr(line))
print("\nCharacters around problem:")
for i, c in enumerate(line):
    if ord(c) > 127 or c == '"':
        print(f"  pos {i}: {repr(c)} U+{ord(c):04X}")
