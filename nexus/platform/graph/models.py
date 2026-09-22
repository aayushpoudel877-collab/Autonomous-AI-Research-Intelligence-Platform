from dataclasses import dataclass
@dataclass(frozen=True)
class Node:
    node_id:str
    label:str
    kind:str='entity'
@dataclass(frozen=True)
class Edge:
    source:str
    target:str
    relation:str
    weight:float=1.0