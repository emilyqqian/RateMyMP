from sqlalchemy import ARRAY, Boolean, Column, Date, Enum, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import MotionClassification


class Motion(Base):
    __tablename__ = "motions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    introduced_by_mp_id = Column(Integer, ForeignKey("mps.id"), nullable=False)
    introduced_by_party = Column(String)
    vote_results_by_party = Column(JSON)
    passed = Column(Boolean, default=False)
    categories = Column(ARRAY(String))
    classification = Column(
        Enum(
            MotionClassification,
            name="motionclassification",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )
    date = Column(Date)

    introduced_by_mp = relationship("MP", back_populates="motions")
    votes = relationship("VoteRecord", back_populates="motion", cascade="all,delete")
    speeches = relationship("Speech", back_populates="motion", cascade="all,delete")
