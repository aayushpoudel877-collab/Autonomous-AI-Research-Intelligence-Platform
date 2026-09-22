from nexus.types import Chunk, SourceDocument
from nexus.utils import stable_id

def chunk_document(doc: SourceDocument, size: int = 800, overlap: int = 100) -> list[Chunk]:
    if size <= overlap: raise ValueError("size must exceed overlap")
    chunks=[]; start=0; index=0
    while start < len(doc.text):
        end=min(len(doc.text), start+size); text=doc.text[start:end]
        chunks.append(Chunk(stable_id(doc.document_id, str(index), text), doc.document_id, text, index, doc.metadata.copy()))
        if end == len(doc.text): break
        start=end-overlap; index+=1
    return chunks
