import hashlib


def make_id(namespace: str, value: str) -> str:
    """Create a stable, short identifier for an entity."""
    digest = hashlib.sha256(f"{namespace}:{value}".encode()).hexdigest()
    return f"{namespace}_{digest[:16]}"
