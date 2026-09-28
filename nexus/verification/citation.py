def verify_citations(citations: list[dict], evidence: list) -> dict:
    valid, invalid = [], []
    evidence_ids = {f"E{i}" for i, _ in enumerate(evidence[:5], start=1)}
    for citation in citations:
        cid = citation.get("id")
        (valid if cid in evidence_ids else invalid).append(cid)
    total = len(citations)
    return {"valid": len(valid), "invalid": len(invalid), "integrity": 1.0 if total == 0 else round(len(valid) / total, 4), "invalid_ids": invalid}
