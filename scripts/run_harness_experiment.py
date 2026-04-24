from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from epilepsy_agents.agents import MultiAgentPipeline, SinglePassBaseline
from epilepsy_agents.data import iter_records, load_synthetic_subset
from epilepsy_agents.metrics import EvaluationRow, evaluate_prediction, summarize
from epilepsy_agents.schema import Prediction

HARNESS_IDS = {
    "single": "h001_single_pass",
    "multi": "h002_multi_agent_verify",
}

MANIFEST_FIELDS = [
    "experiment_id",
    "timestamp_utc",
    "harness_id",
    "pipeline",
    "data_path",
    "data_sha256",
    "row_ok_only",
    "limit",
    "n",
    "exact_label_accuracy",
    "monthly_rate_accuracy_tolerance_15pct",
    "pragmatic_micro_f1",
    "purist_micro_f1",
    "run_record_path",
    "description",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run and record a harness experiment.")
    parser.add_argument("--harness", choices=sorted(HARNESS_IDS), default="multi")
    parser.add_argument("--data", default="synthetic_data_subset_1500.json")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--include-failed-rows", action="store_true")
    parser.add_argument("--experiment-id", default=None)
    parser.add_argument("--description", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--output-dir", default="project_state/runs")
    parser.add_argument("--manifest", default="project_state/experiments/manifest.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    timestamp = datetime.now(timezone.utc).replace(microsecond=0)
    experiment_id = args.experiment_id or make_experiment_id(timestamp, args.harness, args.limit)

    data_path = (ROOT / args.data).resolve() if not Path(args.data).is_absolute() else Path(args.data)
    output_dir = (ROOT / args.output_dir).resolve()
    manifest_path = (ROOT / args.manifest).resolve()

    records = load_synthetic_subset(data_path)
    pipeline = build_pipeline(args.harness)
    rows: list[EvaluationRow] = []
    error_categories: Counter[str] = Counter()
    prediction_counts: Counter[str] = Counter()

    for record in iter_records(records, args.limit, row_ok_only=not args.include_failed_rows):
        prediction = pipeline.predict(record.letter)
        row = evaluate_prediction(record.source_row_index, record.gold_label, prediction)
        rows.append(row)
        prediction_counts[prediction.label] += 1
        error_categories[categorize_error(row, prediction)] += 1

    summary = summarize(rows)
    run_record_path = output_dir / f"{experiment_id}.json"
    run_record = {
        "experiment_id": experiment_id,
        "timestamp_utc": timestamp.isoformat().replace("+00:00", "Z"),
        "harness_id": HARNESS_IDS[args.harness],
        "pipeline": args.harness,
        "description": args.description,
        "notes": args.notes,
        "data": {
            "path": str(data_path.relative_to(ROOT) if data_path.is_relative_to(ROOT) else data_path),
            "sha256": sha256_file(data_path),
            "row_ok_only": not args.include_failed_rows,
            "limit": args.limit,
        },
        "code": git_state(),
        "summary": summary,
        "error_categories": dict(sorted(error_categories.items())),
        "prediction_label_counts": dict(prediction_counts.most_common(25)),
        "rows": [safe_row(row) for row in rows],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    run_record_path.write_text(json.dumps(run_record, indent=2), encoding="utf-8")
    append_manifest(manifest_path, args, experiment_id, timestamp, data_path, run_record_path, summary)

    print(json.dumps({"experiment_id": experiment_id, "summary": summary}, indent=2))
    print(f"Wrote {run_record_path.relative_to(ROOT)}")
    return 0


def build_pipeline(name: str):
    return MultiAgentPipeline() if name == "multi" else SinglePassBaseline()


def make_experiment_id(timestamp: datetime, harness: str, limit: int | None) -> str:
    limit_text = "full" if limit is None else str(limit)
    return f"{timestamp.strftime('%Y%m%dT%H%M%SZ')}_{HARNESS_IDS[harness]}_n{limit_text}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_state() -> dict[str, Any]:
    return {
        "commit": run_git("rev-parse", "HEAD"),
        "dirty": bool(run_git("status", "--porcelain")),
    }


def run_git(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            capture_output=True,
            check=False,
            text=True,
            timeout=5,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def categorize_error(row: EvaluationRow, prediction: Prediction) -> str:
    gold = row.gold_label.lower()
    predicted = row.predicted_label.lower()
    if row.exact_match:
        return "correct"
    if not prediction.evidence and predicted not in {"unknown", "no seizure frequency reference"}:
        return "unsupported_or_empty_prediction"
    if "cluster" in gold or "cluster" in predicted:
        return "cluster_error"
    if "seizure free" in gold or "seizure free" in predicted:
        return "seizure_free_error"
    if (
        row.gold_pragmatic_class == "UNK"
        or row.predicted_pragmatic_class == "UNK"
        or gold == "unknown"
        or predicted == "unknown"
        or "no seizure frequency reference" in {gold, predicted}
    ):
        return "unknown_or_no_reference_error"
    if row.gold_pragmatic_class != row.predicted_pragmatic_class:
        return "class_confusion"
    if not row.monthly_rate_match:
        return "monthly_rate_mismatch"
    return "exact_label_mismatch"


def safe_row(row: EvaluationRow) -> dict[str, Any]:
    payload = asdict(row)
    return {
        "source_row_index": payload["source_row_index"],
        "gold_label": payload["gold_label"],
        "predicted_label": payload["predicted_label"],
        "exact_match": payload["exact_match"],
        "monthly_rate_match": payload["monthly_rate_match"],
        "gold_pragmatic_class": payload["gold_pragmatic_class"],
        "predicted_pragmatic_class": payload["predicted_pragmatic_class"],
        "gold_purist_class": payload["gold_purist_class"],
        "predicted_purist_class": payload["predicted_purist_class"],
        "confidence": payload["confidence"],
    }


def append_manifest(
    manifest_path: Path,
    args: argparse.Namespace,
    experiment_id: str,
    timestamp: datetime,
    data_path: Path,
    run_record_path: Path,
    summary: dict[str, Any],
) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    needs_header = not manifest_path.exists() or manifest_path.stat().st_size == 0
    row = {
        "experiment_id": experiment_id,
        "timestamp_utc": timestamp.isoformat().replace("+00:00", "Z"),
        "harness_id": HARNESS_IDS[args.harness],
        "pipeline": args.harness,
        "data_path": str(data_path.relative_to(ROOT) if data_path.is_relative_to(ROOT) else data_path),
        "data_sha256": sha256_file(data_path),
        "row_ok_only": str(not args.include_failed_rows).lower(),
        "limit": "" if args.limit is None else args.limit,
        "n": summary["n"],
        "exact_label_accuracy": summary["exact_label_accuracy"],
        "monthly_rate_accuracy_tolerance_15pct": summary["monthly_rate_accuracy_tolerance_15pct"],
        "pragmatic_micro_f1": summary["pragmatic"]["micro_f1"],
        "purist_micro_f1": summary["purist"]["micro_f1"],
        "run_record_path": run_record_path.relative_to(ROOT).as_posix(),
        "description": args.description,
    }
    with manifest_path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    raise SystemExit(main())
