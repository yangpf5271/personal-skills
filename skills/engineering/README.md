# Software Engineering Skills

软件工程能力：架构设计、安全扫描、MCP 构建、任务规划。开发过程中"怎么做对、做稳、做得有规划"的支持。

## Skills

| Skill | 用途 |
|---|---|
| [architecture-designer](./architecture-designer/) | 系统架构设计/ADR 顾问：分布式系统、云架构、技术选型、可扩展性规划 |
| [code-security](./code-security/) | 代码安全扫描：Semgrep 检测漏洞/密钥泄露/OWASP Top 10（含完整 rules/） |
| [mcp-builder](./mcp-builder/) | 构建 MCP 服务器：让 LLM 通过工具与外部服务交互（Python FastMCP / Node TS） |
| [planning-with-files](./planning-with-files/) | 文件式任务规划（Manus 风格）：task_plan/findings/progress，支持 /clear 后会话恢复 |

## 推荐搭配

- **新项目启动**：`planning-with-files`（拆任务+跟踪）→ `architecture-designer`（定架构+写 ADR）
- **开发中护航**：`code-security`（扫描漏洞）+ `planning-with-files`（跟踪进度）
- **搭工具生态**：`mcp-builder` 给 agent 加自定义工具

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill architecture-designer --skill code-security --skill mcp-builder --skill planning-with-files
```
