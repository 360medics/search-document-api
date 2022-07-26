from datetime import date

from application.src.core.preprocessing import split_text, compute_age


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
