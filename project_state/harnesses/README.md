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
