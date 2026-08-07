# Framework Mapping

## Table of Contents

- Neutral-first rule
- React mapping
- Vue mapping
- Other stacks

## Neutral-First Rule

Start from responsibilities and contracts, not from file names in a source project.

- Input means component props or equivalent inbound API
- Output event means emit, callback prop, signal, or event dispatcher
- Controller means hook, composable, store action, or service
- Workspace means page component, route component, or feature shell

Use neutral names in design notes first:

- `DragSchedulingWorkspace`
- `GanttTimelineBoard`
- `TaskDragController`
- `TimelineLayoutAdapter`
- `ResequenceGateway`
- `ResequenceProgressDialog`

## React Mapping

Suggested files:

- `pages/DragSchedulingWorkspace.tsx`
- `components/GanttTimelineBoard.tsx`
- `components/ResequenceProgressDialog.tsx`
- `hooks/useTaskDragHandler.ts`
- `hooks/useGanttTimeline.ts`
- `services/resequenceGateway.ts`

Suggested interface names:

- `onDateDrop`
- `onBarClick`
- `onClose`
- `onConfirm`

Implementation notes:

- Keep business mutations in the workspace or controller hook, not inside the board component
- Let the board remain controlled by props for focus and selection recovery
- Treat tab switch, refresh, and focus restoration as page behavior

## Vue Mapping

Suggested files:

- `views/DragSchedulingWorkspace.vue`
- `components/GanttTimelineBoard.vue`
- `components/ResequenceProgressDialog.vue`
- `composables/useTaskDragHandler.ts`
- `composables/useGanttTimeline.ts`
- `api/resequence.ts`

Suggested interface names:

- inputs through `props`
- outputs through `emit("date-drop")`
- outputs through `emit("bar-click")`

Implementation notes:

- Keep drag and polling state in composables or the page layer
- Keep the board presentational except for local hover or drag UI state

## Other Stacks

For Svelte, Angular, Solid, Web Components, or custom component systems:

- Keep the neutral module split
- Keep the board contract stable
- Keep drop payload minimal
- Keep resequencing semantics in a higher-level controller or page layer
- Keep progress polling and focus restoration outside the board

If the stack lacks popovers or sticky table primitives, approximate them without changing the underlying event model.
