# Decisions

Last updated: 2026-04-24.

This page records decisions that shape the project and should not be rediscovered every session.

## D001: Treat The Project As A Harness-Reliability Study

### Decision

The central research posture is harness reliability, not a simple model leaderboard.

### Rationale

The dissertation question is whether constrained, evidence-grounded extraction improves seizure-frequency reliability under matched budgets.

### Rejected Alternatives

- Optimizing only for one aggregate score.
- Comparing unrelated models without stable harness controls.

### Consequence

Each meaningful change should alter one harness, prompt, provider, verification rule, or visibility artifact, then be evaluated through a fixed metric bundle.

### Evidence

[research_program.md](research_program.md), [harness_experiment_protocol.md](harness_experiment_protocol.md).

## D002: Keep Deterministic Baselines Before LLM Expansion

### Decision

The repository starts with deterministic `single` and `multi` harnesses that mirror planned role boundaries.

### Rationale

This gives a reproducible offline baseline before provider variance, cost, latency, and schema failures enter the study.

### Rejected Alternatives

- Starting directly with closed-provider prompt experiments.
- Treating deterministic extraction as clinically useful output.

### Consequence

Deterministic metrics provide the first comparison floor, but the system must not claim final LLM or clinical performance from them.

### Evidence

[project_specification.md](project_specification.md), [project_state/harnesses/README.md](../project_state/harnesses/README.md), [project_state/experiments/manifest.csv](../project_state/experiments/manifest.csv).

## D003: Use The Pareto Frontier Rule For Harness Selection

### Decision

Keep candidate harnesses that are non-dominated across reliability, evidence support, invalid-output behavior, and cost/runtime rather than forcing a single early winner.

### Rationale

Clinical extraction quality is multi-dimensional. A slightly better F1 score may not be worth unsupported claims or poor abstention behavior.

### Rejected Alternatives

- Selecting only the highest pragmatic micro-F1.
- Discarding slower but more auditable candidates too early.

### Consequence

Run records must retain enough information to compare class F1, monthly-rate accuracy, exact label accuracy, safe error categories, and later provider/runtime metadata.

### Evidence

[harness_experiment_protocol.md](harness_experiment_protocol.md), [evaluation_protocol.md](evaluation_protocol.md).

## D004: Keep Closed Providers Synthetic-Only Unless Governance Changes

### Decision

Closed-provider experiments are acceptable only for synthetic data in the current repository context.

### Rationale

Real clinical text must not leave the approved environment or enter external logs, traces, prompts, screenshots, or artifacts without explicit governance approval.

### Rejected Alternatives

- Treating API keys as permission to process real clinical data.
- Exporting real examples for qualitative error analysis.

### Consequence

Provider adapters must make data-governance boundaries explicit, and real-data evaluation outputs must be aggregate and de-identified.

### Evidence

[real_data_governance.md](real_data_governance.md), [local_model_feasibility.md](local_model_feasibility.md).

## D005: Prefer A Local Runtime For Real-Data Readiness

### Decision

The first local inference path should use an OpenAI-compatible local server such as LM Studio, Ollama, or llama.cpp server.

### Rationale

The real-data stage needs a plausible local/offline pathway. A server interface also keeps orchestration separated from model runtime.

### Rejected Alternatives

- Directly wiring the extraction harness to one Python inference library first.
- Making closed providers the default architecture.

### Consequence

Provider code should stay modular and record runtime/model metadata for reproducibility.

### Evidence

[local_model_feasibility.md](local_model_feasibility.md), [src/epilepsy_agents/providers.py](../src/epilepsy_agents/providers.py).

## D006: Use Evidence Notebook As The Visibility Direction

### Decision

The visual orchestration layer should use the Evidence Notebook direction.

### Rationale

The project needs source-backed, supervisor-reviewable claims rather than a generic operational dashboard.

### Rejected Alternatives

- Live Mission Control as the first implementation.
- Project Atlas as the first implementation.

### Consequence

Project-state files should be written as claim, evidence, uncertainty, and next-action entries that can later render into a local dashboard.

### Evidence

[agent_visibility_plan.md](agent_visibility_plan.md), [agent_visibility_ui_mockups.html](agent_visibility_ui_mockups.html).

