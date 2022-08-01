import unittest
from datetime import date

from application.src.core.preprocessing import (
    compute_age,
    multiple_match_phrase,
    split_text,
)


class TestProprocessing(unittest.TestCase):
    def test_split_text(self):
        text_1 = "Camembert // Fromage"
        text_2 = "St marcelin +++ Gouda"
        text_3 = "Gruyere / Emmental +; Parmesan"
        self.assertEqual(split_text(text_1), ["Camembert", "Fromage"])
        self.assertEqual(split_text(text_2), ["St marcelin", "Gouda"])
        self.assertEqual(split_text(text_3), ["Gruyere", "Emmental", "Parmesan"])

    def test_compute_age(self):
        date_1 = date(1917, 10, 13)
        date_2 = date(2022, 7, 26)
        diff_age = compute_age(date_1, date_2)
        self.assertEqual(diff_age, 104)

    def test_multiple_match_phrase(self):
        queries = ["Son Goku", "Vegeta", "Krilin"]
        match_phrases = multiple_match_phrase(queries)
        self.assertEqual(match_phrases[0], {"match_phrase": {"content": "Son Goku"}})
        self.assertEqual(match_phrases[1], {"match_phrase": {"content": "Vegeta"}})
        self.assertEqual(match_phrases[2], {"match_phrase": {"content": "Krilin"}})


if __name__ == "__main__":
    unittest.main()
