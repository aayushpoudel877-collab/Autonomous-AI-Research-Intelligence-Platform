from nexus.graph.model import Edge, Node

class GraphStore:
    def __init__(self): self.nodes={}; self.edges=[]
    def add_node(self,node:Node): self.nodes[node.id]=node
    def add_edge(self,edge:Edge): self.edges.append(edge)
    def neighbors(self,node_id): return [e.target for e in self.edges if e.source==node_id]
