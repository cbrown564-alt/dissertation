# Typical Session Workflow

Use this workflow at the start and end of each substantial Codex session on this repository.

The compact rhythm is:

```text
Read state -> choose one question -> change one thing -> run paired eval -> log results -> decide next action.
```

## 1. Reload Project State

Read these first:

- `docs/research_program.md`
- `docs/current_state.md`
- `docs/active_threads.md`
- `docs/project_specification.md`
- `docs/evaluation_protocol.md`
- `docs/real_data_governance.md`
- `docs/harness_experiment_protocol.md`
- `docs/run_logs/README.md`
- `project_state/experiments/manifest.csv`
- the latest JSON records under `project_state/runs/`

Then summarize:

- current project phase;
- latest `single` vs `multi` harness results;
- active risks or blockers;
- most useful next action.

## 2. Pick One Clear Target

Keep the session narrow. Good session targets include:

- improve candidate-span retrieval;
- add or compare an LLM-backed baseline;
- configure or test a local model provider;
- strengthen verifier logic;
- classify recent errors into the taxonomy;
- run a fixed comparison between `single` and `multi`;
- update the visibility/dashboard layer;
- create a dissertation-supporting artifact.

## 3. Make One Meaningful Change

Prefer one change unit per session:

- one harness variant;
- one prompt/schema change;
- one evaluation feature;
- one project-state or visibility feature;
- one dissertation-supporting artifact.

Avoid changing multiple experimental variables at once unless the run is explicitly marked as a combined intervention.

## 4. Run A Fixed Smoke Evaluation

Default multi-agent run:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_harness_experiment.py --harness multi --limit 100 --description "<short description>"
```

Paired single-pass baseline:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_harness_experiment.py --harness single --limit 100 --description "<paired baseline description>"
```

Use the same limit, dataset, and row filtering for paired comparisons.

## 5. Check Tests

Run:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

If tests are not run, record why.

## 6. Update Project Memory

The experiment runner updates:

- `project_state/runs/*.json`
- `project_state/experiments/manifest.csv`

For meaningful project changes, also update whichever applies:

- `docs/development_log.md`
- `project_state/harnesses/README.md`
- `docs/harness_experiment_protocol.md`
- `docs/research_program.md`
- `docs/current_state.md`
- `docs/active_threads.md`
- `docs/milestones.md`, `docs/decisions.md`, or `docs/artifact_registry.md` when the session changes their claims.
- a markdown session log under `docs/run_logs/` for any substantial session.
- an optional JSON companion under `docs/run_logs/` when the session should be machine-readable for a future dashboard.

Do not write raw real clinical text into logs, run records, prompts, screenshots, or exported artifacts.

## 7. End With A Decision

Each session should close with one of:

- keep this harness variant;
- reject this variant;
- inconclusive, rerun on a larger slice;
- implementation works but needs full synthetic evaluation;
- blocked by local model/runtime setup;
- documentation/visibility updated, no metric decision needed.

Finish by naming the next recommended action.

Use the exact closing decision labels from [run_logs/README.md](run_logs/README.md) so future dashboard views can group sessions consistently.
