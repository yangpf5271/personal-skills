# 系统 UI 设计规范成熟度与接受度调研(2026-08)

> 目的:为 web-page-engineer 技能 Track A(管理系统页面)梳理市面上成熟度高、接受度广的系统级 UI 设计规范,量化其接受度,并评估对 A 轨道交付物(单文件 HTML 管理系统页面)的可用性。
> 数据采集日期:**2026-08-25**。

---

## 1. 数据口径说明

- **量化数据全部来自一手 API**(当次采集):
  - GitHub stars / 最近推送时间 / 许可证:`api.github.com/repos/<owner>/<repo>`
  - npm 周下载量:`api.npmjs.org/downloads/point/last-week/<package>`
  - 当前版本号:`registry.npmjs.org/<package>/latest`
- **npm 周下载量是生态规模指标**,含 CI 重复安装与间接依赖,不等于"使用该系统的站点数"。受间接依赖放大明显的包在表中单独注明(如 `tailwindcss`、`radix-ui`、`class-variance-authority`)。
- **二手来源**(仅 4 项,均标注):Shopify Polaris 的 stars(约 6.2k,GitHub API 对该仓库连续失败);Polaris 转向 Web Components 的事实;Material 3 Expressive 发布背景;SAP Fiori Horizon 现状。
- **首发年**依据各官方文档/仓库 README,标"约"者为约数。
- 许可证为 GitHub API 的 SPDX 识别结果;`NOASSERTION` 表示仓库使用自定义或多重许可证文本、API 无法归类,实际许可证见各仓库 LICENSE 文件。
- 无 npm 发布主体的规范(Apple HIG、SAP Fiori、Atlassian Design System)只做定性评估,不进量化总表。

## 2. TL;DR 核心结论

1. **B 端/管理系统领域的事实标准**:世界范围内是 **Ant Design**(中后台绝对主流,npm 3.77M/周)、**Fluent**(微软企业血统)、**Carbon**(IBM);**SAP Fiori / Salesforce Lightning / Atlassian** 在各自企业生态内不可替代。
2. **开源组件生态的接受度之王**:按 npm 周下载是 MUI(10.37M)与 Radix(12.39M,大量间接依赖);按 GitHub 增速与话题度是 **shadcn/ui**(2023 年发布即达 122k stars,是"复制粘贴式组件规范"路线的代表)。
3. **中国 B 端生态呈"一超多强"**:Ant Design(99.2k stars)一家独大,Element Plus、Arco Design、TDesign、Semi Design、Naive UI 构成活跃第二梯队,全部持续维护中(2026-08 均有近期发布)。
4. **共性趋势**:design token 化(所有头部系统)、Web Components 化(Material Web、Polaris 2025-10 转型)、无头原语化(Radix/shadcn)、暗色模式与 WCAG 无障碍成为标配、高密度模式成为 B 端系统标配(Carbon productive 模式、antd small 尺寸)。
5. **对 A 轨道最直接的可用结论**:能通过 CDN 直接引入浏览器(无构建链)的成熟规范是 **Ant Design、Element Plus、Arco、Semi、TDesign、Bootstrap、Salesforce SLDS、GOV.UK、USWDS、Material Web**;React 系(MUI/Chakra/Radix/shadcn)不适合直接引入单文件交付物,但其布局范式与组件规范是高价值视觉参照。

## 3. 接受度量化总表(2026-08-25 采集)

按 GitHub stars 降序。npm 列为周下载量。

| 设计规范 | 组织 | 首发年 | 当前版本 | GitHub stars | npm 周下载 | 许可证 | 最近推送 |
|---|---|---|---|---|---|---|---|
| Bootstrap | Twitter 起源/社区 | 2011 | 5.3.8 | 174,649 | 6,462,713 | MIT | 2026-08-24 |
| shadcn/ui | 社区(shadcn) | 2023 | 复制式分发,无主包 | 122,068 | 生态代理 64,794,507¹ | MIT | 2026-08-25 |
| Ant Design | 蚂蚁集团 | 2015 | antd 6.6.1(v6) | 99,182 | 3,765,959 | MIT | 2026-08-25 |
| Tailwind CSS | Tailwind Labs | 2017 | 4.3.3 | 97,329 | 126,443,545² | MIT | 2026-08-14 |
| MUI | MUI 团队(原 Material-UI) | 2014 | 9.3.1(v9) | 98,920 | 10,365,517 | MIT | 2026-08-25 |
| Chakra UI | 社区(Segun Adebayo) | 约2019 | 3.36.1(v3) | 40,594 | 1,755,968 | MIT | 2026-08-24 |
| Fluent UI | 微软 | 2017(Fluent 2 于 2023) | @fluentui/react-components 9.74.7 | 20,226 | 394,167 | NOASSERTION³ | 2026-08-25 |
| HeroUI | 社区(原 NextUI, 2021) | 2024 更名 | 3.2.4 | 30,458 | 516,707 | Apache-2.0 | 2026-08-22 |
| Element Plus | Element 团队(饿了么起源) | 2020(Element UI 2016) | 2.14.5 | 27,697 | 677,956 | MIT | 2026-08-24 |
| Radix UI Primitives | WorkOS 起源/社区 | 约2020 | 单调多包 | 19,208 | 12,391,015⁴ | MIT | 2026-08-08 |
| Naive UI | 社区(07akioni) | 约2020 | 2.45.2 | 18,508 | 177,584 | MIT | 2026-08-21 |
| Material Components Web | Google | 2016 | 已由 material-web 接棒 | 17,056 | —(冻结) | MIT | 2025-01-13 |
| React Spectrum(Spectrum 实现) | Adobe | 约2020(Spectrum 规范 2019) | 3.47.3 | 15,815 | 1,195,606⁵ | Apache-2.0 | 2026-08-25 |
| Material Web(@material/web) | Google | 约2020 | 2.5.0 | 11,197 | 134,690 | Apache-2.0 | 2026-08-21 |
| Semi Design | 字节跳动/抖音 | 2021 | 2.102.0 | 10,311 | 28,704 | NOASSERTION⁶ | 2026-08-21 |
| Carbon Design System | IBM | 约2016 | carbon-components-react 8.67.0 | 9,387 | 21,426 | Apache-2.0 | 2026-08-25 |
| USWDS | 美国总务署(GSA) | 2015 | 2.14.0 | 7,159 | 25,024 | NOASSERTION⁷ | 2026-08-24 |
| Polaris | Shopify | 2017 | 13.9.5(React 线已归档⁸) | 约 6,200(二手) | 269,175 | 见仓库 | 2026 归档 |
| Arco Design | 字节跳动 | 2021 | 2.66.16 | 5,673 | 59,840 | MIT | 2026-08-24 |
| Gestalt | Pinterest | 约2017 | 177.0.12 | 4,368 | 21,615 | Apache-2.0 | 2026-08-06 |
| TDesign | 腾讯 | 2021 | tdesign-vue-next 1.20.6 | 4,033(主仓) | 50,412 | MIT | 2026-08-19 |
| Primer React | GitHub | 约2019 | 38.36.0 | 3,892 | 57,345 | MIT | 2026-08-25 |
| Lightning Design System | Salesforce | 2015 | 2.264.0 | 3,700 | 77,140 | NOASSERTION⁹ | 2026-06-02 |
| GOV.UK Design System | 英国政府 GDS | 2018 | 6.4.0 | 1,442 | 292,891 | MIT | 2026-08-25 |

脚注:
1. shadcn/ui 无 npm 主包(组件代码复制进用户项目)。`class-variance-authority` 是其生态标志性依赖,64.8M/周可视为生态代理指标,含大量间接依赖。
2. `tailwindcss` 周下载含构建工具链与传递依赖,代表工具链渗透率而非站点数。
3. Fluent UI 仓库为 MIT(多包复合许可,API 归类失败)。
4. `radix-ui` 12.39M/周含海量间接依赖(大量组件库构建于其上),生态规模指标。
5. `@adobe/react-spectrum` 含 react-aria 生态联动,数字偏高。
6. Semi Design 实际为 MIT。
7. USWDS 为美国政府公共领域作品(CC0 风格声明,API 无法归类)。
8. **重要时点事实**:2025-10-01 Shopify 发布 Polaris Web Components 并推荐所有 Shopify App 采用;原 React 仓库于 2026 年归档为只读(`Shopify/polaris-react-archive`)。npm 上 `@shopify/polaris` 269k/周反映存量。
9. SLDS 许可证见仓库(自定义条款,代码与设计资产分别声明)。

**无 npm 主体的定性条目**:Apple Human Interface Guidelines(平台规范,不适用 stars/下载衡量)、SAP Fiori(当前主题 Horizon,SAPUI5 内置)、Atlassian Design System(闭源,`@atlaskit/*` 多包体系)。

## 4. 分组详述

### 4.1 全球事实标准(通用/跨平台)

**Material Design(Google,2014;现 Material 3 / M3 Expressive)**
- 定位:Google 全平台设计语言,Web/Android/Wear OS 统一。2025 年 Google I/O 发布 **Material 3 Expressive**(弹簧物理动效、更大胆形状与排版、鲜活色彩,基于 18,000+ 用户研究),2025 年底起在 Google 全系 App 推广,2026 年持续推进。
- 原则:Material as metaphor(材质隐喻)、自适应、颜色系统(dynamic color)、无障碍内建。
- 实现:`@material/web` 2.5.0(Web Components,134,690 周下载,可 CDN 直引);经典 `material-components-web` 已冻结(2025-01)。
- B 端适配:中。数据表格/表单能力强,但基因偏消费端;B 端气质弱于 Ant Design/Fluent/Carbon。

**Apple Human Interface Guidelines(1987 首版,持续在线更新)**
- 定位:iOS/macOS/visionOS 平台规范,接受度标杆(所有 App Store 生态的事实约束)。
- 对 Web 管理系统适配:低。列为"接受度"参照,不建议 A 轨道直接对标。

**Bootstrap(Twitter 起源,2011)**
- 定位:最老牌开源 CSS/UI 规范,响应式栅格事实标准。174.6k stars / 6.46M 周下载,十余年持续维护(5.3.8)。
- B 端适配:中。通用、稳定、CDN 直引零成本,但组件保真度与数据密度弱于现代 B 端系统;"Bootstrap 观感"在高端产品语境中反而显旧。

**MUI(2014,原 Material-UI)**
- 定位:React 生态最大的组件实现体,v9(9.3.1),10.37M 周下载。
- 原则:Material 规范的可定制实现 + `MUI Base` 无头线 + X Grid/X Charts 企业级付费扩展(数据网格能力对标企业后台)。
- B 端适配:高(通过 X Grid);但需 React 构建链,不能 CDN 直引进单文件 HTML。

### 4.2 企业软件系统系(B 端血统)

**Fluent 2 / Fluent UI(微软,Fluent 2017 / Fluent 2 2023)**
- 定位:微软全系(M365/Azure/Windows/Dynamics)企业软件设计语言;20.2k stars,394k 周下载。
- 原则:依赖 Metronome(一致的节奏感)、Faster than fast、模糊化上下文、内建无障碍(WCAG 2.1 AA 基线)。
- B 端适配:**高**。企业后台气质典范:密集表格、表单、命令栏、侧边导航。A 轨道"真实系统观感"的高价值参照(视觉范式可借鉴;React 实现不便直引,但存在 Web Components 版本)。

**Carbon(IBM,约2016)**
- 定位:IBM 全产品线设计系统,企业级标杆,9.4k stars。
- 原则:2x Grid 栅格、productive(高密度工作模式)/expressive(表达模式)**双密度体系**、完整 design token、WCAG AA 严格达标。
- B 端适配:**高**。其 productive 密度模式正是管理系统页面的形态;数据表格(Data Table)规范业界最完整之一。

**Salesforce Lightning Design System(2015)**
- 定位:CRM 界面规范,77k 周下载;纯 CSS 资产分发包,**可直引**。
- B 端适配:**高**(企业 CRM 形态:对象详情页、列表视图、向导)。

**SAP Fiori / Horizon(SAP,2013;当前主题 Horizon)**
- 定位:全球最大企业软件的 UI 规范。Horizon 主题 2022 GA(SAPUI5 1.102),Belize 2023 弃用,S/4HANA 2025 进一步精化色彩/间距/排版。晨昏双主题 + 高对比变体。
- B 端适配:**高**(企业 ERP 形态:launchpad、事实记录页、智能表格)。闭源生态,作视觉参照。

**Atlassian Design System**
- 定位:Jira/Confluence 全线规范,闭源多包(`@atlaskit/*`)。原则:直观、可信赖、团队协作语境。B 端适配:高(项目/工单/知识库三形态)。

**Polaris(Shopify,2017)**
- 定位:电商商家后台规范。**2025-10 起转向 Web Components**,框架无关(React/Vue/vanilla 皆可),React 版归档。B 端适配:高(商家后台:订单、商品、分析)。转型后社区对组件覆盖度有争议(二手来源)。

**Primer(GitHub,约2019 React 线)**
- 定位:开发者工具界面规范(仓库、PR、issue 列表形态)。B 端适配:中高(开发者平台后台)。

**Gestalt(Pinterest,约2017)**
- 定位:内部设计系统开源,21.6k 周下载。B 端适配:中(内容运营后台)。

**Spectrum / React Spectrum(Adobe,规范 2019 / 实现约2020)**
- 定位:Adobe 全系(PS/ XD/CC 界面)规范;React Spectrum 1.2M 周下载,以无障碍与国际化(react-aria)著称。B 端适配:中。

### 4.3 公共服务(政务)

**GOV.UK Design System(英国 GDS,2018)**
- 定位:政府服务标准,1.4k stars 但 **293k 周下载**(英国政府全站使用),MIT。
- 原则:服务设计先行、表单极度务实、WCAG 2.1 AA 强制、内容设计(文字即界面)。
- B 端适配:中高(表单密集型系统的可访问性范本,纯 CSS/JS 可直引)。

**USWDS(美国 GSA,2015)**
- 定位:美国联邦政府设计系统,25k 周下载,公共领域。B 端适配:中高(政务表单/信息发布)。

### 4.4 中国 B 端生态

**Ant Design(蚂蚁集团,2015;当前 v6)**
- 定位:**中国中后台事实标准**,也是全球接受度最高的 B 端设计系统——99.2k stars、3.77M 周下载、v6 持续演进(6.6.1,采集日当天仍有推送)。
- 原则:自然(基于自然规律的设计)、确定性、意义感、生长性;v5 起 CSS-in-JS + 完整 token 体系,v6 延续。
- B 端适配:**极高**。布局范式(Layout/Sider/ProComponents)、表格/表单密度、四套密度尺寸、暗色 token 完整。UMD/CDN 引入方式官方支持(v6 以官方文档为准)。

**Element Plus(Element 团队,2020;前身 Element UI 2016)**
- 定位:Vue 生态 B 端第二极,27.7k stars、678k 周下载。中后台适配:极高(表单/表格规范成熟,CDN 直引官方支持)。

**Arco Design(字节跳动,2021)** — 5.7k stars、60k 周下载;企业中后台+设计资产齐全,CDN 可用。
**TDesign(腾讯,2021)** — 主仓 4.0k stars(vue-next 子仓 2.2k)、50k 周下载;多框架实现(React/Vue/小程序),CDN 可用。
**Semi Design(抖音,2021)** — 10.3k stars、29k 周下载;特点:Design to Code(主题定制从 Figma 直达 token),CDN 可用。
**Naive UI(社区,约2020)** — 18.5k stars、178k 周下载;Vue 3 + TypeScript,可定制性强,口碑组件库。

共性:全部 MIT、全部活跃维护(2026-08 均有近期发布)、全部为中后台而生、全部支持暗色主题与设计 token。

### 4.5 现代组合式 / 无头原语

**Tailwind CSS(2017;v4)**
- 定位:原子化 CSS 工具,本身不是组件规范,但是当代 Web UI 的事实底座(126M 周下载为工具链渗透率)。生态:Tailwind UI(官方付费组件)、daisyUI 等。Play CDN 可浏览器直跑(官方注明不建议生产)。

**Radix UI Primitives(约2020)** — 无头(无样式)可访问组件原语,19.2k stars、12.4M 周下载(大量组件库建于其上);只管行为与无障碍,不管视觉。

**shadcn/ui(2023)**
- 定位:**"复制粘贴式组件规范"**——不发布 npm 包,把基于 Radix + Tailwind 的组件源码复制进用户项目,风格完全归用户。发布 3 年 122k stars,是接受度增速最高的项目;`class-variance-authority` 64.8M 周下载为其生态代理。
- 对 B 端:现代 SaaS 后台的主流路线(Vercel/Cal.com 等风格),需 React 构建链。

**Chakra UI(约2019;v3)** — 1.76M 周下载,可访问性内建、token 化彻底,React。
**HeroUI(原 NextUI,2021;2024 更名)** — 30.5k stars、517k 周下载,视觉现代感强,React。

## 5. 横向观察

1. **接受度与"血统"强相关**:下载量/stars 头部的系统几乎都背靠大平台(Ant/Google/微软/IBM/Twitter 系),但 2023 年后最快的增量来自 shadcn/ui 这种反发行模式(源码即分发)。
2. **Web Components 化是企业系统的新共识**:Material Web(2.5.0)、Polaris(2025-10)、Fluent/Carbon 均有 Web Components 线——动机正是框架无关与直接嵌入。
3. **双密度体系是 B 端规范分水岭**:Carbon(productive/expressive)、antd(大中小尺寸)、Fluent(密度 token)都把"高密度工作模式"作为一等公民;消费端规范(Material/HIG)则无此概念。A 轨道"数据密度真实"的验收标准与这一分水岭直接对应。
4. **GOV.UK 的启示**:stars 最低(1.4k)但下载量(293k/周)超过绝大多数商业开源系统——政务生态的强制采用使"接受度"与"社区热度"完全脱钩。评估成熟度时应区分"社区热度"与"装机采用"两类指标。
5. **无障碍已从加分项变基线**:头部系统全部声明 WCAG 2.1 AA(政府系强制、Carbon/Fluent/Spectrum 严格内建,React Aria 即为此生)。

## 6. 对 web-page-engineer Track A 的启示

1. **"真实系统观感"的参照系应显式化**:A 轨道生成管理系统页面时,最可信的观感来源是 Ant Design v6 / Fluent 2 / Carbon productive 三家的布局范式(侧边导航 + 顶栏 + 多标签 + 高密度表格表单)。建议视觉基准对齐其一,而不是泛化"好看的后台"。
2. **CDN 直引是硬约束**:A 轨道交付物为单文件 HTML(双击即开)。可直引候选:Ant Design、Element Plus、Arco、Semi、TDesign、Bootstrap、SLDS、GOV.UK、USWDS、Material Web;不可直引(仅作参照):MUI、Chakra、Radix/shadcn、HeroUI、Fluent React 线。
3. **密度规范可抄作业**:antd 的紧凑表格(行高、内边距、小尺寸控件)、Carbon 的 productive 密度参数、Fluent 的密度 token,可直接内化为 A 轨道 CSS 密度常量。
4. **暗色模式与 token**:国内六强(antd/Element/Arco/TDesign/Semi/Naive)全部原生暗色 + token 化;A 轨道若输出浅色为主,也应保持中性色阶可映射(token 命名对齐业界惯例)。
5. **shadcn/ui 路线对 Track B 的参考价值**:其"风格完全归项目"的理念适合 B 轨道(单页视觉设计)的组件审美,但技术路线(React 构建链)不适用;可借鉴其变体组织方式(CVA 的 variant/size 思维)用于 A 轨道自绘组件的 class 体系。

## 7. 来源清单

一手(2026-08-25 采集):
- GitHub REST API:`https://api.github.com/repos/{owner}/{repo}`(stars / pushed_at / license)
- npm Downloads API:`https://api.npmjs.org/downloads/point/last-week/{package}`
- npm Registry:`https://registry.npmjs.org/{package}/latest`(版本号)

官方文档(定性字段提炼来源):
- Material:https://m3.material.io/ · Fluent:https://fluent2.microsoft.design/ · Carbon:https://carbondesignsystem.com/ · SLDS:https://www.lightningdesignsystem.com/ · Polaris:https://polaris.shopify.com/ · Primer:https://primer.style/ · Spectrum:https://spectrum.adobe.com/ · GOV.UK:https://design-system.service.gov.uk/ · USWDS:https://designsystem.digital.gov/ · Atlassian:https://atlassian.design/ · Ant Design:https://ant.design/ · Element Plus:https://element-plus.org/ · Arco:https://arco.design/ · TDesign:https://tdesign.tencent.com/ · Semi:https://semi.design/ · Naive UI:https://www.naiveui.com/ · MUI:https://mui.com/ · Chakra:https://chakra-ui.com/ · Radix:https://www.radix-ui.com/ · shadcn/ui:https://ui.shadcn.com/ · Tailwind:https://tailwindcss.com/ · Bootstrap:https://getbootstrap.com/ · HeroUI:https://www.heroui.com/ · HIG:https://developer.apple.com/design/human-interface-guidelines/ · SAP Fiori:https://www.sap.com/design

二手(仅时点性事实,已在正文标注):
- Polaris 转型与归档:[Shopify/polaris-react-archive](https://github.com/Shopify/polaris-react-archive)、[Shopify 社区讨论](https://community.shopify.dev/t/is-anyone-else-disappointed-with-polaris-web-components-so-many-missing-features/23687)
- Material 3 Expressive:[官方发布说明](https://m3.material.io/blog/building-with-m3-expressive)、[Google Blog](https://blog.google/products-and-platforms/platforms/android/material-3-expressive-android-wearos-launch/)
- SAP Fiori Horizon:[SAP Community GA 公告](https://community.sap.com/t5/technology-blog-posts-by-sap/sap-fiori-evolution-horizon-now-generally-available-in-ui-technologies-and/ba-p/13532969)、[Belize 弃用公告](https://community.sap.com/t5/technology-blog-posts-by-sap/announcement-removal-of-belize-theme-of-sap-fiori/ba-p/14061924)
