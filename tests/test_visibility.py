import unittest
from pathlib import Path
import shutil

from epilepsy_agents.visibility import (
    build_dashboard,
    parse_active_threads,
    parse_current_state,
    parse_table,
    parse_tables,
)


class VisibilityParsingTests(unittest.TestCase):
    def test_parse_current_state_claim(self) -> None:
        claims = parse_current_state(
            """# Current State

## Project Snapshot

### Claim

The project has a source-backed dashboard.

### Evidence

- [Plan](agent_visibility_plan.md)
- [Source](../src/epilepsy_agents/visibility.py)

| Metric | Value |
| --- | ---: |
| Exact | 0.20 |

### Uncertainty

Manual updates can drift.

### Next Action

Regenerate the page after changing source docs.
"""
        )

        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0].title, "Project Snapshot")
        self.assertIn("source-backed dashboard", claims[0].claim)
        self.assertIn("Regenerate", claims[0].next_action)

    def test_parse_markdown_table(self) -> None:
        rows = parse_table(
            """# Milestones

| Milestone | Status | Outcome |
| --- | --- | --- |
| Phase 1 | Complete | State docs exist. |
| Phase 3 | Planned | Build dashboard. |
"""
        )

        self.assertEqual(rows[1]["Milestone"], "Phase 3")
        self.assertEqual(rows[1]["Status"], "Planned")

    def test_parse_all_milestone_tables(self) -> None:
        rows = parse_tables(
            """# Milestones

## Delivered

| Milestone | Status | Outcome |
| --- | --- | --- |
| Phase 1 | Complete | State docs exist. |

## Phase A

| Milestone | Status | Intended Outcome |
| --- | --- | --- |
| M-A2 h003 | In progress | Local LLM smoke. |
"""
        )

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]["Milestone"], "M-A2 h003")
        self.assertEqual(rows[1]["Status"], "In progress")

    def test_parse_active_threads(self) -> None:
        threads = parse_active_threads(
            """# Active Threads

## Evidence Notebook Visibility

### Current Question

How should project state stay legible?

### Latest Evidence

- Dashboard source files exist.

### Blocker Or Risk

The source pages can drift.

### Next Action

Run the generator.
"""
        )

        self.assertEqual(threads[0].name, "Evidence Notebook Visibility")
        self.assertIn("legible", threads[0].question)

    def test_dashboard_preserves_parent_relative_links(self) -> None:
        claims = parse_current_state(
            """# Current State

## Project Snapshot

### Claim

Link claim.

### Evidence

- [Source](../src/epilepsy_agents/visibility.py)

### Uncertainty

None.

### Next Action

Review.
"""
        )

        self.assertIn("../src/epilepsy_agents/visibility.py", claims[0].evidence)

    def test_build_dashboard_from_minimal_docs(self) -> None:
        root = Path.cwd() / ".test_tmp_visibility"
        if root.exists():
            shutil.rmtree(root, ignore_errors=True)
        try:
            docs = root / "docs"
            run_logs = docs / "run_logs"
            run_logs.mkdir(parents=True)
            (docs / "current_state.md").write_text(
                """# Current State

Last updated: 2026-04-24.

## Project Snapshot

### Claim

Dashboard claim.

### Evidence

- [Plan](agent_visibility_plan.md)
- [Source](../src/epilepsy_agents/visibility.py)

| Metric | Value |
| --- | ---: |
| Exact | 0.20 |

### Uncertainty

None.

### Next Action

Review.
""",
                encoding="utf-8",
            )
            (docs / "milestones.md").write_text(
                """# Milestones

Last updated: 2026-04-24.

| Milestone | Status | Outcome | Evidence | Remaining Risk | Next Action |
| --- | --- | --- | --- | --- | --- |
| Phase 3 | Planned | Build dashboard. | [Plan](agent_visibility_plan.md) | None. | Generate HTML. |
""",
                encoding="utf-8",
            )
            (docs / "active_threads.md").write_text(
                """# Active Threads

Last updated: 2026-04-24.

## Evidence Notebook Visibility

### Current Question

Question.

### Latest Evidence

Evidence.

### Blocker Or Risk

Risk.

### Next Action

Action.
""",
                encoding="utf-8",
            )
            (docs / "decisions.md").write_text(
                """# Decisions

Last updated: 2026-04-24.

## D001: Choose Notebook

### Decision

Use the notebook.

### Rationale

It is reviewable.

### Consequence

Claims need evidence.

### Evidence

[Plan](agent_visibility_plan.md).
""",
                encoding="utf-8",
            )
            (docs / "artifact_registry.md").write_text(
                """# Artifact Registry

Last updated: 2026-04-24.

| Artifact | Purpose | Source Inputs | Status | Path | Intended Use |
| --- | --- | --- | --- | --- | --- |
| Dashboard | Visibility. | Docs. | Active | [evidence_notebook.html](evidence_notebook.html) | Review. |
""",
                encoding="utf-8",
            )
            (run_logs / "20260424T000000Z_visibility.md").write_text(
                """# Visibility Session

## Session Metadata

- Date: 2026-04-24
- Session objective: Build dashboard.

## Outcome

HTML exists.

## Evidence

- `docs/evidence_notebook.html`

## Uncertainty

Visual QA needed.

## Handoff

Open the page.

## Decision

documentation/visibility updated, no metric decision needed.
""",
                encoding="utf-8",
            )

            html = build_dashboard(root)
        finally:
            shutil.rmtree(root, ignore_errors=True)

        self.assertIn("Evidence Notebook", html)
        self.assertIn("Dashboard claim", html)
        self.assertIn("Visibility Session", html)
        self.assertIn("../src/epilepsy_agents/visibility.py", html)
        self.assertIn("<table>", html)
        self.assertIn("<th>Metric<\\/th>", html)


if __name__ == "__main__":
    unittest.main()
