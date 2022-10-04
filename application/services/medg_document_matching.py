import logging

from application.src.core.preprocessing import split_text, clean_text
from application.src.core.search_api import get_search, get_sve
from application.src.models.data_models import MedGDocument
from application.src.core.es_search import get_rewritten_query
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

    def match(self, document: MedGDocument) -> list:
        document = self.test_patient if self.test_patient else document
        texts = ""
        index_consult = 3
        consult = document.Consultations[-index_consult]
        texts = (
            consult.Resultat_consultation
            if consult.Resultat_consultation
            else consult.Text
        )
        logger.info(texts)

        texts = "" if len(texts) <= 3 else texts
        prescriptions = split_text(consult.Prescription)
        if prescriptions:
            medics_res = get_search(prescriptions[0], "prod")[:3]
        else:
            medics_res = []
        texts = clean_text(texts)
        good_query = get_rewritten_query(texts)
        logger.debug(len(good_query) / len(texts))
        if (len(good_query) / len(texts)) > 0.02:
            search_res = get_sve(good_query)
        else:
            search_res = []
        return medics_res + search_res


medg_document_service = MedGDocumentService()
