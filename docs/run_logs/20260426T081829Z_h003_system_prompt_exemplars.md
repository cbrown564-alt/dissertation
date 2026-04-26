# Session Log: h003 system prompt worked exemplars (intervention 1)

## Session Metadata

- Date: 2026-04-26
- Session ID: 20260426T081829Z_h003_system_prompt_exemplars
- Session objective: Apply intervention 1 from the 2026-04-25 abstention classification (six worked label exemplars in `system_prompt()`) so the next available LLM-runtime session can rerun `h003` on the 25-row slice for a paired comparison.
- Related active thread: Harness Reliability (and Provider And Local Model Setup, indirectly).
- Starting commit: dda6ac0fd76be1687d4da4d2863b5d77362abbda
- Dirty worktree at start: false
- Optional JSON companion: none

## Outcome

`system_prompt()` in [structured_schema.py](../../src/epilepsy_agents/structured_schema.py) now appends six worked phrasing -> label exemplars covering each abstention failure family identified on 2026-04-25:

- explicit rate (`'two events each week' -> '2 per week'`),
- multi-month window (`'six episodes over the past seven months' -> '6 per 7 month'`),
- single-interval window (`'roughly one seizure every six weeks' -> '1 per 6 week'`),
- cluster days plus per-cluster (`'two cluster days per month, around six seizures per cluster' -> '2 cluster per month, 6 per cluster'`),
- seizure-free (`'seizure free for several months since the last review' -> 'seizure free for multiple month'`),
- qualitative high-frequency (`'multiple seizures per week, exact count not given' -> 'multiple per week'`).

Phrasings on the left of each `->` are synthetic-style paraphrases authored for the prompt rather than copied from any letter. The prompt still starts with `/no_think` and still requires schema-conformant JSON-only output supported by quoted evidence, so the existing `test_system_prompt_disables_qwen_thinking_mode` and the surrounding `SinglePromptLLMPipelineTests` checks continue to pass.

The change only affects the `h003_single_prompt_llm` pipeline path; the deterministic `h001_single_pass` and `h002_multi_agent_verify` harnesses do not use `system_prompt()` and so are unchanged. No run records, manifest rows, or schema fields were modified, and no new experiment was added to [project_state/experiments/manifest.csv](../../project_state/experiments/manifest.csv).

The empirical paired rerun on the 25-row slice could not be executed in this session because no Ollama runtime is available in the current sandbox (`curl http://localhost:11434/api/tags` returns connection refused, and `ollama` is not on `$PATH`). The change is therefore landed but unmeasured; the next LLM-runtime session should run the paired comparison.

### Pre-change parser round-trip check

Per the 2026-04-25 handoff step 1, the five labels named in the next-action list, plus the `2 per week` and `6 per 7 month` exemplars, all round-trip cleanly through `parse_label` in [labels.py](../../src/epilepsy_agents/labels.py):

| Label | monthly_rate | pragmatic | purist | kind |
| --- | ---: | --- | --- | --- |
| `multiple per week` | 13.04 | frequent | (1/W,1/D) | rate |
| `multiple per day` | 91.31 | frequent | >=1/D | rate |
| `1 per 4 day` | 7.61 | frequent | (1/W,1/D) | rate |
| `1 per 6 week` | 0.72 | infrequent | (1/6M,1/M) | rate |
| `2 cluster per month, 6 per cluster` | 12.00 | frequent | (1/W,1/D) | cluster |
| `6 per 7 month` | 0.86 | infrequent | (1/6M,1/M) | rate |
| `2 per week` | 8.70 | frequent | (1/W,1/D) | rate |
| `seizure free for multiple month` | 0.00 | NS | NS | seizure_free |

This means none of the new exemplar labels would silently fall through to `unknown` if a model emits them verbatim.

## Evidence

- Files changed: [src/epilepsy_agents/structured_schema.py](../../src/epilepsy_agents/structured_schema.py) (only `system_prompt()`); this session log.
- Run records consulted:
  - [project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json](../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json) (the n=25 baseline this intervention targets).
  - [run_logs/20260425T081533Z_h003_abstention_classification.md](20260425T081533Z_h003_abstention_classification.md) (defines intervention 1).
- Tests or checks: `PYTHONPATH=src python -m unittest discover -s tests` -> 38/38 pass on the post-edit working tree.
- Generated artifacts: this session log only; no machine-readable companion.
- Runtime probe: `curl -s -m 3 http://localhost:11434/api/tags` returns connection refused (exit 7); `ollama` not on `$PATH`. The LLM rerun is therefore deferred.

## Uncertainty

- The expected lifts on window, cluster, and qualitative cases are reasoned from the 2026-04-25 family breakdown, not measured. Until a paired rerun on the same 25-row slice exists, the intervention's effect on invalid-output rate, abstention count, and pragmatic micro-F1 remains a hypothesis.
- The new exemplars may interact with `qwen3.5:4b`'s tendency toward verbatim copying. If the model starts echoing the exemplar phrasings into the `evidence` field, that would be a privacy-safe artefact (the phrasings are synthetic) but would inflate evidence-support metrics; the next session should spot-check evidence spans against letter text.
- No deterministic paired smoke was rerun because the change does not touch `h001`/`h002` behaviour; the existing 100-row results in [manifest.csv](../../project_state/experiments/manifest.csv) remain the deterministic baseline.

## Handoff

The next LLM-runtime session should:

1. Bring up Ollama with `qwen3.5:4b` (and `think: false` already wired into the pipeline).
2. Rerun `h003_single_prompt_llm` on the same 25-row `row_ok` slice used in [20260424T180629Z_h003_single_prompt_llm_n25.json](../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json), using `python scripts/run_harness_experiment.py --harness single_llm --limit 25 --description "h003 worked-exemplar intervention 1 rerun"` (or the equivalent LLM-harness invocation registered in `run_harness_experiment.py`).
3. Compare invalid-output rate, abstention count, and pragmatic micro-F1 against the 2026-04-24 baseline; classify any remaining abstentions back into the seven 2026-04-25 families.
4. Only if window and cluster cases improve but NS or qualitative cases remain, apply intervention 2 (NS-vs-no-reference rule in the user prompt in `llm_pipeline.py`) in a separate paired run.

## Decision

blocked by local model/runtime setup.

The intervention is implemented and unit tests pass, but the paired empirical rerun that would justify a `keep this harness variant` or `reject this variant` decision requires a local Ollama runtime that is not present in this sandbox.

## Privacy Check

The dataset referenced is `synthetic_data_subset_1500.json` (Gan et al. synthetic letters). The six new exemplar phrasings are synthetic paraphrases authored for the prompt and contain no real clinical text. No raw real clinical text was written into this log, the prompt, the schema, the tests, the run records, or any exported artifact.
