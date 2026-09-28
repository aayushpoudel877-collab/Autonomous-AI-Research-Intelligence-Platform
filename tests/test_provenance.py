from nexus.verification.provenance import content_hash


def test_content_hash_is_deterministic():
    assert content_hash("evidence") == content_hash("evidence")
    assert content_hash("evidence") != content_hash("other evidence")
