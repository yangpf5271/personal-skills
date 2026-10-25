# UI Baseline

A shared operating baseline in two parts. **Part I · Universal** applies to any product UI — admin systems, portals, marketing pages, standalone artifacts. **Part II · Admin / B-end** stacks on top of Part I for management-style surfaces.

Scope rules:

- C-end surface (marketing site, portal, consumer page): Part I plus the product's own conventions; Part II does not apply.
- Admin / B-end surface: Part I + Part II together.
- Host or product conventions override the baseline wherever they exist; it fills gaps, never competes.

## Part I · Universal

### Visual Consistency Sweep

The classic "looks messy but cannot say why" causes — sweep all of them in one pass:

- Icons: one icon set, one stroke weight, stepped sizes (16/20); icons vertically centered with adjacent text, 8px gap after.
- Data presentation: units and precision consistent per column type (money two decimals, counts integers); one date-time format across the page; empty values render "—" — never blank; numeric columns right-aligned with `font-variant-numeric: tabular-nums`.
- Truncation: long text and IDs use single-line ellipsis plus tooltip; headers never wrap; only prose columns wrap.
- Border discipline: prefer spacing and background shifts over extra borders; kill double borders and redundant dividers; inner table lines one step lighter than outer frames.
- Elevation budget: shadows belong to floating layers; cards use borders or the lowest shadow step, never stacked shadows.

### Interaction And Accessibility

- Every interactive control covers hover, active, focus-visible, disabled, and loading where applicable.
- Disabled controls stay visible when they explain state or permissions; pair them with a reason tooltip or inline note.
- Focus rings must be visible. Use a 2px ring with offset or an equally clear system treatment.
- Body text contrast should meet WCAG AA 4.5:1; large text and meaningful graphics should meet 3:1.
- State is never communicated by color alone. Pair color with text, icons, tags, or helper copy.
- Field validation renders under the field with a visible error state; toast alone is not enough for form errors.

### Scroll Mechanics

- Inner scroll regions set `overscroll-behavior: contain` — scrolling to the end of a list must not chain to the page behind it.
- Reserve `scrollbar-gutter: stable` on scrolling containers so content does not shift when a scrollbar appears or disappears.
- Sticky elements fail silently when any ancestor has `overflow: hidden/auto/scroll` — keep sticky regions free of overflowed ancestors.
- Anchor targets behind sticky bars get `scroll-margin-top` so they are not obscured on jump.
- Sticky headers/toolbars stay compact, opaque, and unanimated; they trade viewport space, so they must earn it (NN/g).
- While a modal or drawer is open, lock body scroll; the overlay panel scrolls internally with its header and footer pinned.

### Action Placement Grammar

Baseline rules for where actions live, how they align, and how they wrap. Host conventions override these when they exist (sources: Ant Design button placement and list-page patterns, Carbon toolbar guidance, GOV.UK one-primary rule; wrap rules field-validated by real mock-review failures).

**One action zone per region — never duplicate:**

- Page-level actions: page header — title left, actions right.
- List-level actions: toolbar above the list; row actions at the end of the row.
- Form-level actions: the form footer slot at the bottom.
- The same action never appears in two zones. A standalone button lives in the zone of the thing it owns: "新建" belongs to the list → list toolbar, not beside the page title unless the page is that list.

**Toolbar composition:**

- Left: title, filters, query controls; right: batch actions and primary actions. Pagination right-aligned below the list.
- Search inputs are fixed-width — they must not squeeze the right-side buttons out of their row.
- Batch actions appear only after selection (with the selected count), inside the toolbar.

**Wrapping discipline:**

- A button group never breaks internally (`white-space: nowrap` on the group). When a bar overflows, it wraps by whole groups, never scattered single buttons.
- No `margin-left: auto` pushing buttons right while relying on no-wrap — under space pressure the behavior goes uncontrolled. Use flex with a gap between explicit left/right containers, or grid regions.

**Bottom alignment:**

- Form footers and dialog actions: right-aligned, primary rightmost (Ant Design / Element / TDesign B-end convention; Windows desktop puts the primary leftmost — pick one and stay consistent system-wide).
- The form footer sits in a fixed slot; buttons do not float with content flow. A submitting trigger locks (disabled) to prevent double submits.
- Very long forms may repeat the submit bar at the top as well (reduces scroll cost); follow the host convention.

### Page Assembly

**Card grids:**

- Equal height per row: `align-items: stretch` and `height: 100%` on the card container (not its body); row content top-aligned, row actions bottom-aligned.
- Gaps 16/24; widths and heights stay on the base spacing grid; columns collapse 4→2→1.
- Empty cards keep a minimum height instead of collapsing.

**Page anatomy:**

- Page header quartet: breadcrumb / title + description / right-aligned actions / tabs.
- Forms and long text inside wide layouts cap to a readable column (~720-840px, centered) — controls do not stretch across a 1600px viewport.

## Part II · Admin / B-end

### Posture

- Default posture: dense, restrained, task-first admin UI.
- Visual references: Ant Design-style Chinese admin density, Fluent command-and-form discipline, Carbon productive table density.
- Avoid consumer-page signals: oversized hero typography, decorative section cards, soft gradients, and one-off accent colors.

### Shell, Layout, And Scrolling

- Full-viewport shells: `html`/`body` height locked, the shell grid never scrolls, only data regions scroll internally (list body, content column); every flex level on the scroll chain needs `min-height: 0` or the pattern silently fails.
- Shell: left navigation 200-264px, collapsible to 48-80px; top bar 44-64px; content padding 16-24px.
- Surfaces: page background light gray; content containers white; 1px borders and restrained shadows.
- Tables: toolbar above table, sticky header for scrolling regions, row dividers or zebra rows, operation column at the far right.

### Token Baseline (B-end values)

The token pattern is universal — semantic custom properties, no rogue hex outside token declarations. The values below are B-end defaults:

```css
:root {
  /* Spacing: 4px atom, 8px main grid */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;

  /* Radius: three useful tiers */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-full: 999px;

  /* Typography: B2B/admin 14px base */
  --font-xs: 12px;
  --font-base: 14px;
  --font-lg: 16px;
  --font-xl: 20px;
  --font-2xl: 24px;
  --font-3xl: 30px;
  --line-height: 1.5;

  /* Controls */
  --control-h: 32px;
  --control-h-sm: 24px;
  --control-h-lg: 40px;

  /* Color: one brand color, neutral surfaces, semantic status colors */
  --brand: #1677ff;
  --brand-hover: #4096ff;
  --brand-active: #0958d9;
  --success: #52c41a;
  --warning: #faad14;
  --error: #ff4d4f;
  --text-1: rgba(0, 0, 0, .88);
  --text-2: rgba(0, 0, 0, .65);
  --text-3: rgba(0, 0, 0, .45);
  --bg-page: #f0f2f5;
  --bg-container: #fff;
  --border: #e5e6eb;

  /* Shell */
  --header-h: 48px;
  --sider-w: 220px;
  --sider-w-collapsed: 64px;

  /* Elevation */
  --shadow-1: 0 1px 2px rgba(0, 0, 0, .06);
  --shadow-2: 0 4px 12px rgba(0, 0, 0, .12);
  --z-popup: 1000;
}
```

### Density And Type

- Admin body text defaults to 14px; auxiliary text bottoms out at 12px.
- Default controls are 32px high; compact controls may use 24-28px when the task needs high density.
- Table rows usually sit between 32px and 48px, depending on density and secondary text.
- Headings use only the needed steps: 16px section titles, 20-24px page titles, 30px only for rare overview pages.
- Non-admin surfaces use their own conventions — do not import these density defaults.

### Form And Filter Machinery

**Forms:**

- Horizontal forms use one unified label-column width, grid-aligned with the controls.
- Control width reflects the expected content length — short codes narrow, long text wide — and stays on the spacing grid; never one width for everything.
- Filter forms default to three columns (advanced-search convention); long forms keep the submit bar sticky, with a shadow once the form scrolls.
- Drawer width tiers: 378px default, 736px large (Ant Design convention).

**Filter bars:**

- Filters beyond one row collapse to an expand/collapse toggle, collapsed by default with the common items visible.
- Active filters stay visible and persist; overflow filters move into a popover; query/reset stay inline with the fields (see Action Placement Grammar).

**Responsive degradation ladder:**

- ≥1280px full density; ~1024px side nav collapses to icons; ≤768px tables become cards or horizontal scroll. Functionality survives, layout degrades; breakpoints never change the information architecture.
