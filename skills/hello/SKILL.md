---
name: hello
description: 示例 skill：A minimal example skill. Replace this with your own — copy this folder, change name/description, write the body. Invoke by typing /hello.
disable-model-invocation: true
---

# Hello

This is a minimal **user-invoked** skill. It exists as a template: copy this folder, rename it, and write your own `SKILL.md` to turn it into a real skill.

## What this example does

It greets the user by name if known, and explains the parts of a skill so you can see the shape.

## How a skill is structured

- The **frontmatter** (between `---` lines above) is required. `name` is the command (`/hello`); `description` is a one-line summary shown to humans when `disable-model-invocation: true` is set.
- The **body** is plain markdown the agent reads when the skill runs. Write the process in order; each step should end on a condition that tells the agent when it's done.
- A skill folder can hold **sibling files** (templates, reference docs, scripts) alongside `SKILL.md` — they install with the skill. Files outside the skill folder (like a repo-level `docs/`) do **not** install, so keep a skill self-contained.

## Process

1. Greet the user. If a name is available in context, use it; otherwise ask.
2. Point them at this file as the template to copy for their next skill.

## Guardrails

- This is user-invoked (`disable-model-invocation: true`): the agent will not fire it on its own — only when you type `/hello`.
- To make a skill the agent reaches autonomously, remove `disable-model-invocation` and write a trigger-rich `description` ("Use when the user wants…, mentions…").
