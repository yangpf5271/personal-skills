# Flow-Driven Admin UI — Track A Implementation Patterns

The business flow never appears as UI. It lives in one pure state machine that *controls* the pages: which actions are enabled, how a record's view varies by state. The artifact must read as a real management system; the only demo affordance is a collapsible scenario panel behind a draggable floating ball.

## The Pure State Machine (Internal Controller)

One `<script>` block (or file) holding all transition logic, written so it could be lifted into the real codebase unchanged.

Rules:

- No DOM, no `document`, no event handlers inside it. The page calls into it; nothing flows back.
- Pure where possible: given `(state, action)` → new state.
- The machine is **never rendered**. The UI asks it "what is legal right now" (`can(state, action)`) and obeys; it never displays the machine itself.

Skeleton (explicit machine with guards and roles — trim to the decision-rich parts for your domain):

```js
const machine = {
  roles: ['applicant', 'approver', 'finance'],
  states: ['draft', 'pending', 'approved', 'rejected', 'withdrawn'],
  initial: 'draft',
  // action: { from: [...], to, roles: [...] }
  actions: {
    submit:   { from: ['draft'],            to: 'pending',  roles: ['applicant'] },
    approve:  { from: ['pending'],          to: 'approved', roles: ['approver'] },
    reject:   { from: ['pending'],          to: 'rejected', roles: ['approver'] },
    withdraw: { from: ['draft', 'pending'], to: 'withdrawn', roles: ['applicant'] },
  },
};

// { ok: true, state } or { ok: false, reason } — never throws
function dispatch(state, action) { /* check from-states, apply or explain */ }
// what the UI asks before rendering each action button
function can(state, action) { /* legal right now? + why-not reason */ }
```

## State-Gated Actions

- Action illegal in the record's current state → render **disabled** with a reason tooltip ("打款仅在审批通过后可用"). A disabled-with-reason button is the visible evidence that the flow logic governs the page — no console needed.
- Terminal records → the whole action area disabled, with a terminal note.
- Role dimension: by default render the **max-permission union** (all action areas visible; see below). Only when the design explicitly requires showing permission differences, add a role-perspective toggle *inside the scenario panel* — never in the system UI.

## Max-Permission View (Default Rendering Strategy)

Every screen in the nav; every action area rendered, regardless of which role owns it. Rationale: the deliverable is qualified pages — the reviewer must see the full UI surface at a glance, and permission enforcement is a backend concern, not a page-design one. Do not build login simulation or role switchers by default.

## View Variants per State

Each screen renders from record state: status badge, banners (e.g. rejection reason on a rejected record), the state-gated action area, disabled/pending states of actions mid-transition. Variants of a screen are derived views from the same state store, not separate copies.

## Seed Data Discipline

- Realistic density: believable records in realistic volume (a dozen+ rows for lists, full fields, working filters) — the page must look like a system in daily use, not a three-row demo.
- Consistent across screens: the same record shows the same data everywhere.
- Coverage: at least one record per business state; one known initial state per scenario.

## Scenario Panel (the Only Demo Chrome)

A draggable floating ball (bottom-right by default) styled as clearly-not-part-of-the-system demo chrome. Click opens a panel containing:

- **Scenario list** — one click resets the in-memory seed data to that scenario's known initial state and navigates to the screen where it plays out (happy path, big-amount branch, reject loop, boundary value…).
- **Record-state overview** — a compact table of current records and their business states.
- **Variant tweaks**, if the artifact has any, as a section in the same panel — one floating control, not two.

Fully hidden when closed: during presentation the artifact looks like nothing but the system.

## Full-Viewport Shell, Inner Scrolling

The management system must not scroll as a page. The shell (sidebar + topbar) is pinned to the viewport; vertical scrolling happens only inside the regions that own the data.

```css
html, body { height: 100%; overflow: hidden; }          /* kill page scroll */
#app { height: 100vh; display: grid; grid-template-columns: 224px minmax(0, 1fr); }
.main  { display: flex; flex-direction: column; min-height: 0; }
.top   { flex: none; }                                    /* topbar pinned */
.view  { flex: 1; min-height: 0; overflow-y: auto; }      /* scroll region */
/* list screens: pin the toolbar, scroll only the table */
.view--list   { display: flex; flex-direction: column; overflow: hidden; }
.card--table  { flex: 1; min-height: 0; display: flex; flex-direction: column; }
.tblwrap      { flex: 1; min-height: 0; overflow: auto; }
.tbl thead th { position: sticky; top: 0; z-index: 1; background: var(--surface); }
```

- **The `min-height: 0` lines are load-bearing**: flex children default to `min-height: auto` and refuse to shrink below their content — without it the pattern silently fails and the page scrolls again.
- Non-list screens (detail, article) keep the pinned shell but may scroll the whole `.view` content column.
- Exempt mobile: under a narrow breakpoint restore natural page scrolling (`html, body { height: auto; overflow: auto }`) — fixed 100vh shells are hostile on touch.

## Wiring Screens in a Standalone Artifact

- One shared shell component across screens: nav, layout.
- Screen routing: a `screen` field in state (or hash routing) — no framework router needed.
- Respect the React hard rules from the main skill: namespaced style objects, `Object.assign(window, {...})` for cross-file components, no `scrollIntoView`.
- Artifact shape: small folder — entry HTML + `flow-machine.js` + `seed.js` + `styles.css`; JSX inlined in one `text/babel` block (file:// constraint).

## Liftoff

When the design is accepted, the machine module moves into the real codebase as-is; the HTML shell stays behind. State in the closing summary: which branches the build covered, which remain uncovered, which assumptions shipped.
