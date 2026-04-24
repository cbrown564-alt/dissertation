from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

from .agents import MultiAgentPipeline, SinglePassBaseline
from .data import iter_records, load_synthetic_subset
from .metrics import evaluate_prediction, summarize
from .providers import (
    ChatMessage,
    local_lmstudio_provider,
    local_ollama_provider,
    local_vllm_provider,
    probe_ollama,
    probe_openai_compatible,
)


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

    notebook = subparsers.add_parser("notebook", help="Regenerate the Evidence Notebook site payload.")
    notebook.add_argument("--site-dir", default="site", help="Deployable site root; data.js is written to its assets/ subdirectory.")
    notebook.add_argument("--session-limit", type=int, default=6)

    provider_smoke = subparsers.add_parser(
        "provider-smoke",
        help="Probe a local LLM runtime and optionally run one JSON-schema smoke request.",
    )
    provider_smoke.add_argument("--provider", choices=["lmstudio", "vllm", "ollama"], required=True)
    provider_smoke.add_argument("--model", required=True)
    provider_smoke.add_argument("--base-url", default=None)
    provider_smoke.add_argument("--timeout-seconds", type=int, default=10)
    provider_smoke.add_argument("--skip-chat", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "evaluate":
        return evaluate(args)
    if args.command == "predict":
        return predict(args)
    if args.command == "notebook":
        return notebook(args)
    if args.command == "provider-smoke":
        return provider_smoke(args)
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
    from .visibility import write_site

    site_dir = Path(args.site_dir)
    data_js = write_site(Path("."), site_dir=site_dir, session_limit=args.session_limit)
    print(f"Wrote {data_js}")
    return 0


def provider_smoke(args: argparse.Namespace) -> int:
    probe = _probe_provider(args.provider, args.base_url, args.timeout_seconds)
    payload: dict[str, object] = {
        "provider": args.provider,
        "model": args.model,
        "base_url": args.base_url or _default_base_url(args.provider),
        "probe": probe,
    }
    if not probe.get("ok"):
        print(json.dumps(payload, indent=2))
        return 1
    if args.skip_chat:
        print(json.dumps(payload, indent=2))
        return 0

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "status": {"type": "string"},
            "label": {"type": "string"},
        },
        "required": ["status", "label"],
    }
    messages = [
        ChatMessage(
            role="system",
            content=(
                "Return only JSON matching the supplied schema. "
                "Use label 'smoke_ok' for this connectivity test."
            ),
        ),
        ChatMessage(role="user", content="Confirm the local extraction runtime is reachable."),
    ]
    result = _provider_instance(
        args.provider,
        args.model,
        args.base_url,
        args.timeout_seconds,
    ).chat_json(messages, schema)
    payload["chat_result"] = {
        "provider": result.provider,
        "model": result.model,
        "content": result.content,
    }
    print(json.dumps(payload, indent=2))
    return 0


def _default_base_url(provider: str) -> str:
    if provider == "lmstudio":
        return "http://localhost:1234/v1"
    if provider == "vllm":
        return "http://localhost:8000/v1"
    return "http://localhost:11434/api"


def _probe_provider(provider: str, base_url: str | None, timeout_seconds: int) -> dict[str, object]:
    resolved_base_url = base_url or _default_base_url(provider)
    if provider == "ollama":
        return probe_ollama(resolved_base_url, timeout_seconds=timeout_seconds)
    return probe_openai_compatible(resolved_base_url, timeout_seconds=timeout_seconds)


def _provider_instance(provider: str, model: str, base_url: str | None, timeout_seconds: int):
    resolved_base_url = base_url or _default_base_url(provider)
    if provider == "lmstudio":
        return local_lmstudio_provider(model=model, base_url=resolved_base_url, timeout_seconds=timeout_seconds)
    if provider == "vllm":
        return local_vllm_provider(model=model, base_url=resolved_base_url, timeout_seconds=timeout_seconds)
    return local_ollama_provider(model=model, base_url=resolved_base_url, timeout_seconds=timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
