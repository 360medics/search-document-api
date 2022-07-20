from application.main.src.models.data_models import MedGDocument
from application.main.src.core.es_search import match_with_prescription

from elasticsearch import Elasticsearch


class MedGDocumentService:
    def __init__(self, env: str = "dev") -> None:
        self.es_client = Elasticsearch(
            hosts=f"https://data-elastic-{env}.360medics.com:9200",
            http_auth=("elastic", "david"),
            verify_certs=True,
        )

    def match(self, document: MedGDocument) -> str:
        if document.input_text and document.prescription:
            return match_with_prescription(
                self.es_client, document.input_text, document.prescription
            )
        else:
            return ""
