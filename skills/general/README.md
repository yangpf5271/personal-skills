# General Skills（通用工程与工具）

语言无关的软件工程能力和开发工具：架构与 API 设计、安全扫描、数据库、Git 工作流、性能优化、MCP 构建、任务规划，以及 skill 发现/创建和浏览器自动化。

## Skills

| Skill | 用途 |
|---|---|
| [architecture-designer](./architecture-designer/) | 系统架构设计/ADR 顾问：分布式系统、云架构、技术选型、可扩展性规划（语言无关，前后端通吃） |
| [api-and-interface-design](./api-and-interface-design/) | API 与接口设计：REST/GraphQL 端点、模块边界、类型契约，设计难以误用的稳定接口 |
| [code-security](./code-security/) | 代码安全扫描：Semgrep 检测漏洞/密钥泄露/OWASP Top 10（含完整 rules/） |
| [computer-science-algorithms](./computer-science-algorithms/) | 算法与数据结构最佳实践：51 条规则、9 大类（复杂度/数据结构/排序搜索/DP/图论/分治/贪心/字符串/概率算法） |
| [database-architecture](./database-architecture/) | PostgreSQL 18 数据库架构：UUIDv7 主键、时态约束、虚拟生成列、零停机迁移、索引策略（部分/表达式/JSONB GIN） |
| [git-workflow-and-versioning](./git-workflow-and-versioning/) | Git 工作流与版本管理：提交规范、分支策略、冲突处理、语义化版本/tag/changelog 发布流程 |
| [performance-optimization](./performance-optimization/) | 性能优化方法论：先测量后优化，覆盖前端 Core Web Vitals、后端、N+1 查询、数据库瓶颈定位 |
| [verification-before-completion](./verification-before-completion/) | 完成前验证门禁：声称"完成/修好/通过"之前必须先跑验证命令并确认输出，证据先于断言 |
| [radical-simplification](./radical-simplification/) | 激进简化认知工具箱：9 把认知刀（重述/澄清/缩减/分解/倒推/约束/迁移/泛化/审计），把复杂问题变简单 |
| [theory-of-constraints](./theory-of-constraints/) | 约束理论瓶颈定位：测量→找唯一瓶颈→榨干→加资源→重复，自带诊断脚本和决策树 |
| [mcp-builder](./mcp-builder/) | 构建 MCP 服务器：让 LLM 通过工具与外部服务交互（Python FastMCP / Node TS） |
| [planning-with-files](./planning-with-files/) | 文件式任务规划（Manus 风格）：task_plan/findings/progress，支持 /clear 后会话恢复 |
| [find-skills](./find-skills/) | 发现和安装 agent skill（Windows 兼容版，修复 Git Bash 空输出问题） |
| [skill-creator](./skill-creator/) | 创建/修改/优化 skill，跑 eval 评估 skill 触发准确性和性能 |
| [gh](./gh/) | GitHub CLI（gh）调用模式：--json/--jq 结构化输出、分页防截断、search vs list、gh api 回退（官方出品） |
| [agent-browser](./agent-browser/) | 无头浏览器自动化 CLI：导航/点击/输入/截图/提取数据（Rust + Node 回退） |

## 推荐搭配

- **新项目启动**：`planning-with-files`（拆任务+跟踪）→ `architecture-designer`（定架构+写 ADR）
- **设计新 API**：`api-and-interface-design`（稳定接口契约）+ `architecture-designer`（系统级边界）
- **开发中护航**：`code-security`（扫描漏洞）+ `planning-with-files`（跟踪进度）
- **提交/发布前把关**：`verification-before-completion`（先跑验证再声称完成）+ `git-workflow-and-versioning`（规范提交/版本号/changelog）
- **性能问题排查**：`performance-optimization`（先测量后优化）+ `database-architecture`（查询/索引层面）
- **算法选型/性能评审**：`computer-science-algorithms`（51 条规则，避免 O(n²) 等常见陷阱）
- **数据库设计**：`database-architecture`（PostgreSQL 18 schema/索引/迁移/查询优化）+ `architecture-designer`（系统级数据层架构）
- **复杂问题简化**：`radical-simplification`（9 把认知刀，换角度把复杂度塌缩）
- **流程/流水线优化**：`theory-of-constraints`（定位唯一瓶颈，别在非瓶颈上浪费时间）
- **搭工具生态**：`find-skills`（找现成 skill）→ `skill-creator`（自己造）→ `mcp-builder`（给 agent 加自定义工具）
- **需要 agent 操作网页**：`agent-browser` 提供浏览器自动化能力

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill architecture-designer --skill api-and-interface-design --skill code-security --skill computer-science-algorithms --skill database-architecture --skill git-workflow-and-versioning --skill performance-optimization --skill verification-before-completion --skill radical-simplification --skill theory-of-constraints --skill mcp-builder --skill planning-with-files --skill find-skills --skill skill-creator --skill gh --skill agent-browser
```
