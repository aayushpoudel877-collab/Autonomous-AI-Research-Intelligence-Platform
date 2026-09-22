from nexus.agents.base import Agent
class PlanningAgent(Agent):
    name='planner'
    def run(self,context):
        context.state['plan']=['retrieve evidence','verify claims','compose report']
        return context
