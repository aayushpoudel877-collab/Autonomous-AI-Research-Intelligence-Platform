from nexus.research.sources import SourceCandidate, SourceSearchProvider, canonicalize_url


class StaticURLProvider:
    """Provider-neutral adapter for caller-supplied URLs.

    This is deliberately deterministic. Real search engines can implement
    SourceSearchProvider without changing the acquisition controller.
    """

    name = "static_urls"

    def __init__(self, urls: list[str]):
        self.urls = [canonicalize_url(url) for url in urls]

    def search(self, query: str, limit: int = 5) -> list[SourceCandidate]:
        return [SourceCandidate(url, provider=self.name) for url in self.urls[:max(0, limit)]]


class IndexedSourceProvider:
    """Turns already-known source URIs into candidates for controller composition."""

    name = "indexed_sources"

    def __init__(self, source_uris: list[str]):
        self.source_uris = [canonicalize_url(uri) for uri in source_uris if uri.startswith(("http://", "https://"))]

    def search(self, query: str, limit: int = 5) -> list[SourceCandidate]:
        return [SourceCandidate(url, provider=self.name) for url in self.source_uris[:max(0, limit)]]
