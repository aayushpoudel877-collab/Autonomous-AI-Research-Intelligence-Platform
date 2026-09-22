from nexus.agents.base import Agent
class ResearchAgent(Agent):
    name="researcher"
    def run(self, context):
        context.state["research_started"]=True
        return context
