from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter

from application.routers.medg_document_matching import router as response_medg
from application.routers.es_service import router as response_utils

from config import Config


router = APIRouter()
router.include_router(response_medg, prefix="/api/v1")
router.include_router(response_utils, prefix="/api/v1")

app = FastAPI(
    title=Config.API_NAME,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION,
)
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def app_shutdown():
    print("On App Shutdown.")
