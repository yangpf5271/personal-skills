---
name: web-page-integrator
description: |
  Build production-oriented frontend UI changes inside an existing web app: new business pages, admin pages, dashboards, forms, tables, detail views, and flow-driven screens that must be wired into the host project's routes, layout, components, tokens, permissions, data/state layer, and validation commands. Use when the user points at a repo/app or asks to add, modify, redesign, or integrate UI in an existing system from PRDs, screenshots, mockups, or business-flow specs with roles, states, transitions, or approval flows. Not for standalone HTML pages, prototypes, slide decks, or landing pages outside an app — those belong to `web-page-engineer` — nor pure back-end logic, CLI tools, data-processing scripts, or command-line debugging.
---

# Web Page Integrator

This skill is the codebase-integration sibling of `web-page-engineer`. It builds and modifies UI inside an existing frontend project. The output is production-oriented app code, not a standalone HTML preview, mock artifact, local demo, or separate design canvas.

The unit of work is a **host-app change**: route registration, page/component code, state/data integration, styling through existing tokens, permissions, validation, and project verification.

## Rule Priority

1. **Host app wins**: existing framework, router, layout shell, components, tokens, icon set, data layer, permissions, i18n, tests, and build commands override generic design advice.
2. **User-provided context wins**: PRDs, business specs, explicit constraints, and **decided design sources** — a `design-spec.md` from `web-page-engineer`, approved design mockups/images, or documents carrying design decisions — shape the change. An approved design source drives the visual layer, including the token updates it defines.
3. **System consistency wins over novelty**: new UI must look and behave like it belongs to the product.
4. **Production integration wins over preview speed**: do not create standalone HTML, vendored demo assets, scenario panels, parallel mock apps, or separate prototypes. If the request is for an independent preview/prototype, use `web-page-engineer` instead.
5. **Business behavior is part of UI**: roles, states, transitions, illegal actions, loading, empty, error, and permission variants must be represented in the host app.

---

## Step 0: Triage And Host Contract

Use this skill when the user asks to add, modify, redesign, or integrate front-end UI in an existing app. If there is no existing codebase, this skill is the wrong tool — use `web-page-engineer`.

Before writing code, identify the **host contract**:

- Framework and package manager: React/Vue/Svelte/Next/Nuxt, npm/pnpm/yarn, app scripts.
- Router and shell: route files, layout wrappers, navigation, breadcrumbs, tabs, page containers.
- Design system: tokens, theme files, component library, icon set, density, typography, spacing, radius.
- Page patterns: analogous list/detail/form/dashboard pages, table components, drawers/modals, empty/error/loading states.
- Data and state: existing API clients, query/store layer, schemas/types, API docs or OpenAPI specs (contracts designed but not yet implemented count as existing), form conventions, and any project-level mocks/fixtures/test data factories.
- Business guards: permissions, roles, feature flags, state-dependent action rules.
- Design sources (when the task has a decided direction): a `design-spec.md` handed over from `web-page-engineer`, approved design mockups or images, or documents carrying design decisions.
- Verification: lint, typecheck, tests, build, Storybook, dev server, browser smoke-test route.

State the host contract briefly before implementation when it affects design or file choices. Division of authority: the **current system** is read from code (source conventions decide how the app works today); the **target design** is read from design sources (a spec, mockup, or document is authoritative for the intended look — image-extracted values are approximate, so declare them as assumptions and confirm critical ones).

---

## Business Page Integration

Use this path for management-system pages, admin workflows, approval flows, MES/ERP/CRM screens, dashboards, data-entry pages, and any UI governed by roles, states, or transitions.

### 1. Model The Business UI

Extract before styling:

- **Actors and permissions**: who can see the page, which actions each role can take.
- **Business states**: status values, terminal states, partial states, failed states, and blocked states.
- **Transitions**: allowed actions, guarded actions, side effects, and illegal actions.
- **Screen inventory**: route/page, main task, visible states, data dependencies.
- **Scenarios**: happy path, one edge case, one blocked action, one empty/error/loading condition when relevant.

Use domain language in labels and messages. Labels read like the business, not the code.

**Ambiguity resolution — ask, don't guess.** When the flow document is unclear or conflicts with existing system behavior — undefined states or transitions, unspecified illegal actions, backend status enums that don't match the documented states, unclear role permissions — ask the user in grilling style (see the `grill-me`/`grilling` skill if present): one round at a time, every currently unblocked question numbered with your recommended answer, facts looked up from the codebase yourself rather than asked. Wait for the answers before the next round; stop when nothing is silently assumed. Ambiguities discovered later — during pattern selection or implementation — get the same treatment: stop and ask; never improvise a rule the flow model depends on.

For new or changed business flows, confirm the flow model with the user (one round) before producing the needs list and building screens — a wrong flow model poisons both the pages and the interface needs list.

### 2. Extend The Existing Design System

Declare the inherited design system once: density, type scale, table/form specs, status-color semantics, nav structure, spacing, radius, shadows, motion, and accessibility conventions.

If the host app has an established design system, extend it. Do not introduce a competing palette, font stack, spacing scale, icon library, CSS framework, or component primitive. An approved design source overrides this — its tokens and treatments replace the host's, per the design-source discipline.

If the host app is weak or inconsistent, use [references/admin-ui-baseline.md](references/admin-ui-baseline.md) only as a stabilizing baseline, then express it through the project's own tokens/classes/components.

### 3. Choose The Closest Local Pattern

Find the nearest existing page or component pattern before creating anything new:

- Tables for comparison and operational lists.
- Forms for data entry and approval inputs.
- Detail pages or split panes when list context must be preserved.
- Drawers/modals only when the host app already uses them for the same task type.
- Dashboards only when the user needs monitoring or decision support, not because a page needs visual decoration.

Every screen's layout follows that screen's task. If multiple screens share one skeleton only because it is easy to generate, redesign the outliers.

### 4. The Interface Seam — Needs List, Not API Design

Frontend responsibility ends at the interface seam. When pages require new or changed backend capabilities, produce a **page needs list** and hand it off; never design the API or the database yourself.

The needs list states WHAT each screen requires, in domain language:

- Data items displayed or edited per screen (business field names, formats, editability)
- List/query needs: filters, sort, pagination, expected data volume
- Actions: name, from-state → to-state, role permissions, side effects visible to the UI
- Error cases the UI must distinguish (e.g. permission denied vs. state-blocked vs. validation failed)
- Loading and empty conditions per screen

It must NOT contain HOW: no endpoints, HTTP methods, request/response schemas, error code numbers, tables, or storage design. Those belong to the interface and database owners.

Handoff channels:

- If the environment provides an interface design skill (e.g. `api-and-interface-design`), invoke it with the needs list to produce the contract, then return here and wire the page. The page skill orchestrates but never authors the contract.
- Otherwise hand the needs list to the user or backend team. Do not wait idle: wire the page through a **dev adapter** behind the data-access boundary — the adapter implements the agreed contract when one exists, otherwise the needs list (transitions follow the confirmed flow model). With a designed-but-unimplemented contract, write the real client against the contract and use the adapter as its runtime backing until the backend is live. The adapter is clearly marked dev-only, single location at the service layer, mechanically replaceable.

The needs list is delivered as a section of the final response (and written to the project's docs location if one exists), so the interface and database owners can consume it as-is.

Gap feedback: when a delivered contract cannot express something the UI needs, send it back as a needs-list amendment; never silently drop the requirement.

Contract arrival: when a contract lands after pages shipped on the adapter, reconcile it against the needs list (gaps become amendments), point the page at the real client, delete the adapter rather than leaving both paths, and re-run verification on the affected routes.

### 5. Implement In The Host App

Implementation order:

1. Host touchpoints: route, nav, layout shell, permissions, data entry point.
2. Data/state mapping: existing (including designed-but-unimplemented) API/query/store/schema contracts first; project mock/fixture/test-data mechanisms only when the host app already uses them; when no backend contract exists, produce the page needs list (section 4) and wire through its handoff channel.
3. Page/component structure: reuse existing components first; add new local components only when reuse would spread duplication or distort a pattern.
4. Business-state UI: enabled/disabled actions, terminal notes, blocked-action reasons, status tags, empty/loading/error states.
5. Responsive and accessibility pass: no text overflow, visible focus, keyboard path, semantic labels, field-level errors.
6. Project verification: lint/typecheck/tests/build/browser or Storybook smoke test.

For business flows, the source of truth is the host app's backend status, API contract, permissions, feature flags, and existing query/store layer. Implement UI gating with local guard/helper functions only when needed, such as `canApprove(record, user)` or `getAvailableActions(record, permissions)`. A formal state machine is optional and only appropriate when the host architecture already supports that pattern. Do not force a standalone mock controller into production code.

### Admin Conventions

- **One primary action per screen or action area**. Secondary buttons sit with a primary as Cancel/Back/Reset; destructive actions use the host danger treatment and always have text labels.
- **Button labels are verb(+noun)**, such as "提交审批" or "驳回申请"; avoid lone nouns and vague "确定".
- **Row actions: <=3 inline, rest in overflow**. Bulk workflows use the host checkbox and batch-action pattern.
- **Tables are operational surfaces**: toolbar above table, sticky header if the region scrolls, operation column far right, numeric columns right-aligned with tabular numbers.
- **Action triggers lock while submitting**. Loading buttons are disabled to prevent double submit.
- **Forms validate deliberately**: blur, debounced input, or submit, matching host convention. Field errors render near the field; toast alone is not enough.
- **Illegal-in-state actions stay visible when useful** and render disabled with a reason. Terminal records show a terminal note.

---

## Existing-UI Redesign Or Extension

Use this path when the task is visual refresh, layout improvement, component refinement, or design-to-existing-app implementation. It runs in one of two states, decided by whether a **design source** exists (see Step 0). In both states, the integrator never initiates token or visual-direction changes of its own.

**Without a design source — refine within the existing token system:**

- Read the existing vocabulary first: color ratio, density, spacing, hover/focus feedback, component anatomy, table/form patterns, icon style, motion, and copy tone.
- Preserve recognizable product behavior unless the user explicitly asks to change it.
- Improve by aligning, simplifying, clarifying hierarchy, and using existing primitives better — layout and polish only, tokens untouched.
- If the request asks for a *new look* rather than better execution, do not invent a direction: run `web-page-engineer`'s exploration first (review drafts + `design-spec.md`) and come back with an approved source.

**With a design source — execute the decided design:**

- Consume `design-spec.md` directly: tokens, shell & density, status-color semantics, and the delta-vs-current section. From mockup images or design-bearing documents, extract the design information and state assumptions for approximate or unstated values; confirm critical ones (brand color, status-color semantics) with the user per the ambiguity rules.
- The design source drives the visual layer, including token updates it defines — updating the host's token/theme values is in scope; replace the old treatment, never fork a parallel system. Host architecture still governs routing, components, and verification.
- The delta section is the scope contract: what it marks as kept must stay, what it marks as changed must land, and gaps go back to the user rather than being silently improvised.
- Translate the design into host components and tokens; never bolt it on as one-off CSS.
- Data or interface needs discovered during redesign follow section 4 (The Interface Seam).
- If the request is only a mockup or visual direction and there is no app to change, stop and use `web-page-engineer`.

---

## Technical Rules

### Codebase Integration

Follow [references/codebase-integration.md](references/codebase-integration.md).

- Reuse existing components before writing new ones.
- Keep route, permission, data-fetching, form, state, and i18n conventions identical to neighboring pages.
- Keep changes close to the feature boundary. Avoid unrelated refactors.
- Do not vendor this skill's libraries into the app. Use the host app's package manager and dependency policy.
- Do not create standalone HTML, React+Babel scripts, local demo pages, Tweaks panels, scenario balls, or review-only chrome.
- Do not use `file://` verification or `scripts/verify_artifact.py`; those belong to `web-page-engineer`'s standalone artifact delivery, which this skill does not produce.

### CSS And Design Tokens

- Use the host styling system: CSS modules, scoped CSS, Tailwind, styled components, theme tokens, or component props, whichever the project already uses.
- Use semantic tokens/classes for color. Avoid random hex values outside theme files.
- Track A/admin screens default to 14px body, 12px auxiliary text, around 32px controls, dense table rows 32-48px, unless the host system differs.
- Ensure visible `focus-visible`, sufficient contrast, and state not communicated by color alone.
- Use `font-variant-numeric: tabular-nums` or the host equivalent for money, counts, percentages, and durations.

### File Management

- Edit files where the host app expects the feature: routes, page modules, local components, stores/queries, tests, and styles.
- Split files when they exceed local norms or mix unrelated concerns.
- Add a new shared component only after checking existing shared/local components.
- Preserve user changes and unrelated work in the repository. Do not reformat broad areas or rewrite neighboring features to fit the new page. Exception when executing an approved design source: its delta section is the sanctioned change scope — updating the host's token/theme values is in scope and propagates naturally through CSS custom properties; do not additionally rewrite page markup across the app just because token values changed (per-page propagation is separately scoped by the user). Outside the delta, these preserve rules hold.

---

## Pre-Delivery Checklist

All integrated app changes:

- [ ] Host contract identified: framework, router/layout, component system, tokens, data/state layer, permissions, and available validation commands.
- [ ] Route/nav/layout integration follows host conventions; no orphan page or parallel shell.
- [ ] UI reuses existing components, tokens, icons, forms, tables, overlays, state conventions, and accessibility/i18n patterns.
- [ ] Design-source discipline holds: token/visual changes trace to an approved design source (`design-spec.md`, mockup, or design-bearing document); without a source, zero token changes — layout and polish only; image-extracted values declared as assumptions with critical ones confirmed.
- [ ] Data uses existing (or designed-but-unimplemented) API clients, schemas/types, query/store contracts, project-level mocks/fixtures, or a contract-pending dev adapter per the interface seam; new backend needs went out as a needs list through a handoff channel — never as page-authored API designs or hidden page-local mock data; stale adapters removed once their contract is live.
- [ ] Flow-model ambiguities resolved with the user in rounds (or explicitly declared as assumptions when the user defers); nothing silently assumed for new/changed flows.
- [ ] Business states represented: enabled/disabled actions, terminal notes, blocked reasons, loading, empty, and error states where relevant.
- [ ] Tables/forms follow admin density and task fit; numeric columns align correctly; operation column placement matches host pattern.
- [ ] Browser console clean on the changed route/component; no visible text overflow at target viewports.
- [ ] Accessibility basics pass: visible focus ring, field errors near fields, state not only by color, keyboard path for key actions.
- [ ] Host project checks run where available: lint, typecheck, relevant tests, build, Storybook/browser smoke test.
- [ ] New dependencies, skipped checks, assumptions, uncovered branches, and risk boundaries reported explicitly.

---

## Final Response

Lead with what changed in the app. Include:

- Files or routes changed.
- Host patterns reused.
- Business states/branches covered and not covered.
- Interface status: which capabilities the needs list covers, which channel it went to, which contracts arrived, and which pages remain dev-adapter-backed pending backend.
- Verification commands run and their results.
- Any skipped checks, new dependencies, assumptions, or remaining risks.

Do not tell the user to open a standalone HTML file or start a preview server unless that is the host app's normal verification path for the integrated route.

---

## Further Reference

- [references/codebase-integration.md](references/codebase-integration.md) — existing-app contracts, component reuse, routing/state/data conventions, project verification.
- [references/admin-ui-baseline.md](references/admin-ui-baseline.md) — fallback admin baseline for weak or incomplete host systems: tokens, density, shell, tables, accessibility.
- [references/components.md](references/components.md) — component selection by user task: navigation, tables, forms, feedback, overlays, mobile.
- [references/design-playbooks.md](references/design-playbooks.md) — audit, polish, responsive, and accessibility passes.
