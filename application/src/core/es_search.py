from application.services.es_service import es_client, indices_client
from application.src.core.preprocessing import multiple_match_phrase
import logging

logger = logging.getLogger("uvicorn.error")

STANDARD_SOURCE = [
    "name",
    "source",
    "keywords.title",
    "keywords.description",
    "pdf_data.extracted_title",
    "document.url",
]
STANDARD_FILTER = {
    "bool": {
        "should": [{"term": {"id": 921}}, {"term": {"id": 9999999}}],
    }
}

STANDARD_MUST_NOT = {
    "match_phrase": {"pdf_data.extracted_title": "COMMISSION DE LA TRANSPARENCE"},
}


def match_text(input_text: str, explain: bool = False) -> str:
    res = es_client.search(
        index="tools",
        body={
            "query": {
                "bool": {
                    "must": [{"match": {"content": input_text}}],
                    "filter": STANDARD_FILTER,
                    "must_not": STANDARD_MUST_NOT,
                }
            },
            "_source": STANDARD_SOURCE,
        },
        explain=explain,
    )
    return res["hits"]["hits"]


def match_texts(input_texts: list[str], explain: bool = False) -> str:
    logger.info(multiple_match_phrase(input_texts))
    res = es_client.search(
        index="tools",
        body={
            "query": {
                "bool": {
                    "should": multiple_match_phrase(input_texts),
                    "filter": STANDARD_FILTER,
                    "must_not": STANDARD_MUST_NOT,
                }
            },
            "_source": STANDARD_SOURCE,
        },
        explain=explain,
    )
    return res["hits"]["hits"]


def match_texts_with_prescription(
    input_texts: list[str], prescription: str, explain: bool = False
) -> str:
    logger.info(multiple_match_phrase(input_texts))
    res = es_client.search(
        index="tools",
        body={
            "query": {
                "bool": {
                    "must": [
                        {"bool": {"should": multiple_match_phrase(input_texts)}},
                        {"match": {"content": prescription}},
                    ],
                    "filter": STANDARD_FILTER,
                    "must_not": STANDARD_MUST_NOT,
                }
            },
            "_source": STANDARD_SOURCE,
        },
        explain=explain,
    )
    return res["hits"]["hits"]


def match_with_prescription(
    input_text: str, prescription: str, explain: bool = False
) -> str:
    res = es_client.search(
        index="tools",
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"content": input_text}},
                        {"match": {"content": prescription}},
                    ],
                    "filter": STANDARD_FILTER,
                    "must_not": STANDARD_MUST_NOT,
                }
            },
            "_source": STANDARD_SOURCE,
        },
        explain=explain,
    )
    return res["hits"]["hits"]


def analyze_es_text(text: str, analyzer: str = "custom_analyzer"):
    return indices_client.analyze(
        index="tools",
        body={
            "analyzer": analyzer,
            "text": text,
        },
    )


def explain_es_match(id: str):
    return es_client.explain(index="tools", id=id, source=STANDARD_SOURCE)
