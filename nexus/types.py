from dataclasses import dataclass, field
from typing import Any

@dataclass
class SourceDocument:
    document_id: str
    title: str
    text: str
    source_uri: str = "local"
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    text: str
    index: int
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Evidence:
    chunk_id: str
    text: str
    score: float
    source_uri: str

@dataclass
class Claim:
    statement: str
    evidence: list[Evidence] = field(default_factory=list)
    confidence: float = 0.0
