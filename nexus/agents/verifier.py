from nexus.agents.base import Agent
class VerificationAgent(Agent):
    name="verifier"
    def run(self,context):
        context.state["verification"]={"evidence_count":len(context.evidence),"grounded":bool(context.evidence)}
        return context
