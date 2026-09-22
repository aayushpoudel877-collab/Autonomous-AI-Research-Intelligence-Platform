from nexus.retrieval.hybrid import lexical_score

def rerank(query, results):
    return sorted(results,key=lambda r: 0.7*r.score+0.3*lexical_score(query,r.text),reverse=True)
