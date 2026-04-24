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
