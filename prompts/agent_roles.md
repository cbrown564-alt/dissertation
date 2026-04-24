# Agent Roles

These prompts define the intended LLM-backed implementation. The current package includes an offline deterministic baseline with the same role boundaries so the evaluation harness is usable before credentials or local model weights are available.

## Section and Timeline Agent

Input: one epilepsy clinic letter.

Tasks:
- Segment administrative header, diagnosis, medication, history, seizure-frequency discussion, investigations, and plan.
- Extract all candidate seizure-frequency statements with character offsets.
- Preserve temporal anchors such as clinic date, "since last visit", "over the last four weeks", and specific months.
- Return JSON only.

## Field Extractor Agent

Input: candidate spans from the Section and Timeline Agent.

Tasks:
- Produce the seizure-frequency label using Gan et al.'s structured label scheme.
- Prefer explicit current or recent frequency over remote history.
- Preserve cluster structure as `<n> cluster per <period>, <m> per cluster`.
- Return supporting quotes; answer `unknown` or `no seizure frequency reference` if unsupported.

## Verification Agent

Input: letter, extracted label, candidate evidence.

Tasks:
- Check that the label is directly supported by evidence.
- Identify contradictions, stale history, missing frequency, and ambiguous windows.
- Reject unsupported labels.
- Return confidence and warnings.

## Aggregator Agent

Input: verified candidate outputs.

Tasks:
- Emit final JSON with label, normalized monthly rate, pragmatic/purist class, evidence, confidence, and warnings.
- Keep output schema stable for automated evaluation.
