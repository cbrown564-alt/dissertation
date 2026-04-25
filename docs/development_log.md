# Development Log

## 2026-04-24

Initial repository build-out from source materials.

Added:

- Python package under `src/epilepsy_agents`.
- Synthetic subset loader.
- Gan-style label parser and monthly-rate normalizer.
- Deterministic single-pass and multi-agent baselines.
- Evaluation metrics for exact labels, monthly rates, pragmatic classes, and purist classes.
- CLI for evaluation and prediction.
- Unit tests for label parsing.
- Dissertation, evaluation, literature, project-specification, and governance scaffolds.

Initial smoke test:

- Unit tests pass with `python -m unittest discover -s tests`.
- `--limit 100` synthetic smoke evaluations run for both `multi` and `single` pipelines.

Known limitations:

- The deterministic extractor is only a harness baseline, not the intended final LLM system.
- It misses many temporal arithmetic cases and should not be treated as a clinically useful model.
- LLM provider adapters and schema-enforced prompt execution are the next engineering step.

Local LLM feasibility pass:

- Probed laptop hardware: RTX 4070 Laptop GPU with 8 GB VRAM, 22 CPU threads, and substantial free disk.
- Confirmed `.env` contains OpenAI, Anthropic, Gemini, and Hugging Face keys without exposing secret values.
- Confirmed no local Ollama, LM Studio, or vLLM/llama.cpp server is currently running.
- Added local model feasibility report, provider abstraction, shared structured-output schema, and safe model probe script.

Visual artifact direction:

- Captured the shared Clinical Blueprint + Evidence Highlighter visual language.
- Listed the first visual artifact set for architecture, deployment, dataset/evaluation, agent roles, milestones, local model feasibility, evidence grounding, and final dissertation packaging.
- Added the first project architecture poster image brief for the next generation pass.

Research harness workflow:

- Added a Meta-Harness/autoresearch-inspired research program and harness experiment protocol.
- Added `scripts/run_harness_experiment.py` to run fixed-budget `single` and `multi` experiments, write safe run records, and append the experiment manifest.
- Created initial 20-row paired smoke records for `h001_single_pass` and `h002_multi_agent_verify`.
- Added a repo-local `dissertation-research` Codex plugin scaffold with a dissertation research harness skill and slash-command definitions for orienting, running experiments, and closing sessions.
- Added `PyYAML` as a project dependency so Codex skill validation can run.
- Added `docs/typical_session_workflow.md` as the canonical cross-session workflow checklist.

Candidate retrieval smoke iteration:

- Expanded deterministic frequency candidate retrieval to include adjacent sentence windows, spasm/spell/jerk/attack terms, ranged counts written with "or", hyphenated clinical modifiers, shared-window count summation, and dated event count lists.
- Added focused unit tests for these extraction forms and for avoiding seizure-free inference from "between episodes" wording.
- Ran paired 100-row synthetic smoke records after the final retrieval update: `20260424T090105Z_h002_multi_agent_verify_n100` and `20260424T090110Z_h001_single_pass_n100`.
- Result: multi improved over the intermediate run and narrowly led the paired single baseline on exact accuracy, monthly-rate match, pragmatic micro-F1, and purist micro-F1, but absolute performance remains too low for anything beyond harness iteration.
- Decision: keep the retrieval expansion as a candidate baseline improvement; next action is to classify remaining `unknown_or_no_reference_error`, `seizure_free_error`, and `cluster_error` cases before broadening beyond deterministic patterns.

Seizure-free detection expansion:

- Broadened deterministic seizure-free detection in `FieldExtractorAgent._extract_from_text` with a structured sequence covering numeric durations, numeric negation windows ("no seizures for over N units"), qualitative durations ("for a long duration"/"prolonged period"), unit-only durations ("for years"), "since"/"off ASMs since"/"interval since" forms, present-tense statements ("by patient report", "currently seizure-free"), sustained seizure freedom, long-term remission, verb-phrase negation ("seizure occurrences have not been happening"), and an expanded absence-of-events catch-all guarded against "otherwise"/"between"/"prior to"/"previously"/"for context".
- Added `remission`, `recurrence`, and `seizure freedom` to `FREQUENCY_TERMS` so the section/timeline retriever picks these candidate sentences.
- Added eleven focused tests covering the new branches plus a past-tense negative case.
- Ran paired 100-row synthetic smoke after the change: `20260424T144559Z_h002_multi_agent_verify_n100` and `20260424T144606Z_h001_single_pass_n100`.
- Result: multi exact 0.20->0.31, monthly 0.35->0.48, pragmatic micro-F1 0.42->0.55, purist micro-F1 0.40->0.53, NS F1 0.26->0.82; single exact 0.18->0.25, monthly 0.33->0.43, pragmatic micro-F1 0.40->0.50, purist micro-F1 0.38->0.48, NS F1 0.00->0.73; `seizure_free_error` dropped from 18 to 9 on multi and from 19 to 13 on single; no regressions in other error categories.
- Decision: keep this harness variant; next action is to audit residual NS false positives and move on to `unknown_or_no_reference_error` or `cluster_error`.

Phase A kickoff:

- Added a `provider-smoke` CLI command that probes `lmstudio`, `vllm`, or `ollama` and can round-trip a minimal schema-constrained JSON request through `src/epilepsy_agents/providers.py` (M-A1 verification path).
- Brought Ollama online with `qwen3.5:4b` available locally at `http://localhost:11434/api`; `provider-smoke` succeeded end to end. M-A1 Complete.
- Implemented `h003_single_prompt_llm` as a schema-constrained single-call LLM harness with retries, invalid-output rate, latency, and token-budget metadata in `src/epilepsy_agents/llm_pipeline.py`; registered it in `project_state/harnesses/README.md`.
- First h003 run: `20260424T171400Z_h003_single_prompt_llm_n5.json` -> exact 0.20, invalid-output rate 0.80, mean latency 52.9 s. Slow latency traced to Ollama thinking traces.
- Set `think: false` on the Ollama request and capped the completion budget; rerun `20260424T180607Z_h003_single_prompt_llm_n5.json` -> exact 0.40, invalid-output rate 0.40, mean latency 0.95 s.
- First 25-row h003 smoke: `20260424T180629Z_h003_single_prompt_llm_n25.json` -> exact 0.20, monthly 0.28, pragmatic micro-F1 0.36, purist micro-F1 0.32, invalid-output rate 0.28, mean latency 1.29 s. Abstention dominates on cluster, window, and seizure-free rows.

Project re-scope into phases:

- Restructured [milestones.md](milestones.md) into Delivered Infrastructure plus Phase A (stand up the LLM path), Phase B (reliability interventions), Phase C (scale and external baselines), Phase D (locked-down real-data evaluation), Phase E (dissertation and packaging).
- Added [D007](decisions.md) to freeze further deterministic regex expansion; the deterministic harnesses stay as the comparison floor per [D002](decisions.md) but are no longer an active development target.
- Added a Project Phases section to [research_program.md](research_program.md) that aligns harness IDs and milestones with the phase structure.
- Confirmed `current_state.md` and `active_threads.md` now describe the project as early Phase A with M-A2 in progress.
- Next useful action stays on M-A2: classify the 25-row h003 abstentions and add one narrow intervention (prompt or candidate-span aid) for cluster/window/seizure-free cases, then rerun h003 on the same 25-row slice. Do not return to deterministic regex work (D007).
