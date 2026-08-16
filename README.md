# personal-skills

A personal collection of agent skills, distributed via [skills.sh](https://skills.sh) and installable on any coding agent (Claude Code, Codex, ZCode, …).

## Install

```bash
npx skills@latest add yangpf5271/personal-skills
```

Pick the skills you want and which coding agents to install them on. The installer writes each skill as ordinary, editable files you own — nothing updates behind your back. Pull the latest when you want it:

```bash
npx skills@latest update
```

## What's here

A curated set of 39 skills grouped by function into 6 categories. Plus 8 optional `creative-video` skills available as "Other" during install. Each group has its own `README.md` with skill list, recommended combos, and a one-line group-install command. Browse [`skills/`](./skills/) or jump to a group:

| Group | What it covers | Skills | README |
| --- | --- | --- | --- |
| 🎨 `frontend` | 前端编码规范、设计系统、视觉制品、动效、质量检测 | 8 | [skills/frontend/README.md](./skills/frontend/README.md) |
| 🐍 `python` | Python 现代工具链与编码规范 | 2 | [skills/python/README.md](./skills/python/README.md) |
| 🔧 `general` | 架构设计、代码安全、数据库、MCP、任务规划、skill 工具、浏览器自动化、算法、方法论 | 11 | [skills/general/README.md](./skills/general/README.md) |
| 🛡️ `security` | 逆向分析（APK/移动端/IDA/.NET/JS）与授权渗透测试工具链 | 6 | [skills/security/README.md](./skills/security/README.md) |
| 📄 `docs` | 文档生成（Word/PDF/PPT/Excel）+ 写作、研究、标书、文字润色 | 9 | [skills/docs/README.md](./skills/docs/README.md) |
| ✏️ `mine` | 我的原创（多 agent 编排、日志查询、工蜂 CLI） | 3 | [skills/mine/README.md](./skills/mine/README.md) |

> 🎬 **创意视频制作**（8 skills）：未加入主分组，安装时在 "Other" 中可选。详见 [`skills/creative-video/README.md`](./skills/creative-video/README.md)。

### Skill sources

Each skill is tracked to its upstream where known. Skills with no listed source are original or untraceable.

| Group | Skill | Upstream source | Notes |
| --- | --- | --- | --- |
| frontend | canvas-design | [anthropics/skills](https://github.com/anthropics/skills) | |
| frontend | figma | — | Source untraceable (Apache 2.0) |
| frontend | fireworks-tech-graph | [yizhiyanhua-ai/fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) | |
| frontend | motion | — | Upstream [jezweb/claude-skills](https://github.com/jezweb/claude-skills) removed it; local copy kept as orphan |
| frontend | react-frontend-guide | [mrgoonie/claudekit-skills](https://github.com/mrgoonie/claudekit-skills) | Upstream dir is `frontend-development`; renamed locally |
| frontend | ui-ux-pro-max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | |
| frontend | web-design-engineer | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) | 上游已重写为新一代；本地谱系：上游旧版 + 工蜂 fork 的架构优先流程演进 + 离线资源/中文定制 + 选择性吸收新版方法论（critique/failure-patterns/design-calibration/browser-acceptance） |
| frontend | web-quality | [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills) | Upstream skill `web-quality-audit`; renamed locally |
| python | modern-python | [trailofbits/skills](https://github.com/trailofbits/skills) | uv + ruff + ty + pytest toolchain |
| python | python-best-practices | [nathan-gage/python-skills](https://github.com/nathan-gage/python-skills) | 70 rules / 8 categories from real PR review patterns |
| general | agent-browser | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | `hidden: true` removed locally so it stays visible |
| general | architecture-designer | [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | |
| general | code-security | [semgrep/skills](https://github.com/semgrep/skills) | Includes full `rules/` directory |
| general | computer-science-algorithms | [community-skills](https://github.com/anthropics/community-skills) | 51 rules / 9 categories; CLRS + cp-algorithms distillation |
| general | database-architecture | — | PostgreSQL 18: UUIDv7, temporal constraints, zero-downtime migration, indexing |
| general | radical-simplification | [pproenca/dot-skills](https://github.com/pproenca/dot-skills) | 9 cognitive moves for collapsing complexity |
| general | theory-of-constraints | [pproenca/dot-skills](https://github.com/pproenca/dot-skills) | Goldratt ToC: find → exploit → subordinate → elevate → repeat |
| general | find-skills | [KimYx0207/findskill](https://github.com/KimYx0207/findskill) | Windows-compat fork of [vercel-labs/skills](https://github.com/vercel-labs/skills); kept to avoid the Git Bash empty-output bug |
| general | mcp-builder | [anthropics/skills](https://github.com/anthropics/skills) | |
| general | planning-with-files | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | |
| general | skill-creator | [anthropics/skills](https://github.com/anthropics/skills) | |
| security | apk-reverse | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | Android APK 逆向：jadx/apktool/Frida |
| security | mobile-reverse | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | Android+iOS 统一方法论；description 已中文化 |
| security | ida-reverse | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | IDA Pro 二进制逆向，含 start.ps1/open.ps1 |
| security | dotnet-reverse | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | dnSpyEx + de4dot，.NET 混淆脱壳与 IL patch |
| security | js-reverse | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | JS 逆向：签名定位/AST 去混淆/补环境 |
| security | pentest-tools | [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | 内嵌 src-hunter 子技能（[MyuriKanao/src-hunter-skill](https://github.com/MyuriKanao/src-hunter-skill)） |
| docs | content-research-writer | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | |
| docs | docx | [anthropics/skills](https://github.com/anthropics/skills) | |
| docs | humanizer-zh | [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) | |
| docs | office | — | Source untraceable (distributed via OpenClaw) |
| docs | pdf | [anthropics/skills](https://github.com/anthropics/skills) | |
| docs | pptx | [anthropics/skills](https://github.com/anthropics/skills) | |
| docs | xlsx | [anthropics/skills](https://github.com/anthropics/skills) | |
| docs | hv-analysis | [khazix/hv-analysis](https://github.com/khazix/hv-analysis) | 横纵分析法：纵轴生命历程 + 横轴竞品对比 → PDF 研究报告 |
| docs | tender-bid-writer | — | Original (self-authored); 招标需求+大纲 → 技术标 .docx |
| mine | agent-teams-playbook | — | Original (self-authored) |
| mine | ccr-log-query | — | Original (self-authored) |
| mine | tencent-code-cli | — | Original (self-authored) |

> 🎬 creative-video 组（8 skills，不注册在主分组）：hyperframes、hyperframes-cli、hyperframes-media、motion-design、video-spec-builder、video-agency-roles、gsap、storyboard-script。来源 [HeyGen/hyperframes](https://github.com/heygen-com/hyperframes)（除 video-spec-builder、video-agency-roles、storyboard-script 为本地自建；前二者以 video-spec.md §0-§9 为契约咬合——builder 生成、roles 审查）。安装时在 "Other" 中可选。

## Repository layout

```
personal-skills/
├── .claude-plugin/
│   └── plugin.json          ← manifest: lists every installable skill path (nested)
├── skills/
│   ├── frontend/            ← group folder
│   │   ├── README.md        ← group description (GitHub auto-renders; not installed)
│   │   ├── react-frontend-guide/SKILL.md
│   │   └── ...
│   ├── python/
│   ├── general/
│   ├── security/
│   ├── docs/
│   ├── mine/
│   └── creative-video/       ← "Other" group (not in plugin.json, optional install)
└── README.md                ← human-facing (not packaged into installs)
```

The install unit is **each `<skill>/` directory** (the one containing a `SKILL.md`). Group folders and their `README.md` are organizational only — they are never installed. The installer flattens skills on install (e.g. `skills/frontend/ui-ux-pro-max` installs as `~/.claude/skills/ui-ux-pro-max/`), so group choice is for repo navigation, not for the installed layout.

## Add your own skill

1. Pick the right group folder under `skills/<group>/` (create the folder if it's a new group).
2. Create `skills/<group>/<your-skill-name>/` with a `SKILL.md` (use any existing skill folder as a reference for the frontmatter shape).
3. Edit `SKILL.md`: set `name` (the command), write a `description`, decide on `disable-model-invocation`, and write the body.
4. Add `"./skills/<group>/<your-skill-name>"` to the `skills` array in `.claude-plugin/plugin.json` to register it in a group. Skills not in `plugin.json` are still installable — they appear under "Other" during install.
5. If it's a new group, add a `skills/<group>/README.md` describing the group.
6. Commit and push. `npx skills@latest add yangpf5271/personal-skills` picks it up.

## Skill authoring quick reference

- **`name`** — the slash command (`/your-skill`).
- **`description`** — one-line summary. For user-invoked skills it's human-facing; for model-invoked skills it carries trigger phrasing the agent matches on.
- **`disable-model-invocation: true`** — user-invoked only (zero context load, you must remember to type it). Omit it to let the agent (and other skills) reach the skill autonomously.
- **Self-contained** — any file the skill needs at runtime must live in its folder. Don't depend on repo-level paths.
- **Sibling files** — templates, reference docs, scripts alongside `SKILL.md` install with the skill.

## License

MIT
