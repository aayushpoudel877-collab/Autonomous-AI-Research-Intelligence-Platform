from nexus.chunking.fixed import chunk_document
from nexus.types import SourceDocument

def test_chunking_preserves_content():
    doc=SourceDocument('d','t','abcdefghij')
    chunks=chunk_document(doc,size=5,overlap=1)
    assert ''.join(c.text for c in chunks).startswith('abcde')
    assert len(chunks)>=2
