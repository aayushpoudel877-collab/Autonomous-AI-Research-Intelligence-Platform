from dataclasses import dataclass
from time import monotonic

@dataclass
class HealthState:
    name: str
    healthy: bool = True
    checked_at: float = 0.0

    def check(self, healthy: bool) -> None:
        self.healthy = healthy
        self.checked_at = monotonic()
