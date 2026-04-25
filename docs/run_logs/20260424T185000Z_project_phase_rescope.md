# Project Phase Re-scope

## Session Metadata

- Date: 2026-04-24
- Session ID: 20260424T185000Z_project_phase_rescope
- Session objective: Restructure the core project-state documentation into explicit Phase A-E milestones so the dissertation's critical path is visible at the top of every future session.
- Related active thread: Harness Reliability, Provider And Local Model Setup
- Starting commit: `dd081bd3085172fc8dabcc66615cf4a3ec775470`
- Dirty worktree at start: yes
- Optional JSON companion: none

## Outcome

The core project-state documentation now names five research phases with stable milestone IDs:

- Phase A: Stand up the LLM path (M-A1 Complete, M-A2 In progress, M-A3 Planned).
- Phase B: Reliability interventions (M-B1 evidence-requiring verification, M-B2 self-consistency, M-B3 evidence-required vs answer-only ablation).
- Phase C: Scale and external baselines (M-C1 full synthetic corpus, M-C2 Gan et al. fine-tuned baseline comparison, M-C3 optional budget-matched closed-provider comparison on synthetic).
- Phase D: Locked-down real-data evaluation (M-D1, governance-gated and optional).
- Phase E: Dissertation and packaging (M-E1 draft, M-E2 curated visuals, M-E3 final paper and reproducibility guide).

Deterministic regex expansion is frozen per [D007](../decisions.md); the deterministic harnesses stay as the reproducible offline floor per [D002](../decisions.md) but are no longer an active development target. The dissertation's central question is answered primarily by Phase A-C work, not by further rule-based tuning.

## Evidence

- Milestones restructured into Delivered Infrastructure plus Phases A-E in [milestones.md](../milestones.md).
- Current Phase A progress (M-A1 Complete on Ollama `qwen3.5:4b`; M-A2 In progress with three h003 records) reflected in [current_state.md](../current_state.md) and [active_threads.md](../active_threads.md).
- [D007](../decisions.md) Freeze Further Deterministic Regex Expansion recorded.
- Project Phases section added to [research_program.md](../research_program.md) mapping harness IDs to milestones.
- Phase A kickoff and project re-scope entries added to [development_log.md](../development_log.md).
- No code or test changes in this session; no new run records produced.

## Uncertainty

Phase D may never happen — it is fully governance-gated and optional. Phase E visual artifacts are still "Planned" and should later be cross-linked with [visual_artifacts_direction.md](../visual_artifacts_direction.md). The new phase vocabulary is retrofitted onto earlier session logs, so cross-references to pre-phase work are necessarily loose. The harnesses registry still lists `h004` and `h005` as "pending" rather than phase-tagged; that is fine for now and can be tightened when each becomes a serious comparison target.

## Handoff

Next useful action is M-A2 continuation: classify the `h003_single_prompt_llm` abstentions on [20260424T180629Z_h003_single_prompt_llm_n25.json](20260424T180629Z_h003_single_prompt_llm_n25.json), add one narrow intervention (prompt or candidate-span aid) for cluster, window, and seizure-free cases, and rerun h003 on the same 25-row slice. Only then consider M-A3 (`h004_multi_agent_llm`). Do not return to deterministic regex expansion — see [D007](../decisions.md).

## Decision

documentation/visibility updated, no metric decision needed

## Privacy Check

Confirmed: no raw real clinical text was written into logs, prompts, screenshots, traces, run records, or exported artifacts.
