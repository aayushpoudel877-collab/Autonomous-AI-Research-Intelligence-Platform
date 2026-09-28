from nexus.retrieval.hybrid import lexical_score


def test_lexical_score_prefers_matching_terms():
    assert lexical_score("quantum computing", "quantum computing research") > lexical_score("quantum computing", "weather forecast")
