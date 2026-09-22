def direct_path(store, source, target):
    return any(edge.source == source and edge.target == target for edge in store.edges)
