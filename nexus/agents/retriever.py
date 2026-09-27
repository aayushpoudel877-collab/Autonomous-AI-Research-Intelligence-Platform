from nexus.agents.base import Agent


class RetrievalAgent(Agent):
    name = "retriever"

    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, context):
        top_k = int(context.state.get("top_k", 5))
        context.evidence = self.retriever.search(context.question, top_k=top_k)
        return context
