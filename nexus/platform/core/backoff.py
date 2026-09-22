def exponential_backoff(attempt: int, base: float = 0.25, cap: float = 30.0) -> float:
    """Calculate bounded retry delay without sleeping."""
    if attempt < 0:
        raise ValueError("attempt must be non-negative")
    return min(cap, base * (2 ** attempt))
