---
name: web-page-engineer
description: |
  Build high-quality visual Web artifacts using HTML/CSS/JavaScript/React — web pages, landing pages, dashboards, interactive prototypes, HTML slide decks, animated demos, UI mockups, data visualizations, and management-system (admin) UI pages.
  Use this skill whenever the user's request involves a visual, interactive, or front-end deliverable, including:
  - Creating web pages, landing pages, dashboards, marketing pages
  - Building interactive prototypes or UI mockups (with device frames)
  - Implementing system designs that contain business processes — roles, states, transitions, approval flows — as management-system UI pages (flow logic as an internal control layer)
  - Turning design mockups, screenshots, or PRDs into interactive implementations
  - Data visualization (Chart.js / D3, etc.)
  - Building HTML slide decks / presentations
  - Design system / UI Kit exploration
  Even if the user doesn't explicitly say "HTML" or "web page," this skill applies whenever the intent is to produce something visual, interactive, or presentational.
  Not applicable: pure back-end logic, CLI tools, data-processing scripts, non-visual code tasks, command-line debugging.
---

# Web Page Engineer

This skill positions the Agent as a top-tier design engineer producing HTML artifacts. The design unit differs per task: a **page** (one visual artifact) or a **system** (screens × roles × states × transitions). The question decides the shape — never push every task through one pipeline.

The quality bar is branch-conditional:

- **Visual exploration** (landing pages, concepts, decks): the bar is *stunning* — bold proportion, whitespace rhythm, type-scale contrast, memorable moments.
- **Business systems** (Track A): the bar is *flow fidelity and per-screen task fit* — restrained, dense, task-first. The craft shows as alignment, state coverage, keyboard flow, and data-ink, not decoration.

## Scope

✅ Applicable: visual front-end deliverables — pages, prototypes, business-system prototypes, dashboards, visualizations, UI mockups, design systems

❌ Not applicable: back-end APIs, CLI tools, data-processing scripts, non-visual logic, performance tuning

## Rule Priority

1. **User-provided context wins**: existing codebase, brand, screenshots, data, and explicit constraints override generic style advice.
2. **Artifact purpose wins over showcase ambition**: rebuilds, patches, and system implementations stay faithful and restrained; explorations can push.
3. **System consistency wins over anti-cliché rules**: don't fight a real design system just because it uses familiar patterns.
4. **Offline portability wins over convenience**: no remote dependencies unless explicitly requested.
5. **References are scaffolds, not rules**: adapt their placeholders to the declared design system.

---

## Step 0: Triage — pick track and lane

| Input signal | Route | User stops |
|---|---|---|
| System design / PRD containing business flows, states, or multiple roles | **Track A** | 1 |
| Single page or visual task; intent sufficient; or user says "直接做 / fast / you decide" | Track B · fast lane | 0 |
| Exploratory single page with open style (e.g. "design a photography showcase site") | Track B · standard lane | 0–1 |
| UI screenshot / existing codebase / brand guide provided | Track B · context lane | 0 |

Boundary rule: a lightweight system (≤3 screens, trivial states) may run Track A in light mode or Track B — state which and why.

Laws of elasticity:

- **Internalize, don't skip.** Every lane still declares a design system and runs the full checklist; only the waiting differs. Steps are cheap; round-trips are expensive.
- **Declare assumptions.** Any decision made without the user ships with the artifact as a stated, overridable assumption.
- **Only one stop is sacred** — the "wrong understanding = full rework" confirmation. Track A: the flow model. Track B standard lane: the direction. Everything else merges into artifact-first delivery.
- **The pre-delivery checklist is never skipped** in any lane.

---

## Track A: Business System Design

**Deliverable: management-system pages.** The artifact must read as a real admin system — realistic data density, state-conditioned UI, in-memory mock backend. The business flow never appears as UI: it lives in a pure state machine that *controls* the pages (which actions are enabled, how views vary by state). Validation apparatus (state panels, walkthrough tabs, free-play consoles) belongs to the process, not the artifact; the only demo affordance is a collapsible scenario panel (A4).

The system layer models the business; the page layer still does full page design. Neither swallows the other.

### A1 · Model the system — one confirmation round

Ingest the system design / PRD / flow diagrams and produce, before any styling:

- **Flow model**: roles; business states; transitions including branches and exceptions (reject, revoke, timeout, delegation); guarded or illegal actions.
- **Screen inventory**: one line per screen — `role × task × states visible on that screen`.
- **Scenario list**: at minimum the happy path, one tricky edge case, and one attempt at an action that should be blocked.

Deliver the flow model **plus the pilot screens v0 in the same message** — one round of feedback corrects both the flow understanding and the design direction. Use domain language throughout: labels read like the business, not the code.

### A2 · Declare the design system once

One system-wide declaration; every screen inherits: density, type scale, table/form specs, **status-color semantics** (which colors mean pending / approved / rejected / disabled), nav structure, spacing, radius, shadows, motion. If an existing product UI or brand exists, extract its tokens and extend — never invent a competing system.

### A3 · Page layer — mandatory, tiered depth

- **Pilot screens (2–3)**: the screens carrying the most complex tasks. Design them fully in v0 — task analysis, layout pattern, component choice, information hierarchy, all of that screen's business states, polish. They are the benchmark for the whole system.
- **Standard screens** (plain lists, simple forms, simple detail): during build, run each through `task → layout → component → states`, using [references/components.md](references/components.md) as the operating manual. Craft here = density, alignment, empty/loading/error states, keyboard flow.
- **Anti-isomorphism law**: every screen's layout is decided by that screen's task. All screens sharing one skeleton is a design failure — redo the outliers.

Admin conventions distilled from mature systems (Carbon, Ant Design):

- **One primary action per screen** (per action area in a max-permission union view). Secondary buttons only alongside a primary (as Cancel/Back); destructive actions get a distinct danger style and always a text label — never icon-only.
- **Button labels are verb(+noun)** ("提交审批", "驳回"), never lone nouns or vague "确定"; casing consistent system-wide.
- **Row actions: ≤3 inline, the rest into an overflow menu**; bulk workflows add a checkbox column and a batch-action bar (select-all with an indeterminate state).
- **Lock the trigger during an action** — a loading button is disabled (no double submits); skeletons for list loading.
- **Forms validate on a deliberate trigger** (blur or debounced input, not every keystroke); errors render below the control; a failed submit scrolls to the first error.

### A4 · Assemble

Build order: **seed data → pure state machine → shared shell → pilot screens → remaining screens by state → scenario panel**.

- Seed data with realistic density: believable records in realistic volume (tables with a dozen+ rows, full fields), consistent across screens, at least one record per business state, one known initial state per scenario. In-memory only; never fabricated statistics.
- All transition logic lives in one **pure state machine module** — no DOM inside it; the page calls into it, nothing flows back. The machine is an **internal controller**, never rendered as UI: it answers "what is legal right now" and the pages obey. A validated machine is liftable into the real codebase later. Patterns and skeleton: [references/flow-driven-ui.md](references/flow-driven-ui.md).
- **State-gated actions**: illegal-in-current-state actions render disabled with a reason tooltip ("打款仅在审批通过后可用"); terminal records disable the whole action area with a terminal note.
- **Max-permission view**: every screen in the nav, every action area rendered (union of roles). Only when the design explicitly requires showing permission differences: add a role-perspective toggle inside the scenario panel — never in the system UI.
- Shared shell: nav + layout shared by every screen; every screen rendered per record state, not just the happy path. **The shell fills the viewport and never scrolls** — on list screens the toolbar stays pinned and the list region scrolls independently with a sticky table header; non-list screens may scroll their content column inside the shell; mobile is exempt (natural page scroll). Pattern and the `min-height: 0` gotcha: [references/flow-driven-ui.md](references/flow-driven-ui.md).
- **Scenario panel** — the only demo chrome: a draggable floating ball (bottom-right by default, visually distinct from the system UI) opening a panel with a scenario list (one click resets seed data to that scenario's initial state and navigates to the relevant screen) and a record-state overview. Variant tweaks, if any, live in the same panel. Fully hidden when closed.

### A5 · Verify and close

Run the full pre-delivery checklist (visual block + Track A block). Then deliver a **closing summary**: what the build covered, which branches remain uncovered, which assumptions shipped.

---

## Track B: Single Page / Visual

### B1 · Understand (ask only when needed)

| Scenario | Ask? |
|---|---|
| No PRD, no audience ("make a deck", "design onboarding for my app") | ✅ heavily |
| PRD + audience + duration given | ❌ start building |
| Screenshot → prototype | ⚠️ only if interactions are unclear |
| Existing codebase → rebuild/extend | ❌ read the code directly |

Probe as needed: product context, output type, variation dimensions, constraints.

### B2 · Gather design context (by priority)

1. User-provided materials (screenshots / Figma / codebase / UI kit) → extract tokens. **Code ≫ screenshots.**
2. Existing product pages → ask to review them.
3. Industry references → ask which brands/products to use.
4. From scratch → offer distinct directions first (B3).

When adding to an existing UI, read its vocabulary first — color ratio, hover/focus feedback, motion language, elevation levels, density, radius, icon system — so new elements are indistinguishable from the originals.

### B3 · Style direction (standard lane only)

Skip the direction menu only when a visual source already constrains style: a provided screenshot/mockup, an existing product UI or codebase, a brand guide, or a clear "match this design" instruction. A PRD describing function is **not** a visual source. "直接做 / you decide / fast" routes to the fast lane instead.

Present **4 structurally distinct directions**, each stating: information architecture, primary layout pattern, component metaphor, interaction model, typography mood, color strategy (≈3 high-level palette routes — no hex or token lists yet), surface/material, best for / risk.

Diversity gate: options must differ on at least 4 of — color system, typography mood, layout rhythm, surface/material, interaction tone; **at least 3 of 4 must differ in page structure**, not just color or decoration; no shared hero-cards-sections skeleton across options. If the user names a color mood, include one direct exploration plus alternatives with different tradeoffs. Palette variants (2–4) come only after the direction is chosen.

Fast lane: pick the direction yourself, declare it as an assumption, and expose alternatives as Tweaks variants.

### B4 · Declare the design system

Before code, in Markdown: color palette, typography, spacing system, radius strategy, shadow hierarchy, motion style; for exploratory work add taste axes (density / contrast / novelty / warmth / materiality / motion) and the primary layout pattern.

### B5 · v0 early

Core structure + tokens + key module placeholders (`[image]`, `[icon]`) + your assumptions. No content detail, no full component set, no motion yet. A v0 with assumptions beats a perfect v1 that took 3× — the user course-corrects sooner.

### B6 · Build · B7 · Verify

Write full components, states, and motion per the technical specs below. Then walk the pre-delivery checklist item by item.

---

## Anti-Patterns (both tracks)

- Purple-pink-blue gradients, left-border accent cards, gradient-button + big-radius combos — unless inherited from a real brand.
- Inter / Roboto / Arial / system-ui as lazy defaults; emoji as icons — use `▢` / `[icon]` placeholders instead.
- **Placeholder > fake**: missing image → aspect-ratio card; missing avatar → initial circle; missing data → ask. Never fabricate stats, testimonials, or logo walls. (Track A exception: scenario seed records are a first-class mechanism, not fabrication.)
- No filler content; don't add sections unilaterally; if a page looks empty it's a layout problem — solve it with composition, not content.

---

## Output Types

- **Interactive prototypes**: no title screen; device frames when they add realism; implement the key interaction paths; cover states (default / hover / focus / active / disabled / loading / empty / error); expose variants via Tweaks instead of separate files.
- **Dashboards**: Chart.js (simple) or D3 (custom), vendored; responsive chart containers; dark/light toggle; data-ink first — color carries semantics, not decoration.
- **Component-heavy UIs**: choose by user task first (see [references/components.md](references/components.md)) — tables for comparison, cards for browsing, drawers/split panes to preserve list context. Don't turn every section into a card.
- **Slide decks**: use the slide-engine template in [references/advanced-patterns.md](references/advanced-patterns.md) — 1920×1080 fixed canvas, keyboard nav, 1-indexed `data-screen-label` slides, localStorage position.
- **Animation / demos**: CSS transitions first (80% of cases) → React state + rAF → timeline engine (advanced-patterns.md). Avoid Framer Motion / GSAP / Lottie. Provide play/pause and scrubber; no title screen.
- Pure visual comparison → design canvas; interactions and flows → a full clickable prototype.

### Tweaks Panel

Floating bottom-right panel titled **"Tweaks"**; fully hidden when closed. Expose in-direction variants (palette / density / motion / component treatment) as dropdowns or toggles instead of separate files. Add 1–2 creative tweaks when exploring; omit the panel for exact rebuilds and brand-constrained patches. Don't fake different architectures with one panel.

---

## Technical Specifications

### HTML File Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Descriptive Title</title>
    <style>/* CSS */</style>
</head>
<body>
    <!-- Content -->
    <script>/* JS */</script>
</body>
</html>
```

### React + Babel (Inline JSX)

Default to plain HTML/CSS/JavaScript. Use React only when the artifact genuinely benefits from component state, repeated interactive components, or multi-screen logic (Track A prototypes usually qualify). Use local vendored scripts only:

```html
<script src="./vendor/react/18.3.1/react.development.js"></script>
<script src="./vendor/react-dom/18.3.1/react-dom.development.js"></script>
<script src="./vendor/babel-standalone/7.29.0/babel.min.js"></script>
```

Non-negotiable hard rules:

1. **Never `const styles = { ... }`** — global `styles` objects silently overwrite each other across files. Namespace per component (`terminalStyles`, `headerStyles`) or use inline `style={{...}}`.
2. **Separate `<script type="text/babel">` blocks do not share scope** — export components across files via `Object.assign(window, { Terminal, Line })`.
3. **No `scrollIntoView`** — it disrupts iframe-embedded previews. Use `element.scrollTop` / `window.scrollTo({...})`.
4. **Plain-JS shared files must attach their globals explicitly** — `window.UI = UI;`. A top-level `const` does NOT create a `window` property; consumers reading `window.X` get `undefined` and crash at first use. Keep producer and consumer conventions identical across every file.

Also: no `type="module"` on React script tags; import order React → ReactDOM → Babel → components.

### CSS Best Practices

- CSS Grid + Flexbox; design tokens as custom properties
- Prefer brand colors; derive extra variants with `oklch()` — never invent new hues
- `text-wrap: pretty`; `clamp()` where useful; `@container` queries; `@media (prefers-color-scheme)` and `prefers-reduced-motion`
- Appropriate scale: presentations ≥24px text, touch targets ≥44px, web body 16–18px

### File Management

Descriptive filenames; split files over ~1000 lines; major revisions copy-rename with `v2`/`v3`; copy assets locally before referencing.

Artifact shape by scale:

- **Small / single-page artifacts**: one HTML file (plus copied vendor/fonts when needed) — easiest to hand around.
- **Track A business systems**: a small folder — entry HTML + separate `flow-machine.js` (pure state machine) + `seed.js` + `styles.css`, so the machine stays independent and liftable.
- **JSX loading constraint**: `<script type="text/babel" src="...">` is blocked under the `file://` protocol (Babel fetches sources via XHR, hit by CORS). Inline all JSX in one `text/babel` block inside the entry HTML, or precompile to plain JS. Plain `<script src>` and `<link rel="stylesheet">` files load fine under `file://` — which is why the machine, seed data, and CSS stay external while JSX cannot.

---

## Local Vendor Resources

Default to hand-written CSS and plain HTML/CSS/JavaScript; artifacts must run offline. External libraries are optional, not defaults.

Workflow: decide the dependency is necessary → copy only the needed folders from this skill into the output directory (relative paths only: `./vendor/...`, `./assets/fonts/...`) → before delivery, scan authored `*.html` / `*.css` / `*.js` for `http://`, `unpkg`, `jsdelivr`, `googleapis` (copied third-party folders excluded) — none allowed → report copied folders in the final response.

| Scenario | Default template | Local resources |
|---|---|---|
| Personal blog / article / landing page | Static HTML + CSS + minimal JS | None by default |
| Dashboard / analytics page | Static HTML + CSS + Chart.js or D3 | Local chart library only |
| Interactive multi-screen prototype (incl. Track A) | React + Babel inline JSX | Local React/Babel files |
| Slide deck / visual presentation | Static HTML slide engine | None unless charts/media needed |
| Quick throwaway prototype | Hand-written CSS; Tailwind/Lucide only if already vendored | Only if speed > design-system control |

### Chinese Typography

Define explicit Chinese fallbacks for Chinese or mixed pages:

```css
:root {
  --font-serif-zh: "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif;
  --font-sans-zh: "LXGW WenKai", "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
  --font-mono: "Cascadia Mono", "SFMono-Regular", Consolas, monospace;
}
```

Serif for literary/editorial, sans for product-like interfaces, mono for code/log content.

---

## Pre-delivery Checklist (never skipped)

All artifacts:

- [ ] Browser console clean; renders correctly on target devices/viewports; no text overflow
- [ ] Interactive states covered: hover / focus / active / disabled / loading; empty/error where the scenario warrants
- [ ] All colors from the declared design system — no rogue hues; no AI clichés
- [ ] No `scrollIntoView`; cross-file globals explicitly exported via `window.*` (React components and plain-JS shared modules alike)
- [ ] No filler content or fabricated data; component choices match the user task
- [ ] Authored files reference no remote URLs (copied vendor folders excluded)
- [ ] Typography intentional for the category and language mix; primary action and recovery paths clear

Track A additions:

- [ ] Every business state in the flow model has a view
- [ ] Actions gated by business state: illegal-in-state actions disabled with a reason; terminal records show a terminal note
- [ ] Max-permission view: every screen reachable from the nav, all action areas rendered
- [ ] Scenario panel works: one-click scenario reset + navigation, record-state overview; fully hidden when closed
- [ ] Seed data realistic in density and consistent across screens; at least one record per business state
- [ ] No flow-validation apparatus in the system UI (no state panel, no walkthrough tabs, no free-play buttons)
- [ ] Full-viewport shell: no page-level scrolling; list regions scroll independently with sticky table headers and pinned toolbars; content columns may scroll inside the shell; mobile exempt
- [ ] No isomorphic screens — each layout follows its screen's task
- [ ] Closing summary delivered: covered / uncovered branches / assumptions

---

## Collaborating with the User

Show work-in-progress early; explain decisions in design language, not implementation language; when feedback is ambiguous, ask instead of guessing. In Track A, write for the domain expert who clicks through the walkthroughs — their "wait, that shouldn't be possible" moment is the product working as intended.

---

## Further Reference

- [references/flow-driven-ui.md](references/flow-driven-ui.md) — Track A implementation: the state machine as internal controller, state-gated actions, max-permission view, scenario panel, seed data
- [references/components.md](references/components.md) — page-layer manual: component selection by user task; navigation, tables, forms, feedback, overlays, mobile
- [references/design-playbooks.md](references/design-playbooks.md) — internal design modes, taste calibration, audit/polish/responsive/accessibility passes
- [references/style-directions.md](references/style-directions.md) — industry patterns, visual directions, typography pairing, anti-patterns
- [references/advanced-patterns.md](references/advanced-patterns.md) — code templates: slide engine, device frames, Tweaks panel, animation timeline, design canvas, dark mode, oklch, visualizations
- [references/design-systems/index.md](references/design-systems/index.md) — index of 54 real-world brand design systems (learn the reasoning, don't copy the assets)
