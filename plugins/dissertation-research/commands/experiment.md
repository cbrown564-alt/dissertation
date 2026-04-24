---
description: Run a fixed-budget dissertation harness experiment and record it in project_state.
argument-hint: [single|multi] [limit] [description]
---

# Dissertation Harness Experiment

## Arguments

The user invoked this command with: $ARGUMENTS

## Preflight

1. Confirm `scripts/run_harness_experiment.py` exists.
2. Check `git status --short` and preserve unrelated work.
3. Confirm the requested harness. Use `multi` if omitted.
4. Confirm the requested limit. Use `100` if omitted.
5. Ensure the description is short and meaningful.

## Plan

Run a fixed-budget experiment through the canonical runner. If the user asks for a comparison, run both `multi` and `single` with the same limit.

## Commands

Default:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_harness_experiment.py --harness multi --limit 100 --description "multi smoke"
```

Single baseline:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_harness_experiment.py --harness single --limit 100 --description "single paired baseline"
```

Tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

## Verification

1. Confirm a JSON run record was written under `project_state/runs/`.
2. Confirm `project_state/experiments/manifest.csv` gained the expected row.
3. Confirm tests pass or report why they were not run.

## Summary

Report:

- experiment ID;
- harness;
- limit and row count;
- exact accuracy;
- monthly-rate accuracy;
- pragmatic micro-F1;
- purist micro-F1;
- run record path.

## Next Steps

Recommend whether to keep, reject, or rerun on a larger slice.
