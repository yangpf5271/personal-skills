# 跨设计系统 UI 共性设计原则(2026-08)

> 目的:基于《[系统 UI 设计规范成熟度与接受度调研(2026-08)](./2026-08-design-systems-survey.md)》界定的系统范围,提取各系统在 UI 设计层面**共同遵守的原则**,按配色、圆角与间距、文字排印、布局分布、交互状态、密度与无障碍六个维度整理成可执行清单,供 web-page-engineer Track A(管理系统页面)直接内化为 CSS 常量与布局范式。
> 口径:系统范围、分组与优先级引自调研文档;各维度**代表数值来自各系统公开 design token 与官方规范**(2026-08 时点,以各官方文档为准;个别未逐项核实的常识值已在文中注明"约")。
> 生成日期:2026-08-25。

## 1. 提取方法

- 覆盖对象:调研文档量化总表 24 个系统 + 4 个定性条目(Apple HIG、SAP Fiori、Atlassian、Lightning),共 28 个。
- 判定标准:某原则在**过半头部系统**中稳定成立 → 列为共性原则;少数派不视为"错误",在 §9 记录其偏离及理由。
- 表述方式:每条原则附**代表系统的实测值**(官方 token 或规范原文数值),使原则可直接换算为 CSS 常量。
- 术语:"B 端"指管理系统/企业软件语境(Track A 目标),"消费端"指面向公众的内容型界面。

## 2. TL;DR:十二条共性原则

1. **色彩结构 = 一个主色 + 10 级左右中性灰阶 + 3~4 个功能色**,再无其他自由色;颜色经语义 token 引用,不裸写色值。
2. **主色用蓝**:除 M3(紫/动态色)、Naive UI(绿)、GOV.UK(黑主体)外,头部系统主色全部为蓝色系(HSL 色相约 205-225、亮度 35-55%),保证主色底上白字对比 ≥ 4.5:1。
3. **正文不写纯黑,页面不写纯灰之外的花色**:文本是灰阶 900-1000 档(#1D2129~#161616)或黑色 88% 不透明度;页面底是 1-3% 冷灰(#F0F2F5 家族),纯白留给卡片表面。
4. **间距以 4px 为原子、8px 为主网格**,常用档 4/8/12/16/24/32/40/48/64;唯一成体系例外是 GOV.UK 的 5px。
5. **圆角三档**:控件 3-6px、卡片与浮层 6-12px、胶囊/标签 999px;总趋势从小变大(antd 2→6、M3 4→28),但 Carbon/GOV.UK 坚持直角。
6. **字号基准:B 端 14px、消费端 16px**;阶梯 12/14/16/20/24/30,实际使用级数 ≤7;最小可读字号 12px(M3 下探 11,GOV.UK 反向设底线 16)。
7. **行高 1.5±0.1,层级靠"字号+字重+灰度"三手段**;字重只用 400/500/600(700 罕用),中文语境不用斜体。
8. **B 端骨架统一:左侧导航(200-264px,可折叠至 48-80)+ 顶栏(44-64px)+ 高密度内容区(内边距 16-24px)**;表格全宽、表单单列、标签同一种对齐。
9. **双密度是 B 端分水岭**:紧凑档控件/行高约为默认档的 75-80%(表格行 32-40 vs 48-54);Carbon/antd/Fluent 均把密度做成一等 token。
10. **交互五态全覆盖**:hover / active / focus-visible / disabled(降透明 40-60%)/ loading;禁用不等于隐藏。
11. **动效短促**:常规过渡 150-300ms、ease-out;动效用于状态衔接而非装饰(Fluent "Metronome" 节奏隐喻)。
12. **无障碍是基线不是加分项**:正文对比 ≥ 4.5:1、大字与图形 ≥ 3:1(WCAG 2.1 AA)、焦点环可见、暗色模式标配。

## 3. 配色

### 3.1 结构共识:一主色 + 中性阶 + 功能色

所有被考察系统无一例外地遵循同一色彩结构:**品牌主色一个、中性灰阶一组、语义功能色三到四个**。没有任何头部系统采用双主色或自由配色。

| 系统 | 主色 | 备注 |
|---|---|---|
| Ant Design(v5/v6) | #1677FF | hover #4096FF / active #0958D9(官方主题编辑器实测) |
| Element Plus | #409EFF | |
| Arco Design | #165DFF | 官方梯度:5=#4080FF(hover)/7=#0E42D2(active)/4=#6AA1FF(禁用) |
| TDesign | #0052D9 | |
| Semi Design | 品牌蓝(可配) | 主题从 Figma 经 DSM 直达 token(调研文档 §4.4) |
| Bootstrap 5 | #0D6EFD | |
| MUI | #1976D2 | 长期默认值 |
| Fluent 2 | #0F6CBD | 品牌通信蓝 |
| Carbon | #0F62FE | blue-60 |
| Salesforce SLDS | #0176D3 | |
| Atlassian | #0052CC | |
| USWDS | #005EA2 | blue-60v |
| SAP Fiori Horizon | #0070F2 | 约,以官方主题为准 |
| GOV.UK | 链接 #1D70B8 | 主体黑 #0B0C0C,无品牌色 |
| Material 3 | #6750A4(基线) | 动态色可整体替换(例外) |
| Naive UI | #18A058(绿) | 证明主色可换而结构不变(例外) |

**主色梯度的共识**:主色必须预生成 10 级梯度(Arco primary-1..10、antd 由算法从 seed 派生 10 档),hover 取亮一档、active 取深一档、disabled 取低饱和档——交互状态不许现调颜色。

### 3.2 中性色:文本三档 + 表面两档 + 边框一档

| 层级 | 代表值(亮色模式) |
|---|---|
| 文本 主/次/弱 | antd rgba(0,0,0,.88)/.65/.45;Element #303133/#606266/#909399;Arco #1D2129/#4E5969/#86909C;Carbon gray-100 #161616/gray-70/gray-50 |
| 页面底 | #F0F2F5(antd 经典中后台底)~#F7F8FA;GOV.UK 辅助底 #F3F2F1 |
| 容器表面 | 纯白 #FFFFFF——亮色模式下卡片一律白底,靠灰底页面衬托层级 |
| 边框/分割线 | #D9D9D9~#E5E7EB(Element #DCDFE6、Arco #E5E6EB、Tailwind gray-200 #E5E7EB) |

灰阶总数 9-13 级(Tailwind 11 级 gray-50..950、antd 12 级中性、Arco 10 级灰),但 UI 实际只用上表 6-7 个语义位。

### 3.3 功能色:语义四件套

success=绿 / warning=橙黄 / error=红 / info=蓝(或直接复用主色)。
代表:antd #52C41A/#FAAD14/#FF4D4F;Element #67C23A/#E6A23C/#F56C6C;Bootstrap #198754/#FFC107/#DC3545;Carbon #24A148/#F1C21B/#DA1E28;GOV.UK 绿 #00703C/红 #D4351C。
共识:**红色只表达错误与破坏性操作**;黄色底上放白字普遍不过对比度,warning 一般以深色文字或图标承载(GOV.UK/Carbon 的做法)。

### 3.4 对比度与焦点

- 正文文本/背景 ≥ 4.5:1;大号文本(≥18.66px 或 ≥14px 粗体)与有意义图形 ≥ 3:1(WCAG 2.1 AA)。政府系强制,Carbon/Fluent/Spectrum 内建校验。
- 焦点必须可见:`:focus-visible` 焦点环,惯用做法是 2px 外环 + 2px 间隙(Tailwind ring-2 ring-offset-2 范式);GOV.UK 用黄底黑字 #FFDD00 做到最强可见性。

### 3.5 暗色模式(标配)

调研文档共性趋势之一:头部系统(含国内六强)全部原生暗色 + token 化。做法高度一致:

- 表面色阶反转:容器底 #141414~#1E1E1E,**绝不纯黑**;
- 文本改白色 85-95% 不透明度;
- 主色提亮去饱和(antd 暗色算法将 #1677FF 派生为 #1668DC);
- 阴影在暗色下基本失效,分层改用 1px 亮边框;
- 功能色同步调亮,重过对比度校验。

## 4. 圆角、边框与间距

### 4.1 间距:4px 原子,8px 主网格

| 系统 | 间距体系 |
|---|---|
| Tailwind | 1 单位 = 4px,线性递增 |
| Bootstrap 5 | $spacer = 1rem(16px),工具类档位 4/8/16/24/48 |
| antd | 离散 token:8/12/16/24/32(xs/sm/md/lg/xl),组件级 8px 网格 |
| Carbon | 2px 起:2/4/8/12/16/24/32/40/48/64/80/96/160 |
| Material 3 / Fluent / Arco / Semi / TDesign / SLDS / Polaris / Atlassian | 4px 基网格(官方声明 4pt/8pt grid) |
| USWDS | 8px 单位制 |
| GOV.UK | **唯一成体系例外:5px 基数**(5/10/15/20/25/30/40) |

常用档共识:**4/8/12/16/24/32/40/48/64**;超过 64 的间距交由布局组件控制,不设 token。

### 4.2 圆角:三档阶梯

| 系统 | 控件 | 卡片/浮层 | 备注 |
|---|---|---|---|
| antd v5/v6 | 6(SM 4) | 8(LG) | v4 曾为 2,升级后翻三倍 |
| Element Plus | 4 | 4 | 另设 round 20px 用于胶囊按钮 |
| Arco | 2(S)/4(M) | 8(L) | 官方 token 页实测 |
| TDesign | 3(默认)/2(S) | — | |
| Semi | 3 | 6 | dropdown/scroll list 等用 6 |
| Bootstrap 5 | 4 | 8 | |
| Tailwind | 4 | 6/8/12/16 | |
| shadcn/ui | 8 | 8-12 | 单一 `--radius` 变量派生全部档位 |
| MUI | 4 | 4 | |
| Fluent 2 | 4 | 8 | |
| Material 3 | 4/8 | 12/16/28 | 五档 shape scale,Expressive 继续放大 |
| Carbon | 0 | 0-2 | 企业直角风 |
| GOV.UK | 0 | 0 | 全站无一处圆角 |

共识与趋势:

- 控件圆角收敛于 **3-6px**,卡片浮层 **6-12px**,**胶囊(标签/头像/开关)999px 全圆**——三档足够,无需更多。
- 圆角是"时代感"最敏感的参数:约 2px(2016 前)→ 4-6px(2020 主流)→ 8px+(2023 后,shadcn/SAP Horizon/M3 Expressive)。A 轨道取值 <4px 会显旧。
- 圆角作用于背景与边框,不裁切内容(M3 明文规则);相邻元素嵌套时内层圆角略小,视觉上同心。

### 4.3 边框与分层

- 边框 1px 实线,#D9D9D9~#E5E7EB;表格线/分割线比外边框更浅一档。
- B 端分层靠"灰底 / 白卡 / 1px 边框"三件套,阴影克制:卡片 0-1 档(如 0 1px 2px rgba(0,0,0,.06)),浮层 2 档(0 4px 12px rgba(0,0,0,.12))。大范围投影是消费端语言(M3 elevation 0-5 五档递增)。
- 浮层 z-index 阶梯化:antd 弹层基线 1000;Bootstrap 1000(dropdown)→1080(tooltip);MUI 1100(app bar)→1500(tooltip)。间隔 10-1000,杜绝随机数。

## 5. 文字排印

### 5.1 基准字号:14(B 端)/ 16(消费端)

| 阵营 | 系统 | 正文基准 |
|---|---|---|
| B 端 14 | antd、Element Plus、Arco、TDesign、Semi、Fluent 2、SAP Fiori、Polaris、Primer、SLDS、Carbon(productive 模式) | 14px |
| 消费端 16 | Bootstrap、Tailwind/shadcn 生态、M3(body-large)、MUI(body-1)、GOV.UK(19px,全站底线 16) | 16px |

B 端选 14 的理由一致:**信息密度优先于单字阅读舒适**。A 轨道(管理系统)应对齐 14。

### 5.2 字号阶梯:模数约 1.2,级数 ≤7

- antd:12/14/16/20/24/30/38(heading1-5 = 38/30/24/20/16)
- Fluent 2 type ramp:10/12/14/16/20/28/40/56/68
- M3:11/12/14/16/22/24/28/32/36/45/57
- Tailwind:12/14/16/18/20/24/30/36/48/60
- Element/Arco/TDesign/Semi 同为 14 基准的离散档位

共识:相邻档比约 1.2-1.25,单页实际只用 5-7 档;**12=辅助说明,14=正文,16=小标题,20-24=区块标题,30+=页面主标题**。

### 5.3 最小字号

- 通用下限 **12px**(B 端辅助文字、表格次级信息)。
- M3 label-small 下探 11px(消费端极限);GOV.UK 反向把全站底线设为 16px——同一问题的两种立场:A 轨道取 12px 封底、正文 14。

### 5.4 行高与字重

- 行高:正文 1.4-1.6(取 1.5);标题 1.2-1.3;表格单元格 1.3-1.4。
- 字重三档:400(正文)/ 500 或 600(强调、按钮、小标题)/ 700(大标题,罕用)。中文没有斜体传统,层级靠字重与灰度表达;数字场景用 `font-variant-numeric: tabular-nums`(表格金额/计数对齐)。

### 5.5 字体:系统字体栈,零外部依赖

共识:**UI 默认用系统字体栈,不引外部字体**(性能与一致性;对单文件交付物更是硬约束)。中英文混排栈各系统高度一致:

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
  "Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
```

- 政务系用自有字体但同理念(GOV.UK GDS Transport、USWDS Public Sans),均系统级回退。
- 等宽字体只用于代码/ID 类内容:`SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace`(GitHub Primer 范式)。

### 5.6 文案约定

英文界面 **sentence case**(仅首词首字母大写)是 Apple/Microsoft/Google/GOV.UK 风格指南的共同要求;按钮用动词短语(如 Save changes)。中文对应约定:按钮 2-6 字动宾短语,不带句号;标题不堆砌感叹号。

## 6. 布局分布

### 6.1 B 端页面骨架(高度一致)

```
┌──────────┬────────────────────────────────┐
│          │ 顶栏 44-64px(antd 64 / Carbon 48)│
│ 侧导航    ├────────────────────────────────┤
│ 200-264  │ 内容区 padding 16-24px           │
│ (折叠至   │ ┌────────┐  ┌────────┐          │
│  48-80)  │ │ 白底卡片 │  │ 白底卡片 │ 间距16/24│
│          │ └────────┘  └────────┘          │
└──────────┴────────────────────────────────┘
   页面底 #F0F2F5,卡片 #FFF,圆角 6-8,边框 1px
```

实测:antd Sider 默认 200px(折叠 80px)、Header 64px;Carbon UI shell 顶栏 48px、左导航 256px;M3 navigation rail 80px、drawer 360px。
共识:**侧导航必须可折叠**;顶栏容纳面包屑/全局搜索/用户态;内容区按 ≥1280px 桌面基准设计,移动端只做降级(表格转卡片、导航自动折叠),不做全功能对等。

### 6.2 栅格与断点

- 列数:**12 列栅格是绝对主流**(Bootstrap/antd/MUI/Element);Carbon 用 16 列 2x 栅格(2px 基网格)。B 端实际以"分栏卡片"为主,流式栅格多用于表单页(2/3 主表单 + 1/3 侧边说明卡)。

| 系统 | 断点阶梯(px) |
|---|---|
| Bootstrap 5 | 576 / 768 / 992 / 1200 / 1400 |
| antd | 576 / 768 / 992 / 1200 / 1600 |
| Tailwind | 640 / 768 / 1024 / 1280 / 1536 |
| MUI | 600 / 900 / 1200 / 1536 |
| M3 窗口类 | 600 / 840 / 1200(compact/medium/expanded) |

共识:**768(平板)、1200(桌面工作区)、1536+(宽屏)是三个关键阈值**;断点只服务于降级策略,不改变信息架构。

### 6.3 内容区三大件:页头、卡片、表格/表单

- **页头**:页面标题(20px 级)+ 描述(14px 次级灰)+ 主操作按钮(右上),几乎所有 B 端系统页面的第一行。
- **卡片**:白底、圆角 6-8、1px 边框或 0-1 档阴影、内边距 16-24;卡片间距 16-24;Dashboard 用 2×N 或 12 列网格排布(间距 16)。
- **表格**(B 端核心组件):
  - 工具栏(搜索/筛选/批量操作/列设置)置于表格上方;
  - 表头粘性固定;斑马纹或行分割线二选一;
  - 行高:默认约 48-54(MUI DataGrid 默认 52),紧凑 32-40(DataGrid compact 36、Carbon 紧凑 32、antd small 档);
  - 数字列右对齐 + 等宽数字;操作列固定在最右。
- **表单**:
  - **单列优先**,多列仅用于强相关字段;
  - 标签顶对齐(GOV.UK/Fluent/antd Pro 场景)或左对齐(Element/Arco 后台常见),同一系统内不混用;
  - 控件统一高度、水平节奏 16-24、分组间距 32-48;
  - 控件默认高:B 端 32-40(antd 32,sm 24/lg 40;Fluent medium 32),消费端 40-56(MUI/Bootstrap);输入宽度 240-320px,搜索框可全宽。

### 6.4 对齐规则

- 文本左对齐(F 型阅读动线);**数字右对齐**(小数点对齐);
- 表单标签文字左对齐;**对话框按钮右下角、主按钮在最右**(antd/Element 惯例;Windows 习惯主键在左,二选一后全系统一致即可);
- 图标与相邻文字垂直居中,图标后留 8px;
- 悬浮层(下拉/气泡)与触发元素左对齐,溢出屏幕才翻转。

## 7. 交互与状态

1. **五态全覆盖**:任何可交互元素必须定义 hover(背景或边框微变)、active(再深一档)、focus-visible(焦点环)、disabled(降透明 40-60% 或灰阶替换,**保留占位**)、loading(spinner 或骨架屏)。
2. **错误态 = 红边 + 红色帮助文本**:错误信息写在字段正下方(带 `aria-invalid`/`aria-describedby`),不用 toast 承载表单校验。
3. **点击目标**:触控 ≥44×44(iOS HIG)/ ≥48dp(Android/M3);桌面紧凑模式 ≥24×24(Fluent/Carbon compact)。
4. **动效**:过渡 150-300ms、ease-out 为主;进入快于退出;动效表达状态变化(展开/出现/成功反馈),不做无信息量的装饰动画。
5. **加载**:首屏用骨架屏(形状与最终布局一致)优于 spinner;局部刷新不遮罩整页。

## 8. 密度与无障碍:B 端两个分水岭

### 8.1 双密度体系(呼应调研文档横向观察 #3)

Carbon productive/expressive 双模式、antd 尺寸三档 + 紧凑算法、Fluent 密度 token、MUI/Element 的 dense/small——头部 B 端系统全部把"高密度工作模式"做成一等能力。
换算规律:**紧凑档 ≈ 默认档的 75-80%**(控件 32→24-28,表格行 48-54→32-40,页边距 24→16)。A 轨道"数据密度真实"的验收可据此量化。

### 8.2 无障碍基线(呼应调研文档横向观察 #5)

头部系统全部声明 WCAG 2.1 AA。可执行清单:对比度(§3.4)、焦点可见(§3.4)、点击目标(§7)、**不靠纯颜色传达状态**(红边之外加图标或文字)、表单 label 显式关联、图片 alt、键盘可完成全部操作。

## 9. 有理由的少数派(偏离 ≠ 错误)

| 系统 | 偏离点 | 理由 |
|---|---|---|
| GOV.UK | 5px 间距、19px 正文、全直角、黄色焦点、链接默认下划线 | 普惠可访问性最大化(服务全英人口),"文字即界面"的内容设计优先 |
| Carbon | 直角、16 列 2x 栅格、productive 密度 | 专业工作场景的严肃工具气质 |
| Material 3 | 紫基线色 + 动态色、圆角 4-28dp、字号下探 11 | 消费端品牌个性与个性化(dynamic color) |
| Naive UI | 绿主色 #18A058 | 品牌自由度示范:主色可换,结构不变 |
| SAP Fiori Horizon | 卡片级大圆角(约 12px+)、晨昏双主题 + 高对比变体 | 从拟物(Belize)转向现代亲和的企业新形象 |
| Bootstrap | 消费级 16px 基准、控件偏高 | 通用建站而非高密度后台 |

## 10. 落地:Track A CSS 常量清单

依据上述共性,给 A 轨道(单文件 HTML 管理系统页面)一套开箱常量(数值对齐 antd v6/Arco,即本文实测值):

```css
:root {
  /* 间距:4px 原子,8px 网格 */
  --space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 16px;
  --space-5: 20px; --space-6: 24px; --space-8: 32px; --space-10: 40px;
  /* 圆角:三档 */
  --radius-sm: 4px; --radius-md: 6px; --radius-lg: 8px; --radius-full: 999px;
  /* 字号:B 端 14 基准,模数约 1.2 */
  --font-xs: 12px; --font-base: 14px; --font-lg: 16px;
  --font-xl: 20px; --font-2xl: 24px; --font-3xl: 30px;
  --line-height: 1.5;
  /* 控件 */
  --control-h: 32px; --control-h-sm: 24px; --control-h-lg: 40px;
  /* 颜色:亮色;文本三档/表面两档/边框一档 */
  --brand: #1677ff; --brand-hover: #4096ff; --brand-active: #0958d9;
  --success: #52c41a; --warning: #faad14; --error: #ff4d4f;
  --text-1: rgba(0,0,0,.88); --text-2: rgba(0,0,0,.65); --text-3: rgba(0,0,0,.45);
  --bg-page: #f0f2f5; --bg-container: #fff; --border: #e5e6eb;
  /* 布局 */
  --header-h: 48px; --sider-w: 220px; --sider-w-collapsed: 64px;
  /* 浮层 */
  --shadow-1: 0 1px 2px rgba(0,0,0,.06);
  --shadow-2: 0 4px 12px rgba(0,0,0,.12);
  --z-popup: 1000;
}
```

配套检查项(可并入 A 轨道验收清单):

- [ ] 全部颜色经 token 引用,无裸写十六进制(品牌定义处除外)
- [ ] 文本/背景对比 ≥ 4.5:1;主色按钮上白字 ≥ 4.5:1
- [ ] 间距全部落在 4 的倍数;圆角只用三档 token
- [ ] 正文 14px、辅助 12px,无 <12px 文本
- [ ] 侧导航可折叠;顶栏 + 面包屑;内容区内边距 16-24px
- [ ] 表格:工具栏 + 固定表头 + 行分割线;数字右对齐 + 等宽数字
- [ ] 交互元素五态齐备,焦点环可见
- [ ] 表格行高或控件提供紧凑档(密度真实)

## 11. 来源

- 系统范围与接受度:本文 §1 所引调研文档(一手 API,2026-08-25 采集)。
- 代表值核实(2026-08 时点,一手查阅官方 token/规范页):
  - Ant Design 定制主题与主题编辑器:<https://ant.design/docs/react/customize-theme-cn>、<https://ant.design/theme-editor-cn/>(#1677FF、圆角 6、#FF4D4F 等)
  - Arco Design 设计变量:<https://arco.design/react/docs/token>(圆角 0/2/4/8/50%;主色梯度 #165DFF/#4080FF/#0E42D2/#6AA1FF)
  - Semi Design Tokens:<https://semi.design/zh-CN/basic/tokens>(圆角 3/6)
  - TDesign 主题与 token:<https://tdesign.tencent.com/>(圆角 2/3,主色 #0052D9)
  - Material 3:<https://m3.material.io/>(color / type / shape 三套规范)
  - Fluent 2:<https://fluent2.microsoft.design/>(type ramp、圆角、密度)
  - Carbon:<https://carbondesignsystem.com/>(2x 栅格、productive、spacing/gray token)
  - Bootstrap 5.3:<https://getbootstrap.com/docs/5.3/>(CSS 变量、断点表)
  - Tailwind:<https://tailwindcss.com/docs>(spacing/border-radius/font-size 默认值)
  - GOV.UK:<https://design-system.service.gov.uk/>(colour / spacing / typography 规范页)
- 通用标准:WCAG 2.1 <https://www.w3.org/TR/WCAG21/>。
- 其余系统官方文档入口见调研文档 §7 来源清单。
