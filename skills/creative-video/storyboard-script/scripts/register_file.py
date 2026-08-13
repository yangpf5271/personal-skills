#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新增文件注册自动化脚本 — Register New Reference File
====================================================
新增一个reference文件时，需要手动改5处：
1. INDEX.txt 注册新条目
2. 题材路由表 添加到对应簇
3. SKILL.md 步骤调用 添加引用
4. 文件导航.md 更新速查表+section
5. 双目录同步

本脚本自动完成1/2/4/5（步骤3需人工判断在哪个步骤调用，给出提示）。

用法：
    python register_file.py --name "知识库-天气环境动态.txt" --category C --cluster A,B --step 4
    python register_file.py --name "台词时长指南.txt" --category G --cluster all --step 7

参数：
    --name      文件名（含.txt后缀）
    --category  INDEX分类：A/B/C/D/E/F/G/H
    --cluster   题材簇：A/B/C/D/E/F/G/all（逗号分隔多簇）
    --step      SKILL.md步骤号（如4/6/7）
    --optional  是否可选库（默认False=必选）
    --desc      一句话描述（用于INDEX/导航/路由表）
    --version   版本号（默认V1.0）
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import Optional

# === 路径 ===
PROJECT_DIR = Path(r"C:\Users\Administrator\Desktop\AI\分镜脚本skills\storyboard-script")
INSTALL_DIR = Path.home() / ".workbuddy" / "skills" / "storyboard-script"

INDEX_FILE = PROJECT_DIR / "references" / "INDEX.txt"
ROUTE_FILE = PROJECT_DIR / "references" / "题材路由表.txt"
NAV_FILE = PROJECT_DIR / "references" / "文件导航.md"
SKILL_FILE = PROJECT_DIR / "SKILL.md"

# === 分类信息 ===
CATEGORY_INFO = {
    "A": {"name": "规划与路由", "step": "步骤1/1.5调用"},
    "B": {"name": "通用参数", "step": "步骤3/7调用"},
    "C": {"name": "视觉系统", "step": "步骤1/4/5调用"},
    "D": {"name": "题材专属", "step": "步骤6路由加载"},
    "E": {"name": "连续性与节奏", "step": "步骤1.8/2/3.5调用"},
    "F": {"name": "音效", "step": "步骤7调用"},
    "G": {"name": "输出与检查", "step": "步骤7/8调用"},
    "H": {"name": "辅助参考", "step": "按需查阅"},
}

CLUSTER_NAMES = {
    "A": "现代都市",
    "B": "古装武侠",
    "C": "仙侠玄幻",
    "D": "动作打斗",
    "E": "悬疑惊悚",
    "F": "科幻机甲",
    "G": "喜剧搞笑",
}


def get_next_number() -> int:
    """从INDEX.txt获取下一个可用编号"""
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    numbers = re.findall(r"^(\d+)\w?\.\s", content, re.MULTILINE)
    if numbers:
        return max(int(n) for n in numbers) + 1
    return 1


def count_lines(filepath: Path) -> int:
    """统计文件行数"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except:
        return 0


def register_in_index(name: str, category: str, desc: str, version: str, step: str) -> bool:
    """在INDEX.txt中注册新文件"""
    filepath = PROJECT_DIR / "references" / name
    lines = count_lines(filepath)

    num = get_next_number()
    cat_info = CATEGORY_INFO.get(category, {})
    cat_name = cat_info.get("name", "未分类")
    cat_step = cat_info.get("step", "")

    entry = f"""
{num}. {name}
    版本：{version}  ｜  {lines}行
    用途：{desc}
    调用步骤：{step}
    依赖：无
    被引用：SKILL步骤{step}
    修改注意：新增文件，首次注册
"""
    # 在对应分类section末尾插入
    section_pattern = rf"\[{category}\] {re.escape(cat_name)}.*?（\d+个）"
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 找到下一个 [X] section 或 ══ 分隔线
    next_section = re.search(rf"\n\n[{chr(ord(category)+1)}-H] ", content)
    if next_section:
        insert_pos = next_section.start()
        content = content[:insert_pos] + entry + "\n" + content[insert_pos:]
    else:
        # 插入到脚本文件区域之前
        script_pos = content.find("【脚本文件】")
        if script_pos > 0:
            content = content[:script_pos] + entry + "\n" + content[script_pos:]

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    # 更新分类计数
    old_count_pattern = rf"\[{category}\] {re.escape(cat_name)}（(\d+)个）"
    match = re.search(old_count_pattern, content)
    if match:
        old_count = int(match.group(1))
        new_count = old_count + 1
        content = content.replace(
            f"[{category}] {cat_name}（{old_count}个）",
            f"[{category}] {cat_name}（{new_count}个）",
        )
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(content)

    # 更新overview树状图中的计数
    overview_pattern = rf"├─ \[{category}\].*?(\d+)"
    match = re.search(overview_pattern, content)
    if match:
        old_count = int(match.group(1))
        new_count = old_count + 1
        old_line = match.group(0)
        new_line = old_line.replace(str(old_count), str(new_count), 1)
        content = content.replace(old_line, new_line)
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"  [OK] INDEX.txt: 注册 #{num} {name} → [{category}] {cat_name}")
    return True


def register_in_route(name: str, clusters: list, desc: str, optional: bool) -> bool:
    """在题材路由表中注册"""
    with open(ROUTE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    label = "【可选】" if optional else "【必选】"

    for cluster in clusters:
        cluster_name = CLUSTER_NAMES.get(cluster, cluster)
        # 找到对应簇的专属库列表末尾（"说明："行之前）
        pattern = rf"(簇{cluster}.*?)(\n说明：)"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            insert_text = f"  {label}{name} — {desc}\n"
            insert_pos = match.start(2)
            content = content[:insert_pos] + insert_text + content[insert_pos:]
            print(f"  [OK] 题材路由表: 簇{cluster}({cluster_name}) → {label}{name}")
        else:
            print(f"  [WARN] 题材路由表: 未找到簇{cluster}，跳过")

    with open(ROUTE_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def register_in_nav(name: str, category: str, desc: str, step: str) -> bool:
    """在文件导航.md中注册"""
    with open(NAV_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    cat_info = CATEGORY_INFO.get(category, {})
    cat_name = cat_info.get("name", "未分类")

    # 找到对应section的表格末尾（下一个 ## 之前）
    pattern = rf"(## {re.escape(cat_name)}.*?\|.*?\n)(.*?)(\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        new_row = f"| {name} | {desc} | {step} |\n"
        insert_pos = match.start(3) if match.group(3) else len(content)
        content = content[:insert_pos] + new_row + content[insert_pos:]

        # 更新section header计数
        header_pattern = rf"(## {re.escape(cat_name)}.*?)(（\d+个）)"
        match2 = re.search(header_pattern, content)
        if match2:
            old_count = int(re.search(r"(\d+)个", match2.group(2)).group(1))
            new_count = old_count + 1
            content = content.replace(
                f"（{old_count}个）",
                f"（{new_count}个）",
                1  # 只替换第一个匹配
            )

        # 更新速查表计数
        speed_pattern = rf"(\| {re.escape(category)}\..*? \| )(\d+)( \|)"
        match3 = re.search(speed_pattern, content)
        if match3:
            old_count = int(match3.group(2))
            new_count = old_count + 1
            content = content[:match3.start(2)] + str(new_count) + content[match3.end(2):]

        with open(NAV_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [OK] 文件导航.md: 添加到 [{category}] {cat_name}")
    else:
        print(f"  [WARN] 文件导航.md: 未找到 section {cat_name}，跳过")
    return True


def sync_to_install(name: str) -> bool:
    """同步新文件到安装目录"""
    src = PROJECT_DIR / "references" / name
    dst = INSTALL_DIR / "references" / name

    if not src.exists():
        print(f"  [WARN] 源文件不存在: {src}")
        return False

    dst.parent.mkdir(parents=True, exist_ok=True)

    import shutil
    shutil.copy2(src, dst)
    print(f"  [OK] 同步到安装目录: {dst}")

    # 同步修改过的INDEX/路由/导航
    for f in [INDEX_FILE, ROUTE_FILE, NAV_FILE]:
        dst_f = INSTALL_DIR / "references" / f.name
        if f.exists():
            shutil.copy2(f, dst_f)
            print(f"  [OK] 同步 {f.name}")

    return True


def main():
    parser = argparse.ArgumentParser(description="新增文件注册自动化")
    parser.add_argument("--name", required=True, help="文件名（含.txt）")
    parser.add_argument("--category", required=True, choices=list("ABCDEFGH"), help="INDEX分类")
    parser.add_argument("--cluster", default="all", help="题材簇（逗号分隔或all）")
    parser.add_argument("--step", required=True, help="SKILL.md步骤号")
    parser.add_argument("--optional", action="store_true", help="是否可选库")
    parser.add_argument("--desc", required=True, help="一句话描述")
    parser.add_argument("--version", default="V1.0", help="版本号")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  注册新文件: {args.name}")
    print(f"  分类: [{args.category}] | 簇: {args.cluster} | 步骤: {args.step}")
    print(f"{'='*60}\n")

    clusters = ["all"] if args.cluster == "all" else args.cluster.split(",")

    # 1. INDEX注册
    print("[1/4] INDEX.txt 注册...")
    register_in_index(args.name, args.category, args.desc, args.version, args.step)

    # 2. 题材路由表
    print("\n[2/4] 题材路由表 注册...")
    register_in_route(args.name, clusters, args.desc, args.optional)

    # 3. 文件导航.md
    print("\n[3/4] 文件导航.md 注册...")
    register_in_nav(args.name, args.category, args.desc, args.step)

    # 4. 双目录同步
    print("\n[4/4] 双目录同步...")
    sync_to_install(args.name)

    # 5. SKILL.md提示
    print(f"\n{'='*60}")
    print(f"  ✅ 注册完成！")
    print(f"  ⚠️  还需手动在 SKILL.md 步骤{args.step} 中添加对 {args.name} 的调用指令")
    print(f"     建议格式：Read {args.name}（按需/必选）")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
