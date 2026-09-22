from dataclasses import dataclass
@dataclass(frozen=True)
class IngestionSchema:
    required_fields: tuple[str,...]=("text","source_uri")
    def validate(self, record: dict[str,object])->bool:
        return all(field in record for field in self.required_fields)
