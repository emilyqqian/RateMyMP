from __future__ import annotations

import logging
from datetime import date
from typing import Any, Dict, List

from app.models import Motion
from app.models.enums import MotionClassification
from app.services.data_ingestion.common import fetch_html, normalize_list, upsert_entities

logger = logging.getLogger(__name__)

OUR_COMMONS_VOTES = "https://www.ourcommons.ca/members/en/votes"
OPEN_PARLIAMENT_BILLS = "https://openparliament.ca/bills/"


def scrape_motions() -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for url in [OUR_COMMONS_VOTES, OPEN_PARLIAMENT_BILLS]:
        try:
            html = fetch_html(url)
            records.append(
                {
                    "id": len(records) + 1,
                    "title": f"Motion scraped from {url}",
                    "description": html[:500],
                    "introduced_by_mp_id": 1,
                    "introduced_by_party": "Unknown",
                    "vote_results_by_party": {},
                    "passed": False,
                    "categories": ["general"],
                    "classification": MotionClassification.SUBSTANTIVE,
                    "date": date.today(),
                }
            )
        except Exception as exc:  # pragma: no cover - network dependent
            logger.warning("Failed to fetch %s: %s", url, exc)
    if not records:
        records = [
            {
                "id": 1,
                "title": "Placeholder Motion",
                "description": "Placeholder motion description; replace via ingestion.",
                "introduced_by_mp_id": 1,
                "introduced_by_party": "Independent",
                "vote_results_by_party": {"Independent": {"yea": 1, "nay": 0}},
                "passed": True,
                "categories": ["governance"],
                "classification": MotionClassification.SUBSTANTIVE,
                "date": date.today(),
            }
        ]
    return records


def normalize_motion(record: Dict[str, Any]) -> Dict[str, Any]:
    record["categories"] = normalize_list(record.get("categories"))
    classification = record.get("classification", MotionClassification.SUBSTANTIVE)
    classification_enum = classification
    if not isinstance(classification_enum, MotionClassification):
        normalized_value = str(classification).lower()
        if "motionclassification." in normalized_value:
            normalized_value = normalized_value.split("motionclassification.", 1)[1]
        try:
            classification_enum = MotionClassification(normalized_value)
        except ValueError:
            classification_enum = MotionClassification.SUBSTANTIVE
    record["classification"] = classification_enum.value
    return record


def ingest_motions(db_session) -> int:
    raw_records = scrape_motions()
    normalized = [normalize_motion(record) for record in raw_records]
    return upsert_entities(db_session, Motion, normalized)
