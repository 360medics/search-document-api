from application.main.services.es_service import es_client, indices_client

STANDARD_SOURCE = [
    "name",
    "source",
    "keywords.title",
    "keywords.description",
    "pdf_data.extracted_title",
    "document.url",
]
STANDAR_FILTER = {
    "bool": {
        "should": [{"term": {"id": 921}}, {"term": {"id": 9999999}}],
    }
}


def match_text(input_text: str, explain: bool = False) -> str:
    res = es_client.search(
        index="tools",
        body={
            "query": {
                "bool": {
                    "must": [{"match": {"content": f"{input_text}"}}],
                    "filter": STANDAR_FILTER,
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
                        {"match": {"content": f"{input_text}"}},
                        {"match": {"content": f"{prescription}"}},
                    ],
                    "filter": STANDAR_FILTER,
                    "must_not": {
                        "match_phrase": {
                            "pdf_data.extracted_title": "COMMISSION DE LA TRANSPARENCE"
                        },
                    },
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
