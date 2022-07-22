from datetime import date
import re


def split_text(text: str) -> str:
    return re.split(r"\W+", text)


def compute_age(DDN: date, Date_consultation: date) -> int:
    delta = Date_consultation - DDN
    return delta.days // 365
