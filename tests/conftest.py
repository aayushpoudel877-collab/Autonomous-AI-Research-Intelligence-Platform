import pytest
from nexus.retrieval.in_memory import InMemoryRetriever
@pytest.fixture
def retriever(): return InMemoryRetriever()
