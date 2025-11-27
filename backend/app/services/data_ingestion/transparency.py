from __future__ import annotations

import logging
from datetime import date
from typing import Dict, List

from app.models import TransparencyEntry
from app.services.data_ingestion.common import fetch_html, upsert_entities

logger = logging.getLogger(__name__)

ETHICS_REGISTRY_URL = (
    "https://prciec-rpccie.parl.gc.ca/EN/PublicRegistries/Pages/PublicRegistryCode.aspx"
)


def scrape_transparency() -> List[Dict[str, Any]]:
    try:
        html = fetch_html(ETHICS_REGISTRY_URL)
        return [
            {
                "id": 1,
                "mp_id": 1,
                "registry_type": "Ethics",
                "details": html[:1000],
                "filed_date": date.today(),
            }
        ]
    except Exception as exc:  # pragma: no cover - network dependent
        logger.warning("Failed to fetch transparency registry: %s", exc)
        return [
            {
                "id": 1,
                "mp_id": 1,
                "registry_type": "Placeholder",
                "details": "No data available",
                "filed_date": date.today(),
            }
        ]


def ingest_transparency(db_session) -> int:
    records = scrape_transparency()
    return upsert_entities(db_session, TransparencyEntry, records)
