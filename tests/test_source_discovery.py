from nexus.research.discovery import SourceDiscovery


def test_source_discovery_deduplicates_and_ranks():
    items = [
        type("E", (), {"source_uri": "a", "score": 0.4})(),
        type("E", (), {"source_uri": "a", "score": 0.9})(),
        type("E", (), {"source_uri": "b", "score": 0.8})(),
    ]
    result = SourceDiscovery().discover(items)
    assert result == [{"source_uri": "a", "max_score": 0.9}, {"source_uri": "b", "max_score": 0.8}]
