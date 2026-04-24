import unittest

from epilepsy_agents.llm_pipeline import SinglePromptLLMPipeline
from epilepsy_agents.providers import LLMResult
from epilepsy_agents.structured_schema import system_prompt


class SinglePromptLLMPipelineTests(unittest.TestCase):
    def test_returns_structured_prediction_with_usage_metadata(self) -> None:
        provider = _FakeProvider(
            LLMResult(
                content=(
                    '{"label":"2 per week","evidence":[{"text":"2 seizures per week","start":1,"end":19,"source":"letter"}],'
                    '"confidence":0.8,"analysis":"Explicit frequency statement.","warnings":[]}'
                ),
                model="fake-model",
                provider="fake-provider",
                raw={"prompt_eval_count": 100, "eval_count": 25},
            )
        )
        pipeline = SinglePromptLLMPipeline(provider=provider)

        prediction = pipeline.predict("Synthetic letter")

        self.assertEqual(prediction.label, "2 per week")
        self.assertEqual(prediction.pragmatic_class, "frequent")
        self.assertEqual(prediction.metadata["provider"], "fake-provider")
        self.assertEqual(prediction.metadata["total_tokens"], 125)
        self.assertFalse(prediction.metadata["invalid_output"])

    def test_falls_back_to_unknown_on_invalid_output(self) -> None:
        provider = _FakeProvider(ValueError("bad json"), raises=True)
        pipeline = SinglePromptLLMPipeline(provider=provider, max_retries=1)

        prediction = pipeline.predict("Synthetic letter")

        self.assertEqual(prediction.label, "unknown")
        self.assertIn("invalid_output", prediction.warnings)
        self.assertTrue(prediction.metadata["invalid_output"])
        self.assertEqual(prediction.metadata["attempt"], 2)

    def test_recovers_json_from_local_model_wrapper(self) -> None:
        provider = _FakeProvider(
            LLMResult(
                content=(
                    "<think>I should answer with JSON.</think>\n"
                    '```json\n{"label":"4 per day","evidence":[{"text":"four seizures each day",'
                    '"start":10,"end":32,"source":"letter"}],"confidence":0.9,'
                    '"analysis":"Explicit daily frequency.","warnings":[]}\n```'
                ),
                model="fake-model",
                provider="fake-provider",
                raw={},
            )
        )
        pipeline = SinglePromptLLMPipeline(provider=provider)

        prediction = pipeline.predict("Synthetic letter")

        self.assertEqual(prediction.label, "4 per day")
        self.assertEqual(prediction.purist_class, ">=1/D")
        self.assertFalse(prediction.metadata["invalid_output"])

    def test_accepts_schema_near_evidence_string(self) -> None:
        provider = _FakeProvider(
            LLMResult(
                content='{"label":"2 per week","evidence":"The patient currently has 2 seizures per week."}',
                model="fake-model",
                provider="fake-provider",
                raw={},
            )
        )
        pipeline = SinglePromptLLMPipeline(provider=provider)

        prediction = pipeline.predict("Synthetic letter")

        self.assertEqual(prediction.label, "2 per week")
        self.assertEqual(prediction.evidence[0].text, "The patient currently has 2 seizures per week.")
        self.assertEqual(prediction.confidence, 0.0)
        self.assertFalse(prediction.metadata["invalid_output"])

    def test_user_prompt_discourages_unnecessary_unknown(self) -> None:
        provider = _FakeProvider(
            LLMResult(
                content='{"label":"unknown","evidence":[],"confidence":0.0,"analysis":"No answer.","warnings":[]}',
                model="fake-model",
                provider="fake-provider",
            )
        )
        pipeline = SinglePromptLLMPipeline(provider=provider)

        pipeline.predict("Synthetic letter")

        user_prompt = provider.calls[0]["messages"][1].content
        self.assertIn("Prefer an explicit frequency label", user_prompt)
        self.assertIn("use unknown only", user_prompt)

    def test_system_prompt_disables_qwen_thinking_mode(self) -> None:
        self.assertTrue(system_prompt().startswith("/no_think"))


class _FakeProvider:
    provider_name = "fake-provider"
    model = "fake-model"

    def __init__(self, response, raises: bool = False) -> None:
        self.response = response
        self.raises = raises
        self.calls = []

    def chat_json(self, messages, schema):
        self.calls.append({"messages": messages, "schema": schema})
        if self.raises:
            raise self.response
        return self.response


if __name__ == "__main__":
    unittest.main()
