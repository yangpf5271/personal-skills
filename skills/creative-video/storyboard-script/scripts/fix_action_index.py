# -*- coding: utf-8 -*-
"""只修复动作特效库的节标记（全角括号版本）"""
import re

base = "C:/Users/Administrator/Desktop/AI/分镜脚本skills/storyboard-script/references"
fpath = f"{base}/知识库-动作特效.txt"

with open(fpath, "r", encoding="utf-8") as f:
    original = f.read()

indices = [
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

idx_header = """# 关键词索引（按需检索，不全量加载）
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

modified = original
for pattern, marker in indices:
    modified = modified.replace(pattern, f"══════════ {marker} ══════════\n{pattern}")

modified = idx_header + modified

with open(fpath, "w", encoding="utf-8") as f:
    f.write(modified)

lines = modified.count("\n")
size_kb = len(modified.encode("utf-8")) / 1024
print(f"[OK] {fpath}")
print(f"     12 sections marked, {lines} lines, {size_kb:.1f} KB")
for pat, marker in indices:
    count = modified.count(marker)
    status = "OK" if count == 1 else f"WARN({count})"
    print(f"     {marker}: {status}")
