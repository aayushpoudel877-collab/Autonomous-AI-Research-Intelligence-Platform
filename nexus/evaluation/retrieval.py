def recall_at_k(relevant:set[str],retrieved:list[str],k:int)->float:
    return len(relevant & set(retrieved[:k]))/len(relevant) if relevant else 0.0
