---
name: ccr-log-query
description: 查询 CCR 日志、ccr日志、Claude Code Router 日志、claude-code-router 日志、CCR 请求追踪、CCR trace、traceKey、运行日志、debug日志、上游请求响应、供应商响应、status_code、违反平台政策、image 生成失败等问题时必须使用本 Skill。通过 CCR HTTP API 查询 trace 列表、trace 详情和 Logs API，不要直接读 SQLite 或日志文件；适用于用户说“查一下 ccr 日志”“查询ccr日志”“看 CCR 请求日志”“看运行日志”“看debug日志”“按 traceKey 找请求”“看上游返回了什么”。
---

# ccr-log-query

## 适用场景

当需要查询 CCR 请求追踪日志或服务运行日志时使用本 Skill。查询通过 CCR HTTP API 完成，不直接读取 SQLite 文件或日志文件。

Trace 包含完整请求与响应，可能包含敏感 prompt、工具结果、文件内容和供应商响应。不要把查询结果发送到不可信位置。

## 环境变量

| 变量 | 说明 |
| --- | --- |
| `CCR_BASE_URL` | CCR 服务地址，默认 `http://127.0.0.1:3456` |
| `CCR_API_KEY` | 调用 CCR 代理服务使用的 key，也就是当前 Agent 调模型时使用的同一个代理 key。Claude、Codex 或其他客户端访问同一个 CCR 代理时使用的是同一类 key；通常由调用方从当前模型调用凭证、CCR 配置或当前会话环境解析后注入给脚本 |
| `PAGE` | 列表页码，默认 `1` |
| `PAGE_SIZE` | 每页数量，默认 `20` |
| `PROVIDER` | provider 过滤 |
| `MODEL` | model 过滤 |
| `PROTOCOL` | protocol 过滤 |
| `STATUS` | `success` 或 `fail` |

## 使用方法

脚本位于本 Skill 目录。执行命令前先切换到当前 Skill 目录。

优先按问题类型选择入口：

| 问题类型 | 查询入口 |
| --- | --- |
| 模型请求、协议转换、供应商响应、转换后响应、status_code、工具调用参数 | Trace API |
| 服务启动、路由器内部异常、插件错误、运行时 debug/info/warn/error 日志 | Logs API |

查询列表：

```powershell
node ./list-traces.mjs
```

查询详情：

```powershell
node ./get-trace.mjs <traceKey>
```

列表返回的 `traceKey` 是详情查询主键，格式类似 `traceKey-123`。排查时先查列表，再使用目标行的完整 `traceKey` 查询详情。

筛选示例：

```powershell
$env:PROVIDER = "米醋"
$env:MODEL = "gpt-5.5"
$env:PROTOCOL = "anthropic"
$env:STATUS = "success"
node ./list-traces.mjs
Remove-Item Env:PROVIDER, Env:MODEL, Env:PROTOCOL, Env:STATUS -ErrorAction SilentlyContinue
```

## 运行日志查询

CCR 已提供日志查看器和 Logs API。需要看服务运行日志时使用 Logs API，不要新建日志表，也不要直接读取日志文件。先列出日志文件，再使用返回的 `path` 读取目标日志。

列出日志文件：

```powershell
$config = Get-Content -LiteralPath "C:/Users/Administrator/.claude-code-router/config.json" -Raw | ConvertFrom-Json
$headers = @{ "X-API-Key" = $config.APIKEY }
$baseUrl = if ($env:CCR_BASE_URL) { $env:CCR_BASE_URL } else { "http://127.0.0.1:3456" }
Invoke-RestMethod -Uri "$baseUrl/api/logs/files" -Headers $headers
```

读取指定日志文件：

```powershell
$config = Get-Content -LiteralPath "C:/Users/Administrator/.claude-code-router/config.json" -Raw | ConvertFrom-Json
$headers = @{ "X-API-Key" = $config.APIKEY }
$baseUrl = if ($env:CCR_BASE_URL) { $env:CCR_BASE_URL } else { "http://127.0.0.1:3456" }
$file = "<logs/files 返回的 path>"
Invoke-RestMethod -Uri "$baseUrl/api/logs?file=$([uri]::EscapeDataString($file))" -Headers $headers
```

如果 `CCR_BASE_URL` 未设置，默认使用 `http://127.0.0.1:3456`。只读取 key 用于请求 header，不要打印 key。

## 认证解析规则

Trace 查询接口使用 CCR 代理服务现有认证机制，不需要额外的查询密钥。这里的 key 就是当前 Agent 调模型时使用的同一个 CCR 代理 key；Claude 和 Codex 接入 CCR 时也是同一类 key。调用方不要询问用户输入 APIKEY，应复用当前模型调用凭证；如果当前运行环境没有直接暴露该凭证，再从本机 CCR 配置或会话环境读取，并只作为环境变量注入脚本。

解析顺序：

| 顺序 | 来源 | 读取位置 |
| --- | --- | --- |
| 1 | 当前模型调用凭证 | 当前 Agent 调用模型时使用的 CCR 代理 key；如果运行环境可访问，直接复用它并注入为 `CCR_API_KEY` |
| 2 | 显式覆盖 | 当前进程环境变量 `CCR_API_KEY` |
| 3 | Claude Code 会话环境 | 当前进程环境里用于访问 CCR 代理的 `ANTHROPIC_AUTH_TOKEN`，它通常就是 Claude 调模型的同一个代理 key |
| 4 | Codex 普通 APIKEY 模式 | 当前认证上下文里用于访问 CCR 代理的 `OPENAI_API_KEY`，它通常就是 Codex 调模型的同一个代理 key |
| 5 | Codex ChatGPT 模式 | 当前认证上下文中的 `experimental_bearer_token`，如果这是当前模型调用凭证，调用方应注入为 `CCR_API_KEY` 后运行脚本 |
| 6 | CCR 本机配置 | `C:/Users/Administrator/.claude-code-router/config.json` 的顶层 `APIKEY` 字段，这是 CCR 代理服务自身的访问 key |

读取规则：只读取字段值用于请求 header 或注入 `CCR_API_KEY`，不要在终端或回复中打印 key。PowerShell 调用时可以在同一个命令作用域里设置临时环境变量，例如先从 `config.json` 读取顶层 `APIKEY`，再执行脚本：

```powershell
$config = Get-Content -LiteralPath "C:/Users/Administrator/.claude-code-router/config.json" -Raw | ConvertFrom-Json
$env:CCR_API_KEY = $config.APIKEY
node ./list-traces.mjs
Remove-Item Env:CCR_API_KEY
```

如果以上都没有，停止并说明无法确定 CCR 代理 key。不要猜测密钥，不要要求用户把密钥粘贴到对话中，不要把密钥输出到日志、终端、trace 结果或回答正文中。

读取到 key 后，请求 trace API 时设置任一 header：

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
