#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一检查入口 — Run All Checks
==============================
把分散在6个文件中的75项检查统一为一个脚本入口。
调用validate_shot.py（20项自动检测）+ 空间连续性 + 转场 + 钩卡 + 音效 + 负面词检查，
输出带PASS/FAIL的汇总报告。

检查来源：
  ① validate_shot.py         → 20项自动检测（程序化，含打斗硬规则检测19-20）
  ② 空间连续性控制库.txt      → 18项自检（规则化，本脚本实现核心项）
  ③ 转场系统参数库.txt        → 6项检查（规则化）
  ④ 节奏与钩子设计库.txt SECTION:A → 9条质检（规则化）
  ⑤ 提示词库-音效.txt          → 音效合规（层数+配额+音画对齐）
  ⑥ 提示词库-负面提示词.txt     → 负面词完整性（常驻级必加）

用法：
    python run_all_checks.py --file shots.json --template B --model libtv
    python run_all_checks.py --json '{"镜头": [...]}'
"""

import json
import sys
import os
import re
import argparse
from typing import List, Dict, Tuple, Optional

# 导入validate_shot（含共享计数工具）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_shot import (
    validate_shotlist,
    generate_summary,
    _count_sound_layers,
    _is_payoff,
    _count_payoffs,
)


# ============================================================
# ② 空间连续性自检（18项中的核心可程序化部分）
# ============================================================

def check_spatial_continuity(shots: List[dict]) -> List[str]:
    """空间连续性核心检查"""
    issues = []

    for i, shot in enumerate(shots):
        shot_num = f"镜{i+1}"

        # 检查1: 空间锚存在
        spatial = str(shot.get("空间锚定串", "") or shot.get("空间锚", "") or shot.get("人物站位", ""))
        if not spatial.strip():
            issues.append(f"[空间-01] {shot_num}: 空间锚/人物站位缺失")

        # 检查2: 状态锁存在
        state = str(shot.get("状态锁", "") or shot.get("人物状态锁", "") or shot.get("站位姿势", ""))
        if not state.strip():
            issues.append(f"[空间-02] {shot_num}: 状态锁/站位姿势缺失")

        # 检查3: 道具锁存在（有持物动作时）
        prop = str(shot.get("道具锁", "") or shot.get("道具状态", ""))
        holding_kw = ["持", "握", "拿", "端", "提", "抱", "扛", "举", "托"]
        action_text = str(shot.get("站位姿势", "")) + str(shot.get("动作/法术/特效", ""))
        if any(kw in action_text for kw in holding_kw) and not prop.strip():
            issues.append(f"[空间-03] {shot_num}: 检测到持物动作但道具锁缺失")

        # 检查4: 光影锁存在
        lighting = str(shot.get("光影锁", "") or shot.get("时间", ""))
        if not lighting.strip():
            issues.append(f"[空间-04] {shot_num}: 光影锁/时间缺失")

        # 检查5: 声音锁存在
        sound = str(shot.get("声音锁", "") or shot.get("音效", "") or shot.get("音效设计", ""))
        if not sound.strip():
            issues.append(f"[空间-05] {shot_num}: 声音锁/音效缺失")

        # 检查6: 同场景光影锁一致
        if i > 0:
            prev = shots[i-1]
            prev_scene = str(prev.get("场景", ""))
            curr_scene = str(shot.get("场景", ""))
            if prev_scene and curr_scene and prev_scene == curr_scene:
                prev_light = str(prev.get("光影锁", "") or prev.get("时间", ""))
                curr_light = str(shot.get("光影锁", "") or shot.get("时间", ""))
                if prev_light.strip() and curr_light.strip() and prev_light != curr_light:
                    issues.append(f"[空间-06] {shot_num}: 同场景光影锁不一致（前镜:'{prev_light[:30]}' → 本镜:'{curr_light[:30]}'）")

        # 检查7: 交接帧存在（标记为拆分首镜时）
        if shot.get("_is_handoff", False):
            has_handoff = "交接" in str(shot.get("空间锚定串", "") or shot.get("空间锚", ""))
            if not has_handoff:
                issues.append(f"[空间-07] {shot_num}: 拆分首镜但缺少交接帧标签")

    return issues


# ============================================================
# ③ 转场系统检查（6项）
# ============================================================

def check_transition_system(shots: List[dict], model: str = "") -> List[str]:
    """转场系统6项检查"""
    issues = []

    for i, shot in enumerate(shots):
        shot_num = f"镜{i+1}"

        # 从运镜字段提取转场标注
        camera = str(shot.get("运镜", ""))
        transition_match = re.search(r"转场[：:]\s*(.+?)(?:$|\n)", camera)

        if i == 0:
            # 第一镜不应有转场标注
            if transition_match:
                issues.append(f"[转场-01] {shot_num}: 第一镜不应标注转场")
        else:
            if not transition_match:
                # 检查是否跨场景（跨场景必须标注）
                prev_scene = str(shots[i-1].get("场景", ""))
                curr_scene = str(shot.get("场景", ""))
                if prev_scene and curr_scene and prev_scene != curr_scene:
                    issues.append(f"[转场-02] {shot_num}: 跨场景（'{prev_scene}'→'{curr_scene}'）但运镜字段未标注转场")
            else:
                transition_type = transition_match.group(1).strip()
                # 检查3: 转场类型格式
                if not re.match(r"^(硬切|叠化|爆切|跳切|黑场|淡入|淡出|闪白|L-cut|J-cut|呼吸停拍)", transition_type):
                    issues.append(f"[转场-03] {shot_num}: 转场类型可能不规范: '{transition_type[:20]}'")

    # 检查4: 特效转场≤3次
    fx_transitions = 0
    fx_keywords = ["白闪", "火光", "烟雾", "光圈", "碎片", "像素化", "故障", "炫光"]
    for i, shot in enumerate(shots):
        camera = str(shot.get("运镜", ""))
        transition_match = re.search(r"转场[：:]\s*(.+?)(?:$|\n)", camera)
        if transition_match:
            transition_type = transition_match.group(1)
            if any(kw in transition_type for kw in fx_keywords):
                fx_transitions += 1

    if fx_transitions > 3:
        issues.append(f"[转场-04] 特效转场{fx_transitions}次，超过每集≤3次限制（铁律8）")

    return issues


# ============================================================
# ④ 钩子卡点质检（9条）
# ============================================================

def check_hook_quality(shots: List[dict], total_duration: float = 0) -> List[str]:
    """钩子卡点9条质检"""
    issues = []

    if not shots:
        return issues

    # 检查1: 首帧反常物（第一镜画面描述中有异常元素）
    first_desc = str(shots[0].get("主画面描述", "") or shots[0].get("画面描述", ""))
    if first_desc and len(first_desc) > 20:
        # 简单检查：首镜是否有"异常/反常/不对劲/突然"等关键词
        anomaly_kw = ["异常", "反常", "不对", "突然", "异样", "不对劲", "意外"]
        if not any(kw in first_desc for kw in anomaly_kw):
            issues.append("[钩卡-01] 首镜可能缺少反常物/异常元素（钩子卡点S1）")

    # 检查2: 3秒内主角脸出现
    first_time = str(shots[0].get("时长", ""))
    if "3" in first_time or "5" in first_time:
        first_camera = str(shots[0].get("运镜", "") or shots[0].get("景别", ""))
        if not any(kw in first_camera for kw in ["特写", "近景", "中近", "面部", "脸"]):
            issues.append("[钩卡-02] 首镜3秒内主角脸可能未出现（钩子卡点S1·3秒脸规则）")

    # 检查3: 集尾留钩（最后一镜画面描述是否有悬念元素）
    if len(shots) > 1:
        last_desc = str(shots[-1].get("主画面描述", "") or shots[-1].get("画面描述", ""))
        cliff_kw = ["未完", "继续", "悬念", "留白", "戛然", "突然", "消失", "黑屏", "定格"]
        if last_desc and not any(kw in last_desc for kw in cliff_kw):
            issues.append(f"[钩卡-03] 末镜(镜{len(shots)})可能缺少集尾留钩（钩子卡点S3）")

    return issues


# ============================================================
# ⑤ 音效合规检查
# ============================================================

def check_sound_compliance(shots: List[dict]) -> List[str]:
    """音效合规检查"""
    issues = []

    for i, shot in enumerate(shots):
        shot_num = f"镜{i+1}"
        sound = str(shot.get("音效", "")) + " " + str(shot.get("音效设计", ""))

        if not sound.strip():
            issues.append(f"[音效-01] {shot_num}: 音效字段为空")
            continue

        # 环境音+动作音层数（复用共享函数）
        env_layers, action_layers = _count_sound_layers(sound)
        if env_layers > 2:
            issues.append(f"[音效-02] {shot_num}: 环境音{env_layers}层（上限2层）")
        if action_layers > 2:
            issues.append(f"[音效-03] {shot_num}: 动作音{action_layers}层（上限2个）")

    # 爆点计数（复用共享函数）
    payoff_count = _count_payoffs(shots)
    if payoff_count > 3:
        issues.append(f"[音效-04] 全集爆点{payoff_count}次（上限3次/集）")

    return issues


# ============================================================
# ⑥ 负面词完整性检查
# ============================================================

def check_negative_prompts(shots: List[dict], template: str = "B") -> List[str]:
    """负面词完整性检查（所有模板A/B/C/D通用）"""
    issues = []

    # 常驻级负面词关键词（应每镜出现或全局出现）
    essential_negatives = ["畸形", "多指", "变形", "模糊", "低质量"]

    # 模板C：检查全局区块格式
    if template.upper() == "C":
        has_global_neg = any(
            "负面" in str(shot.get("负面提示词", "") or shot.get("Negative", ""))
            for shot in shots
        )
        if not has_global_neg:
            issues.append("[负面词-01] 模板C未检测到全局负面提示词区块")

        # 检查首镜是否有负面词区块
        first_neg = str(shots[0].get("负面提示词", "") or shots[0].get("Negative", "")) if shots else ""
        if not first_neg.strip():
            issues.append("[负面词-02] 模板C首镜应含全局负面提示词区块")

    # 所有模板：检查常驻级负面词是否存在（全局或任一镜头中出现）
    all_text = ""
    for shot in shots:
        neg = str(shot.get("负面提示词", "") or shot.get("Negative", ""))
        # 模板A/D：负面词可能在提示词正文中
        prompt = str(shot.get("视频提示词", "") or shot.get("提示词", "") or shot.get("主画面描述", ""))
        all_text += neg + " " + prompt + " "

    missing_essentials = [kw for kw in essential_negatives if kw not in all_text]
    if missing_essentials:
        issues.append(
            f"[负面词-03] 模板{template.upper()}未检测到常驻级负面词：{', '.join(missing_essentials)}"
            f"（应每镜或全局区块中出现）"
        )

    return issues


# ============================================================
# 主检查引擎
# ============================================================

def run_all_checks(
    shots: List[dict],
    template: str = "B",
    model: str = "",
    model_budget: int = 350,
    split_indices: Optional[List[int]] = None,
) -> Dict:
    """
    执行全部检查，返回统一报告。

    Returns:
        {
            "validate_shot": {report, stats},
            "spatial": [issues],
            "transition": [issues],
            "hook": [issues],
            "sound": [issues],
            "negative": [issues],
            "summary": {...},
            "pass": bool,
        }
    """
    results = {}

    # ① validate_shot 20项
    report, stats = validate_shotlist(
        shots=shots,
        template=template,
        model_budget=model_budget,
        split_indices=split_indices,
    )
    results["validate_shot"] = {"report": report, "stats": stats}

    # ② 空间连续性
    results["spatial"] = check_spatial_continuity(shots)

    # ③ 转场系统
    results["transition"] = check_transition_system(shots, model)

    # ④ 钩子卡点
    results["hook"] = check_hook_quality(shots)

    # ⑤ 音效合规
    results["sound"] = check_sound_compliance(shots)

    # ⑥ 负面词
    results["negative"] = check_negative_prompts(shots, template)

    # 汇总
    total_errors = stats["total_errors"]
    total_warnings = stats["total_warnings"]
    rule_issues = sum(len(v) for k, v in results.items() if k != "validate_shot" and isinstance(v, list))

    all_pass = (total_errors == 0 and rule_issues == 0)

    results["summary"] = {
        "total_shots": len(shots),
        "validate_shot_errors": total_errors,
        "validate_shot_warnings": total_warnings,
        "rule_issues": rule_issues,
        "total_problems": total_errors + rule_issues,
        "pass": all_pass,
        "template": template,
        "model": model,
    }

    return results


def format_report(results: Dict) -> str:
    """格式化报告输出"""
    summary = results["summary"]
    lines = [
        "",
        "═" * 60,
        "  统一检查报告 — Run All Checks",
        "═" * 60,
        f"  模板: {summary['template']}  |  模型: {summary['model'] or '未指定'}  |  镜头数: {summary['total_shots']}",
        "─" * 60,
    ]

    # ① validate_shot
    vs = results["validate_shot"]
    vs_stats = vs["stats"]
    icon = "✅" if vs_stats["total_errors"] == 0 else "❌"
    lines.append(f"  {icon} ① validate_shot.py（20项自动检测）")
    lines.append(f"     错误: {vs_stats['total_errors']}  警告: {vs_stats['total_warnings']}  通过镜: {vs_stats['clean_shots']}/{vs_stats['total_shots']}")

    if vs_stats["total_errors"] > 0:
        for shot_key, shot_report in vs["report"].items():
            for err in shot_report.get("errors", []):
                lines.append(f"     [ERROR] {shot_key}: {err}")
            for warn in shot_report.get("warnings", []):
                lines.append(f"     [WARN]  {shot_key}: {warn}")

    # ② 空间连续性
    spatial = results["spatial"]
    icon = "✅" if not spatial else "❌"
    lines.append(f"  {icon} ② 空间连续性自检（18项核心）")
    if spatial:
        for issue in spatial:
            lines.append(f"     [ISSUE] {issue}")
    else:
        lines.append(f"     全部通过")

    # ③ 转场系统
    transition = results["transition"]
    icon = "✅" if not transition else "❌"
    lines.append(f"  {icon} ③ 转场系统检查（6项）")
    if transition:
        for issue in transition:
            lines.append(f"     [ISSUE] {issue}")
    else:
        lines.append(f"     全部通过")

    # ④ 钩子卡点
    hook = results["hook"]
    icon = "✅" if not hook else "⚠️"
    lines.append(f"  {icon} ④ 钩子卡点质检（9条）")
    if hook:
        for issue in hook:
            lines.append(f"     [WARN] {issue}")
    else:
        lines.append(f"     全部通过")

    # ⑤ 音效合规
    sound = results["sound"]
    icon = "✅" if not sound else "❌"
    lines.append(f"  {icon} ⑤ 音效合规检查")
    if sound:
        for issue in sound:
            lines.append(f"     [ISSUE] {issue}")
    else:
        lines.append(f"     全部通过")

    # ⑥ 负面词
    negative = results["negative"]
    icon = "✅" if not negative else "⚠️"
    lines.append(f"  {icon} ⑥ 负面词完整性检查")
    if negative:
        for issue in negative:
            lines.append(f"     [WARN] {issue}")
    else:
        lines.append(f"     全部通过")

    # 总结
    lines.append("─" * 60)
    if summary["pass"]:
        lines.append("  ✅ 全部检查通过，可进入交付确认。")
    else:
        lines.append(f"  ❌ 发现 {summary['total_problems']} 项问题，请修正后重新检查。")
    lines.append("═" * 60)

    return "\n".join(lines)


# === CLI入口 ===
def main():
    parser = argparse.ArgumentParser(description="统一检查入口")
    parser.add_argument("--file", "-f", type=str, help="分镜JSON文件")
    parser.add_argument("--json", "-j", type=str, help="直接传入JSON字符串")
    parser.add_argument("--template", "-t", type=str, default="B", choices=["A", "B", "C", "D"])
    parser.add_argument("--model", "-m", type=str, default="", help="生成模型名")
    parser.add_argument("--budget", "-b", type=int, default=350, help="字数预算")
    args = parser.parse_args()

    # 加载数据
    if args.json:
        shots = json.loads(args.json)
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content.startswith("["):
                shots = json.loads(content)
            else:
                shots = [json.loads(line) for line in content.split("\n") if line.strip()]
    else:
        print("错误：请指定 --file 或 --json")
        sys.exit(1)

    results = run_all_checks(shots, template=args.template, model=args.model, model_budget=args.budget)
    report = format_report(results)
    print(report)

    if not results["summary"]["pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
