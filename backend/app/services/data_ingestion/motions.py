from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models import MP, Motion
from app.models.enums import MotionClassification
from app.services.data_ingestion.common import (
    extract_parl_mp_id,
    fetch_openparliament,
    normalize_list,
    paginate_openparliament,
    upsert_entities,
)

logger = logging.getLogger(__name__)

MAX_BILLS = 75


class SponsorResolver:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.cache: Dict[str, Optional[int]] = {}
        self.fallback_mp_id: Optional[int] = self._get_fallback_mp_id()

    def _get_fallback_mp_id(self) -> Optional[int]:
        mp = self.db_session.query(MP).first()
        return mp.id if mp else None

    def resolve(self, sponsor_path: Optional[str]) -> Optional[int]:
        if not sponsor_path:
            return self.fallback_mp_id
        slug = sponsor_path.rstrip("/")
        if slug in self.cache:
            return self.cache[slug]
        try:
            detail = fetch_openparliament(sponsor_path)
        except Exception as exc:  # pragma: no cover - network dependent
            logger.warning("Failed to fetch sponsor detail %s: %s", sponsor_path, exc)
            self.cache[slug] = self.fallback_mp_id
            return self.fallback_mp_id
        mp_id = extract_parl_mp_id(detail)
        if mp_id is None:
            mp_id = self.fallback_mp_id
        else:
            mp = self.db_session.query(MP).filter(MP.id == mp_id).first()
            if not mp:
                logger.debug("Sponsor MP %s not found in DB; using fallback", mp_id)
                mp_id = self.fallback_mp_id
        self.cache[slug] = mp_id
        return mp_id


def _fetch_vote_summary(vote_urls: List[str]) -> Tuple[Dict[str, Dict[str, Any]], Optional[bool]]:
    for vote_url in vote_urls or []:
        try:
            vote = fetch_openparliament(vote_url)
        except Exception as exc:  # pragma: no cover - network dependent
            logger.warning("Failed to fetch vote %s: %s", vote_url, exc)
            continue
        party_votes = {}
        for entry in vote.get("party_votes", []):
            party = entry.get("party", {}).get("short_name", {}).get("en")
            if not party:
                continue
            party_votes[party] = {"vote": entry.get("vote")}
        result = vote.get("result", "").lower()
        passed = None
        if result:
            passed = any(keyword in result for keyword in ("passed", "agreed", "adopted", "royal assent"))
        if party_votes:
            return party_votes, passed
    return {}, None


def scrape_motions() -> List[Dict[str, Any]]:
    bills: List[Dict[str, Any]] = []
    for summary in paginate_openparliament("/bills/", page_size=50, max_records=MAX_BILLS):
        try:
            detail = fetch_openparliament(summary["url"])
            bills.append(detail)
        except Exception as exc:  # pragma: no cover - network dependent
            logger.warning("Failed to download bill detail %s: %s", summary.get("url"), exc)
    return bills


def normalize_motion(
    detail: Dict[str, Any],
    sponsor_resolver: SponsorResolver,
    db_session: Session,
) -> Optional[Dict[str, Any]]:
    categories = normalize_list(
        [
            detail.get("home_chamber"),
            f"Session {detail.get('session')}",
        ]
    )
    sponsor_mp_id = sponsor_resolver.resolve(detail.get("sponsor_politician_url"))
    vote_summary, vote_passed = _fetch_vote_summary(detail.get("vote_urls") or [])
    status_text = (detail.get("status") or {}).get("en", "")
    description = status_text or detail.get("short_title", {}).get("en") or detail.get("name", {}).get("en")
    introduced_str = detail.get("introduced")
    introduced_date = None
    if introduced_str:
        try:
            introduced_date = datetime.fromisoformat(introduced_str).date()
        except ValueError:
            try:
                introduced_date = datetime.strptime(introduced_str.split("T")[0], "%Y-%m-%d").date()
            except ValueError:
                introduced_date = date.today()
    classification = (
        MotionClassification.SUBSIDIARY if detail.get("private_member_bill") else MotionClassification.SUBSTANTIVE
    )
    passed = vote_passed
    if passed is None and status_text:
        lower_status = status_text.lower()
        passed = "law" in lower_status or "royal assent" in lower_status or "passed" in lower_status

    if sponsor_mp_id is None:
        logger.debug("Skipping motion %s due to missing sponsor MP", detail.get("url"))
        return None

    mp_party = None
    if sponsor_mp_id:
        mp = db_session.query(MP).filter(MP.id == sponsor_mp_id).first()
        mp_party = mp.party if mp else None

    return {
        "id": detail.get("legisinfo_id") or abs(hash(detail.get("url"))) % 10_000_000,
        "title": detail.get("name", {}).get("en", "Unknown Motion"),
        "description": description,
        "introduced_by_mp_id": sponsor_mp_id,
        "introduced_by_party": mp_party,
        "vote_results_by_party": vote_summary,
        "passed": bool(passed),
        "categories": categories,
        "classification": classification.value,
        "date": introduced_date or date.today(),
    }


def ingest_motions(db_session) -> int:
    sponsor_resolver = SponsorResolver(db_session)
    raw_records = scrape_motions()
    normalized: List[Dict[str, Any]] = []
    seen_ids: set[int] = set()
    for record in raw_records:
        normalized_motion = normalize_motion(record, sponsor_resolver, db_session)
        if not normalized_motion:
            continue
        motion_id = normalized_motion["id"]
        if motion_id in seen_ids:
            continue
        seen_ids.add(motion_id)
        normalized.append(normalized_motion)
    return upsert_entities(db_session, Motion, normalized)
