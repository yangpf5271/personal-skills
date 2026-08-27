# Version Log

## 2026-08-27 · v2.16 · 触发判别键收紧:贪婪触发句限定 standalone artifact,补 openai 入口兄弟分流

- 审核动因:与接入版共享触发词(admin pages/dashboards/roles, states, transitions, approval flows 逐字相同),判别键应为产物落点。接入版 description 以 "inside an existing web app" 位置先行,本版中段贪婪句 "whenever the request involves any visual...deliverable" 丢失 artifact 限定,会吞掉接入版辖域,结尾分流句权重压不住。
- 修复:description 贪婪句补 "as a standalone artifact","Even if" 句补 "to be delivered standalone"——两边均以"产物落点"为第一判别键。agents/openai.yaml default_prompt 补 "If my request is UI changes inside an existing app codebase, switch to $web-page-integrator"(此前仅接入版反向分流,不对称);short_description 改为"独立 Web 交付物:管理系统页面原型 + 单页面视觉设计"消除入口歧义。
- 结果:description 982 字符(初版收紧后曾压线 1024,零余量有截断风险,再收两处措辞:删 "(with device frames)"、"Even if" 句改写为 "must ship standalone")。

## 2026-08-26 · v2.15 · design-spec.md 交接物:方向产物附带可供接入版直接消费的设计说明

- 动因:与 web-page-integrator 的接力链存在缝——拍板后接入版只拿到评审稿 HTML,token/密度/状态语义要靠反向扫描代码还原。这些信息在 A2/B4 声明里本就存在,落成交接文件近零成本。
- 规则落点(File Management 为唯一知识源,A2/B4 指针,checklist 闸门):`design-spec.md` 随产物同目录交付;触发=可能经 web-page-integrator 落地的产物(Track A 必带,Track B 改造/原型化既有产品必带,deck/动画/一次性 demo 不带);内容=token(CSS custom properties)/shell 与密度/状态色语义/相对现状 Delta(保留/改变/为什么)/待定假设/Tweaks 变体(默认值+清单)。
- 纪律:交付时定稿并与成品逐项核对(防 B4 声明与实物漂移);HTML 不引用不依赖该文件(单文件可携性不变);verify_artifact.py 只扫 html/css/js,.md 不进扫描,示例 URL 无误报风险(已核实 SCAN_EXTS)。
- 与接入版 v2.21 配对:文件名固定 design-spec.md,双技能指针机械可靠。

## 2026-08-26 · v2.14 · 仓库并列双技能化:接入版分出为 web-page-integrator,本技能定位为 standalone artifact 版

- 动因:接入版(v2.14~v2.20 在 feat/existing-system-integration 分支演进)与本技能规则实质分叉——交付物(app 代码 vs HTML 产物)、闸门(项目命令 vs file:// 双击)、文件集都不同,同名共存无法同时部署。定为同仓库 `skills/<name>/` 并列双技能(对齐 anthropics/skills 官方布局),各自独立演进与记版本。
- 本技能整体迁入 `skills/web-page-engineer/`(SKILL.md、references、scripts、vendor、assets、docs、agents、CONTEXT.md),行为无变化;description 尾部与正文首段补兄弟指针:"UI changes inside an existing app codebase → use `web-page-integrator`"。
- 兄弟技能 `skills/web-page-integrator/` 来自 feat 分支 v2.20 快照,含接口缝(页面需求清单交出接口/库表设计)、grilling 式歧义问询、dev 适配器契约回填等接入版全部规则;共享 references(admin-ui-baseline/components/design-playbooks)双份存在,本仓为源头,分叉风险自担。
- 部署方式变更:复制 `skills/<name>/` 整目录到技能目录(如 ~/.zcode/skills/<name>/),不再以仓库根为技能目录。
- feat/existing-system-integration 分支就此退役(保留历史不删)。

## 2026-08-26 · v2.13 · 吸收管理系统 UI 共性原则为稳定引用基线

- 动因:复查 `docs/research/2026-08-ui-common-principles.md` 与 `docs/research/2026-08-design-systems-survey.md` 后确认,对技能有执行价值的是 Track A 的默认管理系统视觉基线,而不是调研文档本身;主技能不应直接引用探索/研究材料。
- 新增 `references/admin-ui-baseline.md`:摘取稳定规则作为执行引用,覆盖默认参照系(Ant Design / Fluent / Carbon productive)、CSS token、B 端密度与字号、shell/表格布局、交互五态与无障碍。
- SKILL.md 接线:A2 无既有系统时指向该基线;A3 admin conventions 补 Fluent 与表格操作面规则;CSS Best Practices 改为按 Track A/Track B 分支定尺度,避免把消费端 16-18px 与 44px 触控目标误套到管理系统。
- Checklist 加固:通用块补 focus-visible、对比度、状态不只靠颜色、字段错误就近呈现、颜色 token 化;Track A 块补表格密度检查(工具栏、sticky 表头、右侧操作列、数字右对齐与 tabular numbers)。
- 文风修正:Anti-Patterns 不再把系统 UI 字体栈一概视为懒默认;Track A 可使用基线系统字体栈,Track B 视觉探索仍需有意选择。

## 2026-08-25 · v2.12 · description 收紧至 1024 字符内(平台硬限),触发覆盖零丢失

- 动因:实测原 description 1178 字符,超出 Anthropic Agent Skills 规范的 1024 字符硬限(按官方格式分发会被截断);且产出类型枚举写了两遍(首段 9 类 + bullet 列表重复其中 6 类),违反 writing-for-agents"一个 branch 一个触发词"原则。
- 重写:合并两遍枚举为一段;bullet 只保留新增触发信息(输入侧:mockups/screenshots/PRDs;业务流程信号词:roles/states/transitions/approval flows;design system 探索);pushy 尾句与负面边界(Not for...)保留,删被覆盖的 "non-visual code tasks";按用户要求移除 Chart.js/D3 工具名(data visualization 语义已覆盖,工具细节属正文 identity)。
- 结果:1178 → 895 字符(余量 129),159 → 122 词(skill-creator 的 ~100 词软参考线附近)。全部触发 branch 核对无丢失。agents/openai.yaml 不受影响(display_name/short_description/default_prompt 均不复制 description)。

## 2026-08-25 · v2.11 · 闭环审核修复:脚本行注释误报、调用路径 cwd 歧义、块名指代

- 审核动因:用户要求审核 v2.9~v2.10 修改的流程闭环性。主干确认闭环(file:// 三时点防线、A5/B7→checklist 引用、Anti-Patterns 合并无信息丢失);实测抓出 4 处问题,本版全修。
- **[高] 脚本 `//` 误报(实测复现)**:无空格 JS 行注释(`//eslint-disable-next-line`)被当成协议相对 URL 报出——正常带注释产物会持续误报,"零发现"永不可达,agent 将学会无视扫描结果,闸门 credibility 失效(v2.7 教训重演形态)。修法:URL 检测拆双正则——绝对 `http(s)://` 保持全文扫描(注释内也报,维持 "none allowed" 字面规则);协议相对 `//` 仅在属性/url() 上下文(前导引号/括号/等号)命中。块注释内 https:// 仍报属规则字面语义,非 bug。
- **[中] 调用路径 cwd 歧义**:`python scripts/verify_artifact.py` 隐含 cwd=技能仓库根,而执行 agent 的 cwd 通常是用户项目目录。两处(Local Vendor workflow、checklist)改为 `python <skill-dir>/scripts/verify_artifact.py <artifact-dir>`,占位符对仗,不依赖 cwd。
- **[低] A5 块名不一致(既有)**:"visual block" 改为 "All-artifacts block",与 checklist 实际小节名对应。
- **[低] File Management 指针补定位**:"hard rule 5" → "hard rule 5 (React + Babel)"。
- 回归:case-1b 7 文件零发现;行注释(带/不带空格)零误报;协议相对 URL 在 HTML src 与 CSS url() 均命中;五类违规(外置 text/babel、type=module、绝对远程 URL、import、fetch)全检出;vendor 与 xmlns 豁免正常。
- 附注:checklist 机械项引入 python 依赖,常规 agent 环境均具备;不写手扫 fallback 以免重新引入 v2.10 刚删除的 duplication。

## 2026-08-25 · v2.10 · 按 writing-for-agents 规范审查:单一真源收敛,删重复表述

- 依据 writing-for-agents(.agents/skills)agent 文档写作规范复查:信息层级/分支披露/完成判据/checklist 可核对性/leading words(file://、double-click、pilot screens 等术语纪律)均达标;invocation 为 model-invoked + description 承载触发分支,符合 SKILL-MECHANICS。
- 删四处 duplication(同一 meaning 多处副本,虚增层级地位且花双份 token):①Step 0 弹性法则第 4 条"checklist never skipped"——与第 1 条"runs the full checklist"及 checklist 标题三重重复;②File Management 的 "JSX loading constraint" 段——知识并入硬规则第 5 条(补"plain script/link 外链合法"的 why),File Management 只留产物形态分级;③④checklist 的 text/babel 禁令条与 remote-URL 条——均为 v2.9 脚本扫描项的子集,机械验证超集已涵盖。
- Anti-Patterns 第 3、4 条合并(Placeholder>fake 与 no filler 语义重叠)。
- 净 -7 行。JSX/file:// 约束现为三时点三角色:写前规范(硬规则 5,唯一知识源)→ 写中冒烟(A4)→ 交付机械验证(脚本)+ 双击核对(checklist),时点/角色不同不属 duplication。
- 有意不动:①description 保持 pushy 详尽——与该规范"指针逐词精剪"存在张力,skill-creator 的欠触发对策优先(v2.6 刚定稿);②HTML File Structure 模板段为 no-op 候选(模型默认会写标准骨架),但 no-op 判定 model-relative 需实跑验证,不凭辩论删;③Chinese Typography 仅 8 行,披露收益低于指针成本;④A3 admin conventions 摘要与 components.md 明细属"内联摘要+披露明细"合法层级。

## 2026-08-25 · v2.9 · 按 skill-creator 规范审查:固化交付扫描脚本,删正文冗余

- 依据 skill-creator(claude-plugins-official)技能写作规范复查:结构性规则基本达标——渐进披露(~290 行主文件 + references 按需)、advanced-patterns.md 已带 TOC、design-systems/ 经 index.md 按品牌索引、6 个 references 均在正文带时机引用、description 已是 pushy 风格含正反边界。
- 删正文 Scope 段:与 frontmatter description 完全重复;规范明确"when to use"信息只进 description 不占正文上下文。
- 新增 `scripts/verify_artifact.py`:把交付前手扫(v2.7 起的 http/unpkg/jsdelivr/googleapis 扫描)固化为确定性脚本,并扩展 file:// 不兼容写法检测——外置 text/babel、`type="module"`、authored 纯 JS 的顶层 import/export、fetch/XHR(v2.7 事故根因均在此列)。vendor/ 与 assets/fonts/ 自动豁免,xmlns/W3C 命名空间不误报。
- 接线:Local Vendor Resources 扫描步骤改为跑脚本(零发现才通过);checklist 新增"静态扫描零发现"条目,列 file:// 双击验证之后。
- 实测:case-1b 产物 7 文件零发现(exit 0);构造坏样例 5 类违规全部命中、豁免项零误报。
- 两处有意取舍:①design-systems/ 下 20+ 档案文件超 300 行不加逐文件 TOC——按品牌名查阅的档案,入口 index.md 即总目录,符合规则"帮模型定位内容"的意图;②hard rules 保留编号禁令格式——每条均带 why 解释,满足规范的"解释理由"要求,而 v2.3/v2.8 事故换来的闸门语义("Non-negotiable")优先于"少用 MUST"的文风建议。

## 2026-08-24 · v2.8 · 防线前移:硬规则第 5 条 + A4 逐页 file:// 冒烟

- 背景:v2.7 只补了结尾闸门,缺陷仍要到 A5 统一验证才暴露,返工面最大;且 JSX 约束散在正文("React + Babel (Inline JSX)" 段、File Management 段)时效力不足——写代码时 agent 真正遵守的是 Non-negotiable hard rules 序列(v2.3 的 window.X 规则落此后再未被踩)。
- 硬规则新增第 5 条:JSX 不得外置(`text/babel src` 在 file:// 下被 CORS 拦),内联单块或预编译;产物必须双击即开,永不为本地 HTTP server 而设计。
- A4 build order 追加:每页组装完立即以 `file://` 双击冒烟,不把验证攒到 A5。B 轨道不动:单页产物 Build 与 Verify 本就相邻。
- 三层防线成型:写前(硬规则)→ 写中(A4 逐页冒烟)→ 写完(checklist 兜底,v2.7)。

## 2026-08-24 · v2.7 · file:// 闸门:JSX 外置禁令与双击验证进检查清单(来自真实执行事故)

- 背景:一次真实执行中,产物把 JSX 外置为 `<script type="text/babel" src="./app.js">`——正中 v2.1 记录的 file:// CORS 限制(白屏);agent 未回改为内联,而是引入 `python -m http.server` 绕过,交付属性从"双击即开"静默降级为"需命令行起服务"。checklist 在 http:// 环境验证照样全绿,偏离一路溜到用户面前。
- 教训:明文警告(正文 JSX loading constraint)仍被踩——散在正文的约束是"读过去就忘"的,checklist 逐项打钩才是闸门;且验证协议不锚定 `file://` 时,起服务验证会掩盖 file:// 白屏。
- 通用检查清单新增两项:①逐页以 `file://` 双击方式验证,本地 HTTP server 通过不替代;②禁止 `<script type="text/babel" src="...">`,JSX 内联单块或预编译为纯 JS。
- Local Vendor Resources 新增交付说明约束:最终回复不得指示用户起本地 HTTP server 查看产物(必须双击即开);确需服务的极少数场景,产物须显式声明理由,不得静默降级。

## 2026-08-24 · v2.6 · 技能更名:web-design-engineer → web-page-engineer

- 理由:原名中 "design" 源于旧"视觉惊艳"定位,对执行实例有视觉优先的残余引力;双轨道的共同单位是"页面"、立场是"工程",新名与"面向技术的页面设计"定位对齐。触发行为由 description 承担,更名属身份对齐非功能变更。
- 同步修改:SKILL.md `name:` 与标题;agents/openai.yaml 三处(display_name、short_description、default_prompt——原 default_prompt 写死"先提 4 方向再选",与新 Step 0 分诊矛盾,重写为分诊版)。
- 仓库根目录同步改名(git 不跟踪根目录名,为文件系统重命名)。**注意:其他机器/路径的部署副本需以新名重新同步;持久记忆按项目路径索引,改名后新会话将是新的记忆命名空间——所幸关键决策已沉淀在仓库内(CONTEXT.md/ADR/version.md)。**

## 2026-08-24 · v2.5 · 吸收成熟后台设计规范:5 条管理界面惯例进 A3

- 来源(一手文档核对):Carbon button usage、Carbon data table usage、Ant Design Form。Polaris 规则页已迁移未能核对,未引用。
- SKILL.md A3 新增 "Admin conventions" 五条:①每屏一个主操作(最大权限并集视图下按操作区计;次操作仅与主操作成对;危险操作独立样式且必须文字标签)②按钮文案=动词(+宾语),禁孤名词/含糊"确定"③行内操作 ≤3,多余进溢出菜单;批量场景复选列+批量操作栏(全选含半选态)④动作进行中锁定触发按钮防重复提交⑤表单按有意时机校验(blur/防抖),错误在控件下方,提交失败滚到首个错误。
- components.md 同步:Table 条目补行操作/批量规则;Inline validation 条目补校验时机与提交失败滚动。

## 2026-08-24 · v2.4 · 新增布局要求:满视口外壳,列表区独立内滚

- 来源:用户指出列表数据多时不应让整个界面滚动。定为 A 轨道硬性要求:外壳(侧栏+顶栏)钉满视口永不参与滚动,纵向滚动只发生在数据区自己身上。
- SKILL.md A4 共享外壳条款 + 检查清单新增项(锁页滚/表头 sticky/工具栏常驻/非列表屏内容列可在外壳内滚/移动端豁免)。
- flow-driven-ui.md 新增 "Full-Viewport Shell, Inner Scrolling" 套路:html/body 锁高、grid 外壳、flex 链、表头 sticky,并写明关键坑——**flex 子项默认 `min-height: auto` 不收缩,链条上每层都要 `min-height: 0`,否则模式静默失效**。
- case-1b 产物同步改造(原为整页滚动):styles.css 外壳改满视口 + `.view--list`/`.card--table` 变体 + 表头 sticky + 860px 以下恢复自然滚动;index/approve 两列表页接线。经真实浏览器动态验证:表格区滚 724px 时页面 scrollY=0、表头/工具栏/顶栏坐标不变;详情页内容列在外壳内滚 580px,页面不动。

## 2026-08-24 · v2.3 · 硬规则第 4 条:纯 JS 共享全局必须显式挂 window(来自 case-1b 运行时缺陷)

- 背景:case-1b 产物 `shared.js` 以顶层 `const UI` 导出,三个页面以 `window.UI` 读取——顶层 `const` 不产生 window 属性,首用即 `TypeError: Cannot read properties of undefined`。subagent 的"全部校验通过"仅覆盖逐文件语法检查,未发现跨文件约定不一致;经真实浏览器验证发现并修复。
- 硬规则 #2(跨 babel 块需显式 window 导出)推广为独立的第 4 条:纯 JS 共享文件的跨文件全局必须显式 `window.X = X`,且生产者/消费者命名约定全文件一致。
- 检查清单同步:window exports 检查项涵盖 React 组件与纯 JS 共享模块。
- 产物已修复(`shared.js` 尾部 `window.UI = UI;`),并经真实浏览器逐页验证:列表 15 单全状态渲染、详情页三操作区 + 门控禁用带原因、工作台三队列均正常。

## 2026-08-24 · v2.2 · A 轨道重定位:交付管理系统页面,流程逻辑内化(ADR-0001)

- **交付物重定义**:A 轨道产出管理系统页面(真实系统观感、状态条件化 UI、真实数据密度、内存 mock 后端),不再产出带验证装置的流程演示原型。
- **状态机身份变更**:从"被演示对象"变为"内部控制器"——永不渲染为 UI,由页面查询 `can(state, action)` 决定按钮启用/禁用;状态级非法动作 = 禁用 + 原因提示,终态 = 操作区整体禁用 + 终态说明。
- **最大权限视图**:默认所有屏幕进导航、所有操作区渲染(角色并集);仅当设计明确要求权限差异时,在场景面板内加角色视角切换。
- **场景面板替代验证装置**:可拖拽圆球(默认右下角,demo 视觉语言)展开,含场景一键重置/跳转 + 记录状态速览(+ 变体分区);收起时完全不可见。状态面板/自由操作/walkthrough 标签页从产物 UI 中移除。
- **参考文件改写**:`references/flow-prototypes.md` → `references/flow-driven-ui.md`(控制器模式:守卫→按钮状态、状态→视图变体、最大权限视图、场景面板、种子数据纪律)。
- 新增 `CONTEXT.md` 术语表与 `docs/adr/0001-track-a-delivers-admin-ui-not-validation-demos.md`。
- 检查清单 Track A 块同步改写(新增"无验证装置"检查项)。

## 2026-08-24 · v2.1 · File Management 补充(来自行为测试经验)

- 产物形态按规模分级:小产物/单页 = 单 HTML 文件;Track A 业务系统 = 小目录(入口 HTML + `flow-machine.js` + `seed.js` + `styles.css`,状态机保持独立可起吊)。
- 记录 `file://` 技术约束:`<script type="text/babel" src>` 会被浏览器 CORS 拦截,JSX 须内联进入口页单个 text/babel 块或预编译为纯 JS;纯 JS/CSS 外链不受限(因此状态机、种子数据、样式独立成文件,JSX 不行)。
- 修正原文"超 1000 行拆成 JSX 模块用 script 标签组合"的指引——该做法在 file:// 下不可行。

## 2026-08-24 · v2 · 双轨道重构(业务系统适配 + 主文件精简)

依据:`.scratch/dual-track-skill-restructure/spec.md`

### 新增

- **Step 0 分诊表**:按输入信号选轨道与通道(业务流程/状态流转 → A 轨道;单页面任务 → B 轨道快速/标准/上下文通道),停下等用户的次数 0/1 封顶;含轻量系统边界规则与弹性四原则(内化≠跳过、假设必声明、唯一不可合并停顿、检查清单永不跳过)。
- **A 轨道(业务系统设计)**五阶段:A1 系统建模(流程模型 + 屏幕清单「角色×任务×状态集」+ 场景清单,与飞行屏幕 v0 合并为一轮确认);A2 一次性设计系统声明(含状态色语义);A3 显式页面层(飞行屏幕 2~3 个做完整单页设计 + 标准屏幕逐屏「任务→布局→组件→状态」+ 反同构法则);A4 装配顺序(种子数据→纯状态机→共享外壳→屏幕→walkthrough);A5 双清单验证 + 收尾说明。
- **references/flow-prototypes.md**:纯状态机模块(含骨架代码)、状态面板、自由操作按钮、引导式场景(含重置与场景选择:happy path/边界/非法操作)、角色切换、场景种子数据、独立 HTML 的屏幕接线与"起吊"约定。
- **检查清单 Track A 块**:业务状态全覆盖、流转可点、非法操作有拦截演示、角色视图齐全、walkthrough 可重置、跨屏数据一致、反同构、收尾说明。

### 修改

- 质量标准分支条件化:视觉探索=惊艳;业务系统=流程保真 + 任务适配(克制、密度、任务优先)。
- B 轨道(原 Step 1~7)精简保留:需求理解、上下文收集、风格方向门禁(含多样性门)、设计系统声明、v0、构建、验证。
- 幻灯片章节压缩为指针(细节留在 references/advanced-patterns.md);动画方案压缩为三层递进两句话;Tweaks 压缩为一节;变体哲学并入 B3。
- 检查清单拆为「通用块 + Track A 块」。
- frontmatter description 增加业务系统原型触发描述。

### 数据

- SKILL.md:约 581 行 → 约 320 行。
- 未改动:references/design-systems、vendor/、assets/、agents/openai.yaml、references/components.md(升格为 A3 页面层操作手册引用)。

### 待办(spec 测试决策)

用五组代表性输入对加载本技能的 agent 做行为验证:①带审批流的系统设计(应走 A 轨道、1 次停顿)②"摄影集展示网站"(B 快速通道、0 停顿)③UI 截图/代码库(上下文通道、0 停顿)④轻量系统边界⑤营销落地页(视觉质量回归)。
