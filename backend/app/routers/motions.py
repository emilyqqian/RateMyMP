from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import AISummaryResponse, Motion, MotionVoteRequest, MotionVoteResponse
from app.services.motion_service import MotionService

router = APIRouter()


@router.get("", response_model=List[Motion])
def list_motions(
    category: Optional[str] = Query(None, description="Filter motions by category tag"),
    limit: Optional[int] = Query(
        None,
        ge=1,
        le=100,
        description="Optional maximum number of motions to return",
    ),
    db: Session = Depends(get_db),
):
    return MotionService(db).list_motions(category=category, limit=limit)


@router.get("/{motion_id}", response_model=Motion)
def get_motion(motion_id: int, db: Session = Depends(get_db)):
    return MotionService(db).get_motion(motion_id)


@router.get("/{motion_id}/ai-summary", response_model=AISummaryResponse)
def get_motion_ai_summary(motion_id: int, db: Session = Depends(get_db)):
    return MotionService(db).get_ai_summary(motion_id)


@router.post("/{motion_id}/vote", response_model=MotionVoteResponse)
def vote_on_motion(
    motion_id: int,
    payload: MotionVoteRequest,
    db: Session = Depends(get_db),
):
    return MotionService(db).vote_on_motion(
        motion_id=motion_id,
        mp_id=payload.mp_id,
        vote=payload.vote,
    )
