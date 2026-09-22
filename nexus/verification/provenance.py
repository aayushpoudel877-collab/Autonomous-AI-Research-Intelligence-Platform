from dataclasses import dataclass
@dataclass(frozen=True)
class Provenance:
    source_uri:str
    content_hash:str
    retrieved_at:str
