# Session Log Template

Use this template for substantial Codex sessions that change code, experiments, project state, or dissertation-supporting artifacts.

File naming suggestion:

```text
docs/run_logs/YYYYMMDDTHHMMSSZ_short-session-name.md
```

## Session Metadata

- Date:
- Session ID:
- Session objective:
- Related active thread:
- Starting commit:
- Dirty worktree at start:
- Optional JSON companion:

## Outcome

What is now true that was not true before?

## Evidence

Link to files, run records, commands, tests, generated artifacts, or metrics that support the outcome.

- Files changed:
- Run records:
- Tests or checks:
- Generated artifacts:

## Uncertainty

What was not checked, remains fragile, or needs human review?

## Handoff

What is the most useful next action for the next session?

## Decision

Close the session with exactly one of:

- keep this harness variant;
- reject this variant;
- inconclusive, rerun on a larger slice;
- implementation works but needs full synthetic evaluation;
- blocked by local model/runtime setup;
- documentation/visibility updated, no metric decision needed.

## Privacy Check

Confirm that no raw real clinical text was written into logs, prompts, screenshots, traces, run records, or exported artifacts.
