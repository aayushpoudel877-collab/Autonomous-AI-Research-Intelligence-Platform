from nexus.agents.base import AgentContext
from nexus.agents.graph_retriever import GraphRetrievalAgent
from nexus.graph.extractor import EntityGraphExtractor
from nexus.graph.store import GraphStore
from nexus.types import Evidence


def test_relation_extraction_is_provenance_aware():
    nodes, edges = EntityGraphExtractor().extract("Python powers NEXUS Research.", "c1", "local")
    assert len(nodes) >= 2
    assert any(e.relation == "powers" and e.evidence_chunk_id == "c1" for e in edges)


def test_graph_retrieval_expands_one_hop():
    graph = GraphStore()
    agent = GraphRetrievalAgent(graph)
    ctx = AgentContext("What powers NEXUS?", evidence=[Evidence("c1", "Python powers NEXUS Research.", 0.9, "local")])
    agent.run(ctx)
    assert ctx.state["graph_facts"]
    assert any(f["relation"] == "powers" for f in ctx.state["graph_facts"])


def test_graph_store_neighbors_support_two_hops():
    nodes, edges = EntityGraphExtractor().extract("Alpha supports Beta. Beta supports Gamma.", "c1", "local")
    graph = GraphStore()
    graph.add(nodes, edges)
    alpha = next(n for n in nodes if n.label == "Alpha")
    assert graph.neighbors(alpha.id, hops=2)
