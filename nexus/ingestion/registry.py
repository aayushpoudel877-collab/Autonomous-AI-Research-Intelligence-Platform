from nexus.ingestion.file import FileIngestor
from nexus.ingestion.text import TextIngestor

INGESTORS = {"text": TextIngestor(), "file": FileIngestor()}

def get_ingestor(kind: str):
    try: return INGESTORS[kind]
    except KeyError as exc: raise ValueError(f"Unsupported ingestor: {kind}") from exc
