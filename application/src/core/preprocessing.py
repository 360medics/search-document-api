from datetime import date
import re


def split_text(text: str) -> str:
    return list(filter(None, map(str.strip, re.split(r"[^\w\s]", text))))


def compute_age(DDN: date, Date_consultation: date) -> int:
    assert DDN <= Date_consultation
    delta = Date_consultation - DDN
    return delta.days // 365


def multiple_match_phrase(queries: list[str]) -> list:
    return [{"match_phrase": {"content": query}} for query in queries]
