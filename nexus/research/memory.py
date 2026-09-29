from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchMemory:
    question: str
    plan: tuple[str, ...]
    evidence_count: int
    graph_fact_count: int
    citation_integrity: float


class ResearchMemoryStore:
    def __init__(self, sqlite_store):
        self.store = sqlite_store

    def remember(self, memory: ResearchMemory) -> None:
        self.store.save_research_memory(memory)

    def recent(self, limit: int = 10) -> list[ResearchMemory]:
        return self.store.load_research_memory(limit)
