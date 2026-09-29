from nexus.graph.model import Edge, Node
from nexus.graph.store import GraphStore
from nexus.storage.sqlite import SQLiteStore


def test_graph_persistence(tmp_path):
    storage = SQLiteStore(tmp_path / "nexus.db")
    graph = GraphStore(storage)
    a, b = Node("a", "Alpha"), Node("b", "Beta")
    graph.add([a, b], [Edge("a", "b", "supports", 0.8, "c1", "local")])
    nodes, edges = storage.load_graph()
    assert {n.label for n in nodes} == {"Alpha", "Beta"}
    assert edges[0].relation == "supports"
