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
