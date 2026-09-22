from nexus.embeddings.hash_embedding import HashEmbeddingModel
from nexus.retrieval.in_memory import InMemoryRetriever
retriever=InMemoryRetriever(HashEmbeddingModel())
