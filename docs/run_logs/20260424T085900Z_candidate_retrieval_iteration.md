# Candidate Retrieval Iteration Session

## Session Metadata

- Date: 2026-04-24
- Session objective: Improve deterministic seizure-frequency candidate retrieval, add focused tests, and rerun a paired 100-row synthetic smoke comparison.
- Related active thread: Harness Reliability
- Starting commit: `91d2ba20f2d19c1589f0cc201037f7eeffbdf711`
- Dirty worktree at start: yes; later visibility work shared the same commit window

## Outcome

The deterministic harnesses gained a broader candidate-retrieval pass covering adjacent sentence windows, seizure-like event synonyms, ranged counts written with "or", hyphenated modifiers, shared-window count summation, and dated event count lists. After the final retrieval update, the paired 100-row smoke comparison slightly favored `h002_multi_agent_verify`, so the expansion was kept as a baseline improvement candidate rather than discarded.

## Evidence

- Files changed in the retrieval-and-visibility commit `dd081bd3085172fc8dabcc66615cf4a3ec775470`:
  - `src/epilepsy_agents/agents.py`
  - `tests/test_agents.py`
  - `docs/development_log.md`
  - `project_state/experiments/manifest.csv`
  - `project_state/harnesses/README.md`
- Intermediate 100-row smoke records after the broader retrieval expansion:
  - `project_state/runs/20260424T085945Z_h002_multi_agent_verify_n100.json`
  - `project_state/runs/20260424T085948Z_h001_single_pass_n100.json`
- Final paired 100-row smoke records after the adjacent-window update:
  - `project_state/runs/20260424T090105Z_h002_multi_agent_verify_n100.json`
  - `project_state/runs/20260424T090110Z_h001_single_pass_n100.json`
- Manifest summary:
  - `project_state/experiments/manifest.csv`
- Follow-on note in the harness registry:
  - `project_state/harnesses/README.md`
- Development summary:
  - `docs/development_log.md`

## Uncertainty

The retrieval changes and the first visibility-artifact work were committed together, so this backfilled session isolates the harness iteration conceptually rather than claiming it was the only thing happening in the working tree. The metric lift is still small, and the remaining failures are substantial.

## Handoff

Classify the remaining `unknown_or_no_reference_error`, `seizure_free_error`, and `cluster_error` cases, then rerun the same paired 100-row slice before broadening the experiment surface.

## Decision

Keep this harness variant.

## Privacy Check

No raw real clinical text was written into logs, prompts, screenshots, traces, run records, or exported artifacts.
