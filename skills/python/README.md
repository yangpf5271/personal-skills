# Python Skills

Python 开发：现代工具链、编码规范、项目脚手架。目前是地基性质的两个 skill，后续可按需扩展框架（FastAPI/Django）和数据分析（pandas）方向。

## Skills

| Skill | 用途 |
|---|---|
| [modern-python](./modern-python/) | Python 现代工具链：uv + ruff + ty + pytest 工具链配置与编码 best practices（trailofbits 出品，2026 事实标准） |
| [python-best-practices](./python-best-practices/) | Python 软件工程最佳实践：70 条规则、8 大类（数据建模/错误处理/类型安全/API 设计/简化/性能/命名/导入），来自真实 PR 评审模式 |

## 推荐搭配

- **新 Python 项目启动**：`modern-python`（定工具链+规范）+ 通用组的 `architecture-designer`（定系统架构/ADR）
- **写/审/重构代码**：`python-best-practices`（70 条规则按 impact 分级）+ `modern-python`（工具链）
- **开发中护航**：`modern-python`（规范）+ 通用组的 `code-security`（安全扫描）

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill modern-python --skill python-best-practices
```
