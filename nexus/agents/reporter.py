from nexus.agents.base import Agent


class ReportAgent(Agent):
    name = "reporter"

    def run(self, context):
        citations = []
        excerpts = []
        for index, evidence in enumerate(context.evidence[:5], start=1):
            citations.append({
                "id": f"E{index}",
                "source_uri": evidence.source_uri,
                "score": round(evidence.score, 4),
            })
            excerpts.append(f"[E{index}] {evidence.text}")
        context.state["citations"] = citations
        context.state["report"] = (
            f"Research question: {context.question}\\n\\n"
            f"Evidence:\\n{chr(10).join('- ' + item for item in excerpts) or '- No indexed evidence found.'}"
        )
        return context
