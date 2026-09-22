def normalize_tags(tags: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    """Normalize tags for consistent filtering and analytics."""
    return tuple(sorted({tag.strip().lower() for tag in tags if tag.strip()}))
