from nexus.graph.model import Edge, Node


class GraphStore:
    """Deterministic graph with optional SQLite persistence and provenance-aware edges."""

    def __init__(self, storage=None):
        self.storage = storage
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        if edge not in self.edges:
            self.edges.append(edge)

    def add(self, nodes: list[Node], edges: list[Edge]) -> None:
        for node in nodes:
            self.add_node(node)
        for edge in edges:
            self.add_edge(edge)
        if self.storage:
            self.storage.save_graph(nodes, edges)

    def neighbors(self, node_id: str, hops: int = 1) -> list[str]:
        if hops < 1:
            return []
        frontier, seen = {node_id}, {node_id}
        for _ in range(hops):
            nxt = {e.target for e in self.edges if e.source in frontier}
            nxt |= {e.source for e in self.edges if e.target in frontier}
            nxt -= seen
            seen |= nxt
            frontier = nxt
        return sorted(seen - {node_id})

    def edges_for(self, node_ids: set[str]) -> list[Edge]:
        return [e for e in self.edges if e.source in node_ids or e.target in node_ids]

    def facts_for(self, node_ids: set[str], hops: int = 1) -> list[Edge]:
        expanded = set(node_ids)
        for node_id in node_ids:
            expanded.update(self.neighbors(node_id, hops=hops))
        return self.edges_for(expanded)

    def load(self, nodes: list[Node], edges: list[Edge]) -> None:
        for node in nodes:
            self.add_node(node)
        for edge in edges:
            self.add_edge(edge)
