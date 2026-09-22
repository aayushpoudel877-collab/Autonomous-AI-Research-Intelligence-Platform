from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass(frozen=True)
class PlatformEvent:
    name: str
    payload: dict[str, object] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
