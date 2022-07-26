from datetime import date
import re


def split_text(text: str) -> str:
    return list(map(str.strip, filter(None, re.split(r"[^\w\s]", text))))


def compute_age(DDN: date, Date_consultation: date) -> int:
    assert DDN <= Date_consultation
    delta = Date_consultation - DDN
    return delta.days // 365
