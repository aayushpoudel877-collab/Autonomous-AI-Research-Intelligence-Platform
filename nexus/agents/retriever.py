from nexus.agents.base import Agent


class RetrievalAgent(Agent):
    name = "retriever"

    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, context):
        top_k = int(context.state.get("top_k", 5))
        queries = context.state.get("research_queries") or [context.question]
        results = []
        seen = set()
        for query in queries[:3]:
            for item in self.retriever.search(query, top_k=top_k):
                if item.chunk_id not in seen:
                    seen.add(item.chunk_id)
                    results.append(item)
        context.evidence = results[:20]
        return context
