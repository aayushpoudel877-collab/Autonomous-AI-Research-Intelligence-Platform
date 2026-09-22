import hashlib
import numpy as np

class HashEmbeddingModel:
    def __init__(self, dimension: int = 256): self.dimension=dimension
    def embed(self, text: str) -> np.ndarray:
        vector=np.zeros(self.dimension, dtype=float)
        for token in text.lower().split():
            digest=hashlib.sha256(token.encode()).digest()
            index=int.from_bytes(digest[:4], "big") % self.dimension
            vector[index] += 1.0
        norm=np.linalg.norm(vector)
        return vector/norm if norm else vector
    def embed_many(self, texts): return np.vstack([self.embed(t) for t in texts])
