def rank_distance(first:list[str],second:list[str])->float:
    positions={item:i for i,item in enumerate(first)}
    distances=[abs(positions[item]-i) for i,item in enumerate(second) if item in positions]
    return sum(distances)/len(distances) if distances else float('inf')
