# Milestones

Last updated: 2026-04-24.

This page tracks project progress as source-backed milestones rather than a loose changelog. Milestones are grouped into delivered infrastructure and the remaining dissertation phases.

The dissertation's central research question — whether a training-free, evidence-grounded multi-agent LLM framework improves seizure-frequency extraction reliability compared with a single-prompt LLM baseline under matched budgets, and whether it approaches the Gan et al. fine-tuned baseline — is answered primarily by the Phase A–C work below. The deterministic harnesses and visibility layer are the floor beneath those experiments, not the contribution itself.

## Delivered Infrastructure

| Milestone | Status | Outcome | Evidence | Remaining Risk | Next Action |
| --- | --- | --- | --- | --- | --- |
| Source materials and project frame | Complete | Dissertation question, objectives, data plan, methods, metrics, and risks are defined. | [project_specification.md](project_specification.md), [literature_review_map.md](literature_review_map.md), [dissertation_scaffold.md](dissertation_scaffold.md) | Scope may change if full synthetic or real-data access differs from assumptions. | Keep the research question stable while harnesses mature. |
| Repository scaffold | Complete | Python package, deterministic agents, CLI, metrics, label parser, tests, and initial docs exist. | [development_log.md](development_log.md), [pyproject.toml](../pyproject.toml), [tests](../tests) | Deterministic code is a baseline, not the final LLM-backed system. | Preserve deterministic comparability while adding providers. |
| Synthetic subset loaded | Complete | The 1,500-row synthetic subset is available for local evaluation, with `row_ok` filtering used by default. | [project_specification.md](project_specification.md), [synthetic_data_subset_1500.json](../synthetic_data_subset_1500.json) | The full synthetic dataset is not yet integrated. | Keep data ingestion compatible with a future full-dataset drop-in. |
| Evaluation harness | Complete | Metrics cover exact labels, monthly-rate tolerance, pragmatic classes, and purist classes. | [evaluation_protocol.md](evaluation_protocol.md), [src/epilepsy_agents/metrics.py](../src/epilepsy_agents/metrics.py) | Evidence support and invalid-output metrics need more importance once LLM output is active. | Add provider-backed output validation and evidence-support checks (see M-A2, M-B1). |
| Harness experiment protocol | Complete | Runs are recorded under `project_state/runs/` and indexed in a manifest. | [harness_experiment_protocol.md](harness_experiment_protocol.md), [project_state/experiments/manifest.csv](../project_state/experiments/manifest.csv) | Some run records are from smoke tests and should not be overinterpreted. | Continue fixed-budget paired comparisons. |
| Initial paired smoke evaluations | Complete | `single` and `multi` deterministic baselines have 20-row and 100-row paired synthetic records. | [20260424T144559Z_h002_multi_agent_verify_n100.json](../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json), [20260424T144606Z_h001_single_pass_n100.json](../project_state/runs/20260424T144606Z_h001_single_pass_n100.json) | Deterministic results are the floor, not the study. | Freeze deterministic tuning (see [D007](decisions.md)) and move to Phase A. |
| Seizure-free detection expansion | Complete | Deterministic extractor now covers numeric, qualitative, unit-only, and "since"/present-tense seizure-free phrasings; multi exact 0.20->0.31 and NS F1 0.26->0.82 on the paired 100-row smoke. | [src/epilepsy_agents/agents.py](../src/epilepsy_agents/agents.py), [tests/test_agents.py](../tests/test_agents.py), [20260424T144559Z_h002_multi_agent_verify_n100.json](../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json), [20260424T144606Z_h001_single_pass_n100.json](../project_state/runs/20260424T144606Z_h001_single_pass_n100.json), [20260424T144639Z_seizure_free_detection_expansion.md](run_logs/20260424T144639Z_seizure_free_detection_expansion.md) | NS precision 0.73 on multi; residual regex-tuning has diminishing returns. | Do not pursue further deterministic regex expansion (see [D007](decisions.md)). |
| Local model feasibility | Complete | Hardware, runtime options, candidate model tiers, and provider requirements are documented. | [local_model_feasibility.md](local_model_feasibility.md) | No local runtime is currently installed or responding. | Resolved in M-A1. |
| Visibility Phase 1: project-state layer | Complete | Canonical Evidence Notebook pages exist for current state, milestones, active threads, decisions, and artifacts. | [agent_visibility_plan.md](agent_visibility_plan.md), [current_state.md](current_state.md), [active_threads.md](active_threads.md), [decisions.md](decisions.md), [artifact_registry.md](artifact_registry.md) | Pages are manually maintained. | Update at the end of substantial sessions. |
| Visibility Phase 2: session logging | Complete | Session logging has naming rules, required sections, status labels, evidence rules, privacy rules, a template, optional JSON companion files, and a first historical backfill. | [run_logs/README.md](run_logs/README.md), [session_log_template.md](run_logs/session_log_template.md), [session_log_companion_schema.json](run_logs/session_log_companion_schema.json) | Backfilled notes are reconstructions. | Use the convention prospectively. |
| Visibility Phase 3: local dashboard | Complete | A generated static Evidence Notebook dashboard renders current claims, milestones, recent sessions, active threads, artifacts, and decisions. | [evidence_notebook.html](evidence_notebook.html), [src/epilepsy_agents/visibility.py](../src/epilepsy_agents/visibility.py), [tests/test_visibility.py](../tests/test_visibility.py) | Dashboard regenerates manually. | Regenerate with `epilepsy-agents notebook` after substantial state updates. |
| Historical notebook backfill | Complete | Reconstructed records exist for the initial scaffold, harness protocol and first paired smoke runs, and the candidate retrieval iteration. | [20260424T075111Z_initial_scaffold.md](run_logs/20260424T075111Z_initial_scaffold.md), [20260424T084000Z_harness_protocol_and_smoke_runs.md](run_logs/20260424T084000Z_harness_protocol_and_smoke_runs.md), [20260424T085900Z_candidate_retrieval_iteration.md](run_logs/20260424T085900Z_candidate_retrieval_iteration.md) | Backfills are reconstructions, not contemporaneous notes. | Keep future session logs contemporaneous. |

## Phase A: Stand Up The LLM Path

The current baseline is entirely rule-based. Phase A replaces the rule engine with an actual LLM under the same role boundaries so the dissertation's research question can start being answered.

| Milestone | Status | Intended Outcome | Evidence Source | Remaining Risk | Next Action |
| --- | --- | --- | --- | --- | --- |
| M-A1 Local runtime live | Planned | One OpenAI-compatible local server (LM Studio, Ollama, or llama.cpp server) is running a candidate model (e.g. Qwen2.5-7B-Instruct, Phi-4-mini, or Gemma-3-4B-it) and responds to `src/epilepsy_agents/providers.py`. | [local_model_feasibility.md](local_model_feasibility.md), [src/epilepsy_agents/providers.py](../src/epilepsy_agents/providers.py) | 8 GB laptop VRAM constrains quantization; candidate model must support JSON-schema-constrained output. | Install LM Studio or Ollama, load one 7B-class instruct model, and round-trip a minimal prompt through the provider adapter. |
| M-A2 h003 single-prompt LLM smoke | Planned | 25-50 synthetic letters run end-to-end through `h003_single_prompt_llm` with JSON-schema validation, retries, and fixed temperature. Primary deliverables: first LLM run record, invalid-output rate, latency, token budget per row. | [harness_experiment_protocol.md](harness_experiment_protocol.md), [project_state/harnesses/README.md](../project_state/harnesses/README.md), [prompts/agent_roles.md](../prompts/agent_roles.md) | Model may emit invalid JSON before schema-constrained decoding is tuned. | Implement h003 harness and record the first LLM-backed run against the live local model. |
| M-A3 h004 multi-agent LLM pipeline | Planned | Role-separated LLM pipeline mirroring deterministic `multi`: section/timeline, extractor, verifier, aggregator, each with its own prompt and schema. Produce first paired `h003` vs `h004` n=100 synthetic record at matched budgets. | [prompts/agent_roles.md](../prompts/agent_roles.md), [project_state/harnesses/README.md](../project_state/harnesses/README.md) | Token/call budget parity must be measured, not assumed. | Build h004 on top of h003 provider plumbing and run first paired n=100 smoke. |

## Phase B: Reliability Interventions (The Study)

Phase B produces the actual dissertation results: which harness interventions improve reliability under matched budgets, measured on the primary metric bundle plus the safety/auditability secondary bundle.

| Milestone | Status | Intended Outcome | Evidence Source | Remaining Risk | Next Action |
| --- | --- | --- | --- | --- | --- |
| M-B1 Verification with evidence requirement | Planned | Verifier rejects extractor outputs lacking evidence-span support. Measure change in pragmatic micro-F1, purist micro-F1, evidence support rate, and invalid-output rate vs. h004 without verification. | [project_specification.md](project_specification.md), [evaluation_protocol.md](evaluation_protocol.md) | Strict verification can over-abstain; tradeoff must be read on the Pareto frontier ([D003](decisions.md)). | Add verifier prompt once h004 is stable. |
| M-B2 h005 self-consistency | Planned | Sample k=3 then k=5, aggregate by agreement. Compare at matched call budget and matched token budget against h003 and against h004 without self-consistency. | [harness_experiment_protocol.md](harness_experiment_protocol.md), [research_program.md](research_program.md) | Cost scaling with k; sampling variance on small synthetic slices. | Add sampling controller to the provider adapter after M-B1. |
| M-B3 Evidence-required vs answer-only ablation | Planned | Fixed paired comparison of h004 with evidence-required schema versus answer-only schema. Report evidence support, invalid-output rate, and class F1. | [evaluation_protocol.md](evaluation_protocol.md) | Schema changes touch both prompt and metrics code. | Run after M-B2 on the same synthetic slice. |

## Phase C: Scale And External Baselines

Phase C moves from smoke to a comparison the dissertation can stand on.

| Milestone | Status | Intended Outcome | Evidence Source | Remaining Risk | Next Action |
| --- | --- | --- | --- | --- | --- |
| M-C1 Full synthetic corpus run | Planned | Rerun the Pareto comparison on the full synthetic dataset once released, with confidence intervals. | [project_specification.md](project_specification.md) | Dataset release timing is outside our control. | Keep the loader drop-in compatible; ingest when Gan et al. publish the full set. |
| M-C2 Gan et al. fine-tuned baseline comparison | Planned | On the same synthetic slice, compare our best Pareto candidate against the published fine-tuned baseline (reported numbers or released model outputs). | [project_specification.md](project_specification.md), [literature_review_map.md](literature_review_map.md) | Evaluation setup must be comparable; metric cuts may differ. | Request or reproduce baseline numbers after Phase B. |
| M-C3 Budget-matched closed-provider comparison | Planned | Matched call/token budgets across one local model and one closed provider, synthetic-only per [D004](decisions.md). | [real_data_governance.md](real_data_governance.md), [decisions.md](decisions.md) | Cost; provider variance; no real data. | After Phase B, decide if an external reference point materially strengthens the dissertation. |

## Phase D: Locked-Down Real-Data Evaluation (governance-gated)

Phase D is optional and only runs if synthetic results justify it and KCH governance permits.

| Milestone | Status | Intended Outcome | Evidence Source | Remaining Risk | Next Action |
| --- | --- | --- | --- | --- | --- |
| M-D1 Real KCH evaluation inside approved environment | Blocked by governance | Evaluate best Pareto candidate on real KCH letters inside the approved environment; export only aggregate metrics and de-identified error-category counts. | [real_data_governance.md](real_data_governance.md), [decisions.md](decisions.md) | Governance approval, environment availability, time budget; strict no-raw-text export. | Revisit only when Phase B/C synthetic results and governance both support it. |

## Phase E: Dissertation And Packaging

Phase E converts Phase A–C results into the conference-format paper and supporting materials.

| Milestone | Status | Intended Outcome | Evidence Source | Remaining Risk | Next Action |
| --- | --- | --- | --- | --- | --- |
| M-E1 First dissertation draft | Planned | Methods, synthetic results, error taxonomy, and discussion fitted to the 8-page conference template (~5,000 words). | [dissertation_scaffold.md](dissertation_scaffold.md), [README.md](../README.md) | Results from Phase B must exist before drafting results. | Begin outlining methods and results as Phase B produces numbers. |
| M-E2 Curated visual artifacts | Planned | Architecture poster, dataset/evaluation diagram, agent-role diagram, milestone timeline, local-first hospital deployment diagram, evidence-grounding figure. | [visual_artifacts_direction.md](visual_artifacts_direction.md), [artifact_registry.md](artifact_registry.md) | Visuals risk being decorative if unmoored from results. | Generate the first architecture poster and a phase-aware milestone timeline. |
| M-E3 Final paper and reproducibility guide | Planned | Submit-ready dissertation, commands-to-reproduce section, and a reproducible run export. | [README.md](../README.md), [evaluation_protocol.md](evaluation_protocol.md) | Scope creep if Phase D is attempted too late. | Enter after M-E1 draft cycle. |
