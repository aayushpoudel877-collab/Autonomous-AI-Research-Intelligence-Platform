from dataclasses import dataclass

@dataclass
class Budget:
    limit: int
    used: int = 0

    @property
    def remaining(self) -> int:
        return max(0, self.limit - self.used)

    def consume(self, amount: int = 1) -> bool:
        if amount < 0 or self.used + amount > self.limit:
            return False
        self.used += amount
        return True
