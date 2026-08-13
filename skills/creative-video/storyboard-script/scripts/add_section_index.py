# -*- coding: utf-8 -*-
"""给大文件加前置索引和节标记，支持按需段落检索而非全文加载。"""

import re

# ── 知识库-动作特效.txt ──
ACTION_INDICES = [
    ("（1）常用动作类型", "SECTION:01-常用动作"),
    ("（2）中国武术派系", "SECTION:02-中国武术派系"),
    ("（3）中国武术招式", "SECTION:03-中国武术招式"),
    ("（4）国际武术", "SECTION:04-国际武术"),
    ("（5）多人混战", "SECTION:05-多人混战"),
    ("（6）技能动作", "SECTION:06-技能动作"),
    ("（7）技能特效", "SECTION:07-技能特效"),
    ("（8）身躯轮廓特效", "SECTION:08-身躯轮廓特效"),
    ("（9）巨物打斗", "SECTION:09-巨物打斗"),
    ("（10）手势动作", "SECTION:10-手势动作"),
    ("（11）力量感搭配", "SECTION:11-力量感搭配"),
    ("（12）变身特效", "SECTION:12-变身特效"),
]

ACTION_INDEX_HEADER = """# 关键词索引（按需检索，不全量加载）
# 用法：先匹配镜头需求中的关键词，Grep定位对应SECTION，Read仅加载目标段落。
# 单次加载建议: <=2个段落（约5-15KB），避免全文83KB全量加载。
# 注意：通用基础动作（站立/行走/奔跑/跳跃等）在 SECTION:01；
#       具体武术派系在 SECTION:02-03；
#       特效/法术在 SECTION:07-08；
#       变身/形态变化在 SECTION:12。

## 快速索引表
| 镜头需求 | 关键词 | 目标段落 |
|----------|--------|----------|
| 基础肢体动作 | 站立/行走/奔跑/跳跃/躺下/坐下/蹲下/趴下/游泳/骑行/飞行/瞬移/躲避 | SECTION:01-常用动作 |
| 中国传统武术 | 太极拳/咏春/少林/武当/峨眉/八卦掌/形意拳/南拳/轻功/剑法/刀法/棍法 | SECTION:02-中国武术派系 |
| 武术招式详解 | 拳招/腿招/掌招/剑招/刀招/枪招/棍招/锤招/斧招/扇招/弓箭/三路攻防/组合招式 | SECTION:03-中国武术招式 |
| 国际格斗术 | 拳击/泰拳/自由搏击/MMA/摔跤/柔术/跆拳道/空手道/柔道/合气道/截拳道/剑道/桑搏/卡波耶拉 | SECTION:04-国际武术 |
| 多人混战场面 | 群战/近身互搏/兵器混战/多人乱战/缠斗/围殴/贴身搏杀/混战 | SECTION:05-多人混战 |
| 技能/必杀动作 | 重拳/劈砍/突刺/飞踢/格挡/蓄力/施法/结印/位移/闪身/领域/光阵/踏空 | SECTION:06-技能动作 |
| 法术/能量特效 | 法相/火焰/寒冰/雷电/风元素/剑气/刀气/枪芒/符文/圣光/黑雾/岩土/防御罩/光束/漩涡/灵力/毒瘴 | SECTION:07-技能特效 |
| 角色周身特效 | 烈焰体/寒冰气/雷电/圣光粒子/黑雾/风元素/熔岩/星尘/幻彩/妖气/魔气/圣光柱/岩屑/水纹/凤凰焰/符文覆体/龙鳞/佛纹 | SECTION:08-身躯轮廓特效 |
| 巨物/怪兽打斗 | 巨掌/巨拳/巨臂/巨兽/庞躯/巨尾/巨翼/巨型机甲/巨人/践踏/碾压 | SECTION:09-巨物打斗 |
| 手势/手印/法诀 | 剑指/弹指/拂袖/虚掌/单指/扬手/沉掌/翻掌/双掌推送/勾指/掌刃/合掌/捻指/结印 | SECTION:10-手势动作 |
| 力量风格参考 | 近战搏击/东方武侠/硬汉/机甲/怪兽/元素力量/玄幻/静态力量/高速力量/群像/凌空跃击/持械/蓄力/重甲/空战 | SECTION:11-力量感搭配 |
| 变身/形态变化 | 巨型生物变身/战甲合体/巨型机甲降临/玄幻神体/变形金刚/快速变身/狐仙/铠甲变身 | SECTION:12-变身特效 |

═══════════════════════════════════════════════════

"""

# ── 知识库-运镜整合.txt ──
CAMERA_INDICES = [
    ("# 一、基础单一运镜", "SECTION:A-基础单一运镜"),
    ("# 二、复合联动运镜", "SECTION:B-复合联动运镜"),
    ("# 三、动态特效创意运镜", "SECTION:C-动态特效创意运镜"),
    ("# 四、高燃打斗专项运镜", "SECTION:D-高燃打斗专项运镜"),
    ("# 五、特殊镜头视角", "SECTION:E-特殊镜头视角"),
]

CAMERA_INDEX_HEADER = """# 关键词索引（按需检索，不全量加载）
# 用法：先匹配运镜类型，Grep定位对应SECTION，Read仅加载目标段落。
# 单次加载建议: <=2个大段落（约3-8KB），避免全文35KB全量加载。
# 注意：基础推拉摇移在 SECTION:A；复合运镜组合在 SECTION:B；
#       高燃打斗专项在 SECTION:D；特殊视角（FPV/虫视/主观）在 SECTION:E。

## 快速索引表
| 运镜需求 | 关键词 | 目标段落 |
|----------|--------|----------|
| 基础单一运镜 | 推镜头/拉镜头/摇镜头/移镜头/升镜头/降镜头/跟镜头/旋转/环绕/景别切换 | SECTION:A-基础单一运镜 |
| 复合联动运镜 | 环绕急推/摇镜升镜/跟转第一视角/推拉反转/希区柯克/投掷跟拍/空镜转场 | SECTION:B-复合联动运镜 |
| 动态特效运镜 | 沉浸跟拍/环绕旋转/横摇平移/升降变速/子弹时间/跳切闪回/穿模/滚筒翻转/失重漂浮/微距 | SECTION:C-动态特效创意运镜 |
| 高燃打斗运镜 | 近身搏斗/兵器缠斗/柔性武器/弓箭暗器/仙侠法术/慢动作/鞭/锁链/流星锤 | SECTION:D-高燃打斗专项运镜 |
| 特殊镜头视角 | 主观视角/第一人称/越肩/FPV穿越机/虫视/低机位/情绪镜头/焦虑/恐惧/愤怒 | SECTION:E-特殊镜头视角 |

"""


def inject_index(filepath, indices, index_header):
    """读取文件，在头部插入索引，在每节前插入SECTION标记。"""
    with open(filepath, "r", encoding="utf-8") as f:
        original = f.read()

    # 先插入SECTION标记：在每个节标题前插入标记行
    modified = original
    for pattern, marker in indices:
        # 在节标题前面插入标记，但保留原标题
        modified = modified.replace(
            pattern,
            f"══════════ {marker} ══════════\n{pattern}"
        )

    # 在文件最前面插入索引头
    modified = index_header + modified

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(modified)

    # 统计
    sections = [m for _, m in indices]
    lines = modified.count("\n")
    size_kb = len(modified.encode("utf-8")) / 1024
    print(f"[OK] {filepath}")
    print(f"     {len(sections)} sections marked, {lines} lines, {size_kb:.1f} KB")
    for pat, marker in indices:
        count = modified.count(marker)
        print(f"     {marker}: found {count} occurrence(s)")


def main():
    base = "C:/Users/Administrator/Desktop/AI/分镜脚本skills/storyboard-script/references"

    inject_index(
        f"{base}/知识库-动作特效.txt",
        ACTION_INDICES,
        ACTION_INDEX_HEADER
    )
    print()
    inject_index(
        f"{base}/知识库-运镜整合.txt",
        CAMERA_INDICES,
        CAMERA_INDEX_HEADER
    )


if __name__ == "__main__":
    main()
