# Project Specification

## Title

Training-Free Multi-Agent LLM System for Epilepsy Letter Extraction

## Supervisor and Context

Supervisor: Yujian Gan.

This project follows Gan et al.'s synthetic clinical letter work on seizure-frequency information extraction. The initial evaluation will reuse the released synthetic subset in `synthetic_data_subset_1500.json`, then move to the full synthetic dataset when available. If the multi-agent system outperforms the fine-tuned baseline reported by Gan et al. on seizure-frequency extraction, the next evaluation stage will use real patient data from King's College Hospital under the applicable governance approvals.

## Problem

Epilepsy clinic letters contain clinically important information such as seizure frequency, seizure type, epilepsy type, anti-seizure medication, investigations, and management plans. Much of this information is written in variable free text, with temporal phrases such as "since the last review", "two events over five months", "cluster days twice this month", and "seizure-free since June". This makes extraction difficult for rule-based systems, single-prompt LLMs, and fine-tuned models.

The core research question is:

Can a training-free, evidence-grounded multi-agent LLM framework improve reliability of seizure-frequency extraction compared with a single-prompt extractor under the same inference budget, and ultimately compete with or exceed the fine-tuned model baseline from Gan et al.?

## Objectives

- Build a reproducible end-to-end extraction framework with role-separated agents.
- Implement an evaluation harness for exact labels, normalized monthly rates, pragmatic categories, purist categories, confidence, and evidence support.
- Compare single-prompt and multi-agent extraction under matched budget constraints.
- Evaluate self-consistency, evidence requirements, schema validation, and verification as reliability interventions.
- Prepare the system for full synthetic data and later locked-down real clinical evaluation.
- Produce a 5,000-word dissertation paper and supporting materials describing the design, implementation, evaluation, and limitations.

## Initial System Design

The framework uses four conceptual roles:

- Section and Timeline Agent: segments the letter and identifies seizure-relevant spans.
- Field Extractor Agent: extracts seizure-frequency labels from evidence spans.
- Verification Agent: checks evidence support, contradictions, missingness, and temporal recency.
- Aggregator Agent: emits final structured JSON with label, evidence, confidence, warnings, and normalized classes.

The current implementation provides deterministic offline agents with these same boundaries. This allows local evaluation before external LLM providers or local model weights are configured.

## Data

Current data:

- `synthetic_data_subset_1500.json`: 1,500 synthetic letters.
- 1,435 rows are currently marked `row_ok = true`.
- Each row includes the letter text, a normalized seizure-frequency label, reference evidence, and quality-check fields.

Planned data:

- Full synthetic dataset from Gan et al.
- Potential real King's College Hospital clinical letters for final evaluation, only inside the approved environment.

## Methods

1. Establish a deterministic baseline and evaluation harness.
2. Add LLM-backed provider adapters while preserving the same output schema.
3. Run paired experiments comparing:
   - single-prompt extraction;
   - multi-agent extraction;
   - multi-agent plus verification;
   - multi-agent plus self-consistency;
   - evidence-required outputs versus answer-only outputs.
4. Evaluate all systems on the synthetic subset, then the full synthetic dataset.
5. If performance justifies it and governance permits, evaluate on KCH real letters without exporting raw clinical text.

## Metrics

- Exact structured-label accuracy.
- Normalized monthly-rate match within tolerance.
- Purist class micro/macro/weighted F1.
- Pragmatic class micro/macro/weighted F1.
- Evidence support rate.
- Invalid JSON/schema failure rate.
- Abstention and unknown handling.
- Runtime and token budget.

## Anticipated Contributions

- A reproducible agentic extraction harness for temporally complex clinical information.
- Evidence-grounded extraction outputs that support clinical audit.
- A careful comparison between training-free agent design and fine-tuned synthetic-data supervision.
- A dissertation case study in privacy-aware clinical NLP engineering.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Full synthetic data delayed | Limits statistical power | Keep subset harness working and design ingestion for drop-in full data |
| Real clinical data unavailable | Limits external validity | Frame real-data evaluation as next stage and report synthetic-only results honestly |
| LLM outputs are unstable | Invalid outputs and noisy metrics | Use JSON schema validation, retries, evidence requirements, and deterministic decoding |
| Multi-agent pipeline costs too much | Unfair comparison | Match token and call budgets with single-prompt baselines |
| Evidence spans are unsupported | Reduced clinical trust | Verification agent rejects unsupported claims |
| Privacy or governance constraints | Blocks real-data experiments | Never persist raw real letters outside approved systems; evaluate aggregate metrics only |

## Timeline

| Phase | Output |
| --- | --- |
| Setup and source review | Repository scaffold, literature map, first specification |
| Baseline harness | Data loader, label parser, metrics, deterministic baseline |
| LLM agent implementation | Provider adapters, prompts, schema validation, retry logic |
| Synthetic experiments | Single vs multi-agent comparison on subset and full data |
| Robustness experiments | Self-consistency, evidence requirement, ablations |
| Dissertation drafting | 5,000-word paper, figures, tables, references |
| Final packaging | Documentation, reproducibility guide, supporting materials |

