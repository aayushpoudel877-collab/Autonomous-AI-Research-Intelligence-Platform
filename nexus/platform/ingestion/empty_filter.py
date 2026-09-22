def remove_empty(items:list[str])->list[str]:
    return [item for item in items if item and item.strip()]
