from nexus.agents.base import Agent, AgentContext


class Orchestrator:
    def __init__(self, agents: list[Agent]):
        self.agents = agents

    def run(self, question: str, **options):
        ctx = AgentContext(question=question)
        ctx.state.update(options)
        for agent in self.agents:
            ctx = agent.run(ctx)
        return ctx
