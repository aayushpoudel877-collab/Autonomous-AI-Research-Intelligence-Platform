from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return an aware UTC timestamp for reproducible service boundaries."""
    return datetime.now(UTC)
