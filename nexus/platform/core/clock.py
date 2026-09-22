from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return an aware UTC timestamp for reproducible service boundaries."""
    return datetime.now(timezone.utc)
