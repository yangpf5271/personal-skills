# Drag Scheduling Rebuild Spec

This reference is distilled from `APS_DRAG_SCHEDULING_COMPONENT_REBUILD.md` and reorganized for reusable skill consumption.

## Table of Contents

- Core outcome
- Neutral module map
- Board contract
- Drag semantics
- Interaction sequence
- Backend contract
- Progress dialog
- Visual language

## Core Outcome

Rebuild the APS drag scheduling experience as a composed feature, not as a standalone gantt chart skin. The minimum complete scope is:

- A workspace with resource and order tabs
- A shared gantt board
- Daily aggregate matrix mode
- Expandable task chips inside each date cell
- Drag and drop from task chips to target dates
- Confirmation before resequencing
- Progress dialog with polling
- Refresh, tab restore, scroll, and focus after success

## Neutral Module Map

Use these neutral names even if the project later maps them into framework-specific files:

| Neutral name | Responsibility |
| --- | --- |
| `DragSchedulingWorkspace` | Compose tabs, filters, dialogs, polling, refresh, and focus |
| `GanttTimelineBoard` | Render timeline mode and aggregate matrix mode; emit board events only |
| `TaskDragController` | Hold drag context, submit resequencing, normalize errors |
| `TimelineLayoutAdapter` | Normalize ranges, build ticks, compute bar positions, clip ranges |
| `ResequenceGateway` | Submit resequence jobs and query job status |
| `ResequenceProgressDialog` | Show fixed progress steps and success or failure output |

## Board Contract

Treat the board as a reusable view component. It does not own business meaning.

```ts
type GanttTimelineBoardProps = {
  rows: TimelineRow[]
  startTime: string | Date
  endTime: string | Date
  emptyText?: string
  labelTitle?: string
  aggregateByDay?: boolean
  enableDateDragDrop?: boolean
  focusRowId?: string | null
  focusItemId?: string | null
  onBarClick?: (payload: unknown) => void
  onDateDrop?: (payload: { item: unknown; targetDate: string; rowId: string }) => void
}

interface TimelineRow {
  id: string
  label: string
  subLabel?: string
  highlightVariant?: "bottleneck"
  items: TimelineItem[]
}

interface TimelineItem {
  id: string
  label: string
  tooltip?: string
  start: string | Date
  end: string | Date
  status?: string
  highlightVariant?: "bottleneck"
  raw?: unknown
}
```

Resource drag requires `raw` to include:

- `task_id`
- `resource_id`
- `start_time`
- `end_time`
- `work_order_no`
- `seq_no`

Order drag requires `raw` to include:

- `task_id`
- `planned_start_time`
- `planned_end_time`
- `work_order_no`

## Drag Semantics

Do not treat every drag as the same operation.

### Resource Gantt

Meaning:

- Move the resource task to the target date
- Use that task as the resequencing anchor
- Resequence later operations and affected tasks

Required scope:

- `resequenceScope = "resource_task"`

Cross-row rule:

- Allow drag only inside the original resource row
- If `resource_id !== rowId`, block immediately
- Do not open confirmation
- Do not send a request

### Order Gantt

Meaning:

- Change the earliest start date of the work order
- Use that date as the new order-level scheduling constraint
- Resequence the entire work order

Required scope:

- `resequenceScope = "work_order_start"`

### Shared Rules

- Support drag only in `aggregateByDay = true`
- Start drag from the aggregate popover task chip, not the timeline bar
- Use a `button` for the task chip so click and drag share the same interactive element
- Emit only `item`, `targetDate`, and `rowId`
- Block drag resequencing while the primary scheduling job is running

## Interaction Sequence

Follow this sequence for both tabs:

1. Expand a date cell to reveal task chips.
2. Start drag from a task chip button.
3. Highlight the target date cell.
4. Emit `date-drop` from the board on drop.
5. Validate at the workspace layer.
6. Show the tab-specific confirmation copy.
7. On confirm, open the progress dialog.
8. Save drag context in `TaskDragController`.
9. Submit resequencing through `ResequenceGateway`.
10. Start polling with the returned `job_id`.
11. Map backend job stages into the fixed five-step progress UI.
12. Stop polling on success or failure.
13. Refresh data after success.
14. Switch to the correct tab, scroll to the target row or item, and highlight it.

Also preserve:

- Auto-expand and scroll when `focusRowId`, `focusItemId`, `rows`, or `aggregateByDay` changes
- Polling cleanup on page destroy or unmount

## Backend Contract

Submit resequencing with:

```ts
POST /aps/scheduling/tasks/{taskId}/resequence

{
  target_date: string
  anchor_policy: "resource_first_work_slot"
  resequence_scope?: "resource_task" | "work_order_start"
  scheduling_unit_id?: string
  work_order_no?: string
  seq_no?: number
}
```

Poll job status with:

```ts
GET /aps/scheduling/tasks/resequence-jobs/{jobId}

{
  job_id: string
  task_id: string
  status: string
  stage: string
  progress_pct: number
  stage_message?: string
  resolved_anchor_start_time?: string
  affected_task_count: number
  affected_work_order_count: number
  warnings: string[]
  error_message?: string | null
}
```

## Progress Dialog

Keep five fixed UI steps:

1. `submit`
2. `scope`
3. `backend`
4. `persist`
5. `refresh`

Map backend stages like this:

```ts
submitted     -> submit
loading_scope -> scope
rescheduling  -> backend
persisting    -> persist
completed     -> persist
```

Map stage labels like this:

```ts
submitted     -> 提交重排请求
loading_scope -> 加载影响范围
rescheduling  -> 后端重排计算
persisting    -> 保存重排结果
completed     -> 刷新甘特结果
not_found     -> 查询重排状态
```

Polling rules:

- Poll every 3 seconds by default
- Retry after 5 seconds when the backend reports excessive frequency
- Stop on success
- Stop on failure
- Stop on page destroy or unmount

Success output must include:

- `重排成功`
- affected task count
- affected work order count
- resolved anchor time when present

Failure output must include:

- `重排失败`
- failed stage
- backend error message

## Visual Language

Preserve these visual traits when the goal is APS-like parity:

- Light industrial admin look
- Blue-gray palette
- Card containers with large radii
- White to light blue-gray gradients
- Soft shadows
- Sticky table header
- Sticky left label column
- Orange drop-target feedback
- Yellow bottleneck state

Key dimensions:

- left label column: `196px`
- day column: `92px`
- timeline min width: `max(420px, dayCount * 95px)`
- scroll area max height: `560px`

Important interaction styling:

- date cell target highlight uses light orange gradient
- target cell shows orange dashed inner border
- summary button also shifts to orange tones
- empty target cells still show clear drop feedback
- task chips are colorful rounded cards with stronger shadow
- dragging chip scales down and reduces opacity
