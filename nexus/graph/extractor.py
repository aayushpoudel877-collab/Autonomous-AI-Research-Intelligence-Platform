import re
from nexus.graph.model import Node, Edge
from nexus.utils import stable_id

class EntityGraphExtractor:
    def extract(self, text: str):
        phrases=re.findall(r"\b[A-Z][A-Za-z0-9_-]{2,}\b", text)
        nodes=[Node(stable_id("entity",p),p,"entity") for p in dict.fromkeys(phrases)]
        edges=[Edge(nodes[i].id,nodes[i+1].id,"co_occurs") for i in range(len(nodes)-1)]
        return nodes, edges
