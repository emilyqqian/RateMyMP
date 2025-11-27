from fastapi import APIRouter

from app.services.lookup_service import LookupService

router = APIRouter()
lookup_service = LookupService()


@router.get("/postal-code/{postal_code}")
def lookup_postal_code(postal_code: str):
    return lookup_service.lookup_postal_code(postal_code)
