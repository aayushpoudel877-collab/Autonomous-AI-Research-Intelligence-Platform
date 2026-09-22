from nexus.agents.base import Agent
class ReportAgent(Agent):
    name="reporter"
    def run(self,context):
        excerpts="\n".join(f"- {e.text}" for e in context.evidence[:5])
        context.state["report"]=f"Research question: {context.question}\n\nEvidence:\n{excerpts or '- No indexed evidence found.'}"
        return context
