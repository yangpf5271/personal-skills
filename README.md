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

- [`hello`](./skills/hello/SKILL.md) — a minimal example skill. Copy its folder to start your own.

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

1. Copy `skills/hello/` to `skills/<your-skill-name>/`.
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
