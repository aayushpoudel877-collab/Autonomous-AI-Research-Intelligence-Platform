from nexus.chunking.fixed import chunk_document
from nexus.normalization.cleaner import normalize
from nexus.retrieval.in_memory import InMemoryRetriever


class IndexPipeline:
    def __init__(self, retriever=None, store=None):
        self.retriever = retriever or InMemoryRetriever()
        self.store = store

    def index(self, documents):
        chunks = []
        for doc in documents:
            normalized = normalize(doc)
            normalized.metadata["source_uri"] = normalized.source_uri
            doc_chunks = chunk_document(normalized)
            chunks.extend(doc_chunks)
            if self.store:
                self.store.save_document(normalized)
                self.store.save_chunks(doc_chunks)
        self.retriever.add(chunks)
        return chunks
