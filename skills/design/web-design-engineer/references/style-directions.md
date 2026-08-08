# Style Directions and Industry Patterns

Use this reference when designing from scratch, choosing a visual direction, matching a product category, selecting typography, or avoiding generic AI-looking output.

## Table of Contents

1. [Style Direction Matrix](#style-direction-matrix)
2. [Industry Defaults](#industry-defaults)
3. [Typography Pairing](#typography-pairing)
4. [Common Anti-Patterns](#common-anti-patterns)

---

## Style Direction Matrix

Pick a direction that fits the product and task.

| Direction | Good for | Key moves | Risks |
|---|---|---|---|
| Precise Minimal | Dev tools, infra, finance | Thin borders, crisp grids, restrained accent | Can feel cold or generic |
| Dense Operations | CRM, analytics, internal tools | Compact controls, tables, saved views | Can feel cluttered without hierarchy |
| Editorial Premium | portfolios, thought leadership, luxury | Large type, strong images, generous whitespace | Can become brochure-like |
| Cinematic Dark | AI demos, media, creative tools | Near-black canvas, luminous content, depth | Often becomes purple-gradient cliche |
| Warm Human | consumer apps, support, productivity | Softer neutrals, friendly copy, moderate radius | Can feel childish if over-rounded |
| Technical Console | developer/admin products | Monospace accents, logs, explicit status | Poor for broad consumer audiences |
| Tactile Material | commerce, mobile apps, playful tools | Layered surfaces, real shadows, press states | Can become noisy |
| Data Journal | reports, dashboards, narratives | Annotation, chart hierarchy, readable tables | Can become static if interaction matters |

---

## Style Option Diversity

When presenting multiple directions, vary the system, not just the labels.

Each option should make different choices across these axes:

| Axis | Examples |
|---|---|
| Base lightness | light, warm light, mixed, dark, high-contrast |
| Temperature | cool, warm, neutral, earthy, vivid |
| Primary hue family | blue/cyan, green, red/coral, yellow/amber, violet, monochrome |
| Accent role | rare signal, navigation anchor, data semantic, editorial highlight, interactive state |
| Typography mood | precise sans, humanist sans, serif editorial, condensed display, mono accent |
| Layout rhythm | dense grid, airy editorial, split pane, asymmetric, timeline/index, full-bleed canvas |
| Surface/material | flat, paper, tactile, glass, industrial, luminous, OS-native |
| Motion tone | quiet, snappy, smooth, cinematic, direct-manipulation |

### Palette Variant Rules

When color is an open decision, give 2-3 palette variants inside each promising style direction. Keep them compact but concrete enough to choose from.

Each palette variant should name:

- Base surface: white, off-white, warm cream, pale green, mist gray, charcoal, etc.
- Primary hue: the dominant brand/action color.
- Secondary/support hue: a separate hue family or neutral support.
- Accent: a small signal color with a clear role.
- Mood: fresh, calm, premium, technical, playful, editorial, etc.

If the user mentions a desired color mood, include it explicitly. For example, if they ask for a fresh light-green feeling, include a palette with pale green surfaces or green primary, but still offer alternatives so they can compare.

Avoid these weak option sets:

- Same palette with only the accent color changed.
- All options dark, all options beige, all options blue SaaS, or all options purple-gradient.
- No option matching the user's named color preference.
- Same card grid with different names.
- Same type mood with only font weight changed.
- Options that differ in copywriting but not in visual system.

For a 3-option set, aim for clear contrast such as:

1. Light / editorial / restrained accent / spacious.
2. Warm or tactile / approachable / medium density.
3. Cool or dark / high contrast / technical or dramatic.

For a 5-option set, include at least one light, one warm, one cool/technical, one high-contrast or dark, and one unconventional layout/material direction unless the user's brand constraints forbid it.

---

## Industry Defaults

Use these as starting points, then adapt to user context.

| Product type | Structure | Visual tone | Avoid |
|---|---|---|---|
| Fintech | Clear dashboard, transaction list, trust markers | Calm, precise, high contrast | Neon, game-like styling, vague metrics |
| Healthcare | Guided flows, readable records, reassurance | Warm, calm, accessible | Tiny text, alarmist red, decorative complexity |
| Developer tool | Docs, console, logs, status, examples | Precise, dense, sharp | Marketing cards that hide real workflow |
| AI product | Input/output proof, examples, controls | Capability-forward, transparent | Abstract gradients without real output |
| CRM/internal ops | Table/list first, filters, saved views | Dense, efficient, restrained | Oversized hero sections, card-only dashboards |
| Creative tool | Canvas, inspector, asset previews | Expressive but controllable | Hiding the creative output behind chrome |
| Ecommerce | Product imagery, comparison, trust, checkout clarity | Tactile, direct, conversion-aware | Fake urgency, weak image treatment |
| Education | Progress, modules, exercises, feedback | Clear, encouraging, structured | Long walls of text, unclear next action |
| Portfolio | Work first, case-study narrative | Editorial, confident, specific | Generic "selected works" grids without context |
| Presentation deck | Story arc, large type, strong visuals | High contrast, low density | Dense bullets and tiny charts |

---

## Typography Pairing

- Use one strong family plus system fallback for product UI unless a brand needs more.
- Use serif heading plus sans body for editorial, culture, education, and narrative pages.
- Use monospace as accent for code, IDs, metrics, labels, and technical status; avoid monospace body copy.
- For Chinese-heavy pages, define explicit Chinese fallbacks and test mixed Latin/CJK line height.
- Avoid lazy defaults when designing from scratch. If using system-ui or Inter because the product already uses it, treat that as a fidelity decision.

| Context | Heading | Body | Accent |
|---|---|---|---|
| SaaS app | Neutral sans 600-700 | Neutral sans 400-500 | Mono for IDs/status |
| Editorial | Serif or high-contrast sans | Readable serif/sans | Small labels sparingly |
| Developer tool | Precise sans | Precise sans | Mono for commands/code |
| Luxury/product | Refined serif or narrow sans | Quiet sans | Minimal labels |
| Slides | Bold display sans/serif | Large readable sans | Mono only for code |

---

## Common Anti-Patterns

- Purple-blue-pink gradients used as a substitute for product specificity.
- Card grids for every type of content, including dense operational workflows.
- Fake statistics, fake logos, fake testimonials, or decorative analytics.
- Default font choices when no brand/system requires them.
- Low-contrast gray text used to create fake sophistication.
- Over-rounded controls in professional tools.
- Icons used as decoration without semantic purpose.
- Tooltips containing required instructions.
- Motion that delays task completion or ignores reduced-motion preferences.
