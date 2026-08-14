# spec-rules：字段约束 + 一致性校验 + 自检清单

起草 / 迭代 `video-spec.md` 前必读。模板见 `../templates/video-spec-template.md`。

## 1. 字段约束（逐字段）

### § 0 元信息
| 字段 | 约束 |
|---|---|
| `message` | 一句话，主语是受众。检验：能否填进 "This video tells [audience] that [___]" 且不换行 |
| `audience` | 不接受"所有人/大众"。必须有具体人群 + 场景 |
| `platform` | 枚举值之一。决定 § 8 全部内容和 aspect 默认值 |
| `aspect` | 16:9 / 9:16 / 1:1，受 P-1 约束 |
| `fps` | bilibili/youtube：30 或 60；douyin/xiaohongshu：30；默认 30 |
| `duration_total` | 带 `s` 后缀。受 P-3 约束 |
| `theme` | 8 预设名之一（Swiss Pulse / Velvet Standard / Deconstructed / Maximalist Type / Data Drift / Soft Signal / Folk Frequency / Shadow Cut）或字面量 `design.md / DESIGN.md（项目根目录）` |
| `status` | `locked` 前必须过一遍 § 3 自检清单 |

### § 3 分镜表
| 字段 | 约束 |
|---|---|
| `#` | 从 1 递增，不跳号；插镜头用 `3a`/`3b`，重排前先问用户 |
| `status` | outline → built → animated，只进不退；退回必须写原因到 § 9 |
| `duration` | `≥4s` 的镜头 info_payload 必须说清这 4 秒表达什么，否则砍；`≤1s` 必须强视觉刺激；禁止空帧（无文案/数据/冲击/节奏点的镜头） |
| `scene` | 一句话，写"观众看到什么"，不写"制作什么"。禁形容词（"高级感的画面"❌） |
| `voiceover` | 旁白原文逐字（TTS/字幕的来源），无旁白写"无" |
| `component` | 必须是 `components-catalog.md` 里存在的 `C<nn>` ID。写不出组件的镜头标 `[待确认]` 进 § 9 |
| `motion` | 说画面语言不说术语（"水墨化开"✓ "shader 转场"❌） |
| `transition_in` | hard cut / crossfade / wipe / shader / 其他 catalog 内转场名；首镜固定 hard cut |
| `info_payload` | 文案 / 数据 / 视觉冲击 / 节奏点，至少一项；`≥4s` 镜头此项为审查必查 |

### § 7 claim log
- 只登记**原子断言**（单一、自包含、可独立判定真假）；复合句拆开。
- 优先级：重要性高 × 可证伪 × 有争议 → 高。
- 状态只有四值：`verified`（须附来源，见下来源合法值）/ `false` / `unverifiable` / `待核`。
- 来源合法值：一手来源 URL / `作者口述（用户=权利人，适用于产品/技术类自述事实）` / 待补。作者口述来源的 claim 允许标 `verified`，但须在来源列写明口述。
- `unverifiable` 的 claim 在 voiceover 里必须改为留有余地的措辞（"据 X 称" / "截至 Y 年"）。
- "研究表明 / 专家表示 / 据统计" 无主语引用 → 直接 fail，必须补来源或删除。

## 2. 一致性校验（P 系列，跨字段）

| # | 规则 | 检查方法 |
|---|---|---|
| P-1 | aspect 与 platform 匹配（bilibili/youtube 主 16:9；douyin/xiaohongshu 主 9:16） | 对照 § 0 两字段 |
| P-2 | theme = `design.md / DESIGN.md（项目根目录）` 时，design.md / DESIGN.md 任一必须实际存在 | `ls design.md DESIGN.md` 任一存在 |
| P-3 | `duration_total` ≈ Σ duration（±10%） | 分镜表求和 |
| P-4 | § 1 三个关键信息点的兑现镜头号必须在分镜表中存在 | 逐条对照 |
| P-5 | § 1 标题/封面承诺对照表每条承诺都有兑现镜头 | 逐条对照 |
| P-6 | § 6 钩子三层引用的镜头号存在，且开环有关环镜头 | 逐条对照 |
| P-7 | 语速双口径：全片 3.5-5.5 字/秒（演示/读屏类取下限），另逐镜对账：单镜字数 ÷ 镜时长 ≤6 字/秒，超出即拆镜或砍字 | 全片估算 + 逐镜对账 |
| P-8 | § 2 标"待生成"的素材，对应能力必须在能力对照表内（SKILL.md [能力对照表]） | 逐条对照 |
| P-9 | 迭代时：任何被修改的字段，检查 § 1/§ 6/§ 7/§ 8 + 一切含镜头号引用的章节（§ 5/§ 9）+ § 2 字数是否被波及（改时长→总时长/节奏基准/章节时间戳） | 改动溯源 |

## 3. 自检清单（status: locked 前过一遍）

- [ ] Phase 1 七维度（目的/受众/平台时长/核心信息/信息密度/品牌 tone/观众熟悉度）全部有答案
- [ ] P-1 ~ P-8 全过（P-9 仅迭代模式）
- [ ] 分镜表无空帧、无形容词 scene、无悬空 component
- [ ] 每个 `≥4s` 镜头的 info_payload 经得起"这 4 秒在表达什么"的追问
- [ ] § 7 无 `待核` 且无高优先级 `unverifiable`（中低优先级 unverifiable 已改措辞）
- [ ] § 9 的 `[待用户确认]` 全部清零，或用户明确说"留着"
- [ ] 全文无用户没说过、又没标 `[待用户确认]` 的内容（失效 4 防御）

## 4. 迭代模式的冲突检测

修改请求进来，先跑这张表再动手：

| 改动类型 | 必查 |
|---|---|
| 换镜头/删镜头 | P-4、P-5、P-6 的镜头号引用；Σ duration（P-3）；前后镜 transition 兼容 |
| 改时长 | P-3、P-7、§ 6 节奏基准、§ 8 章节时间戳、§ 6 钩子三层时间窗边界重算 |
| 换平台/换比例 | P-1；§8 全章重写；§0 message/audience 措辞复审；§3 scene 横竖构图适配；§6 钩子时间标准（如 B站 0-7s→抖音 0-3s）；voiceover 全扫平台黑话（三连/老铁等）；§2 素材比例规格 |
| 删/合并镜头 | 默认先问用户；§1/§6/§7/§9 中区间与镜头号引用逐条收缩；变更记录留痕 |
| 换音乐 | § 5 音画关系；若改配乐驱动，§ 3 motion 列的节奏点镜头要重审 |
| 改字幕样式 | § 4 视觉规范是否被波及 |
| 换配色 | theme 是否变；P-2；§ 4 accent 覆盖 |

冲突处理：发现矛盾 → 停下来向用户复述矛盾（"你要求 X，但现有 spec 第 3 镜是 Y，二者冲突"）→ 用户裁决 → 一次改齐所有波及字段。
