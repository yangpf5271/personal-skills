#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行时Token跟踪器 — Runtime Token Tracker
==========================================
在SKILL执行过程中，每次Read文件后调用此脚本，累计token并分级预警。
与token_estimate.py（事后估算）不同，本脚本设计为执行中实时拦截。

工作原理：
1. SKILL每步加载文件后，调用 track_add(filepath, step) 记录
2. 脚本返回当前预警级别：safe / warn / critical
3. warn时建议后续步骤用索引定位替代全文加载
4. critical时建议释放已完成步骤的大文件引用
5. 所有记录持久化到 token_session.json，可事后分析

用法（SKILL内部调用）：
    from token_tracker import RuntimeTokenTracker
    tracker = RuntimeTokenTracker(model="128k")
    tracker.track("SKILL.md", "Q1")
    tracker.track("references/题材路由表.txt", "Q1")
    level = tracker.check()  # → "safe" / "warn" / "critical"
    if level == "critical":
        print(tracker.suggest_release())

独立测试：
    python token_tracker.py --model 128k --files SKILL.md references/题材路由表.txt
"""

import os
import json
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

# === Windows GBK 编码修复 ===
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# === 常量 ===
TOKEN_RATIO = 0.4  # bytes → tokens
# 以下两个常量与 token_estimate.py 保持一致，确保两个模块预警行为统一
WARN_RATIO = 0.80   # 80% 预警（运行时含对话开销，实际更保守）
CRITICAL_RATIO = 0.85  # 85% 危险

# 模型预设
MODEL_PRESETS = {
    "128k": {"threshold": 128000, "name": "128K模型（保守）"},
    "200k": {"threshold": 200000, "name": "Claude等200K模型"},
    "gpt4": {"threshold": 128000, "name": "GPT-4 / 128K"},
    "claude": {"threshold": 200000, "name": "Claude / 200K"},
    "gemini": {"threshold": 128000, "name": "Gemini / 128K"},
    "libtv": {"threshold": 128000, "name": "LibTV / 128K"},
}

# 对话上下文估算（系统提示+对话历史的预估token开销）
DIALOG_OVERHEAD = {
    "quick": 15000,   # 快速模式：系统提示+少量对话
    "full": 25000,    # 完整模式：系统提示+多轮确认+中间输出
}

# 各步骤推荐释放的大文件
RELEASE_CANDIDATES = {
    "Q1": ["题材路由表.txt", "根据剧情故事转脚本.txt"],
    "Q2": ["AIGC-真人短剧-漫剧通用提示词.txt", "知识库-视频风格.txt"],
    "Step1": ["知识库-视频风格.txt"],
    "Step2": ["节奏与钩子设计库.txt"],
    "Step3": ["AIGC-真人短剧-漫剧通用提示词.txt"],
    "Step4": ["S级视觉分层库.txt"],
    "Step5": ["知识库-表情大全.txt"],
    "Step6": ["知识库-运镜整合.txt", "知识库-动作特效.txt", "120个AI漫剧分镜指令大全.txt"],
    "Step7": ["S级漫剧分镜输出模板.txt", "提示词库-音效.txt", "提示词库-负面提示词.txt"],
}


class RuntimeTokenTracker:
    """运行时token跟踪器，在执行过程中实时累计和预警。"""

    def __init__(self, model: str = "128k", mode: str = "full"):
        """
        Args:
            model: 模型名（128k/200k/gpt4/claude/gemini/libtv）
            mode: 执行模式（quick/full）
        """
        preset = MODEL_PRESETS.get(model, MODEL_PRESETS["128k"])
        self.threshold = preset["threshold"]
        self.model_name = preset["name"]
        self.mode = mode
        self.dialog_overhead = DIALOG_OVERHEAD.get(mode, 20000)
        self.records: List[Dict] = []
        self.session_file = Path("scripts/token_session.json")

    def estimate_tokens(self, filepath: str) -> int:
        """估算文件token数"""
        try:
            size = os.path.getsize(filepath)
            return int(size * TOKEN_RATIO)
        except OSError:
            return 0

    def track(self, filepath: str, step: str = "") -> Dict:
        """
        记录一个已加载文件（SKILL每步Read后调用）。

        Args:
            filepath: 文件路径
            step: 当前步骤标识

        Returns:
            该文件的记录dict，含预警级别
        """
        tokens = self.estimate_tokens(filepath)
        name = os.path.basename(filepath)
        record = {
            "path": filepath,
            "name": name,
            "tokens": tokens,
            "step": step,
            "timestamp": datetime.now().isoformat(),
        }
        self.records.append(record)

        level = self.check()
        record["alert_level"] = level

        return record

    def cumulative_tokens(self) -> int:
        """返回累计token（含对话开销）"""
        file_tokens = sum(r["tokens"] for r in self.records)
        return file_tokens + self.dialog_overhead

    def file_tokens_only(self) -> int:
        """返回纯文件token（不含对话开销）"""
        return sum(r["tokens"] for r in self.records)

    def check(self) -> str:
        """
        返回当前预警级别。

        Returns:
            "safe" | "warn" | "critical"
        """
        cumulative = self.cumulative_tokens()
        ratio = cumulative / self.threshold if self.threshold > 0 else 0

        if ratio >= CRITICAL_RATIO:
            return "critical"
        elif ratio >= WARN_RATIO:
            return "warn"
        return "safe"

    def ratio(self) -> float:
        """返回当前占比"""
        return self.cumulative_tokens() / self.threshold if self.threshold > 0 else 0

    def suggest_release(self) -> str:
        """生成释放建议"""
        current_step = self.records[-1]["step"] if self.records else ""
        suggestions = []

        # 找出已完成步骤的大文件
        step_groups: Dict[str, List[Dict]] = {}
        for r in self.records:
            step = r["step"]
            if step not in step_groups:
                step_groups[step] = []
            step_groups[step].append(r)

        for step, records in step_groups.items():
            if step == current_step:
                continue  # 不释放当前步骤的文件
            for r in records:
                if r["tokens"] > 2000:  # 大于2000 tokens的文件建议释放
                    suggestions.append(f"  - [{step}] {r['name']} ({r['tokens']:,} tokens)")

        # 推荐释放的文件
        release_candidates = RELEASE_CANDIDATES.get(current_step, [])

        lines = [
            f"[CRITICAL] 累计 {self.cumulative_tokens():,} tokens ({self.ratio()*100:.0f}% of {self.threshold:,})",
            f"模型: {self.model_name} | 模式: {self.mode}",
            f"文件加载: {self.file_tokens_only():,} tokens | 对话开销: {self.dialog_overhead:,} tokens",
            "",
            "建议释放以下已完成步骤的大文件引用：",
        ]
        if suggestions:
            lines.extend(suggestions)
        else:
            lines.append("  (无可释放的大文件)")
        lines.append("")
        lines.append("后续步骤策略：")
        lines.append("  1. 优先使用P1索引定位（Read索引→Grep→Read段落），不全量加载")
        lines.append("  2. 段落加载限制退回≤2（token≥80K时）")
        lines.append("  3. 跳过非必要的辅助参考库")

        return "\n".join(lines)

    def step_report(self, step: str) -> str:
        """某步骤的token简报"""
        step_records = [r for r in self.records if r["step"] == step]
        step_tokens = sum(r["tokens"] for r in step_records)
        cumulative = self.cumulative_tokens()
        pct = self.ratio() * 100
        level = self.check()
        icon = "🟢" if level == "safe" else ("🟡" if level == "warn" else "🔴")
        return (
            f"{icon} [{step}] +{step_tokens:,} tokens ({len(step_records)} files) | "
            f"累计 {cumulative:,} ({pct:.0f}%) | {level}"
        )

    def full_report(self) -> str:
        """完整报告"""
        level = self.check()
        icon = "🟢" if level == "safe" else ("🟡" if level == "warn" else "🔴")

        lines = [
            f"\n{'='*60}",
            f"  {icon} Token 跟踪报告",
            f"{'='*60}",
            f"  模型: {self.model_name}",
            f"  模式: {self.mode}",
            f"  阈值: {self.threshold:,} tokens",
            f"  累计: {self.cumulative_tokens():,} tokens ({self.ratio()*100:.0f}%)",
            f"  文件: {self.file_tokens_only():,} + 对话: {self.dialog_overhead:,}",
            f"  状态: {level.upper()}",
            f"{'='*60}",
            "",
            f"  {'步骤':<8} {'文件数':>4} {'Tokens':>10} {'累计':>10} {'占比':>6}",
            f"  {'-'*50}",
        ]

        # 按步骤汇总
        step_order = []
        seen = set()
        for r in self.records:
            if r["step"] not in seen:
                seen.add(r["step"])
                step_order.append(r["step"])

        running_total = self.dialog_overhead
        for step in step_order:
            step_records = [r for r in self.records if r["step"] == step]
            step_tokens = sum(r["tokens"] for r in step_records)
            running_total += step_tokens
            pct = running_total / self.threshold * 100
            files = len(step_records)
            lines.append(f"  {step:<8} {files:>4} {step_tokens:>10,} {running_total:>10,} {pct:>5.0f}%")

        lines.append(f"  {'-'*50}")
        lines.append(f"  {'TOTAL':<8} {len(self.records):>4} {self.file_tokens_only():>10,} {self.cumulative_tokens():>10,} {self.ratio()*100:>5.0f}%")
        lines.append("")

        if level == "critical":
            lines.append(self.suggest_release())
        elif level == "warn":
            lines.append("[WARN] 接近阈值，后续步骤优先使用索引定位。")

        return "\n".join(lines)

    def save_session(self):
        """保存会话记录到JSON文件"""
        data = {
            "model": self.model_name,
            "mode": self.mode,
            "threshold": self.threshold,
            "dialog_overhead": self.dialog_overhead,
            "total_tokens": self.cumulative_tokens(),
            "file_tokens": self.file_tokens_only(),
            "ratio": round(self.ratio(), 3),
            "level": self.check(),
            "records": self.records,
            "timestamp": datetime.now().isoformat(),
        }
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.session_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# === CLI入口 ===
def main():
    parser = argparse.ArgumentParser(description="运行时Token跟踪器")
    parser.add_argument("--model", default="128k", choices=list(MODEL_PRESETS.keys()), help="模型名")
    parser.add_argument("--mode", default="full", choices=["quick", "full"], help="执行模式")
    parser.add_argument("--files", nargs="*", help="文件列表（用于独立测试）")
    parser.add_argument("--steps", nargs="*", help="各文件对应的步骤（与files一一对应）")
    args = parser.parse_args()

    tracker = RuntimeTokenTracker(model=args.model, mode=args.mode)
    print(f"\n模型: {tracker.model_name}")
    print(f"阈值: {tracker.threshold:,} tokens")
    print(f"对话开销: {tracker.dialog_overhead:,} tokens")
    print()

    if args.files:
        steps = args.steps or ["test"] * len(args.files)
        for f, s in zip(args.files, steps):
            record = tracker.track(f, s)
            print(f"  [{s}] {record['name']:<40} {record['tokens']:>8,} tokens → {record['alert_level']}")

    print(tracker.full_report())


if __name__ == "__main__":
    main()
