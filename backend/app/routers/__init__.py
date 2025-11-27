from fastapi import APIRouter

from app.routers import lookup, motions, mps

api_router = APIRouter()
api_router.include_router(motions.router, prefix="/motions", tags=["motions"])
api_router.include_router(mps.router, prefix="/mps", tags=["mps"])
api_router.include_router(lookup.router, prefix="/lookup", tags=["lookup"])
