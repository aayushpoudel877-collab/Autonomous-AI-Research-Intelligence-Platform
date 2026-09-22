from nexus.ingestion.base import Ingestor
from nexus.types import SourceDocument
from nexus.utils import clean_text, stable_id

class TextIngestor(Ingestor):
    def ingest(self, source: str) -> SourceDocument:
        text = clean_text(source)
        return SourceDocument(stable_id(text), "Text Input", text, "inline")
