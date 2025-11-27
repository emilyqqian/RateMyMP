from typing import List

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import (
    MP,
    MPActivity,
    MPSpendingSummary,
    MPTransparencySummary,
    MPVotingRecord,
    Speech,
)
from app.services.mp_service import MPService

router = APIRouter()


@router.get("", response_model=List[MP])
def list_mps(
    search: Optional[str] = Query(
        None,
        min_length=1,
        description="Optional search string that matches MP name or riding",
    ),
    db: Session = Depends(get_db),
):
    return MPService(db).list_mps(search=search)


@router.get("/{mp_id}", response_model=MP)
def get_mp(mp_id: int, db: Session = Depends(get_db)):
    return MPService(db).get_mp(mp_id)


@router.get("/{mp_id}/voting-record", response_model=List[MPVotingRecord])
def get_voting_record(mp_id: int, db: Session = Depends(get_db)):
    return MPService(db).get_voting_record(mp_id)


@router.get("/{mp_id}/parliamentary-activity", response_model=MPActivity)
def get_parliamentary_activity(mp_id: int, db: Session = Depends(get_db)):
    return MPService(db).get_parliamentary_activity(mp_id)


@router.get("/{mp_id}/spending", response_model=MPSpendingSummary)
def get_spending(mp_id: int, db: Session = Depends(get_db)):
    return MPService(db).get_spending(mp_id)


@router.get("/{mp_id}/transparency", response_model=MPTransparencySummary)
def get_transparency(mp_id: int, db: Session = Depends(get_db)):
    return MPService(db).get_transparency(mp_id)


@router.get("/{mp_id}/speeches", response_model=List[Speech])
def get_speeches(mp_id: int, db: Session = Depends(get_db)):
    return MPService(db).get_speeches(mp_id)
