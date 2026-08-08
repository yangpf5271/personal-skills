# Mine Skills（我的原创）

作者自研的技能，不来自任何上游，针对个人工作流定制。

## Skills

| Skill | 用途 |
|---|---|
| [agent-teams-playbook](./agent-teams-playbook/) | 多代理/子代理协作编排手册：决定何时拆分任务、分配子 agent、收集结果 |
| [ccr-log-query](./ccr-log-query/) | 查询 Claude Code Router 日志：trace 列表/详情、请求追踪、上游响应（通过 CCR HTTP API） |

## 说明

这两个技能是为作者的个人工作流定制的，不强求通用性。如果你也用 Claude Code Router 或做多 agent 编排，可以参考或直接安装。

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill agent-teams-playbook --skill ccr-log-query
```
