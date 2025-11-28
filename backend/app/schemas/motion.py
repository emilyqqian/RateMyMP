import datetime as dt
from typing import Any, Dict, List, Optional

from pydantic import Field

from app.models.enums import MotionClassification
from app.schemas.base import ORMBase


class MotionBase(ORMBase):
    title: str
    description: Optional[str] = None
    introduced_by_mp_id: int
    introduced_by_party: Optional[str] = None
    # Allow flexible vote payloads from OpenParliament (e.g. {"vote": "yea"})
    # as well as normalized tallies ({"yea": 10, "nay": 5, "abstain": 0}).
    vote_results_by_party: Optional[Dict[str, Dict[str, Any]]] = None
    passed: bool = False
    categories: List[str] = Field(default_factory=list)
    classification: MotionClassification
    date: Optional[dt.date] = None


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
