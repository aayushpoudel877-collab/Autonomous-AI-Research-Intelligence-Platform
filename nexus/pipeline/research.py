from nexus.agents.graph_retriever import GraphRetrievalAgent
from nexus.agents.orchestrator import Orchestrator
from nexus.agents.retriever import RetrievalAgent
from nexus.agents.researcher import ResearchAgent
from nexus.agents.verifier import VerificationAgent
from nexus.agents.reporter import ReportAgent
from nexus.graph.store import GraphStore


def build_orchestrator(retriever):
    graph = GraphStore()
    return Orchestrator([
        ResearchAgent(),
        RetrievalAgent(retriever),
        GraphRetrievalAgent(graph),
        VerificationAgent(),
        ReportAgent(),
    ])
