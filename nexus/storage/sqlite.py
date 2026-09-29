import sqlite3
from pathlib import Path

from nexus.graph.model import Edge, Node
from nexus.types import Chunk


class SQLiteStore:
    def __init__(self, path="nexus.db"):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as c:
            c.execute("CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY,title TEXT,text TEXT,source_uri TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS chunks(id TEXT PRIMARY KEY,document_id TEXT,text TEXT,idx INTEGER,source_uri TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS research_memory(id INTEGER PRIMARY KEY AUTOINCREMENT,question TEXT NOT NULL,plan TEXT NOT NULL,evidence_count INTEGER NOT NULL,graph_fact_count INTEGER NOT NULL,citation_integrity REAL NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
            c.execute("CREATE TABLE IF NOT EXISTS graph_nodes(id TEXT PRIMARY KEY,label TEXT NOT NULL,kind TEXT NOT NULL,mentions TEXT NOT NULL)")
            c.execute("CREATE TABLE IF NOT EXISTS graph_edges(source TEXT NOT NULL,target TEXT NOT NULL,relation TEXT NOT NULL,confidence REAL NOT NULL,evidence_chunk_id TEXT NOT NULL,source_uri TEXT NOT NULL,PRIMARY KEY(source,target,relation,evidence_chunk_id))")

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

    def save_graph(self, nodes, edges):
        with self.connect() as c:
            c.executemany("INSERT OR REPLACE INTO graph_nodes VALUES (?,?,?,?)", [(n.id, n.label, n.kind, "\n".join(n.mentions)) for n in nodes])
            c.executemany("INSERT OR IGNORE INTO graph_edges VALUES (?,?,?,?,?,?)", [(e.source, e.target, e.relation, e.confidence, e.evidence_chunk_id, e.source_uri) for e in edges])

    def load_graph(self):
        with self.connect() as c:
            nodes = c.execute("SELECT id,label,kind,mentions FROM graph_nodes").fetchall()
            edges = c.execute("SELECT source,target,relation,confidence,evidence_chunk_id,source_uri FROM graph_edges").fetchall()
        return ([Node(row[0], row[1], row[2], tuple(x for x in row[3].split("\n") if x)) for row in nodes], [Edge(*row) for row in edges])

    def save_research_memory(self, memory):
        with self.connect() as c:
            c.execute("INSERT INTO research_memory(question,plan,evidence_count,graph_fact_count,citation_integrity) VALUES (?,?,?,?,?)", (memory.question, "\n".join(memory.plan), memory.evidence_count, memory.graph_fact_count, memory.citation_integrity))

    def load_research_memory(self, limit=10):
        from nexus.research.memory import ResearchMemory
        with self.connect() as c:
            rows = c.execute("SELECT question,plan,evidence_count,graph_fact_count,citation_integrity FROM research_memory ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [ResearchMemory(row[0], tuple(x for x in row[1].split("\n") if x), row[2], row[3], row[4]) for row in rows]
