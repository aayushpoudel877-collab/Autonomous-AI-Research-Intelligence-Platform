from types import SimpleNamespace

from nexus.research.evidence import EvidenceController


def test_evidence_controller_requires_diverse_sources():
    controller = EvidenceController()
    evidence = [
        SimpleNamespace(score=0.8, source_uri="a"),
        SimpleNamespace(score=0.8, source_uri="a"),
        SimpleNamespace(score=0.8, source_uri="a"),
        SimpleNamespace(score=0.8, source_uri="a"),
        SimpleNamespace(score=0.8, source_uri="a"),
    ]
    result = controller.assess(evidence, target_evidence=5, target_sources=2)
    assert not result.sufficient
    assert result.reason == "more_source_diversity_needed"


def test_evidence_controller_stops_when_targets_met():
    controller = EvidenceController()
    evidence = [
        SimpleNamespace(score=0.8, source_uri="a"),
        SimpleNamespace(score=0.7, source_uri="b"),
        SimpleNamespace(score=0.6, source_uri="a"),
        SimpleNamespace(score=0.5, source_uri="b"),
        SimpleNamespace(score=0.4, source_uri="a"),
    ]
    result = controller.assess(evidence, target_evidence=5, target_sources=2)
    assert result.sufficient
    assert result.coverage == 1.0
