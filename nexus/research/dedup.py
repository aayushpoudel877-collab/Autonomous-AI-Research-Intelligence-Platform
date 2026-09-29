import hashlib
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DedupKey:
    canonical_url: str
    content_hash: str


def content_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text).strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


class SourceDeduplicator:
    def __init__(self):
        self._seen: set[DedupKey] = set()

    def accept(self, canonical_url: str, text: str) -> bool:
        key = DedupKey(canonical_url, content_hash(text))
        if key in self._seen:
            return False
        self._seen.add(key)
        return True
