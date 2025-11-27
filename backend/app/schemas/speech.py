from datetime import date
from typing import Optional

from app.schemas.base import ORMBase


class Speech(ORMBase):
    id: int
    mp_id: int
    motion_id: Optional[int] = None
    title: str
    content: Optional[str] = None
    date: Optional[date] = None
