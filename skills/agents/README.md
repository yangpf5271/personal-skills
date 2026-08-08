# Agent & Tooling Skills

智能体编排和开发工具：发现/创建 skill、浏览器自动化。围绕 agent 生态本身的工具型技能。

## Skills

| Skill | 用途 |
|---|---|
| [find-skills](./find-skills/) | 发现和安装 agent skill（Windows 兼容版，修复 Git Bash 空输出问题） |
| [skill-creator](./skill-creator/) | 创建/修改/优化 skill，跑 eval 评估 skill 触发准确性和性能 |
| [agent-browser](./agent-browser/) | 无头浏览器自动化 CLI：导航/点击/输入/截图/提取数据（Rust + Node 回退） |

## 推荐搭配

- **扩展 skill 库**：`find-skills`（搜现成的）→ `skill-creator`（自己造）
- **需要 agent 操作网页**：`agent-browser` 提供浏览器自动化能力

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill find-skills --skill skill-creator --skill agent-browser
```
