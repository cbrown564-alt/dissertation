# Active Threads

Last updated: 2026-04-26.

This page tracks the moving workstreams that should guide future sessions.

## Harness Reliability

### Current Question

How can the deterministic and future LLM-backed harnesses reduce seizure-frequency extraction errors while preserving evidence support and auditability?

### Latest Evidence

- Latest paired 100-row synthetic smoke runs (after seizure-free detection expansion):
  - `h002_multi_agent_verify`: exact 0.31, monthly 0.48, pragmatic micro-F1 0.55, purist micro-F1 0.53, NS F1 0.82.
  - `h001_single_pass`: exact 0.25, monthly 0.43, pragmatic micro-F1 0.50, purist micro-F1 0.48, NS F1 0.73.
- First local LLM smoke run:
  - `h003_single_prompt_llm`: exact 0.20, monthly 0.20, pragmatic micro-F1 0.20, purist micro-F1 0.20, invalid-output rate 0.80, mean latency about 52.9 s on `ollama` with `qwen3.5:4b`.
- Updated local LLM smoke after disabling Ollama thinking and tolerating schema-near JSON:
  - `h003_single_prompt_llm` n5: exact 0.40, monthly 0.40, pragmatic micro-F1 0.40, purist micro-F1 0.40, invalid-output rate 0.40, mean latency about 0.95 s.
  - `h003_single_prompt_llm` n25: exact 0.20, monthly 0.28, pragmatic micro-F1 0.36, purist micro-F1 0.32, invalid-output rate 0.28, mean latency about 1.29 s.
- `seizure_free_error` dropped from 18 to 9 on multi and from 19 to 13 on single; `correct` rose from 20 to 31 on multi.
- Run records: [multi n100](../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json), [single n100](../project_state/runs/20260424T144606Z_h001_single_pass_n100.json), [h003 original n5](../project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json), [h003 updated n25](../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json).
- The 17 abstentions in the latest `h003` 25-row smoke are now classified into seven failure families (9 window/aggregation, 4 cluster-shape, 2 NS-vs-no-reference, 2 qualitative, 2 actually-correct true-unknowns); see [run_logs/20260425T081533Z_h003_abstention_classification.md](run_logs/20260425T081533Z_h003_abstention_classification.md) for the per-row breakdown and an ordered three-step intervention list.
- Intervention 1 (six worked phrasing -> label exemplars in `system_prompt()`) is now landed in [structured_schema.py](../src/epilepsy_agents/structured_schema.py); the unit-test suite still passes (38/38). The empirical paired rerun on the 25-row slice is deferred because no Ollama runtime is reachable in the current sandbox; see [run_logs/20260426T081829Z_h003_system_prompt_exemplars.md](run_logs/20260426T081829Z_h003_system_prompt_exemplars.md).
- Session logs: [20260424T144639Z_seizure_free_detection_expansion.md](run_logs/20260424T144639Z_seizure_free_detection_expansion.md), [20260425T081533Z_h003_abstention_classification.md](run_logs/20260425T081533Z_h003_abstention_classification.md), [20260426T081829Z_h003_system_prompt_exemplars.md](run_logs/20260426T081829Z_h003_system_prompt_exemplars.md).

### Blocker Or Risk

The deterministic baseline still has residual seizure-free and cluster-family errors. On the LLM side, intervention 1 is implemented but unmeasured: the paired empirical rerun that would justify keep/reject for the new system prompt requires a local Ollama runtime that is not present in the current sandbox.

### Next Action

Steps 1 (parser round-trip check) and 2 (apply intervention 1 to `system_prompt()`) from the 2026-04-25 ordered list are done; see [20260426T081829Z_h003_system_prompt_exemplars.md](run_logs/20260426T081829Z_h003_system_prompt_exemplars.md). The next LLM-runtime session should: (a) bring up Ollama with `qwen3.5:4b`; (b) rerun `h003_single_prompt_llm` on the same 25-row `row_ok` slice as [20260424T180629Z_h003_single_prompt_llm_n25.json](../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json); (c) compare invalid-output rate, abstention count, and pragmatic micro-F1 against the 2026-04-24 baseline and re-classify any remaining abstentions; (d) only if window and cluster cases improve but NS or qualitative cases remain, apply intervention 2 (NS-vs-no-reference rule in the user prompt) in a separate paired run.

## Provider And Local Model Setup

### Current Question

Which local runtime and first model should be used for schema-constrained extraction smoke tests?

### Latest Evidence

- The laptop has an RTX 4070 Laptop GPU with 8 GB VRAM and enough disk for quantized local inference.
- Ollama is installed locally and its API is responding at `http://localhost:11434/api`.
- Local models currently visible through Ollama include `qwen3.5:4b`, `qwen3.5:9b`, `qwen3.5:35b-a3b`, and `llama3.1:latest`.
- `provider-smoke` succeeded end to end against local `qwen3.5:4b`.
- `h003` now sends `think: false` with a capped Ollama completion budget, avoiding the earlier timeout caused by model reasoning traces.
- Candidate model tiers are documented in [local_model_feasibility.md](local_model_feasibility.md).

### Blocker Or Risk

Local runtime installation is no longer the blocker. The active risk is whether the first chosen model plus prompt/schema setup can avoid excessive abstention while preserving evidence support.

### Next Action

Keep Ollama as the active runtime, improve `h003` extraction validity on `qwen3.5:4b`, and compare against `qwen3.5:9b` if the smaller model stays too abstention-heavy.

## Evidence Notebook Visibility

### Current Question

How should project state stay legible across long agent-assisted development sessions?

### Latest Evidence

- The chosen visibility direction is Evidence Notebook.
- Phase 1 markdown pages now exist: [current_state.md](current_state.md), [milestones.md](milestones.md), [active_threads.md](active_threads.md), [decisions.md](decisions.md), and [artifact_registry.md](artifact_registry.md).
- Phase 2 session logging convention exists at [run_logs/README.md](run_logs/README.md), with a template and optional JSON companion files.
- The notebook archive now includes backfilled pre-visibility session logs for the initial scaffold, harness protocol, and retrieval iteration.
- Phase 3 dashboard exists at [site/index.html](../site/index.html) with CSS/JS in [site/assets/](../site/assets/), generated by [src/epilepsy_agents/visibility/](../src/epilepsy_agents/visibility/).

### Blocker Or Risk

The source markdown layer is still hand-maintained, the dashboard can drift unless future sessions regenerate it after state updates, and the historical backfill is only as good as the surviving repo evidence behind it.

### Next Action

Use the dashboard for quick review, keep new session logs contemporaneous, regenerate after substantial closeouts, and proceed to the first curated Phase 4 visual artifact.

## Visual And Dissertation Artifacts

### Current Question

Which explanatory visuals should be produced first for README, dissertation, and supervisor review?

### Latest Evidence

- The shared Clinical Blueprint + Evidence Highlighter visual language is defined in [visual_artifacts_direction.md](visual_artifacts_direction.md).
- The first target set includes architecture, deployment, dataset/evaluation, agent roles, milestones, local model feasibility, evidence grounding, and final packaging.

### Blocker Or Risk

Generated visuals can become decorative if not tied to evidence and current project state.

### Next Action

Create the Project Architecture Poster first, using only synthetic/anonymised-looking text and sparse labels.

## Real-Data Governance

### Current Question

How should the project prepare for possible real King's College Hospital evaluation without leaking raw clinical content?

### Latest Evidence

- Governance rules are documented in [real_data_governance.md](real_data_governance.md).
- The research program explicitly prohibits autonomous loops on real clinical text and raw-text exports.

### Blocker Or Risk

Any future real-data stage must happen inside the approved environment and may restrict providers, telemetry, examples, traces, screenshots, and artifacts.

### Next Action

Keep real-data support as an architecture constraint, not an active local-data workflow.
