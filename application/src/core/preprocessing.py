import re
from datetime import date
import unidecode
import string


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


def clean_text(text: str) -> str:
    cleaned_text = text.lower()
    cleaned_text = unidecode.unidecode(cleaned_text)
    cleaned_text = "".join(filter(lambda x: x in string.printable, cleaned_text))
    cleaned_text = cleaned_text.translate(str.maketrans("", "", string.punctuation))
    cleaned_text = cleaned_text.strip()
    return cleaned_text
