from application.services.rcp_document_matching import frcp_service
from application.src.models.data_models import FRCP
from fastapi.routing import APIRouter

router = APIRouter(prefix="/frcp_match")


@router.post("/")
async def frcp_document_route(frcpdoc: FRCP):
    """_summary_

    Args:
        frcpdoc (FRCP): _description_

    Returns:
        _type_: _description_
    """
    document_res = frcp_service.match(frcpdoc)
    return document_res
