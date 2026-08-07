# Acceptance Checklist

Use this list before closing an implementation or during review.

- Both resource and order tabs use the same `GanttTimelineBoard`
- Both tabs run in daily aggregate mode
- Each date cell can expand into multiple task chips
- Drag starts from a task chip inside the aggregate detail layer
- Drag target cells show orange highlight and dashed feedback
- Resource drag is blocked across rows
- Resource drag and order drag use different confirmation copy
- Resource drag submits `resource_task`
- Order drag submits `work_order_start`
- Drag resequencing is blocked while primary scheduling is still running
- Drop emits only the task, target date, and target row ID
- Confirmation opens before resequencing submission
- Submission opens a progress dialog
- Progress dialog shows five fixed steps
- Polling stops on success, failure, and page destroy
- Success refreshes gantt data
- Success restores the correct tab
- Success scrolls to the affected row or item
- Success highlights the affected item
- Success shows affected task count and affected work order count
- Success shows resolved anchor time when available
- Failure shows failed stage and failure reason
- Sticky header and sticky left label column are preserved
- APS-like visuals preserve blue-gray base tones, orange drop feedback, and yellow bottleneck styling
