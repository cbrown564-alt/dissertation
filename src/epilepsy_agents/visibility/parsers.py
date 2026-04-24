"""Parse the project's markdown source docs into structured state."""
from __future__ import annotations

import html
import re
from pathlib import Path

from .state import Claim, Decision, SessionLog, Workstream


PROJECT_DOCS = {
    "current_state": Path("docs/current_state.md"),
    "milestones": Path("docs/milestones.md"),
    "active_threads": Path("docs/active_threads.md"),
    "decisions": Path("docs/decisions.md"),
    "artifact_registry": Path("docs/artifact_registry.md"),
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
        markdown = read_text(path)
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
        if (
            not line.startswith("|")
            or index + 1 >= len(lines)
            or not _is_table_separator(lines[index + 1])
        ):
            index += 1
            continue
        headers = _split_table_row(line)
        index += 2
        while index < len(lines) and lines[index].startswith("|"):
            cells = _split_table_row(lines[index])
            rows.append(
                {
                    header: _clean(cells[pos]) if pos < len(cells) else ""
                    for pos, header in enumerate(headers)
                }
            )
            index += 1
    return rows


def parse_last_updated(markdown: str) -> str:
    match = re.search(r"^Last updated:\s*(.+?)\.?\s*$", markdown, flags=re.MULTILINE)
    return match.group(1) if match else ""


def inline(text: str) -> str:
    """Render inline markdown (code, links) into an HTML-safe fragment."""
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_match, escaped)


def block(text: str) -> str:
    """Render block markdown (paragraphs, lists, tables) into HTML."""
    if not text:
        return "<p>Not recorded.</p>"
    lines = text.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline(' '.join(paragraph))}</p>")
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
            list_items.append(f"<li>{inline(stripped[2:])}</li>")
            index += 1
            continue
        flush_list()
        paragraph.append(stripped)
        index += 1

    flush_paragraph()
    flush_list()
    return "".join(output)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relative_doc_path(path: Path) -> str:
    parts = path.parts
    if "docs" in parts:
        return "/".join(parts[parts.index("docs") + 1 :])
    return path.name


def _clean(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text.strip())


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
            rows.append(
                {
                    header: _clean(cells[pos]) if pos < len(cells) else ""
                    for pos, header in enumerate(headers)
                }
            )
        return rows
    return []


def _heading_blocks(markdown: str, level: int) -> list[tuple[str, str]]:
    marker = "#" * level
    pattern = re.compile(
        rf"^{re.escape(marker)}\s+(.+?)\s*$\n(.*?)(?=^{re.escape(marker)}\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    return [
        (match.group(1).strip(), match.group(2).strip())
        for match in pattern.finditer(markdown)
    ]


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


def _starts_table(lines: list[str], index: int) -> bool:
    return (
        lines[index].strip().startswith("|")
        and index + 1 < len(lines)
        and _is_table_separator(lines[index + 1].strip())
    )


def _render_markdown_table(lines: list[str]) -> str:
    headers = _split_table_row(lines[0])
    body_rows = [_split_table_row(line) for line in lines[2:]]
    head = "".join(f"<th>{inline(header)}</th>" for header in headers)
    rows = []
    for row in body_rows:
        cells = "".join(f"<td>{inline(cell)}</td>" for cell in row)
        rows.append(f"<tr>{cells}</tr>")
    return (
        f"<table><thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _link_match(match: re.Match[str]) -> str:
    label = match.group(1)
    target = match.group(2)
    return f'<a href="{html.escape(target, quote=True)}">{label}</a>'
