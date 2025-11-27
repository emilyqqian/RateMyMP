from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, Iterator, List, Optional

import httpx

from urllib.parse import urlencode, urljoin

logger = logging.getLogger(__name__)

OPENPARLIAMENT_BASE = "https://api.openparliament.ca"


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


def _build_openparliament_url(path_or_url: str, params: Optional[Dict[str, Any]] = None) -> str:
    if path_or_url.startswith("http"):
        url = path_or_url
    else:
        url = urljoin(OPENPARLIAMENT_BASE, path_or_url)
    separator = "&" if "?" in url else "?"
    if "format=" not in url:
        url = f"{url}{separator}format=json"
    if params:
        query = urlencode(params)
        url = f"{url}&{query}"
    return url


def fetch_openparliament(path_or_url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = _build_openparliament_url(path_or_url, params)
    return fetch_json(url)


def paginate_openparliament(
    resource_path: str,
    page_size: int = 100,
    max_records: Optional[int] = None,
) -> Iterator[Dict[str, Any]]:
    fetched = 0
    next_url: Optional[str] = f"{resource_path}?limit={page_size}"
    while next_url:
        data = fetch_openparliament(next_url)
        objects: Iterable[Dict[str, Any]] = data.get("objects", [])
        for obj in objects:
            yield obj
            fetched += 1
            if max_records is not None and fetched >= max_records:
                return
        next_url = data.get("pagination", {}).get("next_url")


def extract_parl_mp_id(detail: Dict[str, Any]) -> Optional[int]:
    other = detail.get("other_info") or {}
    candidates = other.get("parl_mp_id") or other.get("parl_affil_id") or []
    for candidate in candidates:
        try:
            return int(candidate)
        except (TypeError, ValueError):
            continue
    return None


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
