# Component Decision Reference

Use this reference for component-heavy product UIs, dashboards, forms, tables, navigation systems, mobile app prototypes, and UX audits.

## Table of Contents

1. [Selection Principle](#selection-principle)
2. [Navigation](#navigation)
3. [Data Display](#data-display)
4. [Inputs](#inputs)
5. [Feedback](#feedback)
6. [Overlays](#overlays)
7. [Mobile](#mobile)

---

## Selection Principle

Choose components by user task first, visual style second.

| User task | Prefer | Avoid |
|---|---|---|
| Compare many records | Table, saved views, split filters | Decorative card grids |
| Monitor status | Dashboard grid, alert rail, compact charts | Charts with no decision attached |
| Create or edit structured data | Sectioned form, wizard, autosave, inline validation | Long ungrouped forms |
| Browse visual content | Cards, gallery, collections | Dense tables |
| Manage workflow | Kanban, queue, timeline, activity log | Static marketing sections |
| Configure settings | Grouped forms, clear defaults, preview/diff | Modal chains |
| Inspect one object from a list | Drawer, split pane, inspector | Full navigation jumps for minor edits |

---

## Navigation

- Sidebar: use for persistent multi-area products. Group only when there are many items.
- Top nav: use for marketing sites, simple apps, or a few primary destinations.
- Tabs: use for sibling views inside one object. Do not use tabs as primary site navigation.
- Breadcrumbs: use for deep hierarchy or object detail pages.
- Command palette: use for expert tools with many actions; implement real search if shown.
- Pagination: use when result count and position matter. Infinite scroll is better for casual browsing than precise workflows.

---

## Data Display

- Table: use for comparison, sorting, scanning, bulk actions, and precise values. Align numbers right, keep identifiers sticky when horizontal scroll is needed, and include empty and loading states. Keep at most 3 row actions inline with the rest in an overflow menu; bulk workflows add a checkbox column and a batch-action bar (select-all checkbox includes an indeterminate state).
- Cards: use for heterogeneous items, visual previews, or browse behavior. For operational/product structure, do not make every page section a card; use tables, lists, split panes, inspectors, or unframed sections when they match the task better.
- List: use for activity, messages, search results, tasks, and compact object collections.
- Metric tile: include label, value, timeframe, comparison, and meaning. Do not invent numbers.
- Chart: choose the simplest chart that answers the user's decision. Use semantic color, direct labels, and annotations where useful.
- Timeline: use for history, lifecycle, approvals, and incident narratives.

---

## Inputs

- Text input: always provide label, focus state, disabled state, and validation message when invalid.
- Select: use for 4-15 known options. For larger sets, use searchable combobox.
- Segmented control: use for 2-5 mutually exclusive modes that change the current view.
- Toggle: use for immediate binary settings. Use checkbox for multi-select or form submission.
- Slider: use when approximate adjustment is acceptable. Pair with numeric input when precision matters.
- Date range: provide presets, calendar, manual input, and timezone context when relevant.
- File upload: show accepted formats, size limits, progress, failure reason, and retry/removal.

---

## Feedback

- Empty state: explain why it is empty, what to do next, and whether this is normal. Avoid cheerful filler.
- Loading state: use skeletons for layout-preserving content; use spinner only for unknown-duration actions.
- Error state: state what failed, consequence, recovery action, and diagnostic detail where useful.
- Toast: use for temporary confirmation. Do not use as the only place for critical errors.
- Inline validation: validate near the field, on a deliberate trigger (blur or debounced input, not every keystroke); show the error below the control, and on failed submit scroll to the first error. Preserve user input unless it is unsafe.
- Success state: confirm completion and show the next useful action.

---

## Overlays

- Modal: use for focused, interruptive decisions. Keep it short.
- Drawer: use for object detail or editing while preserving list context.
- Popover: use for lightweight choices or details.
- Tooltip: clarify unfamiliar controls. Do not hide required instructions in hover-only UI.
- Confirmation: reserve for destructive or irreversible actions. Prefer undo for low-risk actions.

---

## Mobile

- Use bottom navigation for 3-5 top-level destinations.
- Keep primary actions thumb-reachable and at least 44px tall.
- Avoid hover-dependent interactions.
- Collapse dense tables into cards only when comparison is not the main task; otherwise keep horizontal scroll with sticky identifiers.
- Keep forms one column and group sections clearly.
