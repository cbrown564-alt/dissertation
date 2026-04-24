---
description: Close out a dissertation work session with tests, run records, and project-memory updates.
argument-hint: [optional summary of work]
---

# Dissertation Close Session

## Arguments

The user invoked this command with: $ARGUMENTS

## Preflight

1. Run `git status --short`.
2. Identify files changed during the session.
3. Check whether any experiment was run and whether `project_state/experiments/manifest.csv` changed.
4. Read `docs/development_log.md` if meaningful project work occurred.

## Plan

Produce a concise closeout:

1. Run tests if code changed.
2. Update `docs/development_log.md` for meaningful project changes.
3. Summarize experiment records and metrics.
4. State unresolved risks and next actions.

## Commands

Tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

Status:

```powershell
git status --short
Get-Content project_state\experiments\manifest.csv
```

## Verification

Confirm:

- tests passed or explain the blocker;
- run records were written if experiments ran;
- real clinical text was not written into project-state records;
- unrelated user changes were not reverted.

## Summary

Report:

- what changed;
- what was verified;
- what was recorded;
- what remains next.

## Next Steps

Suggest one concrete next session target, such as local model setup, verifier improvement, full synthetic run, or visibility dashboard work.
