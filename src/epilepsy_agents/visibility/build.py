"""Load project state and build the Evidence Notebook site payload."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .parsers import (
    PROJECT_DOCS,
    block,
    inline,
    parse_active_threads,
    parse_current_state,
    parse_decisions,
    parse_last_updated,
    parse_session_logs,
    parse_table,
    parse_tables,
    read_text,
    relative_doc_path,
)
from .state import Claim


def load_project_state(root: Path, session_limit: int = 6) -> dict[str, object]:
    docs = {name: read_text(root / path) for name, path in PROJECT_DOCS.items()}
    return {
        "claims": parse_current_state(docs["current_state"]),
        "milestones": parse_tables(docs["milestones"]),
        "workstreams": parse_active_threads(docs["active_threads"]),
        "decisions": parse_decisions(docs["decisions"]),
        "artifacts": parse_table(docs["artifact_registry"]),
        "sessions": parse_session_logs(root / "docs" / "run_logs", limit=session_limit),
        "last_updated": {name: parse_last_updated(text) for name, text in docs.items()},
    }


def build_data(root: Path, session_limit: int = 6) -> dict[str, object]:
    """Return the JSON-serializable payload that powers site/assets/app.js."""
    source = load_project_state(root, session_limit=session_limit)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return _shape_app_data(source, generated_at=generated_at)


def write_site(root: Path, site_dir: Path, session_limit: int = 6) -> Path:
    """Regenerate site/assets/data.js from the current project docs."""
    data = build_data(root, session_limit=session_limit)
    data_js = site_dir / "assets" / "data.js"
    data_js.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    data_js.write_text(
        f"window.__NOTEBOOK_DATA__ = {payload};\n", encoding="utf-8"
    )
    return data_js


def _shape_app_data(
    source: dict[str, object], generated_at: str
) -> dict[str, object]:
    claims = source["claims"]
    milestones = source["milestones"]
    workstreams = source["workstreams"]
    decisions = source["decisions"]
    artifacts = source["artifacts"]
    sessions = source["sessions"]
    last_updated = source["last_updated"]

    active_milestone = _first_incomplete_milestone(milestones) or {}
    latest_claim = claims[0] if claims else None
    evaluation_claim = _claim_by_title(claims, "Latest Evaluation Claim")

    return {
        "generatedAt": generated_at,
        "latestClaim": {
            "title": latest_claim.title if latest_claim else "Current state",
            "claim": inline(latest_claim.claim)
            if latest_claim
            else "No current-state claim found.",
        },
        "activeMilestone": {
            "name": inline(active_milestone.get("Milestone", "Visibility dashboard")),
            "next": inline(
                active_milestone.get(
                    "Next Action",
                    "Review the current state and decide the next action.",
                )
            ),
            "status": inline(active_milestone.get("Status", "Review")),
            "outcome": inline(
                active_milestone.get("Outcome", "")
                or active_milestone.get("Intended Outcome", "")
            ),
            "risk": inline(active_milestone.get("Remaining Risk", "")),
            "evidence": inline(
                active_milestone.get("Evidence", "")
                or active_milestone.get("Evidence Source", "")
            ),
        },
        "evaluationClaim": {
            "title": evaluation_claim.title
            if evaluation_claim
            else "Latest evaluation",
            "claim": inline(evaluation_claim.claim)
            if evaluation_claim
            else "No evaluation claim found.",
            "evidence": block(evaluation_claim.evidence) if evaluation_claim else "",
            "uncertainty": block(evaluation_claim.uncertainty)
            if evaluation_claim
            else "",
            "next": block(evaluation_claim.next_action) if evaluation_claim else "",
        },
        "stats": [
            {"label": "Claims", "value": len(claims)},
            {"label": "Milestones", "value": len(milestones)},
            {"label": "Sessions", "value": len(sessions)},
            {"label": "Threads", "value": len(workstreams)},
            {"label": "Artifacts", "value": len(artifacts)},
            {"label": "Decisions", "value": len(decisions)},
        ],
        "sources": [
            {"label": "current_state.md", "href": "current_state.md"},
            {"label": "milestones.md", "href": "milestones.md"},
            {"label": "active_threads.md", "href": "active_threads.md"},
            {"label": "artifact_registry.md", "href": "artifact_registry.md"},
            {"label": "decisions.md", "href": "decisions.md"},
        ],
        "sourceFreshness": [
            {
                "label": "current_state.md",
                "updated": last_updated.get("current_state") or "Not recorded",
            },
            {
                "label": "milestones.md",
                "updated": last_updated.get("milestones") or "Not recorded",
            },
            {
                "label": "active_threads.md",
                "updated": last_updated.get("active_threads") or "Not recorded",
            },
            {
                "label": "artifact_registry.md",
                "updated": last_updated.get("artifact_registry") or "Not recorded",
            },
            {
                "label": "decisions.md",
                "updated": last_updated.get("decisions") or "Not recorded",
            },
        ],
        "claims": [
            {
                "title": claim.title,
                "claim": inline(claim.claim),
                "evidence": block(claim.evidence),
                "uncertainty": block(claim.uncertainty),
                "next": block(claim.next_action),
            }
            for claim in claims
        ],
        "milestones": [
            {
                "title": inline(row.get("Milestone", "")),
                "status": row.get("Status", ""),
                "outcome": inline(
                    row.get("Outcome", "") or row.get("Intended Outcome", "")
                ),
                "evidence": inline(
                    row.get("Evidence", "") or row.get("Evidence Source", "")
                ),
                "risk": inline(row.get("Remaining Risk", "")),
                "next": inline(row.get("Next Action", "")),
            }
            for row in milestones
        ],
        "sessions": [
            {
                "title": session.title,
                "date": session.date or session.path.stem[:8],
                "objective": inline(session.objective),
                "outcome": block(session.outcome),
                "evidence": block(session.evidence),
                "uncertainty": block(session.uncertainty),
                "handoff": block(session.handoff),
                "decision": inline(session.decision),
                "href": relative_doc_path(session.path),
            }
            for session in sessions
        ],
        "workstreams": [
            {
                "name": thread.name,
                "question": inline(thread.question),
                "evidence": block(thread.evidence),
                "risk": block(thread.risk),
                "next": block(thread.next_action),
            }
            for thread in workstreams
        ],
        "artifacts": [
            {
                "name": inline(row.get("Artifact", "")),
                "purpose": inline(row.get("Purpose", "")),
                "status": row.get("Status", ""),
                "path": inline(row.get("Path", "")),
                "use": inline(row.get("Intended Use", "")),
            }
            for row in artifacts
        ],
        "decisions": [
            {
                "id": decision.identifier,
                "title": decision.title,
                "decision": inline(decision.decision),
                "rationale": block(decision.rationale),
                "consequence": block(decision.consequence),
                "evidence": inline(decision.evidence),
            }
            for decision in decisions
        ],
    }


def _claim_by_title(claims: list[Claim], title: str) -> Claim | None:
    for claim in claims:
        if claim.title == title:
            return claim
    return None


def _first_incomplete_milestone(
    milestones: list[dict[str, str]],
) -> dict[str, str] | None:
    for milestone in milestones:
        status = milestone.get("Status", "").strip().lower()
        if status and status != "complete":
            return milestone
    return milestones[-1] if milestones else None
