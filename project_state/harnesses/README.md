# Harness Registry

This directory records named extraction-harness variants.

Current canonical IDs:

| Harness ID | Pipeline | Status | Description |
| --- | --- | --- | --- |
| `h001_single_pass` | `single` | implemented | Deterministic single-pass baseline over the letter text. |
| `h002_multi_agent_verify` | `multi` | implemented | Deterministic section/timeline, extractor, verifier, and aggregator baseline. |
| `h003_single_prompt_llm` | pending | planned | Future one-call LLM baseline with schema-constrained output. |
| `h004_multi_agent_llm` | pending | planned | Future LLM-backed role-separated extraction pipeline. |
| `h005_multi_agent_self_consistency_3` | pending | planned | Future LLM-backed multi-agent pipeline with three sampled candidates. |

Add a short note here whenever a harness variant becomes a serious comparison target.

## Notes

- 2026-04-24: `h002_multi_agent_verify` now includes an adjacent-window candidate retrieval expansion for deterministic synthetic smoke testing. Paired 100-row run `20260424T090105Z_h002_multi_agent_verify_n100` narrowly outperformed the matched `h001_single_pass` run `20260424T090110Z_h001_single_pass_n100`, but remaining error categories show this is still a baseline harness rather than a final extractor.
- 2026-04-24: Both harnesses now include a broadened deterministic seizure-free detector covering qualitative durations, "since" forms, present-tense statements, remission, and a wider absence-of-events catch-all. Paired 100-row runs after the change: `20260424T144559Z_h002_multi_agent_verify_n100` (exact 0.31, monthly 0.48, pragmatic 0.55, purist 0.53, NS F1 0.82) and `20260424T144606Z_h001_single_pass_n100` (exact 0.25, monthly 0.43, pragmatic 0.50, purist 0.48, NS F1 0.73). `seizure_free_error` halved on multi; other error categories are unchanged or slightly improved.
