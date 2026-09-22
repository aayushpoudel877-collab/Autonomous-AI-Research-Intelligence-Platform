from nexus.agents.base import Agent
class RetrievalAgent(Agent):
    name="retriever"
    def __init__(self,retriever): self.retriever=retriever
    def run(self,context):
        context.evidence=self.retriever.search(context.question)
        return context
