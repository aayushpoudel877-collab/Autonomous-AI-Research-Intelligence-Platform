from nexus.research.planner import ResearchPlanner


class AutonomousResearchEngine:
    """Runs bounded iterative retrieval over the indexed corpus."""

    def __init__(self, retriever, orchestrator_factory, memory_store=None):
        self.retriever = retriever
        self.orchestrator_factory = orchestrator_factory
        self.memory_store = memory_store
        self.planner = ResearchPlanner()

    def run(self, question: str, top_k: int = 5, graph_hops: int = 1, max_iterations: int = 3):
        plan = self.planner.plan(question, max_subquestions=max_iterations)
        evidence = []
        seen = set()
        for subquestion in plan.subquestions[:max_iterations]:
            for item in self.retriever.search(subquestion, top_k=top_k):
                if item.chunk_id not in seen:
                    seen.add(item.chunk_id)
                    evidence.append(item)
        ctx = self.orchestrator_factory().run(question, top_k=min(max(top_k, len(evidence)), 20), graph_hops=graph_hops)
        if evidence:
            by_id = {item.chunk_id: item for item in ctx.evidence}
            for item in evidence:
                by_id[item.chunk_id] = item
            ctx.evidence = list(by_id.values())[:20]
        ctx.state["research_plan"] = list(plan.subquestions)
        ctx.state["iterations"] = len(plan.subquestions[:max_iterations])
        if self.memory_store:
            verification = ctx.state.get("verification", {})
            integrity = verification.get("citation_integrity", {}).get("integrity", 0.0)
            from nexus.research.memory import ResearchMemory
            self.memory_store.remember(ResearchMemory(question, plan.subquestions, len(ctx.evidence), len(ctx.state.get("graph_facts", [])), integrity))
        return ctx
