from application.src.models.data_models import MedGDocument
from application.src.core.es_search import (
    match_text,
    match_texts,
    match_texts_with_prescription,
)
from application.src.core.preprocessing import split_text
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
        if consult.Resultat_consultation and consult.Prescription:
            text = consult.Resultat_consultation
            text = split_text(text)
            return match_texts_with_prescription(
                text, consult.Prescription, explain=explain
            )
        elif consult.Resultat_consultation:
            text = consult.Resultat_consultation
            text = split_text(text)
            return match_texts(text, explain=explain)
        elif consult.Prescription:
            return match_text(consult.Prescription, explain=explain)
        return []


medg_document_service = MedGDocumentService()
