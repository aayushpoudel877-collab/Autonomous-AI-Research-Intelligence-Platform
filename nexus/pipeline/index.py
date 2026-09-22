from nexus.chunking.fixed import chunk_document
from nexus.normalization.cleaner import normalize
from nexus.retrieval.in_memory import InMemoryRetriever

class IndexPipeline:
    def __init__(self,retriever=None): self.retriever=retriever or InMemoryRetriever()
    def index(self,documents):
        chunks=[]
        for doc in documents: chunks.extend(chunk_document(normalize(doc)))
        self.retriever.add(chunks); return chunks
