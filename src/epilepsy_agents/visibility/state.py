"""Dataclasses representing parsed project state."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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
