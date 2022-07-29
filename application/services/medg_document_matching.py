import logging

from application.src.core.preprocessing import split_text
from application.src.core.search_api import get_medics, get_search
from application.src.models.data_models import MedGDocument
from config import Config

logger = logging.getLogger("uvicorn.error")


class MedGDocumentService:
    def __init__(self) -> None:
        if Config.API_DEBUG_MODE:
            logger.setLevel(logging.DEBUG)
            self.test_patient = MedGDocument.parse_raw(
                open("data/patient_4.json").read()
            )

    def match(self, document: MedGDocument) -> str:
        document = self.test_patient if self.test_patient else document
        consult = document.Consultations[-1]
        texts = consult.Resultat_consultation
        prescriptions = split_text(consult.Prescription)
        medics_res = [get_medics(prescription) for prescription in prescriptions]
        search_res = get_search(texts)
        return medics_res + search_res


medg_document_service = MedGDocumentService()
