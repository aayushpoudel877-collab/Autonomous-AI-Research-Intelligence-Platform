from pathlib import Path
from nexus.ingestion.base import Ingestor
from nexus.types import SourceDocument
from nexus.utils import clean_text, stable_id

class FileIngestor(Ingestor):
    def ingest(self, source: str) -> SourceDocument:
        path = Path(source)
        text = clean_text(path.read_text(encoding="utf-8"))
        return SourceDocument(stable_id(str(path), text), path.name, text, str(path))
