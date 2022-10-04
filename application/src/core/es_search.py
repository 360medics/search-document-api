from application.services.es_service import es_client, indices_client
from application.src.core.preprocessing import multiple_match_phrase
import logging
import json
import requests

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


def match_texts_with_prescriptions(
    input_texts: list[str], prescriptions: list[str], explain: bool = False
) -> str:
    logger.info(multiple_match_phrase(input_texts))
    res = es_client.search(
        index="tools",
        body={
            "query": {
                "bool": {
                    "must": [
                        {"bool": {"should": multiple_match_phrase(input_texts)}},
                        {"match": {"content": " ".join(prescriptions)}},
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


def get_rewritten_query(text):
    url = f"https://search-intent-detection-api-dev-jwtwih6oja-ew.a.run.app/v1?q={text}&lang=fr&highlight=true&offset=0&limit=10&page=1&country=FR&medics_area=ansm&skiprcppart=0"  # noqa: E501

    payload = json.dumps(
        {
            "id": 223046,
            "profession_id": 2,
            "roles": ["ROLE_EXPERT", "ROLE_BETA_USER", "ROLE_USER"],
            "specialty_id": 26,
            "title": "DOCTOR",
        }
    )
    headers = {
        "Content-Type": "application/json",
        "X-User-Api-Key": "1ade9001222a075902bc1ea12e0dc643",
        "correlation_id": "606d1513-c518-fd5a-ce6d-2449cbb88c9a",
        "tab": "all",
    }

    logger.debug(text)

    response = requests.request("POST", url, headers=headers, data=payload)

    logger.debug(response.text)

    return json.loads(response.text).get("results").get("data").get("rewritten_query")
