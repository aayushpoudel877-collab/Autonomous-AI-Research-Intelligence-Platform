from nexus.research.dedup import SourceDeduplicator, content_hash
from nexus.research.providers import StaticURLProvider
from nexus.research.quality import SourceQualityScorer
from nexus.research.sources import canonicalize_url


def test_canonicalize_url_removes_tracking():
    assert canonicalize_url("HTTPS://Example.COM/path?utm_source=x&a=1#frag") == "https://example.com/path?a=1"


def test_static_provider_is_deterministic():
    provider = StaticURLProvider(["https://example.com", "https://example.com/?utm_medium=x"])
    results = provider.search("anything", 5)
    assert results[0].url == "https://example.com/"


def test_deduplication_and_hash():
    dedup = SourceDeduplicator()
    assert dedup.accept("https://example.com/", "Same text")
    assert not dedup.accept("https://example.com/", " same   TEXT ")
    assert content_hash("A") != content_hash("B")


def test_quality_score_is_bounded():
    score = SourceQualityScorer().score("https://example.gov/paper", "x" * 2500)
    assert 0 <= score <= 1
