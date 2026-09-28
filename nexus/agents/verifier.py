from nexus.agents.base import Agent
from nexus.verification.citation import verify_citations
from nexus.verification.contradiction import find_graph_contradictions


class VerificationAgent(Agent):
    name = "verifier"

    def run(self, context):
        citations = [
            {"id": f"E{i}", "source_uri": evidence.source_uri, "score": round(evidence.score, 4)}
            for i, evidence in enumerate(context.evidence[:5], start=1)
        ]
        context.state["citations"] = citations
        citation_check = verify_citations(citations, context.evidence)
        contradictions = find_graph_contradictions(context.state.get("graph_facts", []))
        context.state["verification"] = {
            "evidence_count": len(context.evidence),
            "grounded": bool(context.evidence),
            "citation_integrity": citation_check,
            "contradictions": contradictions,
        }
        return context
