import unittest

from epilepsy_agents.agents import FieldExtractorAgent, SectionTimelineAgent


class FieldExtractorAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.extractor = FieldExtractorAgent()

    def test_extracts_or_range_over_implicit_one_week(self) -> None:
        extracted = self.extractor._extract_from_text(
            "The patient reports six or seven seizures over the past week."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "6 to 7 per week")

    def test_extracts_hyphenated_modifiers_in_window_first_phrase(self) -> None:
        extracted = self.extractor._extract_from_text(
            "Over the past six weeks there were four brief focal-aware episodes."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "4 per 6 week")

    def test_sums_distinct_event_counts_in_shared_window(self) -> None:
        extracted = self.extractor._extract_from_text(
            "Since her last review three months ago, she describes two drop attacks "
            "and five convulsions in the past three months."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "7 per 3 month")

    def test_sums_dated_count_list_over_calendar_span(self) -> None:
        extracted = self.extractor._extract_from_text(
            "Regarding recent events: In February she experienced a prolonged focal seizure. "
            "In May there were four further brief absences, and in August a single "
            "generalised tonic-clonic seizure was reported."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "6 per 7 month")

    def test_spasms_are_frequency_candidates(self) -> None:
        timeline = SectionTimelineAgent().run(
            "As per diary review, focal epileptic spasms occur several times each week."
        )
        self.assertTrue(timeline.candidates)
        extracted = self.extractor._extract_from_text(timeline.candidates[0].text)
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "multiple per week")

    def test_between_episodes_does_not_imply_seizure_freedom(self) -> None:
        extracted = self.extractor._extract_from_text(
            "Otherwise, no events were documented between these episodes."
        )
        self.assertIsNone(extracted)


if __name__ == "__main__":
    unittest.main()
