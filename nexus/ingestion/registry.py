from nexus.ingestion.file import FileIngestor
from nexus.ingestion.text import TextIngestor
from nexus.ingestion.web import URLIngestor

INGESTORS = {"text": TextIngestor(), "file": FileIngestor(), "url": URLIngestor()}


def get_ingestor(kind: str):
    try:
        return INGESTORS[kind]
    except KeyError as exc:
        raise ValueError(f"Unsupported ingestor: {kind}") from exc
