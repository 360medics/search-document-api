from application.main.src.models.data_models import MedGDocument
from application.main.src.core.es_search import match, match_with_prescription

from elasticsearch import Elasticsearch

import logging

logger = logging.getLogger("uvicorn.error")


class MedGDocumentService:
    def __init__(self, env: str = "dev", debug: bool = False) -> None:
        self.es_client = Elasticsearch(
            hosts=f"https://data-elastic-{env}.360medics.com:9200",
            http_auth=("elastic", "david"),
            verify_certs=True,
        )
        if debug:
            logger.setLevel(logging.DEBUG)
            self.test_patient = MedGDocument.parse_raw(
                open("data/patient_0.json").read()
            )

    def match(self, document: MedGDocument) -> str:
        document = self.test_patient if self.test_patient else document
        consult = document.Consultations[-1]
        logger.debug(consult)
        if (consult.Text or consult.Resultat_consultation) and consult.Prescription:
            text = consult.Text if consult.Text else consult.Resultat_consultation
            return match_with_prescription(self.es_client, text, consult.Prescription)
        elif consult.Text or consult.Resultat_consultation:
            text = consult.Text if consult.Text else consult.Resultat_consultation
            return match(self.es_client, text)
        elif consult.Prescription:
            return match(self.es_client, consult.Prescription)
        return []
