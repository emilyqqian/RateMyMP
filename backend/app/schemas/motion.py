from datetime import date
from typing import Dict, List, Optional

from pydantic import Field

from app.models.enums import MotionClassification
from app.schemas.base import ORMBase


class MotionBase(ORMBase):
    title: str
    description: Optional[str] = None
    introduced_by_mp_id: int
    introduced_by_party: Optional[str] = None
    vote_results_by_party: Optional[Dict[str, Dict[str, int]]] = None
    passed: bool = False
    categories: List[str] = Field(default_factory=list)
    classification: MotionClassification
    date: Optional[date] = None


class MotionCreate(MotionBase):
    pass


class MotionUpdate(MotionBase):
    pass


class Motion(MotionBase):
    id: int


class MotionVoteRequest(ORMBase):
    mp_id: int
    vote: str = Field(pattern="^(upvote|downvote)$")


class MotionVoteResponse(ORMBase):
    motion_id: int
    mp_id: int
    vote: str


class AISummaryResponse(ORMBase):
    motion_id: int
    summary: str
