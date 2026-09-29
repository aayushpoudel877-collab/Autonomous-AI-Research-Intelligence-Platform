from urllib.parse import urlsplit


class SourceQualityScorer:
    """Transparent heuristic source-quality score; not a claim of factual truth."""

    TRUSTED_SUFFIXES = {".gov", ".edu", ".ac.uk", ".int"}

    def score(self, url: str, text: str, provider_score: float = 0.0) -> float:
        host = (urlsplit(url).hostname or "").lower()
        score = 0.35
        if any(host.endswith(suffix) for suffix in self.TRUSTED_SUFFIXES):
            score += 0.25
        if len(text) >= 500:
            score += 0.15
        if len(text) >= 2000:
            score += 0.10
        if provider_score > 0:
            score += min(0.15, provider_score * 0.15)
        return round(min(1.0, score), 4)
