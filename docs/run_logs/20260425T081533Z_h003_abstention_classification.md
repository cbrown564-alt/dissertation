# Session Log: h003 25-row abstention classification

## Session Metadata

- Date: 2026-04-25
- Session ID: 20260425T081533Z_h003_abstention_classification
- Session objective: Classify the 17 abstentions in the latest `h003_single_prompt_llm` 25-row smoke into the project error taxonomy and produce a narrow, ordered intervention list for the next LLM-iteration session.
- Related active thread: Harness Reliability (and Provider And Local Model Setup, indirectly).
- Starting commit: b126cbe8fbe187582528a7b23dbaa08eb654ab5f
- Dirty worktree at start: false
- Optional JSON companion: none

## Outcome

The 17 abstentions in [20260424T180629Z_h003_single_prompt_llm_n25.json](../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json) now have a structured failure-family breakdown, and there is an ordered list of three narrow interventions to try in the next LLM-iteration session. Two of the 17 abstentions are revealed to be correct (gold also `unknown`), so the practical abstention-error count is 15.

No code, prompts, schema, or run records changed in this session. The unit-test suite still passes (38/38).

### Failure-family breakdown of the 17 abstentions

| Family | Count | Predicted | Notes |
| --- | ---: | --- | --- |
| `cluster` | 4 | 3x `unknown`, plus 1 partial | 2 rows have explicit cluster-day counts (gold like `2 cluster per month, 6 per cluster`); 2 rows have `unknown, X per cluster` gold where pragmatic UNK was technically matched but the cluster annotation was lost. |
| `window_month` | 4 | 2x `unknown`, 2x `no seizure frequency reference` | Gold labels of the form `X per N month` with `N>1`; letters describe seizures across multiple named months and require aggregation across the visible window. |
| `seizure_free` | 2 | 2x `no seizure frequency reference` | Gold is `seizure free for multiple month`; model collapses NS into "no reference". This is the same failure mode the deterministic baselines fixed in the 2026-04-24 seizure-free expansion. |
| `qualitative_multiple` | 2 | 2x `unknown` | Letter says `several episodes per week` / `multiple seizures in past day`; gold is `multiple per week` / `multiple per day`. The schema permits these labels but the prompt does not surface them. |
| `true_unknown` | 2 | 2x `unknown` | Gold is also `unknown`; not actually errors. Pragmatic-class match was correct on both. |
| `window_week` | 1 | 1x `unknown` | `Median inter-seizure interval ~ six weeks` -> `1 per 6 week`. |
| `window_day` | 1 | 1x `unknown` | `clusters every 4 days` -> `1 per 4 day`. |
| `other` | 1 | 1x `unknown` | `abs *monthly` (abbreviation) -> `1 per month`. |

So of 15 real abstention-errors:

- 9 (60 percent) are window/aggregation problems (4 multi-month windows, 2 cluster-day windows that need aggregation, 2 single-interval windows, 1 abbreviated monthly).
- 4 (27 percent) are cluster-shape problems (need to emit the `N cluster per month, M per cluster` form or its `unknown, M per cluster` partial variant).
- 2 (13 percent) are NS vs no-reference confusion (the seizure-free family).
- 2 (13 percent) are qualitative-frequency phrasings the prompt does not exemplify.

(Counts overlap because cluster cases also need windowing.)

### Ordered intervention list for the next session

These are listed one-change-at-a-time per [research_program.md](../research_program.md). The next LLM-iteration session should pick exactly one and rerun on the same 25-row slice for paired comparison.

1. **Add 6 worked label exemplars to `system_prompt()` in [structured_schema.py](../../src/epilepsy_agents/structured_schema.py#L47-L58)**, one per family above, all derived from synthetic-style phrasings rather than copied from the dataset:
   - explicit rate (`2 per week`),
   - multi-month window (`6 per 7 month`),
   - single-interval window (`1 per 6 week`),
   - cluster days plus per-cluster (`2 cluster per month, 6 per cluster`),
   - seizure-free (`seizure free for multiple month`),
   - qualitative high-frequency (`multiple per week`).
   Expected effect: lifts the 9 window cases, the 4 cluster cases, and the 2 qualitative cases. Lowest-risk single change.

2. **Add an explicit NS-vs-no-reference rule to the user prompt in [llm_pipeline.py](../../src/epilepsy_agents/llm_pipeline.py#L80-L93)**: "Use `seizure free for multiple month` when the letter states the patient is currently seizure-free; reserve `no seizure frequency reference` for letters with no seizure-related content at all." Expected effect: lifts the 2 NS cases and may reduce false `no seizure frequency reference` outputs more broadly. Hold this back until intervention 1 is measured, so the variables stay separated.

3. **Surface a candidate-span pre-filter** by re-using the deterministic `multi`-pipeline section/timeline retriever in [agents.py](../../src/epilepsy_agents/agents.py) to prepend a `Candidate spans:` block to the user prompt. This is more architectural and risks crossing into the planned `h004_multi_agent_llm` design boundary, so it should not be combined with intervention 1 or 2 in a single run.

## Evidence

- Files changed: this session log only (no code, prompts, schema, manifest, or run records changed).
- Run records consulted:
  - [project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json](../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json) (the n=25 smoke being analyzed).
  - [project_state/experiments/manifest.csv](../../project_state/experiments/manifest.csv) for paired-baseline context.
- Tests or checks: `PYTHONPATH=src python -m unittest discover -s tests` -> 38/38 pass on commit b126cbe.
- Generated artifacts: this session log only; no machine-readable companion.
- Source-of-truth files for the proposal: [structured_schema.py](../../src/epilepsy_agents/structured_schema.py), [llm_pipeline.py](../../src/epilepsy_agents/llm_pipeline.py), [agents.py](../../src/epilepsy_agents/agents.py).

## Uncertainty

- The classification was done from gold labels and the dataset's own `reference` field, not from the actual LLM completion text (which the run record deliberately does not store). It is possible some of the multi-month-window failures are caused by JSON-format issues rather than reasoning issues, but the same run had only 0.28 invalid-output rate so most of these abstentions were schema-valid `unknown`/`no seizure frequency reference` outputs.
- This sandbox has no Ollama runtime, so the proposed prompt change cannot be measured here. The expected lifts above are reasoned, not empirical.
- The `qualitative_multiple` and `window_day` interventions assume the parser in [labels.py](../../src/epilepsy_agents/labels.py) already accepts `multiple per week`, `multiple per day`, and `1 per 4 day`. This was not verified in this session and should be checked before the next LLM rerun.

## Handoff

The next LLM-iteration session should:

1. Confirm `multiple per week`, `multiple per day`, `1 per 4 day`, `1 per 6 week`, and `2 cluster per month, 6 per cluster` round-trip cleanly through `parse_label`.
2. Apply intervention 1 above (6 worked exemplars in `system_prompt()`).
3. Rerun `h003_single_prompt_llm` on the same 25-row slice and compare invalid-output rate, abstention count, and pragmatic micro-F1 against the 2026-04-24 baseline.
4. Only if intervention 1 helps but NS and qualitative cases remain, add intervention 2 in a separate paired run.

## Decision

documentation/visibility updated, no metric decision needed.

## Privacy Check

The dataset analyzed is `synthetic_data_subset_1500.json` (Gan et al. synthetic letters). Short reference snippets quoted in the failure-family table are from this synthetic dataset and contain no real clinical text. No raw real clinical text was written into this log, the run records, prompts, schemas, screenshots, or traces.
