from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.initializer import IncludeAPIRouter
from application.main.config import settings


def get_application():
    _app = FastAPI(
        title=settings.API_NAME,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
    )
    _app.include_router(IncludeAPIRouter())
    _app.add_middleware(
        CORSMiddleware,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


app = get_application()


@app.on_event("shutdown")
async def app_shutdown():
    print("On App Shutdown i will be called.")
