from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass(frozen=True)
class DomainEvent:
    event_type: str
    payload: dict[str, Any]
    timestamp: datetime
