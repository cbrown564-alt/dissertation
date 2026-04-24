from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

from .agents import MultiAgentPipeline, SinglePassBaseline
from .data import iter_records, load_synthetic_subset
from .metrics import evaluate_prediction, summarize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate seizure-frequency extraction agents.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Evaluate on the synthetic JSON subset.")
    evaluate.add_argument("--data", default="synthetic_data_subset_1500.json")
    evaluate.add_argument("--limit", type=int, default=None)
    evaluate.add_argument("--include-failed-rows", action="store_true")
    evaluate.add_argument("--pipeline", choices=["multi", "single"], default="multi")
    evaluate.add_argument("--out", default=None, help="Optional JSON output path.")
    evaluate.add_argument("--csv", default=None, help="Optional per-row CSV output path.")

    predict = subparsers.add_parser("predict", help="Predict one letter from a text file.")
    predict.add_argument("path")
    predict.add_argument("--pipeline", choices=["multi", "single"], default="multi")

    notebook = subparsers.add_parser("notebook", help="Build the local Evidence Notebook dashboard.")
    notebook.add_argument("--out", default="docs/evidence_notebook.html")
    notebook.add_argument("--session-limit", type=int, default=6)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "evaluate":
        return evaluate(args)
    if args.command == "predict":
        return predict(args)
    if args.command == "notebook":
        return notebook(args)
    raise ValueError(args.command)


def _pipeline(name: str):
    return MultiAgentPipeline() if name == "multi" else SinglePassBaseline()


def evaluate(args: argparse.Namespace) -> int:
    records = load_synthetic_subset(args.data)
    pipeline = _pipeline(args.pipeline)
    rows = []
    examples = []
    for record in iter_records(records, args.limit, row_ok_only=not args.include_failed_rows):
        prediction = pipeline.predict(record.letter)
        row = evaluate_prediction(record.source_row_index, record.gold_label, prediction)
        rows.append(row)
        if len(examples) < 10 and not row.monthly_rate_match:
            examples.append(
                {
                    "source_row_index": record.source_row_index,
                    "gold_label": record.gold_label,
                    "predicted_label": prediction.label,
                    "gold_evidence": record.gold_evidence,
                    "predicted_evidence": [span.text for span in prediction.evidence],
                    "analysis": prediction.analysis,
                }
            )

    summary = summarize(rows)
    payload = {
        "pipeline": args.pipeline,
        "data": args.data,
        "summary": summary,
        "error_examples": examples,
    }
    print(json.dumps(payload["summary"], indent=2))
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if args.csv:
        Path(args.csv).parent.mkdir(parents=True, exist_ok=True)
        with Path(args.csv).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0]).keys()) if rows else [])
            if rows:
                writer.writeheader()
                for row in rows:
                    writer.writerow(asdict(row))
    return 0


def predict(args: argparse.Namespace) -> int:
    letter = Path(args.path).read_text(encoding="utf-8")
    prediction = _pipeline(args.pipeline).predict(letter)
    print(json.dumps(asdict(prediction), indent=2))
    return 0


def notebook(args: argparse.Namespace) -> int:
    from .visibility import build_dashboard

    out = Path(args.out)
    html_text = build_dashboard(Path("."), session_limit=args.session_limit)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
