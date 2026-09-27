from nexus.types import Chunk


def test_retrieval_returns_evidence(retriever):
    retriever.add([Chunk("1", "d", "machine learning models", 0, {"source_uri": "x"}), Chunk("2", "d", "cooking recipes", 1, {})])
    results = retriever.search("machine learning", 1)
    assert results and results[0].chunk_id == "1"


def test_retrieval_honors_top_k(retriever):
    retriever.add([Chunk(str(i), "d", f"machine learning topic {i}", i, {}) for i in range(4)])
    assert len(retriever.search("machine learning", top_k=2)) == 2
