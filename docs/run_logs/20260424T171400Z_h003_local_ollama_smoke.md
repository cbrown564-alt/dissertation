# h003 Local Ollama Smoke

## Session Metadata

- Date: 2026-04-24
- Session ID: 20260424T171400Z_h003_local_ollama_smoke
- Session objective: Verify a live local runtime and record the first `h003_single_prompt_llm` smoke run.
- Related active thread: Provider and local model setup
- Starting commit: `dd081bd3085172fc8dabcc66615cf4a3ec775470`
- Dirty worktree at start: yes
- Optional JSON companion: none

## Outcome

The local Ollama runtime is now confirmed live for Phase A work. `provider-smoke` succeeded against local `qwen3.5:4b`, and the repository produced its first `h003_single_prompt_llm` run record on a 5-row synthetic slice. The blocker has moved from runtime setup to prompt and schema robustness: the first `h003` smoke returned `unknown` on four of five rows and recorded an invalid-output rate of 0.80.

## Evidence

- Files changed:
  - [src/epilepsy_agents/llm_pipeline.py](/C:/Users/cbrow/Code/dissertation/src/epilepsy_agents/llm_pipeline.py)
  - [scripts/run_harness_experiment.py](/C:/Users/cbrow/Code/dissertation/scripts/run_harness_experiment.py)
  - [tests/test_llm_pipeline.py](/C:/Users/cbrow/Code/dissertation/tests/test_llm_pipeline.py)
  - [src/epilepsy_agents/cli.py](/C:/Users/cbrow/Code/dissertation/src/epilepsy_agents/cli.py)
  - [src/epilepsy_agents/providers.py](/C:/Users/cbrow/Code/dissertation/src/epilepsy_agents/providers.py)
- Run records:
  - [20260424T171400Z_h003_single_prompt_llm_n5.json](/C:/Users/cbrow/Code/dissertation/project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json)
- Tests or checks:
  - `PYTHONPATH=src python -m unittest discover -s tests` -> 32 tests passed.
  - `PYTHONPATH=src python -m epilepsy_agents.cli provider-smoke --provider ollama --model qwen3.5:4b --timeout-seconds 60` -> probe and schema-constrained chat succeeded.
  - `PYTHONPATH=src python scripts\run_harness_experiment.py --harness single_llm --provider ollama --model qwen3.5:4b --limit 5 --timeout-seconds 60` -> first `h003` run recorded.
- Generated artifacts:
  - Manifest entry added under [project_state/experiments/manifest.csv](/C:/Users/cbrow/Code/dissertation/project_state/experiments/manifest.csv).

## Uncertainty

The first `h003` smoke is only five rows and is not yet a meaningful baseline comparison. Mean latency was about 52.9 seconds per row, so larger slices will be slow unless validity improves enough to justify them. The initial prompt and schema path likely needs targeted tuning for explicit frequency extraction and cluster handling.

## Handoff

Inspect the four `unknown` outputs in [20260424T171400Z_h003_single_prompt_llm_n5.json](/C:/Users/cbrow/Code/dissertation/project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json), tighten the prompt and schema handling, then rerun `h003_single_prompt_llm` on 25 rows. If `qwen3.5:4b` remains too abstention-heavy, compare against local `qwen3.5:9b`.

## Decision

implementation works but needs full synthetic evaluation

## Privacy Check

Confirmed: no raw real clinical text was written into logs, prompts, screenshots, traces, run records, or exported artifacts.
