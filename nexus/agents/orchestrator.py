from nexus.agents.base import Agent, AgentContext
class Orchestrator:
    def __init__(self, agents:list[Agent]): self.agents=agents
    def run(self, question:str):
        ctx=AgentContext(question=question)
        for agent in self.agents: ctx=agent.run(ctx)
        return ctx
