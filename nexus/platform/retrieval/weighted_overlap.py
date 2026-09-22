def weighted_overlap(query:set[str],text:set[str],weights:dict[str,float])->float:
    if not query:return 0.0
    return sum(weights.get(term,1.0) for term in query&text)/sum(weights.get(term,1.0) for term in query)
