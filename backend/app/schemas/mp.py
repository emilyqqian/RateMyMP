from typing import List, Optional

from app.schemas.base import ORMBase
from app.schemas.spending import SpendingEntry
from app.schemas.transparency import TransparencyEntry


class MPBase(ORMBase):
    name: str
    riding: str
    party: str
    photo_url: Optional[str] = None
    attendance_rate: Optional[float] = None
    party_line_voting_rate: Optional[float] = None
    years_in_office: Optional[int] = None


class MP(MPBase):
    id: int


class MPVotingRecord(ORMBase):
    motion_id: int
    motion_title: str
    vote: str


class MPActivity(ORMBase):
    speeches_count: int
    motions_sponsored: int


class MPSpendingSummary(ORMBase):
    total_amount: float
    entries: List[SpendingEntry]


class MPTransparencySummary(ORMBase):
    filings_count: int
    entries: List[TransparencyEntry]
