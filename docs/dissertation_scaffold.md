# Dissertation Paper Scaffold

Target: approximately 5,000 words in the supplied eight-page conference-style template.

## Working Title

Evidence-Grounded Multi-Agent LLMs for Training-Free Seizure-Frequency Extraction from Epilepsy Clinic Letters

## Abstract - 180 words

State the clinical problem, privacy constraint, synthetic-data setup, training-free multi-agent approach, evaluation design, main results, and implications for clinical NLP reliability.

## 1. Introduction - 650 words

- Why seizure frequency matters clinically and for research.
- Why clinic-letter extraction is difficult: free text, temporal windows, ranges, clusters, stale history, and missingness.
- Why synthetic clinical letters are relevant for reproducible evaluation.
- Gap: fine-tuned systems can perform well, but training-free LLM workflows need systematic reliability evaluation.
- Contributions:
  - end-to-end multi-agent extraction framework;
  - evidence-grounded schema and evaluation harness;
  - comparison with single-prompt extraction;
  - readiness for full synthetic and real KCH evaluation.

## 2. Related Work - 900 words

Planned structure:

- Clinical NLP and structured extraction from EHR text.
- Epilepsy-specific extraction systems, including ExECT and KCL LLM work.
- Seizure-frequency extraction and temporal reasoning.
- Synthetic clinical text and privacy-preserving evaluation.
- Agentic and verification-based LLM workflows.
- Evidence/rationale evaluation and clinical auditability.

## 3. Data and Task - 600 words

- Describe the synthetic subset and planned full dataset.
- Define seizure-frequency label scheme.
- Explain pragmatic and purist category mappings.
- Explain evidence-span requirement and handling of unknown/no-reference cases.
- State real KCH evaluation as conditional next stage, not assumed available.

## 4. Method - 1,100 words

- Architecture overview figure.
- Section and Timeline Agent.
- Field Extractor Agent.
- Verification Agent.
- Aggregator and schema validation.
- Single-prompt baseline and budget matching.
- Deterministic offline baseline in the repository.
- LLM-backed implementation plan.

## 5. Experiments - 700 words

- Dataset splits and row filtering.
- Metrics: exact label, monthly-rate tolerance, pragmatic/purist F1, evidence support, invalid-output rate.
- Ablations:
  - single prompt vs multi-agent;
  - with/without verification;
  - with/without evidence requirement;
  - self-consistency budget levels.
- Robustness checks for temporal wording, clusters, seizure-free durations, and unknown cases.

## 6. Results - 650 words

Reserve space for:

- Main comparison table.
- Confusion matrix for pragmatic categories.
- Error typology table.
- Token/cost/runtime table.

## 7. Discussion - 850 words

- Interpret whether decomposition improves reliability.
- Compare to Gan et al.'s fine-tuned baseline.
- Discuss where agentic workflows help: evidence, contradiction detection, auditability.
- Discuss where they fail: temporal arithmetic, stale history, ambiguous reference periods.
- Clinical deployment implications and governance constraints.

## 8. Conclusion - 250 words

Summarise the engineering contribution, empirical finding, and next step toward full synthetic and real-data evaluation.

## Figures and Tables

- Figure 1: Multi-agent extraction architecture.
- Table 1: Label categories and normalization rules.
- Table 2: Main results.
- Table 3: Error typology with examples.
- Table 4: Ablation study.

## Supporting Materials

The 30 percent supporting-materials component should include:

- Repository and reproducibility guide.
- Prompt versions and schema definitions.
- Development log and experiment manifest.
- Supplementary error analysis.
- Real-data governance note.

