from dataclasses import dataclass, field
from datetime import UTC, datetime

@dataclass(frozen=True)
class PlatformEvent:
    name: str
    payload: dict[str, object] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
