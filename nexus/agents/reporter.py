from nexus.agents.base import Agent


class ReportAgent(Agent):
    name = "reporter"

    def run(self, context):
        citations = []
        excerpts = []
        for index, evidence in enumerate(context.evidence[:5], start=1):
            citations.append({"id": f"E{index}", "source_uri": evidence.source_uri, "score": round(evidence.score, 4)})
            excerpts.append(f"[E{index}] {evidence.text}")
        context.state["citations"] = citations
        facts = context.state.get("graph_facts", [])
        fact_lines = [f"- {f['source']} {f['relation']} {f['target']} (confidence {f['confidence']})" for f in facts[:8]]
        contradictions = context.state.get("verification", {}).get("contradictions", [])
        contradiction_lines = [f"- {c['source']} {c['relation']} has conflicting targets" for c in contradictions]
        context.state["report"] = (
            f"Research question: {context.question}\\n\\n"
            f"Evidence:\\n{chr(10).join('- ' + item for item in excerpts) or '- No indexed evidence found.'}\\n\\n"
            f"Knowledge graph:\\n{chr(10).join(fact_lines) or '- No graph facts found.'}\\n\\n"
            f"Verification:\\n"
            f"- Citation integrity: {context.state.get('verification', {}).get('citation_integrity', {}).get('integrity', 0.0)}\\n"
            f"{chr(10).join(contradiction_lines) or '- No graph contradictions detected.'}"
        )
        return context
