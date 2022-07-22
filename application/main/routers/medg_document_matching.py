from fastapi.routing import APIRouter

from application.main.src.models.data_models import MedGDocument
from application.main.services.medg_document_matching import medg_document_service

router = APIRouter(prefix="/medg_match")


@router.post("/")
async def medg_document_route(medgdoc: MedGDocument, explain: bool = "False"):
    """

    Args:
        medgdoc (MedGDocument)

        {
            "date_of_birth": datetime.date,
            "consultations": [
                {
                "input_text": "string",
                "prescription": "string",
                "resultat_consultation": "string",
                "accident_travail": "string",
                "biometrie": "string",
                "biologie": "string",
                "date_consultation": datetime.date
                }
            ],
            "gender": ["Homme", "Femme"]
        }

    Returns:
        pdf document: WIP
    """
    document_res = medg_document_service.match(medgdoc, explain)
    return document_res
