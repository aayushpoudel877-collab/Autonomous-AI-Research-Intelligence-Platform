from nexus.agents.base import Agent
from nexus.graph.extractor import EntityGraphExtractor
from nexus.graph.store import GraphStore


class GraphRetrievalAgent(Agent):
    name = "graph_retriever"

    def __init__(self, graph: GraphStore):
        self.graph = graph
        self.extractor = EntityGraphExtractor()

    def _resolve_question_ids(self, question_nodes):
        ids = set()
        for question_node in question_nodes:
            exact = self.graph.nodes.get(question_node.id)
            if exact:
                ids.add(exact.id)
                continue
            label = question_node.label.lower()
            for node in self.graph.nodes.values():
                node_label = node.label.lower()
                if node_label.startswith(label + " ") or label.startswith(node_label + " "):
                    ids.add(node.id)
        return ids

    def run(self, context):
        for evidence in context.evidence:
            nodes, edges = self.extractor.extract(
                evidence.text, evidence.chunk_id, evidence.source_uri
            )
            self.graph.add(nodes, edges)

        question_nodes, _ = self.extractor.extract(context.question)
        ids = self._resolve_question_ids(question_nodes)
        if not ids:
            context.state["graph_facts"] = []
            return context

        facts = self.graph.facts_for(ids, hops=int(context.state.get("graph_hops", 1)))
        context.state["graph_facts"] = [
            {
                "source": self.graph.nodes[e.source].label,
                "relation": e.relation,
                "target": self.graph.nodes[e.target].label,
                "confidence": round(e.confidence, 4),
                "chunk_id": e.evidence_chunk_id,
                "source_uri": e.source_uri,
            }
            for e in facts
            if e.source in self.graph.nodes and e.target in self.graph.nodes
        ][:20]
        return context
