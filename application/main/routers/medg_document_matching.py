from fastapi.routing import APIRouter

from application.main.services.document_matching import MedGDocumentService

medg_document_service = MedGDocumentService("dev")
router = APIRouter(prefix="/medg_match")


@router.get("/")
async def medg_document_route(
    input_text: str | None = None, prescription: str | None = None
):
    document_res = medg_document_service.match(
        input_text=input_text, prescription=prescription
    )
    return document_res
