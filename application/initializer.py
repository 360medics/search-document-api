from fastapi.routing import APIRouter
from application.main.routers.medg_document_matching import router as response_medg


class IncludeAPIRouter:
    def __new__(cls):
        router = APIRouter()
        router.include_router(response_medg, prefix="/api/v1", tags=["medg_match"])
        return router
