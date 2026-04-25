# Research Program

## Purpose

This file is the operating brief for future agent-assisted work on the repository. It adapts the useful parts of autoresearch, Meta-Harness, and reflective prompt-optimization workflows to this dissertation project.

The project should be treated as a harness-reliability study, not simply as a model comparison. The central question is whether a constrained, evidence-grounded extraction harness improves seizure-frequency extraction compared with simpler prompting under matched budgets.

## Research Posture

Work in small, comparable loops:

- change one meaningful harness, prompt, provider, or verification component at a time;
- run a fixed synthetic-data evaluation slice before broader runs;
- record the run in structured form;
- keep improvements only when they improve the agreed metric bundle without creating unacceptable regressions;
- turn failures into reusable error taxonomy entries and next actions.

Do not run autonomous loops on real clinical text. Real King's College Hospital data, if used later, must stay inside the approved environment and must not be written into traces, prompts, screenshots, run logs, or exported artifacts.

## Current Harnesses

The repository currently supports deterministic offline harnesses that mirror the planned LLM role boundaries:

- `single`: a single-pass baseline over the letter text.
- `multi`: section/timeline candidate selection, field extraction, verification, and aggregation.

Future harness variants should receive stable IDs before results are compared, for example:

- `h001_single_pass`
- `h002_multi_agent_verify`
- `h003_multi_agent_evidence_required_llm`
- `h004_multi_agent_self_consistency_3`
- `h005_multi_agent_self_consistency_5`

## Project Phases

The project roadmap is tracked as explicit phases in [milestones.md](milestones.md). The phases align the harness IDs above to the dissertation's critical path:

- **Delivered infrastructure**: repo scaffold, deterministic `single` and `multi` harnesses, evaluation harness, run manifest, session logging, and Evidence Notebook dashboard.
- **Phase A — Stand up the LLM path**: local runtime live (M-A1), `h003_single_prompt_llm` schema-constrained smoke (M-A2), `h004_multi_agent_llm` role-separated pipeline with the first paired `h003` vs `h004` comparison (M-A3).
- **Phase B — Reliability interventions**: evidence-requiring verification (M-B1), self-consistency `h005_*` at k=3 and k=5 (M-B2), evidence-required vs answer-only ablation (M-B3). Phase B is where the dissertation's primary results come from.
- **Phase C — Scale and external baselines**: full synthetic corpus (M-C1), Gan et al. fine-tuned baseline comparison (M-C2), optional budget-matched closed-provider comparison on synthetic data (M-C3).
- **Phase D — Locked-down real-data evaluation**: governance-gated real KCH letter evaluation with aggregate-metrics-only export (M-D1). Optional.
- **Phase E — Dissertation and packaging**: first draft (M-E1), curated visual artifacts (M-E2), final paper and reproducibility guide (M-E3).

The deterministic harnesses remain the reproducible offline floor per [D002](decisions.md), but further deterministic regex expansion is explicitly frozen per [D007](decisions.md). New research effort should improve Phase A quality (abstention and schema validity on `h003`) before building `h004`.

## Allowed Experimental Variables

Good harness-level variables:

- candidate-span retrieval policy;
- role separation and message structure;
- evidence requirements;
- verifier prompts or deterministic verification rules;
- aggregation and conflict-resolution policy;
- schema strictness and retry policy;
- self-consistency sample count;
- local model/provider choice for synthetic or approved local evaluation;
- closed-provider comparison on synthetic data only.

Avoid changing multiple variables in one experiment unless the experiment is explicitly marked as a combined intervention.

## Fixed Controls

Each comparable run should record:

- dataset path and SHA-256 hash;
- whether only `row_ok` rows were used;
- row limit or full-run status;
- pipeline/harness ID;
- prompt/schema version when LLM-backed;
- provider and model when LLM-backed;
- temperature and decoding constraints;
- date and code commit if available;
- runtime and token/cost metadata when available.

## Acceptance Rule

A harness change is worth keeping as a candidate if it improves at least one primary reliability metric without materially worsening safety or auditability.

Primary metric bundle:

- pragmatic micro-F1;
- purist micro-F1;
- monthly-rate match within 15 percent tolerance;
- exact structured-label accuracy.

Safety and auditability checks:

- invalid-output rate;
- evidence support rate;
- unknown/no-reference handling;
- abstention behaviour;
- runtime and token budget.

When metrics disagree, keep the candidate on a Pareto frontier instead of forcing a single winner too early.

## Failure Feedback

Every substantial run should produce text-free error categories that can be inspected safely:

- `class_confusion`
- `monthly_rate_mismatch`
- `exact_label_mismatch`
- `unsupported_or_empty_prediction`
- `unknown_or_no_reference_error`
- `seizure_free_error`
- `cluster_error`
- `format_or_schema_error`

Representative synthetic examples may be reviewed during development, but real clinical examples must not be exported.

## Human Review Points

Pause for human review before:

- changing real-data governance behaviour;
- adding external telemetry;
- sending real clinical text to any provider;
- treating a synthetic-data improvement as a clinical conclusion;
- replacing the canonical evaluation metric bundle;
- broadening autonomous editing beyond the harness/prompt/config surface.

## Next Agent Checklist

Before starting:

- read `docs/project_specification.md`;
- read `docs/evaluation_protocol.md`;
- read `docs/real_data_governance.md`;
- read this file;
- inspect recent records under `project_state/runs/`;
- inspect `project_state/experiments/manifest.csv`.

Before finishing:

- run the smallest relevant evaluation;
- write or update a structured run record;
- update the manifest;
- record unresolved risks or next actions.
