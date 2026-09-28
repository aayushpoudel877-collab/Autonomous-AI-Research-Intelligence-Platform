from dataclasses import dataclass, field


@dataclass(frozen=True)
class Node:
    id: str
    label: str
    kind: str = "entity"
    mentions: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str
    confidence: float = 1.0
    evidence_chunk_id: str = ""
    source_uri: str = ""
