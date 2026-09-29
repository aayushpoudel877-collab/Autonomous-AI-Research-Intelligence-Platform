from nexus.agents.graph_retriever import GraphRetrievalAgent
from nexus.agents.orchestrator import Orchestrator
from nexus.agents.retriever import RetrievalAgent
from nexus.agents.researcher import ResearchAgent
from nexus.agents.verifier import VerificationAgent
from nexus.agents.reporter import ReportAgent
from nexus.api import dependencies


def build_orchestrator(retriever, graph=None):
    graph = graph or dependencies.graph
    return Orchestrator([ResearchAgent(), RetrievalAgent(retriever), GraphRetrievalAgent(graph), VerificationAgent(), ReportAgent()])
