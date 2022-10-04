import logging

from application.src.models.data_models import FRCP
from application.src.core.search_api import get_direct_es, get_result_related, get_sve
from config import Config

logger = logging.getLogger("uvicorn.error")


class FRCPService:
    """_Service for processing FRCP"""

    def __init__(self) -> None:
        if Config.API_DEBUG_MODE:
            logger.setLevel(logging.DEBUG)
            self.test_patient = FRCP.parse_raw(
                open("data/fake-rcp230622/Fake_2.json").read()
            )

    def match(self, document: FRCP) -> list:
        document = self.test_patient if self.test_patient else document
        search_res = get_direct_es(document.Patho).get("hits").get("hits")

        search_res = [
            {
                "title": elem.get("_source").get("title"),
                "url": elem.get("_source").get("document").get("url"),
                "from": "search syntax",
            }
            for elem in search_res
        ]

        search_reco = search_res[:1] + search_res[2:6]

        sve_res = get_sve(document.HDM)[:3]

        sve_res = [
            {
                "title": elem.get("data").get("title"),
                "url": elem.get("data").get("document").get("url"),
                "logo": elem.get("data").get("source").get("logo"),
                "from": "search sem",
            }
            for elem in sve_res
        ]

        return search_reco + sve_res

    def match_related(self, document: FRCP) -> list:
        document = self.test_patient if self.test_patient else document

        logger.debug(document.Patho)
        res = get_result_related(text=f"Traitement {document.Patho}")
        return res


frcp_service = FRCPService()
