# Session Logging Convention

This directory is the human-readable run ledger for substantial Codex sessions. It complements experiment JSON records under `project_state/runs/`; it does not replace them.

## When To Create A Session Log

Create one markdown session log for any session that does at least one of:

- changes code, prompts, schemas, evaluation logic, project-state docs, or artifact outputs;
- runs or interprets a meaningful experiment;
- makes a decision that changes project direction;
- closes a blocker or creates a new one;
- updates visibility/dashboard infrastructure.

Tiny typo fixes and purely exploratory reads do not need a session log unless they change the handoff state.

## Naming

Use UTC timestamps and a short lowercase slug:

```text
docs/run_logs/YYYYMMDDTHHMMSSZ_short-session-name.md
```

If using an optional JSON companion, use the same stem:

```text
docs/run_logs/YYYYMMDDTHHMMSSZ_short-session-name.json
```

## Required Markdown Sections

Every session log should keep these headings:

- `Session Metadata`
- `Outcome`
- `Evidence`
- `Uncertainty`
- `Handoff`
- `Decision`
- `Privacy Check`

The Evidence Notebook dashboard should treat `Outcome`, `Evidence`, `Uncertainty`, and `Handoff` as first-class display fields.

## Status Labels

Use one closing decision label per session:

| Label | Use When |
| --- | --- |
| `keep this harness variant` | A harness change is worth keeping as a candidate comparison target. |
| `reject this variant` | The change is clearly worse, unsafe, or not worth carrying forward. |
| `inconclusive, rerun on a larger slice` | The change may help, but the slice or checks were too small. |
| `implementation works but needs full synthetic evaluation` | The feature works locally, but metrics need a larger run. |
| `blocked by local model/runtime setup` | Progress depends on installing or configuring a local/provider runtime. |
| `documentation/visibility updated, no metric decision needed` | The session changed project memory, docs, or visuals rather than harness behavior. |

If none of these fit, add the closest label and explain the nuance in `Uncertainty`.

## Evidence Rules

Prefer links over prose. Evidence can include:

- changed files;
- run records under `project_state/runs/`;
- manifest entries;
- tests or checks run;
- generated artifacts;
- decisions updated in `docs/decisions.md`;
- project-state pages updated.

Do not paste raw terminal logs unless the exact text is short and necessary. Summarize command results when possible.

## JSON Companion Files

Machine-readable companions are optional. Add them when a future dashboard or script should ingest the session directly.

Use:

- [session_log_companion_schema.json](session_log_companion_schema.json) for the shape;
- [session_log_companion_template.json](session_log_companion_template.json) as a copyable starting point.

The JSON companion should reference the markdown log path and repeat only compact metadata, status, evidence paths, and handoff text. The markdown file remains the readable source of truth.

## Privacy Rule

Never write raw real clinical text into session logs, JSON companions, prompts, screenshots, traces, run records, or exported artifacts. For future real-data work, session logs should contain only aggregate metrics, de-identified error categories, prompt/schema versions, runtime metadata, and approved artifact links.

## Closeout Checklist

Before ending a substantial session:

- create or update the session log;
- update `docs/current_state.md` if the top-level phase, latest result, or next action changed;
- update `docs/active_threads.md` for the relevant workstream;
- update `docs/milestones.md`, `docs/decisions.md`, or `docs/artifact_registry.md` when their claims changed;
- confirm the privacy check;
- name the next useful action.

