from dataclasses import dataclass

@dataclass(frozen=True)
class Page:
    offset: int
    limit: int

    def slice(self, values: list[object]) -> list[object]:
        if self.offset < 0 or self.limit < 0:
            raise ValueError("offset and limit must be non-negative")
        return values[self.offset:self.offset + self.limit]
