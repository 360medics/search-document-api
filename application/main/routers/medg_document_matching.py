from fastapi.routing import APIRouter

from application.main.services.document_matching import MedGDocumentService

medg_document_service = MedGDocumentService("dev")
router = APIRouter(prefix="/medg_match")


@router.get("/")
async def question_classification(input_text: str, prescription: str):
    question_type = medg_document_service.match(
        input_text=input_text, prescription=prescription
    )
    return question_type
