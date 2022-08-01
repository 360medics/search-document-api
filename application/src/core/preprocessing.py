import re
from datetime import date


# [^\w\s]
def split_text(text: str) -> str:
    return (
        list(filter(None, map(str.strip, re.split(r"\+|\/|\;", text)))) if text else ""
    )


def compute_age(ddn: date, date_consultation: date) -> int:
    assert ddn <= date_consultation
    delta = date_consultation - ddn
    return delta.days // 365


def multiple_match_phrase(queries: list[str]) -> list:
    return [{"match_phrase": {"content": query}} for query in queries]
