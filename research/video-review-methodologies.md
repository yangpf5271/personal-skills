# 视频制作链路审查方法论调研（供 video-agency-roles 技能使用）

调研日期：2026-08-14。目标：为 video-agency-roles（7 角色在 spec 定稿后、渲染前做质量关卡审查）收集**可判定的检查标准/锚点**，避免审查退化为 LLM 泛泛点评。

---

## 1. 专业制作流程中的审查环节

### 1.1 Pixar 的 Dailies / Notes Session / Braintrust

**Dailies（每日审查会）怎么运作：**
- 每天早上召开，逐条放映每个团队的进行中镜头（work-in-progress），无论完成度如何都必须展示，目的是消灭信息孤岛、自我审查和"藏私货"。
- 关键规则（常被引用为 **25%–75% 法则**）：提交审查的作品应至少完成 25%、不超过 75%——太早无法有效评估，太晚改不动。来源：[Goods, Bads, and Dailies (Medium)](https://medium.com/creating-a-ux-strategy-playbook/goods-bads-and-dailies-lessons-for-conducting-great-critiques-f2089046b274)、[Pixar Dailies (Shortform)](https://www.shortform.com/blog/pixar-dailies/)
- 审查关注点：动作是否达到"blocking 可评估"状态、表演意图是否清晰、镜头是否服务于Sequence目标（[Animation Mentor: Inside Dailies at Pixar](https://www.animationmentor.com/blog/inside-dailies-at-pixar-expressing-your-opinion-about-changes-in-animation/)）

**Notes（意见）的给法：**
- 制作链上任何人（含 Ed Catmull、John Lasseter 等最高层）都可以给 notes，但**没有任何人有权限否决导演**——notes 是诊断性建议，不是命令；导演必须被说服而不是被命令。来源：[Now Go Create: The brains trust, dailies & giving notes](https://nowgocreate.co.uk/blog/creative-lessons-pixar/)、[HBR: How Pixar Fosters Collective Creativity (Catmull)](https://hbr.org/2008/09/how-pixar-fosters-collective-creativity)

**Braintrust（深度审查会）：**
- 只在制作遇到困难、制片人主动求助时召集；成员是少数"最受信任、资深、受尊敬"的人；固定**两小时**辩论式讨论；产出是问题诊断清单而非解决方案命令。来源：[Now Go Create](https://nowgocreate.co.uk/blog/creative-lessons-pixar/)、[HBR](https://hbr.org/2008/09/how-pixar-fosters-collective-creativity)

**对审查环节的可移植机制**（比内容更有价值）：
- 时机锚点：25%–75% 完成度之间审查（对应本项目："spec 定稿后、渲染前"正是这个窗口）
- 反馈格式约束：notes 必须指向具体镜头/时间段 + 描述问题而非直接命令改法
- 问题清单 vs 解决方案分离；最终决定权归单一 owner

### 1.2 广告/创意行业的 Creative Review / Pre-flight Check

- **Pre-flight testing**（Creativex 等工具）：素材发布前对照"平台最佳实践 + 品牌规则 + 合规标准"三类硬性规则打分。来源：[Creativex: What is Pre-Flight Testing](https://support.creativex.com/hc/en-us/articles/6135744080411-What-is-Pre-Flight-Testing-and-how-do-I-use-it)
- 广告平台侧的 creative review（如 [Google DV360](https://support.google.com/displayvideo/answer/6063030?hl=en)）：技术规格合规 + 政策合规 + 落地页一致性三类检查。
- Meta 广告 pre-flight 检查（[Sellixo 示例](https://www.sellixo.org/services/creative-review)）：创意、主文案、目标页三件套逐一对照平台政策，输出"带政策条款引用的具体反馈"——**每条反馈必须能指向一条明文规则**是行业惯例。
- 典型制作公司流程为 Concept → Script → Filming → Editing → Delivery 的门禁式推进（[Flight Creative Media](https://www.flightcreativemedia.com/capabilities)），每个门禁有明确的交付物验收。

---

## 2. 视频叙事/节奏的可判定指标

### 2.1 留存与钩子的量化锚点

- **vidIQ 基准**：平均观看百分比 ~30% 为良好；**前 30 秒后仍留存 60% 视众**为及格线。来源：[vidIQ: YouTube Audience Retention](https://vidiq.com/blog/post/increase-audience-retention-youtube/)
- 数据型参考（Prepublish.ai）：多数视频在前 30 秒流失 20–35% 观众；头部视频前 30 秒留存 ≥70%（RSinc）。
- **TubeBuddy 三层钩子结构**（脚本阶段可判定）：
  1. 前 7 秒：确认观众"点对了视频"（呼应标题/封面承诺）；
  2. 8–30 秒：说明视频讲什么 + 为什么由你来讲（资历/独特性）；
  3. 开一个"环"（loop）：抛出稍后才揭晓的问题/悬念。
  另要求全片用 Problem→Solution 节奏分节，并预先写下观众的情绪回报（emotional payoff）。来源：[TubeBuddy: The YouTube Video Checklist](https://www.tubebuddy.com/blog/youtube-video-checklist/)
- **MrBeast 泄露内部手册**（[Simon Willison 分析](https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/)）：
  - 每支视频的创意流程**从标题+封面开始**，而非从内容开始；标题封面设定的预期若与正片不符，观众即流失；
  - **第一分钟是全片最重要的分钟**，职责是"兑现封面承诺 + 给出 wow factor"（例如第 30 秒就用吊车送来承诺的房子）；
  - 1–3 分钟、3–6 分钟、6 分钟后各有明确定义的职责；
  - 核心指标只有两个：CTR（点击率）与 AVD（平均观看时长）；"还有谁能在 YouTube 做到"（who else can do that）是 wow factor 的检验问句。

### 2.2 剪辑节奏的可判定参考

- **平均镜头长度（ASL）参考区间**：ASL = 总时长(秒) ÷ 总镜头数（[Filmmakers Academy](https://www.filmmakersacademy.com/glossary/average-shot-length-of-films/)）。现代电影约 2.5–4 秒（从 1930 年 ~12 秒压缩而来，[Film Editing Pro](https://www.filmeditingpro.com/fast-vs-slow-video-editing-pacing-tips/)；动作片 ~2 秒，[No Film School](https://nofilmschool.com/2016/01/furious-film-editing-watch-five-films-average-2-seconds-shot)）；YouTube 口播类建议 15–25 秒一切换、每 2–3 分钟插入 5–10 秒快切 burst 重新抓注意力（Air.io，经搜索摘要）。结论：**ASL 应匹配内容类型，可判定的规则是"是否存在远超该类型基准的静态长镜头且无新信息"**。
- **"每个镜头必须带来新信息"**（film editing 根本规则之一）：只在必要时切；切点必须带来节奏、喜剧时机、冲击或新信息之一，否则不切。来源：[Filmic Grammar: The Rules of Filmmaking](https://2822digitalcinematography.wordpress.com/filmic-grammar-the-rules-of-filmmaking/)、[InVideo: Long Take vs Cutting](https://invideo.io/faq/how-do-you-decide-between-a-long-take-and-cutting-in/)。推论：**b-roll 若只是重复旁白已说的内容而无新信息/情绪增量，即为冗余镜头**。
- **Walter Murch 剪辑六法则**（判断"这个切点对不对"的优先级权重）：Emotion 51% > Story 23% > Rhythm 10% > Eye-trace 7% > 2D 屏面方向 5% > 3D 空间连续 4%。来源：[Go Into The Story](https://gointothestory.blcklst.com/walter-murch-and-the-rule-of-six-47de34be834a)、[StudioBinder](https://www.studiobinder.com/blog/walter-murch-rule-of-six/)、非叙事内容应用版：[No Film School](https://nofilmschool.com/editing-emotion-using-walter-murchs-rule-six-non-narrative-content)
- 镜头时长应**有变化**：连续等长镜头会催眠，全短镜头会疲劳（[LWKS 剪辑指南](https://lwks.com/blog/a-precise-cut-a-beginners-guide-to-video-editing-cuts-and-techniques)）。

---

## 3. 平台发布前 Checklist

### 3.1 YouTube 官方（youtube.com/creators，原 Creator Academy）

来源：[Optimize & evolve your content](https://www.youtube.com/creators/grow/optimize-your-content/)、[YouTube for Creators 资源页](https://www.youtube.com/creators/resources/)

官方明确建议项：
- 标题准确反映视频内容；重要关键词放在标题前部；**避免滥用大写和 emoji**；
- 缩略图与标题组合设定正确预期（预期错配 = 点击即走）；
- 描述前两句承载关键信息；
- 用数据驱动迭代：对比 CTR、平均观看时长、流量来源做实验。

### 3.2 TubeBuddy 七阶段出片清单（[来源](https://www.tubebuddy.com/blog/youtube-video-checklist/)）

出片前最终检查（Phase 6）逐条：
- 标题朗读测试：能引发好奇但不误导；
- 缩略图在 YouTube Studio 里切换到**手机尺寸预览**，手机上看不清就简化；
- 描述 + 时间戳（章节）完整，结尾软性订阅引导；
- 后台设置核对：分类、语言、字幕准确性、Made for Kids 标记；
- 有意识地选择"首播(Premiere)造势"还是"直接发布抢观看速度"。

缩略图判定规则（Phase 4）：
- 核心元素 ≤3 个（表情/焦点物/可读文字）；
- 手臂距离手机尺寸可读性测试；
- "留悬念不给答案"（tease, don't tell）；
- 准备一个 A/B 备选封面。

发布后 48 小时复查（Phase 7，可作为 spec 里预埋的复盘钩子）：
- 24h CTR 低于频道均值 → 包装问题；48h 留存曲线前 30 秒陡降 → 钩子失败；
- 记录 CTR/AVD/流量来源三个数字。

### 3.3 B站（官方创作手册 + 社区总结）

来源：B站官方《Up主创作手册》PDF（[activity.hdslb.com/blackboard/static/pdf/20200331.pdf](https://activity.hdslb.com/blackboard/static/pdf/20200331.pdf)）、[B站封面规范说明](https://m.gaoding.com/article/1780154930818461696)、[B站合集功能官方指南](https://www.bilibili.com/read/cv20373513/)

- 封面内容必须与视频内容相关，不得含违法/低俗/限制级元素；
- 视频头尾加入"求三连"（点赞/投币/收藏）引导片段；
- 封面+标题按热门规律自查（大字标题、高对比、关键信息前置——社区对 4952 个热门视频的分析总结）；
- 系列内容归入合集（创作中心→内容管理→合集管理，填合集标题/简介）；
- 分P标题清晰、顺序正确；创作中心核对水印、智能字幕、分区、标签、定时发布；
- 发布后流量自查锚点（社区经验）：发布后 3/7/13 小时流量增幅 <10% 需警惕；首日观众粉丝占比 >50%（新号 >30%）为预警。

---

## 4. 事实核查（for video script）行业标准轻量版

### 4.1 新闻事实核查工作流（可裁剪为脚本版）

来源：[jamditi/claude-skills journalism fact-check-workflow（LobeHub 收录）](https://lobehub.com/skills/jamditis-claude-skills-journalism-fact-check-workflow)（六步管线：claim 提取 → 逐条研究 → 证据收集 → 联系信源 → 定级 → 输出）

可借用的轻量组件：
- **Claim 清单化（claim log）**：从文本中提取可核查断言，登记字段：来源/原句/说话人/语境/类型/**优先级**/状态；
- **优先级矩阵**：先核查"重要性高 × 可证伪 × 有争议"的断言，而不是全部平铺；
- **证据优先一手来源**：研究、政府数据、原始录音录像优先于二手转述；证据也逐条登记，形成可审计链；
- **定级桶**：verified / false / unverifiable（无法核实），三桶制比五档制更适合轻量流程；
- 微软 [Claimify](https://www.microsoft.com/en-us/research/blog/claimify-extracting-high-quality-claims-from-language-model-outputs/) 的原子化断言标准：把复合句拆成**单一、自包含、可独立判定真假**的最小断言。

### 4.2 SIFT 四步法（Mike Caulfield，来源评估）

来源：[Hapgood 原文](https://hapgood.us/2019/06/19/sift-the-four-moves/)、[UChicago 图书馆指南](https://guides.lib.uchicago.edu/c.php?g=1241077&p=9082322)

- **S**top：遇到引用/数据先停，检查情绪反应（越"气人/惊人"越要先核）；
- **I**nvestigate the source：横读（lateral reading）——先查"这个来源是谁"，再读内容；
- **F**ind better coverage：找更权威的同行覆盖/共识；
- **T**race to original：把引用、数据、图片**追到原始语境**，检查是否断章取义/过期/单位错误。

---

## 5. 可移植到 video-agency-roles 的检查项（按 7 角色分组，均为可判定问句）

每条要求审查时回答 yes/no 或给出 spec 中的具体证据（时间码/字段/原文引用），禁止无锚点评。

### 选题策划（Topic/Concept）
1. 这个选题能否用**一句话**讲清（TubeBuddy Phase 1）？spec 里能否指出这句话？
2. 创意是否**从标题+封面倒推**（MrBeast 规则）：spec 是否已存在标题/封面草案，且正文承诺与之逐条对应？
3. 标题/封面设定的每一条预期，spec 中哪个段落/镜头兑现它？（逐条列出；任何一条无对应即 fail）
4. 选题有没有"wow factor"检验通过的点：能否回答"还有谁能做出这个"并举出具体桥段？
5. 视频 A→Z 路径是否明确写出（起点状态→终点状态/观众获得的转变）？
6. 目标观众的情绪回报（emotional payoff）是否被显式写下？
7. 是否规划了发布后 48h 复盘钩子（CTR/AVD 记录点）？

### 事实核查（Fact-check）
1. 是否从脚本提取了 **claim 清单**，每条含：原句、语境、类型、优先级、状态？
2. 复合句是否已拆成**原子断言**（单一、自包含、可独立判定）？
3. 每个数字/引语/对比是否**追溯到一手来源**（原始论文/官方数据/原始录音）而非转述媒体？
4. 每条关键 claim 是否完成 SIFT 四问：停一秒→来源是谁→有没有更好的覆盖→原始语境是否被断章取义？
5. 高优先级 claim 是否都有定级：verified / false / unverifiable？"unverifiable"的claim在脚本中是否改为留有余地的措辞？
6. 惊人/反直觉的表述（最容易带流量的）是否被优先核查（优先级矩阵）？
7. 脚本中"研究表明/专家表示/据统计"类无主语引用是否存在？存在即 fail，要求补来源。

### 技术实现（Technical）
1. spec 是否定义了交付规格（分辨率/帧率/时长/宽高比）且与目标平台要求一致？
2. 音频是否有检查锚点：录 10 秒回放查 hum/echo/hiss/电平不一致（TubeBuddy Phase 3）？
3. 灯光/画面是否有"测试帧"检查项（眼下/鼻下/下巴阴影）？
4. 字幕/字体/渲染参数是否逐项列出（而非"加字幕"一句带过）？
5. 每个"技术性承诺"（转场、特效、动画）在当前工具链中是否可行——能否指出等价的已验证实现？
6. 是否核对了平台硬性合规项（水印、Made for Kids 类标记、分区/分类/语言字段）？

### 视觉设计（Visual design）
1. 每个 b-roll/画面是否回答："这个镜头带来什么**新信息或新情绪**？"答不出的镜头列出并标删（"每镜头必须带来新信息"规则）。
2. 关键画面的**阅读顺序**是否被设计过（eye-trace：观众视线先看哪、后看哪）？
3. 图表/字幕是否在手机尺寸下可读（缩略图同样适用手臂距离测试）？
4. 视觉元素数量是否受控：封面 ≤3 个核心元素；画面主信息 ≤1 个焦点？
5. 切换镜头时是否遵守轴线/方向连续（或有意打破并说明理由）？
6. 视觉风格是否有可指认的参照（3 个参考片 + 指明借鉴的具体维度），而非"高级感"这类形容词？

### 审美品味（Taste / 逐镜头判断）
1. 逐个切点用 Murch 六问检验：这个切点服务情绪(51%)还是故事(23%)还是仅仅节奏(10%)？若仅为后四项技术理由而切，标记可疑。
2. spec 中是否存在"仅因好看"而存在、不推进情绪也不推进信息的段落？逐段标记。
3. 全片是否至少有一个"值得截图/值得转述给别人"的时刻？指出来。
4. 若把任一段落删掉，观众会损失什么？答不出损失的段落进入删减候选。
5. 开头承诺与结尾交付是否形成闭环（loop 是否被关上）？
6. 全片是否避免了"形容词堆砌的审美指令"（如"要有电影感"）——每个审美要求是否都翻译成了可执行的参数（焦段/速度/留白比例/色板）？

### 节奏控制（Pacing）
1. 前 7 秒是否确认了"点对了视频"（呼应标题/封面）？
2. 8–30 秒是否完成"讲什么+为什么是你"并**开出一个环**？
3. 是否为 1–3 分钟、3–6 分钟、6 分钟后分别定义了节奏职责（MrBeast 结构）？
4. 计算或估算 spec 的**镜头时长分布**：口播类是否存在 >25 秒无切换且无新信息的段（对照 ASL 基准）？
5. 镜头时长是否有变化（非均质）？是否存在连续 N 个等长镜头？
6. 每 2–3 分钟是否有一个节奏重置点（快切 burst / 场景切换 / 图形插入）？
7. 全片是否按 Problem→Solution 波浪分节，节与节之间有无明确张力-释放点？
8. 删除测试：任一 30 秒段落能否被压缩 1/3 而不损失信息？对拖沓嫌疑段逐段执行。

### 平台包装（Packaging）
1. 标题：重要关键词是否前置？是否避免大写/emoji 滥用（YouTube 官方）？朗读测试是否"好奇但不误导"？
2. 封面：≤3 核心元素？手机尺寸可读？"留悬念不给答案"？是否准备了 A/B 备选？
3. 描述前两句是否承载关键词与内容概述？
4. 章节时间戳是否规划好（每章有独立可点击的价值点）？
5. 结尾卡/end screen 是否指定了引导去的具体视频/播放列表？
6. B站专项：封面与内容相关性合规、片头/片尾三连引导、合集归属、分P标题与顺序、分区/标签/定时发布设置是否逐项核对？
7. 发布后检查锚点是否预埋：24h CTR vs 频道均值、48h 前 30 秒留存陡降检测、（B站）3/7/13 小时流量增幅与首日粉丝占比预警？

### 审查流程本身（来自 Pixar 机制，建议作为 skill 的元规则）
1. 审查时机符合 25%–75% 法则（spec 定稿后、渲染前 = 可改且可评）。
2. 每条审查意见格式：指向具体时间码/spec 字段 + 描述问题（诊断），**不直接下命令改法**；是否处方交给创作者。
3. 每条意见必须能指向本清单中某一条规则或 spec 中某处证据，否则不输出（抑制泛泛点评）。
4. 七角色平等给 notes，但最终裁决权归单一 owner（对应"导演权威"机制）。

---

## 主要来源汇总

- Pixar/审查机制：[HBR Catmull](https://hbr.org/2008/09/how-pixar-fosters-collective-creativity) · [Now Go Create](https://nowgocreate.co.uk/blog/creative-lessons-pixar/) · [Medium: Goods, Bads, and Dailies](https://medium.com/creating-a-ux-strategy-playbook/goods-bads-and-dailies-lessons-for-conducting-great-critiques-f2089046b274) · [Shortform](https://www.shortform.com/blog/pixar-dailies/) · [Animation Mentor](https://www.animationmentor.com/blog/inside-dailies-at-pixar-expressing-your-opinion-about-changes-in-animation/)
- Pre-flight/创意审查：[Creativex](https://support.creativex.com/hc/en-us/articles/6135744080411-What-is-Pre-Flight-Testing-and-how-do-I-use-it) · [Google DV360](https://support.google.com/displayvideo/answer/6063030?hl=en)
- 留存/节奏：[vidIQ](https://vidiq.com/blog/post/increase-audience-retention-youtube/) · [TubeBuddy](https://www.tubebuddy.com/blog/youtube-video-checklist/) · [MrBeast 手册分析 (Simon Willison)](https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/) · [Film Editing Pro](https://www.filmeditingpro.com/fast-vs-slow-video-editing-pacing-tips/) · [Filmic Grammar](https://2822digitalcinematography.wordpress.com/filmic-grammar-the-rules-of-filmmaking/) · [Murch Rule of Six (Go Into The Story)](https://gointothestory.blcklst.com/walter-murch-and-the-rule-of-six-47de34be834a) · [StudioBinder](https://www.studiobinder.com/blog/walter-murch-rule-of-six/) · [No Film School](https://nofilmschool.com/editing-emotion-using-walter-murchs-rule-six-non-narrative-content) · [LWKS](https://lwks.com/blog/a-precise-cut-a-beginners-guide-to-video-editing-cuts-and-techniques) · [Filmmakers Academy ASL](https://www.filmmakersacademy.com/glossary/average-shot-length-of-films/)
- 平台 checklist：[YouTube 官方 Optimize & evolve](https://www.youtube.com/creators/grow/optimize-your-content/) · [YouTube Creators 资源](https://www.youtube.com/creators/resources/) · [B站创作手册 PDF](https://activity.hdslb.com/blackboard/static/pdf/20200331.pdf) · [B站封面规范](https://m.gaoding.com/article/1780154930818461696) · [B站合集指南](https://www.bilibili.com/read/cv20373513/)
- 事实核查：[fact-check-workflow skill](https://lobehub.com/skills/jamditis-claude-skills-journalism-fact-check-workflow) · [Claimify (Microsoft Research)](https://www.microsoft.com/en-us/research/blog/claimify-extracting-high-quality-claims-from-language-model-outputs/) · [SIFT 原文](https://hapgood.us/2019/06/19/sift-the-four-moves/) · [UChicago SIFT 指南](https://guides.lib.uchicago.edu/c.php?g=1241077&p=9082322)
