from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceAssessment:
    evidence_count: int
    unique_sources: int
    average_score: float
    source_diversity: float
    coverage: float
    sufficient: bool
    reason: str


class EvidenceController:
    """Auditable stopping policy for bounded research.

    The policy measures quantity, source diversity, and retrieval relevance.
    It does not claim that a source is factually correct merely because it
    receives a high heuristic score.
    """

    def assess(
        self,
        evidence: list,
        *,
        target_evidence: int = 5,
        target_sources: int = 2,
        min_average_score: float = 0.15,
    ) -> EvidenceAssessment:
        count = len(evidence)
        sources = {
            getattr(item, "source_uri", "local") or "local"
            for item in evidence
        }
        average = (
            sum(float(getattr(item, "score", 0.0)) for item in evidence) / count
            if count
            else 0.0
        )
        source_diversity = min(1.0, len(sources) / max(1, target_sources))
        coverage = min(1.0, count / max(1, target_evidence))
        sufficient = (
            count >= target_evidence
            and len(sources) >= target_sources
            and average >= min_average_score
        )
        if sufficient:
            reason = "evidence_and_source_targets_met"
        elif count < target_evidence:
            reason = "more_evidence_needed"
        elif len(sources) < target_sources:
            reason = "more_source_diversity_needed"
        else:
            reason = "retrieval_relevance_below_threshold"
        return EvidenceAssessment(
            count,
            len(sources),
            round(average, 4),
            round(source_diversity, 4),
            round(coverage, 4),
            sufficient,
            reason,
        )
