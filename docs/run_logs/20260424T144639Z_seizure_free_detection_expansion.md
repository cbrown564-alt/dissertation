# Seizure-Free Detection Expansion

## Session Metadata

- Date: 2026-04-24
- Session objective: Reduce `seizure_free_error` in the deterministic harnesses by broadening seizure-free span detection and label emission, then rerun the paired 100-row synthetic smoke comparison.
- Related active thread: Harness Reliability
- Starting commit: `dd081bd3085172fc8dabcc66615cf4a3ec775470`
- Dirty worktree at start: yes

## Outcome

The deterministic field extractor now recognises seizure-free status across a much wider range of phrasings: explicit numeric durations, numeric negation windows ("no seizures for over N units"), qualitative durations ("for a long duration", "prolonged period"), unit-only durations ("for years"), "since <date>" / "off ASMs since" / "interval since" forms, present-tense statements ("by patient report", "at today's visit", "currently seizure-free"), long-term remission / sustained seizure freedom, verb-phrase negation ("seizure occurrences have not been happening"), and an expanded absence-of-events catch-all. The retrieval frequency-term list also now covers `remission`, `recurrence`, and `seizure freedom`.

On the paired 100-row synthetic smoke after these changes, the multi harness improved meaningfully across every primary metric, and the single baseline improved in step. `seizure_free_error` halved on the multi harness and dropped by six on the single baseline, with no regressions in other error categories.

| Harness | Exact | Monthly 15% | Pragmatic micro-F1 | Purist micro-F1 | NS F1 | `seizure_free_error` | `correct` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `h002_multi_agent_verify` (prior) | 0.20 | 0.35 | 0.42 | 0.40 | 0.26 | 18 | 20 |
| `h002_multi_agent_verify` (new) | 0.31 | 0.48 | 0.55 | 0.53 | 0.82 | 9 | 31 |
| `h001_single_pass` (prior) | 0.18 | 0.33 | 0.40 | 0.38 | 0.00 | 19 | 18 |
| `h001_single_pass` (new) | 0.25 | 0.43 | 0.50 | 0.48 | 0.73 | 13 | 25 |

## Evidence

- Code change: [src/epilepsy_agents/agents.py](../../src/epilepsy_agents/agents.py) — expanded `_extract_from_text` with a structured seizure-free detection sequence and added `remission`, `recurrence`, and `seizure freedom` to `FREQUENCY_TERMS`.
- Tests: [tests/test_agents.py](../../tests/test_agents.py) — eleven new focused cases covering numeric durations, numeric negation windows, qualitative durations, unit-only durations, "since" forms, present-tense forms, remission, absence catch-all, and a past-tense negative test.
- Test run: 26/26 passing under `python -m unittest discover -s tests`.
- New paired 100-row smoke records:
  - [project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json](../../project_state/runs/20260424T144559Z_h002_multi_agent_verify_n100.json)
  - [project_state/runs/20260424T144606Z_h001_single_pass_n100.json](../../project_state/runs/20260424T144606Z_h001_single_pass_n100.json)
- Manifest updated: [project_state/experiments/manifest.csv](../../project_state/experiments/manifest.csv).

## Uncertainty

The 100-row slice is still a smoke test. NS precision on the multi harness is 0.73, so a small number of frequent/infrequent/UNK gold rows are now mispredicted as seizure-free. The qualitative pattern emits `seizure free for multiple month` regardless of whether the duration was actually in years, so rare exact-match cases for seizure-free-for-multiple-year still depend on numeric negation patterns rather than the qualitative fallback. Single-pass retains hard-coded `"before"`/`"after"` guards that suppress some valid matches when a whole letter is used as the single candidate.

## Handoff

Review the six NS false positives in the new multi confusion matrix and the remaining nine `seizure_free_error` cases to decide whether to add past-tense guards in specific patterns, then move on to the next failure family — most likely `unknown_or_no_reference_error` (34 cases on multi) or `cluster_error` (13 cases on multi) — before broadening beyond deterministic changes.

## Decision

keep this harness variant

## Privacy Check

No raw real clinical text was written into logs, prompts, screenshots, traces, run records, or exported artifacts. All evaluation was on the synthetic subset.
