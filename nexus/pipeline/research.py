from nexus.agents.orchestrator import Orchestrator
from nexus.agents.retriever import RetrievalAgent
from nexus.agents.researcher import ResearchAgent
from nexus.agents.verifier import VerificationAgent
from nexus.agents.reporter import ReportAgent

def build_orchestrator(retriever):
    return Orchestrator([ResearchAgent(), RetrievalAgent(retriever), VerificationAgent(), ReportAgent()])
