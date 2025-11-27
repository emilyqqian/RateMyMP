from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from app.models import MP
from app.services.data_ingestion.common import (
    OPENPARLIAMENT_BASE,
    extract_parl_mp_id,
    fetch_openparliament,
    paginate_openparliament,
    upsert_entities,
)

logger = logging.getLogger(__name__)

MAX_POLITICIANS = 400


def _absolute_photo_url(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    return f"{OPENPARLIAMENT_BASE.rstrip('/')}{path}"


def _extract_mp_id(detail: Dict[str, Any]) -> int:
    extracted = extract_parl_mp_id(detail)
    if extracted:
        return extracted
    # Fallback: hash the unique politician slug for deterministic ID
    fallback = abs(hash(detail.get("url"))) % 10_000_000
    return fallback or 1


def _years_in_office(detail: Dict[str, Any]) -> Optional[int]:
    memberships = detail.get("memberships") or []
    start_dates = []
    for membership in memberships:
        start = membership.get("start_date")
        if start:
            try:
                start_dates.append(datetime.fromisoformat(start).date())
            except ValueError:
                continue
    if not start_dates:
        return None
    earliest = min(start_dates)
    return max(0, date.today().year - earliest.year)


def _current_riding(detail: Dict[str, Any]) -> str:
    current = detail.get("memberships") or []
    if current:
        latest = current[-1]
        riding = latest.get("riding", {}).get("name", {}).get("en")
        if riding:
            return riding
    riding = detail.get("current_riding", {}).get("name", {}).get("en")
    return riding or "Unknown Riding"


def _current_party(detail: Dict[str, Any]) -> str:
    party = detail.get("current_party", {}).get("short_name", {}).get("en")
    if party:
        return party
    memberships = detail.get("memberships") or []
    if memberships:
        party = memberships[-1].get("party", {}).get("short_name", {}).get("en")
        if party:
            return party
    return "Independent"


def scrape_mps() -> List[Dict[str, Any]]:
    details: List[Dict[str, Any]] = []
    for summary in paginate_openparliament("/politicians/", page_size=100, max_records=MAX_POLITICIANS):
        try:
            detail = fetch_openparliament(summary["url"])
            details.append(detail)
        except Exception as exc:  # pragma: no cover - network issues
            logger.warning("Failed to download politician detail %s: %s", summary.get("url"), exc)
    return details


def normalize_mp(detail: Dict[str, Any]) -> Dict[str, Any]:
    mp_id = _extract_mp_id(detail)
    normalized = {
        "id": mp_id,
        "name": detail.get("name", "Unknown"),
        "riding": _current_riding(detail),
        "party": _current_party(detail),
        "photo_url": _absolute_photo_url(detail.get("image")),
        "attendance_rate": None,
        "party_line_voting_rate": None,
        "years_in_office": _years_in_office(detail),
    }
    return normalized


def ingest_mps(db_session) -> int:
    raw_records = scrape_mps()
    normalized = [normalize_mp(record) for record in raw_records]
    return upsert_entities(db_session, MP, normalized)
