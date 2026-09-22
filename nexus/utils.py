import hashlib
import re
from pathlib import Path

def stable_id(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]

def clean_text(text: str) -> str:
    return re.sub(r"\\s+", " ", text).strip()

def ensure_parent(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
