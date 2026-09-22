from nexus.graph.extractor import EntityGraphExtractor

def test_graph_extracts_entities():
    nodes,edges=EntityGraphExtractor().extract('Python powers NEXUS Research.')
    assert len(nodes)>=2 and edges
