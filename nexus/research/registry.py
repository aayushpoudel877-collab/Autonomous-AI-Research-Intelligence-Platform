from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class SourceRecord:
    canonical_url: str
    content_hash: str
    quality: float
    fetched_at: str
    version: int

    @property
    def age_days(self) -> float:
        fetched = datetime.fromisoformat(self.fetched_at)
        return max(0.0, (datetime.now(UTC) - fetched).total_seconds() / 86400)


class SourceRegistry:
    """Persistent-source policy facade.

    Storage owns durability; this class owns cache/freshness decisions.
    """

    def __init__(self, storage):
        self.storage = storage

    def get(self, canonical_url: str) -> SourceRecord | None:
        row = self.storage.get_acquired_source(canonical_url)
        if not row:
            return None
        return SourceRecord(
            canonical_url=row["canonical_url"],
            content_hash=row["content_hash"],
            quality=float(row["quality"]),
            fetched_at=row["fetched_at"],
            version=int(row["version"]),
        )

    def is_fresh(self, canonical_url: str, max_age_days: float) -> bool:
        record = self.get(canonical_url)
        return bool(record and record.age_days <= max(0.0, max_age_days))
