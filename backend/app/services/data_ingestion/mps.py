from __future__ import annotations

import logging
from typing import Any, Dict, List

from app.models import MP
from app.services.data_ingestion.common import fetch_html, upsert_entities

logger = logging.getLogger(__name__)

OUR_COMMONS_CONSTITUENCIES = "https://www.ourcommons.ca/members/en/constituencies"
OPEN_PARLIAMENT_POLITICIANS = "https://openparliament.ca/politicians/"


def _placeholder_mp_payload() -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "name": "Sample MP",
            "riding": "Demo Riding",
            "party": "Independent",
            "photo_url": None,
            "attendance_rate": 0.95,
            "party_line_voting_rate": 0.7,
            "years_in_office": 2,
        }
    ]


def fetch_mp_sources() -> List[str]:
    return [OUR_COMMONS_CONSTITUENCIES, OPEN_PARLIAMENT_POLITICIANS]


def scrape_mps() -> List[Dict[str, Any]]:
    payload: List[Dict[str, Any]] = []
    for url in fetch_mp_sources():
        try:
            html = fetch_html(url)
            payload.append(
                {
                    "id": len(payload) + 1,
                    "name": f"Scraped MP #{len(payload) + 1}",
                    "riding": "Unknown",
                    "party": "Unknown",
                    "photo_url": None,
                    "attendance_rate": None,
                    "party_line_voting_rate": None,
                    "years_in_office": None,
                    "_source": url,
                    "_raw": html[:2000],  # keep snippet for debugging
                }
            )
        except Exception as exc:  # pragma: no cover - network dependent
            logger.warning("Failed to scrape %s: %s", url, exc)
    if not payload:
        payload = _placeholder_mp_payload()
    return payload


def normalize_mp(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": record.get("id"),
        "name": record.get("name", "Unknown"),
        "riding": record.get("riding", "Unknown Riding"),
        "party": record.get("party", "Unknown Party"),
        "photo_url": record.get("photo_url"),
        "attendance_rate": record.get("attendance_rate"),
        "party_line_voting_rate": record.get("party_line_voting_rate"),
        "years_in_office": record.get("years_in_office"),
    }


def ingest_mps(db_session) -> int:
    raw_records = scrape_mps()
    normalized = [normalize_mp(record) for record in raw_records]
    return upsert_entities(db_session, MP, normalized)
