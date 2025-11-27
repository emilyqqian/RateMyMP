from typing import List

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import MP, Motion, SpendingEntry, Speech, TransparencyEntry, VoteRecord
from app.schemas import MP as MPSchema
from app.schemas import (
    MPActivity,
    MPSpendingSummary,
    MPTransparencySummary,
    MPVotingRecord,
    Speech as SpeechSchema,
    SpendingEntry as SpendingEntrySchema,
    TransparencyEntry as TransparencyEntrySchema,
)


class MPService:
    """Business logic for Member of Parliament resources."""

    def __init__(self, db: Session):
        self.db = db

    def list_mps(self) -> List[MPSchema]:
        return self.db.query(MP).order_by(MP.name.asc()).all()

    def get_mp(self, mp_id: int) -> MPSchema:
        mp = self.db.query(MP).filter(MP.id == mp_id).first()
        if not mp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MP not found")
        return mp

    def get_voting_record(self, mp_id: int) -> List[MPVotingRecord]:
        self.get_mp(mp_id)
        records = (
            self.db.query(VoteRecord, Motion)
            .join(Motion, VoteRecord.motion_id == Motion.id)
            .filter(VoteRecord.mp_id == mp_id)
            .order_by(Motion.date.desc().nullslast())
            .all()
        )
        return [
            MPVotingRecord(motion_id=motion.id, motion_title=motion.title, vote=vote.vote.value)
            for vote, motion in records
        ]

    def get_parliamentary_activity(self, mp_id: int) -> MPActivity:
        self.get_mp(mp_id)
        speeches_count = self.db.query(func.count(Speech.id)).filter(Speech.mp_id == mp_id).scalar() or 0
        motions_sponsored = self.db.query(func.count(Motion.id)).filter(Motion.introduced_by_mp_id == mp_id).scalar() or 0
        return MPActivity(speeches_count=speeches_count, motions_sponsored=motions_sponsored)

    def get_spending(self, mp_id: int) -> MPSpendingSummary:
        self.get_mp(mp_id)
        entries = (
            self.db.query(SpendingEntry)
            .filter(SpendingEntry.mp_id == mp_id)
            .order_by(SpendingEntry.fiscal_year.desc())
            .all()
        )
        total_amount = sum(entry.amount or 0 for entry in entries)
        entry_schemas = [
            SpendingEntrySchema(
                id=entry.id,
                mp_id=entry.mp_id,
                category=entry.category,
                amount=entry.amount,
                fiscal_year=entry.fiscal_year,
                details_url=entry.details_url,
            )
            for entry in entries
        ]
        return MPSpendingSummary(total_amount=total_amount, entries=entry_schemas)

    def get_transparency(self, mp_id: int) -> MPTransparencySummary:
        self.get_mp(mp_id)
        entries = (
            self.db.query(TransparencyEntry)
            .filter(TransparencyEntry.mp_id == mp_id)
            .order_by(TransparencyEntry.filed_date.desc().nullslast())
            .all()
        )
        entry_schemas = [
            TransparencyEntrySchema(
                id=entry.id,
                mp_id=entry.mp_id,
                registry_type=entry.registry_type,
                details=entry.details,
                filed_date=entry.filed_date,
            )
            for entry in entries
        ]
        return MPTransparencySummary(filings_count=len(entries), entries=entry_schemas)

    def get_speeches(self, mp_id: int) -> List[SpeechSchema]:
        self.get_mp(mp_id)
        speeches = (
            self.db.query(Speech)
            .filter(Speech.mp_id == mp_id)
            .order_by(Speech.date.desc().nullslast())
            .all()
        )
        return [
            SpeechSchema(
                id=speech.id,
                mp_id=speech.mp_id,
                motion_id=speech.motion_id,
                title=speech.title,
                content=speech.content,
                date=speech.date,
            )
            for speech in speeches
        ]
