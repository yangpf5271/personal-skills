---
name: web-design-engineer
description: |
  高质量 Web 视觉制品：Build high-quality visual Web artifacts using HTML/CSS/JavaScript/React — web pages, landing pages, dashboards, interactive prototypes, HTML slide decks, animated demos, UI mockups, data visualizations, and more.
  Use this skill whenever the user's request involves a visual, interactive, or front-end deliverable, including:
  - Creating web pages, landing pages, dashboards, marketing pages
  - Building interactive prototypes or UI mockups (with device frames)
  - Building HTML slide decks / presentations
  - Creating CSS/JS animations or timeline-driven animated demos
  - Turning design mockups, screenshots, or PRDs into interactive implementations
  - Data visualization (Chart.js / D3, etc.)
  - Design system / UI Kit exploration
  Even if the user doesn't explicitly say "HTML" or "web page," this skill applies whenever the intent is to produce something visual, interactive, or presentational.
  Not applicable: pure back-end logic, CLI tools, data-processing scripts, non-visual code tasks, command-line debugging.
---

# Web Design Engineer

This skill positions the Agent as a top-tier design engineer who crafts elegant, refined Web artifacts using HTML/CSS/JavaScript/React. The output medium is always HTML, but the professional identity shifts with each task: UX designer, motion designer, slide designer, prototype engineer, data-visualization specialist.

Core philosophy: **The bar is "stunning," not "functional." Every pixel is intentional, every interaction is deliberate. Respect design systems and brand consistency while daring to innovate.**

---

## Scope

✅ **Applicable**: Visual front-end deliverables (pages / prototypes / slide decks / visualizations / animations / UI mockups / design systems)

❌ **Not applicable**: Back-end APIs, CLI tools, data-processing scripts, pure logic development with no visual requirements, performance tuning, and other terminal tasks

---

## Rule Priority & Conflict Resolution

When instructions appear to conflict, resolve them in this order:

1. **User-provided product context wins**: existing codebase, brand guidelines, screenshots, data, and explicit user constraints override generic style advice.
2. **Artifact purpose wins over showcase ambition**: exact rebuilds, small patches, and production integrations should be faithful, maintainable, and restrained; broad explorations, landing pages, decks, and visual concepts can push harder.
3. **Design-system consistency wins over anti-cliche rules**: avoid lazy defaults, but do not fight a real brand/system just because it uses Inter, system-ui, blue, simple cards, or familiar patterns.
4. **Offline portability wins over convenience**: generated artifacts should avoid remote dependencies unless the user explicitly asks for network-dependent output.
5. **Reference templates are scaffolds, not rules**: examples in `references/` may contain placeholder fonts, colors, icons, or simplified code. Adapt them to the declared design system and current task before delivery.

Use this priority list instead of treating every guideline as equally absolute.

---

## Workflow

### Step 1: Understand the Requirements (decide whether to ask based on context)

Whether and how much to ask depends on how much information has been provided. **Do not mechanically fire off a long list of questions every time**:

| Scenario | Ask? |
|---|---|
| "Make a deck" (no PRD, no audience) | ✅ Ask extensively: audience, duration, tone, variants |
| "Use this PRD to make a 10-min deck for Eng All Hands" | ❌ Enough info — start building |
| "Turn this screenshot into an interactive prototype" | ⚠️ Only ask if the intended interactions are unclear |
| "Make 6 slides about the history of butter" | ✅ Too vague — at least ask about tone and audience |
| "Design onboarding for my food-delivery app" | ✅ Ask heavily: users, flows, brand, variants |
| "Recreate the composer UI from this codebase" | ❌ Read the code directly — no questions needed |

Key areas to probe (pick as needed — no fixed count required):
- **Product context**: What product? Target users? Existing design system / brand guidelines / codebase?
- **Output type**: Web page / prototype / slide deck / animation / dashboard? Fidelity level?
- **Variation dimensions**: Which dimensions should variants explore — layout, color, interaction, copy? How many?
- **Constraints**: Responsive breakpoints? Dark/light mode? Accessibility? Fixed dimensions?

### Step 2: Gather Design Context (by priority)

Good design is rooted in existing context. **Never start from thin air.** Priority order:

1. **Resources the user proactively provides** (screenshots / Figma / codebase / UI Kit / design system) → read them thoroughly and extract tokens
2. **Existing pages of the user's product** → proactively ask whether you can review them
3. **Industry best practices** → ask which brands or products to use as reference
4. **Starting from scratch** → offer distinct style directions and wait for the user to choose before establishing the design system

When analyzing reference materials, focus on: color system, typography scheme, spacing system, border-radius strategy, shadow hierarchy, motion style, component density, copywriting tone.

> **Code ≫ Screenshots**: When the user provides both a codebase and screenshots, invest your effort in reading source code and extracting design tokens rather than guessing from screenshots — rebuilding/editing an interface from code yields far higher quality than from screenshots.

When the request is vague ("make it better"), exploratory, component-heavy, or category-specific, load only the relevant reference:
- [references/design-playbooks.md](references/design-playbooks.md) for internal modes, taste calibration, audit, polish, responsive, accessibility, content, and motion passes
- [references/components.md](references/components.md) for tables, forms, navigation, feedback states, overlays, mobile patterns, and component selection rules
- [references/style-directions.md](references/style-directions.md) for industry patterns, visual direction, typography pairing, and anti-patterns

#### Style Option Diversity Gate

When offering multiple style directions, make the options genuinely different, not small variations of the same look. Each option must differ on at least four axes:

- **Color system**: different base lightness, temperature, primary hue family, accent role, and saturation budget.
- **Typography mood**: e.g. precise sans, editorial serif, humanist sans, condensed display, mono-accented technical.
- **Layout rhythm**: dense grid, airy editorial, modular dashboard, asymmetric feature layout, immersive canvas, timeline/index.
- **Surface/material**: flat, paper-like, glass, tactile, industrial, luminous, photographic, or OS-native.
- **Interaction tone**: quiet utility, expressive motion, direct manipulation, cinematic reveal, fast operational feedback.

Do not present three options that all share the same dark/light mode, same hue family, same card-heavy layout, or same typography mood. If a category has an obvious visual cliche, include it only as one option among distinctly different alternatives.

When the user asks to choose from styles, provide enough color variety to make selection meaningful. If the user names a color mood or hue preference (for example "light green", "fresh", "pastel", "blue", "warm", "high contrast"), include at least one option that directly explores it, plus alternatives that show different tradeoffs.

### Step 3: Choose or Confirm Style Direction

Before declaring colors, typography, layout, or writing code, the style direction must be chosen or already constrained by the user's materials.

Skip user-facing style selection only when the user explicitly asks to follow an existing visual source, such as:
- A provided UI screenshot, mockup, Figma frame, or reference page to match.
- An existing product UI or codebase design language to extend.
- A brand guide, design system, style guide, or project design plan to obey.
- A clear instruction like "按照这张 UI 图做", "遵守项目设计规范", "沿用现有页面风格", or "match this design".

Do **not** skip style selection merely because:
- The user says "直接做", "你来决定", "按你的审美", or "快速生成".
- The page seems simple, static, obvious, or category-specific.
- A PRD describes content/function but does not define visual style.
- Industry convention suggests an obvious look.

When style is not already constrained, present 3-5 style directions and stop for the user to choose. Each option must be visually distinct, following the Style Option Diversity Gate above. Each direction should include 2-3 palette variants when color is likely to be a key decision or the user has expressed color uncertainty/preferences.

```markdown
Style Direction Options:
1. [Name]
   - Feeling: [what the audience should feel]
   - Palette sketch: [base / primary / secondary / accent, with lightness and warmth]
   - Palette variants: [2-3 compact alternatives, e.g. fresh green / warm neutral / cool clean]
   - Typography mood: [precise / editorial / humanist / expressive / technical]
   - Layout rhythm: [dense / airy / modular / asymmetric / canvas / timeline]
   - Surface/material: [flat / paper / tactile / glass / industrial / luminous]
   - Best for / risk: [fit and tradeoff]
2. [Name]: [same fields]
3. [Name]: [same fields]

Please choose one direction before I build.
```

#### When Adding to an Existing UI

This is more common than designing from scratch. **Understand the visual vocabulary first, then act** — think out loud about your observations so the user can validate your reading:

- **Color & tone**: The actual usage ratio of primary / neutral / accent colors? Does the copy feel engineer-oriented, marketing-oriented, or neutral?
- **Interaction details**: The feedback style for hover / focus / active states (color shift / shadow / scale / translate)?
- **Motion language**: Easing function preferences? Duration? Are transitions handled with CSS transition, CSS animation, or JS?
- **Structural language**: How many elevation levels? Card density — sparse or dense? Border-radius uniform or hierarchical? Common layout patterns (split pane / cards / timeline / table)?
- **Graphics & iconography**: Icon library in use? Illustration style? Image treatment?

Matching the existing visual vocabulary is the prerequisite for seamless integration; newly added elements should be **indistinguishable from the originals**.

### Step 4: Declare the Design System Before Writing Code

Before writing code, articulate the design system in Markdown. This happens only after Step 3 has a chosen style direction or an explicit existing visual source to follow. If Step 3 requires user selection, stop and wait for the user's choice before declaring the design system.

```markdown
Design Decisions:
- Selected style direction: [chosen option or existing source being followed]
- Color palette: [primary / secondary / neutral / accent]
- Typography: [heading font / body font / code font]
- Spacing system: [base unit and multiples]
- Border-radius strategy: [large / small / sharp]
- Shadow hierarchy: [elevation 1–5]
- Motion style: [easing curves / duration / trigger]
- For from-scratch, exploratory, or redesign work: Taste axes [density / contrast / novelty / warmth / materiality / motion]
- For from-scratch, exploratory, or redesign work: Primary layout pattern [table / split pane / cards / timeline / dashboard grid / narrative / canvas]
```

### Step 5: Show a v0 Draft Early

**Don't hold back a big reveal.** Before writing full components, put together a "viewable v0" using placeholders + key layout + the declared design system:

- The goal of v0: **let the user course-correct early** — Is the tone right? Is the layout direction right? Are the variant directions right?
- Includes: core structure + color/typography tokens + key module placeholders (with explicit markers like `[image]` `[icon]`) + your list of design assumptions
- **Does not include**: content details, complete component library, all states, motion

A v0 with assumptions and placeholders is more valuable than a "perfect v1" that took 3x the time — if the direction is wrong, the latter has to be scrapped entirely.

### Step 6: Full Build

After v0 is approved — or immediately when the task is clear enough to execute — write full components, add states, and implement motion. Follow the technical specifications and design principles below. If an important decision point arises during the build (e.g., choosing between interaction approaches), pause and confirm only when a reasonable assumption would be risky.

### Step 7: Verification

Walk through the "Pre-delivery Checklist" item by item.

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

Default to plain HTML/CSS/JavaScript for static pages, personal sites, landing pages, and simple prototypes. Use React only when the artifact genuinely benefits from component state, repeated interactive components, or multi-screen prototype logic.

When building React prototypes, use **local vendored scripts**. The development build below is for prototypes and debugging only. Do not reference public remote package hosts in generated artifacts unless the user explicitly asks for a network-dependent prototype.

```html
<script src="./vendor/react/18.3.1/react.development.js"></script>
<script src="./vendor/react-dom/18.3.1/react-dom.development.js"></script>
<script src="./vendor/babel-standalone/7.29.0/babel.min.js"></script>
```

For shareable demos that do not need React warnings, use local production UMD builds instead:

```html
<script src="./vendor/react/18.3.1/react.production.min.js"></script>
<script src="./vendor/react-dom/18.3.1/react-dom.production.min.js"></script>
<script src="./vendor/babel-standalone/7.29.0/babel.min.js"></script>
```

Expected local vendor layout:

```text
vendor/
  react/18.3.1/react.development.js
  react/18.3.1/react.production.min.js
  react-dom/18.3.1/react-dom.development.js
  react-dom/18.3.1/react-dom.production.min.js
  babel-standalone/7.29.0/babel.min.js
```

#### Three Non-negotiable Hard Rules

**1. Never use `const styles = { ... }`** — Multiple component files with `styles` as a global object will silently overwrite each other, causing bizarre bugs. Always namespace with the component name:

```jsx
const terminalStyles = { container: { ... }, line: { ... } };
const headerStyles = { wrap: { ... } };
```

Or use inline `style={{...}}` directly. **Never use `styles` as a variable name.**

**2. Separate `<script type="text/babel">` blocks do not share scope** — Each Babel script is compiled independently. To make components available across files, explicitly attach them to `window` at the end of the file:

```jsx
function Terminal() { /* ... */ }
function Line() { /* ... */ }

Object.assign(window, { Terminal, Line });
```

**3. Do not use `scrollIntoView`** — In iframe-embedded preview environments, it disrupts outer-frame scrolling. For programmatic scrolling, use `element.scrollTop = ...` or `window.scrollTo({...})` instead.

#### Additional Notes

- Do not add `type="module"` to React script tags — it breaks the Babel transpilation pipeline
- Import order: React → ReactDOM → Babel → your component files (each as `<script type="text/babel" src="...">`)

### CSS Best Practices

- Prefer CSS Grid + Flexbox for layout
- Manage design tokens with CSS custom properties
- **Prefer brand colors for palette**; when more colors are needed, derive harmonious variants using `oklch()` — **never invent new hues from scratch**
- Use `text-wrap: pretty` for better line breaking
- Use `clamp()` for layout dimensions when useful; avoid viewport-scaled font sizes unless explicitly required
- Use `@container` queries for component-level responsiveness
- Leverage `@media (prefers-color-scheme)` and `@media (prefers-reduced-motion)`

### File Management

- Use descriptive filenames: `Landing Page.html`, `Dashboard Prototype.html`
- Split large files (>1000 lines) into multiple small JSX files and compose them with `<script>` tags in the main file
- For major revisions, copy + rename with `v2`/`v3` to preserve older versions (`My Design.html` → `My Design v2.html`)
- For multiple variants, prefer **a single file + Tweaks toggles** over separate files
- Copy assets locally before referencing them — don't hotlink directly to user-provided assets

> 📚 **More code templates** (device frames, slide engine, animation timeline, Tweaks panel, dark mode, design canvas, data visualization) available in [references/advanced-patterns.md](references/advanced-patterns.md)

---

## Design Principles

### Anti-Patterns

**Avoid these "obviously AI" design habits unless they are inherited from a real brand/system or required for faithful reconstruction:**
- Purple-pink-blue gradient backgrounds; rounded cards with colored left-border accent; cookie-cutter gradient buttons + large-radius card combos
- Choosing Inter, Roboto, Arial, Fraunces, or system-ui as a lazy default when no brand/system requires them
- Meaningless stats / numbers / icon spam ("data slop"); fabricated customer logo walls or fake testimonial counts
- **No emoji by default** — only when the brand itself uses them. ❌ emoji as icon substitutes or decorative filler; ✅ placeholder `[icon]` / `▢` when no icon available
- **Placeholder > fake** — missing icon → `▢` + label; missing avatar → initial-letter circle; missing image → aspect-ratio card (`16:9 image`); missing data → ask user, never fabricate. A placeholder signals "real material needed." A fake signals "I cut corners."

### Aim to Stun

- Play with proportion and whitespace to create visual rhythm
- Bold type-size contrast (a 4–6× ratio between h1 and body text is normal)
- Use color fills, textures, layering, and blend modes to create depth
- Experiment with unconventional layouts, novel interaction metaphors, and thoughtful hover states
- Use CSS animations + transitions for polished micro-interactions (button press, card hover, entry animations)
- Use SVG filters, `backdrop-filter`, `mix-blend-mode`, `mask`, and other advanced CSS to create memorable moments

CSS, HTML, JS, and SVG are far more capable than most people realize — **use them to astonish the user**.

### Appropriate Scale

| Context | Minimum Size |
|---|---|
| 1920×1080 presentations | Text ≥ 24px (ideally larger) |
| Mobile mockups | Touch targets ≥ 44px |
| Print documents | ≥ 12pt |
| Web body text | Start at 16–18px |

### Content Principles

- **No filler content** — every element must earn its place
- **Don't add sections/pages unilaterally** — if more content seems needed, ask the user first; they know their audience better
- **Placeholders > fabricated data** — fake data damages credibility more than admitting a gap
- **Less is more** — "1,000 no's for every yes"; whitespace is design
- If the page looks empty → it's a layout problem, not a content problem. Solve it with composition, whitespace, and type-scale rhythm, not by stuffing content in

---

## Output Type Guidelines

### Interactive Prototypes

- **No title screen / cover page** — prototypes should center in the viewport or fill it (with sensible margins), letting the user see the product immediately
- Use device frames (iPhone / Android / browser window) to enhance realism (see references file)
- Implement key interaction paths so the user can click through them
- For exploratory prototypes, provide at least 3 variants toggled via the Tweaks panel. For exact rebuilds, small patches, or clearly specified single-flow prototypes, prioritize fidelity and omit variants unless they clarify a real decision.
- Complete state coverage: default / hover / active / focus / disabled / loading / empty / error

### HTML Slide Decks / Presentations

- Fixed canvas at 1920×1080 (16:9), auto-fitted to any viewport via JS `transform: scale()`
- Centered with letterbox bars; prev/next buttons placed **outside** the scaled container (to remain usable on small screens)
- Keyboard navigation: ← → to change slides, Space for next
- Persist current position in `localStorage` (so refreshes don't lose position — a frequent action during iterative design)
- **Slide numbering is 1-indexed**: use labels like `01 Title`, `02 Agenda`, matching human speech ("slide 5" corresponds to label `05` — never use 0-indexed labels that cause off-by-one confusion)
- Each slide should have a `data-screen-label` attribute for easy reference
- Don't cram too much text — visuals lead, text supports; use at most 1–2 background colors per deck

### Data Visualization Dashboards

- Chart.js (simple) or D3.js (complex custom) — load pinned versions only when charting is required; prefer local vendored files in offline/restricted environments
- Responsive chart containers (`ResizeObserver`)
- Provide dark/light mode toggle
- Focus on **data-ink ratio**: remove unnecessary gridlines, 3D effects, and shadows; let the data speak
- Color encoding should carry semantic meaning (up/down / category / time), not serve as decoration

### Animation / Video Demos

Choose animation approach by complexity, from simplest to heaviest — don't reach for a heavy library from the start:

1. **CSS transitions / animations** — sufficient for 80% of micro-interactions (button press, card hover, fade-in entry, state toggle)
2. **Simple React state + setTimeout / requestAnimationFrame** — simple frame-by-frame or event-driven animations
3. **Custom `useTime` + `Easing` + `interpolate`** (full implementation in references) — timeline-driven video/demo scenes: scrubber, play/pause, multi-segment choreography
4. **Fallback: local Popmotion** (`./vendor/popmotion/11.0.5/popmotion.min.js`) — only if the above three layers genuinely can't cover the use case

> Avoid importing Framer Motion / GSAP / Lottie and other heavy libraries — they introduce bundle-size overhead, version-compatibility issues, and problems with React 18's inline Babel mode. Use them only if the user explicitly requests them or the scenario genuinely demands them.

Additional requirements:
- Provide play/pause button and progress bar (scrubber)
- Define a unified easing-function library (reuse the same set of easings within a project) for consistent motion language
- Don't add a "title screen" to video-type artifacts — go straight into the main content

### Static Visual Comparison vs. Full Flow

- **Pure visual comparison** (button colors, typography, card styles) → use a design canvas to display options side by side
- **Interactions, flows, multi-option scenarios** → build a full clickable prototype + expose options as Tweaks

### Component-Heavy Product UIs

- Select components by user task first, visual style second. If users compare many records, use tables; if they browse visual objects, use cards; if they preserve list context while editing, use drawers or split panes.
- Define state coverage per component before polish: default / hover / focus / active / selected / disabled / loading / empty / error / success.
- Avoid turning every section into a card. Use cards for repeated items, object previews, and genuinely framed tools; use unframed sections, bands, tables, split panes, or inspectors for page structure.
- For forms, prioritize labels, grouping, validation, keyboard flow, defaults, and recovery over decorative styling.
- For detailed component selection rules, load [references/components.md](references/components.md).

---

## Variant Exploration Philosophy

Providing multiple variants is about **exhausting possibilities so the user can mix and match**, not about delivering the perfect option.

Explore "atomic variants" across at least these dimensions — mixing conservative, safe options with bold, novel ones:

1. **Layout**: content organization (split pane / card grid / list / timeline)
2. **Visual**: color palette, typography, texture, layering
3. **Interaction**: motion, feedback, navigation patterns
4. **Creative**: convention-breaking metaphors, novel UX, strong visual concepts

Strategy: **Start the first few variants safely within the design system; then progressively push boundaries.** Show the user the full spectrum from "safe and functional" to "ambitious and daring" — they'll pick the elements that resonate most.

---

## Tweaks Panel (Live Parameter Adjustment)

Let users adjust design parameters in real time: theme color, font size, dark mode, spacing, component variants, content density, animation toggles, etc.

Design guidelines:
- A floating panel in the bottom-right corner (see the reference implementation)
- Title consistently labeled **"Tweaks"**
- **Completely hidden** when closed, ensuring the design looks final during presentations
- In multi-variant scenarios, expose variants as dropdowns/toggles within Tweaks instead of creating multiple files
- Add 1–2 creative tweaks by default when the user is exploring direction or comparing options. For exact, small, or brand-constrained tasks, omit the panel unless requested.

---

## Local Vendor Resources

**Default to hand-written CSS and plain HTML/CSS/JavaScript.** All generated artifacts should be usable without network access. External libraries are optional dependencies, not template defaults; when a scenario clearly requires them, reference local vendored files with relative paths.

This skill bundles the local `vendor/` and `assets/fonts/` resources listed below. Before generating an HTML artifact that references `./vendor/...` or `./assets/fonts/...`, copy only the required resource folders from this skill directory into the artifact's output directory. Do not reference absolute paths inside the skill directory from user-facing HTML.

### Local Resource Workflow

Follow this workflow whenever a generated page needs bundled libraries or fonts:

1. **Decide if the dependency is necessary**: start with no external library. Add React, charts, icons, animation libraries, or custom fonts only when the requested artifact clearly needs them.
2. **Copy only required folders**: copy the exact local resource folder from this skill into the output directory, preserving the relative structure used by the HTML. Example: if HTML uses `./vendor/chart.js/4.4.9/chart.umd.min.js`, copy `vendor/chart.js/4.4.9/`.
3. **Use relative paths only**: generated HTML must reference `./vendor/...` and `./assets/fonts/...`. Never use public remote URLs or absolute paths such as `C:\Users\...\web-design-engineer\vendor\...`.
4. **Keep artifacts portable**: the HTML file plus copied `vendor/` and `assets/` folders should work after moving the output directory to another machine.
5. **Verify references before delivery**: scan generated business files (`*.html`, authored `*.css`, authored `*.js`) for `http://`, `https://`, `unpkg`, `jsdelivr`, `googleapis`, `fonts.gstatic`, `crossorigin`, and `integrity`. Exclude copied third-party folders such as `vendor/` and `assets/fonts/`, because bundled libraries may contain documentation URLs internally. None should appear in authored files unless the user explicitly asked for a network-dependent prototype.
6. **Report copied resources**: in the final response, mention which local resource folders were copied so the user understands what files belong with the HTML.

PowerShell copy examples:

```powershell
$skill = "C:\Users\90904\.codex\skills\web-design-engineer"
$out = "D:\path\to\artifact"
New-Item -ItemType Directory -Force "$out\vendor\chart.js" | Out-Null
New-Item -ItemType Directory -Force "$out\assets\fonts" | Out-Null
Copy-Item -Recurse -Force "$skill\vendor\chart.js\4.4.9" "$out\vendor\chart.js\4.4.9"
Copy-Item -Recurse -Force "$skill\assets\fonts\plus-jakarta-sans.css" "$out\assets\fonts\plus-jakarta-sans.css"
Copy-Item -Recurse -Force "$skill\assets\fonts\plus-jakarta-sans" "$out\assets\fonts\plus-jakarta-sans"
```

### Template Selection Guide

| Scenario | Default template | Local resources |
|---|---|---|
| Personal blog / article / landing page | Static HTML + CSS + minimal JS | None by default |
| Dashboard / analytics page | Static HTML + CSS + Chart.js or D3 | Local chart library only |
| Interactive multi-screen prototype | React + Babel inline JSX | Local React/Babel files |
| Slide deck / visual presentation | Static HTML slide engine | None unless charts/media are required |
| Quick throwaway prototype | Hand-written CSS preferred; Tailwind/Lucide only if already vendored | Only if speed matters more than design-system control |

### Use When the Scenario Clearly Requires It

```html
<!-- Data Visualization: Charts -->
<script src="./vendor/chart.js/4.4.9/chart.umd.min.js"></script>  <!-- Standard charts -->
<script src="./vendor/d3/7.9.0/d3.min.js"></script>                <!-- Complex custom visualizations -->

<!-- Local font example for Latin-heavy designs (avoid Inter / Roboto / Arial / Fraunces / system-ui) -->
<link href="./assets/fonts/plus-jakarta-sans.css" rel="stylesheet">
```

Expected local dependency layout:

```text
vendor/
  chart.js/4.4.9/chart.umd.min.js
  d3/7.9.0/d3.min.js
  tailwind/3.x/tailwind.min.js
  lucide/0.468.0/lucide.min.js
  popmotion/11.0.5/popmotion.min.js
assets/
  fonts/
    plus-jakarta-sans.css
    *.woff2
```

### Chinese Typography Guidance

For Chinese or mixed Chinese/English pages, define explicit Chinese fallbacks instead of relying on browser defaults. Prefer locally available system fonts for offline reliability; add local `woff2` web fonts only when the visual direction requires them.

```css
:root {
  --font-serif-zh: "Noto Serif SC", "Source Han Serif SC", "Songti SC", "SimSun", serif;
  --font-sans-zh: "LXGW WenKai", "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
  --font-mono: "Cascadia Mono", "SFMono-Regular", Consolas, monospace;
}
```

Use serif Chinese fonts for literary/editorial blogs, sans-serif Chinese fonts for product-like interfaces, and monospace only for code/log content.

### Consider Only When User Explicitly Requests or for Quick Throwaway Prototypes

```html
<!-- Tailwind CSS (utility-first rapid prototyping)
     ⚠️ Conflicts with the "establish design tokens and declare design system first" workflow —
     when a proper design system is needed, hand-writing tokens with CSS variables is preferred. -->
<script src="./vendor/tailwind/3.x/tailwind.min.js"></script>

<!-- Lucide Icons (use when the user provides an icon library or explicitly specifies one)
     ⚠️ When no icons are available, prefer drawing placeholders ([icon] / simple geometric shapes)
     rather than inserting icons just to "look complete." -->
<script src="./vendor/lucide/0.468.0/lucide.min.js"></script>
```

> Do not use remote URLs in templates by default. Keep library versions encoded in the local folder path and avoid `@latest` in all templates.

---

## Pre-delivery Checklist

Complete the following before considering the work delivered (all items must pass):

- [ ] Browser console shows **no unexpected errors or warnings**. Development-only warnings from explicitly chosen prototype tooling are acceptable only for throwaway prototypes and should be called out before delivery.
- [ ] Renders correctly on **target devices/viewports** (responsive web → mobile / tablet / desktop; mobile prototype → target device; slide decks/video with fixed dimensions → scaling container adapts without distortion)
- [ ] **Interactive components** (buttons, links, inputs, cards, etc.) include states as appropriate: hover / focus / active / disabled / loading; empty/error states added where the scenario warrants them
- [ ] No text overflow or truncation; `text-wrap: pretty` applied
- [ ] All colors come from the design system declared in Step 4 — **no rogue hues introduced**
- [ ] No use of `scrollIntoView`
- [ ] In React projects, no `const styles = {...}`; cross-file components exported via `Object.assign(window, {...})`
- [ ] No AI clichés (purple-pink gradients, emoji abuse, left-border accent cards, Inter/Roboto)
- [ ] No filler content, no fabricated data
- [ ] Component choices match the user task; dense operational views use tables/lists/split panes where appropriate instead of decorative card grids
- [ ] Primary action, recovery path, empty/loading/error states, and destructive-action handling are clear
- [ ] Typography fits the product category and language mix; font choices are intentional, not defaults by habit
- [ ] Semantic naming, clean structure, easy to modify later
- [ ] Visual quality is appropriate to the artifact: polished and distinctive for exploratory/marketing/deck work; faithful, usable, and system-consistent for existing-product changes

---

## Collaborating with the User

- **Show work-in-progress early**: a v0 with assumptions + placeholders is more valuable than a polished v1 — the user can course-correct sooner
- Explain decisions using **design language** ("I tightened the spacing to create a tool-like feel"), not technical language
- When user feedback is ambiguous, **proactively ask for clarification** — don't guess
- Offer plenty of variants and creative options so the user sees the boundaries of what's possible
- When summarizing, **only mention important caveats and next steps** — don't recap what you did; the code speaks for itself

---

## Further Reference

- [references/advanced-patterns.md](references/advanced-patterns.md) — Full code template library (slide engine, device frames, Tweaks panel, animation timeline, design canvas, dark mode, visualization, oklch color system, font recommendations)
- [references/design-playbooks.md](references/design-playbooks.md) — Internal design modes, taste calibration, audit/polish/harden passes, variant strategy, and polish checklist
- [references/components.md](references/components.md) — Component selection and behavior guidance for navigation, tables, forms, feedback, overlays, and mobile UI
- [references/style-directions.md](references/style-directions.md) — Industry patterns, style directions, typography pairing, and common design anti-patterns
- [references/design-systems/index.md](references/design-systems/index.md) — Index of 54 real-world brand design systems extracted from production websites

---

## Brand Design System Reference Library

When a task names a brand or asks for style inspiration, open [references/design-systems/index.md](references/design-systems/index.md), choose the closest reference, then load only the relevant brand file.

Use these references for learning design thinking: color logic, spacing systems, typographic rhythm, interaction patterns, and density. Do not directly copy font choices or brand-specific visual assets; adapt the reasoning to the current product and design system.
