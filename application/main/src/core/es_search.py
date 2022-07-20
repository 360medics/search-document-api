from elasticsearch import Elasticsearch


def match_with_prescription(
    es_client: Elasticsearch, input_text: str, prescription: str
) -> str:
    res = es_client.search(
        index="tools-flat-content",
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"content": f"{input_text}"}},
                        {"match": {"content": f"{prescription}"}},
                    ]
                }
            },
            "_source": [
                "name",
                "source",
                "keywords.title",
                "keywords.description",
                "pdf_data.extracted_title",
                "",
            ],
        },
    )
    return res["hits"]["hits"]
