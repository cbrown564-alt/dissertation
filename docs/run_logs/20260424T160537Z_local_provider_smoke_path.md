# Local Provider Smoke Path

## Session Metadata

- Date: 2026-04-24
- Session ID: 20260424T160537Z_local_provider_smoke_path
- Session objective: Add a minimal local-runtime verification path for M-A1 and check whether a local provider is currently reachable.
- Related active thread: Local model runtime and provider plumbing
- Starting commit: `dd081bd3085172fc8dabcc66615cf4a3ec775470`
- Dirty worktree at start: yes
- Optional JSON companion: none

## Outcome

A dedicated `provider-smoke` CLI command now probes `lmstudio`, `vllm`, or `ollama` and can run one minimal schema-constrained JSON request through the provider adapter. This makes M-A1 verifiable in one command once a local model server is live. The current environment is still blocked on runtime availability: an LM Studio probe against `http://localhost:1234/v1` returned `URLError`.

## Evidence

- Files changed:
  - [src/epilepsy_agents/cli.py](/C:/Users/cbrow/Code/dissertation/src/epilepsy_agents/cli.py)
  - [src/epilepsy_agents/providers.py](/C:/Users/cbrow/Code/dissertation/src/epilepsy_agents/providers.py)
  - [tests/test_cli.py](/C:/Users/cbrow/Code/dissertation/tests/test_cli.py)
  - [tests/test_visibility.py](/C:/Users/cbrow/Code/dissertation/tests/test_visibility.py)
- Tests or checks:
  - `PYTHONPATH=src python -m unittest discover -s tests` -> 30 tests passed.
  - `PYTHONPATH=src python -m epilepsy_agents.cli provider-smoke --provider lmstudio --model qwen2.5-7b-instruct --skip-chat` -> probe failed with `URLError`.
- Generated artifacts:
  - none

## Uncertainty

The new command verifies connectivity and a tiny schema-constrained round trip, but it does not yet implement `h003_single_prompt_llm` or record token/latency metadata. Ollama was not fully characterized in this session because the targeted blocker remained "no confirmed live local runtime." The existing worktree had unrelated modifications at session start and was left intact.

## Handoff

Install or launch one local runtime, then rerun:

```powershell
$env:PYTHONPATH = "src"
python -m epilepsy_agents.cli provider-smoke --provider lmstudio --model <loaded-model-id>
```

If that passes, use the same provider path to implement `h003_single_prompt_llm` with invalid-output, latency, and token-budget recording.

## Decision

blocked by local model/runtime setup

## Privacy Check

Confirmed: no raw real clinical text was written into logs, prompts, screenshots, traces, run records, or exported artifacts.
