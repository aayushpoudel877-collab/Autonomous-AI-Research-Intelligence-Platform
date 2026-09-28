from nexus.verification.citation import verify_citations


def test_citations_are_verified_against_evidence():
    result = verify_citations([{"id": "E1"}, {"id": "E9"}], [object()])
    assert result["valid"] == 1
    assert result["invalid"] == 1
    assert result["integrity"] == 0.5
