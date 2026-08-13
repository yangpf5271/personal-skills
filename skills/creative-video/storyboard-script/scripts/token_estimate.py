#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 估算与预警器 — Token Estimate & Alert
============================================
用于分镜脚本 SKILL 步骤执行中，累计已加载文件的 token 估算值，
在接近上下文阈值时主动预警，防止上下文溢出导致后半段质量下降。

估算公式：tokens ≈ bytes × 0.4（中文 UTF-8 经验值）
阈值默认 128K（兼容最保守模型），可按模型调整。

用法（独立测试）：
    python token_estimate.py --files SKILL.md references/题材路由表.txt --threshold 128000

用法（SKILL 内部调用）：
    from token_estimate import TokenTracker
    tracker = TokenTracker(threshold=128000)
    tracker.add("SKILL.md")
    tracker.add("references/题材路由表.txt")
    report = tracker.report()
    if report["alert"]:
        print(report["summary"])

注意：本模块的 TokenTracker 用于事后静态估算（仅文件 token，不含对话开销）。
运行时实时跟踪请使用 token_tracker.py 的 RuntimeTokenTracker（含对话开销预估+释放建议+会话持久化）。
"""

import os
import sys
import argparse
from typing import List, Dict, Optional, Tuple


# ============================================================
# 常量
# ============================================================

TOKEN_RATIO = 0.4  # bytes → tokens 换算系数（中文 UTF-8 经验值）
DEFAULT_THRESHOLD = 128000  # 默认阈值 128K tokens
# 以下两个常量与 token_tracker.py 保持一致，确保两个模块预警行为统一
WARN_RATIO = 0.8  # 80% 预警线（静态估算不含对话开销，留更多余量）
CRITICAL_RATIO = 0.85  # 85% 危险线（与 token_tracker.py 一致）


# ============================================================
# 核心类
# ============================================================

class TokenTracker:
    """跟踪文件加载的累计 token 消耗，提供分级预警。"""

    def __init__(self, threshold: int = DEFAULT_THRESHOLD, ratio: float = TOKEN_RATIO):
        """
        Args:
            threshold: 上下文窗口 token 上限
            ratio: bytes → tokens 换算系数
        """
        self.threshold = threshold
        self.ratio = ratio
        self.records: List[Dict] = []  # [{path, bytes, tokens, step}]

    def estimate_file(self, filepath: str) -> Tuple[int, int]:
        """估算单个文件的 bytes 和 tokens。

        Args:
            filepath: 文件路径

        Returns:
            (bytes, tokens) 元组
        """
        try:
            size = os.path.getsize(filepath)
        except OSError:
            return (0, 0)
        return (size, int(size * self.ratio))

    def add(self, filepath: str, step: str = "") -> Dict:
        """记录一个已加载文件。

        Args:
            filepath: 文件路径
            step: 当前步骤标识（如 "Step1", "Q2"）

        Returns:
            该文件的估算记录 dict
        """
        size, tokens = self.estimate_file(filepath)
        name = os.path.basename(filepath)
        record = {
            "path": filepath,
            "name": name,
            "bytes": size,
            "tokens": tokens,
            "step": step,
        }
        self.records.append(record)
        return record

    def cumulative_tokens(self) -> int:
        """返回累计 token 数。"""
        return sum(r["tokens"] for r in self.records)

    def current_ratio(self) -> float:
        """返回当前累计 / 阈值的比例。"""
        if self.threshold == 0:
            return 0.0
        return self.cumulative_tokens() / self.threshold

    def alert_level(self) -> str:
        """返回当前预警级别。

        Returns:
            "safe" | "warn" | "critical"
        """
        ratio = self.current_ratio()
        if ratio >= CRITICAL_RATIO:
            return "critical"
        elif ratio >= WARN_RATIO:
            return "warn"
        return "safe"

    def report(self) -> Dict:
        """生成完整预警报告。

        Returns:
            {
                "records": [...],
                "cumulative_tokens": int,
                "threshold": int,
                "ratio": float,
                "alert": bool,
                "level": str,
                "summary": str,
            }
        """
        cumulative = self.cumulative_tokens()
        ratio = self.current_ratio()
        level = self.alert_level()
        alert = level != "safe"

        # 构建摘要文本
        pct = ratio * 100
        if level == "critical":
            summary = (
                f"[CRITICAL] 累计 {cumulative:,} tokens ({pct:.0f}% of {self.threshold:,})，"
                f"已超出上下文阈值！后续步骤质量将严重下降。"
                f"建议：释放已完成步骤的大文件引用，或精简后续加载。"
            )
        elif level == "warn":
            remaining = self.threshold - cumulative
            summary = (
                f"[WARN] 累计 {cumulative:,} tokens ({pct:.0f}% of {self.threshold:,})，"
                f"剩余预算 {remaining:,} tokens。"
                f"后续步骤需谨慎加载大文件，优先使用索引定位。"
            )
        else:
            summary = (
                f"[OK] 累计 {cumulative:,} tokens ({pct:.0f}% of {self.threshold:,})，"
                f"上下文预算充足。"
            )

        return {
            "records": self.records,
            "cumulative_tokens": cumulative,
            "threshold": self.threshold,
            "ratio": round(ratio, 3),
            "alert": alert,
            "level": level,
            "summary": summary,
        }

    def step_summary(self, step: str) -> str:
        """返回某步骤新增 token 的简报。

        Args:
            step: 步骤标识

        Returns:
            简报字符串
        """
        step_records = [r for r in self.records if r["step"] == step]
        step_tokens = sum(r["tokens"] for r in step_records)
        file_count = len(step_records)
        cumulative = self.cumulative_tokens()
        pct = self.current_ratio() * 100
        return (
            f"[{step}] +{step_tokens:,} tokens ({file_count} files) | "
            f"累计 {cumulative:,} ({pct:.0f}%)"
        )


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Token 估算与预警器 — 估算文件 token 消耗，预警上下文溢出"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="待估算的文件路径列表",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help=f"上下文 token 上限 (默认 {DEFAULT_THRESHOLD})",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="",
        help="模型名 (自动设置阈值: claude=200k, gpt4=128k, gemini=128k)",
    )
    args = parser.parse_args()

    # 模型预设阈值
    threshold = args.threshold
    if args.model:
        model_presets = {
            "claude": 200000,
            "gpt4": 128000,
            "gemini": 128000,
            "libtv": 128000,
        }
        key = args.model.lower()
        if key in model_presets:
            threshold = model_presets[key]
            print(f"模型 {args.model} → 阈值 {threshold:,} tokens")

    tracker = TokenTracker(threshold=threshold)

    print("\n=== 逐文件估算 ===")
    print(f"{'文件':<40} {'bytes':>10} {'tokens':>10}")
    print("-" * 65)

    for f in args.files:
        record = tracker.add(f)
        print(f"{record['name']:<40} {record['bytes']:>10,} {record['tokens']:>10,}")

    print("-" * 65)
    print(f"{'合计':<40} {'':>10} {tracker.cumulative_tokens():>10,}")
    print(f"{'阈值':<40} {'':>10} {threshold:>10,}")
    print(f"{'占比':<40} {'':>10} {tracker.current_ratio()*100:>9.1f}%")

    report = tracker.report()
    print(f"\n{'='*65}")
    print(report["summary"])


if __name__ == "__main__":
    main()
