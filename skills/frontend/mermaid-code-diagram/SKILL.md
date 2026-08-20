---
name: mermaid-code-diagram
description: "代码生成 Mermaid 图：Generate architecture diagrams, ER diagrams, sequence diagrams, flowcharts, and class diagrams from codebases using Mermaid.js. Use when users ask to visualize code structure, draw architecture diagrams, create ER diagrams from database models, generate sequence diagrams from API flows, or produce any diagram from source code. Triggers on: 'draw architecture', 'generate diagram', 'visualize code', 'ER diagram', 'sequence diagram', 'class diagram', 'flowchart from code', 'module dependency graph'."
---

# Mermaid Code Diagram

Generate production-quality diagrams from source code via Mermaid.js. The Mermaid source itself is the primary deliverable — embed it in Markdown and it renders natively on GitHub/GitLab/VSCode. Syntax is verified by the bundled zero-dependency validation script; image files download on demand from the mermaid.ink render service. No Node.js, no Chromium, no `mmdc`.

## Environment

**No install required.** Syntax validation runs through the bundled script:

```bash
python scripts/validate_mermaid.py <file.md | diagram.mmd>   # exit 0 = valid
python scripts/validate_mermaid.py --code "flowchart TD
    A --> B"
```

Two layers, zero dependencies (Python only):
1. **Local pre-check** — 11 regex rules catching common errors, with a focus on CJK pitfalls (unquoted Chinese labels, Chinese subgraph names, unclosed subgraph, bracket/quote imbalance, list-syntax traps)
2. **Remote render check** — calls the mermaid.ink API for a real render; if the network is unreachable it degrades to local-pre-check-only and still passes (exit 0)

**Optional — standalone image export** (only when the user needs an SVG/PNG file for PPT/Word/IM). The validation script downloads the render from mermaid.ink directly — zero extra dependencies:

```bash
python scripts/validate_mermaid.py diagram.mmd --export          # PNG, auto-recommended width
python scripts/validate_mermaid.py diagram.mmd --export out/     # into a directory
python scripts/validate_mermaid.py diagram.mmd --export --svg    # SVG instead (vector, no width needed)
python scripts/validate_mermaid.py diagram.mmd --export --width 3000   # manual width
python scripts/validate_mermaid.py doc.md --export out/          # multi-block md → out/doc-1.png, doc-2.png…
```

PNG width defaults to **auto**: the script first fetches a default-viewport render, reads the diagram's natural width from the PNG header, then re-renders at `natural × 2` (clamped to 2400–4800; small diagrams scale ×3 gently instead of jumping to 2400).

Export requires network. When offline, ship the Mermaid source — the viewer (GitHub/VSCode/browser) renders it.

## Workflow

1. **Analyze** — Read the codebase to understand structure (`glob`, `grep`, `read`)
2. **Plan** — Decide diagram type(s) based on user request and code patterns
3. **Generate** — Write the Mermaid source (`.mmd` file or ` ```mermaid ` block in Markdown)
4. **Validate** — Run `python scripts/validate_mermaid.py <file>`; fix and re-run until exit 0
5. **Verify** — Confirm all code entities are represented and data flow directions are correct; when a rendered image was produced, read it back and check visually

## Diagram Type Selection

| User Intent | Diagram Type | Mermaid Keyword |
|-------------|-------------|-----------------|
| System overview, module layout | Architecture | `graph TD` + `subgraph` |
| Database tables, ORM models | ER Diagram | `erDiagram` |
| API flow, request lifecycle | Sequence Diagram | `sequenceDiagram` |
| Inheritance, interfaces | Class Diagram | `classDiagram` |
| Business logic, conditionals | Flowchart | `flowchart TD` |
| Task states, lifecycle | State Diagram | `stateDiagram-v2` |
| Import/dependency tree | Dependency Graph | `graph LR` |
| Timeline, project phases | Gantt Chart | `gantt` |

## Analysis Strategy

Do NOT read every file. Use progressive analysis:

**Step 1 — Detect the stack** — read the dependency manifest first (`pyproject.toml` / `package.json` / `pom.xml` / `go.mod` / `Cargo.toml` / `*.csproj` / `composer.json` / `Gemfile` / `mix.exs`); it identifies both the language and the framework (FastAPI vs Django, NestJS vs Express, Spring Boot vs plain). Then load [references/stack-anchor-map.md](references/stack-anchor-map.md) for that stack's anchors (entry / routes / data models / services / async / config), monorepo handling, and noise directories to exclude.

**Step 2 — Directory scan:** glob the main source dirs only, excluding `node_modules/` `venv/` `target/` `build/` `dist/` and friends, to understand module structure.

**Step 3 — Targeted reads by diagram type** (per-stack paths in the anchor map):
- **ER** → ORM models + migrations (migrations reveal the real schema better than models)
- **Architecture** → routes + service layer + config → service boundaries
- **Sequence** → one endpoint's full chain: handler → service → repository → external calls
- **Data flow** → four-anchor scan: sources (routes / MQ consumers / cron) → transforms (services) → sinks (ORM / Redis / object storage) → exports (third-party SDK calls); solid arrows for the main spine, dashed for read-backs and side exits
- **Class** → class definitions via `grep("class ")`

**Step 4 — GitHub repos:**
```bash
git clone --depth 1 <url> /tmp/repo-name
```
Then apply the same progressive scan.

## Optional: Standalone Image Export

Only when the user explicitly needs an image file (PPT / Word / IM / email). Otherwise skip — the Mermaid source embedded in Markdown is the deliverable. Export = `python scripts/validate_mermaid.py <file> --export [--svg]` (downloads the mermaid.ink render; PNG is 2x-sharp by default).

## Mermaid Syntax Reference

For detailed patterns and examples per diagram type, see [references/mermaid-patterns.md](references/mermaid-patterns.md).

Key rules:
- Short IDs, descriptive labels: `DB[("PostgreSQL 16")]`
- Use `subgraph` for logical grouping in architecture diagrams
- Limit ER diagrams to ~10 entities — split by domain if larger
- `participant` aliases in sequence diagrams for short names
- Quote labels with special chars: `A["Node (v1)"]`
- Max ~20 nodes per diagram — split into multiple if larger

## Output Conventions

**Pick the delivery form by destination:**

- Diagram lives in project docs (GitHub/GitLab/VSCode) → embed the Mermaid source directly in the Markdown as a ` ```mermaid ` fenced block — these render natively, need no `mmdc`, stay editable and diffable. This is the default.
- Standalone image needed (PPT / Word / IM / email) → download via `scripts/validate_mermaid.py --export` (optional, see below)
- Always keep the `.mmd` source alongside any rendered file — never ship images only

Other conventions:

- Write `.mmd` source + rendered files to workspace
- Descriptive names: `architecture.mmd`, `er-diagram.png`, `api-sequence.svg`
- Multiple diagrams → create `diagrams/` folder with index

## Quality Checklist

- All entities/modules from the code are represented
- Relationships and data flow directions are correct
- Labels readable, not truncated or overlapping
- No Mermaid syntax errors — `python scripts/validate_mermaid.py` exits 0 before delivery; syntax reference: [references/mermaid-patterns.md](references/mermaid-patterns.md)
- When a rendered image exists, visually verify it
