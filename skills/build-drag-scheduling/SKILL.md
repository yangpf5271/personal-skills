---
name: build-drag-scheduling
description: Build or rebuild an APS-style drag scheduling feature set with a framework-agnostic gantt board, daily aggregate matrix, task chip drag and drop, dual resequencing semantics, confirmation and progress dialogs, polling, refresh, and focus restoration. Use when Codex needs to generate, refactor, or port drag scheduling behavior from requirement docs into React, Vue, or other frontend stacks, especially when the target must match APS drag scheduling workflow rather than a generic gantt chart.
---

# Build Drag Scheduling

## Overview

Implement drag scheduling as a coordinated workspace, not as an isolated chart widget. Start from framework-neutral roles, contracts, and event semantics, then map them into the target stack's component, hook/composable, and service structure.

## Quick Start

- Read `references/rebuild-spec.md` before writing code when the user needs a full APS-like rebuild.
- Read `references/framework-mapping.md` after identifying the target stack.
- Read `references/acceptance-checklist.md` before finishing or reviewing an implementation.

## Required Delivery Model

Treat the feature as these cooperating modules:

- `DragSchedulingWorkspace`
- `GanttTimelineBoard`
- `TaskDragController`
- `TimelineLayoutAdapter`
- `ResequenceGateway`
- `ResequenceProgressDialog`

Do not collapse the feature into a single gantt component unless the user explicitly asks for a reduced scope. If the user only requests the visual board, still preserve the neutral input and output contracts so the page layer can add confirmations, polling, refresh, and focus restoration later.

## Workflow

1. Identify the target stack, routing model, state model, and styling constraints.
2. Map the neutral modules and contracts from `references/rebuild-spec.md` into the target project structure.
3. Implement `GanttTimelineBoard` with both timeline mode and daily aggregate matrix mode.
4. Limit drag initiation to task chips inside the aggregate popover and emit only the minimum payload on drop.
5. Implement page-layer interpretation for the two drag semantics:
   - Resource drag resequences a resource task and later operations.
   - Order drag shifts the work order start constraint and resequences the whole order.
6. Add confirmation handling, progress dialog state, backend polling, success refresh, tab switch, and focus restoration.
7. Verify behavior and visuals against `references/acceptance-checklist.md`.

## Non-Negotiable Rules

- Preserve framework-neutral names and contracts first. Treat Vue `props/emits`, React callback props, and equivalent patterns in other stacks as syntax-level mappings.
- Support drag and drop only in aggregate-by-day mode. Do not make the timeline bar the main drag entry.
- Use a clickable draggable task button for the aggregate task item. The same item must support both click and drag.
- Keep API submission outside the board. The board emits `item`, `targetDate`, and `rowId`; the workspace decides what that means.
- Block cross-row drag in the resource gantt.
- Block drag resequencing while the primary scheduling job is still running.
- Refresh data and restore focus after success. A matching-looking UI without focus recovery is not behaviorally complete.

## Implementation Notes

- Prefer a single board implementation shared by the resource and order tabs.
- Preserve sticky header, sticky left label column, orange drop-target feedback, and yellow bottleneck styling if the user asks for APS-like parity.
- If the backend does not exist yet, still define the `ResequenceGateway` interface and the progress-stage mapping so UI code does not bake business logic into the board.
- If the user provides an existing codebase, adapt to its design system and naming conventions while keeping the same responsibilities and event boundaries.

## References

- `references/rebuild-spec.md`: roles, contracts, drag semantics, API contract, polling, and visual behavior.
- `references/framework-mapping.md`: React, Vue, and framework-neutral mapping guidance.
- `references/acceptance-checklist.md`: final parity checklist for implementation or review.
