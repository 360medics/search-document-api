from datetime import date

from application.src.core.preprocessing import (
    split_text,
    compute_age,
    multiple_match_phrase,
)


def test_split_text():
    text_1 = "Camembert // Fromage"
    text_2 = "St marcelin +++ Gouda"
    text_3 = "Gruyere / Emmental +; Parmesan"
    assert split_text(text_1) == ["Camembert", "Fromage"]
    assert split_text(text_2) == ["St marcelin", "Gouda"]
    assert split_text(text_3) == ["Gruyere", "Emmental", "Parmesan"]


def test_compute_age():
    date_1 = date(1917, 10, 13)
    date_2 = date(2022, 7, 26)
    diff_age = compute_age(date_1, date_2)
    assert diff_age == 104


def test_multiple_match_phrase():
    queries = ["Son Goku", "Vegeta", "Krilin"]
    match_phrases = multiple_match_phrase(queries)
    assert match_phrases[0] == {"match_phrase": {"content": "Son Goku"}}
    assert match_phrases[1] == {"match_phrase": {"content": "Vegeta"}}
    assert match_phrases[2] == {"match_phrase": {"content": "Krilin"}}
