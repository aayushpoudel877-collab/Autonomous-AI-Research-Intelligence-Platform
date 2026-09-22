from dataclasses import dataclass

@dataclass(frozen=True)
class Node:
    id: str
    label: str
    kind: str

@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str
