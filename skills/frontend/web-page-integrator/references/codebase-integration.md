# Existing Codebase Integration

Use this reference for UI work inside an existing frontend project. The deliverable is integrated application code: routes, pages, components, state/data wiring, styles through host tokens, tests, and project verification.

## Read The Host App First

Before designing or coding, identify the host app's actual contracts:

- Framework and router: React/Vue/Svelte/Next/Nuxt, route files, layout shells, navigation registration.
- Design system: tokens, theme files, component library, icon set, spacing/radius/type conventions.
- Page patterns: list/detail/form/dashboard shells, table components, empty/error/loading states, modal/drawer conventions.
- Data contracts: existing API clients, schemas/types, stores, query keys, state management, validation schemas, and project-level mocks/fixtures/test data factories.
- Business rules: route guards, role checks, permissions, feature flags, status-dependent actions.
- Design sources (when the task has a decided direction): a `design-spec.md` from `web-page-engineer`, approved design mockups or images, or documents carrying design decisions.
- Quality gates: package manager, lint, typecheck, test, build, Storybook or visual test commands.

Division of authority: code outranks screenshots **for the current system** — implementation follows the host app's source conventions. The **target design** is read from design sources: a spec, mockup, or document is authoritative for the intended look; image-extracted values are approximate, so declare them as assumptions and confirm critical ones.

## Integration Rules

- Reuse existing components before creating new ones. Add a new component only when no local pattern fits or duplication would otherwise spread.
- Extend the existing token/theme system. Do not introduce a parallel palette, spacing scale, font stack, icon library, CSS framework, or component primitive.
- Design-source discipline: token and visual-direction changes trace to an approved design source. Executing one — including the token updates a `design-spec.md` defines — is in scope; update the host's token/theme values rather than forking a second system. Without a design source, tokens stay untouched: layout and polish only. The integrator never initiates token or visual-direction changes of its own; a request for a new look without a source routes to `web-page-engineer` exploration first.
- Keep route, permission, data-fetching, form, state, validation, and i18n conventions identical to neighboring pages.
- Use existing interfaces before mocks. If the host app already has API clients, query hooks, schemas, DTOs, OpenAPI/GraphQL/RPC contracts, or service modules, wire the page through them. Contracts designed but not yet implemented count as existing.
- Use mock data only through project-level mechanisms such as MSW, mock server, fixtures, Storybook stories, test data factories, or existing dev adapters — a service-layer dev adapter created per the interface seam rules is the sanctioned fallback when no project mechanism exists. Do not hide page-local demo data inside production components.
- When the UI requires a new or changed backend capability, produce a page needs list — WHAT each screen requires in domain language: data items displayed/edited, list/query needs (filters, sort, pagination), actions with from-state → to-state and role permissions, error cases the UI must distinguish, loading/empty conditions. Hand it off: invoke the environment's interface design skill (e.g. `api-and-interface-design`) with the needs list, or give it to the user/backend team. Never author endpoints, HTTP methods, schemas, error codes, or database design from the page side. Deliver the needs list in the final response (and the project's docs location if one exists) so interface/database owners can consume it as-is.
- Until the real contract is implemented, wire the page through a dev-only adapter at the data-access boundary — it implements the agreed contract when one exists, otherwise the needs list; mark it dev-only, keep it in one place at the service layer, and report it as contract-pending. When a delivered contract cannot express a UI need, amend the needs list instead of silently dropping it. When the contract goes live, point the page at the real client and delete the adapter rather than leaving both paths.
- Keep changes close to the feature boundary. Avoid unrelated refactors while integrating UI. Exception: when executing an approved design source, its delta is the sanctioned scope (token/theme updates included); outside the delta, boundary and preserve rules hold — and do not rewrite page markup across the app merely because token values changed.
- Preserve existing accessibility conventions; add labels, focus states, error text, and keyboard behavior in the same style as the host app.
- For business flows, the source of truth is the host app's backend status, API contract, permissions, feature flags, and existing query/store layer. Implement UI gating with guard/helper functions only when needed; a formal state machine is optional and only appropriate when the host architecture already supports that pattern.
- Do not add demo-only chrome: scenario panels, floating review balls, local mock shells, alternate preview routes, or separate prototype surfaces. If the task is an independent preview/prototype, route it to `web-page-engineer` instead.

## Design Output Before Editing

Before changing files, briefly state:

- Host contracts found: framework, component system, routing/layout, data/state, validation commands.
- Design decision: which existing pattern the new or changed page follows.
- Risk boundary: files or modules expected to change, and anything intentionally left untouched.

## Verification

Use the host app's own gates, in this order when available:

1. Static checks: lint, typecheck, formatting check.
2. Unit/component tests for changed logic or components.
3. Build.
4. Browser or Storybook smoke test for the changed route/component.
5. Visual inspection for responsive behavior, text overflow, focus states, loading/empty/error states, and token consistency.

If a gate is missing or cannot run, say that explicitly and use the nearest available substitute. Verification means the integrated route/component works in the host app; a separate HTML preview is not a substitute.
