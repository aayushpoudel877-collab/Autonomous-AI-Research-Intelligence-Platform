import hashlib


def cache_key(namespace: str, *parts: object) -> str:
    raw = "|".join(str(part) for part in parts)
    return f"{namespace}:{hashlib.sha256(raw.encode()).hexdigest()[:24]}"
