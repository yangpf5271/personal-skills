#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inject_field.py - 通用字段注入工具

将自定义字段批量注入到分镜脚本文件中的每个镜头。
取代旧版 add_positioning.py（硬编码路径和内容的一次性脚本）。

用法:
  python inject_field.py <storyboard_file> <field_json> [options]

参数:
  storyboard_file  分镜脚本文件路径（.md格式，镜头以 "### 镜N" 分隔）
  field_json       JSON文件路径，格式: {"1": "字段文本", "2": "字段文本", ...}
                   键为镜头号（字符串），值为要注入的字段文本（含**加粗标题**）

选项:
  --after FIELD    在指定字段后插入（默认: 角色锚点）
  --before FIELD   在指定字段前插入
  --dry-run        仅预览不写入
  --header-pattern 镜头分隔正则（默认: ### 镜(\\d+)）

示例:
  python inject_field.py script.md positioning.json --after "角色锚点"
  python inject_field.py script.md positioning.json --before "场景锚点" --dry-run
  python inject_field.py script.md fields.json --after "角色锚点" --header-pattern '## 镜(\\d+)'

JSON格式示例 (positioning.json):
{
  "1": "**角色站位，站位姿势：** 助产士立于产床右侧...",
  "2": "**角色站位，站位姿势：** 助产士居画面偏左...",
  ...
}

注意:
  - --after 和 --before 互斥，只能选一个
  - 默认 --after "角色锚点"，即在每个镜头的"角色锚点"字段后插入新字段
  - 字段匹配基于 Markdown 加粗格式: **字段名：**
  - 如果某镜头中找不到锚点字段，会跳过并打印警告
  - --dry-run 模式下不会写入文件，仅在终端输出预览
"""

import json
import re
import sys
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="将自定义字段批量注入分镜脚本文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s script.md positioning.json
  %(prog)s script.md positioning.json --after "角色锚点"
  %(prog)s script.md positioning.json --before "场景锚点" --dry-run
        """,
    )
    parser.add_argument(
        "storyboard_file",
        type=str,
        help="分镜脚本文件路径（.md格式）",
    )
    parser.add_argument(
        "field_json",
        type=str,
        help="JSON文件路径，键为镜头号（字符串），值为字段文本",
    )
    insert_group = parser.add_mutually_exclusive_group()
    insert_group.add_argument(
        "--after",
        type=str,
        default="角色锚点",
        help="在指定字段后插入（默认: 角色锚点）",
    )
    insert_group.add_argument(
        "--before",
        type=str,
        help="在指定字段前插入",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅预览不写入",
    )
    parser.add_argument(
        "--header-pattern",
        type=str,
        default=r"### 镜(\d+)",
        help="镜头分隔正则（默认: ### 镜(\\d+)）",
    )
    return parser.parse_args()


def load_field_mapping(json_path: str) -> dict:
    """加载 JSON 字段映射文件"""
    path = Path(json_path)
    if not path.exists():
        print(f"错误: JSON文件不存在: {json_path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 统一转为 int -> str 映射
    return {str(k): v for k, v in data.items()}


def build_insert_pattern(anchor_field: str) -> str:
    """构建字段匹配正则

    匹配格式: **字段名：** 后面跟内容，直到下一个 **字段名：** 或空行
    """
    escaped = re.escape(anchor_field)
    # 匹配: **字段名：** 内容\n\n**下一个字段**
    return rf'(\*\*{escaped}[：:]\*\* [^\n]+)\n\n(\*\*)'


def inject_fields(
    content: str,
    field_map: dict,
    anchor_field: str,
    insert_after: bool,
    header_pattern: str,
) -> tuple:
    """
    将字段注入到分镜脚本内容中

    修复：原实现使用 re.split(rf"({header_pattern})", content)，
    当 header_pattern 内含捕获组（如 (\\d+)）时会产生嵌套组，
    导致每个匹配分割出2个元素（full_match + inner_group），
    循环步长2取到的 body 实际是 inner_group 而非正文。
    现改用 re.finditer + 从尾到头修改，避免分割问题。

    Returns:
        (result_content, injected_count, skipped_shots)
    """
    # 找到所有镜头标题的位置
    matches = list(re.finditer(header_pattern, content))

    if not matches:
        return content, 0, []

    injected_count = 0
    skipped_shots = []

    # 从后向前处理，保持前面的位置不变
    for idx in range(len(matches) - 1, -1, -1):
        match = matches[idx]
        shot_num = match.group(1)
        header_end = match.end()

        # body 范围：从当前标题结束到下一个标题开始（或文件末尾）
        if idx + 1 < len(matches):
            body_end = matches[idx + 1].start()
        else:
            body_end = len(content)

        body = content[header_end:body_end]

        if shot_num not in field_map:
            skipped_shots.append(f"镜{shot_num}: JSON中无此镜头号的字段")
            continue

        field_text = field_map[shot_num]

        if insert_after:
            # 在锚点字段后插入
            pattern = build_insert_pattern(anchor_field)
            replacement = rf"\1\n\n{field_text}\n\n\2"
            new_body, count = re.subn(pattern, replacement, body, count=1)

            if count > 0:
                content = content[:header_end] + new_body + content[body_end:]
                injected_count += 1
            else:
                skipped_shots.append(
                    f"镜{shot_num}: 未找到锚点字段 '**{anchor_field}：**'"
                )
        else:
            # 在锚点字段前插入
            escaped = re.escape(anchor_field)
            pattern = rf'(\n\n)(\*\*{escaped}[：:])'
            replacement = rf"\1{field_text}\n\n\2"
            new_body, count = re.subn(pattern, replacement, body, count=1)

            if count > 0:
                content = content[:header_end] + new_body + content[body_end:]
                injected_count += 1
            else:
                skipped_shots.append(
                    f"镜{shot_num}: 未找到锚点字段 '**{anchor_field}：**'"
                )

    # 恢复正向顺序
    skipped_shots.reverse()

    return content, injected_count, skipped_shots


def main():
    args = parse_args()

    # 加载文件
    storyboard_path = Path(args.storyboard_file)
    if not storyboard_path.exists():
        print(f"错误: 分镜脚本文件不存在: {storyboard_path}")
        sys.exit(1)

    with open(storyboard_path, "r", encoding="utf-8") as f:
        content = f.read()

    field_map = load_field_mapping(args.field_json)

    # 确定插入模式
    if args.before:
        insert_after = False
        anchor_field = args.before
    else:
        insert_after = True
        anchor_field = args.after

    print(f"分镜文件: {storyboard_path}")
    print(f"字段JSON: {args.field_json}")
    print(f"插入位置: {'在' + anchor_field + '后' if insert_after else '在' + anchor_field + '前'}")
    print(f"镜头匹配: {args.header_pattern}")
    print(f"JSON镜头数: {len(field_map)}")
    print("-" * 60)

    # 执行注入
    result, injected_count, skipped_shots = inject_fields(
        content,
        field_map,
        anchor_field,
        insert_after,
        args.header_pattern,
    )

    print(f"成功注入: {injected_count} 镜")
    if skipped_shots:
        print(f"跳过: {len(skipped_shots)} 镜")
        for s in skipped_shots:
            print(f"  - {s}")

    if args.dry_run:
        print("\n[DRY-RUN] 未写入文件。去掉 --dry-run 以实际写入。")
        # 显示第一个成功注入的预览
        if injected_count > 0:
            print("\n--- 预览（第一个注入点附近）---")
            # 找到第一个注入的字段
            for shot_num, text in field_map.items():
                idx = result.find(text)
                if idx != -1:
                    start = max(0, idx - 100)
                    end = min(len(result), idx + len(text) + 100)
                    preview = result[start:end]
                    print(preview)
                    break
    else:
        with open(storyboard_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n已写入: {storyboard_path}")

        # 验证
        with open(storyboard_path, "r", encoding="utf-8") as f:
            verify = f.read()

        # 统计注入的字段数
        for shot_num in field_map:
            text = field_map[shot_num]
            # 提取字段名（**和：**之间的部分）
            name_match = re.match(r"\*\*(.+?)[：:]\*\*", text)
            if name_match:
                field_name = name_match.group(1)
                count = verify.count(f"**{field_name}：**") + verify.count(f"**{field_name}:**")
                print(f"验证: 找到 {count} 处 '{field_name}'")
                break


if __name__ == "__main__":
    main()
