from __future__ import annotations

import importlib.util
import json
import os
import platform
import subprocess
import urllib.request
from pathlib import Path


MODELS = [
    {
        "id": "microsoft/Phi-4-mini-instruct",
        "params_b": 3.8,
        "target_quant": "Q5_K_M or Q6_K",
        "fit": "comfortable",
        "notes": "Small reasoning model; supports tool-enabled function-calling format.",
    },
    {
        "id": "google/gemma-3-4b-it",
        "params_b": 4.0,
        "target_quant": "Q4_K_M or Q5_K_M",
        "fit": "comfortable",
        "notes": "Long-context 4B text/image model; good small-model baseline if license is acceptable.",
    },
    {
        "id": "Qwen/Qwen2.5-7B-Instruct",
        "params_b": 7.6,
        "target_quant": "Q4_K_M",
        "fit": "comfortable",
        "notes": "Strong JSON/structured-output baseline; likely best first local extractor.",
    },
    {
        "id": "Qwen/Qwen3-8B",
        "params_b": 8.0,
        "target_quant": "Q4_K_M",
        "fit": "comfortable-to-borderline",
        "notes": "Stronger reasoning/agentic model; test no-thinking mode for extraction speed.",
    },
    {
        "id": "mistralai/Ministral-8B-Instruct-2410",
        "params_b": 8.0,
        "target_quant": "Q4_K_M",
        "fit": "comfortable-to-borderline",
        "notes": "Function-calling capable, but Mistral Research License limits commercial use.",
    },
    {
        "id": "meta-llama/Llama-3.1-8B-Instruct",
        "params_b": 8.0,
        "target_quant": "Q4_K_M",
        "fit": "comfortable-to-borderline",
        "notes": "Good general baseline; gated model and custom community license.",
    },
    {
        "id": "google/gemma-3-12b-it",
        "params_b": 12.0,
        "target_quant": "Q3_K_M or Q4_K_M with offload",
        "fit": "borderline",
        "notes": "May be useful as an accuracy ceiling on this laptop, but expect slower runs.",
    },
    {
        "id": "Qwen/Qwen3-14B",
        "params_b": 14.8,
        "target_quant": "Q3_K_M or Q4_K_M with CPU offload",
        "fit": "borderline",
        "notes": "Probably too tight for routine 8GB VRAM experiments; still worth a small feasibility test.",
    },
]


def main() -> int:
    report = {
        "python": {
            "version": platform.python_version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
        },
        "gpu": nvidia_smi(),
        "env_keys_present": sorted(load_env_keys()),
        "python_packages": package_presence(
            ["torch", "transformers", "llama_cpp", "ctransformers", "openai", "anthropic", "google", "pydantic"]
        ),
        "local_servers": {
            "ollama": probe_url("http://localhost:11434/api/tags"),
            "lmstudio": probe_url("http://localhost:1234/v1/models"),
            "vllm_or_llamacpp": probe_url("http://localhost:8000/v1/models"),
        },
        "candidate_models": MODELS,
    }
    print(json.dumps(report, indent=2))
    return 0


def nvidia_smi() -> dict[str, object]:
    command = [
        "nvidia-smi",
        "--query-gpu=name,memory.total,memory.free,driver_version",
        "--format=csv,noheader",
    ]
    try:
        output = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__}
    parts = [part.strip() for part in output.split(",")]
    if len(parts) < 4:
        return {"ok": True, "raw": output}
    return {
        "ok": True,
        "name": parts[0],
        "memory_total": parts[1],
        "memory_free": parts[2],
        "driver_version": parts[3],
    }


def load_env_keys(path: str = ".env") -> set[str]:
    env_path = Path(path)
    keys: set[str] = set()
    if not env_path.exists():
        return keys
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#") and "=" in line:
            keys.add(line.split("=", 1)[0].strip())
    return keys


def package_presence(names: list[str]) -> dict[str, bool]:
    output = {}
    for name in names:
        try:
            output[name] = bool(importlib.util.find_spec(name))
        except ModuleNotFoundError:
            output[name] = False
    return output


def probe_url(url: str) -> dict[str, object]:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return {"ok": True, "status": response.status}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__}


if __name__ == "__main__":
    raise SystemExit(main())
