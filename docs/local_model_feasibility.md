# Local Model Feasibility and Architecture

Date: 2026-04-24.

## Local Hardware Probe

Observed from the current laptop:

- GPU: NVIDIA GeForce RTX 4070 Laptop GPU.
- VRAM: 8,188 MiB total, 7,948 MiB free at probe time.
- Driver: NVIDIA 581.95; `nvidia-smi` reports CUDA 13.0 support.
- CPU: 22 logical threads reported by Python.
- Disk: about 478 GB free on `C:`.
- `.env` contains keys for OpenAI, Anthropic, Gemini, and Hugging Face. Values were not printed or copied.

Current local inference status:

- Ollama is installed locally and its API is responding at `http://localhost:11434/api/tags`.
- Visible local Ollama models include `qwen3.5:4b`, `qwen3.5:9b`, `qwen3.5:35b-a3b`, and `llama3.1:latest`.
- The repository now has a `provider-smoke` CLI path that successfully round-trips schema-constrained JSON through the local Ollama adapter.
- LM Studio command is still not on disk at the probed Windows paths and `http://localhost:1234/v1/models` is not responding.
- vLLM/llama.cpp-style server at `http://localhost:8000/v1/models` is not responding.
- Python packages for direct inference are not installed in the active environment: `torch`, `transformers`, `llama_cpp`, `ctransformers`.

Conclusion: this machine now has a working local runtime through Ollama. The active problem is no longer installation but achieving acceptable validity and latency for `h003_single_prompt_llm`.

## Practical Model Tiers for 8 GB VRAM

The clinically relevant target is not "largest possible model"; it is reliable structured extraction with acceptable latency and no patient text leaving the hospital environment.

### Tier 1: First Local Test Set

These should be tried first because they are likely to run fully or mostly on the 8 GB GPU in 4-bit or 5-bit GGUF quantization.

| Model | Why test it | Expected fit |
| --- | --- | --- |
| `Qwen/Qwen2.5-7B-Instruct` | Strong structured/JSON-output reputation, long-context support, Apache 2.0 license. | Comfortable at Q4_K_M. |
| `Qwen/Qwen3-8B` | Newer Qwen model with stronger reasoning and agentic/tool-use focus. Test `/no_think` for extraction. | Comfortable to borderline at Q4_K_M. |
| `microsoft/Phi-4-mini-instruct` | 3.8B, MIT license, long context, explicitly documents tool-enabled function calling. | Comfortable at Q5/Q6. |
| `google/gemma-3-4b-it` | Strong 4B baseline with 128K context, useful for speed and long letters if Gemma terms are acceptable. | Comfortable at Q4/Q5. |

### Tier 2: Stretch Local Models

These may fit only with heavier quantization, reduced context, CPU offload, or slow throughput.

| Model | Why test it | Expected fit |
| --- | --- | --- |
| `mistralai/Ministral-8B-Instruct-2410` | Function-calling capable and designed for edge/local use. | Comfortable to borderline at Q4_K_M; license limits commercial use. |
| `meta-llama/Llama-3.1-8B-Instruct` | Widely used general baseline, 128K context. | Comfortable to borderline at Q4_K_M; gated/custom license. |
| `google/gemma-3-12b-it` | Stronger reasoning and long context. | Borderline at Q3/Q4 with offload. |
| `Qwen/Qwen3-14B` | Stronger agentic/reasoning model than 8B. | Borderline; likely too slow for routine experiments on this laptop. |

### Tier 3: Not Suitable on This Laptop

- `openai/gpt-oss-20b`: attractive open-weight model, but OpenAI's own release says the 20B model targets edge devices with 16 GB memory. This laptop has 8 GB VRAM, so it is not a first-pass local candidate unless using CPU/offload experiments.
- 27B, 32B, 70B, 120B models: not appropriate for routine local testing here.

## Recommended Runtime

### Best Development Path: LM Studio or Ollama

Use one local server interface, not direct `transformers`, for the first research prototype.

Recommended order:

1. LM Studio: easiest Windows workflow, OpenAI-compatible API, supports structured output via JSON schema, supports tool use, and uses llama.cpp for GGUF models.
2. Ollama: very simple model management and structured outputs via JSON schema, also exposes an OpenAI-compatible API.
3. llama.cpp server: best low-level reproducibility once model files and flags are locked.
4. vLLM: excellent for servers, structured outputs, and tool calling, but likely too heavy for this 8 GB laptop except for small models.

## Architecture To Build

The extraction framework should separate orchestration from model runtime:

```text
Evaluation harness
  -> Pipeline runner
    -> Agent prompts
      -> Provider adapter
        -> Local server first: LM Studio / Ollama / llama.cpp / vLLM
        -> Closed providers only for synthetic-data comparison
    -> JSON schema validation
    -> Label normalization
    -> Metrics
```

### Provider Requirements

Each provider must support:

- chat messages;
- deterministic decoding (`temperature = 0`);
- schema-constrained JSON output where possible;
- timeout/retry handling;
- logging of model id, prompt version, token/cost metadata when available;
- no raw real clinical text in persistent logs.

### Tool Calling

For this project, "tool calling" should be treated narrowly:

- `normalize_label(label)` to calculate monthly rate and category;
- `validate_schema(output)` to reject malformed extraction;
- `retrieve_candidate_spans(letter)` for section/timeline support;
- `compare_candidates(candidates)` for verification.

The LLM does not need arbitrary tools for the clinical pipeline. We should prefer constrained extraction outputs plus deterministic local tools.

## Closed Provider Comparison

Closed providers are appropriate for synthetic-data experiments only. The `.env` file includes keys for:

- OpenAI;
- Anthropic;
- Gemini.

The implementation should produce comparable records for all providers but mark them as `synthetic_only`. They should not be configured as valid providers for real KCH letters unless governance explicitly permits that.

## Immediate Next Experiments

1. Keep Ollama as the active local runtime for Phase A.
2. Use `qwen3.5:4b` as the first tuning target and compare against `qwen3.5:9b` if validity remains poor.
3. Rerun `h003_single_prompt_llm` on a 25-letter slice after prompt/schema tightening.
4. Measure:
   - valid JSON rate;
   - exact label accuracy;
   - pragmatic/purist F1;
   - evidence support;
   - tokens/sec or wall-clock seconds per letter;
   - VRAM use during generation.
5. Keep the best two local models for fuller synthetic evaluation.

## Current Code Support

Added:

- `src/epilepsy_agents/providers.py`: provider interface plus OpenAI-compatible and Ollama adapters.
- `src/epilepsy_agents/structured_schema.py`: shared extraction JSON schema and system prompt.
- `scripts/model_probe.py`: safe local hardware/runtime probe that does not print secret values.

## Source Notes

- LM Studio documents JSON-schema structured output through `/v1/chat/completions` and notes that GGUF models use llama.cpp grammar-based sampling.
- Ollama documents structured outputs by passing a JSON schema to the `format` field and recommends temperature `0` for determinism.
- vLLM documents structured outputs through JSON schema, regex, choice, grammar, and structural tags in its OpenAI-compatible server.
- vLLM tool calling supports named or required function calls with schema-constrained decoding for tool arguments.
- Qwen2.5-7B-Instruct's model card highlights stronger structured-output generation, 7.61B parameters, Apache 2.0 licensing, and long-context support.
- Qwen3-8B's model card documents thinking/non-thinking modes; non-thinking mode is likely better for fast extraction.
- Microsoft's Phi-4-mini-instruct model card documents 128K context and a tool-enabled function-calling format under an MIT license.
- Google's Gemma 3 documentation lists 4B, 12B, and 27B variants with 128K context for 4B+ models and function-calling support.
- OpenAI's gpt-oss release states that `gpt-oss-20b` requires 16 GB memory, which makes it a second-stage rather than first-stage test on this 8 GB VRAM laptop.
