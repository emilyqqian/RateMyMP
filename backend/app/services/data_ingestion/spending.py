from __future__ import annotations

import hashlib
import logging
from typing import Any, Dict, List

from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.models import MP, SpendingEntry
from app.services.data_ingestion.common import fetch_html, upsert_entities

logger = logging.getLogger(__name__)

SPENDING_YEAR = 2026
SPENDING_QUARTER = 1
SPENDING_URL = f"https://www.ourcommons.ca/ProactiveDisclosure/en/members/{SPENDING_YEAR}/{SPENDING_QUARTER}"
CATEGORIES = ["Salaries", "Travel", "Hospitality", "Contracts"]


def _normalize_name(value: str) -> str:
    if "," in value:
        last, first = value.split(",", 1)
        return f"{first.strip()} {last.strip()}"
    return value.strip()


def _parse_currency(value: str) -> float:
    cleaned = value.replace("$", "").replace(",", "").strip()
    if not cleaned:
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _deterministic_id(key: str) -> int:
    digest = hashlib.sha1(key.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) & 0x7FFFFFFF


def _build_mp_index(db_session: Session) -> Dict[str, int]:
    return {mp.name.lower(): mp.id for mp in db_session.query(MP).all()}


def scrape_spending_rows() -> List[Dict[str, Any]]:
    html = fetch_html(SPENDING_URL)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        logger.warning("Spending table not found on %s", SPENDING_URL)
        return []

    rows: List[Dict[str, Any]] = []
    for tr in table.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cells) < 7:
            continue
        entry = {
            "name": _normalize_name(cells[0]),
            "riding": cells[1],
            "party": cells[2],
            "amounts": {
                "Salaries": _parse_currency(cells[3]),
                "Travel": _parse_currency(cells[4]),
                "Hospitality": _parse_currency(cells[5]),
                "Contracts": _parse_currency(cells[6]),
            },
        }
        rows.append(entry)
    return rows


def expand_spending_entries(rows: List[Dict[str, Any]], db_session: Session) -> List[Dict[str, Any]]:
    mp_index = _build_mp_index(db_session)
    fiscal_label = f"{SPENDING_YEAR}-Q{SPENDING_QUARTER}"
    entries: List[Dict[str, Any]] = []

    for row in rows:
        mp_id = mp_index.get(row["name"].lower())
        if not mp_id:
            logger.debug("Skipping spending row for %s; MP not found", row["name"])
            continue
        for category, amount in row["amounts"].items():
            key = f"{mp_id}:{category}:{fiscal_label}"
            entry_id = _deterministic_id(key)
            entries.append(
                {
                    "id": entry_id,
                    "mp_id": mp_id,
                    "category": category,
                    "amount": amount,
                    "fiscal_year": fiscal_label,
                    "details_url": SPENDING_URL,
                }
            )
    return entries


def ingest_spending(db_session) -> int:
    rows = scrape_spending_rows()
    normalized = expand_spending_entries(rows, db_session)
    return upsert_entities(db_session, SpendingEntry, normalized)
