from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class LLMResult:
    content: str
    model: str
    provider: str
    raw: dict[str, object] = field(default_factory=dict)


class LLMProvider(Protocol):
    provider_name: str
    model: str

    def chat_json(self, messages: list[ChatMessage], schema: dict[str, object]) -> LLMResult:
        ...


def load_dotenv_keys(path: str | Path = ".env") -> set[str]:
    """Load .env into the process without returning or printing secret values."""
    env_path = Path(path)
    keys: set[str] = set()
    if not env_path.exists():
        return keys
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)
        keys.add(key)
    return keys


class OpenAICompatibleProvider:
    """Provider for local OpenAI-compatible servers and OpenAI's chat endpoint."""

    provider_name = "openai-compatible"

    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str = "EMPTY",
        provider_name: str = "openai-compatible",
        timeout_seconds: int = 120,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.provider_name = provider_name
        self.timeout_seconds = timeout_seconds

    def chat_json(self, messages: list[ChatMessage], schema: dict[str, object]) -> LLMResult:
        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "seizure_frequency_extraction",
                "strict": True,
                "schema": schema,
            },
        }
        payload = {
            "model": self.model,
            "messages": [message.__dict__ for message in messages],
            "temperature": 0,
            "response_format": response_format,
        }
        response = _post_json(
            f"{self.base_url}/chat/completions",
            payload,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout_seconds=self.timeout_seconds,
        )
        content = response["choices"][0]["message"]["content"]  # type: ignore[index]
        return LLMResult(
            content=str(content),
            model=self.model,
            provider=self.provider_name,
            raw=response,
        )


class OllamaProvider:
    provider_name = "ollama"

    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434/api",
        timeout_seconds: int = 120,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def chat_json(self, messages: list[ChatMessage], schema: dict[str, object]) -> LLMResult:
        payload = {
            "model": self.model,
            "messages": [message.__dict__ for message in messages],
            "stream": False,
            "format": schema,
            "options": {"temperature": 0},
        }
        response = _post_json(
            f"{self.base_url}/chat",
            payload,
            headers={},
            timeout_seconds=self.timeout_seconds,
        )
        content = response["message"]["content"]  # type: ignore[index]
        return LLMResult(content=str(content), model=self.model, provider=self.provider_name, raw=response)


def local_lmstudio_provider(
    model: str,
    base_url: str = "http://localhost:1234/v1",
    timeout_seconds: int = 120,
) -> OpenAICompatibleProvider:
    return OpenAICompatibleProvider(
        base_url=base_url,
        model=model,
        provider_name="lmstudio",
        timeout_seconds=timeout_seconds,
    )


def local_vllm_provider(
    model: str,
    base_url: str = "http://localhost:8000/v1",
    timeout_seconds: int = 120,
) -> OpenAICompatibleProvider:
    return OpenAICompatibleProvider(
        base_url=base_url,
        model=model,
        provider_name="vllm",
        timeout_seconds=timeout_seconds,
    )


def local_ollama_provider(
    model: str,
    base_url: str = "http://localhost:11434/api",
    timeout_seconds: int = 120,
) -> OllamaProvider:
    return OllamaProvider(model=model, base_url=base_url, timeout_seconds=timeout_seconds)


def openai_provider(model: str) -> OpenAICompatibleProvider:
    load_dotenv_keys()
    api_key = os.environ.get("openai_api_key") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OpenAI API key is not configured in .env or environment.")
    return OpenAICompatibleProvider(
        base_url="https://api.openai.com/v1",
        model=model,
        api_key=api_key,
        provider_name="openai",
    )


def probe_openai_compatible(base_url: str, timeout_seconds: int = 2) -> dict[str, object]:
    try:
        response = _get_json(f"{base_url.rstrip('/')}/models", timeout_seconds=timeout_seconds)
        return {"ok": True, "response": response}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__}


def probe_ollama(base_url: str = "http://localhost:11434/api", timeout_seconds: int = 2) -> dict[str, object]:
    try:
        response = _get_json(f"{base_url.rstrip('/')}/tags", timeout_seconds=timeout_seconds)
        return {"ok": True, "response": response}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__}


def _post_json(
    url: str,
    payload: dict[str, object],
    headers: dict[str, str],
    timeout_seconds: int,
) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def _get_json(url: str, timeout_seconds: int) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"Content-Type": "application/json"}, method="GET")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))
