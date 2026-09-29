from nexus.agents.base import AgentContext
from nexus.agents.retriever import RetrievalAgent
from nexus.types import Chunk


class FakeRetriever:
    def search(self, query, top_k=5):
        return [type("R", (), {"chunk_id": query, "document_id": "d", "text": query, "score": 1.0, "source_uri": "local"})()]


def test_retriever_merges_planned_queries():
    ctx = AgentContext("main")
    ctx.state["research_queries"] = ("first", "second")
    RetrievalAgent(FakeRetriever()).run(ctx)
    assert [x.chunk_id for x in ctx.evidence] == ["first", "second"]
