from nexus.verification.claims import extract_claims

def test_claim_extraction(): assert len(extract_claims('One claim. Another claim!'))==2
