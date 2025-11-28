from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import VoteChoice


class VoteRecord(Base):
    __tablename__ = "vote_records"

    id = Column(Integer, primary_key=True, index=True)
    mp_id = Column(Integer, ForeignKey("mps.id"), nullable=False)
    motion_id = Column(Integer, ForeignKey("motions.id"), nullable=False)
    vote = Column(
        Enum(
            VoteChoice,
            name="votechoice",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )

    mp = relationship("MP", back_populates="votes")
    motion = relationship("Motion", back_populates="votes")
