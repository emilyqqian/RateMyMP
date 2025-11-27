from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.routers import api_router
from app.services.demo_data import seed_demo_data
from app.utils.logging import configure_logging

configure_logging()
init_db()
if settings.LOAD_DEMO_DATA:
    seed_demo_data()

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["meta"])
def health_check():
    return {"status": "ok", "service": settings.APP_NAME, "version": settings.VERSION}
