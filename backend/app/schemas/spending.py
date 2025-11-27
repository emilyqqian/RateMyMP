from app.schemas.base import ORMBase


class SpendingEntry(ORMBase):
    id: int
    mp_id: int
    category: str
    amount: float
    fiscal_year: str
    details_url: str | None = None
