def relations(store, relation):
    return [edge for edge in store.edges if edge.relation == relation]
