# Harness Experiment Protocol

## Purpose

This protocol makes harness iteration reproducible. It applies the main lessons from Meta-Harness and autoresearch in a restrained form:

- harnesses are experimental objects;
- feedback should include metrics and failure categories;
- runs should be fixed-budget and comparable;
- the filesystem should act as durable project memory.

## Directory Layout

Recommended state layout:

```text
project_state/
  experiments/
    manifest.csv
  runs/
    <experiment_id>.json
  harnesses/
    README.md
```

The manifest is the compact index. Run JSON files hold structured details for one experiment. Harness notes describe named variants and their intended difference from baseline.

## Standard Run Command

Use the runner for deterministic harness experiments:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_harness_experiment.py --harness multi --limit 100 --description "multi baseline smoke"
```

Single-pass comparison:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_harness_experiment.py --harness single --limit 100 --description "single baseline smoke"
```

Full current synthetic subset:

```powershell
$env:PYTHONPATH = "src"
python scripts\run_harness_experiment.py --harness multi --description "multi baseline full synthetic subset"
```

## Run Record Contents

Each run record should include:

- experiment ID and timestamp;
- harness ID and pipeline;
- data path and SHA-256 hash;
- row filtering and limit;
- code commit and dirty-worktree flag when available;
- aggregate metric summary;
- text-free error categories;
- notes and next actions.

Run records should not include raw letter text. This makes the habit compatible with later real-data evaluation.

## Harness IDs

Use stable, human-readable IDs:

| Harness ID | Meaning |
| --- | --- |
| `h001_single_pass` | Deterministic single-pass baseline. |
| `h002_multi_agent_verify` | Deterministic section/timeline, extractor, verifier, aggregator baseline. |
| `h003_single_prompt_llm` | Future single-prompt LLM baseline. |
| `h004_multi_agent_llm` | Future role-separated LLM pipeline. |
| `h005_multi_agent_self_consistency_3` | Future role-separated LLM pipeline with three sampled candidates. |

## Metric Bundle

Primary:

- pragmatic micro-F1;
- purist micro-F1;
- monthly-rate match within 15 percent tolerance;
- exact structured-label accuracy.

Secondary:

- macro-F1 and weighted-F1;
- evidence support rate;
- invalid-output rate;
- abstention handling;
- latency;
- token/cost budget.

## Error Categories

The runner assigns safe, broad categories:

- `correct`
- `class_confusion`
- `monthly_rate_mismatch`
- `exact_label_mismatch`
- `unknown_or_no_reference_error`
- `seizure_free_error`
- `cluster_error`
- `unsupported_or_empty_prediction`

These categories are intentionally coarse. Deeper qualitative review can add a dissertation-facing error typology later, using synthetic examples only unless real-data governance explicitly permits otherwise.

## Pareto Frontier Rule

Do not collapse the study to one metric too early. Keep candidates that are non-dominated across:

- class F1;
- monthly-rate accuracy;
- evidence support;
- invalid-output rate;
- runtime or token budget.

A slightly slower harness may be worthwhile if it is more evidence-grounded. A higher-F1 harness may be worse if it produces unsupported claims.

## Governance Rule

Closed-provider experiments are allowed only for synthetic data unless governance explicitly permits otherwise. Real clinical data must not be persisted in run records, traces, screenshots, prompts, or dashboard artifacts.
