---
description: Orient on the current dissertation project state and recommend the next concrete move.
argument-hint: [optional focus]
---

# Dissertation Orient

## Arguments

The user invoked this command with: $ARGUMENTS

## Preflight

1. Confirm the current directory is the dissertation repository by checking for `docs/project_specification.md` and `synthetic_data_subset_1500.json`.
2. Run `git status --short` and note untracked or modified files without reverting anything.
3. Read `docs/research_program.md`, `docs/evaluation_protocol.md`, `docs/real_data_governance.md`, and `project_state/experiments/manifest.csv`.
4. Read the latest two JSON records under `project_state/runs/` if present.

## Plan

Build a concise session briefing:

1. Summarize the project objective.
2. Summarize the latest harness results.
3. Identify active risks or blockers.
4. Recommend one concrete next action.

## Commands

Useful local reads:

```powershell
git status --short
Get-Content docs\research_program.md
Get-Content project_state\experiments\manifest.csv
Get-ChildItem project_state\runs -File | Sort-Object LastWriteTime -Descending | Select-Object -First 2
```

## Verification

Check that the briefing references actual local files and the latest available manifest rows.

## Summary

Report:

- current project phase;
- latest single vs multi metrics if available;
- highest-value next move;
- any governance reminders.

## Next Steps

Suggest one of:

- run `/dissertation-research:experiment`;
- implement a narrow harness change;
- update visibility/project-state docs;
- configure a local model runtime.
