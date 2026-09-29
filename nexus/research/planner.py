import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchPlan:
    question: str
    subquestions: tuple[str, ...]


class ResearchPlanner:
    """Deterministic query decomposition used as a provider-free planning baseline."""

    def plan(self, question: str, max_subquestions: int = 4) -> ResearchPlan:
        q = question.strip().rstrip("?")
        parts = [p.strip() for p in re.split(r"\s+(?:and|vs\.?|versus)\s+", q, flags=re.IGNORECASE) if p.strip()]
        candidates = [q]
        if len(parts) > 1:
            candidates.extend(parts)
        if re.search(r"\bwhat\b|\bhow\b|\bwhy\b", q, re.IGNORECASE):
            candidates.extend([f"What evidence supports {q}?", f"What limitations or risks apply to {q}?"])
        unique = []
        for item in candidates:
            item = re.sub(r"\s+", " ", item).strip()
            if item and item.lower() not in {x.lower() for x in unique}:
                unique.append(item)
        return ResearchPlan(q, tuple(unique[:max_subquestions]))
