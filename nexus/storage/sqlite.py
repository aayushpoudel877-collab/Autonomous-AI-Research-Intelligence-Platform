import sqlite3
from pathlib import Path

class SQLiteStore:
    def __init__(self, path="nexus.db"):
        self.path=path; Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as c:
            c.execute("CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY,title TEXT,text TEXT,source_uri TEXT)")
            c.execute("CREATE TABLE IF NOT EXISTS chunks(id TEXT PRIMARY KEY,document_id TEXT,text TEXT,idx INTEGER,source_uri TEXT)")
    def connect(self): return sqlite3.connect(self.path)
    def save_document(self, doc):
        with self.connect() as c: c.execute("INSERT OR REPLACE INTO documents VALUES (?,?,?,?)", (doc.document_id,doc.title,doc.text,doc.source_uri))
    def save_chunks(self, chunks):
        with self.connect() as c: c.executemany("INSERT OR REPLACE INTO chunks VALUES (?,?,?,?,?)", [(x.chunk_id,x.document_id,x.text,x.index,x.metadata.get("source_uri","local")) for x in chunks])
