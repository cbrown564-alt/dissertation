---
name: dissertation-research-harness
description: Use for this dissertation repository when Codex needs to orient across sessions, run or compare fixed-budget seizure-frequency extraction harness experiments, update project-state memory, close out a research session, or apply the Meta-Harness/autoresearch workflow to the epilepsy multi-agent extraction project.
---

# Dissertation Research Harness

## Overview

Use this skill to keep work on the epilepsy extraction dissertation reproducible across sessions. Treat the repository as a harness-reliability study: read state, choose one question, change one thing, run a fixed comparison, record results, and close with a decision.

## Slash Commands

When the repo-local plugin is available:

- `/dissertation-research:orient`: reload project state, inspect recent runs, and recommend the next concrete move.
- `/dissertation-research:experiment`: run a fixed-budget harness experiment and record it in `project_state`.
- `/dissertation-research:close-session`: close out with tests, run-record checks, project-memory updates, and the next recommended action.

## Session Start

Read these files before substantial work:

- `docs/typical_session_workflow.md`
- `docs/research_program.md`
- `docs/project_specification.md`
- `docs/evaluation_protocol.md`
- `docs/real_data_governance.md`
- `docs/harness_experiment_protocol.md`
- `project_state/experiments/manifest.csv`
- the latest records under `project_state/runs/`

Summarize the current state in terms of:

- current harnesses and last metric results;
- active risks or blockers;
- the best next experiment or implementation target;
- governance constraints relevant to the requested task.

## Experiment Loop

Use this default rhythm:

1. Pick one clear question.
2. Change one harness, prompt, provider, verification rule, or visibility artifact.
3. Run a fixed smoke experiment.
4. Compare against the paired baseline when relevant.
5. Run tests.
6. Update project memory.
7. End with a keep/reject/inconclusive decision.

Default smoke command:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_harness_experiment.py --harness multi --limit 100 --description "<short description>"
```

Paired single-pass comparison:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_harness_experiment.py --harness single --limit 100 --description "<paired baseline description>"
```

Tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

## Harness IDs

- `h001_single_pass`: deterministic single-pass baseline.
- `h002_multi_agent_verify`: deterministic section/timeline, extractor, verifier, and aggregator baseline.
- `h003_single_prompt_llm`: planned schema-constrained LLM baseline.
- `h004_multi_agent_llm`: planned role-separated LLM pipeline.
- `h005_multi_agent_self_consistency_3`: planned three-sample self-consistency variant.

Update `project_state/harnesses/README.md` when a new serious harness variant appears.

## Governance

Closed-provider calls are for synthetic data only unless governance explicitly permits otherwise. Never persist real clinical text in logs, traces, prompts, screenshots, run records, or dashboard artifacts.

Run records should contain labels, aggregate metrics, hashes, and safe error categories, not raw letters.

## Closeout

Before ending a substantial session:

- confirm tests or explain why they were not run;
- confirm any experiment records written;
- update `docs/development_log.md` for meaningful project changes;
- update `project_state/experiments/manifest.csv` through the runner rather than by hand when possible;
- state the next recommended action.
