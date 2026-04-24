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

    def test_numeric_seizure_free_duration_still_extracted(self) -> None:
        extracted = self.extractor._extract_from_text(
            "She has now been seizure free for 3 years."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for 3 year")

    def test_qualitative_seizure_free_duration_maps_to_multiple_month(self) -> None:
        extracted = self.extractor._extract_from_text(
            "He has remained seizure-free for a prolonged period."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for multiple month")

    def test_seizure_free_unit_only_maps_to_multiple_unit(self) -> None:
        extracted = self.extractor._extract_from_text(
            "He has been seizure free for years."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for multiple year")

    def test_seizure_free_since_date_maps_to_multiple_month(self) -> None:
        extracted = self.extractor._extract_from_text(
            "Seizure-free off ASMs since 25 Jun 2015."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for multiple month")

    def test_seizure_free_by_patient_report_maps_to_multiple_month(self) -> None:
        extracted = self.extractor._extract_from_text(
            "At today's visit, he is Seizure-free by patient report."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for multiple month")

    def test_no_seizures_for_numeric_window_extracts_duration(self) -> None:
        extracted = self.extractor._extract_from_text(
            "He has not reported seizures for over several years."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for multiple year")

    def test_long_term_remission_maps_to_multiple_month(self) -> None:
        extracted = self.extractor._extract_from_text(
            "He is currently in long-term remission."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for multiple month")

    def test_no_witnessed_episodes_catch_all(self) -> None:
        extracted = self.extractor._extract_from_text(
            "There have been no witnessed episodes of impaired awareness."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for multiple month")

    def test_without_any_recurrence_catch_all(self) -> None:
        extracted = self.extractor._extract_from_text(
            "She reports a sustained period without any recurrence of her typical events."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for multiple month")

    def test_seizure_occurrences_have_not_been_happening(self) -> None:
        extracted = self.extractor._extract_from_text(
            "Seizure occurrences have not been happening."
        )
        self.assertIsNotNone(extracted)
        self.assertEqual(extracted[0], "seizure free for multiple month")

    def test_prior_to_history_not_interpreted_as_seizure_free(self) -> None:
        extracted = self.extractor._extract_from_text(
            "Prior to retirement he had no breakthrough events on his current regimen."
        )
        self.assertIsNone(extracted)


if __name__ == "__main__":
    unittest.main()
