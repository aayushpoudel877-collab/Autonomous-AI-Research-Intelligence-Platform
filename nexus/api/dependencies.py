from nexus.embeddings.hash_embedding import HashEmbeddingModel
from nexus.graph.store import GraphStore
from nexus.retrieval.in_memory import InMemoryRetriever
from nexus.storage.sqlite import SQLiteStore


store = SQLiteStore()
retriever = InMemoryRetriever(HashEmbeddingModel())
graph = GraphStore(store)
restored_chunks = store.load_chunks()
if restored_chunks:
    retriever.add(restored_chunks)
restored_nodes, restored_edges = store.load_graph()
graph.load(restored_nodes, restored_edges)
