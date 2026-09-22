from nexus.types import SourceDocument
from nexus.utils import clean_text

def normalize(document: SourceDocument) -> SourceDocument:
    document.text = clean_text(document.text)
    document.metadata["normalized"] = True
    return document
