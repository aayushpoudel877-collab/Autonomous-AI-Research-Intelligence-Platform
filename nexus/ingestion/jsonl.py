import json
from pathlib import Path
from nexus.types import SourceDocument
from nexus.utils import stable_id

def load_jsonl(path: str) -> list[SourceDocument]:
    docs=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        row=json.loads(line); text=str(row.get("text", ""))
        docs.append(SourceDocument(stable_id(text), row.get("title","Untitled"), text, row.get("source_uri","jsonl"), row))
    return docs
