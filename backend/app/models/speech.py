from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Speech(Base):
    __tablename__ = "speeches"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mps.id"), nullable=False)
    motion_id = Column(Integer, ForeignKey("motions.id"), nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    date = Column(Date)

    mp = relationship("MP", back_populates="speeches")
    motion = relationship("Motion", back_populates="speeches")
