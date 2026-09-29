from nexus.retrieval.in_memory import InMemoryRetriever
from nexus.types import Chunk


def test_retriever_replaces_duplicate_chunk_ids():
    retriever = InMemoryRetriever()
    retriever.add([Chunk("same", "d", "first text", 0, {})])
    retriever.add([Chunk("same", "d", "updated text", 0, {})])
    assert len(retriever.items) == 1
    assert retriever.items[0].text == "updated text"
