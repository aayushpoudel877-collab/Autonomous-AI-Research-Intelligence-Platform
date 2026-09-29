import sqlite3
from pathlib import Path

from nexus.types import Chunk


class SQLiteStore:
    def __init__(self, path="nexus.db"):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as c:
            c.execute("CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY,title TEXT,text TEXT,source_uri TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS chunks(id TEXT PRIMARY KEY,document_id TEXT,text TEXT,idx INTEGER,source_uri TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS research_memory(id INTEGER PRIMARY KEY AUTOINCREMENT,question TEXT NOT NULL,plan TEXT NOT NULL,evidence_count INTEGER NOT NULL,graph_fact_count INTEGER NOT NULL,citation_integrity REAL NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP)")

    def connect(self):
        return sqlite3.connect(self.path)

    def save_document(self, doc):
        with self.connect() as c:
            c.execute("INSERT OR REPLACE INTO documents VALUES (?,?,?,?)", (doc.document_id, doc.title, doc.text, doc.source_uri))

    def save_chunks(self, chunks):
        with self.connect() as c:
            c.executemany("INSERT OR REPLACE INTO chunks VALUES (?,?,?,?,?)", [(x.chunk_id, x.document_id, x.text, x.index, x.metadata.get("source_uri", "local")) for x in chunks])

    def load_chunks(self):
        with self.connect() as c:
            rows = c.execute("SELECT id, document_id, text, idx, source_uri FROM chunks ORDER BY document_id, idx").fetchall()
        return [Chunk(row[0], row[1], row[2], row[3], {"source_uri": row[4]}) for row in rows]

    def save_research_memory(self, memory):
        plan = "\n".join(memory.plan)
        with self.connect() as c:
            c.execute("INSERT INTO research_memory(question,plan,evidence_count,graph_fact_count,citation_integrity) VALUES (?,?,?,?,?)", (memory.question, plan, memory.evidence_count, memory.graph_fact_count, memory.citation_integrity))

    def load_research_memory(self, limit=10):
        from nexus.research.memory import ResearchMemory
        with self.connect() as c:
            rows = c.execute("SELECT question,plan,evidence_count,graph_fact_count,citation_integrity FROM research_memory ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [ResearchMemory(row[0], tuple(x for x in row[1].split("\n") if x), row[2], row[3], row[4]) for row in rows]
