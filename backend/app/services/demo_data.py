"""Developer-friendly seed data so the API works without a full ingest."""

from __future__ import annotations

from datetime import date
from typing import Dict, List

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import MP, Motion, SpendingEntry, Speech, TransparencyEntry, VoteRecord
from app.models.enums import MotionClassification, VoteChoice


def _upsert(session: Session, model, payload: Dict) -> None:
    instance = session.get(model, payload["id"])
    if instance:
        for key, value in payload.items():
            setattr(instance, key, value)
        return
    session.add(model(**payload))


DEMO_MPS: List[Dict] = [
    {
        "id": 1,
        "name": "John Smith",
        "riding": "Toronto Centre",
        "party": "Liberal",
        "photo_url": None,
        "attendance_rate": 94.0,
        "party_line_voting_rate": 87.0,
        "years_in_office": 6,
    },
    {
        "id": 2,
        "name": "Marie Leclerc",
        "riding": "Rosemont—La Petite-Patrie",
        "party": "NDP",
        "photo_url": None,
        "attendance_rate": 91.0,
        "party_line_voting_rate": 82.0,
        "years_in_office": 4,
    },
]

DEMO_MOTIONS: List[Dict] = [
    {
        "id": 1,
        "title": "Bill C-15: An Act to amend the Canada Health Act",
        "description": "Amendment to expand coverage for mental health services",
        "introduced_by_mp_id": 1,
        "introduced_by_party": "Liberal",
        "vote_results_by_party": {
            "Liberal": {"yea": 155, "nay": 0, "abstain": 3},
            "Conservative": {"yea": 25, "nay": 94, "abstain": 0},
            "NDP": {"yea": 24, "nay": 0, "abstain": 1},
            "Bloc Québécois": {"yea": 32, "nay": 0, "abstain": 0},
            "Green": {"yea": 2, "nay": 0, "abstain": 0},
        },
        "passed": True,
        "categories": ["healthcare"],
        "classification": MotionClassification.SUBSTANTIVE,
        "date": date(2024, 11, 15),
    },
    {
        "id": 2,
        "title": "Motion M-47: Climate Emergency Response Fund",
        "description": "Establish a $10B fund for climate adaptation infrastructure",
        "introduced_by_mp_id": 2,
        "introduced_by_party": "NDP",
        "vote_results_by_party": {
            "Liberal": {"yea": 120, "nay": 38, "abstain": 0},
            "Conservative": {"yea": 0, "nay": 119, "abstain": 0},
            "NDP": {"yea": 25, "nay": 0, "abstain": 0},
            "Bloc Québécois": {"yea": 32, "nay": 0, "abstain": 0},
            "Green": {"yea": 2, "nay": 0, "abstain": 0},
        },
        "passed": False,
        "categories": ["environment/energy", "infrastructure"],
        "classification": MotionClassification.SUBSTANTIVE,
        "date": date(2024, 11, 20),
    },
]

DEMO_SPEECHES: List[Dict] = [
    {
        "id": 1,
        "mp_id": 1,
        "motion_id": 1,
        "title": "Second Reading Remarks on Bill C-15",
        "content": "Mental health parity is overdue. This legislation finally treats it as essential care.",
        "date": date(2024, 11, 16),
    },
    {
        "id": 2,
        "mp_id": 2,
        "motion_id": 2,
        "title": "Introducing the Climate Emergency Fund",
        "content": "Communities are on the frontlines of climate change. This fund is about resilience.",
        "date": date(2024, 11, 21),
    },
]

DEMO_VOTES: List[Dict] = [
    {"id": 1, "mp_id": 1, "motion_id": 1, "vote": VoteChoice.YEA},
    {"id": 2, "mp_id": 2, "motion_id": 1, "vote": VoteChoice.YEA},
    {"id": 3, "mp_id": 1, "motion_id": 2, "vote": VoteChoice.YEA},
    {"id": 4, "mp_id": 2, "motion_id": 2, "vote": VoteChoice.YEA},
]

DEMO_SPENDING: List[Dict] = [
    {
        "id": 1,
        "mp_id": 1,
        "category": "Constituency Operations",
        "amount": 325000.0,
        "fiscal_year": "2023-2024",
        "details_url": "https://www.ourcommons.ca/ProactiveDisclosure/en/members/2026/1",
    },
    {
        "id": 2,
        "mp_id": 1,
        "category": "Travel",
        "amount": 15251.40,
        "fiscal_year": "2023-2024",
        "details_url": "https://www.ourcommons.ca/ProactiveDisclosure/en/members/2026/1",
    },
    {
        "id": 3,
        "mp_id": 2,
        "category": "Constituency Operations",
        "amount": 287000.0,
        "fiscal_year": "2023-2024",
        "details_url": "https://www.ourcommons.ca/ProactiveDisclosure/en/members/2026/1",
    },
]

DEMO_TRANSPARENCY: List[Dict] = [
    {
        "id": 1,
        "mp_id": 1,
        "registry_type": "stock",
        "details": "Declared holdings in Canadian Clean Energy ETF.",
        "filed_date": date(2024, 5, 12),
    },
    {
        "id": 2,
        "mp_id": 2,
        "registry_type": "gift",
        "details": "Accepted travel sponsorship from Climate Action Network for UN summit.",
        "filed_date": date(2024, 9, 5),
    },
]


def seed_demo_data() -> None:
    session = SessionLocal()
    try:
        if session.query(MP).count() == 0:
            for mp in DEMO_MPS:
                _upsert(session, MP, mp)
        if session.query(Motion).count() == 0:
            for motion in DEMO_MOTIONS:
                _upsert(session, Motion, motion)
        if session.query(Speech).count() == 0:
            for speech in DEMO_SPEECHES:
                _upsert(session, Speech, speech)
        if session.query(VoteRecord).count() == 0:
            for vote in DEMO_VOTES:
                _upsert(session, VoteRecord, vote)
        if session.query(SpendingEntry).count() == 0:
            for entry in DEMO_SPENDING:
                _upsert(session, SpendingEntry, entry)
        if session.query(TransparencyEntry).count() == 0:
            for entry in DEMO_TRANSPARENCY:
                _upsert(session, TransparencyEntry, entry)
        session.commit()
    finally:
        session.close()

