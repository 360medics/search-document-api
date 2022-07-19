class IncludeAPIRouter(object):
    def __new__(cls):
        from application.main.routers.medg_document_matching import (
            router as response_medg,
        )
        from fastapi.routing import APIRouter

        router = APIRouter()

        router.include_router(response_medg, prefix="/api/v1", tags=["medg_match"])
        return router
