from __future__ import annotations

import re
from dataclasses import dataclass

from .labels import parse_label
from .schema import EvidenceSpan, Prediction

FREQUENCY_TERMS = re.compile(
    r"\b(seizure|seizures|event|events|episode|episodes|absence|absences|cluster|clusters|fit|fits|"
    r"tonic-clonic|convulsion|convulsions|frequency|seizure-free|seizure free)\b",
    re.IGNORECASE,
)

NUMBER_WORDS = {
    "one": "1",
    "two": "2",
    "twice": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "several": "multiple",
    "multiple": "multiple",
}


def _clean_evidence(text: str) -> str:
    return " ".join(text.strip().strip("-:;,.").split())


def _num(text: str) -> str:
    return NUMBER_WORDS.get(text.lower(), text)


def _singular_unit(unit: str) -> str:
    return unit.lower().rstrip("s")


@dataclass(frozen=True)
class SectionTimeline:
    candidates: list[EvidenceSpan]
    sections: dict[str, str]


class SectionTimelineAgent:
    """Segments a letter and keeps seizure-relevant evidence candidates."""

    def run(self, letter: str) -> SectionTimeline:
        sections: dict[str, list[str]] = {}
        current = "body"
        for raw_line in letter.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.endswith(":") and len(line) <= 60:
                current = line[:-1].strip().lower()
                sections.setdefault(current, [])
            else:
                sections.setdefault(current, []).append(line)

        candidates: list[EvidenceSpan] = []
        sentence_pattern = re.compile(r"[^.!?\n]+(?:[.!?]|\n|$)")
        for match in sentence_pattern.finditer(letter):
            sentence = _clean_evidence(match.group(0))
            if sentence and FREQUENCY_TERMS.search(sentence):
                candidates.append(EvidenceSpan(sentence, match.start(), match.end()))

        for heading, lines in sections.items():
            if "seizure frequency" in heading:
                text = _clean_evidence(" ".join(lines[:2]))
                if text:
                    candidates.insert(0, EvidenceSpan(text, source=f"section:{heading}"))

        compact_sections = {key: " ".join(value) for key, value in sections.items()}
        return SectionTimeline(candidates=candidates, sections=compact_sections)


class FieldExtractorAgent:
    """A deterministic extractor used as the offline baseline agent."""

    def run(self, timeline: SectionTimeline) -> list[Prediction]:
        predictions: list[Prediction] = []
        for candidate in timeline.candidates:
            text = candidate.text
            extracted = self._extract_from_text(text)
            if extracted:
                label, reason = extracted
                parsed = parse_label(label)
                predictions.append(
                    Prediction(
                        label=label,
                        evidence=[candidate],
                        confidence=0.62,
                        analysis=reason,
                        parsed_monthly_rate=parsed.monthly_rate,
                        pragmatic_class=parsed.pragmatic_class,
                        purist_class=parsed.purist_class,
                    )
                )
        return predictions

    def _extract_from_text(self, text: str) -> tuple[str, str] | None:
        lower = (
            text.lower()
            .replace("≤", "")
            .replace("≥", "")
            .replace("≈", "")
            .replace("approximately", "")
            .replace("around", "")
        )
        count = (
            r"(?:\d+(?:\.\d+)?|one|two|twice|three|four|five|six|seven|eight|nine|ten|"
            r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|several|multiple)"
        )
        unit = r"(?:day|days|week|weeks|month|months|year|years)"

        no_ref = [
            "unable to quantify",
            "cannot quantify",
            "unclear frequency",
            "frequency is unclear",
            "unknown frequency",
        ]
        if any(phrase in lower for phrase in no_ref):
            return "unknown", "The candidate explicitly states that frequency cannot be quantified."

        if (
            re.search(r"\b(no|denies|without)\s+(further\s+)?(seizures|events|fits)\b", lower)
            and "at the wheel" not in lower
            and "before" not in lower
            and "after" not in lower
        ):
            return "seizure free for multiple month", "The candidate states there have been no further seizures."

        seizure_free = re.search(
            rf"seizure[- ]free\s+for\s+(?P<value>{count}(?:\s+(?:to|-)\s+{count})?)\s+(?P<unit>{unit})",
            lower,
        )
        if seizure_free and "before" not in lower and "then" not in lower:
            value = _num(seizure_free.group("value"))
            return (
                f"seizure free for {value} {_singular_unit(seizure_free.group('unit'))}",
                "The candidate contains an explicit seizure-free duration.",
            )

        cluster = re.search(
            rf"cluster\s+(?:days?\s+)?(?P<clusters>{count})\s+(?:this|per|a|each|every|last)\s+"
            rf"(?P<period>{unit}).{{0,80}}?(?P<count>{count})\s+(?:seizures?|events?|episodes?|fits?)\s+"
            rf"(?:in|per|during|within)\s+(?:24\s*h|cluster|day)",
            lower,
        )
        if cluster:
            clusters = _num(cluster.group("clusters"))
            per_cluster = _num(cluster.group("count"))
            unit_text = _singular_unit(cluster.group("period"))
            return (
                f"{clusters} cluster per {unit_text}, {per_cluster} per cluster",
                "The candidate describes cluster frequency and within-cluster seizure count.",
            )

        over_window = re.search(
            rf"(?P<count>{count})\s+(?:events?|seizures?|episodes?|absences|fits)\s+"
            rf"(?:over|in|during|across)\s+(?:the\s+)?(?:last|past|previous)?\s*"
            rf"(?P<period>{count})\s+(?P<unit>{unit})",
            lower,
        )
        if over_window:
            seizure_count = _num(over_window.group("count"))
            period = _num(over_window.group("period"))
            return (
                f"{seizure_count} per {period} {_singular_unit(over_window.group('unit'))}",
                "The candidate gives a count over a defined retrospective window.",
            )

        window_first = re.search(
            rf"(?:over|in|during|across)\s+(?:the\s+)?(?:last|past|previous)?\s*"
            rf"(?P<period>{count})\s+(?P<unit>{unit}).{{0,80}}?\b(?:were|was|had|reports?|recorded)\s+"
            rf"(?P<count>{count})\s+(?:\w+\s+){{0,4}}?(?:seizures?|events?|episodes?|absences|fits)",
            lower,
        )
        if window_first:
            seizure_count = _num(window_first.group("count"))
            period = _num(window_first.group("period"))
            return (
                f"{seizure_count} per {period} {_singular_unit(window_first.group('unit'))}",
                "The candidate gives a count over a defined retrospective window.",
            )

        interval = re.search(
            rf"(?:inter-seizure interval|clusters?\s+every|seizures?\s+every|events?\s+every)\s+"
            rf"(?P<period>{count})\s+(?P<unit>{unit})",
            lower,
        )
        if interval:
            period = _num(interval.group("period"))
            return (
                f"1 per {period} {_singular_unit(interval.group('unit'))}",
                "The candidate gives an event interval, normalised as one event per interval.",
            )

        direct = re.search(
            rf"(?P<count>{count}(?:\s+(?:to|-)\s+{count})?)\s+"
            rf"(?:times\s+)?(?:\w+\s+){{0,5}}?(?:seizures?|events?|episodes?|absences|fits)?\s*"
            rf"(?:per|a|each|every)\s+"
            rf"(?P<period>{count}\s+)?(?P<unit>{unit})",
            lower,
        )
        if direct:
            count_text = _num(direct.group("count"))
            period_text = (direct.group("period") or "1 ").strip()
            period_text = _num(period_text)
            if period_text == "1":
                return (
                    f"{count_text} per {_singular_unit(direct.group('unit'))}",
                    "The candidate contains a direct frequency expression.",
                )
            return (
                f"{count_text} per {period_text} {_singular_unit(direct.group('unit'))}",
                "The candidate contains a direct frequency expression.",
            )

        present = re.search(r"present seizure frequency\s*:?\s*(?P<phrase>.+)", lower)
        if present:
            phrase = present.group("phrase")
            return self._extract_from_text(phrase)

        return None


class VerificationAgent:
    """Checks support and resolves ambiguous or unsupported extraction candidates."""

    def run(self, predictions: list[Prediction], timeline: SectionTimeline) -> Prediction:
        if not predictions:
            label = "no seizure frequency reference"
            parsed = parse_label(label)
            return Prediction(
                label=label,
                evidence=[],
                confidence=0.25,
                analysis="No seizure-frequency candidate with a parseable value was found.",
                parsed_monthly_rate=parsed.monthly_rate,
                pragmatic_class=parsed.pragmatic_class,
                purist_class=parsed.purist_class,
                warnings=["no_supported_candidate"],
            )

        scored = sorted(predictions, key=self._score, reverse=True)
        best = scored[0]
        evidence_text = best.evidence[0].text.lower() if best.evidence else ""
        confidence = best.confidence
        warnings = list(best.warnings)
        if "present seizure frequency" in evidence_text:
            confidence += 0.18
        if any(word in evidence_text for word in ["over", "per", "seizure free", "cluster"]):
            confidence += 0.1
        if len(scored) > 1 and scored[1].label != best.label:
            warnings.append("competing_candidate")
            confidence -= 0.08

        return Prediction(
            label=best.label,
            evidence=best.evidence,
            confidence=max(0.0, min(confidence, 0.95)),
            analysis=best.analysis,
            parsed_monthly_rate=best.parsed_monthly_rate,
            pragmatic_class=best.pragmatic_class,
            purist_class=best.purist_class,
            warnings=warnings,
            metadata={"candidate_count": len(predictions)},
        )

    def _score(self, prediction: Prediction) -> tuple[float, int]:
        evidence = prediction.evidence[0].text.lower() if prediction.evidence else ""
        priority = 0
        if "present seizure frequency" in evidence:
            priority += 4
        if "over" in evidence or "per" in evidence:
            priority += 2
        if "cluster" in evidence:
            priority += 1
        if prediction.label.startswith("seizure free for multiple"):
            priority -= 3
        return (prediction.confidence, priority)


class MultiAgentPipeline:
    def __init__(self) -> None:
        self.timeline_agent = SectionTimelineAgent()
        self.extractor_agent = FieldExtractorAgent()
        self.verification_agent = VerificationAgent()

    def predict(self, letter: str) -> Prediction:
        timeline = self.timeline_agent.run(letter)
        candidates = self.extractor_agent.run(timeline)
        prediction = self.verification_agent.run(candidates, timeline)
        return prediction


class SinglePassBaseline:
    """Simpler baseline: scan the whole letter and return the first parseable pattern."""

    def __init__(self) -> None:
        self.extractor = FieldExtractorAgent()

    def predict(self, letter: str) -> Prediction:
        timeline = SectionTimeline(candidates=[EvidenceSpan(_clean_evidence(letter[:3000]))], sections={})
        predictions = self.extractor.run(timeline)
        if predictions:
            return predictions[0]
        parsed = parse_label("no seizure frequency reference")
        return Prediction(
            label="no seizure frequency reference",
            evidence=[],
            confidence=0.2,
            analysis="Single-pass baseline found no parseable expression.",
            parsed_monthly_rate=parsed.monthly_rate,
            pragmatic_class=parsed.pragmatic_class,
            purist_class=parsed.purist_class,
            warnings=["no_supported_candidate"],
        )
