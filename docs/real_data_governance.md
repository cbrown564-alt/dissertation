# Real Clinical Data Governance Note

The repository is currently safe for synthetic data development. Real King's College Hospital patient letters should be treated as a separate evaluation stage.

## Rules for Real-Data Stage

- Do not commit raw clinical text.
- Do not write raw clinical text into logs, prompts, screenshots, traces, or evaluation artifacts.
- Store only aggregate metrics and de-identified error categories outside the approved environment.
- Ensure any LLM provider is approved for the clinical-data setting; if not, use an internal/offline model only.
- Disable external telemetry.
- Use deterministic run IDs, dataset hashes, and prompt versions rather than patient identifiers.
- Review outputs for accidental PHI leakage before export.

## Recommended Real-Data Evaluation Output

Allowed outside the secure environment, subject to approval:

- aggregate F1/accuracy tables;
- confusion matrices;
- counts of error categories;
- prompt/schema versions;
- runtime and model metadata.

Avoid outside the secure environment:

- raw letters;
- verbatim evidence spans from real letters;
- patient-level predictions;
- examples containing dates, names, NHS numbers, hospital numbers, addresses, or rare clinical narratives.

