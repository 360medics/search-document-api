from application.main.src.models.data_models import MedGDocument
from application.main.src.core.es_search import match_text, match_with_prescription

import logging

from config import Config

logger = logging.getLogger("uvicorn.error")


class MedGDocumentService:
    def __init__(self) -> None:
        if Config.API_DEBUG_MODE:
            logger.setLevel(logging.DEBUG)
            self.test_patient = MedGDocument.parse_raw(
                open("data/patient_4.json").read()
            )

    def match(self, document: MedGDocument, explain: bool = False) -> str:
        document = self.test_patient if self.test_patient else document
        consult = document.Consultations[-2]
        if (consult.Text or consult.Resultat_consultation) and consult.Prescription:
            text = consult.Text + consult.Resultat_consultation
            return match_with_prescription(text, consult.Prescription, explain=explain)
        elif consult.Text or consult.Resultat_consultation:
            text = consult.Text if consult.Text else consult.Resultat_consultation
            return match_text(text, explain=explain)
        elif consult.Prescription:
            return match_text(consult.Prescription, explain=explain)
        return []


medg_document_service = MedGDocumentService()
