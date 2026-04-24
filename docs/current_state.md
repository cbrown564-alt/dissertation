# Current State

Last updated: 2026-04-24.

This page is the top-level Evidence Notebook snapshot. Each claim should stay short, source-backed, and reviewable.

## Project Snapshot

### Claim

The repository is now in early Phase A of the dissertation: a local LLM runtime is live, the first single-prompt LLM harness exists, and the main blocker has shifted from runtime/schema setup to extraction reliability and abstention behaviour.

### Evidence

- Project question and objectives are defined in [project_specification.md](project_specification.md).
- The operating research posture is defined in [research_program.md](research_program.md).
- Deterministic `single` and `multi` harnesses are registered in [project_state/harnesses/README.md](../project_state/harnesses/README.md).
- A first 25-row LLM-backed smoke run now exists at [20260424T180629Z_h003_single_prompt_llm_n25.json](../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json).
- The Evidence Notebook direction for project visibility is selected in [agent_visibility_plan.md](agent_visibility_plan.md).
- Phase 1 project-state pages and the Phase 2 session logging convention now exist under `docs/` and `docs/run_logs/`.

### Uncertainty

The current LLM path is only at smoke-test maturity. Ollama/Qwen now returns fast structured or schema-near outputs, but `h003` still over-abstains on many rows and remains below the deterministic baselines.

### Next Action

Keep iteration narrow: reduce `h003` over-abstention on cluster, seizure-free, and windowed frequency cases before starting `h004`.

## Visibility Claim

### Claim

The Evidence Notebook layer now has canonical state pages, a repeatable session logging convention, a generated local dashboard, and backfilled session coverage for the pre-visibility foundation work.

### Evidence

- Canonical state pages: [milestones.md](milestones.md), [active_threads.md](active_threads.md), [decisions.md](decisions.md), and [artifact_registry.md](artifact_registry.md).
- Session logging convention: [run_logs/README.md](run_logs/README.md).
- Session log template: [run_logs/session_log_template.md](run_logs/session_log_template.md).
- Optional companion schema and template: [session_log_companion_schema.json](run_logs/session_log_companion_schema.json), [session_log_companion_template.json](run_logs/session_log_companion_template.json).
- Backfilled historical logs: [20260424T075111Z_initial_scaffold.md](run_logs/20260424T075111Z_initial_scaffold.md), [20260424T084000Z_harness_protocol_and_smoke_runs.md](run_logs/20260424T084000Z_harness_protocol_and_smoke_runs.md), [20260424T085900Z_candidate_retrieval_iteration.md](run_logs/20260424T085900Z_candidate_retrieval_iteration.md).
- Deployable notebook site: [site/index.html](../site/index.html) with static assets at [site/assets/](../site/assets/).
- Dashboard generator: [src/epilepsy_agents/visibility/](../src/epilepsy_agents/visibility/).

### Uncertainty

The dashboard is a static generated artifact. The new historical logs are reconstructed from repo evidence rather than written contemporaneously, so they are faithful summaries but not verbatim session notes.

### Next Action

Regenerate the dashboard after substantial updates to project-state docs or session logs, then proceed to the first curated Phase 4 visual artifact.

## Latest Evaluation Claim

### Claim

The latest completed evaluation work now has two layers: the deterministic paired 100-row smoke still defines the strongest baseline result, and the local `h003_single_prompt_llm` path now runs quickly enough for 25-row smoke testing but remains extraction-fragile.

### Evidence

| Harness | Run | Exact | Monthly 15 pct | Pragmatic micro-F1 | Purist micro-F1 |
| --- | --- | ---: | ---: | ---: | ---: |
| `h002_multi_agent_verify` | [20260424T144559Z_h002_multi_agent_verify_n100.json](../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json) | 0.31 | 0.48 | 0.55 | 0.53 |
| `h001_single_pass` | [20260424T144606Z_h001_single_pass_n100.json](../project_state/runs/20260424T144606Z_h001_single_pass_n100.json) | 0.25 | 0.43 | 0.50 | 0.48 |

The manifest index is [project_state/experiments/manifest.csv](../project_state/experiments/manifest.csv). Session log: [20260424T144639Z_seizure_free_detection_expansion.md](run_logs/20260424T144639Z_seizure_free_detection_expansion.md).

Current LLM smoke:

| Harness | Run | Exact | Monthly 15 pct | Pragmatic micro-F1 | Purist micro-F1 | Invalid-output rate | Mean latency |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `h003_single_prompt_llm` | [20260424T171400Z_h003_single_prompt_llm_n5.json](../project_state/runs/20260424T171400Z_h003_single_prompt_llm_n5.json) | 0.20 | 0.20 | 0.20 | 0.20 | 0.80 | 52.9 s |
| `h003_single_prompt_llm` | [20260424T180607Z_h003_single_prompt_llm_n5.json](../project_state/runs/20260424T180607Z_h003_single_prompt_llm_n5.json) | 0.40 | 0.40 | 0.40 | 0.40 | 0.40 | 0.95 s |
| `h003_single_prompt_llm` | [20260424T180629Z_h003_single_prompt_llm_n25.json](../project_state/runs/20260424T180629Z_h003_single_prompt_llm_n25.json) | 0.20 | 0.28 | 0.36 | 0.32 | 0.28 | 1.29 s |

### Uncertainty

The deterministic 100-row comparison is still a smoke test. The new `h003` 25-row result is a usable local-model smoke, but it is not yet a credible comparison baseline because `unknown` and `no seizure frequency reference` predictions dominate.

### Next Action

Classify the 25-row `h003` abstentions and add a narrow prompt or candidate-span aid for cluster/window/seizure-free cases, then rerun `h003` on the same 25-row slice.

## Data And Governance Claim

### Claim

The current development environment is safe for synthetic-data iteration, while real King's College Hospital letters remain a later governed evaluation stage.

### Evidence

- Synthetic subset details are in [project_specification.md](project_specification.md).
- Real-data export boundaries are documented in [real_data_governance.md](real_data_governance.md).
- Run records store aggregate metrics, row indexes, labels, and safe error categories rather than raw clinical text.

### Uncertainty

The full synthetic dataset and any real-data access are not yet part of the current local evaluation loop.

### Next Action

Maintain the no-raw-real-text rule for logs, prompts, screenshots, run records, and dashboard artifacts.

## Implementation Claim

### Claim

The local codebase already has the scaffolding needed for deterministic evaluation and future provider-backed extraction.

### Evidence

- `src/epilepsy_agents` contains package code for agents, labels, metrics, providers, schema, and CLI behavior.
- Local runtime feasibility and provider architecture notes are recorded in [local_model_feasibility.md](local_model_feasibility.md).
- The standard session workflow is documented in [typical_session_workflow.md](typical_session_workflow.md).

### Uncertainty

The local runtime now works through Ollama, and `think: false` plus a completion cap makes `qwen3.5:4b` fast enough for short smoke runs. The remaining issue is extraction reliability, not provider availability.

### Next Action

Improve `h003` abstention behaviour on `qwen3.5:4b`, then compare whether `qwen3.5:9b` improves validity enough to justify the extra latency.
