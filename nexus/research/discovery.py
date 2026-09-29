class SourceDiscovery:
    """Discovers distinct indexed sources from retrieved evidence, ranked by relevance."""

    def discover(self, evidence: list) -> list[dict]:
        ranked = {}
        for item in evidence:
            uri = getattr(item, "source_uri", "local") or "local"
            ranked[uri] = max(float(getattr(item, "score", 0.0)), ranked.get(uri, float("-inf")))
        return [
            {"source_uri": uri, "max_score": round(score, 4)}
            for uri, score in sorted(ranked.items(), key=lambda pair: pair[1], reverse=True)
        ]
