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

A curated set of 21 skills — browser automation, design, document creation (docx/pdf/pptx/xlsx), React frontend guidelines, MCP building, research/writing, file-based planning, and more. Browse [`skills/`](./skills/) for the full list; each folder is one self-contained skill.

### Skill sources

Each skill is tracked to its upstream where known. Skills with no listed source are original or untraceable.

| Skill | Upstream source | Notes |
| --- | --- | --- |
| agent-browser | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | `hidden: true` removed locally so it stays visible |
| agent-teams-playbook | — | Original (self-authored) |
| architecture-designer | [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | |
| canvas-design | [anthropics/skills](https://github.com/anthropics/skills) | |
| ccr-log-query | — | Original (self-authored) |
| code-security | [semgrep/skills](https://github.com/semgrep/skills) | Includes full `rules/` directory |
| content-research-writer | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | |
| docx | [anthropics/skills](https://github.com/anthropics/skills) | |
| figma | — | Source untraceable (Apache 2.0) |
| find-skills | [KimYx0207/findskill](https://github.com/KimYx0207/findskill) | Windows-compat fork of [vercel-labs/skills](https://github.com/vercel-labs/skills); kept to avoid the Git Bash empty-output bug |
| mcp-builder | [anthropics/skills](https://github.com/anthropics/skills) | |
| motion | — | Upstream [jezweb/claude-skills](https://github.com/jezweb/claude-skills) removed it; local copy kept as orphan |
| office | — | Source untraceable (distributed via OpenClaw) |
| pdf | [anthropics/skills](https://github.com/anthropics/skills) | |
| planning-with-files | [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | |
| pptx | [anthropics/skills](https://github.com/anthropics/skills) | |
| react-frontend-guide | [mrgoonie/claudekit-skills](https://github.com/mrgoonie/claudekit-skills) | Upstream dir is `frontend-development`; renamed locally for clarity |
| skill-creator | [anthropics/skills](https://github.com/anthropics/skills) | |
| ui-ux-pro-max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | |
| web-design-engineer | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) | Customized locally; not synced from upstream |
| xlsx | [anthropics/skills](https://github.com/anthropics/skills) | |

## Repository layout

```
personal-skills/
├── .claude-plugin/
│   └── plugin.json          ← manifest: lists every installable skill path
├── skills/
│   └── <skill-name>/
│       └── SKILL.md         ← frontmatter (name/description) + body
└── README.md                ← human-facing (not packaged into installs)
```

The install unit is **each `skills/<name>/` directory**. Only `SKILL.md` and its sibling files in that folder are installed. Repo-level docs, this README, and config files are **not** packaged — so keep every skill self-contained.

## Add your own skill

1. Create `skills/<your-skill-name>/` with a `SKILL.md` (use any existing skill folder as a reference for the frontmatter shape).
2. Edit `SKILL.md`: set `name` (the command), write a `description`, decide on `disable-model-invocation`, and write the body.
3. Add `"./skills/<your-skill-name>"` to the `skills` array in `.claude-plugin/plugin.json`.
4. Commit and push. `npx skills@latest add yangpf5271/personal-skills` picks it up.

## Skill authoring quick reference

- **`name`** — the slash command (`/your-skill`).
- **`description`** — one-line summary. For user-invoked skills it's human-facing; for model-invoked skills it carries trigger phrasing the agent matches on.
- **`disable-model-invocation: true`** — user-invoked only (zero context load, you must remember to type it). Omit it to let the agent (and other skills) reach the skill autonomously.
- **Self-contained** — any file the skill needs at runtime must live in its folder. Don't depend on repo-level paths.
- **Sibling files** — templates, reference docs, scripts alongside `SKILL.md` install with the skill.

## License

MIT
