---
name: mcr-log-query
description: 查询 MCR 日志、mcr日志、mcr-router 日志、MCR 请求追踪、MCR trace、traceKey、运行日志、debug日志、上游请求响应、供应商响应、status_code、违反平台政策、image 生成失败等问题时必须使用本 Skill。通过 MCR HTTP API 查询 trace 列表、trace 详情和 Logs API，不要直接读 SQLite 或日志文件；适用于用户说“查一下 mcr 日志”“查询mcr日志”“看 MCR 请求日志”“看运行日志”“看debug日志”“按 traceKey 找请求”“看上游返回了什么”。
---

# mcr-log-query

## 适用场景

当需要查询 MCR 请求追踪日志或服务运行日志时使用本 Skill。查询通过 MCR HTTP API 完成，不直接读取 SQLite 文件或日志文件。

Trace 包含完整请求与响应，可能包含敏感 prompt、工具结果、文件内容和供应商响应。不要把查询结果发送到不可信位置。

## 安装与同步

本 Skill 是仓库内源文件（`docs/skills/mcr-log-query/`）。全局使用时把整个目录同步到 `~/.zcode/skills/mcr-log-query/`、`~/.agents/skills/mcr-log-query/`、`~/.claude/skills/mcr-log-query/`。

## 环境变量

| 变量 | 说明 |
| --- | --- |
| `MCR_BASE_URL` | MCR 服务地址，默认 `http://127.0.0.1:3456` |
| `MCR_API_KEY` | 调用 MCR 代理服务使用的 key，也就是当前 Agent 调模型时使用的同一个代理 key。Claude、Codex 或其他客户端访问同一个 MCR 代理时使用的是同一类 key；通常由调用方从当前模型调用凭证、MCR 配置或当前会话环境解析后注入给脚本 |
| `MCR_CONFIG_PATH` | 覆盖本机配置文件路径，默认 `~/.mcr-router/config.json` |
| `PAGE` | 列表页码，默认 `1` |
| `PAGE_SIZE` | 每页数量，默认 `20` |
| `PROVIDER` | provider 过滤 |
| `MODEL` | model 过滤 |
| `PROTOCOL` | protocol 过滤 |
| `STATUS` | `success` 或 `fail` |

## 使用方法

脚本位于本 Skill 目录，无第三方依赖。执行命令前先切换到当前 Skill 目录。

优先按问题类型选择入口：

| 问题类型 | 查询入口 |
| --- | --- |
| 模型请求、协议转换、供应商响应、转换后响应、status_code、工具调用参数 | Trace API（`list-traces.mjs` / `get-trace.mjs`） |
| 服务启动、路由器内部异常、插件错误、运行时 debug/info/warn/error 日志 | Logs API（`logs.mjs`） |

查询 trace 列表：

```powershell
node ./list-traces.mjs
```

查询 trace 详情：

```powershell
node ./get-trace.mjs <traceKey>
```

列表返回的 `traceKey` 是详情查询主键，格式类似 `traceKey-123`。排查时先查列表，再使用目标行的完整 `traceKey` 查询详情。详情可能很大，建议重定向到临时文件后用脚本摘取关键字段，分析完删除临时文件。

筛选示例（PowerShell）：

```powershell
$env:PROVIDER = "米醋"
$env:MODEL = "gpt-5.5"
$env:PROTOCOL = "anthropic"
$env:STATUS = "success"
node ./list-traces.mjs
Remove-Item Env:PROVIDER, Env:MODEL, Env:PROTOCOL, Env:STATUS -ErrorAction SilentlyContinue
```

bash 等价写法：

```bash
PROVIDER=米醋 MODEL=gpt-5.5 STATUS=success PAGE_SIZE=20 node ./list-traces.mjs
```

## 运行日志查询

MCR 已提供日志查看器和 Logs API。需要看服务运行日志时使用 Logs API，不要新建日志表，也不要直接读取日志文件。

列出日志文件：

```powershell
node ./logs.mjs
```

读取指定日志文件（`path` 来自上一步返回的完整路径）：

```powershell
node ./logs.mjs "<logs 文件列表返回的 path>"
```

## 认证解析规则

三个脚本内置了相同的 key 解析逻辑，按以下顺序取第一个非空值，调用方通常只需要注入 `MCR_API_KEY`，其余情况直接运行脚本即可：

| 顺序 | 来源 | 说明 |
| --- | --- | --- |
| 1 | 环境变量 `MCR_API_KEY` | 当前 Agent 调模型时使用的同一个 MCR 代理 key，由调用方显式注入 |
| 2 | 环境变量 `ANTHROPIC_AUTH_TOKEN` | Claude Code 会话环境，通常就是 Claude 调模型的同一个代理 key |
| 3 | 环境变量 `OPENAI_API_KEY` | Codex 普通 APIKEY 模式，通常就是 Codex 调模型的同一个代理 key |
| 4 | 本机配置文件顶层 `APIKEY` 字段 | 按 `MCR_CONFIG_PATH` → `~/.mcr-router/config.json` 顺序探测 |

Codex ChatGPT 模式没有上述环境变量时，调用方应把当前认证上下文中的 `experimental_bearer_token` 注入为 `MCR_API_KEY` 后运行脚本。

调用方不要询问用户输入 APIKEY，不要猜测密钥，不要要求用户把密钥粘贴到对话中，不要把密钥输出到日志、终端、trace 结果或回答正文中。只读取字段值用于请求 header 或注入 `MCR_API_KEY`。

如果以上都没有，停止并说明无法确定 MCR 代理 key。

读取到 key 后，请求 API 时设置任一 header：

```text
X-API-Key: <APIKEY>
Authorization: Bearer <APIKEY>
```

## API

Trace 列表接口：

```text
GET /api/traces
```

Trace 详情接口：

```text
GET /api/trace/:traceKey
```

详情返回 4 个 trace 数据点：

| 字段 | 说明 |
| --- | --- |
| `originalRequest` | 原始请求 |
| `transformedRequest` | 转换后发送给供应商的请求 |
| `providerResponse` | 供应商原始响应 |
| `transformedResponse` | 转换后返回给客户端的响应 |

Logs 文件列表接口：

```text
GET /api/logs/files
```

Logs 内容接口：

```text
GET /api/logs?file=<path>
```

`file` 使用 `/api/logs/files` 返回的完整 `path`。
