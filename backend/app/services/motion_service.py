from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Motion as MotionModel, MP, VoteRecord
from app.models.enums import VoteChoice
from app.schemas import AISummaryResponse, MotionVoteResponse


class MotionService:
    """Encapsulates business logic for working with motions."""

    def __init__(self, db: Session):
        self.db = db

    def list_motions(self) -> List[MotionModel]:
        return self.db.query(MotionModel).order_by(MotionModel.date.desc().nullslast()).all()

    def get_motion(self, motion_id: int) -> MotionModel:
        motion = self.db.query(MotionModel).filter(MotionModel.id == motion_id).first()
        if not motion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motion not found")
        return motion

    def get_ai_summary(self, motion_id: int) -> AISummaryResponse:
        motion = self.get_motion(motion_id)
        summary = (
            f"This is a placeholder AI summary for '{motion.title}'. "
            "Integrate your preferred LLM provider to replace this text."
        )
        return AISummaryResponse(motion_id=motion.id, summary=summary)

    def vote_on_motion(self, motion_id: int, mp_id: int, vote: str) -> MotionVoteResponse:
        motion = self.get_motion(motion_id)
        mp = self.db.query(MP).filter(MP.id == mp_id).first()
        if not mp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MP not found")

        normalized_vote = VoteChoice.YEA if vote == "upvote" else VoteChoice.NAY

        record = (
            self.db.query(VoteRecord)
            .filter(VoteRecord.motion_id == motion.id, VoteRecord.mp_id == mp.id)
            .first()
        )
        if record:
            record.vote = normalized_vote
        else:
            record = VoteRecord(motion_id=motion.id, mp_id=mp.id, vote=normalized_vote)
            self.db.add(record)

        self.db.commit()
        self.db.refresh(record)

        return MotionVoteResponse(motion_id=motion.id, mp_id=mp.id, vote=vote)
