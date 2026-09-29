from nexus.research.planner import ResearchPlanner


class AutonomousResearchEngine:
    """Runs a bounded, auditable research plan through the normal agent pipeline."""

    def __init__(self, retriever, orchestrator_factory, memory_store=None):
        self.retriever = retriever
        self.orchestrator_factory = orchestrator_factory
        self.memory_store = memory_store
        self.planner = ResearchPlanner()

    def run(self, question: str, top_k: int = 5, graph_hops: int = 1, max_iterations: int = 3):
        plan = self.planner.plan(question, max_subquestions=max_iterations)
        ctx = self.orchestrator_factory().run(
            question,
            top_k=top_k,
            graph_hops=graph_hops,
            research_queries=plan.subquestions,
        )
        ctx.state["research_plan"] = list(plan.subquestions)
        ctx.state["iterations"] = len(plan.subquestions)
        if self.memory_store:
            verification = ctx.state.get("verification", {})
            integrity = verification.get("citation_integrity", {}).get("integrity", 0.0)
            from nexus.research.memory import ResearchMemory
            self.memory_store.remember(ResearchMemory(question, plan.subquestions, len(ctx.evidence), len(ctx.state.get("graph_facts", [])), integrity))
        return ctx
