import re

from nexus.graph.model import Edge, Node
from nexus.utils import stable_id

_ENTITY = re.compile(r"\b[A-Z][A-Za-z0-9_-]{2,}(?:\s+[A-Z][A-Za-z0-9_-]{2,}){0,3}\b")
_RELATION = re.compile(
    r"(?P<a>\b[A-Z][A-Za-z0-9_-]{2,}(?:\s+[A-Z][A-Za-z0-9_-]{2,}){0,2})\s+"
    r"(?P<rel>supports|uses|powers|enables|depends on|contains|includes|improves|"
    r"influences|develops|builds|is|are)\s+"
    r"(?P<b>\b[A-Z][A-Za-z0-9_-]{2,}(?:\s+[A-Z][A-Za-z0-9_-]{2,}){0,2})"
)


class EntityGraphExtractor:
    def extract(self, text: str, chunk_id: str = "", source_uri: str = "") -> tuple[list[Node], list[Edge]]:
        labels = list(dict.fromkeys(_ENTITY.findall(text)))
        nodes = [Node(stable_id("entity", label.lower()), label, "entity", (chunk_id,) if chunk_id else ()) for label in labels]
        by_label = {n.label.lower(): n for n in nodes}
        edges: list[Edge] = []
        for match in _RELATION.finditer(text):
            a, b = match.group("a").strip(), match.group("b").strip()
            left, right = by_label.get(a.lower()), by_label.get(b.lower())
            if left and right and left.id != right.id:
                edges.append(Edge(left.id, right.id, match.group("rel").lower(), 0.85, chunk_id, source_uri))
        if not edges:
            for left, right in zip(nodes, nodes[1:]):
                edges.append(Edge(left.id, right.id, "co_occurs", 0.35, chunk_id, source_uri))
        return nodes, edges
