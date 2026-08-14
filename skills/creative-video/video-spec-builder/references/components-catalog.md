# components-catalog：组件目录与匹配规则

> 选组件时必读。所有组件从 HyperFrames 渲染端本地文件**真实提取**（不发明渲染端做不出的东西）：
> `../../hyperframes/patterns.md`、`../../hyperframes/references/css-patterns.md`、`../../hyperframes/visual-styles.md`、`../../hyperframes/references/transitions/catalog.md`、`../../hyperframes/references/transitions.md`、`../../hyperframes/references/captions.md`、`../../hyperframes/references/dynamic-techniques.md`、`../../hyperframes/data-in-motion.md`、`../../hyperframes/house-style.md`、`../../hyperframes/references/audio-reactive.md`。
>
> 用法：`video-spec.md` § 3 分镜表的 `component` 字段填本目录的 `C<nn>` ID；`transition_in` 字段用枚举值（hard cut / crossfade / wipe / shader），可附本目录的转场 ID（见文末 [转场枚举对应]）。写不出组件的镜头按 `spec-rules.md` 标 `[待确认]` 进 § 9。

---

## 一、文字呈现（C01-C08）

来源：`../../hyperframes/patterns.md`（Title Card / Slide Show）、`../../hyperframes/references/captions.md`（Script-to-Style Mapping）、`../../hyperframes/references/dynamic-techniques.md`、`../../hyperframes/visual-styles.md`、`../../hyperframes/house-style.md`

| ID | 名称 | 画面一句话 | 适用场景 | 来源 |
|---|---|---|---|---|
| C01 | 标题卡 | 深色底上一行大标题由暗到亮浮现，停几秒后淡出 | 开场定调、章节名、结尾卡 | patterns.md "Title Card with Fade" |
| C02 | 逐词点亮字幕 | 旁白讲到哪个词，哪个词就亮起来、微微放大 | 全程跟旁白的字幕基线（各能量级别通用） | dynamic-techniques.md karaoke |
| C03 | 打字机字幕 | 文字一个一个敲出来，像在终端里输入 | 讲代码、终端、聊天记录、技术操作 | captions.md Tutorial 行 |
| C04 | 弹跳大字幕 | 短句一个词一个词蹦进画面，带过冲回弹 | 高能量营销、社交向、口号句 | captions.md Social 行（word-by-word bounce） |
| C05 | 分节幻灯页 | 整页内容随时间自动换页，每页带章节标题 | 知识点逐条讲解、清单式内容 | patterns.md "Slide Show with Section Headers" |
| C06 | 重锤砸字 | 大字猛地砸进画面并急停，甚至碎裂 | 宣布重大消息、转折点、强调句 | visual-styles.md Deconstructed "Text SLAMS and SHATTERS" |
| C07 | 乱序归位字 | 字母先乱码闪动，再咔哒对齐成最终文字 | 科技发布、安全主题、punk 感 | visual-styles.md Deconstructed "scramble then snap" |
| C08 | 幽灵大字背景 | 主题词以 3-8% 透明度铺满画面背后，缓慢漂移 | 任何镜头的背景氛围层，填住空白 | house-style.md Background Layer "Ghost text" |

## 二、强调标记（C09-C13）

来源：`../../hyperframes/references/css-patterns.md`（五种 marker 模式，全部纯 CSS+GSAP 确定性实现）

| ID | 名称 | 画面一句话 | 适用场景 | 来源 |
|---|---|---|---|---|
| C09 | 荧光笔扫过 | 像黄色荧光笔从左到右划过文字底部 | 标准强调：关键词、结论句 | css-patterns.md "Highlight Mode" |
| C10 | 手绘红圈 | 一个带手绘抖动感的不闭合圆圈把词圈住 | 圈注关键术语、数字、反差点 | css-patterns.md "Circle Mode" |
| C11 | 放射线爆开 | 文字四周向八方炸出长短不一的放射线 | hype 时刻、惊人数据、"炸出来"的强调 | css-patterns.md "Burst Mode" |
| C12 | 波浪手划线 | 一条波浪线自己画出来，划在文字下方（或中间作删除线） | 轻度强调、口语化点评、旧说法作废 | css-patterns.md "Scribble Mode"（含 Strikethrough 变体） |
| C13 | 划掉旧信息 | 两道斜线交叉划过文字，像把旧答案叉掉 | 纠正误解、推翻旧结论、旧价格 | css-patterns.md "Sketchout Mode" |

## 三、数据图表（C14-C19）

来源：`../../hyperframes/data-in-motion.md`、`../../hyperframes/visual-styles.md`（Swiss Pulse / Data Drift）、`../../hyperframes/references/typography.md`

> 反模式（data-in-motion.md 明令禁止，选组件时绕开）：饼图、多轴图、6 面板仪表盘、网格线/刻度/图例、Chart.js/D3 输出。

| ID | 名称 | 画面一句话 | 适用场景 | 来源 |
|---|---|---|---|---|
| C14 | 数字滚增 | 一个数字从 0 快速滚动到目标值后定住 | 展示规模、增长、速度、金额 | visual-styles.md Swiss Pulse "counters count up from 0" |
| C15 | 比例填充 | 进度环或填充条随数值长满，长度即数值 | 完成度、占比、目标达成 | data-in-motion.md "fill bar / progress ring" |
| C16 | 巨号数据定格 | 一个数字占满半个画面（80-120px+），旁配一行小标签 | 全片最重的那个数字、单点结论 | visual-styles.md Swiss Pulse "Numbers dominate the frame" |
| C17 | 同位换数 | 同一画框同一构图，只有数值/内容在换（Q1→Q2→Q3） | 同一概念的连续数据、时间序列 | data-in-motion.md "Visual Continuity" |
| C18 | 粒子聚成数字 | 散落的粒子汇聚成一个数字，光线勾勒数据轨迹 | AI/前沿科技主题的数据揭示 | visual-styles.md Data Drift "Particles coalesce into numbers" |
| C19 | 双指标对排 | 2-3 个相关指标并排各占一列，逐列点亮 | 对比、记分牌、AB 两方结局 | data-in-motion.md "2-3 related metrics side-by-side" |

## 四、媒体合成（C20-C23）

来源：`../../hyperframes/patterns.md`、SKILL.md [能力对照表]（抠像→透明 WebM）

| ID | 名称 | 画面一句话 | 适用场景 | 来源 |
|---|---|---|---|---|
| C20 | 画中画视频框 | 一段视频缩成圆角小窗，可在画面里移动、缩放、换位 | 真人口播+素材、多画面讲解 | patterns.md "Picture-in-Picture" |
| C21 | 全屏实拍+字幕层 | 实拍视频铺满画面，动效字幕作为独立轨道叠在上面 | 发射/发布会/新闻素材配解说 | patterns.md "Top-Level Composition"（caption-overlay 子合成） |
| C22 | 资料图缓推 | 静态图片在画面里缓慢放大或平移，像镜头缓缓推近 | 老照片、截图、图表、新闻配图 | SKILL.md GSAP/CSS 动画默认能力（img 入轨+transform） |
| C23 | 透明人像叠加 | 抠好像的真人（透明 WebM）叠在图形层之上讲话 | 真人出镜但不要实景背景 | SKILL.md [能力对照表] 抠像（人物分割，透明 WebM） |

## 五、转场（C24-C65，填 `transition_in` 字段）

来源：`../../hyperframes/references/transitions/catalog.md`（CSS 转场路由表）、`../../hyperframes/references/transitions.md`（shader 名单与能量表）、`../../hyperframes/visual-styles.md`

规则提醒（transitions.md 硬规则）：一个片子里挑**一种主转场**，最高频转场占比 ≥50%（含本数），目标区间 60-70%，另备 1-2 种点缀；**CSS 转场与 shader 转场不混用于同一合成**；不要每个镜头换一种。禁用（渲染端明确做不了/会穿帮）：星形光圈、移轴、镜头光晕、铰链门。

### 溶解家族（枚举值 crossfade）

| ID | 名称 | 画面一句话 | 适用场景 | 来源 |
|---|---|---|---|---|
| C24 | 硬切 | 无过渡直接换画面 | 首镜固定值；需要冲击；Swiss Pulse 等主题的默认 | spec 模板枚举；catalog.md |
| C25 | 交叉溶解 | 前后画面互相渗入渗出，平滑交接 | 内容延续、"接着说" | catalog.md Dissolve 行 crossfade |
| C26 | 虚化交叠 | 前画面先虚化，后画面从虚里实起来 | 梦境、回忆、情绪流动（"跟我漂一会儿"） | catalog.md blur crossfade |
| C27 | 变焦点转移 | 焦点从一个平面拉到另一个平面，主体换人 | 高端产品、双主体对话感 | catalog.md focus pull |
| C28 | 浸色过渡 | 画面浸入一种颜色（常为黑）再浮出下一幕 | 段落终结、郑重收束 | catalog.md color dip |

### 推压/位移家族（枚举值 wipe）

| ID | 名称 | 画面一句话 | 适用场景 | 来源 |
|---|---|---|---|---|
| C29 | 平移推入 | 新画面把旧画面整体横向推出去 | "下一点"、杂志翻页感 | catalog.md Push 行 push slide |
| C30 | 纵向推入 | 新画面从下方/上方整幅推上来 | 章节递进、列表推进 | catalog.md vertical push |
| C31 | 弹性推入 | 推入时带过冲回弹 | 轻松、玩具感、消费向 | catalog.md elastic push |
| C32 | 挤压缩放 | 旧画面被压扁/压缩让位给新画面 | 冷静机械、克制的技术感 | catalog.md squeeze |
| C33 | 圆形揭幕 | 一个圆从中心张开，揭开新画面 | 聚焦单一主体、柔和揭示 | catalog.md circle iris |
| C34 | 菱形揭幕 | 菱形轮廓扩张揭开新画面 | 几何感、精确主题 | catalog.md diamond iris |
| C35 | 斜线对切 | 一条斜线扫过，两个画面沿斜线换防 | 版式感强的编辑向内容 | catalog.md diagonal split |
| C36 | 穿越放大 | 镜头猛推进旧画面，穿过它进入新画面 | 冲进细节、进入下一层级 | catalog.md zoom through |
| C37 | 缩远揭幕 | 旧画面缩小退场，新画面在它身后露出 | "跳出来看全局" | catalog.md zoom out |
| C38 | 重力坠落 | 旧画面整个掉下去，露出底下的新画面 | 戏剧性翻篇、失败/坠落隐喻 | catalog.md gravity drop |
| C39 | 立体翻牌 | 画面像一张卡片 3D 翻面，背面是新画面 | 换主题、揭示答案 | catalog.md 3D card flip |
| C40 | 色块拼合 | 几块全屏色块先后盖满再退开，拼出新画面 | 高能量分节、话题切换 | catalog.md staggered blocks |
| C41 | 百叶窗 | 横/竖条叶片依次翻转或覆盖（疏密随能量：缓 4/6 条，高能 12-16 条） | 干净的机械感切换 | catalog.md blinds（数量按能量） |
| C42 | 快门开合 | 像相机快门叶片开合一样切换 | 瞬间抓拍、记录感 | catalog.md shutter |
| C43 | 时钟擦除 | 一根指针扫过扇面，扫过处变成新画面 | 计时、里程碑、"时间到了" | catalog.md clock wipe |
| C44 | 网格溶解 | 画面碎成方格，逐格换成新画面（每格循环色板色） | 科技感、数据主题核心转场 | catalog.md grid dissolve |
| C45 | 圆形变形 | 旧画面的主体形状（圆）变形放大成为新画面 | 主体延续的柔切换 | catalog.md morph circle |
| C46 | 漏光渗色 | 一道过曝的光斑从画面边缘渗进来带走旧画面 | 温暖、胶片感、怀旧 | catalog.md light leak |
| C47 | 过曝闪白 | 画面亮度冲到发白，白里浮出新画面 | 高潮、爆点、强闪光节奏点 | catalog.md overexposure burn |
| C48 | 胶片灼烧 | 胶片烧穿的边缘蔓延，烧穿处露出新画面 | 复古、暴力推进、情绪灼烧 | catalog.md film burn |
| C49 | 纸页烧穿 | 内容随"纸面"一起烧穿掉，无碎片坠落 | 叙事毁灭感、旧篇章终结 | catalog.md page burn |
| C50 | 故障撕裂 | 画面RGB错位、撕裂、闪跳成新画面（有 shader 加强版） | 科技故障、紧张、punk | catalog.md glitch（+transitions.md shader glitch） |
| C51 | 色散错位 | 红蓝两色副本错开抖动再合拢 | 数字失稳、眩晕感 | catalog.md chromatic aberration |
| C52 | 涟漪荡漾 | 画面像水面一样起波纹，波纹里长出新画面 | 有机流动、轻松揭示 | catalog.md ripple |
| C53 | 录像带错位 | 画面像老录像带一样整条错位、拖影、色边 | 复古 VHS、记忆回放 | catalog.md VHS tape |
| C54 | 穿雾过渡 | 画面整体虚成一片雾，雾散见新画面 | 情绪过渡、长镜头之间的呼吸 | catalog.md blur through |
| C55 | 定向虚化 | 画面朝一个方向拖出速度虚影，甩到新画面 | 迅速带过、赶路感 | catalog.md directional blur |

### shader 家族（枚举值 shader；WebGL 逐像素合成，CSS 做不出的扭曲）

| ID | 名称 | 画面一句话 | 适用场景 | 来源 |
|---|---|---|---|---|
| C56 | 电影推镜 | 镜头像电影一样带景深推近，两个场景熔接 | 精确、临床感的主题（Swiss Pulse 首选） | visual-styles.md Swiss Pulse 行 |
| C57 | SDF 揭幕 | 几何形状以数学般的精确边缘扩张揭开新画面 | 几何、技术主题 | visual-styles.md Swiss Pulse 行 SDF Iris |
| C58 | 交叉形变 | 两个场景像有机体一样互相生长交融 | 高端、奢侈、从容（Velvet Standard 首选） | visual-styles.md Velvet Standard 行 |
| C59 | 甩镜 | 镜头横向猛甩，速度模糊里换场景 | 攻击性切换、punk 新闻感 | visual-styles.md Deconstructed 行 Whip Pan |
| C60 | 闪电灼边 | 闪电状裂纹爬满画面，沿裂纹烧穿成新场景 | 爆炸性发布、无法忽视的时刻 | visual-styles.md Maximalist Type 行 Ridged Burn |
| C61 | 引力透镜 | 画面像被引力透镜弯曲折叠后翻到新场景 | AI/数据/未来感主题 | visual-styles.md Data Drift 行 Gravitational Lens |
| C62 | 域扭曲 | 空间本身溶解扭曲，现实被改写后揭示新场景 | 戏剧性揭示、黑色主题 | visual-styles.md Shadow Cut 行 Domain Warp |
| C63 | 热浪扭曲 | 画面像透过热空气一样扭动，扭出下一场景 | 温暖、亲密、人的故事 | visual-styles.md Soft Signal 行 Thermal Distortion |
| C64 | 漩涡卷入 | 画面被卷进一个有机漩涡，漩涡里吐出新场景 | 喜庆、消费向、催眠式切换 | visual-styles.md Folk Frequency 行 Swirl Vortex |
| C65 | 波纹荡开 | 波纹从中心荡开，荡过之处变成新场景 | 庆祝、水润品牌感 | visual-styles.md Folk Frequency 行 Ripple Waves |

## 六、背景与氛围（C66-C70）

来源：`../../hyperframes/house-style.md` Background Layer、`../../hyperframes/references/audio-reactive.md`、`../../hyperframes/references/dynamic-techniques.md`

| ID | 名称 | 画面一句话 | 适用场景 | 来源 |
|---|---|---|---|---|
| C66 | 呼吸光晕 | 主题色的柔光斑在背景里缓慢胀缩呼吸 | 所有深色主题的底层氛围 | house-style.md "Radial glows (breathing)" |
| C67 | 脉冲细线 | 发丝级的主题色细线横贯画面，微微脉动 | 分隔、科技感、Swiss/编辑向 | house-style.md "Accent lines (subtle pulse)" |
| C68 | 颗粒质感 | 细噪点覆盖层让画面有胶片颗粒 | 消灭"太干净"的数字感 | house-style.md "Grain/noise overlay" |
| C69 | 主题纹饰 | 与内容强相关的装饰（轨道环、黑胶纹、网格线）随内容缓动 | 让画面"属于这个主题"（航天→轨道环） | house-style.md "Thematic decoratives" |
| C70 | 节拍律动 | 鼓点响时元素缩放/发光，跟音乐同呼吸 | 配乐驱动的片子、强节拍段落 | audio-reactive.md + dynamic-techniques.md |

## 七、界面/终端演示（C71-C74）

来源：hyperframes captions.md（Script-to-Style Mapping Tutorial 行：mono 字体 + typewriter 动画 + 高对比极简）、hyperframes typography.md（Monospace 字体分类与 `code`/`.code` 连字禁用规则）、hyperframes SKILL.md（GSAP/CSS 动画默认能力，img 入轨+transform）、hyperframes patterns.md（"Picture-in-Picture" 的 wrapper 位置/尺寸补间）

| ID | 名称 | 画面一句话 | 适用场景 | 来源 |
|---|---|---|---|---|
| C71 | 终端窗口演示 | 深色终端窗里命令逐字符敲出、光标闪烁，回车后输出行整块打印 | 讲命令行操作、部署/构建流程、黑客感段落 | captions.md Tutorial 行（typewriter）+ typography.md（Monospace / .code 规则） |
| C72 | 代码逐行揭示 | 等宽字体的代码块整段铺开，行按讲解顺序逐行点亮，关键行染 accent 色 | 逐行讲解代码、diff 对比、配置文件走读 | typography.md（code/.code mono 规则）+ captions.md Tutorial 行（fade 逐行变体） |
| C73 | 界面截图漫游 | 产品界面截图在画面里缓慢平移/推近，镜头依次走到各个功能区域 | UI 全貌导览、功能分区介绍、改版前后对照 | hyperframes SKILL.md GSAP/CSS 动画默认能力（img 入轨+transform，同 C22） |
| C74 | 界面聚焦推近 | 一个高亮框在界面截图上移动、缩放，把观众的视线钉到当前讲解的控件上 | 操作演示"点这里→再点那里"、表单流程走查 | patterns.md "Picture-in-Picture"（wrapper 位置/尺寸/圆角补间） |

---

## 组件选择顺序

给镜头挑组件时按这个顺序走，别跳步：

1. **先问这一镜的信息类型**（文案 / 数据 / 视觉冲击 / 节奏点）——它就是 info_payload，也是选组件的入口。
2. **再问画面主体是什么**：实拍素材 → 四、媒体合成（C20-C23）；数字/对比 → 三、数据图表（C14-C19）；纯文字/清单 → 一、文字呈现（C01-C08）；界面截图/终端操作 → 七、界面/终端演示（C71-C74）。
3. **需要强调时叠二、强调标记（C09-C13）**——强调标记是叠加层，不单独成镜，永远叠在 1-2 步选出的主体组件上。
4. **画面太空 → 叠六、背景氛围（C66-C70）**，每场景 2-5 个装饰（house-style 硬建议）。
5. **最后定 transition_in**（C24-C65），依据 `pacing-rules.md` § 5 的相邻镜头关系，不是按"哪个炫"挑。
6. 主题已定时，用文末 [主题偏好] 核对一遍组件与主题的绑定关系。

一个镜头的 component 字段填**主体组件**一个 ID；叠加层（强调标记/氛围）写进 motion 列的画面描述里（如"'解体'一词叠 C10 手绘圈"）。



### 需求 → 组件（用户的话怎么翻）

| 用户说 | 映射 | 说明 |
|---|---|---|
| "数字要炸出来" | C11 放射线爆开 + C16 巨号数据定格 | 先炸后定，一个负责冲击一个负责读清 |
| "数字要有仪式感地出现" | C14 数字滚增 / C18 粒子聚数 | 前者精确（Swiss 系），后者未来感（Data Drift 系） |
| "把这个词圈出来" | C10 手绘红圈 | 短词用紧圈变体 |
| "旧说法作废" | C13 划掉旧信息 或 C12 波浪删除线 | C13 更重、更暴力 |
| "整句一起安静出现" / "一个字一个字蹦" | 前者 C01/C05 的静呈现；后者 C02 逐词点亮 或 C04 弹跳 | 对应 SKILL.md 里字幕二选一的追问 |
| "像看电影那种字幕" | C02 低能量档（白色微亮、3% 缩放） | dynamic-techniques 能量分级 |
| "讲到哪个词亮哪个" | C02 karaoke + 强调词叠 C09/C10/C11 | 强调词永远打破基础模式 |
| "终端里敲代码的感觉" | C03 打字机字幕 | 配 monospace 字体 |
| "标题要砸出来" | C06 重锤砸字 / C07 乱序归位 | C6 猛、C7 科技 |
| "画面跟着鼓点跳" | C70 节拍律动（叠加到既有组件上） | 文字幅度限 3-6%，非文字可 10-30% |
| "多段视频拼一起" / "真人+素材" | C20 画中画 / C21 全屏实拍+字幕层 / C23 透明人像 | 按谁当主画面选 |
| "画面太空" | C66-C69 背景氛围层（每场景 2-5 个装饰） | house-style 硬建议，不是可选项 |
| "换个花哨的转场" | 先问情绪再从 C25-C65 挑（见下） | 转场表达的是两镜关系，不是装饰 |

### 逐字稿句型 → 组件类

| 逐字稿里的句子类型 | 组件类 | 例子 |
|---|---|---|
| 数字/规模句（"高达 X""增长了 X"） | 三、数据图表 C14-C19 | "速度达到每小时两万六千公里"→C14+C16 |
| 对比句（"A 是…而 B 是…"） | C19 双指标对排 | 助推器 vs 飞船各自结局 |
| 连续同概念数据（Q1→Q2→Q3） | C17 同位换数 | 换数字不换构图 |
| 关键词强调句 | 二、强调标记 C09-C13 | 按能量挑：hype→C11、术语→C10、常规→C09 |
| 宣告/转折句（"但就在这时…"） | C06/C07 + 高能量转场（C36/C40/C47） | 文字与转场一起加码 |
| 叙述推进句（默认） | 一、文字呈现 C01-C08 + 对应转场 | 不加码就沉底，镜头会空 |
| 描述既有素材的句子 | 四、媒体合成 C20-C23 | 有实拍就别用图形重复旁白 |

### 转场枚举对应（spec § 3 `transition_in` 字段）

| 模板枚举值 | 对应目录区间 | 语义 |
|---|---|---|
| `hard cut` | C24 | 冲击/首镜/主题默认 |
| `crossfade` | C25-C28（溶解家族） | "内容在延续" |
| `wipe` | C29-C55（CSS 推压/揭幕/覆盖/光效/故障…） | "分节/换话题/机械感" |
| `shader` | C56-C65（WebGL 家族） | 最 distinctive 的一击（开场/高潮） |

填写格式：`wipe · C43 时钟擦除`（枚举值在前，ID 附后）。同片只用一种主转场（60-70%）+1-2 种点缀；CSS 与 shader 不混用。

### 主题偏好（visual-styles.md 的绑定关系，选组件时顺带核对）

- Swiss Pulse → C14/C16 数字系 + C24 硬切 / C56 / C57
- Data Drift → C18 粒子聚数 + C61/C62
- Deconstructed → C06/C07 + C50/C59
- Maximalist Type → C04/C06 + C60
- Soft Signal → C08/C12 + C63；Shadow Cut → C62 + 慢推揭示

---

## 统计

实际组件总数：**74**（C01-C74）。
分布：文字呈现 8（C01-C08）｜强调标记 5（C09-C13）｜数据图表 6（C14-C19）｜媒体合成 4（C20-C23）｜转场 42（C24-C65：溶解 5 + CSS 转场 26 + shader 10 + 硬切 1）｜背景氛围 5（C66-C70）｜界面/终端演示 4（C71-C74）。
