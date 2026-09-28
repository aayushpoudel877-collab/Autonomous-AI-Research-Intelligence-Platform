from pathlib import Path

from nexus.ingestion.base import Ingestor
from nexus.security.limits import validate_bytes_size
from nexus.types import SourceDocument
from nexus.utils import clean_text, stable_id


class PDFIngestor(Ingestor):
    """Extract text from a local PDF with a bounded file size."""

    def __init__(self, max_bytes=10_000_000):
        self.max_bytes = max_bytes

    def ingest(self, source: str) -> SourceDocument:
        path = Path(source)
        if path.suffix.lower() != ".pdf":
            raise ValueError("PDF ingestor requires a .pdf file")
        payload = path.read_bytes()
        validate_bytes_size(payload, self.max_bytes)
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("PDF ingestion requires the pypdf dependency") from exc
        reader = PdfReader(path)
        pages = []
        for index, page in enumerate(reader.pages, start=1):
            text = clean_text(page.extract_text() or "")
            if text:
                pages.append(f"[Page {index}]\\n{text}")
        text = clean_text("\\n\\n".join(pages))
        if not text:
            raise ValueError("PDF contained no extractable text")
        metadata = {"content_type": "application/pdf", "page_count": len(reader.pages)}
        return SourceDocument(stable_id(str(path), text), path.name, text, str(path), metadata)
