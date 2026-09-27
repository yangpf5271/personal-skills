# Security Skills

安全逆向与授权渗透测试。覆盖二进制逆向（IDA/.NET）、移动端逆向（Android/iOS）、前端 JS 逆向、APK 逆向与渗透测试工具链。全部 skill 内置授权门禁（ACTION REQUIRED 第一步即确认已授权场景），仅用于自有资产、书面授权、众测范围或 CTF 靶场。来自 [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill)（MIT）。

本组是从大型安全/逆向技能库中按实际工作流抽取的子集：`apk-reverse`、`mobile-reverse`、`ida-reverse`、`dotnet-reverse`、`js-reverse` 是逆向分析入口，`reverse-engineering` 是通用二进制逆向总纲（内嵌 `dsl-vm-reverse` 子技能，随本组一同注册）；`pentest-tools` 是主动渗透/SRC 众测入口，`api-security`、`llm-security`、`supply-chain-security`、`firmware-pentest` 是专项评估入口。`pentest-tools/src-hunter/` 保持为嵌入资料库和子工作流，复用 `pentest-tools` 的 scope 契约、Evidence 记录和风险门禁，不作为独立注册 skill 暴露。

## Skills

| Skill | 用途 |
|---|---|
| [apk-reverse](./apk-reverse/) | Android APK 逆向：jadx/apktool 解包反编译、smali 修改重打包、Frida 动态 Hook，按需切换 so/native 分析（联动 ida-reverse） |
| [mobile-reverse](./mobile-reverse/) | 移动端逆向方法论（Android + iOS）：APK/IPA 分析、Frida/Objection 运行时注入、SSL Pinning 绕过、OWASP MSTG 平台保护检查 |
| [ida-reverse](./ida-reverse/) | IDA Pro 授权二进制逆向：PE/ELF/SO/DLL/Mach-O 反编译分析、漏洞研究、恶意样本/固件/native 代码分析；内置 start/open 脚本组 + MCP supervisor 保活体系（watchdog 巡检、recover 强制恢复、登录自启动、死锁自愈，ida-pro-mcp 2.x） |
| [dotnet-reverse](./dotnet-reverse/) | .NET/C# 逆向：dnSpyEx + de4dot 反编译托管程序，ConfuserEx/SmartAssembly 等脱壳，IL patch 优先于重编译；红队 Sharp* 工具与 info-stealer 样本分析 |
| [js-reverse](./js-reverse/) | 前端 JavaScript 逆向：签名/加密参数链路定位、AST 去混淆、本地补环境复现、运行时采样与证据化输出（js-reverse-mcp / jshookmcp） |
| [reverse-engineering](./reverse-engineering/) | 通用二进制逆向总纲：非 PE 格式/WASM/固件/自定义 VM、OLLVM 去混淆、Go/Rust/IL2CPP、内核驱动、CTF 逆向题型菜谱；内嵌 `dsl-vm-reverse/`（JS 自定义 VM/风控引擎逆向） |
| [firmware-pentest](./firmware-pentest/) | 固件/IoT 渗透链：binwalk/unblob 提取、EMBA 自动化分析、Firmadyne/QEMU 仿真、AFL++ 模糊测试到利用 |
| [pentest-tools](./pentest-tools/) | 渗透测试工具链：侦察→枚举→验证流水线，scope 范围契约 + Evidence 降误报门禁；内嵌 `src-hunter/` 子技能（19 类攻击 playbook、305 结构化 payload、WAF 绕过变体、HackerOne/WooYun 真实案例统计） |
| [api-security](./api-security/) | API 安全评估：REST/GraphQL/WebSocket/SOAP 发现、JWT/OAuth 认证授权测试、限流绕过、CI/CD 集成测试 |
| [llm-security](./llm-security/) | LLM 应用与 AI Agent 安全评估：prompt injection、工具滥用、RAG/记忆投毒、模型供应链风险、Agent 服从性工程（OWASP LLM Top 10 v2.0 + Agentic AI Top 10） |
| [supply-chain-security](./supply-chain-security/) | 软件供应链安全评估：SBOM、SCA、CI/CD 流水线、容器镜像、构建完整性、依赖溯源与漏洞可达性 |

## 推荐搭配

- **Android APK 分析**：`apk-reverse`（解包/反编译/Hook）+ `ida-reverse`（so/native 层）
- **移动应用安全测试**：`mobile-reverse`（方法论 + iOS）+ `apk-reverse`（Android 工具链落地）
- **授权渗透 / SRC 众测**：`pentest-tools`（流水线 + src-hunter playbook），配合其 `templates/scope.md` 建范围契约
- **.NET 程序分析**：`dotnet-reverse`（托管层）+ `ida-reverse`（native/AOT 层）
- **Web 加密参数分析**：`js-reverse`（签名链路定位）+ frontend 组对应 skill 看页面实现
- **自定义 VM / 风控引擎逆向**：`js-reverse`（JS 侧采样）+ `reverse-engineering`（内嵌 dsl-vm-reverse 子技能）
- **API 专项测试**：`api-security`（JWT/OAuth/GraphQL 专项）+ `pentest-tools`（工具链与流水线）
- **LLM 应用 / Agent 安全评估**：`llm-security`（提示注入/工具滥用/RAG 投毒）
- **供应链与 CI/CD 自检**：`supply-chain-security`（SBOM/SCA/构建完整性）
- **IoT 固件分析**：`firmware-pentest`（提取→仿真→利用）+ `reverse-engineering`（native 层）

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill apk-reverse --skill mobile-reverse --skill ida-reverse --skill dotnet-reverse --skill js-reverse --skill reverse-engineering --skill firmware-pentest --skill api-security --skill llm-security --skill supply-chain-security --skill pentest-tools
```
