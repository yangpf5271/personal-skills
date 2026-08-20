# Frontend Skills（前端开发与设计）

前端开发全链路：从编码规范、设计系统到视觉制品、动效、质量检测。覆盖"写出规范的前端代码 + 做出好看的界面 + 验证质量"。

## Skills

| Skill | 用途 |
|---|---|
| [react-frontend-guide](./react-frontend-guide/) | React/TypeScript 前端开发规范（Suspense/MUI v7/TanStack Router） |
| [web-quality](./web-quality/) | Web 质量检测：Lighthouse 性能 + WCAG 2.2 可访问性 + SEO 一体化审计 |
| [ui-ux-pro-max](./ui-ux-pro-max/) | UI/UX 设计智能系统（84 风格/192 调色板/9 技术栈），规划/构建/审查 UI 代码 |
| [web-design-engineer](./web-design-engineer/) | 顶级 Web 设计工程师，产出 HTML/CSS/JS/React 视觉制品（页面/落地页/仪表板/原型） |
| [motion](./motion/) | React 动画库 Motion（原 Framer Motion）：手势/滚动/弹簧/布局动画 |
| [canvas-design](./canvas-design/) | 创作静态视觉艺术（.png/.pdf 海报、设计稿），强调原创不抄袭 |
| [figma](./figma/) | Figma 设计转代码：拉取设计上下文/截图/变量，转成生产代码 |
| [mermaid-code-diagram](./mermaid-code-diagram/) | 分析代码库生成 Mermaid 图（架构/ER/时序/流程/类图），.mmd 可编辑、GitHub 原生渲染，零依赖校验脚本 + 远程导出图片 |

## 推荐搭配

- **做完整 Web 项目**：`react-frontend-guide`（写代码）+ `web-design-engineer`（做视觉制品）+ `motion`（加动效）+ `web-quality`（测性能/a11y）
- **设计转代码**：`figma`（拉设计）→ `ui-ux-pro-max`（按设计系统生成）→ `react-frontend-guide`（规范代码）
- **画技术图**：`mermaid-code-diagram`（从代码分析出图，.mmd 可编辑可 diff，适合文档/PR）
- **做海报/平面**：单独用 `canvas-design`

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill react-frontend-guide --skill web-quality --skill ui-ux-pro-max --skill web-design-engineer --skill motion --skill canvas-design --skill figma --skill mermaid-code-diagram
```
