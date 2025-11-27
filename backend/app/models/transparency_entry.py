from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class TransparencyEntry(Base):
    __tablename__ = "transparency_entries"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mps.id"), nullable=False)
    registry_type = Column(String, nullable=False)
    details = Column(Text)
    filed_date = Column(Date)

    mp = relationship("MP", back_populates="transparency_entries")
