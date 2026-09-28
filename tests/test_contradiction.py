from nexus.verification.contradiction import find_graph_contradictions


def test_graph_contradiction_detects_conflicting_targets():
    facts = [
        {"source": "A", "relation": "is", "target": "B"},
        {"source": "A", "relation": "is", "target": "C"},
    ]
    assert len(find_graph_contradictions(facts)) == 1
