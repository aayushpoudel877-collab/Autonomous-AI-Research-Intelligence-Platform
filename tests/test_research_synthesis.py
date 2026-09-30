from types import SimpleNamespace

from nexus.research.synthesis import ResearchSynthesis


def test_synthesis_preserves_evidence_provenance():
    evidence = [
        SimpleNamespace(text="NEXUS supports evidence-based research.", source_uri="https://a.test", score=0.8),
        SimpleNamespace(text="NEXUS supports evidence-based research.", source_uri="https://b.test", score=0.6),
    ]
    result = ResearchSynthesis().run("What does NEXUS support?", evidence, ["What does NEXUS support?"])
    assert len(result["claims"]) == 1
    assert result["claims"][0]["evidence_ids"] == ("E1", "E2")
    assert len(result["claims"][0]["source_uris"]) == 2


def test_synthesis_reports_single_source_limitation():
    evidence = [SimpleNamespace(text="A sufficiently long statement for extraction.", source_uri="local", score=0.2)]
    result = ResearchSynthesis().run("Question?", evidence)
    assert result["source_review"]["unique_sources"] == 1
    assert result["source_review"]["limitations"]


def test_synthesis_exposes_heuristic_limitations():
    result = ResearchSynthesis().run("Question?", [])
    assert result["claims"] == []
    assert result["limitations"]
