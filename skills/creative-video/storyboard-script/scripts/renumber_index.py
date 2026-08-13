#!/usr/bin/env python3
"""Renumber INDEX.txt entries from old 16→17 up to old 25→26."""

import re

INDEX_PATH = "references/INDEX.txt"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Map: old_number -> new_number (shift +1 from 16 onwards)
# Handle special 17a → 18a
renumber_map = {}
for n in range(16, 26):
    renumber_map[str(n)] = str(n + 1)
renumber_map["17a"] = "18a"

# Also update counts: [D] 题材专属 3个→4个, tree 27→28
count_replacements = [
    ("[D] 题材专属 ────────── 3个  步骤6路由加载", "[D] 题材专属 ────────── 4个  步骤6路由加载"),
    ("└── references/            ← 27个知识库（本索引管理）", "└── references/            ← 28个知识库（本索引管理）"),
    ("当前=24", "当前=28"),
]

new_lines = []
for line in lines:
    modified = False
    
    # Apply count replacements first
    for old_str, new_str in count_replacements:
        if old_str in line:
            line = line.replace(old_str, new_str)
            modified = True
            break
    
    if not modified:
        # Renumber: match patterns like "16. " or "17a. "
        m = re.match(r'^(\d+[a-z]?)\. ', line)
        if m:
            old_num = m.group(1)
            if old_num in renumber_map:
                new_num = renumber_map[old_num]
                line = re.sub(r'^\d+[a-z]?\. ', f'{new_num}. ', line)
    
    new_lines.append(line)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

# Verify
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Print all numbered entries for verification
numbered = re.findall(r'^(\d+[a-z]?\. )', content, re.MULTILINE)
print("Renumbered entries:", numbered)
print(f"Total entries: {len(numbered)}")
print("Continuous check:", end=" ")
nums = []
for n in numbered:
    num_str = n.rstrip(". ")
    if num_str[-1].isalpha():
        nums.append((int(num_str[:-1]), num_str[-1]))
    else:
        nums.append((int(num_str), ""))

# Check base numbers are 1-26 continuous
base_nums = [x[0] for x in nums]
expected = list(range(1, 27))
for b, e in zip(base_nums, expected):
    if b != e:
        print(f"GAP at {b} (expected {e})")
        break
else:
    print("PASS — 1→26 continuous")

print(f"\nTree counts:")
for line in content.split("\n"):
    if "知识库" in line and "←" in line:
        print(f"  {line.strip()}")
    if "题材专属" in line:
        print(f"  {line.strip()}")
