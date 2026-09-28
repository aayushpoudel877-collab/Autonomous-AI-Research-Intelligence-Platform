import re

_NEGATIONS = {"not", "never", "no", "false", "cannot", "without"}


def detect_conflict(a: str, b: str) -> bool:
    return bool((set(a.lower().split()) & _NEGATIONS) ^ (set(b.lower().split()) & _NEGATIONS))


def find_graph_contradictions(facts: list[dict]) -> list[dict]:
    """Find same subject/relation pairs that point to different objects."""
    conflicts = []
    grouped: dict[tuple[str, str], list[dict]] = {}
    for fact in facts:
        key = (fact["source"].lower(), fact["relation"].lower())
        grouped.setdefault(key, []).append(fact)
    for (source, relation), items in grouped.items():
        targets = {item["target"].lower() for item in items}
        if len(targets) > 1:
            conflicts.append({"source": source, "relation": relation, "facts": items})
    return conflicts
