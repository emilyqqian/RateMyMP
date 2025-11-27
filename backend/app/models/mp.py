from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class MP(Base):
    __tablename__ = "mps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    riding = Column(String, nullable=False)
    party = Column(String, nullable=False)
    photo_url = Column(String)
    attendance_rate = Column(Float)
    party_line_voting_rate = Column(Float)
    years_in_office = Column(Integer)

    motions = relationship("Motion", back_populates="introduced_by_mp", cascade="all,delete")
    votes = relationship("VoteRecord", back_populates="mp", cascade="all,delete")
    speeches = relationship("Speech", back_populates="mp", cascade="all,delete")
    spending_entries = relationship("SpendingEntry", back_populates="mp", cascade="all,delete")
    transparency_entries = relationship("TransparencyEntry", back_populates="mp", cascade="all,delete")
