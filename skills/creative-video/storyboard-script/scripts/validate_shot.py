#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则冲突自动检测器 — Validate Shot Constraints
================================================
用于分镜脚本 SKILL 步骤 7.5，在人工步骤8检查之前自动预审20项规则冲突。
输入：分镜 JSON 数组（由 SKILL 在执行过程中生成）
输出：错误报告 (errors[]) + 警告报告 (warnings[])

检测19-20为打斗镜头节奏冲击法则的程序化检测（对应SKILL.md步骤2.4.5八条硬规则中的规则4和规则6）。

用法（SKILL 内部调用）：
    from validate_shot import validate_shotlist
    errors, warnings = validate_shotlist(shots, template="B", model_budget=350)

独立测试：
    python validate_shot.py --file shots_sample.json --template B
"""

import json
import re
import sys
from typing import List, Dict, Tuple, Optional


# ============================================================
# 工具函数
# ============================================================

def _safe_get(obj: dict, key: str, default: str = "") -> str:
    """安全获取字段值，自动做小写标准化"""
    val = obj.get(key, default)
    if not isinstance(val, str):
        return str(val) if val is not None else default
    return val.lower().strip()


def _char_count(text: str) -> int:
    """中文字数统计（忽略英文字母/数字的单字符计数，只统计中文+标点+空格）"""
    if not text:
        return 0
    return len(text.replace("\n", "").replace(" ", ""))


def _extract_emotion_intensity(text: str) -> Optional[int]:
    """从情绪标注中提取强度百分比，如 '冷冽宣告40%' → 40"""
    m = re.search(r"(\d{1,3})\s*%", text)
    if m:
        return int(m.group(1))
    return None


def _extract_scene(text: str) -> str:
    """从空间锚或场景字段中提取场景名"""
    m = re.search(r"场景[：:]\s*(.+?)(?:[｜|\n]|$)", text)
    if m:
        return m.group(1).strip().lower()
    return ""


def _has_keyword(text: str, keywords: List[str]) -> bool:
    """文本中是否包含任意关键词"""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def _extract_direction(text: str) -> List[str]:
    """从文本中提取方向词"""
    directions = []
    direction_patterns = [
        ("左侧", "左"), ("右侧", "右"), ("上方", "上"), ("下方", "下"),
        ("前方", "前"), ("后方", "后"), ("画面左", "左"), ("画面右", "右"),
        ("中央", "中"), ("正中", "中"), ("居中", "中"),
    ]
    for pattern, tag in direction_patterns:
        if pattern in text.lower():
            if tag not in directions:
                directions.append(tag)
    return directions


def _extract_framing_level(shot: dict) -> int:
    """景别转数值：特写=1, 近景=2, 中近景=3, 中景=4, 全景=5, 远景=6"""
    framing_map = {
        "特写": 1, "大特写": 1, "极近景": 1, "特写镜头": 1,
        "近景": 2, "胸像": 2,
        "中近景": 3, "中近": 3, "近中景": 3,
        "中景": 4, "中全景": 4, "膝上": 4,
        "全景": 5, "大全景": 5,
        "远景": 6, "大远景": 6, "极远景": 6,
    }
    framing_text = _safe_get(shot, "景别", "")
    for key, val in framing_map.items():
        if key in framing_text:
            return val
    return 4  # 默认中景


# ============================================================
# 共享计数工具（validate_shot.py 和 run_all_checks.py 共用）
# ============================================================

PAYOFF_KEYWORDS = ["静默", "爆点", "0.3s", "绝对静默"]


def _count_sound_layers(sound_text: str) -> Tuple[int, int]:
    """从音效文本中统计环境音和动作音层数。

    Args:
        sound_text: 合并后的音效字段文本

    Returns:
        (env_layers, action_layers) 元组
    """
    env_layers = 0
    env_match = re.search(r"环境(?:音|音效)[：:]\s*(.+?)(?:[；;]|动作|$)", sound_text)
    if env_match:
        env_text = env_match.group(1).strip()
        if env_text:
            parts = [p.strip() for p in env_text.split("\u00b7") if p.strip()]
            env_layers = len(parts)

    action_layers = 0
    action_match = re.search(r"动作(?:音|音效)[：:]\s*(.+?)(?:[；;]|$)", sound_text)
    if action_match:
        action_text = action_match.group(1).strip()
        if action_text and action_text != "无":
            parts = [p.strip() for p in action_text.split("\u00b7") if p.strip()]
            action_layers = len(parts)

    return (env_layers, action_layers)


def _is_payoff(sound_text: str) -> bool:
    """判断音效文本是否包含爆点标记。"""
    return any(kw in sound_text for kw in PAYOFF_KEYWORDS)


def _count_payoffs(shots: List[dict]) -> int:
    """统计全部镜头中的爆点总次数。"""
    count = 0
    for s in shots:
        sound = _safe_get(s, "音效", "") + " " + _safe_get(s, "音效设计", "")
        if _is_payoff(sound):
            count += 1
    return count


# ============================================================
# 20 项自检清单
# ============================================================

def check_01_spatial_vs_action(shot: dict) -> Optional[str]:
    """检测1：空间锚与动作/运镜方向矛盾"""
    spatial = _safe_get(shot, "空间锚定串", "") or _safe_get(shot, "空间锚", "")
    action = _safe_get(shot, "画面描述", "") + " " + _safe_get(shot, "主画面描述", "")
    action += " " + _safe_get(shot, "运镜", "") + " " + _safe_get(shot, "动作/法术/特效", "") + " " + _safe_get(shot, "视频提示词", "")

    spatial_dirs = _extract_direction(spatial)
    action_dirs = _extract_direction(action)

    # 检测空间锚说"左侧"，但动作描述说"从右侧"
    contradictions = []
    if "左" in spatial_dirs and "从右侧" in action:
        contradictions.append("空间锚标注'左侧'，但动作描述含'从右侧'")
    if "右" in spatial_dirs and "从左侧" in action:
        contradictions.append("空间锚标注'右侧'，但动作描述含'从左侧'")
    if "前" in spatial_dirs and "从后方" in action:
        contradictions.append("空间锚标注'前方'，但动作描述含'从后方'")

    if contradictions:
        return "空间锚与动作方向矛盾：" + "；".join(contradictions)
    return None


def check_02_emotion_jump(prev_shot: Optional[dict], shot: dict, shot_idx: int) -> Optional[str]:
    """检测2：情绪弧线跳跃 > 40%"""
    if prev_shot is None:
        return None

    # 从人物表情或情绪标注中提取强度
    prev_expr = _safe_get(prev_shot, "人物表情", "")
    curr_expr = _safe_get(shot, "人物表情", "")
    prev_desc = _safe_get(prev_shot, "主画面描述", "") + " " + _safe_get(prev_shot, "画面描述", "")
    curr_desc = _safe_get(shot, "主画面描述", "") + " " + _safe_get(shot, "画面描述", "")

    prev_intensity = _extract_emotion_intensity(prev_expr) or _extract_emotion_intensity(prev_desc)
    curr_intensity = _extract_emotion_intensity(curr_expr) or _extract_emotion_intensity(curr_desc)

    # 如果没标注百分比，从情绪词推断（简单映射）
    if prev_intensity is None or curr_intensity is None:
        return None  # 无法自动判断，跳过

    jump = abs(curr_intensity - prev_intensity)
    if jump > 40:
        return f"情绪跳跃超标：镜{shot_idx-1}({prev_intensity}%) → 镜{shot_idx}({curr_intensity}%)，波动{jump}%超过40%上限"
    return None


def check_03_prop_lock_missing(shot: dict) -> Optional[str]:
    """检测3：道具锁缺失（手持/持有物品描述存在但道具锁未标注）"""
    prop_lock = _safe_get(shot, "道具锁", "") or _safe_get(shot, "道具状态", "")

    # 检测动作描述中的手持物品关键词
    holding_keywords = ["持", "握", "拿", "端", "提", "抱", "扛", "举", "托", "拽", "拎", "夹", "执"]
    action_text = _safe_get(shot, "站位姿势", "") + " " + _safe_get(shot, "动作/法术/特效", "")

    has_holding = any(kw in action_text for kw in holding_keywords)

    if has_holding and not prop_lock:
        # 尝试在站位姿势中提取手持物品
        held_items = []
        for kw in holding_keywords:
            if kw in action_text:
                idx = action_text.index(kw)
                snippet = action_text[idx:idx+6]
                held_items.append(snippet.strip())

        items_str = "、".join(held_items[:3]) if held_items else "手持物品"
        return f"道具锁缺失：检测到手持动作({items_str})但道具锁字段为空"

    return None


def check_04_coordinate_anchor_change(prev_shot: Optional[dict], shot: dict, shot_idx: int) -> Optional[str]:
    """检测4：站位轴参照物变化（同场景参照物不应变化）"""
    if prev_shot is None:
        return None

    prev_axis = _safe_get(prev_shot, "站位轴", "")
    curr_axis = _safe_get(shot, "站位轴", "")

    if not prev_axis or not curr_axis:
        return None

    # 提取参照物（以「...」为中心 或 以"..."为中心）
    prev_ref = re.search(r"以[「「\"\"'](.+?)[」」\"\"']", prev_axis)
    curr_ref = re.search(r"以[「「\"\"'](.+?)[」」\"\"']", curr_axis)

    prev_scene = _extract_scene(_safe_get(prev_shot, "场景", ""))
    curr_scene = _extract_scene(_safe_get(shot, "场景", ""))

    if prev_ref and curr_ref:
        prev_center = prev_ref.group(1)
        curr_center = curr_ref.group(1)
        if prev_center != curr_center:
            # 同场景下参照物不应变化
            if prev_scene and curr_scene and prev_scene == curr_scene:
                return f"站位轴参照物在同场景内变化：'{prev_center}' → '{curr_center}'（同场景『{prev_scene}』内参照物应固定）"

    return None


def check_05_state_lock_inconsistency(prev_shot: Optional[dict], shot: dict, shot_idx: int) -> Optional[str]:
    """检测5：状态锁不一致（角色姿态无理由变化）"""
    if prev_shot is None:
        return None

    prev_state = _safe_get(prev_shot, "状态锁", "") or _safe_get(prev_shot, "人物状态锁", "")
    curr_state = _safe_get(shot, "状态锁", "") or _safe_get(shot, "人物状态锁", "")

    if not prev_state or not curr_state:
        return None

    # 简单检测：如果前一镜明确写"僵直不动"而当前镜写"走动"，且中间无剧情理由
    static_keywords = ["僵直", "定格", "不动", "静止", "石化", "僵住", "凝固", "定住"]
    move_keywords = ["走动", "移动", "行走", "步", "转身", "离开", "跑", "冲"]

    prev_is_static = any(kw in prev_state for kw in static_keywords)
    curr_is_moving = any(kw in curr_state for kw in move_keywords)

    if prev_is_static and curr_is_moving:
        # 检查中间是否有过渡镜头或剧情理由
        return f"状态锁疑似不一致：镜{shot_idx-1}标注静止（{', '.join(kw for kw in static_keywords if kw in prev_state)}），镜{shot_idx}突然移动（{', '.join(kw for kw in move_keywords if kw in curr_state)}），请确认是否需要过渡"

    return None


def check_06_lighting_lock_break(prev_shot: Optional[dict], shot: dict, shot_idx: int) -> Optional[str]:
    """检测6：光影锁断裂"""
    if prev_shot is None:
        return None

    prev_scene = _extract_scene(_safe_get(prev_shot, "场景", ""))
    curr_scene = _extract_scene(_safe_get(shot, "场景", ""))
    if prev_scene != curr_scene or not prev_scene:
        return None

    prev_time = _safe_get(prev_shot, "时间", "")
    curr_time = _safe_get(shot, "时间", "")

    # 简单检测：同场景内时间/天气关键词变化
    time_keywords = ["日间", "白天", "正午", "傍晚", "黄昏", "夜间", "夜晚", "午夜", "凌晨", "清晨", "上午", "下午"]
    for tk in time_keywords:
        if tk in prev_time and tk not in curr_time:
            return f"光影锁断裂：同场景『{prev_scene}』内，时间从'{prev_time}'变为'{curr_time}'（含'{tk}'特征词消失）"

    weather_keywords = ["晴", "阴", "雨", "雪", "雾", "风"]
    for wk in weather_keywords:
        if wk in prev_time and wk not in curr_time:
            return f"光影锁断裂：同场景『{prev_scene}』内，天气从'{prev_time}'变为'{curr_time}'"

    return None


def check_07_sound_lock_break(prev_shot: Optional[dict], shot: dict, shot_idx: int) -> Optional[str]:
    """检测7：声音锁断裂"""
    if prev_shot is None:
        return None

    prev_scene = _extract_scene(_safe_get(prev_shot, "场景", ""))
    curr_scene = _extract_scene(_safe_get(shot, "场景", ""))
    if prev_scene != curr_scene or not prev_scene:
        return None

    prev_sound = _safe_get(prev_shot, "音效", "") + " " + _safe_get(prev_shot, "音效设计", "")
    curr_sound = _safe_get(shot, "音效", "") + " " + _safe_get(shot, "音效设计", "")

    if not prev_sound or not curr_sound:
        return None

    # 提取环境音部分（"环境音："之后到"动作音："或"；"之前）
    prev_env = re.search(r"环境(?:音|音效)[：:]\s*(.+?)(?:[；;]|动作|$)", prev_sound)
    curr_env = re.search(r"环境(?:音|音效)[：:]\s*(.+?)(?:[；;]|动作|$)", curr_sound)

    if prev_env and curr_env:
        prev_env_text = prev_env.group(1).strip()
        curr_env_text = curr_env.group(1).strip()
        if prev_env_text != curr_env_text and prev_env_text and curr_env_text:
            return f"声音锁断裂：同场景『{prev_scene}』内环境音从'{prev_env_text[:30]}'变为'{curr_env_text[:30]}'"

    return None


def check_08_spatial_anchor_missing(shot: dict) -> Optional[str]:
    """检测8：空间锚缺失"""
    spatial = _safe_get(shot, "空间锚定串", "") or _safe_get(shot, "空间锚", "")
    # 模板B用"人物站位"等价于空间锚
    positioning = _safe_get(shot, "人物站位", "")

    if not spatial and not positioning:
        return "空间锚（或人物站位）缺失：镜头缺少空间定位信息"
    return None


def check_09_state_lock_missing(shot: dict) -> Optional[str]:
    """检测9：状态锁缺失"""
    state = _safe_get(shot, "状态锁", "") or _safe_get(shot, "人物状态锁", "")
    posture = _safe_get(shot, "站位姿势", "")

    if not state and not posture:
        return "状态锁（或站位姿势）缺失：镜头缺少角色姿态信息"
    return None


def check_10_prop_continuity(prev_shot: Optional[dict], shot: dict, shot_idx: int) -> Optional[str]:
    """检测10：道具状态不一致（物理变化未延续——受伤/被泼/撕裂等）"""
    if prev_shot is None:
        return None

    prev_prop = _safe_get(prev_shot, "道具锁", "") or _safe_get(prev_shot, "道具状态", "")
    curr_prop = _safe_get(shot, "道具锁", "") or _safe_get(shot, "道具状态", "")

    if not prev_prop or not curr_prop:
        return None

    # 检测持久性物理状态：受伤/破损/泼溅 一旦出现必须延续
    persistent_keywords = ["受伤", "破损", "撕裂", "泼溅", "染", "破", "血迹", "瘀", "肿", "烧焦", "浸湿"]

    prev_has_damage = [kw for kw in persistent_keywords if kw in prev_prop]
    curr_has_damage = [kw for kw in persistent_keywords if kw in curr_prop]

    if prev_has_damage and not curr_has_damage:
        return f"道具状态不一致：镜{shot_idx-1}标注了物理变化（{', '.join(prev_has_damage)}），但镜{shot_idx}该状态消失（物理损伤必须延续直到'换装'或'恢复'）"

    return None


def check_11_framing_jump(prev_shot: Optional[dict], shot: dict, shot_idx: int) -> Optional[str]:
    """检测11：景别跳跃（相邻差 > 2级）"""
    if prev_shot is None:
        return None

    prev_level = _extract_framing_level(prev_shot)
    curr_level = _extract_framing_level(shot)

    if abs(curr_level - prev_level) > 2:
        prev_framing = _safe_get(prev_shot, "景别", "未知")
        curr_framing = _safe_get(shot, "景别", "未知")
        return f"景别跳跃超标：镜{shot_idx-1}景别'{prev_framing.strip()}' → 镜{shot_idx}景别'{curr_framing.strip()}'（差{abs(curr_level - prev_level)}级，超过2级上限）"

    return None


def check_12_dialogue_over_budget(shot: dict, budget: int = 200) -> Optional[str]:
    """检测12：台词字数超限"""
    dialogue = _safe_get(shot, "台词", "") or _safe_get(shot, "台词/旁白", "")
    # 提取引号内台词内容（兼容中文引号""和ASCII引号"）
    m = re.search(r'[\u201c"](.+?)[\u201d"]', dialogue)
    if m:
        content = m.group(1)
        count = _char_count(content)
        if count > budget:
            return f"台词字数超限：{count}字（预算{budget}字），内容：'{content[:30]}...'"
    return None


def check_13_sound_layer_over_limit(shot: dict) -> Optional[str]:
    """检测13：音效层数超限"""
    sound = _safe_get(shot, "音效", "") + " " + _safe_get(shot, "音效设计", "")
    env_layers, action_layers = _count_sound_layers(sound)

    errors = []
    if env_layers > 2:
        errors.append(f"环境音{env_layers}层（上限2层）")
    if action_layers > 2:
        errors.append(f"动作音{action_layers}层（上限2层）")

    if errors:
        return "音效层数超限：" + "；".join(errors)
    return None


def check_14_payoff_quota_over(shots: List[dict], current_idx: int) -> Optional[str]:
    """检测14：爆点配额超限（单集 > 3次）"""
    sound_text = _safe_get(shots[current_idx], "音效", "") + " " + _safe_get(shots[current_idx], "音效设计", "")

    if _is_payoff(sound_text):
        payoff_count = sum(
            1 for s in shots[:current_idx + 1]
            if _is_payoff(_safe_get(s, "音效", "") + " " + _safe_get(s, "音效设计", ""))
        )
        if payoff_count > 3:
            return f"爆点配额超限：已使用{payoff_count}次（上限3次/集），镜{current_idx+1}可能超标"
    return None


def check_15_off_screen_character_missing(shot: dict) -> Optional[str]:
    """检测15：画外角色遗漏（多角色场景中部分未标注）"""
    characters = _safe_get(shot, "人物", "")
    posture = _safe_get(shot, "站位姿势", "") or _safe_get(shot, "状态锁", "")

    if not characters or not posture:
        return None

    # 提取人物列表（用｜；、,分隔）
    char_list = re.split(r"[｜|；;、,，]", characters)
    # 限制20字以过滤描述性片段，同时容纳带称号/全名的长角色名
    # （如"唐·马泰奥·亚历山德罗·维塔莱"=15字、"教父·维塔莱"=7字）
    char_list = [c.strip() for c in char_list if c.strip() and len(c.strip()) <= 20]

    for char in char_list:
        if char not in posture and "画外" not in posture:
            # 可能不在画面中但未标注"画外"
            if char not in ["无", "无人物", "空镜"]:
                return f"画外角色漏标：人物列表含'{char}'，但站位姿势/状态锁中未出现且未标注'画外'"

    return None


def check_16_handoff_missing(shot: dict, is_first_after_split: bool = False) -> Optional[str]:
    """检测16：跨视频交接帧缺失"""
    if not is_first_after_split:
        return None

    spatial = _safe_get(shot, "空间锚定串", "") or _safe_get(shot, "空间锚", "")
    has_handoff = "交接" in spatial

    if not has_handoff:
        return "跨视频交接帧缺失：该镜头为视频拆分后的第一镜，缺少[交接]标签"

    return None


def check_17_emotion_value_oob(shot: dict) -> Optional[str]:
    """检测17：情绪弧线值越界（< 0% 或 > 100%）"""
    expr = _safe_get(shot, "人物表情", "")
    desc = _safe_get(shot, "主画面描述", "") + " " + _safe_get(shot, "画面描述", "")

    for text in [expr, desc]:
        matches = re.findall(r"(\d{1,3})\s*%", text)
        for m in matches:
            val = int(m)
            if val < 0:
                return f"情绪值越界：{val}% < 0%（非法负值）"
            if val > 100:
                return f"情绪值越界：{val}% > 100%（超过上限）"

    return None


def check_18_lock_tag_incomplete(shot: dict, template: str = "B") -> Optional[str]:
    """检测18：六层锁标签格式不完整（仅模板C检查）"""
    if template.upper() != "C":
        return None

    missing = []

    spatial = _safe_get(shot, "空间锚定串", "") or _safe_get(shot, "空间锚", "")
    if not spatial or "[空间锚]" not in spatial:
        missing.append("[空间锚]")

    state = _safe_get(shot, "状态锁", "") or _safe_get(shot, "人物状态锁", "")
    if not state or "[状态锁]" not in state:
        missing.append("[状态锁]")

    prop = _safe_get(shot, "道具锁", "")
    if not prop or "[道具锁]" not in prop:
        missing.append("[道具锁]")

    if missing:
        return f"模板C六层锁标签不完整：缺少 {'、'.join(missing)}"

    return None


# ============================================================
# 打斗镜头节奏冲击法则检测（check 19-20）
# 对应 SKILL.md 步骤2.4.5 八条硬规则中可程序化检测的两项
# ============================================================

# 基础运镜关键词（规则4：同一基础动作全镜≤1次）
BASIC_CAMERA_KEYWORDS = [
    "推镜头", "拉镜头", "摇镜头", "移镜头", "升镜头", "降镜头",
    "跟镜头", "旋转", "环绕", "基础推", "基础拉", "基础摇", "基础移",
]

# 复合/特效/专项级运镜关键词（高级运镜，允许重复但建议变化）
ADVANCED_CAMERA_KEYWORDS = [
    "B级", "C级", "D级", "复合", "联动", "动态特效", "专项",
    "希区柯克", "子弹时间", "甩镜", "穿模", "螺旋", "变焦",
    "急推", "急拉", "径向", "爆发",
]


def check_19_combat_camera_repeat(all_shots: List[dict], shot_idx: int) -> Optional[str]:
    """检测19：打斗场景中基础运镜重复（规则4：同一基础运镜全镜≤1次）

    当镜头包含打斗/格斗/战斗关键词时，检查全部打斗镜头的运镜字段，
    若同一基础运镜出现超过1次则报警。
    """
    shot = all_shots[shot_idx]
    camera = _safe_get(shot, "运镜", "")
    action = _safe_get(shot, "动作/法术/特效", "") + " " + _safe_get(shot, "画面描述", "")
    desc = _safe_get(shot, "主画面描述", "")

    # 判断是否为打斗镜头
    combat_keywords = ["打斗", "格斗", "战斗", "搏斗", "拳", "踢", "砍", "刺", "挥", "格挡", "攻击"]
    is_combat = any(kw in action or kw in desc for kw in combat_keywords)
    if not is_combat:
        return None

    # 统计所有打斗镜头中基础运镜出现次数
    basic_camera_counts: Dict[str, int] = {}
    for s in all_shots:
        s_action = _safe_get(s, "动作/法术/特效", "") + " " + _safe_get(s, "画面描述", "")
        s_desc = _safe_get(s, "主画面描述", "")
        s_is_combat = any(kw in s_action or kw in s_desc for kw in combat_keywords)
        if not s_is_combat:
            continue

        s_camera = _safe_get(s, "运镜", "")
        for kw in BASIC_CAMERA_KEYWORDS:
            if kw in s_camera:
                basic_camera_counts[kw] = basic_camera_counts.get(kw, 0) + 1

    # 当前镜头使用的基础运镜中，是否有超过1次的
    current_basics = [kw for kw in BASIC_CAMERA_KEYWORDS if kw in camera]
    repeats = []
    for kw in current_basics:
        total = basic_camera_counts.get(kw, 0)
        if total > 1:
            repeats.append(f"'{kw}'出现{total}次")

    if repeats:
        return (
            f"打斗运镜重复（规则4·全镜≤1次）：{'；'.join(repeats)}，"
            f"请替换为B级复合联动/C级动态特效/D级专项运镜"
        )
    return None


def check_20_combat_closeup_limit(all_shots: List[dict], shot_idx: int) -> Optional[str]:
    """检测20：打斗场景中特写超限（规则6：每场最多1-2次特写）

    统计同一场景内的特写镜头数量，超过2次则报警。
    """
    shot = all_shots[shot_idx]
    scene = _extract_scene(_safe_get(shot, "场景", "") or _safe_get(shot, "空间锚定串", ""))
    if not scene:
        return None

    # 判断当前镜头是否为特写
    framing_text = _safe_get(shot, "景别", "")
    is_closeup = any(kw in framing_text for kw in ["特写", "大特写", "极近景"])
    if not is_closeup:
        return None

    # 统计同场景内所有特写
    closeup_count = 0
    for s in all_shots:
        s_scene = _extract_scene(_safe_get(s, "场景", "") or _safe_get(s, "空间锚定串", ""))
        if s_scene != scene:
            continue
        s_framing = _safe_get(s, "景别", "")
        if any(kw in s_framing for kw in ["特写", "大特写", "极近景"]):
            closeup_count += 1

    if closeup_count > 2:
        return f"特写超限（规则6·每场≤2次）：场景'{scene}'内已有{closeup_count}次特写"
    return None


# ============================================================
# 主检测引擎
# ============================================================

# 分发表：(检测名, 检测函数, 参数spec, 是否为警告)
# 参数spec: 元组，指定从 call_kwargs 中提取哪些参数传给检测函数
# 新增检测项只需在此表追加一行，无需修改 validate_single_shot
CHECK_DISPATCH = [
    ("检测01-空间锚与动作方向矛盾", check_01_spatial_vs_action, ("shot",), False),
    ("检测02-情绪弧线跳跃超标", check_02_emotion_jump, ("prev_shot", "shot", "shot_idx"), False),
    ("检测03-道具锁缺失", check_03_prop_lock_missing, ("shot",), False),
    ("检测04-站位轴参照物变化", check_04_coordinate_anchor_change, ("prev_shot", "shot", "shot_idx"), False),
    ("检测05-状态锁不一致", check_05_state_lock_inconsistency, ("prev_shot", "shot", "shot_idx"), True),
    ("检测06-光影锁断裂", check_06_lighting_lock_break, ("prev_shot", "shot", "shot_idx"), False),
    ("检测07-声音锁断裂", check_07_sound_lock_break, ("prev_shot", "shot", "shot_idx"), False),
    ("检测08-空间锚缺失", check_08_spatial_anchor_missing, ("shot",), False),
    ("检测09-状态锁缺失", check_09_state_lock_missing, ("shot",), False),
    ("检测10-道具状态不一致", check_10_prop_continuity, ("prev_shot", "shot", "shot_idx"), False),
    ("检测11-景别跳跃超标", check_11_framing_jump, ("prev_shot", "shot", "shot_idx"), False),
    ("检测12-台词字数超限", check_12_dialogue_over_budget, ("shot", "model_budget"), True),
    ("检测13-音效层数超限", check_13_sound_layer_over_limit, ("shot",), False),
    ("检测14-爆点配额超限", check_14_payoff_quota_over, ("all_shots", "shot_idx"), False),
    ("检测15-画外角色漏标", check_15_off_screen_character_missing, ("shot",), False),
    ("检测16-跨视频交接帧缺失", check_16_handoff_missing, ("shot", "is_handoff"), False),
    ("检测17-情绪值越界", check_17_emotion_value_oob, ("shot",), False),
    ("检测18-六层锁标签不完整", check_18_lock_tag_incomplete, ("shot", "template"), False),
    ("检测19-打斗运镜重复", check_19_combat_camera_repeat, ("all_shots", "shot_idx"), True),
    ("检测20-打斗特写超限", check_20_combat_closeup_limit, ("all_shots", "shot_idx"), True),
]

# 向后兼容：保留 ALL_CHECKS 名称（仅含 name + function）
ALL_CHECKS = [(name, fn) for name, fn, _, _ in CHECK_DISPATCH]


def validate_single_shot(
    shot: dict,
    prev_shot: Optional[dict],
    shot_idx: int,
    all_shots: Optional[List[dict]] = None,
    template: str = "B",
    is_handoff: bool = False,
    model_budget: int = 350,
) -> Tuple[List[str], List[str]]:
    """
    对单个镜头执行全部20项检测。

    参数：
        shot: 当前镜头 dict
        prev_shot: 上一镜 dict（首镜传 None）
        shot_idx: 当前镜头索引（0-based）
        all_shots: 全部镜头列表（用于配额统计）
        template: 模板档位 'A'/'B'/'C'/'D'
        is_handoff: 是否为跨视频拆分后的第一镜
        model_budget: 生成模型台词字数预算

    返回：
        (errors, warnings): 错误列表 + 警告列表
    """
    errors = []
    warnings = []

    # 构建参数字典，分发表按 spec 提取所需参数
    call_kwargs = {
        "shot": shot,
        "prev_shot": prev_shot,
        "shot_idx": shot_idx,
        "all_shots": all_shots or [],
        "template": template,
        "is_handoff": is_handoff,
        "model_budget": model_budget,
    }

    for check_name, check_fn, arg_spec, is_warning in CHECK_DISPATCH:
        try:
            call_args = tuple(call_kwargs[arg] for arg in arg_spec)
            result = check_fn(*call_args)
            if result:
                if is_warning:
                    warnings.append(f"[{check_name}] {result}")
                else:
                    errors.append(f"[{check_name}] {result}")
        except Exception as e:
            warnings.append(f"[{check_name}] 检测执行异常: {str(e)}")

    return errors, warnings


def validate_shotlist(
    shots: List[dict],
    template: str = "B",
    model_budget: int = 350,
    split_indices: Optional[List[int]] = None,
) -> Tuple[Dict, Dict]:
    """
    对整个分镜列表执行20项自动校验。

    参数：
        shots: 分镜 dict 列表，每个 dict 至少包含模板B/C的必填字段
        template: 'A' / 'B' / 'C' / 'D'
        model_budget: 生成模型字数预算（默认350）
        split_indices: 跨视频拆分的首镜索引列表（如 [10, 20] 表示镜11和镜21是拆分首镜）

    返回：
        (report, stats):
        report = {
            "镜0": {"errors": [...], "warnings": [...]},
            "镜1": {...},
            ...
        }
        stats = {"total_shots": N, "total_errors": N, "total_warnings": N, "clean_shots": N, "has_errors_shots": N}
    """
    report = {}
    total_errors = 0
    total_warnings = 0
    clean_shots = 0
    has_errors_shots = 0

    split_set = set(split_indices or [])

    for i, shot in enumerate(shots):
        prev_shot = shots[i - 1] if i > 0 else None
        is_handoff = i in split_set

        errors, warnings = validate_single_shot(
            shot=shot,
            prev_shot=prev_shot,
            shot_idx=i,
            all_shots=shots,
            template=template,
            is_handoff=is_handoff,
            model_budget=model_budget,
        )

        shot_key = f"镜{i + 1}"
        report[shot_key] = {
            "errors": errors,
            "warnings": warnings,
        }

        if errors:
            has_errors_shots += 1
        else:
            clean_shots += 1

        total_errors += len(errors)
        total_warnings += len(warnings)

    stats = {
        "total_shots": len(shots),
        "total_errors": total_errors,
        "total_warnings": total_warnings,
        "clean_shots": clean_shots,
        "has_errors_shots": has_errors_shots,
        "template": template,
        "model_budget": model_budget,
    }

    return report, stats


def generate_summary(report: Dict, stats: Dict) -> str:
    """生成可读的校验摘要"""
    lines = []
    lines.append("=" * 60)
    lines.append("  规则冲突自动检测 · 校验报告")
    lines.append("=" * 60)
    lines.append(f"  模板档位: {stats['template']}  |  总镜头数: {stats['total_shots']}")
    lines.append(f"  错误数: {stats['total_errors']}  |  警告数: {stats['total_warnings']}")
    lines.append(f"  通过镜: {stats['clean_shots']}  |  问题镜: {stats['has_errors_shots']}")
    lines.append("=" * 60)

    if stats["total_errors"] == 0 and stats["total_warnings"] == 0:
        lines.append("\n[PASS] 全部20项检测通过，无冲突。")
        return "\n".join(lines)

    # 按镜号输出详细报告
    for shot_key in sorted(report.keys(), key=lambda x: int(x.replace("镜", ""))):
        shot_report = report[shot_key]
        errors = shot_report.get("errors", [])
        warnings = shot_report.get("warnings", [])

        if not errors and not warnings:
            continue

        lines.append(f"\n--- {shot_key} ---")
        for err in errors:
            lines.append(f"  [ERROR] {err}")
        for warn in warnings:
            lines.append(f"  [WARN] {warn}")

    # 结论
    lines.append("\n" + "=" * 60)
    if stats["total_errors"] > 0:
        lines.append(f"[WARNING]  发现 {stats['total_errors']} 项错误，请修正后重新校验。")
    else:
        lines.append(f"[PASS] 无错误，仅 {stats['total_warnings']} 项警告，可进入步骤8人工审核。")
    lines.append("=" * 60)

    return "\n".join(lines)


# ============================================================
# CLI 入口（独立测试用）
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="规则冲突自动检测器")
    parser.add_argument("--file", "-f", type=str, help="分镜 JSON/JSONL 文件路径")
    parser.add_argument("--template", "-t", type=str, default="B", choices=["A", "B", "C", "D"], help="模板档位")
    parser.add_argument("--budget", "-b", type=int, default=350, help="字数预算")
    parser.add_argument("--splits", "-s", type=str, default="", help="拆分首镜索引，逗号分隔，如 '5,12'")
    parser.add_argument("--json-input", "-j", type=str, help="直接传入 JSON 字符串（用于 SKILL 内部调用）")
    args = parser.parse_args()

    # 加载数据
    shots = []
    if args.json_input:
        try:
            shots = json.loads(args.json_input)
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content.startswith("["):
                shots = json.loads(content)
            else:
                # JSONL 格式
                shots = [json.loads(line) for line in content.split("\n") if line.strip()]
    else:
        print("错误：请指定 --file 或 --json-input", file=sys.stderr)
        sys.exit(1)

    split_indices = []
    if args.splits:
        try:
            split_indices = [int(x.strip()) for x in args.splits.split(",") if x.strip()]
        except ValueError:
            print("错误：--splits 格式不正确", file=sys.stderr)
            sys.exit(1)

    # 执行校验
    report, stats = validate_shotlist(
        shots=shots,
        template=args.template,
        model_budget=args.budget,
        split_indices=split_indices,
    )

    # 输出报告
    summary = generate_summary(report, stats)
    print(summary)

    # 返回状态码
    if stats["total_errors"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
