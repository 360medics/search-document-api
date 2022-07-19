from elasticsearch import Elasticsearch


class MedGDocumentService:
    def __init__(self, env: str = "dev") -> None:
        self.es_client = Elasticsearch(
            hosts="https://data-elastic-dev.360medics.com:9200",
            http_auth=("elastic", "david"),
            verify_certs=True,
        )

    def match(self, input_text: str, prescription: str) -> str:
        res = self.es_client.search(
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
