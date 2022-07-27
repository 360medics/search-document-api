from application.src.core.search_api import get_medics
from application.src.models.data_models import MedGDocument
from application.src.core.es_search import (
    match_texts,
    match_texts_with_prescriptions,
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
            prescriptions = split_text(consult.Prescription)
            medics_res = [get_medics(prescription) for prescription in prescriptions]
            es_res = match_texts_with_prescriptions(
                text, prescriptions, explain=explain
            )
            return medics_res + es_res
        elif consult.Resultat_consultation:
            text = consult.Resultat_consultation
            text = split_text(text)
            return match_texts(text, explain=explain)
        elif consult.Prescription:
            prescriptions = split_text(consult.Prescription)
            return [get_medics(prescription) for prescription in prescriptions]
        return []


medg_document_service = MedGDocumentService()
