# Security Skills

安全逆向与授权渗透测试。覆盖二进制逆向（IDA/.NET）、移动端逆向（Android/iOS）、前端 JS 逆向、APK 逆向与渗透测试工具链。全部 skill 内置授权门禁（ACTION REQUIRED 第一步即确认已授权场景），仅用于自有资产、书面授权、众测范围或 CTF 靶场。来自 [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill)（MIT）。

本组是从大型安全/逆向技能库中按实际工作流抽取的子集：`apk-reverse`、`mobile-reverse`、`ida-reverse`、`dotnet-reverse`、`js-reverse` 是逆向分析入口；`pentest-tools` 是主动渗透/SRC 众测入口。`pentest-tools/src-hunter/` 保持为嵌入资料库和子工作流，复用 `pentest-tools` 的 scope 契约、Evidence 记录和风险门禁，不作为独立注册 skill 暴露。

## Skills

| Skill | 用途 |
|---|---|
| [apk-reverse](./apk-reverse/) | Android APK 逆向：jadx/apktool 解包反编译、smali 修改重打包、Frida 动态 Hook，按需切换 so/native 分析（联动 ida-reverse） |
| [mobile-reverse](./mobile-reverse/) | 移动端逆向方法论（Android + iOS）：APK/IPA 分析、Frida/Objection 运行时注入、SSL Pinning 绕过、OWASP MSTG 平台保护检查 |
| [ida-reverse](./ida-reverse/) | IDA Pro 授权二进制逆向：PE/ELF/SO/DLL/Mach-O 反编译分析、漏洞研究、恶意样本/固件/native 代码分析；内置 start.ps1/open.ps1 脚本做确定性 server 管理与文件打开 |
| [dotnet-reverse](./dotnet-reverse/) | .NET/C# 逆向：dnSpyEx + de4dot 反编译托管程序，ConfuserEx/SmartAssembly 等脱壳，IL patch 优先于重编译；红队 Sharp* 工具与 info-stealer 样本分析 |
| [js-reverse](./js-reverse/) | 前端 JavaScript 逆向：签名/加密参数链路定位、AST 去混淆、本地补环境复现、运行时采样与证据化输出（js-reverse-mcp / jshookmcp） |
| [pentest-tools](./pentest-tools/) | 渗透测试工具链：侦察→枚举→验证流水线，scope 范围契约 + Evidence 降误报门禁；内嵌 `src-hunter/` 子技能（19 类攻击 playbook、305 结构化 payload、WAF 绕过变体、HackerOne/WooYun 真实案例统计） |

## 推荐搭配

- **Android APK 分析**：`apk-reverse`（解包/反编译/Hook）+ `ida-reverse`（so/native 层）
- **移动应用安全测试**：`mobile-reverse`（方法论 + iOS）+ `apk-reverse`（Android 工具链落地）
- **授权渗透 / SRC 众测**：`pentest-tools`（流水线 + src-hunter playbook），配合其 `templates/scope.md` 建范围契约
- **.NET 程序分析**：`dotnet-reverse`（托管层）+ `ida-reverse`（native/AOT 层）
- **Web 加密参数分析**：`js-reverse`（签名链路定位）+ frontend 组对应 skill 看页面实现

## 整组安装

```bash
npx skills@latest add yangpf5271/personal-skills --skill apk-reverse --skill mobile-reverse --skill ida-reverse --skill dotnet-reverse --skill js-reverse --skill pentest-tools
```
