# Agent Visibility Plan

## Purpose

This document captures a practical plan for improving visibility into the progress, trajectory, and working state of this agentic coding project.

The goal is to make the project legible at a higher level of abstraction than raw commits, terminal commands, or long markdown logs. The plan combines generated visual artifacts with a lightweight orchestration layer built on top of structured project documents.

## Problem

The repository is progressing well, but the development process is still relatively opaque from a human oversight perspective. It is hard to quickly answer questions such as:

- What has been done recently?
- What path is the project currently following?
- What decisions have been made?
- What work is active, blocked, or next?
- How do code changes connect to the broader dissertation trajectory?

## Research Summary

Current practice in agentic engineering tends to combine multiple visibility layers rather than relying on a single dashboard.

Common tactics include:

- Execution traces and replay systems for model calls, tool use, and intermediate steps.
- Session summaries and audit trails generated from hooks or end-of-run logging.
- Evaluation dashboards that track regressions, experiments, and dataset performance over time.
- Markdown-based memory banks or knowledge bases that preserve project state in structured, human-readable form.
- Higher-level roadmap and timeline views that abstract away low-level implementation noise.
- Curated diagrams and posters that explain architecture, milestones, deployment boundaries, and evidence flow.

## Working Recommendation

The strongest approach for this repository is a four-layer visibility stack:

1. Machine-captured run ledger.
2. Markdown-backed project state.
3. Visual orchestration layer.
4. Curated one-off visual artifacts.

This avoids overloading any single tool. The ledger captures what happened, the markdown layer captures the project state, the orchestration layer makes it navigable, and the visual artifacts make it understandable at a glance.

## Chosen UI Direction: Evidence Notebook

After exploring three distinct interface directions for the visual orchestration layer, the preferred direction is the **Evidence Notebook**.

This direction treats the dashboard less like a generic status board and more like a readable project lab book. The interface should foreground claims, sources, decisions, and next actions, with a clear visual relationship between each high-level statement and the underlying markdown or run-log evidence.

The Evidence Notebook direction is preferred because it best matches the purpose of this repository:

- it supports supervisor review and dissertation writing;
- it makes project progress auditable without exposing raw terminal noise;
- it keeps the source-of-truth documents visible rather than hiding them behind decorative charts;
- it encourages every status claim to be backed by a document, session log, decision, artifact, or evaluation output;
- it can be implemented incrementally on top of simple markdown files before adding richer automation.

The other explored directions remain useful as references:

- **Live Mission Control** is strongest for real-time operational awareness, but risks looking over-precise before the run ledger is mature.
- **Project Atlas** is strongest for high-level storytelling and artifact browsing, but should be saved for a later, more visual presentation layer.

The first implementation of the orchestration layer should therefore use Evidence Notebook principles:

- paper-like pages rather than dashboard-card mosaics;
- annotated summaries with visible source links;
- margin notes for open risks, reviewer questions, and next actions;
- clear sections for current state, milestones, active threads, decisions, recent sessions, and artifacts;
- restrained use of color as evidence highlighting rather than decoration.

This UI direction also changes the content contract for the earlier layers. The markdown-backed project state and run ledger should not be written as generic status dumps. They should be written as notebook-ready claims that can be quoted, annotated, linked, and reviewed.

Each canonical project-state entry should aim to answer:

- What is the current claim?
- What evidence supports it?
- What changed recently?
- What uncertainty or risk remains?
- What is the next useful action?

## Proposed Visibility Stack

### 1. Machine-Captured Run Ledger

Create a structured record for each meaningful Codex work session.

Each entry should ideally capture:

- date and session identifier;
- task objective;
- files touched;
- commands run;
- tests executed;
- outputs generated;
- decisions made;
- blockers or unresolved risks;
- suggested next actions.

For the Evidence Notebook direction, run ledger entries should also include a short human-readable session note:

- outcome: what is now true that was not true before;
- evidence: files, tests, generated artifacts, or command outputs supporting that outcome;
- uncertainty: what was not checked, remains fragile, or needs human review;
- handoff: the most useful next action for the next session.

Possible storage formats:

- markdown with frontmatter;
- JSON files in a `project_state/runs/` folder;
- one markdown file per session in `docs/run_logs/`.

Primary value:

- gives an auditable answer to "what did the agent actually do?"

### 2. Markdown-Backed Project State

Maintain a small number of canonical project-state documents.

Suggested files:

- `docs/current_state.md`
- `docs/milestones.md`
- `docs/active_threads.md`
- `docs/decisions.md`
- `docs/artifact_registry.md`

Suggested purpose of each:

- `current_state.md`: concise project snapshot, current phase, immediate next steps.
- `milestones.md`: completed, active, and upcoming milestones.
- `active_threads.md`: parallel workstreams, questions, experiments, and blockers.
- `decisions.md`: important choices, rationale, and consequences.
- `artifact_registry.md`: generated visuals, diagrams, evaluations, and supporting outputs.

For the Evidence Notebook direction, these files should be structured as source-backed pages rather than loose notes:

- `current_state.md`: concise claims about the project phase, each with evidence links and immediate next actions.
- `milestones.md`: milestone, date/status, outcome, supporting evidence, remaining risk.
- `active_threads.md`: workstream, current question, latest evidence, blocker/risk, next action.
- `decisions.md`: decision, rationale, rejected alternatives, consequence, evidence.
- `artifact_registry.md`: artifact purpose, source inputs, status, output path, intended dissertation or README use.

Primary value:

- provides durable human-readable project memory;
- separates project meaning from raw implementation details;
- creates a stable data source for a future UI layer.

### 3. Visual Orchestration Layer

Build a small local web app that reads the markdown and/or JSON files and presents project state visually.

Suggested views:

- milestone timeline;
- active workstreams;
- recent agent sessions;
- artifact gallery;
- evaluation status;
- open decisions;
- next recommended actions.

Potential implementation styles:

- a lightweight local Next.js app over markdown/json;
- a static site generator with structured content collections;
- a knowledge-base style interface with cards, timelines, and linked records.

Primary value:

- answers "where are we, what is moving, and what matters now?" quickly;
- gives high-level visibility without reading every markdown file manually.

### 4. Curated One-Off Visual Artifacts

Use GPT Images 2.0 and related visual generation workflows to create high-value explanatory artifacts.

These should not replace the orchestration layer. They should sit above it as curated communication assets.

The existing direction in [visual_artifacts_direction.md](C:/Users/cbrow/Code/dissertation/docs/visual_artifacts_direction.md) already defines a strong style system and artifact family.

Priority artifact types:

- project architecture poster;
- local-first hospital deployment diagram;
- dataset and evaluation overview;
- agent role cards;
- milestone timeline;
- local model feasibility board;
- evidence-grounding concept visual;
- dissertation/supporting-materials cover visual.

Primary value:

- makes the project explainable to a supervisor, reader, or future reviewer at a glance;
- creates high-quality dissertation and README support material.

## Recommended Principle

Use the orchestration layer as the source of truth, and use generated visuals as explanatory snapshots.

In other words:

- structured markdown/json underneath;
- visual dashboard on top;
- curated generated posters for explanation and presentation.

This is likely to be more robust than trying to encode the entire project state directly into generated images.

## Proposed Near-Term Implementation Path

### Phase 1: Minimal Visibility Infrastructure

Create the canonical markdown files and define a repeatable Evidence Notebook update pattern.

Deliverables:

- `docs/current_state.md`
- `docs/milestones.md`
- `docs/active_threads.md`
- `docs/decisions.md`
- `docs/artifact_registry.md`
- a simple template for run/session logs
- a shared entry pattern: claim, evidence, uncertainty, next action

Outcome:

- immediate improvement in project legibility without building a UI first;
- project-state content that can later render directly into the Evidence Notebook interface.

Implementation status as of 2026-04-24:

- started with `docs/current_state.md`, `docs/milestones.md`, `docs/active_threads.md`, `docs/decisions.md`, and `docs/artifact_registry.md`;
- added `docs/run_logs/session_log_template.md` as the first session-note pattern;
- the next visibility task is to use these files at session close, then decide whether to backfill historical session logs or build a small local dashboard first.

### Phase 2: Session Logging Convention

Add a lightweight session summary workflow so each substantial coding session produces a structured record and a reviewable session note.

Deliverables:

- session-log template;
- conventions for status labels, decision capture, and next actions;
- optional machine-readable JSON companion files.
- human-readable outcome/evidence/uncertainty/handoff fields for notebook display.

Outcome:

- durable trace of progress and direction over time;
- recent-session content that can be shown without exposing raw terminal noise.

Implementation status as of 2026-04-24:

- added `docs/run_logs/README.md` as the session logging convention;
- added `docs/run_logs/session_log_companion_schema.json` and `docs/run_logs/session_log_companion_template.json` for optional machine-readable companions;
- tightened `docs/run_logs/session_log_template.md` around session IDs, optional companions, and exactly one closing decision label;
- created `docs/run_logs/20260424T092054Z_visibility_phase2.md` as the Phase 2 implementation note;
- the next visibility task is Phase 3: build a minimal local Evidence Notebook dashboard over project-state docs and recent session logs.

### Phase 3: Local Visual Dashboard

Build a minimal local Evidence Notebook dashboard on top of the project-state files.

Minimum viable interface:

- home overview;
- timeline of milestones;
- recent session feed;
- active workstreams panel;
- artifact gallery;
- open decisions list.

Outcome:

- higher-level, always-available project oversight;
- source-backed claims, margin notes, and evidence links rather than a generic dashboard-card mosaic.

Implementation status as of 2026-04-24:

- added `src/epilepsy_agents/visibility.py` as a dependency-free generator for the local Evidence Notebook dashboard;
- added the `epilepsy-agents notebook` CLI command to regenerate the dashboard from project-state markdown and recent session logs;
- generated `docs/evidence_notebook.html` as the first local dashboard artifact;
- added parser coverage in `tests/test_visibility.py`;
- the next visibility task is Phase 4: begin curated visual artifact production, while continuing to regenerate the dashboard after meaningful project-state updates.

### Phase 4: Curated Visual Artifact Production

Generate the first explanatory posters and diagrams using the visual direction already documented.

Suggested first set:

1. Project Architecture Poster
2. Milestone Timeline
3. Local-First Hospital Deployment Diagram
4. Dataset and Evaluation Overview

Outcome:

- immediate improvement in explainability for README, dissertation, and presentations

## Candidate Research References

These references informed the plan and may be useful later when designing implementation details:

- OpenAI Codex product direction: real-time progress and evidence-backed execution views.
- Anthropic Claude Code hooks: hook-based logging and session-level observability.
- LangSmith: tracing, observability, and evaluation workflows for LLM systems.
- Phoenix / OpenInference: open tracing and instrumentation for agentic systems.
- Linear-style project/timeline views: higher-level abstraction over implementation detail.
- Markdown memory-bank approaches in agentic project management systems.

## Initial Conclusion

The visibility problem in this repository is best solved by combining:

- structured project memory;
- session-level execution summaries;
- a lightweight local orchestration interface;
- a curated family of generated explanatory visuals.

This creates a system where progress is both inspectable and interpretable.

## Next Time This Work Is Picked Up

Recommended next action:

Create the markdown-backed project-state layer first, then build the orchestration layer on top of it, then generate the first curated visuals.
