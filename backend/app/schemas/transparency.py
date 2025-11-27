from datetime import date

from app.schemas.base import ORMBase


class TransparencyEntry(ORMBase):
    id: int
    mp_id: int
    registry_type: str
    details: str | None = None
    filed_date: date | None = None
