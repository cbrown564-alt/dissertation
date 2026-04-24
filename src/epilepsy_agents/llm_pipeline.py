from __future__ import annotations

import json
import time
from typing import Any

from .labels import parse_label
from .providers import (
    ChatMessage,
    LLMProvider,
    local_lmstudio_provider,
    local_ollama_provider,
    local_vllm_provider,
    openai_provider,
)
from .schema import EvidenceSpan, Prediction
from .structured_schema import EXTRACTION_JSON_SCHEMA, system_prompt


class SinglePromptLLMPipeline:
    """Single-prompt LLM baseline used for the first Phase A smoke runs."""

    def __init__(self, provider: LLMProvider, max_retries: int = 1) -> None:
        self.provider = provider
        self.max_retries = max_retries

    def predict(self, letter: str) -> Prediction:
        warnings: list[str] = []
        last_error: str | None = None

        for attempt in range(1, self.max_retries + 2):
            started = time.perf_counter()
            try:
                result = self.provider.chat_json(self._messages(letter), EXTRACTION_JSON_SCHEMA)
                latency_ms = round((time.perf_counter() - started) * 1000, 1)
                prediction = self._prediction_from_result(result.content)
                metadata = {
                    "provider": result.provider,
                    "model": result.model,
                    "latency_ms": latency_ms,
                    "attempt": attempt,
                    "invalid_output": False,
                    **_usage_metadata(result.raw),
                }
                return Prediction(
                    label=prediction.label,
                    evidence=prediction.evidence,
                    confidence=prediction.confidence,
                    analysis=prediction.analysis,
                    parsed_monthly_rate=prediction.parsed_monthly_rate,
                    pragmatic_class=prediction.pragmatic_class,
                    purist_class=prediction.purist_class,
                    warnings=warnings + prediction.warnings,
                    metadata=metadata,
                )
            except Exception as exc:
                last_error = type(exc).__name__
                warnings.append(f"attempt_{attempt}_{type(exc).__name__.lower()}")

        parsed = parse_label("unknown")
        return Prediction(
            label="unknown",
            evidence=[],
            confidence=0.0,
            analysis="The LLM pipeline failed to return a valid schema-conformant response.",
            parsed_monthly_rate=parsed.monthly_rate,
            pragmatic_class=parsed.pragmatic_class,
            purist_class=parsed.purist_class,
            warnings=warnings + ["invalid_output"],
            metadata={
                "provider": getattr(self.provider, "provider_name", "unknown"),
                "model": getattr(self.provider, "model", "unknown"),
                "latency_ms": None,
                "attempt": self.max_retries + 1,
                "invalid_output": True,
                "error_type": last_error,
            },
        )

    def _messages(self, letter: str) -> list[ChatMessage]:
        return [
            ChatMessage(role="system", content=system_prompt()),
            ChatMessage(
                role="user",
                content=(
                    "Extract the current seizure-frequency label from this synthetic epilepsy clinic letter. "
                    "Return only JSON matching the provided schema.\n\n"
                    f"Letter:\n{letter}"
                ),
            ),
        ]

    def _prediction_from_result(self, content: str) -> Prediction:
        payload = json.loads(content)
        label = str(payload["label"]).strip()
        parsed = parse_label(label)
        evidence = [
            EvidenceSpan(
                text=str(item["text"]),
                start=item.get("start"),
                end=item.get("end"),
                source=str(item.get("source", "letter")),
            )
            for item in payload.get("evidence", [])
            if str(item.get("text", "")).strip()
        ]
        warnings = [str(item) for item in payload.get("warnings", [])]
        return Prediction(
            label=label,
            evidence=evidence,
            confidence=float(payload.get("confidence", 0.0)),
            analysis=str(payload.get("analysis", "")),
            parsed_monthly_rate=parsed.monthly_rate,
            pragmatic_class=parsed.pragmatic_class,
            purist_class=parsed.purist_class,
            warnings=warnings,
        )


def create_provider(name: str, model: str, base_url: str | None = None, timeout_seconds: int = 120) -> LLMProvider:
    if name == "lmstudio":
        return local_lmstudio_provider(
            model=model,
            base_url=base_url or "http://localhost:1234/v1",
            timeout_seconds=timeout_seconds,
        )
    if name == "vllm":
        return local_vllm_provider(
            model=model,
            base_url=base_url or "http://localhost:8000/v1",
            timeout_seconds=timeout_seconds,
        )
    if name == "ollama":
        return local_ollama_provider(
            model=model,
            base_url=base_url or "http://localhost:11434/api",
            timeout_seconds=timeout_seconds,
        )
    if name == "openai":
        return openai_provider(model=model)
    raise ValueError(f"Unsupported provider: {name}")


def _usage_metadata(raw: dict[str, Any]) -> dict[str, Any]:
    prompt_tokens = raw.get("prompt_eval_count") or raw.get("usage", {}).get("prompt_tokens")
    completion_tokens = raw.get("eval_count") or raw.get("usage", {}).get("completion_tokens")
    total_tokens = raw.get("usage", {}).get("total_tokens")
    if total_tokens is None and prompt_tokens is not None and completion_tokens is not None:
        total_tokens = prompt_tokens + completion_tokens

    metadata: dict[str, Any] = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }
    for key in ("total_duration", "load_duration", "prompt_eval_duration", "eval_duration"):
        if key in raw:
            metadata[key] = raw[key]
    return metadata
