from dataclasses import dataclass, field

@dataclass
class Metadata:
    source: str = "unknown"
    language: str = "und"
    attributes: dict[str, str] = field(default_factory=dict)

    def with_attribute(self, key: str, value: str) -> "Metadata":
        self.attributes[key] = value
        return self
