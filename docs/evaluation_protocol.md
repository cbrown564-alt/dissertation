# Evaluation Protocol

## Primary Evaluation Question

Does the multi-agent extraction framework produce more reliable seizure-frequency outputs than a single-prompt extractor under the same inference budget?

## Current Dataset

The current repository contains `synthetic_data_subset_1500.json`, a 1,500-row subset of synthetic clinic letters. The harness can run on all rows or only rows where `row_ok` is true. The default is to evaluate only `row_ok` rows.

## Output Schema

Every extractor must emit:

- `label`: Gan-style structured seizure-frequency label.
- `evidence`: one or more supporting text spans.
- `confidence`: calibrated or heuristic confidence from 0 to 1.
- `analysis`: short audit rationale.
- `parsed_monthly_rate`: deterministic normalization when parseable.
- `pragmatic_class`: `infrequent`, `frequent`, `UNK`, or `NS`.
- `purist_class`: fine-grained class from Gan et al.'s scheme.
- `warnings`: validation or contradiction flags.

## Metrics

Primary:

- Pragmatic micro-F1.
- Purist micro-F1.
- Monthly-rate match within 15 percent tolerance.

Secondary:

- Exact structured-label accuracy.
- Macro-F1 and weighted-F1.
- Evidence support rate.
- Abstention accuracy for `unknown` and `no seizure frequency reference`.
- Invalid-output rate.
- Cost, latency, and token use.

## Baselines

- Deterministic single-pass baseline: scans the letter once and extracts the first supported pattern.
- Deterministic multi-agent baseline: segments the letter, extracts candidates, verifies, and aggregates.
- Future single-prompt LLM baseline: one prompt, one schema-validated answer.
- Future multi-agent LLM pipeline: section/timeline, extraction, verification, aggregation.
- Gan et al. fine-tuned model baseline: compare against reported held-out real-letter scores when the evaluation setup is comparable, and against any available model outputs if provided.

## Experimental Controls

- Use identical input letters for paired comparisons.
- Keep model, temperature, context budget, and maximum output tokens fixed within each comparison.
- Record prompt version, code commit, model version, dataset hash, and date.
- Report aggregate metrics and confidence intervals.
- Avoid storing real patient text in logs or outputs during real-data evaluation.

## Commands

Synthetic subset smoke run:

```powershell
$env:PYTHONPATH = "src"
python -m epilepsy_agents.cli evaluate --data synthetic_data_subset_1500.json --limit 100 --pipeline multi
```

Full current subset:

```powershell
$env:PYTHONPATH = "src"
python -m epilepsy_agents.cli evaluate --data synthetic_data_subset_1500.json --pipeline multi --out outputs/evaluation/multi_full.json --csv outputs/evaluation/multi_full.csv
```

