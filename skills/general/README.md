# General Skills（通用工程与工具）

语言无关的软件工程能力和开发工具：架构设计、安全扫描、MCP 构建、任务规划，以及 skill 发现/创建和浏览器自动化。

## Skills

| Skill | 用途 |
|---|---|
| [architecture-designer](./architecture-designer/) | 系统架构设计/ADR 顾问：分布式系统、云架构、技术选型、可扩展性规划（语言无关，前后端通吃） |
| [code-security](./code-security/) | 代码安全扫描：Semgrep 检测漏洞/密钥泄露/OWASP Top 10（含完整 rules/） |
| [computer-science-algorithms](./computer-science-algorithms/) | 算法与数据结构最佳实践：51 条规则、9 大类（复杂度/数据结构/排序搜索/DP/图论/分治/贪心/字符串/概率算法） |
| [mcp-builder](./mcp-builder/) | 构建 MCP 服务器：让 LLM 通过工具与外部服务交互（Python FastMCP / Node TS） |
| [planning-with-files](./planning-with-files/) | 文件式任务规划（Manus 风格）：task_plan/findings/progress，支持 /clear 后会话恢复 |
| [find-skills](./find-skills/) | 发现和安装 agent skill（Windows 兼容版，修复 Git Bash 空输出问题） |
| [skill-creator](./skill-creator/) | 创建/修改/优化 skill，跑 eval 评估 skill 触发准确性和性能 |
| [agent-browser](./agent-browser/) | 无头浏览器自动化 CLI：导航/点击/输入/截图/提取数据（Rust + Node 回退） |

## 推荐搭配

- **新项目启动**：`planning-with-files`（拆任务+跟踪）→ `architecture-designer`（定架构+写 ADR）
- **开发中护航**：`code-security`（扫描漏洞）+ `planning-with-files`（跟踪进度）
- **算法选型/性能评审**：`computer-science-algorithms`（51 条规则，避免 O(n²) 等常见陷阱）
- **搭工具生态**：`find-skills`（找现成 skill）→ `skill-creator`（自己造）→ `mcp-builder`（给 agent 加自定义工具）
- **需要 agent 操作网页**：`agent-browser` 提供浏览器自动化能力

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill architecture-designer --skill code-security --skill computer-science-algorithms --skill mcp-builder --skill planning-with-files --skill find-skills --skill skill-creator --skill agent-browser
```
