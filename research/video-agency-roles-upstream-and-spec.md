# video-agency-roles 补强调研：本地事实 + 上游仓库（heygen-com/hyperframes）

调研日期：2026-08-14。目的：为 video-agency-roles（7 角色审查技能）提供可判定的审查标准，并与被审查对象（video-spec.md / hyperframes composition）咬合。

---

## Part 1 本地事实

### 1.1 video-spec.md 的结构（来自 video-spec-builder/SKILL.md）

**重要事实**：`video-spec-builder` 的 SKILL.md 引用了 `templates/video-spec-template.md`、`examples/video-spec-spacex.md` 和 8 个 `references/*.md`，但**这些文件在本地仓库中全部不存在**（该技能目录下只有一个 SKILL.md，git 历史也只有两次提交，从未提交过模板）。因此 video-spec.md 的实际结构只能从 SKILL.md 正文的描述反推：

可确认的结构线索：
- **§ 4 视觉规范**：SKILL.md 明确提到"选定主题后写进 `video-spec.md` 的 § 4 视觉规范"——说明 spec 有编号章节，§ 4 是视觉规范
- **theme 字段**：`用户选定主题后写到 video-spec.md 的 theme 字段`；值为预设名（如 `Swiss Pulse`）或 `design.md（项目根目录）`
- **分镜表**：spec 的核心是包含"分镜表"的表格，产出定义 = "确定每页讲什么、怎么动、何时切换"
- 分镜粒度要求：每个镜头锚定到 `references/components-catalog.md` 的具体组件 ID（目录号称 69 个组件，但该文件不存在）；每镜头决定转场（crossfade / wipe / shader / hard cut）
- 迭代模式要求"检测与现有 spec 的冲突"，字段约束与一致性校验放在（不存在的）`references/spec-rules.md`
- spec 生成后的交接约定："HyperFrames 会自己读 video-spec.md"——spec 是渲染端的直接输入

分镜表可推断的字段维度（从 SKILL.md 的追问维度反推）：镜头号 / 时长（镜头时长 ≥4s 须解释信息载荷，≤1s 须有强视觉刺激）/ 文案（逐字稿拆到单镜头）/ 动效语言 / 转场类型 / 组件 ID / 节奏基准 / 情绪曲线节点 / 音画关系。**这些字段名没有权威定义——这正是 video-agency-roles 审查时"无法咬合"的根源之一。**

### 1.2 [能力对照表] 完整内容（video-spec-builder SKILL.md 第 187-215 行）

| 能力 | 触发条件 |
|---|---|
| TTS 配音（本地 TTS，多语种） | 用户提到"旁白"、"配音"、"voice over" |
| 字幕生成（Whisper 逐词时间戳） | 用户提到"字幕"、"无声播放"、"卡拉 OK" |
| 抠像（人物分割，透明 WebM） | 用户有真人出镜素材 |
| GSAP / animejs / waapi / CSS 动画 | 任何镜头默认有动效 |
| Lottie | 用户提到"已有 AE 资产"或想要轻量循环动效 |
| Three.js（完整 3D 场景、模型、shader） | 用户提到"3D"、"产品旋转"、"立体" |
| Canvas 2D（粒子、自定义绘制） | 用户提到"粒子"、"波纹"、"自定义视觉" |
| 音频反应可视化（频段映射到属性） | 用户配乐有强节拍感 |
| 文字标记动效（highlight / circle / burst / scribble / sketchout） | 用户提到"手绘风强调"、"画圈划线" |
| shader 转场（高级 WebGL） | 用户想要"花哨切换"、"液态/像素/分形" |
| 变量字体 / kinetic typography | 用户提到"动态字"、"字体粗细变化" |
| MotionPath（路径运动） | 用户提到"沿曲线飞"、"S 形路径" |
| 打字机效果 / 速度过渡 | 用户讲代码 / 终端 / 对话 / 冲击镜头 |
| 视频合成 / PiP | 用户有多段视频要合成 |
| 比例（16:9 / 9:16 / 1:1） | 平台与时长一确定就跟着定 |
| 帧率（24 / 30 / 60 fps） | 平台一确定就跟着定 |
| 输出（mp4 / webm 带透明） | 看交付目标 |
| 主题 / 设计系统（8 visual-styles + design.md） | 聊视觉风格的时候定 |

这张表在 video-spec-builder 的 SKILL.md 里，**不在 video-agency-roles 自己的目录里**——video-agency-roles 第 67 行引用"（对照 [能力对照表]）"属于跨文件悬空引用。

### 1.3 design.md / DESIGN.md 格式约定

两套约定并存，有轻微冲突：

**video-spec-builder 侧（design.md，小写）**：
- 项目根目录单个 `design.md`（+ 可选 `tokens.css`），无 `styles/` 文件夹（旧三件套已废弃）
- 格式 = HyperFrames YAML 格式：YAML 头（colors / typography / rounded / spacing / motion）+ 章节（Overview / Colors / Typography / Elevation / Components / Do's and Don'ts）
- 范本在（上游的）hyperframes 的 `visual-styles.md`

**hyperframes 侧（DESIGN.md，大写，Visual Identity Gate 硬门禁）**：
- 优先级顺序：① 项目里的 `DESIGN.md` → ② `visual-style.md`（项目级）→ ③ 用户点名 8 预设之一（Swiss Pulse / Velvet Standard / Deconstructed / Maximalist Type / Data Drift / Soft Signal / Folk Frequency / Shadow Cut）→ ④ 都没有则先问 3 个问题（情绪 / 明暗 / 品牌参考）再生成最小 DESIGN.md
- 最小 DESIGN.md 结构：`## Style Prompt`（一段话）/ `## Colors`（3-5 个带角色标注的 hex）/ `## Typography`（1-2 字体族）/ `## What NOT to Do`（3-5 条反模式）
- 硬规则："Every composition must trace its palette and typography back to a DESIGN.md"——用了 `#333`、`#3b82f6`、`Roboto` 就是跳过了这个门

**审查含义**：video-agency-roles 的"视觉设计"角色可以直接判定"spec 的 theme 字段 vs 项目根实际存在 design.md/DESIGN.md 与否"是否一致。

### 1.4 lint 与 inspect 的职责（本地 hyperframes-cli / hyperframes）

**`npx hyperframes lint`**（结构检查，纯静态）：
- 检查 index.html 和 compositions/ 全部文件
- 报 errors（必须修）/ warnings（应该修）/ info（--verbose）
- 捕获：缺失 `data-composition-id`、同轨重叠（data-track-index 冲突）、未注册的时间线（window.__timelines）

**`npx hyperframes validate`**（对比度审计，浏览器）：
- WCAG 对比度：seek 到 5 个时间点截图，采样每个文字元素背后的背景像素，算对比度
- 普通文字需 4.5:1，大字（24px+ 或 19px+ 粗体）3:1
- `--no-contrast` 可跳过（快速迭代时）

**`npx hyperframes inspect`**（视觉布局检查，headless Chrome）：
- seek 扫过时间轴，报告：文字溢出容器/气泡、固定宽高盒裁剪文字、文字出画布、子元素逃逸裁剪容器
- 带 timestamp / selector / bounding box / fix hints；`--samples 15` 加密采样、`--at 1.5,4,7.25` 指定 hero frame、`--json` 给 agent 读
- 溢出若是有意的（入场/出场动画）标记 `data-layout-allow-overflow`；装饰元素标 `data-layout-ignore`

**`animation-map.mjs`**（hyperframes/scripts/，编排审计）：
- 输出 per-tween 摘要、ASCII 时间轴甘特图、stagger 检测、**Dead zones（>1s 无动画段落）**、元素生命周期、5 个关键时间点的场景快照
- Flags：`offscreen` / `collision` / `invisible` / `paced-fast`（<0.2s）/ `paced-slow`（>2s）

**composition 的硬性约定**（技术审查的"法条"）：data-start/data-duration/data-track-index/data-composition-id；timeline 必须 `{paused:true}` 并注册到 `window.__timelines`；禁 Math.random/Date.now；禁 repeat:-1；禁异步建时间线；video 必须 muted playsinline + 独立 `<audio>`；多场景必须有转场、每元素必须有 gsap.from() 入场、除末场景外禁出场动画。

**渲染/预览验证手段**：`npx hyperframes preview`（热重载 Studio，交付用 `http://localhost:<port>/#project/<name>` URL 而非 index.html 路径）；`render --quality draft` 迭代 / `standard` 审阅 / `high` 交付；`--strict` 有 lint 错误即失败；`doctor` 排障。

**分工结论**：lint/validate/inspect/animation-map 已经覆盖了"代码层"的技术审查（结构、对比度、溢出、编排）。video-agency-roles 的"技术实现"角色应审 **spec 层**（能力对照表比对、素材链路断点、性能预算）并把代码层检查**委托**给 CLI 工具，而不是重复。

### 1.5 video-agency-roles 自身的悬空引用清单

通读 207 行 SKILL.md，发现：

1. **`[能力对照表]`（第 67 行）**——该表不在本技能目录，在 video-spec-builder/SKILL.md 第 187 行。无路径指引，若两个技能没同时安装则悬空。
2. **`design.md 或预设`（第 85 行）**——依赖项目根的 design.md 或 8 预设名，但没有说明去哪读预设定义（在 hyperframes/visual-styles.md）。
3. **无任何 references/ 文件**——7 个角色只有维度形容词（"对比度够吗"、"节奏拖不拖"），没有可判定标准和检查脚本。
4. **审查对象不明确**——声称可审"spec 和实施结果"，但实施结果（compositions HTML / 渲染产物）与 CLI 工具的检查项无分工说明。
5. **需要外部输入的维度**：选题策划（需要平台/受众数据）、事实核查（需要联网搜索）、平台包装（硬编码为 B 站，但 spec 里平台字段是自由的）；弹幕预判、竞争环境等维度没有信息来源。
6. 输出的"评分 X/10"没有评分锚点（什么算 3 分什么算 8 分），容易出现 SKILL.md 自己警告的"敷衍的全 7 分"。

---

## Part 2 上游发现（heygen-com/hyperframes，分支 main）

来源：https://github.com/heygen-com/hyperframes 及其 raw 文件。

### 2.1 技能清单（skills/ 目录，共 20 个）

通过 GitHub API（https://api.github.com/repos/heygen-com/hyperframes/contents/skills ）确认目录：

- 路由入口：`hyperframes`
- 创作工作流（10）：`product-launch-video`、`faceless-explainer`、`pr-to-video`、`embedded-captions`、`talking-head-recut`、`motion-graphics`、`music-to-video`、`slideshow`、`general-video`、`remotion-to-hyperframes`
- 领域技能（9）：`hyperframes-core`、`hyperframes-animation`、`hyperframes-keyframes`、`hyperframes-creative`、`hyperframes-audio`、`media-use`、`hyperframes-cli`、`hyperframes-registry`、`figma`

README（https://github.com/heygen-com/hyperframes#readme ）确认了这套结构：路由技能 + 10 个创作工作流 + 8 个领域技能（README 未列 hyperframes-audio，但目录存在）。README 强调："a router skill that reads intent and routes to the right workflow — plus 10 end-to-end creation workflows, plus 8 domain skills that load on demand"。

### 2.2 有没有审查类技能？

**没有独立的 review/audit/QA/critique 技能。** 但审查能力以三种形式内嵌在体系里：

**(a) Review Loop**（`skills/hyperframes-core/references/review-loop.md`，raw: https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/hyperframes-core/references/review-loop.md ）——storyboard 驱动工作流的共享检查点流程，四道关卡：
1. **§ 1 Plan（文字计划）**：必须复述核心命题"This video tells [audience] that [message]"，呈现 frame 表（beats / 画面元素 / 叙事角色）；用户批准或点名修改
2. **§ 2 Sketch Pass（线稿）**：用真实文字但无样式无动效的 wireframe（"a wireframe with the real words, not a styled frame"）；每帧完成标 `built`；只改被点名的帧，"until the layout is confirmed"
3. **§ 3 Building**：布局/层级/文案在 sketch 阶段锁定；built frame "must still visually read as the approved wireframe, just fully dressed"
4. **§ 4 Final Look**：所有工作流检查通过后开 timeline preview，"renders only upon explicit approval"；自主模式保留唯一一个问题："preview first, or render?"

**(b) Storyboard 结构化反馈通道**（`storyboard-format.md`，raw: https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/hyperframes-core/references/storyboard-format.md ）：
- `.hyperframes/frame-comments.json` 是结构化反馈 sidecar：工作流发现它即视为修订指令，"revise exactly the frames named, delete the file, re-present"，且"never lingers across rounds"
- Frame 状态机：`outline`（占位）→ `built`（HTML 存在且**布局已确认**，未加动效）→ `animated`
- 这是"审查结果落回被审查对象"的机制——我们 video-agency-roles 的汇总清单目前只停在聊天里

**(c) Design Adherence 审计**（`skills/hyperframes-creative/references/design-adherence.md`，raw: https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/hyperframes-creative/references/design-adherence.md ）——建完后、preview 前跑，六类可判定检查：
1. **Colors**：composition 里每个 hex 必须出现在 spec 的 palette 区，"Flag any invented colors"
2. **Typography**：字体族和字重必须匹配 spec，"No substitutions"
3. **Corners**：border-radius 必须匹配声明的 corner style
4. **Spacing**：padding/gap 必须落在声明的密度区间
5. **Depth**：阴影用法匹配声明的深度级别（flat=none / subtle=light / layered=glows）
6. **Avoidance rules**：spec 里 "Don'ts"/"Anti-patterns" 列出的项逐一验证不存在
- 无 spec 时走 house-style-only 路径：检查跨场景 palette 一致性 + 对照 house-style.md 的 "lazy defaults" 清单
- 产出："Report violations as a checklist"，"Fix each one before serving"

### 2.3 上游的 spec / storyboard 格式

上游没有 video-spec-builder 的对应物，而是**四层 artifact 栈**（`brief-format.md`，raw: https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/hyperframes-core/references/brief-format.md ）：

**层 1 · `BRIEF.md`**（"why"，the no-repeat token，项目根，intent 阶段一次写成）：
- frontmatter 确认字段：`workflow`（如 faceless-explainer）、`flow`（automation/companion）、`storyboard`（yes/no，决定 board 是否作为 review surface）、`message`（一句话核心命题）、registry 字段（`destination` / `aspect` / `language` / `audience` / `length` / `angle`）
- body 四个可选 prose 段：`## Intent` / `## Assets` / `## Customizations` / `## Notes`
- 生命周期规则："a decision that lives only in chat is a decision resume never sees"（中途决策必须写回文件）；BRIEF 与 STORYBOARD 冲突时 "BRIEF.md holds what the user confirmed"

**层 2 · `STORYBOARD.md`**（storyboard-format.md）：
- 顶部 YAML 全局方向：`format`（画布）、`duration`（advisory）、`message`、`arc`、`audience`、`mode`；未识别 key 保留在 `globals.extra`
- 每帧一个 `## Frame N — Title`（Frame/Beat/Scene 均可），metadata 用 `- key: value` 列表：
  - `status`（outline/built/animated，默认 outline）
  - `src`（帧的 HTML 子合成物项目相对路径）
  - `duration`（如 4s）
  - `transition_in`（crossfade/cut/wipe 等别名，alias: `transition`）
  - `scene`（一句话 contact-sheet 说明；alias: description/summary/caption）——即 beat 文本
  - `voiceover`（该帧旁白 guide；alias: vo/narration）
  - `poster`（tile 封面 seek 到第几秒）
  - 自定义 key 原样保留在 `frame.extra`
- 标题以下直到下一个标题的自由叙述即 narrative

**层 3 · `frame.md`**（设计 spec，hyperframes-creative 解析，"frontmatter tokens as brand truth"——colors/fonts/spacing/tone）
**层 4 · `compositions/`**（HTML 合成物）

对比：我们的 video-spec.md ≈ 把上游 BRIEF.md + STORYBOARD.md 压成一个文件。上游把"意图"（review 时看 message/audience）与"分镜"（review 时看 duration/transition/beat）分层，每层有确定性字段——这正是 7 角色审查时可以逐字段咬合的抓手。

### 2.4 上游推荐的出片前检查流程

来自上游 `hyperframes-cli` SKILL.md（raw: https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/hyperframes-cli/SKILL.md ）与 `general-video` SKILL.md（raw: https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/general-video/SKILL.md ）：

1. **迭代用 lint**：首版 HTML 和结构性修改后跑 `npx hyperframes lint`
2. **最终门禁 `npx hyperframes check`**：一条命令 = lint + 单浏览器单 seek pass 审计 runtime 错误 / 失败请求 / 布局 / `*.motion.json` 断言 / WCAG 对比度；"Persistent findings gate the exit code; transient entrance or exit findings are informational"；`--strict` 连 warning 也 gate；`--snapshots` 出带标注的总览帧。上游已把 validate/inspect/layout 降级为兼容别名——**`check` 是上游版本的总质检门**（本地版本还没有这个命令，本地等价物 = lint + validate + inspect 三连）
3. **子合成物冒烟测试**：index.html 挂 `data-composition-src` 时快照各场景 midpoint；"multi-scene sheets use scene midpoints"；无样式内容或注册超时视为 render-blocking
4. **Design adherence + contrast 发现项全部解决**后才算 Done（general-video 的 Done 条件清单还包括：scope 精确实现、animation map 已审、**"the user approves the final Studio preview before render"**）
5. **渲染后验证产物**："confirm the file exists, is non-empty, and has a plausible duration"——`test -s out.mp4` + `ffprobe -v error -show_format out.mp4`
6. **批准后可冻结为 recipe**（`scripts/recipe.mjs freeze`）复用设计 spec + 骨架

---

## Part 3 对 video-agency-roles 的补强素材（可判定标准建议）

基于以上事实，逐角色落地：

### 通用：先解决咬合问题
- **A1（最高优先）**：video-spec-builder 的模板/引用文件全部不存在，video-spec.md 字段无权威定义。审查前应先定义"最小可审字段集"（可借上游 STORYBOARD.md 字段：镜头号/scene/duration/transition_in/voiceover/status/theme/message/audience/platform），spec 缺字段本身就是可判定的 ❌（"第 N 镜缺 duration，无法审节奏"）。
- **A2**：悬空引用修复：把 [能力对照表] 内联或给出跨技能路径（video-spec-builder/SKILL.md）；列出 8 预设定义位置（hyperframes/visual-styles.md）。
- **A3**：引入上游的**结构化反馈回写**机制（frame-comments.json 思路）：审查汇总清单应能映射回 video-spec.md 的具体镜头号/字段，改完可复审，而不是一次性聊天输出。

### 角色级可判定标准

| 角色 | 可判定标准来源 |
|---|---|
| **1 选题策划** | 借 BRIEF.md 字段做锚：`message` 是否一句话能复述（上游格式："This video tells [audience] that [message]" 测试）；`audience`/`length`/`destination` 是否齐；缺任一字段 = 直接扣分项而不是凭感觉打分 |
| **2 事实核查** | spec 内每个数字/版本号/产品说法标注来源；未标注的列出清单逐条联网核实（video-spec-builder 已有"联网优先"原则可引用）；`[待用户确认]` 标记（video-spec-builder 追问纪律失效 4 的机制）可直接复用为"核查状态"标签 |
| **3 技术实现** | 明确与 CLI 分工：结构/对比度/溢出/编排 → 委托 `lint + validate + inspect + animation-map`（引用命令而非重做）；本角色只审 spec 层：① spec 里的每个效果能在 [能力对照表] 找到对应行（找不到 = ❌ 当前方案做不了）② 素材链路完整性（TTS 音频/抠像/3D 模型文件是否已存在或可生成）③ 硬性约定前置检查（禁 repeat:-1、禁随机数、多场景必须有转场——这些在 spec 阶段就能预判违例）④ 性能预算（60fps 翻倍渲染时长、Three.js 镜头数量） |
| **4 视觉设计** | 直接移植上游 design-adherence.md 六类检查：colors（每个 hex ∈ design.md palette）/ typography（无替换字体）/ corners / spacing（落在声明密度区间）/ depth（flat=none 等）/ avoidance（Do's and Don'ts 逐条验证）。加上对比度判定标准已有现成数值：普通字 4.5:1、大字 3:1（validate 的 WCAG 阈值） |
| **5 审美品味** | "廉价感"检测落地为清单：hyperframes Visual Identity Gate 点名的 lazy defaults（`#333`/`#3b82f6`/`Roboto`）+ 8 预设之外的拼凑配色；风格统一 = 全片 hex/字体族可追溯到同一 theme 字段 |
| **6 节奏控制** | 数值化：镜头时长规则已有明文（≥4s 必须有信息载荷解释、≤1s 必须有强视觉刺激、"空帧"禁止——video-spec-builder [信息密度]）；成品阶段接 animation-map 的 Dead zones（>1s 无动画）、paced-fast（<0.2s）/ paced-slow（>2s）flags；转场密度可从 spec 的 transition_in 列直接统计 |
| **7 平台包装** | 目前硬编码 B 站但 spec 的平台字段是自由的——应改为读取 spec 的 platform/aspect/fps 字段分支判定（B 站 16:9 / 抖音 9:16 各有不同前 3 秒/完播标准）；标题/封面三要素可做成 spec 的可选章节（上游 BRIEF.md 的 `## Customizations` + STORYBOARD 的 `poster` 字段是现成挂载点） |

### 审查流程本身可借鉴上游 Review Loop
- 三段式关卡替代"一次审完"：Plan 审（对 spec 文字）→ Sketch/Build 审（对 composition）→ Final Look 审（对 preview）；每关"只改被点名的帧，改完删除反馈文件，重新呈现"
- Frame 状态机（outline/built/animated）可作为 video-agency-roles 判断"现在审什么"的依据：outline 状态审 1/2/6/7 角色（纸面维度），built/animated 才审 3/4/5（实现维度）——解决目前"不管做到什么阶段都全审"的模糊性
- 评分锚点可借 Done 清单思路：每个角色定义"必过项"（gate）与"加分项"，gate 未过直接进 🔴 清单

### 最有价值的 3 条（浓缩）
1. **上游 review-loop.md + frame-comments.json**：四道关卡 + 结构化反馈回写 + 只改点名帧——审查技能的"结果如何落回被审对象"的完整范式
2. **上游 design-adherence.md 六类检查**：colors/typography/corners/spacing/depth/avoidance，每条都是"读 HTML 对照 spec"的可判定动作，直接填充"视觉设计"角色
3. **上游 STORYBOARD.md 帧字段 schema**（status/src/duration/transition_in/scene/voiceover/poster）：给 video-spec.md 分镜表一个可逐字段审查的权威结构，配合 animation-map 的 dead-zone/paced flags 让"节奏控制"从形容词变成数字
