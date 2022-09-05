import logging

from application.src.models.data_models import FRCP
from application.src.core.search_api import get_search
from config import Config

logger = logging.getLogger("uvicorn.error")


class FRCPService:
    """_Service for processing FRCP"""

    def __init__(self) -> None:
        if Config.API_DEBUG_MODE:
            logger.setLevel(logging.DEBUG)
            self.test_patient = FRCP.parse_raw(
                open("data/fake-rcp230622/Fake_0.json").read()
            )

    def match(self, document: FRCP) -> list:
        document = self.test_patient if self.test_patient else document
        search_res = get_search(document.HDM)
        return search_res


frcp_service = FRCPService()
