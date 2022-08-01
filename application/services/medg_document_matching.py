import logging

from application.src.core.preprocessing import split_text
from application.src.core.search_api import get_medics, get_search
from application.src.models.data_models import MedGDocument
from config import Config

logger = logging.getLogger("uvicorn.error")


class MedGDocumentService:
    """_Service for processing general medicin document"""

    def __init__(self) -> None:
        if Config.API_DEBUG_MODE:
            logger.setLevel(logging.DEBUG)
            self.test_patient = MedGDocument.parse_raw(
                open("data/patient_0.json").read()
            )

    def match(self, document: MedGDocument) -> str:
        document = self.test_patient if self.test_patient else document
        texts = ""
        index_consult = 1
        while len(texts) <= 3 or len(document.Consultations) < index_consult:
            consult = document.Consultations[-index_consult]
            texts = (
                consult.Resultat_consultation
                if consult.Resultat_consultation
                else consult.Text
            )
            logger.info(texts)
            index_consult += 1

        texts = "" if len(texts) <= 3 else texts
        prescriptions = split_text(consult.Prescription)
        medics_res = [get_medics(prescription) for prescription in prescriptions]
        search_res = get_search(texts)
        return medics_res + search_res


medg_document_service = MedGDocumentService()
