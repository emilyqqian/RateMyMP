from app.models.enums import VoteChoice
from app.schemas.base import ORMBase


class VoteRecord(ORMBase):
    id: int
    mp_id: int
    motion_id: int
    vote: VoteChoice
