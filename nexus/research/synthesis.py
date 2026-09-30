from collections import defaultdict
from dataclasses import asdict, dataclass
import re


@dataclass(frozen=True)
class EvidenceClaim:
    claim_id: str
    text: str
    evidence_ids: tuple[str, ...]
    source_uris: tuple[str, ...]
    confidence: float


class EvidenceMapper:
    """Extracts auditable sentence-level evidence units; not a truth classifier."""

    def map(self, evidence: list, limit: int = 30) -> list[EvidenceClaim]:
        grouped = defaultdict(lambda: {"text": "", "ids": [], "sources": [], "scores": []})
        for index, item in enumerate(evidence[:limit], start=1):
            text = re.sub(r"\s+", " ", str(getattr(item, "text", ""))).strip()
            if not text:
                continue
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) >= 20]
            if not sentences:
                sentences = [text[:500]]
            source = str(getattr(item, "source_uri", "") or "local")
            score = float(getattr(item, "score", 0.0))
            for sentence in sentences[:4]:
                key = re.sub(r"[^a-z0-9]+", " ", sentence.lower()).strip()
                if not key:
                    continue
                entry = grouped[key]
                entry["text"] = sentence[:700]
                entry["ids"].append(f"E{index}")
                entry["sources"].append(source)
                entry["scores"].append(max(0.0, min(1.0, (score + 1.0) / 2.0)))
        claims = []
        for index, entry in enumerate(grouped.values(), start=1):
            sources = tuple(dict.fromkeys(entry["sources"]))
            scores = entry["scores"]
            support = min(1.0, len(sources) / 2.0)
            relevance = sum(scores) / len(scores) if scores else 0.0
            claims.append(EvidenceClaim(f"C{index}", entry["text"], tuple(dict.fromkeys(entry["ids"])), sources, round(0.6 * relevance + 0.4 * support, 4)))
        return claims


class SourceCritic:
    """Reports source coverage and relevance without asserting source truth."""

    def review(self, evidence: list) -> dict:
        sources = sorted({str(getattr(x, "source_uri", "") or "local") for x in evidence})
        scores = [float(getattr(x, "score", 0.0)) for x in evidence]
        return {"evidence_count": len(evidence), "unique_sources": len(sources), "source_uris": sources, "mean_retrieval_score": round(sum(scores) / len(scores), 4) if scores else 0.0, "limitations": [] if len(sources) >= 2 else ["Evidence comes from fewer than two distinct sources."]}


class DisagreementAnalyst:
    """Flags polarity differences between near-identical normalized statements."""

    _NEGATIONS = {"not", "never", "no", "cannot", "without", "false"}

    def analyze(self, claims: list[EvidenceClaim]) -> list[dict]:
        findings = []
        for i, left in enumerate(claims):
            left_words = set(re.findall(r"\b\w+\b", left.text.lower()))
            for right in claims[i + 1:]:
                right_words = set(re.findall(r"\b\w+\b", right.text.lower()))
                union = left_words | right_words
                similarity = len(left_words & right_words) / len(union) if union else 0.0
                polarity_differs = bool((left_words & self._NEGATIONS) ^ (right_words & self._NEGATIONS))
                if similarity >= 0.65 and polarity_differs:
                    findings.append({"claim_ids": [left.claim_id, right.claim_id], "similarity": round(similarity, 4), "description": "Potential polarity disagreement; inspect the cited passages."})
        return findings


class ResearchSynthesis:
    """Combines bounded evidence tracks into a provenance-preserving synthesis."""

    def __init__(self):
        self.mapper = EvidenceMapper()
        self.critic = SourceCritic()
        self.disagreement = DisagreementAnalyst()

    def run(self, question: str, evidence: list, plan: list[str] | None = None) -> dict:
        claims = self.mapper.map(evidence)
        review = self.critic.review(evidence)
        disagreements = self.disagreement.analyze(claims)
        return {"question": question, "research_tracks": list(plan or [question]), "claims": [asdict(claim) for claim in claims], "source_review": review, "disagreements": disagreements, "summary": f"Mapped {len(claims)} distinct evidence statements across {review['unique_sources']} source(s). Flagged {len(disagreements)} potential disagreement(s).", "limitations": ["Sentence extraction and polarity checks are heuristic.", "Confidence is a support/relevance indicator, not a probability that a claim is true.", "No external LLM or search provider is invoked by this synthesis baseline."]}
