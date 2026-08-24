# Workflow 编排流程（确定性流水线范式）

> ⚠️ **平台专属**：本文档仅在编排范式决策判定走 Workflow 分支且当前会话有 Workflow 工具时读取；其他平台（ZCode、Codex）暂无等价能力，读者无需关注本文档内容。本文档描述的 Workflow 范式依赖 Claude Code 2.1.154+ 的 `Workflow` 工具、`/workflows` 命令和 `/effort ultracode` 触发词。经"编排范式决策"检查到当前会话无 Workflow 工具时，跳过此分支，所有任务走 Agent Teams 范式。

> 本文档是 agent-teams-playbook 的 reference。经"编排范式决策"判定走 Workflow 范式，且用户已 opt-in（ultracode 或关键词）时读取本文件。

Workflow 用确定性脚本编排大规模子代理，后台执行，适合控制流可预先写死的任务。

## 流程

1. **触发确认**：确认 ultracode 已开 或 prompt 已含 workflow 意图；缺失则提示用户 opt-in，不静默调用
2. **脚本设计**：确定 fan-out 结构 + 质量模式
3. **编写并提交**：用 `Workflow` 工具提交 JS 脚本（脚本自动持久化，可迭代）
4. **后台执行**：`/workflows` 观察进度，完成自动通知
5. **结果汇总**：读取脚本 return 值，按阶段5格式输出报告
6. **清理**：worktree 隔离产物、脚本文件

## 脚本编写要点

| Hook | 用途 |
|------|------|
| `pipeline(items, stage1, ...)` | **默认**多阶段，item 独立流过无屏障，wall-clock 最优 |
| `parallel(thunks)` | 屏障等全部完成（仅当真需全部结果：去重/合并/早退时用） |
| `agent(prompt, {schema})` | spawn 子代理，schema 强制结构化输出 |
| `phase()` / `log()` | 进度分组与播报 |
| `budget.total/spent()/remaining()` | budget 感知，控制自适应扩展 |

> **默认 pipeline，慎用 parallel**：parallel 是屏障会浪费空闲 slot；仅去重/合并/早退判断需全部前序结果时才用 barrier。

## 质量模式选择

| 任务要求 | 模式 |
|---------|------|
| 高置信度（审查/验证） | adversarial verify：N 个 skeptic 投票，多数 refute 则杀 |
| 多失败维度 | perspective-diverse verify：每 verifier 不同 lens |
| 解空间宽（方案设计） | judge panel：N 独立尝试 + 评分 + 综合 |
| 未知规模发现（找bug/边界） | loop-until-dry：连续 K 轮无新发现才停 |
| 兜底 | completeness critic：收尾问"漏了什么" |

## 用户可见性

脚本启动前展示 fan-out 结构和质量模式经用户确认；`/workflows` 实时观察；完成通知后输出结构化报告。

## 与 Agent Teams 的复合（A+D 范式）

Agent Teams 阶段3 遇大规模可并行子块时，协调器可 spawn 一个 Workflow 批量处理：
- Agent Teams 负责：整体协调、用户交互、动态决策
- Workflow 负责：子块的确定性批量执行（迁移、审查、生成）
- 子块产出落盘后，协调器纳入阶段4 质量把关
