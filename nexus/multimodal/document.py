from pathlib import Path

def inspect_asset(path: str) -> dict:
    p=Path(path); return {"name":p.name,"suffix":p.suffix.lower(),"bytes":p.stat().st_size}
