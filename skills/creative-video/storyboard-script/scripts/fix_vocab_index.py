# -*- coding: utf-8 -*-
"""修复提示词库-词汇库.txt：补注缺失的11个SECTION标记（emoji keycap编码不匹配导致）"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/references"
filepath = os.path.join(BASE, "提示词库-词汇库.txt")

# 需要注入的11个section（#1~#9, #11~#12）
# 用文件中实际出现的emoji header文本——从文件读取后自动匹配
SECTION_MAP = [
    # (关键词片段, SECTION标记)
    ("霸总台词库（24句）", "SECTION:1-霸总台词"),
    ("仙侠台词库（26句）", "SECTION:2-仙侠台词"),
    ("反派压迫台词库（24句）", "SECTION:3-反派压迫台词"),
    ("女主隐忍台词库（22句）", "SECTION:4-女主隐忍台词"),
    ("打脸台词库（24句，全部≤10字）", "SECTION:5-打脸台词"),
    ("爽文爆点台词库（22句，独占一镜）", "SECTION:6-爽文爆点台词"),
    ("悬疑质问台词库（22句）", "SECTION:7-悬疑质问台词"),
    ("诀别台词库（20句，字数=日常×50%）", "SECTION:8-诀别台词"),
    ("重逢台词库（20句）", "SECTION:9-重逢台词"),
    ("内心独白库（24句，第一人称/无口型/≤15字）", "SECTION:11-内心独白"),
    ("旁白词库（20句，四风格）", "SECTION:12-旁白词库"),
]

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

count = 0
for keyword, marker in SECTION_MAP:
    # 在文件中找到包含该关键词的完整行
    for line in content.split("\n"):
        if keyword in line and line.strip().startswith("## "):
            # 找到了对应的header行
            marker_line = f"══════════ {marker} ══════════\n{line}"
            if marker_line in content:
                print(f"  [SKIP] {marker}: 已注入")
                count += 1
                break
            content = content.replace(line, marker_line, 1)
            print(f"  [OK] {marker}: {line.strip()}")
            count += 1
            break
    else:
        print(f"  [WARN] 未找到: {keyword}")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\n补注完成: {count}/11")

# 验证
with open(filepath, "r", encoding="utf-8") as f:
    verified = f.read()
all_markers = [m for _, m in SECTION_MAP] + ["SECTION:10-留钩台词", "SECTION:REF-调用索引"]
for m in all_markers:
    if m in verified:
        print(f"  [✓] {m}")
    else:
        print(f"  [✗] 缺失: {m}")
