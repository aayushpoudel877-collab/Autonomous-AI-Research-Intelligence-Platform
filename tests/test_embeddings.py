from nexus.embeddings.hash_embedding import HashEmbeddingModel

def test_embedding_is_normalized():
    v=HashEmbeddingModel(32).embed('research intelligence')
    assert abs(float((v*v).sum())-1)<1e-6
