# Evidence Notebook Design Evolution Plan

## Design Thesis

Turn the Evidence Notebook from a strong static dashboard into a research-grade dossier interface: editorial enough to feel memorable, disciplined enough to support evidence review, and structured enough that every screen answers:

- What is currently true?
- What evidence supports it?
- What remains uncertain?
- What should happen next?

The product should evolve toward exceptionally crafted product UI with editorial character. It should not become a marketing page, generic SaaS dashboard, or decorative AI control room.

## Status Snapshot

This plan is now partly implemented in the deployable `site/` notebook.

Completed to date:

- `DESIGN.md` and `PRODUCT.md` are now active design inputs for the notebook.
- `site/assets/styles.css` has been consolidated around named visual tokens aligned to `DESIGN.md`.
- Non-overview views now use a more compact header treatment.
- Claims now render as a dossier reader with a left index and fixed Claim/Evidence/Uncertainty/Next action sections.
- Timeline now includes phase grouping, status treatment, and a "next visible move" panel.
- Artifacts now render as a grouped shelf instead of a flat register.
- Decisions now use an ADR-like structure with rationale, consequence, evidence, and derived markers.
- Sessions now render as an expandable ledger with tags and structured session metadata.
- Overview now includes a review-risk area to surface what should not be overclaimed.
- Responsive fixes have started, including rail collapse, header compaction, focus states, and table/path overflow control.

Still open or only partially complete:

- The overview and evaluation sections still need further polish at awkward intermediate viewport widths.
- The component-system pass is implemented in practice through CSS/DOM patterns, but not yet documented as a formal reusable system.
- Responsive QA is in progress, especially for dense evidence tables and other high-information blocks.

## Design Skill Operating Guidance

Use `impeccable` and `gpt-taste` together, but give them different jobs.

### Default Skill: `impeccable`

Use `impeccable` as the primary design discipline for this project because Evidence Notebook is product UI. It should be loaded for:

- UX critique;
- layout and hierarchy work;
- product interaction design;
- responsive behavior;
- accessibility and focus states;
- component system decisions;
- color, typography, and spacing refinement;
- final polish before shipping.

When using `impeccable`, treat this repository as `product` register. Load or respect:

- `PRODUCT.md` for product intent;
- `DESIGN.md` for visual tokens and design rules;
- `docs/evidence_notebook_design_evolution_plan.md` for the evolution path.

Decision rule: if a design choice improves trust, evidence review, scanability, accessibility, or repeat use, it belongs. If it only makes the screen more theatrical, cut it.

### Secondary Skill: `gpt-taste`

Use `gpt-taste` as a ceiling-raising critique lens, not as the literal implementation contract for the working notebook. It is most useful for:

- making safe layouts more distinctive;
- avoiding cramped six-line headings;
- improving editorial typography;
- finding stronger artifact-shelf compositions;
- adding memorable but controlled micro-interactions;
- designing separate presentation or visual-explainer surfaces.

Do not apply `gpt-taste` literally to every notebook screen. In particular, avoid:

- AIDA structure on inner product views;
- heavy GSAP choreography;
- random stock imagery;
- cinematic spacing that pushes evidence below the fold;
- decorative motion that does not communicate state.

Decision rule: borrow the ambition, not the spectacle.

### How To Combine Them

Use this order for future design sessions:

1. Start with `impeccable` to frame the product job, hierarchy, accessibility, and component behavior.
2. Use `gpt-taste` to challenge the result: is it memorable enough, well typeset, and visually decisive?
3. Return to `impeccable` to trim anything that harms task flow, evidence traceability, or product trust.
4. Validate final choices against `DESIGN.md`.

The final design should feel like an excellent research tool with editorial taste, not an award-site landing page embedded inside a dissertation project.

## Phase 1: Stabilize The Design Contract

Goal: make future design work consistent.

Status: substantially complete.

- Treat `DESIGN.md` as the visual source of truth.
- Treat `PRODUCT.md` as the product intent source.
- Refactor the current `site/assets/styles.css` toward named tokens:
  - paper surfaces;
  - ink text;
  - source ledger borders;
  - evidence teal;
  - warning amber;
  - semantic states.
- Remove duplicated or legacy CSS blocks if the generated file has accumulated repeated style layers.

Success test: a future agent can read `DESIGN.md` and generate a compatible screen without asking what the product should look like.

Completed notes:

- `DESIGN.md` now exists as the notebook visual contract.
- `PRODUCT.md` now exists as the notebook product-intent contract.
- `site/assets/styles.css` has already been reduced to a named token system and the previous repeated style drift has been consolidated.

## Phase 2: Fix Information Hierarchy

Goal: reduce repeated chrome and bring substance above the fold.

Status: mostly complete, with some viewport-specific polish still needed.

Keep the large "Evidence Notebook" editorial hero only on Overview. On Claims, Timeline, Sessions, Workstreams, Artifacts, and Decisions, use a compact header.

Inner screen structure:

```text
rail
compact top context
view title + one-sentence purpose
primary working content
secondary source/stats context
```

Specific improvements:

- Collapse source ledger into a compact "Sources" strip on inner views.
- Convert stats into smaller navigational counters.
- Keep search visible, but integrate it into the header instead of floating as a separate box.
- Make active view content start much higher.

Success test: on a 1440x1000 viewport, every view shows meaningful screen-specific content without scrolling.

Completed notes:

- The editorial hero is now effectively reserved for Overview while inner views use compact headers.
- Source ledger and stats are already compressed on inner views.
- Search is integrated into the header rather than rendered as a detached floating control.
- Above-the-fold usefulness has improved substantially across Claims, Timeline, Sessions, Workstreams, Artifacts, and Decisions.

## Phase 3: Redesign Each View Around Its Job

Goal: each screen gets a distinct information model, not the same panel treatment.

Status: largely complete for the first redesign pass.

### Overview

- Keep as the front page.
- Show current claim, active milestone, latest evaluation, latest decision, and next move.
- Add a compact review-risk area: what should not be overclaimed.

Completed notes:

- Overview now functions as the front page.
- Current claim, active research path, evaluation signal, recent sessions, artifact shelf, and latest decision are all surfaced.
- A review-risk panel has now been added.

### Claims

- Make it the canonical dossier reader.
- Left: claim index with status/risk markers.
- Right: selected claim with four fixed sections:
  - Claim.
  - Evidence.
  - Uncertainty.
  - Next action.
- Consider tabs or anchored subsections only if the content gets too long.

Completed notes:

- Claims now follow the intended dossier-reader split with a left index and fixed reading frame.
- Risk labels are already surfaced in the claim index.

### Timeline

- Group milestones by phase.
- Make active milestone visually dominant.
- Show complete, planned, blocked, and review-needed states.
- Add "next visible move" as a sticky right-side note.

Completed notes:

- Timeline now groups milestones into phases, distinguishes status visually, and includes the sticky next-move panel.

### Sessions

- Make recent sessions scannable as a ledger.
- Collapsed row should show date, title, outcome, and source log.
- Expanded row should show outcome, evidence, uncertainty, and handoff.
- Add tags for tests run, files changed, and generated artifacts if available.

Completed notes:

- Sessions now render as a ledger with stronger collapsed summaries.
- Expanded records already show outcome, evidence, uncertainty, and handoff.
- Tags and derived metadata for files changed, checks run, artifacts updated, and run evidence are now surfaced where available.

### Workstreams

- Treat each as a research lane.
- Show current question, latest evidence, risk/blocker, and next move.
- Add visual priority: active, waiting, blocked, watch.

Completed notes:

- Workstreams now render as research lanes with question, evidence, risk, and next move.
- Priority treatment for active, waiting, blocked, and watch is already implemented.

### Artifacts

- Make this the biggest redesign opportunity.
- Replace the flat table feel with a true shelf:
  - Active evidence.
  - Generated visuals.
  - Planned visuals.
  - Dissertation support.
- Each artifact should show purpose, status, path, source inputs, and intended use.
- This screen can be more visually distinctive than the others while staying source-backed.

Completed notes:

- Artifacts now render as grouped shelf sections rather than a flat table treatment.
- Current grouping includes Active evidence, Generated visuals, Session logs, Planned visuals, Dissertation support, and Source documents.

### Decisions

- Make it ADR-like.
- Structure each decision as:
  - decision;
  - rationale;
  - consequence;
  - evidence.
- Add markers for "governs future work," "reversible," "real-data governance," or "evaluation protocol" when available.

Completed notes:

- Decisions now render in an ADR-like record format.
- Derived markers are already shown for governance and protocol-related decisions.

## Phase 4: Component System Pass

Goal: one coherent interaction vocabulary.

Status: partly complete in implementation, not yet fully formalized in documentation.

Define and apply:

- `AppRail`
- `CompactHeader`
- `SourceLedger`
- `StatsStrip`
- `ClaimDossier`
- `EvidenceBlock`
- `UncertaintyBlock`
- `NextActionBlock`
- `TimelineMilestone`
- `SessionRecord`
- `WorkstreamLane`
- `ArtifactShelfItem`
- `DecisionRecord`

Each component needs:

- default state;
- hover state;
- focus state;
- active/current state;
- disabled or empty state where relevant;
- mobile behavior.

Success test: clickable things look clickable; selected things look selected; evidence links are never visually lost.

Completed notes:

- `AppRail`, `CompactHeader`, `SourceLedger`, `StatsStrip`, `ClaimDossier`, `TimelineMilestone`, `SessionRecord`, `WorkstreamLane`, `ArtifactShelfItem`, and `DecisionRecord` are now effectively present as working UI patterns.
- Focus-visible styling and selected/active states are already implemented across navigation, cards, buttons, and records.
- Remaining work is to formalize the component vocabulary and document the interaction states more explicitly.

## Phase 5: Motion, Carefully

Goal: add polish without turning the tool into a showpiece.

Status: complete.

Use motion only for:

- view transitions;
- expanding session records;
- claim selection changes;
- timeline active milestone reveal;
- artifact shelf hover or preview;
- source ledger collapse or expand.

Avoid:

- page-load choreography;
- decorative scroll effects;
- heavy GSAP unless building a separate presentation artifact.

Motion should be 150 to 250ms, ease-out, and state-driven.

## Phase 6: Responsive And Accessibility Pass

Goal: make the notebook usable on laptop, tablet, and mobile.

Status: in progress.

Checks:

- Left rail collapses cleanly on mobile.
- Search remains reachable.
- Claim index becomes horizontal or drawer-like on small screens.
- Tables and artifact paths do not overflow.
- Focus states are visible.
- Link contrast passes.
- Long run IDs and paths wrap intelligently.
- No content requires hover only.

Success test: mobile view still answers "what is true, what proves it, what is next?"

Completed notes:

- The rail already collapses on smaller widths.
- Search remains present and reachable.
- Focus-visible styling is present on all interactive controls.
- `a:focus-visible` rule now applies the amber outline to content links, not just chrome controls.
- Long paths and run IDs now wrap more safely.
- Table overflow handling has been improved, though dense tables still need more layout-specific treatment in some overview contexts.
- Skip navigation link added (`#main-content` target on the `<main>` element), visible on focus.
- ARIA landmark labels added: `aria-label="Site navigation"` on rail nav, `aria-label="Evidence Notebook home"` on the EN mark.
- `aria-current="page"` now marks the active rail button on every render.
- `aria-pressed` now marks the selected claim in the claim index (true/false per button).
- `aria-live="polite"` region added to the static HTML; view changes trigger a textContent announcement so screen readers hear "Claims view", "Timeline view", etc.
- Source card links now carry an explicit `aria-label` so screen readers announce label and freshness without the redundant "Source" prefix.
- Decorative elements (rail timestamp paragraph, source card "Source" label) marked `aria-hidden="true"`.

## Phase 7: Implementation Strategy

Use three build passes.

### 1. CSS And Token Pass

- Normalize colors, type, spacing, and borders.
- Align styles with `DESIGN.md`.
- Remove repeated style drift.
- Keep current DOM mostly intact.

### 2. Layout Pass

- Compact inner headers.
- Redesign per-view structure.
- Improve above-the-fold usefulness.

### 3. Interaction And Content Pass

- Improve claim selection.
- Improve expandable sessions.
- Group and enrich the artifact shelf.
- Add timeline state treatment.
- Run accessibility and responsive QA.

## Recommended First Sprint

Start with these five changes:

1. Compact the header on non-overview views.
2. Redesign Claims into a stronger dossier reader.
3. Redesign Artifacts into a shelf grouped by purpose.
4. Add phase and status treatment to Timeline.
5. Tokenize CSS against `DESIGN.md`.

This gives the biggest improvement without destabilizing the whole generated notebook.

Status update:

All five recommended first-sprint items have now been implemented in the current notebook.

Suggested next sprint:

1. Continue responsive and viewport-specific cleanup on Overview and the evaluation block.
2. Formalize the component-system vocabulary in code comments or design docs.
3. Decide whether the evaluation evidence area should remain table-first or move to a comparison-summary pattern on narrower laptop widths.
4. ~~Add a minimal motion pass for session expansion, claim switching, and artifact hover states.~~ Complete (commit 8a85138).
5. ~~Run a deliberate accessibility QA pass across keyboard navigation, contrast, and small-screen reading order.~~ Complete: skip link, ARIA landmarks, `aria-current`, `aria-pressed`, live-region announcements, content link focus styles.

## References

- `DESIGN.md`
- `PRODUCT.md`
- `site/index.html`, `site/assets/styles.css`, `site/assets/app.js`
- `docs/agent_visibility_plan.md`
- `docs/visual_artifacts_direction.md`
