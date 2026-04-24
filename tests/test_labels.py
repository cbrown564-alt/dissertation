import unittest

from epilepsy_agents.labels import parse_label


class LabelParsingTests(unittest.TestCase):
    def test_parse_direct_rate(self) -> None:
        parsed = parse_label("2 per week")
        self.assertEqual(parsed.pragmatic_class, "frequent")
        self.assertTrue(8.0 < (parsed.monthly_rate or 0) < 9.0)

    def test_parse_cluster_rate(self) -> None:
        parsed = parse_label("2 cluster per month, 6 per cluster")
        self.assertEqual(parsed.monthly_rate, 12.0)
        self.assertEqual(parsed.pragmatic_class, "frequent")

    def test_parse_seizure_free(self) -> None:
        parsed = parse_label("seizure free for 12 month")
        self.assertEqual(parsed.monthly_rate, 0.0)
        self.assertEqual(parsed.pragmatic_class, "NS")

    def test_parse_unknown(self) -> None:
        parsed = parse_label("unknown, 2 to 3 per cluster")
        self.assertEqual(parsed.monthly_rate, 1000.0)
        self.assertEqual(parsed.purist_class, "UNK")


if __name__ == "__main__":
    unittest.main()
