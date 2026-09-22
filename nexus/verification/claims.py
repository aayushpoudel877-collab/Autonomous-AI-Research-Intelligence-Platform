import re
from nexus.types import Claim

def extract_claims(text: str) -> list[Claim]:
    parts=[p.strip() for p in re.split(r"[.!?]", text) if p.strip()]
    return [Claim(statement=p) for p in parts]
