# Track A Admin UI Baseline

Use this reference when Track A has no existing product UI, brand system, or user-provided design system to extend. It is a stable operating baseline for management-system pages, distilled from mature admin systems such as Ant Design, Fluent, and Carbon productive mode.

## Default Visual Reference

- Default posture: dense, restrained, task-first admin UI.
- Visual references: Ant Design-style Chinese admin density, Fluent command-and-form discipline, Carbon productive table density.
- Avoid consumer-page signals: oversized hero typography, decorative section cards, soft gradients, and one-off accent colors.

## CSS Token Baseline

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

Use colors through semantic custom properties. Outside the token declaration, avoid random hex values and ad hoc `rgba()` variants unless they derive from declared tokens.

## Layout Baseline

- Shell: left navigation 200-264px, collapsible to 48-80px; top bar 44-64px; content padding 16-24px.
- Surfaces: page background light gray; content containers white; 1px borders and restrained shadows.
- Forms: single column by default; multi-column only for tightly related fields. Keep label alignment consistent within the system.
- Tables: toolbar above table, sticky header for scrolling regions, row dividers or zebra rows, operation column at the far right.
- Numeric columns: right-align values and use `font-variant-numeric: tabular-nums` for counts, money, percentages, and durations.

## Density And Type

- Track A body text defaults to 14px; auxiliary text bottoms out at 12px.
- Default controls are 32px high; compact controls may use 24-28px when the task needs high density.
- Table rows usually sit between 32px and 48px, depending on density and secondary text.
- Headings use only the needed steps: 16px section titles, 20-24px page titles, 30px only for rare overview pages.
- Track B visual pages may use larger type and touch targets; do not import those defaults into dense admin screens.

## Interaction And Accessibility

- Every interactive control covers hover, active, focus-visible, disabled, and loading where applicable.
- Disabled controls stay visible when they explain state or permissions; pair them with a reason tooltip or inline note.
- Focus rings must be visible. Use a 2px ring with offset or an equally clear system treatment.
- Body text contrast should meet WCAG AA 4.5:1; large text and meaningful graphics should meet 3:1.
- State is never communicated by color alone. Pair color with text, icons, tags, or helper copy.
- Field validation renders under the field with a visible error state; toast alone is not enough for form errors.
