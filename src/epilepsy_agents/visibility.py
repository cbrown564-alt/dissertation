from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DOCS = {
    "current_state": Path("docs/current_state.md"),
    "milestones": Path("docs/milestones.md"),
    "active_threads": Path("docs/active_threads.md"),
    "decisions": Path("docs/decisions.md"),
    "artifact_registry": Path("docs/artifact_registry.md"),
}


@dataclass(frozen=True)
class Claim:
    title: str
    claim: str
    evidence: str
    uncertainty: str
    next_action: str


@dataclass(frozen=True)
class Workstream:
    name: str
    question: str
    evidence: str
    risk: str
    next_action: str


@dataclass(frozen=True)
class Decision:
    identifier: str
    title: str
    decision: str
    rationale: str
    consequence: str
    evidence: str


@dataclass(frozen=True)
class SessionLog:
    title: str
    path: Path
    date: str
    objective: str
    outcome: str
    evidence: str
    uncertainty: str
    handoff: str
    decision: str


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the local Evidence Notebook dashboard.")
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument(
        "--out",
        default="docs/evidence_notebook.html",
        help="Output HTML path, relative to the repository root unless absolute.",
    )
    parser.add_argument("--session-limit", type=int, default=6)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).resolve()
    out = Path(args.out)
    if not out.is_absolute():
        out = root / out
    html_text = build_dashboard(root, session_limit=args.session_limit)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


def build_dashboard(root: Path, session_limit: int = 6) -> str:
    source = load_project_state(root, session_limit=session_limit)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return render_dashboard(source, generated_at=generated_at)


def load_project_state(root: Path, session_limit: int = 6) -> dict[str, object]:
    docs = {name: _read(root / path) for name, path in PROJECT_DOCS.items()}
    return {
        "claims": parse_current_state(docs["current_state"]),
        "milestones": parse_tables(docs["milestones"]),
        "workstreams": parse_active_threads(docs["active_threads"]),
        "decisions": parse_decisions(docs["decisions"]),
        "artifacts": parse_table(docs["artifact_registry"]),
        "sessions": parse_session_logs(root / "docs" / "run_logs", limit=session_limit),
        "last_updated": {
            name: parse_last_updated(text) for name, text in docs.items()
        },
    }


def parse_current_state(markdown: str) -> list[Claim]:
    claims: list[Claim] = []
    for title, body in _heading_blocks(markdown, level=2):
        fields = dict(_heading_blocks(body, level=3))
        if "Claim" not in fields:
            continue
        claims.append(
            Claim(
                title=title,
                claim=_clean(fields.get("Claim", "")),
                evidence=_clean(fields.get("Evidence", "")),
                uncertainty=_clean(fields.get("Uncertainty", "")),
                next_action=_clean(fields.get("Next Action", "")),
            )
        )
    return claims


def parse_active_threads(markdown: str) -> list[Workstream]:
    threads: list[Workstream] = []
    for name, body in _heading_blocks(markdown, level=2):
        fields = dict(_heading_blocks(body, level=3))
        if "Current Question" not in fields:
            continue
        threads.append(
            Workstream(
                name=name,
                question=_clean(fields.get("Current Question", "")),
                evidence=_clean(fields.get("Latest Evidence", "")),
                risk=_clean(fields.get("Blocker Or Risk", "")),
                next_action=_clean(fields.get("Next Action", "")),
            )
        )
    return threads


def parse_decisions(markdown: str) -> list[Decision]:
    decisions: list[Decision] = []
    for heading, body in _heading_blocks(markdown, level=2):
        fields = dict(_heading_blocks(body, level=3))
        match = re.match(r"(?P<id>D\d+):\s*(?P<title>.+)", heading)
        identifier = match.group("id") if match else heading
        title = match.group("title") if match else heading
        decisions.append(
            Decision(
                identifier=identifier,
                title=title,
                decision=_clean(fields.get("Decision", "")),
                rationale=_clean(fields.get("Rationale", "")),
                consequence=_clean(fields.get("Consequence", "")),
                evidence=_clean(fields.get("Evidence", "")),
            )
        )
    return decisions


def parse_session_logs(directory: Path, limit: int = 6) -> list[SessionLog]:
    if not directory.exists():
        return []
    logs = [
        path
        for path in directory.glob("*.md")
        if path.name not in {"README.md", "session_log_template.md"}
    ]
    sessions: list[SessionLog] = []
    for path in sorted(logs, reverse=True)[:limit]:
        markdown = _read(path)
        title = _first_heading(markdown) or path.stem
        fields = dict(_heading_blocks(markdown, level=2))
        metadata = _parse_metadata(fields.get("Session Metadata", ""))
        sessions.append(
            SessionLog(
                title=title,
                path=path,
                date=metadata.get("Date", ""),
                objective=metadata.get("Session objective", ""),
                outcome=_clean(fields.get("Outcome", "")),
                evidence=_clean(fields.get("Evidence", "")),
                uncertainty=_clean(fields.get("Uncertainty", "")),
                handoff=_clean(fields.get("Handoff", "")),
                decision=_clean(fields.get("Decision", "")),
            )
        )
    return sessions


def parse_table(markdown: str) -> list[dict[str, str]]:
    return _first_table(markdown)


def parse_tables(markdown: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in markdown.splitlines()]
    rows: list[dict[str, str]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.startswith("|") or index + 1 >= len(lines) or not _is_table_separator(lines[index + 1]):
            index += 1
            continue
        headers = _split_table_row(line)
        index += 2
        while index < len(lines) and lines[index].startswith("|"):
            cells = _split_table_row(lines[index])
            rows.append({header: _clean(cells[pos]) if pos < len(cells) else "" for pos, header in enumerate(headers)})
            index += 1
        continue
    return rows


def _first_table(markdown: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in markdown.splitlines()]
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        if index + 1 >= len(lines) or not _is_table_separator(lines[index + 1]):
            continue
        headers = _split_table_row(line)
        rows: list[dict[str, str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.startswith("|"):
                break
            cells = _split_table_row(row_line)
            rows.append({header: _clean(cells[pos]) if pos < len(cells) else "" for pos, header in enumerate(headers)})
        return rows
    return []


def parse_last_updated(markdown: str) -> str:
    match = re.search(r"^Last updated:\s*(.+?)\.?\s*$", markdown, flags=re.MULTILINE)
    return match.group(1) if match else ""


def render_dashboard(source: dict[str, object], generated_at: str) -> str:
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
    open_decisions = list(decisions)
    app_data = {
        "generatedAt": generated_at,
        "latestClaim": {
            "title": latest_claim.title if latest_claim else "Current state",
            "claim": _inline(latest_claim.claim) if latest_claim else "No current-state claim found.",
        },
        "activeMilestone": {
            "name": _inline(active_milestone.get("Milestone", "Visibility dashboard")),
            "next": _inline(active_milestone.get("Next Action", "Review the current state and decide the next action.")),
            "status": _inline(active_milestone.get("Status", "Review")),
            "outcome": _inline(
                active_milestone.get("Outcome", "")
                or active_milestone.get("Intended Outcome", "")
            ),
            "risk": _inline(active_milestone.get("Remaining Risk", "")),
            "evidence": _inline(
                active_milestone.get("Evidence", "")
                or active_milestone.get("Evidence Source", "")
            ),
        },
        "evaluationClaim": {
            "title": evaluation_claim.title if evaluation_claim else "Latest evaluation",
            "claim": _inline(evaluation_claim.claim) if evaluation_claim else "No evaluation claim found.",
            "evidence": _block(evaluation_claim.evidence) if evaluation_claim else "",
            "uncertainty": _block(evaluation_claim.uncertainty) if evaluation_claim else "",
            "next": _block(evaluation_claim.next_action) if evaluation_claim else "",
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
            {"label": "current_state.md", "updated": last_updated.get("current_state") or "Not recorded"},
            {"label": "milestones.md", "updated": last_updated.get("milestones") or "Not recorded"},
            {"label": "active_threads.md", "updated": last_updated.get("active_threads") or "Not recorded"},
            {"label": "artifact_registry.md", "updated": last_updated.get("artifact_registry") or "Not recorded"},
            {"label": "decisions.md", "updated": last_updated.get("decisions") or "Not recorded"},
        ],
        "claims": [
            {
                "title": claim.title,
                "claim": _inline(claim.claim),
                "evidence": _block(claim.evidence),
                "uncertainty": _block(claim.uncertainty),
                "next": _block(claim.next_action),
            }
            for claim in claims
        ],
        "milestones": [
            {
                "title": _inline(row.get("Milestone", "")),
                "status": row.get("Status", ""),
                "outcome": _inline(row.get("Outcome", "") or row.get("Intended Outcome", "")),
                "evidence": _inline(row.get("Evidence", "") or row.get("Evidence Source", "")),
                "risk": _inline(row.get("Remaining Risk", "")),
                "next": _inline(row.get("Next Action", "")),
            }
            for row in milestones
        ],
        "sessions": [
            {
                "title": session.title,
                "date": session.date or session.path.stem[:8],
                "objective": _inline(session.objective),
                "outcome": _block(session.outcome),
                "evidence": _block(session.evidence),
                "uncertainty": _block(session.uncertainty),
                "handoff": _block(session.handoff),
                "decision": _inline(session.decision),
                "href": _relative_doc_path(session.path),
            }
            for session in sessions
        ],
        "workstreams": [
            {
                "name": thread.name,
                "question": _inline(thread.question),
                "evidence": _block(thread.evidence),
                "risk": _block(thread.risk),
                "next": _block(thread.next_action),
            }
            for thread in workstreams
        ],
        "artifacts": [
            {
                "name": _inline(row.get("Artifact", "")),
                "purpose": _inline(row.get("Purpose", "")),
                "status": row.get("Status", ""),
                "path": _inline(row.get("Path", "")),
                "use": _inline(row.get("Intended Use", "")),
            }
            for row in artifacts
        ],
        "decisions": [
            {
                "id": decision.identifier,
                "title": decision.title,
                "decision": _inline(decision.decision),
                "rationale": _block(decision.rationale),
                "consequence": _block(decision.consequence),
                "evidence": _inline(decision.evidence),
            }
            for decision in open_decisions
        ],
    }
    app_json = json.dumps(app_data, ensure_ascii=False).replace("</", "<\\/")

    html_body = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Evidence Notebook</title>
    <link rel="icon" href="data:," />
    <style>{_css()}</style>
  </head>
  <body class="app-body">
    <div id="app" class="app-shell" data-view="overview"></div>
    <script id="notebook-data" type="application/json">{app_json}</script>
    <script>
{_js()}
    </script>
  </body>
</html>
"""
    return html_body


def _render_claims(claims: list[Claim]) -> str:
    return "\n".join(
        f"""
        <article class="claim">
          <h3>{html.escape(claim.title)}</h3>
          <p class="statement">{_inline(claim.claim)}</p>
          <div class="claim-meta">
            <div><b>Evidence</b>{_block(claim.evidence)}</div>
            <div><b>Uncertainty</b>{_block(claim.uncertainty)}</div>
            <div><b>Next action</b>{_block(claim.next_action)}</div>
          </div>
        </article>
        """
        for claim in claims
    )


def _render_milestones(milestones: list[dict[str, str]]) -> str:
    return "\n".join(
        f"""
        <li class="milestone {html.escape(row.get("Status", "").lower())}">
          <span>{html.escape(row.get("Status", ""))}</span>
          <h3>{_inline(row.get("Milestone", ""))}</h3>
          <p>{_inline(row.get("Outcome", ""))}</p>
          <small>{_inline(row.get("Evidence", ""))}</small>
        </li>
        """
        for row in milestones
    )


def _render_sessions(sessions: list[SessionLog]) -> str:
    return "\n".join(
        f"""
        <details class="session" open>
          <summary>
            <span>{html.escape(session.date or session.path.stem[:8])}</span>
            <strong>{html.escape(session.title)}</strong>
          </summary>
          <p class="objective">{_inline(session.objective)}</p>
          <div class="session-fields">
            <div><b>Outcome</b>{_block(session.outcome)}</div>
            <div><b>Evidence</b>{_block(session.evidence)}</div>
            <div><b>Uncertainty</b>{_block(session.uncertainty)}</div>
            <div><b>Handoff</b>{_block(session.handoff)}</div>
          </div>
          <footer>
            <span>{_inline(session.decision)}</span>
            <a href="{_relative_doc_path(session.path)}">source log</a>
          </footer>
        </details>
        """
        for session in sessions
    )


def _render_workstreams(workstreams: list[Workstream]) -> str:
    return "\n".join(
        f"""
        <article class="thread">
          <h3>{html.escape(thread.name)}</h3>
          <p>{_inline(thread.question)}</p>
          <dl>
            <dt>Latest evidence</dt><dd>{_block(thread.evidence)}</dd>
            <dt>Risk</dt><dd>{_block(thread.risk)}</dd>
            <dt>Next action</dt><dd>{_block(thread.next_action)}</dd>
          </dl>
        </article>
        """
        for thread in workstreams
    )


def _render_artifacts(artifacts: list[dict[str, str]]) -> str:
    rows = []
    for row in artifacts:
        rows.append(
            f"""
            <article class="artifact">
              <div>
                <span>{html.escape(row.get("Status", ""))}</span>
                <h3>{_inline(row.get("Artifact", ""))}</h3>
              </div>
              <p>{_inline(row.get("Purpose", ""))}</p>
              <small>{_inline(row.get("Path", ""))}</small>
            </article>
            """
        )
    return "\n".join(rows)


def _render_decisions(decisions: list[Decision]) -> str:
    return "\n".join(
        f"""
        <article class="decision">
          <span>{html.escape(decision.identifier)}</span>
          <h3>{html.escape(decision.title)}</h3>
          <p>{_inline(decision.decision)}</p>
          <div>
            <b>Consequence</b>
            {_block(decision.consequence)}
          </div>
          <small>{_inline(decision.evidence)}</small>
        </article>
        """
        for decision in decisions
    )


def _heading_blocks(markdown: str, level: int) -> list[tuple[str, str]]:
    marker = "#" * level
    next_marker = "#" * level
    pattern = re.compile(
        rf"^{re.escape(marker)}\s+(.+?)\s*$\n(.*?)(?=^{re.escape(next_marker)}\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    return [(match.group(1).strip(), match.group(2).strip()) for match in pattern.finditer(markdown)]


def _first_heading(markdown: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def _parse_metadata(markdown: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in markdown.splitlines():
        match = re.match(r"-\s*([^:]+):\s*(.*)", line.strip())
        if match:
            metadata[match.group(1).strip()] = match.group(2).strip()
    return metadata


def _split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _is_table_separator(line: str) -> bool:
    return all(set(cell.strip()) <= {"-", ":"} for cell in _split_table_row(line))


def _first_matching(rows: list[dict[str, str]], key: str, values: set[str]) -> dict[str, str] | None:
    for row in rows:
        if row.get(key) in values:
            return row
    return None


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _clean(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def _inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_match, escaped)


def _block(text: str) -> str:
    if not text:
        return "<p>Not recorded.</p>"
    lines = text.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{_inline(' '.join(paragraph))}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            output.append(f"<ul>{''.join(list_items)}</ul>")
            list_items.clear()

    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            flush_paragraph()
            flush_list()
            index += 1
            continue
        if _starts_table(lines, index):
            flush_paragraph()
            flush_list()
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            output.append(_render_markdown_table(table_lines))
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            list_items.append(f"<li>{_inline(stripped[2:])}</li>")
            index += 1
            continue
        flush_list()
        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    flush_list()
    return "".join(output)


def _starts_table(lines: list[str], index: int) -> bool:
    return (
        lines[index].strip().startswith("|")
        and index + 1 < len(lines)
        and _is_table_separator(lines[index + 1].strip())
    )


def _render_markdown_table(lines: list[str]) -> str:
    headers = _split_table_row(lines[0])
    body_rows = [_split_table_row(line) for line in lines[2:]]
    head = "".join(f"<th>{_inline(header)}</th>" for header in headers)
    rows = []
    for row in body_rows:
        cells = "".join(f"<td>{_inline(cell)}</td>" for cell in row)
        rows.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def _link_match(match: re.Match[str]) -> str:
    label = match.group(1)
    target = match.group(2)
    return f'<a href="{html.escape(target, quote=True)}">{label}</a>'


def _relative_doc_path(path: Path) -> str:
    parts = path.parts
    if "docs" in parts:
        return "/".join(parts[parts.index("docs") + 1 :])
    return path.name


def _claim_by_title(claims: list[Claim], title: str) -> Claim | None:
    for claim in claims:
        if claim.title == title:
            return claim
    return None


def _first_incomplete_milestone(milestones: list[dict[str, str]]) -> dict[str, str] | None:
    for milestone in milestones:
        status = milestone.get("Status", "").strip().lower()
        if status and status != "complete":
            return milestone
    return milestones[-1] if milestones else None


def _js() -> str:
    return r"""
const data = JSON.parse(document.getElementById("notebook-data").textContent);
const app = document.getElementById("app");

const views = [
  ["overview", "Overview"],
  ["claims", "Claims"],
  ["timeline", "Timeline"],
  ["sessions", "Sessions"],
  ["workstreams", "Workstreams"],
  ["artifacts", "Artifacts"],
  ["decisions", "Decisions"],
];

const statTargets = {
  claims: "claims",
  milestones: "timeline",
  sessions: "sessions",
  threads: "workstreams",
  artifacts: "artifacts",
  decisions: "decisions",
};

let state = {
  view: location.hash.replace("#", "") || "overview",
  query: "",
  selectedClaim: 0,
};

function textFromHtml(value) {
  const div = document.createElement("div");
  div.innerHTML = value || "";
  return div.textContent || "";
}

function includesQuery(record) {
  if (!state.query) return true;
  const haystack = JSON.stringify(record).toLowerCase();
  return haystack.includes(state.query.toLowerCase());
}

function filtered(records) {
  return records.filter(includesQuery);
}

function setView(view) {
  state.view = view;
  location.hash = view;
  render();
}

function render() {
  const activeView = views.some(([id]) => id === state.view) ? state.view : "overview";
  state.view = activeView;
  app.dataset.view = activeView;
  app.innerHTML = `
    <aside class="app-rail">
      <a class="app-mark" href="#overview" data-view-link="overview">EN</a>
      <nav>${views.map(([id, label]) => `<button type="button" class="${id === activeView ? "is-active" : ""}" data-view-link="${id}">${label}</button>`).join("")}</nav>
      <p>Local archive<br>${data.generatedAt}</p>
    </aside>
    <main class="app-main">
      <header class="app-header">
        <div>
          <p class="app-kicker">Clinical evidence register</p>
          <h1>Evidence Notebook</h1>
          <p>${data.latestClaim.claim}</p>
          <div class="header-meta">
            <span>Generated ${data.generatedAt}</span>
            <span>${data.latestClaim.title}</span>
          </div>
        </div>
        <label class="app-search">
          <span>Search</span>
          <input type="search" value="${escapeAttr(state.query)}" placeholder="claims, sessions, artifacts..." />
        </label>
      </header>
      <section class="source-ledger">${data.sources.map((source, index) => sourceCard(source, data.sourceFreshness[index])).join("")}</section>
      <section class="app-stats">${data.stats.map((item) => statButton(item)).join("")}</section>
      <section class="app-view">${renderView(activeView)}</section>
    </main>
  `;

  app.querySelectorAll("[data-view-link]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      setView(button.dataset.viewLink);
    });
  });

  const search = app.querySelector(".app-search input");
  search.addEventListener("input", (event) => {
    state.query = event.target.value;
    render();
    const next = app.querySelector(".app-search input");
    next.focus();
    next.setSelectionRange(next.value.length, next.value.length);
  });

  app.querySelectorAll("[data-select-claim]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedClaim = Number(button.dataset.selectClaim);
      render();
    });
  });
}

function renderView(view) {
  if (view === "overview") return renderOverview();
  if (view === "claims") return renderClaims();
  if (view === "timeline") return renderTimeline();
  if (view === "sessions") return renderSessions();
  if (view === "workstreams") return renderWorkstreams();
  if (view === "artifacts") return renderArtifacts();
  if (view === "decisions") return renderDecisions();
  return renderOverview();
}

function renderOverview() {
  const claim = data.claims[state.selectedClaim] || data.claims[0];
  const latestDecision = data.decisions[0];
  return `
    <div class="overview-grid">
      ${claimDossier(claim, "Current claim")}
      <aside class="archive-panel action-panel">
        <p class="app-kicker">Active research path</p>
        <span class="status-chip ${statusClass(data.activeMilestone.status)}">${data.activeMilestone.status}</span>
        <h3>${data.activeMilestone.name}</h3>
        <p>${data.activeMilestone.next}</p>
        <button type="button" data-view-link="timeline">Open timeline</button>
      </aside>
      <section class="archive-panel evaluation-panel">
        <div class="panel-heading row">
          <div><p class="app-kicker">Evaluation signal</p><h2>${data.evaluationClaim.title}</h2></div>
          <button type="button" data-view-link="claims">Open claim</button>
        </div>
        <p class="body-lead">${data.evaluationClaim.claim}</p>
        <div class="compact-fields">
          <section><b>Evidence</b>${data.evaluationClaim.evidence}</section>
          <section><b>Uncertainty</b>${data.evaluationClaim.uncertainty}</section>
          <section><b>Next experiment</b>${data.evaluationClaim.next}</section>
        </div>
      </section>
      <section class="archive-panel index-panel session-panel">
        <div class="panel-heading row">
          <div><p class="app-kicker">Run ledger</p><h2>Recent Sessions</h2></div>
          <button type="button" data-view-link="sessions">View all</button>
        </div>
        ${rowsOrEmpty(data.sessions.slice(0, 3).map(sessionRow), "No session logs recorded.")}
      </section>
      <section class="archive-panel index-panel artifact-panel">
        <div class="panel-heading row">
          <div><p class="app-kicker">Output register</p><h2>Artifact Shelf</h2></div>
          <button type="button" data-view-link="artifacts">View all</button>
        </div>
        ${rowsOrEmpty(data.artifacts.slice(0, 5).map(artifactRow), "No artifacts recorded.")}
      </section>
      <section class="archive-panel decision-brief">
        <div class="panel-heading">
          <p class="app-kicker">Decision anchor</p>
          <h2>${latestDecision ? latestDecision.id : "None"}</h2>
        </div>
        ${latestDecision ? `<h3>${latestDecision.title}</h3><p>${latestDecision.decision}</p><small>${latestDecision.evidence}</small>` : `<p>No decisions recorded.</p>`}
      </section>
    </div>
  `;
}

function renderClaims() {
  const claims = filtered(data.claims);
  const selected = claims[state.selectedClaim] || claims[0] || data.claims[0];
  if (!selected) return emptyState("No matching claims.");
  return `
    <div class="claim-app">
      <aside class="record-list">
        ${claims.map((claim, index) => `<button type="button" class="${claim === selected ? "is-active" : ""}" data-select-claim="${index}"><span>${pad(index + 1)}</span>${claim.title}</button>`).join("")}
      </aside>
      ${claimDossier(selected, "Claim record")}
    </div>
  `;
}

function renderTimeline() {
  const milestones = filtered(data.milestones);
  return `<section class="archive-panel timeline-panel"><div class="panel-heading"><p class="app-kicker">Milestone spine</p><h2>Timeline</h2></div>${renderTimelineSummary(milestones)}<ol class="app-timeline">${rowsOrEmpty(milestones.map((item) => `
    <li class="${statusClass(item.status)}">
      <span>${item.status}</span>
      <div><h3>${item.title}</h3><p>${item.outcome}</p><small>${item.evidence}</small><em>${item.next}</em></div>
    </li>`), "No matching milestones.")}</ol></section>`;
}

function renderTimelineSummary(milestones) {
  if (!milestones.length) return emptyState("No matching milestones.");
  const keyEvents = timelineKeyEvents(milestones);
  const completed = milestones.filter((item) => normalizedStatus(item.status) === "complete").length;
  const next = milestones.find((item) => normalizedStatus(item.status) !== "complete") || milestones[milestones.length - 1];
  const progress = Math.round((completed / milestones.length) * 100);
  return `<div class="timeline-summary">
    <section class="timeline-progress">
      <div>
        <p class="app-kicker">Progress map</p>
        <strong>${completed}/${milestones.length}</strong>
        <span>milestones complete</span>
      </div>
      <div class="progress-rail" aria-hidden="true"><i style="width: ${progress}%"></i></div>
      <p><b>Next visible move</b>${next ? next.title : "No next milestone recorded"}</p>
    </section>
    <section class="timeline-keyline">
      <div class="keyline-heading">
        <p class="app-kicker">Key sequence</p>
        <h3>Major events</h3>
      </div>
      <ol>${keyEvents.map((event, index) => `<li class="${statusClass(event.status)}">
        <span>${pad(index + 1)}</span>
        <strong>${event.title}</strong>
        <small>${event.status}</small>
      </li>`).join("")}</ol>
    </section>
  </div>`;
}

function timelineKeyEvents(milestones) {
  const patterns = [/project frame/i, /synthetic subset/i, /evaluation harness/i, /smoke/i, /local model/i, /local dashboard/i, /visual artifacts/i];
  const picked = [];
  patterns.forEach((pattern) => {
    const item = milestones.find((milestone) => pattern.test(milestone.title));
    if (item && !picked.includes(item)) picked.push(item);
  });
  if (picked.length < 4) {
    milestones.forEach((item) => {
      if (picked.length < 4 && !picked.includes(item)) picked.push(item);
    });
  }
  return picked.slice(0, 7);
}

function normalizedStatus(status) {
  return String(status || "").toLowerCase();
}

function renderSessions() {
  const sessions = filtered(data.sessions);
  return `<section class="archive-panel"><div class="panel-heading"><p class="app-kicker">Run ledger</p><h2>Recent Session Feed</h2></div>${rowsOrEmpty(sessions.map((session) => `
    <details class="session-record">
      <summary><span>${session.date}</span><strong>${session.title}</strong><a href="${session.href}">source log</a></summary>
      <p>${session.objective}</p>
      <div class="quad">
        <section><b>Outcome</b>${session.outcome}</section>
        <section><b>Evidence</b>${session.evidence}</section>
        <section><b>Uncertainty</b>${session.uncertainty}</section>
        <section><b>Handoff</b>${session.handoff}</section>
      </div>
      <footer>${session.decision}</footer>
    </details>`), "No matching session logs.")}</section>`;
}

function renderWorkstreams() {
  const workstreams = filtered(data.workstreams);
  return `<div class="card-grid">${rowsOrEmpty(workstreams.map((thread) => `
    <article class="archive-panel">
      <div class="panel-heading"><p class="app-kicker">Thread</p><h2>${thread.name}</h2></div>
      <p class="body-lead">${thread.question}</p>
      <div class="stacked-fields">
        <section><b>Latest evidence</b>${thread.evidence}</section>
        <section><b>Risk</b>${thread.risk}</section>
        <section><b>Next action</b>${thread.next}</section>
      </div>
    </article>`), "No matching workstreams.")}</div>`;
}

function renderArtifacts() {
  const artifacts = filtered(data.artifacts);
  const groups = groupedArtifacts(artifacts);
  return `<section class="archive-panel"><div class="panel-heading"><p class="app-kicker">Artifact shelf</p><h2>Outputs And Planned Visuals</h2></div><div class="artifact-groups">${rowsOrEmpty(groups.map(([label, rows]) => `
    <section class="artifact-group">
      <h3>${label}</h3>
      <div class="shelf">${rowsOrEmpty(rows.map(artifactRow), "No artifacts in this group.")}</div>
    </section>`), "No matching artifacts.")}</div></section>`;
}

function renderDecisions() {
  const decisions = filtered(data.decisions);
  return `<section class="archive-panel"><div class="panel-heading"><p class="app-kicker">Decision register</p><h2>Decisions</h2></div>${rowsOrEmpty(decisions.map((decision) => `
    <article class="decision-record">
      <span>${decision.id}</span>
      <div><h3>${decision.title}</h3><p>${decision.decision}</p></div>
      <section><b>Consequence</b>${decision.consequence}<small>${decision.evidence}</small></section>
    </article>`), "No matching decisions.")}</section>`;
}

function claimDossier(claim, label) {
  return `<section class="archive-panel primary-panel claim-dossier">
    <div class="panel-heading">
      <p class="app-kicker">${label}</p>
      <h2>${claim.title}</h2>
    </div>
    <p class="claim-line">${claim.claim}</p>
    <div class="triad">
      <section><b>Evidence</b>${claim.evidence}</section>
      <section><b>Uncertainty</b>${claim.uncertainty}</section>
      <section><b>Next action</b>${claim.next}</section>
    </div>
  </section>`;
}

function sourceCard(source, freshness) {
  return `<a class="source-card" href="${source.href}">
    <span>Source</span>
    <strong>${source.label}</strong>
    <small>Updated ${freshness ? freshness.updated : "Not recorded"}</small>
  </a>`;
}

function statButton(item) {
  const key = item.label.toLowerCase();
  const target = statTargets[key] || "overview";
  return `<button type="button" data-view-link="${target}"><strong>${item.value}</strong><span>${item.label}</span></button>`;
}

function sessionRow(session) {
  return `<article class="index-row"><span>${session.date}</span><strong>${session.title}</strong><small>${session.objective || session.decision}</small></article>`;
}

function artifactRow(item) {
  return `<article class="index-row artifact-row ${statusClass(item.status)}"><span>${item.status}</span><strong>${item.name}</strong><small>${item.path}</small></article>`;
}

function rowsOrEmpty(rows, message) {
  return rows.length ? rows.join("") : emptyState(message);
}

function groupedArtifacts(artifacts) {
  const buckets = [
    ["Active evidence", []],
    ["Source documents", []],
    ["Session logs", []],
    ["Planned visuals", []],
    ["Reference", []],
  ];
  const byLabel = Object.fromEntries(buckets);
  artifacts.forEach((item) => {
    const name = `${item.name} ${item.path}`.toLowerCase();
    const status = String(item.status || "").toLowerCase();
    if (status.includes("planned") || name.includes("to be generated")) byLabel["Planned visuals"].push(item);
    else if (name.includes("session log") || name.includes("run_logs/")) byLabel["Session logs"].push(item);
    else if (status.includes("active") || name.includes("manifest") || name.includes("run record") || name.includes("dashboard")) byLabel["Active evidence"].push(item);
    else if (status.includes("reference")) byLabel["Reference"].push(item);
    else byLabel["Source documents"].push(item);
  });
  return buckets.filter(([, rows]) => rows.length);
}

function emptyState(message) {
  return `<p class="empty-state">${message}</p>`;
}

function statusClass(status) {
  return `is-${String(status || "unknown").toLowerCase().replace(/[^a-z0-9]+/g, "-")}`;
}

function pad(value) {
  return String(value).padStart(2, "0");
}

function escapeAttr(value) {
  return String(value || "").replaceAll("&", "&amp;").replaceAll('"', "&quot;").replaceAll("<", "&lt;");
}

window.addEventListener("hashchange", () => {
  state.view = location.hash.replace("#", "") || "overview";
  render();
});

render();
"""


def _css() -> str:
    return """
:root {
  color-scheme: light;
  --ink: #171614;
  --muted: #66645c;
  --paper: #fffdf6;
  --wash: #f3efe3;
  --line: rgba(23, 22, 20, 0.16);
  --accent: #0f8f8c;
  --accent-soft: rgba(15, 143, 140, 0.11);
  --amber: #c98713;
  --green: #2d7653;
  --blue: #315d9b;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  overflow-x: hidden;
  background: #f5f1e8;
  color: var(--ink);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

a {
  color: inherit;
  text-decoration-color: rgba(15, 143, 140, 0.55);
  text-underline-offset: 3px;
}

code {
  padding: 1px 4px;
  background: rgba(23, 22, 20, 0.08);
  border-radius: 4px;
  font-size: 0.92em;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  gap: 18px;
  align-items: center;
  justify-content: space-between;
  min-height: 64px;
  padding: 10px clamp(18px, 4vw, 44px);
  border-bottom: 1px solid var(--line);
  background: rgba(255, 253, 246, 0.88);
  backdrop-filter: blur(16px);
}

.brand {
  display: grid;
  gap: 2px;
  text-decoration: none;
}

.brand span {
  font-weight: 800;
}

.brand small,
.section-heading span,
.artifact small,
.decision small {
  color: var(--muted);
  font-size: 12px;
}

nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
}

nav a {
  min-height: 34px;
  padding: 8px 10px;
  border: 1px solid transparent;
  border-radius: 999px;
  font-size: 13px;
  text-decoration: none;
  transition: border-color 160ms ease, background 160ms ease;
}

nav a:hover {
  border-color: var(--line);
  background: rgba(255, 255, 255, 0.62);
}

.hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, 360px);
  gap: 32px;
  align-items: start;
  width: min(1180px, calc(100vw - 36px));
  margin: 0 auto;
  padding: 28px 0;
  border-bottom: 1px solid var(--line);
}

.hero-copy {
  max-width: 760px;
}

.eyebrow {
  margin: 0 0 12px;
  color: var(--accent);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h1,
h2,
h3,
p {
  margin: 0;
}

h1 {
  max-width: 760px;
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(36px, 4.2vw, 56px);
  font-weight: 700;
  line-height: 1.02;
}

h2 {
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(30px, 3vw, 44px);
  line-height: 1.05;
}

h3 {
  font-size: 18px;
  line-height: 1.24;
}

.lede {
  max-width: 700px;
  margin-top: 14px;
  color: #37352f;
  font-size: clamp(17px, 1.7vw, 21px);
  line-height: 1.4;
}

.source-line {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 26px;
}

.source-line a,
.hero-note span,
.milestone span,
.artifact span,
.decision span,
.session summary span {
  width: fit-content;
  padding: 5px 8px;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.55);
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
  text-decoration: none;
  text-transform: uppercase;
}

.hero-note {
  padding: 20px;
  border-left: 5px solid var(--accent);
  background: var(--paper);
  box-shadow: 5px 5px 0 rgba(23, 22, 20, 0.07);
}

.hero-note strong {
  display: block;
  margin-top: 12px;
  font-size: 24px;
  line-height: 1.12;
}

.hero-note p {
  margin-top: 18px;
  color: var(--muted);
  line-height: 1.5;
}

.band {
  width: min(1180px, calc(100vw - 36px));
  margin: 0 auto;
  padding: 38px 0;
  border-bottom: 1px solid var(--line);
}

.section-heading {
  display: flex;
  gap: 18px;
  align-items: end;
  justify-content: space-between;
  margin-bottom: 28px;
}

.section-heading > div {
  display: grid;
  gap: 8px;
}

.claim-sheet {
  border-top: 2px solid var(--ink);
  background: var(--paper);
}

.claim {
  display: grid;
  grid-template-columns: minmax(180px, 250px) minmax(0, 1fr);
  gap: 20px 28px;
  padding: 22px 0;
  border-bottom: 1px solid var(--line);
}

.claim:last-child {
  border-bottom: 0;
}

.statement {
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(20px, 2vw, 28px);
  line-height: 1.18;
}

.claim-meta {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.claim-meta div,
.thread,
.decision,
.artifact,
.session {
  background: transparent;
}

.claim-meta div {
  min-width: 0;
  padding: 14px 14px 0 0;
  border-top: 1px solid var(--line);
}

b,
dt {
  display: block;
  margin-bottom: 8px;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.claim-meta p,
.claim-meta li,
.thread p,
.thread dd,
.artifact p,
.decision p,
.decision div,
.session p,
.session li {
  color: #4b4941;
  font-size: 14px;
  line-height: 1.5;
}

.claim-meta p,
.thread dd p,
.session p,
.decision p {
  max-width: 72ch;
}

ul {
  margin: 0;
  padding-left: 18px;
}

table {
  display: block;
  width: 100%;
  max-width: 100%;
  margin-top: 10px;
  overflow-x: auto;
  border-collapse: collapse;
  background: rgba(255, 253, 246, 0.78);
  font-size: 13px;
}

th,
td {
  padding: 8px 9px;
  border: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}

th {
  color: #37352f;
  font-size: 11px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.timeline-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0 28px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.milestone {
  position: relative;
  min-height: 150px;
  padding: 0 0 28px 34px;
  border-left: 2px solid var(--line);
}

.milestone::before {
  position: absolute;
  top: 2px;
  left: -7px;
  width: 12px;
  height: 12px;
  border: 2px solid var(--ink);
  border-radius: 50%;
  background: var(--wash);
  content: "";
}

.milestone.complete::before {
  background: var(--green);
}

.milestone.planned::before {
  background: var(--amber);
}

.milestone h3,
.artifact h3,
.decision h3,
.thread h3 {
  margin: 12px 0 8px;
}

.milestone p,
.milestone small {
  display: block;
  max-width: 620px;
  color: var(--muted);
  line-height: 1.45;
}

.split {
  display: grid;
  grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);
  gap: 36px;
  align-items: start;
}

.sticky {
  position: sticky;
  top: 92px;
}

.session-list {
  display: grid;
  gap: 14px;
}

.session {
  border-top: 1px solid var(--ink);
  padding: 18px 0;
}

.session summary {
  display: grid;
  grid-template-columns: 110px minmax(0, 1fr);
  gap: 14px;
  align-items: center;
  cursor: pointer;
  list-style: none;
}

.session summary::-webkit-details-marker {
  display: none;
}

.objective {
  margin: 14px 0 0 124px;
}

.session-fields {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin-top: 18px;
}

.session-fields > div {
  min-width: 0;
}

.session footer {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  margin-top: 18px;
  padding-top: 12px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 13px;
}

.thread-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.thread {
  padding: 18px 0 18px 18px;
  border-left: 5px solid var(--accent);
}

.thread dl {
  display: grid;
  gap: 10px;
  margin: 18px 0 0;
}

.thread dd {
  margin: 0;
}

.artifact-table,
.decision-list {
  display: grid;
  gap: 1px;
  background: var(--line);
  border: 1px solid var(--line);
}

.artifact,
.decision {
  display: grid;
  grid-template-columns: minmax(190px, 0.55fr) minmax(260px, 1fr) minmax(160px, 0.35fr);
  gap: 18px;
  align-items: start;
  min-width: 0;
  padding: 18px;
  background: var(--paper);
}

.decision {
  grid-template-columns: 82px minmax(220px, 0.7fr) minmax(260px, 1fr);
}

.artifact span,
.decision span {
  border-color: rgba(15, 143, 140, 0.28);
  color: var(--accent);
}

.artifact:hover,
.decision:hover,
.thread:hover,
.session:hover {
  background: #fffefa;
  transition: background 160ms ease;
}

@media (max-width: 980px) {
  .topbar,
  .hero,
  .split,
  .claim,
  .claim-meta,
  .timeline-list,
  .thread-grid,
  .session-fields,
  .artifact,
  .decision {
    grid-template-columns: 1fr;
  }

  .hero {
    padding-top: 26px;
  }

  .section-heading {
    display: grid;
    align-items: start;
  }

  .sticky {
    position: static;
  }

  .objective {
    margin-left: 0;
  }
}

@media (max-width: 640px) {
  .topbar {
    padding-right: 16px;
    padding-left: 16px;
  }

  .band,
  .hero {
    width: min(100vw - 28px, 1180px);
  }

  nav {
    justify-content: flex-start;
  }

  .session summary {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: clamp(34px, 10vw, 44px);
  }
}

/* Archive Atlas direction */
body {
  background:
    linear-gradient(90deg, rgba(47, 43, 35, 0.035) 1px, transparent 1px),
    #ece7dc;
  background-size: 56px 100%;
}

.archive-shell {
  display: grid;
  grid-template-columns: 104px minmax(0, 1fr);
  min-height: 100svh;
}

.atlas-sidebar {
  position: sticky;
  top: 0;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 22px;
  height: 100svh;
  padding: 20px 0;
  background:
    linear-gradient(90deg, rgba(255, 255, 255, 0.04), transparent),
    #27241f;
  color: #f4efe4;
}

.monogram {
  display: grid;
  width: 54px;
  height: 54px;
  place-items: center;
  margin: 0 auto;
  border: 1px solid rgba(244, 239, 228, 0.38);
  color: #f4efe4;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 20px;
  text-decoration: none;
  box-shadow: inset 0 0 0 4px rgba(255, 255, 255, 0.04);
}

.atlas-sidebar nav {
  display: grid;
  align-content: start;
  gap: 2px;
  justify-content: stretch;
}

.atlas-sidebar nav a {
  min-height: 38px;
  padding: 11px 14px;
  border: 0;
  border-left: 3px solid transparent;
  border-radius: 0;
  color: rgba(244, 239, 228, 0.82);
  font-size: 12px;
  text-align: left;
}

.atlas-sidebar nav a:hover {
  border-left-color: #b5a16f;
  background: rgba(244, 239, 228, 0.1);
  color: #fffaf0;
}

.atlas-sidebar p {
  margin: 0;
  padding: 0 12px;
  color: rgba(244, 239, 228, 0.6);
  font-size: 11px;
  line-height: 1.45;
}

.archive-main {
  width: min(1320px, calc(100vw - 104px));
  min-width: 0;
  margin: 0 auto;
  padding: 26px clamp(24px, 3vw, 42px) 42px;
}

.archive-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 240px;
  gap: 32px;
  padding: 22px 0 24px;
  border-bottom: 2px solid rgba(47, 43, 35, 0.55);
}

.archive-hero h1 {
  font-size: clamp(42px, 5vw, 64px);
  line-height: 0.98;
}

.archive-hero .lede {
  max-width: 840px;
  color: #494438;
  font-size: 17px;
}

.archive-stamp {
  align-self: start;
  padding: 14px;
  border: 1px solid rgba(47, 43, 35, 0.2);
  background: rgba(255, 252, 243, 0.55);
}

.archive-stamp span {
  display: block;
  margin-bottom: 12px;
  color: var(--muted);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.archive-stamp strong {
  display: block;
  font-size: 17px;
  line-height: 1.18;
}

.archive-stamp p {
  margin-top: 12px;
  color: var(--muted);
  font-size: 12px;
  line-height: 1.45;
}

.source-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0;
  margin-top: 18px;
  border: 1px solid var(--line);
  background: rgba(255, 252, 243, 0.5);
}

.source-tabs a {
  min-height: 38px;
  padding: 11px 14px;
  border-right: 1px solid var(--line);
  color: #514a3b;
  font-size: 12px;
  font-weight: 800;
  text-decoration: none;
}

.source-tabs a:hover {
  background: var(--paper);
}

.archive-stats {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  margin: 16px 0 26px;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}

.archive-stats div {
  display: grid;
  gap: 4px;
  min-height: 74px;
  place-items: center;
  border-right: 1px solid var(--line);
}

.archive-stats div:last-child {
  border-right: 0;
}

.archive-stats strong {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 28px;
  font-weight: 400;
}

.archive-stats span {
  color: var(--muted);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.band {
  width: 100%;
  padding: 28px 0;
}

.section-heading {
  padding-bottom: 12px;
  margin-bottom: 0;
  border-bottom: 1px solid rgba(47, 43, 35, 0.3);
}

.section-heading h2 {
  font-size: clamp(27px, 2.5vw, 38px);
}

.eyebrow {
  color: #566d63;
}

.claim-sheet {
  border-top: 0;
  background: rgba(255, 252, 243, 0.58);
}

.claim {
  grid-template-columns: 210px minmax(0, 1fr);
  gap: 16px 28px;
  padding: 22px 0 0;
}

.claim h3 {
  margin-top: 3px;
  font-size: 16px;
}

.statement {
  max-width: 920px;
  font-size: clamp(21px, 2.1vw, 30px);
  line-height: 1.16;
}

.claim-meta {
  grid-template-columns: minmax(240px, 0.9fr) minmax(220px, 0.7fr) minmax(220px, 0.7fr);
  gap: 0;
  border-top: 1px solid var(--line);
}

.claim-meta div {
  padding: 16px 18px 18px 0;
  border-top: 0;
  border-right: 1px solid var(--line);
}

.claim-meta div + div {
  padding-left: 18px;
}

.claim-meta div:last-child {
  border-right: 0;
}

.claim-meta li,
.claim-meta p,
.thread dd,
.session p,
.session li,
.artifact p,
.decision p,
.decision div {
  color: #4f493d;
  font-size: 13px;
}

table {
  background: rgba(255, 252, 243, 0.82);
}

th {
  color: #5b5548;
}

.timeline-list {
  grid-template-columns: 1fr;
  max-width: 980px;
  margin-top: 18px;
}

.milestone {
  min-height: 0;
  padding-bottom: 20px;
}

.milestone h3 {
  font-size: 16px;
}

.split {
  grid-template-columns: 230px minmax(0, 1fr);
}

.session {
  padding: 16px 0;
  border-top: 1px solid var(--line);
}

.session summary strong {
  font-size: 17px;
}

.session-fields {
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0;
  border-top: 1px solid var(--line);
  margin-top: 14px;
}

.session-fields > div {
  padding: 14px 14px 0 0;
  border-right: 1px solid var(--line);
}

.session-fields > div + div {
  padding-left: 14px;
}

.session-fields > div:last-child {
  border-right: 0;
}

.thread-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0;
  border: 1px solid var(--line);
  border-bottom: 0;
}

.thread {
  padding: 18px;
  border-left: 0;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 252, 243, 0.56);
}

.thread:nth-child(odd) {
  border-right: 1px solid var(--line);
}

.artifact-table,
.decision-list {
  margin-top: 0;
  background: transparent;
  border-color: var(--line);
}

.artifact,
.decision {
  background: rgba(255, 252, 243, 0.66);
}

.artifact {
  grid-template-columns: minmax(210px, 0.55fr) minmax(340px, 1fr) minmax(190px, 0.35fr);
}

.decision {
  grid-template-columns: 80px minmax(260px, 0.7fr) minmax(340px, 1fr);
}

.artifact:hover,
.decision:hover,
.thread:hover,
.session:hover {
  background: #fffdf6;
}

@media (max-width: 1100px) {
  .archive-shell {
    grid-template-columns: 1fr;
  }

  .atlas-sidebar {
    position: sticky;
    z-index: 20;
    height: auto;
    grid-template-columns: auto 1fr;
    grid-template-rows: auto;
    align-items: center;
    padding: 10px 14px;
  }

  .atlas-sidebar p {
    display: none;
  }

  .atlas-sidebar nav {
    display: flex;
    flex-wrap: wrap;
  }

  .atlas-sidebar nav a {
    min-height: 32px;
    padding: 8px 10px;
    border-left: 0;
    border-bottom: 2px solid transparent;
  }

  .archive-main {
    width: min(100vw, 1320px);
  }

  .archive-hero,
  .claim,
  .split,
  .artifact,
  .decision,
  .session-fields {
    grid-template-columns: 1fr;
  }

  .claim-meta {
    grid-template-columns: 1fr;
  }

  .claim-meta div,
  .claim-meta div + div,
  .session-fields > div,
  .session-fields > div + div {
    padding-left: 0;
    border-right: 0;
  }

  .archive-stats {
    grid-template-columns: repeat(3, 1fr);
  }

  .thread-grid {
    grid-template-columns: 1fr;
  }

  .thread:nth-child(odd) {
    border-right: 0;
  }
}

@media (max-width: 640px) {
  .archive-main {
    padding-right: 16px;
    padding-left: 16px;
  }

  .archive-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .archive-hero h1 {
    font-size: 38px;
  }
}

/* Archive Atlas polish pass: compact, crisp, document-register density. */
body {
  -webkit-font-smoothing: antialiased;
  text-rendering: geometricPrecision;
}

.archive-shell {
  grid-template-columns: 86px minmax(0, 1fr);
}

.archive-main {
  width: min(1240px, calc(100vw - 86px));
  padding-top: 18px;
}

.atlas-sidebar {
  gap: 18px;
}

.monogram {
  width: 46px;
  height: 46px;
  font-size: 19px;
}

.atlas-sidebar nav a {
  min-height: 32px;
  padding: 8px 12px;
  font-size: 11px;
}

.archive-hero {
  grid-template-columns: minmax(0, 1fr) 220px;
  gap: 26px;
  padding: 14px 0 18px;
}

.archive-hero h1 {
  font-size: clamp(36px, 4vw, 52px);
}

.archive-hero .lede {
  max-width: 780px;
  margin-top: 10px;
  font-size: 14px;
  line-height: 1.42;
}

.archive-stamp {
  padding: 11px;
}

.archive-stamp strong {
  font-size: 14px;
}

.archive-stamp p {
  font-size: 11px;
}

.source-tabs {
  margin-top: 12px;
}

.source-tabs a {
  min-height: 32px;
  padding: 8px 12px;
  font-size: 11px;
}

.archive-stats {
  margin: 12px 0 14px;
}

.archive-stats div {
  min-height: 52px;
}

.archive-stats strong {
  font-size: 22px;
}

.archive-stats span {
  font-size: 9px;
}

.band {
  padding: 16px 0;
}

.section-heading {
  align-items: end;
  padding-bottom: 9px;
}

.section-heading h2 {
  font-size: clamp(23px, 2vw, 31px);
}

.section-heading span {
  align-self: end;
}

.eyebrow {
  margin-bottom: 7px;
  font-size: 10px;
}

.claim {
  grid-template-columns: 170px minmax(0, 1fr);
  gap: 10px 24px;
  padding-top: 14px;
}

.claim h3 {
  margin-top: 2px;
  font-size: 13px;
  line-height: 1.25;
}

.statement {
  max-width: 820px;
  font-size: clamp(16px, 1.35vw, 21px);
  line-height: 1.2;
}

.claim-meta {
  grid-template-columns: minmax(260px, 0.95fr) minmax(220px, 0.7fr) minmax(220px, 0.7fr);
}

.claim-meta div {
  padding: 11px 16px 13px 0;
}

.claim-meta div + div {
  padding-left: 16px;
}

b,
dt {
  margin-bottom: 7px;
  font-size: 10px;
}

.claim-meta p,
.claim-meta li,
.thread p,
.thread dd,
.artifact p,
.decision p,
.decision div,
.session p,
.session li {
  font-size: 12px;
  line-height: 1.42;
}

ul {
  padding-left: 15px;
}

li + li {
  margin-top: 3px;
}

code {
  padding: 1px 4px;
  font-size: 0.88em;
}

table {
  font-size: 11px;
}

th,
td {
  padding: 6px 7px;
}

th {
  font-size: 9px;
}

.timeline-list {
  margin-top: 12px;
}

.milestone {
  padding-bottom: 13px;
}

.milestone h3,
.thread h3,
.artifact h3,
.decision h3 {
  font-size: 14px;
}

.milestone p,
.milestone small {
  font-size: 12px;
}

.split {
  grid-template-columns: 210px minmax(0, 1fr);
}

.session {
  padding: 12px 0;
}

.session summary {
  grid-template-columns: 94px minmax(0, 1fr);
}

.session summary strong {
  font-size: 14px;
}

.objective {
  margin-left: 108px;
  font-size: 12px;
}

.session-fields {
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin-top: 10px;
}

.session-fields > div {
  padding: 10px 12px 0 0;
}

.session-fields > div + div {
  padding-left: 12px;
}

.thread {
  padding: 13px;
}

.thread dl {
  gap: 8px;
  margin-top: 12px;
}

.artifact,
.decision {
  padding: 13px;
}

.artifact {
  grid-template-columns: minmax(190px, 0.55fr) minmax(300px, 1fr) minmax(160px, 0.35fr);
}

.decision {
  grid-template-columns: 70px minmax(230px, 0.7fr) minmax(300px, 1fr);
}

@media (max-width: 1100px) {
  .archive-main {
    width: min(100vw, 1240px);
  }

  .claim,
  .claim-meta,
  .session-fields,
  .split {
    grid-template-columns: 1fr;
  }

  .objective {
    margin-left: 0;
  }
}

/* Self-contained JS web app shell */
.app-body {
  min-height: 100svh;
  background:
    linear-gradient(90deg, rgba(44, 40, 33, 0.035) 1px, transparent 1px),
    #eee9dd;
  background-size: 56px 100%;
  -webkit-font-smoothing: antialiased;
  text-rendering: geometricPrecision;
}

.app-shell {
  display: grid;
  grid-template-columns: 88px minmax(0, 1fr);
  min-height: 100svh;
}

.app-rail {
  position: sticky;
  top: 0;
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 18px;
  height: 100svh;
  padding: 20px 0;
  background: #292621;
  color: #f7f0e2;
}

.app-mark {
  display: grid;
  width: 48px;
  height: 48px;
  place-items: center;
  margin: 0 auto;
  border: 1px solid rgba(247, 240, 226, 0.42);
  color: #fff8e9;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 19px;
  text-decoration: none;
}

.app-rail nav {
  display: grid;
  align-content: start;
  gap: 2px;
}

.app-rail button {
  min-height: 33px;
  padding: 8px 12px;
  border: 0;
  border-left: 3px solid transparent;
  background: transparent;
  color: rgba(247, 240, 226, 0.8);
  cursor: pointer;
  font: inherit;
  font-size: 11px;
  text-align: left;
}

.app-rail button:hover,
.app-rail button.is-active {
  border-left-color: #b49f6b;
  background: rgba(247, 240, 226, 0.1);
  color: #fffaf0;
}

.app-rail p {
  margin: 0;
  padding: 0 12px;
  color: rgba(247, 240, 226, 0.58);
  font-size: 10px;
  line-height: 1.45;
}

.app-main {
  width: min(1240px, calc(100vw - 88px));
  min-width: 0;
  margin: 0 auto;
  padding: 18px clamp(24px, 3vw, 38px) 36px;
}

.app-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: 28px;
  align-items: start;
  padding: 14px 0 18px;
  border-bottom: 2px solid rgba(47, 43, 35, 0.55);
}

.app-header h1 {
  font-size: clamp(36px, 4vw, 52px);
  line-height: 1;
}

.app-header p {
  max-width: 820px;
  margin-top: 10px;
  color: #494438;
  font-size: 14px;
  line-height: 1.42;
}

.app-kicker {
  margin: 0 0 7px;
  color: #566d63;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.app-search {
  display: grid;
  gap: 8px;
  padding: 12px;
  border: 1px solid var(--line);
  background: rgba(255, 252, 243, 0.62);
}

.app-search span {
  color: var(--muted);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.app-search input {
  width: 100%;
  min-height: 34px;
  border: 1px solid rgba(47, 43, 35, 0.22);
  background: #fffdf6;
  color: var(--ink);
  font: inherit;
  font-size: 13px;
  padding: 7px 9px;
}

.source-tabs {
  margin-top: 12px;
}

.app-stats {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  margin: 12px 0 18px;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}

.app-stats button {
  display: grid;
  gap: 3px;
  min-height: 52px;
  place-items: center;
  border: 0;
  border-right: 1px solid var(--line);
  background: transparent;
  color: var(--ink);
  cursor: default;
}

.app-stats button:last-child {
  border-right: 0;
}

.app-stats strong {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 22px;
  font-weight: 400;
}

.app-stats span {
  color: var(--muted);
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.app-view {
  min-width: 0;
}

.view-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 260px;
  gap: 14px;
}

.primary-panel {
  grid-column: span 1;
}

.archive-panel {
  min-width: 0;
  border: 1px solid var(--line);
  background: rgba(255, 252, 243, 0.68);
}

.archive-panel > * {
  padding-right: 14px;
  padding-left: 14px;
}

.panel-heading {
  padding-top: 13px;
  padding-bottom: 11px;
  border-bottom: 1px solid var(--line);
}

.panel-heading.row {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 14px;
}

.panel-heading h2 {
  font-size: clamp(22px, 2vw, 30px);
}

.panel-heading button {
  border: 1px solid var(--line);
  background: #fffdf6;
  color: var(--muted);
  cursor: pointer;
  font: inherit;
  font-size: 11px;
  padding: 6px 8px;
}

.claim-line {
  max-width: 820px;
  padding-top: 14px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--line);
  font-family: Georgia, "Times New Roman", serif;
  font-size: clamp(17px, 1.45vw, 22px);
  line-height: 1.2;
}

.triad,
.quad {
  display: grid;
  gap: 0;
}

.triad {
  grid-template-columns: minmax(260px, 0.95fr) minmax(220px, 0.7fr) minmax(220px, 0.7fr);
}

.quad {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.triad section,
.quad section {
  min-width: 0;
  padding: 12px 14px 14px;
  border-right: 1px solid var(--line);
}

.triad section:last-child,
.quad section:last-child {
  border-right: 0;
}

.archive-panel p,
.archive-panel li,
.archive-panel dd,
.archive-panel small,
.index-row small {
  color: #4f493d;
  font-size: 12px;
  line-height: 1.42;
}

.archive-panel ul {
  padding-left: 15px;
}

.compact-panel {
  padding: 13px;
}

.compact-panel h3 {
  margin: 0 0 10px;
  font-size: 15px;
}

.index-row {
  display: grid;
  grid-template-columns: 76px minmax(0, 1fr) minmax(110px, 0.42fr);
  gap: 12px;
  align-items: start;
  padding: 11px 14px;
  border-bottom: 1px solid var(--line);
}

.index-row:last-child {
  border-bottom: 0;
}

.index-row span,
.session-record summary span,
.decision-record > span {
  color: var(--muted);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.index-row strong {
  font-size: 13px;
  line-height: 1.25;
}

.view-grid > .archive-panel .artifact-row {
  grid-template-columns: 72px minmax(0, 1fr);
}

.view-grid > .archive-panel .artifact-row small {
  display: none;
}

.artifact-row strong a {
  display: inline;
  overflow-wrap: anywhere;
}

.claim-app {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 14px;
}

.record-list {
  display: grid;
  align-content: start;
  border: 1px solid var(--line);
  background: rgba(255, 252, 243, 0.42);
}

.record-list button {
  display: grid;
  grid-template-columns: 34px 1fr;
  gap: 8px;
  align-items: start;
  min-height: 42px;
  padding: 10px;
  border: 0;
  border-bottom: 1px solid var(--line);
  background: transparent;
  color: var(--ink);
  cursor: pointer;
  font: inherit;
  font-size: 12px;
  text-align: left;
}

.record-list button.is-active,
.record-list button:hover {
  background: #fffdf6;
}

.record-list span {
  color: var(--muted);
  font-size: 10px;
  font-weight: 900;
}

.app-timeline {
  margin: 0;
  padding: 12px 14px 4px;
  list-style: none;
}

.app-timeline li {
  position: relative;
  display: grid;
  grid-template-columns: 94px minmax(0, 1fr);
  gap: 18px;
  padding: 0 0 17px 20px;
  border-left: 1px solid rgba(47, 43, 35, 0.26);
}

.app-timeline li::before {
  position: absolute;
  top: 2px;
  left: -5px;
  width: 9px;
  height: 9px;
  border: 1px solid var(--ink);
  border-radius: 50%;
  background: #eee9dd;
  content: "";
}

.app-timeline h3,
.decision-record h3 {
  margin: 0 0 4px;
  font-size: 14px;
}

.session-record {
  padding: 0 14px 12px;
  border-bottom: 1px solid var(--line);
}

.session-record summary {
  display: grid;
  grid-template-columns: 84px minmax(0, 1fr) 80px;
  gap: 12px;
  align-items: center;
  min-height: 42px;
  cursor: pointer;
}

.session-record summary strong {
  font-size: 14px;
}

.session-record summary a {
  font-size: 11px;
}

.session-record footer {
  padding-top: 10px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 12px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.body-lead {
  padding-top: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--line);
}

.stacked-fields section {
  padding: 12px 14px;
  border-bottom: 1px solid var(--line);
}

.stacked-fields section:last-child {
  border-bottom: 0;
}

.shelf {
  display: grid;
}

.decision-record {
  display: grid;
  grid-template-columns: 64px minmax(220px, 0.72fr) minmax(280px, 1fr);
  gap: 14px;
  padding: 13px 14px;
  border-bottom: 1px solid var(--line);
}

.decision-record:last-child {
  border-bottom: 0;
}

.decision-record small {
  display: block;
  margin-top: 8px;
}

@media (max-width: 1100px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .app-rail {
    position: sticky;
    z-index: 20;
    height: auto;
    grid-template-columns: auto 1fr;
    grid-template-rows: auto;
    align-items: center;
    padding: 10px 14px;
  }

  .app-rail p {
    display: none;
  }

  .app-rail nav {
    display: flex;
    flex-wrap: wrap;
  }

  .app-rail button {
    border-left: 0;
    border-bottom: 2px solid transparent;
  }

  .app-main {
    width: min(100vw, 1240px);
  }

  .app-header,
  .view-grid,
  .claim-app,
  .triad,
  .quad,
  .card-grid,
  .decision-record {
    grid-template-columns: 1fr;
  }

  .triad section,
  .quad section {
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }

  .app-stats {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 680px) {
  .app-main {
    padding-right: 16px;
    padding-left: 16px;
  }

  .app-stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .index-row,
  .session-record summary,
  .app-timeline li {
    grid-template-columns: 1fr;
  }
}

/* Evidence Notebook upgrade: source-ledger workspace with denser review affordances. */
:root {
  --blueprint: #111827;
  --paper-strong: #fffdf7;
  --paper-soft: rgba(255, 253, 247, 0.74);
  --cyan: #168d91;
  --clinical-green: #2f7d57;
  --review-amber: #b7791f;
}

.app-body {
  background:
    linear-gradient(90deg, rgba(22, 141, 145, 0.04) 1px, transparent 1px),
    linear-gradient(rgba(47, 43, 35, 0.025) 1px, transparent 1px),
    #ede8dc;
  background-size: 64px 100%, 100% 28px;
}

.app-rail {
  background:
    linear-gradient(180deg, rgba(22, 141, 145, 0.16), transparent 42%),
    #25231f;
}

.app-mark {
  border-color: rgba(255, 253, 247, 0.5);
  box-shadow: inset 0 0 0 4px rgba(255, 255, 255, 0.045);
}

.app-main {
  width: min(1320px, calc(100vw - 88px));
  padding-top: 22px;
}

.app-header {
  grid-template-columns: minmax(0, 1fr) minmax(240px, 320px);
  padding-bottom: 20px;
}

.app-header h1 {
  max-width: 880px;
  font-size: clamp(42px, 5.2vw, 72px);
  letter-spacing: 0;
}

.app-header p {
  max-width: 900px;
  font-size: 15px;
}

.header-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.header-meta span,
.source-card span,
.source-card small,
.action-panel button,
.panel-heading button {
  color: var(--muted);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.header-meta span {
  padding: 5px 8px;
  border: 1px solid var(--line);
  background: rgba(255, 253, 247, 0.62);
}

.app-search {
  background: var(--paper-soft);
}

.source-ledger {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 1px;
  margin-top: 14px;
  border: 1px solid var(--line);
  background: var(--line);
}

.source-card {
  display: grid;
  gap: 6px;
  min-height: 82px;
  padding: 12px;
  background: rgba(255, 253, 247, 0.76);
  text-decoration: none;
}

.source-card strong {
  overflow-wrap: anywhere;
  font-size: 13px;
}

.source-card:hover,
.app-stats button:hover,
.panel-heading button:hover,
.action-panel button:hover {
  background: var(--paper-strong);
}

.app-stats {
  border: 1px solid var(--line);
  background: rgba(255, 253, 247, 0.56);
}

.app-stats button {
  cursor: pointer;
  transition: background 150ms ease, color 150ms ease;
}

.app-stats button:hover strong {
  color: var(--cyan);
}

.overview-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(240px, 300px);
  gap: 14px;
}

.overview-grid .primary-panel {
  grid-column: 1;
  grid-row: span 2;
}

.archive-panel {
  background: var(--paper-soft);
  box-shadow: 0 22px 70px rgba(48, 43, 34, 0.06);
}

.claim-dossier {
  border-top: 3px solid var(--ink);
}

.claim-line {
  font-size: clamp(19px, 1.7vw, 27px);
}

.triad section:first-child {
  border-top: 3px solid rgba(22, 141, 145, 0.28);
}

.triad section:nth-child(2) {
  border-top: 3px solid rgba(183, 121, 31, 0.34);
}

.triad section:nth-child(3) {
  border-top: 3px solid rgba(47, 125, 87, 0.34);
}

.action-panel {
  display: grid;
  align-content: start;
  gap: 10px;
  padding: 14px;
  border-top: 3px solid var(--clinical-green);
}

.action-panel h3 {
  font-size: 17px;
}

.action-panel button,
.panel-heading button {
  width: fit-content;
  min-height: 32px;
  padding: 7px 9px;
  border: 1px solid var(--line);
  background: rgba(255, 253, 247, 0.8);
  cursor: pointer;
}

.decision-brief {
  padding-bottom: 14px;
  border-top: 3px solid var(--review-amber);
}

.decision-brief h3,
.decision-brief p,
.decision-brief small {
  display: block;
  padding-right: 14px;
  padding-left: 14px;
}

.decision-brief h3 {
  padding-top: 14px;
  font-size: 15px;
}

.decision-brief p {
  padding-top: 8px;
}

.decision-brief small {
  padding-top: 10px;
  overflow-wrap: anywhere;
}

.index-panel {
  min-height: 220px;
}

.index-row {
  transition: background 150ms ease;
}

.index-row:hover {
  background: var(--paper-strong);
}

.artifact-row.is-planned span {
  color: var(--review-amber);
}

.artifact-row.is-active span,
.artifact-row.is-current span {
  color: var(--cyan);
}

.claim-app {
  grid-template-columns: minmax(210px, 260px) minmax(0, 1fr);
}

.record-list {
  position: sticky;
  top: 18px;
  max-height: calc(100svh - 36px);
  overflow: auto;
}

.app-timeline li {
  min-height: 82px;
}

.app-timeline li::before {
  background: var(--paper-strong);
}

.app-timeline li.is-complete::before {
  border-color: var(--clinical-green);
  background: var(--clinical-green);
}

.app-timeline li.is-planned::before,
.app-timeline li.is-active::before {
  border-color: var(--review-amber);
  background: var(--review-amber);
}

.app-timeline em {
  display: block;
  margin-top: 7px;
  color: #5e5545;
  font-size: 12px;
  font-style: normal;
}

.session-record[open] {
  background: rgba(255, 253, 247, 0.44);
}

.session-record summary a {
  text-align: right;
}

.empty-state {
  padding: 16px 14px;
  color: var(--muted);
  font-size: 13px;
}

@media (max-width: 1100px) {
  .app-main {
    width: min(100vw, 1320px);
  }

  .source-ledger {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .overview-grid,
  .overview-grid .primary-panel {
    grid-template-columns: 1fr;
    grid-column: auto;
  }

  .record-list {
    position: static;
    max-height: none;
  }
}

@media (max-width: 680px) {
  .source-ledger {
    grid-template-columns: 1fr;
  }

  .app-header h1 {
    font-size: 40px;
  }

  .header-meta {
    display: grid;
  }
}

/* Typography and spacing refinement: calmer scale, tighter rhythm, cleaner reading measure. */
:root {
  --content-max: 1184px;
  --rail-width: 332px;
  --gutter: clamp(20px, 3vw, 32px);
}

body {
  font-size: 14px;
  font-feature-settings: "kern" 1, "liga" 1, "tnum" 1;
}

.app-shell {
  grid-template-columns: 96px minmax(0, 1fr);
}

.app-rail {
  gap: 14px;
}

.app-mark {
  width: 44px;
  height: 44px;
  font-size: 18px;
}

.app-rail button {
  min-height: 38px;
  padding: 10px 16px;
  font-size: 12px;
}

.app-rail p {
  padding: 0 10px;
  font-size: 11px;
}

.app-main {
  width: min(var(--content-max), calc(100vw - 96px));
  padding: 34px var(--gutter) 44px;
}

.app-header {
  grid-template-columns: minmax(0, 760px) minmax(260px, 340px);
  gap: clamp(28px, 5vw, 72px);
  padding: 18px 0 26px;
  align-items: start;
}

.app-header h1 {
  max-width: 760px;
  font-size: clamp(52px, 5.2vw, 78px);
  line-height: 0.92;
}

.app-header p {
  max-width: 760px;
  margin-top: 18px;
  color: #2f312d;
  font-size: 17px;
  line-height: 1.42;
}

.app-kicker,
.header-meta span,
.source-card span,
.source-card small,
.action-panel button,
.panel-heading button,
.app-stats span,
.index-row span,
.session-record summary span,
.decision-record > span {
  letter-spacing: 0.12em;
}

.app-kicker {
  margin-bottom: 10px;
  font-size: 11px;
}

.header-meta {
  gap: 10px;
  margin-top: 20px;
}

.header-meta span {
  padding: 6px 9px;
  background: rgba(255, 253, 247, 0.78);
}

.app-search {
  padding: 14px;
}

.app-search input {
  min-height: 38px;
  padding: 9px 10px;
}

.source-ledger {
  margin-top: 18px;
}

.source-card {
  gap: 8px;
  min-height: 76px;
  padding: 14px 15px;
}

.source-card strong {
  font-size: 13px;
  line-height: 1.25;
}

.app-stats {
  margin: 12px 0 22px;
}

.app-stats button {
  min-height: 58px;
}

.app-stats strong {
  font-size: 24px;
  line-height: 1;
}

.overview-grid {
  grid-template-columns: minmax(0, 1fr) var(--rail-width);
  gap: 18px;
  align-items: start;
}

.overview-grid .primary-panel {
  grid-row: auto;
}

.session-panel,
.artifact-panel,
.decision-brief {
  grid-column: 1;
}

.action-panel {
  grid-column: 2;
}

.artifact-panel {
  grid-row: 3;
}

.decision-brief {
  grid-row: 4;
}

.archive-panel {
  box-shadow: 0 18px 50px rgba(48, 43, 34, 0.045);
}

.archive-panel > * {
  padding-right: 17px;
  padding-left: 17px;
}

.panel-heading {
  padding-top: 18px;
  padding-bottom: 15px;
}

.panel-heading h2 {
  font-size: clamp(22px, 2.1vw, 34px);
  line-height: 1;
}

.index-panel .panel-heading h2,
.decision-brief .panel-heading h2 {
  font-size: clamp(26px, 2.4vw, 38px);
  line-height: 0.98;
}

.claim-dossier {
  border-top-width: 2px;
}

.claim-line {
  max-width: 74ch;
  padding-top: 18px;
  padding-bottom: 18px;
  font-size: 16px;
  line-height: 1.48;
}

.triad {
  grid-template-columns: minmax(320px, 1.1fr) minmax(220px, 0.7fr) minmax(220px, 0.7fr);
}

.triad section,
.quad section {
  padding: 16px 17px 18px;
}

.archive-panel p,
.archive-panel li,
.archive-panel dd,
.archive-panel small,
.index-row small {
  color: #3f3b33;
  font-size: 13px;
  line-height: 1.52;
}

.archive-panel li + li {
  margin-top: 6px;
}

b,
dt {
  margin-bottom: 10px;
  font-size: 11px;
}

.action-panel {
  gap: 14px;
  padding: 18px;
  border-top-width: 2px;
}

.action-panel h3 {
  max-width: 20ch;
  font-size: 19px;
  line-height: 1.18;
}

.action-panel p {
  max-width: 28ch;
}

.action-panel button,
.panel-heading button {
  min-height: 36px;
  padding: 8px 12px;
}

.index-row {
  grid-template-columns: 96px minmax(0, 1fr) minmax(100px, 0.38fr);
  gap: 16px;
  padding: 14px 17px;
}

.index-row strong {
  font-size: 13px;
  line-height: 1.28;
}

.index-panel .index-row {
  grid-template-columns: 96px minmax(0, 0.9fr) minmax(0, 1fr);
}

.artifact-panel .index-row {
  grid-template-columns: 96px minmax(180px, 0.75fr) minmax(180px, 0.65fr);
}

.view-grid > .archive-panel .artifact-row,
.artifact-row {
  grid-template-columns: 92px minmax(0, 1fr) minmax(160px, 0.55fr);
}

.view-grid > .archive-panel .artifact-row small {
  display: block;
}

.decision-brief {
  padding-bottom: 18px;
  border-top-width: 2px;
}

.decision-brief h3,
.decision-brief p,
.decision-brief small {
  padding-right: 17px;
  padding-left: 17px;
}

.decision-brief h3 {
  max-width: 26ch;
  padding-top: 18px;
  font-size: 17px;
  line-height: 1.22;
}

.decision-brief p {
  max-width: 32ch;
}

.record-list button {
  min-height: 48px;
  padding: 12px;
  line-height: 1.28;
}

.app-timeline {
  padding-top: 16px;
}

.app-timeline li {
  grid-template-columns: 112px minmax(0, 1fr);
  gap: 22px;
  min-height: 0;
  padding-bottom: 22px;
}

.app-timeline h3,
.decision-record h3 {
  font-size: 15px;
  line-height: 1.24;
}

.app-timeline em {
  margin-top: 8px;
  line-height: 1.45;
}

.session-record {
  padding: 0 17px 15px;
}

.session-record summary {
  grid-template-columns: 96px minmax(0, 1fr) 84px;
  min-height: 50px;
}

.session-record summary strong {
  line-height: 1.25;
}

.card-grid {
  gap: 18px;
}

.stacked-fields section {
  padding: 15px 17px;
}

.decision-record {
  grid-template-columns: 76px minmax(220px, 0.72fr) minmax(300px, 1fr);
  padding: 16px 17px;
}

@media (max-width: 1200px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }

  .session-panel,
  .artifact-panel,
  .decision-brief,
  .action-panel {
    grid-column: auto;
    grid-row: auto;
  }
}

@media (max-width: 1100px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .app-main {
    width: min(100vw, var(--content-max));
  }

  .app-header {
    grid-template-columns: 1fr;
  }

  .app-header p {
    max-width: 70ch;
  }

  .triad,
  .index-panel .index-row,
  .view-grid > .archive-panel .artifact-row,
  .artifact-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 680px) {
  .app-main {
    padding: 24px 16px 36px;
  }

  .app-header h1 {
    font-size: 44px;
  }

  .app-header p {
    font-size: 15px;
  }
}

/* Overview alignment pass: one shared column rhythm, no narrow artifact table. */
.overview-grid {
  grid-template-columns: minmax(0, 1fr);
  gap: 18px;
}

.overview-grid .primary-panel,
.session-panel,
.artifact-panel,
.decision-brief,
.action-panel {
  grid-column: 1;
  grid-row: auto;
}

.action-panel {
  display: grid;
  grid-template-columns: minmax(180px, 0.32fr) minmax(260px, 1fr) auto;
  gap: 18px;
  align-items: center;
}

.action-panel .app-kicker {
  grid-column: 1 / -1;
  margin-bottom: 0;
}

.action-panel h3 {
  max-width: none;
  margin: 0;
}

.action-panel p {
  max-width: 54ch;
}

.action-panel button {
  justify-self: end;
}

.panel-heading.row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
}

.panel-heading.row h2 {
  max-width: none;
}

.artifact-panel .index-row,
.view-grid > .archive-panel .artifact-row,
.artifact-row {
  grid-template-columns: 120px minmax(260px, 0.8fr) minmax(260px, 1fr);
  align-items: center;
}

.artifact-panel .index-row strong,
.artifact-panel .index-row small,
.artifact-row strong,
.artifact-row small {
  min-width: 0;
  overflow-wrap: anywhere;
}

.artifact-panel .index-row small {
  justify-self: start;
}

@media (max-width: 900px) {
  .action-panel,
  .artifact-panel .index-row,
  .view-grid > .archive-panel .artifact-row,
  .artifact-row {
    grid-template-columns: 1fr;
  }

  .action-panel button {
    justify-self: start;
  }
}

/* Timeline view polish: turn the loose spine into a compact milestone ledger. */
.timeline-panel > .panel-heading {
  border-bottom: 0;
}

.timeline-summary {
  display: grid;
  gap: 1px;
  padding: 0;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  background: var(--line);
}

.timeline-progress {
  display: grid;
  grid-template-columns: minmax(190px, 0.28fr) minmax(260px, 1fr) minmax(260px, 0.58fr);
  gap: 18px;
  align-items: center;
  padding: 18px 20px;
  background: rgba(255, 253, 247, 0.78);
}

.timeline-progress > div:first-child {
  display: grid;
  gap: 4px;
}

.timeline-progress strong {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 38px;
  line-height: 0.9;
}

.timeline-progress span,
.timeline-progress p {
  color: #504a40;
  font-size: 12px;
  line-height: 1.42;
}

.timeline-progress p {
  margin: 0;
}

.timeline-progress b {
  margin-bottom: 5px;
}

.progress-rail {
  position: relative;
  height: 10px;
  border: 1px solid rgba(47, 43, 35, 0.18);
  background: rgba(47, 43, 35, 0.06);
}

.progress-rail i {
  position: absolute;
  inset: 0 auto 0 0;
  display: block;
  background: linear-gradient(90deg, rgba(47, 125, 87, 0.62), rgba(22, 141, 145, 0.48));
}

.phase-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1px;
  background: var(--line);
}

.phase-strip article {
  display: grid;
  grid-template-columns: 32px minmax(0, 1fr);
  gap: 10px;
  align-items: start;
  min-height: 86px;
  padding: 15px 16px;
  background: rgba(255, 253, 247, 0.72);
}

.phase-strip article.has-items {
  background: rgba(255, 253, 247, 0.9);
}

.phase-strip span {
  display: grid;
  width: 30px;
  height: 30px;
  place-items: center;
  border: 1px solid rgba(22, 141, 145, 0.28);
  color: var(--cyan);
  font-size: 10px;
  font-weight: 900;
}

.phase-strip h3 {
  margin: 0;
  font-size: 14px;
  line-height: 1.2;
}

.phase-strip p {
  grid-column: 2;
  margin: -4px 0 0;
  color: #5c5548;
  font-size: 12px;
}

.key-events {
  display: grid;
  grid-template-columns: minmax(180px, 0.34fr) repeat(3, minmax(0, 1fr));
  gap: 1px;
  background: var(--line);
}

.key-events > div,
.key-events article {
  display: grid;
  align-content: start;
  gap: 8px;
  min-height: 118px;
  padding: 16px;
  background: rgba(255, 253, 247, 0.86);
}

.key-events h3 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 24px;
  line-height: 1;
}

.key-events article span {
  width: fit-content;
  padding: 5px 7px;
  border: 1px solid rgba(47, 125, 87, 0.22);
  color: var(--clinical-green);
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.key-events article strong {
  font-size: 13px;
  line-height: 1.22;
}

.key-events article small {
  color: #655d50;
  font-size: 11px;
  line-height: 1.36;
}

.app-view > .archive-panel .app-timeline {
  display: grid;
  gap: 0;
  padding: 0;
}

.app-timeline li {
  display: grid;
  grid-template-columns: 148px minmax(0, 1fr);
  gap: 26px;
  min-height: 0;
  padding: 22px 24px 22px 0;
  border-left: 0;
  border-bottom: 1px solid var(--line);
}

.app-timeline li:last-child {
  border-bottom: 0;
}

.app-timeline li::before {
  display: none;
}

.app-timeline li > span {
  align-self: start;
  justify-self: end;
  min-width: 92px;
  padding: 7px 9px;
  border: 1px solid rgba(47, 43, 35, 0.18);
  background: rgba(255, 253, 247, 0.74);
  color: #4d493f;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.1em;
  line-height: 1;
  text-align: center;
  text-transform: uppercase;
}

.app-timeline li.is-complete > span {
  border-color: rgba(47, 125, 87, 0.28);
  background: rgba(47, 125, 87, 0.1);
  color: var(--clinical-green);
}

.app-timeline li.is-planned > span,
.app-timeline li.is-active > span {
  border-color: rgba(183, 121, 31, 0.32);
  background: rgba(183, 121, 31, 0.1);
  color: var(--review-amber);
}

.app-timeline li > div {
  position: relative;
  display: grid;
  grid-template-columns: minmax(260px, 0.5fr) minmax(320px, 1fr);
  gap: 18px 28px;
  align-items: start;
}

.app-timeline h3 {
  margin: 0;
  color: #292721;
  font-size: 17px;
  line-height: 1.2;
}

.app-timeline p {
  margin: 0;
  max-width: 74ch;
  color: #403c33;
  font-size: 13px;
  line-height: 1.45;
}

.app-timeline small {
  display: block;
  grid-column: 2;
  margin-top: -8px;
  overflow-wrap: anywhere;
  color: #5c5548;
  font-size: 12px;
  line-height: 1.4;
}

.app-timeline em {
  grid-column: 2;
  margin-top: -8px;
  color: #686052;
  font-size: 12px;
  line-height: 1.45;
}

@media (max-width: 900px) {
  .timeline-progress,
  .key-events {
    grid-template-columns: 1fr;
  }

  .app-timeline li,
  .app-timeline li > div {
    grid-template-columns: 1fr;
  }

  .app-timeline li {
    padding: 18px 17px;
  }

  .app-timeline li > span {
    justify-self: start;
  }

  .app-timeline small,
  .app-timeline em {
    grid-column: 1;
    margin-top: 0;
  }
}

/* Minimal chronological keyline: separates signal from the detailed ledger. */
.timeline-summary {
  gap: 0;
}

.timeline-keyline {
  display: grid;
  grid-template-columns: 170px minmax(0, 1fr);
  gap: 0;
  padding: 0;
  border-top: 1px solid var(--line);
  background: rgba(255, 253, 247, 0.84);
}

.keyline-heading {
  padding: 18px 20px;
  border-right: 1px solid var(--line);
}

.keyline-heading h3 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 24px;
  line-height: 1;
}

.timeline-keyline ol {
  position: relative;
  display: grid;
  grid-template-columns: repeat(7, minmax(96px, 1fr));
  gap: 0;
  margin: 0;
  padding: 18px 18px 20px;
  list-style: none;
}

.timeline-keyline ol::before {
  position: absolute;
  top: 33px;
  right: calc((100% - 170px) / 14 + 18px);
  left: calc((100% - 170px) / 14 + 18px);
  height: 1px;
  background: rgba(47, 43, 35, 0.22);
  content: "";
}

.timeline-keyline li {
  position: relative;
  display: grid;
  align-content: start;
  justify-items: center;
  gap: 9px;
  min-width: 0;
  padding: 0 8px;
  text-align: center;
}

.timeline-keyline li span {
  z-index: 1;
  display: grid;
  width: 30px;
  height: 30px;
  place-items: center;
  border: 1px solid rgba(22, 141, 145, 0.34);
  border-radius: 999px;
  background: var(--paper-strong);
  color: var(--cyan);
  font-size: 10px;
  font-weight: 900;
}

.timeline-keyline li.is-complete span {
  border-color: rgba(47, 125, 87, 0.34);
  color: var(--clinical-green);
}

.timeline-keyline li.is-planned span,
.timeline-keyline li.is-active span {
  border-color: rgba(183, 121, 31, 0.42);
  color: var(--review-amber);
}

.timeline-keyline li strong {
  max-width: 14ch;
  color: #27241f;
  font-size: 12px;
  line-height: 1.2;
}

.timeline-keyline li small {
  color: #6a6255;
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

@media (max-width: 900px) {
  .timeline-keyline {
    grid-template-columns: 1fr;
  }

  .keyline-heading {
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }

  .timeline-keyline ol {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .timeline-keyline ol::before {
    top: 28px;
    bottom: 28px;
    left: 32px;
    width: 1px;
    height: auto;
  }

  .timeline-keyline li {
    grid-template-columns: 34px minmax(0, 1fr);
    justify-items: start;
    text-align: left;
  }

.timeline-keyline li small {
    grid-column: 2;
  }
}

/* Research-workspace pass: make the first screen decision-shaped. */
.evaluation-panel {
  border-top: 2px solid rgba(22, 141, 145, 0.44);
}

.evaluation-panel .body-lead {
  max-width: 82ch;
}

.compact-fields {
  display: grid;
  grid-template-columns: minmax(320px, 1fr) minmax(220px, 0.62fr) minmax(220px, 0.62fr);
  border-top: 1px solid var(--line);
}

.compact-fields section {
  min-width: 0;
  padding: 15px 17px 17px;
  border-right: 1px solid var(--line);
}

.compact-fields section:last-child {
  border-right: 0;
}

.compact-fields table {
  font-size: 12px;
}

.compact-fields th,
.compact-fields td {
  padding: 6px 7px;
}

.status-chip {
  width: fit-content;
  padding: 7px 9px;
  border: 1px solid rgba(183, 121, 31, 0.32);
  background: rgba(183, 121, 31, 0.1);
  color: var(--review-amber);
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.1em;
  line-height: 1;
  text-transform: uppercase;
}

.status-chip.is-complete {
  border-color: rgba(47, 125, 87, 0.28);
  background: rgba(47, 125, 87, 0.1);
  color: var(--clinical-green);
}

.action-panel .status-chip {
  grid-column: 1;
  justify-self: start;
}

.action-panel h3 {
  grid-column: 1;
}

.action-panel p {
  grid-column: 2;
  grid-row: 2 / span 2;
}

.action-panel button {
  grid-column: 3;
  grid-row: 2 / span 2;
}

.artifact-groups {
  display: grid;
  gap: 1px;
  padding: 0;
  background: var(--line);
}

.artifact-group {
  display: grid;
  grid-template-columns: 190px minmax(0, 1fr);
  background: rgba(255, 253, 247, 0.84);
}

.artifact-group h3 {
  margin: 0;
  padding: 16px 17px;
  border-right: 1px solid var(--line);
  color: #2d2a24;
  font-size: 14px;
  line-height: 1.2;
}

.artifact-group .shelf {
  min-width: 0;
}

.artifact-group .index-row {
  background: transparent;
}

@media (max-width: 900px) {
  .compact-fields,
  .artifact-group {
    grid-template-columns: 1fr;
  }

  .action-panel .status-chip,
  .action-panel h3,
  .action-panel p,
  .action-panel button {
    grid-column: auto;
    grid-row: auto;
  }

  .compact-fields section,
  .artifact-group h3 {
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }
}
"""


if __name__ == "__main__":
    raise SystemExit(main())
