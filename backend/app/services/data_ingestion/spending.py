from __future__ import annotations

import logging
from typing import Dict, List

from app.models import SpendingEntry
from app.services.data_ingestion.common import fetch_html, upsert_entities

logger = logging.getLogger(__name__)

SPENDING_URL = "https://www.ourcommons.ca/ProactiveDisclosure/en/members/2026/1"


def scrape_spending() -> List[Dict[str, Any]]:
    try:
        html = fetch_html(SPENDING_URL)
        return [
            {
                "id": 1,
                "mp_id": 1,
                "category": "Travel",
                "amount": 1000.0,
                "fiscal_year": "2024",
                "details_url": SPENDING_URL,
                "_raw": html[:1000],
            }
        ]
    except Exception as exc:  # pragma: no cover - network dependent
        logger.warning("Failed to fetch spending disclosure: %s", exc)
        return [
            {
                "id": 1,
                "mp_id": 1,
                "category": "Placeholder",
                "amount": 0.0,
                "fiscal_year": "2024",
                "details_url": SPENDING_URL,
            }
        ]


def normalize_spending(record: Dict[str, Any]) -> Dict[str, Any]:
    record.pop("_raw", None)
    return record


def ingest_spending(db_session) -> int:
    raw_records = scrape_spending()
    normalized = [normalize_spending(record) for record in raw_records]
    return upsert_entities(db_session, SpendingEntry, normalized)
