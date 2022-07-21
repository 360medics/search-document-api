from elasticsearch import Elasticsearch

STANDARD_SOURCE = [
    "name",
    "source",
    "keywords.title",
    "keywords.description",
    "pdf_data.extracted_title",
    "document.url",
]
STANDAR_FILTER = {
    "bool": {"should": [{"term": {"id": 921}}, {"term": {"id": 9999999}}]}
}


def match(es_client: Elasticsearch, input_text: str) -> str:
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
    )
    return res["hits"]["hits"]


def match_with_prescription(
    es_client: Elasticsearch, input_text: str, prescription: str
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
                }
            },
            "_source": STANDARD_SOURCE,
        },
    )
    return res["hits"]["hits"]
