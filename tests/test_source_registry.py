from datetime import UTC, datetime, timedelta

from nexus.research.registry import SourceRecord


def test_source_record_age_is_non_negative():
    record = SourceRecord(
        "https://example.com/",
        "hash",
        0.5,
        (datetime.now(UTC) - timedelta(days=1)).isoformat(),
        2,
    )
    assert record.age_days >= 0
