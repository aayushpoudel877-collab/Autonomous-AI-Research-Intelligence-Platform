from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class Provenance:
    source_uri: str
    content_hash: str
    retrieved_at: str


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
