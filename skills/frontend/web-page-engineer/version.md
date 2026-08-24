# Version Log

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
