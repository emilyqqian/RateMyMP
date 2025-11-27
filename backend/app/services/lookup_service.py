from dataclasses import dataclass
from typing import Optional


@dataclass
class PostalCodeLookupResult:
    postal_code: str
    presumed_riding: str
    presumed_province: str
    mp_id: Optional[int]


class LookupService:
    """Provides helper lookups for frontend dropdowns and search."""

    def lookup_postal_code(self, code: str) -> PostalCodeLookupResult:
        formatted = code.upper().replace(" ", "")
        # Placeholder mapping; integrate Elections Canada API here later.
        return PostalCodeLookupResult(
            postal_code=formatted,
            presumed_riding="Placeholder Riding",
            presumed_province="ON",
            mp_id=None,
        )
