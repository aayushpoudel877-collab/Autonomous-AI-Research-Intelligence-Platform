from nexus.embeddings.hash_embedding import HashEmbeddingModel
from nexus.retrieval.in_memory import InMemoryRetriever
from nexus.storage.sqlite import SQLiteStore


store = SQLiteStore()
retriever = InMemoryRetriever(HashEmbeddingModel())
restored_chunks = store.load_chunks()
if restored_chunks:
    retriever.add(restored_chunks)
