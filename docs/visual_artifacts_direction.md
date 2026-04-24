# Visual Artifacts Direction

This document defines the visual language for generated project imagery and the first set of visual outputs to create for the dissertation, README, supporting materials, and presentation deck.

## Purpose

The visuals should document project progress and explain the system clearly. They should not be generic decoration. Each artifact should help a reader understand one of:

- the system architecture;
- the local-first clinical deployment argument;
- the dataset and evaluation design;
- the agent roles;
- the development milestones;
- the privacy and governance constraints.

## Core Style Direction

Use a hybrid of:

1. Clinical Blueprint
2. Evidence Highlighter

This gives the project a coherent family:

- dark, technical blueprint-style posters for architecture, deployment, local model feasibility, and roadmap;
- paper-white evidence/highlighter visuals for dataset examples, evaluation, error analysis, and extraction examples.

The tone should be bold, distinctive, serious, and research-grade. Avoid playful sci-fi, generic AI imagery, floating robot heads, glowing brains, stock hospital photos, or decorative abstractions that do not explain the project.

## Visual Language

### Palette

- Background: deep navy, graphite, or near-black.
- Primary linework: white or soft cool grey.
- Data-flow accent: electric cyan.
- Verification accent: amber.
- Validated output accent: clinical green.
- Error/contradiction accent: magenta or red.
- Evidence-highlight mode: off-white paper with fluorescent cyan, yellow, amber, and green highlights.

### Typography

- Use clean technical sans-serif typography.
- Prefer uppercase section labels for system modules.
- Keep in-image text sparse and highly legible.
- Avoid long paragraphs in generated images.
- For exact dissertation figures with many labels or numbers, prefer code-native diagrams or manually edited text after generation.

### Motifs

- NHS-style clinical letter fragments, anonymised and synthetic-looking.
- Highlighted evidence spans.
- Structured JSON output panels.
- Agent modules as technical panels or workstations.
- Local GPU/server icon inside a secure hospital boundary.
- Verification checks, warnings, confidence indicators.
- Evaluation harness blocks showing metrics and confusion matrices abstractly, not with precise numbers unless added later by code.

### Layout Principles

- Use strong hierarchy: title, pipeline, output.
- Prefer clear horizontal or radial flows over cluttered networks.
- Use generous spacing and a visible evidence trail from input to output.
- Keep the architecture understandable at thumbnail size.
- Make each artifact feel like part of the same visual system.

## Artifact Set

### 1. Project Architecture Poster

Purpose: Explain the end-to-end multi-agent extraction framework.

Suggested composition:

- Dark clinical-blueprint background.
- Left: synthetic epilepsy clinic letter panel with highlighted seizure-frequency evidence.
- Centre: four agent modules connected by cyan data-flow lines:
  - Section and Timeline Agent
  - Field Extractor Agent
  - Verification Agent
  - Aggregator Agent
- Right: structured JSON output panel and evaluation harness.
- Bottom strip: synthetic data -> local/open-source LLMs -> closed-provider synthetic comparison -> future KCH real-data evaluation.

Text to include, sparingly:

- "Training-Free Multi-Agent Epilepsy Letter Extraction"
- "Evidence-grounded structured output"
- "Local-first clinical NLP"
- Agent names above.

Avoid:

- Real patient identifiers.
- Overly detailed metrics.
- Brains, robots, cartoon clinicians, or stock-photo hospitals.

### 2. Local-First Hospital Deployment Diagram

Purpose: Show why local/open-source LLMs are preferred for real patient data.

Suggested composition:

- Secure hospital boundary.
- Local workstation/GPU node inside the boundary.
- Synthetic-data experiments can connect to closed providers outside the boundary.
- Real KCH letters remain inside the secure environment.
- Aggregate metrics only leave the boundary.

Key message:

- "Synthetic comparison can use external APIs; real clinical data stays local."

### 3. Dataset and Evaluation Overview

Purpose: Explain the seizure-frequency task.

Suggested composition:

- Synthetic letter stack.
- Label families:
  - explicit rates;
  - ranges;
  - clusters;
  - seizure-free durations;
  - unknown/no reference.
- Evaluation blocks:
  - exact label;
  - monthly-rate tolerance;
  - pragmatic F1;
  - purist F1;
  - evidence support.

Style:

- Evidence Highlighter mode, mostly off-white paper with colored highlights.

### 4. Agent Role Cards

Purpose: Create reusable visual cards for the four conceptual agents.

Cards:

- Section and Timeline Agent: segments letter and temporal anchors.
- Field Extractor Agent: extracts candidate labels.
- Verification Agent: checks evidence, contradictions, and missingness.
- Aggregator Agent: produces final JSON, confidence, warnings, and citations.

Style:

- Matching dark panels with one distinct accent color per role.

### 5. Milestone Timeline

Purpose: Show project progress and next stages.

Milestones:

- Source materials received.
- Synthetic subset loaded.
- Evaluation harness built.
- Local model feasibility completed.
- Provider architecture added.
- Local model smoke tests.
- Full synthetic evaluation.
- Potential KCH real-data evaluation.
- Dissertation paper and supporting materials.

Style:

- Clinical Blueprint mode with cyan path and milestone nodes.

### 6. Local Model Feasibility Board

Purpose: Explain hardware constraints and local model shortlist.

Content:

- RTX 4070 Laptop GPU, 8 GB VRAM.
- First local candidates:
  - Qwen2.5-7B-Instruct;
  - Qwen3-8B;
  - Phi-4-mini-instruct;
  - Gemma-3-4B-it.
- Stretch candidates:
  - Ministral-8B;
  - Llama-3.1-8B;
  - Gemma-3-12B;
  - Qwen3-14B.

Style:

- Dark technical board with status bands: comfortable, borderline, not first-pass.

### 7. Evidence-Grounding Concept

Purpose: Communicate that predictions must be supported by quotes.

Suggested composition:

- A letter paragraph with highlighted evidence.
- Arrow into extraction label.
- Verification stamp.
- JSON output with evidence span.

Style:

- Evidence Highlighter mode.

### 8. Dissertation / Supporting Materials Cover

Purpose: Create a visual identity for the final package.

Suggested composition:

- Abstracted clinical letter layers, structured JSON, local GPU/server, and evidence trail.
- Minimal title lockup.

Style:

- Formal, restrained, bold.

## First Image Brief: Project Architecture Poster

Use case: infographic-diagram

Asset type: dissertation/README architecture poster

Primary request: Create a bold, distinctive project architecture poster for a training-free multi-agent LLM system that extracts seizure frequency from epilepsy clinic letters.

Scene/backdrop: dark clinical blueprint background with subtle technical grid, no hospital stock photography.

Subject: left-to-right pipeline showing a synthetic epilepsy clinic letter with highlighted evidence spans flowing through four agent modules into structured JSON output and an evaluation harness.

Style/medium: polished editorial technical infographic, clinical AI research poster, high contrast, crisp linework.

Composition/framing:

- Wide landscape poster.
- Left third: synthetic clinical letter panel with 2-3 highlighted phrases.
- Middle: four connected modules:
  - Section and Timeline Agent
  - Field Extractor Agent
  - Verification Agent
  - Aggregator Agent
- Right third: JSON output panel plus evaluation metrics block.
- Bottom strip: synthetic data, local open-source LLMs, closed-provider synthetic comparison, future KCH evaluation.

Lighting/mood: precise, serious, local-first clinical engineering.

Color palette: deep navy/graphite background, white linework, cyan data-flow arrows, amber verification highlights, green validated output.

Text:

- "Training-Free Multi-Agent Epilepsy Letter Extraction"
- "Evidence-grounded structured output"
- "Local-first clinical NLP"
- Agent names as listed above.

Constraints:

- Use only synthetic/anonymised-looking clinical text.
- Keep text sparse and legible.
- Avoid real patient identifiers.
- Avoid cartoon agents, robots, glowing brains, stock hospital scenes, and generic AI swirls.

