from __future__ import annotations

import logging
from typing import Any, Dict, List

import httpx

logger = logging.getLogger(__name__)


def fetch_json(url: str) -> Any:
    logger.info("Fetching %s", url)
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def fetch_html(url: str) -> str:
    logger.info("Fetching %s", url)
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text


def normalize_list(values: List[str] | None) -> List[str]:
    return [value.strip() for value in values or [] if value]


def upsert_entities(db_session, model, data: List[Dict[str, Any]], lookup_field: str = "id") -> int:
    """Simple bulk upsert helper used by ingestion tasks."""

    updated = 0
    for item in data:
        lookup_value = item.get(lookup_field)
        instance = None
        if lookup_value is not None:
            instance = db_session.query(model).filter(getattr(model, lookup_field) == lookup_value).first()
        if instance:
            for key, value in item.items():
                setattr(instance, key, value)
        else:
            instance = model(**item)
            db_session.add(instance)
        updated += 1
    db_session.commit()
    return updated
