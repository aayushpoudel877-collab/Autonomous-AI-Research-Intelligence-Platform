import numpy as np
from nexus.embeddings.hash_embedding import HashEmbeddingModel
from nexus.retrieval.hybrid import lexical_score
from nexus.retrieval.models import SearchResult


class InMemoryRetriever:
    def __init__(self, embedder=None, semantic_weight=0.75):
        self.embedder = embedder or HashEmbeddingModel()
        self.semantic_weight = semantic_weight
        self.items = []
        self.matrix = None

    def add(self, chunks):
        self.items.extend(chunks)
        self.matrix = self.embedder.embed_many([c.text for c in self.items]) if self.items else None

    def search(self, query, top_k=5):
        if not self.items:
            return []
        top_k = max(1, min(top_k, len(self.items)))
        q = self.embedder.embed(query)
        semantic = self.matrix @ q
        lexical = np.array([lexical_score(query, item.text) for item in self.items])
        scores = self.semantic_weight * semantic + (1 - self.semantic_weight) * lexical
        ids = np.argsort(scores)[::-1][:top_k]
        return [
            SearchResult(
                chunk_id=self.items[i].chunk_id,
                document_id=self.items[i].document_id,
                text=self.items[i].text,
                score=float(scores[i]),
                source_uri=self.items[i].metadata.get("source_uri", "local"),
            )
            for i in ids
        ]
