from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class SpendingEntry(Base):
    __tablename__ = "spending_entries"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mps.id"), nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    fiscal_year = Column(String, nullable=False)
    details_url = Column(String)

    mp = relationship("MP", back_populates="spending_entries")
