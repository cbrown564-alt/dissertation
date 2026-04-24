# h003 Ollama Think-Disabled Smoke

## Session Metadata

- Date: 2026-04-24
- Session ID: 20260424T180900Z_h003_ollama_think_disabled_smoke
- Session objective: Make the local `h003_single_prompt_llm` path usable enough for a 25-row smoke evaluation.
- Related active thread: Harness Reliability; Provider And Local Model Setup
- Starting commit: 47a1bd128e8c79ca07a43e1de1ebdaca53c1eeef
- Dirty worktree at start: yes
- Optional JSON companion: none

## Outcome

`h003_single_prompt_llm` now disables Ollama thinking mode, caps local completions, recovers JSON from common local-model wrappers, and tolerates schema-near evidence strings. The local `qwen3.5:4b` path moved from timeout-heavy plumbing validation to a fast 25-row smoke, but extraction quality remains weak because the model over-abstains.

## Evidence

- Files changed: [llm_pipeline.py](../../src/epilepsy_agents/llm_pipeline.py), [providers.py](../../src/epilepsy_agents/providers.py), [structured_schema.py](../../src/epilepsy_agents/structured_schema.py), [test_llm_pipeline.py](../../tests/test_llm_pipeline.py), [test_cli.py](../../tests/test_cli.py), [current_state.md](../current_state.md), [active_threads.md](../active_threads.md).
- Run records: [original h003 n5](../../project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json), [updated h003 n5](../../project_state/runs/20260424T180607Z_h003_single_prompt_llm_n5.json), [updated h003 n25](../../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json).
- Manifest: [manifest.csv](../../project_state/experiments/manifest.csv) now includes the new n1, n5, and n25 `h003` smoke records from this session.
- Tests or checks: `python -m unittest discover -s tests` passed with 37 tests.

Key metric movement:

| Run | n | Exact | Monthly 15 pct | Pragmatic micro-F1 | Purist micro-F1 | Invalid-output rate | Mean latency |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `20260424T171400Z_h003_single_prompt_llm_n5` | 5 | 0.20 | 0.20 | 0.20 | 0.20 | 0.80 | 52.9 s |
| `20260424T180607Z_h003_single_prompt_llm_n5` | 5 | 0.40 | 0.40 | 0.40 | 0.40 | 0.40 | 0.95 s |
| `20260424T180629Z_h003_single_prompt_llm_n25` | 25 | 0.20 | 0.28 | 0.36 | 0.32 | 0.28 | 1.29 s |

## Uncertainty

The 25-row result is still too small and too abstention-heavy to compare against deterministic baselines. The run has many `unknown` or `no seizure frequency reference` predictions, especially where the gold label is frequent or infrequent. The parser now accepts schema-near output, so future work should separate true model extraction failure from output-format failure more carefully.

## Handoff

Next, classify the 25-row `h003` abstentions by gold family and add one targeted intervention for cluster, windowed-rate, or seizure-free phrasing. Rerun the same 25-row slice before comparing `qwen3.5:9b` or starting `h004_multi_agent_llm`.

## Decision

implementation works but needs full synthetic evaluation

## Privacy Check

No raw real clinical text was written into logs, prompts, screenshots, traces, run records, or exported artifacts. The only manually inspected prompt used a tiny invented synthetic sentence.
