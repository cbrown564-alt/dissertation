# Harness Protocol And Smoke Runs Session

## Session Metadata

- Date: 2026-04-24
- Session objective: Add a reproducible harness experiment workflow with stable IDs, structured run records, and the first paired smoke evaluations.
- Related active thread: Harness Reliability
- Starting commit: `22c397481d9a5ddd691bfc34fbd5f0d1f74ea9da`
- Dirty worktree at start: unknown; backfilled from commit history and manifest outputs

## Outcome

The project moved from a scaffold with ad hoc smoke checks to a named harness study with an explicit research posture, structured experiment protocol, stable harness IDs, a run manifest, repo-local run records, and the first paired 20-row synthetic comparison for `h001_single_pass` and `h002_multi_agent_verify`.

## Evidence

- Files added in commit `91d2ba20f2d19c1589f0cc201037f7eeffbdf711`:
  - `docs/research_program.md`
  - `docs/harness_experiment_protocol.md`
  - `scripts/run_harness_experiment.py`
  - `project_state/harnesses/README.md`
  - `project_state/experiments/manifest.csv`
  - `project_state/runs/20260424T083823Z_h002_multi_agent_verify_n20.json`
  - `project_state/runs/20260424T083902Z_h001_single_pass_n20.json`
- Visibility direction research also began in the same change set:
  - `docs/agent_visibility_plan.md`
  - `docs/agent_visibility_ui_mockups.html`
- First paired smoke records:
  - `project_state/runs/20260424T083823Z_h002_multi_agent_verify_n20.json`
  - `project_state/runs/20260424T083902Z_h001_single_pass_n20.json`
- Manifest entries:
  - `project_state/experiments/manifest.csv`
- Supporting summary in `docs/development_log.md`:
  - initial 20-row paired smoke records were created for `h001_single_pass` and `h002_multi_agent_verify`

## Uncertainty

This log is also backfilled from the commit boundary, run manifest, and development notes. The exact point at which the visibility-plan research was interleaved with the harness protocol work is not separately logged, so the narrative here reflects the artifacts that survived rather than a minute-by-minute account.

## Handoff

Use the new run-ledger setup to iterate on one deterministic retrieval or verification change at a time, then rerun a fixed paired synthetic slice and keep only improvements that survive the metric bundle.

## Decision

Implementation works but needs full synthetic evaluation.

## Privacy Check

No raw real clinical text was written into logs, prompts, screenshots, traces, run records, or exported artifacts.
