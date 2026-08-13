"""
Fix INDEX.txt numbering: entry "3. AIGC..." at line 68 is a duplicate of
the legitimate "3. 感性意图解码表.txt" at line 53. Shift all B-section
entries onwards by +1. Also remove the ghost entry "18a. 模板B完整示例.txt".
"""
import re

INDEX_PATH = r"C:\Users\Administrator\Desktop\AI\分镜脚本skills\storyboard-script\references\INDEX.txt"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Step 1: Remove ghost entry (lines 291-297, the "18a." block)
# The ghost block starts at 18a.* and ends before the next section header or blank line
# Use 0-indexed: lines 290-296
new_lines = []
skip = False
renumber_from_line = None  # First line with "3. AIGC" that starts the duplicate numbering
ghost_removed_count = 0

for i, line in enumerate(lines):
    # Detect ghost entry start
    if line.strip().startswith("18a.") and "模板B完整示例" in line:
        skip = True
        ghost_removed_count += 1
        continue
    if skip:
        # Skip continuation lines until we hit a blank line or next numbered entry or section header
        stripped = line.strip()
        if stripped == "" or stripped.startswith("══") or stripped.startswith("──") or stripped.startswith("【"):
            skip = False
            if stripped == "":
                continue  # skip the blank line too
        else:
            continue

    new_lines.append(line)

print(f"Removed {ghost_removed_count} ghost entry block(s)")

# Step 2: Renumber entries — from the duplicate "3." to end, shift all entry numbers by +1
# Match patterns like: "3. FileName" or "16a. FileName" at the start of a line (after optional whitespace)
# Only match lines that start with digits followed by optional letter and ". "

def should_renumber(line):
    """Check if this line is a numbered entry line that should be renumbered."""
    stripped = line.strip()
    if not stripped:
        return False
    # Must start with digit(s) + optional lowercase letter + ". "
    if not re.match(r'^\d+[a-z]?\.\s', stripped):
        return False
    return True

def shift_number(line):
    """Increment the leading number by 1, preserving suffix letter."""
    stripped = line.strip()
    m = re.match(r'^(\d+)([a-z]?)\.\s(.*)', stripped)
    if not m:
        return line
    num = int(m.group(1))
    letter = m.group(2)
    rest = m.group(3)
    new_num = num + 1
    # Preserve the original indentation
    indent = line[:len(line) - len(line.lstrip())]
    return f"{indent}{new_num}{letter}. {rest}\n"

# Find the line index where the first duplicate "3." occurs (B-section start)
# This is where "3. AIGC-真人短剧" appears, which is the duplicate
dup_start = None
for i, line in enumerate(new_lines):
    stripped = line.strip()
    if stripped.startswith("3. ") and "AIGC-真人短剧" in stripped:
        dup_start = i
        break

if dup_start is None:
    # Fallback: find first "3. " after line 53 (the legitimate one)
    for i, line in enumerate(new_lines):
        stripped = line.strip()
        if i > 53 and stripped.startswith("3. "):
            dup_start = i
            break

if dup_start is None:
    print("ERROR: Could not find duplicate '3.' entry to start renumbering!")
else:
    print(f"Found duplicate numbering start at line index {dup_start}: {new_lines[dup_start].strip()}")
    renumbered = 0
    for i in range(dup_start, len(new_lines)):
        if should_renumber(new_lines[i]):
            old = new_lines[i].strip()
            new_lines[i] = shift_number(new_lines[i])
            renumbered += 1
    
    print(f"Renumbered {renumbered} entries")

# Also update the total count in the header
for i, line in enumerate(new_lines):
    if "27个知识库" in line:
        new_lines[i] = line.replace("27个知识库", "26个知识库")
        print(f"Updated total count: 27→26")
        break

# Write back
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Done. INDEX.txt updated.")
