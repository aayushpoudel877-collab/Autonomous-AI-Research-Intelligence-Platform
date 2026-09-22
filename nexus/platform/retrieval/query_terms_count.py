def count_terms(query:str)->int:
    return len(set(query.lower().split()))
