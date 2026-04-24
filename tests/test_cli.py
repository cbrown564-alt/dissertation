import argparse
import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from epilepsy_agents import cli
from epilepsy_agents.providers import LLMResult


class ProviderSmokeTests(unittest.TestCase):
    def test_default_base_urls_match_provider(self) -> None:
        self.assertEqual(cli._default_base_url("lmstudio"), "http://localhost:1234/v1")
        self.assertEqual(cli._default_base_url("vllm"), "http://localhost:8000/v1")
        self.assertEqual(cli._default_base_url("ollama"), "http://localhost:11434/api")

    def test_probe_provider_uses_ollama_tags_endpoint(self) -> None:
        with patch("epilepsy_agents.cli.probe_ollama", return_value={"ok": True}) as probe_ollama:
            result = cli._probe_provider("ollama", None, 5)

        self.assertEqual(result, {"ok": True})
        probe_ollama.assert_called_once_with("http://localhost:11434/api", timeout_seconds=5)

    def test_provider_smoke_returns_failure_when_probe_fails(self) -> None:
        args = argparse.Namespace(
            provider="lmstudio",
            model="qwen-test",
            base_url=None,
            timeout_seconds=3,
            skip_chat=False,
        )
        output = io.StringIO()
        with patch("epilepsy_agents.cli._probe_provider", return_value={"ok": False, "error": "URLError"}):
            with redirect_stdout(output):
                status = cli.provider_smoke(args)

        self.assertEqual(status, 1)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["provider"], "lmstudio")
        self.assertFalse(payload["probe"]["ok"])

    def test_provider_smoke_runs_chat_when_probe_passes(self) -> None:
        args = argparse.Namespace(
            provider="ollama",
            model="phi-test",
            base_url="http://localhost:11434/api",
            timeout_seconds=4,
            skip_chat=False,
        )
        fake_provider = _FakeProvider()
        output = io.StringIO()
        with patch("epilepsy_agents.cli._probe_provider", return_value={"ok": True, "response": {"models": []}}):
            with patch("epilepsy_agents.cli._provider_instance", return_value=fake_provider):
                with redirect_stdout(output):
                    status = cli.provider_smoke(args)

        self.assertEqual(status, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["chat_result"]["content"], '{"status":"ok","label":"smoke_ok"}')
        self.assertEqual(fake_provider.calls[0]["messages"][1].content, "Confirm the local extraction runtime is reachable.")
        self.assertEqual(fake_provider.calls[0]["schema"]["required"], ["status", "label"])


class OllamaProviderTests(unittest.TestCase):
    def test_ollama_caps_completion_tokens(self) -> None:
        with patch("epilepsy_agents.providers._post_json", return_value={"message": {"content": "{}"}}) as post_json:
            provider = cli.local_ollama_provider(model="qwen-test", base_url="http://localhost:11434/api")

            provider.chat_json([], {"type": "object"})

        payload = post_json.call_args.args[1]
        self.assertIs(payload["think"], False)
        self.assertEqual(payload["options"]["temperature"], 0)
        self.assertEqual(payload["options"]["num_predict"], 512)


class _FakeProvider:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def chat_json(self, messages, schema):
        self.calls.append({"messages": messages, "schema": schema})
        return LLMResult(
            content='{"status":"ok","label":"smoke_ok"}',
            model="fake-model",
            provider="fake-provider",
        )


if __name__ == "__main__":
    unittest.main()
