from nexus.agents.base import Agent
from nexus.verification.citation import verify_citations
from nexus.verification.contradiction import find_graph_contradictions


class VerificationAgent(Agent):
    name = "verifier"

    def run(self, context):
        citations = context.state.get("citations", [])
        citation_check = verify_citations(citations, context.evidence)
        contradictions = find_graph_contradictions(context.state.get("graph_facts", []))
        context.state["verification"] = {
            "evidence_count": len(context.evidence),
            "grounded": bool(context.evidence),
            "citation_integrity": citation_check,
            "contradictions": contradictions,
        }
        return context
