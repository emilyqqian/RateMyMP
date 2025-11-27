"""Command-line entrypoint for data ingestion pipelines."""

import logging

from app.core.database import SessionLocal
from app.services.data_ingestion.motions import ingest_motions
from app.services.data_ingestion.mps import ingest_mps
from app.services.data_ingestion.spending import ingest_spending
from app.services.data_ingestion.transparency import ingest_transparency
from app.utils.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    session = SessionLocal()
    try:
        logger.info("Starting data ingestion run")
        mp_count = ingest_mps(session)
        motion_count = ingest_motions(session)
        spending_count = ingest_spending(session)
        transparency_count = ingest_transparency(session)
        logger.info(
            "Ingestion complete | MPs=%s Motions=%s Spending=%s Transparency=%s",
            mp_count,
            motion_count,
            spending_count,
            transparency_count,
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
