---
name: tencent-code-cli
description: |
  操作腾讯工蜂（code.tencent.com / git.code.tencent.com）代码托管平台的 CLI 工具 tcode。
  封装工蜂 REST API（/api/v3，GitLab v3 兼容），覆盖项目、仓库、分支、Tag、提交、合并请求（MR）、
  代码评审、缺陷单、标签、里程碑、Webhook、版本发布等全部端点。当用户提到工蜂、tcode、
  git.code.tencent.com，或要在工蜂上做任何平台操作（查/建项目、看 MR diff、创建 MR、管缺陷、
  操作分支、配 webhook、代码评审等）时使用。
---

# tcode — 腾讯工蜂 CLI

封装腾讯工蜂 REST API 的命令行工具，覆盖官方 Rest Api 板块全部 5 个一级分组、22 个子分组。供 AI agent 操作工蜂平台（建项目、看 MR、管缺陷等）时使用，免去手动跑网页。

## 职责边界（重要）

**tcode 操作工蜂平台（经 REST API），git 操作代码本身（经 Git 协议），两者凭证与职责不重叠：**

- **tcode**：建项目/项目组、MR/缺陷/分支/Tag 管理、看 diff、保护分支、webhook、代码评审、查提交历史等 —— 用 API token（`PRIVATE-TOKEN`/`OAUTH-TOKEN` header）
- **git**：clone / push / pull / commit —— 用 SSH key 或工蜂 Git 密码，是另一套凭证

用户要 push/clone 代码时，引导用 `git` 命令（tcode 不走 Git 协议）。

## 前置条件

1. **tcode 已安装**（`pip install -e .` 或全局安装），终端能运行 `tcode --help`
2. **已配置 token**（二选一，见下「获取 token」）

> 若未配置 token，命令返回退出码 3（配置/参数错误）。`tcode --help` / `tcode auth login` 无需 token。

## 操作前先检查登录状态

**执行任何业务命令前，先跑 `tcode auth status` 判断是否已登录**，避免每个命令都失败在认证上：

```bash
tcode auth status
# 退出码 0 = 已登录（输出"已登录：<用户名>"），可继续操作
# 退出码 1 = 未登录或 token 失效 → 引导用户 tcode auth login
```

`auth status` 会真实调 `GET /user` 验证 token 有效性（不只是看配置文件有没有 token），
能检测出 token 被撤销/过期。区分两种未登录原因：
- "未配置 token" → 用户从未登录，引导 `tcode auth login`
- "token 已失效" → 之前登过但 token 失效，引导重新 `tcode auth login`

## 获取 token（两种方式）

### 方式 A：OAuth 登录（推荐，免手动复制）

需用户先在工蜂「个人设置 → 管理应用」创建一个 OAuth 应用，拿到 client_id / client_secret，
回调地址配 `http://localhost:8888/auth`。然后：

```bash
# 用环境变量传凭证（避免留在命令历史）
export TCODE_OAUTH_CLIENT_ID="<应用ID>"
export TCODE_OAUTH_CLIENT_SECRET="<应用秘钥>"
tcode auth login
```

流程：自动打开用户默认浏览器 → 用户在工蜂授权 → 回调 localhost:8888 → 自动拿 token 写入配置。

### 方式 B：手动设置 Private Token

用户在 `git.code.tencent.com/profile/account` 生成私有访问令牌，然后：

```bash
tcode config set-token                # 交互输入（推荐）
# 或
export TENCENT_CODE_ACCESS_TOKEN="..."  # 临时（当前会话）
```

## 配置

```bash
tcode config init          # 交互式初始化
tcode config set-token     # 设置 token
tcode config show          # 查看当前配置（token 脱敏）
```

配置优先级：CLI 参数 > 环境变量（`TENCENT_CODE_ACCESS_TOKEN`）> `~/.tcode/config.toml` > 默认值。

## 退出码与错误排查（判断命令结果）

agent 通过退出码 `$?` 判断命令成败，无需解析输出：

| 退出码 | 常见现象 | 原因 | 处理 |
|--------|----------|------|------|
| **0** | 列表为空 | 项目内无该资源，或筛选条件过严 | 去掉 `--state` 等过滤再看 |
| **1** | 401 Unauthorized | token 错误/过期 | `tcode auth login`（OAuth）或 `tcode config set-token` 重设 |
| **2** | 404 Not Found | 资源不存在，**或账号无项目权限**（工蜂用 404 防撞库） | 确认 id/iid 和权限 |
| **3** | 未找到 API token | 本地未配置 token，或参数缺失 | `tcode auth login` 或 `config set-token`；补全必需参数 |
| **4** | 405 / OAuth 换 token 失败 / 其余 4xx·5xx | 资源不支持该方法（如 issue 无 DELETE）；或 code 过期 / client_secret 错 / 回调地址不匹配 | 换用正确命令（如 `issue close`）；OAuth 检查秘钥与回调配置；读 stderr |

```bash
tcode mr list 123; case $? in 0);; 1) auth login;; 2) 确认 id/权限;; esac
```

## 核心命令速查

### 项目与仓库
```bash
tcode project list --membership              # 我参与的项目
tcode project get <id|ns/proj>               # 项目详情（支持数字 id 或 路径）
tcode repo file tree <id> --ref main         # 目录树
tcode repo file get <id> --path README.md    # 读文件（Base64 自动解码）
tcode repo file blob <id> --sha main --path src/app.py  # 按 commit+path 取原始内容
tcode repo raw-blob <id> <blob_sha> [-o out.bin]        # 按 blob sha 取原始内容
tcode repo compare <id> --from feat --to main         # 差异对比
```

### 分支与 Tag
```bash
tcode branch list <id>                       # 分支列表
tcode branch create <id> --name feat/x --ref main
tcode branch protect <id> main --push-level 40        # 保护分支（--merge-level/--developers-can-push/--developers-can-merge）
tcode branch show-protect <id> main          # 查看保护规则详情（含 approver_rule 等）
tcode branch member add <id> --branch main --user-id 5 --access-level 30  # 保护分支成员（工蜂特有）
tcode branch lifecycle <id> [--branch main] [--tag v1.0]  # 分支生命周期审计（工蜂特有，可过滤）
tcode tag list <id> && tcode tag create <id> --name v1.0 --ref main
```

### 合并请求 MR（重点）
```bash
tcode mr list <id>                           # MR 列表
tcode mr get <id> <mr_id>                    # MR 详情
tcode mr diff <id> <mr_id>                   # 文件级 diff
tcode mr create <id> --source feat --target main --title "新功能" \
    --reviewers 1,2 --approver-rule 2        # 工蜂特有：评审人 + 评审规则
tcode mr merge <id> <mr_id>                  # 合并
tcode mr note add <id> <mr_id> --body "LGTM" --reviewer-state approved  # 行级评审
```

### 代码评审（工蜂特有）
```bash
tcode review invite <id> <mr_id> --reviewer-id 5
tcode review summary <id> <mr_id> --event approve --summary "代码质量良好"
tcode review cancel <id> <mr_id>
```

### 缺陷单 Issue
```bash
tcode issue list --project <id> --state opened
tcode issue create <id> --title "Bug" --grade 8 --assignee-ids 1,2  # 工蜂特有：权重/多处理人
tcode issue update <id> <issue_id> --labels "bug,p0" --assignee-ids 1,2 \
    --grade 5 --resolve-state resolved       # 改已存在 issue（labels/assignee 为整体替换）
tcode issue close <id> <issue_id>            # 关闭（无 DELETE，用 state_event=close）
```

### 提交
```bash
tcode commit list <id> --branch main --since 2026-07-01   # 提交历史（写日报用）
tcode commit diff <id> <sha> [--path src/x] [--ignore-white-space]  # 提交差异
tcode commit refs <id> <sha>                 # 提交对应的分支/Tag
```

### 里程碑 / 标签 / Hook
```bash
tcode milestone list <id> [--state active] [--order-by due_date] [--sort asc]  # 过滤排序
tcode milestone issues <id> <mid>            # 里程碑下的缺陷
tcode milestone update <id> <mid> --state-event active   # 激活（close 关闭；activate 为兼容写法）
tcode label create <id> --name bug --color '#fc2929'
tcode hook add <id> --url U --push-events --merge-requests-events \
    --issues-events --tag-push-events --note-events --review-events --token T  # 全事件 flag
tcode hook update <id> <hook_id> --merge-requests-events --token T2           # 同款 flag
```

### 版本发布 / 提交检测（CI）
```bash
tcode release create <id> --tag v1.0 --start-point main [--title 备注] [--type release] [--desc 描述]
tcode release update <id> <release_id> --description "新描述"   # 仅 description 可改
tcode release list <id> && tcode fork create <id>
tcode status create <id> --sha <sha> --state success --block   # state: pending/success/error/failure
#   （也接受 running/failed/canceled 别名，自动映射到上述取值）
```

### 用户 / 关注 / 命名空间
```bash
tcode user whoami                           # 当前用户
tcode user find-by-email --email a@b.com    # 邮箱反查用户（工蜂特有）
tcode user key get <key_id> && tcode user email get <email_id>  # 单查密钥/邮箱
tcode watch on <id> --mute                  # 关注项目（静音通知）
tcode watch watchers <id>                   # 项目的关注人列表
tcode group list && tcode namespace list
```

## 输出格式

```bash
tcode --format table project list    # 表格（默认，人看）
tcode --format json project list     # JSON（脚本管道用）
tcode --format raw project list      # 原始 JSON（调试用）
tcode --page 2 --per-page 50 ...     # 分页（per_page 最大 100）
```

## 工蜂路径怪异点（调试时须知）

tcode 已正确处理，但理解这些有助于排查 404：
- **MR 单个操作用单数** `/merge_request/:id`，列表用复数 `/merge_requests`
- **Fork 路径在前**：`POST /projects/fork/:id`
- **编辑项目组无 :id**（body 传 id）
- **标签 DELETE 靠 body** 传 name
- **缺陷无 DELETE**：关闭用 `PUT` + `state_event=close`（`issue delete` 不存在）
- **Watch 用 PUT/DELETE**（非 POST）

## 技术细节

- **API Base URL**：`https://git.code.tencent.com/api/v3`（`http://` 自动重定向 https）
- **认证**：Private token 用 `PRIVATE-TOKEN` header；OAuth access_token 用 `OAUTH-TOKEN` header（由 `config.token_type` 决定，二者不混用）
- **路径编码**：`ns/proj` 自动编码为 `ns%2Fproj`，可直接当 `:id` 用
- **分页**：自动翻页聚合，响应头 `X-Total` 等
- **文件内容**：Base64 自动解码

## 参考文档

- 设计与实现：项目内 `docs/tencent-code-design.md`
- API 调研与端点清单：`docs/tencent-code-api-research.md`
- 官方原文存档：`docs/api-raw/`（22 份文档，含 README 与使用前必读）
