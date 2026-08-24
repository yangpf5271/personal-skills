# Design Playbooks

Use this reference for broad visual exploration, vague requests like "make it better", design audits, final polish, motion direction, responsive hardening, or when the artifact feels generic.

## Table of Contents

1. [Internal Modes](#internal-modes)
2. [Taste Calibration](#taste-calibration)
3. [Design Passes](#design-passes)
4. [Variant Strategy](#variant-strategy)
5. [Polish Checklist](#polish-checklist)

---

## Internal Modes

Map vague design requests to a concrete mode before changing the UI.

| Mode | Use when | Primary output |
|---|---|---|
| `audit` | Existing UI needs critique or improvement | Findings by severity, then fixes |
| `shape` | Product/page direction is unclear | IA, layout pattern, visual direction |
| `tokens` | CSS or visuals are inconsistent | Color, type, spacing, radius, shadow, motion tokens |
| `variants` | User wants exploration | 3-5 materially different directions |
| `component-pass` | UI is form/table/nav/card heavy | Component choices, behavior, states |
| `responsive-pass` | Layout must work across sizes | Breakpoint behavior, overflow fixes |
| `accessibility-pass` | Production UI, forms, keyboard flows | Labels, focus, contrast, reduced motion |
| `content-pass` | Copy or hierarchy feels generic | Stronger labels, hierarchy, removed filler |
| `motion-pass` | Interaction should feel premium | Easing, timing, choreography, reduced-motion fallback |
| `polish-pass` | Artifact works but feels average | Composition, rhythm, detail, edge states |

Do not expose these as literal commands unless the user asks for a command list. Use them as an execution lens.

---

## Taste Calibration

Before designing from scratch, set these axes. If the user did not specify them, infer conservatively from the product category.

| Axis | Low end | High end | Design effect |
|---|---|---|---|
| Density | Spacious | Dense | Controls spacing, type scale, amount of visible data |
| Contrast | Quiet | Dramatic | Controls value range, type weight, color intensity |
| Novelty | Familiar | Experimental | Controls layout risk and interaction metaphor |
| Warmth | Technical | Human | Controls copy tone, radius, color temperature |
| Materiality | Flat | Layered | Controls borders, shadows, textures, depth |
| Motion | Static | Expressive | Controls transitions and choreography |

Default by category:

- SaaS, CRM, internal tools: medium-high density, medium contrast, low-medium novelty, restrained motion.
- Developer tools: medium density, high precision, crisp borders, visible status and focus states.
- Fintech, security, healthcare: restrained novelty, high trust, strong hierarchy, explicit recovery paths.
- Consumer lifestyle, travel, food: lower density, stronger imagery, warmer copy, more tactile surfaces.
- Creative tools and AI demos: medium density, higher novelty, expressive previews of output.
- Slides and storytelling: low density, high contrast, large type, visual-led composition.

---

## Design Passes

### Audit Pass

1. Identify the user's primary task on each screen.
2. List visual, interaction, content, accessibility, and responsive issues by severity.
3. Fix structural problems before decoration.
4. Recheck states and smallest viewport after visual changes.

### Shape Pass

1. Choose the page's job: sell, explain, operate, compare, create, monitor, or present.
2. Pick the layout pattern that fits that job: narrative, dashboard grid, table, split pane, editor canvas, timeline, queue, or gallery.
3. Define the taste axes and design tokens.
4. Build only the minimum structure needed to validate direction.

### Harden Pass

1. Check smallest and largest target viewport.
2. Verify long labels, mixed-language text, empty states, errors, loading states, and disabled states.
3. Ensure focus order and keyboard access.
4. Remove remote dependencies unless explicitly required.

### Accessibility Pass

1. Verify semantic HTML for headings, landmarks, buttons, links, labels, tables, and form fields.
2. Check keyboard flow: visible focus, logical tab order, no keyboard traps, and no hover-only required actions.
3. Confirm contrast, touch target size, text scaling, reduced-motion behavior, and non-color status cues.
4. Ensure errors and confirmations are announced near the relevant control, not only in transient toasts.

### Content Pass

1. Make the primary action and page purpose clear within the first scan.
2. Replace vague labels with task-specific verbs and nouns.
3. Remove filler claims, fake metrics, fake testimonials, and decorative copy.
4. Check empty, loading, error, success, and destructive-action copy for recovery guidance.

### Motion Pass

1. Assign motion purpose: orientation, feedback, hierarchy, continuity, or delight.
2. Keep durations consistent: 120-180ms for micro feedback, 220-360ms for view transitions, 500ms+ only for narrative motion.
3. Use one easing family across a project.
4. Provide `prefers-reduced-motion` behavior.

---

## Variant Strategy

When exploring variants, vary one or two meaningful axes per option instead of randomly changing colors.

Useful variant axes:

- Layout: split pane, card grid, table-first, timeline, canvas, editorial narrative.
- Density: spacious, balanced, operational.
- Tone: technical, warm, premium, playful, cinematic.
- Interaction: direct manipulation, wizard, inspector, command palette, saved views.
- Visual material: flat, bordered, glass, tactile, editorial, terminal-like.

Name variants by intent, not style trivia:

- "Operations Console" instead of "Dark Blue"
- "Editorial Product Story" instead of "Big Hero"
- "Dense Analyst Workspace" instead of "Table Version"

---

## Polish Checklist

Use this when a design is functional but not strong enough:

- Remove filler before adding decoration.
- Strengthen one focal point per screen.
- Tighten spacing rhythm: related items closer, sections further apart.
- Replace generic cards with task-specific structures where appropriate.
- Add visible but calm hover, focus, pressed, selected, loading, and disabled states.
- Add one domain-specific detail: chart annotation, real preview, timeline marker, status pulse, media crop, command result, or before/after comparison.
- Recheck mobile and text overflow after polish.
