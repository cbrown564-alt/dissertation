import unittest

from epilepsy_agents.llm_pipeline import SinglePromptLLMPipeline
from epilepsy_agents.providers import LLMResult


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


class _FakeProvider:
    provider_name = "fake-provider"
    model = "fake-model"

    def __init__(self, response, raises: bool = False) -> None:
        self.response = response
        self.raises = raises

    def chat_json(self, messages, schema):
        if self.raises:
            raise self.response
        return self.response


if __name__ == "__main__":
    unittest.main()
