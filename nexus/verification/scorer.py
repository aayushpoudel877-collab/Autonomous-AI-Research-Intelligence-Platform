from nexus.types import Claim

def score_claim(claim: Claim) -> Claim:
    if not claim.evidence: claim.confidence=0.0
    else: claim.confidence=min(1.0, 0.2*len(claim.evidence)+max(e.score for e in claim.evidence))
    return claim
