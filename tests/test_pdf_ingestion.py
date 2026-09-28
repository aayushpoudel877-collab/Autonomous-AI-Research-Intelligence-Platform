import pytest

from nexus.ingestion.pdf import PDFIngestor


def test_pdf_ingestor_rejects_non_pdf(tmp_path):
    path = tmp_path / "note.txt"
    path.write_text("not a pdf", encoding="utf-8")
    with pytest.raises(ValueError, match=".pdf"):
        PDFIngestor().ingest(str(path))
