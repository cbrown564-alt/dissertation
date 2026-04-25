"""Load project state and build the Evidence Notebook site payload."""
from __future__ import annotations

import json
import re
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
    review_risks = _overview_review_risks(claims, active_milestone)

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
        "reviewRisks": review_risks,
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
                **{
                    "title": session.title,
                    "date": session.date or session.path.stem[:8],
                    "objective": inline(session.objective),
                    "outcome": block(session.outcome),
                    "outcomePlain": _plain_text(session.outcome),
                    "evidence": block(session.evidence),
                    "uncertainty": block(session.uncertainty),
                    "handoff": block(session.handoff),
                    "decision": inline(session.decision),
                    "href": relative_doc_path(session.path),
                    "tags": _session_tags(session),
                },
                **_session_meta(session),
            }
            for session in sessions
        ],
        "workstreams": [
            {
                "name": thread.name,
                "question": inline(thread.question),
                "evidence": block(thread.evidence),
                "evidencePlain": _plain_text(thread.evidence),
                "risk": block(thread.risk),
                "riskPlain": _plain_text(thread.risk),
                "next": block(thread.next_action),
                "nextPlain": _plain_text(thread.next_action),
                "priority": _workstream_priority(thread),
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
                "markers": _decision_markers(decision),
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


def _plain_text(value: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", value or "")
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _overview_review_risks(
    claims: list[Claim], active_milestone: dict[str, str]
) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    evaluation_claim = _claim_by_title(claims, "Latest Evaluation Claim")
    governance_claim = _claim_by_title(claims, "Data And Governance Claim")

    if evaluation_claim and evaluation_claim.uncertainty:
        items.append(
            {
                "title": "Evaluation confidence limit",
                "detail": inline(evaluation_claim.uncertainty),
                "tone": "warning",
            }
        )

    risk_text = active_milestone.get("Remaining Risk", "")
    if risk_text:
        items.append(
            {
                "title": "Current delivery risk",
                "detail": inline(risk_text),
                "tone": "review-needed",
            }
        )

    if governance_claim and governance_claim.next_action:
        items.append(
            {
                "title": "Governance boundary",
                "detail": inline(governance_claim.next_action),
                "tone": "info",
            }
        )

    if not items:
        items.append(
            {
                "title": "Review stance",
                "detail": "No explicit overclaim guardrails are recorded yet.",
                "tone": "info",
            }
        )
    return items[:3]


def _session_meta(session) -> dict[str, object]:
    artifact_count = _count_session_list_items(session.evidence, "Generated artifacts")
    if not artifact_count:
        artifact_count = _count_artifact_mentions(session.evidence)
    return {
        "filesChangedCount": _count_session_list_items(session.evidence, "Files changed"),
        "checksRunCount": _count_session_list_items(session.evidence, "Tests or checks"),
        "artifactsUpdatedCount": artifact_count,
        "runEvidenceCount": _count_session_list_items(session.evidence, "Run records"),
        "hasDecision": bool((session.decision or "").strip()),
    }


def _session_tags(session) -> list[str]:
    tags: list[str] = []
    evidence = session.evidence.lower()

    if "files changed:" in evidence:
        match = re.search(r"files changed:\s*(.+)", session.evidence, flags=re.IGNORECASE)
        if match:
            count = match.group(1).count("[")
            if count:
                tags.append(f"{count} files changed")
            else:
                tags.append("files changed")

    if "tests or checks:" in evidence:
        tags.append("tests run")

    if any(
        phrase in evidence
        for phrase in ("generated artifact", "generated artifacts", ".png", ".svg", ".html", ".pptx")
    ):
        tags.append("artifacts updated")

    if "run records:" in evidence or "manifest:" in evidence:
        tags.append("run evidence")

    if "decision" in (session.decision or "").lower():
        tags.append(session.decision.strip())

    seen: set[str] = set()
    deduped: list[str] = []
    for tag in tags:
        if tag not in seen:
            seen.add(tag)
            deduped.append(tag)
    return deduped[:4]


def _count_session_list_items(markdown: str, label: str) -> int:
    lines = [line.strip() for line in (markdown or "").splitlines()]
    label_prefix = f"- {label.lower()}:"
    all_labels = {
        "- files changed:",
        "- tests or checks:",
        "- generated artifacts:",
        "- run records:",
        "- manifest:",
    }
    for index, line in enumerate(lines):
        if line.lower().startswith(label_prefix):
            trailing = line.split(":", 1)[1].strip()
            if trailing and trailing.lower() != "none":
                return 1
            count = 0
            for follower in lines[index + 1 :]:
                lowered = follower.lower()
                if lowered in all_labels:
                    break
                if follower.startswith("- "):
                    count += 1
            return count
    return 0


def _count_artifact_mentions(markdown: str) -> int:
    lines = [line.strip() for line in (markdown or "").splitlines()]
    count = 0
    for line in lines:
        if not line.startswith("- "):
            continue
        if re.search(r"\.(png|svg|html|pptx|pdf|docx|md)\b", line, flags=re.IGNORECASE):
            count += 1
    return count


def _workstream_priority(thread) -> str:
    combined = " ".join(
        [
            thread.name or "",
            thread.question or "",
            thread.risk or "",
            thread.next_action or "",
        ]
    ).lower()
    if any(term in combined for term in ("blocked", "blocker", "cannot", "depends on")):
        return "blocked"
    if any(term in combined for term in ("future", "later", "not active", "watch")):
        return "watch"
    if any(term in combined for term in ("keep", "monitor", "waiting")):
        return "waiting"
    return "active"


def _decision_markers(decision) -> list[str]:
    markers: list[str] = []
    text = " ".join(
        [
            decision.title or "",
            decision.decision or "",
            decision.rationale or "",
            decision.consequence or "",
            decision.evidence or "",
        ]
    ).lower()

    if any(term in text for term in ("future work", "future sessions", "next useful research action", "govern")):
        markers.append("governs future work")
    if any(term in text for term in ("real-data", "real data", "clinical", "governance", "privacy")):
        markers.append("real-data governance")
    if any(term in text for term in ("evaluation", "metric", "metrics", "harness", "pareto")):
        markers.append("evaluation protocol")
    if any(term in text for term in ("local runtime", "provider", "ollama", "server")):
        markers.append("runtime architecture")
    if any(term in text for term in ("first", "start", "freeze", "prefer", "keep")):
        markers.append("governs future work")

    seen: set[str] = set()
    deduped: list[str] = []
    for marker in markers:
        if marker not in seen:
            seen.add(marker)
            deduped.append(marker)
    return deduped[:3]
