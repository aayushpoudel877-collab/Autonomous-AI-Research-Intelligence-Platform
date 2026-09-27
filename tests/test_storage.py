from nexus.storage.sqlite import SQLiteStore
from nexus.types import Chunk, SourceDocument


def test_sqlite_round_trip(tmp_path):
    store = SQLiteStore(tmp_path / "nexus.db")
    doc = SourceDocument("d1", "Demo", "persistent evidence", "demo://1")
    chunk = Chunk("c1", "d1", "persistent evidence", 0, {"source_uri": "demo://1"})
    store.save_document(doc)
    store.save_chunks([chunk])
    restored = store.load_chunks()
    assert restored[0].chunk_id == "c1"
    assert restored[0].metadata["source_uri"] == "demo://1"
