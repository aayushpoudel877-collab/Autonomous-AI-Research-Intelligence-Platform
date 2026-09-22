from abc import ABC, abstractmethod
from nexus.types import SourceDocument

class Ingestor(ABC):
    @abstractmethod
    def ingest(self, source: str) -> SourceDocument: ...
