from nexus.research.memory import ResearchMemory, ResearchMemoryStore
from nexus.storage.sqlite import SQLiteStore


def test_research_memory_round_trip(tmp_path):
    store = ResearchMemoryStore(SQLiteStore(tmp_path / "nexus.db"))
    item = ResearchMemory("What is NEXUS?", ("What is NEXUS?", "What evidence supports NEXUS?"), 3, 2, 1.0)
    store.remember(item)
    result = store.recent(1)[0]
    assert result.question == item.question
    assert result.evidence_count == 3
