def weighted_neighbors(store, node_id):
    return sorted(((edge.target, edge.weight) for edge in store.edges if edge.source == node_id), key=lambda item: -item[1])
