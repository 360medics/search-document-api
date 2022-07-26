from application.src.core.preprocessing import split_text


def test_split_text():
    text_1 = "Camembert // Fromage"
    text_2 = "St marcelin +++ Gouda"
    text_3 = "Gruyere / Emmental +; Parmesan"
    assert split_text(text_1) == ["Camembert", "Fromage"]
    assert split_text(text_2) == ["St marcelin", "Gouda"]
    assert split_text(text_3) == ["Gruyere", "Emmental", "Parmesan"]
